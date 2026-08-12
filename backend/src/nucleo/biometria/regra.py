import uuid
from datetime import UTC, datetime
from functools import lru_cache
from math import sqrt
from random import Random

from sqlalchemy.orm import Session

from ..configuracao import Configuracao
from ..consentimentos.modelo import DecisaoDeConsentimento
from ..consentimentos.regra import consultar_consentimento_vigente_em
from ..erros import ErroDeValidacao
from ..personas.modelo import Credencial, Nick, Papel, Persona, TipoDeCredencial
from .cifra import cifrar_descritor, decifrar_descritor
from .modelo import AcessoAoTemplate, DesfechoDoAcesso, NaturezaDoAcesso

# `Consentimento.tipo` é campo aberto (design da fatia anterior — decisões);
# esta é a string que a captura biométrica usa (`RN-01-17`, documento 03 §3.3).
TIPO_DE_CONSENTIMENTO_BIOMETRIA = "captura_biometrica"


@lru_cache(maxsize=1)
def _template_de_descarte(dimensao: int) -> list[float]:
    """Gerado uma vez, na subida do processo — nunca confere com um
    descritor real, e serve só para igualar o tempo de resposta quando o
    nick não existe (`RN-01-22`, design — decisões)."""
    gerador = Random()
    return [gerador.uniform(-1.0, 1.0) for _ in range(dimensao)]


def _distancia_euclidiana(a: list[float], b: list[float]) -> float | None:
    if len(a) != len(b):
        return None
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b, strict=True)))


def _credencial_biometrica_ativa(sessao: Session, persona_id: uuid.UUID) -> Credencial | None:
    return (
        sessao.query(Credencial)
        .filter_by(persona_id=persona_id, tipo=TipoDeCredencial.biometria, ativa=True)
        .first()
    )


def _registrar_acesso(
    sessao: Session,
    *,
    guerreiro_id: uuid.UUID,
    acessado_por: uuid.UUID | None,
    natureza: NaturezaDoAcesso,
    desfecho: DesfechoDoAcesso,
) -> None:
    sessao.add(
        AcessoAoTemplate(
            guerreiro_id=guerreiro_id,
            acessado_por=acessado_por,
            natureza=natureza,
            desfecho=desfecho,
        )
    )
    sessao.flush()


def gravar_ou_recadastrar_template(
    sessao: Session,
    configuracao: Configuracao,
    *,
    guerreiro: Persona,
    descritor: list[float],
    operado_por: Persona,
) -> Credencial:
    """Grava o primeiro _template_ ou recadastra o existente (`RF-01-05`,
    `RF-01-07`, `RF-01-08`). A permissão de quem opera é conferida na rota,
    pela matriz (`RF-01-16`) — aqui só as invariantes do próprio _template_.
    """
    if guerreiro.papel != Papel.guerreiro:
        raise ErroDeValidacao(mensagem="Só Guerreiro(a) tem template biométrico.", campo="id")

    if len(descritor) != configuracao.biometria_dimensao_do_descritor:
        raise ErroDeValidacao(mensagem="Descritor fora da dimensão esperada.", campo="descritor")

    vigente = consultar_consentimento_vigente_em(
        sessao,
        guerreiro_id=guerreiro.id,
        tipo=TIPO_DE_CONSENTIMENTO_BIOMETRIA,
        em=datetime.now(UTC),
    )
    if vigente is None or vigente.decisao != DecisaoDeConsentimento.concede:
        raise ErroDeValidacao(
            mensagem="Cadastro biométrico exige consentimento vigente do responsável "
            "para a captura."
        )

    segredo_cifrado = cifrar_descritor(descritor, configuracao)

    credencial_anterior = _credencial_biometrica_ativa(sessao, guerreiro.id)
    natureza = NaturezaDoAcesso.gravacao
    if credencial_anterior is not None:
        credencial_anterior.ativa = False
        sessao.flush()
        natureza = NaturezaDoAcesso.recadastro

    credencial = Credencial(
        persona_id=guerreiro.id,
        tipo=TipoDeCredencial.biometria,
        identificador=str(guerreiro.id),
        segredo=segredo_cifrado,
        criada_por=operado_por.id,
        ativa=True,
    )
    sessao.add(credencial)
    sessao.flush()

    _registrar_acesso(
        sessao,
        guerreiro_id=guerreiro.id,
        acessado_por=operado_por.id,
        natureza=natureza,
        desfecho=DesfechoDoAcesso.sucesso,
    )
    return credencial


def autenticar_por_nick_e_descritor(
    sessao: Session, configuracao: Configuracao, *, nick: str, descritor: list[float]
) -> Persona | None:
    """Confere o descritor contra o _template_ de um único Guerreiro(a),
    restrito pelo nick (`RF-01-04`, design — decisões). Devolve `None` para
    nick inexistente, Guerreiro(a) sem _template_ e descritor que não
    confere — os três casos que a rota funde numa recusa indistinguível
    (`RN-01-22`).
    """
    registro_de_nick = sessao.query(Nick).filter_by(valor=nick).first()
    guerreiro_id = registro_de_nick.persona_id if registro_de_nick is not None else None
    guerreiro = sessao.get(Persona, guerreiro_id) if guerreiro_id is not None else None

    credencial = _credencial_biometrica_ativa(sessao, guerreiro_id) if guerreiro_id else None

    dimensao = configuracao.biometria_dimensao_do_descritor
    template_para_comparar = (
        decifrar_descritor(credencial.segredo, configuracao)
        if credencial is not None
        else _template_de_descarte(dimensao)
    )

    distancia = _distancia_euclidiana(descritor, template_para_comparar)
    confere = (
        credencial is not None
        and distancia is not None
        and distancia <= configuracao.biometria_limiar_de_comparacao
    )

    if guerreiro_id is not None:
        _registrar_acesso(
            sessao,
            guerreiro_id=guerreiro_id,
            acessado_por=None,
            natureza=NaturezaDoAcesso.comparacao_de_login,
            desfecho=DesfechoDoAcesso.sucesso if confere else DesfechoDoAcesso.recusa,
        )

    return guerreiro if confere else None
