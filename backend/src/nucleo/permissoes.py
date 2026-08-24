import enum
from typing import Annotated, Literal

from fastapi import Depends

from .autenticacao import ContextoDaSessao, exigir_persona
from .erros import PermissaoNegada
from .personas.modelo import Papel

Acesso = Literal["escreve", "le"]

TUDO = "tudo"


class Operacao(enum.StrEnum):
    """Uma entrada por item de cada célula da tabela de personas e
    permissões do PRD-01 §4 — a matriz é dado, não decisão espalhada pelas
    rotas (design — decisões). Rotas futuras, de fatias e PRDs seguintes,
    declaram a operação que exigem contra este mesmo vocabulário.
    """

    # Admin
    tudo = TUDO
    # Mestre — escreve
    suas_trilhas_e_conteudos = "suas_trilhas_e_conteudos"
    lancamentos_e_pontuacao_negativa_das_suas_atividades = (
        "lancamentos_e_pontuacao_negativa_das_suas_atividades"
    )
    conducao_do_quiz_ao_vivo_das_suas_aulas = "conducao_do_quiz_ao_vivo_das_suas_aulas"
    auditoria_de_coleta = "auditoria_de_coleta"
    aprovacao_de_local = "aprovacao_de_local"
    aportes_seus = "aportes_seus"
    cadastro_de_responsavel = "cadastro_de_responsavel"
    vinculo_com_guerreiros_e_guerreiras = "vinculo_com_guerreiros_e_guerreiras"
    confirmacao_de_identidade_do_guerreiro = "confirmacao_de_identidade_do_guerreiro"
    cadastro_biometrico_do_guerreiro = "cadastro_biometrico_do_guerreiro"
    homologacao_da_equipe_da_trilha = "homologacao_da_equipe_da_trilha"
    credencial_de_dispositivo_dos_seus_desafios = "credencial_de_dispositivo_dos_seus_desafios"
    cadastro_do_guerreiro_no_encontro = "cadastro_do_guerreiro_no_encontro"
    testemunho_do_termo_impresso = "testemunho_do_termo_impresso"
    # Mestre — lê
    suas_turmas = "suas_turmas"
    painel_do_dia_na_app_03 = "painel_do_dia_na_app_03"
    # Guerreiro(a) — escreve
    seus_registros_de_coleta = "seus_registros_de_coleta"
    suas_criacoes = "suas_criacoes"
    suas_sugestoes = "suas_sugestoes"
    recompensas_recebidas_nos_marcos = "recompensas_recebidas_nos_marcos"
    equipe_que_forma_na_aula = "equipe_que_forma_na_aula"
    resposta_de_quiz_da_equipe = "resposta_de_quiz_da_equipe"
    solicitacao_de_local = "solicitacao_de_local"
    # Guerreiro(a) — lê
    seus_dados = "seus_dados"
    equipes_da_aula_em_andamento = "equipes_da_aula_em_andamento"
    # Responsável — escreve
    consentimentos = "consentimentos"
    autorizacoes = "autorizacoes"
    solicitacoes_e_propostas = "solicitacoes_e_propostas"
    # Responsável — lê
    guerreiros_sob_sua_responsabilidade = "guerreiros_sob_sua_responsabilidade"
    # Apoiador — escreve
    aportes_declarados = "aportes_declarados"
    cobertura_de_missao = "cobertura_de_missao"
    propostas_de_desafio_extra = "propostas_de_desafio_extra"
    documentos_comprobatorios = "documentos_comprobatorios"
    propostas_de_evolucao = "propostas_de_evolucao"
    # Apoiador — lê
    seus_aportes = "seus_aportes"
    efetividade_agregada = "efetividade_agregada"
    # Comum a várias personas — lê
    publico = "publico"
    # Catálogo — nenhum papel tem entrada dele na matriz; o Admin o alcança
    # por `Operacao.tudo`, e negar por padrão recusa os demais (`RF-01-62`).
    catalogo_de_poderes = "catalogo_de_poderes"
    # Mesmo precedente: nenhum papel tem entrada, inclusive o Mestre, que
    # escolhe entre os tipos cadastrados e nunca cria um novo (`RF-08-05`).
    catalogo_de_tipos_de_coleta = "catalogo_de_tipos_de_coleta"


MATRIZ_DE_PERMISSOES: dict[Papel, dict[Acesso, frozenset[Operacao]]] = {
    Papel.admin: {
        "escreve": frozenset({Operacao.tudo}),
        "le": frozenset({Operacao.tudo}),
    },
    Papel.mestre: {
        "escreve": frozenset(
            {
                Operacao.suas_trilhas_e_conteudos,
                Operacao.lancamentos_e_pontuacao_negativa_das_suas_atividades,
                Operacao.conducao_do_quiz_ao_vivo_das_suas_aulas,
                Operacao.auditoria_de_coleta,
                Operacao.aprovacao_de_local,
                Operacao.aportes_seus,
                Operacao.cadastro_de_responsavel,
                Operacao.vinculo_com_guerreiros_e_guerreiras,
                Operacao.confirmacao_de_identidade_do_guerreiro,
                Operacao.cadastro_biometrico_do_guerreiro,
                Operacao.homologacao_da_equipe_da_trilha,
                Operacao.credencial_de_dispositivo_dos_seus_desafios,
                Operacao.cadastro_do_guerreiro_no_encontro,
                Operacao.testemunho_do_termo_impresso,
                Operacao.propostas_de_evolucao,
            }
        ),
        "le": frozenset({Operacao.publico, Operacao.suas_turmas, Operacao.painel_do_dia_na_app_03}),
    },
    Papel.guerreiro: {
        "escreve": frozenset(
            {
                Operacao.seus_registros_de_coleta,
                Operacao.suas_criacoes,
                Operacao.suas_sugestoes,
                Operacao.recompensas_recebidas_nos_marcos,
                Operacao.equipe_que_forma_na_aula,
                Operacao.resposta_de_quiz_da_equipe,
                Operacao.solicitacao_de_local,
            }
        ),
        "le": frozenset(
            {Operacao.seus_dados, Operacao.equipes_da_aula_em_andamento, Operacao.publico}
        ),
    },
    Papel.responsavel: {
        "escreve": frozenset(
            {Operacao.consentimentos, Operacao.autorizacoes, Operacao.solicitacoes_e_propostas}
        ),
        "le": frozenset({Operacao.guerreiros_sob_sua_responsabilidade, Operacao.publico}),
    },
    Papel.apoiador: {
        "escreve": frozenset(
            {
                Operacao.aportes_declarados,
                Operacao.cobertura_de_missao,
                Operacao.propostas_de_desafio_extra,
                Operacao.documentos_comprobatorios,
                Operacao.propostas_de_evolucao,
            }
        ),
        "le": frozenset({Operacao.seus_aportes, Operacao.efetividade_agregada, Operacao.publico}),
    },
}


def conferir_permissao(papel: Papel, acesso: Acesso, operacao: Operacao) -> bool:
    """Nega por padrão (`RF-01-16`): papel sem entrada na matriz, ou matriz
    sem a operação pedida, não passa."""
    permitidos = MATRIZ_DE_PERMISSOES.get(papel, {}).get(acesso, frozenset())
    return operacao in permitidos or Operacao.tudo in permitidos


def exigir_permissao(operacao: Operacao, acesso: Acesso):
    """Dependência única de conferência da matriz (design — decisões): a
    rota esquecida de um decorador passaria despercebida; aqui o padrão é
    negar.
    """

    def _dependencia(
        contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    ) -> ContextoDaSessao:
        if not conferir_permissao(contexto.papel, acesso, operacao):
            raise PermissaoNegada()
        return contexto

    return _dependencia


def exigir_qualquer_permissao(operacoes: frozenset[Operacao], acesso: Acesso):
    """Mesma dependência única, para a rota que uma mesma ação alcança por
    operações de nomes diferentes conforme o papel — caso da fila de
    avaliação, em que `suas_sugestoes`, `solicitacoes_e_propostas` e
    `propostas_de_evolucao` levam à mesma rota (`RF-01-25`)."""

    def _dependencia(
        contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    ) -> ContextoDaSessao:
        if not any(conferir_permissao(contexto.papel, acesso, operacao) for operacao in operacoes):
            raise PermissaoNegada()
        return contexto

    return _dependencia
