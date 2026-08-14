import pytest

from nucleo.comunidades.modelo import ComunidadeVirtual, VinculoJogador
from nucleo.comunidades.regra import abrir_vinculo, criar_comunidade
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.locais.modelo import Local
from nucleo.personas.modelo import Papel, Persona


def _criar_admin(sessao) -> Persona:
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    return admin


def test_admin_cria_comunidade_que_nasce_vazia(sessao):
    admin = _criar_admin(sessao)

    comunidade = criar_comunidade(
        sessao,
        operador=admin,
        nome="Comunidade Nova",
        localizacao="Bairro Novo",
        granularidade_maxima="bairro",
    )
    sessao.commit()

    assert comunidade.admin_criador_id == admin.id
    assert comunidade.criada_em is not None
    assert sessao.query(Local).filter_by(comunidade_virtual_id=comunidade.id).count() == 0
    assert sessao.query(VinculoJogador).filter_by(comunidade_virtual_id=comunidade.id).count() == 0


def test_persona_que_nao_e_admin_nao_cria_comunidade(sessao):
    mestre = Persona(papel=Papel.mestre)
    sessao.add(mestre)
    sessao.flush()

    with pytest.raises(PermissaoNegada):
        criar_comunidade(
            sessao,
            operador=mestre,
            nome="X",
            localizacao="Y",
            granularidade_maxima="bairro",
        )
    assert sessao.query(ComunidadeVirtual).count() == 0


@pytest.mark.parametrize("campo_em_falta", ["nome", "localizacao", "granularidade_maxima"])
def test_comunidade_sem_atributo_declarado_e_recusada(sessao, campo_em_falta):
    admin = _criar_admin(sessao)
    valores = {"nome": "N", "localizacao": "L", "granularidade_maxima": "bairro"}
    valores[campo_em_falta] = None

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_comunidade(sessao, operador=admin, **valores)
    assert excinfo.value.campo == campo_em_falta
    assert sessao.query(ComunidadeVirtual).count() == 0


def test_segundo_vinculo_vigente_e_recusado_e_o_existente_permanece(sessao):
    admin = _criar_admin(sessao)
    comunidade_um = criar_comunidade(
        sessao, operador=admin, nome="Um", localizacao="L", granularidade_maxima="bairro"
    )
    comunidade_dois = criar_comunidade(
        sessao, operador=admin, nome="Dois", localizacao="L", granularidade_maxima="bairro"
    )
    guerreiro = Persona(papel=Papel.guerreiro)
    sessao.add(guerreiro)
    sessao.flush()

    vinculo = abrir_vinculo(sessao, guerreiro=guerreiro, comunidade_id=comunidade_um.id)
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        abrir_vinculo(sessao, guerreiro=guerreiro, comunidade_id=comunidade_dois.id)

    vigente = sessao.query(VinculoJogador).filter_by(guerreiro_id=guerreiro.id, data_fim=None).one()
    assert vigente.id == vinculo.id
    assert vigente.comunidade_virtual_id == comunidade_um.id


def test_vinculo_so_vale_para_guerreiro(sessao):
    admin = _criar_admin(sessao)
    comunidade = criar_comunidade(
        sessao, operador=admin, nome="C", localizacao="L", granularidade_maxima="bairro"
    )

    with pytest.raises(ErroDeValidacao):
        abrir_vinculo(sessao, guerreiro=admin, comunidade_id=comunidade.id)
