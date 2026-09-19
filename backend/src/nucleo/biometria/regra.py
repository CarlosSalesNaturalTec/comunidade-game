import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from functools import lru_cache
from math import sqrt
from random import Random

from sqlalchemy.orm import Session

from ..aulas.modelo import Aula, SituacaoDaAula
from ..configuracao import Configuracao
from ..consentimentos.modelo import DecisaoDeConsentimento, TipoDeConsentimento
from ..consentimentos.regra import consultar_consentimento_vigente_em
from ..erros import ErroDeValidacao
from ..personas.modelo import Credencial, Nick, Papel, Persona, TipoDeCredencial
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..tempo import agora
from .cifra import cifrar_descritor, decifrar_descritor
from .modelo import (
    AcessoAoTemplate,
    ApagamentoDeTemplate,
    DesfechoDoAcesso,
    GatilhoDeApagamento,
    MedicaoDoLimiar,
    NaturezaDoAcesso,
)

# O tipo do consentimento que a captura biométrica exige (`RN-01-17`,
# documento 03 §3.3), do conjunto fechado que `consentimentos.modelo` define
# (`RN-13-06`).
TIPO_DE_CONSENTIMENTO_BIOMETRIA = TipoDeConsentimento.biometria

# Quantas posições tem o descritor que o aparelho gera. NÃO é parâmetro de
# implantação: é fato da biblioteca decidida no documento 03 §3.3 — o modelo
# `faceres` da Human, cuja saída `global_pooling/Mean` tem shape `[1, 1024]`.
# A biblioteca procura exatamente esse tensor (`src/face/faceres.ts`); o 128
# que ela traz comentado é redução abandonada, da era do `face-api.js`.
#
# Ficou como variável de ambiente da implantação de 2026-08-12 até
# 2026-09-17, declarada 17 dias antes de a Human entrar no projeto e com o
# valor daquela outra convenção: toda captura respondia 422 e nenhum
# _template_ chegou a ser gravado. Trocar de biblioteca é trocar este número
# aqui, junto com a decisão que o produziu (decisão do fundador, 2026-09-17).
DIMENSAO_DO_DESCRITOR = 1024


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

    if len(descritor) != DIMENSAO_DO_DESCRITOR:
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


# Os mínimos por série e o piso de pessoas no teto do `RN-04-35`, conferidos
# **também aqui**: o cálculo do aparelho não é autoridade sobre o que o núcleo
# grava (design — decisão 2, decisão do fundador, 2026-09-18).
MINIMO_DE_MEDICOES_POR_SERIE = 8
MINIMO_DE_PESSOAS_NO_TETO = 2


def limiar_proposto(distancias_do_piso: list[float], distancias_do_teto: list[float]) -> float:
    """O ponto médio entre o maior piso e o menor teto — a escolha equidistante
    das duas formas de errar: recusar quem é e aceitar quem não é (`RN-04-35`,
    decisão do fundador, 2026-09-18).

    O **núcleo** é quem calcula. O aparelho mostra o mesmo número para quem
    opera confirmar, mas não o envia: número enviado é número em que se
    precisaria confiar, e a fórmula é curta demais para valer essa confiança.
    """
    return (max(distancias_do_piso) + min(distancias_do_teto)) / 2


def consultar_limiar_vigente(sessao: Session, *, ponto_de_apoio_id: uuid.UUID) -> float | None:
    """O limiar vigente de um ponto de apoio é o da **medição mais recente**
    dele; `None` quando nunca se mediu ali (`RF-01-73`, design — decisão 4)."""
    medicao = (
        sessao.query(MedicaoDoLimiar)
        .filter_by(ponto_de_apoio_id=ponto_de_apoio_id)
        .order_by(MedicaoDoLimiar.registrado_em.desc())
        .first()
    )
    return medicao.limiar if medicao is not None else None


def consultar_limiares_por_ponto_de_apoio(
    sessao: Session,
) -> list[tuple[PontoDeApoio, MedicaoDoLimiar | None]]:
    """Cada ponto de apoio com a sua medição vigente, ou `None` quando nunca
    se mediu ali — é esse `None` que a App 03 destaca, porque ali o
    reconhecimento não confere ninguém (`RF-02-109`, `RN-01-56`)."""
    pontos = sessao.query(PontoDeApoio).order_by(PontoDeApoio.nome).all()
    return [
        (
            ponto,
            sessao.query(MedicaoDoLimiar)
            .filter_by(ponto_de_apoio_id=ponto.id)
            .order_by(MedicaoDoLimiar.registrado_em.desc())
            .first(),
        )
        for ponto in pontos
    ]


def gravar_medicao_do_limiar(
    sessao: Session,
    *,
    ponto_de_apoio_id: uuid.UUID,
    distancias_do_piso: list[float],
    distancias_do_teto: list[float],
    pessoas_no_teto: int,
    operado_por: Persona,
) -> MedicaoDoLimiar:
    """Grava a medição que passa a valer para o ponto de apoio (`RF-01-73`,
    `RF-04-66`, `RN-04-35`). A permissão de quem opera é conferida na rota,
    pela matriz (`RF-01-16`) — aqui, o critério de conclusão.

    Séries que se **sobrepõem** não geram limiar: não existe número que acerte
    os dois lados, e gravar um ali seria gravar um erro (`RN-04-35`).
    """
    if (
        len(distancias_do_piso) < MINIMO_DE_MEDICOES_POR_SERIE
        or len(distancias_do_teto) < MINIMO_DE_MEDICOES_POR_SERIE
    ):
        raise ErroDeValidacao(
            mensagem=(f"Cada série precisa de ao menos {MINIMO_DE_MEDICOES_POR_SERIE} medições."),
            campo="distancias_do_piso",
        )
    if pessoas_no_teto < MINIMO_DE_PESSOAS_NO_TETO:
        raise ErroDeValidacao(
            mensagem=(
                f"O teto precisa de ao menos {MINIMO_DE_PESSOAS_NO_TETO} pessoas diferentes "
                "da referência."
            ),
            campo="pessoas_no_teto",
        )
    if max(distancias_do_piso) >= min(distancias_do_teto):
        raise ErroDeValidacao(
            mensagem=(
                "As séries se sobrepõem: não existe limiar viável com essas capturas. Meça de novo."
            ),
            campo="distancias_do_teto",
        )

    medicao = MedicaoDoLimiar(
        ponto_de_apoio_id=ponto_de_apoio_id,
        limiar=limiar_proposto(distancias_do_piso, distancias_do_teto),
        distancias_do_piso=distancias_do_piso,
        distancias_do_teto=distancias_do_teto,
        pessoas_no_teto=pessoas_no_teto,
        autor_id=operado_por.id,
        papel_do_autor=operado_por.papel.value,
    )
    sessao.add(medicao)
    sessao.flush()
    return medicao


def _aula_vale_para(guerreiro: Persona | None, aula: Aula | None) -> bool:
    """A aula informada determina o ponto de apoio, e com ele o limiar. Vale
    apenas a aula **vigente** da **comunidade do próprio Guerreiro(a)** — o
    mesmo laço que `registrar_presenca` já aplica —, para que escolher a aula
    NUNCA alcance o limiar de outra comunidade (`RF-01-73`, design —
    decisão 3)."""
    if aula is None or guerreiro is None:
        return False
    if aula.situacao == SituacaoDaAula.cancelada:
        return False
    momento = agora()
    if not (aula.inicio_em <= momento <= aula.fim_em):
        return False
    vinculo = guerreiro.vinculo_vigente
    return vinculo is not None and vinculo.comunidade_virtual_id == aula.comunidade_virtual_id


def autenticar_por_nick_e_descritor(
    sessao: Session,
    configuracao: Configuracao,
    *,
    nick: str,
    descritor: list[float],
    aula: Aula | None,
) -> Persona | None:
    """Confere o descritor contra o _template_ de um único Guerreiro(a),
    restrito pelo nick, com o **limiar do ponto de apoio da aula** em que a
    entrada acontece (`RF-01-04`, `RF-01-73`, design — decisões). Devolve
    `None` para nick inexistente, Guerreiro(a) sem _template_, descritor que
    não confere, **ponto de apoio sem limiar medido** e **aula que não vale
    para aquele Guerreiro(a)** — os cinco casos que a rota funde numa recusa
    indistinguível (`RN-01-22`, `RN-01-56`).

    O trabalho é o mesmo nos cinco, inclusive o cálculo da distância contra o
    _template_ de descarte: a indistinguibilidade do `RN-01-22` alcança o
    tempo, não só o corpo da resposta.
    """
    registro_de_nick = sessao.query(Nick).filter_by(valor=nick).first()
    guerreiro_id = registro_de_nick.persona_id if registro_de_nick is not None else None
    guerreiro = sessao.get(Persona, guerreiro_id) if guerreiro_id is not None else None

    credencial = _credencial_biometrica_ativa(sessao, guerreiro_id) if guerreiro_id else None

    template_para_comparar = (
        decifrar_descritor(credencial.segredo, configuracao)
        if credencial is not None
        else _template_de_descarte(DIMENSAO_DO_DESCRITOR)
    )

    limiar = (
        consultar_limiar_vigente(sessao, ponto_de_apoio_id=aula.ponto_de_apoio_id)
        if aula is not None and _aula_vale_para(guerreiro, aula)
        else None
    )

    distancia = _distancia_euclidiana(descritor, template_para_comparar)
    confere = (
        credencial is not None
        and limiar is not None
        and distancia is not None
        and distancia <= limiar
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


# Os prazos do documento 03 §12.2, por gatilho (`RF-13-43`, `RF-13-44`,
# `RN-13-22`, decisão do fundador, 2026-09-01).
PRAZO_DE_APAGAMENTO_POR_GATILHO: dict[GatilhoDeApagamento, timedelta] = {
    GatilhoDeApagamento.exclusao_deferida: timedelta(days=5),
    GatilhoDeApagamento.recusa_biometria: timedelta(days=5),
    GatilhoDeApagamento.fim_do_vinculo: timedelta(days=30),
}


def marcar_apagamento(
    sessao: Session, *, guerreiro_id: uuid.UUID, gatilho: GatilhoDeApagamento
) -> ApagamentoDeTemplate | None:
    """Marca a data do apagamento do _template_ nos três gatilhos do
    documento 03 §12.2. Sem _template_ gravado não marca e não falha: o ato
    que disparou o gatilho é gravado do mesmo jeito. Havendo marca, não
    substitui nem adia — o primeiro gatilho prevalece, e a marca nunca se
    cancela (`RF-13-43`, `RF-13-44`, `RN-13-22`, decisão do fundador,
    2026-09-01).
    """
    if _credencial_biometrica_ativa(sessao, guerreiro_id) is None:
        return None

    existente = sessao.query(ApagamentoDeTemplate).filter_by(guerreiro_id=guerreiro_id).first()
    if existente is not None:
        return existente

    apagamento = ApagamentoDeTemplate(
        guerreiro_id=guerreiro_id,
        gatilho=gatilho,
        apagar_em=datetime.now(UTC) + PRAZO_DE_APAGAMENTO_POR_GATILHO[gatilho],
    )
    sessao.add(apagamento)
    sessao.flush()
    return apagamento


def apagar_templates_vencidos(sessao: Session) -> int:
    """Remove a `Credencial` de tipo `biometria` cuja marca já venceu,
    destruindo o dado cifrado sem deixar rastro do descritor. Audita o
    apagamento como acesso de natureza `apagamento`, sem `acessado_por` —
    o comando não tem persona — e preserva a auditoria anterior, que é
    somente inserção. Repetível: quem já foi apagado não é contado de novo
    (`RF-13-43`, `RN-01-14`, documento 03 §3.3).
    """
    vencidos = (
        sessao.query(ApagamentoDeTemplate)
        .filter(ApagamentoDeTemplate.apagar_em <= datetime.now(UTC))
        .all()
    )

    apagados = 0
    for marca in vencidos:
        credencial = _credencial_biometrica_ativa(sessao, marca.guerreiro_id)
        if credencial is None:
            continue

        sessao.delete(credencial)
        sessao.flush()
        _registrar_acesso(
            sessao,
            guerreiro_id=marca.guerreiro_id,
            acessado_por=None,
            natureza=NaturezaDoAcesso.apagamento,
            desfecho=DesfechoDoAcesso.sucesso,
        )
        apagados += 1

    return apagados


@dataclass(frozen=True)
class EstadoDaBiometria:
    tem_template: bool
    decisao_do_termo: DecisaoDeConsentimento | None
    apagar_em: datetime | None
    gatilho_do_apagamento: GatilhoDeApagamento | None


def consultar_estado_da_biometria(sessao: Session, *, guerreiro_id: uuid.UUID) -> EstadoDaBiometria:
    """`RF-13-27`, `RF-13-44`, `RN-13-04`: o estado da captura, a decisão
    mais recente do termo próprio e, havendo marca, a data e o gatilho do
    apagamento — nunca o descritor nem o _template_.
    """
    tem_template = _credencial_biometrica_ativa(sessao, guerreiro_id) is not None
    vigente = consultar_consentimento_vigente_em(
        sessao,
        guerreiro_id=guerreiro_id,
        tipo=TIPO_DE_CONSENTIMENTO_BIOMETRIA,
        em=datetime.now(UTC),
    )
    apagamento = sessao.query(ApagamentoDeTemplate).filter_by(guerreiro_id=guerreiro_id).first()
    return EstadoDaBiometria(
        tem_template=tem_template,
        decisao_do_termo=vigente.decisao if vigente is not None else None,
        apagar_em=apagamento.apagar_em if apagamento is not None else None,
        gatilho_do_apagamento=apagamento.gatilho if apagamento is not None else None,
    )
