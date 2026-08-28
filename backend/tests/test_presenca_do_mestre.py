import uuid
from datetime import UTC, datetime, timedelta

from nucleo.aulas.modelo import ModoDeComprovacao, Presenca
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import FormatoDeAtividade

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def test_mestre_confirma_a_presenca_que_faltou(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    sessao,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(mestre, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "confirmacao",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["modo"] == "confirmacao"
    assert corpo["confirmador_id"] == str(mestre.id)

    presenca = sessao.query(Presenca).filter_by(aula_id=aula.id, guerreiro_id=guerreiro.id).one()
    assert presenca.modo == ModoDeComprovacao.confirmacao
    assert presenca.confirmador_id == mestre.id


def test_mestre_nao_registra_presenca_por_reconhecimento(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    sessao,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(mestre, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "reconhecimento",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
    assert sessao.query(Presenca).count() == 0


def test_reenvio_da_mesma_presenca_nao_duplica(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    sessao,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(mestre, comunidade)

    corpo_da_requisicao = {
        "guerreiro_id": str(guerreiro.id),
        "modo": "confirmacao",
        "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
    }
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    primeira = cliente.post(
        f"/v1/aulas/{aula.id}/presencas", json=corpo_da_requisicao, headers=headers
    )
    segunda = cliente.post(
        f"/v1/aulas/{aula.id}/presencas", json=corpo_da_requisicao, headers=headers
    )

    assert primeira.status_code == 201
    assert segunda.status_code == 201
    assert primeira.json()["id"] == segunda.json()["id"]
    assert sessao.query(Presenca).filter_by(aula_id=aula.id, guerreiro_id=guerreiro.id).count() == 1


def test_papel_sem_a_operacao_e_recusado_na_presenca(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "confirmacao",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_guerreiro_nao_registra_a_propria_presenca(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    """A matriz de permissões (`RF-01-20`) não concede ao Guerreiro(a)
    operação de escrita de presença alguma — a presença é fato do
    encontro, não ato dele (design — decisão 1)."""
    chave, _ = criar_chave(aplicacao="app-01-aula-presencial")
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    token, _ = criar_sessao_de_teste(guerreiro)
    aula = criar_aula(admin, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "reconhecimento",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_app_01_registra_presenca_por_reconhecimento_sem_confirmador(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula, sessao
):
    """A sessão de trabalho do aparelho autentica a escrita sem virar
    confirmadora (`RF-04-18`, design — decisão 2)."""
    chave, _ = criar_chave(aplicacao="app-01-aula-presencial")
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "reconhecimento",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["modo"] == "reconhecimento"
    assert corpo["confirmador_id"] is None

    presenca = sessao.query(Presenca).filter_by(aula_id=aula.id, guerreiro_id=guerreiro.id).one()
    assert presenca.modo == ModoDeComprovacao.reconhecimento
    assert presenca.confirmador_id is None


def test_app_01_confirma_presenca_e_grava_quem_confirmou(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula, sessao
):
    """A App 01 continua aceitando o modo confirmação, gravando o adulto
    da sessão de trabalho (`RF-04-21`)."""
    chave, _ = criar_chave(aplicacao="app-01-aula-presencial")
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "confirmacao",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["modo"] == "confirmacao"
    assert corpo["confirmador_id"] == str(admin.id)


def test_reenvio_devolve_o_momento_do_fato_original(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    """O sinal de presença já registrada é o momento do fato gravado, não
    o enviado no reenvio (`RF-04-19`, design — decisão 3)."""
    chave, _ = criar_chave(aplicacao="app-01-aula-presencial")
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    primeira = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "reconhecimento",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers=headers,
    )
    momento_do_reenvio = MOMENTO_DO_FATO + timedelta(minutes=5)
    segunda = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "reconhecimento",
            "momento_do_fato": momento_do_reenvio.isoformat(),
        },
        headers=headers,
    )

    assert primeira.status_code == 201
    assert segunda.status_code == 201
    assert segunda.json()["id"] == primeira.json()["id"]
    assert segunda.json()["momento_do_fato"] == primeira.json()["momento_do_fato"]
    assert segunda.json()["momento_do_fato"] != momento_do_reenvio.isoformat()


def test_mestre_ve_as_proprias_turmas_e_atividades(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    aula = criar_aula(mestre, comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)

    resposta = cliente.get(
        "/v1/minhas-turmas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [item["id"] for item in corpo["itens"]] == [str(aula.id)]
    assert [a["id"] for a in corpo["atividades_presenciais"]] == [str(atividade.id)]
    assert corpo["atividades_on_line"] == []


def test_atividade_de_outro_mestre_nao_aparece(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    criar_aula(mestre, comunidade)
    trilha_do_outro = criar_trilha(outro_mestre)
    missao_do_outro = criar_missao(trilha_do_outro, outro_mestre)
    criar_atividade(missao_do_outro, outro_mestre)

    resposta = cliente.get(
        "/v1/minhas-turmas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert resposta.json()["atividades_presenciais"] == []


def test_atividades_saem_separadas_por_formato(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    criar_aula(mestre, comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    presencial = criar_atividade(missao, mestre, formato=FormatoDeAtividade.presencial)
    on_line = criar_atividade(missao, mestre, formato=FormatoDeAtividade.on_line_assincrona)

    resposta = cliente.get(
        "/v1/minhas-turmas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    corpo = resposta.json()
    assert [a["id"] for a in corpo["atividades_presenciais"]] == [str(presencial.id)]
    assert [a["id"] for a in corpo["atividades_on_line"]] == [str(on_line.id)]


def test_admin_anula_presenca_registrada_por_engano(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    sessao,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    registrada = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "confirmacao",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers=headers,
    )
    id_da_presenca = registrada.json()["id"]

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/presencas/{id_da_presenca}/anulacao",
        json={"motivo": "Reconhecimento apontou a pessoa errada."},
        headers=headers,
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["anulada_em"] is not None
    assert corpo["anulada_por_id"] == str(admin.id)
    assert corpo["motivo_da_anulacao"] == "Reconhecimento apontou a pessoa errada."

    presenca = sessao.query(Presenca).filter_by(id=id_da_presenca).one()
    assert presenca.modo == ModoDeComprovacao.confirmacao
    assert presenca.momento_do_fato == MOMENTO_DO_FATO


def test_anulacao_sem_motivo_e_recusada(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    registrada = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "confirmacao",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers=headers,
    )
    id_da_presenca = registrada.json()["id"]

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/presencas/{id_da_presenca}/anulacao",
        json={"motivo": ""},
        headers=headers,
    )

    assert resposta.status_code == 422


def test_presenca_ja_anulada_nao_se_anula_de_novo(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    registrada = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "confirmacao",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers=headers,
    )
    id_da_presenca = registrada.json()["id"]

    primeira = cliente.post(
        f"/v1/aulas/{aula.id}/presencas/{id_da_presenca}/anulacao",
        json={"motivo": "Engano."},
        headers=headers,
    )
    segunda = cliente.post(
        f"/v1/aulas/{aula.id}/presencas/{id_da_presenca}/anulacao",
        json={"motivo": "De novo."},
        headers=headers,
    )

    assert primeira.status_code == 201
    assert segunda.status_code == 409


def test_mestre_nao_anula_presenca(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    token_do_admin, _ = criar_sessao_de_teste(admin)
    token_do_mestre, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)

    registrada = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "confirmacao",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_admin}"},
    )
    id_da_presenca = registrada.json()["id"]

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/presencas/{id_da_presenca}/anulacao",
        json={"motivo": "Engano."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_mestre}"},
    )

    assert resposta.status_code == 403


def test_registro_correto_e_aceito_depois_da_anulacao(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    sessao,
):
    """Anulada a presença, o par (aula, guerreiro) volta a aceitar o
    registro correto, sem que a anulada seja tocada (`RF-02-36`,
    `RN-02-12`)."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    errada = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "confirmacao",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers=headers,
    )
    id_da_errada = errada.json()["id"]

    cliente.post(
        f"/v1/aulas/{aula.id}/presencas/{id_da_errada}/anulacao",
        json={"motivo": "Reconhecimento apontou a pessoa errada."},
        headers=headers,
    )

    momento_correto = MOMENTO_DO_FATO + timedelta(minutes=10)
    correta = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "confirmacao",
            "momento_do_fato": momento_correto.isoformat(),
        },
        headers=headers,
    )

    assert correta.status_code == 201
    assert correta.json()["id"] != id_da_errada
    assert correta.json()["anulada_em"] is None

    presencas = sessao.query(Presenca).filter_by(aula_id=aula.id, guerreiro_id=guerreiro.id).all()
    assert len(presencas) == 2
    anulada = next(p for p in presencas if p.id == uuid.UUID(id_da_errada))
    assert anulada.anulada_em is not None


def test_presenca_anulada_nao_aparece_no_painel_do_dia(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    registrada = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "confirmacao",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers=headers,
    )
    id_da_presenca = registrada.json()["id"]

    cliente.post(
        f"/v1/aulas/{aula.id}/presencas/{id_da_presenca}/anulacao",
        json={"motivo": "Engano."},
        headers=headers,
    )

    painel = cliente.get("/v1/painel-do-dia", headers=headers)

    assert painel.status_code == 200
    ids_no_painel = [item["guerreiro_id"] for item in painel.json()["presencas"]]
    assert str(guerreiro.id) not in ids_no_painel


def test_reenvio_da_app_01_nao_ressuscita_presenca_anulada(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
):
    """O reenvio idempotente não pode devolver a presença que o Admin
    acabou de anular — sem isso o ajuste manual do `RF-02-36` não se
    completa (design — decisão 6)."""
    chave_da_gestao, _ = criar_chave()
    chave_do_encontro, _ = criar_chave(aplicacao="app-01-aula-presencial")
    admin = criar_persona(Papel.admin)
    token_do_admin, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)

    registrada = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "reconhecimento",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers={
            "X-Chave-Aplicacao": chave_do_encontro,
            "Authorization": f"Bearer {token_do_admin}",
        },
    )
    id_da_anulada = registrada.json()["id"]

    cliente.post(
        f"/v1/aulas/{aula.id}/presencas/{id_da_anulada}/anulacao",
        json={"motivo": "Reconheceu a pessoa errada."},
        headers={"X-Chave-Aplicacao": chave_da_gestao, "Authorization": f"Bearer {token_do_admin}"},
    )

    reenvio = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "reconhecimento",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers={
            "X-Chave-Aplicacao": chave_do_encontro,
            "Authorization": f"Bearer {token_do_admin}",
        },
    )

    assert reenvio.status_code == 201
    assert reenvio.json()["id"] != id_da_anulada
    assert reenvio.json()["anulada_em"] is None


def test_papel_sem_a_operacao_e_recusado_em_minhas_turmas(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(
        "/v1/minhas-turmas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
