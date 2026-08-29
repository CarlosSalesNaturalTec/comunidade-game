import pytest

from nucleo.coletas.modelo import FormaDeRegistro, TipoDeColeta
from nucleo.coletas.regra import (
    alterar_tipo_de_coleta,
    cadastrar_tipo_de_coleta,
    consultar_tipos_de_coleta,
    desativar_tipo_de_coleta,
)
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel


def test_admin_cadastra_tipo_de_coleta_por_numero(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    tipo = cadastrar_tipo_de_coleta(
        sessao,
        operador=admin,
        nome="Temperatura",
        forma_de_registro=FormaDeRegistro.numero.value,
        unidade="°C",
        faixa_minima=-10,
        faixa_maxima=55,
    )
    sessao.commit()

    assert tipo.autor_id == admin.id
    assert tipo.papel_do_autor == Papel.admin.value
    assert tipo.registrado_em is not None
    assert tipo.ativo is True
    assert tipo.unidade == "°C"
    assert tipo.faixa_minima == -10
    assert tipo.faixa_maxima == 55


def test_admin_cadastra_tipo_de_coleta_por_foto_sem_unidade_e_faixa(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    tipo = cadastrar_tipo_de_coleta(
        sessao,
        operador=admin,
        nome="Buraco na via",
        forma_de_registro=FormaDeRegistro.foto.value,
    )
    sessao.commit()

    assert tipo.unidade is None
    assert tipo.faixa_minima is None
    assert tipo.faixa_maxima is None


def test_mestre_nao_cadastra_tipo_de_coleta(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        cadastrar_tipo_de_coleta(
            sessao,
            operador=mestre,
            nome="Temperatura",
            forma_de_registro=FormaDeRegistro.numero.value,
            unidade="°C",
            faixa_minima=-10,
            faixa_maxima=55,
        )
    assert sessao.query(TipoDeColeta).count() == 0


def test_mestre_nao_altera_nem_desativa_tipo_de_coleta(sessao, criar_persona, criar_tipo_de_coleta):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    tipo = criar_tipo_de_coleta(admin)

    with pytest.raises(PermissaoNegada):
        alterar_tipo_de_coleta(sessao, tipo, operador=mestre, nome="Novo nome")
    with pytest.raises(PermissaoNegada):
        desativar_tipo_de_coleta(sessao, tipo, operador=mestre)

    sessao.refresh(tipo)
    assert tipo.nome != "Novo nome"
    assert tipo.ativo is True


def test_tipo_sem_nome_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_tipo_de_coleta(
            sessao,
            operador=admin,
            nome="",
            forma_de_registro=FormaDeRegistro.numero.value,
            unidade="°C",
            faixa_minima=-10,
            faixa_maxima=55,
        )
    assert excinfo.value.campo == "nome"
    assert sessao.query(TipoDeColeta).count() == 0


def test_forma_de_registro_fora_da_lista_e_recusada(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_tipo_de_coleta(
            sessao,
            operador=admin,
            nome="Barulho",
            forma_de_registro="audio",
        )
    assert excinfo.value.campo == "forma_de_registro"
    assert sessao.query(TipoDeColeta).count() == 0


def test_tipo_por_numero_sem_unidade_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_tipo_de_coleta(
            sessao,
            operador=admin,
            nome="Temperatura",
            forma_de_registro=FormaDeRegistro.numero.value,
            faixa_minima=-10,
            faixa_maxima=55,
        )
    assert excinfo.value.campo == "unidade"
    assert sessao.query(TipoDeColeta).count() == 0


def test_tipo_por_numero_sem_faixa_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_tipo_de_coleta(
            sessao,
            operador=admin,
            nome="Temperatura",
            forma_de_registro=FormaDeRegistro.numero.value,
            unidade="°C",
        )
    assert excinfo.value.campo == "faixa_minima"
    assert sessao.query(TipoDeColeta).count() == 0


def test_faixa_invertida_e_recusada(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_tipo_de_coleta(
            sessao,
            operador=admin,
            nome="Temperatura",
            forma_de_registro=FormaDeRegistro.numero.value,
            unidade="°C",
            faixa_minima=55,
            faixa_maxima=-10,
        )
    assert excinfo.value.campo == "faixa_minima"
    assert sessao.query(TipoDeColeta).count() == 0


def test_tipo_por_evidencia_com_unidade_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_tipo_de_coleta(
            sessao,
            operador=admin,
            nome="Buraco na via",
            forma_de_registro=FormaDeRegistro.foto.value,
            unidade="cm",
        )
    assert excinfo.value.campo == "unidade"
    assert sessao.query(TipoDeColeta).count() == 0


def test_admin_desativa_tipo_de_coleta(sessao, criar_persona, criar_tipo_de_coleta):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_coleta(admin)

    desativar_tipo_de_coleta(sessao, tipo, operador=admin)
    sessao.commit()
    sessao.refresh(tipo)

    assert tipo.ativo is False


def test_admin_altera_o_nome_do_tipo_de_coleta(sessao, criar_persona, criar_tipo_de_coleta):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_coleta(admin, nome="Nome original")

    alterar_tipo_de_coleta(sessao, tipo, operador=admin, nome="Nome revisado")
    sessao.commit()
    sessao.refresh(tipo)

    assert tipo.nome == "Nome revisado"


def test_alterar_tipo_de_coleta_para_nome_vazio_e_recusado(
    sessao, criar_persona, criar_tipo_de_coleta
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_coleta(admin, nome="Nome original")

    with pytest.raises(ErroDeValidacao) as excinfo:
        alterar_tipo_de_coleta(sessao, tipo, operador=admin, nome="   ")
    assert excinfo.value.campo == "nome"
    sessao.refresh(tipo)
    assert tipo.nome == "Nome original"


def test_mestre_le_o_catalogo_para_escolher_o_tipo(sessao, criar_persona, criar_tipo_de_coleta):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    criar_tipo_de_coleta(admin, nome="Temperatura")

    pagina = consultar_tipos_de_coleta(sessao, operador=mestre, cursor=None, tamanho=10)

    assert len(pagina.itens) == 1
    item = pagina.itens[0]
    assert item.nome == "Temperatura"
    assert item.forma_de_registro == FormaDeRegistro.numero.value
    assert item.unidade == "°C"
    assert item.faixa_minima == -10
    assert item.faixa_maxima == 55
    assert item.ativo is True


def test_tipo_por_evidencia_sai_sem_unidade_e_sem_faixa(
    sessao, criar_persona, criar_tipo_de_coleta
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    criar_tipo_de_coleta(
        admin,
        nome="Buraco na via",
        forma_de_registro=FormaDeRegistro.foto,
        unidade=None,
        faixa_minima=None,
        faixa_maxima=None,
    )

    pagina = consultar_tipos_de_coleta(sessao, operador=mestre, cursor=None, tamanho=10)

    item = pagina.itens[0]
    assert item.unidade is None
    assert item.faixa_minima is None
    assert item.faixa_maxima is None


def test_tipo_desativado_sai_assinalado(sessao, criar_persona, criar_tipo_de_coleta):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    criar_tipo_de_coleta(admin, nome="Descontinuado", ativo=False)

    pagina = consultar_tipos_de_coleta(sessao, operador=mestre, cursor=None, tamanho=10)

    assert pagina.itens[0].ativo is False


def test_admin_le_o_mesmo_catalogo(sessao, criar_persona, criar_tipo_de_coleta):
    admin = criar_persona(Papel.admin)
    criar_tipo_de_coleta(admin, nome="Temperatura")

    pagina = consultar_tipos_de_coleta(sessao, operador=admin, cursor=None, tamanho=10)

    assert len(pagina.itens) == 1


@pytest.mark.parametrize("papel", [Papel.guerreiro, Papel.responsavel, Papel.apoiador])
def test_papel_que_nao_escolhe_nem_cadastra_e_recusado(sessao, criar_persona, papel):
    persona = criar_persona(papel)

    with pytest.raises(PermissaoNegada):
        consultar_tipos_de_coleta(sessao, operador=persona, cursor=None, tamanho=10)
