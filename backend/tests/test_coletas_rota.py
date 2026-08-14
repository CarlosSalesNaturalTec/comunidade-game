from nucleo.coletas.modelo import Cadencia, FormaDeRegistro
from nucleo.locais.modelo import NivelDoLocal
from nucleo.personas.modelo import Papel

INICIO = "2026-01-01T00:00:00-03:00"
FIM = "2026-12-31T00:00:00-03:00"


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
