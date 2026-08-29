import uuid

from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..comunidades.modelo import VinculoJogador
from ..erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..paginacao import ParametrosDeListagem, codificar_cursor, decodificar_cursor
from ..personas.modelo import Papel, Persona
from ..personas.regra import criar_persona
from .modelo import VinculoResponsavel

# `RN-01-19`: cada Guerreiro(a) tem no máximo três responsáveis vigentes.
TETO_DE_RESPONSAVEIS = 3


def cadastrar_responsavel(sessao: Session, *, criado_por: Persona | None, nome: str) -> Persona:
    """O cadastro não dá, por si só, acesso a Guerreiro(a) algum — o que o
    responsável alcança vem do vínculo (`RF-01-13`). `criar_persona` já
    recusa quem não é Admin nem Mestre (`RN-01-01`). O nome é exigido: é
    sobre ele que se apoia o consentimento que autoriza a captura da imagem
    da criança (`RF-04-60`, design — decisão 1).
    """
    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem="O responsável exige o nome.", campo="nome")
    return criar_persona(sessao, papel=Papel.responsavel, criada_por=criado_por, nome=nome)


def criar_vinculo(
    sessao: Session,
    *,
    responsavel: Persona,
    guerreiro_id: uuid.UUID,
    grau_de_parentesco: str,
    cadastrado_por: Persona,
) -> VinculoResponsavel:
    """Trava a linha do Guerreiro(a) antes de contar os vínculos vigentes,
    para que duas criações simultâneas do quarto vínculo não passem as duas
    (`RN-01-19`, design — decisões).
    """
    if not grau_de_parentesco or not grau_de_parentesco.strip():
        raise ErroDeValidacao(
            mensagem="O vínculo exige o grau de parentesco.", campo="grau_de_parentesco"
        )

    guerreiro = (
        sessao.query(Persona)
        .filter_by(id=guerreiro_id, papel=Papel.guerreiro)
        .with_for_update()
        .first()
    )
    if guerreiro is None:
        raise NaoEncontrado(mensagem="Guerreiro(a) não encontrado.", campo="guerreiro_id")

    vigentes = (
        sessao.query(VinculoResponsavel).filter_by(guerreiro_id=guerreiro.id, fim=None).count()
    )
    if vigentes >= TETO_DE_RESPONSAVEIS:
        raise ErroDeValidacao(
            mensagem="Este Guerreiro(a) já tem três responsáveis vigentes.",
            campo="guerreiro_id",
        )

    vinculo = VinculoResponsavel(
        responsavel_id=responsavel.id,
        guerreiro_id=guerreiro.id,
        grau_de_parentesco=grau_de_parentesco,
        autor_id=cadastrado_por.id,
        papel_do_autor=cadastrado_por.papel.value,
    )
    sessao.add(vinculo)
    sessao.flush()
    return vinculo


def guerreiros_vinculados(sessao: Session, responsavel_id: uuid.UUID) -> list[uuid.UUID]:
    """Só os vínculos vigentes — o recorte de leitura do responsável
    (`RF-01-15`)."""
    linhas = (
        sessao.query(VinculoResponsavel.guerreiro_id)
        .filter_by(responsavel_id=responsavel_id, fim=None)
        .all()
    )
    return [linha[0] for linha in linhas]


def guerreiros_vinculaveis(
    sessao: Session, *, mestre: Persona, parametros: ParametrosDeListagem
) -> tuple[list[Persona], str | None]:
    """Guerreiros e Guerreiras ativos da comunidade do vínculo vigente do
    Mestre — sem vínculo, lista vazia, no mesmo molde de
    `aulas.regra.escopo_de_comunidade_da_leitura` (`RF-09-62`, `RN-01-20`,
    `RN-09-18`, decisão do fundador, 2026-08-29, documento 09 §1).
    """
    vinculo: VinculoJogador | None = mestre.vinculo_vigente
    if vinculo is None:
        return [], None

    consulta = (
        sessao.query(Persona)
        .join(
            VinculoJogador,
            and_(VinculoJogador.guerreiro_id == Persona.id, VinculoJogador.data_fim.is_(None)),
        )
        .filter(
            Persona.papel == Papel.guerreiro,
            VinculoJogador.comunidade_virtual_id == vinculo.comunidade_virtual_id,
        )
    )

    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(Persona.id > id_cursor)

    consulta = consulta.order_by(Persona.id).limit(parametros.tamanho + 1)
    personas = consulta.all()

    proximo_cursor = None
    if len(personas) > parametros.tamanho:
        personas = personas[: parametros.tamanho]
        proximo_cursor = codificar_cursor({"id": str(personas[-1].id)})
    return personas, proximo_cursor


def exigir_vinculo_do_responsavel(
    sessao: Session, *, papel: Papel, responsavel_id: uuid.UUID, guerreiro_id: uuid.UUID
) -> None:
    """Nega por padrão: quando o papel em sessão é responsável, exige vínculo
    vigente com o Guerreiro(a) alvo. Para os demais papéis, quem decide
    continua sendo a matriz de permissões (`RF-01-15`, `RF-01-16`, design —
    decisões). O recorte é o vínculo, não a comunidade: a mesma comunidade
    nunca amplia o alcance de um responsável.
    """
    if papel != Papel.responsavel:
        return
    vinculo_vigente = (
        sessao.query(VinculoResponsavel)
        .filter_by(responsavel_id=responsavel_id, guerreiro_id=guerreiro_id, fim=None)
        .first()
    )
    if vinculo_vigente is None:
        raise PermissaoNegada(
            mensagem="Responsável só alcança os Guerreiros e Guerreiras vinculados a ele."
        )
