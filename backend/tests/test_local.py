import pytest

from nucleo.comunidades.regra import criar_comunidade
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.locais.modelo import Local, NivelDoLocal
from nucleo.locais.regra import cadastrar_local, paginar_locais
from nucleo.personas.modelo import Papel, Persona


def _criar_admin(sessao) -> Persona:
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    return admin


def _criar_comunidade(sessao, admin, nome="Comunidade"):
    return criar_comunidade(
        sessao, operador=admin, nome=nome, localizacao="L", granularidade_maxima="quadra"
    )


def test_local_com_pai_do_nivel_imediatamente_acima_e_aceito(sessao):
    admin = _criar_admin(sessao)
    comunidade = _criar_comunidade(sessao, admin)

    raiz = cadastrar_local(
        sessao,
        operador=admin,
        comunidade_id=comunidade.id,
        nivel=NivelDoLocal.comunidade.value,
        rotulo="Comunidade",
        local_pai_id=None,
    )
    bairro = cadastrar_local(
        sessao,
        operador=admin,
        comunidade_id=comunidade.id,
        nivel=NivelDoLocal.bairro.value,
        rotulo="Bairro",
        local_pai_id=raiz.id,
    )
    sessao.commit()

    assert bairro.local_pai_id == raiz.id
    assert bairro.comunidade_virtual_id == comunidade.id


def test_pai_de_nivel_que_nao_e_o_imediatamente_acima_e_recusado(sessao):
    admin = _criar_admin(sessao)
    comunidade = _criar_comunidade(sessao, admin)

    raiz = cadastrar_local(
        sessao,
        operador=admin,
        comunidade_id=comunidade.id,
        nivel=NivelDoLocal.comunidade.value,
        rotulo="Comunidade",
        local_pai_id=None,
    )
    rua = cadastrar_local(
        sessao,
        operador=admin,
        comunidade_id=comunidade.id,
        nivel=NivelDoLocal.bairro.value,
        rotulo="Bairro",
        local_pai_id=raiz.id,
    )
    rua = cadastrar_local(
        sessao,
        operador=admin,
        comunidade_id=comunidade.id,
        nivel=NivelDoLocal.rua.value,
        rotulo="Rua",
        local_pai_id=rua.id,
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_local(
            sessao,
            operador=admin,
            comunidade_id=comunidade.id,
            nivel=NivelDoLocal.quadra.value,
            rotulo="Quadra",
            local_pai_id=rua.id,
        )
    assert excinfo.value.campo == "local_pai_id"


def test_pai_de_outra_comunidade_e_recusado(sessao):
    admin = _criar_admin(sessao)
    comunidade_um = _criar_comunidade(sessao, admin, "Um")
    comunidade_dois = _criar_comunidade(sessao, admin, "Dois")

    raiz_um = cadastrar_local(
        sessao,
        operador=admin,
        comunidade_id=comunidade_um.id,
        nivel=NivelDoLocal.comunidade.value,
        rotulo="C1",
        local_pai_id=None,
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_local(
            sessao,
            operador=admin,
            comunidade_id=comunidade_dois.id,
            nivel=NivelDoLocal.bairro.value,
            rotulo="B",
            local_pai_id=raiz_um.id,
        )
    assert excinfo.value.campo == "local_pai_id"
    assert sessao.query(Local).filter_by(comunidade_virtual_id=comunidade_dois.id).count() == 0


def test_so_o_nivel_comunidade_existe_sem_pai(sessao):
    admin = _criar_admin(sessao)
    comunidade = _criar_comunidade(sessao, admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_local(
            sessao,
            operador=admin,
            comunidade_id=comunidade.id,
            nivel=NivelDoLocal.bairro.value,
            rotulo="Bairro",
            local_pai_id=None,
        )
    assert excinfo.value.campo == "local_pai_id"


def test_persona_que_nao_e_admin_nao_cadastra_local(sessao):
    admin = _criar_admin(sessao)
    comunidade = _criar_comunidade(sessao, admin)
    mestre = Persona(papel=Papel.mestre)
    sessao.add(mestre)
    sessao.flush()

    with pytest.raises(PermissaoNegada):
        cadastrar_local(
            sessao,
            operador=mestre,
            comunidade_id=comunidade.id,
            nivel=NivelDoLocal.comunidade.value,
            rotulo="C",
            local_pai_id=None,
        )
    assert sessao.query(Local).count() == 0


def test_comunidade_nasce_sem_local_e_ganha_os_que_o_admin_cadastra(sessao):
    admin = _criar_admin(sessao)
    comunidade = _criar_comunidade(sessao, admin)

    assert sessao.query(Local).filter_by(comunidade_virtual_id=comunidade.id).count() == 0

    cadastrar_local(
        sessao,
        operador=admin,
        comunidade_id=comunidade.id,
        nivel=NivelDoLocal.comunidade.value,
        rotulo="C",
        local_pai_id=None,
    )
    sessao.commit()

    assert sessao.query(Local).filter_by(comunidade_virtual_id=comunidade.id).count() == 1


def test_listagem_devolve_so_os_locais_da_comunidade_filtrada(sessao):
    admin = _criar_admin(sessao)
    comunidade_um = _criar_comunidade(sessao, admin, "Um")
    comunidade_dois = _criar_comunidade(sessao, admin, "Dois")

    cadastrar_local(
        sessao,
        operador=admin,
        comunidade_id=comunidade_um.id,
        nivel=NivelDoLocal.comunidade.value,
        rotulo="C1",
        local_pai_id=None,
    )
    cadastrar_local(
        sessao,
        operador=admin,
        comunidade_id=comunidade_dois.id,
        nivel=NivelDoLocal.comunidade.value,
        rotulo="C2",
        local_pai_id=None,
    )
    sessao.commit()

    pagina = paginar_locais(sessao, comunidade_id=comunidade_um.id, cursor=None, tamanho=10)

    assert len(pagina.itens) == 1
    assert pagina.itens[0].rotulo == "C1"
