import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Persona
from ..tempo import DataHoraComFuso
from ..trilhas.modelo import Atividade
from .modelo import OcorrenciaDeConduta
from .regra import lancar_ocorrencia_de_conduta

roteador = APIRouter()


class LancarOcorrenciaDeCondutaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    guerreiro_id: uuid.UUID
    aula_id: uuid.UUID
    atividade_id: uuid.UUID
    motivo: str = Field(min_length=1)
    momento_do_fato: DataHoraComFuso


class OcorrenciaDeCondutaSaida(BaseModel):
    id: uuid.UUID
    guerreiro_id: uuid.UUID
    aula_id: uuid.UUID
    atividade_id: uuid.UUID
    valor: int
    motivo: str | None
    momento_do_fato: DataHoraComFuso


def _saida(ocorrencia: OcorrenciaDeConduta) -> OcorrenciaDeCondutaSaida:
    """O motivo apagado (expurgo futuro, `RN-01-52`) nunca volta em nenhuma
    rota — o campo já é `None` no modelo, e este `BaseModel` só reproduz o
    que lá está, sem esconder nada por decisão própria."""
    return OcorrenciaDeCondutaSaida(
        id=ocorrencia.id,
        guerreiro_id=ocorrencia.guerreiro_id,
        aula_id=ocorrencia.aula_id,
        atividade_id=ocorrencia.atividade_id,
        valor=ocorrencia.valor,
        motivo=ocorrencia.motivo,
        momento_do_fato=ocorrencia.momento_do_fato,
    )


@roteador.post("/ocorrencias-de-conduta", status_code=201)
def lancar_ocorrencia_de_conduta_rota(
    entrada: LancarOcorrenciaDeCondutaEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(
            exigir_permissao(
                Operacao.lancamentos_e_pontuacao_negativa_das_suas_atividades, "escreve"
            )
        ),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> OcorrenciaDeCondutaSaida:
    """Mestre autor da trilha da atividade, ou Admin: lança a ocorrência e
    debita o ponto regular na mesma operação, sem valor declarado pelo
    cliente e sem revisão de terceiro (`RF-09-46`, `RF-01-57`, `RN-09-08`,
    `RN-09-09`, 11 §5)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, entrada.aula_id)
    atividade = sessao_bd.get(Atividade, entrada.atividade_id)

    ocorrencia = lancar_ocorrencia_de_conduta(
        sessao_bd,
        operador=operador,
        aula=aula,
        atividade=atividade,
        guerreiro_id=entrada.guerreiro_id,
        motivo=entrada.motivo,
        momento_do_fato=entrada.momento_do_fato,
    )
    sessao_bd.commit()
    return _saida(ocorrencia)
