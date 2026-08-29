from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..comunidades.regra import abrir_vinculo
from ..erros import ErroDeValidacao, PermissaoNegada
from ..fila.modelo import SolicitacaoDeParticipacao
from ..tempo import agora
from .modelo import ArtefatoComprobatorio, Credencial, Nick, Papel, Persona, TipoDeCredencial

# Mesma mensagem nos dois pontos de gravação que a aplicam (`criar_persona` e
# `definir_ou_trocar_nick`) — a rota do cadastro do encontro reconhece a
# recusa por esta mensagem para anexar as variações de alcance total
# (`RF-04-08`, design — decisão 4).
MENSAGEM_NICK_EM_USO = "Este nick já está em uso."

# Quem cadastra quem (RN-01-01, RN-01-02). Guerreiro(a) tem autocadastro:
# frozenset vazio significa "nenhum autor exigido".
_PAPEIS_QUE_CADASTRAM: dict[Papel, frozenset[Papel]] = {
    Papel.guerreiro: frozenset(),
    Papel.mestre: frozenset({Papel.admin}),
    Papel.apoiador: frozenset({Papel.admin}),
    Papel.responsavel: frozenset({Papel.admin, Papel.mestre}),
    Papel.admin: frozenset({Papel.admin}),
}


def criar_persona(
    sessao: Session,
    *,
    papel: Papel | None,
    criada_por: Persona | None,
    aula: Aula | None = None,
    nick: str | None = None,
    nome: str | None = None,
    nascimento: date | None = None,
    email: str | None = None,
    whatsapp: str | None = None,
    avatar: str | None = None,
    permitir_semeadura_de_admin: bool = False,
) -> Persona:
    """Cria a persona aplicando RN-01-01, RN-01-02 e RN-01-05. Login nunca
    chama esta função (`RN-01-04`) — quem chama é quem cadastra: Admin,
    Mestre ou, no caso do Guerreiro(a), o próprio autocadastro.

    O nick é exigido só do Guerreiro(a) (`RF-01-19`); Apoiador e Mestre podem
    nascer sem ele e recebê-lo depois (`RN-14-10`). A unicidade — insensível
    a caixa, alcançando qualquer papel — é conferida antes de qualquer
    gravação, para que a recusa nunca deixe persona nem nick a meio caminho,
    e sem revelar de quem é o nick em uso (`RN-01-30`). A comunidade do
    Guerreiro(a) nunca é parâmetro desta função: ela vem só da `aula`
    agendada em que ele se cadastra, nunca de quem cadastra (`RF-08-02`,
    `RN-08-02`, PRD-08).
    """
    if papel is None:
        raise ErroDeValidacao(mensagem="Toda persona precisa declarar o papel.", campo="papel")

    autores_exigidos = _PAPEIS_QUE_CADASTRAM[papel]
    eh_semeadura_de_admin = permitir_semeadura_de_admin and papel == Papel.admin
    if autores_exigidos and not eh_semeadura_de_admin:
        if criada_por is None or criada_por.papel not in autores_exigidos:
            raise PermissaoNegada(
                mensagem=f"Persona de {papel.value} só é cadastrada por quem tem autoridade "
                "para isso."
            )

    if papel == Papel.guerreiro and aula is None:
        raise ErroDeValidacao(
            mensagem="Guerreiro(a) precisa de uma aula agendada que origine o vínculo de "
            "comunidade.",
            campo="aula_id",
        )

    if papel == Papel.guerreiro and (not nick or not nick.strip()):
        raise ErroDeValidacao(mensagem="Guerreiro(a) precisa de nick.", campo="nick")

    if nick is not None and _nick_em_uso(sessao, nick):
        raise ErroDeValidacao(mensagem=MENSAGEM_NICK_EM_USO, campo="nick")

    persona = Persona(
        papel=papel,
        nome=nome,
        nascimento=nascimento,
        email=email,
        whatsapp=whatsapp,
        avatar=avatar,
        criada_por=criada_por.id if criada_por is not None else None,
    )
    sessao.add(persona)
    sessao.flush()

    if nick is not None:
        sessao.add(Nick(persona_id=persona.id, valor=nick))
        sessao.flush()

    if papel == Papel.guerreiro:
        abrir_vinculo(sessao, guerreiro=persona, comunidade_id=aula.comunidade_virtual_id)

    return persona


def _nick_em_uso(sessao: Session, nick: str) -> bool:
    """Unicidade global insensível a caixa, contra qualquer papel
    (`RN-01-30`) — a mesma comparação que o índice `uq_nick_valor` aplica no
    banco, feita aqui para que a recusa vire 422 em vez de erro de
    integridade."""
    return (
        sessao.query(Nick).filter(func.lower(Nick.valor) == nick.strip().lower()).first()
        is not None
    )


def buscar_guerreiro_por_nick(sessao: Session, nick: str) -> Persona | None:
    """Resolução interna, nunca exposta como busca: correspondência exata
    insensível a caixa, restrita a `Papel.guerreiro`. É o único uso
    autorizado de nick de Guerreiro(a) fora da abertura de sessão por
    biometria — a confirmação humana o consome sem devolver identificador
    algum a quem chamou (`RN-01-22`, openspec —
    esqueleto-da-aula-presencial-e-equipe-da-aula, design — decisão 1.1)."""
    return (
        sessao.query(Persona)
        .join(Nick, Nick.persona_id == Persona.id)
        .filter(func.lower(Nick.valor) == nick.strip().lower(), Persona.papel == Papel.guerreiro)
        .first()
    )


_PAPEIS_DE_ADULTO = (Papel.apoiador, Papel.mestre)

_QUANTIDADE_DE_SUGESTOES_DE_VARIACAO = 3


def conferir_disponibilidade_de_nick(sessao: Session, nick: str) -> bool:
    """Conferência restrita a nicks de adulto — Apoiador e Mestre —, mais os
    reservados por solicitação de participação ainda dentro do prazo. NEVER
    compara com nick de Guerreiro(a): é a restrição de alcance que evita o
    oráculo que `RN-01-22` e `RN-14-23` vedam — nick de Guerreiro(a) sempre
    sai como disponível. Conveniência da tela, não substitui a unicidade
    apurada em `criar_persona` e `definir_ou_trocar_nick` na gravação
    (`RF-14-13`, `RN-01-22`, `RN-14-23`, `RN-01-28`).
    """
    nick_normalizado = nick.strip().lower()

    em_uso_por_adulto = (
        sessao.query(Nick)
        .join(Persona, Persona.id == Nick.persona_id)
        .filter(Persona.papel.in_(_PAPEIS_DE_ADULTO))
        .filter(func.lower(Nick.valor) == nick_normalizado)
        .first()
        is not None
    )
    if em_uso_por_adulto:
        return False

    reservado = (
        sessao.query(SolicitacaoDeParticipacao)
        .filter(
            func.lower(SolicitacaoDeParticipacao.nick) == nick_normalizado,
            SolicitacaoDeParticipacao.decidido_em.is_(None),
            SolicitacaoDeParticipacao.prazo >= agora(),
        )
        .first()
        is not None
    )
    return not reservado


def sugerir_variacoes_de_nick(sessao: Session, nick: str) -> list[str]:
    """Variações do nick indisponível, cada uma passada pela mesma
    conferência restrita a adulto — nunca sugere nick já usado por Apoiador
    ou Mestre. Pode sugerir variação já usada por um Guerreiro(a), porque a
    conferência não a enxerga; a colisão que daí resulte é resolvida na
    gravação (`RF-14-13`, `RN-01-22`).
    """
    sugestoes: list[str] = []
    for sufixo in range(2, 100):
        if len(sugestoes) == _QUANTIDADE_DE_SUGESTOES_DE_VARIACAO:
            break
        candidata = f"{nick.strip()}{sufixo}"
        if conferir_disponibilidade_de_nick(sessao, candidata):
            sugestoes.append(candidata)
    return sugestoes


def definir_ou_trocar_nick(sessao: Session, persona: Persona, nick: str) -> Persona:
    """O adulto — Apoiador ou Mestre — em sessão define, se ainda não tem, ou
    troca o próprio nick. Aplica a mesma unicidade global de `criar_persona`
    (`RF-14-12`, `RN-14-10`, `RN-01-30`, PRD-01 §9)."""
    if not nick or not nick.strip():
        raise ErroDeValidacao(mensagem="Nick é obrigatório.", campo="nick")

    if _nick_em_uso(sessao, nick):
        raise ErroDeValidacao(mensagem=MENSAGEM_NICK_EM_USO, campo="nick")

    registro = sessao.query(Nick).filter_by(persona_id=persona.id).first()
    if registro is None:
        sessao.add(Nick(persona_id=persona.id, valor=nick))
    else:
        registro.valor = nick
    sessao.flush()
    return persona


def conferir_disponibilidade_de_nick_com_alcance_total(sessao: Session, nick: str) -> bool:
    """Mesma forma de `conferir_disponibilidade_de_nick`, mas contra
    **qualquer** papel, inclusive Guerreiro(a). Segunda exceção declarada do
    requisito "o núcleo nunca descobre nem sugere um nick": só é chamada pela
    montagem da recusa de gravação do cadastro do encontro, nunca por rota de
    consulta (`RN-01-22`, `RF-04-08`, design — decisão 4).
    """
    return not _nick_em_uso(sessao, nick)


def sugerir_variacoes_de_nick_com_alcance_total(sessao: Session, nick: str) -> list[str]:
    """Variações do nick recusado no cadastro do encontro, cada uma conferida
    com alcance total — nunca sugere nick já usado por qualquer papel
    (`RF-04-08`, design — decisão 4)."""
    sugestoes: list[str] = []
    for sufixo in range(2, 100):
        if len(sugestoes) == _QUANTIDADE_DE_SUGESTOES_DE_VARIACAO:
            break
        candidata = f"{nick.strip()}{sufixo}"
        if conferir_disponibilidade_de_nick_com_alcance_total(sessao, candidata):
            sugestoes.append(candidata)
    return sugestoes


# `RF-02-04`, `RN-02-01`: artefato comprobatório obrigatório só para Mestre e
# Apoiador — o Admin não declara prova nenhuma para incluir outro Admin.
_PAPEIS_QUE_EXIGEM_ARTEFATO = (Papel.mestre, Papel.apoiador)


def _gravar_credencial_de_login_social(
    sessao: Session, *, persona: Persona, email: str, criada_por: Persona
) -> None:
    """O e-mail declarado no cadastro é o identificador que a rota de login
    social já procura (`sessoes.rotas.login_social`, `personas.semeadura`) —
    sem esta credencial, o adulto cadastrado nunca conseguiria entrar pela
    conta Google (documento 03 §1.1)."""
    sessao.add(
        Credencial(
            persona_id=persona.id,
            tipo=TipoDeCredencial.login_social,
            identificador=email,
            criada_por=criada_por.id,
            troca_pendente=False,
            ativa=True,
        )
    )


_IDADE_MINIMA_DO_GUERREIRO = 6
_IDADE_MAXIMA_DO_GUERREIRO = 16


def _idade_em(nascimento: date, referencia: date) -> int:
    idade = referencia.year - nascimento.year
    if (referencia.month, referencia.day) < (nascimento.month, nascimento.day):
        idade -= 1
    return idade


def _validar_dados_comuns_do_guerreiro(
    *, nome: str | None, nascimento: date | None, avatar: str | None
) -> None:
    """Nome, nascimento, avatar e a faixa de 6 a 16 anos — comuns aos dois
    caminhos de cadastro de Guerreiro(a), gestão e encontro, para que a
    faixa exista num só lugar e alcance os dois (`RN-04-11`, documento 99
    §6 invariante 2, design — decisão 2 e 3).
    """
    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem="Guerreiro(a) precisa de nome.", campo="nome")
    if nascimento is None:
        raise ErroDeValidacao(
            mensagem="Guerreiro(a) precisa de data de nascimento.", campo="nascimento"
        )
    if not avatar or not avatar.strip():
        raise ErroDeValidacao(mensagem="Guerreiro(a) precisa de avatar.", campo="avatar")

    idade = _idade_em(nascimento, agora().date())
    if idade < _IDADE_MINIMA_DO_GUERREIRO or idade > _IDADE_MAXIMA_DO_GUERREIRO:
        raise ErroDeValidacao(
            mensagem="Guerreiro(a) precisa ter entre 6 e 16 anos.", campo="nascimento"
        )


def cadastrar_guerreiro_pela_gestao(
    sessao: Session,
    *,
    operador: Persona,
    nome: str | None,
    nascimento: date | None,
    nick: str | None,
    avatar: str | None,
    aula: Aula,
) -> Persona:
    """`RF-02-01`: cadastro do Guerreiro(a) pelo Admin. A comunidade vem da
    aula agendada em que ele se cadastra, nunca de quem o cadastra — a
    mesma regra do autocadastro do PRD-04, aplicada aqui ao caminho da
    gestão (`RF-08-02`, `RN-08-02`). `criar_persona` não restringe autor
    algum para Guerreiro(a) — o autocadastro do PRD-04 não tem um —, então
    é aqui que o caminho da gestão exige Admin.
    """
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin cadastra Guerreiro(a) pela gestão.")
    _validar_dados_comuns_do_guerreiro(nome=nome, nascimento=nascimento, avatar=avatar)

    return criar_persona(
        sessao,
        papel=Papel.guerreiro,
        criada_por=operador,
        aula=aula,
        nick=nick,
        nome=nome,
        nascimento=nascimento,
        avatar=avatar,
    )


def cadastrar_guerreiro_no_encontro(
    sessao: Session,
    *,
    nome: str | None,
    nascimento: date | None,
    nick: str | None,
    avatar: str | None,
    aula: Aula,
) -> Persona:
    """`RF-04-07`, `RF-04-10`, `RN-04-04`: autocadastro do Guerreiro(a) no
    encontro. A sessão de trabalho do aparelho, aberta por Mestre ou Admin,
    autentica esta escrita — a rota exige a operação da matriz para isso —
    sem se tornar autora dela: por isso, ao contrário do caminho da gestão,
    esta função **não** recebe operador algum, e `criar_persona` grava a
    persona sem criador (invariante 3 do documento 99 §6).
    """
    _validar_dados_comuns_do_guerreiro(nome=nome, nascimento=nascimento, avatar=avatar)

    return criar_persona(
        sessao,
        papel=Papel.guerreiro,
        criada_por=None,
        aula=aula,
        nick=nick,
        nome=nome,
        nascimento=nascimento,
        avatar=avatar,
    )


def editar_guerreiro(
    sessao: Session,
    persona: Persona,
    *,
    nome: str | None,
    nascimento: date | None,
    nick: str | None,
    avatar: str | None,
) -> Persona:
    """`RF-02-01`: mesmas recusas do cadastro. NEVER apaga a persona nem
    troca o papel dela — só atualiza os quatro campos (`RN-02-21`)."""
    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem="Guerreiro(a) precisa de nome.", campo="nome")
    if nascimento is None:
        raise ErroDeValidacao(
            mensagem="Guerreiro(a) precisa de data de nascimento.", campo="nascimento"
        )
    if not avatar or not avatar.strip():
        raise ErroDeValidacao(mensagem="Guerreiro(a) precisa de avatar.", campo="avatar")
    if not nick or not nick.strip():
        raise ErroDeValidacao(mensagem="Guerreiro(a) precisa de nick.", campo="nick")

    # Exclui a própria persona da checagem: reenviar o nick que ela já tem
    # não pode se confundir com colisão (RN-01-30 conta contra QUALQUER
    # outra persona, nunca contra ela mesma).
    nick_normalizado = nick.strip().lower()
    em_uso_por_outra_persona = (
        sessao.query(Nick)
        .filter(func.lower(Nick.valor) == nick_normalizado, Nick.persona_id != persona.id)
        .first()
        is not None
    )
    if em_uso_por_outra_persona:
        raise ErroDeValidacao(mensagem="Este nick já está em uso.", campo="nick")

    registro_de_nick = sessao.query(Nick).filter_by(persona_id=persona.id).first()
    if registro_de_nick is None:
        sessao.add(Nick(persona_id=persona.id, valor=nick))
    else:
        registro_de_nick.valor = nick

    persona.nome = nome
    persona.nascimento = nascimento
    persona.avatar = avatar
    sessao.flush()
    return persona


def cadastrar_adulto_com_artefatos(
    sessao: Session,
    *,
    papel: Papel,
    operador: Persona,
    nome: str | None,
    email: str | None,
    whatsapp: str | None,
    nick: str | None,
    artefatos: list[tuple[str, str]],
) -> Persona:
    """`RF-02-02`, `RF-02-03`: cadastro de Mestre ou de Apoiador, com o
    artefato comprobatório obrigatório (`RF-02-04`, `RN-02-01`) — a prova é
    link declarado, nunca anexo de arquivo. O nick não é exigido aqui: o do
    Apoiador vem do pré-cadastro e o do Mestre é definido por ele no
    primeiro acesso."""
    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem=f"{papel.value.capitalize()} precisa de nome.", campo="nome")
    if not email or not email.strip():
        raise ErroDeValidacao(
            mensagem=f"{papel.value.capitalize()} precisa de e-mail.", campo="email"
        )
    if papel in _PAPEIS_QUE_EXIGEM_ARTEFATO and not artefatos:
        raise ErroDeValidacao(
            mensagem="O cadastro exige ao menos um artefato comprobatório.", campo="artefatos"
        )

    persona = criar_persona(
        sessao,
        papel=papel,
        criada_por=operador,
        nick=nick,
        nome=nome,
        email=email,
        whatsapp=whatsapp,
    )

    for endereco, rotulo in artefatos:
        sessao.add(
            ArtefatoComprobatorio(
                persona_id=persona.id,
                endereco=endereco,
                rotulo=rotulo,
                declarado_por_id=operador.id,
            )
        )

    _gravar_credencial_de_login_social(sessao, persona=persona, email=email, criada_por=operador)
    sessao.flush()
    return persona


def incluir_admin(
    sessao: Session,
    *,
    operador: Persona,
    nome: str | None,
    email: str | None,
    whatsapp: str | None,
) -> Persona:
    """`RF-02-05`, `RN-02-02`: único caminho de entrada de um Admin novo —
    `criar_persona` já recusa quem não é Admin (`criada_por`)."""
    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem="Admin precisa de nome.", campo="nome")
    if not email or not email.strip():
        raise ErroDeValidacao(mensagem="Admin precisa de e-mail.", campo="email")

    persona = criar_persona(
        sessao, papel=Papel.admin, criada_por=operador, nome=nome, email=email, whatsapp=whatsapp
    )
    _gravar_credencial_de_login_social(sessao, persona=persona, email=email, criada_por=operador)
    sessao.flush()
    return persona
