import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..poderes.modelo import NaturezaDoPoder, Poder
from .modelo import (
    Atividade,
    FormatoDeAtividade,
    Missao,
    ModalidadeDeAtividade,
    SituacaoDaTrilha,
    Trilha,
)


def conferir_posse_da_trilha(trilha: Trilha, persona: Persona) -> None:
    """Aceita o Mestre autor e o Admin; recusa qualquer outro Mestre com
    403, ainda que o papel dele permita escrever trilhas em geral
    (`RF-01-16`, PRD-01 §4, design — decisões). Aplicada depois da matriz —
    a rota que a matriz protege é do PRD-09.
    """
    if persona.papel == Papel.admin:
        return
    if trilha.autor_id != persona.id:
        raise PermissaoNegada(mensagem="Só o Mestre autor escreve na própria trilha.")


def criar_trilha(
    sessao: Session,
    *,
    autor: Persona,
    nome: str,
    objetivo: str,
    area_do_conhecimento: str,
    poder_id: uuid.UUID | None,
) -> Trilha:
    """Exige poder do catálogo, de natureza de Guerreiro(a) (`RF-01-20`,
    `RN-01-43`). Nasce sempre em rascunho — a publicação é do PRD-09.
    """
    if poder_id is None:
        raise ErroDeValidacao(mensagem="Trilha exige um poder do catálogo.", campo="poder_id")

    poder = sessao.get(Poder, poder_id)
    if poder is None:
        raise ErroDeValidacao(mensagem="Poder não encontrado no catálogo.", campo="poder_id")
    if poder.natureza != NaturezaDoPoder.de_guerreiro:
        raise ErroDeValidacao(
            mensagem="Trilha só se vincula a poder de Guerreiro(a); o Poder Sustentador "
            "é derivado do aporte.",
            campo="poder_id",
        )

    trilha = Trilha(
        nome=nome,
        objetivo=objetivo,
        area_do_conhecimento=area_do_conhecimento,
        poder_id=poder_id,
        situacao=SituacaoDaTrilha.rascunho,
        autor_id=autor.id,
        papel_do_autor=autor.papel.value,
    )
    sessao.add(trilha)
    sessao.flush()
    return trilha


def consultar_trilhas(sessao: Session, *, persona: Persona | None = None) -> list[Trilha]:
    """Bem comum da plataforma: sem parâmetro nem filtro de comunidade
    (`RN-01-42`). O rascunho só aparece ao Mestre autor e ao Admin
    (`RF-01-20`, `RF-09-04`); a listagem pública desta fatia é só esta
    função — a rota de consulta é do PRD-09/PRD-03.
    """
    consulta = sessao.query(Trilha)
    if persona is not None and persona.papel == Papel.admin:
        return consulta.all()
    if persona is not None:
        return consulta.filter(
            or_(Trilha.situacao == SituacaoDaTrilha.publicada, Trilha.autor_id == persona.id)
        ).all()
    return consulta.filter(Trilha.situacao == SituacaoDaTrilha.publicada).all()


def criar_missao(
    sessao: Session,
    *,
    operador: Persona,
    trilha: Trilha | None,
    posicao: int,
    nivel_de_dificuldade: int,
    obrigatoria: bool | None,
    e_sondagem: bool = False,
) -> Missao:
    """A dificuldade é só o que o Mestre autor declara — nunca deriva da
    idade do Guerreiro(a) (documento 99 §6 invariante 2). A sondagem
    exige a primeira posição e admite no máximo uma por trilha
    (documento 99 §6 invariante 5); a trilha em rascunho pode não ter
    sondagem ainda — a trava de publicação é `RF-09-82`.
    """
    if trilha is None:
        raise ErroDeValidacao(mensagem="Missão exige uma trilha.", campo="trilha_id")
    conferir_posse_da_trilha(trilha, operador)
    if obrigatoria is None:
        raise ErroDeValidacao(
            mensagem="Missão exige a declaração de obrigatória ou opcional.",
            campo="obrigatoria",
        )

    if e_sondagem:
        if posicao != 1:
            raise ErroDeValidacao(
                mensagem="A missão de sondagem ocupa a primeira posição da trilha.",
                campo="e_sondagem",
            )
        ja_tem_sondagem = (
            sessao.query(Missao).filter_by(trilha_id=trilha.id, e_sondagem=True).first()
        )
        if ja_tem_sondagem is not None:
            raise ErroDeValidacao(
                mensagem="Esta trilha já tem uma missão de sondagem.", campo="e_sondagem"
            )

    missao = Missao(
        trilha_id=trilha.id,
        posicao=posicao,
        nivel_de_dificuldade=nivel_de_dificuldade,
        obrigatoria=obrigatoria,
        e_sondagem=e_sondagem,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(missao)
    sessao.flush()
    return missao


def _normalizar_natureza(natureza: str) -> str:
    """Reduz variação de digitação na lista aberta (design — riscos); o
    catálogo sugerido de `RF-09-85` reduz mais quando o PRD-09 chegar."""
    return natureza.strip().lower()


def criar_atividade(
    sessao: Session,
    *,
    operador: Persona,
    missao: Missao | None,
    modalidade: str | None,
    formato: str | None,
    natureza: str | None,
    producao_esperada: str | None,
) -> Atividade:
    """Sempre pertence a uma missão, com a escrita restrita ao Mestre autor
    da trilha e a Admin, pela mesma conferência de posse da trilha
    (`RF-01-20`, `RF-01-16`). Os três eixos combinam livremente; a natureza
    é lista aberta e a produção declarada é sempre exigida
    (documento 99 §6 invariante 19).
    """
    if missao is None:
        raise ErroDeValidacao(mensagem="Atividade exige uma missão.", campo="missao_id")

    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    if not modalidade:
        raise ErroDeValidacao(mensagem="Atividade exige modalidade.", campo="modalidade")
    try:
        modalidade_valida = ModalidadeDeAtividade(modalidade)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Modalidade fora dos valores previstos.", campo="modalidade"
        ) from exc

    if not formato:
        raise ErroDeValidacao(mensagem="Atividade exige formato.", campo="formato")
    try:
        formato_valido = FormatoDeAtividade(formato)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Formato fora dos valores previstos.", campo="formato"
        ) from exc

    if not natureza or not natureza.strip():
        raise ErroDeValidacao(mensagem="Atividade exige natureza.", campo="natureza")

    if not producao_esperada or not producao_esperada.strip():
        raise ErroDeValidacao(
            mensagem="Atividade exige a declaração do que o Guerreiro(a) produz.",
            campo="producao_esperada",
        )

    atividade = Atividade(
        missao_id=missao.id,
        modalidade=modalidade_valida,
        formato=formato_valido,
        natureza=_normalizar_natureza(natureza),
        producao_esperada=producao_esperada,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(atividade)
    sessao.flush()
    return atividade
