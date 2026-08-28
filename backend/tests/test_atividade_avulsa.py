import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from nucleo.atividades.regra import cadastrar_atividade_avulsa
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import Atividade, FormatoDeAtividade, ModalidadeDeAtividade
from nucleo.trilhas.regra import criar_atividade

# `RF-02-29`: a atividade avulsa é cadastrada por Admin, fora de trilha e
# sem missão, ancorada no poder que ela desenvolve.


def test_admin_cadastra_a_atividade_avulsa(sessao, criar_persona, criar_poder):
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin)

    atividade = cadastrar_atividade_avulsa(
        sessao,
        operador=admin,
        titulo="Mutirão de limpeza",
        modalidade=ModalidadeDeAtividade.em_equipe,
        formato=FormatoDeAtividade.presencial,
        natureza="meio ambiente",
        producao_esperada="Registro fotográfico do mutirão.",
        poder_id=poder.id,
    )
    sessao.commit()

    assert atividade.missao_id is None
    assert atividade.poder_id == poder.id
    assert atividade.autor_id == admin.id


def test_mestre_nao_cadastra_atividade_avulsa(sessao, criar_persona, criar_poder):
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre)

    with pytest.raises(PermissaoNegada):
        cadastrar_atividade_avulsa(
            sessao,
            operador=mestre,
            titulo="Mutirão de limpeza",
            modalidade=ModalidadeDeAtividade.em_equipe,
            formato=FormatoDeAtividade.presencial,
            natureza="meio ambiente",
            producao_esperada="Registro fotográfico do mutirão.",
            poder_id=poder.id,
        )
    assert sessao.query(Atividade).count() == 0


def test_cadastro_sem_producao_esperada_e_recusado(sessao, criar_persona, criar_poder):
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_atividade_avulsa(
            sessao,
            operador=admin,
            titulo="Mutirão de limpeza",
            modalidade=ModalidadeDeAtividade.em_equipe,
            formato=FormatoDeAtividade.presencial,
            natureza="meio ambiente",
            producao_esperada=None,
            poder_id=poder.id,
        )
    assert excinfo.value.campo == "producao_esperada"
    assert sessao.query(Atividade).count() == 0


def test_modalidade_fora_dos_valores_previstos_e_recusada(sessao, criar_persona, criar_poder):
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_atividade_avulsa(
            sessao,
            operador=admin,
            titulo="Mutirão de limpeza",
            modalidade="modalidade-inexistente",
            formato=FormatoDeAtividade.presencial,
            natureza="meio ambiente",
            producao_esperada="Registro fotográfico do mutirão.",
            poder_id=poder.id,
        )
    assert excinfo.value.campo == "modalidade"
    assert sessao.query(Atividade).count() == 0


def test_atividade_avulsa_sem_poder_e_recusada(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_atividade_avulsa(
            sessao,
            operador=admin,
            titulo="Mutirão de limpeza",
            modalidade=ModalidadeDeAtividade.em_equipe,
            formato=FormatoDeAtividade.presencial,
            natureza="meio ambiente",
            producao_esperada="Registro fotográfico do mutirão.",
            poder_id=None,
        )
    assert excinfo.value.campo == "poder_id"
    assert sessao.query(Atividade).count() == 0


def test_poder_inexistente_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_atividade_avulsa(
            sessao,
            operador=admin,
            titulo="Mutirão de limpeza",
            modalidade=ModalidadeDeAtividade.em_equipe,
            formato=FormatoDeAtividade.presencial,
            natureza="meio ambiente",
            producao_esperada="Registro fotográfico do mutirão.",
            poder_id=uuid.uuid4(),
        )
    assert excinfo.value.campo == "poder_id"
    assert sessao.query(Atividade).count() == 0


def test_atividade_com_missao_e_poder_e_recusada_pelo_banco(
    sessao, criar_persona, criar_trilha, criar_missao, criar_poder
):
    """A âncora é garantida no esquema, não só na regra — nem
    `cadastrar_atividade_avulsa` nem `criar_atividade` aceitam declarar as
    duas ao mesmo tempo; o `CheckConstraint` é quem recusa quem tentar
    pelo ORM direto (design — decisões 2)."""
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    poder = criar_poder(mestre)

    atividade = Atividade(
        missao_id=missao.id,
        poder_id=poder.id,
        titulo="Atividade inválida",
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Produção de teste.",
        autor_id=mestre.id,
        papel_do_autor=mestre.papel.value,
    )
    sessao.add(atividade)
    with pytest.raises(IntegrityError):
        sessao.flush()
    sessao.rollback()


def test_atividade_sem_missao_nem_poder_e_recusada_pelo_banco(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    atividade = Atividade(
        missao_id=None,
        poder_id=None,
        titulo="Atividade inválida",
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Produção de teste.",
        autor_id=mestre.id,
        papel_do_autor=mestre.papel.value,
    )
    sessao.add(atividade)
    with pytest.raises(IntegrityError):
        sessao.flush()
    sessao.rollback()


def test_atividade_de_trilha_segue_exigindo_missao_e_nunca_declara_poder(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`trilhas.regra.criar_atividade` continua recusando atividade sem
    missão e nunca grava `poder_id` — a âncora da atividade de trilha
    continua sendo só a missão (design — decisões 1, 2)."""
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=None,
            titulo="Atividade de Teste",
            modalidade=ModalidadeDeAtividade.individual,
            formato=FormatoDeAtividade.presencial,
            natureza="construcao",
            producao_esperada="Produção de teste.",
        )
    assert excinfo.value.campo == "missao_id"

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Atividade de Teste",
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Produção de teste.",
    )
    sessao.commit()
    assert atividade.poder_id is None
