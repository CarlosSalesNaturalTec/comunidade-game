import uuid
from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..armazenamento.limites import (
    FORMATOS_DE_ENVIO_ACEITOS,
    TAMANHO_TETO_ARQUIVO,
    TAMANHO_TETO_VIDEO,
    formatar_mb,
)
from ..armazenamento.porta import PortaDeArmazenamento
from ..aulas.modelo import Aula, Presenca
from ..aulas.regra import presenca_vigente
from ..comunidades.regra import comunidades_do_mestre, filtrar_personas_por_comunidades
from ..erros import ArquivoAcimaDoTeto, ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..ponto_extra.regra import creditar_ponto_extra
from ..recompensas_de_marco.modelo import EntregaDeRecompensa, RecompensaDeMarco
from ..recursos.modelo import TipoDeRecurso
from ..tempo import agora
from ..trilhas.modelo import DesbloqueioDaMissao, Missao, TipoDeDesafioDeDesbloqueio, Trilha
from .modelo import (
    FonteDaPontuacaoDoBem,
    PontuacaoDoBem,
    RegistroDeCustomizacao,
    SituacaoDoRegistroDeCustomizacao,
)

# Documento 11 §5: a conservação validada e a customização aprovada rendem,
# cada uma, 1 ponto extra por bem, por encontro.
PONTOS_EXTRAS_DO_CUIDADO_DO_BEM = 1

_NOME_DA_FONTE = {
    FonteDaPontuacaoDoBem.conservacao: "conservação",
    FonteDaPontuacaoDoBem.customizacao: "customização",
}


# ---------------------------------------------------------------------------
# Abertura e último registro aprovado (`RF-01-84`, `RF-09-141`)
# ---------------------------------------------------------------------------


def desbloqueio_que_abre_a_customizacao(
    sessao: Session, entrega: EntregaDeRecompensa
) -> DesbloqueioDaMissao | None:
    """O prático aprovado, do mesmo Guerreiro(a), de uma missão que declara a
    recompensa da entrega como kit apresentado — é ele que abre a
    customização, e a comprovação dele é o primeiro registro do kit (design —
    decisão 2)."""
    return (
        sessao.query(DesbloqueioDaMissao)
        .join(Missao, Missao.id == DesbloqueioDaMissao.missao_id)
        .filter(
            Missao.desafio_pratico_kit_id == entrega.recompensa_de_marco_id,
            Missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.pratico,
            DesbloqueioDaMissao.guerreiro_id == entrega.guerreiro_id,
            DesbloqueioDaMissao.cumpriu.is_(True),
        )
        .order_by(DesbloqueioDaMissao.momento.desc())
        .first()
    )


@dataclass
class UltimoRegistroAprovado:
    """O "antes" que o Mestre compara com o kit na mão: o registro de
    customização aprovado mais recente ou, sem nenhum, a comprovação do
    prático que abriu a customização."""

    fonte: str
    id: uuid.UUID
    descricao: str | None
    tipo_do_arquivo: str | None
    aprovado_em: datetime | None


def ultimo_registro_aprovado(
    sessao: Session, entrega: EntregaDeRecompensa, desbloqueio: DesbloqueioDaMissao
) -> UltimoRegistroAprovado:
    registro = (
        sessao.query(RegistroDeCustomizacao)
        .filter_by(
            entrega_de_recompensa_id=entrega.id,
            situacao=SituacaoDoRegistroDeCustomizacao.aprovado,
        )
        .order_by(RegistroDeCustomizacao.julgado_em.desc())
        .first()
    )
    if registro is not None:
        return UltimoRegistroAprovado(
            fonte="customizacao_do_kit",
            id=registro.id,
            descricao=registro.descricao,
            tipo_do_arquivo=registro.midia_tipo_do_arquivo,
            aprovado_em=registro.julgado_em,
        )
    return UltimoRegistroAprovado(
        fonte="comprovacao_do_pratico",
        id=desbloqueio.id,
        descricao=None,
        tipo_do_arquivo=desbloqueio.comprovacao_tipo_do_arquivo,
        aprovado_em=desbloqueio.julgado_em,
    )


# ---------------------------------------------------------------------------
# Conferências comuns
# ---------------------------------------------------------------------------


def conferir_mestre_da_aula(sessao: Session, operador: Persona, aula_id: uuid.UUID | None) -> Aula:
    """Mestre da aula é o Mestre vinculado à comunidade dela, como na fila de
    entregas do encontro (design — decisão 4)."""
    if operador.papel != Papel.mestre:
        raise PermissaoNegada(mensagem="Só o Mestre da aula cuida dos bens no encontro.")
    aula = sessao.get(Aula, aula_id) if aula_id is not None else None
    if aula is None:
        raise NaoEncontrado(mensagem="Aula não encontrada.")
    if aula.comunidade_virtual_id not in comunidades_do_mestre(sessao, mestre=operador):
        raise PermissaoNegada(
            mensagem="Só o Mestre vinculado à comunidade da aula cuida dos bens no encontro."
        )
    return aula


def _conferir_presenca(sessao: Session, aula: Aula, guerreiro_id: uuid.UUID) -> None:
    if presenca_vigente(sessao, aula_id=aula.id, guerreiro_id=guerreiro_id) is None:
        raise ErroDeValidacao(
            mensagem="Este Guerreiro(a) não tem presença registrada nesta aula.",
            campo="guerreiro_id",
        )


def _obter_entrega_do_guerreiro(
    sessao: Session, entrega_id: uuid.UUID | None, guerreiro_id: uuid.UUID
) -> EntregaDeRecompensa:
    entrega = sessao.get(EntregaDeRecompensa, entrega_id) if entrega_id is not None else None
    if entrega is None or entrega.guerreiro_id != guerreiro_id:
        raise ErroDeValidacao(
            mensagem="Este bem não foi entregue a este Guerreiro(a).",
            campo="entrega_de_recompensa_id",
        )
    return entrega


# ---------------------------------------------------------------------------
# Registro, envio, leitura e cancelamento (`RF-01-84`, `RF-01-86`)
# ---------------------------------------------------------------------------


def registrar_customizacao(
    sessao: Session,
    *,
    operador: Persona,
    entrega_de_recompensa_id: uuid.UUID | None,
    descricao: str | None,
    guerreiro_id: uuid.UUID | None = None,
    aula_id: uuid.UUID | None = None,
) -> RegistroDeCustomizacao:
    """O próprio Guerreiro(a) registra, ou o Mestre da aula captura em nome
    de Guerreiro(a) com presença naquela aula (`RF-01-84`, `RF-04-80`,
    `RF-04-82`, `RF-05-102`). Um só pendente por kit."""
    if operador.papel == Papel.guerreiro:
        guerreiro_id = operador.id
    elif operador.papel == Papel.mestre:
        aula = conferir_mestre_da_aula(sessao, operador, aula_id)
        if guerreiro_id is None:
            raise ErroDeValidacao(mensagem="A captura exige o Guerreiro(a).", campo="guerreiro_id")
        _conferir_presenca(sessao, aula, guerreiro_id)
    else:
        raise PermissaoNegada(
            mensagem="A customização é registrada pelo Guerreiro(a) ou pelo Mestre da aula."
        )

    entrega = _obter_entrega_do_guerreiro(sessao, entrega_de_recompensa_id, guerreiro_id)
    if desbloqueio_que_abre_a_customizacao(sessao, entrega) is None:
        raise ErroDeValidacao(
            mensagem="A customização deste kit ainda não abriu: ela abre quando o Mestre "
            "aprova o desafio prático que apresenta o kit.",
            campo="entrega_de_recompensa_id",
        )

    texto = descricao.strip() if descricao is not None else ""
    if not texto:
        raise ErroDeValidacao(mensagem="Conte o que você customizou no kit.", campo="descricao")

    pendente = (
        sessao.query(RegistroDeCustomizacao)
        .filter_by(
            entrega_de_recompensa_id=entrega.id,
            situacao=SituacaoDoRegistroDeCustomizacao.pendente,
        )
        .first()
    )
    if pendente is not None:
        raise ErroDeValidacao(
            mensagem="Já há um registro deste kit esperando o Mestre.",
            campo="entrega_de_recompensa_id",
        )

    registro = RegistroDeCustomizacao(
        entrega_de_recompensa_id=entrega.id,
        guerreiro_id=guerreiro_id,
        descricao=texto,
        situacao=SituacaoDoRegistroDeCustomizacao.pendente,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(registro)
    sessao.flush()
    return registro


def _referencia_da_midia(registro: RegistroDeCustomizacao) -> str:
    return f"customizacoes/{registro.id}/midia"


def _teto_do_formato(tipo_mime: str) -> int:
    return TAMANHO_TETO_VIDEO if tipo_mime.startswith("video/") else TAMANHO_TETO_ARQUIVO


def _conferir_envio(
    registro: RegistroDeCustomizacao | None, operador: Persona
) -> RegistroDeCustomizacao:
    """Envia quem gravou o registro, enquanto ele estiver pendente (design —
    decisão 5)."""
    if registro is None:
        raise NaoEncontrado(mensagem="Registro de customização não encontrado.")
    if registro.autor_id != operador.id:
        raise PermissaoNegada(mensagem="A mídia é enviada por quem fez o registro.")
    if registro.situacao != SituacaoDoRegistroDeCustomizacao.pendente:
        raise ErroDeValidacao(
            mensagem="Este registro não está mais pendente; não recebe mídia.", campo="midia"
        )
    return registro


def abrir_envio_da_customizacao(
    sessao: Session,
    registro: RegistroDeCustomizacao | None,
    *,
    operador: Persona,
    tipo_mime: str | None,
    tamanho_declarado: int | None,
    armazenamento: PortaDeArmazenamento,
    origem: str | None = None,
) -> str:
    """Só foto ou vídeo, com o teto do tipo, pela mesma sessão retomável da
    comprovação do prático (`RF-01-84`, design — decisão 5)."""
    registro = _conferir_envio(registro, operador)
    if (
        tipo_mime is None
        or tipo_mime not in FORMATOS_DE_ENVIO_ACEITOS
        or not tipo_mime.startswith(("image/", "video/"))
    ):
        raise ErroDeValidacao(
            mensagem="A customização aceita foto (JPG, PNG, WebP) ou vídeo (MP4, WebM).",
            campo="tipo_mime",
        )
    if tamanho_declarado is None or tamanho_declarado <= 0:
        raise ErroDeValidacao(
            mensagem="Envio exige o tamanho declarado do arquivo.", campo="tamanho_declarado"
        )
    teto = _teto_do_formato(tipo_mime)
    if tamanho_declarado > teto:
        raise ArquivoAcimaDoTeto(
            mensagem=f"O arquivo tem {formatar_mb(tamanho_declarado)} e o limite é "
            f"{formatar_mb(teto)}."
        )
    return armazenamento.abrir_sessao(
        referencia=_referencia_da_midia(registro),
        tipo_mime=tipo_mime,
        tamanho_declarado=tamanho_declarado,
        origem=origem,
    )


def confirmar_envio_da_customizacao(
    sessao: Session,
    registro: RegistroDeCustomizacao | None,
    *,
    operador: Persona,
    armazenamento: PortaDeArmazenamento,
) -> RegistroDeCustomizacao:
    """A referência só é gravada depois de o armazenamento confirmar o tamanho
    real; até aqui o registro não é julgável."""
    registro = _conferir_envio(registro, operador)
    envio = armazenamento.consultar_envio(referencia=_referencia_da_midia(registro))
    if envio is None:
        raise ErroDeValidacao(mensagem="O envio ainda não foi concluído.", campo="midia")
    teto = _teto_do_formato(envio.tipo_mime)
    if envio.tamanho > teto:
        raise ArquivoAcimaDoTeto(
            mensagem=f"O arquivo enviado tem {formatar_mb(envio.tamanho)} e o limite é "
            f"{formatar_mb(teto)}."
        )
    registro.midia_referencia = _referencia_da_midia(registro)
    registro.midia_tamanho = envio.tamanho
    registro.midia_tipo_do_arquivo = envio.tipo_mime
    sessao.flush()
    return registro


@dataclass
class ArquivoDaCustomizacao:
    bytes_do_arquivo: bytes
    tipo_mime: str


def _mestre_da_comunidade_do_guerreiro(
    sessao: Session, operador: Persona, guerreiro_id: uuid.UUID
) -> bool:
    if operador.papel != Papel.mestre:
        return False
    alvos = comunidades_do_mestre(sessao, mestre=operador)
    if not alvos:
        return False
    consulta = sessao.query(Persona.id).filter(Persona.id == guerreiro_id)
    return filtrar_personas_por_comunidades(consulta, alvos).first() is not None


def ler_arquivo_da_customizacao(
    sessao: Session,
    registro: RegistroDeCustomizacao | None,
    *,
    operador: Persona,
    armazenamento: PortaDeArmazenamento,
) -> ArquivoDaCustomizacao:
    """Os bytes vão ao Guerreiro(a) dono e ao Mestre da comunidade dele, que é
    quem julga no encontro (`RF-01-84`, `RF-04-81`)."""
    if registro is None:
        raise NaoEncontrado(mensagem="Registro de customização não encontrado.")
    if registro.guerreiro_id != operador.id and not _mestre_da_comunidade_do_guerreiro(
        sessao, operador, registro.guerreiro_id
    ):
        raise PermissaoNegada(
            mensagem="A mídia é servida ao Guerreiro(a) e ao Mestre da comunidade dele."
        )
    if registro.midia_referencia is None:
        raise NaoEncontrado(mensagem="Este registro ainda não tem mídia.")
    return ArquivoDaCustomizacao(
        bytes_do_arquivo=armazenamento.ler(referencia=registro.midia_referencia),
        tipo_mime=registro.midia_tipo_do_arquivo or "application/octet-stream",
    )


def cancelar_customizacao(
    sessao: Session, registro: RegistroDeCustomizacao | None, *, operador: Persona
) -> RegistroDeCustomizacao:
    """Só o próprio Guerreiro(a), e só o pendente (`RF-05-103`, `RF-01-86`)."""
    if registro is None:
        raise NaoEncontrado(mensagem="Registro de customização não encontrado.")
    if registro.guerreiro_id != operador.id:
        raise PermissaoNegada(mensagem="Só o próprio Guerreiro(a) cancela o registro.")
    if registro.situacao != SituacaoDoRegistroDeCustomizacao.pendente:
        raise ErroDeValidacao(
            mensagem="Só o registro que espera o Mestre pode ser cancelado.", campo="situacao"
        )
    registro.situacao = SituacaoDoRegistroDeCustomizacao.cancelado
    sessao.flush()
    return registro


def expirar_customizacoes_pendentes(sessao: Session) -> int:
    """Terceiro efeito do encerramento do ciclo: todo pendente vira expirado,
    num `UPDATE` de Core, como o expurgo da ocorrência de conduta
    (`RF-01-86`, design — decisão 8)."""
    tabela = RegistroDeCustomizacao.__table__
    resultado = sessao.execute(
        update(tabela)
        .where(tabela.c.situacao == SituacaoDoRegistroDeCustomizacao.pendente.value)
        .values(situacao=SituacaoDoRegistroDeCustomizacao.expirado.value)
    )
    return resultado.rowcount


# ---------------------------------------------------------------------------
# Pontuação do bem: julgamento e conservação (`RF-01-85`, `RF-01-87`,
# `RN-01-66`)
# ---------------------------------------------------------------------------


def _pontuar_bem(
    sessao: Session,
    *,
    aula: Aula,
    entrega: EntregaDeRecompensa,
    operador: Persona,
    fonte: FonteDaPontuacaoDoBem,
    registro: RegistroDeCustomizacao | None = None,
) -> PontuacaoDoBem:
    """Grava a pontuação do bem no encontro e credita 1 extra, na mesma
    transação. A conferência prévia diz por qual caminho o bem já pontuou; a
    unicidade do banco segura qualquer outra via (design — decisões 3 e 7)."""
    anterior = (
        sessao.query(PontuacaoDoBem)
        .filter_by(aula_id=aula.id, entrega_de_recompensa_id=entrega.id)
        .first()
    )
    if anterior is not None:
        raise ErroDeValidacao(
            mensagem=f"Este bem já pontuou neste encontro pela {_NOME_DA_FONTE[anterior.fonte]}.",
            campo="entrega_de_recompensa_id",
        )
    pontuacao = PontuacaoDoBem(
        aula_id=aula.id,
        entrega_de_recompensa_id=entrega.id,
        guerreiro_id=entrega.guerreiro_id,
        fonte=fonte,
        registro_de_customizacao_id=registro.id if registro is not None else None,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    try:
        with sessao.begin_nested():
            sessao.add(pontuacao)
            sessao.flush()
    except IntegrityError as exc:
        raise ErroDeValidacao(
            mensagem="Este bem já pontuou neste encontro.", campo="entrega_de_recompensa_id"
        ) from exc
    creditar_ponto_extra(
        sessao, guerreiro_id=entrega.guerreiro_id, valor=PONTOS_EXTRAS_DO_CUIDADO_DO_BEM
    )
    return pontuacao


def julgar_customizacao(
    sessao: Session,
    registro: RegistroDeCustomizacao | None,
    *,
    operador: Persona,
    aula_id: uuid.UUID | None,
    aprovado: bool | None,
    motivo: str | None = None,
) -> RegistroDeCustomizacao:
    """O Mestre da aula julga ao vivo: aprovado credita 1 extra e leva o
    registro ao acervo; reprovado exige motivo (`RF-01-85`, `RF-04-82`,
    `RF-04-83`, `RN-01-66`)."""
    aula = conferir_mestre_da_aula(sessao, operador, aula_id)
    if registro is None:
        raise NaoEncontrado(mensagem="Registro de customização não encontrado.")
    if registro.situacao != SituacaoDoRegistroDeCustomizacao.pendente:
        raise ErroDeValidacao(mensagem="Este registro já não espera julgamento.", campo="situacao")
    if registro.midia_referencia is None:
        raise ErroDeValidacao(
            mensagem="O registro ainda não tem a foto ou o vídeo do kit.", campo="midia"
        )
    if aprovado is None:
        raise ErroDeValidacao(mensagem="Diga se a customização foi aprovada.", campo="aprovado")
    _conferir_presenca(sessao, aula, registro.guerreiro_id)

    if aprovado:
        entrega = sessao.get(EntregaDeRecompensa, registro.entrega_de_recompensa_id)
        _pontuar_bem(
            sessao,
            aula=aula,
            entrega=entrega,
            operador=operador,
            fonte=FonteDaPontuacaoDoBem.customizacao,
            registro=registro,
        )
        registro.situacao = SituacaoDoRegistroDeCustomizacao.aprovado
        registro.motivo_do_julgamento = None
    else:
        texto = motivo.strip() if motivo is not None else ""
        if not texto:
            raise ErroDeValidacao(
                mensagem="Diga à criança, em linguagem simples, por que não passou.",
                campo="motivo",
            )
        registro.situacao = SituacaoDoRegistroDeCustomizacao.reprovado
        registro.motivo_do_julgamento = texto

    registro.aula_id = aula.id
    registro.julgado_por_id = operador.id
    registro.julgado_em = agora()
    sessao.flush()
    return registro


def validar_conservacao(
    sessao: Session,
    *,
    operador: Persona,
    aula_id: uuid.UUID | None,
    guerreiro_id: uuid.UUID | None,
    entrega_de_recompensa_id: uuid.UUID | None,
) -> PontuacaoDoBem:
    """A conservação da recompensa de marco entregue, validada pelo Mestre da
    aula a pedido do Guerreiro(a): 1 extra por bem, por encontro (`RF-01-87`,
    `RF-09-113`, `RF-04-84`, `RN-01-66`). Item do catálogo avulso não é bem
    recebido aqui — só a entrega de recompensa de marco."""
    aula = conferir_mestre_da_aula(sessao, operador, aula_id)
    if guerreiro_id is None:
        raise ErroDeValidacao(mensagem="A validação exige o Guerreiro(a).", campo="guerreiro_id")
    entrega = _obter_entrega_do_guerreiro(sessao, entrega_de_recompensa_id, guerreiro_id)
    _conferir_presenca(sessao, aula, guerreiro_id)
    return _pontuar_bem(
        sessao,
        aula=aula,
        entrega=entrega,
        operador=operador,
        fonte=FonteDaPontuacaoDoBem.conservacao,
    )


# ---------------------------------------------------------------------------
# Leituras: a do Guerreiro(a) e a fila do encontro (`RF-05-103`, `RF-04-81`,
# `RF-04-84`)
# ---------------------------------------------------------------------------


@dataclass
class BemRecebido:
    entrega: EntregaDeRecompensa
    recompensa: RecompensaDeMarco
    tipo_de_recurso_nome: str
    trilha_id: uuid.UUID
    trilha_nome: str
    customizacao_aberta: bool = False
    ultimo_aprovado: UltimoRegistroAprovado | None = None
    pendente: RegistroDeCustomizacao | None = None
    pontuado_na_aula: FonteDaPontuacaoDoBem | None = None


def bens_recebidos(sessao: Session, guerreiro_id: uuid.UUID) -> list[BemRecebido]:
    """As recompensas de marco entregues ao Guerreiro(a), com a abertura da
    customização, o último aprovado e o pendente de cada uma."""
    linhas = (
        sessao.query(EntregaDeRecompensa, RecompensaDeMarco, TipoDeRecurso.nome, Trilha)
        .join(RecompensaDeMarco, RecompensaDeMarco.id == EntregaDeRecompensa.recompensa_de_marco_id)
        .join(TipoDeRecurso, TipoDeRecurso.id == RecompensaDeMarco.tipo_de_recurso_id)
        .join(Trilha, Trilha.id == RecompensaDeMarco.trilha_id)
        .filter(EntregaDeRecompensa.guerreiro_id == guerreiro_id)
        .order_by(EntregaDeRecompensa.registrado_em)
        .all()
    )
    bens: list[BemRecebido] = []
    for entrega, recompensa, nome_do_tipo, trilha in linhas:
        bem = BemRecebido(
            entrega=entrega,
            recompensa=recompensa,
            tipo_de_recurso_nome=nome_do_tipo,
            trilha_id=trilha.id,
            trilha_nome=trilha.nome,
        )
        desbloqueio = desbloqueio_que_abre_a_customizacao(sessao, entrega)
        if desbloqueio is not None:
            bem.customizacao_aberta = True
            bem.ultimo_aprovado = ultimo_registro_aprovado(sessao, entrega, desbloqueio)
        bem.pendente = (
            sessao.query(RegistroDeCustomizacao)
            .filter_by(
                entrega_de_recompensa_id=entrega.id,
                situacao=SituacaoDoRegistroDeCustomizacao.pendente,
            )
            .first()
        )
        bens.append(bem)
    return bens


def registros_do_guerreiro(
    sessao: Session, guerreiro_id: uuid.UUID
) -> list[RegistroDeCustomizacao]:
    return (
        sessao.query(RegistroDeCustomizacao)
        .filter_by(guerreiro_id=guerreiro_id)
        .order_by(RegistroDeCustomizacao.registrado_em.desc())
        .all()
    )


@dataclass
class PresenteNaFila:
    guerreiro: Persona
    bens: list[BemRecebido] = field(default_factory=list)


def fila_do_cuidado(
    sessao: Session, *, operador: Persona, aula_id: uuid.UUID | None
) -> tuple[Aula, list[PresenteNaFila]]:
    """Cada Guerreiro(a) com presença não anulada na aula, com os bens
    recebidos e o que já pontuou ali (`RF-04-81`, `RF-04-84`)."""
    aula = conferir_mestre_da_aula(sessao, operador, aula_id)
    presentes = (
        sessao.query(Persona)
        .join(Presenca, Presenca.guerreiro_id == Persona.id)
        .filter(
            Persona.papel == Papel.guerreiro,
            Presenca.aula_id == aula.id,
            Presenca.anulada_em.is_(None),
        )
        .all()
    )
    pontuados = {
        pontuacao.entrega_de_recompensa_id: pontuacao.fonte
        for pontuacao in sessao.query(PontuacaoDoBem).filter_by(aula_id=aula.id)
    }
    fila: list[PresenteNaFila] = []
    for guerreiro in presentes:
        bens = bens_recebidos(sessao, guerreiro.id)
        for bem in bens:
            bem.pontuado_na_aula = pontuados.get(bem.entrega.id)
        fila.append(PresenteNaFila(guerreiro=guerreiro, bens=bens))
    return aula, fila
