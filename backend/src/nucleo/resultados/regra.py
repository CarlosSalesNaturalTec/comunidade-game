import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session

from ..aulas.modelo import Aula, Presenca, SituacaoDaAula
from ..equipes.modelo import Equipe, IntegranteDaEquipe
from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..ponto_extra.regra import creditar_ponto_extra_do_resultado
from ..pontuacao.regra import creditar_pontuacao_do_resultado
from ..reservas.regra import consumir_reservas_da_aula
from ..trilhas.modelo import Atividade, Missao, ModalidadeDeAtividade, Trilha
from ..trilhas.regra import conferir_atividade_vigente, conferir_posse_da_trilha
from .modelo import DesfechoDoResultado, Resultado

_SITUACOES_COM_DESFECHO = (SituacaoDaAula.realizada, SituacaoDaAula.cancelada)


def registrar_resultado(
    sessao: Session,
    *,
    operador: Persona,
    aula: Aula | None,
    guerreiro_id: uuid.UUID | None,
    atividade: Atividade | None,
    momento_do_fato: datetime | None,
    producao: str | None,
    desfecho: str | None,
) -> Resultado:
    """Grava o Resultado e credita, na mesma operação, o ponto regular e o
    ponto extra, além de reavaliar nível e badge — só o Mestre autor da
    trilha da atividade ou o Admin lançam o desfecho, pela mesma
    conferência de posse da quinta fatia (`RF-01-20`, `RF-01-16`,
    `RF-01-03`, 11 §4). A aula é quem liga o resultado às reservas que a
    baixa consome (`RF-07-09`, `RF-02-35`, documento 04 §1).

    Na **atividade avulsa** — sem missão —, não há posse de Mestre a
    conferir: o lançamento é restrito ao Admin, e o crédito segue o poder
    declarado pela atividade, não uma trilha (`RF-02-29`, `RF-02-33`,
    design — decisão 4).
    """
    if atividade is None:
        raise ErroDeValidacao(mensagem="Resultado exige uma atividade.", campo="atividade_id")

    trilha = None
    if atividade.missao_id is None:
        if operador.papel != Papel.admin:
            raise PermissaoNegada(mensagem="Só o Admin lança o resultado da atividade avulsa.")
    else:
        missao = sessao.get(Missao, atividade.missao_id)
        trilha = sessao.get(Trilha, missao.trilha_id)
        conferir_posse_da_trilha(trilha, operador)

    if guerreiro_id is None:
        raise ErroDeValidacao(mensagem="Resultado exige um Guerreiro(a).", campo="guerreiro_id")
    if aula is None:
        raise ErroDeValidacao(
            mensagem="Resultado exige a aula em que foi lançado.", campo="aula_id"
        )
    if momento_do_fato is None:
        raise ErroDeValidacao(mensagem="Resultado exige a data do fato.", campo="momento_do_fato")
    if not producao or not producao.strip():
        raise ErroDeValidacao(
            mensagem="Resultado exige a produção do Guerreiro(a).", campo="producao"
        )
    if not desfecho:
        raise ErroDeValidacao(mensagem="Resultado exige um desfecho.", campo="desfecho")
    try:
        desfecho_valido = DesfechoDoResultado(desfecho)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Desfecho fora dos valores previstos.", campo="desfecho"
        ) from exc

    resultado = Resultado(
        guerreiro_id=guerreiro_id,
        atividade_id=atividade.id,
        aula_id=aula.id,
        momento_do_fato=momento_do_fato,
        producao=producao,
        desfecho=desfecho_valido,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(resultado)
    sessao.flush()

    creditar_pontuacao_do_resultado(sessao, resultado=resultado, atividade=atividade, trilha=trilha)
    creditar_ponto_extra_do_resultado(sessao, resultado=resultado)

    return resultado


@dataclass
class ResultadoDeclarado:
    """Um participante do lançamento da atividade realizada — os mesmos
    campos de `registrar_resultado`, sem `aula`, que o ato já fixa uma vez
    para todos (`RF-07-09`, `RF-02-35`)."""

    guerreiro_id: uuid.UUID | None
    atividade: Atividade | None
    momento_do_fato: datetime | None
    producao: str | None
    desfecho: str | None


@dataclass
class ResultadoDaEquipe:
    """O lançamento declarado **pela equipe da aula**, sem Guerreiro(a): o
    desfecho e a produção são dela e valem igualmente a cada integrante
    presente, que é quem recebe um `Resultado` (`RF-02-112`, `RN-02-32`,
    documento 11 §4)."""

    equipe_id: uuid.UUID | None
    momento_do_fato: datetime | None
    producao: str | None
    desfecho: str | None


def _registrar_resultados(
    sessao: Session, *, operador: Persona, aula: Aula, resultados: list[ResultadoDeclarado]
) -> list[Resultado]:
    """Montagem comum aos dois atos de lançamento — por aula, do Admin, e
    por atividade, do Mestre autor: grava um `Resultado` por participante,
    na mesma transação, sem decidir nada sobre reserva nem situação da aula
    — isso é exclusivo de quem chama (design — Decisions 1, riscos)."""
    return [
        registrar_resultado(
            sessao,
            operador=operador,
            aula=aula,
            guerreiro_id=entrada.guerreiro_id,
            atividade=entrada.atividade,
            momento_do_fato=entrada.momento_do_fato,
            producao=entrada.producao,
            desfecho=entrada.desfecho,
        )
        for entrada in resultados
    ]


def lancar_atividade_realizada(
    sessao: Session,
    *,
    operador: Persona,
    aula: Aula | None,
    resultados: list[ResultadoDeclarado],
) -> tuple[Aula, list[Resultado]]:
    """Ato **por aula**, restrito ao Admin: registra em uma operação os
    Resultados de todos os participantes, converte cada reserva da aula em
    baixa e leva a aula a **realizada** — não há operação de baixa separada
    deste ato (`RF-07-09`, `RF-02-35`, `RN-07-36`, `RF-01-16`, documento
    04 §1, design — Decisions 7).
    """
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin lança a atividade realizada da aula.")
    if aula is None:
        raise ErroDeValidacao(mensagem="Lançamento exige uma aula.", campo="aula_id")
    if aula.situacao in _SITUACOES_COM_DESFECHO:
        raise ErroDeValidacao(
            mensagem="Esta aula já teve desfecho; o lançamento não se repete.",
            campo="situacao",
        )

    gravados = _registrar_resultados(sessao, operador=operador, aula=aula, resultados=resultados)

    consumir_reservas_da_aula(sessao, aula=aula, operador=operador)
    aula.situacao = SituacaoDaAula.realizada
    sessao.flush()

    return aula, gravados


def _expandir_equipe(
    sessao: Session,
    *,
    aula: Aula,
    atividade: Atividade,
    declaracao: ResultadoDaEquipe,
) -> tuple[list[ResultadoDeclarado], list[uuid.UUID]]:
    """Abre o lançamento da equipe em um `ResultadoDeclarado` por integrante
    **presente**, com o desfecho e a produção dela — o valor do motor é
    integral a cada um, porque dividir puniria a colaboração (documento 11
    §4, `RN-02-32`).

    Fica de fora quem não tem `Presenca` não anulada naquela aula, e é
    devolvido para que a tela diga quem não recebeu. O integrante que não é
    Guerreiro(a) — o familiar da modalidade em equipe com familiar — é
    pulado em silêncio: nunca recebeu Resultado para ficar de fora dele
    (`RN-02-32`). Equipe sem nenhum presente é erro de operação, não
    lançamento vazio (`RN-02-33`).
    """
    if declaracao.equipe_id is None:
        raise ErroDeValidacao(mensagem="Lançamento por equipe exige a equipe.", campo="equipe_id")
    equipe = sessao.get(Equipe, declaracao.equipe_id)
    if equipe is None or equipe.aula_id != aula.id:
        raise ErroDeValidacao(mensagem="Equipe não encontrada nesta aula.", campo="equipe_id")

    integrantes = (
        sessao.query(IntegranteDaEquipe)
        .filter(IntegranteDaEquipe.equipe_id == equipe.id)
        .order_by(IntegranteDaEquipe.entrou_em)
        .all()
    )

    declarados: list[ResultadoDeclarado] = []
    fora_por_falta_de_presenca: list[uuid.UUID] = []
    for integrante in integrantes:
        persona = sessao.get(Persona, integrante.persona_id)
        if persona is None or persona.papel != Papel.guerreiro:
            continue
        tem_presenca = (
            sessao.query(Presenca.id)
            .filter(
                Presenca.aula_id == aula.id,
                Presenca.guerreiro_id == persona.id,
                Presenca.anulada_em.is_(None),
            )
            .first()
            is not None
        )
        if not tem_presenca:
            fora_por_falta_de_presenca.append(persona.id)
            continue
        declarados.append(
            ResultadoDeclarado(
                guerreiro_id=persona.id,
                atividade=atividade,
                momento_do_fato=declaracao.momento_do_fato,
                producao=declaracao.producao,
                desfecho=declaracao.desfecho,
            )
        )

    if not declarados:
        raise ErroDeValidacao(
            mensagem="Nenhum integrante desta equipe tem presença na aula.", campo="equipe_id"
        )
    return declarados, fora_por_falta_de_presenca


def _recusar_resultado_repetido(
    sessao: Session, *, atividade: Atividade, resultados: list[ResultadoDeclarado]
) -> None:
    """O ato por atividade roda quantas vezes o encontro exigir, e o
    Resultado não se edita nem se remove — sem esta guarda o ponto dobraria
    em silêncio. A conferência precede a gravação de qualquer um da lista;
    o índice único de `(guerreiro_id, atividade_id)` trava a corrida entre
    dois envios simultâneos (`RN-02-33`, design — decisão 4)."""
    ja_tem = {
        linha.guerreiro_id
        for linha in sessao.query(Resultado.guerreiro_id).filter(
            Resultado.atividade_id == atividade.id
        )
    }
    for entrada in resultados:
        if entrada.guerreiro_id is None:
            continue
        if entrada.guerreiro_id in ja_tem:
            raise ErroDeValidacao(
                mensagem="Este Guerreiro(a) já tem Resultado nesta atividade.",
                campo="guerreiro_id",
            )
        ja_tem.add(entrada.guerreiro_id)


def lancar_resultados_da_atividade(
    sessao: Session,
    *,
    operador: Persona,
    aula: Aula | None,
    atividade: Atividade | None,
    resultados: list[ResultadoDeclarado],
    equipe: ResultadoDaEquipe | None = None,
) -> tuple[list[Resultado], list[uuid.UUID]]:
    """Ato **por atividade**, aberto ao Mestre autor da trilha dela ou ao
    Admin: registra em uma operação os Resultados de todos os participantes
    — a mesma `registrar_resultado` do ato por aula —, sem consumir reserva
    nem alterar a situação da aula, que permanecem exclusivas do lançamento
    por aula (`RF-09-43`, `RF-09-44`, `RF-09-49`, `RF-09-74`, design —
    Decisions 1). A posse é conferida aqui, antes de iterar os participantes,
    para que a lista vazia também recuse o Mestre que não é o autor
    (`RN-09-08`).

    É também o ato da **atividade avulsa**: sem missão não há posse de
    Mestre a conferir, e o lançamento fica restrito ao Admin — por rodar
    sem tocar reserva nem situação da aula, corre quantas vezes o encontro
    exigir (`RF-02-112`).

    Na avulsa, o lançamento é **por participante ou por equipe da aula**,
    nunca os dois: `equipe` abre em um Resultado por integrante presente, e
    a forma segue a modalidade da atividade (`RN-02-32`, `RN-02-33`,
    documento 11 §4). A atividade **de trilha** não se lança pela equipe —
    o `RN-02-33` é regra do PRD-02, e o PRD-09 não foi revisto nesta fatia.
    Devolve os Resultados gravados e quem ficou de fora por não ter
    presença.

    A recusa do **segundo Resultado do mesmo par** vale para as duas: o
    índice único que a sustenta é total por desenho (design — decisão 4),
    então o 422 legível é melhor que o erro do banco.
    """
    if atividade is None:
        raise ErroDeValidacao(mensagem="Lançamento exige uma atividade.", campo="atividade_id")
    conferir_atividade_vigente(atividade)

    if atividade.missao_id is None:
        if operador.papel != Papel.admin:
            raise PermissaoNegada(mensagem="Só o Admin lança o resultado da atividade avulsa.")
    else:
        missao = sessao.get(Missao, atividade.missao_id)
        trilha = sessao.get(Trilha, missao.trilha_id)
        conferir_posse_da_trilha(trilha, operador)

    if aula is None:
        raise ErroDeValidacao(mensagem="Lançamento exige a aula em que aconteceu.", campo="aula_id")

    # A forma do lançamento é regra da **avulsa** (`RN-02-33`, PRD-02): o
    # ato por atividade de trilha segue como está, porque o Mestre não
    # declara equipe na App 09 e o PRD-09 não foi revisto nesta fatia.
    if atividade.missao_id is None:
        if equipe is None and not resultados:
            raise ErroDeValidacao(
                mensagem="Lançamento exige a equipe ou a lista de participantes.",
                campo="equipe_id",
            )
        if equipe is not None and resultados:
            raise ErroDeValidacao(
                mensagem="Lançamento declara a equipe ou os participantes, nunca os dois.",
                campo="equipe_id",
            )

        e_individual = atividade.modalidade == ModalidadeDeAtividade.individual
        if equipe is not None and e_individual:
            raise ErroDeValidacao(
                mensagem="Atividade individual se lança por participante, não por equipe.",
                campo="equipe_id",
            )
        if equipe is None and not e_individual:
            raise ErroDeValidacao(
                mensagem="Atividade em equipe se lança pela equipe, não por participante.",
                campo="participantes",
            )
    elif equipe is not None:
        raise ErroDeValidacao(
            mensagem="Só a atividade avulsa se lança pela equipe da aula.", campo="equipe_id"
        )

    fora_por_falta_de_presenca: list[uuid.UUID] = []
    if equipe is not None:
        resultados, fora_por_falta_de_presenca = _expandir_equipe(
            sessao, aula=aula, atividade=atividade, declaracao=equipe
        )

    _recusar_resultado_repetido(sessao, atividade=atividade, resultados=resultados)
    gravados = _registrar_resultados(sessao, operador=operador, aula=aula, resultados=resultados)
    return gravados, fora_por_falta_de_presenca
