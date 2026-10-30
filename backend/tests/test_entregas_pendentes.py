from decimal import Decimal

import pytest

from nucleo.erros import PermissaoNegada
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.personas.modelo import Papel
from nucleo.recompensas_de_marco.regra import listar_entregas_pendentes, registrar_entrega
from nucleo.recursos.modelo import NaturezaDoRecurso
from nucleo.trilhas.modelo import DesbloqueioDaMissao


def _desbloquear(sessao, *, guerreiro, missao, aprovado=True):
    desbloqueio = DesbloqueioDaMissao(
        guerreiro_id=guerreiro.id, missao_id=missao.id, aprovado=aprovado
    )
    sessao.add(desbloqueio)
    sessao.commit()
    return desbloqueio


@pytest.fixture
def cenario(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_lancamento,
    criar_vinculo_do_mestre,
    criar_trilha,
    criar_missao,
    criar_recompensa_de_marco,
):
    def _montar(*, quantidade=Decimal("1"), lastro=Decimal("10")):
        admin = criar_persona(Papel.admin)
        comunidade = criar_comunidade()
        ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
        tipo = criar_tipo_de_recurso(admin, natureza=NaturezaDoRecurso.consumivel)
        criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
        criar_lancamento(
            admin, tipo, ponto_de_apoio, natureza=NaturezaDoLancamento.credito, quantidade=lastro
        )

        mestre = criar_persona(Papel.mestre)
        criar_vinculo_do_mestre(mestre, comunidade)

        trilha = criar_trilha(mestre)
        missao = criar_missao(trilha, mestre)
        recompensa = criar_recompensa_de_marco(mestre, trilha, missao, tipo, quantidade=quantidade)

        guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)

        return {
            "admin": admin,
            "comunidade": comunidade,
            "ponto_de_apoio": ponto_de_apoio,
            "tipo": tipo,
            "mestre": mestre,
            "trilha": trilha,
            "missao": missao,
            "recompensa": recompensa,
            "guerreiro": guerreiro,
        }

    return _montar


def test_marco_desbloqueado_aparece_na_fila_do_mestre(sessao, cenario):
    c = cenario()
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"])

    pendencias = listar_entregas_pendentes(sessao, operador=c["mestre"])

    assert len(pendencias) == 1
    pendencia = pendencias[0]
    assert pendencia.guerreiro_id == c["guerreiro"].id
    assert pendencia.trilha_id == c["trilha"].id
    assert pendencia.trilha_nome == c["trilha"].nome
    assert pendencia.missao_id == c["missao"].id
    assert pendencia.missao_titulo == c["missao"].titulo
    assert pendencia.tipo_de_recurso_id == c["tipo"].id
    assert pendencia.quantidade == c["recompensa"].quantidade
    assert pendencia.quantidade_esgotada is False


def test_entrega_confirmada_sai_da_fila(sessao, cenario):
    c = cenario()
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"])
    registrar_entrega(
        sessao,
        operador=c["mestre"],
        recompensa=c["recompensa"],
        guerreiro=c["guerreiro"],
        ponto_de_apoio=c["ponto_de_apoio"],
    )
    sessao.commit()

    pendencias = listar_entregas_pendentes(sessao, operador=c["mestre"])

    assert pendencias == []


def test_fila_e_da_comunidade_nao_da_autoria(
    sessao, cenario, criar_persona, criar_vinculo_do_mestre
):
    c = cenario()
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"])
    outro_mestre = criar_persona(Papel.mestre)
    criar_vinculo_do_mestre(outro_mestre, c["comunidade"])

    pendencias = listar_entregas_pendentes(sessao, operador=outro_mestre)

    assert len(pendencias) == 1
    assert pendencias[0].guerreiro_id == c["guerreiro"].id


def test_guerreiro_de_outra_comunidade_nao_aparece(
    sessao, cenario, criar_persona, criar_comunidade
):
    c = cenario()
    outra_comunidade = criar_comunidade("Outra Comunidade")
    outro_guerreiro = criar_persona(Papel.guerreiro, comunidade=outra_comunidade)
    _desbloquear(sessao, guerreiro=outro_guerreiro, missao=c["missao"])

    pendencias = listar_entregas_pendentes(sessao, operador=c["mestre"])

    assert pendencias == []


def test_mestre_sem_vinculo_recebe_fila_vazia(sessao, criar_persona):
    mestre_sem_vinculo = criar_persona(Papel.mestre)

    pendencias = listar_entregas_pendentes(sessao, operador=mestre_sem_vinculo)

    assert pendencias == []


def test_quem_nao_e_mestre_nao_le_a_fila(sessao, cenario):
    c = cenario()

    with pytest.raises(PermissaoNegada):
        listar_entregas_pendentes(sessao, operador=c["guerreiro"])


def test_quantidade_esgotada_continua_na_fila_marcada(sessao, cenario, criar_persona):
    c = cenario(quantidade=Decimal("1"))
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"])
    registrar_entrega(
        sessao,
        operador=c["mestre"],
        recompensa=c["recompensa"],
        guerreiro=c["guerreiro"],
        ponto_de_apoio=c["ponto_de_apoio"],
    )
    sessao.commit()

    outro_guerreiro = criar_persona(Papel.guerreiro, comunidade=c["comunidade"])
    _desbloquear(sessao, guerreiro=outro_guerreiro, missao=c["missao"])

    pendencias = listar_entregas_pendentes(sessao, operador=c["mestre"])

    assert len(pendencias) == 1
    assert pendencias[0].guerreiro_id == outro_guerreiro.id
    assert pendencias[0].quantidade_esgotada is True


def test_desbloqueio_pratico_nao_julgado_nao_entra_na_fila(sessao, cenario):
    c = cenario()
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"], aprovado=None)

    pendencias = listar_entregas_pendentes(sessao, operador=c["mestre"])

    assert pendencias == []


def test_fila_nao_traz_custo(sessao, cliente, criar_chave, criar_sessao_de_teste, cenario):
    c = cenario()
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"])
    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(c["mestre"])

    resposta = cliente.get(
        "/v1/recompensas-de-marco/pendentes",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    assert "guerreiro_nick" in corpo[0]
    assert "guerreiro_avatar" in corpo[0]
    for chave_do_item in corpo[0]:
        assert "moeda" not in chave_do_item and "real" not in chave_do_item


def test_persona_que_nao_e_mestre_recebe_403_na_rota(
    cliente, criar_chave, criar_sessao_de_teste, criar_persona
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(
        "/v1/recompensas-de-marco/pendentes",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_fila_reune_as_pendencias_das_duas_comunidades_do_mestre(
    sessao, cenario, criar_vinculo_do_mestre
):
    """O plural que a spec já escrevia e o núcleo não servia: antes do
    vínculo próprio do Mestre, `operador.vinculo_vigente` resolvia sempre
    nulo e a fila saía vazia (decisão do fundador, 2026-10-30)."""
    c1 = cenario()
    c2 = cenario()
    # O mesmo Mestre atua nas duas comunidades.
    criar_vinculo_do_mestre(c1["mestre"], c2["comunidade"])

    _desbloquear(sessao, guerreiro=c1["guerreiro"], missao=c1["missao"])
    _desbloquear(sessao, guerreiro=c2["guerreiro"], missao=c2["missao"])
    sessao.commit()

    pendencias = listar_entregas_pendentes(sessao, operador=c1["mestre"])

    assert {p.guerreiro_id for p in pendencias} == {
        c1["guerreiro"].id,
        c2["guerreiro"].id,
    }


# --- A fila do encontro na App 01 (`RF-09-75`, fatia 31) -----------------------


def test_fila_da_aula_traz_so_quem_registrou_presenca(
    sessao, cenario, criar_persona, criar_aula, criar_presenca
):
    c = cenario()
    aula = criar_aula(c["admin"], c["comunidade"], ponto_de_apoio=c["ponto_de_apoio"])
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"])
    criar_presenca(aula, c["guerreiro"])

    ausente = criar_persona(Papel.guerreiro, comunidade=c["comunidade"])
    _desbloquear(sessao, guerreiro=ausente, missao=c["missao"])

    pendencias = listar_entregas_pendentes(sessao, operador=c["mestre"], aula_id=aula.id)

    assert [p.guerreiro_id for p in pendencias] == [c["guerreiro"].id]


def test_presenca_anulada_tira_a_pendencia_da_fila_da_aula(
    sessao, cenario, criar_aula, criar_presenca
):
    c = cenario()
    aula = criar_aula(c["admin"], c["comunidade"], ponto_de_apoio=c["ponto_de_apoio"])
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"])
    criar_presenca(aula, c["guerreiro"], confirmador=c["mestre"], anulada=True)

    pendencias = listar_entregas_pendentes(sessao, operador=c["mestre"], aula_id=aula.id)

    assert pendencias == []


def test_fila_sem_recorte_segue_sendo_das_comunidades(
    sessao, cenario, criar_persona, criar_aula, criar_presenca
):
    c = cenario()
    aula = criar_aula(c["admin"], c["comunidade"], ponto_de_apoio=c["ponto_de_apoio"])
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"])
    criar_presenca(aula, c["guerreiro"])

    sem_presenca = criar_persona(Papel.guerreiro, comunidade=c["comunidade"])
    _desbloquear(sessao, guerreiro=sem_presenca, missao=c["missao"])

    pendencias = listar_entregas_pendentes(sessao, operador=c["mestre"])

    assert {p.guerreiro_id for p in pendencias} == {c["guerreiro"].id, sem_presenca.id}


def test_fila_de_aula_de_outra_comunidade_e_recusada(sessao, cenario, criar_comunidade, criar_aula):
    c = cenario()
    outra_comunidade = criar_comunidade("Outra Comunidade")
    aula_de_fora = criar_aula(c["admin"], outra_comunidade)

    with pytest.raises(PermissaoNegada):
        listar_entregas_pendentes(sessao, operador=c["mestre"], aula_id=aula_de_fora.id)


def test_fila_do_encontro_por_rota(
    sessao, cliente, criar_chave, criar_sessao_de_teste, cenario, criar_aula, criar_presenca
):
    c = cenario()
    aula = criar_aula(c["admin"], c["comunidade"], ponto_de_apoio=c["ponto_de_apoio"])
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"])
    criar_presenca(aula, c["guerreiro"])
    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(c["mestre"])

    resposta = cliente.get(
        f"/v1/recompensas-de-marco/pendentes?aula_id={aula.id}",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [item["guerreiro_id"] for item in corpo] == [str(c["guerreiro"].id)]
