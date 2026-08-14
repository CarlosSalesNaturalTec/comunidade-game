import uuid
from datetime import datetime

from sqlalchemy.orm import Query, Session

from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Papel, Persona
from .modelo import ComunidadeVirtual, VinculoJogador


def criar_comunidade(
    sessao: Session,
    *,
    operador: Persona,
    nome: str | None,
    localizacao: str | None,
    granularidade_maxima: str | None,
) -> ComunidadeVirtual:
    """Só Admin cria a Comunidade Virtual, que nasce vazia (`RF-08-01`,
    `RN-08-01`)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin cria a Comunidade Virtual.")
    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem="Comunidade exige nome.", campo="nome")
    if not localizacao or not localizacao.strip():
        raise ErroDeValidacao(mensagem="Comunidade exige localização.", campo="localizacao")
    if not granularidade_maxima or not granularidade_maxima.strip():
        raise ErroDeValidacao(
            mensagem="Comunidade exige granularidade máxima.", campo="granularidade_maxima"
        )

    comunidade = ComunidadeVirtual(
        nome=nome,
        localizacao=localizacao,
        granularidade_maxima=granularidade_maxima,
        admin_criador_id=operador.id,
    )
    sessao.add(comunidade)
    sessao.flush()
    return comunidade


def abrir_vinculo(
    sessao: Session,
    *,
    guerreiro: Persona,
    comunidade_id: uuid.UUID,
) -> VinculoJogador:
    """Abre o vínculo vigente do Guerreiro(a) com a comunidade, recusando um
    segundo vigente (`RF-08-02`, `RN-08-02`, `RN-01-05`). O índice parcial
    único de `VinculoJogador` garante a unicidade sob concorrência; aqui a
    recusa é traduzida para mensagem simples antes de a gravação alcançar o
    banco (design — Decisions).
    """
    if guerreiro.papel != Papel.guerreiro:
        raise ErroDeValidacao(mensagem="Só o Guerreiro(a) tem vínculo de comunidade.")

    vigente = (
        sessao.query(VinculoJogador).filter_by(guerreiro_id=guerreiro.id, data_fim=None).first()
    )
    if vigente is not None:
        raise ErroDeValidacao(
            mensagem="Este Guerreiro(a) já tem um vínculo de comunidade vigente.",
            campo="comunidade_id",
        )

    vinculo = VinculoJogador(guerreiro_id=guerreiro.id, comunidade_virtual_id=comunidade_id)
    sessao.add(vinculo)
    sessao.flush()
    return vinculo


def resolver_vinculo_na_data(
    sessao: Session, *, guerreiro_id: uuid.UUID, data: datetime
) -> VinculoJogador | None:
    """Localiza o vínculo do Guerreiro(a) cujo intervalo `[data_inicio,
    data_fim)` contém `data` — `data_fim` nulo é tratado como aberto. É o
    que prende o registro de coleta à comunidade vigente **na data da
    medição**, e não à comunidade corrente do coletor (`RN-08-03`, design —
    decisões)."""
    return (
        sessao.query(VinculoJogador)
        .filter(
            VinculoJogador.guerreiro_id == guerreiro_id,
            VinculoJogador.data_inicio <= data,
            (VinculoJogador.data_fim.is_(None)) | (VinculoJogador.data_fim > data),
        )
        .first()
    )


def unir_vinculo_vigente(consulta: Query) -> Query:
    """Junta uma consulta que já tem `Persona` no `FROM` ao vínculo vigente
    de cada Guerreiro(a) — a junção que os seis pontos de leitura antigos
    dispensavam, lendo direto a coluna que saiu de `Persona` (`RN-01-05`,
    design — Decisions)."""
    return consulta.join(
        VinculoJogador,
        (VinculoJogador.guerreiro_id == Persona.id) & VinculoJogador.data_fim.is_(None),
    )


def filtrar_personas_por_comunidade(consulta: Query, comunidade_id: uuid.UUID) -> Query:
    """Filtro por comunidade sobre o vínculo vigente — substitui a
    comparação direta de `Persona.comunidade_virtual_id` nos seis pontos de
    leitura que a coluna deixou (`RN-01-05`, design — Decisions)."""
    return unir_vinculo_vigente(consulta).filter(
        VinculoJogador.comunidade_virtual_id == comunidade_id
    )
