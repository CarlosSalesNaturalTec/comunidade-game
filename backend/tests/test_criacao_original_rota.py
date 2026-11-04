from nucleo.culminancias.modelo import ModalidadeDaCulminancia
from nucleo.personas.modelo import Papel


def _cabecalhos(chave, criar_sessao_de_teste, persona):
    token, _ = criar_sessao_de_teste(persona)
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def test_entrega_em_equipe_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_culminancia,
    criar_equipe,
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)

    resposta = cliente.post(
        f"/v1/culminancias/{culminancia.id}/criacoes",
        json={"equipe_id": str(equipe.id), "tipo": "texto", "producao": "Nosso robô."},
        headers=cabecalhos,
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["trilha_id"] == str(trilha.id)
    assert corpo["equipe_id"] == str(equipe.id)
    assert corpo["situacao"] == "entregue"


def test_entrega_individual_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_culminancia
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.individual)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)

    resposta = cliente.post(
        f"/v1/culminancias/{culminancia.id}/criacoes",
        json={"tipo": "texto", "producao": "Meu diário."},
        headers=cabecalhos,
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["guerreiro_id"] == str(guerreiro.id)
    assert corpo["equipe_id"] is None


def test_entrega_em_culminancia_inexistente_e_recusada(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    import uuid

    guerreiro = criar_persona(Papel.guerreiro)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)

    resposta = cliente.post(
        f"/v1/culminancias/{uuid.uuid4()}/criacoes",
        json={"tipo": "texto", "producao": "Produção."},
        headers=cabecalhos,
    )

    assert resposta.status_code == 404


def test_mestre_nao_entrega_criacao_original(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_culminancia
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.individual)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)

    resposta = cliente.post(
        f"/v1/culminancias/{culminancia.id}/criacoes",
        json={"tipo": "texto", "producao": "Produção."},
        headers=cabecalhos,
    )

    assert resposta.status_code == 403


def test_minha_criacao_da_trilha_reflete_a_situacao_atual(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_culminancia
):
    """`RF-05-40`, `RF-05-42`: a App 05 relê a própria entrega, com motivo
    de devolução, mesmo depois de reabrir a aplicação."""
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.individual)
    chave, _ = criar_chave()
    cabecalhos_guerreiro = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)

    resposta_sem_entrega = cliente.get(
        f"/v1/eu/trilhas/{trilha.id}/criacao", headers=cabecalhos_guerreiro
    )
    assert resposta_sem_entrega.status_code == 404

    cliente.post(
        f"/v1/culminancias/{culminancia.id}/criacoes",
        json={"tipo": "texto", "producao": "Meu diário."},
        headers=cabecalhos_guerreiro,
    )

    resposta = cliente.get(f"/v1/eu/trilhas/{trilha.id}/criacao", headers=cabecalhos_guerreiro)
    assert resposta.status_code == 200
    assert resposta.json()["situacao"] == "entregue"


def test_sessao_de_midia_e_aberta_para_criacao_de_imagem(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_culminancia
):
    guerreiro = criar_persona(Papel.guerreiro)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.individual)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)

    resposta_entrega = cliente.post(
        f"/v1/culminancias/{culminancia.id}/criacoes",
        json={"tipo": "imagem"},
        headers=cabecalhos,
    )
    assert resposta_entrega.status_code == 201
    criacao_id = resposta_entrega.json()["id"]

    resposta = cliente.post(
        f"/v1/criacoes/{criacao_id}/arquivo",
        json={"tipo_mime": "image/png", "tamanho_declarado": 10},
        headers=cabecalhos,
    )

    assert resposta.status_code == 201
    assert resposta.json()["endereco_da_sessao"].startswith("/v1/armazenamento/sessoes/")


def test_portfolio_traz_apenas_as_criacoes_validadas_do_proprio_guerreiro(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_criacao_original,
):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    outro_guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(admin)

    criar_criacao_original(trilha, admin, guerreiro=guerreiro)
    criar_criacao_original(trilha, admin, guerreiro=outro_guerreiro)

    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)

    resposta = cliente.get("/v1/eu/portfolio", headers=cabecalhos)

    assert resposta.status_code == 200
    itens = resposta.json()
    assert len(itens) == 1
    assert itens[0]["publica"] is False


def test_fila_do_mestre_autor_nao_alcanca_trilha_de_outro_mestre(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_culminancia,
    criar_equipe,
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre_autor)
    culminancia = criar_culminancia(
        trilha, mestre_autor, modalidade=ModalidadeDaCulminancia.em_equipe
    )
    equipe = criar_equipe(guerreiro, trilha=trilha)
    chave, _ = criar_chave()
    cabecalhos_guerreiro = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)
    cliente.post(
        f"/v1/culminancias/{culminancia.id}/criacoes",
        json={"equipe_id": str(equipe.id), "tipo": "texto", "producao": "Nosso robô."},
        headers=cabecalhos_guerreiro,
    )

    cabecalhos_autor = _cabecalhos(chave, criar_sessao_de_teste, mestre_autor)
    resposta_autor = cliente.get("/v1/criacoes/fila", headers=cabecalhos_autor)
    assert resposta_autor.status_code == 200
    assert len(resposta_autor.json()) == 1

    cabecalhos_outro = _cabecalhos(chave, criar_sessao_de_teste, outro_mestre)
    resposta_outro = cliente.get("/v1/criacoes/fila", headers=cabecalhos_outro)
    assert resposta_outro.status_code == 200
    assert resposta_outro.json() == []


def test_fila_traz_trilha_criterio_e_o_papel_de_cada_integrante(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_sessao_de_teste,
    criar_trilha,
    criar_culminancia,
    criar_equipe,
):
    """`RF-09-31`, `RF-09-32`: a fila traz o critério que o próprio Mestre
    declarou e, na modalidade de equipe, o papel de cada integrante."""
    mestre = criar_persona(Papel.mestre)
    criador = criar_persona(Papel.guerreiro)
    criar_nick(criador, "criadora")
    colega = criar_persona(Papel.guerreiro)
    criar_nick(colega, "colega")
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(
        trilha,
        mestre,
        modalidade=ModalidadeDaCulminancia.em_equipe,
        criterio_de_validacao="Precisa funcionar de verdade.",
    )
    equipe = criar_equipe(criador, trilha=trilha)

    chave, _ = criar_chave()
    cabecalhos_criador = _cabecalhos(chave, criar_sessao_de_teste, criador)
    cliente.post(
        f"/v1/equipes/{equipe.id}/integrantes",
        json={"papel": "quem testou"},
        headers=_cabecalhos(chave, criar_sessao_de_teste, colega),
    )
    cliente.post(
        f"/v1/culminancias/{culminancia.id}/criacoes",
        json={"equipe_id": str(equipe.id), "tipo": "texto", "producao": "Nosso robô."},
        headers=cabecalhos_criador,
    )

    resposta = cliente.get(
        "/v1/criacoes/fila", headers=_cabecalhos(chave, criar_sessao_de_teste, mestre)
    )

    assert resposta.status_code == 200
    item = resposta.json()[0]
    assert item["trilha_nome"] == trilha.nome
    assert item["criterio_de_validacao"] == "Precisa funcionar de verdade."
    autores_por_nick = {autor["nick"]: autor["papel"] for autor in item["autores"]}
    assert autores_por_nick == {"criadora": None, "colega": "quem testou"}


def test_mestre_autor_valida_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_culminancia,
    criar_equipe,
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    chave, _ = criar_chave()
    cabecalhos_guerreiro = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)
    resposta_entrega = cliente.post(
        f"/v1/culminancias/{culminancia.id}/criacoes",
        json={"equipe_id": str(equipe.id), "tipo": "texto", "producao": "Nosso robô."},
        headers=cabecalhos_guerreiro,
    )
    criacao_id = resposta_entrega.json()["id"]

    cabecalhos_mestre = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    resposta = cliente.post(f"/v1/criacoes/{criacao_id}/validacao", headers=cabecalhos_mestre)

    assert resposta.status_code == 200
    assert resposta.json()["situacao"] == "validada"


def test_devolucao_pela_rota_exige_motivo(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_culminancia,
    criar_equipe,
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    chave, _ = criar_chave()
    cabecalhos_guerreiro = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)
    resposta_entrega = cliente.post(
        f"/v1/culminancias/{culminancia.id}/criacoes",
        json={"equipe_id": str(equipe.id), "tipo": "texto", "producao": "Nosso robô."},
        headers=cabecalhos_guerreiro,
    )
    criacao_id = resposta_entrega.json()["id"]

    cabecalhos_mestre = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    resposta_sem_motivo = cliente.post(
        f"/v1/criacoes/{criacao_id}/devolucao", json={}, headers=cabecalhos_mestre
    )
    assert resposta_sem_motivo.status_code == 422

    resposta = cliente.post(
        f"/v1/criacoes/{criacao_id}/devolucao",
        json={"motivo": "Falta explicar como funciona."},
        headers=cabecalhos_mestre,
    )
    assert resposta.status_code == 200
    assert resposta.json()["situacao"] == "devolvida"
    assert resposta.json()["motivo_da_devolucao"] == "Falta explicar como funciona."


def _criacao_com_arquivo_enviado(
    cliente, cabecalhos, culminancia_id, *, tipo="imagem", tipo_mime="image/png", corpo=b"PNG-falso"
):
    """Entrega, envia os bytes e confirma — o caminho inteiro por HTTP,
    como o Guerreiro(a) o percorre."""
    resposta = cliente.post(
        f"/v1/culminancias/{culminancia_id}/criacoes",
        json={"tipo": tipo},
        headers=cabecalhos,
    )
    assert resposta.status_code == 201
    criacao_id = resposta.json()["id"]
    resposta_sessao = cliente.post(
        f"/v1/criacoes/{criacao_id}/arquivo",
        json={"tipo_mime": tipo_mime, "tamanho_declarado": len(corpo)},
        headers=cabecalhos,
    )
    assert resposta_sessao.status_code == 201
    cliente.put(
        resposta_sessao.json()["endereco_da_sessao"],
        content=corpo,
        headers={**cabecalhos, "Content-Range": f"bytes 0-{len(corpo) - 1}/{len(corpo)}"},
    )
    assert (
        cliente.patch(f"/v1/criacoes/{criacao_id}/arquivo", headers=cabecalhos).status_code == 200
    )
    return criacao_id


def test_autor_le_os_bytes_da_propria_criacao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_culminancia
):
    """`RF-01-78`: até 2026-11-03 não havia `GET` — o arquivo entrava e
    nunca saía."""
    guerreiro = criar_persona(Papel.guerreiro)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.individual)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)
    criacao_id = _criacao_com_arquivo_enviado(
        cliente, cabecalhos, culminancia.id, corpo=b"bytes-da-criacao"
    )

    resposta = cliente.get(f"/v1/criacoes/{criacao_id}/arquivo", headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.content == b"bytes-da-criacao"
    assert resposta.headers["content-type"].startswith("image/png")


def test_mestre_autor_le_os_bytes_da_criacao_que_lhe_cabe_julgar(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_culminancia
):
    guerreiro = criar_persona(Papel.guerreiro)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.individual)
    chave, _ = criar_chave()
    cabecalhos_guerreiro = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)
    criacao_id = _criacao_com_arquivo_enviado(cliente, cabecalhos_guerreiro, culminancia.id)
    cabecalhos_mestre = _cabecalhos(chave, criar_sessao_de_teste, mestre)

    resposta = cliente.get(f"/v1/criacoes/{criacao_id}/arquivo", headers=cabecalhos_mestre)

    assert resposta.status_code == 200


def test_quem_nao_e_creditado_nem_autor_e_recusado(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_culminancia
):
    """`RN-01-60`: 403, e nenhum byte."""
    guerreiro = criar_persona(Papel.guerreiro)
    estranho = criar_persona(Papel.guerreiro)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.individual)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)
    criacao_id = _criacao_com_arquivo_enviado(cliente, cabecalhos, culminancia.id)
    cabecalhos_estranho = _cabecalhos(chave, criar_sessao_de_teste, estranho)

    resposta = cliente.get(f"/v1/criacoes/{criacao_id}/arquivo", headers=cabecalhos_estranho)

    assert resposta.status_code == 403
    assert resposta.content != b"PNG-falso"


def test_criacao_de_texto_e_criacao_sem_envio_respondem_404(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_culminancia
):
    guerreiro = criar_persona(Papel.guerreiro)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.individual)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)

    id_do_texto = cliente.post(
        f"/v1/culminancias/{culminancia.id}/criacoes",
        json={"tipo": "texto", "producao": "Meu diário."},
        headers=cabecalhos,
    ).json()["id"]
    assert cliente.get(f"/v1/criacoes/{id_do_texto}/arquivo", headers=cabecalhos).status_code == 404


def test_criacao_com_envio_nao_confirmado_responde_404(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_culminancia
):
    outro_mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.individual)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)
    assert outro_mestre is not None

    criacao_id = cliente.post(
        f"/v1/culminancias/{culminancia.id}/criacoes",
        json={"tipo": "audio"},
        headers=cabecalhos,
    ).json()["id"]
    cliente.post(
        f"/v1/criacoes/{criacao_id}/arquivo",
        json={"tipo_mime": "audio/mpeg", "tamanho_declarado": 9},
        headers=cabecalhos,
    )

    resposta = cliente.get(f"/v1/criacoes/{criacao_id}/arquivo", headers=cabecalhos)

    assert resposta.status_code == 404


def test_envio_da_criacao_recusa_formato_fora_da_lista(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_culminancia
):
    """A lista fechada de formatos saiu de `criacoes_originais.regra` para
    `armazenamento.limites`, de onde a comprovação do prático também a lê: a
    recusa e a mensagem seguem as de antes da extração (`RF-05-91`)."""
    guerreiro = criar_persona(Papel.guerreiro)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.individual)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)

    criacao_id = cliente.post(
        f"/v1/culminancias/{culminancia.id}/criacoes",
        json={"tipo": "imagem"},
        headers=cabecalhos,
    ).json()["id"]

    resposta = cliente.post(
        f"/v1/criacoes/{criacao_id}/arquivo",
        json={"tipo_mime": "image/gif", "tamanho_declarado": 10},
        headers=cabecalhos,
    )

    assert resposta.status_code == 422
    assert "MP4, WebM, JPG, PNG, WebP, MP3 e PDF" in resposta.text


def test_envio_da_criacao_recusa_tamanho_acima_do_teto_dizendo_o_teto(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_culminancia
):
    """O teto por tipo também saiu para `armazenamento.limites` — 20 MB fora
    do vídeo —, e a recusa continua sendo o 413 de `ArquivoAcimaDoTeto`, com a
    mensagem dizendo o limite (`RF-05-91`)."""
    guerreiro = criar_persona(Papel.guerreiro)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    culminancia = criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.individual)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)

    criacao_id = cliente.post(
        f"/v1/culminancias/{culminancia.id}/criacoes",
        json={"tipo": "imagem"},
        headers=cabecalhos,
    ).json()["id"]

    resposta = cliente.post(
        f"/v1/criacoes/{criacao_id}/arquivo",
        json={"tipo_mime": "image/png", "tamanho_declarado": 21 * 1024 * 1024},
        headers=cabecalhos,
    )

    assert resposta.status_code == 413
    assert "20 MB" in resposta.text
