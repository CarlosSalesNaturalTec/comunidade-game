from decimal import Decimal

from nucleo.desafios_extras.modelo import Modalidade, SituacaoDoDesafioExtra
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import SituacaoDaTrilha


def _cabecalhos(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def _entrada_de_proposta(trilha, tipo, ponto, **sobrescritas):
    entrada = {
        "trilha_id": str(trilha.id),
        "modalidade": "aberto",
        "tipo_de_recurso_id": str(tipo.id),
        "ponto_de_apoio_id": str(ponto.id),
        "quantidade_disponivel": 5,
        "criterio_de_atribuicao": "Quem entregar primeiro.",
        "pontos_extras": 5,
        "formato": "on_line",
        "custeio": "saldo_de_recurso",
        "vigencia_inicio": "2026-01-01",
        "vigencia_fim": "2026-12-31",
    }
    entrada.update(sobrescritas)
    return entrada


def test_apoiador_propoe_desafio_extra_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    resposta = cliente.post(
        "/v1/desafios-extras",
        json=_entrada_de_proposta(trilha, tipo, ponto),
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["trilha_id"] == str(trilha.id)
    assert corpo["situacao"] == "em_validacao_do_mestre"


def test_papel_que_nao_e_apoiador_nem_mestre_e_recusado(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    resposta = cliente.post(
        "/v1/desafios-extras",
        json=_entrada_de_proposta(trilha, tipo, ponto),
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 403


def test_mestre_propoe_desafio_extra_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    outro_mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(outro_mestre)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    resposta = cliente.post(
        "/v1/desafios-extras",
        json=_entrada_de_proposta(trilha, tipo, ponto),
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    assert resposta.json()["situacao"] == "em_validacao_do_mestre"


def test_mestre_autor_da_trilha_propoe_e_ja_nasce_em_aprovacao_do_admin(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    chave, _ = criar_chave()
    mestre_autor = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre_autor)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())

    resposta = cliente.post(
        "/v1/desafios-extras",
        json=_entrada_de_proposta(trilha, tipo, ponto),
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    assert resposta.json()["situacao"] == "em_aprovacao_do_admin"


def test_proposta_e_registrada_com_o_proponente_da_sessao(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    outro_apoiador = criar_persona(Papel.apoiador)
    token_do_apoiador, _ = criar_sessao_de_teste(apoiador)
    token_do_outro, _ = criar_sessao_de_teste(outro_apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    cliente.post(
        "/v1/desafios-extras",
        json=_entrada_de_proposta(trilha, tipo, ponto),
        headers=_cabecalhos(chave, token_do_apoiador),
    )

    resposta_do_proponente = cliente.get(
        "/v1/eu/desafios-extras", headers=_cabecalhos(chave, token_do_apoiador)
    )
    resposta_do_outro = cliente.get(
        "/v1/eu/desafios-extras", headers=_cabecalhos(chave, token_do_outro)
    )

    assert len(resposta_do_proponente.json()) == 1
    assert resposta_do_outro.json() == []


def test_leitura_devolve_situacao_motivo_lastro_e_quantidade_restante(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.recusado,
        motivo_da_recusa="A trilha já foi encerrada.",
        quantidade_disponivel=3,
    )

    resposta = cliente.get("/v1/eu/desafios-extras", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    (desafio,) = resposta.json()
    assert desafio["situacao"] == "recusado"
    assert desafio["motivo_da_recusa"] == "A trilha já foi encerrada."
    assert desafio["quantidade_restante"] == 3
    assert desafio["lastro_provido"] is False
    assert desafio["lastro_faltante"] is not None


def test_nenhuma_resposta_identifica_guerreiro_nem_confirma_o_nick(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    resposta_da_proposta = cliente.post(
        "/v1/desafios-extras",
        json=_entrada_de_proposta(
            trilha,
            tipo,
            ponto,
            modalidade="direcionado",
            nick_do_destinatario="nick-que-nao-existe",
            justificativa_do_vinculo="É meu vizinho.",
        ),
        headers=_cabecalhos(chave, token),
    )
    resposta_da_leitura = cliente.get("/v1/eu/desafios-extras", headers=_cabecalhos(chave, token))

    assert resposta_da_proposta.status_code == 201
    corpo_da_proposta = resposta_da_proposta.json()
    assert corpo_da_proposta["nick_do_destinatario"] == "nick-que-nao-existe"

    (desafio,) = resposta_da_leitura.json()
    campos_proibidos = {"nome", "nome_real", "contato", "email", "telefone", "avatar"}
    assert campos_proibidos.isdisjoint(desafio.keys())


# --- 4.4 — as quatro rotas do Admin -------------------------------------------


def test_fila_do_admin_so_traz_em_aprovacao_do_admin(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(admin)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre
    )
    pendente = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin
    )
    criar_desafio_extra(apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.publicado)
    criar_desafio_extra(apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.recusado)

    resposta = cliente.get("/v1/desafios-extras/pendentes", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    ids = [item["id"] for item in resposta.json()]
    assert ids == [str(pendente.id)]


def test_persona_de_outro_papel_recebe_403_nas_quatro_rotas(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin
    )

    assert (
        cliente.get("/v1/desafios-extras/pendentes", headers=_cabecalhos(chave, token)).status_code
        == 403
    )
    assert (
        cliente.post(
            f"/v1/desafios-extras/{desafio.id}/aprovacao",
            json={"situacao": "publicado"},
            headers=_cabecalhos(chave, token),
        ).status_code
        == 403
    )
    assert (
        cliente.get("/v1/desafios-extras/publicados", headers=_cabecalhos(chave, token)).status_code
        == 403
    )
    assert (
        cliente.post(
            f"/v1/desafios-extras/{desafio.id}/encerramento", headers=_cabecalhos(chave, token)
        ).status_code
        == 403
    )


def test_aprovacao_e_encerramento_devolvem_o_desafio_atualizado(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
    criar_lancamento,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(admin)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    criar_lancamento(
        admin, tipo, ponto, natureza=NaturezaDoLancamento.credito, quantidade=Decimal("5")
    )
    desafio = criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin,
        quantidade_disponivel=5,
    )

    resposta_da_aprovacao = cliente.post(
        f"/v1/desafios-extras/{desafio.id}/aprovacao",
        json={"situacao": "publicado"},
        headers=_cabecalhos(chave, token),
    )
    assert resposta_da_aprovacao.status_code == 200
    assert resposta_da_aprovacao.json()["situacao"] == "publicado"

    resposta_dos_publicados = cliente.get(
        "/v1/desafios-extras/publicados", headers=_cabecalhos(chave, token)
    )
    assert [item["id"] for item in resposta_dos_publicados.json()] == [str(desafio.id)]

    resposta_do_encerramento = cliente.post(
        f"/v1/desafios-extras/{desafio.id}/encerramento", headers=_cabecalhos(chave, token)
    )
    assert resposta_do_encerramento.status_code == 200
    corpo = resposta_do_encerramento.json()
    assert corpo["admin_encerrador_id"] == str(admin.id)
    assert corpo["encerrado_em"] is not None


def test_recusa_pela_rota_exige_motivo(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(admin)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin
    )

    resposta = cliente.post(
        f"/v1/desafios-extras/{desafio.id}/aprovacao",
        json={"situacao": "recusado"},
        headers=_cabecalhos(chave, token),
    )
    assert resposta.status_code == 422

    resposta_com_motivo = cliente.post(
        f"/v1/desafios-extras/{desafio.id}/aprovacao",
        json={"situacao": "recusado", "motivo": "Sem aderência à trilha."},
        headers=_cabecalhos(chave, token),
    )
    assert resposta_com_motivo.status_code == 200
    assert resposta_com_motivo.json()["situacao"] == "recusado"


def test_nenhuma_resposta_das_rotas_do_admin_identifica_guerreiro(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(admin)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin,
        modalidade=Modalidade.direcionado,
        nick_do_destinatario="nick-do-destinatario",
        justificativa_do_vinculo="É minha vizinha.",
    )

    resposta = cliente.get("/v1/desafios-extras/pendentes", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    (desafio,) = resposta.json()
    assert desafio["nick_do_destinatario"] == "nick-do-destinatario"
    campos_proibidos = {"nome", "nome_real", "contato", "email", "telefone", "avatar"}
    assert campos_proibidos.isdisjoint(desafio.keys())


def test_as_quatro_rotas_de_desafios_extras_estao_no_openapi_sob_v1(cliente):
    schema = cliente.get("/openapi.json").json()

    assert "get" in schema["paths"]["/v1/desafios-extras/pendentes"]
    assert "post" in schema["paths"]["/v1/desafios-extras/{id_do_desafio}/aprovacao"]
    assert "get" in schema["paths"]["/v1/desafios-extras/publicados"]
    assert "post" in schema["paths"]["/v1/desafios-extras/{id_do_desafio}/encerramento"]


# --- 3.1 e 3.2 — a validação do Mestre e a fila do que ele tem a validar -----


def test_fila_de_validacao_e_restrita_ao_mestre_autor(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    chave, _ = criar_chave()
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    token_do_autor, _ = criar_sessao_de_teste(mestre_autor)
    token_do_outro, _ = criar_sessao_de_teste(outro_mestre)
    token_do_apoiador, _ = criar_sessao_de_teste(apoiador)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())
    esperado = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre
    )

    resposta_do_autor = cliente.get(
        "/v1/desafios-extras/a-validar", headers=_cabecalhos(chave, token_do_autor)
    )
    resposta_do_outro = cliente.get(
        "/v1/desafios-extras/a-validar", headers=_cabecalhos(chave, token_do_outro)
    )
    resposta_do_apoiador = cliente.get(
        "/v1/desafios-extras/a-validar", headers=_cabecalhos(chave, token_do_apoiador)
    )

    assert resposta_do_autor.status_code == 200
    assert [item["id"] for item in resposta_do_autor.json()] == [str(esperado.id)]
    assert resposta_do_outro.json() == []
    assert resposta_do_apoiador.status_code == 403


def test_validacao_pela_rota_exige_parecer_e_leva_ao_admin(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    chave, _ = criar_chave()
    mestre_autor = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(mestre_autor)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre
    )

    resposta_sem_parecer = cliente.post(
        f"/v1/desafios-extras/{desafio.id}/validacao",
        json={"situacao": "em_aprovacao_do_admin"},
        headers=_cabecalhos(chave, token),
    )
    assert resposta_sem_parecer.status_code == 422

    resposta_com_parecer = cliente.post(
        f"/v1/desafios-extras/{desafio.id}/validacao",
        json={"situacao": "em_aprovacao_do_admin", "parecer": "Boa proposta pedagógica."},
        headers=_cabecalhos(chave, token),
    )
    assert resposta_com_parecer.status_code == 200
    corpo = resposta_com_parecer.json()
    assert corpo["situacao"] == "em_aprovacao_do_admin"
    assert corpo["parecer_do_mestre"] == "Boa proposta pedagógica."


def test_recusa_pela_rota_do_mestre_exige_motivo_e_nao_chega_ao_admin(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    chave, _ = criar_chave()
    mestre_autor = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(mestre_autor)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre
    )

    resposta_sem_motivo = cliente.post(
        f"/v1/desafios-extras/{desafio.id}/validacao",
        json={"situacao": "recusado"},
        headers=_cabecalhos(chave, token),
    )
    assert resposta_sem_motivo.status_code == 422

    resposta_com_motivo = cliente.post(
        f"/v1/desafios-extras/{desafio.id}/validacao",
        json={"situacao": "recusado", "motivo": "Sem mérito pedagógico."},
        headers=_cabecalhos(chave, token),
    )
    assert resposta_com_motivo.status_code == 200
    assert resposta_com_motivo.json()["situacao"] == "recusado"

    resposta_da_fila_do_admin = cliente.get(
        "/v1/desafios-extras/pendentes", headers=_cabecalhos(chave, token)
    )
    # O Mestre não tem acesso à fila do Admin (`Operacao.tudo`) — 403 já
    # confirma, por outra via, que o recusado não está nela.
    assert resposta_da_fila_do_admin.status_code == 403


def test_mestre_que_nao_e_autor_recebe_403_na_validacao(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    chave, _ = criar_chave()
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(outro_mestre)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre
    )

    resposta = cliente.post(
        f"/v1/desafios-extras/{desafio.id}/validacao",
        json={"situacao": "em_aprovacao_do_admin", "parecer": "Ok."},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 403


def test_criterio_de_aceite_recusado_pelo_mestre_nao_aparece_na_fila_do_admin(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre_autor = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    token_do_mestre, _ = criar_sessao_de_teste(mestre_autor)
    token_do_admin, _ = criar_sessao_de_teste(admin)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre
    )

    cliente.post(
        f"/v1/desafios-extras/{desafio.id}/validacao",
        json={"situacao": "recusado", "motivo": "Sem mérito pedagógico."},
        headers=_cabecalhos(chave, token_do_mestre),
    )

    resposta_da_fila_do_admin = cliente.get(
        "/v1/desafios-extras/pendentes", headers=_cabecalhos(chave, token_do_admin)
    )

    assert resposta_da_fila_do_admin.json() == []


def test_eu_desafios_extras_serve_qualquer_proponente(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre)
    ponto = criar_ponto_de_apoio(mestre, criar_comunidade())

    cliente.post(
        "/v1/desafios-extras",
        json=_entrada_de_proposta(trilha, tipo, ponto),
        headers=_cabecalhos(chave, token),
    )
    resposta = cliente.get("/v1/eu/desafios-extras", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    (desafio,) = resposta.json()
    assert desafio["situacao"] == "em_aprovacao_do_admin"


def test_as_duas_rotas_novas_estao_no_openapi_sob_v1(cliente):
    schema = cliente.get("/openapi.json").json()

    assert "post" in schema["paths"]["/v1/desafios-extras/{id_do_desafio}/validacao"]
    assert "get" in schema["paths"]["/v1/desafios-extras/a-validar"]
