import math
import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Query, Session

from ..coletas.modelo import DesafioDeColeta, RegistroDeColeta, SerieDeColeta
from ..comunidades.regra import filtrar_personas_por_comunidade
from ..consentimentos.regra import condicao_de_autorizacao_vigente
from ..criacoes_originais.modelo import CriacaoOriginal
from ..equipes.modelo import IntegranteDaEquipe
from ..erros import ErroDeValidacao, PoderDoTerritorioNaoDeclarado
from ..ocorrencias_de_conduta.modelo import OcorrenciaDeConduta
from ..personas.modelo import Nick, Papel, Persona
from ..poderes.regra import buscar_poder_do_territorio
from ..quiz.modelo import (
    EquipeNaPartida,
    PartidaDeQuiz,
    PerguntaAnuladaNaPartida,
    PerguntaDeQuiz,
    RespostaDeQuiz,
)
from ..resultados.modelo import DesfechoDoResultado, Resultado
from ..trilhas.modelo import Atividade, Missao, ModalidadeDeAtividade, Trilha
from .modelo import Badge, Nivel, PontoRegular, TipoDeBadge

# Documento 11 §5, "Desafio semanal": valor-base pela modalidade da
# atividade, e o adicional de mérito que o desfecho acrescenta.
VALOR_BASE_EM_EQUIPE_COM_FAMILIAR = 20
VALOR_BASE_PADRAO = 10
ADICIONAL_DE_MERITO = 5
ADICIONAL_DE_MERITO_EXTRA_POR_AUXILIO = 10

# Documento 11 §5: a criação original validada credita 50 pontos regulares
# integrais a cada integrante da equipe da trilha, sem rateio pelo tamanho.
VALOR_DA_CRIACAO_ORIGINAL = 50

# Documento 11 §5: registro de coleta válido credita o mesmo valor, qualquer
# que seja o tipo medido, sem teto por período — só o desafio limita quantos
# registros do período pontuam (`RF-08-09`, `RN-08-05`).
VALOR_DO_REGISTRO_DE_COLETA = 5

# Documento 11 §5, "Quiz ao Vivo": 1 ponto por acerto da equipe, mais 1 de
# bônus à primeira a acertar cada pergunta, com teto de 10 por partida. O
# valor apurado vai integral a cada integrante, sem rateio.
VALOR_POR_ACERTO_NO_QUIZ = 1
BONUS_DA_PRIMEIRA_A_ACERTAR = 1
TETO_DE_PONTO_POR_PARTIDA_DE_QUIZ = 10

# Documento 11 §7: o badge de valores/causas nasce da natureza declarada na
# atividade, já normalizada por `trilhas.regra._normalizar_natureza`.
NATUREZA_DE_VALORES_E_CAUSAS = "valores e temas transversais"

NIVEL_1 = 1
NIVEL_2 = 2
NIVEL_4 = 4
NIVEL_5 = 5


def _valor_regular(atividade: Atividade, desfecho: DesfechoDoResultado) -> int:
    valor_base = (
        VALOR_BASE_EM_EQUIPE_COM_FAMILIAR
        if atividade.modalidade == ModalidadeDeAtividade.em_equipe_com_familiar
        else VALOR_BASE_PADRAO
    )
    if desfecho == DesfechoDoResultado.realizada_com_merito:
        return valor_base + ADICIONAL_DE_MERITO
    if desfecho == DesfechoDoResultado.merito_extra_por_auxilio:
        return valor_base + ADICIONAL_DE_MERITO_EXTRA_POR_AUXILIO
    return valor_base


def creditar_ponto_regular(
    sessao: Session,
    *,
    guerreiro_id: uuid.UUID,
    valor: int,
    trilha_id: uuid.UUID | None = None,
    poder_id: uuid.UUID | None = None,
) -> PontoRegular:
    """Credita — nunca debita: débito é `debitar_ponto_regular`, restrito ao
    estorno por fato desfeito (`RF-01-57`, `RN-01-38`). Exige exatamente uma
    referência — trilha **ou** poder, nunca as duas nem nenhuma (`RF-08-09`,
    `RN-08-15`)."""
    if (trilha_id is None) == (poder_id is None):
        raise ErroDeValidacao(
            mensagem="Crédito de ponto regular exige exatamente uma trilha ou um poder."
        )
    if valor <= 0:
        raise ErroDeValidacao(
            mensagem="Crédito de ponto regular exige valor positivo.", campo="valor"
        )

    filtro = {"guerreiro_id": guerreiro_id, "trilha_id": trilha_id, "poder_id": poder_id}
    conta = sessao.query(PontoRegular).filter_by(**filtro).first()
    if conta is None:
        conta = PontoRegular(**filtro, total=valor)
        sessao.add(conta)
    else:
        conta.total += valor
    sessao.flush()
    return conta


def debitar_ponto_regular(
    sessao: Session,
    *,
    guerreiro_id: uuid.UUID,
    valor: int,
    trilha_id: uuid.UUID | None = None,
    poder_id: uuid.UUID | None = None,
) -> PontoRegular:
    """Debita por **fato desfeito** — o estorno de registro de coleta
    invalidado e a ocorrência de conduta lançada (`RF-01-57`, `RF-01-69`,
    `ocorrencias_de_conduta.regra.lancar_ocorrencia_de_conduta`). Exige
    exatamente uma referência — trilha **ou** poder — e valor positivo, como
    o crédito; o saldo nunca fica negativo — o débito maior que o total para
    em zero (`RN-01-55`)."""
    if (trilha_id is None) == (poder_id is None):
        raise ErroDeValidacao(
            mensagem="Débito de ponto regular exige exatamente uma trilha ou um poder."
        )
    if valor <= 0:
        raise ErroDeValidacao(
            mensagem="Débito de ponto regular exige valor positivo.", campo="valor"
        )

    filtro = {"guerreiro_id": guerreiro_id, "trilha_id": trilha_id, "poder_id": poder_id}
    conta = sessao.query(PontoRegular).filter_by(**filtro).first()
    if conta is None:
        conta = PontoRegular(**filtro, total=0)
        sessao.add(conta)
    else:
        conta.total = max(0, conta.total - valor)
    sessao.flush()
    return conta


def _missoes_obrigatorias_da_trilha(sessao: Session, trilha_id: uuid.UUID) -> list[Missao]:
    return sessao.query(Missao).filter_by(trilha_id=trilha_id, obrigatoria=True).all()


def missoes_concluidas_pelo_guerreiro(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID
) -> set[uuid.UUID]:
    """As missões da trilha que o Guerreiro(a) já concluiu, derivadas dos
    `Resultado`s — pública porque `recompensas_de_marco.regra` também a
    chama, para verificar o marco alcançado sem duplicar a consulta
    (`RF-07-13`, design — Decisions)."""
    linhas = (
        sessao.query(Missao.id)
        .join(Atividade, Atividade.missao_id == Missao.id)
        .join(Resultado, Resultado.atividade_id == Atividade.id)
        .filter(Missao.trilha_id == trilha_id, Resultado.guerreiro_id == guerreiro_id)
        .distinct()
        .all()
    )
    return {linha[0] for linha in linhas}


def _ja_certificado(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID, valor: int
) -> bool:
    return (
        sessao.query(Nivel)
        .filter_by(guerreiro_id=guerreiro_id, trilha_id=trilha_id, valor=valor)
        .first()
        is not None
    )


def _certificar_nivel(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID, valor: int
) -> None:
    """Nível conquistado nunca regride: o registro nasce e nunca é
    removido, mesmo que o critério deixe de valer depois (`RF-01-21`,
    design — decisões). Concede junto o badge de nível correspondente
    (`RF-01-21`, 11 §7)."""
    sessao.add(Nivel(guerreiro_id=guerreiro_id, trilha_id=trilha_id, valor=valor))
    sessao.add(Badge(guerreiro_id=guerreiro_id, trilha_id=trilha_id, tipo=TipoDeBadge.de_nivel))
    sessao.flush()


def _tem_merito_de_auxilio_na_trilha(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID
) -> bool:
    return (
        sessao.query(Resultado)
        .join(Atividade, Atividade.id == Resultado.atividade_id)
        .join(Missao, Missao.id == Atividade.missao_id)
        .filter(
            Missao.trilha_id == trilha_id,
            Resultado.guerreiro_id == guerreiro_id,
            Resultado.desfecho == DesfechoDoResultado.merito_extra_por_auxilio,
        )
        .first()
        is not None
    )


def avaliar_niveis(sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID) -> None:
    """Certifica os níveis 1, 2 e 4 quando o critério verificável do
    documento 11 §6 é atingido pela primeira vez — 3 depende de entidade de
    outro PRD e fica fora desta fatia (proposta — o que esta fatia não
    tem); o 5 é `certificar_nivel_5`, disparado pela validação da criação
    original, não por Resultado. Só a missão obrigatória conta no percurso
    (11 §6)."""
    obrigatorias = _missoes_obrigatorias_da_trilha(sessao, trilha_id)
    concluidas = missoes_concluidas_pelo_guerreiro(
        sessao, guerreiro_id=guerreiro_id, trilha_id=trilha_id
    )

    if concluidas and not _ja_certificado(
        sessao, guerreiro_id=guerreiro_id, trilha_id=trilha_id, valor=NIVEL_1
    ):
        _certificar_nivel(sessao, guerreiro_id=guerreiro_id, trilha_id=trilha_id, valor=NIVEL_1)

    if not obrigatorias:
        return

    # Só a missão obrigatória conta no percurso (11 §6): a opcional pontua,
    # mas fica fora do denominador e do numerador de nível 2 e 4.
    ids_das_obrigatorias = {missao.id for missao in obrigatorias}
    concluidas_obrigatorias = concluidas & ids_das_obrigatorias

    # 1/3 arredondado para cima (definição do fundador): garante que o
    # nível 2 sempre exija progresso real, mesmo com poucas obrigatórias.
    limiar_do_nivel_2 = math.ceil(len(obrigatorias) / 3)
    if len(concluidas_obrigatorias) >= limiar_do_nivel_2 and not _ja_certificado(
        sessao, guerreiro_id=guerreiro_id, trilha_id=trilha_id, valor=NIVEL_2
    ):
        _certificar_nivel(sessao, guerreiro_id=guerreiro_id, trilha_id=trilha_id, valor=NIVEL_2)

    todas_obrigatorias_concluidas = ids_das_obrigatorias <= concluidas_obrigatorias
    if (
        todas_obrigatorias_concluidas
        and not _ja_certificado(
            sessao, guerreiro_id=guerreiro_id, trilha_id=trilha_id, valor=NIVEL_4
        )
        and _tem_merito_de_auxilio_na_trilha(sessao, guerreiro_id=guerreiro_id, trilha_id=trilha_id)
    ):
        _certificar_nivel(sessao, guerreiro_id=guerreiro_id, trilha_id=trilha_id, valor=NIVEL_4)


def conceder_badge_de_valores_e_causas(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID
) -> None:
    """Concedido uma vez por trilha — Resultados seguintes da mesma
    natureza não duplicam o badge (`RF-01-21`, 11 §7)."""
    ja_tem = (
        sessao.query(Badge)
        .filter_by(
            guerreiro_id=guerreiro_id, trilha_id=trilha_id, tipo=TipoDeBadge.de_valores_e_causas
        )
        .first()
    )
    if ja_tem is not None:
        return
    sessao.add(
        Badge(guerreiro_id=guerreiro_id, trilha_id=trilha_id, tipo=TipoDeBadge.de_valores_e_causas)
    )
    sessao.flush()


def creditar_pontuacao_do_resultado(
    sessao: Session, *, resultado: Resultado, atividade: Atividade, trilha: Trilha
) -> None:
    """Ponto de entrada único, chamado por
    `resultados.regra.registrar_resultado`: credita o ponto regular,
    reavalia nível e concede o badge de valores/causas quando a natureza da
    atividade for essa (`RF-01-20`, `RF-01-21`, 11 §§4, 5, 6, 7)."""
    valor = _valor_regular(atividade, resultado.desfecho)
    creditar_ponto_regular(
        sessao, guerreiro_id=resultado.guerreiro_id, trilha_id=trilha.id, valor=valor
    )
    avaliar_niveis(sessao, guerreiro_id=resultado.guerreiro_id, trilha_id=trilha.id)
    if atividade.natureza == NATUREZA_DE_VALORES_E_CAUSAS:
        conceder_badge_de_valores_e_causas(
            sessao, guerreiro_id=resultado.guerreiro_id, trilha_id=trilha.id
        )


def certificar_nivel_5(sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID) -> None:
    """Certificado quando a criação original da trilha é validada — ao
    contrário dos níveis 1, 2 e 4, não depende de missão obrigatória
    (`RF-01-21`, 11 §6). Reaproveita `_certificar_nivel`, que também
    concede o badge de nível correspondente e nunca regride."""
    if _ja_certificado(sessao, guerreiro_id=guerreiro_id, trilha_id=trilha_id, valor=NIVEL_5):
        return
    _certificar_nivel(sessao, guerreiro_id=guerreiro_id, trilha_id=trilha_id, valor=NIVEL_5)


def creditar_pontuacao_da_coleta(
    sessao: Session,
    *,
    registro: RegistroDeColeta,
    serie: SerieDeColeta,
    desafio: DesafioDeColeta,
    periodo_inicio: datetime,
    periodo_fim: datetime,
) -> int:
    """Ponto de entrada único, chamado por
    `coletas.regra.gravar_registro_de_coleta`: credita ao **Poder do
    Território** — identificado pelo papel declarado no catálogo, nunca ao
    poder da trilha em que o desafio nasceu —, respeitando quantos
    registros do período de cadência pontuam (`RF-08-09`, `RN-08-05`,
    `RN-08-06`, `RN-08-15`, `RN-01-54`). Devolve o valor efetivamente
    creditado — zero quando o registro excede a cota do período; ele
    permanece válido de qualquer forma, só não credita.

    `periodo_inicio`/`periodo_fim` vêm já apurados por
    `coletas.regra.periodo_de_cadencia`, para que este módulo não precise
    importar de volta o módulo que o chama (evita ciclo de import).
    """
    poder_do_territorio = buscar_poder_do_territorio(sessao)
    if poder_do_territorio is None:
        raise PoderDoTerritorioNaoDeclarado()

    ja_pontuaram = (
        sessao.query(func.count(RegistroDeColeta.id))
        .filter(
            RegistroDeColeta.serie_de_coleta_id == serie.id,
            RegistroDeColeta.pontos_creditados > 0,
            RegistroDeColeta.momento_do_fato >= periodo_inicio,
            RegistroDeColeta.momento_do_fato < periodo_fim,
        )
        .scalar()
    )
    if ja_pontuaram >= desafio.registros_que_pontuam_por_periodo:
        return 0

    creditar_ponto_regular(
        sessao,
        guerreiro_id=serie.coletor_id,
        poder_id=poder_do_territorio.id,
        valor=VALOR_DO_REGISTRO_DE_COLETA,
    )
    return VALOR_DO_REGISTRO_DE_COLETA


def estornar_pontuacao_da_coleta(
    sessao: Session, *, registro: RegistroDeColeta, serie: SerieDeColeta
) -> None:
    """Ponto de entrada único, chamado por
    `coletas.regra.invalidar_registro_de_coleta`: estorna ao **Poder do
    Território** do coletor exatamente o que `registro.pontos_creditados`
    diz que aquele registro creditou — o próprio campo é a fonte do
    estorno, sem livro-razão por evento (`RF-08-13`, `RN-08-09`, design —
    decisão 1). Não faz nada quando o registro nada creditou, como o "a
    conferir" ainda não confirmado e o excedente da quantidade do período
    (`RN-08-26`)."""
    if registro.pontos_creditados <= 0:
        return

    poder_do_territorio = buscar_poder_do_territorio(sessao)
    if poder_do_territorio is None:
        raise PoderDoTerritorioNaoDeclarado()

    debitar_ponto_regular(
        sessao,
        guerreiro_id=serie.coletor_id,
        poder_id=poder_do_territorio.id,
        valor=registro.pontos_creditados,
    )


def conceder_badge_de_autoria(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID
) -> None:
    """Concedido a cada integrante da equipe cuja criação original for
    validada; sem guarda de duplicidade porque a unicidade de
    `CriacaoOriginal` por equipe já impede validar a mesma trilha duas
    vezes para a mesma equipe (`RF-01-21`, `RF-01-64`, 11 §7, design —
    decisões)."""
    sessao.add(Badge(guerreiro_id=guerreiro_id, trilha_id=trilha_id, tipo=TipoDeBadge.de_autoria))
    sessao.flush()


def conceder_badge_de_protagonismo(sessao: Session, *, guerreiro_id: uuid.UUID) -> None:
    """Único badge global (`RN-01-50`): concedido ao autor da sugestão
    adotada, sem trilha nem poder, e uma única vez por autor (`RF-01-21`,
    11 §7)."""
    ja_tem = (
        sessao.query(Badge)
        .filter_by(guerreiro_id=guerreiro_id, tipo=TipoDeBadge.de_protagonismo)
        .first()
    )
    if ja_tem is not None:
        return
    sessao.add(Badge(guerreiro_id=guerreiro_id, tipo=TipoDeBadge.de_protagonismo))
    sessao.flush()


def apurar_partida_de_quiz(sessao: Session, *, partida: PartidaDeQuiz) -> dict[uuid.UUID, int]:
    """Apuração por equipe disputante, já com o teto da partida aplicado —
    1 por acerto e 1 de bônus à primeira a acertar cada pergunta, pela
    ordem de chegada ao servidor (`RF-01-21`, `RF-01-36`, 11 §5).

    É **leitura**: nada credita. Serve tanto ao placar ao vivo da App 03,
    com a partida ainda aberta, quanto ao crédito do encerramento — o mesmo
    cálculo nos dois, para que o painel não divirja do que foi creditado
    (design — decisão 1, riscos). Pergunta anulada fica fora, lida da
    tabela de anulação e não da marca da resposta, que é só a projeção
    consultável (design — decisão 6).
    """
    apuracao: dict[uuid.UUID, int] = dict.fromkeys(
        (
            linha.equipe_id
            for linha in sessao.query(EquipeNaPartida).filter_by(partida_id=partida.id).all()
        ),
        0,
    )
    anuladas = {
        linha.pergunta_id
        for linha in sessao.query(PerguntaAnuladaNaPartida).filter_by(partida_id=partida.id).all()
    }

    # `(momento_de_chegada, id)`: o `id` só desempata dois carimbos
    # idênticos ao microssegundo, e é o que torna a apuração reproduzível
    # em vez de arbitrária (design — decisão 2).
    respostas = (
        sessao.query(RespostaDeQuiz, PerguntaDeQuiz.alternativa_correta)
        .join(PerguntaDeQuiz, PerguntaDeQuiz.id == RespostaDeQuiz.pergunta_id)
        .filter(RespostaDeQuiz.partida_id == partida.id)
        .order_by(RespostaDeQuiz.momento_de_chegada, RespostaDeQuiz.id)
        .all()
    )

    perguntas_com_primeira_acertada: set[uuid.UUID] = set()
    for resposta, alternativa_correta in respostas:
        if resposta.pergunta_id in anuladas:
            continue
        if resposta.alternativa_escolhida != alternativa_correta:
            continue
        valor = VALOR_POR_ACERTO_NO_QUIZ
        if resposta.pergunta_id not in perguntas_com_primeira_acertada:
            perguntas_com_primeira_acertada.add(resposta.pergunta_id)
            valor += BONUS_DA_PRIMEIRA_A_ACERTAR
        apuracao[resposta.equipe_id] = apuracao.get(resposta.equipe_id, 0) + valor

    return {
        equipe_id: min(TETO_DE_PONTO_POR_PARTIDA_DE_QUIZ, total)
        for equipe_id, total in apuracao.items()
    }


def creditar_pontuacao_da_partida_de_quiz(
    sessao: Session, *, partida: PartidaDeQuiz, trilha: Trilha
) -> None:
    """Ponto de entrada único, chamado por `quiz.regra.encerrar_partida`:
    credita o valor apurado integral a **cada integrante** da equipe, sem
    rateio pelo tamanho, na trilha derivada da atividade da partida
    (`RF-01-21`, `RN-01-42`, 11 §5).

    Reaproveita `creditar_ponto_regular`, o mesmo ponto de entrada da
    criação original — e portanto o mesmo respeito ao gatilho que recusa
    débito (`RN-01-38`). A régua do valor é própria do quiz e não passa por
    `_valor_regular`, que é a do Resultado (design — decisão 5). Equipe sem
    acerto não entra: crédito de valor não positivo é recusado por
    `creditar_ponto_regular`, e nada é debitado.
    """
    for equipe_id, valor in apurar_partida_de_quiz(sessao, partida=partida).items():
        if valor <= 0:
            continue
        integrantes = sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe_id).all()
        for integrante in integrantes:
            creditar_ponto_regular(
                sessao, guerreiro_id=integrante.persona_id, trilha_id=trilha.id, valor=valor
            )


def consulta_de_ranking(
    sessao: Session,
    *,
    exigir_divulgacao: bool,
    comunidade_id: uuid.UUID | None = None,
    trilha_id: uuid.UUID | None = None,
    poder_id: uuid.UUID | None = None,
) -> Query:
    """A derivação única do ranking — soma de `PontoRegular`, recortada por
    trilha ou por poder quando declarado, menos o débito das ocorrências de
    `RF-02-100` —, extraída de `vitrine.rotas.ranking_publico` para que o
    ranking logado da turma (`RF-05-52`, `RF-05-53`) a reaproveite sem
    duplicar a regra do ciclo encerrado (design — Decisions). `Persona.id`
    desempata o `row_number()` de forma determinística quando o total
    empata. O portão da divulgação é opcional: o ranking público sempre o
    exige, e o ranking da turma sempre o dispensa (`RN-05-16`)."""
    filtro_do_recorte = []
    if trilha_id is not None:
        filtro_do_recorte.append(PontoRegular.trilha_id == trilha_id)
    if poder_id is not None:
        filtro_do_recorte.append(PontoRegular.poder_id == poder_id)

    totais = (
        sessao.query(
            PontoRegular.guerreiro_id.label("guerreiro_id"),
            func.sum(PontoRegular.total).label("total"),
        )
        .filter(*filtro_do_recorte)
        .group_by(PontoRegular.guerreiro_id)
        .subquery()
    )
    debitos_de_ciclo_encerrado = (
        sessao.query(
            OcorrenciaDeConduta.guerreiro_id.label("guerreiro_id"),
            func.sum(OcorrenciaDeConduta.valor_debitado).label("total"),
        )
        .filter(OcorrenciaDeConduta.encerrada_em.is_not(None))
        .group_by(OcorrenciaDeConduta.guerreiro_id)
        .subquery()
    )
    total_expr = func.coalesce(totais.c.total, 0) + func.coalesce(
        debitos_de_ciclo_encerrado.c.total, 0
    )
    posicao_expr = func.row_number().over(order_by=[total_expr.desc(), Persona.id]).label("posicao")

    consulta = (
        sessao.query(
            Persona.id.label("persona_id"),
            Persona.avatar.label("avatar"),
            Nick.valor.label("nick"),
            total_expr.label("total"),
            posicao_expr,
        )
        .join(Nick, Nick.persona_id == Persona.id)
        .outerjoin(totais, totais.c.guerreiro_id == Persona.id)
        .outerjoin(
            debitos_de_ciclo_encerrado, debitos_de_ciclo_encerrado.c.guerreiro_id == Persona.id
        )
        .filter(Persona.papel == Papel.guerreiro)
    )
    if exigir_divulgacao:
        consulta = consulta.filter(condicao_de_autorizacao_vigente(sessao, Persona.id))
    if comunidade_id is not None:
        consulta = filtrar_personas_por_comunidade(consulta, comunidade_id)
    return consulta


def creditar_pontuacao_da_criacao_original(
    sessao: Session, *, criacao_original: CriacaoOriginal, trilha: Trilha
) -> None:
    """Ponto de entrada único, chamado por
    `criacoes_originais.regra.validar_criacao_original`: credita os 50
    pontos regulares integrais a cada integrante da equipe da trilha, sem
    rateio pelo tamanho, certifica o nível 5 e concede o badge de autoria a
    cada um deles (`RF-01-21`, `RF-01-64`, 11 §§5-7)."""
    integrantes = (
        sessao.query(IntegranteDaEquipe).filter_by(equipe_id=criacao_original.equipe_id).all()
    )
    for integrante in integrantes:
        creditar_ponto_regular(
            sessao,
            guerreiro_id=integrante.persona_id,
            trilha_id=trilha.id,
            valor=VALOR_DA_CRIACAO_ORIGINAL,
        )
        certificar_nivel_5(sessao, guerreiro_id=integrante.persona_id, trilha_id=trilha.id)
        conceder_badge_de_autoria(sessao, guerreiro_id=integrante.persona_id, trilha_id=trilha.id)
