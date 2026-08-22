from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nucleo.aulas.regra import cancelar_aula
from nucleo.erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from nucleo.livro_razao.regra import lancar_credito, saldo_de, transferir_saldo
from nucleo.personas.modelo import Papel
from nucleo.pontos_de_apoio.modelo import PontoDeApoio
from nucleo.pontos_de_apoio.regra import (
    cadastrar_ponto_de_apoio,
    desativar_ponto_de_apoio,
    designar_responsavel,
    reativar_ponto_de_apoio,
)


def test_admin_cadastra_ponto_de_apoio_com_autoria_gravada(sessao, criar_persona, criar_comunidade):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()

    ponto_de_apoio = cadastrar_ponto_de_apoio(
        sessao, operador=admin, nome="Sede", comunidade_id=comunidade.id
    )
    sessao.commit()

    assert ponto_de_apoio.nome == "Sede"
    assert ponto_de_apoio.comunidade_virtual_id == comunidade.id
    assert ponto_de_apoio.responsavel_id is None
    assert ponto_de_apoio.ativo is True
    assert ponto_de_apoio.autor_id == admin.id
    assert ponto_de_apoio.papel_do_autor == Papel.admin.value


def test_mestre_nao_cadastra_ponto_de_apoio(sessao, criar_persona, criar_comunidade):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()

    with pytest.raises(PermissaoNegada):
        cadastrar_ponto_de_apoio(sessao, operador=mestre, nome="Sede", comunidade_id=comunidade.id)
    assert sessao.query(PontoDeApoio).count() == 0


def test_ponto_de_apoio_sem_nome_e_recusado(sessao, criar_persona, criar_comunidade):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_ponto_de_apoio(sessao, operador=admin, nome=None, comunidade_id=comunidade.id)
    assert excinfo.value.campo == "nome"
    assert sessao.query(PontoDeApoio).count() == 0


def test_ponto_de_apoio_sem_comunidade_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_ponto_de_apoio(sessao, operador=admin, nome="Sede", comunidade_id=None)
    assert excinfo.value.campo == "comunidade_id"
    assert sessao.query(PontoDeApoio).count() == 0


def test_ponto_de_apoio_de_comunidade_inexistente_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_ponto_de_apoio(sessao, operador=admin, nome="Sede", comunidade_id=admin.id)
    assert excinfo.value.campo == "comunidade_id"
    assert sessao.query(PontoDeApoio).count() == 0


def test_ponto_de_apoio_nasce_sem_responsavel(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()

    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    assert ponto_de_apoio.responsavel_id is None


def test_admin_designa_mestre_como_responsavel(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    mestre = criar_persona(Papel.mestre)

    resultado = designar_responsavel(sessao, ponto_de_apoio, operador=admin, responsavel=mestre)
    sessao.commit()

    assert resultado.responsavel_id == mestre.id


def test_apoiador_pode_ser_designado_responsavel(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    apoiador = criar_persona(Papel.apoiador)

    resultado = designar_responsavel(sessao, ponto_de_apoio, operador=admin, responsavel=apoiador)
    sessao.commit()

    assert resultado.responsavel_id == apoiador.id


def test_guerreiro_nao_e_designado_responsavel(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        designar_responsavel(sessao, ponto_de_apoio, operador=admin, responsavel=guerreiro)
    assert excinfo.value.campo == "responsavel_id"
    assert ponto_de_apoio.responsavel_id is None


def test_responsavel_familiar_nao_e_designado_responsavel_pelo_acervo(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        designar_responsavel(sessao, ponto_de_apoio, operador=admin, responsavel=responsavel)
    assert excinfo.value.campo == "responsavel_id"
    assert ponto_de_apoio.responsavel_id is None


def test_troca_do_responsavel_substitui_o_anterior(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    primeiro = criar_persona(Papel.mestre)
    segundo = criar_persona(Papel.apoiador)

    designar_responsavel(sessao, ponto_de_apoio, operador=admin, responsavel=primeiro)
    sessao.commit()

    resultado = designar_responsavel(sessao, ponto_de_apoio, operador=admin, responsavel=segundo)
    sessao.commit()

    assert resultado.responsavel_id == segundo.id


def test_mestre_nao_designa_responsavel(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    mestre = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        designar_responsavel(sessao, ponto_de_apoio, operador=mestre, responsavel=outro_mestre)
    assert ponto_de_apoio.responsavel_id is None


def test_designacao_em_ponto_de_apoio_inexistente_e_recusada(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(NaoEncontrado):
        designar_responsavel(sessao, None, operador=admin, responsavel=mestre)


def test_admin_le_pontos_de_apoio_filtrado_por_comunidade(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    outra_comunidade = criar_comunidade("Outra Comunidade")
    criar_ponto_de_apoio(admin, comunidade, nome="Sede")
    criar_ponto_de_apoio(admin, outra_comunidade, nome="Sede de Outra Comunidade")
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/pontos-de-apoio",
        params={"comunidade": str(comunidade.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    assert corpo["itens"][0]["nome"] == "Sede"


def test_mestre_le_apenas_pontos_de_apoio_do_seu_vinculo(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_vinculo_jogador,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    outra_comunidade = criar_comunidade("Outra Comunidade")
    criar_ponto_de_apoio(admin, comunidade, nome="Sede")
    criar_ponto_de_apoio(admin, outra_comunidade, nome="Sede de Outra Comunidade")
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/pontos-de-apoio",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    assert corpo["itens"][0]["nome"] == "Sede"


def test_guerreiro_recebe_403_ao_ler_pontos_de_apoio(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade
):
    chave, _ = criar_chave()
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(
        "/v1/pontos-de-apoio",
        params={"comunidade": str(comunidade.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_ponto_de_apoio_sem_responsavel_vem_na_leitura(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    criar_ponto_de_apoio(admin, comunidade)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/pontos-de-apoio",
        params={"comunidade": str(comunidade.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    assert corpo["itens"][0]["responsavel_id"] is None


def test_listagem_de_pontos_de_apoio_sem_filtro_de_comunidade_e_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/pontos-de-apoio",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422


def test_admin_desativa_ponto_de_apoio_gravando_motivo_e_autoria(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    resultado = desativar_ponto_de_apoio(
        sessao, ponto_de_apoio, operador=admin, motivo="Fechou o espaço."
    )
    sessao.commit()

    assert resultado.ativo is False
    assert resultado.motivo_da_situacao == "Fechou o espaço."
    assert resultado.autor_da_situacao_id == admin.id
    assert resultado.papel_do_autor_da_situacao == Papel.admin.value
    assert resultado.situacao_alterada_em is not None


def test_admin_reativa_ponto_de_apoio(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    desativar_ponto_de_apoio(sessao, ponto_de_apoio, operador=admin, motivo="Fechou o espaço.")
    sessao.commit()

    resultado = reativar_ponto_de_apoio(
        sessao, ponto_de_apoio, operador=admin, motivo="Reabriu o espaço."
    )
    sessao.commit()

    assert resultado.ativo is True
    assert resultado.motivo_da_situacao == "Reabriu o espaço."


def test_mestre_nao_desativa_ponto_de_apoio(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    with pytest.raises(PermissaoNegada):
        desativar_ponto_de_apoio(sessao, ponto_de_apoio, operador=mestre, motivo="Fechou o espaço.")
    assert ponto_de_apoio.ativo is True


def test_desativacao_sem_motivo_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        desativar_ponto_de_apoio(sessao, ponto_de_apoio, operador=admin, motivo=None)
    assert excinfo.value.campo == "motivo"
    assert ponto_de_apoio.ativo is True


def test_desativar_ponto_ja_inativo_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    desativar_ponto_de_apoio(sessao, ponto_de_apoio, operador=admin, motivo="Fechou o espaço.")
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        desativar_ponto_de_apoio(sessao, ponto_de_apoio, operador=admin, motivo="De novo.")
    assert excinfo.value.campo == "ativo"


def test_reativar_ponto_ja_ativo_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        reativar_ponto_de_apoio(sessao, ponto_de_apoio, operador=admin, motivo="Já está ativo.")
    assert excinfo.value.campo == "ativo"


def test_aula_passada_continua_apontando_o_ponto_desativado(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_aula
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    passado = datetime.now(UTC) - timedelta(days=2)
    aula_passada = criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=passado,
        fim_em=passado + timedelta(hours=1),
    )

    resultado = desativar_ponto_de_apoio(
        sessao, ponto_de_apoio, operador=admin, motivo="Fechou o espaço."
    )
    sessao.commit()
    sessao.refresh(aula_passada)

    assert resultado.ativo is False
    assert aula_passada.ponto_de_apoio_id == ponto_de_apoio.id


def test_ponto_de_apoio_com_aula_futura_nao_e_desativado(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_aula
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    futuro = datetime.now(UTC) + timedelta(days=1)
    criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=futuro,
        fim_em=futuro + timedelta(hours=1),
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        desativar_ponto_de_apoio(sessao, ponto_de_apoio, operador=admin, motivo="Fechou o espaço.")
    assert excinfo.value.campo == "aulas_futuras"
    assert "1" in excinfo.value.mensagem
    assert ponto_de_apoio.ativo is True


def test_aula_ja_realizada_ou_cancelada_nao_bloqueia(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_aula
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    passado = datetime.now(UTC) - timedelta(days=1)
    criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=passado,
        fim_em=passado + timedelta(hours=1),
    )
    futuro = datetime.now(UTC) + timedelta(days=1)
    aula_cancelada = criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=futuro,
        fim_em=futuro + timedelta(hours=1),
    )
    cancelar_aula(sessao, operador=admin, aula=aula_cancelada, motivo="Não vai mais acontecer.")
    sessao.commit()

    resultado = desativar_ponto_de_apoio(
        sessao, ponto_de_apoio, operador=admin, motivo="Fechou o espaço."
    )
    sessao.commit()

    assert resultado.ativo is False


def test_cancelada_a_aula_a_desativacao_passa(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_aula
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    futuro = datetime.now(UTC) + timedelta(days=1)
    aula = criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=futuro,
        fim_em=futuro + timedelta(hours=1),
    )

    with pytest.raises(ErroDeValidacao):
        desativar_ponto_de_apoio(sessao, ponto_de_apoio, operador=admin, motivo="Fechou o espaço.")

    cancelar_aula(sessao, operador=admin, aula=aula, motivo="Não vai mais acontecer.")
    sessao.commit()

    resultado = desativar_ponto_de_apoio(
        sessao, ponto_de_apoio, operador=admin, motivo="Fechou o espaço."
    )
    sessao.commit()

    assert resultado.ativo is False


def test_ponto_de_apoio_com_saldo_nao_e_desativado(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        desativar_ponto_de_apoio(sessao, ponto_de_apoio, operador=admin, motivo="Fechou o espaço.")
    assert excinfo.value.campo == "saldo"
    assert tipo.nome in excinfo.value.mensagem
    assert ponto_de_apoio.ativo is True


def test_transferido_o_saldo_a_desativacao_passa(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    origem = criar_ponto_de_apoio(admin, comunidade, nome="Origem")
    destino = criar_ponto_de_apoio(admin, comunidade, nome="Destino")
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=origem.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    transferir_saldo(
        sessao,
        operador=admin,
        tipo_de_recurso=tipo,
        ponto_de_apoio_origem=origem,
        ponto_de_apoio_destino=destino,
        quantidade=Decimal("3.00"),
        motivo="Esvazia para desativar.",
    )
    sessao.commit()

    resultado = desativar_ponto_de_apoio(sessao, origem, operador=admin, motivo="Fechou o espaço.")
    sessao.commit()

    assert resultado.ativo is False


def test_saldo_nao_e_zerado_ao_recusar_a_desativacao(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        desativar_ponto_de_apoio(sessao, ponto_de_apoio, operador=admin, motivo="Fechou o espaço.")

    saldo = saldo_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id)
    assert saldo == Decimal("3.00")
