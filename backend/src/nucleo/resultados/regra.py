import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session

from ..armazenamento.limites import (
    FORMATOS_ACEITOS_EM_TEXTO,
    FORMATOS_DE_ENVIO_ACEITOS,
    formatar_mb,
    teto_do_tipo_de_producao,
)
from ..armazenamento.porta import PortaDeArmazenamento
from ..aulas.modelo import Aula, Presenca, SituacaoDaAula
from ..criacoes_originais.modelo import TipoDeProducaoDaCriacaoOriginal
from ..equipes.modelo import Equipe, IntegranteDaEquipe
from ..erros import ArquivoAcimaDoTeto, ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..ponto_extra.regra import creditar_ponto_extra_do_resultado
from ..pontuacao.regra import creditar_pontuacao_do_resultado
from ..recompensas_de_marco.regra import entregar_na_aprovacao
from ..trilhas.modelo import Atividade, Missao, ModalidadeDeAtividade, Trilha
from ..trilhas.regra import (
    ComprovanteDoLancamento,
    conferir_atividade_vigente,
    conferir_posse_da_trilha,
    julgar_pratico_no_lancamento,
    missoes_desbloqueadas_pelo_guerreiro,
)
from .modelo import DesfechoDoResultado, Resultado

_FORMAS_EM_TEXTO = frozenset(
    {TipoDeProducaoDaCriacaoOriginal.texto, TipoDeProducaoDaCriacaoOriginal.link_externo}
)


@dataclass
class ComprovanteDeclarado:
    """O comprovante de um participante, como chega no lançamento: a forma e,
    conforme ela, o texto ou endereço, ou o envio já concluído do arquivo
    (`RF-09-149`, design — decisão 2)."""

    tipo: str | None
    texto: str | None = None
    envio_id: uuid.UUID | None = None


@dataclass
class JulgamentoDeclarado:
    """O julgamento do prático que acompanha o lançamento (`RF-09-150`)."""

    cumpriu: bool
    publicavel: bool = False
    motivo: str | None = None


def referencia_do_envio_do_comprovante(persona_id: uuid.UUID, envio_id: uuid.UUID) -> str:
    """A referência leva quem abriu o envio: é ela que faz o envio de outra
    persona não ser encontrado no lançamento (design — decisão 2)."""
    return f"resultados/envios/{persona_id}/{envio_id}"


def _conferir_posse_do_lancamento(sessao: Session, atividade: Atividade, operador: Persona) -> None:
    if atividade.missao_id is None:
        if operador.papel != Papel.admin:
            raise PermissaoNegada(mensagem="Só o Admin lança o resultado da atividade avulsa.")
        return
    missao = sessao.get(Missao, atividade.missao_id)
    conferir_posse_da_trilha(sessao.get(Trilha, missao.trilha_id), operador)


def _forma_do_comprovante(valor: str | None) -> TipoDeProducaoDaCriacaoOriginal:
    try:
        return TipoDeProducaoDaCriacaoOriginal(valor)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Forma de comprovante fora das seis previstas.", campo="comprovante"
        ) from exc


def abrir_envio_do_comprovante(
    sessao: Session,
    *,
    operador: Persona,
    atividade: Atividade | None,
    tipo: str | None,
    tipo_mime: str | None,
    tamanho_declarado: int | None,
    armazenamento: PortaDeArmazenamento,
    origem: str | None = None,
) -> tuple[uuid.UUID, str]:
    """Abre, **antes** do lançamento, a sessão retomável do comprovante em mídia
    — quem lança a atividade, a lista fechada e o teto da criação original
    (`RF-09-149`, `RF-01-78`, design — decisão 2). Devolve o identificador do
    envio, que o lançamento referencia, e o endereço da sessão."""
    if atividade is None:
        raise NaoEncontrado(mensagem="Atividade não encontrada.")
    _conferir_posse_do_lancamento(sessao, atividade, operador)
    forma = _forma_do_comprovante(tipo)
    if forma in _FORMAS_EM_TEXTO:
        raise ErroDeValidacao(
            mensagem="Comprovante em texto ou link vai no próprio lançamento, sem envio de "
            "arquivo.",
            campo="tipo",
        )
    if tipo_mime not in FORMATOS_DE_ENVIO_ACEITOS:
        raise ErroDeValidacao(
            mensagem=f"Formato '{tipo_mime}' não aceito. A lista aceita é "
            f"{FORMATOS_ACEITOS_EM_TEXTO}.",
            campo="tipo_mime",
        )
    if tamanho_declarado is None or tamanho_declarado <= 0:
        raise ErroDeValidacao(
            mensagem="Envio exige o tamanho declarado do arquivo.", campo="tamanho_declarado"
        )
    teto = teto_do_tipo_de_producao(forma)
    if tamanho_declarado > teto:
        raise ArquivoAcimaDoTeto(
            mensagem=f"O arquivo tem {formatar_mb(tamanho_declarado)} e o limite para este tipo "
            f"de comprovante é {formatar_mb(teto)}."
        )
    envio_id = uuid.uuid4()
    endereco = armazenamento.abrir_sessao(
        referencia=referencia_do_envio_do_comprovante(operador.id, envio_id),
        tipo_mime=tipo_mime,
        tamanho_declarado=tamanho_declarado,
        origem=origem,
    )
    return envio_id, endereco


def _resolver_comprovante(
    sessao: Session,
    *,
    operador: Persona,
    producao: str | None,
    comprovante: ComprovanteDeclarado | None,
    armazenamento: PortaDeArmazenamento | None,
) -> ComprovanteDoLancamento:
    """A produção do Resultado é o **comprovante**, obrigatório (`RN-09-64`).
    A produção em texto simples, sem forma, vale como comprovante em texto —
    é o caminho da App 03 (design — decisão 3). Na mídia, o envio tem de ter
    **concluído**, ser de quem lança e não estar já usado, e o teto e o tipo
    são conferidos sobre o que o armazenamento apurou (design — decisão 2)."""
    texto_da_producao = producao.strip() if producao else None
    if comprovante is None:
        if not texto_da_producao:
            raise ErroDeValidacao(
                mensagem="Resultado exige a produção do Guerreiro(a).", campo="producao"
            )
        return ComprovanteDoLancamento(
            tipo=TipoDeProducaoDaCriacaoOriginal.texto,
            texto=producao,
            referencia=None,
            tamanho=None,
            tipo_do_arquivo=None,
        )
    if texto_da_producao:
        raise ErroDeValidacao(
            mensagem="Informe o comprovante ou a produção em texto, não os dois.",
            campo="producao",
        )

    forma = _forma_do_comprovante(comprovante.tipo)
    texto = comprovante.texto.strip() if comprovante.texto else None
    if forma in _FORMAS_EM_TEXTO:
        if comprovante.envio_id is not None:
            raise ErroDeValidacao(
                mensagem="Comprovante em texto ou link não leva arquivo.", campo="comprovante"
            )
        if not texto:
            raise ErroDeValidacao(
                mensagem=(
                    "O comprovante em texto exige o que foi escrito."
                    if forma == TipoDeProducaoDaCriacaoOriginal.texto
                    else "O comprovante em link exige o endereço."
                ),
                campo="comprovante",
            )
        return ComprovanteDoLancamento(
            tipo=forma, texto=texto, referencia=None, tamanho=None, tipo_do_arquivo=None
        )

    if texto:
        raise ErroDeValidacao(
            mensagem=f"O comprovante em {forma.value} vai pelo envio do arquivo, não escrito.",
            campo="comprovante",
        )
    if comprovante.envio_id is None:
        raise ErroDeValidacao(
            mensagem="Envie o arquivo do comprovante antes de lançar.", campo="comprovante"
        )
    if armazenamento is None:
        raise ErroDeValidacao(
            mensagem="Este lançamento não aceita comprovante em arquivo.", campo="comprovante"
        )
    referencia = referencia_do_envio_do_comprovante(operador.id, comprovante.envio_id)
    envio = armazenamento.consultar_envio(referencia=referencia)
    if envio is None:
        raise ErroDeValidacao(
            mensagem="O envio do comprovante ainda não terminou. Aguarde e tente de novo.",
            campo="comprovante",
        )
    ja_usado = (
        sessao.query(Resultado.id).filter(Resultado.comprovante_referencia == referencia).first()
    )
    if ja_usado is not None:
        raise ErroDeValidacao(
            mensagem="Este arquivo já é comprovante de outro lançamento.", campo="comprovante"
        )
    if envio.tipo_mime not in FORMATOS_DE_ENVIO_ACEITOS:
        raise ErroDeValidacao(
            mensagem=f"Formato '{envio.tipo_mime}' não aceito. A lista aceita é "
            f"{FORMATOS_ACEITOS_EM_TEXTO}.",
            campo="comprovante",
        )
    teto = teto_do_tipo_de_producao(forma)
    if envio.tamanho > teto:
        raise ArquivoAcimaDoTeto(
            mensagem=f"O arquivo enviado tem {formatar_mb(envio.tamanho)} e o limite para este "
            f"tipo de comprovante é {formatar_mb(teto)}."
        )
    return ComprovanteDoLancamento(
        tipo=forma,
        texto=None,
        referencia=referencia,
        tamanho=envio.tamanho,
        tipo_do_arquivo=envio.tipo_mime,
    )


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
    comprovante: ComprovanteDeclarado | None = None,
    julgamento: JulgamentoDeclarado | None = None,
    armazenamento: PortaDeArmazenamento | None = None,
    conferir_pratico: bool = False,
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

    A produção é o **comprovante**, numa das seis formas (`RF-09-149`,
    `RN-09-64`), e, quando a missão da atividade tem prático que o
    Guerreiro(a) não cumpriu, o **julgamento** vem junto e roda nesta mesma
    operação (`RF-09-150`, `RN-09-65`, `RN-09-66`).
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
    gravado = _resolver_comprovante(
        sessao,
        operador=operador,
        producao=producao,
        comprovante=comprovante,
        armazenamento=armazenamento,
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
        producao=gravado.texto,
        comprovante_tipo=gravado.tipo,
        comprovante_referencia=gravado.referencia,
        comprovante_tamanho=gravado.tamanho,
        comprovante_tipo_do_arquivo=gravado.tipo_do_arquivo,
        desfecho=desfecho_valido,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(resultado)
    sessao.flush()

    creditar_pontuacao_do_resultado(sessao, resultado=resultado, atividade=atividade, trilha=trilha)
    creditar_ponto_extra_do_resultado(sessao, resultado=resultado, detalhe=atividade.titulo)

    if not conferir_pratico:
        # O lançamento **por aula**, do Admin, fica como estava: o julgamento
        # do prático é do ato por atividade (design — decisão 4).
        return resultado

    missao = sessao.get(Missao, atividade.missao_id) if atividade.missao_id else None
    desbloqueadas_antes = (
        missoes_desbloqueadas_pelo_guerreiro(
            sessao, guerreiro_id=guerreiro_id, trilha_id=missao.trilha_id
        )
        if missao is not None and julgamento is not None
        else set()
    )
    julgado = julgar_pratico_no_lancamento(
        sessao,
        operador=operador,
        missao=missao,
        guerreiro_id=guerreiro_id,
        comprovante=gravado,
        julgamento=(julgamento.cumpriu, julgamento.publicavel, julgamento.motivo)
        if julgamento is not None
        else None,
    )
    if julgado is not None and julgado.cumpriu:
        # A mesma entrega de recompensa de marco que a bancada faz ao aprovar
        # (`RF-09-146`, design — decisão 4).
        entregar_na_aprovacao(
            sessao,
            operador=operador,
            guerreiro=sessao.get(Persona, guerreiro_id),
            trilha_id=missao.trilha_id,
            desbloqueadas_antes=desbloqueadas_antes,
        )
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
    comprovante: ComprovanteDeclarado | None = None
    julgamento: JulgamentoDeclarado | None = None


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
    sessao: Session,
    *,
    operador: Persona,
    aula: Aula,
    resultados: list[ResultadoDeclarado],
    armazenamento: PortaDeArmazenamento | None = None,
    conferir_pratico: bool = False,
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
            comprovante=entrada.comprovante,
            julgamento=entrada.julgamento,
            armazenamento=armazenamento,
            conferir_pratico=conferir_pratico,
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
    Resultados dos participantes, durante ou depois da aula. Não baixa
    reserva nem muda a situação — a aula não tem fechamento, e isso é do
    sistema no fim do horário (`RF-02-33`, `RF-02-35`, `RN-07-43`,
    `RF-01-16`, change `baixa-no-fim-da-aula`, design — decisão 5). O
    Resultado repetido segue recusado por `_registrar_resultados`.
    """
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin lança a atividade realizada da aula.")
    if aula is None:
        raise ErroDeValidacao(mensagem="Lançamento exige uma aula.", campo="aula_id")
    if aula.situacao == SituacaoDaAula.cancelada:
        raise ErroDeValidacao(
            mensagem="Esta aula foi cancelada; não há resultado a lançar.",
            campo="situacao",
        )

    gravados = _registrar_resultados(sessao, operador=operador, aula=aula, resultados=resultados)
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
    armazenamento: PortaDeArmazenamento | None = None,
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
    gravados = _registrar_resultados(
        sessao,
        operador=operador,
        aula=aula,
        resultados=resultados,
        armazenamento=armazenamento,
        conferir_pratico=True,
    )
    return gravados, fora_por_falta_de_presenca


def listar_resultados_da_aula(
    sessao: Session, *, operador: Persona, aula: Aula | None
) -> list[tuple[Resultado, Atividade]]:
    """Os Resultados lançados na aula, com a atividade de cada um: o Admin vê
    todos, e o Mestre só os das atividades de que é autor — a mesma posse do
    lançamento (`RF-09-151`, design — decisão 6). Aula inexistente é 404."""
    if aula is None:
        raise NaoEncontrado(mensagem="Aula não encontrada.")
    consulta = (
        sessao.query(Resultado, Atividade)
        .join(Atividade, Atividade.id == Resultado.atividade_id)
        .filter(Resultado.aula_id == aula.id)
    )
    if operador.papel != Papel.admin:
        consulta = (
            consulta.join(Missao, Missao.id == Atividade.missao_id)
            .join(Trilha, Trilha.id == Missao.trilha_id)
            .filter(Trilha.autor_id == operador.id)
        )
    return consulta.order_by(Resultado.momento_do_fato, Resultado.id).all()


@dataclass
class ArquivoDoComprovante:
    bytes_do_arquivo: bytes
    tipo_mime: str


def ler_arquivo_do_comprovante(
    sessao: Session,
    *,
    operador: Persona,
    resultado: Resultado | None,
    armazenamento: PortaDeArmazenamento,
) -> ArquivoDoComprovante:
    """Os bytes do comprovante vão ao **Mestre autor** da atividade e ao
    **Admin**; a leitura pelo Guerreiro(a) é fatia própria (`RF-09-151`,
    decisão do fundador de 2026-11-27). Comprovante sem arquivo é 404."""
    if resultado is None:
        raise NaoEncontrado(mensagem="Resultado não encontrado.")
    if operador.papel != Papel.admin:
        atividade = sessao.get(Atividade, resultado.atividade_id)
        missao = sessao.get(Missao, atividade.missao_id) if atividade.missao_id else None
        trilha = sessao.get(Trilha, missao.trilha_id) if missao is not None else None
        if trilha is None or trilha.autor_id != operador.id:
            raise PermissaoNegada(
                mensagem="O comprovante é servido ao Mestre autor da atividade e ao Admin."
            )
    if resultado.comprovante_referencia is None:
        raise NaoEncontrado(mensagem="Este lançamento não tem arquivo de comprovante.")
    return ArquivoDoComprovante(
        bytes_do_arquivo=armazenamento.ler(referencia=resultado.comprovante_referencia),
        tipo_mime=resultado.comprovante_tipo_do_arquivo or "application/octet-stream",
    )
