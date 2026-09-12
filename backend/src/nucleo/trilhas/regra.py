import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..armazenamento.porta import PortaDeArmazenamento
from ..aulas.modelo import Aula
from ..coletas.modelo import DesafioDeColeta
from ..culminancias.modelo import Culminancia
from ..erros import ArquivoAcimaDoTeto, ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..poderes.modelo import NaturezaDoPoder, Poder
from ..pontuacao.regra import avaliar_niveis, missoes_concluidas_pelo_guerreiro
from ..tempo import agora
from .modelo import (
    PRIMEIRA_ALTERNATIVA_DO_DESBLOQUEIO,
    TOTAL_DE_ALTERNATIVAS_DO_DESBLOQUEIO,
    Atividade,
    DesbloqueioDaMissao,
    EtapaDoCiclo,
    FormatoDeAtividade,
    InscricaoNaTrilha,
    Missao,
    ModalidadeDeAtividade,
    PerguntaDoDesbloqueio,
    RespostaDaSubmissao,
    SituacaoDaTrilha,
    SubmissaoDoDesbloqueio,
    TipoDeDesafioDeDesbloqueio,
    Trilha,
)

# Passa quem acerta ao menos 60% das perguntas do quiz (`RN-05-45`,
# documento 11 §2.2). Em inteiro, para não depender de ponto flutuante:
# 3 de 5 passa, 2 de 3 passa, 1 de 2 não passa (design — decisão 3).
NUMERADOR_DO_CORTE_DO_QUIZ = 6
DENOMINADOR_DO_CORTE_DO_QUIZ = 10


def _passou_no_quiz(acertos: int, total: int) -> bool:
    return acertos * DENOMINADOR_DO_CORTE_DO_QUIZ >= total * NUMERADOR_DO_CORTE_DO_QUIZ


def perguntas_do_desbloqueio(
    sessao: Session, *, missao_id: uuid.UUID
) -> list[PerguntaDoDesbloqueio]:
    """As perguntas **vigentes** do quiz, na ordem declarada pelo Mestre
    autor (`RF-09-118`). Acessor único: a pergunta substituída permanece
    guardada, para a submissão que a aponta, e sai de toda leitura do
    desafio por este filtro (`RN-05-47`, design — decisão 4)."""
    return (
        sessao.query(PerguntaDoDesbloqueio)
        .filter(
            PerguntaDoDesbloqueio.missao_id == missao_id,
            PerguntaDoDesbloqueio.substituida_em.is_(None),
        )
        .order_by(PerguntaDoDesbloqueio.ordem)
        .all()
    )


def perguntas_do_desbloqueio_por_missao(
    sessao: Session, *, missao_ids: list[uuid.UUID]
) -> dict[uuid.UUID, list[PerguntaDoDesbloqueio]]:
    """As perguntas vigentes de **várias** missões de uma vez, agrupadas por
    missão — o mesmo filtro e a mesma ordem de `perguntas_do_desbloqueio`,
    para que não haja duas noções de pergunta vigente. A leitura das trilhas
    do Mestre percorre todas as missões de cada trilha: uma consulta por
    missão multiplicaria as idas ao banco pelo tamanho da trilha (design —
    decisão 3)."""
    if not missao_ids:
        return {}
    perguntas = (
        sessao.query(PerguntaDoDesbloqueio)
        .filter(
            PerguntaDoDesbloqueio.missao_id.in_(missao_ids),
            PerguntaDoDesbloqueio.substituida_em.is_(None),
        )
        .order_by(PerguntaDoDesbloqueio.ordem)
        .all()
    )
    agrupadas: dict[uuid.UUID, list[PerguntaDoDesbloqueio]] = {}
    for pergunta in perguntas:
        agrupadas.setdefault(pergunta.missao_id, []).append(pergunta)
    return agrupadas


def referencia_da_imagem_da_pergunta(pergunta: PerguntaDoDesbloqueio) -> str:
    """A referência nasce do id da pergunta que existia no momento do envio
    e **nunca se renomeia**: substituída a pergunta, a linha nova recebe a
    mesma string e o objeto continua onde está (design — decisão 2)."""
    return f"perguntas-do-desbloqueio/{pergunta.id}/imagem"


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


def missoes_desbloqueadas_pelo_guerreiro(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID
) -> set[uuid.UUID]:
    """As missões da trilha que o Guerreiro(a) já **desbloqueou** — o marco
    alcançado que `recompensas_de_marco.regra` verifica, e não mais a
    existência de `Resultado` numa atividade (`RF-09-84`, documento 03 §11,
    documento 11 §2.2, design — decisão 6). Desafio prático ainda não
    julgado (`aprovado is None`) não conta: enquanto o Mestre não julga, a
    missão aguarda. `missoes_concluidas_pelo_guerreiro` permanece em
    `pontuacao.regra`, a serviço só do motor de níveis, que continua
    contando por `Resultado`."""
    linhas = (
        sessao.query(Missao.id)
        .join(DesbloqueioDaMissao, DesbloqueioDaMissao.missao_id == Missao.id)
        .filter(
            Missao.trilha_id == trilha_id,
            DesbloqueioDaMissao.guerreiro_id == guerreiro_id,
            DesbloqueioDaMissao.aprovado.is_(True),
        )
        .distinct()
        .all()
    )
    return {linha[0] for linha in linhas}


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


def duplicar_trilha(
    sessao: Session, trilha_de_origem: Trilha | None, *, operador: Persona
) -> Trilha:
    """Duplica a trilha do catálogo como ponto de partida de outra — bem
    comum sob CC BY-SA, então a autoria da cópia é sempre de quem duplicou,
    mesmo que a origem seja de outro Mestre (`RF-09-13`, documento 03 §11,
    design — decisão 8).

    Copia missões e atividades; nunca inscrição, desbloqueio, resultado,
    criação original, recompensa de marco, entrega, desafio de coleta,
    conteúdo, bibliografia, culminância, etiqueta ou auditoria — tudo o que
    é fato de pessoa ou lastro da origem fica com ela. `aula_id` da
    atividade também não é copiado: é vínculo do encontro da origem, não da
    cópia. A origem nunca é alterada.
    """
    if trilha_de_origem is None:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")
    if operador.papel != Papel.mestre:
        raise PermissaoNegada(mensagem="Só o Mestre duplica trilha do catálogo.")
    if (
        trilha_de_origem.situacao == SituacaoDaTrilha.rascunho
        and trilha_de_origem.autor_id != operador.id
    ):
        raise PermissaoNegada(mensagem="Rascunho de outro Mestre não pode ser duplicado.")

    copia = Trilha(
        nome=f"{trilha_de_origem.nome} (cópia)",
        objetivo=trilha_de_origem.objetivo,
        area_do_conhecimento=trilha_de_origem.area_do_conhecimento,
        poder_id=trilha_de_origem.poder_id,
        situacao=SituacaoDaTrilha.rascunho,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(copia)
    sessao.flush()

    missoes_da_origem = (
        sessao.query(Missao).filter_by(trilha_id=trilha_de_origem.id).order_by(Missao.posicao).all()
    )
    for missao_de_origem in missoes_da_origem:
        missao_copiada = Missao(
            trilha_id=copia.id,
            titulo=missao_de_origem.titulo,
            posicao=missao_de_origem.posicao,
            nivel_de_dificuldade=missao_de_origem.nivel_de_dificuldade,
            obrigatoria=missao_de_origem.obrigatoria,
            e_sondagem=missao_de_origem.e_sondagem,
            etapa_do_ciclo=missao_de_origem.etapa_do_ciclo,
            cadencia_de_retomada=missao_de_origem.cadencia_de_retomada,
            tipo_do_desafio_de_desbloqueio=missao_de_origem.tipo_do_desafio_de_desbloqueio,
            desafio_de_desbloqueio_enunciado=missao_de_origem.desafio_de_desbloqueio_enunciado,
            autor_id=operador.id,
            papel_do_autor=operador.papel.value,
        )
        sessao.add(missao_copiada)
        sessao.flush()

        for pergunta_de_origem in perguntas_do_desbloqueio(sessao, missao_id=missao_de_origem.id):
            sessao.add(
                PerguntaDoDesbloqueio(
                    missao_id=missao_copiada.id,
                    ordem=pergunta_de_origem.ordem,
                    enunciado=pergunta_de_origem.enunciado,
                    alternativa_1=pergunta_de_origem.alternativa_1,
                    alternativa_2=pergunta_de_origem.alternativa_2,
                    alternativa_3=pergunta_de_origem.alternativa_3,
                    alternativa_4=pergunta_de_origem.alternativa_4,
                    alternativa_correta=pergunta_de_origem.alternativa_correta,
                    # A cópia aponta a **mesma** referência, sem copiar
                    # bytes: imagem de trilha é bem comum como a trilha
                    # (`RF-09-13`, `RF-09-119`).
                    imagem_referencia=pergunta_de_origem.imagem_referencia,
                    imagem_tipo=pergunta_de_origem.imagem_tipo,
                    imagem_tamanho=pergunta_de_origem.imagem_tamanho,
                )
            )

        atividades_da_origem = (
            sessao.query(Atividade).filter_by(missao_id=missao_de_origem.id).all()
        )
        for atividade_de_origem in atividades_da_origem:
            sessao.add(
                Atividade(
                    missao_id=missao_copiada.id,
                    titulo=atividade_de_origem.titulo,
                    descricao=atividade_de_origem.descricao,
                    modalidade=atividade_de_origem.modalidade,
                    formato=atividade_de_origem.formato,
                    natureza=atividade_de_origem.natureza,
                    producao_esperada=atividade_de_origem.producao_esperada,
                    aula_id=None,
                    autor_id=operador.id,
                    papel_do_autor=operador.papel.value,
                )
            )

    sessao.flush()
    return copia


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
    enunciado: str | None = None,
    perguntas: list[dict] | None = None,
) -> Missao:
    """Só o Mestre autor da trilha declara — declarar de novo substitui o
    anterior, com as perguntas dele, como `declarar_cadencia_de_retomada` já
    faz (`RF-09-26`, `RF-09-117`, `RF-09-118`). O **quiz** traz uma ou mais
    perguntas, cada uma com enunciado, quatro alternativas e a correta entre
    elas; quiz sem nenhuma pergunta é recusado (`RN-09-43`). O **prático**
    usa só o enunciado, como a descrição do que o Guerreiro(a) precisa
    cumprir. Missão sem desafio segue publicável — esta declaração nunca é
    trava de publicação.
    """
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    try:
        tipo_valido = TipoDeDesafioDeDesbloqueio(tipo)
    except (ValueError, TypeError) as exc:
        raise ErroDeValidacao(
            mensagem="Tipo de desafio fora dos valores previstos.", campo="tipo"
        ) from exc

    if tipo_valido == TipoDeDesafioDeDesbloqueio.quiz:
        perguntas_validas = _conferir_perguntas_do_quiz(perguntas)
    elif not enunciado or not enunciado.strip():
        raise ErroDeValidacao(mensagem="Desafio prático exige um enunciado.", campo="enunciado")

    vigentes = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    imagens = _conferir_imagens_declaradas(
        perguntas_validas if tipo_valido == TipoDeDesafioDeDesbloqueio.quiz else [], vigentes
    )

    # Redeclarar substitui, mas nunca apaga: a pergunta anterior é
    # **carimbada** e sai da leitura, de modo que a submissão já gravada
    # siga apontando o que o Guerreiro(a) respondeu (`RN-05-47`, design —
    # decisão 4). O carimbo precede a gravação das novas, para que o índice
    # parcial de (missão, ordem) nunca veja duas gerações vigentes.
    momento = agora()
    for pergunta in vigentes:
        pergunta.substituida_em = momento
    sessao.flush()

    missao.tipo_do_desafio_de_desbloqueio = tipo_valido
    if tipo_valido == TipoDeDesafioDeDesbloqueio.quiz:
        missao.desafio_de_desbloqueio_enunciado = None
        for ordem, (pergunta, imagem) in enumerate(
            zip(perguntas_validas, imagens, strict=True), start=1
        ):
            sessao.add(
                PerguntaDoDesbloqueio(
                    missao_id=missao.id,
                    ordem=ordem,
                    enunciado=pergunta["enunciado"],
                    alternativa_1=pergunta["alternativas"][0],
                    alternativa_2=pergunta["alternativas"][1],
                    alternativa_3=pergunta["alternativas"][2],
                    alternativa_4=pergunta["alternativas"][3],
                    alternativa_correta=pergunta["alternativa_correta"],
                    imagem_referencia=imagem.referencia if imagem is not None else None,
                    imagem_tipo=imagem.tipo if imagem is not None else None,
                    imagem_tamanho=imagem.tamanho if imagem is not None else None,
                )
            )
    else:
        missao.desafio_de_desbloqueio_enunciado = enunciado

    sessao.flush()
    return missao


@dataclass(frozen=True)
class _ImagemPreservada:
    """O que a referência devolvida traz de volta: os três campos da imagem
    da pergunta de origem, copiados sem que byte algum seja reenviado."""

    referencia: str
    tipo: str | None
    tamanho: int | None


def _conferir_imagens_declaradas(
    perguntas: list[dict], vigentes: list[PerguntaDoDesbloqueio]
) -> list[_ImagemPreservada | None]:
    """A referência que volta é conferida contra as imagens das perguntas
    **daquela mesma missão**, antes da substituição: sem isso o campo seria
    um endereço de armazenamento escolhido pelo cliente, capaz de apontar
    arquivo de outra trilha (`RF-09-119`, design — decisão 3). A pergunta
    que omite a referência nasce sem imagem — é assim que o Mestre a remove.
    """
    conhecidas = {
        pergunta.imagem_referencia: _ImagemPreservada(
            referencia=pergunta.imagem_referencia,
            tipo=pergunta.imagem_tipo,
            tamanho=pergunta.imagem_tamanho,
        )
        for pergunta in vigentes
        if pergunta.imagem_referencia is not None
    }
    preservadas: list[_ImagemPreservada | None] = []
    for pergunta in perguntas:
        referencia = pergunta.get("imagem_referencia")
        if referencia is None:
            preservadas.append(None)
            continue
        imagem = conhecidas.get(referencia)
        if imagem is None:
            raise ErroDeValidacao(
                mensagem=(
                    "A imagem devolvida não é de uma pergunta desta missão. Reenvie a "
                    "imagem ou deixe a pergunta sem imagem."
                ),
                campo="perguntas",
            )
        preservadas.append(imagem)
    return preservadas


def _conferir_perguntas_do_quiz(perguntas: list[dict] | None) -> list[dict]:
    """Quiz exige ao menos uma pergunta, e cada uma exige enunciado, quatro
    alternativas e a correta entre elas (`RN-09-43`, `RF-09-118`)."""
    if not perguntas:
        raise ErroDeValidacao(
            mensagem="Desafio em forma de quiz exige ao menos uma pergunta.",
            campo="perguntas",
        )
    for pergunta in perguntas:
        if not pergunta.get("enunciado", "").strip():
            raise ErroDeValidacao(
                mensagem="Toda pergunta do quiz exige um enunciado.", campo="perguntas"
            )
        alternativas = pergunta.get("alternativas") or []
        if len(alternativas) != TOTAL_DE_ALTERNATIVAS_DO_DESBLOQUEIO or not all(
            alternativa and alternativa.strip() for alternativa in alternativas
        ):
            raise ErroDeValidacao(
                mensagem="Toda pergunta do quiz exige quatro alternativas.", campo="perguntas"
            )
        correta = pergunta.get("alternativa_correta")
        if correta is None or not (
            PRIMEIRA_ALTERNATIVA_DO_DESBLOQUEIO <= correta <= TOTAL_DE_ALTERNATIVAS_DO_DESBLOQUEIO
        ):
            raise ErroDeValidacao(
                mensagem="Toda pergunta do quiz exige a alternativa correta.", campo="perguntas"
            )
    return perguntas


# A imagem da pergunta tem lista e teto próprios: só os **formatos de
# imagem** da lista fechada do `RF-09-115`, e 1 MB — teto menor que o do
# conteúdo da missão porque o quiz é lido no aparelho do Guerreiro(a),
# muitas vezes em rede fraca (documento 03 §11).
FORMATOS_DA_IMAGEM_DA_PERGUNTA = frozenset({"image/jpeg", "image/png", "image/webp"})
TAMANHO_TETO_DA_IMAGEM_DA_PERGUNTA = 1024 * 1024


def _formatar_mb(tamanho_em_bytes: int) -> str:
    return f"{tamanho_em_bytes / (1024 * 1024):.1f} MB".replace(".0 MB", " MB")


def _conferir_autoria_da_pergunta(
    sessao: Session, pergunta: PerguntaDoDesbloqueio, operador: Persona
) -> None:
    """A imagem é da pergunta, e a pergunta é da missão do Mestre autor:
    autoria estrita, o mesmo 403 que o conteúdo da missão já usa
    (`RF-09-119`)."""
    missao = sessao.get(Missao, pergunta.missao_id)
    conferir_autoria_estrita_da_trilha(sessao.get(Trilha, missao.trilha_id), operador)


def abrir_envio_da_imagem_da_pergunta(
    sessao: Session,
    pergunta: PerguntaDoDesbloqueio | None,
    *,
    operador: Persona,
    tipo_mime: str | None,
    tamanho_declarado: int | None,
    armazenamento: PortaDeArmazenamento,
) -> str:
    """Confere autoria, formato e teto **antes** de abrir a sessão — a
    recusa acontece sem nenhum byte enviado, como em `conteudos.regra`
    (`RF-09-119`, `RF-09-115`)."""
    if pergunta is None:
        raise NaoEncontrado(mensagem="Pergunta não encontrada.")
    _conferir_autoria_da_pergunta(sessao, pergunta, operador)

    if tipo_mime not in FORMATOS_DA_IMAGEM_DA_PERGUNTA:
        raise ErroDeValidacao(
            mensagem=(
                f"Formato '{tipo_mime}' não aceito na imagem da pergunta. A lista aceita é "
                "JPG, PNG e WebP."
            ),
            campo="tipo_mime",
        )
    if tamanho_declarado is None or tamanho_declarado <= 0:
        raise ErroDeValidacao(
            mensagem="Envio exige o tamanho declarado do arquivo.", campo="tamanho_declarado"
        )
    if tamanho_declarado > TAMANHO_TETO_DA_IMAGEM_DA_PERGUNTA:
        raise ArquivoAcimaDoTeto(
            mensagem=(
                f"A imagem tem {_formatar_mb(tamanho_declarado)} e o limite da imagem da "
                f"pergunta é {_formatar_mb(TAMANHO_TETO_DA_IMAGEM_DA_PERGUNTA)}."
            )
        )

    return armazenamento.abrir_sessao(
        referencia=referencia_da_imagem_da_pergunta(pergunta),
        tipo_mime=tipo_mime,
        tamanho_declarado=tamanho_declarado,
    )


def confirmar_envio_da_imagem_da_pergunta(
    sessao: Session,
    pergunta: PerguntaDoDesbloqueio | None,
    *,
    operador: Persona,
    armazenamento: PortaDeArmazenamento,
) -> PerguntaDoDesbloqueio:
    """Só grava a referência depois de o armazenamento apurar o tamanho e o
    tipo **reais**: o teto vale de novo aqui, porque o recebido pode
    divergir do declarado na abertura (`RF-09-119`)."""
    if pergunta is None:
        raise NaoEncontrado(mensagem="Pergunta não encontrada.")
    _conferir_autoria_da_pergunta(sessao, pergunta, operador)

    referencia = referencia_da_imagem_da_pergunta(pergunta)
    envio = armazenamento.consultar_envio(referencia=referencia)
    if envio is None:
        raise ErroDeValidacao(mensagem="O envio ainda não foi concluído.", campo="imagem")
    if envio.tamanho > TAMANHO_TETO_DA_IMAGEM_DA_PERGUNTA:
        raise ArquivoAcimaDoTeto(
            mensagem=(
                f"A imagem enviada tem {_formatar_mb(envio.tamanho)} e o limite da imagem da "
                f"pergunta é {_formatar_mb(TAMANHO_TETO_DA_IMAGEM_DA_PERGUNTA)}."
            )
        )

    pergunta.imagem_referencia = referencia
    pergunta.imagem_tipo = envio.tipo_mime
    pergunta.imagem_tamanho = envio.tamanho
    sessao.flush()
    return pergunta


@dataclass(frozen=True)
class ImagemDaPergunta:
    """Os bytes servidos pelo núcleo e o tipo declarado no envio."""

    bytes_da_imagem: bytes
    tipo_mime: str


def ler_imagem_da_pergunta(
    sessao: Session,
    pergunta: PerguntaDoDesbloqueio | None,
    *,
    operador: Persona,
    armazenamento: PortaDeArmazenamento,
) -> ImagemDaPergunta:
    """O primeiro caminho de saída de bytes do núcleo, e por isso de
    autorização estrita: serve ao **Mestre autor** da trilha e ao
    **Guerreiro(a) inscrito** nela — os mesmos que já leem a pergunta —, e a
    ninguém mais (`RF-09-119`, `RF-05-89`, design — decisão 5). Servir 1 MB
    pelo núcleo é aceitável; o que a arquitetura mantém fora dele é o
    **envio**.
    """
    if pergunta is None:
        raise NaoEncontrado(mensagem="Pergunta não encontrada.")
    missao = sessao.get(Missao, pergunta.missao_id)
    trilha = sessao.get(Trilha, missao.trilha_id)
    if trilha.autor_id != operador.id:
        inscrito = (
            sessao.query(InscricaoNaTrilha)
            .filter_by(guerreiro_id=operador.id, trilha_id=trilha.id)
            .first()
            is not None
        )
        if not inscrito:
            raise PermissaoNegada(
                mensagem="A imagem da pergunta é servida ao Mestre autor e a quem está "
                "inscrito na trilha."
            )

    if pergunta.imagem_referencia is None:
        raise NaoEncontrado(mensagem="Esta pergunta não tem imagem.")
    return ImagemDaPergunta(
        bytes_da_imagem=armazenamento.ler(referencia=pergunta.imagem_referencia),
        tipo_mime=pergunta.imagem_tipo or "application/octet-stream",
    )


@dataclass
class ResultadoDaSubmissaoDoDesbloqueio:
    """`aprovado`: `True` desbloqueou na hora (quiz que alcançou o corte,
    sondagem respondida ou prático já julgado antes), `None` aguardando o
    Mestre julgar o prático, `False` não alcançou o corte do quiz — submete
    de novo sem limite (`RN-05-20`). `acertos` e `total` são a devolutiva do
    quiz (`RF-05-89`); no prático nascem em zero."""

    aprovado: bool | None
    desbloqueio: DesbloqueioDaMissao | None
    acertos: int = 0
    total: int = 0


def submeter_desafio_de_desbloqueio(
    sessao: Session,
    *,
    guerreiro: Persona,
    missao: Missao | None,
    respostas: list[dict] | None = None,
) -> ResultadoDaSubmissaoDoDesbloqueio:
    """Só o Guerreiro(a) inscrito na trilha submete — sem inscrição, 422
    (`RN-05-20`, `RN-05-06`, documento 11 §2.2). No quiz, a submissão traz a
    resposta de todas as perguntas de uma vez e o núcleo afere pela
    proporção de acertos: passa quem acerta ao menos 60% (`RF-05-89`,
    `RN-05-45`). A **missão de sondagem** é exceção — abre a trilha ao ser
    respondida, acertando ou não (`RN-05-46`), porque mede de onde o
    Guerreiro(a) parte. No prático, grava a declaração do Guerreiro(a),
    aguardando o Mestre autor julgar. **Toda tentativa fica gravada**, a que
    passa e a que não passa (`RN-05-47`). Em nenhum caso o desbloqueio
    credita ponto (`RN-05-06`) — quem credita é sempre o Resultado.
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
        perguntas = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
        if not perguntas:
            raise ErroDeValidacao(
                mensagem="Esta missão não tem desafio de desbloqueio declarado.",
                campo="missao_id",
            )
        escolhas = _conferir_respostas_do_quiz(respostas, perguntas)
        acertos = sum(
            1 for pergunta in perguntas if escolhas[pergunta.id] == pergunta.alternativa_correta
        )
        _gravar_submissao(
            sessao,
            guerreiro_id=guerreiro.id,
            missao_id=missao.id,
            perguntas=perguntas,
            escolhas=escolhas,
            acertos=acertos,
        )
        # A sondagem abre ao ser respondida: o corte não se aplica a ela
        # (`RN-05-46`, design — decisão 4).
        passou = missao.e_sondagem or _passou_no_quiz(acertos, len(perguntas))
        if not passou:
            return ResultadoDaSubmissaoDoDesbloqueio(
                aprovado=False, desbloqueio=None, acertos=acertos, total=len(perguntas)
            )
        desbloqueio = DesbloqueioDaMissao(
            guerreiro_id=guerreiro.id, missao_id=missao.id, aprovado=True
        )
        sessao.add(desbloqueio)
        sessao.flush()
        return ResultadoDaSubmissaoDoDesbloqueio(
            aprovado=True, desbloqueio=desbloqueio, acertos=acertos, total=len(perguntas)
        )

    _gravar_submissao(
        sessao, guerreiro_id=guerreiro.id, missao_id=missao.id, perguntas=[], escolhas={}, acertos=0
    )
    desbloqueio = DesbloqueioDaMissao(guerreiro_id=guerreiro.id, missao_id=missao.id, aprovado=None)
    sessao.add(desbloqueio)
    sessao.flush()
    return ResultadoDaSubmissaoDoDesbloqueio(aprovado=None, desbloqueio=desbloqueio)


def _conferir_respostas_do_quiz(
    respostas: list[dict] | None, perguntas: list[PerguntaDoDesbloqueio]
) -> dict[uuid.UUID, int]:
    """A submissão traz a resposta de todas as perguntas de uma vez
    (`RF-05-89`): resposta faltando, repetida ou apontando pergunta de outra
    missão é 422."""
    escolhas: dict[uuid.UUID, int] = {}
    esperadas = {pergunta.id for pergunta in perguntas}
    for resposta in respostas or []:
        pergunta_id = resposta.get("pergunta_id")
        if pergunta_id not in esperadas:
            raise ErroDeValidacao(
                mensagem="Resposta de pergunta que não é deste desafio.", campo="respostas"
            )
        if pergunta_id in escolhas:
            raise ErroDeValidacao(
                mensagem="Cada pergunta aceita uma resposta só.", campo="respostas"
            )
        escolhida = resposta.get("alternativa_escolhida")
        if escolhida is None or not (
            PRIMEIRA_ALTERNATIVA_DO_DESBLOQUEIO <= escolhida <= TOTAL_DE_ALTERNATIVAS_DO_DESBLOQUEIO
        ):
            raise ErroDeValidacao(
                mensagem="Alternativa escolhida fora das quatro da pergunta.", campo="respostas"
            )
        escolhas[pergunta_id] = escolhida
    if len(escolhas) != len(esperadas):
        raise ErroDeValidacao(
            mensagem="Responda a todas as perguntas do quiz antes de enviar.", campo="respostas"
        )
    return escolhas


def _gravar_submissao(
    sessao: Session,
    *,
    guerreiro_id: uuid.UUID,
    missao_id: uuid.UUID,
    perguntas: list[PerguntaDoDesbloqueio],
    escolhas: dict[uuid.UUID, int],
    acertos: int,
) -> SubmissaoDoDesbloqueio:
    """Acrescenta a tentativa ao histórico, sem tocar nas anteriores
    (`RN-05-47`)."""
    submissao = SubmissaoDoDesbloqueio(
        guerreiro_id=guerreiro_id, missao_id=missao_id, acertos=acertos, total=len(perguntas)
    )
    sessao.add(submissao)
    sessao.flush()
    for pergunta in perguntas:
        sessao.add(
            RespostaDaSubmissao(
                submissao_id=submissao.id,
                pergunta_id=pergunta.id,
                alternativa_escolhida=escolhas[pergunta.id],
                acertou=escolhas[pergunta.id] == pergunta.alternativa_correta,
            )
        )
    sessao.flush()
    return submissao


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


def desafios_em_aberto_do_guerreiro(sessao: Session, *, guerreiro_id: uuid.UUID) -> list[Atividade]:
    """As atividades **em aberto** do Guerreiro(a): das missões que ele já
    desbloqueou, nas trilhas em que está inscrito, subtraídas as que já têm
    `Resultado` lançado para ele — "vigente" como o fundador decidiu
    (`RF-05-19`, proposal — decisão de recorte, design — decisão 1). A
    atividade avulsa fica de fora, por não ter percurso de onde derivar
    "desbloqueada" (design — decisão 2).
    """
    from ..resultados.modelo import Resultado

    ids_das_trilhas = {
        inscricao.trilha_id
        for inscricao in consultar_inscricoes_do_guerreiro(sessao, guerreiro_id=guerreiro_id)
    }
    if not ids_das_trilhas:
        return []

    ids_das_missoes = {
        linha[0]
        for linha in sessao.query(Missao.id)
        .join(DesbloqueioDaMissao, DesbloqueioDaMissao.missao_id == Missao.id)
        .filter(
            Missao.trilha_id.in_(ids_das_trilhas),
            DesbloqueioDaMissao.guerreiro_id == guerreiro_id,
            DesbloqueioDaMissao.aprovado.is_(True),
        )
        .distinct()
        .all()
    }
    if not ids_das_missoes:
        return []

    ids_com_resultado = {
        linha[0]
        for linha in sessao.query(Resultado.atividade_id)
        .filter(Resultado.guerreiro_id == guerreiro_id)
        .distinct()
        .all()
    }

    atividades = sessao.query(Atividade).filter(Atividade.missao_id.in_(ids_das_missoes)).all()
    return [atividade for atividade in atividades if atividade.id not in ids_com_resultado]


@dataclass
class RetomadaEmAberto:
    missao: Missao
    trilha: Trilha
    prazo: datetime


def retomadas_em_aberto_do_guerreiro(
    sessao: Session, *, guerreiro_id: uuid.UUID
) -> list[RetomadaEmAberto]:
    """As retomadas em aberto do Guerreiro(a): cada dia de
    `cadencia_de_retomada` de uma missão que ele desbloqueou é um
    agendamento, com prazo contado do desbloqueio aprovado dele (design —
    decisão 4). Um agendamento está em aberto quando o prazo já venceu e
    nenhuma produção individual dele naquela missão tem `registrado_em >=
    prazo` — como os prazos crescem, uma produção posterior fecha aquele
    agendamento e os anteriores, e uma produção anterior a todos (refazer
    por conta própria) não fecha nenhum (`RF-05-79`, `RF-05-80`,
    `RN-05-38`). Nenhum estado persistido: a lista nasce na leitura, como o
    percurso já nasce.
    """
    from ..producoes.modelo import ProducaoDaMissao

    desbloqueios = (
        sessao.query(DesbloqueioDaMissao, Missao)
        .join(Missao, Missao.id == DesbloqueioDaMissao.missao_id)
        .filter(
            DesbloqueioDaMissao.guerreiro_id == guerreiro_id,
            DesbloqueioDaMissao.aprovado.is_(True),
            Missao.cadencia_de_retomada.isnot(None),
        )
        .all()
    )
    if not desbloqueios:
        return []

    momento_atual = agora()
    resultado = []
    for desbloqueio, missao in desbloqueios:
        momentos_de_producao = [
            linha[0]
            for linha in sessao.query(ProducaoDaMissao.registrado_em).filter(
                ProducaoDaMissao.guerreiro_id == guerreiro_id,
                ProducaoDaMissao.missao_id == missao.id,
            )
        ]
        trilha = sessao.get(Trilha, missao.trilha_id)
        for dias in missao.cadencia_de_retomada:
            prazo = desbloqueio.momento + timedelta(days=dias)
            if momento_atual < prazo:
                continue
            if any(momento >= prazo for momento in momentos_de_producao):
                continue
            resultado.append(RetomadaEmAberto(missao=missao, trilha=trilha, prazo=prazo))
    return resultado


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
