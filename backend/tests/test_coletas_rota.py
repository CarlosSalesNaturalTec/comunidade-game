import uuid
from datetime import UTC, datetime, timedelta

from nucleo.coletas.modelo import Cadencia, FormaDeRegistro, SerieDeColeta
from nucleo.comunidades.modelo import VinculoJogador
from nucleo.locais.modelo import NivelDoLocal
from nucleo.personas.modelo import Papel

INICIO = "2026-01-01T00:00:00-03:00"
FIM = "2026-12-31T00:00:00-03:00"
MOMENTO_DA_MEDICAO = "2026-07-08T14:00:00-03:00"


def test_admin_cadastra_tipo_de_coleta_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/tipos-de-coleta",
        json={
            "nome": "Temperatura",
            "forma_de_registro": FormaDeRegistro.numero.value,
            "unidade": "°C",
            "faixa_minima": -10,
            "faixa_maxima": 55,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == "Temperatura"
    assert corpo["ativo"] is True


def test_mestre_recebe_403_ao_cadastrar_tipo_de_coleta_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/tipos-de-coleta",
        json={"nome": "Temperatura", "forma_de_registro": FormaDeRegistro.numero.value},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_mestre_autor_cria_desafio_de_coleta_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/desafios-de-coleta",
        json={
            "missao_id": str(missao.id),
            "tipo_de_coleta_id": str(tipo.id),
            "cadencia": Cadencia.semanal.value,
            "vigencia_inicio": INICIO,
            "vigencia_fim": FIM,
            "granularidade_exigida": NivelDoLocal.rua.value,
            "registros_que_pontuam_por_periodo": 1,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["missao_id"] == str(missao.id)
    assert corpo["tipo_de_coleta_id"] == str(tipo.id)


def test_mestre_que_nao_e_autor_recebe_403_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
):
    chave, _ = criar_chave()
    autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(autor)
    missao = criar_missao(trilha, autor)
    tipo = criar_tipo_de_coleta(autor)
    token, _ = criar_sessao_de_teste(outro_mestre)

    resposta = cliente.post(
        "/v1/desafios-de-coleta",
        json={
            "missao_id": str(missao.id),
            "tipo_de_coleta_id": str(tipo.id),
            "cadencia": Cadencia.semanal.value,
            "vigencia_inicio": INICIO,
            "vigencia_fim": FIM,
            "granularidade_exigida": NivelDoLocal.rua.value,
            "registros_que_pontuam_por_periodo": 1,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_desafio_com_etiqueta_ods_declarada_e_recusado(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
):
    """A etiqueta ODS é derivada da missão ou da trilha, nunca declarada
    pelo Mestre — o contrato de entrada nem sequer tem o campo, e o
    `extra="forbid"` recusa qualquer tentativa (`RF-08-25`)."""
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/desafios-de-coleta",
        json={
            "missao_id": str(missao.id),
            "tipo_de_coleta_id": str(tipo.id),
            "cadencia": Cadencia.semanal.value,
            "vigencia_inicio": INICIO,
            "vigencia_fim": FIM,
            "granularidade_exigida": NivelDoLocal.rua.value,
            "registros_que_pontuam_por_periodo": 1,
            "etiqueta_ods": 4,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422


def _preparar_serie_pela_rota(
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
        vigencia_inicio="2026-01-01T00:00:00+00:00",
        vigencia_fim="2026-12-31T00:00:00+00:00",
    )
    # `criar_comunidade` nasce com granularidade máxima "bairro" — o mesmo
    # teto exigido pelo desafio acima.
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    # A medição do teste é datada no passado simulado; recua o início do
    # vínculo, que nasce em `server_default=func.now()`, para que aquela
    # data caia dentro do intervalo vigente (`RN-08-03`).
    vinculo = sessao.query(VinculoJogador).filter_by(guerreiro_id=guerreiro.id).one()
    vinculo.data_inicio = datetime(2025, 1, 1, tzinfo=UTC)
    sessao.commit()
    local_da_comunidade = criar_local(
        comunidade, nivel=NivelDoLocal.comunidade, rotulo="Território"
    )
    local = criar_local(
        comunidade, nivel=NivelDoLocal.bairro, rotulo="Bairro", local_pai=local_da_comunidade
    )

    token, _ = criar_sessao_de_teste(guerreiro)
    return chave, token, guerreiro, desafio, local


def test_guerreiro_abre_serie_de_coleta_pela_rota(
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
    chave, token, _, desafio, local = _preparar_serie_pela_rota(
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
    )

    resposta = cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(desafio.id), "local_id": str(local.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["desafio_de_coleta_id"] == str(desafio.id)
    assert corpo["local_id"] == str(local.id)
    assert corpo["estado"] == "ativa"


def test_mestre_recebe_403_ao_abrir_serie_de_coleta_pela_rota(
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
    chave, _, _, desafio, local = _preparar_serie_pela_rota(
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
    )
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(desafio.id), "local_id": str(local.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_coletor_grava_registro_de_coleta_pela_rota(
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
    chave, token, guerreiro, desafio, local = _preparar_serie_pela_rota(
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
    )
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    resposta_serie = cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(desafio.id), "local_id": str(local.id)},
        headers=headers,
    )
    serie_id = resposta_serie.json()["id"]

    resposta = cliente.post(
        "/v1/registros-de-coleta",
        data={
            "serie_de_coleta_id": serie_id,
            "momento_do_fato": MOMENTO_DA_MEDICAO,
            "origem": "manual",
            "valor": "25.0",
            "unidade": "°C",
        },
        headers=headers,
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["serie_de_coleta_id"] == serie_id
    assert corpo["pontos_creditados"] == 5
    assert corpo["pontuou"] is True


def test_mestre_recebe_403_ao_consultar_series_do_guerreiro_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/series-de-coleta/minhas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_guerreiro_consulta_suas_series_pela_rota(
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
    """Ponta a ponta do critério de aceite do PRD-08 §12: série sem
    registro por dois períodos de cadência aparece `interrompida` e para
    de creditar; o registro seguinte a devolve para `ativa` (`RF-08-10`,
    `RF-08-11`, `RF-08-17`)."""
    chave, token, guerreiro, desafio, local = _preparar_serie_pela_rota(
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
    )
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    resposta_serie = cliente.post(
        "/v1/series-de-coleta",
        json={"desafio_de_coleta_id": str(desafio.id), "local_id": str(local.id)},
        headers=headers,
    )
    serie_id = resposta_serie.json()["id"]

    serie = sessao.get(SerieDeColeta, uuid.UUID(serie_id))
    serie.aberta_em = datetime.now(UTC) - timedelta(weeks=3)
    sessao.commit()

    resposta_interrompida = cliente.get("/v1/series-de-coleta/minhas", headers=headers)
    assert resposta_interrompida.status_code == 200
    corpo_interrompido = resposta_interrompida.json()
    assert len(corpo_interrompido) == 1
    assert corpo_interrompido[0]["id"] == serie_id
    assert corpo_interrompido[0]["estado"] == "interrompida"
    assert corpo_interrompido[0]["pontos"] == 0

    resposta_registro = cliente.post(
        "/v1/registros-de-coleta",
        data={
            "serie_de_coleta_id": serie_id,
            "momento_do_fato": datetime.now(UTC).isoformat(),
            "origem": "manual",
            "valor": "25.0",
            "unidade": "°C",
        },
        headers=headers,
    )
    assert resposta_registro.status_code == 201

    resposta_ativa = cliente.get("/v1/series-de-coleta/minhas", headers=headers)
    corpo_ativo = resposta_ativa.json()
    assert corpo_ativo[0]["estado"] == "ativa"
    assert corpo_ativo[0]["pontos"] > 0
