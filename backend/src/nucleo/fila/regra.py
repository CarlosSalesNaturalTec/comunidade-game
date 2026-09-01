import re
import uuid
from datetime import timedelta

from sqlalchemy.orm import Session

from ..armazenamento.porta import PortaDeArmazenamento
from ..erros import ConjuntoDeDadosNaoLiberado, DocumentoPessoalRecusado, ErroDeValidacao
from ..personas.modelo import Papel, Persona
from ..personas.regra import conferir_disponibilidade_de_nick
from ..ponto_extra.regra import creditar_ponto_extra
from ..pontuacao.regra import conceder_badge_de_protagonismo
from ..tempo import agora
from .modelo import (
    PerfilDeApoiador,
    PretensaoDeParticipacao,
    SituacaoDaSolicitacao,
    SituacaoDaSugestao,
    SolicitacaoDeChave,
    SolicitacaoDeDados,
    SolicitacaoDeParticipacao,
    SugestaoOuProposta,
    TipoDeAlvo,
)

# Mesma lista que `aportes` e `ressarcimentos` já aplicam ao comprovante
# (`RF-14-04`, `RN-14-06`).
_FORMATOS_DE_COMPROVANTE_ACEITOS = frozenset({"application/pdf", "image/jpeg", "image/png"})

# O prazo de resposta é promessa de produto (02 §1, 03 §§7, 12.3), gravado na
# linha no registro e nunca recalculado na leitura (`RN-01-49`).
PRAZO_DE_AVALIACAO_EM_DIAS = 7
PRAZO_DE_AVALIACAO = timedelta(days=PRAZO_DE_AVALIACAO_EM_DIAS)

# Guarda da transcrição da sugestão não adotada (03 §12.2).
PRAZO_DE_DESCARTE_DA_TRANSCRICAO_NAO_ADOTADA = timedelta(days=90)

# Documento 11 §5: a proposta de evolução adotada é a única fonte só extra
# do Ciclo 01.
PONTOS_EXTRAS_DA_PROPOSTA_ADOTADA = 20

_PADRAO_CPF = re.compile(r"\d[\d.\-]{9,12}\d")
_PADRAO_CNPJ = re.compile(r"\d[\d.\-/]{12,16}\d")
_PADRAO_RG_FORMATADO = re.compile(r"\b\d{1,2}\.\d{3}\.\d{3}-[0-9Xx]\b")


def _somente_digitos(texto: str) -> str:
    return "".join(caractere for caractere in texto if caractere.isdigit())


def _cpf_valido(digitos: str) -> bool:
    if len(digitos) != 11 or digitos == digitos[0] * 11:
        return False
    for posicao in (9, 10):
        soma = sum(int(digitos[indice]) * (posicao + 1 - indice) for indice in range(posicao))
        digito_esperado = ((soma * 10) % 11) % 10
        if digito_esperado != int(digitos[posicao]):
            return False
    return True


def _cnpj_valido(digitos: str) -> bool:
    if len(digitos) != 14 or digitos == digitos[0] * 14:
        return False
    pesos_do_primeiro_digito = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_do_segundo_digito = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    def _digito_verificador(base: str, pesos: list[int]) -> int:
        soma = sum(int(digito) * peso for digito, peso in zip(base, pesos, strict=True))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    if _digito_verificador(digitos[:12], pesos_do_primeiro_digito) != int(digitos[12]):
        return False
    return _digito_verificador(digitos[:13], pesos_do_segundo_digito) == int(digitos[13])


def contem_documento_pessoal(*textos: str | None) -> bool:
    """Heurística de `RN-01-29`: varre os campos livres da solicitação em
    busca de CPF e CNPJ — com dígito verificador conferido, para não recusar
    à toa um número qualquer — e de RG em formato usual, que não tem dígito
    verificador nacional padronizado."""
    for texto in textos:
        if not texto:
            continue
        for trecho in _PADRAO_CNPJ.findall(texto):
            if _cnpj_valido(_somente_digitos(trecho)):
                return True
        for trecho in _PADRAO_CPF.findall(texto):
            if _cpf_valido(_somente_digitos(trecho)):
                return True
        if _PADRAO_RG_FORMATADO.search(texto):
            return True
    return False


def registrar_solicitacao_de_participacao(
    sessao: Session,
    *,
    nome_ou_razao_social: str,
    email: str,
    whatsapp: str,
    pretensao: PretensaoDeParticipacao,
    apresentacao: str,
    instituicao: str | None = None,
    links: str | None = None,
    nick: str | None = None,
    perfil: PerfilDeApoiador | None = None,
    aporte_declarado: str | None = None,
    comprovante_conteudo: bytes | None = None,
    comprovante_nome_original: str | None = None,
    comprovante_tipo: str | None = None,
    armazenamento: PortaDeArmazenamento | None = None,
) -> SolicitacaoDeParticipacao:
    """Registra o pré-cadastro sem criar cadastro, persona ou acesso
    (`RN-01-03`, `RN-01-28`). A plataforma não coleta CPF, CNPJ nem
    documento de identidade (`RN-01-29`).

    O nick pretendido só existe na pretensão de Apoiador (`RF-01-25`,
    `RF-14-13`) — o Mestre o define no primeiro acesso, nunca no
    pré-cadastro. Passa pela mesma conferência restrita a adulto que a rota
    pública de disponibilidade usa, o que já conta os nicks reservados por
    outra solicitação ainda dentro do prazo (`RN-01-28`, `RN-01-30`); a
    reserva em si não é estado novo, é o próprio `prazo` desta solicitação
    (design — Decisions).
    """
    if contem_documento_pessoal(
        nome_ou_razao_social, apresentacao, instituicao, links, aporte_declarado
    ):
        raise DocumentoPessoalRecusado()

    if nick is not None:
        if pretensao != PretensaoDeParticipacao.apoiador:
            raise ErroDeValidacao(mensagem="Só a pretensão de Apoiador declara nick.", campo="nick")
        if not conferir_disponibilidade_de_nick(sessao, nick):
            raise ErroDeValidacao(mensagem="Este nick já está em uso.", campo="nick")

    if perfil is not None and pretensao != PretensaoDeParticipacao.apoiador:
        raise ErroDeValidacao(mensagem="Só a pretensão de Apoiador declara perfil.", campo="perfil")

    solicitacao = SolicitacaoDeParticipacao(
        nome_ou_razao_social=nome_ou_razao_social,
        email=email,
        whatsapp=whatsapp,
        pretensao=pretensao,
        apresentacao=apresentacao,
        instituicao=instituicao,
        links=links,
        nick=nick,
        perfil=perfil,
        aporte_declarado=aporte_declarado,
        prazo=agora() + PRAZO_DE_AVALIACAO,
    )

    if comprovante_conteudo is not None:
        if pretensao != PretensaoDeParticipacao.apoiador:
            raise ErroDeValidacao(
                mensagem="Só a pretensão de Apoiador aceita comprovante.", campo="comprovante"
            )
        if comprovante_tipo not in _FORMATOS_DE_COMPROVANTE_ACEITOS:
            raise ErroDeValidacao(
                mensagem="Comprovante aceito apenas em PDF, JPG ou PNG.", campo="comprovante"
            )
        if armazenamento is None:
            raise ErroDeValidacao(mensagem="Porta de armazenamento não disponível.")
        referencia = f"comprovantes/{uuid.uuid4()}"
        armazenamento.gravar(referencia=referencia, conteudo=comprovante_conteudo)
        solicitacao.comprovante_referencia = referencia
        solicitacao.comprovante_nome_original = comprovante_nome_original
        solicitacao.comprovante_tipo = comprovante_tipo
        solicitacao.comprovante_tamanho = len(comprovante_conteudo)

    sessao.add(solicitacao)
    sessao.flush()
    return solicitacao


def registrar_solicitacao_de_dados(
    sessao: Session,
    *,
    solicitante: str,
    instituicao: str,
    email: str,
    finalidade_declarada: str,
    recorte_pedido: str,
) -> SolicitacaoDeDados:
    """`RF-01-46`: sem finalidade declarada não há registro."""
    if not finalidade_declarada.strip():
        raise ErroDeValidacao(
            mensagem="Finalidade declarada é obrigatória.", campo="finalidade_declarada"
        )

    solicitacao = SolicitacaoDeDados(
        solicitante=solicitante,
        instituicao=instituicao,
        email=email,
        finalidade_declarada=finalidade_declarada,
        recorte_pedido=recorte_pedido,
        prazo=agora() + PRAZO_DE_AVALIACAO,
    )
    sessao.add(solicitacao)
    sessao.flush()
    return solicitacao


def registrar_solicitacao_de_chave(
    sessao: Session,
    *,
    solicitante: str,
    contato: str,
    o_que_pretende_construir: str,
    instituicao: str | None = None,
) -> SolicitacaoDeChave:
    """`RF-01-49`: registra e não emite chave (`RN-01-37`)."""
    solicitacao = SolicitacaoDeChave(
        solicitante=solicitante,
        contato=contato,
        instituicao=instituicao,
        o_que_pretende_construir=o_que_pretende_construir,
        prazo=agora() + PRAZO_DE_AVALIACAO,
    )
    sessao.add(solicitacao)
    sessao.flush()
    return solicitacao


def registrar_sugestao(
    sessao: Session,
    *,
    autor: Persona,
    alvo_tipo: TipoDeAlvo,
    texto: str,
    alvo_id: uuid.UUID | None = None,
) -> SugestaoOuProposta:
    """`RF-01-25`: só texto — o áudio é descartado antes de chegar aqui
    (03 §12.2)."""
    if alvo_tipo != TipoDeAlvo.plataforma and alvo_id is None:
        raise ErroDeValidacao(
            mensagem="Alvo de atividade ou trilha exige o identificador.", campo="alvo_id"
        )

    sugestao = SugestaoOuProposta(
        autor_id=autor.id,
        papel_do_autor=autor.papel.value,
        alvo_tipo=alvo_tipo,
        alvo_id=alvo_id,
        texto=texto,
        prazo=agora() + PRAZO_DE_AVALIACAO,
    )
    sessao.add(sugestao)
    sessao.flush()
    return sugestao


def _concluir_desfecho(item, *, avaliado_por: Persona, parecer: str | None) -> None:
    item.avaliado_por_id = avaliado_por.id
    item.parecer = parecer
    item.decidido_em = agora()


def avaliar_solicitacao_de_participacao(
    sessao: Session,
    solicitacao: SolicitacaoDeParticipacao,
    *,
    situacao: SituacaoDaSolicitacao,
    avaliado_por: Persona,
    parecer: str | None = None,
) -> SolicitacaoDeParticipacao:
    """O desfecho é ato de Admin; nenhum caminho daqui cria cadastro,
    persona ou credencial (`RN-01-03`, `RN-01-28`) — o cadastro em si é
    ato posterior, fora desta função."""
    if situacao not in (SituacaoDaSolicitacao.aceita, SituacaoDaSolicitacao.recusada):
        raise ErroDeValidacao(mensagem="Desfecho precisa ser aceita ou recusada.", campo="situacao")
    solicitacao.situacao = situacao
    _concluir_desfecho(solicitacao, avaliado_por=avaliado_por, parecer=parecer)
    sessao.flush()
    return solicitacao


def avaliar_solicitacao_de_dados(
    sessao: Session,
    solicitacao: SolicitacaoDeDados,
    *,
    situacao: SituacaoDaSolicitacao,
    avaliado_por: Persona,
    parecer: str,
    compromisso_de_nao_reidentificar: bool = False,
) -> SolicitacaoDeDados:
    """`RN-01-48`: a aprovação exige solicitante identificado — já garantido
    no registro —, finalidade declarada compatível — o parecer do Admin — e
    o compromisso de não reidentificação, afirmado aqui. A recusa registra
    o motivo no parecer."""
    if situacao not in (SituacaoDaSolicitacao.aceita, SituacaoDaSolicitacao.recusada):
        raise ErroDeValidacao(mensagem="Desfecho precisa ser aceita ou recusada.", campo="situacao")
    if not parecer.strip():
        raise ErroDeValidacao(mensagem="O parecer do Admin é obrigatório.", campo="parecer")
    if situacao == SituacaoDaSolicitacao.aceita and not compromisso_de_nao_reidentificar:
        raise ErroDeValidacao(
            mensagem="Aprovação exige o compromisso de não tentar reidentificar ninguém.",
            campo="compromisso_de_nao_reidentificar",
        )
    solicitacao.situacao = situacao
    _concluir_desfecho(solicitacao, avaliado_por=avaliado_por, parecer=parecer)
    sessao.flush()
    return solicitacao


def avaliar_solicitacao_de_chave(
    sessao: Session,
    solicitacao: SolicitacaoDeChave,
    *,
    situacao: SituacaoDaSolicitacao,
    avaliado_por: Persona,
    parecer: str | None = None,
) -> SolicitacaoDeChave:
    """A emissão da chave em si é `RF-01-50`, de fatia seguinte; aqui só o
    desfecho do pedido."""
    if situacao not in (SituacaoDaSolicitacao.aceita, SituacaoDaSolicitacao.recusada):
        raise ErroDeValidacao(mensagem="Desfecho precisa ser aceita ou recusada.", campo="situacao")
    solicitacao.situacao = situacao
    _concluir_desfecho(solicitacao, avaliado_por=avaliado_por, parecer=parecer)
    sessao.flush()
    return solicitacao


def avaliar_sugestao(
    sessao: Session,
    sugestao: SugestaoOuProposta,
    *,
    situacao: SituacaoDaSugestao,
    avaliado_por: Persona,
    parecer: str | None = None,
    motivo_do_retorno: str | None = None,
) -> SugestaoOuProposta:
    """Adotada credita 20 extras e o badge de protagonismo na mesma
    operação, mas **só quando o autor tem papel de Guerreiro(a)**: a
    pontuação é da criança, e proposta de responsável, de Mestre ou de
    Apoiador não credita (`RF-01-56`, `RN-01-50`, `RN-13-18`, design —
    decisão 8). Idempotente pela marca `creditado_em` — regravar "adotada"
    não credita de novo. Não adotada grava o motivo em linguagem simples e
    a data de descarte da transcrição, 90 dias à frente (03 §12.2)."""
    if situacao not in (SituacaoDaSugestao.adotada, SituacaoDaSugestao.nao_adotada):
        raise ErroDeValidacao(
            mensagem="Desfecho precisa ser adotada ou não adotada.", campo="situacao"
        )
    if situacao == SituacaoDaSugestao.nao_adotada and not motivo_do_retorno:
        raise ErroDeValidacao(
            mensagem="Sugestão não adotada exige o motivo do retorno.", campo="motivo_do_retorno"
        )

    sugestao.situacao = situacao
    _concluir_desfecho(sugestao, avaliado_por=avaliado_por, parecer=parecer)

    if situacao == SituacaoDaSugestao.nao_adotada:
        sugestao.motivo_do_retorno = motivo_do_retorno
        sugestao.descartar_em = sugestao.decidido_em + PRAZO_DE_DESCARTE_DA_TRANSCRICAO_NAO_ADOTADA
    elif sugestao.creditado_em is None and sugestao.papel_do_autor == Papel.guerreiro.value:
        creditar_ponto_extra(
            sessao, guerreiro_id=sugestao.autor_id, valor=PONTOS_EXTRAS_DA_PROPOSTA_ADOTADA
        )
        conceder_badge_de_protagonismo(sessao, guerreiro_id=sugestao.autor_id)
        sugestao.creditado_em = sugestao.decidido_em

    sessao.flush()
    return sugestao


def esta_em_atraso(item) -> bool:
    """`RN-01-49`: derivado de `prazo < agora` sem desfecho — nunca um
    estado gravado (design — Decisions)."""
    return item.decidido_em is None and item.prazo < agora()


def liberar_conjunto_de_dados(solicitacao: SolicitacaoDeDados) -> None:
    """Guarda de `RF-01-47`: nenhum conjunto sai sem aprovação de Admin
    registrada. A geração do arquivo em si é do PRD-08 (proposal.md)."""
    if solicitacao.situacao != SituacaoDaSolicitacao.aceita:
        raise ConjuntoDeDadosNaoLiberado()
