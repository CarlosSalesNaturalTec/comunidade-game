import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from ..armazenamento.porta import PortaDeArmazenamento
from ..aulas.modelo import Aula, RecursoDeclaradoDaAula
from ..erros import (
    DeclaracaoDeAporteJaResolvida,
    ErroDeValidacao,
    MissaoDoApoiadorFechada,
    PermissaoNegada,
)
from ..fila.modelo import SolicitacaoDeParticipacao
from ..livro_razao.modelo import DestinacaoDoAporte
from ..livro_razao.regra import lancar_credito
from ..missoes_do_apoiador.modelo import MissaoDoApoiador, SituacaoDaMissao
from ..missoes_do_apoiador.regra import concluir_se_fechou
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import NaturezaDoRecurso, TipoDeRecurso
from ..recursos.regra import consultar_valor_de_referencia
from ..reservas.regra import confirmar_aulas_pendentes
from ..tempo import agora
from .modelo import (
    Aporte,
    AporteDeclarado,
    FormaDeAporte,
    OrigemDaEscolhaDoAporte,
    OrigemDoRegistro,
    SituacaoDaDeclaracao,
    SituacaoDeRessarcimento,
)

_NATUREZAS_COM_DESEMBOLSO = frozenset(
    {NaturezaDoRecurso.consumivel, NaturezaDoRecurso.duravel, NaturezaDoRecurso.financeiro}
)

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
    destinacao: DestinacaoDoAporte = DestinacaoDoAporte.lastro,
    aula: Aula | None = None,
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
    if forma == FormaDeAporte.absorcao and destinacao == DestinacaoDoAporte.ressarcimento:
        raise ErroDeValidacao(
            mensagem="Aporte por absorção não se destina a ressarcimento.", campo="destinacao"
        )
    if aula is not None:
        if forma != FormaDeAporte.absorcao:
            raise ErroDeValidacao(
                mensagem="Só o aporte por absorção declara a aula que atende.", campo="aula_id"
            )
        consome = (
            sessao.query(RecursoDeclaradoDaAula)
            .filter_by(aula_id=aula.id, tipo_de_recurso_id=tipo.id)
            .first()
        )
        if consome is None:
            raise ErroDeValidacao(
                mensagem="A aula declarada não consome este tipo de recurso.", campo="aula_id"
            )
        if ponto_de_apoio.id != aula.ponto_de_apoio_id:
            raise ErroDeValidacao(
                mensagem="O ponto de apoio não confere com o da aula declarada.",
                campo="ponto_de_apoio_id",
            )

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
        destinacao=destinacao,
    )

    if destinacao == DestinacaoDoAporte.lastro:
        # O aporte que fecha a diferença confirma, no mesmo ato, toda aula
        # pendente de lastro que passe a ter disponível bastante — sem ato
        # humano de confirmação à parte, nas três formas que creditam:
        # registro da gestão, absorção e homologação do pré-cadastro
        # (`RN-07-37`, design — Decisions 5). A receita destinada a
        # ressarcir não confirma aula: não vira lastro (`RN-07-38`).
        confirmar_aulas_pendentes(
            sessao, tipo=tipo, ponto_de_apoio=ponto_de_apoio, operador=operador
        )

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
        destinacao=destinacao,
        aula_id=aula.id if aula is not None else None,
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
    destinacao: DestinacaoDoAporte = DestinacaoDoAporte.lastro,
    aula: Aula | None = None,
    valor_de_origem: Decimal | None = None,
    periodo_apurado: date | None = None,
    solicitacao_de_participacao: SolicitacaoDeParticipacao | None = None,
    aporte_declarado: AporteDeclarado | None = None,
    comprovante_conteudo: bytes | None = None,
    comprovante_nome_original: str | None = None,
    comprovante_tipo: str | None = None,
    armazenamento: PortaDeArmazenamento | None = None,
) -> Aporte:
    """Só Admin registra pela rota da gestão (`RF-07-04`). Quem homologa não
    pode ser o provedor (`RN-07-16`); a solicitação de origem, quando
    apontada, é a homologação do que o pré-cadastro só declarou, e não pode
    ser homologada duas vezes (`RF-07-30`, `RN-07-21`). `aporte_declarado`
    é o mesmo desenho, para a declaração da App 08 (`RF-14-26`, `RN-14-07`,
    `RN-14-08`, design — Decisions 1, 2, 5). `destinacao` separa o que vira
    lastro do que não vira; a doação destinada a ressarcir credita o Poder
    Sustentador sem entrar em saldo (`RF-07-23`, `RN-07-38`)."""
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
    elif aporte_declarado is not None:
        if aporte_declarado.provedor_id == operador.id:
            raise PermissaoNegada(
                mensagem="Quem homologa o aporte não pode ser o próprio provedor."
            )
        if aporte_declarado.situacao != SituacaoDaDeclaracao.pendente:
            raise ErroDeValidacao(
                mensagem="Esta declaração de aporte já foi homologada.",
                campo="aporte_declarado_id",
            )
        if provedor.id != aporte_declarado.provedor_id:
            raise ErroDeValidacao(
                mensagem="O provedor precisa ser quem fez a declaração de origem.",
                campo="provedor_id",
            )
        origem_do_registro = OrigemDoRegistro.app_08
        solicitacao_id = None
    else:
        origem_do_registro = OrigemDoRegistro.gestao
        solicitacao_id = None

    aporte = _registrar_aporte_base(
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
        destinacao=destinacao,
        aula=aula,
        solicitacao_de_participacao_id=solicitacao_id,
        valor_de_origem=valor_de_origem,
        periodo_apurado=periodo_apurado,
        comprovante_conteudo=comprovante_conteudo,
        comprovante_nome_original=comprovante_nome_original,
        comprovante_tipo=comprovante_tipo,
        armazenamento=armazenamento,
    )

    if aporte_declarado is not None:
        aporte.aporte_declarado_id = aporte_declarado.id
        aporte_declarado.situacao = SituacaoDaDeclaracao.homologada
        aporte_declarado.resolvido_por_id = operador.id
        aporte_declarado.resolvido_em = agora()
        sessao.flush()

        if aporte_declarado.missao_do_apoiador_id is not None:
            # A mesma homologação abate o que falta e, fechando o saldo,
            # conclui a missão e credita os selos — um só ato, uma só
            # transação (`RF-14-65`, `RF-14-66`, design — Decisions 5).
            missao = sessao.get(MissaoDoApoiador, aporte_declarado.missao_do_apoiador_id)
            concluir_se_fechou(sessao, missao=missao)

    return aporte


def registrar_aporte_por_absorcao(
    sessao: Session,
    *,
    operador: Persona,
    tipo: TipoDeRecurso | None,
    quantidade: Decimal | None,
    ponto_de_apoio: PontoDeApoio | None,
    data_do_aporte: date | None,
    aula: Aula | None = None,
    destinacao: DestinacaoDoAporte = DestinacaoDoAporte.lastro,
    valor_de_origem: Decimal | None = None,
    periodo_apurado: date | None = None,
    comprovante_conteudo: bytes | None = None,
    comprovante_nome_original: str | None = None,
    comprovante_tipo: str | None = None,
    armazenamento: PortaDeArmazenamento | None = None,
) -> Aporte:
    """Só Mestre ou Admin, em nome de quem proveu — a absorção credita no
    ato, sem homologação (`RF-07-06`, `RN-07-06`, `RN-07-35`). Nasce
    ressarcível com situação em aberto, exceto a de tipo de natureza
    **serviço**, que nasce **não ressarcível**: quem absorve serviço dá
    tempo, não dinheiro, e não há desembolso a devolver (`RF-07-21`,
    `RN-07-39`, design — Decisions 6). O valor de origem em reais é
    exigido nas demais naturezas — houve desembolso — e fica vazio no
    serviço, cujo valor é o em moedas que a tabela já fornece (`RN-07-24`).
    `aula` é a necessidade publicada que a absorção assume, do PRD-07 §8
    (`RF-07-28`)."""
    if operador.papel not in (Papel.mestre, Papel.admin):
        raise PermissaoNegada(mensagem="Só Mestre ou Admin registram aporte por absorção.")

    eh_servico = tipo is not None and tipo.natureza == NaturezaDoRecurso.servico
    exige_valor_de_origem = (
        tipo is not None and tipo.natureza in _NATUREZAS_COM_DESEMBOLSO and valor_de_origem is None
    )
    if eh_servico:
        valor_de_origem = None
        ressarcivel = False
        situacao_de_ressarcimento = SituacaoDeRessarcimento.nao_se_aplica
    else:
        if exige_valor_de_origem:
            raise ErroDeValidacao(
                mensagem="Absorção deste tipo exige o valor de origem em reais.",
                campo="valor_de_origem",
            )
        ressarcivel = True
        situacao_de_ressarcimento = SituacaoDeRessarcimento.em_aberto

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
        ressarcivel=ressarcivel,
        situacao_de_ressarcimento=situacao_de_ressarcimento,
        admin_homologador_id=None,
        destinacao=destinacao,
        aula=aula,
        valor_de_origem=valor_de_origem,
        periodo_apurado=periodo_apurado,
        comprovante_conteudo=comprovante_conteudo,
        comprovante_nome_original=comprovante_nome_original,
        comprovante_tipo=comprovante_tipo,
        armazenamento=armazenamento,
    )


def _processar_comprovante_da_declaracao(
    *,
    conteudo: bytes | None,
    nome_original: str | None,
    tipo_mime: str | None,
    armazenamento: PortaDeArmazenamento | None,
) -> tuple[str, str | None, str, int]:
    """O comprovante é sempre obrigatório na declaração — sem exceção por
    tipo de recurso, como o aporte da gestão tem (`RN-14-06`, design —
    Decisions 7)."""
    if conteudo is None:
        raise ErroDeValidacao(
            mensagem="Comprovante obrigatório, em PDF, JPG ou PNG.", campo="comprovante"
        )
    if tipo_mime not in _FORMATOS_DE_COMPROVANTE_ACEITOS:
        raise ErroDeValidacao(
            mensagem="Comprovante aceito apenas em PDF, JPG ou PNG.", campo="comprovante"
        )
    if armazenamento is None:
        raise ErroDeValidacao(mensagem="Porta de armazenamento não disponível.")

    referencia = f"aportes-declarados/{uuid.uuid4()}"
    armazenamento.gravar(referencia=referencia, conteudo=conteudo)
    return referencia, nome_original, tipo_mime, len(conteudo)


def _validar_missao_para_declaracao(sessao: Session, missao: MissaoDoApoiador | None) -> None:
    """Missão concluída, vencida, despublicada ou inexistente não aceita
    nova declaração — a mensagem diz o que aconteceu com ela (`RF-14-63` a
    `RF-14-65`, `RN-14-32`)."""
    if missao is None:
        raise MissaoDoApoiadorFechada(mensagem="Esta missão não existe mais.")
    if missao.situacao == SituacaoDaMissao.concluida:
        raise MissaoDoApoiadorFechada(mensagem="Esta missão já foi concluída.")
    if missao.situacao == SituacaoDaMissao.despublicada:
        raise MissaoDoApoiadorFechada(mensagem="Esta missão foi despublicada.")
    if missao.prazo < agora().date():
        raise MissaoDoApoiadorFechada(mensagem="O prazo desta missão já venceu.")


def declarar_aporte(
    sessao: Session,
    *,
    provedor: Persona,
    valor_declarado: Decimal | None,
    forma: FormaDeAporte | None,
    origem_da_escolha: OrigemDaEscolhaDoAporte | None,
    aula: Aula | None = None,
    tipo: TipoDeRecurso | None = None,
    missao: MissaoDoApoiador | None = None,
    comprovante_conteudo: bytes | None = None,
    comprovante_nome_original: str | None = None,
    comprovante_tipo: str | None = None,
    armazenamento: PortaDeArmazenamento | None = None,
) -> AporteDeclarado:
    """A declaração do Apoiador em sessão: sempre em dinheiro, sempre
    pendente, sem lançamento, crédito ou abatimento até a homologação
    (`RF-14-25` a `RF-14-28`, `RN-14-05` a `RN-14-07`, design — Decisions
    1, 3, 7). A origem `necessidade` guarda o par aula + tipo de recurso
    que motivou a escolha, sem vínculo (design — Decisions 3). A origem
    `missao` guarda a missão escolhida, inteira ou em parte, recusando a
    fechada com 409 (`RF-14-63`, `RN-14-32`)."""
    if provedor.papel != Papel.apoiador:
        raise PermissaoNegada(mensagem="Só o Apoiador declara aporte pela App 08.")
    if forma is None or forma != FormaDeAporte.financeira:
        raise ErroDeValidacao(
            mensagem=(
                "O aporte pela aplicação é só em dinheiro. Material, serviço e "
                "divulgação entram pelo cadastro da gestão."
            ),
            campo="forma",
        )
    if valor_declarado is None or valor_declarado <= 0:
        raise ErroDeValidacao(
            mensagem="Declaração exige valor maior que zero.", campo="valor_declarado"
        )
    if origem_da_escolha is None:
        raise ErroDeValidacao(
            mensagem="Declaração exige a origem da escolha.", campo="origem_da_escolha"
        )
    if origem_da_escolha == OrigemDaEscolhaDoAporte.necessidade and (aula is None or tipo is None):
        raise ErroDeValidacao(
            mensagem="Declaração por necessidade exige a aula e o tipo de recurso escolhidos.",
            campo="aula_id",
        )
    if origem_da_escolha == OrigemDaEscolhaDoAporte.missao:
        _validar_missao_para_declaracao(sessao, missao)

    referencia, nome_original, tipo_mime, tamanho = _processar_comprovante_da_declaracao(
        conteudo=comprovante_conteudo,
        nome_original=comprovante_nome_original,
        tipo_mime=comprovante_tipo,
        armazenamento=armazenamento,
    )

    declaracao = AporteDeclarado(
        provedor_id=provedor.id,
        valor_declarado=valor_declarado,
        origem_da_escolha=origem_da_escolha,
        aula_id=aula.id if aula is not None else None,
        tipo_de_recurso_id=tipo.id if tipo is not None else None,
        missao_do_apoiador_id=missao.id if missao is not None else None,
        comprovante_referencia=referencia,
        comprovante_nome_original=nome_original,
        comprovante_tipo=tipo_mime,
        comprovante_tamanho=tamanho,
        situacao=SituacaoDaDeclaracao.pendente,
        autor_id=provedor.id,
        papel_do_autor=provedor.papel.value,
    )
    sessao.add(declaracao)
    sessao.flush()
    return declaracao


def recusar_declaracao_de_aporte(
    sessao: Session,
    declaracao: AporteDeclarado,
    *,
    operador: Persona,
    motivo: str | None,
) -> AporteDeclarado:
    """Só Admin recusa, com motivo obrigatório; a recusa não gera
    lançamento nem credita, e é terminal como a homologação (`RF-14-27`,
    `RN-14-07`, design — Decisions 5)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin recusa a declaração de aporte.")
    if motivo is None or not motivo.strip():
        raise ErroDeValidacao(mensagem="A recusa exige o motivo.", campo="motivo")
    if declaracao.situacao != SituacaoDaDeclaracao.pendente:
        raise DeclaracaoDeAporteJaResolvida()

    declaracao.situacao = SituacaoDaDeclaracao.recusada
    declaracao.motivo_da_recusa = motivo
    declaracao.resolvido_por_id = operador.id
    declaracao.resolvido_em = agora()
    sessao.flush()
    return declaracao
