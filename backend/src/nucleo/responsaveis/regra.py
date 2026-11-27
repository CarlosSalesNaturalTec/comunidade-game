import uuid

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from ..comunidades.modelo import VinculoJogador
from ..comunidades.regra import comunidades_do_mestre
from ..erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..paginacao import ParametrosDeListagem, codificar_cursor, decodificar_cursor
from ..personas.modelo import Credencial, Nick, Papel, Persona, TipoDeCredencial
from ..personas.regra import (
    credencial_social_ativa,
    criar_persona,
    email_em_uso_por_outra,
    gravar_credencial_de_login_social,
)
from .modelo import VinculoResponsavel

# `RN-01-19`: cada Guerreiro(a) tem no máximo três responsáveis vigentes.
TETO_DE_RESPONSAVEIS = 3


def _email_informado(email: str | None) -> str | None:
    """E-mail vazio ou só de espaços equivale a ausente: no responsável o
    e-mail é opcional (`RF-01-92`)."""
    if email is None or not email.strip():
        return None
    return email.strip()


def _recusar_email_de_outra(sessao: Session, *, email: str, persona: Persona | None) -> None:
    if email_em_uso_por_outra(sessao, email=email, persona=persona):
        raise ErroDeValidacao(mensagem="Este e-mail já é usado por outro cadastro.", campo="email")


def cadastrar_responsavel(
    sessao: Session, *, criado_por: Persona | None, nome: str, email: str | None = None
) -> Persona:
    """O cadastro não dá, por si só, acesso a Guerreiro(a) algum — o que o
    responsável alcança vem do vínculo (`RF-01-13`). `criar_persona` já
    recusa quem não é Admin nem Mestre (`RN-01-01`). O nome é exigido: é
    sobre ele que se apoia o consentimento que autoriza a captura da imagem
    da criança (`RF-04-60`). O e-mail é opcional e, informado, abre o login
    social pela conta Google, como em Mestre e Apoiador (`RF-01-92`,
    decisão do fundador de 2026-11-27).
    """
    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem="O responsável exige o nome.", campo="nome")
    email = _email_informado(email)
    if email is not None:
        _recusar_email_de_outra(sessao, email=email, persona=None)
    persona = criar_persona(
        sessao, papel=Papel.responsavel, criada_por=criado_por, nome=nome, email=email
    )
    if email is not None:
        gravar_credencial_de_login_social(
            sessao, persona=persona, email=email, criada_por=criado_por
        )
        sessao.flush()
    return persona


def buscar_responsavel(sessao: Session, responsavel_id: uuid.UUID) -> Persona:
    persona = sessao.get(Persona, responsavel_id)
    if persona is None or persona.papel != Papel.responsavel:
        raise NaoEncontrado(mensagem="Responsável não encontrado.")
    return persona


def alterar_responsavel(
    sessao: Session, persona: Persona, *, campos: dict[str, str | None], operador: Persona
) -> Persona:
    """Nome e e-mail da ficha, só pelo Admin (`RF-02-121`). Campo ausente
    mantém. Gravar e-mail onde não havia cria a credencial social; trocar
    troca o identificador; retirar desativa a credencial, sem apagá-la, e a
    de usuário e senha segue valendo (`RF-01-92`, design — decisão 3)."""
    if "nome" in campos:
        nome = campos["nome"]
        if not nome or not nome.strip():
            raise ErroDeValidacao(mensagem="O responsável exige o nome.", campo="nome")
        persona.nome = nome
    if "email" in campos:
        email = _email_informado(campos["email"])
        credencial = credencial_social_ativa(sessao, persona)
        if email is None:
            if credencial is not None:
                credencial.ativa = False
            persona.email = None
        elif email != persona.email or credencial is None:
            _recusar_email_de_outra(sessao, email=email, persona=persona)
            if credencial is not None:
                credencial.identificador = email
            else:
                gravar_credencial_de_login_social(
                    sessao, persona=persona, email=email, criada_por=operador
                )
            persona.email = email
    sessao.flush()
    return persona


def acesso_por_responsavel(
    sessao: Session, responsaveis: list[Persona]
) -> dict[uuid.UUID, tuple[str, str]]:
    """O e-mail do login social e o usuário da credencial de usuário e senha,
    só das credenciais ativas, numa consulta por página; nunca senha, hash
    nem troca pendente (`RF-01-92`, design — decisão 5)."""
    acesso: dict[uuid.UUID, tuple[str, str]] = {r.id: ("", "") for r in responsaveis}
    if not responsaveis:
        return acesso
    credenciais = (
        sessao.query(Credencial.persona_id, Credencial.tipo, Credencial.identificador)
        .filter(
            Credencial.persona_id.in_(acesso.keys()),
            Credencial.ativa.is_(True),
            Credencial.tipo.in_([TipoDeCredencial.login_social, TipoDeCredencial.usuario_e_senha]),
        )
        .all()
    )
    for persona_id, tipo, identificador in credenciais:
        email, usuario = acesso[persona_id]
        if tipo == TipoDeCredencial.login_social:
            email = identificador or ""
        else:
            usuario = identificador or ""
        acesso[persona_id] = (email, usuario)
    return acesso


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


def guerreiros_vinculados(sessao: Session, responsavel_id: uuid.UUID) -> list[VinculoResponsavel]:
    """Só os vínculos vigentes — o recorte de leitura do responsável
    (`RF-01-15`). Devolve o vínculo inteiro, e não só o `id` do
    Guerreiro(a), para que a leitura do próprio responsável
    (`GET /v1/eu/guerreiros`) traga o grau de parentesco sem segunda
    consulta (`RF-13-04`, `RF-13-05`).
    """
    return sessao.query(VinculoResponsavel).filter_by(responsavel_id=responsavel_id, fim=None).all()


def guerreiros_vinculaveis(
    sessao: Session, *, mestre: Persona, parametros: ParametrosDeListagem
) -> tuple[list[Persona], str | None]:
    """Guerreiros e Guerreiras ativos da comunidade do vínculo vigente do
    Mestre — sem vínculo, lista vazia, no mesmo molde de
    `aulas.regra.escopo_de_comunidade_da_leitura` (`RF-09-62`, `RN-01-20`,
    `RN-09-18`, decisão do fundador, 2026-08-29, documento 09 §1).
    """
    alvos = comunidades_do_mestre(sessao, mestre=mestre)
    if not alvos:
        return [], None

    consulta = (
        sessao.query(Persona)
        .join(
            VinculoJogador,
            and_(VinculoJogador.guerreiro_id == Persona.id, VinculoJogador.data_fim.is_(None)),
        )
        .filter(
            Persona.papel == Papel.guerreiro,
            VinculoJogador.comunidade_virtual_id.in_(alvos),
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


def responsaveis_vinculados(sessao: Session, guerreiro_id: uuid.UUID) -> list[VinculoResponsavel]:
    """Os vínculos vigentes de um Guerreiro(a) — para o modo assistido
    escolher qual responsável está presente (`RF-13-35`, `RN-13-03`,
    decisão do fundador, 2026-09-01)."""
    return sessao.query(VinculoResponsavel).filter_by(guerreiro_id=guerreiro_id, fim=None).all()


def responsaveis_visiveis(
    sessao: Session, *, operador: Persona, parametros: ParametrosDeListagem
) -> tuple[list[Persona], str | None]:
    """Os responsáveis que o operador em sessão alcança, paginados pelo `id`.

    O Admin alcança todos. O Mestre alcança dois conjuntos somados: os
    responsáveis com vínculo vigente a Guerreiro(a) da comunidade do seu
    vínculo vigente — mesmo recorte de `guerreiros_vinculaveis` — e os que
    **ele próprio cadastrou**, ainda que sem vínculo algum. Sem o segundo
    ramo, o Mestre que cadastra no encontro e sai antes de vincular perde o
    responsável para sempre, que é o defeito que esta leitura existe para
    fechar (`RF-02-111`, `RF-09-122`, decisão do fundador, 2026-09-26).

    Responsável sem vínculo aparece para quem o alcança: é o cadastro
    interrompido. Vínculo encerrado nunca dá alcance, porque só o vigente
    conta (`RN-01-20`, `RN-09-18`).
    """
    consulta = sessao.query(Persona).filter(Persona.papel == Papel.responsavel)

    if operador.papel != Papel.admin:
        alvos = comunidades_do_mestre(sessao, mestre=operador)
        alcance = [Persona.criada_por == operador.id]
        if alvos:
            da_comunidade = (
                sessao.query(VinculoResponsavel.responsavel_id)
                .join(
                    VinculoJogador,
                    and_(
                        VinculoJogador.guerreiro_id == VinculoResponsavel.guerreiro_id,
                        VinculoJogador.data_fim.is_(None),
                    ),
                )
                .filter(
                    VinculoResponsavel.fim.is_(None),
                    VinculoJogador.comunidade_virtual_id.in_(alvos),
                )
            )
            alcance.append(Persona.id.in_(da_comunidade))
        consulta = consulta.filter(or_(*alcance))

    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(Persona.id > id_cursor)

    consulta = consulta.order_by(Persona.id).limit(parametros.tamanho + 1)
    responsaveis = consulta.all()

    proximo_cursor = None
    if len(responsaveis) > parametros.tamanho:
        responsaveis = responsaveis[: parametros.tamanho]
        proximo_cursor = codificar_cursor({"id": str(responsaveis[-1].id)})
    return responsaveis, proximo_cursor


def vinculados_por_responsavel(
    sessao: Session, responsaveis: list[Persona]
) -> dict[uuid.UUID, list[tuple[VinculoResponsavel, str, str]]]:
    """Os vinculados vigentes de uma página inteira de responsáveis, em duas
    consultas em lote — os vínculos, e o nick e o nome dos Guerreiros e
    Guerreiras —, nunca uma por responsável (`RF-02-111`, `RF-09-122`).
    Nick ou nome ausente sai como texto vazio, e quem apresenta decide o que
    dizer, como as demais leituras do núcleo já fazem."""
    if not responsaveis:
        return {}

    ids = {responsavel.id for responsavel in responsaveis}
    vinculos = (
        sessao.query(VinculoResponsavel)
        .filter(VinculoResponsavel.responsavel_id.in_(ids), VinculoResponsavel.fim.is_(None))
        .all()
    )

    identificacao: dict[uuid.UUID, tuple[str, str]] = {}
    if vinculos:
        identificacao = {
            persona_id: (nick or "", nome or "")
            for persona_id, nome, nick in sessao.query(Persona.id, Persona.nome, Nick.valor)
            .outerjoin(Nick, Nick.persona_id == Persona.id)
            .filter(Persona.id.in_({vinculo.guerreiro_id for vinculo in vinculos}))
        }

    por_responsavel: dict[uuid.UUID, list[tuple[VinculoResponsavel, str, str]]] = {
        responsavel.id: [] for responsavel in responsaveis
    }
    for vinculo in vinculos:
        nick, nome = identificacao.get(vinculo.guerreiro_id, ("", ""))
        por_responsavel[vinculo.responsavel_id].append((vinculo, nick, nome))
    return por_responsavel


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
