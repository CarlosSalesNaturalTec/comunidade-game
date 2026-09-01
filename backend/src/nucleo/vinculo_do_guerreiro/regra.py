from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..aulas.modelo import Presenca
from ..biometria.modelo import GatilhoDeApagamento
from ..biometria.regra import marcar_apagamento
from ..coletas.modelo import RegistroDeColeta, SerieDeColeta
from ..erros import VinculoDoGuerreiroJaEncerrado
from ..personas.modelo import Papel, Persona
from ..resultados.modelo import Resultado
from ..tempo import agora
from .modelo import FimDeVinculo, OrigemDoFimDeVinculo

MESES_SEM_ATIVIDADE_PARA_VARREDURA = 12

MOTIVO_DA_VARREDURA = "Varredura automática: 12 meses sem nenhuma atividade registrada."


def _meses_atras(momento: datetime, meses: int) -> datetime:
    """12 meses antes de `momento` é exatamente um ano antes, no mesmo mês e
    dia — só o 29 de fevereiro sem ano bissexto correspondente recua ao dia
    28 (decisão do fundador, 2026-09-01)."""
    ano = momento.year - (meses // 12)
    try:
        return momento.replace(year=ano)
    except ValueError:
        return momento.replace(year=ano, day=28)


def encerrar_vinculo(
    sessao: Session, *, guerreiro: Persona, encerrado_por: Persona, motivo: str
) -> FimDeVinculo:
    """`RF-13-44`: ato de Admin — a matriz de permissões confere o papel na
    rota —, somente inserção, e 409 no vínculo já encerrado. Dispara o
    apagamento do _template_ em 30 dias, sem tocar em nenhum outro dado do
    Guerreiro(a).
    """
    ja_encerrado = sessao.query(FimDeVinculo).filter_by(guerreiro_id=guerreiro.id).first()
    if ja_encerrado is not None:
        raise VinculoDoGuerreiroJaEncerrado()

    fim = FimDeVinculo(
        guerreiro_id=guerreiro.id,
        origem=OrigemDoFimDeVinculo.admin,
        encerrado_por=encerrado_por.id,
        motivo=motivo,
    )
    sessao.add(fim)
    sessao.flush()

    marcar_apagamento(sessao, guerreiro_id=guerreiro.id, gatilho=GatilhoDeApagamento.fim_do_vinculo)
    return fim


def varrer_vinculos_vencidos(sessao: Session) -> int:
    """`RF-13-44`: encerra, sem depender de ato de ninguém, o vínculo de
    quem completou 12 meses sem a mais recente entre presença, resultado e
    coleta registrados — ou, sem nenhum dos três, 12 meses desde a criação
    da persona. Repetível: nunca encerra de novo quem já tem `FimDeVinculo`
    (decisão do fundador, 2026-09-01, documento 03 §12.2).
    """
    limite = _meses_atras(agora(), MESES_SEM_ATIVIDADE_PARA_VARREDURA)

    ja_encerrados = {linha[0] for linha in sessao.query(FimDeVinculo.guerreiro_id).all()}

    guerreiros = sessao.query(Persona).filter(Persona.papel == Papel.guerreiro).all()

    ultima_presenca = dict(
        sessao.query(Presenca.guerreiro_id, func.max(Presenca.momento_do_fato))
        .group_by(Presenca.guerreiro_id)
        .all()
    )
    ultimo_resultado = dict(
        sessao.query(Resultado.guerreiro_id, func.max(Resultado.momento_do_fato))
        .group_by(Resultado.guerreiro_id)
        .all()
    )
    ultima_coleta = dict(
        sessao.query(SerieDeColeta.coletor_id, func.max(RegistroDeColeta.momento_do_fato))
        .join(RegistroDeColeta, RegistroDeColeta.serie_de_coleta_id == SerieDeColeta.id)
        .group_by(SerieDeColeta.coletor_id)
        .all()
    )

    encerrados = 0
    for guerreiro in guerreiros:
        if guerreiro.id in ja_encerrados:
            continue

        candidatos = [
            data
            for data in (
                ultima_presenca.get(guerreiro.id),
                ultimo_resultado.get(guerreiro.id),
                ultima_coleta.get(guerreiro.id),
                guerreiro.criada_em,
            )
            if data is not None
        ]
        ultima_atividade = max(candidatos)
        if ultima_atividade >= limite:
            continue

        fim = FimDeVinculo(
            guerreiro_id=guerreiro.id,
            origem=OrigemDoFimDeVinculo.varredura,
            encerrado_por=None,
            motivo=MOTIVO_DA_VARREDURA,
        )
        sessao.add(fim)
        sessao.flush()
        marcar_apagamento(
            sessao, guerreiro_id=guerreiro.id, gatilho=GatilhoDeApagamento.fim_do_vinculo
        )
        encerrados += 1

    return encerrados
