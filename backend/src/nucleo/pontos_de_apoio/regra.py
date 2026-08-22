import uuid

from sqlalchemy.orm import Session

from ..aulas.modelo import Aula, SituacaoDaAula
from ..comunidades.modelo import ComunidadeVirtual, VinculoJogador
from ..erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..livro_razao.regra import saldos_por_ponto_de_apoio
from ..personas.modelo import Papel, Persona
from ..recursos.modelo import TipoDeRecurso
from ..tempo import agora
from .modelo import PontoDeApoio

PAPEIS_QUE_PODEM_SER_RESPONSAVEL = frozenset({Papel.admin, Papel.mestre, Papel.apoiador})

_SITUACOES_QUE_NAO_BLOQUEIAM_DESATIVACAO = (SituacaoDaAula.realizada, SituacaoDaAula.cancelada)


def cadastrar_ponto_de_apoio(
    sessao: Session,
    *,
    operador: Persona,
    nome: str | None,
    comunidade_id: uuid.UUID | None,
) -> PontoDeApoio:
    """Só Admin cadastra ponto de apoio, sem responsável — quem responde
    pelo acervo é designado depois, em operação própria (`RF-07-47`,
    `RN-07-33`, `RF-07-49`)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin cadastra ponto de apoio.")
    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem="Ponto de apoio exige nome.", campo="nome")
    if comunidade_id is None:
        raise ErroDeValidacao(
            mensagem="Ponto de apoio exige uma comunidade.", campo="comunidade_id"
        )

    comunidade = sessao.get(ComunidadeVirtual, comunidade_id)
    if comunidade is None:
        raise ErroDeValidacao(mensagem="Comunidade não encontrada.", campo="comunidade_id")

    ponto_de_apoio = PontoDeApoio(
        nome=nome,
        comunidade_virtual_id=comunidade.id,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(ponto_de_apoio)
    sessao.flush()
    return ponto_de_apoio


def designar_responsavel(
    sessao: Session,
    ponto_de_apoio: PontoDeApoio | None,
    *,
    operador: Persona,
    responsavel: Persona | None,
) -> PontoDeApoio:
    """Designa ou troca o responsável pelo acervo, a qualquer tempo — só
    Admin, e só para persona de papel Admin, Mestre ou Apoiador; Guerreiro(a)
    e responsável familiar são recusados (`RF-07-49`, `RN-07-34`). A troca
    substitui o designado anterior, cuja designação permanece auditável pela
    trilha de auditoria (`RF-01-29`, design — Decisions 6).
    """
    if ponto_de_apoio is None:
        raise NaoEncontrado(mensagem="Ponto de apoio não encontrado.")
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin designa o responsável pelo acervo.")
    if responsavel is None:
        raise ErroDeValidacao(
            mensagem="Designação exige o responsável pelo acervo.", campo="responsavel_id"
        )
    if responsavel.papel not in PAPEIS_QUE_PODEM_SER_RESPONSAVEL:
        raise ErroDeValidacao(
            mensagem="O responsável pelo acervo precisa ser Admin, Mestre ou Apoiador.",
            campo="responsavel_id",
        )

    ponto_de_apoio.responsavel_id = responsavel.id
    sessao.flush()
    return ponto_de_apoio


def _contar_aulas_futuras(sessao: Session, ponto_de_apoio_id: uuid.UUID) -> int:
    """Aula agendada ainda por acontecer neste ponto de apoio: sem desfecho
    (realizada ou cancelada) e com início depois de agora. Reserva herda a
    aula que a criou, então esta contagem já alcança as reservas ainda
    abertas (`RF-07-47`, `RN-07-01`, `RN-07-33`, design — Decisions 3)."""
    return (
        sessao.query(Aula)
        .filter(
            Aula.ponto_de_apoio_id == ponto_de_apoio_id,
            Aula.situacao.notin_(_SITUACOES_QUE_NAO_BLOQUEIAM_DESATIVACAO),
            Aula.inicio_em > agora(),
        )
        .count()
    )


def _validar_mudanca_de_situacao(
    ponto_de_apoio: PontoDeApoio | None,
    *,
    operador: Persona,
    motivo: str | None,
    ativo_alvo: bool,
    mensagem_de_permissao: str,
    mensagem_de_ja_no_estado: str,
) -> None:
    if ponto_de_apoio is None:
        raise NaoEncontrado(mensagem="Ponto de apoio não encontrado.")
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem=mensagem_de_permissao)
    if not motivo or not motivo.strip():
        raise ErroDeValidacao(mensagem="Esta operação exige motivo.", campo="motivo")
    if ponto_de_apoio.ativo == ativo_alvo:
        raise ErroDeValidacao(mensagem=mensagem_de_ja_no_estado, campo="ativo")


def _aplicar_situacao(
    sessao: Session,
    ponto_de_apoio: PontoDeApoio,
    *,
    operador: Persona,
    motivo: str,
    ativo_alvo: bool,
) -> PontoDeApoio:
    ponto_de_apoio.ativo = ativo_alvo
    ponto_de_apoio.motivo_da_situacao = motivo
    ponto_de_apoio.autor_da_situacao_id = operador.id
    ponto_de_apoio.papel_do_autor_da_situacao = operador.papel.value
    ponto_de_apoio.situacao_alterada_em = agora()
    sessao.flush()
    return ponto_de_apoio


def desativar_ponto_de_apoio(
    sessao: Session,
    ponto_de_apoio: PontoDeApoio | None,
    *,
    operador: Persona,
    motivo: str | None,
) -> PontoDeApoio:
    """Só Admin desativa, sempre com motivo; bloqueada por aula futura e por
    saldo remanescente, cada bloqueio dizendo o que prende o espaço
    (`RF-07-47`, `RN-07-01`, `RN-07-15`, `RN-07-33`, design — Decisions
    2, 3). Não apaga o ponto de apoio nem desfaz vínculo: aula passada e
    lançamento continuam apontando para ele."""
    _validar_mudanca_de_situacao(
        ponto_de_apoio,
        operador=operador,
        motivo=motivo,
        ativo_alvo=False,
        mensagem_de_permissao="Só o Admin desativa ponto de apoio.",
        mensagem_de_ja_no_estado="Este ponto de apoio já está inativo.",
    )

    aulas_futuras = _contar_aulas_futuras(sessao, ponto_de_apoio.id)
    if aulas_futuras > 0:
        plural = "s" if aulas_futuras != 1 else ""
        raise ErroDeValidacao(
            mensagem=(
                f"Este ponto de apoio tem {aulas_futuras} aula{plural} futura{plural} "
                "agendada; cancele-a(s) ou aguarde para desativar."
            ),
            campo="aulas_futuras",
        )

    saldos = saldos_por_ponto_de_apoio(sessao, ponto_de_apoio_id=ponto_de_apoio.id)
    tipos_com_saldo = [
        sessao.get(TipoDeRecurso, tipo_de_recurso_id)
        for tipo_de_recurso_id, saldo in saldos
        if saldo > 0
    ]
    if tipos_com_saldo:
        nomes = ", ".join(tipo.nome for tipo in tipos_com_saldo)
        raise ErroDeValidacao(
            mensagem=(
                f"Este ponto de apoio ainda tem saldo de: {nomes}. Transfira o saldo para "
                "outro ponto de apoio antes de desativar."
            ),
            campo="saldo",
        )

    return _aplicar_situacao(
        sessao, ponto_de_apoio, operador=operador, motivo=motivo, ativo_alvo=False
    )


def reativar_ponto_de_apoio(
    sessao: Session,
    ponto_de_apoio: PontoDeApoio | None,
    *,
    operador: Persona,
    motivo: str | None,
) -> PontoDeApoio:
    """Só Admin reativa, sempre com motivo (`RF-07-47`, `RN-07-33`)."""
    _validar_mudanca_de_situacao(
        ponto_de_apoio,
        operador=operador,
        motivo=motivo,
        ativo_alvo=True,
        mensagem_de_permissao="Só o Admin reativa ponto de apoio.",
        mensagem_de_ja_no_estado="Este ponto de apoio já está ativo.",
    )
    return _aplicar_situacao(
        sessao, ponto_de_apoio, operador=operador, motivo=motivo, ativo_alvo=True
    )


def escopo_de_comunidade_da_leitura(
    *, operador: Persona, comunidade_virtual_id: uuid.UUID | None
) -> uuid.UUID | None:
    """Resolve a comunidade a que a leitura dos pontos de apoio se
    restringe, no molde de `listar_acervo` (`patrimonio/regra.py`): Admin
    declara a comunidade, sempre obrigatória; Mestre herda do vínculo
    vigente, e sem vínculo não tem o que listar — `None` aqui sinaliza
    lista vazia, nunca erro. Demais papéis são recusados (`RF-07-47`,
    `RF-01-28`, `RF-01-18`, `RF-01-16`).
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
    raise PermissaoNegada(mensagem="Persona sem pontos de apoio a consultar.")
