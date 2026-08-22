import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from ..comunidades.modelo import ComunidadeVirtual, VinculoJogador
from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import NaturezaDoRecurso, TipoDeRecurso
from ..reservas.regra import liberar_reservas_da_aula, tentar_reservar_recursos
from ..tempo import agora
from .modelo import Aula, ModoDeComprovacao, Presenca, RecursoDeclaradoDaAula, SituacaoDaAula

_SITUACOES_COM_DESFECHO = (SituacaoDaAula.realizada, SituacaoDaAula.cancelada)


@dataclass
class RecursoDeclaradoEntrada:
    """O par tipo de recurso e quantidade que a rota resolve antes de
    chamar `agendar_aula` — `tipo` já vem carregado (ou `None`, para o 422
    de tipo inexistente) pela mesma convenção de `aportes.regra`."""

    tipo: TipoDeRecurso | None
    quantidade: Decimal | None


def agendar_aula(
    sessao: Session,
    *,
    operador: Persona,
    comunidade: ComunidadeVirtual | None,
    ponto_de_apoio: PontoDeApoio | None,
    inicio_em: datetime | None,
    fim_em: datetime | None,
    recursos_declarados: list[RecursoDeclaradoEntrada] | None = None,
) -> Aula:
    """Restrita ao Admin — o Mestre lê o painel do dia, mas não escreve em
    gestão (`RF-01-20`, `RF-01-16`, `RF-01-03`, PRD-01 §4). O ponto de apoio
    declarado precisa ser da mesma comunidade da aula e estar **ativo**:
    espaço desativado não recebe aula nova (`RF-01-71`, `RF-07-47`,
    `RN-07-33`, invariante 4 do documento 99 §6).

    Os recursos declarados disparam a reserva na mesma operação: havendo
    disponível para todos, a aula nasce **confirmada**; faltando qualquer
    parcela, nasce **pendente de lastro** sem reserva alguma — nem a dos
    tipos que tinham saldo (`RF-07-08`, `RN-07-01`, design — Decisions 1,
    4). Sem recurso declarado, a aula nasce confirmada, pelo padrão do
    próprio modelo.
    """
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin agenda aula.")
    if comunidade is None:
        raise ErroDeValidacao(mensagem="Aula exige uma comunidade.", campo="comunidade_virtual_id")
    if ponto_de_apoio is None:
        raise ErroDeValidacao(mensagem="Aula exige um ponto de apoio.", campo="ponto_de_apoio_id")
    if ponto_de_apoio.comunidade_virtual_id != comunidade.id:
        raise ErroDeValidacao(
            mensagem="O ponto de apoio precisa ser da mesma comunidade da aula.",
            campo="ponto_de_apoio_id",
        )
    if not ponto_de_apoio.ativo:
        raise ErroDeValidacao(
            mensagem="O ponto de apoio está inativo e não recebe aula nova.",
            campo="ponto_de_apoio_id",
        )
    if inicio_em is None:
        raise ErroDeValidacao(mensagem="Aula exige o horário inicial.", campo="inicio_em")
    if fim_em is None:
        raise ErroDeValidacao(mensagem="Aula exige o horário final.", campo="fim_em")
    if fim_em <= inicio_em:
        raise ErroDeValidacao(
            mensagem="O horário final da aula precisa ser posterior ao inicial.",
            campo="fim_em",
        )

    recursos_declarados = recursos_declarados or []
    for entrada in recursos_declarados:
        if entrada.tipo is None:
            raise ErroDeValidacao(
                mensagem="Recurso declarado exige um tipo de recurso existente.",
                campo="recursos_declarados",
            )
        if entrada.tipo.natureza == NaturezaDoRecurso.duravel:
            raise ErroDeValidacao(
                mensagem=(
                    "Tipo de recurso de natureza durável não é reservável: o saldo é "
                    "patrimônio, não insumo de atividade."
                ),
                campo="recursos_declarados",
            )
        if entrada.quantidade is None or entrada.quantidade <= 0:
            raise ErroDeValidacao(
                mensagem="Recurso declarado exige quantidade maior que zero.",
                campo="recursos_declarados",
            )

    aula = Aula(
        comunidade_virtual_id=comunidade.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        inicio_em=inicio_em,
        fim_em=fim_em,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(aula)
    sessao.flush()

    for entrada in recursos_declarados:
        sessao.add(
            RecursoDeclaradoDaAula(
                aula_id=aula.id, tipo_de_recurso_id=entrada.tipo.id, quantidade=entrada.quantidade
            )
        )
    sessao.flush()

    if recursos_declarados:
        reservou = tentar_reservar_recursos(sessao, aula=aula, operador=operador)
        aula.situacao = SituacaoDaAula.confirmada if reservou else SituacaoDaAula.pendente_de_lastro
        sessao.flush()

    return aula


def tentar_reservar_aula_pendente(sessao: Session, *, operador: Persona, aula: Aula | None) -> Aula:
    """Caminho explícito e idempotente da PRD-07 §9: tenta a reserva de uma
    aula pendente de lastro; aula já confirmada devolve o estado corrente
    sem duplicar reserva (design — Decisions 6). Restrita ao Admin, pela
    mesma leitura de `RF-01-17` que reserva a gestão a ele fora das três
    exceções do Mestre.
    """
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin tenta a reserva pelo caminho explícito.")
    if aula is None:
        raise ErroDeValidacao(mensagem="Reserva exige uma aula.", campo="aula_id")
    if aula.situacao != SituacaoDaAula.pendente_de_lastro:
        return aula

    if tentar_reservar_recursos(sessao, aula=aula, operador=operador):
        aula.situacao = SituacaoDaAula.confirmada
        sessao.flush()
    return aula


def cancelar_aula(
    sessao: Session, *, operador: Persona, aula: Aula | None, motivo: str | None
) -> Aula:
    """Admin ou Mestre vinculado à comunidade da aula cancelam, sempre com
    motivo; qualquer outro papel recebe 403 (`RF-01-72`, `RF-01-17`,
    `RF-02-95`, design — Decisions 10). O cancelamento libera as reservas,
    devolvendo as quantidades à disponível, e é a única escrita de gestão
    do Mestre (`RF-01-17`).
    """
    if aula is None:
        raise ErroDeValidacao(mensagem="Cancelamento exige uma aula.", campo="aula_id")

    if operador.papel == Papel.admin:
        pass
    elif operador.papel == Papel.mestre:
        vinculo: VinculoJogador | None = operador.vinculo_vigente
        if vinculo is None or vinculo.comunidade_virtual_id != aula.comunidade_virtual_id:
            raise PermissaoNegada(mensagem="Só o Mestre vinculado à comunidade da aula a cancela.")
    else:
        raise PermissaoNegada(mensagem="Só Admin ou Mestre da comunidade cancelam aula.")

    if not motivo or not motivo.strip():
        raise ErroDeValidacao(mensagem="Cancelamento exige motivo.", campo="motivo")
    if aula.situacao in _SITUACOES_COM_DESFECHO:
        raise ErroDeValidacao(
            mensagem="Esta aula já teve desfecho; o cancelamento não se repete.",
            campo="situacao",
        )

    aula.situacao = SituacaoDaAula.cancelada
    aula.cancelamento_motivo = motivo
    sessao.flush()

    liberar_reservas_da_aula(sessao, aula=aula)
    return aula


def escopo_de_comunidade_da_leitura(
    *, operador: Persona, comunidade_virtual_id: uuid.UUID | None
) -> uuid.UUID | None:
    """Resolve a comunidade a que a leitura da agenda se restringe, no molde
    de `listar_acervo` (`patrimonio/regra.py`) e de
    `pontos_de_apoio.regra.escopo_de_comunidade_da_leitura`: Admin declara a
    comunidade, sempre obrigatória; Mestre herda do vínculo vigente, e sem
    vínculo não tem o que listar — `None` aqui sinaliza lista vazia, nunca
    erro. Demais papéis são recusados (`RF-02-12`, `RF-01-28`, `RF-01-18`,
    `RF-01-16`).
    """
    if operador.papel == Papel.admin:
        if comunidade_virtual_id is None:
            raise ErroDeValidacao(
                mensagem="Esta consulta exige o filtro de comunidade.", campo="comunidade"
            )
        return comunidade_virtual_id
    if operador.papel == Papel.mestre:
        vinculo: VinculoJogador | None = operador.vinculo_vigente
        return vinculo.comunidade_virtual_id if vinculo is not None else None
    raise PermissaoNegada(mensagem="Persona sem agenda de gestão a consultar.")


def aulas_vigentes(sessao: Session) -> list[Aula]:
    """Todas as aulas cujo intervalo contém o momento corrente — havendo
    mais de uma comunidade vigente ao mesmo tempo, a escolha é de quem abre,
    nunca do núcleo (`RF-01-32`, `RF-01-18`).
    """
    momento = agora()
    return sessao.query(Aula).filter(Aula.inicio_em <= momento, Aula.fim_em >= momento).all()


def registrar_presenca(
    sessao: Session,
    *,
    operador: Persona,
    aula: Aula | None,
    guerreiro: Persona | None,
    modo: str | None,
    confirmador: Persona | None,
    momento_do_fato: datetime | None,
) -> Presenca:
    """Idempotente por (aula, guerreiro): o reenvio do App 01 depois da rede
    voltar devolve o registro já gravado, sem duplicar e sem erro
    (`RF-01-20`, PRD-01 §10, design — decisões).
    """
    if aula is None:
        raise ErroDeValidacao(mensagem="Presença exige uma aula.", campo="aula_id")
    if guerreiro is None:
        raise ErroDeValidacao(mensagem="Presença exige o Guerreiro(a).", campo="guerreiro_id")

    existente = sessao.query(Presenca).filter_by(aula_id=aula.id, guerreiro_id=guerreiro.id).first()
    if existente is not None:
        return existente

    vinculo: VinculoJogador | None = guerreiro.vinculo_vigente
    if vinculo is None or vinculo.comunidade_virtual_id != aula.comunidade_virtual_id:
        raise ErroDeValidacao(
            mensagem="Presença só é registrada na comunidade do próprio Guerreiro(a).",
            campo="aula_id",
        )
    if not modo:
        raise ErroDeValidacao(mensagem="Presença exige o modo de comprovação.", campo="modo")
    try:
        modo_valido = ModoDeComprovacao(modo)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Modo de comprovação fora dos valores previstos.", campo="modo"
        ) from exc
    if modo_valido == ModoDeComprovacao.confirmacao and confirmador is None:
        raise ErroDeValidacao(
            mensagem="Presença por confirmação exige quem confirmou.", campo="confirmador_id"
        )
    if momento_do_fato is None:
        raise ErroDeValidacao(
            mensagem="Presença exige o momento em que aconteceu.", campo="momento_do_fato"
        )

    presenca = Presenca(
        aula_id=aula.id,
        guerreiro_id=guerreiro.id,
        modo=modo_valido,
        confirmador_id=confirmador.id if confirmador is not None else None,
        momento_do_fato=momento_do_fato,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(presenca)
    sessao.flush()
    return presenca
