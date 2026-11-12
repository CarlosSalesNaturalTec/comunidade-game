import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..armazenamento.limites import (
    FORMATOS_ACEITOS_EM_TEXTO,
    FORMATOS_DE_ENVIO_ACEITOS,
    formatar_mb,
    teto_do_tipo_de_producao,
)
from ..armazenamento.porta import PortaDeArmazenamento
from ..aulas.modelo import Aula
from ..coletas.modelo import DesafioDeColeta
from ..criacoes_originais.modelo import TipoDeProducaoDaCriacaoOriginal
from ..culminancias.modelo import Culminancia
from ..erros import ArquivoAcimaDoTeto, ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..poderes.modelo import NaturezaDoPoder, Poder
from ..pontuacao.regra import (
    avaliar_niveis,
    creditar_pontuacao_do_desbloqueio_pratico,
    missoes_concluidas_pelo_guerreiro,
)
from ..recompensas_de_marco.modelo import RecompensaDeMarco
from ..recursos.modelo import TipoDeRecurso
from ..tempo import agora
from .modelo import (
    LIMITE_DA_RESPOSTA_FALADA,
    PRIMEIRA_ALTERNATIVA_DO_DESBLOQUEIO,
    TOTAL_DE_ALTERNATIVAS_DO_DESBLOQUEIO,
    Atividade,
    DesbloqueioDaMissao,
    EtapaDoCiclo,
    FormatoDeAtividade,
    InscricaoNaTrilha,
    Missao,
    ModalidadeDeAtividade,
    PerguntaDoDesbloqueio,
    RespostaDaSubmissao,
    SituacaoDaTrilha,
    SubmissaoDoDesbloqueio,
    TipoDeDesafioDeDesbloqueio,
    Trilha,
)

# Passa quem acerta ao menos 60% das perguntas do quiz (`RN-05-45`,
# documento 11 §2.2). Em inteiro, para não depender de ponto flutuante:
# 3 de 5 passa, 2 de 3 passa, 1 de 2 não passa (design — decisão 3).
NUMERADOR_DO_CORTE_DO_QUIZ = 6
DENOMINADOR_DO_CORTE_DO_QUIZ = 10


def _passou_no_quiz(acertos: int, total: int) -> bool:
    return acertos * DENOMINADOR_DO_CORTE_DO_QUIZ >= total * NUMERADOR_DO_CORTE_DO_QUIZ


def perguntas_do_desbloqueio(
    sessao: Session, *, missao_id: uuid.UUID
) -> list[PerguntaDoDesbloqueio]:
    """As perguntas **vigentes** do quiz, na ordem declarada pelo Mestre
    autor (`RF-09-118`). Acessor único: a pergunta substituída permanece
    guardada, para a submissão que a aponta, e sai de toda leitura do
    desafio por este filtro (`RN-05-47`, design — decisão 4)."""
    return (
        sessao.query(PerguntaDoDesbloqueio)
        .filter(
            PerguntaDoDesbloqueio.missao_id == missao_id,
            PerguntaDoDesbloqueio.substituida_em.is_(None),
        )
        .order_by(PerguntaDoDesbloqueio.ordem)
        .all()
    )


def perguntas_do_desbloqueio_por_missao(
    sessao: Session, *, missao_ids: list[uuid.UUID]
) -> dict[uuid.UUID, list[PerguntaDoDesbloqueio]]:
    """As perguntas vigentes de **várias** missões de uma vez, agrupadas por
    missão — o mesmo filtro e a mesma ordem de `perguntas_do_desbloqueio`,
    para que não haja duas noções de pergunta vigente. A leitura das trilhas
    do Mestre percorre todas as missões de cada trilha: uma consulta por
    missão multiplicaria as idas ao banco pelo tamanho da trilha (design —
    decisão 3)."""
    if not missao_ids:
        return {}
    perguntas = (
        sessao.query(PerguntaDoDesbloqueio)
        .filter(
            PerguntaDoDesbloqueio.missao_id.in_(missao_ids),
            PerguntaDoDesbloqueio.substituida_em.is_(None),
        )
        .order_by(PerguntaDoDesbloqueio.ordem)
        .all()
    )
    agrupadas: dict[uuid.UUID, list[PerguntaDoDesbloqueio]] = {}
    for pergunta in perguntas:
        agrupadas.setdefault(pergunta.missao_id, []).append(pergunta)
    return agrupadas


def referencia_da_imagem_da_pergunta(pergunta: PerguntaDoDesbloqueio) -> str:
    """A referência nasce do id da pergunta que existia no momento do envio
    e **nunca se renomeia**: substituída a pergunta, a linha nova recebe a
    mesma string e o objeto continua onde está (design — decisão 2)."""
    return f"perguntas-do-desbloqueio/{pergunta.id}/imagem"


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


def missoes_desbloqueadas_pelo_guerreiro(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID
) -> set[uuid.UUID]:
    """As missões da trilha que o Guerreiro(a) já **desbloqueou** — o marco
    alcançado que `recompensas_de_marco.regra` verifica, e não mais a
    existência de `Resultado` numa atividade (`RF-09-84`, documento 03 §11,
    documento 11 §2.2, design — decisão 6). Desafio prático ainda não
    julgado (`cumpriu is None`) não conta: enquanto o Mestre não julga, a
    missão aguarda. `missoes_concluidas_pelo_guerreiro` permanece em
    `pontuacao.regra`, a serviço só do motor de níveis, que continua
    contando por `Resultado`."""
    linhas = (
        sessao.query(Missao.id)
        .join(DesbloqueioDaMissao, DesbloqueioDaMissao.missao_id == Missao.id)
        .filter(
            Missao.trilha_id == trilha_id,
            DesbloqueioDaMissao.guerreiro_id == guerreiro_id,
            DesbloqueioDaMissao.cumpriu.is_(True),
        )
        .distinct()
        .all()
    )
    return {linha[0] for linha in linhas}


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


def duplicar_trilha(
    sessao: Session, trilha_de_origem: Trilha | None, *, operador: Persona
) -> Trilha:
    """Duplica a trilha do catálogo como ponto de partida de outra — bem
    comum sob CC BY-SA, então a autoria da cópia é sempre de quem duplicou,
    mesmo que a origem seja de outro Mestre (`RF-09-13`, documento 03 §11,
    design — decisão 8).

    Copia missões e atividades; nunca inscrição, desbloqueio, resultado,
    criação original, recompensa de marco, entrega, desafio de coleta,
    conteúdo, bibliografia, culminância, etiqueta ou auditoria — tudo o que
    é fato de pessoa ou lastro da origem fica com ela. `aula_id` da
    atividade também não é copiado: é vínculo do encontro da origem, não da
    cópia. A origem nunca é alterada.
    """
    if trilha_de_origem is None:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")
    if operador.papel != Papel.mestre:
        raise PermissaoNegada(mensagem="Só o Mestre duplica trilha do catálogo.")
    if (
        trilha_de_origem.situacao == SituacaoDaTrilha.rascunho
        and trilha_de_origem.autor_id != operador.id
    ):
        raise PermissaoNegada(mensagem="Rascunho de outro Mestre não pode ser duplicado.")

    copia = Trilha(
        nome=f"{trilha_de_origem.nome} (cópia)",
        objetivo=trilha_de_origem.objetivo,
        area_do_conhecimento=trilha_de_origem.area_do_conhecimento,
        poder_id=trilha_de_origem.poder_id,
        situacao=SituacaoDaTrilha.rascunho,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(copia)
    sessao.flush()

    missoes_da_origem = (
        sessao.query(Missao).filter_by(trilha_id=trilha_de_origem.id).order_by(Missao.posicao).all()
    )
    for missao_de_origem in missoes_da_origem:
        missao_copiada = Missao(
            trilha_id=copia.id,
            titulo=missao_de_origem.titulo,
            posicao=missao_de_origem.posicao,
            nivel_de_dificuldade=missao_de_origem.nivel_de_dificuldade,
            obrigatoria=missao_de_origem.obrigatoria,
            e_sondagem=missao_de_origem.e_sondagem,
            etapa_do_ciclo=missao_de_origem.etapa_do_ciclo,
            cadencia_de_retomada=missao_de_origem.cadencia_de_retomada,
            materiais=list(missao_de_origem.materiais),
            tipo_do_desafio_de_desbloqueio=missao_de_origem.tipo_do_desafio_de_desbloqueio,
            desafio_de_desbloqueio_enunciado=missao_de_origem.desafio_de_desbloqueio_enunciado,
            autor_id=operador.id,
            papel_do_autor=operador.papel.value,
        )
        sessao.add(missao_copiada)
        sessao.flush()

        for pergunta_de_origem in perguntas_do_desbloqueio(sessao, missao_id=missao_de_origem.id):
            sessao.add(
                PerguntaDoDesbloqueio(
                    missao_id=missao_copiada.id,
                    ordem=pergunta_de_origem.ordem,
                    enunciado=pergunta_de_origem.enunciado,
                    alternativa_1=pergunta_de_origem.alternativa_1,
                    alternativa_2=pergunta_de_origem.alternativa_2,
                    alternativa_3=pergunta_de_origem.alternativa_3,
                    alternativa_4=pergunta_de_origem.alternativa_4,
                    alternativa_correta=pergunta_de_origem.alternativa_correta,
                    # A cópia aponta a **mesma** referência, sem copiar
                    # bytes: imagem de trilha é bem comum como a trilha
                    # (`RF-09-13`, `RF-09-119`).
                    imagem_referencia=pergunta_de_origem.imagem_referencia,
                    imagem_tipo=pergunta_de_origem.imagem_tipo,
                    imagem_tamanho=pergunta_de_origem.imagem_tamanho,
                )
            )

        # A duplicação copia a trilha como ela é hoje: atividade carimbada
        # não é parte dela e não atravessa (`RN-09-47`).
        atividades_da_origem = atividade_vigente(
            sessao.query(Atividade).filter_by(missao_id=missao_de_origem.id)
        ).all()
        for atividade_de_origem in atividades_da_origem:
            sessao.add(
                Atividade(
                    missao_id=missao_copiada.id,
                    titulo=atividade_de_origem.titulo,
                    descricao=atividade_de_origem.descricao,
                    modalidade=atividade_de_origem.modalidade,
                    formato=atividade_de_origem.formato,
                    natureza=atividade_de_origem.natureza,
                    producao_esperada=atividade_de_origem.producao_esperada,
                    aula_id=None,
                    autor_id=operador.id,
                    papel_do_autor=operador.papel.value,
                )
            )

    sessao.flush()
    return copia


def _conferir_titulo_da_missao(titulo: str | None) -> str:
    """As conferências de campo da missão valem iguais na criação e na
    correção — mensagem e campo são os mesmos nas duas portas (`RF-09-02`,
    `RF-09-136`, design — decisão 1)."""
    if not titulo or not titulo.strip():
        raise ErroDeValidacao(mensagem="Missão exige um título.", campo="titulo")
    return titulo


def _conferir_obrigatoriedade_da_missao(obrigatoria: bool | None) -> bool:
    if obrigatoria is None:
        raise ErroDeValidacao(
            mensagem="Missão exige a declaração de obrigatória ou opcional.",
            campo="obrigatoria",
        )
    return obrigatoria


def _conferir_etapa_da_missao(etapa_do_ciclo: str | None) -> EtapaDoCiclo:
    try:
        return EtapaDoCiclo(etapa_do_ciclo)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Etapa do ciclo fora dos valores previstos.", campo="etapa_do_ciclo"
        ) from exc


def _conferir_sondagem(
    sessao: Session, *, trilha_id: uuid.UUID, posicao: int, missao_id: uuid.UUID | None
) -> None:
    """A sondagem ocupa a primeira posição e é única na trilha (documento 99
    §6 invariante 5). Na correção, a própria missão não conta como "outra"
    sondagem (`RN-09-57`)."""
    if posicao != 1:
        raise ErroDeValidacao(
            mensagem="A missão de sondagem ocupa a primeira posição da trilha.",
            campo="e_sondagem",
        )
    consulta = sessao.query(Missao).filter_by(trilha_id=trilha_id, e_sondagem=True)
    if missao_id is not None:
        consulta = consulta.filter(Missao.id != missao_id)
    if consulta.first() is not None:
        raise ErroDeValidacao(
            mensagem="Esta trilha já tem uma missão de sondagem.", campo="e_sondagem"
        )


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
    materiais: list[str] | None = None,
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
    titulo = _conferir_titulo_da_missao(titulo)
    obrigatoria = _conferir_obrigatoriedade_da_missao(obrigatoria)
    etapa_valida = _conferir_etapa_da_missao(etapa_do_ciclo)
    materiais_validos = _conferir_materiais_da_missao(materiais if materiais is not None else [])
    if e_sondagem:
        _conferir_sondagem(sessao, trilha_id=trilha.id, posicao=posicao, missao_id=None)

    missao = Missao(
        trilha_id=trilha.id,
        titulo=titulo,
        posicao=posicao,
        nivel_de_dificuldade=nivel_de_dificuldade,
        obrigatoria=obrigatoria,
        etapa_do_ciclo=etapa_valida,
        e_sondagem=e_sondagem,
        cadencia_de_retomada=cadencia_de_retomada,
        materiais=materiais_validos,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(missao)
    sessao.flush()
    return missao


def _despublicar_pela_correcao(
    sessao: Session, trilha: Trilha, *, operador: Persona, missao: Missao
) -> None:
    """A correção do Mestre que quebra trava de trilha publicada é aceita e
    tira a trilha do ar no mesmo ato, com o próprio Mestre como autor da
    situação e o motivo gerado aqui (`RN-09-59`, design — decisão 6). Não
    toca fato gravado do Guerreiro(a), como `despublicar_trilha`."""
    pendentes = _travas_de_publicacao_pendentes(sessao, trilha)
    trilha.situacao = SituacaoDaTrilha.despublicada
    trilha.motivo_da_situacao = (
        f'A correção da missão "{missao.titulo}" deixou a trilha sem '
        f"{_unir_em_portugues(pendentes)}. Corrija e publique de novo."
    )
    trilha.autor_da_situacao_id = operador.id
    trilha.papel_do_autor_da_situacao = operador.papel.value
    trilha.situacao_alterada_em = agora()


def _conferir_materiais_da_missao(materiais: list[str] | None) -> list[str]:
    """Os materiais são só nomes: cada um sem os espaços das pontas, e nome
    vazio é recusado. Sem teto de itens nem de tamanho — nenhum número foi
    decidido (`RF-09-140`, `RN-09-61`, design — decisão 3)."""
    if materiais is None:
        raise ErroDeValidacao(
            mensagem="Mande a lista dos materiais; lista vazia apaga os declarados.",
            campo="materiais",
        )
    aparados = [material.strip() for material in materiais]
    if any(not material for material in aparados):
        raise ErroDeValidacao(mensagem="Cada material precisa de um nome.", campo="materiais")
    return aparados


def corrigir_missao(
    sessao: Session, *, operador: Persona, missao: Missao | None, campos: dict
) -> Missao:
    """Corrige título, dificuldade, obrigatoriedade, etapa, sondagem e os
    materiais (`RF-09-140`), em
    qualquer situação da trilha e só pelo Mestre autor (`RF-09-136`,
    `RN-09-56`). Campo ausente de `campos` conserva o valor gravado; a posição
    não chega aqui — muda só por `mover_missao`. Desmarcar a sondagem de
    trilha publicada despublica (`RN-09-59`, design — decisão 6)."""
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_autoria_estrita_da_trilha(trilha, operador)

    if "titulo" in campos:
        titulo = _conferir_titulo_da_missao(campos["titulo"])
    if "obrigatoria" in campos:
        obrigatoria = _conferir_obrigatoriedade_da_missao(campos["obrigatoria"])
    if "etapa_do_ciclo" in campos:
        etapa = _conferir_etapa_da_missao(campos["etapa_do_ciclo"])
    if "materiais" in campos:
        materiais = _conferir_materiais_da_missao(campos["materiais"])
    if "nivel_de_dificuldade" in campos and campos["nivel_de_dificuldade"] is None:
        raise ErroDeValidacao(
            mensagem="Missão exige o nível de dificuldade.", campo="nivel_de_dificuldade"
        )
    era_sondagem = missao.e_sondagem
    if "e_sondagem" in campos:
        if campos["e_sondagem"] is None:
            raise ErroDeValidacao(
                mensagem="Diga se a missão é ou não a sondagem.", campo="e_sondagem"
            )
        if campos["e_sondagem"] and not era_sondagem:
            _conferir_sondagem(
                sessao, trilha_id=trilha.id, posicao=missao.posicao, missao_id=missao.id
            )

    if "titulo" in campos:
        missao.titulo = titulo
    if "obrigatoria" in campos:
        missao.obrigatoria = obrigatoria
    if "etapa_do_ciclo" in campos:
        missao.etapa_do_ciclo = etapa
    if "nivel_de_dificuldade" in campos:
        missao.nivel_de_dificuldade = campos["nivel_de_dificuldade"]
    if "e_sondagem" in campos:
        missao.e_sondagem = campos["e_sondagem"]
    if "materiais" in campos:
        missao.materiais = materiais
    sessao.flush()

    if era_sondagem and not missao.e_sondagem and trilha.situacao == SituacaoDaTrilha.publicada:
        _despublicar_pela_correcao(sessao, trilha, operador=operador, missao=missao)
        sessao.flush()
    return missao


def mover_missao(
    sessao: Session, *, operador: Persona, missao: Missao | None, direcao: str | None
) -> list[Missao]:
    """Troca a posição com a **vizinha** da sequência inteira da trilha — não
    da etapa —, no molde de `conteudos.regra.mover_conteudo` (`RF-09-137`,
    design — decisões 4 e 5). Só as duas mudam; lacunas na sequência são
    aceitas. A sondagem não desce e nada sobe para o lugar dela (`RN-09-57`).
    A troca roda com a unicidade de posição adiada até o `COMMIT`."""
    from sqlalchemy import text

    from ..conteudos.regra import DirecaoDoMovimento

    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_autoria_estrita_da_trilha(trilha, operador)
    try:
        sentido = DirecaoDoMovimento(direcao)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="A direção do movimento é 'cima' ou 'baixo'.", campo="direcao"
        ) from exc

    irmas = sessao.query(Missao).filter_by(trilha_id=trilha.id).order_by(Missao.posicao).all()
    indice = next(i for i, irma in enumerate(irmas) if irma.id == missao.id)
    vizinha_indice = indice - 1 if sentido == DirecaoDoMovimento.cima else indice + 1
    if vizinha_indice < 0 or vizinha_indice >= len(irmas):
        raise ErroDeValidacao(
            mensagem=(
                "Esta missão já é a primeira da trilha."
                if sentido == DirecaoDoMovimento.cima
                else "Esta missão já é a última da trilha."
            ),
            campo="direcao",
        )
    vizinha = irmas[vizinha_indice]
    if missao.e_sondagem or vizinha.e_sondagem:
        raise ErroDeValidacao(
            mensagem="A missão de sondagem abre a trilha e fica na primeira posição.",
            campo="direcao",
        )

    sessao.execute(text("SET CONSTRAINTS uq_missao_trilha_id_posicao DEFERRED"))
    missao.posicao, vizinha.posicao = vizinha.posicao, missao.posicao
    sessao.flush()
    return [missao, vizinha]


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


def _conferir_titulo_da_atividade(titulo: str | None) -> str:
    """As quatro conferências de campo valem iguais na criação e na correção
    da atividade de trilha: mensagem e campo são os mesmos nas duas portas
    (`RF-09-70`, `RF-09-127`). A **natureza** não tem par aqui — ela só se
    declara na criação (`RN-09-49`)."""
    if not titulo or not titulo.strip():
        raise ErroDeValidacao(mensagem="Atividade exige um título.", campo="titulo")
    return titulo


def _conferir_modalidade_da_atividade(modalidade: str | None) -> ModalidadeDeAtividade:
    if not modalidade:
        raise ErroDeValidacao(mensagem="Atividade exige modalidade.", campo="modalidade")
    try:
        return ModalidadeDeAtividade(modalidade)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Modalidade fora dos valores previstos.", campo="modalidade"
        ) from exc


def _conferir_formato_da_atividade(formato: str | None) -> FormatoDeAtividade:
    if not formato:
        raise ErroDeValidacao(mensagem="Atividade exige formato.", campo="formato")
    try:
        return FormatoDeAtividade(formato)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Formato fora dos valores previstos.", campo="formato"
        ) from exc


def _conferir_producao_esperada_da_atividade(producao_esperada: str | None) -> str:
    if not producao_esperada or not producao_esperada.strip():
        raise ErroDeValidacao(
            mensagem="Atividade exige a declaração do que o Guerreiro(a) produz.",
            campo="producao_esperada",
        )
    return producao_esperada


def atividade_vigente(consulta):
    """Acrescenta a uma consulta de `Atividade` o filtro do carimbo. Porta
    **única** da exclusão: toda leitura de **autoria** (as missões da trilha
    do Mestre e a pública) e de **execução** (os semanais do Guerreiro(a), a
    programação do encontro, as atividades da equipe) passa por aqui, para
    que não haja duas noções de atividade vigente (`RN-09-47`, design —
    decisão 3).

    A leitura que parte de um **fato gravado** — `pontuacao`, `evolucao`, a
    equipe no painel do dia — **não** a chama: é da atividade carimbada que o
    fato fala, e escondê-la ali apagaria o Resultado da vista.
    """
    return consulta.filter(Atividade.removida_em.is_(None))


def conferir_atividade_vigente(atividade: Atividade) -> None:
    """Recusa com 422 o **fato novo** sobre atividade carimbada: lançamento de
    Resultado, entrega de produção, abertura de partida de quiz e ocorrência
    de conduta. Porta única da recusa, par de `atividade_vigente`
    (`RN-09-47`, design — decisão 3)."""
    if atividade.removida_em is not None:
        raise ErroDeValidacao(
            mensagem="A atividade foi removida pelo Mestre autor e não recebe lançamento novo.",
            campo="atividade_id",
        )


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

    titulo_valido = _conferir_titulo_da_atividade(titulo)
    modalidade_valida = _conferir_modalidade_da_atividade(modalidade)
    formato_valido = _conferir_formato_da_atividade(formato)

    if not natureza or not natureza.strip():
        raise ErroDeValidacao(mensagem="Atividade exige natureza.", campo="natureza")

    producao_valida = _conferir_producao_esperada_da_atividade(producao_esperada)

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
        titulo=titulo_valido,
        descricao=descricao,
        modalidade=modalidade_valida,
        formato=formato_valido,
        natureza=_normalizar_natureza(natureza),
        producao_esperada=producao_valida,
        aula_id=aula_id,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(atividade)
    sessao.flush()
    return atividade


@dataclass(frozen=True)
class FatosDaAtividade:
    """Quantos fatos já apontam para uma atividade de trilha — é o que a tela
    diz ao Mestre **antes** de ele confirmar a remoção (`RF-09-128`)."""

    resultados: int
    producoes: int
    partidas_de_quiz: int
    partidas_abertas: int
    ocorrencias_de_conduta: int
    equipes_com_ela_corrente: int


def _conferir_atividade_de_trilha_do_autor(
    sessao: Session, atividade: Atividade | None, operador: Persona
) -> Atividade:
    """A guarda comum das três portas da fatia 25. Três recusas, nesta ordem:
    atividade inexistente é 404; **avulsa** (a que declara `poder_id`) é 422,
    porque é cadastro da gestão pela App 03, com matriz de permissão e âncora
    de ponto próprios (`RF-02-29`); e **carimbada** é 422, porque já saiu.

    A autoria é **estrita** — nem outro Mestre nem Admin: a criação aceita o
    Admin, a correção não, pelo mesmo motivo que a fatia 24 fixou para o
    conteúdo (ele audita e despublica a trilha, não a redige).
    """
    if atividade is None:
        raise NaoEncontrado(mensagem="Atividade não encontrada.")
    if atividade.missao_id is None:
        raise ErroDeValidacao(
            mensagem=(
                "Esta é a atividade avulsa da gestão: ela se corrige e se remove na App 03, "
                "não aqui."
            ),
            campo="atividade_id",
        )
    if atividade.removida_em is not None:
        raise ErroDeValidacao(mensagem="Esta atividade já foi removida.", campo="atividade_id")

    missao = sessao.get(Missao, atividade.missao_id)
    conferir_autoria_estrita_da_trilha(sessao.get(Trilha, missao.trilha_id), operador)
    return atividade


def corrigir_atividade(
    sessao: Session, *, operador: Persona, atividade: Atividade | None, campos: dict
) -> Atividade:
    """Corrige, na própria linha, **título**, **descrição**, **modalidade**,
    **formato** e **produção esperada** de uma atividade de trilha já gravada,
    em qualquer situação da trilha (`RF-09-127`). Campo ausente de `campos`
    conserva o valor; campo presente passa pelas mesmas conferências da
    criação.

    Nada do que já foi gravado é tocado: `Resultado`, produção, partida e
    ocorrência seguem como estavam, e nenhum ponto, badge ou nível é
    estornado (`RF-09-47`). A **natureza** não chega aqui — ela é porta de
    elegibilidade, não rótulo, e trocá-la é remover a atividade e cadastrar
    outra (`RN-09-49`).

    Levar o **formato** para fora do presencial **limpa a aula** declarada:
    atividade on-line com aula é exatamente o estado que `criar_atividade`
    recusa, e a correção não o faz nascer pela porta de trás (`RN-09-48`).
    """
    alvo = _conferir_atividade_de_trilha_do_autor(sessao, atividade, operador)

    if "titulo" in campos:
        alvo.titulo = _conferir_titulo_da_atividade(campos["titulo"])
    if "descricao" in campos:
        alvo.descricao = campos["descricao"]
    if "modalidade" in campos:
        alvo.modalidade = _conferir_modalidade_da_atividade(campos["modalidade"])
    if "formato" in campos:
        alvo.formato = _conferir_formato_da_atividade(campos["formato"])
    if "producao_esperada" in campos:
        alvo.producao_esperada = _conferir_producao_esperada_da_atividade(
            campos["producao_esperada"]
        )

    if alvo.formato != FormatoDeAtividade.presencial:
        alvo.aula_id = None

    sessao.flush()
    return alvo


def remover_atividade(
    sessao: Session, *, operador: Persona, atividade: Atividade | None
) -> Atividade:
    """Tira a atividade da trilha **carimbando-a**: ela sai de toda leitura de
    autoria e de execução e permanece guardada, porque cinco tabelas a apontam
    e `RF-09-47` veda editar ou remover Resultado gravado (`RF-09-128`,
    `RN-09-47`). O carimbo é incondicional, como em
    `remover_pergunta_do_desbloqueio` — um caminho só, sem ramo que dependa de
    contagem.

    Dos cinco ponteiros, quatro são **fato passado** e ficam intactos. O
    quinto é **estado vivo**: a escolha corrente da equipe é zerada, para o
    painel do dia não anunciar missão corrente de atividade que não existe
    mais. Partida de quiz **aberta** impede a remoção — ela se encerra na tela
    da turma, com consequência de pontuação, e não se apaga por baixo
    (decisão do fundador, 2026-10-27).

    Missão pode ficar com **nenhuma** atividade: nenhuma das travas de
    publicação exige atividade (`RF-09-06`, `RF-09-07`, `RF-09-82`).
    """
    from ..equipes.modelo import Equipe
    from ..quiz.modelo import PartidaDeQuiz, SituacaoDaPartida

    alvo = _conferir_atividade_de_trilha_do_autor(sessao, atividade, operador)

    abertas = (
        sessao.query(PartidaDeQuiz)
        .filter(
            PartidaDeQuiz.atividade_id == alvo.id,
            PartidaDeQuiz.situacao == SituacaoDaPartida.aberta,
        )
        .count()
    )
    if abertas:
        raise ErroDeValidacao(
            mensagem=(
                "Corre uma partida de quiz aberta sobre esta atividade. Encerre a partida "
                "antes de removê-la."
            ),
            campo="atividade_id",
        )

    alvo.removida_em = agora()
    # `synchronize_session="fetch"` e não `False`: a equipe já carregada na
    # sessão precisa enxergar a escolha zerada, senão a leitura que vier na
    # mesma transação — o painel do dia, à frente — ainda anuncia a missão
    # corrente da atividade que acabou de sair.
    sessao.query(Equipe).filter(Equipe.atividade_corrente_id == alvo.id).update(
        {Equipe.atividade_corrente_id: None}, synchronize_session="fetch"
    )
    sessao.flush()
    return alvo


def fatos_da_atividade(
    sessao: Session, *, operador: Persona, atividade: Atividade | None
) -> FatosDaAtividade:
    """As contagens que a tela apresenta na confirmação da remoção
    (`RF-09-128`). Leitura **própria**, nunca aninhada em `GET
    /v1/trilhas/minhas`: cinco `COUNT` por atividade por missão seriam pagos
    em toda abertura da tela da trilha, por uma remoção que quase nunca
    acontece — o mesmo motivo de `RN-09-46` (design — decisão 7)."""
    from ..equipes.modelo import Equipe
    from ..ocorrencias_de_conduta.modelo import OcorrenciaDeConduta
    from ..producoes.modelo import ProducaoDaMissao
    from ..quiz.modelo import PartidaDeQuiz, SituacaoDaPartida
    from ..resultados.modelo import Resultado

    alvo = _conferir_atividade_de_trilha_do_autor(sessao, atividade, operador)

    def _contar(modelo, *filtros) -> int:
        return sessao.query(modelo).filter(modelo.atividade_id == alvo.id, *filtros).count()

    return FatosDaAtividade(
        resultados=_contar(Resultado),
        producoes=_contar(ProducaoDaMissao),
        partidas_de_quiz=_contar(PartidaDeQuiz),
        partidas_abertas=_contar(PartidaDeQuiz, PartidaDeQuiz.situacao == SituacaoDaPartida.aberta),
        ocorrencias_de_conduta=_contar(OcorrenciaDeConduta),
        equipes_com_ela_corrente=(
            sessao.query(Equipe).filter(Equipe.atividade_corrente_id == alvo.id).count()
        ),
    )


def inscrever_na_trilha(
    sessao: Session, *, guerreiro: Persona, trilha: Trilha | None
) -> InscricaoNaTrilha:
    """Ato do próprio Guerreiro(a) em sessão — exige trilha publicada
    (`RF-05-09`, `RN-05-43`). Inscrever-se de novo na mesma trilha devolve
    a existente, sem gravar uma segunda (`RN-05-43`). Reavalia o nível 1
    logo em seguida, para o caso raro de já existir `Resultado` anterior à
    inscrição (documento 11 §6)."""
    if trilha is None:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")
    if trilha.situacao != SituacaoDaTrilha.publicada:
        raise ErroDeValidacao(
            mensagem="Só é possível se inscrever numa trilha publicada.", campo="trilha_id"
        )

    existente = (
        sessao.query(InscricaoNaTrilha)
        .filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id)
        .first()
    )
    if existente is not None:
        return existente

    inscricao = InscricaoNaTrilha(guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    sessao.add(inscricao)
    sessao.flush()
    avaliar_niveis(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    return inscricao


def consultar_inscricoes_do_guerreiro(
    sessao: Session, *, guerreiro_id: uuid.UUID
) -> list[InscricaoNaTrilha]:
    return sessao.query(InscricaoNaTrilha).filter_by(guerreiro_id=guerreiro_id).all()


def _conferir_inscricao(sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID) -> None:
    """Comum à submissão do desafio e à leitura do percurso: só quem está
    inscrito tem o que submeter ou ler (`RN-05-21`, documento 11 §2.2)."""
    inscrito = (
        sessao.query(InscricaoNaTrilha)
        .filter_by(guerreiro_id=guerreiro_id, trilha_id=trilha_id)
        .first()
        is not None
    )
    if not inscrito:
        raise ErroDeValidacao(
            mensagem="Esta operação exige inscrição na própria trilha.", campo="trilha_id"
        )


TETO_DO_TITULO_CURTO_DO_PRATICO = 60


def declarar_desafio_de_desbloqueio(
    sessao: Session,
    *,
    operador: Persona,
    missao: Missao | None,
    tipo: str | None,
    enunciado: str | None = None,
    perguntas: list[dict] | None = None,
    forma_de_comprovacao: str | None = None,
    criterio_de_aceite: str | None = None,
    titulo_curto: str | None = None,
    kit_apresentado_id: uuid.UUID | None = None,
) -> Missao:
    """Só o Mestre autor da trilha declara — declarar de novo substitui o
    anterior, com as perguntas dele, como `declarar_cadencia_de_retomada` já
    faz (`RF-09-26`, `RF-09-117`, `RF-09-118`). O **quiz** traz uma ou mais
    perguntas, cada uma com enunciado, quatro alternativas e a correta entre
    elas; quiz sem nenhuma pergunta é recusado (`RN-09-43`). O **prático**
    traz o enunciado do que o Guerreiro(a) precisa cumprir e, desde
    2026-11-04, a **forma de comprovação** que o Mestre aceita, o **critério
    de aceite** e o **título curto** da vitrine (`RF-09-129` a `RF-09-131`,
    `RN-09-50`). Missão sem desafio segue publicável — esta declaração nunca é
    trava de publicação.

    Desde 2026-11-12 o prático declara, opcional, o **kit que apresenta** — uma
    recompensa de marco da mesma trilha; declarar de novo o substitui, e o quiz
    nunca o tem (`RF-09-141`).
    """
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    try:
        tipo_valido = TipoDeDesafioDeDesbloqueio(tipo)
    except (ValueError, TypeError) as exc:
        raise ErroDeValidacao(
            mensagem="Tipo de desafio fora dos valores previstos.", campo="tipo"
        ) from exc

    if tipo_valido == TipoDeDesafioDeDesbloqueio.quiz:
        perguntas_validas = _conferir_perguntas_do_quiz(perguntas)
        _recusar_campos_do_pratico_no_quiz(
            forma_de_comprovacao=forma_de_comprovacao,
            criterio_de_aceite=criterio_de_aceite,
            titulo_curto=titulo_curto,
        )
        if kit_apresentado_id is not None:
            raise ErroDeValidacao(
                mensagem="O quiz não declara o kit apresentado: o campo é só do prático.",
                campo="kit_apresentado_id",
            )
    else:
        if not enunciado or not enunciado.strip():
            raise ErroDeValidacao(mensagem="Desafio prático exige um enunciado.", campo="enunciado")
        forma_valida = _conferir_forma_de_comprovacao(forma_de_comprovacao)
        criterio_valido = _conferir_criterio_de_aceite(criterio_de_aceite)
        titulo_valido = _conferir_titulo_curto(titulo_curto)
        kit_valido = _conferir_kit_apresentado(sessao, missao, kit_apresentado_id)

    vigentes = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    imagens = _conferir_imagens_declaradas(
        perguntas_validas if tipo_valido == TipoDeDesafioDeDesbloqueio.quiz else [], vigentes
    )

    # Redeclarar substitui, mas nunca apaga: a pergunta anterior é
    # **carimbada** e sai da leitura, de modo que a submissão já gravada
    # siga apontando o que o Guerreiro(a) respondeu (`RN-05-47`, design —
    # decisão 4). O carimbo precede a gravação das novas, para que o índice
    # parcial de (missão, ordem) nunca veja duas gerações vigentes.
    momento = agora()
    for pergunta in vigentes:
        pergunta.substituida_em = momento
    sessao.flush()

    missao.tipo_do_desafio_de_desbloqueio = tipo_valido
    if tipo_valido == TipoDeDesafioDeDesbloqueio.quiz:
        missao.desafio_de_desbloqueio_enunciado = None
        missao.desafio_pratico_forma_de_comprovacao = None
        missao.desafio_pratico_criterio_de_aceite = None
        missao.desafio_pratico_titulo_curto = None
        missao.desafio_pratico_kit_id = None
        for ordem, (pergunta, imagem) in enumerate(
            zip(perguntas_validas, imagens, strict=True), start=1
        ):
            sessao.add(
                PerguntaDoDesbloqueio(
                    missao_id=missao.id,
                    ordem=ordem,
                    enunciado=pergunta["enunciado"],
                    alternativa_1=pergunta["alternativas"][0],
                    alternativa_2=pergunta["alternativas"][1],
                    alternativa_3=pergunta["alternativas"][2],
                    alternativa_4=pergunta["alternativas"][3],
                    alternativa_correta=pergunta["alternativa_correta"],
                    imagem_referencia=imagem.referencia if imagem is not None else None,
                    imagem_tipo=imagem.tipo if imagem is not None else None,
                    imagem_tamanho=imagem.tamanho if imagem is not None else None,
                )
            )
    else:
        missao.desafio_de_desbloqueio_enunciado = enunciado
        missao.desafio_pratico_forma_de_comprovacao = forma_valida
        missao.desafio_pratico_criterio_de_aceite = criterio_valido
        missao.desafio_pratico_titulo_curto = titulo_valido
        missao.desafio_pratico_kit_id = kit_valido

    sessao.flush()
    return missao


def _conferir_kit_apresentado(
    sessao: Session, missao: Missao, kit_apresentado_id: uuid.UUID | None
) -> uuid.UUID | None:
    """O kit é opcional; declarado, precisa ser recompensa de marco da **mesma
    trilha** da missão (`RF-09-141`)."""
    if kit_apresentado_id is None:
        return None
    recompensa = sessao.get(RecompensaDeMarco, kit_apresentado_id)
    if recompensa is None or recompensa.trilha_id != missao.trilha_id:
        raise ErroDeValidacao(
            mensagem="O kit apresentado precisa ser uma recompensa de marco desta trilha.",
            campo="kit_apresentado_id",
        )
    return recompensa.id


@dataclass
class KitApresentado:
    recompensa_de_marco_id: uuid.UUID
    tipo_de_recurso_nome: str


def kit_apresentado_da_missao(sessao: Session, missao: Missao) -> KitApresentado | None:
    """O kit que o prático declarou, com o nome do tipo de recurso, para as
    leituras que já servem os campos do prático (`RF-09-141`)."""
    if missao.desafio_pratico_kit_id is None:
        return None
    linha = (
        sessao.query(RecompensaDeMarco.id, TipoDeRecurso.nome)
        .join(TipoDeRecurso, TipoDeRecurso.id == RecompensaDeMarco.tipo_de_recurso_id)
        .filter(RecompensaDeMarco.id == missao.desafio_pratico_kit_id)
        .first()
    )
    if linha is None:
        return None
    return KitApresentado(recompensa_de_marco_id=linha[0], tipo_de_recurso_nome=linha[1])


# Os três campos do prático: a recusa é **por campo**, para que a tela do
# Mestre diga o que falta em vez de uma falha genérica (`RN-09-50`).
_CAMPOS_SO_DO_PRATICO = (
    ("forma_de_comprovacao", "a forma de comprovação"),
    ("criterio_de_aceite", "o critério de aceite"),
    ("titulo_curto", "o título curto"),
)


def _recusar_campos_do_pratico_no_quiz(
    *, forma_de_comprovacao: str | None, criterio_de_aceite: str | None, titulo_curto: str | None
) -> None:
    """No quiz os três não se aplicam: o critério é o corte de acertos, que o
    núcleo afere sozinho, e não há comprovação a enquadrar nem entrega a
    intitular. Recusar é melhor que ignorar em silêncio, que deixaria o Mestre
    achar que declarou o que não declarou (design — decisão 5)."""
    recebidos = {
        "forma_de_comprovacao": forma_de_comprovacao,
        "criterio_de_aceite": criterio_de_aceite,
        "titulo_curto": titulo_curto,
    }
    for campo, nome in _CAMPOS_SO_DO_PRATICO:
        if recebidos[campo] is not None:
            raise ErroDeValidacao(
                mensagem=f"O quiz não declara {nome}: ela é só do desafio prático.",
                campo=campo,
            )


def _conferir_forma_de_comprovacao(valor: str | None) -> TipoDeProducaoDaCriacaoOriginal:
    """Uma das **seis** formas de entrega do Guerreiro(a) (`RF-09-129`,
    documento 02 §4) — o mesmo conjunto fechado da criação original, não uma
    segunda lista dele (design — decisão 3)."""
    if valor is None:
        raise ErroDeValidacao(
            mensagem="Desafio prático exige a forma de comprovação aceita.",
            campo="forma_de_comprovacao",
        )
    try:
        return TipoDeProducaoDaCriacaoOriginal(valor)
    except (ValueError, TypeError) as exc:
        raise ErroDeValidacao(
            mensagem="Forma de comprovação fora das seis formas de entrega.",
            campo="forma_de_comprovacao",
        ) from exc


def _conferir_criterio_de_aceite(valor: str | None) -> str:
    """Texto livre do Mestre autor, que o núcleo guarda e nunca afere
    (`RF-09-130`)."""
    if valor is None or not valor.strip():
        raise ErroDeValidacao(
            mensagem="Desafio prático exige o critério de aceite.", campo="criterio_de_aceite"
        )
    return valor


def _conferir_titulo_curto(valor: str | None) -> str:
    """Campo próprio, nunca o enunciado: é ele que a vitrine exibe ao lado do
    nick, e por isso tem teto (`RF-09-131`, `RN-09-51`)."""
    if valor is None or not valor.strip():
        raise ErroDeValidacao(
            mensagem="Desafio prático exige o título curto.", campo="titulo_curto"
        )
    if len(valor) > TETO_DO_TITULO_CURTO_DO_PRATICO:
        raise ErroDeValidacao(
            mensagem=(
                "O título curto tem no máximo "
                f"{TETO_DO_TITULO_CURTO_DO_PRATICO} caracteres, e chegou com {len(valor)}."
            ),
            campo="titulo_curto",
        )
    return valor


@dataclass(frozen=True)
class _ImagemPreservada:
    """O que a referência devolvida traz de volta: os três campos da imagem
    da pergunta de origem, copiados sem que byte algum seja reenviado."""

    referencia: str
    tipo: str | None
    tamanho: int | None


def _conferir_imagens_declaradas(
    perguntas: list[dict], vigentes: list[PerguntaDoDesbloqueio]
) -> list[_ImagemPreservada | None]:
    """A referência que volta é conferida contra as imagens das perguntas
    **daquela mesma missão**, antes da substituição: sem isso o campo seria
    um endereço de armazenamento escolhido pelo cliente, capaz de apontar
    arquivo de outra trilha (`RF-09-119`, design — decisão 3). A pergunta
    que omite a referência nasce sem imagem — é assim que o Mestre a remove.
    """
    conhecidas = {
        pergunta.imagem_referencia: _ImagemPreservada(
            referencia=pergunta.imagem_referencia,
            tipo=pergunta.imagem_tipo,
            tamanho=pergunta.imagem_tamanho,
        )
        for pergunta in vigentes
        if pergunta.imagem_referencia is not None
    }
    preservadas: list[_ImagemPreservada | None] = []
    for pergunta in perguntas:
        referencia = pergunta.get("imagem_referencia")
        if referencia is None:
            preservadas.append(None)
            continue
        imagem = conhecidas.get(referencia)
        if imagem is None:
            raise ErroDeValidacao(
                mensagem=(
                    "A imagem devolvida não é de uma pergunta desta missão. Reenvie a "
                    "imagem ou deixe a pergunta sem imagem."
                ),
                campo="perguntas",
            )
        preservadas.append(imagem)
    return preservadas


def conferir_pergunta_do_quiz(pergunta: dict, *, campo: str = "perguntas") -> dict:
    """Uma pergunta exige enunciado, quatro alternativas e a correta entre
    elas (`RF-09-118`, `RN-09-44`). Conferência **única**, de dois
    chamadores: a declaração do desafio inteiro, que a aplica a cada
    pergunta da lista, e a escrita de uma pergunta isolada, que grava
    completa ou não grava (design — decisão 4). O `campo` distingue a
    recusa por lista da recusa pela pergunta que o Mestre tem na tela.
    """
    if not pergunta.get("enunciado", "").strip():
        raise ErroDeValidacao(mensagem="Toda pergunta do quiz exige um enunciado.", campo=campo)
    alternativas = pergunta.get("alternativas") or []
    if len(alternativas) != TOTAL_DE_ALTERNATIVAS_DO_DESBLOQUEIO or not all(
        alternativa and alternativa.strip() for alternativa in alternativas
    ):
        raise ErroDeValidacao(
            mensagem="Toda pergunta do quiz exige quatro alternativas.", campo=campo
        )
    correta = pergunta.get("alternativa_correta")
    if correta is None or not (
        PRIMEIRA_ALTERNATIVA_DO_DESBLOQUEIO <= correta <= TOTAL_DE_ALTERNATIVAS_DO_DESBLOQUEIO
    ):
        raise ErroDeValidacao(
            mensagem="Toda pergunta do quiz exige a alternativa correta.", campo=campo
        )
    return pergunta


def _conferir_perguntas_do_quiz(perguntas: list[dict] | None) -> list[dict]:
    """Quiz exige ao menos uma pergunta, e cada uma exige o que
    `conferir_pergunta_do_quiz` confere (`RN-09-43`, `RF-09-118`)."""
    if not perguntas:
        raise ErroDeValidacao(
            mensagem="Desafio em forma de quiz exige ao menos uma pergunta.",
            campo="perguntas",
        )
    for pergunta in perguntas:
        conferir_pergunta_do_quiz(pergunta)
    return perguntas


def _conferir_posse_da_pergunta(
    sessao: Session, pergunta: PerguntaDoDesbloqueio | None, operador: Persona
) -> PerguntaDoDesbloqueio:
    """A pergunta é da missão, e a missão é da trilha do Mestre autor — a
    mesma posse que a declaração do desafio inteiro confere (`RF-09-120`).
    Pergunta já substituída não se escreve: ela pertence ao registro da
    tentativa, não ao desafio vigente (`RN-05-47`)."""
    if pergunta is None:
        raise NaoEncontrado(mensagem="Pergunta não encontrada.")
    if pergunta.substituida_em is not None:
        raise NaoEncontrado(mensagem="Pergunta não encontrada.")
    missao = sessao.get(Missao, pergunta.missao_id)
    conferir_posse_da_trilha(sessao.get(Trilha, missao.trilha_id), operador)
    return pergunta


def _alguma_submissao_respondeu(sessao: Session, pergunta: PerguntaDoDesbloqueio) -> bool:
    return sessao.query(RespostaDaSubmissao).filter_by(pergunta_id=pergunta.id).first() is not None


def _aplicar_pergunta(alvo: PerguntaDoDesbloqueio, pergunta: dict) -> None:
    alvo.enunciado = pergunta["enunciado"]
    (
        alvo.alternativa_1,
        alvo.alternativa_2,
        alvo.alternativa_3,
        alvo.alternativa_4,
    ) = pergunta["alternativas"]
    alvo.alternativa_correta = pergunta["alternativa_correta"]


def acrescentar_pergunta_do_desbloqueio(
    sessao: Session,
    *,
    operador: Persona,
    missao: Missao | None,
    pergunta: dict,
) -> PerguntaDoDesbloqueio:
    """Acrescenta **uma** pergunta ao quiz sem tocar nas demais, ao fim da
    ordem vigente (`RF-09-120`, design — decisão 3). Grava completa ou não
    grava (`RN-09-44`). A pergunta nasce com id próprio, e é por ele que a
    imagem dela passa a ser endereçável, sem declaração prévia do desafio
    inteiro (`RF-09-119`)."""
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    conferir_posse_da_trilha(sessao.get(Trilha, missao.trilha_id), operador)
    conferir_pergunta_do_quiz(pergunta, campo="pergunta")

    if missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.pratico:
        raise ErroDeValidacao(
            mensagem=(
                "O desafio desta missão é prático. Declare-a como quiz antes de acrescentar "
                "perguntas."
            ),
            campo="pergunta",
        )

    vigentes = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    nova = PerguntaDoDesbloqueio(
        missao_id=missao.id,
        ordem=max((vigente.ordem for vigente in vigentes), default=0) + 1,
    )
    _aplicar_pergunta(nova, pergunta)
    sessao.add(nova)

    # Acrescentar pergunta a missão que ainda não tem desafio declarado a
    # faz quiz: é o mesmo efeito da declaração, pela unidade menor.
    if missao.tipo_do_desafio_de_desbloqueio is None:
        missao.tipo_do_desafio_de_desbloqueio = TipoDeDesafioDeDesbloqueio.quiz
        missao.desafio_de_desbloqueio_enunciado = None

    sessao.flush()
    return nova


def corrigir_pergunta_do_desbloqueio(
    sessao: Session,
    *,
    operador: Persona,
    pergunta: PerguntaDoDesbloqueio | None,
    conteudo: dict,
) -> PerguntaDoDesbloqueio:
    """Corrige **uma** pergunta sem tocar nas demais nem na ordem delas
    (`RF-09-120`). Ninguém tendo respondido, a linha é atualizada no lugar e
    o id, a ordem e a imagem seguem os mesmos — é o caminho comum da
    autoria, e é o que mantém estável a referência da imagem, que nasce do
    id. Havendo resposta gravada, a vigente é **carimbada** e uma linha nova
    nasce na mesma ordem, com as três colunas da imagem copiadas: `RN-05-47`
    protege a tentativa registrada, e onde não há tentativa não há o que
    proteger (design — decisão 2)."""
    alvo = _conferir_posse_da_pergunta(sessao, pergunta, operador)
    conferir_pergunta_do_quiz(conteudo, campo="pergunta")

    if not _alguma_submissao_respondeu(sessao, alvo):
        _aplicar_pergunta(alvo, conteudo)
        sessao.flush()
        return alvo

    # O carimbo precede a inserção, com o `flush` entre os dois, para que o
    # índice parcial de (missão, ordem) nunca veja duas gerações vigentes.
    ordem = alvo.ordem
    alvo.substituida_em = agora()
    sessao.flush()

    corrigida = PerguntaDoDesbloqueio(
        missao_id=alvo.missao_id,
        ordem=ordem,
        imagem_referencia=alvo.imagem_referencia,
        imagem_tipo=alvo.imagem_tipo,
        imagem_tamanho=alvo.imagem_tamanho,
    )
    _aplicar_pergunta(corrigida, conteudo)
    sessao.add(corrigida)
    sessao.flush()
    return corrigida


def remover_pergunta_do_desbloqueio(
    sessao: Session, *, operador: Persona, pergunta: PerguntaDoDesbloqueio | None
) -> None:
    """Tira **uma** pergunta do quiz carimbando-a: ela sai da leitura e
    permanece guardada, para a submissão que a aponta (`RN-05-47`). Não
    renumera as restantes — a ordem é sequência, não índice, e reescrever
    linha que o ato não pediu para mudar contraria o próprio requisito
    (`RF-09-120`, design — decisão 3). Remover a **única** pergunta é
    recusado: quiz sem nenhuma pergunta é o estado que `RN-09-43` já recusa
    na declaração (design — decisão 5)."""
    alvo = _conferir_posse_da_pergunta(sessao, pergunta, operador)

    if len(perguntas_do_desbloqueio(sessao, missao_id=alvo.missao_id)) <= 1:
        raise ErroDeValidacao(
            mensagem=(
                "O quiz precisa de ao menos uma pergunta. Acrescente outra antes de remover esta."
            ),
            campo="pergunta",
        )

    alvo.substituida_em = agora()
    sessao.flush()


# A imagem da pergunta tem lista e teto próprios: só os **formatos de
# imagem** da lista fechada do `RF-09-115`, e 1 MB — teto menor que o do
# conteúdo da missão porque o quiz é lido no aparelho do Guerreiro(a),
# muitas vezes em rede fraca (documento 03 §11).
FORMATOS_DA_IMAGEM_DA_PERGUNTA = frozenset({"image/jpeg", "image/png", "image/webp"})
TAMANHO_TETO_DA_IMAGEM_DA_PERGUNTA = 1024 * 1024


def _formatar_mb(tamanho_em_bytes: int) -> str:
    return f"{tamanho_em_bytes / (1024 * 1024):.1f} MB".replace(".0 MB", " MB")


def _conferir_autoria_da_pergunta(
    sessao: Session, pergunta: PerguntaDoDesbloqueio, operador: Persona
) -> None:
    """A imagem é da pergunta, e a pergunta é da missão do Mestre autor:
    autoria estrita, o mesmo 403 que o conteúdo da missão já usa
    (`RF-09-119`)."""
    missao = sessao.get(Missao, pergunta.missao_id)
    conferir_autoria_estrita_da_trilha(sessao.get(Trilha, missao.trilha_id), operador)


def abrir_envio_da_imagem_da_pergunta(
    sessao: Session,
    pergunta: PerguntaDoDesbloqueio | None,
    *,
    operador: Persona,
    tipo_mime: str | None,
    tamanho_declarado: int | None,
    armazenamento: PortaDeArmazenamento,
    origem: str | None = None,
) -> str:
    """Confere autoria, formato e teto **antes** de abrir a sessão — a
    recusa acontece sem nenhum byte enviado, como em `conteudos.regra`
    (`RF-09-119`, `RF-09-115`). `origem` é repassada ao armazenamento, que
    decide se aceita o envio vindo dela (design — decisão 3)."""
    if pergunta is None:
        raise NaoEncontrado(mensagem="Pergunta não encontrada.")
    _conferir_autoria_da_pergunta(sessao, pergunta, operador)

    if tipo_mime not in FORMATOS_DA_IMAGEM_DA_PERGUNTA:
        raise ErroDeValidacao(
            mensagem=(
                f"Formato '{tipo_mime}' não aceito na imagem da pergunta. A lista aceita é "
                "JPG, PNG e WebP."
            ),
            campo="tipo_mime",
        )
    if tamanho_declarado is None or tamanho_declarado <= 0:
        raise ErroDeValidacao(
            mensagem="Envio exige o tamanho declarado do arquivo.", campo="tamanho_declarado"
        )
    if tamanho_declarado > TAMANHO_TETO_DA_IMAGEM_DA_PERGUNTA:
        raise ArquivoAcimaDoTeto(
            mensagem=(
                f"A imagem tem {_formatar_mb(tamanho_declarado)} e o limite da imagem da "
                f"pergunta é {_formatar_mb(TAMANHO_TETO_DA_IMAGEM_DA_PERGUNTA)}."
            )
        )

    return armazenamento.abrir_sessao(
        referencia=referencia_da_imagem_da_pergunta(pergunta),
        tipo_mime=tipo_mime,
        tamanho_declarado=tamanho_declarado,
        origem=origem,
    )


def confirmar_envio_da_imagem_da_pergunta(
    sessao: Session,
    pergunta: PerguntaDoDesbloqueio | None,
    *,
    operador: Persona,
    armazenamento: PortaDeArmazenamento,
) -> PerguntaDoDesbloqueio:
    """Só grava a referência depois de o armazenamento apurar o tamanho e o
    tipo **reais**: o teto vale de novo aqui, porque o recebido pode
    divergir do declarado na abertura (`RF-09-119`)."""
    if pergunta is None:
        raise NaoEncontrado(mensagem="Pergunta não encontrada.")
    _conferir_autoria_da_pergunta(sessao, pergunta, operador)

    referencia = referencia_da_imagem_da_pergunta(pergunta)
    envio = armazenamento.consultar_envio(referencia=referencia)
    if envio is None:
        raise ErroDeValidacao(mensagem="O envio ainda não foi concluído.", campo="imagem")
    if envio.tamanho > TAMANHO_TETO_DA_IMAGEM_DA_PERGUNTA:
        raise ArquivoAcimaDoTeto(
            mensagem=(
                f"A imagem enviada tem {_formatar_mb(envio.tamanho)} e o limite da imagem da "
                f"pergunta é {_formatar_mb(TAMANHO_TETO_DA_IMAGEM_DA_PERGUNTA)}."
            )
        )

    pergunta.imagem_referencia = referencia
    pergunta.imagem_tipo = envio.tipo_mime
    pergunta.imagem_tamanho = envio.tamanho
    sessao.flush()
    return pergunta


@dataclass(frozen=True)
class ImagemDaPergunta:
    """Os bytes servidos pelo núcleo e o tipo declarado no envio."""

    bytes_da_imagem: bytes
    tipo_mime: str


def ler_imagem_da_pergunta(
    sessao: Session,
    pergunta: PerguntaDoDesbloqueio | None,
    *,
    operador: Persona,
    armazenamento: PortaDeArmazenamento,
) -> ImagemDaPergunta:
    """O primeiro caminho de saída de bytes do núcleo, e por isso de
    autorização estrita: serve ao **Mestre autor** da trilha e ao
    **Guerreiro(a) inscrito** nela — os mesmos que já leem a pergunta —, e a
    ninguém mais (`RF-09-119`, `RF-05-89`, design — decisão 5). Servir 1 MB
    pelo núcleo é aceitável; o que a arquitetura mantém fora dele é o
    **envio**.
    """
    if pergunta is None:
        raise NaoEncontrado(mensagem="Pergunta não encontrada.")
    missao = sessao.get(Missao, pergunta.missao_id)
    trilha = sessao.get(Trilha, missao.trilha_id)
    if trilha.autor_id != operador.id:
        inscrito = (
            sessao.query(InscricaoNaTrilha)
            .filter_by(guerreiro_id=operador.id, trilha_id=trilha.id)
            .first()
            is not None
        )
        if not inscrito:
            raise PermissaoNegada(
                mensagem="A imagem da pergunta é servida ao Mestre autor e a quem está "
                "inscrito na trilha."
            )

    if pergunta.imagem_referencia is None:
        raise NaoEncontrado(mensagem="Esta pergunta não tem imagem.")
    return ImagemDaPergunta(
        bytes_da_imagem=armazenamento.ler(referencia=pergunta.imagem_referencia),
        tipo_mime=pergunta.imagem_tipo or "application/octet-stream",
    )


@dataclass
class ResultadoDaSubmissaoDoDesbloqueio:
    """`aprovado`: `True` desbloqueou na hora (quiz que alcançou o corte,
    sondagem respondida ou prático já julgado antes), `None` aguardando o
    Mestre julgar o prático, `False` não alcançou o corte do quiz — submete
    de novo sem limite (`RN-05-20`). `acertos` e `total` são a devolutiva do
    quiz (`RF-05-89`); no prático nascem em zero."""

    aprovado: bool | None
    desbloqueio: DesbloqueioDaMissao | None
    acertos: int = 0
    total: int = 0


def submeter_desafio_de_desbloqueio(
    sessao: Session,
    *,
    guerreiro: Persona,
    missao: Missao | None,
    respostas: list[dict] | None = None,
    comprovacao: str | None = None,
    entrega_presencial: bool = False,
) -> ResultadoDaSubmissaoDoDesbloqueio:
    """Só o Guerreiro(a) inscrito na trilha submete — sem inscrição, 422
    (`RN-05-20`, `RN-05-06`, documento 11 §2.2). No quiz, a submissão traz a
    resposta de todas as perguntas de uma vez e o núcleo afere pela
    proporção de acertos: passa quem acerta ao menos 60% (`RF-05-89`,
    `RN-05-45`). A **missão de sondagem** é exceção — abre a trilha ao ser
    respondida, acertando ou não (`RN-05-46`), porque mede de onde o
    Guerreiro(a) parte. No prático, grava a declaração do Guerreiro(a),
    aguardando o Mestre autor julgar, e com ela a **comprovação** na forma que
    o Mestre autor aceitou (`RF-05-91`) ou a escolha de **entregar ao Mestre no
    encontro** (`RN-05-51`). **Toda tentativa fica gravada**, a que passa e a
    que não passa (`RN-05-47`). A submissão nunca credita ponto: no quiz não há
    crédito algum, e no prático quem credita é o **julgamento** do Mestre autor
    (`RF-09-135`).
    """
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    if missao.tipo_do_desafio_de_desbloqueio is None:
        raise ErroDeValidacao(
            mensagem="Esta missão não tem desafio de desbloqueio declarado.", campo="missao_id"
        )
    _conferir_inscricao(sessao, guerreiro_id=guerreiro.id, trilha_id=missao.trilha_id)

    existente = (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .first()
    )
    if (
        existente is not None
        and missao.e_sondagem
        and missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.quiz
    ):
        # A sondagem respondida **se refaz**: cada realização é tentativa nova,
        # gravada com o placar, e vale a mais recente pelo instante. O
        # desbloqueio segue um só, e nada credita nem define nível
        # (`RF-05-101`, `RN-05-56`, `RN-05-47`).
        acertos, total = _aferir_quiz(
            sessao, guerreiro=guerreiro, missao=missao, respostas=respostas
        )
        return ResultadoDaSubmissaoDoDesbloqueio(
            aprovado=True, desbloqueio=existente, acertos=acertos, total=total
        )
    if existente is not None:
        # Enquanto o Mestre não julgou, entregar de novo **substitui** o que
        # estava, em vez de criar segundo registro — como a criação original já
        # faz antes da validação (`RN-05-52`). Julgado que **não cumpriu**,
        # entregar de novo **reabre a mesma linha**: os quatro campos do
        # julgamento voltam a nulo e ela torna a aguardar o Mestre, sem limite
        # de vezes e sem segundo registro do par (`RN-09-54`, design —
        # decisão 2). Julgado que cumpriu, a resposta segue sendo a situação
        # dele, sem tocar no que está gravado.
        if (
            missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.pratico
            and existente.cumpriu is not True
        ):
            texto, presencial = _conferir_comprovacao_do_pratico(
                missao, comprovacao=comprovacao, entrega_presencial=entrega_presencial
            )
            _substituir_comprovacao(existente, texto=texto, presencial=presencial)
            _reabrir_julgamento(existente)
            sessao.flush()
        return ResultadoDaSubmissaoDoDesbloqueio(aprovado=existente.cumpriu, desbloqueio=existente)

    if missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.quiz:
        # No quiz o corte de acertos é o critério, e o núcleo o afere sozinho:
        # não há comprovação a entregar nem a julgar (`RF-05-91`).
        if comprovacao is not None or entrega_presencial:
            raise ErroDeValidacao(
                mensagem="O quiz não recebe comprovação: o critério dele é o corte de acertos.",
                campo="comprovacao",
            )
        acertos, total = _aferir_quiz(
            sessao, guerreiro=guerreiro, missao=missao, respostas=respostas
        )
        # A sondagem abre ao ser respondida: o corte não se aplica a ela
        # (`RN-05-46`, design — decisão 4).
        passou = missao.e_sondagem or _passou_no_quiz(acertos, total)
        if not passou:
            return ResultadoDaSubmissaoDoDesbloqueio(
                aprovado=False, desbloqueio=None, acertos=acertos, total=total
            )
        desbloqueio = DesbloqueioDaMissao(
            guerreiro_id=guerreiro.id, missao_id=missao.id, cumpriu=True
        )
        sessao.add(desbloqueio)
        sessao.flush()
        return ResultadoDaSubmissaoDoDesbloqueio(
            aprovado=True, desbloqueio=desbloqueio, acertos=acertos, total=total
        )

    texto, presencial = _conferir_comprovacao_do_pratico(
        missao, comprovacao=comprovacao, entrega_presencial=entrega_presencial
    )
    _gravar_submissao(
        sessao,
        guerreiro_id=guerreiro.id,
        missao_id=missao.id,
        perguntas=[],
        escolhas={},
        faladas={},
        acertos=0,
    )
    desbloqueio = DesbloqueioDaMissao(
        guerreiro_id=guerreiro.id,
        missao_id=missao.id,
        cumpriu=None,
        comprovacao=texto,
        entrega_presencial=presencial,
    )
    sessao.add(desbloqueio)
    sessao.flush()
    return ResultadoDaSubmissaoDoDesbloqueio(aprovado=None, desbloqueio=desbloqueio)


def _aferir_quiz(
    sessao: Session, *, guerreiro: Persona, missao: Missao, respostas: list[dict] | None
) -> tuple[int, int]:
    """Confere as respostas do quiz, grava a tentativa com a resposta de cada
    pergunta e devolve os acertos e o total (`RF-05-89`, `RN-05-47`)."""
    perguntas = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    if not perguntas:
        raise ErroDeValidacao(
            mensagem="Esta missão não tem desafio de desbloqueio declarado.",
            campo="missao_id",
        )
    escolhas, faladas = _conferir_respostas_do_quiz(
        respostas, perguntas, e_sondagem=missao.e_sondagem
    )
    acertos = sum(
        1 for pergunta in perguntas if escolhas[pergunta.id] == pergunta.alternativa_correta
    )
    _gravar_submissao(
        sessao,
        guerreiro_id=guerreiro.id,
        missao_id=missao.id,
        perguntas=perguntas,
        escolhas=escolhas,
        faladas=faladas,
        acertos=acertos,
    )
    return acertos, len(perguntas)


_FORMAS_DE_COMPROVACAO_EM_TEXTO = frozenset(
    {TipoDeProducaoDaCriacaoOriginal.texto, TipoDeProducaoDaCriacaoOriginal.link_externo}
)


def _conferir_comprovacao_do_pratico(
    missao: Missao, *, comprovacao: str | None, entrega_presencial: bool
) -> tuple[str | None, bool]:
    """Confere o que o Guerreiro(a) entregou contra a forma que o Mestre autor
    declarou aceitar — a forma vem da **missão**, nunca do corpo da submissão,
    porque `RN-09-50` a fez ser uma só justamente para não haver escolha na
    ponta (`RF-05-91`, design — decisão 2).

    Exatamente um entre a comprovação e a entrega presencial é preenchido
    (`RN-05-51`, design — decisão 3). Na forma **texto** ou **link externo** o
    corpo vem na própria declaração; nas quatro formas de **mídia** a
    declaração nasce sem arquivo e o recebe pela sessão de envio, como a criação
    original (design — decisão 4), e por isso mandar corpo nelas é 422.

    Prático declarado **antes** desta regra não tem forma aceita: a declaração
    segue valendo sem comprovação, porque não há forma contra a qual exigi-la
    (design — decisão 7).
    """
    texto = comprovacao.strip() if comprovacao is not None else None

    if entrega_presencial:
        if texto:
            raise ErroDeValidacao(
                mensagem="Escolha entregar pelo aparelho ou entregar ao Mestre no encontro, "
                "não as duas.",
                campo="entrega_presencial",
            )
        return None, True

    forma = missao.desafio_pratico_forma_de_comprovacao
    if forma is None:
        if texto:
            raise ErroDeValidacao(
                mensagem="Este desafio prático ainda não declarou que forma de comprovação "
                "aceita; o Mestre autor precisa declará-la.",
                campo="comprovacao",
            )
        return None, False

    if forma in _FORMAS_DE_COMPROVACAO_EM_TEXTO:
        if not texto:
            raise ErroDeValidacao(
                mensagem=(
                    "Este desafio aceita comprovação em texto e exige o que você escreveu."
                    if forma == TipoDeProducaoDaCriacaoOriginal.texto
                    else "Este desafio aceita comprovação em link e exige o endereço."
                ),
                campo="comprovacao",
            )
        return texto, False

    if texto:
        raise ErroDeValidacao(
            mensagem=f"Este desafio aceita comprovação em {forma.value}, que vai pelo envio do "
            "arquivo, não escrita na declaração.",
            campo="comprovacao",
        )
    return None, False


def _substituir_comprovacao(
    desbloqueio: DesbloqueioDaMissao, *, texto: str | None, presencial: bool
) -> None:
    """A entrega nova apaga a anterior inteira — o corpo e a mídia —, para que
    não sobre arquivo de uma entrega que o Mestre não vai mais julgar
    (`RN-05-52`)."""
    desbloqueio.comprovacao = texto
    desbloqueio.entrega_presencial = presencial
    desbloqueio.comprovacao_referencia = None
    desbloqueio.comprovacao_tamanho = None
    desbloqueio.comprovacao_tipo_do_arquivo = None


def _referencia_da_comprovacao(desbloqueio: DesbloqueioDaMissao) -> str:
    return f"desbloqueios-praticos/{desbloqueio.id}/comprovacao"


def _reabrir_julgamento(desbloqueio: DesbloqueioDaMissao) -> None:
    """A declaração recusada volta a aguardar o Mestre: os quatro campos do
    julgamento voltam a nulo, de modo que o veredito e o motivo anteriores não
    sobrevivam à entrega nova — ela é outra entrega, e julgá-la é outro ato
    (`RN-09-54`).

    `momento` também é refeito, e não por simetria: a **cadência de retomada**
    conta o prazo dele (`RF-05-79`). Antes desta fatia a linha recusada era
    apagada e a declaração seguinte nascia com momento novo; mantendo o da
    primeira entrega, o Guerreiro(a) recusado que entrega de novo semanas
    depois teria as retomadas de 2, 7 e 21 dias já vencidas no instante em que
    o Mestre aprova. O prazo corre da entrega que foi aceita."""
    desbloqueio.cumpriu = None
    desbloqueio.publicavel = None
    desbloqueio.motivo_do_julgamento = None
    desbloqueio.julgado_por_id = None
    desbloqueio.julgado_em = None
    desbloqueio.momento = agora()


def _conferir_envio_da_comprovacao(
    sessao: Session, desbloqueio: DesbloqueioDaMissao | None, operador: Persona
) -> DesbloqueioDaMissao:
    """Quem envia é quem declarou, e só enquanto o Mestre não julgou: julgada,
    a entrega está encerrada, e a recusada só volta a receber arquivo depois de
    o Guerreiro(a) **entregar de novo**, que é o que reabre a declaração
    (`RF-05-91`, `RN-05-52`, `RN-09-54`)."""
    if desbloqueio is None:
        raise NaoEncontrado(mensagem="Declaração de desafio prático não encontrada.")
    if desbloqueio.guerreiro_id != operador.id:
        raise PermissaoNegada(
            mensagem="A comprovação é enviada por quem declarou que cumpriu o desafio."
        )
    if desbloqueio.cumpriu is not None:
        raise ErroDeValidacao(
            mensagem="Esta declaração já foi julgada; para trocar a comprovação, declare "
            "que cumpriu de novo.",
            campo="comprovacao",
        )
    if desbloqueio.entrega_presencial:
        raise ErroDeValidacao(
            mensagem="Esta declaração escolheu a entrega ao Mestre no encontro; não há arquivo "
            "a enviar.",
            campo="comprovacao",
        )
    missao = sessao.get(Missao, desbloqueio.missao_id)
    forma = missao.desafio_pratico_forma_de_comprovacao
    if forma is None or forma in _FORMAS_DE_COMPROVACAO_EM_TEXTO:
        raise ErroDeValidacao(
            mensagem="A comprovação deste desafio não é arquivo.", campo="comprovacao"
        )
    return desbloqueio


def abrir_envio_da_comprovacao(
    sessao: Session,
    desbloqueio: DesbloqueioDaMissao | None,
    *,
    operador: Persona,
    tipo_mime: str | None,
    tamanho_declarado: int | None,
    armazenamento: PortaDeArmazenamento,
    origem: str | None = None,
) -> str:
    """Espelha `criacoes_originais.regra.abrir_envio_da_criacao`: confere quem
    envia, o formato e o teto antes de abrir a sessão, e repassa a `origem` ao
    armazenamento, que é outra origem e só aceita sabendo de onde vem
    (`RF-05-91`, `RF-09-19`, design — decisão 4)."""
    desbloqueio = _conferir_envio_da_comprovacao(sessao, desbloqueio, operador)
    missao = sessao.get(Missao, desbloqueio.missao_id)

    if tipo_mime not in FORMATOS_DE_ENVIO_ACEITOS:
        raise ErroDeValidacao(
            mensagem=f"Formato '{tipo_mime}' não aceito. A lista aceita é "
            f"{FORMATOS_ACEITOS_EM_TEXTO}.",
            campo="tipo_mime",
        )
    if tamanho_declarado is None or tamanho_declarado <= 0:
        raise ErroDeValidacao(
            mensagem="Envio exige o tamanho declarado do arquivo.", campo="tamanho_declarado"
        )

    teto = teto_do_tipo_de_producao(missao.desafio_pratico_forma_de_comprovacao)
    if tamanho_declarado > teto:
        raise ArquivoAcimaDoTeto(
            mensagem=f"O arquivo tem {formatar_mb(tamanho_declarado)} e o limite para este tipo "
            f"de comprovação é {formatar_mb(teto)}."
        )

    return armazenamento.abrir_sessao(
        referencia=_referencia_da_comprovacao(desbloqueio),
        tipo_mime=tipo_mime,
        tamanho_declarado=tamanho_declarado,
        origem=origem,
    )


def confirmar_envio_da_comprovacao(
    sessao: Session,
    desbloqueio: DesbloqueioDaMissao | None,
    *,
    operador: Persona,
    armazenamento: PortaDeArmazenamento,
) -> DesbloqueioDaMissao:
    """Só grava a referência depois de o armazenamento confirmar o tamanho
    real: até aqui a comprovação não serve bytes (`RF-05-91`, design —
    decisão 4)."""
    desbloqueio = _conferir_envio_da_comprovacao(sessao, desbloqueio, operador)
    missao = sessao.get(Missao, desbloqueio.missao_id)

    envio = armazenamento.consultar_envio(referencia=_referencia_da_comprovacao(desbloqueio))
    if envio is None:
        raise ErroDeValidacao(mensagem="O envio ainda não foi concluído.", campo="arquivo")

    teto = teto_do_tipo_de_producao(missao.desafio_pratico_forma_de_comprovacao)
    if envio.tamanho > teto:
        raise ArquivoAcimaDoTeto(
            mensagem=f"O arquivo enviado tem {formatar_mb(envio.tamanho)} e o limite para este "
            f"tipo de comprovação é {formatar_mb(teto)}."
        )

    desbloqueio.comprovacao_referencia = _referencia_da_comprovacao(desbloqueio)
    desbloqueio.comprovacao_tamanho = envio.tamanho
    desbloqueio.comprovacao_tipo_do_arquivo = envio.tipo_mime
    sessao.flush()
    return desbloqueio


@dataclass
class ArquivoDaComprovacao:
    bytes_do_arquivo: bytes
    tipo_mime: str


def ler_arquivo_da_comprovacao(
    sessao: Session,
    desbloqueio: DesbloqueioDaMissao | None,
    *,
    operador: Persona,
    armazenamento: PortaDeArmazenamento,
) -> ArquivoDaComprovacao:
    """Os bytes vão a **quem entregou** e ao **Mestre autor** da trilha: a ele
    porque é quem julga, a ela porque foi avisada de que a mídia fica guardada
    (`RF-05-93`, decisão do fundador de 2026-11-04). Quem grava entrega também
    quem lê — foi o defeito *write-only* da criação original que ensinou
    (`RF-01-78`)."""
    if desbloqueio is None:
        raise NaoEncontrado(mensagem="Declaração de desafio prático não encontrada.")
    missao = sessao.get(Missao, desbloqueio.missao_id)
    trilha = sessao.get(Trilha, missao.trilha_id)
    if desbloqueio.guerreiro_id != operador.id and trilha.autor_id != operador.id:
        raise PermissaoNegada(
            mensagem="A comprovação é servida a quem a entregou e ao Mestre autor da trilha."
        )
    if desbloqueio.comprovacao_referencia is None:
        raise NaoEncontrado(mensagem="Esta declaração não tem arquivo de comprovação.")
    return ArquivoDaComprovacao(
        bytes_do_arquivo=armazenamento.ler(referencia=desbloqueio.comprovacao_referencia),
        tipo_mime=desbloqueio.comprovacao_tipo_do_arquivo or "application/octet-stream",
    )


def _conferir_respostas_do_quiz(
    respostas: list[dict] | None,
    perguntas: list[PerguntaDoDesbloqueio],
    *,
    e_sondagem: bool,
) -> tuple[dict[uuid.UUID, int | None], dict[uuid.UUID, str]]:
    """A submissão traz a resposta de todas as perguntas de uma vez
    (`RF-05-89`): resposta faltando, repetida ou apontando pergunta de outra
    missão é 422. Na sondagem, e só nela, a resposta pode vir **falada** —
    a transcrição sem alternativa —, quando a fala não se ligou a nenhuma
    (`RF-05-98`, `RN-05-55`)."""
    escolhas: dict[uuid.UUID, int | None] = {}
    faladas: dict[uuid.UUID, str] = {}
    esperadas = {pergunta.id for pergunta in perguntas}
    for resposta in respostas or []:
        pergunta_id = resposta.get("pergunta_id")
        if pergunta_id not in esperadas:
            raise ErroDeValidacao(
                mensagem="Resposta de pergunta que não é deste desafio.", campo="respostas"
            )
        if pergunta_id in escolhas:
            raise ErroDeValidacao(
                mensagem="Cada pergunta aceita uma resposta só.", campo="respostas"
            )
        escolhida = resposta.get("alternativa_escolhida")
        falada = resposta.get("resposta_falada")
        if falada is not None:
            if escolhida is not None:
                raise ErroDeValidacao(
                    mensagem="Cada resposta tem uma forma só: alternativa ou fala.",
                    campo="respostas",
                )
            if not e_sondagem:
                raise ErroDeValidacao(
                    mensagem="Só a sondagem aceita resposta falada sem alternativa.",
                    campo="respostas",
                )
            if len(falada) > LIMITE_DA_RESPOSTA_FALADA:
                raise ErroDeValidacao(
                    mensagem="A resposta falada passou do tamanho aceito.", campo="respostas"
                )
            escolhas[pergunta_id] = None
            faladas[pergunta_id] = falada
            continue
        if escolhida is None or not (
            PRIMEIRA_ALTERNATIVA_DO_DESBLOQUEIO <= escolhida <= TOTAL_DE_ALTERNATIVAS_DO_DESBLOQUEIO
        ):
            raise ErroDeValidacao(
                mensagem="Alternativa escolhida fora das quatro da pergunta.", campo="respostas"
            )
        escolhas[pergunta_id] = escolhida
    if len(escolhas) != len(esperadas):
        raise ErroDeValidacao(
            mensagem="Responda a todas as perguntas do quiz antes de enviar.", campo="respostas"
        )
    return escolhas, faladas


def _gravar_submissao(
    sessao: Session,
    *,
    guerreiro_id: uuid.UUID,
    missao_id: uuid.UUID,
    perguntas: list[PerguntaDoDesbloqueio],
    escolhas: dict[uuid.UUID, int | None],
    faladas: dict[uuid.UUID, str],
    acertos: int,
) -> SubmissaoDoDesbloqueio:
    """Acrescenta a tentativa ao histórico, sem tocar nas anteriores
    (`RN-05-47`)."""
    submissao = SubmissaoDoDesbloqueio(
        guerreiro_id=guerreiro_id, missao_id=missao_id, acertos=acertos, total=len(perguntas)
    )
    sessao.add(submissao)
    sessao.flush()
    for pergunta in perguntas:
        sessao.add(
            RespostaDaSubmissao(
                submissao_id=submissao.id,
                pergunta_id=pergunta.id,
                alternativa_escolhida=escolhas[pergunta.id],
                resposta_falada=faladas.get(pergunta.id),
                acertou=escolhas[pergunta.id] == pergunta.alternativa_correta,
            )
        )
    sessao.flush()
    return submissao


def listar_desbloqueios_praticos_pendentes(
    sessao: Session, *, operador: Persona
) -> list[DesbloqueioDaMissao]:
    """Declarações de desafio prático ainda não julgadas, só das trilhas do
    Mestre autor (`RF-09-26`, `RF-09-117`)."""
    return (
        sessao.query(DesbloqueioDaMissao)
        .join(Missao, Missao.id == DesbloqueioDaMissao.missao_id)
        .join(Trilha, Trilha.id == Missao.trilha_id)
        .filter(
            Trilha.autor_id == operador.id,
            Missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.pratico,
            DesbloqueioDaMissao.cumpriu.is_(None),
        )
        .all()
    )


def julgar_desafio_pratico(
    sessao: Session,
    *,
    operador: Persona,
    desbloqueio: DesbloqueioDaMissao | None,
    cumpriu: bool,
    publicavel: bool = False,
    motivo: str | None = None,
) -> DesbloqueioDaMissao:
    """Só o Mestre autor da trilha julga (`RF-09-117`), e o julgamento tem
    **dois vereditos** (`RF-09-133`): `cumpriu` abre a missão seguinte e
    credita os 5 pontos regulares do documento 11 §5 (`RF-09-135`), e
    `publicavel` diz se aquela entrega vai à vitrine pública — nenhum deriva
    do outro, e cumprir sem ser publicável é julgamento válido.

    O **motivo** é exigido em todo veredito negativo (`RN-09-53`), e é por
    causa dele que a reprovação **não apaga** a linha: ela permanece com o
    veredito e o motivo, para que o Guerreiro(a) leia por que não passou, e
    entregar de novo reabre a mesma declaração (`RN-09-54`). Nada aqui é
    reprovação persistida — é a devolutiva do Mestre, como a criação original
    devolvida (`RN-05-20`).

    Julgar de novo o que já foi julgado é recusado, o que também é a
    idempotência do crédito: a linha legada, julgada antes desta regra
    (`julgado_em` nulo), não se rejulga e não recebe crédito retroativo
    (`RN-09-55`)."""
    if desbloqueio is None:
        raise NaoEncontrado(mensagem="Declaração de desafio prático não encontrada.")
    missao = sessao.get(Missao, desbloqueio.missao_id)
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)
    if desbloqueio.cumpriu is not None:
        raise ErroDeValidacao(mensagem="Esta declaração já foi julgada.", campo="cumpriu")

    _conferir_vereditos_do_pratico(desbloqueio, cumpriu=cumpriu, publicavel=publicavel)
    motivo_limpo = (motivo or "").strip() or None
    if motivo_limpo is None and _nega_algo_ao_guerreiro(
        desbloqueio, cumpriu=cumpriu, publicavel=publicavel
    ):
        raise ErroDeValidacao(
            mensagem="Julgamento que nega algo exige o motivo, em linguagem simples: é o que o "
            "Guerreiro(a) lê.",
            campo="motivo",
        )

    desbloqueio.cumpriu = cumpriu
    desbloqueio.publicavel = publicavel
    desbloqueio.motivo_do_julgamento = motivo_limpo
    desbloqueio.julgado_por_id = operador.id
    desbloqueio.julgado_em = agora()
    sessao.flush()

    if cumpriu:
        creditar_pontuacao_do_desbloqueio_pratico(
            sessao, guerreiro_id=desbloqueio.guerreiro_id, trilha_id=trilha.id
        )
    return desbloqueio


def _tem_comprovacao_gravada(desbloqueio: DesbloqueioDaMissao) -> bool:
    """Há o que publicar: o corpo escrito ou o endereço, ou o arquivo cujo
    envio **concluiu** — a entrega presencial nasce sem mídia, e a declaração em
    forma de mídia só tem bytes depois do envio (`RN-09-52`)."""
    return desbloqueio.comprovacao is not None or (
        desbloqueio.comprovacao_referencia is not None
        and desbloqueio.comprovacao_tipo_do_arquivo is not None
    )


def _conferir_vereditos_do_pratico(
    desbloqueio: DesbloqueioDaMissao, *, cumpriu: bool, publicavel: bool
) -> None:
    """`publicavel` só é aceito junto de `cumpriu` e só sobre declaração com
    **comprovação gravada**: o que o Mestre recusou não vai a público, e a
    entrega presencial nasce sem mídia e não tem o que publicar (`RN-09-52`,
    `RN-05-51`)."""
    if not publicavel:
        return
    if not cumpriu:
        raise ErroDeValidacao(
            mensagem="Só a entrega julgada como cumprida vai à vitrine.", campo="publicavel"
        )
    if not _tem_comprovacao_gravada(desbloqueio):
        raise ErroDeValidacao(
            mensagem="Esta declaração não tem comprovação a publicar.", campo="publicavel"
        )


def _nega_algo_ao_guerreiro(
    desbloqueio: DesbloqueioDaMissao, *, cumpriu: bool, publicavel: bool
) -> bool:
    """O motivo é exigido quando o julgamento **nega algo ao Guerreiro(a)**
    (`RN-09-53`): não ter cumprido, ou ter cumprido e não ir à vitrine.

    Não publicar só é negativa quando publicar **era possível** — havia
    comprovação gravada. Na entrega presencial, e na declaração cujo envio não
    concluiu, não há o que publicar, e exigir que o Mestre explique uma recusa
    que ele não escolheu seria cobrar motivo de um fato estrutural."""
    if not cumpriu:
        return True
    return not publicavel and _tem_comprovacao_gravada(desbloqueio)


@dataclass
class MissaoNoPercurso:
    missao: Missao
    desbloqueada: bool
    e_proxima: bool
    aguardando_mestre: bool
    motivo_do_bloqueio: str | None


def derivar_percurso(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID
) -> list[MissaoNoPercurso]:
    """Deriva o percurso na leitura, a partir da posição — sem tabela de
    estado por missão (design — decisão 2). Só o próprio Guerreiro(a)
    inscrito tem o que ler (`RF-05-08`, `RF-05-10`, `RN-05-21`)."""
    _conferir_inscricao(sessao, guerreiro_id=guerreiro_id, trilha_id=trilha_id)

    missoes = sessao.query(Missao).filter_by(trilha_id=trilha_id).order_by(Missao.posicao).all()
    desbloqueios = {
        d.missao_id: d
        for d in sessao.query(DesbloqueioDaMissao)
        .filter(
            DesbloqueioDaMissao.guerreiro_id == guerreiro_id,
            DesbloqueioDaMissao.missao_id.in_([missao.id for missao in missoes]),
        )
        .all()
    }
    proxima = next(
        (
            missao
            for missao in missoes
            if desbloqueios.get(missao.id) is None or desbloqueios[missao.id].cumpriu is not True
        ),
        None,
    )

    resultado = []
    for missao in missoes:
        desbloqueio = desbloqueios.get(missao.id)
        desbloqueada = desbloqueio is not None and desbloqueio.cumpriu is True
        aguardando_mestre = desbloqueio is not None and desbloqueio.cumpriu is None
        e_proxima = proxima is not None and missao.id == proxima.id
        motivo = None
        if not desbloqueada and not e_proxima:
            motivo = f'Desbloqueie "{proxima.titulo}" primeiro.' if proxima is not None else None
        resultado.append(
            MissaoNoPercurso(
                missao=missao,
                desbloqueada=desbloqueada,
                e_proxima=e_proxima,
                aguardando_mestre=aguardando_mestre,
                motivo_do_bloqueio=motivo,
            )
        )
    return resultado


def obter_proxima_missao(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID
) -> Missao | None:
    """A próxima missão do percurso do Guerreiro(a) naquela trilha, para a
    listagem de `GET /v1/eu/trilhas` (`RF-05-08`, `RF-05-17`)."""
    percurso = derivar_percurso(sessao, guerreiro_id=guerreiro_id, trilha_id=trilha_id)
    proxima = next((item for item in percurso if item.e_proxima), None)
    return proxima.missao if proxima is not None else None


def desafios_em_aberto_do_guerreiro(sessao: Session, *, guerreiro_id: uuid.UUID) -> list[Atividade]:
    """As atividades **em aberto** do Guerreiro(a): das missões que ele já
    desbloqueou, nas trilhas em que está inscrito, subtraídas as que já têm
    `Resultado` lançado para ele — "vigente" como o fundador decidiu
    (`RF-05-19`, proposal — decisão de recorte, design — decisão 1). A
    atividade avulsa fica de fora, por não ter percurso de onde derivar
    "desbloqueada" (design — decisão 2). A **carimbada** também: sem o filtro
    do carimbo, a atividade removida antes de qualquer lançamento ficaria nos
    semanais para sempre, porque a subtração aqui é só pelo Resultado
    (`RN-09-47`).
    """
    from ..resultados.modelo import Resultado

    ids_das_trilhas = {
        inscricao.trilha_id
        for inscricao in consultar_inscricoes_do_guerreiro(sessao, guerreiro_id=guerreiro_id)
    }
    if not ids_das_trilhas:
        return []

    ids_das_missoes = {
        linha[0]
        for linha in sessao.query(Missao.id)
        .join(DesbloqueioDaMissao, DesbloqueioDaMissao.missao_id == Missao.id)
        .filter(
            Missao.trilha_id.in_(ids_das_trilhas),
            DesbloqueioDaMissao.guerreiro_id == guerreiro_id,
            DesbloqueioDaMissao.cumpriu.is_(True),
        )
        .distinct()
        .all()
    }
    if not ids_das_missoes:
        return []

    ids_com_resultado = {
        linha[0]
        for linha in sessao.query(Resultado.atividade_id)
        .filter(Resultado.guerreiro_id == guerreiro_id)
        .distinct()
        .all()
    }

    atividades = atividade_vigente(
        sessao.query(Atividade).filter(Atividade.missao_id.in_(ids_das_missoes))
    ).all()
    return [atividade for atividade in atividades if atividade.id not in ids_com_resultado]


@dataclass
class RetomadaEmAberto:
    missao: Missao
    trilha: Trilha
    prazo: datetime


def retomadas_em_aberto_do_guerreiro(
    sessao: Session, *, guerreiro_id: uuid.UUID
) -> list[RetomadaEmAberto]:
    """As retomadas em aberto do Guerreiro(a): cada dia de
    `cadencia_de_retomada` de uma missão que ele desbloqueou é um
    agendamento, com prazo contado do desbloqueio aprovado dele (design —
    decisão 4). Um agendamento está em aberto quando o prazo já venceu e
    nenhuma produção individual dele naquela missão tem `registrado_em >=
    prazo` — como os prazos crescem, uma produção posterior fecha aquele
    agendamento e os anteriores, e uma produção anterior a todos (refazer
    por conta própria) não fecha nenhum (`RF-05-79`, `RF-05-80`,
    `RN-05-38`). Nenhum estado persistido: a lista nasce na leitura, como o
    percurso já nasce.
    """
    from ..producoes.modelo import ProducaoDaMissao

    desbloqueios = (
        sessao.query(DesbloqueioDaMissao, Missao)
        .join(Missao, Missao.id == DesbloqueioDaMissao.missao_id)
        .filter(
            DesbloqueioDaMissao.guerreiro_id == guerreiro_id,
            DesbloqueioDaMissao.cumpriu.is_(True),
            Missao.cadencia_de_retomada.isnot(None),
        )
        .all()
    )
    if not desbloqueios:
        return []

    momento_atual = agora()
    resultado = []
    for desbloqueio, missao in desbloqueios:
        momentos_de_producao = [
            linha[0]
            for linha in sessao.query(ProducaoDaMissao.registrado_em).filter(
                ProducaoDaMissao.guerreiro_id == guerreiro_id,
                ProducaoDaMissao.missao_id == missao.id,
            )
        ]
        trilha = sessao.get(Trilha, missao.trilha_id)
        for dias in missao.cadencia_de_retomada:
            prazo = desbloqueio.momento + timedelta(days=dias)
            if momento_atual < prazo:
                continue
            if any(momento >= prazo for momento in momentos_de_producao):
                continue
            resultado.append(RetomadaEmAberto(missao=missao, trilha=trilha, prazo=prazo))
    return resultado


@dataclass
class ProgressoDaTrilha:
    trilha: Trilha
    nivel_atual: int | None
    obrigatorias_desbloqueadas: int
    obrigatorias_totais: int
    pontos_regulares: int
    badges: list[str]


def consultar_progresso(sessao: Session, *, guerreiro_id: uuid.UUID) -> list[ProgressoDaTrilha]:
    """Por trilha inscrita: nível certificado, quantas obrigatórias faltam
    para o próximo, pontos e badges — reaproveita `missoes_concluidas_
    pelo_guerreiro`, `Nivel`, `PontoRegular` e `Badge`, sem recalcular nada
    por conta própria (`RF-05-15`, `RF-05-16`, `RN-05-03`, `RN-05-04`,
    design — decisão 7). As recompensas conquistadas continuam só em
    `GET /v1/eu/recompensas`, que já as serve."""
    from ..pontuacao.modelo import Badge, Nivel, PontoRegular

    resultado = []
    for inscricao in consultar_inscricoes_do_guerreiro(sessao, guerreiro_id=guerreiro_id):
        trilha = sessao.get(Trilha, inscricao.trilha_id)
        obrigatorias = sessao.query(Missao).filter_by(trilha_id=trilha.id, obrigatoria=True).all()
        concluidas = missoes_concluidas_pelo_guerreiro(
            sessao, guerreiro_id=guerreiro_id, trilha_id=trilha.id
        )
        ids_obrigatorias = {missao.id for missao in obrigatorias}
        nivel_atual = (
            sessao.query(Nivel.valor)
            .filter_by(guerreiro_id=guerreiro_id, trilha_id=trilha.id)
            .order_by(Nivel.valor.desc())
            .limit(1)
            .scalar()
        )
        conta_de_pontos = (
            sessao.query(PontoRegular)
            .filter_by(guerreiro_id=guerreiro_id, trilha_id=trilha.id)
            .first()
        )
        badges = (
            sessao.query(Badge.tipo).filter_by(guerreiro_id=guerreiro_id, trilha_id=trilha.id).all()
        )
        resultado.append(
            ProgressoDaTrilha(
                trilha=trilha,
                nivel_atual=nivel_atual,
                obrigatorias_desbloqueadas=len(concluidas & ids_obrigatorias),
                obrigatorias_totais=len(obrigatorias),
                pontos_regulares=conta_de_pontos.total if conta_de_pontos is not None else 0,
                badges=[badge.tipo.value for badge in badges],
            )
        )
    return resultado
