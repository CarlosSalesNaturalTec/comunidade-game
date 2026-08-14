import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, PermissaoNegada
from ..locais.modelo import NivelDoLocal
from ..ods.modelo import EtiquetaOds
from ..ods.regra import resolver_etiquetas_da_missao
from ..personas.modelo import Papel, Persona
from ..trilhas.modelo import Missao, Trilha
from ..trilhas.regra import conferir_posse_da_trilha
from .modelo import Cadencia, DesafioDeColeta, FormaDeRegistro, TipoDeColeta


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
