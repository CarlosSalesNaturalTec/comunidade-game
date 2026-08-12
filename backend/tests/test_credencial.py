import pytest

from nucleo.erros import PermissaoNegada
from nucleo.personas.credenciais import criar_credencial_provisoria
from nucleo.personas.modelo import Papel, TipoDeCredencial


def test_admin_cria_credencial_provisoria_de_usuario_e_senha(sessao, configuracao, criar_persona):
    admin = criar_persona(Papel.admin)
    mestre_sem_conta = criar_persona(Papel.mestre, criada_por=admin)

    credencial, senha = criar_credencial_provisoria(
        sessao,
        configuracao,
        persona=mestre_sem_conta,
        usuario="Mestre_sem_conta",
        criada_por=admin,
    )

    assert credencial.tipo == TipoDeCredencial.usuario_e_senha
    assert credencial.troca_pendente is True
    assert credencial.segredo != senha
    assert senha not in credencial.segredo


def test_mestre_tambem_cria_credencial(sessao, configuracao, criar_persona):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)

    credencial, _ = criar_credencial_provisoria(
        sessao, configuracao, persona=responsavel, usuario="Pai_da_Maria", criada_por=mestre
    )
    assert credencial.persona_id == responsavel.id


def test_quem_nao_e_admin_nem_mestre_nao_cria_credencial(sessao, configuracao, criar_persona):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)

    with pytest.raises(PermissaoNegada):
        criar_credencial_provisoria(
            sessao, configuracao, persona=responsavel, usuario="alguem", criada_por=apoiador
        )


def test_credencial_nao_amplia_o_que_a_persona_pode(sessao, configuracao, criar_persona):
    """A credencial só autentica; o papel da persona é quem já era."""
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)

    criar_credencial_provisoria(
        sessao, configuracao, persona=responsavel, usuario="alguem", criada_por=admin
    )
    assert responsavel.papel == Papel.responsavel
