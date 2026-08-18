import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from ..armazenamento.porta import PortaDeArmazenamento
from ..erros import ErroDeValidacao, PermissaoNegada
from ..fila.modelo import SolicitacaoDeParticipacao
from ..livro_razao.regra import lancar_credito
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import TipoDeRecurso
from ..recursos.regra import consultar_valor_de_referencia
from ..reservas.regra import confirmar_aulas_pendentes
from .modelo import Aporte, FormaDeAporte, OrigemDoRegistro, SituacaoDeRessarcimento

_FORMATOS_DE_COMPROVANTE_ACEITOS = frozenset({"application/pdf", "image/jpeg", "image/png"})

_MENSAGEM_TIPO_INEXISTENTE = (
    "Tipo de recurso não encontrado. Cadastre-o em POST /v1/tipos-de-recurso e registre "
    "o aporte de novo."
)


def _valorar_em_moedas(
    sessao: Session, *, tipo: TipoDeRecurso, quantidade: Decimal, data: date
) -> Decimal:
    """Converte pela vigência do valor de referência **na data do aporte**,
    nunca na data do registro (`RF-07-05`, `RN-07-03`, design — Decisions
    8)."""
    referencia = consultar_valor_de_referencia(sessao, tipo=tipo, data=data)
    if referencia is None:
        raise ErroDeValidacao(
            mensagem="Nenhuma vigência do valor de referência cobre a data do aporte.",
            campo="data_do_aporte",
        )
    return (quantidade * referencia.valor_em_moedas).quantize(Decimal("0.01"))


def _processar_comprovante(
    *,
    tipo: TipoDeRecurso,
    conteudo: bytes | None,
    nome_original: str | None,
    tipo_mime: str | None,
    armazenamento: PortaDeArmazenamento | None,
) -> tuple[str | None, str | None, str | None, int | None]:
    """PDF, JPG ou PNG, pelo caminho da porta de armazenamento — os mesmos
    quatro campos que `SolicitacaoDeParticipacao` já guarda (`RN-07-22`,
    design — Decisions 7)."""
    if conteudo is None:
        if tipo.exige_comprovante:
            raise ErroDeValidacao(
                mensagem="Este tipo de recurso exige comprovante.", campo="comprovante"
            )
        return None, None, None, None

    if tipo_mime not in _FORMATOS_DE_COMPROVANTE_ACEITOS:
        raise ErroDeValidacao(
            mensagem="Comprovante aceito apenas em PDF, JPG ou PNG.", campo="comprovante"
        )
    if armazenamento is None:
        raise ErroDeValidacao(mensagem="Porta de armazenamento não disponível.")

    referencia = f"aportes/{uuid.uuid4()}"
    armazenamento.gravar(referencia=referencia, conteudo=conteudo)
    return referencia, nome_original, tipo_mime, len(conteudo)


def _registrar_aporte_base(
    sessao: Session,
    *,
    operador: Persona,
    provedor: Persona,
    tipo: TipoDeRecurso | None,
    quantidade: Decimal | None,
    ponto_de_apoio: PontoDeApoio | None,
    data_do_aporte: date | None,
    forma: FormaDeAporte,
    origem_do_registro: OrigemDoRegistro,
    ressarcivel: bool,
    situacao_de_ressarcimento: SituacaoDeRessarcimento,
    admin_homologador_id: uuid.UUID | None,
    solicitacao_de_participacao_id: uuid.UUID | None = None,
    valor_de_origem: Decimal | None = None,
    periodo_apurado: date | None = None,
    comprovante_conteudo: bytes | None = None,
    comprovante_nome_original: str | None = None,
    comprovante_tipo: str | None = None,
    armazenamento: PortaDeArmazenamento | None = None,
) -> Aporte:
    if tipo is None:
        raise ErroDeValidacao(mensagem=_MENSAGEM_TIPO_INEXISTENTE, campo="tipo_de_recurso_id")
    if quantidade is None or quantidade <= 0:
        raise ErroDeValidacao(
            mensagem="Aporte exige quantidade maior que zero.", campo="quantidade"
        )
    if ponto_de_apoio is None:
        raise ErroDeValidacao(
            mensagem="Aporte exige o ponto de apoio de entrada.", campo="ponto_de_apoio_id"
        )
    if data_do_aporte is None:
        raise ErroDeValidacao(mensagem="Aporte exige a data.", campo="data_do_aporte")

    valor_em_moedas = _valorar_em_moedas(
        sessao, tipo=tipo, quantidade=quantidade, data=data_do_aporte
    )
    referencia, nome_original, tipo_mime, tamanho = _processar_comprovante(
        tipo=tipo,
        conteudo=comprovante_conteudo,
        nome_original=comprovante_nome_original,
        tipo_mime=comprovante_tipo,
        armazenamento=armazenamento,
    )

    lancamento = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=quantidade,
        valor_em_moedas=valor_em_moedas,
        operador=operador,
    )

    # O aporte que fecha a diferença confirma, no mesmo ato, toda aula
    # pendente de lastro que passe a ter disponível bastante — sem ato
    # humano de confirmação à parte, nas três formas que creditam: registro
    # da gestão, absorção e homologação do pré-cadastro (`RN-07-37`, design
    # — Decisions 5).
    confirmar_aulas_pendentes(sessao, tipo=tipo, ponto_de_apoio=ponto_de_apoio, operador=operador)

    aporte = Aporte(
        provedor_id=provedor.id,
        tipo_de_recurso_id=tipo.id,
        quantidade=quantidade,
        ponto_de_apoio_id=ponto_de_apoio.id,
        valor_em_moedas=valor_em_moedas,
        valor_de_origem=valor_de_origem,
        forma=forma,
        origem_do_registro=origem_do_registro,
        solicitacao_de_participacao_id=solicitacao_de_participacao_id,
        ressarcivel=ressarcivel,
        situacao_de_ressarcimento=situacao_de_ressarcimento,
        periodo_apurado=periodo_apurado,
        comprovante_referencia=referencia,
        comprovante_nome_original=nome_original,
        comprovante_tipo=tipo_mime,
        comprovante_tamanho=tamanho,
        admin_homologador_id=admin_homologador_id,
        lancamento_id=lancamento.id,
        data_do_aporte=data_do_aporte,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(aporte)
    sessao.flush()
    return aporte


def registrar_aporte(
    sessao: Session,
    *,
    operador: Persona,
    provedor: Persona | None,
    tipo: TipoDeRecurso | None,
    quantidade: Decimal | None,
    ponto_de_apoio: PontoDeApoio | None,
    data_do_aporte: date | None,
    forma: FormaDeAporte | None,
    valor_de_origem: Decimal | None = None,
    periodo_apurado: date | None = None,
    solicitacao_de_participacao: SolicitacaoDeParticipacao | None = None,
    comprovante_conteudo: bytes | None = None,
    comprovante_nome_original: str | None = None,
    comprovante_tipo: str | None = None,
    armazenamento: PortaDeArmazenamento | None = None,
) -> Aporte:
    """Só Admin registra pela rota da gestão (`RF-07-04`). Quem homologa não
    pode ser o provedor (`RN-07-16`); a solicitação de origem, quando
    apontada, é a homologação do que o pré-cadastro só declarou, e não pode
    ser homologada duas vezes (`RF-07-30`, `RN-07-21`)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin registra aporte pela rota da gestão.")
    if provedor is None:
        raise ErroDeValidacao(mensagem="Aporte exige o provedor.", campo="provedor_id")
    if provedor.id == operador.id:
        raise PermissaoNegada(mensagem="Quem homologa o aporte não pode ser o próprio provedor.")

    if solicitacao_de_participacao is not None:
        ja_homologada = (
            sessao.query(Aporte)
            .filter_by(solicitacao_de_participacao_id=solicitacao_de_participacao.id)
            .first()
        )
        if ja_homologada is not None:
            raise ErroDeValidacao(
                mensagem="Esta solicitação de participação já foi homologada.",
                campo="solicitacao_de_participacao_id",
            )
        origem_do_registro = OrigemDoRegistro.pre_cadastro
        solicitacao_id = solicitacao_de_participacao.id
    else:
        origem_do_registro = OrigemDoRegistro.gestao
        solicitacao_id = None

    return _registrar_aporte_base(
        sessao,
        operador=operador,
        provedor=provedor,
        tipo=tipo,
        quantidade=quantidade,
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=data_do_aporte,
        forma=forma,
        origem_do_registro=origem_do_registro,
        ressarcivel=False,
        situacao_de_ressarcimento=SituacaoDeRessarcimento.nao_se_aplica,
        admin_homologador_id=operador.id,
        solicitacao_de_participacao_id=solicitacao_id,
        valor_de_origem=valor_de_origem,
        periodo_apurado=periodo_apurado,
        comprovante_conteudo=comprovante_conteudo,
        comprovante_nome_original=comprovante_nome_original,
        comprovante_tipo=comprovante_tipo,
        armazenamento=armazenamento,
    )


def registrar_aporte_por_absorcao(
    sessao: Session,
    *,
    operador: Persona,
    tipo: TipoDeRecurso | None,
    quantidade: Decimal | None,
    ponto_de_apoio: PontoDeApoio | None,
    data_do_aporte: date | None,
    valor_de_origem: Decimal | None = None,
    periodo_apurado: date | None = None,
    comprovante_conteudo: bytes | None = None,
    comprovante_nome_original: str | None = None,
    comprovante_tipo: str | None = None,
    armazenamento: PortaDeArmazenamento | None = None,
) -> Aporte:
    """Só Mestre ou Admin, em nome de quem proveu — a absorção credita no
    ato, sem homologação, e nasce ressarcível com situação em aberto
    (`RF-07-06`, `RF-07-21`, `RN-07-06`, `RN-07-35`)."""
    if operador.papel not in (Papel.mestre, Papel.admin):
        raise PermissaoNegada(mensagem="Só Mestre ou Admin registram aporte por absorção.")

    return _registrar_aporte_base(
        sessao,
        operador=operador,
        provedor=operador,
        tipo=tipo,
        quantidade=quantidade,
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=data_do_aporte,
        forma=FormaDeAporte.absorcao,
        origem_do_registro=OrigemDoRegistro.gestao,
        ressarcivel=True,
        situacao_de_ressarcimento=SituacaoDeRessarcimento.em_aberto,
        admin_homologador_id=None,
        valor_de_origem=valor_de_origem,
        periodo_apurado=periodo_apurado,
        comprovante_conteudo=comprovante_conteudo,
        comprovante_nome_original=comprovante_nome_original,
        comprovante_tipo=comprovante_tipo,
        armazenamento=armazenamento,
    )
