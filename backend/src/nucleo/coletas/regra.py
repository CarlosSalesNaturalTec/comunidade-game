import csv
import io
import uuid
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from sqlalchemy import case, func, tuple_
from sqlalchemy.orm import Session

from ..armazenamento.porta import PortaDeArmazenamento
from ..chaves.segredo import calcular_resumo, gerar_segredo
from ..comunidades.modelo import ComunidadeVirtual
from ..comunidades.regra import resolver_vinculo_na_data
from ..erros import (
    CredencialDeDispositivoJaAtiva,
    ErroDeValidacao,
    NaoEncontrado,
    PermissaoNegada,
    SerieDeColetaJaAberta,
)
from ..locais.modelo import ORDEM_DOS_NIVEIS, Local, NivelDoLocal
from ..locais.regra import resolver_locais_publicados
from ..ods.modelo import EtiquetaOds
from ..ods.regra import resolver_etiquetas_da_missao
from ..paginacao import PaginaDeResultado, codificar_cursor, decodificar_cursor
from ..personas.modelo import Credencial, Papel, Persona, TipoDeCredencial
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


def _contar_periodos_decorridos(ancora: datetime, agora_: datetime, cadencia: Cadencia) -> int:
    """Conta quantos períodos de `periodo_de_cadencia` terminaram por
    inteiro entre a âncora e agora — sem subtrair datas, para que a régua
    valha igual na cadência mensal, cujo período não tem duração fixa
    (design — a régua dos períodos)."""
    _, periodo_fim = periodo_de_cadencia(ancora, cadencia)
    periodos = 0
    while periodo_fim <= agora_:
        periodos += 1
        _, periodo_fim = periodo_de_cadencia(periodo_fim, cadencia)
    return periodos


def _derivar_estado_da_serie(
    serie: SerieDeColeta, desafio: DesafioDeColeta, agora_: datetime
) -> EstadoDaSerie:
    """Fonte da verdade do estado: `encerrada` → `interrompida` → `ativa`
    (design — Decisions). `encerrada` prevalece e é terminal, pelo fim da
    vigência do desafio. `interrompida` conta a partir da última medição
    válida ou, na falta dela, da abertura da série — dois períodos cheios
    sem registro interrompem; um só não interrompe (`RN-08-07`).
    """
    if agora_ > desafio.vigencia_fim:
        return EstadoDaSerie.encerrada

    ancora = serie.ultima_medicao_valida_em or serie.aberta_em
    if _contar_periodos_decorridos(ancora, agora_, serie.cadencia) >= 2:
        return EstadoDaSerie.interrompida

    return EstadoDaSerie.ativa


def apurar_estado_da_serie(sessao: Session, serie: SerieDeColeta) -> EstadoDaSerie:
    """Único ponto de apuração do estado, chamado tanto pela gravação do
    registro quanto pela consulta das séries (design — Decisions). O
    estado derivado é sempre a resposta; a coluna é espelho, gravada só
    quando diverge do derivado — nunca lida como fonte.
    """
    desafio = sessao.get(DesafioDeColeta, serie.desafio_de_coleta_id)
    derivado = _derivar_estado_da_serie(serie, desafio, agora())
    if derivado != serie.estado:
        serie.estado = derivado
        sessao.flush()
    return derivado


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


def _trilha_do_desafio_da_serie(sessao: Session, serie: SerieDeColeta) -> Trilha:
    """Mesmo caminho de `resolver_etiquetas_do_desafio` e
    `criar_desafio_de_coleta`: a trilha nunca é declarada, é alcançada a
    partir da série (design — decisões)."""
    desafio = sessao.get(DesafioDeColeta, serie.desafio_de_coleta_id)
    missao = sessao.get(Missao, desafio.missao_id)
    return sessao.get(Trilha, missao.trilha_id)


def emitir_credencial_de_dispositivo(
    sessao: Session,
    *,
    operador: Persona,
    serie: SerieDeColeta | None,
    identificador: str | None,
    trilha_id: uuid.UUID | None,
) -> tuple[Credencial, str]:
    """Emitida por Admin ou pelo Mestre autor do desafio da série
    (`RF-01-67`, decisão do fundador em `proposal.md`). Guarda só o resumo
    do segredo, reaproveitando os utilitários da chave de aplicação, e
    devolve o segredo em claro uma única vez (`RN-01-35`). Entre as ativas,
    no máximo uma por série — a segunda tentativa é recusada pelo índice
    único parcial, e aqui só antecipamos a recusa com uma mensagem clara
    (`RN-01-53`).
    """
    if serie is None:
        raise ErroDeValidacao(
            mensagem="Credencial de dispositivo exige uma série de coleta.",
            campo="serie_de_coleta_id",
        )
    if not identificador or not identificador.strip():
        raise ErroDeValidacao(
            mensagem="Credencial de dispositivo exige o identificador do aparelho.",
            campo="identificador",
        )
    if trilha_id is None:
        raise ErroDeValidacao(
            mensagem="Credencial de dispositivo exige a trilha em que o aparelho foi construído.",
            campo="trilha_id",
        )

    trilha = _trilha_do_desafio_da_serie(sessao, serie)
    conferir_posse_da_trilha(trilha, operador)

    ja_ativa = (
        sessao.query(Credencial)
        .filter_by(serie_de_coleta_id=serie.id, tipo=TipoDeCredencial.dispositivo, ativa=True)
        .first()
    )
    if ja_ativa is not None:
        raise CredencialDeDispositivoJaAtiva()

    segredo = gerar_segredo()
    credencial = Credencial(
        persona_id=serie.coletor_id,
        tipo=TipoDeCredencial.dispositivo,
        identificador=identificador,
        segredo=calcular_resumo(segredo),
        serie_de_coleta_id=serie.id,
        trilha_id=trilha_id,
        criada_por=operador.id,
        ativa=True,
    )
    sessao.add(credencial)
    sessao.flush()
    return credencial, segredo


def revogar_credencial_de_dispositivo(
    sessao: Session,
    credencial: Credencial | None,
    *,
    operador: Persona,
    motivo: str | None,
) -> Credencial:
    """Admin ou o Mestre autor do desafio revoga a qualquer tempo, com
    motivo e autoria (`RF-01-68`). Não desfaz registro algum: a credencial
    só autentica, o registro é somente inserção (`RN-08-10`)."""
    if credencial is None or credencial.tipo != TipoDeCredencial.dispositivo:
        raise NaoEncontrado(mensagem="Credencial de dispositivo não encontrada.")
    if not motivo or not motivo.strip():
        raise ErroDeValidacao(mensagem="A revogação exige o motivo.", campo="motivo")

    serie = sessao.get(SerieDeColeta, credencial.serie_de_coleta_id)
    trilha = _trilha_do_desafio_da_serie(sessao, serie)
    conferir_posse_da_trilha(trilha, operador)

    credencial.ativa = False
    credencial.revogada_por = str(operador.id)
    credencial.motivo_da_revogacao = motivo
    credencial.revogada_em = agora()
    sessao.flush()
    return credencial


def gravar_registro_de_coleta(
    sessao: Session,
    *,
    operador: Persona,
    serie: SerieDeColeta | None,
    momento_do_fato: datetime | None,
    origem: str | None,
    credencial_de_dispositivo_id: uuid.UUID | None = None,
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

    `credencial_de_dispositivo_id` vem só quando a chamada se autenticou
    por credencial de dispositivo (`RF-08-14`); a autoria continua sendo a
    do coletor da série em qualquer uma das duas origens — o aparelho nunca
    é autor (`RN-08-11`).
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
    if credencial_de_dispositivo_id is None and origem_valida == OrigemDoRegistro.sensor:
        raise ErroDeValidacao(
            mensagem="A origem 'sensor' exige credencial de dispositivo.",
            campo="origem",
        )
    if credencial_de_dispositivo_id is not None and origem_valida != OrigemDoRegistro.sensor:
        raise ErroDeValidacao(
            mensagem="A credencial de dispositivo só grava origem 'sensor'.",
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
        credencial_id=credencial_de_dispositivo_id,
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

    if serie.ultima_medicao_valida_em is None or momento_do_fato > serie.ultima_medicao_valida_em:
        serie.ultima_medicao_valida_em = momento_do_fato
    apurar_estado_da_serie(sessao, serie)

    sessao.flush()
    return registro


class SerieDoGuerreiroSaida(BaseModel):
    id: uuid.UUID
    desafio_de_coleta_id: uuid.UUID
    local_id: uuid.UUID
    cadencia: str
    estado: str
    pontos: int


def consultar_series_do_guerreiro(
    sessao: Session, *, operador: Persona, cursor: str | None, tamanho: int
) -> PaginaDeResultado[SerieDoGuerreiroSaida]:
    """As séries do Guerreiro(a) da sessão, paginadas por cursor no par
    `(aberta_em, id)` — a mesma régua de `paginar_locais` (`RF-01-28`).
    Estado e pontos são apurados só das séries que saem na página, para o
    custo ficar proporcional ao tamanho dela, e não ao total de séries do
    Guerreiro(a) (`RF-08-17`, `RN-08-04`, PRD-08 §9). Nunca alcança série
    de outro coletor, e qualquer outro papel recebe 403.
    """
    if operador.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) consulta as suas séries.")

    consulta = sessao.query(SerieDeColeta).filter_by(coletor_id=operador.id)

    if cursor:
        posicao = decodificar_cursor(cursor)
        try:
            aberta_em_cursor = datetime.fromisoformat(posicao["aberta_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(SerieDeColeta.aberta_em, SerieDeColeta.id) > (aberta_em_cursor, id_cursor)
        )

    consulta = consulta.order_by(SerieDeColeta.aberta_em, SerieDeColeta.id).limit(tamanho + 1)
    series = consulta.all()

    proximo_cursor = None
    if len(series) > tamanho:
        series = series[:tamanho]
        ultima = series[-1]
        proximo_cursor = codificar_cursor(
            {"aberta_em": ultima.aberta_em.isoformat(), "id": str(ultima.id)}
        )

    itens = []
    for serie in series:
        estado = apurar_estado_da_serie(sessao, serie)
        pontos = (
            sessao.query(func.coalesce(func.sum(RegistroDeColeta.pontos_creditados), 0))
            .filter(
                RegistroDeColeta.serie_de_coleta_id == serie.id,
                RegistroDeColeta.situacao == SituacaoDoRegistro.valida,
            )
            .scalar()
        )
        itens.append(
            SerieDoGuerreiroSaida(
                id=serie.id,
                desafio_de_coleta_id=serie.desafio_de_coleta_id,
                local_id=serie.local_id,
                cadencia=serie.cadencia.value,
                estado=estado.value,
                pontos=pontos,
            )
        )
    return PaginaDeResultado(itens=itens, proximo_cursor=proximo_cursor)


class RecortePublicadoSaida(BaseModel):
    tipo_de_coleta_id: uuid.UUID
    tipo_de_coleta_nome: str
    local_publicado_id: uuid.UUID
    local_publicado_nivel: str
    local_publicado_rotulo: str


class PontoDaSeriePublicaSaida(BaseModel):
    momento_da_medicao: datetime
    valor: float | None
    recorte: RecortePublicadoSaida


def _consulta_de_registros_publicaveis(
    sessao: Session,
    *,
    comunidade: ComunidadeVirtual,
    periodo_inicio: datetime | None,
    periodo_fim: datetime | None,
    piso: int,
):
    """Os três passos do design — Decisions: rotula cada registro válido da
    comunidade e do período com (tipo de coleta, local publicado), sobe ao
    nível da comunidade o recorte que não alcança o piso e suprime o que
    ainda não o alcança no topo (`RF-08-16`, `RF-08-28`, `RN-08-24`,
    `RN-08-09`, `RN-08-13`)."""
    mapa_de_local = resolver_locais_publicados(sessao, comunidade_id=comunidade.id)

    rotulados = (
        sessao.query(
            RegistroDeColeta.id.label("registro_id"),
            RegistroDeColeta.momento_do_fato.label("momento_do_fato"),
            RegistroDeColeta.valor.label("valor"),
            SerieDeColeta.coletor_id.label("coletor_id"),
            DesafioDeColeta.tipo_de_coleta_id.label("tipo_de_coleta_id"),
            mapa_de_local.c.local_publicado_id.label("local_publicado_id"),
        )
        .select_from(RegistroDeColeta)
        .join(SerieDeColeta, SerieDeColeta.id == RegistroDeColeta.serie_de_coleta_id)
        .join(DesafioDeColeta, DesafioDeColeta.id == SerieDeColeta.desafio_de_coleta_id)
        .join(mapa_de_local, mapa_de_local.c.local_id == SerieDeColeta.local_id)
        .filter(
            RegistroDeColeta.comunidade_virtual_id == comunidade.id,
            RegistroDeColeta.situacao == SituacaoDoRegistro.valida,
        )
    )
    if periodo_inicio is not None:
        rotulados = rotulados.filter(RegistroDeColeta.momento_do_fato >= periodo_inicio)
    if periodo_fim is not None:
        rotulados = rotulados.filter(RegistroDeColeta.momento_do_fato <= periodo_fim)
    rotulados_sub = rotulados.subquery()

    # Passo 2: conta coletores distintos por recorte e sobe ao nível da
    # comunidade o que não alcança o piso — sem deixar rastro do recorte
    # suprimido, porque o rótulo do bairro simplesmente deixa de existir na
    # linha (design — Decisions).
    contagem_por_recorte = (
        sessao.query(
            rotulados_sub.c.tipo_de_coleta_id,
            rotulados_sub.c.local_publicado_id,
            func.count(func.distinct(rotulados_sub.c.coletor_id)).label("coletores_distintos"),
        )
        .group_by(rotulados_sub.c.tipo_de_coleta_id, rotulados_sub.c.local_publicado_id)
        .subquery()
    )
    # O alvo da subida é o `Local` de nível comunidade, nunca a
    # `ComunidadeVirtual` — é ele que `resolver_locais_publicados` já usa
    # como local publicado de quem está direto nela, e é com ele que a
    # contagem do passo 3 precisa casar (design — Decisions).
    local_da_comunidade_id = (
        sessao.query(Local.id)
        .filter(
            Local.comunidade_virtual_id == comunidade.id, Local.nivel == NivelDoLocal.comunidade
        )
        .order_by(Local.criado_em)
        .limit(1)
        .scalar_subquery()
    )
    local_promovido = case(
        (contagem_por_recorte.c.coletores_distintos < piso, local_da_comunidade_id),
        else_=rotulados_sub.c.local_publicado_id,
    )
    promovidos = (
        sessao.query(
            rotulados_sub.c.registro_id,
            rotulados_sub.c.momento_do_fato,
            rotulados_sub.c.valor,
            rotulados_sub.c.coletor_id,
            rotulados_sub.c.tipo_de_coleta_id,
            local_promovido.label("local_final_id"),
        )
        .select_from(rotulados_sub)
        .join(
            contagem_por_recorte,
            (contagem_por_recorte.c.tipo_de_coleta_id == rotulados_sub.c.tipo_de_coleta_id)
            & (contagem_por_recorte.c.local_publicado_id == rotulados_sub.c.local_publicado_id),
        )
        .subquery()
    )

    # Passo 3: reapura a contagem no nível final — a união dos coletores
    # distintos que ali chegaram, nunca a soma das contagens de origem — e
    # suprime o recorte que ainda não alcança o piso, inclusive no topo.
    contagem_final = (
        sessao.query(
            promovidos.c.tipo_de_coleta_id,
            promovidos.c.local_final_id,
            func.count(func.distinct(promovidos.c.coletor_id)).label("coletores_distintos"),
        )
        .group_by(promovidos.c.tipo_de_coleta_id, promovidos.c.local_final_id)
        .subquery()
    )

    return (
        sessao.query(
            promovidos.c.registro_id,
            promovidos.c.momento_do_fato,
            promovidos.c.valor,
            promovidos.c.tipo_de_coleta_id,
            promovidos.c.local_final_id,
        )
        .select_from(promovidos)
        .join(
            contagem_final,
            (contagem_final.c.tipo_de_coleta_id == promovidos.c.tipo_de_coleta_id)
            & (contagem_final.c.local_final_id == promovidos.c.local_final_id),
        )
        .filter(contagem_final.c.coletores_distintos >= piso)
    )


def paginar_serie_publica(
    sessao: Session,
    *,
    comunidade: ComunidadeVirtual,
    piso_de_coletores: int,
    cursor: str | None,
    tamanho: int,
    periodo_inicio: datetime | None = None,
    periodo_fim: datetime | None = None,
) -> PaginaDeResultado[PontoDaSeriePublicaSaida]:
    """A série pública da comunidade: agregada por tipo de coleta e local,
    parando no bairro, sem coletor e sem mídia — o item paginado é o ponto
    da série, não o recorte (`RF-08-16`, `RN-08-13`, `RN-08-12`, `RN-08-16`,
    `RF-08-21`, `RF-08-28`, `RN-08-24`, `RF-01-28`, design — Decisions).
    Ordenação estável por (tipo, local publicado, momento da medição, id do
    registro), a mesma quádrupla do cursor opaco.
    """
    publicaveis = _consulta_de_registros_publicaveis(
        sessao,
        comunidade=comunidade,
        periodo_inicio=periodo_inicio,
        periodo_fim=periodo_fim,
        piso=piso_de_coletores,
    ).subquery()

    consulta = (
        sessao.query(
            publicaveis.c.registro_id,
            publicaveis.c.momento_do_fato,
            publicaveis.c.valor,
            TipoDeColeta.id.label("tipo_de_coleta_id"),
            TipoDeColeta.nome.label("tipo_de_coleta_nome"),
            Local.id.label("local_publicado_id"),
            Local.nivel.label("local_publicado_nivel"),
            Local.rotulo.label("local_publicado_rotulo"),
        )
        .select_from(publicaveis)
        .join(TipoDeColeta, TipoDeColeta.id == publicaveis.c.tipo_de_coleta_id)
        .join(Local, Local.id == publicaveis.c.local_final_id)
    )

    if cursor:
        posicao = decodificar_cursor(cursor)
        try:
            tipo_cursor = uuid.UUID(posicao["tipo_de_coleta_id"])
            local_cursor = uuid.UUID(posicao["local_publicado_id"])
            momento_cursor = datetime.fromisoformat(posicao["momento_do_fato"])
            id_cursor = uuid.UUID(posicao["registro_id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(
                publicaveis.c.tipo_de_coleta_id,
                publicaveis.c.local_final_id,
                publicaveis.c.momento_do_fato,
                publicaveis.c.registro_id,
            )
            > (tipo_cursor, local_cursor, momento_cursor, id_cursor)
        )

    consulta = consulta.order_by(
        publicaveis.c.tipo_de_coleta_id,
        publicaveis.c.local_final_id,
        publicaveis.c.momento_do_fato,
        publicaveis.c.registro_id,
    ).limit(tamanho + 1)

    linhas = consulta.all()

    proximo_cursor = None
    if len(linhas) > tamanho:
        linhas = linhas[:tamanho]
        ultima = linhas[-1]
        proximo_cursor = codificar_cursor(
            {
                "tipo_de_coleta_id": str(ultima.tipo_de_coleta_id),
                "local_publicado_id": str(ultima.local_publicado_id),
                "momento_do_fato": ultima.momento_do_fato.isoformat(),
                "registro_id": str(ultima.registro_id),
            }
        )

    itens = [
        PontoDaSeriePublicaSaida(
            momento_da_medicao=linha.momento_do_fato,
            valor=linha.valor,
            recorte=RecortePublicadoSaida(
                tipo_de_coleta_id=linha.tipo_de_coleta_id,
                tipo_de_coleta_nome=linha.tipo_de_coleta_nome,
                local_publicado_id=linha.local_publicado_id,
                local_publicado_nivel=linha.local_publicado_nivel.value,
                local_publicado_rotulo=linha.local_publicado_rotulo,
            ),
        )
        for linha in linhas
    ]
    return PaginaDeResultado(itens=itens, proximo_cursor=proximo_cursor)


# Cabeçalho declarado da exportação e o dicionário de dados que descreve cada
# campo — a mesma granularidade real do dado, sem geometria que o Ciclo 01
# não coleta: o local sai como rótulo e nível, nunca como coordenada
# (`RF-08-19`, documento 03 §12.3, design — Decisions).
CABECALHO_DA_EXPORTACAO: tuple[str, ...] = (
    "momento_da_medicao",
    "tipo_de_coleta",
    "local_nivel",
    "local_rotulo",
    "valor",
)

CAMPOS_DO_DICIONARIO_DE_DADOS: tuple[dict[str, str], ...] = (
    {
        "campo": "momento_da_medicao",
        "unidade": "data e hora em ISO 8601 (UTC)",
        "cadencia": "uma linha por medição registrada",
        "origem": "data e hora da medição, gravada pelo Guerreiro(a) no registro de coleta "
        "(RF-08-08)",
    },
    {
        "campo": "tipo_de_coleta",
        "unidade": "texto — nome do tipo de coleta",
        "cadencia": "não se aplica",
        "origem": "catálogo de tipos de coleta, mantido por Admin (RF-08-05)",
    },
    {
        "campo": "local_nivel",
        "unidade": "texto — 'comunidade' ou 'bairro'",
        "cadencia": "não se aplica",
        "origem": "local publicado do registro, agregado ao piso de coletores distintos "
        "(RN-08-13, RF-08-28)",
    },
    {
        "campo": "local_rotulo",
        "unidade": "texto — rótulo do local publicado",
        "cadencia": "não se aplica",
        "origem": "local publicado do registro, agregado ao piso de coletores distintos "
        "(RN-08-13, RF-08-28)",
    },
    {
        "campo": "valor",
        "unidade": "numérico, na unidade do tipo de coleta; vazio quando o tipo se mede por "
        "foto ou vídeo",
        "cadencia": "uma medição por registro, na cadência da série de coleta",
        "origem": "valor informado pelo Guerreiro(a) no registro de coleta (RF-08-08)",
    },
)


class ExportacaoDoTerritorio(BaseModel):
    conteudo_csv: str
    periodo_coberto_inicio: datetime | None
    periodo_coberto_fim: datetime | None


def exportar_serie_do_territorio(
    sessao: Session,
    *,
    comunidade: ComunidadeVirtual,
    piso_de_coletores: int,
    periodo_inicio: datetime | None = None,
    periodo_fim: datetime | None = None,
) -> ExportacaoDoTerritorio:
    """A exportação pública do território em CSV: chama
    `_consulta_de_registros_publicaveis` com os mesmos argumentos da série
    pública, sem reimplementar corte, piso ou supressão — a exportação
    herda integralmente as mesmas guardas (`RF-08-19`, `RN-08-12`,
    `RN-08-13`, `RF-08-28`, `RN-08-24`, design — Decisions). Uma tabela por
    arquivo, cabeçalho declarado na primeira linha, local como rótulo e
    nível. O período coberto é apurado da primeira e da última medição
    efetivamente contidas no conjunto, depois do piso — conjunto vazio
    declara período vazio (`RF-08-27`, design — Decisions).
    """
    publicaveis = _consulta_de_registros_publicaveis(
        sessao,
        comunidade=comunidade,
        periodo_inicio=periodo_inicio,
        periodo_fim=periodo_fim,
        piso=piso_de_coletores,
    ).subquery()

    linhas = (
        sessao.query(
            publicaveis.c.momento_do_fato,
            publicaveis.c.valor,
            TipoDeColeta.nome.label("tipo_de_coleta_nome"),
            Local.nivel.label("local_nivel"),
            Local.rotulo.label("local_rotulo"),
        )
        .select_from(publicaveis)
        .join(TipoDeColeta, TipoDeColeta.id == publicaveis.c.tipo_de_coleta_id)
        .join(Local, Local.id == publicaveis.c.local_final_id)
        .order_by(publicaveis.c.momento_do_fato, publicaveis.c.registro_id)
        .all()
    )

    buffer = io.StringIO(newline="")
    escritor = csv.writer(buffer)
    escritor.writerow(CABECALHO_DA_EXPORTACAO)
    for linha in linhas:
        escritor.writerow(
            [
                linha.momento_do_fato.isoformat(),
                linha.tipo_de_coleta_nome,
                linha.local_nivel.value,
                linha.local_rotulo,
                "" if linha.valor is None else linha.valor,
            ]
        )

    if linhas:
        periodo_coberto_inicio = linhas[0].momento_do_fato
        periodo_coberto_fim = linhas[-1].momento_do_fato
    else:
        periodo_coberto_inicio = None
        periodo_coberto_fim = None

    return ExportacaoDoTerritorio(
        conteudo_csv=buffer.getvalue(),
        periodo_coberto_inicio=periodo_coberto_inicio,
        periodo_coberto_fim=periodo_coberto_fim,
    )


def apurar_periodo_coberto_da_exportacao(
    sessao: Session,
    *,
    comunidade: ComunidadeVirtual,
    piso_de_coletores: int,
    periodo_inicio: datetime | None = None,
    periodo_fim: datetime | None = None,
) -> tuple[datetime | None, datetime | None]:
    """O mesmo período que `exportar_serie_do_territorio` declara, apurado
    sem serializar o conjunto — a rota irmã do dicionário de dados devolve a
    mesma declaração sem gerar o CSV inteiro (`RF-08-27`)."""
    publicaveis = _consulta_de_registros_publicaveis(
        sessao,
        comunidade=comunidade,
        periodo_inicio=periodo_inicio,
        periodo_fim=periodo_fim,
        piso=piso_de_coletores,
    ).subquery()
    inicio, fim = sessao.query(
        func.min(publicaveis.c.momento_do_fato), func.max(publicaveis.c.momento_do_fato)
    ).one()
    return inicio, fim
