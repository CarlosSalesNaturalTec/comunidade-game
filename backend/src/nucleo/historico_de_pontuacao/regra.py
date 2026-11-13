import uuid
from datetime import datetime

from sqlalchemy import and_, tuple_
from sqlalchemy.orm import Session

from ..comunidades.modelo import VinculoJogador
from ..comunidades.regra import comunidades_do_mestre
from ..erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..ocorrencias_de_conduta.modelo import OcorrenciaDeConduta
from ..paginacao import ParametrosDeListagem, codificar_cursor, decodificar_cursor
from ..personas.modelo import Papel, Persona
from ..poderes.modelo import Poder
from ..ponto_extra.modelo import PontoExtra
from ..pontuacao.modelo import PontoRegular
from ..trilhas.modelo import Trilha
from .modelo import LancamentoDePontuacao, OrigemDoLancamento


def autorizar_leitura_do_historico(
    sessao: Session, *, operador: Persona, guerreiro_id: uuid.UUID
) -> Persona:
    """Pela rota com identificador, leem o Admin, de qualquer Guerreiro(a),
    e o Mestre com vínculo vigente na comunidade dele; qualquer outro papel
    recebe 403 antes de saber se o Guerreiro(a) existe (`RN-01-68`)."""
    if operador.papel not in (Papel.admin, Papel.mestre):
        raise PermissaoNegada(
            mensagem="Só o Admin e o Mestre da comunidade leem o histórico de pontuação."
        )
    guerreiro = sessao.get(Persona, guerreiro_id)
    if guerreiro is None or guerreiro.papel != Papel.guerreiro:
        raise NaoEncontrado(mensagem="Guerreiro(a) não encontrado.")
    if operador.papel == Papel.admin:
        return guerreiro

    comunidades = comunidades_do_mestre(sessao, mestre=operador)
    vinculado = (
        sessao.query(VinculoJogador.id)
        .filter(
            VinculoJogador.guerreiro_id == guerreiro.id,
            VinculoJogador.data_fim.is_(None),
            VinculoJogador.comunidade_virtual_id.in_(comunidades),
        )
        .first()
        if comunidades
        else None
    )
    if vinculado is None:
        raise PermissaoNegada(
            mensagem="O Mestre lê só o histórico de Guerreiro(a) da comunidade do seu vínculo."
        )
    return guerreiro


def saldos_do_guerreiro(sessao: Session, *, guerreiro_id: uuid.UUID) -> dict:
    """O total regular de cada trilha ou poder, com o nome, e as duas contas
    de ponto extra — zero quando nunca pontuou (`RF-01-89`)."""
    linhas = (
        sessao.query(PontoRegular, Trilha.nome, Poder.nome)
        .outerjoin(Trilha, Trilha.id == PontoRegular.trilha_id)
        .outerjoin(Poder, Poder.id == PontoRegular.poder_id)
        .filter(PontoRegular.guerreiro_id == guerreiro_id)
        .order_by(PontoRegular.total.desc(), PontoRegular.id)
        .all()
    )
    regular = [
        {
            "trilha_id": conta.trilha_id,
            "poder_id": conta.poder_id,
            "nome": nome_da_trilha or nome_do_poder or "",
            "total": conta.total,
        }
        for conta, nome_da_trilha, nome_do_poder in linhas
    ]
    extra = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro_id).first()
    return {
        "regular": regular,
        "extra": {
            "acumulado": extra.acumulado if extra else 0,
            "saldo_disponivel": extra.saldo_disponivel if extra else 0,
        },
    }


def listar_lancamentos(
    sessao: Session, *, guerreiro_id: uuid.UUID, parametros: ParametrosDeListagem
) -> tuple[list[dict], str | None]:
    """Do mais recente ao mais antigo, paginado por `(registrado_em, id)`.
    O motivo da conduta vem da ocorrência, lido agora: apagado lá no fim da
    guarda, some aqui (`RF-01-89`, design — decisão 4)."""
    consulta = (
        sessao.query(LancamentoDePontuacao, Trilha.nome, Poder.nome, OcorrenciaDeConduta.motivo)
        .outerjoin(Trilha, Trilha.id == LancamentoDePontuacao.trilha_id)
        .outerjoin(Poder, Poder.id == LancamentoDePontuacao.poder_id)
        .outerjoin(
            OcorrenciaDeConduta,
            and_(
                LancamentoDePontuacao.origem == OrigemDoLancamento.ocorrencia_de_conduta,
                OcorrenciaDeConduta.id == LancamentoDePontuacao.referencia_id,
            ),
        )
        .filter(LancamentoDePontuacao.guerreiro_id == guerreiro_id)
    )
    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            momento = datetime.fromisoformat(posicao["registrado_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError, TypeError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(LancamentoDePontuacao.registrado_em, LancamentoDePontuacao.id)
            < tuple_(momento, id_cursor)
        )

    linhas = (
        consulta.order_by(
            LancamentoDePontuacao.registrado_em.desc(), LancamentoDePontuacao.id.desc()
        )
        .limit(parametros.tamanho + 1)
        .all()
    )
    proximo_cursor = None
    if len(linhas) > parametros.tamanho:
        linhas = linhas[: parametros.tamanho]
        ultimo = linhas[-1][0]
        proximo_cursor = codificar_cursor(
            {"registrado_em": ultimo.registrado_em.isoformat(), "id": str(ultimo.id)}
        )

    itens = [
        {
            "id": lancamento.id,
            "registrado_em": lancamento.registrado_em,
            "conta": lancamento.conta,
            "origem": lancamento.origem,
            "valor": lancamento.valor,
            "valor_no_acumulado": lancamento.valor_no_acumulado,
            "trilha_id": lancamento.trilha_id,
            "poder_id": lancamento.poder_id,
            "nome_da_trilha_ou_poder": nome_da_trilha or nome_do_poder,
            "detalhe": lancamento.detalhe,
            "motivo": motivo,
        }
        for lancamento, nome_da_trilha, nome_do_poder, motivo in linhas
    ]
    return itens, proximo_cursor
