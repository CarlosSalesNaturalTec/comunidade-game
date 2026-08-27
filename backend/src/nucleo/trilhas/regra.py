import uuid
from dataclasses import dataclass

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..coletas.modelo import DesafioDeColeta
from ..culminancias.modelo import Culminancia
from ..erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..poderes.modelo import NaturezaDoPoder, Poder
from ..pontuacao.regra import avaliar_niveis, missoes_concluidas_pelo_guerreiro
from ..tempo import agora
from .modelo import (
    Atividade,
    DesbloqueioDaMissao,
    EtapaDoCiclo,
    FormatoDeAtividade,
    InscricaoNaTrilha,
    Missao,
    ModalidadeDeAtividade,
    SituacaoDaTrilha,
    TipoDeDesafioDeDesbloqueio,
    Trilha,
)

TOTAL_DE_ALTERNATIVAS_DO_DESAFIO = 4


def conferir_posse_da_trilha(trilha: Trilha, persona: Persona) -> None:
    """Aceita o Mestre autor e o Admin; recusa qualquer outro Mestre com
    403, ainda que o papel dele permita escrever trilhas em geral
    (`RF-01-16`, PRD-01 §4, design — decisões). Aplicada depois da matriz —
    a rota que a matriz protege é do PRD-09.
    """
    if persona.papel == Papel.admin:
        return
    if trilha.autor_id != persona.id:
        raise PermissaoNegada(mensagem="Só o Mestre autor escreve na própria trilha.")


def conferir_autoria_estrita_da_trilha(trilha: Trilha, persona: Persona) -> None:
    """Só o Mestre autor — nem outro Mestre nem Admin publicam a trilha ou
    declaram a culminância dela; a publicação não passa por aprovação, e o
    Admin não edita a trilha de um Mestre (`RF-09-05`, `RF-09-29`, design —
    decisões 1).
    """
    if trilha.autor_id != persona.id:
        raise PermissaoNegada(mensagem="Só o Mestre autor executa esta operação na própria trilha.")


def _unir_em_portugues(itens: list[str]) -> str:
    if len(itens) == 1:
        return itens[0]
    return ", ".join(itens[:-1]) + " e " + itens[-1]


def _travas_de_publicacao_pendentes(sessao: Session, trilha: Trilha) -> list[str]:
    """As três travas do `RF-09-06`, `RF-09-07` e `RN-09-29` — sondagem
    declarada, ao menos um desafio de coleta em alguma missão da trilha
    (existência, não contagem — design — decisões 6) e culminância
    declarada. O lastro de recompensa de marco nunca entra aqui: é
    conferido na entrega, por `RN-09-27`.
    """
    pendentes = []

    tem_sondagem = (
        sessao.query(Missao).filter_by(trilha_id=trilha.id, e_sondagem=True).first() is not None
    )
    if not tem_sondagem:
        pendentes.append("a missão de sondagem")

    tem_desafio_de_coleta = (
        sessao.query(DesafioDeColeta)
        .join(Missao, DesafioDeColeta.missao_id == Missao.id)
        .filter(Missao.trilha_id == trilha.id)
        .first()
        is not None
    )
    if not tem_desafio_de_coleta:
        pendentes.append("o desafio de coleta de dados reais")

    tem_culminancia = sessao.query(Culminancia).filter_by(trilha_id=trilha.id).first() is not None
    if not tem_culminancia:
        pendentes.append("a culminância")

    return pendentes


def publicar_trilha(sessao: Session, trilha: Trilha | None, *, operador: Persona) -> Trilha:
    """Publica ou republica a pedido do Mestre autor, sem aprovação de
    Admin, a partir de `rascunho` ou `despublicada` — uma só rota para as
    duas origens (design — decisões 4). Confere as três travas juntas e
    nomeia **todas** as pendentes na recusa (`RF-09-05` a `RF-09-08`,
    `RF-09-82`, `RN-09-01`, design — decisões 5). A republicação limpa o
    motivo da despublicação (design — decisões 7).
    """
    if trilha is None:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")
    conferir_autoria_estrita_da_trilha(trilha, operador)
    if trilha.situacao == SituacaoDaTrilha.publicada:
        raise ErroDeValidacao(mensagem="Esta trilha já está publicada.", campo="situacao")

    pendentes = _travas_de_publicacao_pendentes(sessao, trilha)
    if pendentes:
        raise ErroDeValidacao(
            mensagem=f"Para publicar, ainda falta declarar: {_unir_em_portugues(pendentes)}."
        )

    trilha.situacao = SituacaoDaTrilha.publicada
    trilha.motivo_da_situacao = None
    trilha.autor_da_situacao_id = operador.id
    trilha.papel_do_autor_da_situacao = operador.papel.value
    trilha.situacao_alterada_em = agora()
    sessao.flush()
    return trilha


def despublicar_trilha(
    sessao: Session, trilha: Trilha | None, *, operador: Persona, motivo: str | None
) -> Trilha:
    """Só Admin despublica, sempre com motivo, e só trilha publicada
    (`RF-09-10`, `RF-09-11`). Não toca missão, atividade, resultado,
    presença nem pontuação: o percurso já realizado permanece íntegro.
    """
    if trilha is None:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin despublica trilha.")
    if not motivo or not motivo.strip():
        raise ErroDeValidacao(mensagem="Despublicação exige motivo.", campo="motivo")
    if trilha.situacao != SituacaoDaTrilha.publicada:
        raise ErroDeValidacao(
            mensagem="Só uma trilha publicada pode ser despublicada.", campo="situacao"
        )

    trilha.situacao = SituacaoDaTrilha.despublicada
    trilha.motivo_da_situacao = motivo
    trilha.autor_da_situacao_id = operador.id
    trilha.papel_do_autor_da_situacao = operador.papel.value
    trilha.situacao_alterada_em = agora()
    sessao.flush()
    return trilha


def criar_trilha(
    sessao: Session,
    *,
    autor: Persona,
    nome: str,
    objetivo: str,
    area_do_conhecimento: str,
    poder_id: uuid.UUID | None,
) -> Trilha:
    """Exige poder do catálogo, de natureza de Guerreiro(a) (`RF-01-20`,
    `RN-01-43`). Nasce sempre em rascunho — a publicação é do PRD-09.
    """
    if poder_id is None:
        raise ErroDeValidacao(mensagem="Trilha exige um poder do catálogo.", campo="poder_id")

    poder = sessao.get(Poder, poder_id)
    if poder is None:
        raise ErroDeValidacao(mensagem="Poder não encontrado no catálogo.", campo="poder_id")
    if poder.natureza != NaturezaDoPoder.de_guerreiro:
        raise ErroDeValidacao(
            mensagem="Trilha só se vincula a poder de Guerreiro(a); o Poder Sustentador "
            "é derivado do aporte.",
            campo="poder_id",
        )

    trilha = Trilha(
        nome=nome,
        objetivo=objetivo,
        area_do_conhecimento=area_do_conhecimento,
        poder_id=poder_id,
        situacao=SituacaoDaTrilha.rascunho,
        autor_id=autor.id,
        papel_do_autor=autor.papel.value,
    )
    sessao.add(trilha)
    sessao.flush()
    return trilha


def consultar_trilhas(sessao: Session, *, persona: Persona | None = None) -> list[Trilha]:
    """Bem comum da plataforma: sem parâmetro nem filtro de comunidade
    (`RN-01-42`). O rascunho só aparece ao Mestre autor e ao Admin
    (`RF-01-20`, `RF-09-04`); a listagem pública desta fatia é só esta
    função — a rota de consulta é do PRD-09/PRD-03.
    """
    consulta = sessao.query(Trilha)
    if persona is not None and persona.papel == Papel.admin:
        return consulta.all()
    if persona is not None:
        return consulta.filter(
            or_(Trilha.situacao == SituacaoDaTrilha.publicada, Trilha.autor_id == persona.id)
        ).all()
    return consulta.filter(Trilha.situacao == SituacaoDaTrilha.publicada).all()


def criar_missao(
    sessao: Session,
    *,
    operador: Persona,
    trilha: Trilha | None,
    titulo: str | None,
    posicao: int,
    nivel_de_dificuldade: int,
    obrigatoria: bool | None,
    etapa_do_ciclo: str | None,
    e_sondagem: bool = False,
    cadencia_de_retomada: list[int] | None = None,
) -> Missao:
    """A dificuldade é só o que o Mestre autor declara — nunca deriva da
    idade do Guerreiro(a) (documento 99 §6 invariante 2). A sondagem
    exige a primeira posição e admite no máximo uma por trilha
    (documento 99 §6 invariante 5); a trilha em rascunho pode não ter
    sondagem ainda — a trava de publicação é `RF-09-82`. A retomada é
    opcional na criação (`RF-09-83`); quem a declara depois é
    `declarar_cadencia_de_retomada`.
    """
    if trilha is None:
        raise ErroDeValidacao(mensagem="Missão exige uma trilha.", campo="trilha_id")
    conferir_posse_da_trilha(trilha, operador)
    if not titulo or not titulo.strip():
        raise ErroDeValidacao(mensagem="Missão exige um título.", campo="titulo")
    if obrigatoria is None:
        raise ErroDeValidacao(
            mensagem="Missão exige a declaração de obrigatória ou opcional.",
            campo="obrigatoria",
        )
    try:
        etapa_valida = EtapaDoCiclo(etapa_do_ciclo)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Etapa do ciclo fora dos valores previstos.", campo="etapa_do_ciclo"
        ) from exc

    if e_sondagem:
        if posicao != 1:
            raise ErroDeValidacao(
                mensagem="A missão de sondagem ocupa a primeira posição da trilha.",
                campo="e_sondagem",
            )
        ja_tem_sondagem = (
            sessao.query(Missao).filter_by(trilha_id=trilha.id, e_sondagem=True).first()
        )
        if ja_tem_sondagem is not None:
            raise ErroDeValidacao(
                mensagem="Esta trilha já tem uma missão de sondagem.", campo="e_sondagem"
            )

    missao = Missao(
        trilha_id=trilha.id,
        titulo=titulo,
        posicao=posicao,
        nivel_de_dificuldade=nivel_de_dificuldade,
        obrigatoria=obrigatoria,
        etapa_do_ciclo=etapa_valida,
        e_sondagem=e_sondagem,
        cadencia_de_retomada=cadencia_de_retomada,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(missao)
    sessao.flush()
    return missao


def declarar_cadencia_de_retomada(
    sessao: Session, *, operador: Persona, missao: Missao, cadencia_de_retomada: list[int] | None
) -> Missao:
    """A cadência declarada é sempre a do Mestre autor — o núcleo nunca a
    impõe (`RF-09-83`, `RF-09-101`). Declarar de novo substitui a anterior;
    `None` deixa a missão sem retomada.
    """
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    missao.cadencia_de_retomada = cadencia_de_retomada
    sessao.flush()
    return missao


def _normalizar_natureza(natureza: str) -> str:
    """Reduz variação de digitação na lista aberta (design — riscos); o
    catálogo sugerido de `RF-09-85` reduz mais quando o PRD-09 chegar."""
    return natureza.strip().lower()


def criar_atividade(
    sessao: Session,
    *,
    operador: Persona,
    missao: Missao | None,
    titulo: str | None,
    descricao: str | None = None,
    modalidade: str | None,
    formato: str | None,
    natureza: str | None,
    producao_esperada: str | None,
    aula_id: uuid.UUID | None = None,
) -> Atividade:
    """Sempre pertence a uma missão, com a escrita restrita ao Mestre autor
    da trilha e a Admin, pela mesma conferência de posse da trilha
    (`RF-01-20`, `RF-01-16`). Os três eixos combinam livremente; a natureza
    é lista aberta e a produção declarada é sempre exigida
    (documento 99 §6 invariante 19). O título é exigido — sem ele nenhuma
    tela lista a atividade; a descrição é opcional (`RF-09-69`, design —
    decisões 5).

    `aula_id` é o vínculo opcional com o encontro (documento 05 §4): só
    atividade de formato presencial o declara, e a aula precisa existir —
    as duas recusas respondem 422 (`RF-09-69`, `RF-09-73`).
    """
    if missao is None:
        raise ErroDeValidacao(mensagem="Atividade exige uma missão.", campo="missao_id")

    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    if not titulo or not titulo.strip():
        raise ErroDeValidacao(mensagem="Atividade exige um título.", campo="titulo")

    if not modalidade:
        raise ErroDeValidacao(mensagem="Atividade exige modalidade.", campo="modalidade")
    try:
        modalidade_valida = ModalidadeDeAtividade(modalidade)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Modalidade fora dos valores previstos.", campo="modalidade"
        ) from exc

    if not formato:
        raise ErroDeValidacao(mensagem="Atividade exige formato.", campo="formato")
    try:
        formato_valido = FormatoDeAtividade(formato)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Formato fora dos valores previstos.", campo="formato"
        ) from exc

    if not natureza or not natureza.strip():
        raise ErroDeValidacao(mensagem="Atividade exige natureza.", campo="natureza")

    if not producao_esperada or not producao_esperada.strip():
        raise ErroDeValidacao(
            mensagem="Atividade exige a declaração do que o Guerreiro(a) produz.",
            campo="producao_esperada",
        )

    if aula_id is not None:
        if formato_valido != FormatoDeAtividade.presencial:
            raise ErroDeValidacao(
                mensagem="Só atividade de formato presencial declara a aula do encontro.",
                campo="aula_id",
            )
        if sessao.get(Aula, aula_id) is None:
            raise ErroDeValidacao(mensagem="Aula não encontrada.", campo="aula_id")

    atividade = Atividade(
        missao_id=missao.id,
        titulo=titulo,
        descricao=descricao,
        modalidade=modalidade_valida,
        formato=formato_valido,
        natureza=_normalizar_natureza(natureza),
        producao_esperada=producao_esperada,
        aula_id=aula_id,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(atividade)
    sessao.flush()
    return atividade


def inscrever_na_trilha(
    sessao: Session, *, guerreiro: Persona, trilha: Trilha | None
) -> InscricaoNaTrilha:
    """Ato do próprio Guerreiro(a) em sessão — exige trilha publicada
    (`RF-05-09`, `RN-05-43`). Inscrever-se de novo na mesma trilha devolve
    a existente, sem gravar uma segunda (`RN-05-43`). Reavalia o nível 1
    logo em seguida, para o caso raro de já existir `Resultado` anterior à
    inscrição (documento 11 §6)."""
    if trilha is None:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")
    if trilha.situacao != SituacaoDaTrilha.publicada:
        raise ErroDeValidacao(
            mensagem="Só é possível se inscrever numa trilha publicada.", campo="trilha_id"
        )

    existente = (
        sessao.query(InscricaoNaTrilha)
        .filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id)
        .first()
    )
    if existente is not None:
        return existente

    inscricao = InscricaoNaTrilha(guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    sessao.add(inscricao)
    sessao.flush()
    avaliar_niveis(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    return inscricao


def consultar_inscricoes_do_guerreiro(
    sessao: Session, *, guerreiro_id: uuid.UUID
) -> list[InscricaoNaTrilha]:
    return sessao.query(InscricaoNaTrilha).filter_by(guerreiro_id=guerreiro_id).all()


def _conferir_inscricao(sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID) -> None:
    """Comum à submissão do desafio e à leitura do percurso: só quem está
    inscrito tem o que submeter ou ler (`RN-05-21`, documento 11 §2.2)."""
    inscrito = (
        sessao.query(InscricaoNaTrilha)
        .filter_by(guerreiro_id=guerreiro_id, trilha_id=trilha_id)
        .first()
        is not None
    )
    if not inscrito:
        raise ErroDeValidacao(
            mensagem="Esta operação exige inscrição na própria trilha.", campo="trilha_id"
        )


def declarar_desafio_de_desbloqueio(
    sessao: Session,
    *,
    operador: Persona,
    missao: Missao | None,
    tipo: str | None,
    enunciado: str | None,
    alternativas: list[str] | None = None,
    alternativa_correta: int | None = None,
) -> Missao:
    """Só o Mestre autor da trilha declara — declarar de novo substitui o
    anterior, como `declarar_cadencia_de_retomada` já faz (`RF-09-26`,
    `RF-09-117`, design — decisão 4). O quiz segue o mesmo formato de
    `quiz.modelo.PerguntaDeQuiz`: enunciado, quatro alternativas e a
    correta entre elas; o prático usa só o enunciado, como a descrição do
    que o Guerreiro(a) precisa cumprir. Missão sem desafio segue publicável
    — esta declaração nunca é trava de publicação.
    """
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    if not enunciado or not enunciado.strip():
        raise ErroDeValidacao(
            mensagem="Desafio de desbloqueio exige um enunciado.", campo="enunciado"
        )
    try:
        tipo_valido = TipoDeDesafioDeDesbloqueio(tipo)
    except (ValueError, TypeError) as exc:
        raise ErroDeValidacao(
            mensagem="Tipo de desafio fora dos valores previstos.", campo="tipo"
        ) from exc

    missao.tipo_do_desafio_de_desbloqueio = tipo_valido
    missao.desafio_de_desbloqueio_enunciado = enunciado
    if tipo_valido == TipoDeDesafioDeDesbloqueio.quiz:
        if not alternativas or len(alternativas) != TOTAL_DE_ALTERNATIVAS_DO_DESAFIO:
            raise ErroDeValidacao(
                mensagem="Desafio em forma de quiz exige quatro alternativas.",
                campo="alternativas",
            )
        if alternativa_correta is None or not (
            1 <= alternativa_correta <= TOTAL_DE_ALTERNATIVAS_DO_DESAFIO
        ):
            raise ErroDeValidacao(
                mensagem="Desafio em forma de quiz exige a alternativa correta.",
                campo="alternativa_correta",
            )
        (
            missao.desafio_de_desbloqueio_alternativa_1,
            missao.desafio_de_desbloqueio_alternativa_2,
            missao.desafio_de_desbloqueio_alternativa_3,
            missao.desafio_de_desbloqueio_alternativa_4,
        ) = alternativas
        missao.desafio_de_desbloqueio_alternativa_correta = alternativa_correta
    else:
        missao.desafio_de_desbloqueio_alternativa_1 = None
        missao.desafio_de_desbloqueio_alternativa_2 = None
        missao.desafio_de_desbloqueio_alternativa_3 = None
        missao.desafio_de_desbloqueio_alternativa_4 = None
        missao.desafio_de_desbloqueio_alternativa_correta = None

    sessao.flush()
    return missao


@dataclass
class ResultadoDaSubmissaoDoDesbloqueio:
    """`aprovado`: `True` desbloqueou na hora (quiz certo ou prático já
    julgado antes), `None` aguardando o Mestre julgar o prático, `False`
    não passou no quiz — nada gravado, submete de novo sem limite
    (`RN-05-20`)."""

    aprovado: bool | None
    desbloqueio: DesbloqueioDaMissao | None


def submeter_desafio_de_desbloqueio(
    sessao: Session,
    *,
    guerreiro: Persona,
    missao: Missao | None,
    alternativa_escolhida: int | None = None,
) -> ResultadoDaSubmissaoDoDesbloqueio:
    """Só o Guerreiro(a) inscrito na trilha submete — sem inscrição, 422
    (`RN-05-20`, `RN-05-06`, documento 11 §2.2). No quiz, o núcleo afere e
    grava o desbloqueio na mesma operação quando passa; não passando, nada
    é gravado. No prático, grava a declaração do Guerreiro(a), aguardando o
    Mestre autor julgar. Em nenhum dos dois casos o desbloqueio credita
    ponto (`RN-05-06`) — quem credita é sempre o Resultado.
    """
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    if missao.tipo_do_desafio_de_desbloqueio is None:
        raise ErroDeValidacao(
            mensagem="Esta missão não tem desafio de desbloqueio declarado.", campo="missao_id"
        )
    _conferir_inscricao(sessao, guerreiro_id=guerreiro.id, trilha_id=missao.trilha_id)

    existente = (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .first()
    )
    if existente is not None:
        return ResultadoDaSubmissaoDoDesbloqueio(aprovado=existente.aprovado, desbloqueio=existente)

    if missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.quiz:
        if alternativa_escolhida == missao.desafio_de_desbloqueio_alternativa_correta:
            desbloqueio = DesbloqueioDaMissao(
                guerreiro_id=guerreiro.id, missao_id=missao.id, aprovado=True
            )
            sessao.add(desbloqueio)
            sessao.flush()
            return ResultadoDaSubmissaoDoDesbloqueio(aprovado=True, desbloqueio=desbloqueio)
        return ResultadoDaSubmissaoDoDesbloqueio(aprovado=False, desbloqueio=None)

    desbloqueio = DesbloqueioDaMissao(guerreiro_id=guerreiro.id, missao_id=missao.id, aprovado=None)
    sessao.add(desbloqueio)
    sessao.flush()
    return ResultadoDaSubmissaoDoDesbloqueio(aprovado=None, desbloqueio=desbloqueio)


def listar_desbloqueios_praticos_pendentes(
    sessao: Session, *, operador: Persona
) -> list[DesbloqueioDaMissao]:
    """Declarações de desafio prático ainda não julgadas, só das trilhas do
    Mestre autor (`RF-09-26`, `RF-09-117`)."""
    return (
        sessao.query(DesbloqueioDaMissao)
        .join(Missao, Missao.id == DesbloqueioDaMissao.missao_id)
        .join(Trilha, Trilha.id == Missao.trilha_id)
        .filter(
            Trilha.autor_id == operador.id,
            Missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.pratico,
            DesbloqueioDaMissao.aprovado.is_(None),
        )
        .all()
    )


def julgar_desafio_pratico(
    sessao: Session, *, operador: Persona, desbloqueio: DesbloqueioDaMissao | None, aprovado: bool
) -> DesbloqueioDaMissao | None:
    """Só o Mestre autor da trilha julga (`RF-09-117`). Aprovado, a linha
    vira o desbloqueio de fato; reprovado, ela é apagada, para que o
    Guerreiro(a) declare de novo, sem limite e sem punição (`RN-05-20`) —
    nunca fica reprovação persistida."""
    if desbloqueio is None:
        raise NaoEncontrado(mensagem="Declaração de desafio prático não encontrada.")
    missao = sessao.get(Missao, desbloqueio.missao_id)
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)
    if desbloqueio.aprovado is not None:
        raise ErroDeValidacao(mensagem="Esta declaração já foi julgada.", campo="aprovado")

    if aprovado:
        desbloqueio.aprovado = True
        desbloqueio.julgado_por_id = operador.id
        sessao.flush()
        return desbloqueio

    sessao.delete(desbloqueio)
    sessao.flush()
    return None


@dataclass
class MissaoNoPercurso:
    missao: Missao
    desbloqueada: bool
    e_proxima: bool
    aguardando_mestre: bool
    motivo_do_bloqueio: str | None


def derivar_percurso(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID
) -> list[MissaoNoPercurso]:
    """Deriva o percurso na leitura, a partir da posição — sem tabela de
    estado por missão (design — decisão 2). Só o próprio Guerreiro(a)
    inscrito tem o que ler (`RF-05-08`, `RF-05-10`, `RN-05-21`)."""
    _conferir_inscricao(sessao, guerreiro_id=guerreiro_id, trilha_id=trilha_id)

    missoes = sessao.query(Missao).filter_by(trilha_id=trilha_id).order_by(Missao.posicao).all()
    desbloqueios = {
        d.missao_id: d
        for d in sessao.query(DesbloqueioDaMissao)
        .filter(
            DesbloqueioDaMissao.guerreiro_id == guerreiro_id,
            DesbloqueioDaMissao.missao_id.in_([missao.id for missao in missoes]),
        )
        .all()
    }
    proxima = next(
        (
            missao
            for missao in missoes
            if desbloqueios.get(missao.id) is None or desbloqueios[missao.id].aprovado is not True
        ),
        None,
    )

    resultado = []
    for missao in missoes:
        desbloqueio = desbloqueios.get(missao.id)
        desbloqueada = desbloqueio is not None and desbloqueio.aprovado is True
        aguardando_mestre = desbloqueio is not None and desbloqueio.aprovado is None
        e_proxima = proxima is not None and missao.id == proxima.id
        motivo = None
        if not desbloqueada and not e_proxima:
            motivo = f'Desbloqueie "{proxima.titulo}" primeiro.' if proxima is not None else None
        resultado.append(
            MissaoNoPercurso(
                missao=missao,
                desbloqueada=desbloqueada,
                e_proxima=e_proxima,
                aguardando_mestre=aguardando_mestre,
                motivo_do_bloqueio=motivo,
            )
        )
    return resultado


def obter_proxima_missao(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID
) -> Missao | None:
    """A próxima missão do percurso do Guerreiro(a) naquela trilha, para a
    listagem de `GET /v1/eu/trilhas` (`RF-05-08`, `RF-05-17`)."""
    percurso = derivar_percurso(sessao, guerreiro_id=guerreiro_id, trilha_id=trilha_id)
    proxima = next((item for item in percurso if item.e_proxima), None)
    return proxima.missao if proxima is not None else None


@dataclass
class ProgressoDaTrilha:
    trilha: Trilha
    nivel_atual: int | None
    obrigatorias_desbloqueadas: int
    obrigatorias_totais: int
    pontos_regulares: int
    badges: list[str]


def consultar_progresso(sessao: Session, *, guerreiro_id: uuid.UUID) -> list[ProgressoDaTrilha]:
    """Por trilha inscrita: nível certificado, quantas obrigatórias faltam
    para o próximo, pontos e badges — reaproveita `missoes_concluidas_
    pelo_guerreiro`, `Nivel`, `PontoRegular` e `Badge`, sem recalcular nada
    por conta própria (`RF-05-15`, `RF-05-16`, `RN-05-03`, `RN-05-04`,
    design — decisão 7). As recompensas conquistadas continuam só em
    `GET /v1/eu/recompensas`, que já as serve."""
    from ..pontuacao.modelo import Badge, Nivel, PontoRegular

    resultado = []
    for inscricao in consultar_inscricoes_do_guerreiro(sessao, guerreiro_id=guerreiro_id):
        trilha = sessao.get(Trilha, inscricao.trilha_id)
        obrigatorias = sessao.query(Missao).filter_by(trilha_id=trilha.id, obrigatoria=True).all()
        concluidas = missoes_concluidas_pelo_guerreiro(
            sessao, guerreiro_id=guerreiro_id, trilha_id=trilha.id
        )
        ids_obrigatorias = {missao.id for missao in obrigatorias}
        nivel_atual = (
            sessao.query(Nivel.valor)
            .filter_by(guerreiro_id=guerreiro_id, trilha_id=trilha.id)
            .order_by(Nivel.valor.desc())
            .limit(1)
            .scalar()
        )
        conta_de_pontos = (
            sessao.query(PontoRegular)
            .filter_by(guerreiro_id=guerreiro_id, trilha_id=trilha.id)
            .first()
        )
        badges = (
            sessao.query(Badge.tipo).filter_by(guerreiro_id=guerreiro_id, trilha_id=trilha.id).all()
        )
        resultado.append(
            ProgressoDaTrilha(
                trilha=trilha,
                nivel_atual=nivel_atual,
                obrigatorias_desbloqueadas=len(concluidas & ids_obrigatorias),
                obrigatorias_totais=len(obrigatorias),
                pontos_regulares=conta_de_pontos.total if conta_de_pontos is not None else 0,
                badges=[badge.tipo.value for badge in badges],
            )
        )
    return resultado
