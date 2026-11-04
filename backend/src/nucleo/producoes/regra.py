import logging
import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Session

from ..armazenamento.porta import PortaDeArmazenamento
from ..aulas.modelo import Aula
from ..equipes.modelo import Equipe, IntegranteDaEquipe
from ..erros import ErroDeAplicacao, ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..tempo import agora
from ..trilhas.modelo import Atividade, Missao, Trilha
from ..trilhas.regra import conferir_atividade_vigente, derivar_percurso
from .modelo import FormaDeEntregaDaProducao, ProducaoDaMissao
from .porta import PortaDaProducaoDaMissao

logger = logging.getLogger("nucleo.producoes")

# A lista fechada de formatos, pelo mesmo motivo e no mesmo molde de
# `criacoes_originais.regra`: a mídia guardada é servida de volta, e servir o
# tipo que o cliente declarou abriria XSS por `text/html`. Aqui o conjunto é o
# subconjunto que as duas formas usam — imagem para a foto, MP3 para o áudio —,
# sem régua nova (`RF-01-79`).
_FORMATOS_DA_FOTO = frozenset({"image/jpeg", "image/png", "image/webp"})
_FORMATOS_DO_AUDIO = frozenset({"audio/mpeg"})


@dataclass
class ArquivoDaProducao:
    bytes_do_arquivo: bytes
    tipo_mime: str


def _referencia_do_arquivo(producao: ProducaoDaMissao) -> str:
    return f"producoes-da-missao/{producao.id}/arquivo"


def _conferir_formato(forma: FormaDeEntregaDaProducao, tipo_mime: str | None) -> str:
    aceitos = _FORMATOS_DA_FOTO if forma == FormaDeEntregaDaProducao.foto else _FORMATOS_DO_AUDIO
    if tipo_mime not in aceitos:
        raise ErroDeValidacao(
            mensagem=(
                f"Formato '{tipo_mime}' não aceito nesta forma. A lista aceita é "
                + ", ".join(sorted(aceitos))
                + "."
            ),
            campo="arquivo",
        )
    return tipo_mime


class LeituraDaProducaoIndisponivel(ErroDeAplicacao):
    """`RF-04-46`: sem leitura não há transcrição da foto, e gravar o registro
    vazio guardaria uma entrega que não diz nada. Só a foto chega ilegível — a
    fala já vem transcrita do aparelho (design — decisão 4)."""

    status_code = 503
    codigo = "leitura_da_producao_indisponivel"
    mensagem = "A leitura da produção não veio agora. Tente enviar de novo."


def _conferir_forma_unica(
    forma: FormaDeEntregaDaProducao, texto: str | None, arquivo: bytes | None
) -> None:
    """A forma declarada diz qual conteúdo a entrega traz. **Mudou em
    2026-11-03** (`RF-01-79`, `RN-01-61`): a **foto** vem só em arquivo; o
    **áudio** passa a vir em arquivo **e** em texto — a fala continua
    transcrita no aparelho, porque é sobre a transcrição que a devolutiva se
    faz, e agora o áudio também é guardado; o **texto** vem só em texto.
    Áudio sem transcrição é recusado: guardar o arquivo sem texto deixaria a
    devolutiva sem sobre o que operar."""
    if forma == FormaDeEntregaDaProducao.foto:
        if arquivo is None or texto is not None:
            raise ErroDeValidacao(
                mensagem="Envie a produção em uma única forma: texto, áudio ou foto.",
                campo="forma",
            )
    elif forma == FormaDeEntregaDaProducao.audio:
        if not texto or arquivo is None:
            raise ErroDeValidacao(
                mensagem="A entrega falada traz a transcrição feita no aparelho e o áudio.",
                campo="forma",
            )
    elif not texto or arquivo is not None:
        raise ErroDeValidacao(
            mensagem="Envie a produção em uma única forma: texto, áudio ou foto.",
            campo="forma",
        )


def _ler_e_montar_producao(
    sessao: Session,
    *,
    operador: Persona,
    equipe_id: uuid.UUID | None,
    guerreiro_id: uuid.UUID | None,
    missao_id: uuid.UUID,
    atividade: Atividade,
    forma: FormaDeEntregaDaProducao,
    texto: str | None,
    arquivo: bytes | None,
    tipo_mime: str | None,
    porta: PortaDaProducaoDaMissao,
    armazenamento: PortaDeArmazenamento,
) -> ProducaoDaMissao:
    """O trecho comum às duas portas: a leitura, o desfecho da
    indisponibilidade, a montagem do registro e a **guarda da mídia**
    (design — decisão 1, e decisão 7 de `audio-e-midia-legivel-no-nucleo`).
    Quem chama já conferiu a forma única e a posse da atividade.

    A porta de leitura recebe `arquivo` **só na foto**: a fala chega
    transcrita do aparelho e o núcleo nunca transcreve áudio — guardar o
    áudio não mudou isso (`RN-01-61`)."""
    leitura = porta.ler(
        forma=forma.value,
        texto=texto,
        arquivo=arquivo if forma == FormaDeEntregaDaProducao.foto else None,
        producao_esperada=atividade.producao_esperada,
    )

    if leitura is not None:
        transcricao = leitura.transcricao
        devolutiva = leitura.devolutiva
    elif forma != FormaDeEntregaDaProducao.foto:
        # Texto digitado e fala transcrita no aparelho já chegam legíveis: sem
        # devolutiva a produção é gravada assim mesmo, e nada se perde por
        # indisponibilidade do modelo (`RF-05-76`, design — decisão 4).
        transcricao = texto
        devolutiva = None
    else:
        logger.warning(
            "Leitura da produção indisponível (forma=%s, tamanho=%d bytes).",
            forma.value,
            len(arquivo or b""),
        )
        raise LeituraDaProducaoIndisponivel()

    producao = ProducaoDaMissao(
        equipe_id=equipe_id,
        guerreiro_id=guerreiro_id,
        missao_id=missao_id,
        atividade_id=atividade.id,
        forma=forma,
        transcricao=transcricao,
        devolutiva=devolutiva,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(producao)
    sessao.flush()

    # Guardar é deixar de descartar o que já chegou na mesma requisição
    # multipart — a foto precisa vir inline porque é dela que sai a
    # transcrição (`RF-01-79`, decisão 7).
    if arquivo is not None:
        formato = _conferir_formato(forma, tipo_mime)
        referencia = _referencia_do_arquivo(producao)
        armazenamento.gravar(referencia=referencia, conteudo=arquivo)
        producao.referencia = referencia
        producao.tamanho = len(arquivo)
        producao.tipo_do_arquivo = formato
        sessao.flush()

    return producao


def registrar_producao(
    sessao: Session,
    *,
    operador: Persona,
    equipe: Equipe,
    forma: FormaDeEntregaDaProducao,
    texto: str | None,
    arquivo: bytes | None,
    tipo_mime: str | None,
    porta: PortaDaProducaoDaMissao,
    armazenamento: PortaDeArmazenamento,
) -> ProducaoDaMissao:
    """Restrita ao Guerreiro(a) integrante da equipe (`RF-04-45`, design —
    decisão 6): a operação da matriz já recusa quem não é Guerreiro(a), mas
    o Admin, que tem `Operacao.tudo`, só é barrado aqui — o mesmo precedente
    de `equipes.regra.criar_equipe`."""
    if operador.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) entrega a produção da missão.")

    integrante = (
        sessao.query(IntegranteDaEquipe)
        .filter_by(equipe_id=equipe.id, persona_id=operador.id)
        .first()
    )
    if integrante is None:
        raise PermissaoNegada(mensagem="Só integrante da equipe entrega a produção pela equipe.")

    if equipe.atividade_corrente_id is None:
        raise ErroDeValidacao(
            mensagem="A equipe ainda não declarou a atividade que está trabalhando.",
            campo="equipe_id",
        )

    if equipe.aula_id is not None:
        aula = sessao.get(Aula, equipe.aula_id)
        if aula.fim_em <= agora():
            raise ErroDeValidacao(mensagem="Esta aula já encerrou.", campo="equipe_id")

    _conferir_forma_unica(forma, texto, arquivo)

    atividade = sessao.get(Atividade, equipe.atividade_corrente_id)
    missao = sessao.get(Missao, atividade.missao_id)

    return _ler_e_montar_producao(
        sessao,
        operador=operador,
        equipe_id=equipe.id,
        guerreiro_id=None,
        missao_id=missao.id,
        atividade=atividade,
        forma=forma,
        texto=texto,
        arquivo=arquivo,
        tipo_mime=tipo_mime,
        porta=porta,
        armazenamento=armazenamento,
    )


def registrar_producao_individual(
    sessao: Session,
    *,
    operador: Persona,
    missao: Missao,
    atividade_id: uuid.UUID,
    forma: FormaDeEntregaDaProducao,
    texto: str | None,
    arquivo: bytes | None,
    tipo_mime: str | None,
    porta: PortaDaProducaoDaMissao,
    armazenamento: PortaDeArmazenamento,
) -> ProducaoDaMissao:
    """A entrega individual, sobre a missão do próprio percurso do
    Guerreiro(a) (`RF-05-74`, `RN-05-35`, design — decisões 2, 3). A
    inscrição e o desbloqueio são reconferidos por `derivar_percurso` — a
    mesma regra de percurso que `GET /v1/eu/trilhas/{id}/missoes/{ordem}`
    já usa —, nunca por consulta própria a `InscricaoNaTrilha` ou
    `DesbloqueioDaMissao`."""
    if operador.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) entrega a produção da missão.")

    atividade = sessao.get(Atividade, atividade_id)
    if atividade is None or atividade.missao_id != missao.id:
        raise ErroDeValidacao(
            mensagem="A atividade declarada não pertence a esta missão.", campo="atividade_id"
        )
    conferir_atividade_vigente(atividade)

    percurso = derivar_percurso(sessao, guerreiro_id=operador.id, trilha_id=missao.trilha_id)
    item_da_missao = next((item for item in percurso if item.missao.id == missao.id), None)
    if item_da_missao is None or not item_da_missao.desbloqueada:
        raise ErroDeValidacao(
            mensagem="Esta missão ainda não foi desbloqueada por você.", campo="missao_id"
        )

    _conferir_forma_unica(forma, texto, arquivo)

    return _ler_e_montar_producao(
        sessao,
        operador=operador,
        equipe_id=None,
        guerreiro_id=operador.id,
        missao_id=missao.id,
        atividade=atividade,
        forma=forma,
        texto=texto,
        arquivo=arquivo,
        tipo_mime=tipo_mime,
        porta=porta,
        armazenamento=armazenamento,
    )


def ler_arquivo_da_producao(
    sessao: Session,
    producao: ProducaoDaMissao | None,
    *,
    operador: Persona,
    armazenamento: PortaDeArmazenamento,
) -> ArquivoDaProducao:
    """Os bytes da mídia da produção, a quem já pode vê-la: quem a entregou
    ou os **integrantes da equipe** dona dela, o **Mestre** da trilha e o
    **Admin** (`RF-01-80`, `RN-01-62`). NEVER SHALL existir rota pública
    equivalente: a produção da missão **não** é item de acervo, porque não
    passa por aprovação — diferente da criação original.
    """
    if producao is None:
        raise NaoEncontrado(mensagem="Produção não encontrada.")

    if operador.papel == Papel.admin:
        pode = True
    elif operador.papel == Papel.mestre:
        # A mesma matriz de posse das demais superfícies: o Mestre **autor**
        # da trilha, nunca qualquer Mestre (`RF-01-16`).
        missao = sessao.get(Missao, producao.missao_id)
        trilha = sessao.get(Trilha, missao.trilha_id) if missao is not None else None
        pode = trilha is not None and trilha.autor_id == operador.id
    elif producao.equipe_id is not None:
        pode = (
            sessao.query(IntegranteDaEquipe)
            .filter_by(equipe_id=producao.equipe_id, persona_id=operador.id)
            .first()
            is not None
        )
    else:
        pode = producao.guerreiro_id == operador.id

    if not pode:
        raise PermissaoNegada(
            mensagem="O arquivo da produção é servido a quem a entregou, à equipe dela e ao "
            "Mestre da trilha."
        )

    if producao.referencia is None:
        raise NaoEncontrado(mensagem="Esta produção não tem arquivo.")
    return ArquivoDaProducao(
        bytes_do_arquivo=armazenamento.ler(referencia=producao.referencia),
        tipo_mime=producao.tipo_do_arquivo or "application/octet-stream",
    )
