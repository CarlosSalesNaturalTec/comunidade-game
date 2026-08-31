"""A porta da leitura e da devolutiva da produção — `RF-04-46`, `RF-04-47`,
`RF-09-90`, design — decisões 4 e 5."""

import io

from nucleo.livro_razao.modelo import Lancamento
from nucleo.personas.modelo import Papel
from nucleo.producoes.fabrica import dependencia_da_producao_da_missao
from nucleo.producoes.local import ProducaoDaMissaoLocal
from nucleo.producoes.modelo import ProducaoDaMissao
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


def test_local_descarta_foto_e_audio_e_devolve_transcricao_e_devolutiva():
    porta = ProducaoDaMissaoLocal()

    leitura_audio = porta.ler(
        forma="audio", texto=None, arquivo=b"bytes-de-audio", producao_esperada="Uma fala."
    )
    leitura_foto = porta.ler(
        forma="foto", texto=None, arquivo=b"bytes-de-foto", producao_esperada="Um desenho."
    )

    assert leitura_audio is not None
    assert "bytes-de-audio" not in leitura_audio.transcricao
    assert leitura_audio.devolutiva

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


def test_503_na_foto_e_no_audio_quando_leitura_indisponivel(
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

        for forma, tipo in (("audio", "audio/webm"), ("foto", "image/jpeg")):
            resposta = cliente.post(
                f"/v1/equipes/{equipe.id}/producao",
                data={"forma": forma},
                files={"arquivo": (f"arquivo.{forma}", io.BytesIO(b"conteudo-fake"), tipo)},
                headers=_cabecalhos(chave, token),
            )
            assert resposta.status_code == 503

        assert sessao.query(ProducaoDaMissao).count() == 0
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
                data={"forma": "audio"},
                files={"arquivo": ("fala.webm", io.BytesIO(b"segredo-do-audio"), "audio/webm")},
                headers=_cabecalhos(chave, token),
            )

        texto_do_log = " ".join(registro.getMessage() for registro in caplog.records)
        assert "segredo-do-audio" not in texto_do_log
        assert "forma=audio" in texto_do_log
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


def test_503_na_foto_e_no_audio_individuais_quando_leitura_indisponivel(
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

        for forma, tipo in (("audio", "audio/webm"), ("foto", "image/jpeg")):
            resposta = cliente.post(
                f"/v1/eu/missoes/{missao.id}/producao",
                data={"forma": forma, "atividade_id": str(atividade.id)},
                files={"arquivo": (f"arquivo.{forma}", io.BytesIO(b"conteudo-fake"), tipo)},
                headers=_cabecalhos(chave, token),
            )
            assert resposta.status_code == 503

        assert sessao.query(ProducaoDaMissao).count() == 0
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
