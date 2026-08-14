from datetime import UTC, datetime

from nucleo.comunidades.modelo import VinculoJogador
from nucleo.locais.modelo import NivelDoLocal
from nucleo.personas.modelo import Papel

INICIO = "2026-01-01T00:00:00-03:00"
FIM = "2026-12-31T00:00:00-03:00"
MOMENTO_DA_MEDICAO = "2026-07-08T14:00:00-03:00"


def _preparar_serie_com_credencial(
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    cliente,
):
    """Chave, token do Mestre autor, série aberta pelo Guerreiro(a) e o
    identificador dela — o estado de que toda rota de credencial de
    dispositivo desta suíte parte."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    criar_poder_do_territorio(admin)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(admin)
    desafio = criar_desafio_de_coleta(
        missao,
        mestre,
        tipo=tipo,
        granularidade_exigida=NivelDoLocal.bairro,
        vigencia_inicio=INICIO,
        vigencia_fim=FIM,
    )
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    vinculo = sessao.query(VinculoJogador).filter_by(guerreiro_id=guerreiro.id).one()
    vinculo.data_inicio = datetime(2025, 1, 1, tzinfo=UTC)
    sessao.commit()
    local_da_comunidade = criar_local(
        comunidade, nivel=NivelDoLocal.comunidade, rotulo="Território"
    )
    local = criar_local(
        comunidade, nivel=NivelDoLocal.bairro, rotulo="Bairro", local_pai=local_da_comunidade
    )

    token_guerreiro, _ = criar_sessao_de_teste(guerreiro)
    resposta_serie = cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(desafio.id), "local_id": str(local.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_guerreiro}"},
    )
    serie_id = resposta_serie.json()["id"]

    token_mestre, _ = criar_sessao_de_teste(mestre)
    token_admin, _ = criar_sessao_de_teste(admin)
    return {
        "chave": chave,
        "admin": admin,
        "mestre": mestre,
        "trilha": trilha,
        "desafio": desafio,
        "comunidade": comunidade,
        "local_da_comunidade": local_da_comunidade,
        "guerreiro": guerreiro,
        "serie_id": serie_id,
        "token_guerreiro": token_guerreiro,
        "token_mestre": token_mestre,
        "token_admin": token_admin,
    }


def _preparar(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    return _preparar_serie_com_credencial(
        sessao,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        cliente,
    )


def test_admin_emite_credencial_de_dispositivo_pela_rota(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    estado = _preparar(
        sessao,
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )

    resposta = cliente.post(
        "/v1/credenciais/dispositivo",
        json={
            "serie_de_coleta_id": estado["serie_id"],
            "identificador": "sensor-01",
            "trilha_id": str(estado["trilha"].id),
        },
        headers={
            "X-Chave-Aplicacao": estado["chave"],
            "Authorization": f"Bearer {estado['token_admin']}",
        },
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["identificador"] == "sensor-01"
    assert "segredo" in corpo and corpo["segredo"]


def test_mestre_que_nao_e_autor_recebe_403_ao_emitir_pela_rota(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    estado = _preparar(
        sessao,
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    outro_mestre = criar_persona(Papel.mestre)
    token_outro, _ = criar_sessao_de_teste(outro_mestre)

    resposta = cliente.post(
        "/v1/credenciais/dispositivo",
        json={
            "serie_de_coleta_id": estado["serie_id"],
            "identificador": "sensor-01",
            "trilha_id": str(estado["trilha"].id),
        },
        headers={"X-Chave-Aplicacao": estado["chave"], "Authorization": f"Bearer {token_outro}"},
    )

    assert resposta.status_code == 403


def test_guerreiro_recebe_403_ao_emitir_pela_rota(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    estado = _preparar(
        sessao,
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )

    resposta = cliente.post(
        "/v1/credenciais/dispositivo",
        json={
            "serie_de_coleta_id": estado["serie_id"],
            "identificador": "sensor-01",
            "trilha_id": str(estado["trilha"].id),
        },
        headers={
            "X-Chave-Aplicacao": estado["chave"],
            "Authorization": f"Bearer {estado['token_guerreiro']}",
        },
    )

    assert resposta.status_code == 403


def _emitir(cliente, estado, token=None, identificador="sensor-01"):
    resposta = cliente.post(
        "/v1/credenciais/dispositivo",
        json={
            "serie_de_coleta_id": estado["serie_id"],
            "identificador": identificador,
            "trilha_id": str(estado["trilha"].id),
        },
        headers={
            "X-Chave-Aplicacao": estado["chave"],
            "Authorization": f"Bearer {token or estado['token_mestre']}",
        },
    )
    corpo = resposta.json()
    return corpo["id"], f"{corpo['identificador']}.{corpo['segredo']}"


def test_mestre_revoga_credencial_pela_rota(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    estado = _preparar(
        sessao,
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    credencial_id, _ = _emitir(cliente, estado)

    resposta = cliente.request(
        "DELETE",
        f"/v1/credenciais/dispositivo/{credencial_id}",
        json={"motivo": "Fim da coleta."},
        headers={
            "X-Chave-Aplicacao": estado["chave"],
            "Authorization": f"Bearer {estado['token_mestre']}",
        },
    )

    assert resposta.status_code == 204


def test_revogar_sem_motivo_e_422(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    estado = _preparar(
        sessao,
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    credencial_id, _ = _emitir(cliente, estado)

    resposta = cliente.request(
        "DELETE",
        f"/v1/credenciais/dispositivo/{credencial_id}",
        json={"motivo": ""},
        headers={
            "X-Chave-Aplicacao": estado["chave"],
            "Authorization": f"Bearer {estado['token_mestre']}",
        },
    )

    assert resposta.status_code == 422


def test_sensor_grava_registro_pela_rota_com_credencial_de_dispositivo(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    estado = _preparar(
        sessao,
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    _, credencial_completa = _emitir(cliente, estado)

    resposta = cliente.post(
        "/v1/registros-de-coleta",
        data={
            "serie_de_coleta_id": estado["serie_id"],
            "momento_do_fato": MOMENTO_DA_MEDICAO,
            "origem": "sensor",
            "valor": "25.0",
            "unidade": "°C",
        },
        headers={
            "X-Chave-Aplicacao": estado["chave"],
            "X-Credencial-Dispositivo": credencial_completa,
        },
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["origem"] == "sensor"
    assert corpo["serie_de_coleta_id"] == estado["serie_id"]
    assert "segredo" not in str(corpo)


def test_sensor_com_segredo_errado_e_recusado(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    estado = _preparar(
        sessao,
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    _emitir(cliente, estado)

    resposta = cliente.post(
        "/v1/registros-de-coleta",
        data={
            "serie_de_coleta_id": estado["serie_id"],
            "momento_do_fato": MOMENTO_DA_MEDICAO,
            "origem": "sensor",
            "valor": "25.0",
            "unidade": "°C",
        },
        headers={
            "X-Chave-Aplicacao": estado["chave"],
            "X-Credencial-Dispositivo": "sensor-01.segredo-errado",
        },
    )

    assert resposta.status_code == 401
    assert resposta.json()["codigo"] == "credencial_de_dispositivo_invalida"


def test_credencial_revogada_e_recusada_na_chamada_seguinte(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    estado = _preparar(
        sessao,
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    credencial_id, credencial_completa = _emitir(cliente, estado)
    cliente.request(
        "DELETE",
        f"/v1/credenciais/dispositivo/{credencial_id}",
        json={"motivo": "Revogada para o teste."},
        headers={
            "X-Chave-Aplicacao": estado["chave"],
            "Authorization": f"Bearer {estado['token_mestre']}",
        },
    )

    resposta = cliente.post(
        "/v1/registros-de-coleta",
        data={
            "serie_de_coleta_id": estado["serie_id"],
            "momento_do_fato": MOMENTO_DA_MEDICAO,
            "origem": "sensor",
            "valor": "25.0",
            "unidade": "°C",
        },
        headers={
            "X-Chave-Aplicacao": estado["chave"],
            "X-Credencial-Dispositivo": credencial_completa,
        },
    )

    assert resposta.status_code == 401


def test_sensor_sem_chave_de_aplicacao_e_401(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    estado = _preparar(
        sessao,
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    _, credencial_completa = _emitir(cliente, estado)

    resposta = cliente.post(
        "/v1/registros-de-coleta",
        data={
            "serie_de_coleta_id": estado["serie_id"],
            "momento_do_fato": MOMENTO_DA_MEDICAO,
            "origem": "sensor",
            "valor": "25.0",
            "unidade": "°C",
        },
        headers={"X-Credencial-Dispositivo": credencial_completa},
    )

    assert resposta.status_code == 401


def test_credencial_de_dispositivo_nao_alcanca_rota_de_consulta(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    """Não há sessão nem papel: uma rota que espera persona nunca reconhece
    o cabeçalho de dispositivo — a chamada é recusada como se não houvesse
    autenticação alguma (`RN-08-23`, `RN-01-34`)."""
    estado = _preparar(
        sessao,
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    _, credencial_completa = _emitir(cliente, estado)

    resposta = cliente.get(
        "/v1/chaves",
        headers={
            "X-Chave-Aplicacao": estado["chave"],
            "X-Credencial-Dispositivo": credencial_completa,
        },
    )

    assert resposta.status_code == 401


def test_credencial_de_dispositivo_nao_alcanca_outra_rota_de_escrita(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    estado = _preparar(
        sessao,
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    _, credencial_completa = _emitir(cliente, estado)

    # `/v1/tipos-de-coleta` é rota de escrita restrita ao Admin, autenticada
    # por sessão de persona — o cabeçalho de dispositivo não é reconhecido
    # ali, e sem `Authorization` a chamada é recusada como sem autenticação.
    resposta = cliente.post(
        "/v1/tipos-de-coleta",
        json={"nome": "Umidade", "forma_de_registro": "numero", "unidade": "%"},
        headers={
            "X-Chave-Aplicacao": estado["chave"],
            "X-Credencial-Dispositivo": credencial_completa,
        },
    )

    assert resposta.status_code == 401


def test_registro_em_outra_serie_e_recusado(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    estado = _preparar(
        sessao,
        cliente,
        criar_chave,
        criar_persona,
        criar_comunidade,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    _, credencial_completa = _emitir(cliente, estado)

    # Uma segunda série, do mesmo desafio, em outro local da mesma
    # comunidade — a credencial da primeira série não a alcança.
    outro_local = criar_local(
        estado["comunidade"],
        nivel=NivelDoLocal.bairro,
        rotulo="Outro bairro",
        local_pai=estado["local_da_comunidade"],
    )
    resposta_outra_serie = cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(estado["desafio"].id), "local_id": str(outro_local.id)},
        headers={
            "X-Chave-Aplicacao": estado["chave"],
            "Authorization": f"Bearer {estado['token_guerreiro']}",
        },
    )
    outra_serie_id = resposta_outra_serie.json()["id"]

    resposta = cliente.post(
        "/v1/registros-de-coleta",
        data={
            "serie_de_coleta_id": outra_serie_id,
            "momento_do_fato": MOMENTO_DA_MEDICAO,
            "origem": "sensor",
            "valor": "25.0",
            "unidade": "°C",
        },
        headers={
            "X-Chave-Aplicacao": estado["chave"],
            "X-Credencial-Dispositivo": credencial_completa,
        },
    )

    assert resposta.status_code == 401
