import uuid
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from ..armazenamento.porta import PortaDeArmazenamento
from ..comunidades.modelo import ComunidadeVirtual
from ..comunidades.regra import resolver_vinculo_na_data
from ..erros import ErroDeValidacao, PermissaoNegada, SerieDeColetaJaAberta
from ..locais.modelo import ORDEM_DOS_NIVEIS, Local, NivelDoLocal
from ..ods.modelo import EtiquetaOds
from ..ods.regra import resolver_etiquetas_da_missao
from ..personas.modelo import Papel, Persona
from ..pontuacao.regra import creditar_pontuacao_da_coleta
from ..tempo import agora
from ..trilhas.modelo import Missao, Trilha
from ..trilhas.regra import conferir_posse_da_trilha
from .modelo import (
    Cadencia,
    DesafioDeColeta,
    EstadoDaSerie,
    FormaDeRegistro,
    OrigemDoRegistro,
    RegistroDeColeta,
    SerieDeColeta,
    SituacaoDoRegistro,
    TipoDeColeta,
)

# O projeto roda no fuso de São Paulo (documento 03 §1): o período civil da
# cadência é apurado nele, nunca em UTC, que é como o núcleo armazena
# (`RN-08-06`, design — decisões).
FUSO_DO_PROJETO = ZoneInfo("America/Sao_Paulo")


def periodo_de_cadencia(
    momento_da_medicao: datetime, cadencia: Cadencia
) -> tuple[datetime, datetime]:
    """Delimita o período civil — dia, semana de segunda a domingo ou mês —
    da data da medição, no fuso do projeto, devolvendo início (inclusive) e
    fim (exclusivo) já convertidos de volta para UTC. Ponto único de
    apuração: a entrega seguinte conta períodos seguidos sem registro com a
    mesma régua (`RN-08-06`, design — decisões).
    """
    local = momento_da_medicao.astimezone(FUSO_DO_PROJETO)

    if cadencia == Cadencia.diaria:
        inicio_local = local.replace(hour=0, minute=0, second=0, microsecond=0)
        fim_local = inicio_local + timedelta(days=1)
    elif cadencia == Cadencia.semanal:
        inicio_do_dia = local.replace(hour=0, minute=0, second=0, microsecond=0)
        inicio_local = inicio_do_dia - timedelta(days=inicio_do_dia.weekday())
        fim_local = inicio_local + timedelta(days=7)
    else:
        inicio_local = local.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if inicio_local.month == 12:
            fim_local = inicio_local.replace(year=inicio_local.year + 1, month=1)
        else:
            fim_local = inicio_local.replace(month=inicio_local.month + 1)

    return inicio_local.astimezone(UTC), fim_local.astimezone(UTC)


def _exigir_admin(operador: Persona) -> None:
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin mantém o catálogo de tipos de coleta.")


def cadastrar_tipo_de_coleta(
    sessao: Session,
    *,
    operador: Persona,
    nome: str | None,
    forma_de_registro: str | None,
    unidade: str | None = None,
    faixa_minima: float | None = None,
    faixa_maxima: float | None = None,
) -> TipoDeColeta:
    """Restrito a Admin (`RF-08-05`); o Mestre escolhe entre os tipos
    cadastrados e nunca cria um novo ao escrever o desafio. Unidade e faixa
    esperada só existem no tipo que se mede por número (`RF-08-12`).
    """
    _exigir_admin(operador)

    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem="Tipo de coleta exige nome.", campo="nome")

    try:
        forma_valida = FormaDeRegistro(forma_de_registro)
    except (ValueError, TypeError) as exc:
        raise ErroDeValidacao(
            mensagem="Forma de registro fora dos valores previstos.",
            campo="forma_de_registro",
        ) from exc

    _conferir_unidade_e_faixa(forma_valida, unidade, faixa_minima, faixa_maxima)

    tipo = TipoDeColeta(
        nome=nome,
        forma_de_registro=forma_valida,
        unidade=unidade,
        faixa_minima=faixa_minima,
        faixa_maxima=faixa_maxima,
        ativo=True,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(tipo)
    sessao.flush()
    return tipo


def _conferir_unidade_e_faixa(
    forma: FormaDeRegistro,
    unidade: str | None,
    faixa_minima: float | None,
    faixa_maxima: float | None,
) -> None:
    if forma == FormaDeRegistro.numero:
        if not unidade or not unidade.strip():
            raise ErroDeValidacao(
                mensagem="Tipo de coleta por número exige unidade de medida.", campo="unidade"
            )
        if faixa_minima is None or faixa_maxima is None:
            raise ErroDeValidacao(
                mensagem="Tipo de coleta por número exige faixa esperada, com mínimo e máximo.",
                campo="faixa_minima",
            )
        if faixa_minima > faixa_maxima:
            raise ErroDeValidacao(
                mensagem="A faixa esperada não pode ter mínimo maior que o máximo.",
                campo="faixa_minima",
            )
    else:
        if unidade is not None or faixa_minima is not None or faixa_maxima is not None:
            raise ErroDeValidacao(
                mensagem="Só o tipo de coleta por número declara unidade e faixa esperada.",
                campo="unidade",
            )


def alterar_tipo_de_coleta(
    sessao: Session,
    tipo: TipoDeColeta,
    *,
    operador: Persona,
    nome: str | None = None,
) -> TipoDeColeta:
    _exigir_admin(operador)
    if nome is not None:
        if not nome.strip():
            raise ErroDeValidacao(mensagem="Tipo de coleta exige nome.", campo="nome")
        tipo.nome = nome
    sessao.flush()
    return tipo


def desativar_tipo_de_coleta(
    sessao: Session, tipo: TipoDeColeta, *, operador: Persona
) -> TipoDeColeta:
    """A desativação nunca altera os desafios já criados com aquele tipo: o
    catálogo governa a escolha, não o que já foi declarado (`RF-08-05`,
    `RF-08-06`)."""
    _exigir_admin(operador)
    tipo.ativo = False
    sessao.flush()
    return tipo


def criar_desafio_de_coleta(
    sessao: Session,
    *,
    operador: Persona,
    missao: Missao | None,
    tipo_de_coleta_id: uuid.UUID | None,
    cadencia: str | None,
    vigencia_inicio: datetime | None,
    vigencia_fim: datetime | None,
    granularidade_exigida: str | None,
    registros_que_pontuam_por_periodo: int | None,
) -> DesafioDeColeta:
    """Criado pelo Mestre autor da trilha, preso a uma missão dela
    (`RF-08-06`). A trilha nunca é declarada: é alcançada por
    `missao.trilha_id`, o mesmo caminho de `criar_etiqueta_ods`
    (design — Decisions). A granularidade exigida é livre — nenhuma
    `ComunidadeVirtual` é lida aqui; o teto é conferido na abertura da série
    (`RN-08-25`).
    """
    if missao is None:
        raise ErroDeValidacao(mensagem="Desafio de coleta exige uma missão.", campo="missao_id")

    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    if tipo_de_coleta_id is None:
        raise ErroDeValidacao(
            mensagem="Desafio de coleta exige um tipo do catálogo.", campo="tipo_de_coleta_id"
        )
    tipo = sessao.get(TipoDeColeta, tipo_de_coleta_id)
    if tipo is None:
        raise ErroDeValidacao(
            mensagem="Tipo de coleta não encontrado no catálogo.", campo="tipo_de_coleta_id"
        )
    if not tipo.ativo:
        raise ErroDeValidacao(
            mensagem="Tipo de coleta desativado não pode ser escolhido.",
            campo="tipo_de_coleta_id",
        )

    if not cadencia:
        raise ErroDeValidacao(mensagem="Desafio de coleta exige cadência.", campo="cadencia")
    try:
        cadencia_valida = Cadencia(cadencia)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Cadência fora dos valores previstos.", campo="cadencia"
        ) from exc

    if vigencia_inicio is None or vigencia_fim is None:
        raise ErroDeValidacao(
            mensagem="Desafio de coleta exige a vigência, com início e fim.",
            campo="vigencia_inicio",
        )
    if vigencia_fim < vigencia_inicio:
        raise ErroDeValidacao(
            mensagem="A vigência não pode terminar antes de começar.", campo="vigencia_fim"
        )

    if not granularidade_exigida:
        raise ErroDeValidacao(
            mensagem="Desafio de coleta exige a granularidade exigida.",
            campo="granularidade_exigida",
        )
    try:
        granularidade_valida = NivelDoLocal(granularidade_exigida)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Granularidade fora dos níveis previstos.", campo="granularidade_exigida"
        ) from exc

    if registros_que_pontuam_por_periodo is None:
        raise ErroDeValidacao(
            mensagem="Desafio de coleta exige quantos registros do período pontuam.",
            campo="registros_que_pontuam_por_periodo",
        )
    if registros_que_pontuam_por_periodo < 1:
        raise ErroDeValidacao(
            mensagem="A quantidade de registros que pontuam por período precisa ser ao menos 1.",
            campo="registros_que_pontuam_por_periodo",
        )

    desafio = DesafioDeColeta(
        missao_id=missao.id,
        tipo_de_coleta_id=tipo.id,
        cadencia=cadencia_valida,
        vigencia_inicio=vigencia_inicio,
        vigencia_fim=vigencia_fim,
        granularidade_exigida=granularidade_valida,
        registros_que_pontuam_por_periodo=registros_que_pontuam_por_periodo,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(desafio)
    sessao.flush()
    return desafio


def resolver_etiquetas_do_desafio(sessao: Session, desafio: DesafioDeColeta) -> list[EtiquetaOds]:
    """Delega inteiramente a `ods.regra.resolver_etiquetas_da_missao`: a
    etiqueta do desafio é derivada, nunca copiada, o que faz "mudar a
    etiqueta da missão muda a do desafio" e "trocar a etiqueta não
    reprocessa pontuação" consequências de não haver nada a sincronizar
    (`RF-08-25`, `RN-08-21`, design — Decisions).
    """
    missao = sessao.get(Missao, desafio.missao_id)
    return resolver_etiquetas_da_missao(sessao, missao)


def abrir_serie_de_coleta(
    sessao: Session,
    *,
    operador: Persona,
    desafio: DesafioDeColeta | None,
    local_id: uuid.UUID | None,
) -> SerieDeColeta:
    """Aberta pelo Guerreiro(a) da sessão sobre um desafio vigente e um
    local da sua própria Comunidade Virtual — nunca sobre local de outra,
    nunca em nome de outro coletor informado no corpo (`RF-08-07`,
    `RN-08-04`). Confere aqui, e não na criação do desafio, o teto de
    granularidade da comunidade (`RN-08-25`).
    """
    if operador.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) abre série de coleta.")
    if desafio is None:
        raise ErroDeValidacao(
            mensagem="Série de coleta exige um desafio de coleta.", campo="desafio_de_coleta_id"
        )

    agora_ = agora()
    if not (desafio.vigencia_inicio <= agora_ <= desafio.vigencia_fim):
        raise ErroDeValidacao(
            mensagem="O desafio de coleta não está vigente.", campo="desafio_de_coleta_id"
        )

    if local_id is None:
        raise ErroDeValidacao(mensagem="Série de coleta exige um local.", campo="local_id")
    local = sessao.get(Local, local_id)
    if local is None:
        raise ErroDeValidacao(mensagem="Local não encontrado.", campo="local_id")

    vinculo = resolver_vinculo_na_data(sessao, guerreiro_id=operador.id, data=agora_)
    if vinculo is None or local.comunidade_virtual_id != vinculo.comunidade_virtual_id:
        raise PermissaoNegada(mensagem="O local escolhido não pertence à sua Comunidade Virtual.")

    comunidade = sessao.get(ComunidadeVirtual, vinculo.comunidade_virtual_id)
    indice_exigido = ORDEM_DOS_NIVEIS.index(desafio.granularidade_exigida)
    indice_teto = ORDEM_DOS_NIVEIS.index(NivelDoLocal(comunidade.granularidade_maxima))
    if indice_exigido > indice_teto:
        raise ErroDeValidacao(
            mensagem="A granularidade exigida pelo desafio é mais fina que o teto da "
            "sua Comunidade Virtual.",
            campo="desafio_de_coleta_id",
        )
    if local.nivel != desafio.granularidade_exigida:
        raise ErroDeValidacao(
            mensagem="O local escolhido não tem o nível exigido pelo desafio.",
            campo="local_id",
        )

    ja_existe = (
        sessao.query(SerieDeColeta)
        .filter_by(coletor_id=operador.id, desafio_de_coleta_id=desafio.id, local_id=local.id)
        .first()
    )
    if ja_existe is not None:
        raise SerieDeColetaJaAberta()

    serie = SerieDeColeta(
        desafio_de_coleta_id=desafio.id,
        coletor_id=operador.id,
        local_id=local.id,
        cadencia=desafio.cadencia,
        estado=EstadoDaSerie.ativa,
    )
    sessao.add(serie)
    sessao.flush()
    return serie


def gravar_registro_de_coleta(
    sessao: Session,
    *,
    operador: Persona,
    serie: SerieDeColeta | None,
    momento_do_fato: datetime | None,
    origem: str | None,
    valor: float | None = None,
    unidade: str | None = None,
    midia_conteudo: bytes | None = None,
    armazenamento: PortaDeArmazenamento | None = None,
) -> RegistroDeColeta:
    """Grava a medição enviada pelo Guerreiro(a) dono da série
    (`RF-08-08`), credita o Poder do Território na mesma transação
    (`RF-08-09`) e atualiza a data da última medição válida da série
    (`RF-08-07`). Somente inserção: não há caminho de alteração nem de
    exclusão (`RN-08-10`, `RN-08-11`).
    """
    if operador.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) registra medição de coleta.")
    if serie is None:
        raise ErroDeValidacao(
            mensagem="Registro de coleta exige uma série de coleta.", campo="serie_de_coleta_id"
        )
    if serie.coletor_id != operador.id:
        raise PermissaoNegada(mensagem="Só o coletor da série registra medição nela.")

    if momento_do_fato is None:
        raise ErroDeValidacao(
            mensagem="Registro de coleta exige a data e hora da medição.",
            campo="momento_do_fato",
        )
    agora_ = agora()
    if momento_do_fato > agora_:
        raise ErroDeValidacao(
            mensagem="A medição não pode ter data e hora no futuro.", campo="momento_do_fato"
        )

    desafio = sessao.get(DesafioDeColeta, serie.desafio_de_coleta_id)
    if not (desafio.vigencia_inicio <= momento_do_fato <= desafio.vigencia_fim):
        raise ErroDeValidacao(
            mensagem="A data da medição está fora da vigência do desafio.",
            campo="momento_do_fato",
        )

    if not origem:
        raise ErroDeValidacao(mensagem="Registro de coleta exige a origem.", campo="origem")
    try:
        origem_valida = OrigemDoRegistro(origem)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Origem fora dos valores previstos.", campo="origem"
        ) from exc
    if origem_valida == OrigemDoRegistro.sensor:
        raise ErroDeValidacao(
            mensagem="A origem 'sensor' exige credencial de dispositivo, ainda não "
            "disponível nesta rota.",
            campo="origem",
        )

    tipo = sessao.get(TipoDeColeta, desafio.tipo_de_coleta_id)

    midia_referencia = None
    if tipo.forma_de_registro == FormaDeRegistro.numero:
        if valor is None:
            raise ErroDeValidacao(
                mensagem="Este tipo de coleta exige valor numérico.", campo="valor"
            )
        if not unidade or not unidade.strip():
            raise ErroDeValidacao(
                mensagem="Este tipo de coleta exige unidade de medida.", campo="unidade"
            )
    else:
        if midia_conteudo is None:
            raise ErroDeValidacao(
                mensagem="Este tipo de coleta exige foto ou vídeo como o registro.",
                campo="midia",
            )
        if armazenamento is None:
            raise ErroDeValidacao(mensagem="Porta de armazenamento não disponível.")
        midia_referencia = f"registros-de-coleta/{uuid.uuid4()}"
        armazenamento.gravar(referencia=midia_referencia, conteudo=midia_conteudo)
        valor = None
        unidade = None

    a_conferir = False
    if (
        tipo.forma_de_registro == FormaDeRegistro.numero
        and tipo.faixa_minima is not None
        and tipo.faixa_maxima is not None
        and not (tipo.faixa_minima <= valor <= tipo.faixa_maxima)
    ):
        a_conferir = True

    vinculo = resolver_vinculo_na_data(sessao, guerreiro_id=operador.id, data=momento_do_fato)
    if vinculo is None:
        raise ErroDeValidacao(
            mensagem="Não há vínculo de Comunidade Virtual na data da medição.",
            campo="momento_do_fato",
        )

    registro = RegistroDeColeta(
        serie_de_coleta_id=serie.id,
        valor=valor,
        unidade=unidade,
        midia_referencia=midia_referencia,
        origem=origem_valida,
        situacao=SituacaoDoRegistro.valida,
        a_conferir=a_conferir,
        comunidade_virtual_id=vinculo.comunidade_virtual_id,
        pontos_creditados=0,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
        momento_do_fato=momento_do_fato,
    )
    sessao.add(registro)
    sessao.flush()

    periodo_inicio, periodo_fim = periodo_de_cadencia(momento_do_fato, serie.cadencia)
    pontos = creditar_pontuacao_da_coleta(
        sessao,
        registro=registro,
        serie=serie,
        desafio=desafio,
        periodo_inicio=periodo_inicio,
        periodo_fim=periodo_fim,
    )
    registro.pontos_creditados = pontos

    serie.ultima_medicao_valida_em = momento_do_fato
    sessao.flush()
    return registro
