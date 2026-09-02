from decimal import Decimal

from sqlalchemy.orm import Session

from ..comunidades.modelo import ComunidadeVirtual, VinculoJogador
from ..erros import ErroDeValidacao, PermissaoNegada
from ..livro_razao.regra import saldo_de
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import NaturezaDoRecurso, TipoDeRecurso
from ..recursos.regra import consultar_preco_de_referencia
from ..tempo import agora
from ..trocas.modelo import Troca
from .modelo import ItemDeCatalogoAvulso, OrigemDoCadastroDoItem, SituacaoDeHomologacao

ESTOQUE_MINIMO = Decimal("1")

_DECISOES_DE_HOMOLOGACAO = (SituacaoDeHomologacao.homologado, SituacaoDeHomologacao.recusado)
SITUACOES_QUE_NUNCA_ATIVAM = (SituacaoDeHomologacao.pendente, SituacaoDeHomologacao.recusado)


def falta_de_lastro(sessao: Session, *, item: ItemDeCatalogoAvulso) -> Decimal:
    """A diferença entre o estoque declarado e o saldo do tipo de recurso no
    ponto de apoio do item — zero ou negativo é lastro suficiente. Lê
    `saldo_de`, nunca `disponivel_de`: o item não compromete saldo entre
    encontros como a reserva da aula compromete, por `RN-07-27` (`RF-07-34`,
    `RN-07-26`, design — Decisions)."""
    disponivel = saldo_de(
        sessao,
        tipo_de_recurso_id=item.tipo_de_recurso_id,
        ponto_de_apoio_id=item.ponto_de_apoio_id,
    )
    return item.estoque - disponivel


def tem_preco_de_referencia_vigente(sessao: Session, *, item: ItemDeCatalogoAvulso) -> bool:
    tipo = sessao.get(TipoDeRecurso, item.tipo_de_recurso_id)
    return consultar_preco_de_referencia(sessao, tipo=tipo, data=agora().date()) is not None


def _recalcular_ativo(sessao: Session, *, item: ItemDeCatalogoAvulso) -> None:
    """`ativo` só é verdadeiro havendo homologação (ou dispensa dela), preço
    de referência vigente e lastro suficiente — recalculado em toda escrita
    que possa mudar qualquer uma das três condições, nunca por exceção: item
    sem lastro ou sem preço é gravado inativo, nunca recusado (`RF-07-34`,
    `RF-09-101`, `RN-07-26`, `RN-07-29`)."""
    if item.situacao_de_homologacao in SITUACOES_QUE_NUNCA_ATIVAM:
        item.ativo = False
        return
    if not tem_preco_de_referencia_vigente(sessao, item=item):
        item.ativo = False
        return
    item.ativo = falta_de_lastro(sessao, item=item) <= 0


def _exigir_admin_ou_mestre_vinculado(operador: Persona, item: ItemDeCatalogoAvulso) -> None:
    if operador.papel == Papel.admin:
        return
    if operador.papel == Papel.mestre:
        vinculo: VinculoJogador | None = operador.vinculo_vigente
        if vinculo is not None and vinculo.comunidade_virtual_id == item.comunidade_virtual_id:
            return
    raise PermissaoNegada(
        mensagem="Só Admin ou Mestre vinculado à comunidade do item operam sobre ele."
    )


def cadastrar_item(
    sessao: Session,
    *,
    operador: Persona,
    nome: str | None,
    tipo: TipoDeRecurso | None,
    estoque: Decimal | None,
    comunidade: ComunidadeVirtual | None,
    ponto_de_apoio: PontoDeApoio | None,
    preco_em_pontos_extras: int | Decimal | None = None,
) -> ItemDeCatalogoAvulso:
    """Mestre cadastra sem homologação; Apoiador nasce pendente. O item não
    tem preço próprio — o preço é sempre o da tabela de referência vigente
    do tipo de recurso (`RF-07-33`, `RF-07-45`, `RF-09-99`, `RF-09-100`,
    `RN-07-29`, `RN-07-33`, `RN-14-42`)."""
    if operador.papel not in (Papel.mestre, Papel.apoiador):
        raise PermissaoNegada(mensagem="Só Mestre ou Apoiador cadastram item do catálogo avulso.")
    if preco_em_pontos_extras is not None:
        raise ErroDeValidacao(
            mensagem=(
                "Item do catálogo avulso não tem preço próprio: o preço vem da tabela de "
                "referência vigente do tipo de recurso."
            ),
            campo="preco_em_pontos_extras",
        )
    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem="Item do catálogo avulso exige nome.", campo="nome")
    if tipo is None:
        raise ErroDeValidacao(
            mensagem="Item do catálogo avulso exige um tipo de recurso existente.",
            campo="tipo_de_recurso_id",
        )
    if tipo.natureza == NaturezaDoRecurso.duravel:
        raise ErroDeValidacao(
            mensagem=(
                "Item do catálogo avulso não aceita tipo de recurso de natureza durável: "
                "o saldo durável é patrimônio e nunca lastreia recompensa."
            ),
            campo="tipo_de_recurso_id",
        )
    if comunidade is None:
        raise ErroDeValidacao(
            mensagem="Item do catálogo avulso exige uma comunidade.",
            campo="comunidade_virtual_id",
        )
    if ponto_de_apoio is None:
        raise ErroDeValidacao(
            mensagem="Item do catálogo avulso exige um ponto de apoio.",
            campo="ponto_de_apoio_id",
        )
    if ponto_de_apoio.comunidade_virtual_id != comunidade.id:
        raise ErroDeValidacao(
            mensagem="O ponto de apoio precisa ser da mesma comunidade do item.",
            campo="ponto_de_apoio_id",
        )
    if estoque is None or estoque < ESTOQUE_MINIMO:
        raise ErroDeValidacao(
            mensagem="Item do catálogo avulso exige estoque de ao menos 1.", campo="estoque"
        )

    if operador.papel == Papel.mestre:
        vinculo: VinculoJogador | None = operador.vinculo_vigente
        if vinculo is None or vinculo.comunidade_virtual_id != comunidade.id:
            raise PermissaoNegada(mensagem="Só o Mestre vinculado à comunidade cadastra item nela.")
        origem = OrigemDoCadastroDoItem.mestre
        situacao_de_homologacao = SituacaoDeHomologacao.nao_se_aplica
    else:
        origem = OrigemDoCadastroDoItem.apoiador
        situacao_de_homologacao = SituacaoDeHomologacao.pendente

    item = ItemDeCatalogoAvulso(
        nome=nome,
        tipo_de_recurso_id=tipo.id,
        estoque=estoque,
        comunidade_virtual_id=comunidade.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        origem_do_cadastro=origem,
        situacao_de_homologacao=situacao_de_homologacao,
        ativo=False,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(item)
    sessao.flush()
    _recalcular_ativo(sessao, item=item)
    sessao.flush()
    return item


def homologar_item(
    sessao: Session,
    *,
    operador: Persona,
    item: ItemDeCatalogoAvulso | None,
    decisao: str | None,
    motivo: str | None = None,
) -> ItemDeCatalogoAvulso:
    """Só Admin homologa ou recusa item pendente de Apoiador; a recusa exige
    motivo, e a homologação reverifica preço e lastro no mesmo ato
    (`RF-09-100`, `RN-14-42`, `RN-07-26`)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin homologa item do catálogo avulso.")
    if item is None:
        raise ErroDeValidacao(mensagem="Homologação exige um item existente.", campo="item_id")
    if item.situacao_de_homologacao != SituacaoDeHomologacao.pendente:
        raise ErroDeValidacao(
            mensagem="Este item não está pendente de homologação.",
            campo="situacao_de_homologacao",
        )
    try:
        decisao_valida = SituacaoDeHomologacao(decisao)
    except (ValueError, TypeError) as exc:
        raise ErroDeValidacao(
            mensagem="Decisão precisa ser homologado ou recusado.", campo="decisao"
        ) from exc
    if decisao_valida not in _DECISOES_DE_HOMOLOGACAO:
        raise ErroDeValidacao(
            mensagem="Decisão precisa ser homologado ou recusado.", campo="decisao"
        )
    if decisao_valida == SituacaoDeHomologacao.recusado and (not motivo or not motivo.strip()):
        raise ErroDeValidacao(mensagem="Recusa exige motivo.", campo="motivo")

    item.situacao_de_homologacao = decisao_valida
    item.homologacao_motivo = motivo if decisao_valida == SituacaoDeHomologacao.recusado else None
    sessao.flush()
    _recalcular_ativo(sessao, item=item)
    sessao.flush()
    return item


def ativar_item(
    sessao: Session, *, operador: Persona, item: ItemDeCatalogoAvulso | None
) -> ItemDeCatalogoAvulso:
    """Admin ou Mestre vinculado reverificam o lastro no ato; item pendente
    de homologação ou recusado nunca ativa (`RF-07-34`, `RN-09-37`,
    `RN-14-42`)."""
    if item is None:
        raise ErroDeValidacao(mensagem="Ativação exige um item existente.", campo="item_id")
    _exigir_admin_ou_mestre_vinculado(operador, item)

    if item.situacao_de_homologacao in SITUACOES_QUE_NUNCA_ATIVAM:
        raise ErroDeValidacao(
            mensagem="Item pendente de homologação ou recusado não pode ser ativado.",
            campo="situacao_de_homologacao",
        )
    if not tem_preco_de_referencia_vigente(sessao, item=item):
        raise ErroDeValidacao(
            mensagem="Este item não tem preço de referência vigente.",
            campo="tipo_de_recurso_id",
        )
    falta = falta_de_lastro(sessao, item=item)
    if falta > 0:
        raise ErroDeValidacao(
            mensagem=f"Lastro insuficiente: faltam {falta} unidades no ponto de apoio.",
            campo="estoque",
        )

    item.ativo = True
    sessao.flush()
    return item


def alterar_estoque(
    sessao: Session,
    *,
    operador: Persona,
    item: ItemDeCatalogoAvulso | None,
    estoque: Decimal | None,
) -> ItemDeCatalogoAvulso:
    """Admin ou Mestre vinculado alteram o estoque; acima do lastro
    disponível desativa o item, sem apagar nada (`RF-07-33`, `RF-07-34`,
    `RF-09-102`)."""
    if item is None:
        raise ErroDeValidacao(
            mensagem="Alteração de estoque exige um item existente.", campo="item_id"
        )
    _exigir_admin_ou_mestre_vinculado(operador, item)
    if estoque is None or estoque < ESTOQUE_MINIMO:
        raise ErroDeValidacao(mensagem="Estoque exige quantidade de ao menos 1.", campo="estoque")

    item.estoque = estoque
    sessao.flush()
    _recalcular_ativo(sessao, item=item)
    sessao.flush()
    return item


def retirar_item(
    sessao: Session, *, operador: Persona, item: ItemDeCatalogoAvulso | None
) -> ItemDeCatalogoAvulso:
    """Admin ou Mestre vinculado retiram o item do catálogo — deixa inativo
    e preserva o registro, nunca apaga (`RF-09-102`)."""
    if item is None:
        raise ErroDeValidacao(mensagem="Retirada exige um item existente.", campo="item_id")
    _exigir_admin_ou_mestre_vinculado(operador, item)

    item.ativo = False
    sessao.flush()
    return item


def listar_catalogo(
    sessao: Session,
    *,
    operador: Persona,
    comunidade: ComunidadeVirtual | None,
    incluir_inativos: bool = False,
) -> list[ItemDeCatalogoAvulso]:
    """Guerreiro(a) lê a comunidade do seu vínculo; Mestre e Apoiador, a
    comunidade do vínculo vigente deles — o mesmo `vinculo_vigente` que
    `aulas.regra` já usa para o Mestre, aqui também alcançando o Apoiador;
    Admin lê qualquer comunidade, sempre declarada. Inativos só para Admin e
    Mestre vinculado (`RF-07-33`, `RF-04-50`, `RF-05-83`, `RF-09-103`,
    `RF-01-24`)."""
    if operador.papel == Papel.admin:
        if comunidade is None:
            raise ErroDeValidacao(
                mensagem="Leitura do catálogo avulso exige o filtro de comunidade.",
                campo="comunidade_virtual_id",
            )
        alvo_id = comunidade.id
    elif operador.papel in (Papel.guerreiro, Papel.mestre, Papel.apoiador):
        vinculo: VinculoJogador | None = operador.vinculo_vigente
        if vinculo is None:
            return []
        alvo_id = vinculo.comunidade_virtual_id
        if operador.papel != Papel.mestre:
            incluir_inativos = False
    else:
        raise PermissaoNegada(mensagem="Persona sem catálogo avulso a consultar.")

    consulta = sessao.query(ItemDeCatalogoAvulso).filter_by(comunidade_virtual_id=alvo_id)
    if not incluir_inativos:
        consulta = consulta.filter_by(ativo=True)
    return consulta.order_by(ItemDeCatalogoAvulso.registrado_em.desc()).all()


def listar_ofertas_do_apoiador(sessao: Session, *, operador: Persona) -> list[ItemDeCatalogoAvulso]:
    """Só os itens cadastrados pelo próprio Apoiador, em qualquer situação —
    pendente, homologado, recusado, ativo ou inativo —, da mais recente para
    a mais antiga (`RF-14-80`, `RF-14-77`, `RN-14-42`)."""
    if operador.papel != Papel.apoiador:
        raise PermissaoNegada(mensagem="Só o Apoiador lê os itens que ofertou.")
    return (
        sessao.query(ItemDeCatalogoAvulso)
        .filter_by(autor_id=operador.id)
        .order_by(ItemDeCatalogoAvulso.registrado_em.desc())
        .all()
    )


def contar_trocas_por_item(sessao: Session, *, item: ItemDeCatalogoAvulso) -> int:
    """A contagem agregada das trocas entregues do item, sem identificar
    quem trocou (`RF-14-80`, `RF-14-81`, `RN-14-44`)."""
    return sessao.query(Troca).filter_by(item_de_catalogo_avulso_id=item.id).count()
