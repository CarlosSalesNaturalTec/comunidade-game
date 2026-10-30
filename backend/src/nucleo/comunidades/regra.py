import uuid
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Query, Session

from ..coletas.modelo import DesafioDeColeta, SerieDeColeta, TipoDeColeta
from ..erros import ErroDeValidacao, PermissaoNegada
from ..locais.modelo import Local, NivelDoLocal
from ..personas.modelo import Papel, Persona
from .modelo import ComunidadeVirtual, VinculoDoMestre, VinculoJogador


def criar_comunidade(
    sessao: Session,
    *,
    operador: Persona,
    nome: str | None,
    localizacao: str | None,
    granularidade_maxima: str | None,
) -> ComunidadeVirtual:
    """Só Admin cria a Comunidade Virtual, que nasce vazia (`RF-08-01`,
    `RN-08-01`)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin cria a Comunidade Virtual.")
    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem="Comunidade exige nome.", campo="nome")
    if not localizacao or not localizacao.strip():
        raise ErroDeValidacao(mensagem="Comunidade exige localização.", campo="localizacao")
    if not granularidade_maxima or not granularidade_maxima.strip():
        raise ErroDeValidacao(
            mensagem="Comunidade exige granularidade máxima.", campo="granularidade_maxima"
        )

    comunidade = ComunidadeVirtual(
        nome=nome,
        localizacao=localizacao,
        granularidade_maxima=granularidade_maxima,
        admin_criador_id=operador.id,
    )
    sessao.add(comunidade)
    sessao.flush()
    return comunidade


def abrir_vinculo(
    sessao: Session,
    *,
    guerreiro: Persona,
    comunidade_id: uuid.UUID,
) -> VinculoJogador:
    """Abre o vínculo vigente do Guerreiro(a) com a comunidade, recusando um
    segundo vigente (`RF-08-02`, `RN-08-02`, `RN-01-05`). O índice parcial
    único de `VinculoJogador` garante a unicidade sob concorrência; aqui a
    recusa é traduzida para mensagem simples antes de a gravação alcançar o
    banco (design — Decisions).
    """
    if guerreiro.papel != Papel.guerreiro:
        raise ErroDeValidacao(mensagem="Só o Guerreiro(a) tem vínculo de comunidade.")

    vigente = (
        sessao.query(VinculoJogador).filter_by(guerreiro_id=guerreiro.id, data_fim=None).first()
    )
    if vigente is not None:
        raise ErroDeValidacao(
            mensagem="Este Guerreiro(a) já tem um vínculo de comunidade vigente.",
            campo="comunidade_id",
        )

    vinculo = VinculoJogador(guerreiro_id=guerreiro.id, comunidade_virtual_id=comunidade_id)
    sessao.add(vinculo)
    sessao.flush()
    return vinculo


def abrir_vinculo_do_mestre(
    sessao: Session,
    *,
    mestre: Persona,
    comunidade_id: uuid.UUID,
) -> VinculoDoMestre | None:
    """Abre o vínculo do Mestre com a comunidade, no agendamento da aula
    (`RF-02-30`, decisão do fundador de 2026-10-30). Devolve `None` quando
    o vínculo já existe: escalar o mesmo Mestre noutra aula da mesma
    comunidade não abre um segundo.

    Diferente de `abrir_vinculo`, não há vigência a conferir — o vínculo do
    Mestre não tem `data_fim` e nunca encerra no Ciclo 01.
    """
    if mestre.papel != Papel.mestre:
        raise ErroDeValidacao(
            mensagem="Só o Mestre tem vínculo de Mestre com comunidade.", campo="mestre_id"
        )

    existente = (
        sessao.query(VinculoDoMestre)
        .filter_by(mestre_id=mestre.id, comunidade_virtual_id=comunidade_id)
        .first()
    )
    if existente is not None:
        return None

    vinculo = VinculoDoMestre(mestre_id=mestre.id, comunidade_virtual_id=comunidade_id)
    sessao.add(vinculo)
    sessao.flush()
    return vinculo


def comunidades_do_mestre(sessao: Session, *, mestre: Persona) -> set[uuid.UUID]:
    """As comunidades a que o Mestre está vinculado — o plural que as specs
    de `aula-e-presenca`, `patrimonio`, `necessidade-de-recurso` e
    `responsavel-e-vinculo` já escreviam e que o núcleo não tinha como
    servir, porque lia `Persona.vinculo_vigente`, que é do Guerreiro(a) e
    resolve sempre nulo para Mestre.

    Mestre ainda não escalado em aula alguma devolve conjunto **vazio** —
    lista vazia nas leituras, nunca erro.
    """
    linhas = (
        sessao.query(VinculoDoMestre.comunidade_virtual_id).filter_by(mestre_id=mestre.id).all()
    )
    return {linha[0] for linha in linhas}


def escopo_de_comunidade_da_leitura(
    sessao: Session,
    *,
    operador: Persona,
    comunidade_virtual_id: uuid.UUID | None,
    mensagem_de_recusa: str,
) -> set[uuid.UUID]:
    """O escopo por comunidade de toda leitura de gestão, num lugar só:
    Admin declara a comunidade, sempre obrigatória, e recebe o conjunto de
    uma; Mestre recebe as dele; conjunto **vazio** significa lista vazia,
    nunca erro. Demais papéis são recusados com a mensagem de quem chama.

    Substitui as três cópias que `aulas/regra.py`, `pontos_de_apoio/regra.py`
    e `patrimonio.listar_acervo` mantinham — as duas primeiras declarando,
    no próprio docstring, que eram "no molde de `listar_acervo`" (design —
    decisão 3).
    """
    if operador.papel == Papel.admin:
        if comunidade_virtual_id is None:
            raise ErroDeValidacao(
                mensagem="Esta consulta exige o filtro de comunidade.", campo="comunidade"
            )
        return {comunidade_virtual_id}
    if operador.papel == Papel.mestre:
        return comunidades_do_mestre(sessao, mestre=operador)
    raise PermissaoNegada(mensagem=mensagem_de_recusa)


def filtrar_personas_por_comunidades(consulta: Query, comunidade_ids: set[uuid.UUID]) -> Query:
    """O irmão plural de `filtrar_personas_por_comunidade`, para quem recorta
    pelo escopo de um Mestre — que é N comunidades desde 2026-10-30. O
    singular continua servindo os quatro pontos que recortam por **uma**
    comunidade declarada (pontuação, vitrine e as duas leituras de ODS).
    """
    return unir_vinculo_vigente(consulta).filter(
        VinculoJogador.comunidade_virtual_id.in_(comunidade_ids)
    )


def resolver_vinculo_na_data(
    sessao: Session, *, guerreiro_id: uuid.UUID, data: datetime
) -> VinculoJogador | None:
    """Localiza o vínculo do Guerreiro(a) cujo intervalo `[data_inicio,
    data_fim)` contém `data` — `data_fim` nulo é tratado como aberto. É o
    que prende o registro de coleta à comunidade vigente **na data da
    medição**, e não à comunidade corrente do coletor (`RN-08-03`, design —
    decisões)."""
    return (
        sessao.query(VinculoJogador)
        .filter(
            VinculoJogador.guerreiro_id == guerreiro_id,
            VinculoJogador.data_inicio <= data,
            (VinculoJogador.data_fim.is_(None)) | (VinculoJogador.data_fim > data),
        )
        .first()
    )


def unir_vinculo_vigente(consulta: Query) -> Query:
    """Junta uma consulta que já tem `Persona` no `FROM` ao vínculo vigente
    de cada Guerreiro(a) — a junção que os seis pontos de leitura antigos
    dispensavam, lendo direto a coluna que saiu de `Persona` (`RN-01-05`,
    design — Decisions)."""
    return consulta.join(
        VinculoJogador,
        (VinculoJogador.guerreiro_id == Persona.id) & VinculoJogador.data_fim.is_(None),
    )


def filtrar_personas_por_comunidade(consulta: Query, comunidade_id: uuid.UUID) -> Query:
    """Filtro por comunidade sobre o vínculo vigente — substitui a
    comparação direta de `Persona.comunidade_virtual_id` nos seis pontos de
    leitura que a coluna deixou (`RN-01-05`, design — Decisions)."""
    return unir_vinculo_vigente(consulta).filter(
        VinculoJogador.comunidade_virtual_id == comunidade_id
    )


def contar_guerreiros_vinculados(sessao: Session, comunidade_id: uuid.UUID) -> int:
    """A **vitalidade** da comunidade do documento 11 §§8.2 e 8.3: quantos
    Guerreiros e Guerreiras têm vínculo vigente com ela. Não é indicador do
    documento 02 §1 — não entra na supressão por piso, que é de coletores
    distintos no recorte publicado — e sai como contagem, nunca como lista
    de pessoas (`RF-03-02`, `RF-03-16`, `RN-01-05`, decisão do fundador de
    2026-09-28)."""
    return (
        sessao.query(func.count(VinculoJogador.id))
        .filter(
            VinculoJogador.comunidade_virtual_id == comunidade_id,
            VinculoJogador.data_fim.is_(None),
        )
        .scalar()
        or 0
    )


class LocalPublicoSaida(BaseModel):
    id: uuid.UUID
    nivel: str
    rotulo: str
    local_pai_id: uuid.UUID | None


class TipoDeColetaPublicoSaida(BaseModel):
    id: uuid.UUID
    nome: str


class ComunidadePublicaSaida(BaseModel):
    id: uuid.UUID
    nome: str
    locais: list[LocalPublicoSaida]
    tipos_de_coleta: list[TipoDeColetaPublicoSaida]
    guerreiros_vinculados: int


def consultar_comunidade_publica(
    sessao: Session, *, comunidade: ComunidadeVirtual
) -> ComunidadePublicaSaida:
    """Leitura pública da comunidade: os locais até o bairro — nunca de rua
    ou abaixo — e os tipos de coleta sobre os quais há série aberta nela,
    nunca os do catálogo sem série ali (`RF-08-16`, `RN-08-13`, PRD-08 §9).
    """
    locais = (
        sessao.query(Local)
        .filter(
            Local.comunidade_virtual_id == comunidade.id,
            Local.nivel.in_([NivelDoLocal.comunidade, NivelDoLocal.bairro]),
        )
        .order_by(Local.criado_em, Local.id)
        .all()
    )
    tipos = (
        sessao.query(TipoDeColeta)
        .join(DesafioDeColeta, DesafioDeColeta.tipo_de_coleta_id == TipoDeColeta.id)
        .join(SerieDeColeta, SerieDeColeta.desafio_de_coleta_id == DesafioDeColeta.id)
        .join(Local, Local.id == SerieDeColeta.local_id)
        .filter(Local.comunidade_virtual_id == comunidade.id)
        .distinct()
        .order_by(TipoDeColeta.nome)
        .all()
    )
    return ComunidadePublicaSaida(
        id=comunidade.id,
        nome=comunidade.nome,
        locais=[
            LocalPublicoSaida(
                id=local.id,
                nivel=local.nivel.value,
                rotulo=local.rotulo,
                local_pai_id=local.local_pai_id,
            )
            for local in locais
        ],
        tipos_de_coleta=[TipoDeColetaPublicoSaida(id=tipo.id, nome=tipo.nome) for tipo in tipos],
        guerreiros_vinculados=contar_guerreiros_vinculados(sessao, comunidade.id),
    )
