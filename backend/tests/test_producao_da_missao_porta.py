"""A porta da leitura e da devolutiva da produção — `RF-04-46`, `RF-04-47`,
`RF-09-90`, design — decisões 4 e 5."""

import io
import json
import logging

import httpx

from nucleo.livro_razao.modelo import Lancamento
from nucleo.personas.modelo import Papel
from nucleo.producoes.fabrica import dependencia_da_producao_da_missao
from nucleo.producoes.local import ProducaoDaMissaoLocal
from nucleo.producoes.modelo import ProducaoDaMissao
from nucleo.producoes.nuvem import ProducaoDaMissaoNaNuvem
from nucleo.producoes.porta import PortaDaProducaoDaMissao
from nucleo.trilhas.modelo import SituacaoDaTrilha


def _cabecalhos(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


class _PortaSempreIndisponivel(PortaDaProducaoDaMissao):
    def ler(self, *, forma, texto, arquivo, producao_esperada):
        return None


def _montar_equipe_com_atividade_corrente(
    *,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    sessao,
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(
        missao, mestre, aula=aula, producao_esperada="Um texto sobre o tema."
    )
    equipe = criar_equipe(guerreiro, aula=aula)
    equipe.atividade_corrente_id = atividade.id
    sessao.commit()
    return guerreiro, equipe


def _montar_guerreiro_com_missao_desbloqueada(
    *,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre, producao_esperada="Um texto sobre o tema.")
    criar_inscricao_na_trilha(guerreiro, trilha)
    criar_desbloqueio_da_missao(guerreiro, missao, aprovado=True)
    return guerreiro, missao, atividade


def test_local_ecoa_a_fala_transcrita_e_descarta_a_foto():
    """`RF-05-76`, `RN-05-32`: a fala chega transcrita do aparelho e passa
    pelo caminho do texto; só a foto é mídia, e o byte dela não vira
    transcrição."""
    porta = ProducaoDaMissaoLocal()

    leitura_da_fala = porta.ler(
        forma="audio",
        texto="O que a equipe falou.",
        arquivo=None,
        producao_esperada="Uma fala.",
    )
    leitura_foto = porta.ler(
        forma="foto", texto=None, arquivo=b"bytes-de-foto", producao_esperada="Um desenho."
    )

    assert leitura_da_fala is not None
    assert leitura_da_fala.transcricao == "O que a equipe falou."
    assert leitura_da_fala.devolutiva

    assert leitura_foto is not None
    assert "bytes-de-foto" not in leitura_foto.transcricao
    assert leitura_foto.devolutiva


def test_devolutiva_em_branco_no_texto_quando_leitura_indisponivel(
    app,
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    app.dependency_overrides[dependencia_da_producao_da_missao] = lambda: _PortaSempreIndisponivel()
    try:
        chave, _ = criar_chave()
        guerreiro, equipe = _montar_equipe_com_atividade_corrente(
            criar_persona=criar_persona,
            criar_comunidade=criar_comunidade,
            criar_aula=criar_aula,
            criar_trilha=criar_trilha,
            criar_missao=criar_missao,
            criar_atividade=criar_atividade,
            criar_equipe=criar_equipe,
            sessao=sessao,
        )
        token, _ = criar_sessao_de_teste(guerreiro)

        resposta = cliente.post(
            f"/v1/equipes/{equipe.id}/producao",
            data={"forma": "texto", "texto": "O que escrevi não pode se perder."},
            headers=_cabecalhos(chave, token),
        )

        assert resposta.status_code == 201
        corpo = resposta.json()
        assert corpo["transcricao"] == "O que escrevi não pode se perder."
        assert corpo["devolutiva"] is None
    finally:
        del app.dependency_overrides[dependencia_da_producao_da_missao]


def test_503_so_na_foto_quando_leitura_indisponivel(
    app,
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    app.dependency_overrides[dependencia_da_producao_da_missao] = lambda: _PortaSempreIndisponivel()
    try:
        chave, _ = criar_chave()
        guerreiro, equipe = _montar_equipe_com_atividade_corrente(
            criar_persona=criar_persona,
            criar_comunidade=criar_comunidade,
            criar_aula=criar_aula,
            criar_trilha=criar_trilha,
            criar_missao=criar_missao,
            criar_atividade=criar_atividade,
            criar_equipe=criar_equipe,
            sessao=sessao,
        )
        token, _ = criar_sessao_de_teste(guerreiro)

        resposta_da_foto = cliente.post(
            f"/v1/equipes/{equipe.id}/producao",
            data={"forma": "foto"},
            files={"arquivo": ("manuscrito.jpg", io.BytesIO(b"conteudo-fake"), "image/jpeg")},
            headers=_cabecalhos(chave, token),
        )
        assert resposta_da_foto.status_code == 503
        assert sessao.query(ProducaoDaMissao).count() == 0

        # `RF-05-76`: a fala já chega transcrita do aparelho, então a
        # indisponibilidade do modelo não tem o que impedir — a produção é
        # gravada com a devolutiva em branco, como a entrega por texto.
        resposta_da_fala = cliente.post(
            f"/v1/equipes/{equipe.id}/producao",
            data={"forma": "audio", "texto": "O que a equipe falou."},
            headers=_cabecalhos(chave, token),
        )
        assert resposta_da_fala.status_code == 201
        corpo = resposta_da_fala.json()
        assert corpo["transcricao"] == "O que a equipe falou."
        assert corpo["devolutiva"] is None
        assert sessao.query(ProducaoDaMissao).count() == 1
    finally:
        del app.dependency_overrides[dependencia_da_producao_da_missao]


def test_falha_na_leitura_nao_registra_o_byte_em_log(
    app,
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
    caplog,
):
    app.dependency_overrides[dependencia_da_producao_da_missao] = lambda: _PortaSempreIndisponivel()
    try:
        chave, _ = criar_chave()
        guerreiro, equipe = _montar_equipe_com_atividade_corrente(
            criar_persona=criar_persona,
            criar_comunidade=criar_comunidade,
            criar_aula=criar_aula,
            criar_trilha=criar_trilha,
            criar_missao=criar_missao,
            criar_atividade=criar_atividade,
            criar_equipe=criar_equipe,
            sessao=sessao,
        )
        token, _ = criar_sessao_de_teste(guerreiro)

        with caplog.at_level("WARNING", logger="nucleo.producoes"):
            cliente.post(
                f"/v1/equipes/{equipe.id}/producao",
                data={"forma": "foto"},
                files={"arquivo": ("manuscrito.jpg", io.BytesIO(b"segredo-da-foto"), "image/jpeg")},
                headers=_cabecalhos(chave, token),
            )

        texto_do_log = " ".join(registro.getMessage() for registro in caplog.records)
        assert "segredo-da-foto" not in texto_do_log
        assert "forma=foto" in texto_do_log
    finally:
        del app.dependency_overrides[dependencia_da_producao_da_missao]


def test_entrega_nao_lanca_custo_no_livro_razao(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    """A porta local, escolhida em `configuracao.ambiente == "desenvolvimento"`,
    nunca mede consumo nem lança custo (`RF-09-90`)."""
    chave, _ = criar_chave()
    guerreiro, equipe = _montar_equipe_com_atividade_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/producao",
        data={"forma": "texto", "texto": "Uma produção qualquer."},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert "custo" not in corpo
    assert "cota" not in corpo
    assert "contagem_de_uso" not in corpo
    assert sessao.query(Lancamento).count() == 0


# --- Os mesmos desfechos de leitura, na porta individual ---


def test_devolutiva_em_branco_no_texto_individual_quando_leitura_indisponivel(
    app,
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    app.dependency_overrides[dependencia_da_producao_da_missao] = lambda: _PortaSempreIndisponivel()
    try:
        chave, _ = criar_chave()
        guerreiro, missao, atividade = _montar_guerreiro_com_missao_desbloqueada(
            criar_persona=criar_persona,
            criar_trilha=criar_trilha,
            criar_missao=criar_missao,
            criar_atividade=criar_atividade,
            criar_inscricao_na_trilha=criar_inscricao_na_trilha,
            criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
        )
        token, _ = criar_sessao_de_teste(guerreiro)

        resposta = cliente.post(
            f"/v1/eu/missoes/{missao.id}/producao",
            data={
                "forma": "texto",
                "texto": "O que escrevi não pode se perder.",
                "atividade_id": str(atividade.id),
            },
            headers=_cabecalhos(chave, token),
        )

        assert resposta.status_code == 201
        corpo = resposta.json()
        assert corpo["transcricao"] == "O que escrevi não pode se perder."
        assert corpo["devolutiva"] is None
    finally:
        del app.dependency_overrides[dependencia_da_producao_da_missao]


def test_503_so_na_foto_individual_quando_leitura_indisponivel(
    app,
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    app.dependency_overrides[dependencia_da_producao_da_missao] = lambda: _PortaSempreIndisponivel()
    try:
        chave, _ = criar_chave()
        guerreiro, missao, atividade = _montar_guerreiro_com_missao_desbloqueada(
            criar_persona=criar_persona,
            criar_trilha=criar_trilha,
            criar_missao=criar_missao,
            criar_atividade=criar_atividade,
            criar_inscricao_na_trilha=criar_inscricao_na_trilha,
            criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
        )
        token, _ = criar_sessao_de_teste(guerreiro)

        resposta_da_foto = cliente.post(
            f"/v1/eu/missoes/{missao.id}/producao",
            data={"forma": "foto", "atividade_id": str(atividade.id)},
            files={"arquivo": ("manuscrito.jpg", io.BytesIO(b"conteudo-fake"), "image/jpeg")},
            headers=_cabecalhos(chave, token),
        )
        assert resposta_da_foto.status_code == 503
        assert sessao.query(ProducaoDaMissao).count() == 0

        resposta_da_fala = cliente.post(
            f"/v1/eu/missoes/{missao.id}/producao",
            data={
                "forma": "audio",
                "atividade_id": str(atividade.id),
                "texto": "O que eu falei.",
            },
            headers=_cabecalhos(chave, token),
        )
        assert resposta_da_fala.status_code == 201
        assert resposta_da_fala.json()["devolutiva"] is None
        assert sessao.query(ProducaoDaMissao).count() == 1
    finally:
        del app.dependency_overrides[dependencia_da_producao_da_missao]


# --- Os cenários HTTP da rota individual — `RF-05-74`, `RF-01-16` ---


def test_guerreiro_em_sessao_entrega_pela_porta_individual(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, missao, atividade = _montar_guerreiro_com_missao_desbloqueada(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={"forma": "texto", "texto": "Um texto", "atividade_id": str(atividade.id)},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201


def test_mestre_e_admin_nao_entregam_pela_porta_individual(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    _, missao, atividade = _montar_guerreiro_com_missao_desbloqueada(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
    )
    for operador in (criar_persona(Papel.mestre), criar_persona(Papel.admin)):
        token, _ = criar_sessao_de_teste(operador)
        resposta = cliente.post(
            f"/v1/eu/missoes/{missao.id}/producao",
            data={"forma": "texto", "texto": "Um texto", "atividade_id": str(atividade.id)},
            headers=_cabecalhos(chave, token),
        )
        assert resposta.status_code == 403


def test_sem_sessao_a_porta_individual_nao_abre(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.post(
        "/v1/eu/missoes/00000000-0000-0000-0000-000000000000/producao",
        data={
            "forma": "texto",
            "texto": "Um texto",
            "atividade_id": "00000000-0000-0000-0000-000000000000",
        },
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 401


def test_porta_de_equipe_segue_intacta_apos_a_porta_individual(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe = _montar_equipe_com_atividade_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/producao",
        data={"forma": "texto", "texto": "Produção da equipe."},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["equipe_id"] == str(equipe.id)
    assert corpo["guerreiro_id"] is None


# --- Adaptador de produção (Gemini) ------------------------------------------
# Design da change `chave-do-gemini-em-producao` — decisão 3: nenhuma causa de
# indisponibilidade é muda, e nenhuma delas vira exceção (`RF-04-46`,
# `RN-05-35`).

_LOGGER_DA_NUVEM = "nucleo.producoes"


class _RespostaFake:
    def __init__(self, corpo: dict):
        self._corpo = corpo

    def raise_for_status(self):
        pass

    def json(self):
        return self._corpo


def _corpo_gemini(texto: str) -> dict:
    return {"candidates": [{"content": {"parts": [{"text": texto}]}}]}


def _ler(porta):
    return porta.ler(
        forma="texto",
        texto="A equipe plantou dez mudas.",
        arquivo=None,
        producao_esperada="Relato do plantio.",
    )


def test_nuvem_sem_chave_devolve_none_e_registra_a_causa(caplog):
    porta = ProducaoDaMissaoNaNuvem(chave_de_api="", modelo="gemini-2.5-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER_DA_NUVEM):
        assert _ler(porta) is None

    assert "Chave de API do Gemini ausente" in caplog.text


def test_nuvem_sem_chave_nao_chega_a_chamar_o_modelo(monkeypatch):
    def _nao_deve_ser_chamado(*args, **kwargs):
        raise AssertionError("sem chave, o adaptador não pode alcançar a rede")

    monkeypatch.setattr(httpx, "post", _nao_deve_ser_chamado)
    porta = ProducaoDaMissaoNaNuvem(chave_de_api="", modelo="gemini-2.5-flash")

    assert _ler(porta) is None


def test_nuvem_devolve_none_em_erro_de_transporte(monkeypatch, caplog):
    def _levanta(*args, **kwargs):
        raise httpx.ConnectError("rede indisponível")

    monkeypatch.setattr(httpx, "post", _levanta)
    porta = ProducaoDaMissaoNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER_DA_NUVEM):
        assert _ler(porta) is None

    assert "Falha ao consultar a leitura da produção no Gemini." in caplog.text


def test_nuvem_devolve_none_e_registra_json_fora_do_formato(monkeypatch, caplog):
    """O validador devolve `None` de dentro do `try`, sem exceção: sem a linha
    própria a causa ficaria indistinguível da chave ausente."""
    corpo = _corpo_gemini(json.dumps({"devolutiva": "Muito bem!"}))
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _RespostaFake(corpo))
    porta = ProducaoDaMissaoNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER_DA_NUVEM):
        assert _ler(porta) is None

    assert "fora do formato esperado" in caplog.text


def test_nuvem_devolve_a_leitura_quando_o_modelo_responde(monkeypatch, caplog):
    corpo = _corpo_gemini(
        json.dumps({"transcricao": "Plantamos dez mudas.", "devolutiva": "Bom relato."})
    )
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _RespostaFake(corpo))
    porta = ProducaoDaMissaoNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    with caplog.at_level(logging.WARNING, logger=_LOGGER_DA_NUVEM):
        leitura = _ler(porta)

    assert leitura is not None
    assert leitura.transcricao == "Plantamos dez mudas."
    assert leitura.devolutiva == "Bom relato."
    assert caplog.text == ""


class _RespostaDeErro:
    def __init__(self, codigo: int, corpo: str):
        self.status_code = codigo
        self.text = corpo

    def raise_for_status(self):
        raise httpx.HTTPStatusError("erro", request=None, response=self)


def test_a_passada_ao_gemini_so_traz_midia_na_foto(monkeypatch):
    """`RF-05-76`, `RN-05-32`: fora da foto, a passada é só de texto — a fala
    já chega transcrita do aparelho e nenhum áudio é montado no corpo."""
    corpos = []

    def _capturar(url, **kwargs):
        corpos.append(kwargs["json"])
        return _RespostaFake(_corpo_gemini(json.dumps({"transcricao": "T", "devolutiva": "D"})))

    monkeypatch.setattr(httpx, "post", _capturar)
    porta = ProducaoDaMissaoNaNuvem(chave_de_api="chave-de-teste", modelo="gemini-2.5-flash")

    porta.ler(
        forma="audio",
        texto="O que a equipe falou.",
        arquivo=None,
        producao_esperada="Relato do plantio.",
    )
    porta.ler(
        forma="foto",
        texto=None,
        arquivo=b"bytes-da-foto",
        producao_esperada="Relato do plantio.",
    )

    partes_da_fala = corpos[0]["contents"][0]["parts"]
    assert all("inlineData" not in parte for parte in partes_da_fala)
    assert any("O que a equipe falou." in parte.get("text", "") for parte in partes_da_fala)

    partes_da_foto = corpos[1]["contents"][0]["parts"]
    midia = next(parte["inlineData"] for parte in partes_da_foto if "inlineData" in parte)
    assert midia["mimeType"] == "image/jpeg"


def test_a_credencial_do_gemini_vai_no_cabecalho_e_nunca_na_url(monkeypatch):
    """A URL entra na mensagem da `HTTPStatusError`, que o log registra:
    chave na _query string_ vira segredo em texto claro (change
    `template-da-missao-no-deepseek`, design — decisão 4)."""
    capturado = {}

    def _capturar(url, **kwargs):
        capturado["url"] = url
        capturado["headers"] = kwargs.get("headers", {})
        return _RespostaFake(_corpo_gemini(json.dumps({"transcricao": "T", "devolutiva": "D"})))

    monkeypatch.setattr(httpx, "post", _capturar)
    porta = ProducaoDaMissaoNaNuvem(chave_de_api="chave-secreta", modelo="gemini-2.5-flash")

    assert _ler(porta) is not None
    assert "chave-secreta" not in capturado["url"]
    assert capturado["headers"]["x-goog-api-key"] == "chave-secreta"


def test_o_corpo_do_erro_de_http_entra_no_log(monkeypatch, caplog):
    corpo = '{"error": {"code": 429, "message": "prepayment credits are depleted"}}'
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _RespostaDeErro(429, corpo))
    porta = ProducaoDaMissaoNaNuvem(chave_de_api="chave-secreta", modelo="gemini-2.5-flash")

    with caplog.at_level(logging.WARNING, logger="nucleo.producoes"):
        assert _ler(porta) is None

    assert "429" in caplog.text
    assert "prepayment credits are depleted" in caplog.text
    assert "chave-secreta" not in caplog.text
