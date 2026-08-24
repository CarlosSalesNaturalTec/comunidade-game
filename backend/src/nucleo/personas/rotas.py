import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula, ModoDeComprovacao
from ..aulas.regra import registrar_presenca
from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..chaves.conferencia import ContextoDaChave, exigir_chave_de_aplicacao
from ..configuracao import Configuracao, obter_configuracao
from ..erros import ErroDeValidacao, NaoEncontrado, NickDeGuerreiroEmUsoNoEncontro, PermissaoNegada
from ..paginacao import (
    PaginaDeResultado,
    ParametrosDeListagem,
    codificar_cursor,
    contrato_de_listagem,
    decodificar_cursor,
)
from ..permissoes import Operacao, conferir_permissao, exigir_permissao
from ..protecao.freio import exigir_freio_por_origem
from ..tempo import agora
from .credenciais import criar_credencial_provisoria
from .modelo import ArtefatoComprobatorio, Credencial, Nick, Papel, Persona, TipoDeCredencial
from .regra import (
    MENSAGEM_NICK_EM_USO,
    cadastrar_adulto_com_artefatos,
    cadastrar_guerreiro_no_encontro,
    cadastrar_guerreiro_pela_gestao,
    conferir_disponibilidade_de_nick,
    definir_ou_trocar_nick,
    editar_guerreiro,
    incluir_admin,
    sugerir_variacoes_de_nick,
    sugerir_variacoes_de_nick_com_alcance_total,
)
from .senha import calcular_hash

roteador = APIRouter()

# `POST /v1/guerreiros` atende os dois caminhos que o design — decisão 1
# separa pela aplicação declarada na chave: só a App 01 leva ao caminho do
# encontro, qualquer outra ao da gestão.
_APLICACAO_DO_ENCONTRO = "app-01-aula-presencial"


def _paginar_personas(
    sessao_bd: Session, *, papel: Papel, parametros: ParametrosDeListagem
) -> tuple[list[Persona], str | None]:
    """Paginação comum às três listas de persona por papel — cursor pelo
    `id`, sem filtro de domínio (`RF-02-01`, `RF-02-02`, `RF-02-03`)."""
    consulta = sessao_bd.query(Persona).filter_by(papel=papel)

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


class GuerreiroSaida(BaseModel):
    id: uuid.UUID
    nome: str
    nascimento: date
    nick: str
    avatar: str


def _saida_do_guerreiro(persona: Persona, sessao_bd: Session) -> GuerreiroSaida:
    nick = sessao_bd.query(Nick).filter_by(persona_id=persona.id).first()
    return GuerreiroSaida(
        id=persona.id,
        nome=persona.nome or "",
        nascimento=persona.nascimento,
        nick=nick.valor if nick is not None else "",
        avatar=persona.avatar or "",
    )


class CadastrarGuerreiroEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1)
    nascimento: date
    nick: str = Field(min_length=1)
    avatar: str = Field(min_length=1)
    aula_id: uuid.UUID


def _exigir_permissao_de_cadastro_de_guerreiro(
    contexto_da_chave: Annotated[ContextoDaChave, Depends(exigir_chave_de_aplicacao)],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
) -> None:
    """A chave escolhe a operação exigida, nunca concede acesso sozinha — a
    autorização continua inteira na matriz (design — decisão 1). Chave da
    App 01 exige a operação do cadastro no encontro, que Mestre e Admin têm;
    qualquer outra exige `Operacao.tudo`, que só o Admin tem."""
    operacao = (
        Operacao.cadastro_do_guerreiro_no_encontro
        if contexto_da_chave.aplicacao == _APLICACAO_DO_ENCONTRO
        else Operacao.tudo
    )
    if not conferir_permissao(contexto.papel, "escreve", operacao):
        raise PermissaoNegada()


@roteador.post("/guerreiros", status_code=201)
def cadastrar_guerreiro_rota(
    entrada: CadastrarGuerreiroEntrada,
    _: Annotated[None, Depends(_exigir_permissao_de_cadastro_de_guerreiro)],
    contexto_da_chave: Annotated[ContextoDaChave, Depends(exigir_chave_de_aplicacao)],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> GuerreiroSaida:
    """Dois caminhos pela mesma rota (`RF-02-01`, `RF-04-07`, design —
    decisão 1): chave da App 01 leva ao caminho do encontro, autocadastro do
    próprio Guerreiro(a) com presença gravada no mesmo ato; qualquer outra
    chave leva ao caminho da gestão, restrito a Admin, como hoje. A
    comunidade vem sempre da aula agendada em que o Guerreiro(a) se
    cadastra, nunca de quem o cadastra (`RF-08-02`, `RN-08-02`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, entrada.aula_id)
    if aula is None:
        raise NaoEncontrado(mensagem="Aula não encontrada.", campo="aula_id")

    if contexto_da_chave.aplicacao == _APLICACAO_DO_ENCONTRO:
        try:
            persona = cadastrar_guerreiro_no_encontro(
                sessao_bd,
                nome=entrada.nome,
                nascimento=entrada.nascimento,
                nick=entrada.nick,
                avatar=entrada.avatar,
                aula=aula,
            )
        except ErroDeValidacao as exc:
            if exc.campo == "nick" and exc.mensagem == MENSAGEM_NICK_EM_USO:
                sugestoes = sugerir_variacoes_de_nick_com_alcance_total(sessao_bd, entrada.nick)
                raise NickDeGuerreiroEmUsoNoEncontro(sugestoes=sugestoes) from exc
            raise

        # RF-04-17: a presença do dia acompanha o cadastro no mesmo ato —
        # um único `commit` mais abaixo grava os dois juntos, ou nenhum dos
        # dois (design — decisão 5). Confirmador é o adulto da sessão de
        # trabalho, nunca reconhecimento: não há captura nesta fatia.
        registrar_presenca(
            sessao_bd,
            operador=operador,
            aula=aula,
            guerreiro=persona,
            modo=ModoDeComprovacao.confirmacao.value,
            confirmador=operador,
            momento_do_fato=agora(),
        )
    else:
        persona = cadastrar_guerreiro_pela_gestao(
            sessao_bd,
            operador=operador,
            nome=entrada.nome,
            nascimento=entrada.nascimento,
            nick=entrada.nick,
            avatar=entrada.avatar,
            aula=aula,
        )

    sessao_bd.commit()
    return _saida_do_guerreiro(persona, sessao_bd)


@roteador.get("/guerreiros", response_model=PaginaDeResultado[GuerreiroSaida])
def listar_guerreiros_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "le"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[GuerreiroSaida]:
    """Restrita a Admin — a gestão apresenta os Guerreiros e Guerreiras já
    cadastrados antes de oferecer um novo cadastro (`RF-02-01`)."""
    personas, proximo_cursor = _paginar_personas(
        sessao_bd, papel=Papel.guerreiro, parametros=parametros
    )
    return PaginaDeResultado(
        itens=[_saida_do_guerreiro(persona, sessao_bd) for persona in personas],
        proximo_cursor=proximo_cursor,
    )


class EditarGuerreiroEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1)
    nascimento: date
    nick: str = Field(min_length=1)
    avatar: str = Field(min_length=1)


@roteador.patch("/guerreiros/{id}")
def editar_guerreiro_rota(
    id: uuid.UUID,
    entrada: EditarGuerreiroEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "escreve"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> GuerreiroSaida:
    """Restrita a Admin. NEVER apaga a persona nem troca o papel dela — só
    atualiza os quatro campos (`RF-02-01`, `RN-02-21`)."""
    persona = sessao_bd.get(Persona, id)
    if persona is None or persona.papel != Papel.guerreiro:
        raise NaoEncontrado(mensagem="Guerreiro(a) não encontrado.", campo="id")

    persona = editar_guerreiro(
        sessao_bd,
        persona,
        nome=entrada.nome,
        nascimento=entrada.nascimento,
        nick=entrada.nick,
        avatar=entrada.avatar,
    )
    sessao_bd.commit()
    return _saida_do_guerreiro(persona, sessao_bd)


class ArtefatoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    endereco: str = Field(min_length=1)
    rotulo: str = Field(min_length=1)


class ArtefatoSaida(BaseModel):
    endereco: str
    rotulo: str


class AdultoSaida(BaseModel):
    id: uuid.UUID
    nome: str
    email: str
    whatsapp: str | None
    nick: str | None
    artefatos: list[ArtefatoSaida]


def _saida_do_adulto(persona: Persona, sessao_bd: Session) -> AdultoSaida:
    nick = sessao_bd.query(Nick).filter_by(persona_id=persona.id).first()
    artefatos = sessao_bd.query(ArtefatoComprobatorio).filter_by(persona_id=persona.id).all()
    return AdultoSaida(
        id=persona.id,
        nome=persona.nome or "",
        email=persona.email or "",
        whatsapp=persona.whatsapp,
        nick=nick.valor if nick is not None else None,
        artefatos=[ArtefatoSaida(endereco=a.endereco, rotulo=a.rotulo) for a in artefatos],
    )


class CadastrarAdultoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1)
    email: str = Field(min_length=1)
    whatsapp: str | None = None
    nick: str | None = None
    artefatos: list[ArtefatoEntrada] = Field(default_factory=list)


@roteador.post("/mestres", status_code=201)
def cadastrar_mestre_rota(
    entrada: CadastrarAdultoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "escreve"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AdultoSaida:
    """Restrita a Admin, com o artefato comprobatório obrigatório
    (`RF-02-02`, `RF-02-04`, `RN-02-01`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    persona = cadastrar_adulto_com_artefatos(
        sessao_bd,
        papel=Papel.mestre,
        operador=operador,
        nome=entrada.nome,
        email=entrada.email,
        whatsapp=entrada.whatsapp,
        nick=entrada.nick,
        artefatos=[(artefato.endereco, artefato.rotulo) for artefato in entrada.artefatos],
    )
    sessao_bd.commit()
    return _saida_do_adulto(persona, sessao_bd)


@roteador.get("/mestres", response_model=PaginaDeResultado[AdultoSaida])
def listar_mestres_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "le"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[AdultoSaida]:
    """Restrita a Admin — sinaliza quem está sem nick, sem sugerir nenhum
    (`RF-02-01`, `RN-14-10`)."""
    personas, proximo_cursor = _paginar_personas(
        sessao_bd, papel=Papel.mestre, parametros=parametros
    )
    return PaginaDeResultado(
        itens=[_saida_do_adulto(persona, sessao_bd) for persona in personas],
        proximo_cursor=proximo_cursor,
    )


@roteador.post("/apoiadores", status_code=201)
def cadastrar_apoiador_rota(
    entrada: CadastrarAdultoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "escreve"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AdultoSaida:
    """Restrita a Admin, com o artefato comprobatório obrigatório
    (`RF-02-03`, `RF-02-04`, `RN-02-01`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    persona = cadastrar_adulto_com_artefatos(
        sessao_bd,
        papel=Papel.apoiador,
        operador=operador,
        nome=entrada.nome,
        email=entrada.email,
        whatsapp=entrada.whatsapp,
        nick=entrada.nick,
        artefatos=[(artefato.endereco, artefato.rotulo) for artefato in entrada.artefatos],
    )
    sessao_bd.commit()
    return _saida_do_adulto(persona, sessao_bd)


@roteador.get("/apoiadores", response_model=PaginaDeResultado[AdultoSaida])
def listar_apoiadores_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "le"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[AdultoSaida]:
    """Restrita a Admin — sinaliza quem está sem nick, sem sugerir nenhum
    (`RF-02-01`, `RN-14-10`)."""
    personas, proximo_cursor = _paginar_personas(
        sessao_bd, papel=Papel.apoiador, parametros=parametros
    )
    return PaginaDeResultado(
        itens=[_saida_do_adulto(persona, sessao_bd) for persona in personas],
        proximo_cursor=proximo_cursor,
    )


class IncluirAdminEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1)
    email: str = Field(min_length=1)
    whatsapp: str | None = None


class AdminSaida(BaseModel):
    id: uuid.UUID
    nome: str
    email: str
    whatsapp: str | None


@roteador.post("/admins", status_code=201)
def incluir_admin_rota(
    entrada: IncluirAdminEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "escreve"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AdminSaida:
    """Restrita a Admin — único caminho de entrada de um Admin novo
    (`RF-02-05`, `RN-02-02`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    persona = incluir_admin(
        sessao_bd,
        operador=operador,
        nome=entrada.nome,
        email=entrada.email,
        whatsapp=entrada.whatsapp,
    )
    sessao_bd.commit()
    return AdminSaida(
        id=persona.id,
        nome=persona.nome or "",
        email=persona.email or "",
        whatsapp=persona.whatsapp,
    )


class GravarNickDoAdultoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nick: str = Field(min_length=1)


class NickGravadoSaida(BaseModel):
    nick: str


@roteador.patch("/personas/{id}/nick")
def gravar_nick_do_adulto_rota(
    id: uuid.UUID,
    entrada: GravarNickDoAdultoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "escreve"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> NickGravadoSaida:
    """Desfecho da colisão de nick: o Admin grava aqui o nick que a pessoa
    lhe passou por canal fora da plataforma. NEVER alcança persona de
    Guerreiro(a) — o nick da criança se edita pela rota de edição dela
    (`RF-02-01`, `RN-01-30`, `RN-14-10`)."""
    persona_alvo = sessao_bd.get(Persona, id)
    if persona_alvo is None or persona_alvo.papel not in (Papel.mestre, Papel.apoiador):
        raise NaoEncontrado(mensagem="Persona não encontrada.", campo="id")

    definir_ou_trocar_nick(sessao_bd, persona_alvo, entrada.nick)
    sessao_bd.commit()
    return NickGravadoSaida(nick=entrada.nick)


class CriarCredencialEntrada(BaseModel):
    persona_id: uuid.UUID
    usuario: str


class CredencialSaida(BaseModel):
    id: uuid.UUID
    usuario: str
    senha_provisoria: str


@roteador.post("/credenciais", status_code=201)
def criar_credencial(
    entrada: CriarCredencialEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> CredencialSaida:
    """Restrita a Admin e Mestre — `criar_credencial_provisoria` recusa com
    403 quem não é (`RF-01-11`, `RF-01-16`)."""
    persona_alvo = sessao_bd.get(Persona, entrada.persona_id)
    if persona_alvo is None:
        raise NaoEncontrado(mensagem="Persona não encontrada.", campo="persona_id")

    criada_por = sessao_bd.get(Persona, contexto.persona_id)
    credencial, senha_provisoria = criar_credencial_provisoria(
        sessao_bd,
        configuracao,
        persona=persona_alvo,
        usuario=entrada.usuario,
        criada_por=criada_por,
    )
    sessao_bd.commit()
    return CredencialSaida(
        id=credencial.id, usuario=credencial.identificador, senha_provisoria=senha_provisoria
    )


class TrocarSenhaEntrada(BaseModel):
    senha_nova: str


@roteador.post("/credenciais/senha", status_code=204)
def trocar_senha(
    entrada: TrocarSenhaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> None:
    """Conclui a troca e derruba a pendência (`RF-01-12`). A senha antiga
    deixa de valer porque o hash é substituído — não há segundo caminho
    de acesso com a senha provisória (`RN-01-18`)."""
    credencial = (
        sessao_bd.query(Credencial)
        .filter_by(
            persona_id=contexto.persona_id,
            tipo=TipoDeCredencial.usuario_e_senha,
            ativa=True,
        )
        .first()
    )
    if credencial is None:
        raise NaoEncontrado(mensagem="Esta persona não tem credencial de usuário e senha.")

    credencial.segredo = calcular_hash(entrada.senha_nova, configuracao)
    credencial.troca_pendente = False
    sessao_bd.commit()


class DisponibilidadeDeNickSaida(BaseModel):
    disponivel: bool
    sugestoes: list[str]


@roteador.get(
    "/nicks/disponibilidade",
    dependencies=[Depends(exigir_freio_por_origem("consulta_por_nick"))],
)
def conferir_disponibilidade_de_nick_rota(
    nick: str,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> DisponibilidadeDeNickSaida:
    """Pública, sem credencial de persona — serve o pré-cadastro e a tela do
    adulto autenticado com a mesma resposta, porque o alcance é o mesmo:
    só nicks de adulto (`RF-14-13`, `RN-01-22`, `RN-14-23`). Entra no freio
    por origem já vigente para consulta de nick, sem superfície nova
    (`RF-01-65`)."""
    disponivel = conferir_disponibilidade_de_nick(sessao_bd, nick)
    sugestoes = [] if disponivel else sugerir_variacoes_de_nick(sessao_bd, nick)
    return DisponibilidadeDeNickSaida(disponivel=disponivel, sugestoes=sugestoes)


class DefinirNickEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nick: str = Field(min_length=1)


class MinhaIdentidadeSaida(BaseModel):
    nick: str


@roteador.put("/eu/apoiador/identidade")
def definir_identidade_do_apoiador(
    entrada: DefinirNickEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MinhaIdentidadeSaida:
    """Define ou troca o próprio nick do Apoiador em sessão; outro papel
    recebe 403 (`RF-14-12`, `RN-14-10`, `RN-01-30`, PRD-01 §9)."""
    if contexto.papel != Papel.apoiador:
        raise PermissaoNegada(mensagem="Só o Apoiador define o próprio nick por aqui.")

    persona = sessao_bd.get(Persona, contexto.persona_id)
    definir_ou_trocar_nick(sessao_bd, persona, entrada.nick)
    sessao_bd.commit()
    return MinhaIdentidadeSaida(nick=entrada.nick)


@roteador.put("/eu/mestre/identidade")
def definir_identidade_do_mestre(
    entrada: DefinirNickEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MinhaIdentidadeSaida:
    """Rota simétrica à do Apoiador, para o Mestre definir ou trocar o
    próprio nick no primeiro acesso; outro papel recebe 403 (`RF-14-12`,
    `RN-14-10`, `RN-01-30`, PRD-01 §9, design — Decisions)."""
    if contexto.papel != Papel.mestre:
        raise PermissaoNegada(mensagem="Só o Mestre define o próprio nick por aqui.")

    persona = sessao_bd.get(Persona, contexto.persona_id)
    definir_ou_trocar_nick(sessao_bd, persona, entrada.nick)
    sessao_bd.commit()
    return MinhaIdentidadeSaida(nick=entrada.nick)
