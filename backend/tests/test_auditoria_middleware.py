from nucleo.auditoria.modelo import Auditoria
from nucleo.personas.modelo import Papel


def test_escrita_aceita_gera_registro_de_auditoria(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    sessao,
    monkeypatch,
    fabrica_de_auditoria,
):
    """`RF-01-29`, critério do PRD-01 §12. A gravação usa uma fábrica própria,
    independente da sessão da rota (`obter_sessao`, sobreposta só para a
    rota nos testes) — prova a decisão 3.4 do `design.md`."""
    monkeypatch.setattr(
        "nucleo.auditoria.middleware.obter_fabrica_de_sessao", lambda: fabrica_de_auditoria
    )
    chave, _ = criar_chave(aplicacao="app-06-vitrine")
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/responsaveis",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201

    registros = sessao.query(Auditoria).all()
    assert len(registros) == 1
    registro = registros[0]
    assert registro.autor_id == admin.id
    assert registro.papel_do_autor == Papel.admin.value
    assert registro.acao == "POST cadastrar_responsavel_rota"
    assert registro.entidade_afetada == "cadastrar_responsavel_rota"
    assert registro.origem == "app-06-vitrine"
    assert registro.momento is not None


def test_duas_rotas_diferentes_produzem_acoes_diferentes_e_estaveis(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    sessao,
    monkeypatch,
    fabrica_de_auditoria,
):
    monkeypatch.setattr(
        "nucleo.auditoria.middleware.obter_fabrica_de_sessao", lambda: fabrica_de_auditoria
    )
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    cliente.post("/v1/responsaveis", headers=cabecalhos)
    cliente.post(
        f"/v1/responsaveis/{responsavel.id}/vinculos",
        json={"guerreiro_id": str(guerreiro.id), "grau_de_parentesco": "mãe"},
        headers=cabecalhos,
    )

    acoes = {registro.acao for registro in sessao.query(Auditoria).all()}
    assert acoes == {"POST cadastrar_responsavel_rota", "POST criar_vinculo_rota"}


def test_leitura_nao_gera_registro(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    sessao,
    monkeypatch,
    fabrica_de_auditoria,
):
    monkeypatch.setattr(
        "nucleo.auditoria.middleware.obter_fabrica_de_sessao", lambda: fabrica_de_auditoria
    )
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/auditoria", headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 200
    assert sessao.query(Auditoria).count() == 0


def test_escrita_recusada_por_permissao_nao_gera_registro(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    sessao,
    monkeypatch,
    fabrica_de_auditoria,
):
    monkeypatch.setattr(
        "nucleo.auditoria.middleware.obter_fabrica_de_sessao", lambda: fabrica_de_auditoria
    )
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.post(
        "/v1/responsaveis",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403
    assert sessao.query(Auditoria).count() == 0


def test_escrita_sem_chave_nao_gera_registro(cliente, sessao, monkeypatch, fabrica_de_auditoria):
    monkeypatch.setattr(
        "nucleo.auditoria.middleware.obter_fabrica_de_sessao", lambda: fabrica_de_auditoria
    )
    resposta = cliente.post("/v1/responsaveis")
    assert resposta.status_code == 401
    assert sessao.query(Auditoria).count() == 0


def test_falha_ao_gravar_auditoria_nao_altera_a_resposta_ja_pronta(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao, monkeypatch, caplog
):
    """Best-effort (`design.md` — Risks): a escrita de negócio não espera
    pela auditoria nem é desfeita por ela."""

    def _fabrica_que_falha():
        raise RuntimeError("falha proposital de infraestrutura")

    monkeypatch.setattr("nucleo.auditoria.middleware.obter_fabrica_de_sessao", _fabrica_que_falha)
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/responsaveis",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    assert "id" in resposta.json()
    assert sessao.query(Auditoria).count() == 0
    assert "Falha ao gravar registro de auditoria" in caplog.text
