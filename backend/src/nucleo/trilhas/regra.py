import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..coletas.modelo import DesafioDeColeta
from ..culminancias.modelo import Culminancia
from ..erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..poderes.modelo import NaturezaDoPoder, Poder
from ..tempo import agora
from .modelo import (
    Atividade,
    EtapaDoCiclo,
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


def conferir_autoria_estrita_da_trilha(trilha: Trilha, persona: Persona) -> None:
    """Só o Mestre autor — nem outro Mestre nem Admin publicam a trilha ou
    declaram a culminância dela; a publicação não passa por aprovação, e o
    Admin não edita a trilha de um Mestre (`RF-09-05`, `RF-09-29`, design —
    decisões 1).
    """
    if trilha.autor_id != persona.id:
        raise PermissaoNegada(mensagem="Só o Mestre autor executa esta operação na própria trilha.")


def _unir_em_portugues(itens: list[str]) -> str:
    if len(itens) == 1:
        return itens[0]
    return ", ".join(itens[:-1]) + " e " + itens[-1]


def _travas_de_publicacao_pendentes(sessao: Session, trilha: Trilha) -> list[str]:
    """As três travas do `RF-09-06`, `RF-09-07` e `RN-09-29` — sondagem
    declarada, ao menos um desafio de coleta em alguma missão da trilha
    (existência, não contagem — design — decisões 6) e culminância
    declarada. O lastro de recompensa de marco nunca entra aqui: é
    conferido na entrega, por `RN-09-27`.
    """
    pendentes = []

    tem_sondagem = (
        sessao.query(Missao).filter_by(trilha_id=trilha.id, e_sondagem=True).first() is not None
    )
    if not tem_sondagem:
        pendentes.append("a missão de sondagem")

    tem_desafio_de_coleta = (
        sessao.query(DesafioDeColeta)
        .join(Missao, DesafioDeColeta.missao_id == Missao.id)
        .filter(Missao.trilha_id == trilha.id)
        .first()
        is not None
    )
    if not tem_desafio_de_coleta:
        pendentes.append("o desafio de coleta de dados reais")

    tem_culminancia = sessao.query(Culminancia).filter_by(trilha_id=trilha.id).first() is not None
    if not tem_culminancia:
        pendentes.append("a culminância")

    return pendentes


def publicar_trilha(sessao: Session, trilha: Trilha | None, *, operador: Persona) -> Trilha:
    """Publica ou republica a pedido do Mestre autor, sem aprovação de
    Admin, a partir de `rascunho` ou `despublicada` — uma só rota para as
    duas origens (design — decisões 4). Confere as três travas juntas e
    nomeia **todas** as pendentes na recusa (`RF-09-05` a `RF-09-08`,
    `RF-09-82`, `RN-09-01`, design — decisões 5). A republicação limpa o
    motivo da despublicação (design — decisões 7).
    """
    if trilha is None:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")
    conferir_autoria_estrita_da_trilha(trilha, operador)
    if trilha.situacao == SituacaoDaTrilha.publicada:
        raise ErroDeValidacao(mensagem="Esta trilha já está publicada.", campo="situacao")

    pendentes = _travas_de_publicacao_pendentes(sessao, trilha)
    if pendentes:
        raise ErroDeValidacao(
            mensagem=f"Para publicar, ainda falta declarar: {_unir_em_portugues(pendentes)}."
        )

    trilha.situacao = SituacaoDaTrilha.publicada
    trilha.motivo_da_situacao = None
    trilha.autor_da_situacao_id = operador.id
    trilha.papel_do_autor_da_situacao = operador.papel.value
    trilha.situacao_alterada_em = agora()
    sessao.flush()
    return trilha


def despublicar_trilha(
    sessao: Session, trilha: Trilha | None, *, operador: Persona, motivo: str | None
) -> Trilha:
    """Só Admin despublica, sempre com motivo, e só trilha publicada
    (`RF-09-10`, `RF-09-11`). Não toca missão, atividade, resultado,
    presença nem pontuação: o percurso já realizado permanece íntegro.
    """
    if trilha is None:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin despublica trilha.")
    if not motivo or not motivo.strip():
        raise ErroDeValidacao(mensagem="Despublicação exige motivo.", campo="motivo")
    if trilha.situacao != SituacaoDaTrilha.publicada:
        raise ErroDeValidacao(
            mensagem="Só uma trilha publicada pode ser despublicada.", campo="situacao"
        )

    trilha.situacao = SituacaoDaTrilha.despublicada
    trilha.motivo_da_situacao = motivo
    trilha.autor_da_situacao_id = operador.id
    trilha.papel_do_autor_da_situacao = operador.papel.value
    trilha.situacao_alterada_em = agora()
    sessao.flush()
    return trilha


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
    titulo: str | None,
    posicao: int,
    nivel_de_dificuldade: int,
    obrigatoria: bool | None,
    etapa_do_ciclo: str | None,
    e_sondagem: bool = False,
    cadencia_de_retomada: list[int] | None = None,
) -> Missao:
    """A dificuldade é só o que o Mestre autor declara — nunca deriva da
    idade do Guerreiro(a) (documento 99 §6 invariante 2). A sondagem
    exige a primeira posição e admite no máximo uma por trilha
    (documento 99 §6 invariante 5); a trilha em rascunho pode não ter
    sondagem ainda — a trava de publicação é `RF-09-82`. A retomada é
    opcional na criação (`RF-09-83`); quem a declara depois é
    `declarar_cadencia_de_retomada`.
    """
    if trilha is None:
        raise ErroDeValidacao(mensagem="Missão exige uma trilha.", campo="trilha_id")
    conferir_posse_da_trilha(trilha, operador)
    if not titulo or not titulo.strip():
        raise ErroDeValidacao(mensagem="Missão exige um título.", campo="titulo")
    if obrigatoria is None:
        raise ErroDeValidacao(
            mensagem="Missão exige a declaração de obrigatória ou opcional.",
            campo="obrigatoria",
        )
    try:
        etapa_valida = EtapaDoCiclo(etapa_do_ciclo)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Etapa do ciclo fora dos valores previstos.", campo="etapa_do_ciclo"
        ) from exc

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
        titulo=titulo,
        posicao=posicao,
        nivel_de_dificuldade=nivel_de_dificuldade,
        obrigatoria=obrigatoria,
        etapa_do_ciclo=etapa_valida,
        e_sondagem=e_sondagem,
        cadencia_de_retomada=cadencia_de_retomada,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(missao)
    sessao.flush()
    return missao


def declarar_cadencia_de_retomada(
    sessao: Session, *, operador: Persona, missao: Missao, cadencia_de_retomada: list[int] | None
) -> Missao:
    """A cadência declarada é sempre a do Mestre autor — o núcleo nunca a
    impõe (`RF-09-83`, `RF-09-101`). Declarar de novo substitui a anterior;
    `None` deixa a missão sem retomada.
    """
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    missao.cadencia_de_retomada = cadencia_de_retomada
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
    titulo: str | None,
    descricao: str | None = None,
    modalidade: str | None,
    formato: str | None,
    natureza: str | None,
    producao_esperada: str | None,
    aula_id: uuid.UUID | None = None,
) -> Atividade:
    """Sempre pertence a uma missão, com a escrita restrita ao Mestre autor
    da trilha e a Admin, pela mesma conferência de posse da trilha
    (`RF-01-20`, `RF-01-16`). Os três eixos combinam livremente; a natureza
    é lista aberta e a produção declarada é sempre exigida
    (documento 99 §6 invariante 19). O título é exigido — sem ele nenhuma
    tela lista a atividade; a descrição é opcional (`RF-09-69`, design —
    decisões 5).

    `aula_id` é o vínculo opcional com o encontro (documento 05 §4): só
    atividade de formato presencial o declara, e a aula precisa existir —
    as duas recusas respondem 422 (`RF-09-69`, `RF-09-73`).
    """
    if missao is None:
        raise ErroDeValidacao(mensagem="Atividade exige uma missão.", campo="missao_id")

    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    if not titulo or not titulo.strip():
        raise ErroDeValidacao(mensagem="Atividade exige um título.", campo="titulo")

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

    if aula_id is not None:
        if formato_valido != FormatoDeAtividade.presencial:
            raise ErroDeValidacao(
                mensagem="Só atividade de formato presencial declara a aula do encontro.",
                campo="aula_id",
            )
        if sessao.get(Aula, aula_id) is None:
            raise ErroDeValidacao(mensagem="Aula não encontrada.", campo="aula_id")

    atividade = Atividade(
        missao_id=missao.id,
        titulo=titulo,
        descricao=descricao,
        modalidade=modalidade_valida,
        formato=formato_valido,
        natureza=_normalizar_natureza(natureza),
        producao_esperada=producao_esperada,
        aula_id=aula_id,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(atividade)
    sessao.flush()
    return atividade
