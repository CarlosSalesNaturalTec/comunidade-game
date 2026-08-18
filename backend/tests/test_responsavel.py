import threading
import uuid
from datetime import UTC, datetime

import pytest
from sqlalchemy.orm import sessionmaker

from nucleo.erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from nucleo.personas.modelo import Papel, Persona
from nucleo.responsaveis.modelo import VinculoResponsavel
from nucleo.responsaveis.regra import (
    cadastrar_responsavel,
    criar_vinculo,
    exigir_vinculo_do_responsavel,
    guerreiros_vinculados,
)


def test_admin_cadastra_responsavel_sem_criar_acesso_a_ninguem(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    assert responsavel.papel == Papel.responsavel
    assert guerreiros_vinculados(sessao, responsavel.id) == []


def test_mestre_cadastra_responsavel(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=mestre)
    assert responsavel.papel == Papel.responsavel


def test_apoiador_nao_cadastra_responsavel(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    with pytest.raises(PermissaoNegada):
        cadastrar_responsavel(sessao, criado_por=apoiador)


def test_vinculo_grava_grau_quem_cadastrou_e_inicio(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)

    vinculo = criar_vinculo(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        grau_de_parentesco="mãe",
        cadastrado_por=admin,
    )
    sessao.commit()

    assert vinculo.grau_de_parentesco == "mãe"
    assert vinculo.autor_id == admin.id
    assert vinculo.papel_do_autor == Papel.admin.value
    assert vinculo.inicio is not None
    assert vinculo.fim is None


def test_vinculo_sem_grau_de_parentesco_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_vinculo(
            sessao,
            responsavel=responsavel,
            guerreiro_id=guerreiro.id,
            grau_de_parentesco="   ",
            cadastrado_por=admin,
        )
    assert excinfo.value.campo == "grau_de_parentesco"
    assert sessao.query(VinculoResponsavel).count() == 0


def test_vinculo_a_guerreiro_inexistente_e_recusado_sem_criar_persona(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    total_personas_antes = sessao.query(Persona).count()

    with pytest.raises(NaoEncontrado):
        criar_vinculo(
            sessao,
            responsavel=responsavel,
            guerreiro_id=uuid.uuid4(),
            grau_de_parentesco="mãe",
            cadastrado_por=admin,
        )

    assert sessao.query(Persona).count() == total_personas_antes
    assert sessao.query(VinculoResponsavel).count() == 0


def test_quarto_vinculo_e_recusado_e_os_tres_permanecem_validos(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    graus = ["mãe", "pai", "avó"]
    responsaveis = [cadastrar_responsavel(sessao, criado_por=admin) for _ in range(4)]

    for responsavel, grau in zip(responsaveis[:3], graus, strict=True):
        criar_vinculo(
            sessao,
            responsavel=responsavel,
            guerreiro_id=guerreiro.id,
            grau_de_parentesco=grau,
            cadastrado_por=admin,
        )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_vinculo(
            sessao,
            responsavel=responsaveis[3],
            guerreiro_id=guerreiro.id,
            grau_de_parentesco="tio",
            cadastrado_por=admin,
        )
    assert excinfo.value.campo == "guerreiro_id"

    vinculos = (
        sessao.query(VinculoResponsavel)
        .filter_by(guerreiro_id=guerreiro.id, fim=None)
        .order_by(VinculoResponsavel.grau_de_parentesco)
        .all()
    )
    assert sorted(v.grau_de_parentesco for v in vinculos) == sorted(graus)
    assert len(vinculos) == 3


def test_teto_conta_por_guerreiro_nao_por_responsavel(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiros = [criar_persona(Papel.guerreiro) for _ in range(4)]

    for guerreiro in guerreiros:
        vinculo = criar_vinculo(
            sessao,
            responsavel=responsavel,
            guerreiro_id=guerreiro.id,
            grau_de_parentesco="mãe",
            cadastrado_por=admin,
        )
        assert vinculo is not None
    sessao.commit()

    assert sessao.query(VinculoResponsavel).filter_by(responsavel_id=responsavel.id).count() == 4


def test_vinculo_encerrado_abre_vaga_para_novo_responsavel(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    responsavel_um = cadastrar_responsavel(sessao, criado_por=admin)
    responsavel_dois = cadastrar_responsavel(sessao, criado_por=admin)
    responsavel_tres_encerrado = cadastrar_responsavel(sessao, criado_por=admin)
    responsavel_novo = cadastrar_responsavel(sessao, criado_por=admin)

    criar_vinculo(
        sessao,
        responsavel=responsavel_um,
        guerreiro_id=guerreiro.id,
        grau_de_parentesco="mãe",
        cadastrado_por=admin,
    )
    criar_vinculo(
        sessao,
        responsavel=responsavel_dois,
        guerreiro_id=guerreiro.id,
        grau_de_parentesco="pai",
        cadastrado_por=admin,
    )
    vinculo_encerrado = criar_vinculo(
        sessao,
        responsavel=responsavel_tres_encerrado,
        guerreiro_id=guerreiro.id,
        grau_de_parentesco="avó",
        cadastrado_por=admin,
    )
    vinculo_encerrado.fim = datetime.now(UTC)
    sessao.commit()

    vinculo_novo = criar_vinculo(
        sessao,
        responsavel=responsavel_novo,
        guerreiro_id=guerreiro.id,
        grau_de_parentesco="tia",
        cadastrado_por=admin,
    )
    assert vinculo_novo is not None
    assert (
        sessao.query(VinculoResponsavel).filter_by(guerreiro_id=guerreiro.id, fim=None).count() == 3
    )


def test_guerreiros_vinculados_traz_so_os_vigentes_do_responsavel(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiro_vinculado = criar_persona(Papel.guerreiro)
    guerreiro_nao_vinculado = criar_persona(Papel.guerreiro)

    criar_vinculo(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro_vinculado.id,
        grau_de_parentesco="mãe",
        cadastrado_por=admin,
    )

    alcancados = guerreiros_vinculados(sessao, responsavel.id)
    assert alcancados == [guerreiro_vinculado.id]
    assert guerreiro_nao_vinculado.id not in alcancados


def test_responsavel_recem_cadastrado_nao_enxerga_ninguem(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    assert guerreiros_vinculados(sessao, responsavel.id) == []


def test_exigir_vinculo_do_responsavel_nega_sem_vinculo_vigente(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)

    with pytest.raises(PermissaoNegada):
        exigir_vinculo_do_responsavel(
            sessao,
            papel=Papel.responsavel,
            responsavel_id=responsavel.id,
            guerreiro_id=guerreiro.id,
        )


def test_exigir_vinculo_do_responsavel_libera_com_vinculo_vigente(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro.id,
        grau_de_parentesco="mãe",
        cadastrado_por=admin,
    )

    exigir_vinculo_do_responsavel(
        sessao, papel=Papel.responsavel, responsavel_id=responsavel.id, guerreiro_id=guerreiro.id
    )


def test_exigir_vinculo_do_responsavel_nao_amplia_por_comunidade(
    sessao, criar_persona, criar_comunidade
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    responsavel = cadastrar_responsavel(sessao, criado_por=admin)
    guerreiro_da_comunidade = criar_persona(Papel.guerreiro, comunidade=comunidade)
    outro_guerreiro_da_mesma_comunidade = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_vinculo(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro_da_comunidade.id,
        grau_de_parentesco="mãe",
        cadastrado_por=admin,
    )

    with pytest.raises(PermissaoNegada):
        exigir_vinculo_do_responsavel(
            sessao,
            papel=Papel.responsavel,
            responsavel_id=responsavel.id,
            guerreiro_id=outro_guerreiro_da_mesma_comunidade.id,
        )


def test_exigir_vinculo_do_responsavel_deixa_outros_papeis_passarem(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    exigir_vinculo_do_responsavel(
        sessao, papel=Papel.admin, responsavel_id=admin.id, guerreiro_id=guerreiro.id
    )


@pytest.mark.banco_compartilhado
def test_duas_criacoes_simultaneas_do_terceiro_vinculo_nao_passam_as_duas(
    engine, sessao, criar_persona
):
    """Trava a linha do Guerreiro(a) antes de contar (design — decisões):
    partindo de dois vínculos vigentes, duas tentativas concorrentes do
    terceiro só podem deixar uma passar. Precisa de dado realmente
    gravado — duas conexões reais concorrendo — por isso o marcador
    `banco_compartilhado` (design.md — Decisions 4)."""
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    responsavel_um = cadastrar_responsavel(sessao, criado_por=admin)
    responsavel_dois = cadastrar_responsavel(sessao, criado_por=admin)
    responsavel_tres = cadastrar_responsavel(sessao, criado_por=admin)
    responsavel_quatro = cadastrar_responsavel(sessao, criado_por=admin)

    criar_vinculo(
        sessao,
        responsavel=responsavel_um,
        guerreiro_id=guerreiro.id,
        grau_de_parentesco="mãe",
        cadastrado_por=admin,
    )
    criar_vinculo(
        sessao,
        responsavel=responsavel_dois,
        guerreiro_id=guerreiro.id,
        grau_de_parentesco="pai",
        cadastrado_por=admin,
    )
    sessao.commit()

    fabrica = sessionmaker(bind=engine, expire_on_commit=False)
    resultados: dict[str, str] = {}

    def _tentar(nome: str, responsavel_id: uuid.UUID) -> None:
        sessao_da_tarefa = fabrica()
        try:
            responsavel = sessao_da_tarefa.get(Persona, responsavel_id)
            admin_da_tarefa = sessao_da_tarefa.get(Persona, admin.id)
            criar_vinculo(
                sessao_da_tarefa,
                responsavel=responsavel,
                guerreiro_id=guerreiro.id,
                grau_de_parentesco="tio",
                cadastrado_por=admin_da_tarefa,
            )
            sessao_da_tarefa.commit()
            resultados[nome] = "sucesso"
        except ErroDeValidacao:
            sessao_da_tarefa.rollback()
            resultados[nome] = "recusado"
        finally:
            sessao_da_tarefa.close()

    tarefas = [
        threading.Thread(target=_tentar, args=("tres", responsavel_tres.id)),
        threading.Thread(target=_tentar, args=("quatro", responsavel_quatro.id)),
    ]
    for tarefa in tarefas:
        tarefa.start()
    for tarefa in tarefas:
        tarefa.join()

    assert sorted(resultados.values()) == ["recusado", "sucesso"]
    assert (
        sessao.query(VinculoResponsavel).filter_by(guerreiro_id=guerreiro.id, fim=None).count() == 3
    )
