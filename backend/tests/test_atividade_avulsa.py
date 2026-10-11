import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from nucleo.atividades.regra import cadastrar_atividade_avulsa, listar_atividades_avulsas
from nucleo.aulas.modelo import Aula, SituacaoDaAula
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import Atividade, FormatoDeAtividade, ModalidadeDeAtividade
from nucleo.trilhas.regra import criar_atividade

# `RF-02-29`: a atividade avulsa é cadastrada por Admin, fora de trilha e
# sem missão, ancorada no poder que ela desenvolve.


def test_admin_cadastra_a_atividade_avulsa(
    sessao, criar_persona, criar_poder, criar_comunidade, criar_aula
):
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin)
    aula = criar_aula(admin, criar_comunidade())

    atividade = cadastrar_atividade_avulsa(
        sessao,
        operador=admin,
        titulo="Mutirão de limpeza",
        modalidade=ModalidadeDeAtividade.em_equipe,
        formato=FormatoDeAtividade.presencial,
        natureza="meio ambiente",
        producao_esperada="Registro fotográfico do mutirão.",
        poder_id=poder.id,
        aula_id=aula.id,
    )
    sessao.commit()

    assert atividade.missao_id is None
    assert atividade.poder_id == poder.id
    assert atividade.autor_id == admin.id


def test_mestre_nao_cadastra_atividade_avulsa(
    sessao, criar_persona, criar_poder, criar_comunidade, criar_aula
):
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre)
    aula = criar_aula(mestre, criar_comunidade())

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
            aula_id=aula.id,
        )
    assert sessao.query(Atividade).count() == 0


def test_cadastro_sem_producao_esperada_e_recusado(
    sessao, criar_persona, criar_poder, criar_comunidade, criar_aula
):
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin)
    aula = criar_aula(admin, criar_comunidade())

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
            aula_id=aula.id,
        )
    assert excinfo.value.campo == "producao_esperada"
    assert sessao.query(Atividade).count() == 0


def test_modalidade_fora_dos_valores_previstos_e_recusada(
    sessao, criar_persona, criar_poder, criar_comunidade, criar_aula
):
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin)
    aula = criar_aula(admin, criar_comunidade())

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
            aula_id=aula.id,
        )
    assert excinfo.value.campo == "modalidade"
    assert sessao.query(Atividade).count() == 0


def test_atividade_avulsa_sem_poder_e_recusada(sessao, criar_persona, criar_comunidade, criar_aula):
    admin = criar_persona(Papel.admin)
    aula = criar_aula(admin, criar_comunidade())

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
            aula_id=aula.id,
        )
    assert excinfo.value.campo == "poder_id"
    assert sessao.query(Atividade).count() == 0


def test_poder_inexistente_e_recusado(sessao, criar_persona, criar_comunidade, criar_aula):
    admin = criar_persona(Papel.admin)
    aula = criar_aula(admin, criar_comunidade())

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
            aula_id=aula.id,
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


# `RF-02-29`, documento 11 §4: a avulsa declara a aula do encontro em que
# acontece e, por isso, é sempre presencial.


def test_cadastro_sem_aula_e_recusado(sessao, criar_persona, criar_poder):
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
            producao_esperada="Registro fotográfico do mutirão.",
            poder_id=poder.id,
            aula_id=None,
        )
    assert excinfo.value.campo == "aula_id"
    assert sessao.query(Atividade).count() == 0


def test_aula_inexistente_e_recusada(sessao, criar_persona, criar_poder):
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
            producao_esperada="Registro fotográfico do mutirão.",
            poder_id=poder.id,
            aula_id=uuid.uuid4(),
        )
    assert excinfo.value.campo == "aula_id"
    assert sessao.query(Atividade).count() == 0


def test_aula_cancelada_e_recusada(
    sessao, criar_persona, criar_poder, criar_comunidade, criar_aula
):
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin)
    aula = criar_aula(admin, criar_comunidade())
    aula.situacao = SituacaoDaAula.cancelada
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_atividade_avulsa(
            sessao,
            operador=admin,
            titulo="Mutirão de limpeza",
            modalidade=ModalidadeDeAtividade.em_equipe,
            formato=FormatoDeAtividade.presencial,
            natureza="meio ambiente",
            producao_esperada="Registro fotográfico do mutirão.",
            poder_id=poder.id,
            aula_id=aula.id,
        )
    assert excinfo.value.campo == "aula_id"
    assert sessao.query(Atividade).count() == 0


def test_formato_on_line_e_recusado_na_avulsa(
    sessao, criar_persona, criar_poder, criar_comunidade, criar_aula
):
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin)
    aula = criar_aula(admin, criar_comunidade())

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_atividade_avulsa(
            sessao,
            operador=admin,
            titulo="Mutirão de limpeza",
            modalidade=ModalidadeDeAtividade.em_equipe,
            formato=FormatoDeAtividade.on_line_assincrona,
            natureza="meio ambiente",
            producao_esperada="Registro fotográfico do mutirão.",
            poder_id=poder.id,
            aula_id=aula.id,
        )
    assert excinfo.value.campo == "formato"
    assert sessao.query(Atividade).count() == 0


def test_a_comunidade_da_avulsa_e_a_da_aula(
    sessao, criar_persona, criar_poder, criar_comunidade, criar_aula
):
    """Não há campo de comunidade: a avulsa a deriva da aula declarada
    (documento 09 §1)."""
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    atividade = cadastrar_atividade_avulsa(
        sessao,
        operador=admin,
        titulo="Mutirão de limpeza",
        modalidade=ModalidadeDeAtividade.em_equipe,
        formato=FormatoDeAtividade.presencial,
        natureza="meio ambiente",
        producao_esperada="Registro fotográfico do mutirão.",
        poder_id=poder.id,
        aula_id=aula.id,
    )
    sessao.commit()

    assert atividade.aula_id == aula.id
    assert sessao.get(Aula, atividade.aula_id).comunidade_virtual_id == comunidade.id


# `RF-02-112`: o filtro por aula é o caminho da área Lançamentos até as
# avulsas da aula vigente.


def test_a_lista_filtrada_traz_so_as_avulsas_da_aula(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_atividade_avulsa
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    outra_aula = criar_aula(admin, comunidade)
    uma = criar_atividade_avulsa(admin, aula=aula, titulo="Uma")
    outra = criar_atividade_avulsa(admin, aula=aula, titulo="Outra")
    criar_atividade_avulsa(admin, aula=outra_aula, titulo="De outra aula")

    da_aula = listar_atividades_avulsas(sessao, aula_id=aula.id)

    assert {atividade.id for atividade in da_aula} == {uma.id, outra.id}


def test_sem_filtro_a_lista_traz_todas(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_atividade_avulsa
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    uma = criar_atividade_avulsa(admin, aula=criar_aula(admin, comunidade), titulo="Uma")
    outra = criar_atividade_avulsa(admin, aula=criar_aula(admin, comunidade), titulo="Outra")

    todas = listar_atividades_avulsas(sessao)

    assert {atividade.id for atividade in todas} == {uma.id, outra.id}


def test_aula_sem_avulsa_devolve_lista_vazia(sessao, criar_persona, criar_comunidade, criar_aula):
    admin = criar_persona(Papel.admin)
    aula = criar_aula(admin, criar_comunidade())

    assert listar_atividades_avulsas(sessao, aula_id=aula.id) == []
