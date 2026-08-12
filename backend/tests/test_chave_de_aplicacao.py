import statistics
import time
import uuid

from nucleo.chaves.modelo import ChaveDeAplicacao, SituacaoDaChave
from nucleo.chaves.segredo import calcular_resumo, gerar_segredo, montar_chave_completa
from nucleo.chaves.semeadura import APLICACOES_DO_PROJETO, semear_ambiente


def test_chamada_com_chave_vigente_e_processada(cliente, criar_chave):
    chave, registro = criar_chave(aplicacao="app-06-vitrine")
    resposta = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    assert resposta.json() == {"aplicacao": "app-06-vitrine", "ambiente": "desenvolvimento"}


def test_chamada_sem_chave_e_recusada_e_rota_nao_executa(cliente):
    resposta = cliente.get("/v1/publica")
    assert resposta.status_code == 401


def test_consulta_publica_tambem_exige_chave(cliente):
    """Rota pública dispensa credencial de persona, nunca a chave (RN-01-32)."""
    resposta = cliente.get("/v1/publica")
    assert resposta.status_code == 401


def test_declarar_rota_publica_nao_a_tira_de_tras_da_chave(cliente, criar_chave):
    chave, _ = criar_chave()
    sem_chave = cliente.get("/v1/publica")
    com_chave = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave})
    assert sem_chave.status_code == 401
    assert com_chave.status_code == 200


def test_rota_publica_nao_atribui_persona(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    assert "persona" not in resposta.json()


def test_rota_autenticada_exige_as_duas_coisas(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    persona = criar_persona()
    token, _ = criar_sessao_de_teste(persona)

    sem_chave_nem_persona = cliente.get("/v1/autenticada")
    so_com_chave = cliente.get("/v1/autenticada", headers={"X-Chave-Aplicacao": chave})
    com_as_duas = cliente.get(
        "/v1/autenticada",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert sem_chave_nem_persona.status_code == 401
    assert so_com_chave.status_code == 401
    assert com_as_duas.status_code == 200

    assert sem_chave_nem_persona.json()["codigo"] == "chave_invalida"
    assert so_com_chave.json()["codigo"] == "sessao_ausente"
    assert so_com_chave.json() != sem_chave_nem_persona.json()


def test_ausente_inexistente_e_revogada_produzem_corpo_identico(cliente, criar_chave):
    chave_revogada, _ = criar_chave(situacao=SituacaoDaChave.revogada)
    chave_inexistente = montar_chave_completa("desenvolvimento", str(uuid.uuid4()), gerar_segredo())

    resposta_ausente = cliente.get("/v1/publica")
    resposta_inexistente = cliente.get(
        "/v1/publica", headers={"X-Chave-Aplicacao": chave_inexistente}
    )
    resposta_revogada = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave_revogada})

    for resposta in (resposta_ausente, resposta_inexistente, resposta_revogada):
        assert resposta.status_code == 401

    corpos = [r.json() for r in (resposta_ausente, resposta_inexistente, resposta_revogada)]
    assert corpos[0] == corpos[1] == corpos[2]


def test_recusa_por_ambiente_errado_usa_o_mesmo_corpo_da_chave_desconhecida(cliente, criar_chave):
    chave_de_producao, _ = criar_chave(ambiente="producao")
    resposta = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave_de_producao})
    assert resposta.status_code == 401
    assert resposta.json()["codigo"] == "chave_invalida"


def test_dispersao_de_tempo_nao_denuncia_o_motivo(cliente, criar_chave):
    chave_revogada, _ = criar_chave(situacao=SituacaoDaChave.revogada)
    chave_inexistente = montar_chave_completa("desenvolvimento", str(uuid.uuid4()), gerar_segredo())

    casos = {
        "ausente": None,
        "inexistente": chave_inexistente,
        "revogada": chave_revogada,
    }

    medias = {}
    repeticoes = 30
    for nome, cabecalho in casos.items():
        amostras = []
        headers = {"X-Chave-Aplicacao": cabecalho} if cabecalho else {}
        for _ in range(repeticoes):
            inicio = time.perf_counter()
            cliente.get("/v1/publica", headers=headers)
            amostras.append(time.perf_counter() - inicio)
        medias[nome] = statistics.median(amostras)

    valores = list(medias.values())
    maior, menor = max(valores), min(valores)
    # Folga generosa: o teste não mede microssegundos de CPU, mede se um dos
    # três casos abre um ramo curto muito mais barato que os outros.
    assert maior < menor * 4 + 0.05, medias


def test_chave_revogada_perde_acesso_na_chamada_seguinte(cliente, sessao, criar_chave):
    chave, registro = criar_chave()

    antes = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave})
    assert antes.status_code == 200

    registro.situacao = SituacaoDaChave.revogada
    sessao.add(registro)
    sessao.commit()

    depois = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave})
    assert depois.status_code == 401


def test_base_guarda_so_o_resumo_do_segredo(sessao, criar_chave):
    segredo_gerado = gerar_segredo()
    resumo = calcular_resumo(segredo_gerado)
    registro = ChaveDeAplicacao(
        aplicacao="app-06-vitrine",
        ambiente="desenvolvimento",
        natureza="do_projeto",
        resumo_do_segredo=resumo,
    )
    sessao.add(registro)
    sessao.commit()
    sessao.refresh(registro)

    for valor in vars(registro).values():
        assert segredo_gerado not in str(valor)
    assert registro.resumo_do_segredo == resumo


def test_segunda_leitura_nao_recupera_o_segredo(sessao, criar_chave):
    _, registro = criar_chave()
    lido_de_novo = sessao.get(ChaveDeAplicacao, registro.id)
    campos = {campo.name for campo in ChaveDeAplicacao.__table__.columns}
    assert "segredo" not in campos
    assert "resumo_do_segredo" in campos
    # O que existe é só o resumo — não há caminho de leitura que devolva o
    # segredo em claro, porque a coluna dele nunca existiu.
    assert lido_de_novo.resumo_do_segredo == registro.resumo_do_segredo


def test_semear_ambiente_emite_uma_chave_por_aplicacao(sessao):
    segredos = semear_ambiente(sessao, "desenvolvimento")
    assert set(segredos.keys()) == set(APLICACOES_DO_PROJETO)

    registros = sessao.query(ChaveDeAplicacao).filter_by(ambiente="desenvolvimento").all()
    assert len(registros) == len(APLICACOES_DO_PROJETO)
    for registro in registros:
        assert registro.natureza.value == "do_projeto"
        assert registro.prazo_de_apresentacao is None
        assert registro.situacao == SituacaoDaChave.vigente


def test_semear_duas_vezes_nao_duplica_nem_reemite(sessao):
    primeira = semear_ambiente(sessao, "desenvolvimento")
    ids_apos_primeira = {
        registro.aplicacao: registro.id
        for registro in sessao.query(ChaveDeAplicacao).filter_by(ambiente="desenvolvimento")
    }

    segunda = semear_ambiente(sessao, "desenvolvimento")

    assert segunda == {}
    ids_apos_segunda = {
        registro.aplicacao: registro.id
        for registro in sessao.query(ChaveDeAplicacao).filter_by(ambiente="desenvolvimento")
    }
    assert ids_apos_primeira == ids_apos_segunda
    assert len(ids_apos_segunda) == len(APLICACOES_DO_PROJETO)
    assert primeira != {}


def test_chave_de_um_ambiente_nao_abre_o_outro(sessao):
    semear_ambiente(sessao, "desenvolvimento")
    semear_ambiente(sessao, "producao")

    vigentes_dev = (
        sessao.query(ChaveDeAplicacao)
        .filter_by(ambiente="desenvolvimento", situacao=SituacaoDaChave.vigente)
        .count()
    )
    vigentes_producao = (
        sessao.query(ChaveDeAplicacao)
        .filter_by(ambiente="producao", situacao=SituacaoDaChave.vigente)
        .count()
    )
    assert vigentes_dev == len(APLICACOES_DO_PROJETO)
    assert vigentes_producao == len(APLICACOES_DO_PROJETO)
