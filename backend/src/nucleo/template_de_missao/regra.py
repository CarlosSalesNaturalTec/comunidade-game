from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, NaoEncontrado
from ..personas.modelo import Persona
from ..poderes.modelo import Poder
from ..trilhas.modelo import Atividade, Missao, Trilha
from ..trilhas.regra import conferir_posse_da_trilha
from .modelo import SituacaoDaSugestaoDeEstrutura, SugestaoDeEstrutura
from .porta import AtividadeSugerida, PortaDoTemplateDeMissao

# O convite aceito da atividade desplugada sugerida grava a `natureza` com
# este valor (`local.TemplateDeMissaoLocal`, `nuvem._validar_estrutura`) —
# `Atividade` não ganha coluna nova para isso: a natureza já é lista aberta
# (`RF-09-88`, `RN-09-34`, design — decisão 5).
NATUREZA_DE_ATIVIDADE_DESPLUGADA = "desplugada"

# Sempre proposta pelo núcleo, nunca pelo modelo — a mesma cadência para
# toda missão, contada do desbloqueio (`RF-09-116`, design — decisão 1).
CADENCIA_DE_RETOMADA_SUGERIDA = [2, 7, 21]

_SITUACOES_DE_DESFECHO = (
    SituacaoDaSugestaoDeEstrutura.aceita,
    SituacaoDaSugestaoDeEstrutura.recusada,
    SituacaoDaSugestaoDeEstrutura.alterada,
)


def calcular_lacunas(sessao: Session, *, missao: Missao, trilha: Trilha) -> list[str]:
    """Lacunas apuradas só pelo que está gravado, nunca pelo que o modelo
    respondeu (`RF-09-86`, `RN-09-31`, `RN-09-34`, design — decisão 1)."""
    lacunas: list[str] = []
    atividades = sessao.query(Atividade).filter_by(missao_id=missao.id).all()

    if not atividades:
        lacunas.append("Esta missão ainda não tem nenhuma atividade.")
    else:
        for atividade in atividades:
            if not atividade.producao_esperada or not atividade.producao_esperada.strip():
                lacunas.append(
                    f'A atividade "{atividade.titulo}" está sem a produção que o '
                    "Guerreiro(a) precisa entregar."
                )

    if not missao.cadencia_de_retomada:
        lacunas.append("Esta missão ainda não tem cadência de retomada declarada.")

    poder = sessao.get(Poder, trilha.poder_id)
    if poder is not None and poder.tecnico:
        tem_desplugada = any(
            atividade.natureza == NATUREZA_DE_ATIVIDADE_DESPLUGADA for atividade in atividades
        )
        if not tem_desplugada:
            lacunas.append(
                "Esta trilha é de poder técnico e ainda não tem nenhuma atividade desplugada."
            )

    return lacunas


@dataclass
class EstruturaEProposta:
    """O que a rota devolve ao Mestre: a sugestão registrada, se a estrutura
    veio do modelo, e o que o núcleo apurou sozinho — lacunas e cadência
    (`RF-09-85`, `RF-09-86`, `RF-09-116`, design — decisões 1, 3)."""

    sugestao: SugestaoDeEstrutura
    disponivel: bool
    atividades: list[AtividadeSugerida] = field(default_factory=list)
    objetivo_ods: int | None = None
    meta_ods: str | None = None
    cadencia_de_retomada: list[int] = field(
        default_factory=lambda: list(CADENCIA_DE_RETOMADA_SUGERIDA)
    )
    lacunas: list[str] = field(default_factory=list)


def pedir_estrutura_da_missao(
    sessao: Session,
    *,
    operador: Persona,
    missao: Missao | None,
    topico: str | None,
    porta: PortaDoTemplateDeMissao,
) -> EstruturaEProposta:
    """Só o Mestre autor pede (403, pela mesma posse do restante da autoria
    da trilha); tópico vazio é 422 (`RF-09-85`, `RF-09-91`). A
    indisponibilidade do modelo nunca vira erro: as lacunas e a cadência
    seguem sendo devolvidas, calculadas pelo núcleo (`RF-09-91`, `RN-09-16`,
    design — decisão 3)."""
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    if not topico or not topico.strip():
        raise ErroDeValidacao(mensagem="Pedido de estrutura exige um tópico.", campo="topico")

    lacunas = calcular_lacunas(sessao, missao=missao, trilha=trilha)

    poder = sessao.get(Poder, trilha.poder_id)
    exigir_atividade_desplugada = poder is not None and poder.tecnico

    estrutura = porta.sugerir_estrutura(
        topico=topico, exigir_atividade_desplugada=exigir_atividade_desplugada
    )

    estrutura_proposta_json = {
        "atividades": [
            {
                "titulo": atividade.titulo,
                "modalidade": atividade.modalidade,
                "formato": atividade.formato,
                "natureza": atividade.natureza,
                "producao_esperada": atividade.producao_esperada,
                "desplugada": atividade.desplugada,
                "descricao": atividade.descricao,
            }
            for atividade in (estrutura.atividades if estrutura is not None else [])
        ],
        "objetivo_ods": estrutura.objetivo_ods if estrutura is not None else None,
        "meta_ods": estrutura.meta_ods if estrutura is not None else None,
        "cadencia_de_retomada": CADENCIA_DE_RETOMADA_SUGERIDA,
    }

    sugestao = SugestaoDeEstrutura(
        missao_id=missao.id,
        topico=topico,
        estrutura_proposta=estrutura_proposta_json,
        lacunas=lacunas,
        situacao=SituacaoDaSugestaoDeEstrutura.proposta,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(sugestao)
    sessao.flush()

    return EstruturaEProposta(
        sugestao=sugestao,
        disponivel=estrutura is not None,
        atividades=list(estrutura.atividades) if estrutura is not None else [],
        objetivo_ods=estrutura.objetivo_ods if estrutura is not None else None,
        meta_ods=estrutura.meta_ods if estrutura is not None else None,
        cadencia_de_retomada=list(CADENCIA_DE_RETOMADA_SUGERIDA),
        lacunas=lacunas,
    )


def registrar_desfecho_da_sugestao(
    sessao: Session,
    *,
    operador: Persona,
    sugestao: SugestaoDeEstrutura | None,
    situacao: SituacaoDaSugestaoDeEstrutura | None,
) -> SugestaoDeEstrutura:
    """O desfecho que o Mestre autor deu à sugestão — aceita, recusada ou
    alterada —, sem que o registro em si altere a missão: quem grava o que
    foi aceito ou alterado são as rotas de autoria que já existem
    (`RF-09-89`, `RN-09-33`)."""
    if sugestao is None:
        raise NaoEncontrado(mensagem="Sugestão de estrutura não encontrada.")
    missao = sessao.get(Missao, sugestao.missao_id)
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    if situacao not in _SITUACOES_DE_DESFECHO:
        raise ErroDeValidacao(
            mensagem="Desfecho deve ser aceita, recusada ou alterada.", campo="situacao"
        )

    sugestao.situacao = situacao
    sessao.flush()
    return sugestao
