from nucleo.permissoes import MATRIZ_DE_PERMISSOES, Operacao, conferir_permissao
from nucleo.personas.modelo import Papel

# Transcrição literal da tabela do PRD-01 §4 — a divergência entre isto e
# `MATRIZ_DE_PERMISSOES` quebra o CI (design — riscos), para que a matriz
# nunca se afaste do que o PRD decidiu.
_TABELA_DO_PRD_01_PAR_4 = {
    Papel.admin: {
        "escreve": {Operacao.tudo},
        "le": {Operacao.tudo},
    },
    Papel.mestre: {
        "escreve": {
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
            Operacao.documentos_comprobatorios,
        },
        "le": {
            Operacao.publico,
            Operacao.suas_turmas,
            Operacao.painel_do_dia_na_app_03,
            Operacao.conducao_do_quiz_ao_vivo_das_suas_aulas,
            Operacao.vinculo_com_guerreiros_e_guerreiras,
        },
    },
    Papel.guerreiro: {
        "escreve": {
            Operacao.seus_registros_de_coleta,
            Operacao.suas_criacoes,
            Operacao.suas_sugestoes,
            Operacao.recompensas_recebidas_nos_marcos,
            Operacao.equipe_que_forma_na_aula,
            Operacao.resposta_de_quiz_da_equipe,
            Operacao.solicitacao_de_local,
        },
        "le": {
            Operacao.seus_dados,
            Operacao.equipes_da_aula_em_andamento,
            Operacao.publico,
            Operacao.resposta_de_quiz_da_equipe,
        },
    },
    Papel.responsavel: {
        "escreve": {
            Operacao.consentimentos,
            Operacao.autorizacoes,
            Operacao.solicitacoes_e_propostas,
        },
        "le": {Operacao.guerreiros_sob_sua_responsabilidade, Operacao.publico},
    },
    Papel.apoiador: {
        "escreve": {
            Operacao.aportes_declarados,
            Operacao.cobertura_de_missao,
            Operacao.propostas_de_desafio_extra,
            Operacao.documentos_comprobatorios,
            Operacao.propostas_de_evolucao,
        },
        "le": {Operacao.seus_aportes, Operacao.efetividade_agregada, Operacao.publico},
    },
}


def test_matriz_percorre_a_tabela_inteira_do_prd_01_par_4():
    assert set(MATRIZ_DE_PERMISSOES.keys()) == set(_TABELA_DO_PRD_01_PAR_4.keys())
    for papel, esperado in _TABELA_DO_PRD_01_PAR_4.items():
        for acesso in ("escreve", "le"):
            assert set(MATRIZ_DE_PERMISSOES[papel][acesso]) == esperado[acesso], (
                papel,
                acesso,
            )


def test_papel_com_permissao_e_atendido():
    assert conferir_permissao(Papel.mestre, "escreve", Operacao.suas_trilhas_e_conteudos)
    assert conferir_permissao(Papel.apoiador, "le", Operacao.publico)


def test_papel_sem_permissao_recebe_recusa():
    assert not conferir_permissao(Papel.mestre, "escreve", Operacao.aportes_declarados)
    assert not conferir_permissao(Papel.guerreiro, "escreve", Operacao.cadastro_de_responsavel)


def test_admin_tem_tudo_em_qualquer_operacao():
    for operacao in Operacao:
        assert conferir_permissao(Papel.admin, "escreve", operacao)
        assert conferir_permissao(Papel.admin, "le", operacao)


def test_catalogo_de_poderes_so_alcancado_por_admin():
    """`RF-01-62`: nenhum papel tem `catalogo_de_poderes` na própria
    matriz — o Admin o alcança só por `Operacao.tudo`, e negar por padrão
    recusa os demais, inclusive o Mestre."""
    for papel in (Papel.mestre, Papel.guerreiro, Papel.responsavel, Papel.apoiador):
        assert not conferir_permissao(papel, "escreve", Operacao.catalogo_de_poderes)
    assert conferir_permissao(Papel.admin, "escreve", Operacao.catalogo_de_poderes)


def test_testemunho_do_termo_impresso_e_de_mestre_e_admin_nao_do_responsavel():
    """O testemunho é ato do Mestre ou Admin, distinto do consentimento que o
    próprio responsável dá na App 07 (design — decisão 3)."""
    assert conferir_permissao(Papel.mestre, "escreve", Operacao.testemunho_do_termo_impresso)
    assert conferir_permissao(Papel.admin, "escreve", Operacao.testemunho_do_termo_impresso)
    assert not conferir_permissao(
        Papel.responsavel, "escreve", Operacao.testemunho_do_termo_impresso
    )


def test_operacao_de_outro_papel_nega_por_padrao():
    """Nega por padrão (RF-01-16): operação fora do que o papel tem
    declarado na matriz não passa, mesmo sendo uma operação real de outro
    papel — não há herança nem coringa fora de Admin."""
    assert not conferir_permissao(Papel.responsavel, "escreve", Operacao.suas_trilhas_e_conteudos)
