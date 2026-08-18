import uuid
from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..armazenamento.fabrica import dependencia_de_armazenamento
from ..armazenamento.porta import PortaDeArmazenamento
from ..aulas.modelo import Aula
from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import ErroDeValidacao
from ..fila.modelo import SolicitacaoDeParticipacao
from ..livro_razao.modelo import DestinacaoDoAporte
from ..personas.modelo import Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import TipoDeRecurso
from .modelo import Aporte, FormaDeAporte
from .regra import registrar_aporte, registrar_aporte_por_absorcao

roteador = APIRouter()


class AporteSaida(BaseModel):
    id: uuid.UUID
    provedor_id: uuid.UUID
    tipo_de_recurso_id: uuid.UUID
    quantidade: Decimal
    ponto_de_apoio_id: uuid.UUID
    valor_em_moedas: Decimal
    forma: str
    origem_do_registro: str
    ressarcivel: bool
    situacao_de_ressarcimento: str
    destinacao: str
    aula_id: uuid.UUID | None
    lancamento_id: uuid.UUID
    data_do_aporte: date


def _saida(aporte: Aporte) -> AporteSaida:
    return AporteSaida(
        id=aporte.id,
        provedor_id=aporte.provedor_id,
        tipo_de_recurso_id=aporte.tipo_de_recurso_id,
        quantidade=aporte.quantidade,
        ponto_de_apoio_id=aporte.ponto_de_apoio_id,
        valor_em_moedas=aporte.valor_em_moedas,
        forma=aporte.forma.value,
        origem_do_registro=aporte.origem_do_registro.value,
        ressarcivel=aporte.ressarcivel,
        situacao_de_ressarcimento=aporte.situacao_de_ressarcimento.value,
        destinacao=aporte.destinacao.value,
        aula_id=aporte.aula_id,
        lancamento_id=aporte.lancamento_id,
        data_do_aporte=aporte.data_do_aporte,
    )


@roteador.post("/aportes", status_code=201)
def registrar_aporte_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
    provedor_id: Annotated[uuid.UUID, Form()],
    tipo_de_recurso_id: Annotated[uuid.UUID, Form()],
    quantidade: Annotated[Decimal, Form()],
    ponto_de_apoio_id: Annotated[uuid.UUID, Form()],
    data_do_aporte: Annotated[date, Form()],
    forma: Annotated[FormaDeAporte, Form()],
    destinacao: Annotated[DestinacaoDoAporte, Form()] = DestinacaoDoAporte.lastro,
    valor_de_origem: Annotated[Decimal | None, Form()] = None,
    periodo_apurado: Annotated[date | None, Form()] = None,
    solicitacao_de_participacao_id: Annotated[uuid.UUID | None, Form()] = None,
    comprovante: Annotated[UploadFile | None, File()] = None,
) -> AporteSaida:
    """Restrita ao Admin (`RF-07-04`, PRD-07 §9). Homologa e credita — a
    conversão em moedas é sempre pela vigência da **data do aporte**
    (`RF-07-05`). `destinacao` separa o que vira lastro do que não vira
    (`RF-07-23`, `RN-07-38`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    provedor = sessao_bd.get(Persona, provedor_id)
    tipo = sessao_bd.get(TipoDeRecurso, tipo_de_recurso_id)
    ponto_de_apoio = sessao_bd.get(PontoDeApoio, ponto_de_apoio_id)
    solicitacao_de_participacao = (
        sessao_bd.get(SolicitacaoDeParticipacao, solicitacao_de_participacao_id)
        if solicitacao_de_participacao_id is not None
        else None
    )
    conteudo = comprovante.file.read() if comprovante is not None else None

    aporte = registrar_aporte(
        sessao_bd,
        operador=operador,
        provedor=provedor,
        tipo=tipo,
        quantidade=quantidade,
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=data_do_aporte,
        forma=forma,
        destinacao=destinacao,
        valor_de_origem=valor_de_origem,
        periodo_apurado=periodo_apurado,
        solicitacao_de_participacao=solicitacao_de_participacao,
        comprovante_conteudo=conteudo,
        comprovante_nome_original=comprovante.filename if comprovante is not None else None,
        comprovante_tipo=comprovante.content_type if comprovante is not None else None,
        armazenamento=armazenamento,
    )
    sessao_bd.commit()
    return _saida(aporte)


@roteador.post("/aportes/absorcao", status_code=201)
def registrar_aporte_por_absorcao_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
    tipo_de_recurso_id: Annotated[uuid.UUID, Form()],
    quantidade: Annotated[Decimal, Form()],
    ponto_de_apoio_id: Annotated[uuid.UUID, Form()],
    data_do_aporte: Annotated[date, Form()],
    aula_id: Annotated[uuid.UUID | None, Form()] = None,
    valor_de_origem: Annotated[Decimal | None, Form()] = None,
    periodo_apurado: Annotated[date | None, Form()] = None,
    comprovante: Annotated[UploadFile | None, File()] = None,
) -> AporteSaida:
    """Restrita a Mestre ou Admin, sempre em nome de quem registra — a
    absorção credita no ato, sem homologação (`RF-07-06`, `RN-07-35`,
    PRD-07 §9). `aula_id`, quando declarada, é a necessidade publicada que
    a absorção assume (`RF-07-28`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    tipo = sessao_bd.get(TipoDeRecurso, tipo_de_recurso_id)
    ponto_de_apoio = sessao_bd.get(PontoDeApoio, ponto_de_apoio_id)
    aula = sessao_bd.get(Aula, aula_id) if aula_id is not None else None
    if aula_id is not None and aula is None:
        raise ErroDeValidacao(mensagem="Aula não encontrada.", campo="aula_id")
    conteudo = comprovante.file.read() if comprovante is not None else None

    aporte = registrar_aporte_por_absorcao(
        sessao_bd,
        operador=operador,
        tipo=tipo,
        quantidade=quantidade,
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=data_do_aporte,
        aula=aula,
        valor_de_origem=valor_de_origem,
        periodo_apurado=periodo_apurado,
        comprovante_conteudo=conteudo,
        comprovante_nome_original=comprovante.filename if comprovante is not None else None,
        comprovante_tipo=comprovante.content_type if comprovante is not None else None,
        armazenamento=armazenamento,
    )
    sessao_bd.commit()
    return _saida(aporte)
