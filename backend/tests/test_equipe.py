from datetime import UTC, datetime, timedelta

import pytest

from nucleo.equipes.modelo import Equipe, IntegranteDaEquipe
from nucleo.equipes.regra import (
    TETO_DE_INTEGRANTES,
    entrar_na_equipe,
    equipes_da_aula,
    homologar_equipe_da_trilha,
    renomear_equipe,
    sair_da_equipe,
)
from nucleo.equipes.regra import criar_equipe as criar_equipe_pela_regra
from nucleo.erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from nucleo.personas.modelo import Papel


def test_quem_cria_entra_como_primeiro_integrante(
    sessao, criar_persona, criar_comunidade, criar_aula
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)

    equipe = criar_equipe_pela_regra(
        sessao, nome="Leões", operador=guerreiro, aula=aula, trilha=None
    )
    sessao.commit()

    integrantes = sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id).all()
    assert len(integrantes) == 1
    assert integrantes[0].persona_id == guerreiro.id


def test_admin_nao_cria_equipe(sessao, criar_persona, criar_comunidade, criar_aula):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    with pytest.raises(PermissaoNegada):
        criar_equipe_pela_regra(sessao, nome="Leões", operador=admin, aula=aula, trilha=None)
    assert sessao.query(Equipe).count() == 0


def test_admin_nao_inclui_integrante(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_equipe
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    equipe = criar_equipe(guerreiro, aula=aula)

    with pytest.raises(PermissaoNegada):
        entrar_na_equipe(sessao, operador=admin, equipe=equipe)
    assert sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id).count() == 1


def test_mestre_nao_remove_integrante(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_equipe
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    equipe = criar_equipe(guerreiro, aula=aula)

    with pytest.raises(PermissaoNegada):
        sair_da_equipe(sessao, operador=mestre, equipe=equipe, persona_id=guerreiro.id)
    assert sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id).count() == 1


def test_equipe_sem_vinculo_e_recusada(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_equipe_pela_regra(sessao, nome="Leões", operador=guerreiro, aula=None, trilha=None)
    assert excinfo.value.campo == "aula_id"
    assert sessao.query(Equipe).count() == 0


def test_equipe_com_aula_e_trilha_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_equipe_pela_regra(sessao, nome="Leões", operador=guerreiro, aula=aula, trilha=trilha)
    assert excinfo.value.campo == "trilha_id"
    assert sessao.query(Equipe).count() == 0


def test_quinto_integrante_e_aceito_sexto_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_equipe
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    criador = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    equipe = criar_equipe(criador, aula=aula)

    guerreiros = [criar_persona(Papel.guerreiro, comunidade=comunidade) for _ in range(4)]
    for guerreiro in guerreiros:
        entrar_na_equipe(sessao, operador=guerreiro, equipe=equipe)
    sessao.commit()

    assert (
        sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id).count()
        == TETO_DE_INTEGRANTES
    )

    sexto = criar_persona(Papel.guerreiro, comunidade=comunidade)
    with pytest.raises(ErroDeValidacao) as excinfo:
        entrar_na_equipe(sessao, operador=sexto, equipe=equipe)
    assert excinfo.value.campo == "equipe_id"
    assert sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id).count() == 5


def test_primeiro_nao_guerreiro_e_aceito_segundo_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_equipe
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    criador = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    equipe = criar_equipe(criador, aula=aula)

    responsavel_um = criar_persona(Papel.responsavel)
    entrar_na_equipe(sessao, operador=responsavel_um, equipe=equipe)
    sessao.commit()

    responsavel_dois = criar_persona(Papel.responsavel)
    with pytest.raises(ErroDeValidacao) as excinfo:
        entrar_na_equipe(sessao, operador=responsavel_dois, equipe=equipe)
    assert excinfo.value.campo == "persona_id"


def test_papel_declarado_e_gravado_e_papel_ausente_e_aceito(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_equipe
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    criador = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    equipe = criar_equipe(criador, aula=aula)

    outro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    integrante = entrar_na_equipe(sessao, operador=outro, equipe=equipe, papel="quem constrói")
    sessao.commit()

    assert integrante.papel == "quem constrói"
    criador_integrante = (
        sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id, persona_id=criador.id).one()
    )
    assert criador_integrante.papel is None


def test_equipe_de_uma_aula_nao_aparece_em_outra(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_equipe
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula_um = criar_aula(admin, comunidade)
    aula_dois = criar_aula(
        admin,
        comunidade,
        inicio_em=datetime(2026, 8, 2, 10, 0, tzinfo=UTC),
        fim_em=datetime(2026, 8, 2, 12, 0, tzinfo=UTC),
    )
    equipe = criar_equipe(guerreiro, aula=aula_um)

    assert equipe.id in {e.id for e in equipes_da_aula(sessao, aula_um.id)}
    assert equipe.id not in {e.id for e in equipes_da_aula(sessao, aula_dois.id)}


def test_equipe_de_aula_encerrada_nao_recebe_integrante(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_equipe
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    criador = criar_persona(Papel.guerreiro, comunidade=comunidade)
    agora = datetime.now(UTC)
    aula_encerrada = criar_aula(
        admin, comunidade, inicio_em=agora - timedelta(hours=3), fim_em=agora - timedelta(hours=1)
    )
    equipe = criar_equipe(criador, aula=aula_encerrada)

    outro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    with pytest.raises(ErroDeValidacao) as excinfo:
        entrar_na_equipe(sessao, operador=outro, equipe=equipe)
    assert excinfo.value.campo == "equipe_id"


def test_mesmo_guerreiro_em_duas_equipes_da_aula(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_equipe
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    outro_criador = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    equipe_um = criar_equipe(guerreiro, aula=aula)
    equipe_dois = criar_equipe(outro_criador, aula=aula)

    entrar_na_equipe(sessao, operador=guerreiro, equipe=equipe_dois)
    sessao.commit()

    ids_de_equipes = {
        i.equipe_id for i in sessao.query(IntegranteDaEquipe).filter_by(persona_id=guerreiro.id)
    }
    assert ids_de_equipes == {equipe_um.id, equipe_dois.id}


def test_segunda_equipe_da_mesma_trilha_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    criar_equipe(guerreiro, trilha=trilha)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_equipe_pela_regra(sessao, nome="Leões", operador=guerreiro, aula=None, trilha=trilha)
    assert excinfo.value.campo == "trilha_id"


def test_equipes_de_trilhas_diferentes_convivem(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha_um = criar_trilha(mestre, nome="Trilha Um")
    trilha_dois = criar_trilha(mestre, nome="Trilha Dois")
    equipe_um = criar_equipe(guerreiro, trilha=trilha_um)

    equipe_dois = criar_equipe_pela_regra(
        sessao, nome="Leões", operador=guerreiro, aula=None, trilha=trilha_dois
    )
    sessao.commit()

    ids_de_equipes = {
        i.equipe_id for i in sessao.query(IntegranteDaEquipe).filter_by(persona_id=guerreiro.id)
    }
    assert ids_de_equipes == {equipe_um.id, equipe_dois.id}


def test_mestre_homologa_e_a_composicao_congela(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    equipe = criar_equipe(guerreiro, trilha=trilha)

    homologar_equipe_da_trilha(sessao, operador=mestre, equipe=equipe)
    sessao.commit()

    assert equipe.homologado_por_id == mestre.id
    assert equipe.homologado_em is not None


def test_entrada_depois_da_homologacao_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    equipe = criar_equipe(guerreiro, trilha=trilha, homologada=True, homologado_por=mestre)

    outro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    with pytest.raises(ErroDeValidacao) as excinfo:
        entrar_na_equipe(sessao, operador=outro, equipe=equipe)
    assert excinfo.value.campo == "equipe_id"


def test_saida_depois_da_homologacao_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    equipe = criar_equipe(guerreiro, trilha=trilha, homologada=True, homologado_por=mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        sair_da_equipe(sessao, operador=guerreiro, equipe=equipe, persona_id=guerreiro.id)
    assert excinfo.value.campo == "equipe_id"
    assert sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id).count() == 1


def test_guerreiro_nao_homologa(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    equipe = criar_equipe(guerreiro, trilha=trilha)

    with pytest.raises(PermissaoNegada):
        homologar_equipe_da_trilha(sessao, operador=guerreiro, equipe=equipe)
    assert equipe.homologado_em is None


def test_equipe_da_trilha_nao_homologada_aceita_composicao(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    equipe = criar_equipe(guerreiro, trilha=trilha)

    outro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    integrante = entrar_na_equipe(sessao, operador=outro, equipe=equipe)
    sessao.commit()

    assert integrante.persona_id == outro.id


def test_sair_da_equipe_inexistente_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_equipe
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    criador = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    equipe = criar_equipe(criador, aula=aula)
    outro = criar_persona(Papel.guerreiro, comunidade=comunidade)

    with pytest.raises(NaoEncontrado):
        sair_da_equipe(sessao, operador=outro, equipe=equipe, persona_id=outro.id)


def test_sair_da_equipe_remove_o_integrante(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_equipe
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    criador = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    equipe = criar_equipe(criador, aula=aula)
    outro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    entrar_na_equipe(sessao, operador=outro, equipe=equipe)
    sessao.commit()

    sair_da_equipe(sessao, operador=outro, equipe=equipe, persona_id=outro.id)
    sessao.commit()

    assert (
        sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id, persona_id=outro.id).first()
        is None
    )


def test_homologar_equipe_da_aula_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_equipe
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    equipe = criar_equipe(guerreiro, aula=aula)

    with pytest.raises(ErroDeValidacao) as excinfo:
        homologar_equipe_da_trilha(sessao, operador=mestre, equipe=equipe)
    assert excinfo.value.campo == "equipe_id"


# `RF-04-69`, `RF-04-70`, `RN-04-39`: o nome da equipe.


@pytest.fixture
def aula_com_guerreiro(criar_persona, criar_comunidade, criar_aula):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    return admin, comunidade, guerreiro, aula


def test_equipe_nasce_com_o_nome_aparado(sessao, aula_com_guerreiro):
    _admin, _comunidade, guerreiro, aula = aula_com_guerreiro

    equipe = criar_equipe_pela_regra(
        sessao, nome="  Leões  ", operador=guerreiro, aula=aula, trilha=None
    )
    sessao.commit()

    assert equipe.nome == "Leões"


@pytest.mark.parametrize("nome", [None, "", "   ", "x" * 21])
def test_nome_ausente_em_branco_ou_longo_e_recusado(sessao, aula_com_guerreiro, nome):
    _admin, _comunidade, guerreiro, aula = aula_com_guerreiro

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_equipe_pela_regra(sessao, nome=nome, operador=guerreiro, aula=aula, trilha=None)
    assert excinfo.value.campo == "nome"
    assert sessao.query(Equipe).count() == 0


def test_nome_de_20_caracteres_e_aceito(sessao, aula_com_guerreiro):
    _admin, _comunidade, guerreiro, aula = aula_com_guerreiro

    equipe = criar_equipe_pela_regra(
        sessao, nome="x" * 20, operador=guerreiro, aula=aula, trilha=None
    )

    assert equipe.nome == "x" * 20


def test_nome_repetido_na_aula_e_recusado_sem_distinguir_caixa(
    sessao, aula_com_guerreiro, criar_persona, criar_equipe
):
    _admin, comunidade, guerreiro, aula = aula_com_guerreiro
    criar_equipe(criar_persona(Papel.guerreiro, comunidade=comunidade), aula=aula, nome="Leões")

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_equipe_pela_regra(sessao, nome=" leões ", operador=guerreiro, aula=aula, trilha=None)
    assert excinfo.value.campo == "nome"
    assert sessao.query(Equipe).count() == 1


def test_nome_repetido_na_trilha_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_equipe
):
    comunidade = criar_comunidade()
    trilha = criar_trilha(criar_persona(Papel.mestre))
    criar_equipe(criar_persona(Papel.guerreiro, comunidade=comunidade), trilha=trilha, nome="Onça")
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_equipe_pela_regra(sessao, nome="ONÇA", operador=guerreiro, aula=None, trilha=trilha)
    assert excinfo.value.campo == "nome"


def test_mesmo_nome_em_aulas_diferentes_e_aceito(
    sessao, aula_com_guerreiro, criar_persona, criar_aula, criar_equipe
):
    admin, comunidade, guerreiro, aula = aula_com_guerreiro
    agora = datetime.now(UTC)
    ontem = criar_aula(
        admin, comunidade, inicio_em=agora - timedelta(days=1), fim_em=agora - timedelta(hours=20)
    )
    criar_equipe(criar_persona(Papel.guerreiro, comunidade=comunidade), aula=ontem, nome="Leões")

    equipe = criar_equipe_pela_regra(
        sessao, nome="Leões", operador=guerreiro, aula=aula, trilha=None
    )

    assert equipe.nome == "Leões"


def test_integrante_renomeia_a_equipe(sessao, aula_com_guerreiro, criar_equipe):
    _admin, _comunidade, guerreiro, aula = aula_com_guerreiro
    equipe = criar_equipe(guerreiro, aula=aula, nome="Leões")

    renomear_equipe(sessao, operador=guerreiro, equipe=equipe, nome=" Onças ")

    assert equipe.nome == "Onças"


def test_mudar_so_a_caixa_do_proprio_nome_e_aceito(sessao, aula_com_guerreiro, criar_equipe):
    _admin, _comunidade, guerreiro, aula = aula_com_guerreiro
    equipe = criar_equipe(guerreiro, aula=aula, nome="leões")

    renomear_equipe(sessao, operador=guerreiro, equipe=equipe, nome="Leões")

    assert equipe.nome == "Leões"


def test_renomear_para_nome_de_outra_equipe_da_aula_e_recusado(
    sessao, aula_com_guerreiro, criar_persona, criar_equipe
):
    _admin, comunidade, guerreiro, aula = aula_com_guerreiro
    criar_equipe(criar_persona(Papel.guerreiro, comunidade=comunidade), aula=aula, nome="Onças")
    equipe = criar_equipe(guerreiro, aula=aula, nome="Leões")

    with pytest.raises(ErroDeValidacao) as excinfo:
        renomear_equipe(sessao, operador=guerreiro, equipe=equipe, nome="onças")
    assert excinfo.value.campo == "nome"
    sessao.refresh(equipe)
    assert equipe.nome == "Leões"


def test_quem_nao_integra_nao_renomeia(sessao, aula_com_guerreiro, criar_persona, criar_equipe):
    _admin, comunidade, guerreiro, aula = aula_com_guerreiro
    equipe = criar_equipe(guerreiro, aula=aula, nome="Leões")
    de_fora = criar_persona(Papel.guerreiro, comunidade=comunidade)

    with pytest.raises(PermissaoNegada):
        renomear_equipe(sessao, operador=de_fora, equipe=equipe, nome="Onças")


@pytest.mark.parametrize("papel", [Papel.admin, Papel.mestre])
def test_a_gestao_nao_renomeia(sessao, aula_com_guerreiro, criar_persona, criar_equipe, papel):
    _admin, _comunidade, guerreiro, aula = aula_com_guerreiro
    equipe = criar_equipe(guerreiro, aula=aula, nome="Leões")

    with pytest.raises(PermissaoNegada):
        renomear_equipe(sessao, operador=criar_persona(papel), equipe=equipe, nome="Onças")


def test_equipe_de_aula_encerrada_nao_troca_de_nome(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_equipe
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    agora = datetime.now(UTC)
    aula = criar_aula(
        admin, comunidade, inicio_em=agora - timedelta(hours=3), fim_em=agora - timedelta(hours=1)
    )
    equipe = criar_equipe(guerreiro, aula=aula, nome="Leões")

    with pytest.raises(ErroDeValidacao):
        renomear_equipe(sessao, operador=guerreiro, equipe=equipe, nome="Onças")


def test_equipe_da_trilha_homologada_nao_troca_de_nome(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_equipe
):
    guerreiro = criar_persona(Papel.guerreiro, comunidade=criar_comunidade())
    trilha = criar_trilha(criar_persona(Papel.mestre))
    equipe = criar_equipe(guerreiro, trilha=trilha, homologada=True, nome="Leões")

    with pytest.raises(ErroDeValidacao):
        renomear_equipe(sessao, operador=guerreiro, equipe=equipe, nome="Onças")
