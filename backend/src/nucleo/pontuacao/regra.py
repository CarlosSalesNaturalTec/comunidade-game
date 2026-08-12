import math
import uuid

from sqlalchemy.orm import Session

from ..criacoes_originais.modelo import CriacaoOriginal
from ..erros import ErroDeValidacao
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
# integrais — sem equipe nesta fatia (proposta — o que esta fatia não tem).
VALOR_DA_CRIACAO_ORIGINAL = 50

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
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID, valor: int
) -> PontoRegular:
    """Só credita — nunca debita, em nenhuma operação (`RF-01-57`,
    `RN-01-38`); o gatilho de `pontuacao.modelo` recusa qualquer redução."""
    if valor <= 0:
        raise ErroDeValidacao(
            mensagem="Crédito de ponto regular exige valor positivo.", campo="valor"
        )

    conta = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro_id, trilha_id=trilha_id).first()
    )
    if conta is None:
        conta = PontoRegular(guerreiro_id=guerreiro_id, trilha_id=trilha_id, total=valor)
        sessao.add(conta)
    else:
        conta.total += valor
    sessao.flush()
    return conta


def _missoes_obrigatorias_da_trilha(sessao: Session, trilha_id: uuid.UUID) -> list[Missao]:
    return sessao.query(Missao).filter_by(trilha_id=trilha_id, obrigatoria=True).all()


def _missoes_concluidas_pelo_guerreiro(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID
) -> set[uuid.UUID]:
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
    concluidas = _missoes_concluidas_pelo_guerreiro(
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


def conceder_badge_de_autoria(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID
) -> None:
    """Concedido a cada criação original validada; sem guarda de
    duplicidade porque a unicidade de `CriacaoOriginal` por (autor, trilha)
    já impede validar a mesma trilha duas vezes (`RF-01-21`, 11 §7, design
    — decisões)."""
    sessao.add(Badge(guerreiro_id=guerreiro_id, trilha_id=trilha_id, tipo=TipoDeBadge.de_autoria))
    sessao.flush()


def creditar_pontuacao_da_criacao_original(
    sessao: Session, *, criacao_original: CriacaoOriginal, trilha: Trilha
) -> None:
    """Ponto de entrada único, chamado por
    `criacoes_originais.regra.validar_criacao_original`: credita os 50
    pontos regulares integrais, certifica o nível 5 e concede o badge de
    autoria (`RF-01-21`, 11 §§5-7)."""
    creditar_ponto_regular(
        sessao,
        guerreiro_id=criacao_original.autor_id,
        trilha_id=trilha.id,
        valor=VALOR_DA_CRIACAO_ORIGINAL,
    )
    certificar_nivel_5(sessao, guerreiro_id=criacao_original.autor_id, trilha_id=trilha.id)
    conceder_badge_de_autoria(sessao, guerreiro_id=criacao_original.autor_id, trilha_id=trilha.id)
