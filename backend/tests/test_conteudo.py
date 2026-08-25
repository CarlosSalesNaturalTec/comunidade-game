import uuid

import pytest

from nucleo.conteudos.modelo import AutoriaDoConteudo, ConteudoDaMissao, TipoDeConteudo
from nucleo.conteudos.regra import criar_conteudo
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.livro_razao.modelo import Lancamento
from nucleo.personas.modelo import Papel
from nucleo.poderes.modelo import NaturezaDoPoder


def _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, natureza=NaturezaDoPoder.de_guerreiro)
    trilha = criar_trilha(mestre, poder=poder)
    missao = criar_missao(trilha, mestre)
    return mestre, missao


# --- 6.1: autoria estrita, os cinco tipos, fonte do terceiro ---------------


def test_mestre_autor_cria_conteudo_de_texto(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)

    conteudo = criar_conteudo(
        sessao,
        operador=mestre,
        missao=missao,
        tipo="texto",
        ordem=1,
        corpo="Texto da missão, sem marcação alguma.",
        endereco=None,
        autoria="propria",
        fonte=None,
    )
    sessao.commit()

    assert conteudo.missao_id == missao.id
    assert conteudo.ordem == 1
    assert conteudo.tipo == TipoDeConteudo.texto
    assert conteudo.corpo == "Texto da missão, sem marcação alguma."
    assert conteudo.autor_id == mestre.id


def test_mestre_que_nao_e_autor_e_recusado(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    mestre_autor, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    outro_mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        criar_conteudo(
            sessao,
            operador=outro_mestre,
            missao=missao,
            tipo="texto",
            ordem=1,
            corpo="Texto.",
            endereco=None,
            autoria="propria",
            fonte=None,
        )
    assert sessao.query(ConteudoDaMissao).count() == 0


def test_admin_nao_escreve_conteudo(sessao, criar_persona, criar_poder, criar_trilha, criar_missao):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    admin = criar_persona(Papel.admin)

    with pytest.raises(PermissaoNegada):
        criar_conteudo(
            sessao,
            operador=admin,
            missao=missao,
            tipo="texto",
            ordem=1,
            corpo="Texto.",
            endereco=None,
            autoria="propria",
            fonte=None,
        )
    assert sessao.query(ConteudoDaMissao).count() == 0


def test_link_externo_e_gravado_com_endereco(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)

    conteudo = criar_conteudo(
        sessao,
        operador=mestre,
        missao=missao,
        tipo="link_externo",
        ordem=1,
        corpo=None,
        endereco="https://video.exemplo.org/aula",
        autoria="propria",
        fonte=None,
    )
    sessao.commit()

    assert conteudo.endereco == "https://video.exemplo.org/aula"
    assert conteudo.referencia is None


def test_texto_sem_corpo_e_recusado(sessao, criar_persona, criar_poder, criar_trilha, criar_missao):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_conteudo(
            sessao,
            operador=mestre,
            missao=missao,
            tipo="texto",
            ordem=1,
            corpo=None,
            endereco=None,
            autoria="propria",
            fonte=None,
        )
    assert excinfo.value.campo == "corpo"
    assert sessao.query(ConteudoDaMissao).count() == 0


def test_link_sem_endereco_e_recusado(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_conteudo(
            sessao,
            operador=mestre,
            missao=missao,
            tipo="link_externo",
            ordem=1,
            corpo=None,
            endereco=None,
            autoria="propria",
            fonte=None,
        )
    assert excinfo.value.campo == "endereco"


@pytest.mark.parametrize("tipo", ["imagem", "video", "arquivo"])
def test_conteudo_de_arquivo_nasce_sem_bytes(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao, tipo
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)

    conteudo = criar_conteudo(
        sessao,
        operador=mestre,
        missao=missao,
        tipo=tipo,
        ordem=1,
        corpo=None,
        endereco=None,
        autoria="propria",
        fonte=None,
    )
    sessao.commit()

    assert conteudo.referencia is None
    assert conteudo.tamanho is None


def test_conteudo_de_terceiro_com_fonte_e_aceito(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)

    conteudo = criar_conteudo(
        sessao,
        operador=mestre,
        missao=missao,
        tipo="texto",
        ordem=1,
        corpo="Trecho citado.",
        endereco=None,
        autoria="terceiro",
        fonte="Autor Exemplo, 2020.",
    )
    sessao.commit()

    assert conteudo.autoria == AutoriaDoConteudo.terceiro
    assert conteudo.fonte == "Autor Exemplo, 2020."


def test_conteudo_de_terceiro_sem_fonte_e_recusado(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_conteudo(
            sessao,
            operador=mestre,
            missao=missao,
            tipo="texto",
            ordem=1,
            corpo="Trecho citado.",
            endereco=None,
            autoria="terceiro",
            fonte=None,
        )
    assert excinfo.value.campo == "fonte"
    assert sessao.query(ConteudoDaMissao).count() == 0


def test_conteudo_proprio_dispensa_fonte(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)

    conteudo = criar_conteudo(
        sessao,
        operador=mestre,
        missao=missao,
        tipo="texto",
        ordem=1,
        corpo="Texto próprio.",
        endereco=None,
        autoria="propria",
        fonte=None,
    )
    sessao.commit()

    assert conteudo.fonte is None


# --- 6.2 e 6.3: envio pela sessão retomável --------------------------------


def _cabecalhos(chave, criar_sessao_de_teste, persona):
    token, _ = criar_sessao_de_teste(persona)
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def _criar_conteudo_de_arquivo_pela_rota(cliente, cabecalhos, missao_id, tipo="arquivo"):
    resposta = cliente.post(
        f"/v1/missoes/{missao_id}/conteudos",
        json={"tipo": tipo, "ordem": 1, "autoria": "propria"},
        headers=cabecalhos,
    )
    assert resposta.status_code == 201
    return resposta.json()["id"]


def test_sessao_e_aberta_e_endereco_volta_ao_cliente(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudo_id = _criar_conteudo_de_arquivo_pela_rota(cliente, cabecalhos, missao.id, "video")

    resposta = cliente.post(
        f"/v1/conteudos/{conteudo_id}/arquivo",
        json={"tipo_mime": "video/mp4", "tamanho_declarado": 10},
        headers=cabecalhos,
    )

    assert resposta.status_code == 201
    endereco = resposta.json()["endereco_da_sessao"]
    assert endereco.startswith("/v1/armazenamento/sessoes/")


def test_sessao_pedida_por_quem_nao_e_autor_e_recusada(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    outro_mestre = criar_persona(Papel.mestre)
    chave, _ = criar_chave()
    cabecalhos_autor = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudo_id = _criar_conteudo_de_arquivo_pela_rota(
        cliente, cabecalhos_autor, missao.id, "video"
    )
    cabecalhos_outro = _cabecalhos(chave, criar_sessao_de_teste, outro_mestre)

    resposta = cliente.post(
        f"/v1/conteudos/{conteudo_id}/arquivo",
        json={"tipo_mime": "video/mp4", "tamanho_declarado": 10},
        headers=cabecalhos_outro,
    )

    assert resposta.status_code == 403


def test_formato_fora_da_lista_e_recusado_antes_do_envio(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudo_id = _criar_conteudo_de_arquivo_pela_rota(cliente, cabecalhos, missao.id, "arquivo")

    resposta = cliente.post(
        f"/v1/conteudos/{conteudo_id}/arquivo",
        json={"tipo_mime": "application/x-executable", "tamanho_declarado": 10},
        headers=cabecalhos,
    )

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "tipo_mime"


def test_video_acima_do_teto_e_recusado_com_413(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudo_id = _criar_conteudo_de_arquivo_pela_rota(cliente, cabecalhos, missao.id, "video")

    resposta = cliente.post(
        f"/v1/conteudos/{conteudo_id}/arquivo",
        json={"tipo_mime": "video/mp4", "tamanho_declarado": 240 * 1024 * 1024},
        headers=cabecalhos,
    )

    assert resposta.status_code == 413


def test_arquivo_de_apoio_acima_do_teto_e_recusado_com_413(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudo_id = _criar_conteudo_de_arquivo_pela_rota(cliente, cabecalhos, missao.id, "arquivo")

    resposta = cliente.post(
        f"/v1/conteudos/{conteudo_id}/arquivo",
        json={"tipo_mime": "application/pdf", "tamanho_declarado": 32 * 1024 * 1024},
        headers=cabecalhos,
    )

    assert resposta.status_code == 413


def test_dois_videos_na_mesma_missao_sao_aceitos(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    primeiro_id = _criar_conteudo_de_arquivo_pela_rota(cliente, cabecalhos, missao.id, "video")
    segundo_id = _criar_conteudo_de_arquivo_pela_rota(cliente, cabecalhos, missao.id, "video")

    resposta_primeiro = cliente.post(
        f"/v1/conteudos/{primeiro_id}/arquivo",
        json={"tipo_mime": "video/mp4", "tamanho_declarado": 180 * 1024 * 1024},
        headers=cabecalhos,
    )
    resposta_segundo = cliente.post(
        f"/v1/conteudos/{segundo_id}/arquivo",
        json={"tipo_mime": "video/mp4", "tamanho_declarado": 150 * 1024 * 1024},
        headers=cabecalhos,
    )

    assert resposta_primeiro.status_code == 201
    assert resposta_segundo.status_code == 201


def test_retomada_depois_de_corte_no_meio_produz_arquivo_identico(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudo_id = _criar_conteudo_de_arquivo_pela_rota(cliente, cabecalhos, missao.id, "arquivo")

    conteudo_do_arquivo = b"0123456789"
    resposta_sessao = cliente.post(
        f"/v1/conteudos/{conteudo_id}/arquivo",
        json={"tipo_mime": "application/pdf", "tamanho_declarado": len(conteudo_do_arquivo)},
        headers=cabecalhos,
    )
    endereco = resposta_sessao.json()["endereco_da_sessao"]

    # Primeira parte enviada, depois a rede cai.
    resposta_parte1 = cliente.put(
        endereco,
        content=conteudo_do_arquivo[:6],
        headers={**cabecalhos, "Content-Range": "bytes 0-5/10"},
    )
    assert resposta_parte1.status_code == 308
    assert resposta_parte1.headers["Range"] == "bytes=0-5"

    # O cliente consulta o que já foi recebido, sem enviar bytes.
    resposta_status = cliente.put(
        endereco, content=b"", headers={**cabecalhos, "Content-Range": "bytes */10"}
    )
    assert resposta_status.status_code == 308
    assert resposta_status.headers["Range"] == "bytes=0-5"

    # E retoma exatamente do ponto já recebido.
    resposta_parte2 = cliente.put(
        endereco,
        content=conteudo_do_arquivo[6:],
        headers={**cabecalhos, "Content-Range": "bytes 6-9/10"},
    )
    assert resposta_parte2.status_code == 200

    resposta_confirmacao = cliente.patch(f"/v1/conteudos/{conteudo_id}/arquivo", headers=cabecalhos)
    assert resposta_confirmacao.status_code == 200
    corpo = resposta_confirmacao.json()
    assert corpo["tamanho"] == len(conteudo_do_arquivo)
    assert corpo["referencia"] is not None


def test_bytes_nao_passam_pelo_nucleo(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
    sessao,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudo_id = _criar_conteudo_de_arquivo_pela_rota(cliente, cabecalhos, missao.id, "video")

    conteudo_do_arquivo = b"x" * 200
    resposta_sessao = cliente.post(
        f"/v1/conteudos/{conteudo_id}/arquivo",
        json={"tipo_mime": "video/mp4", "tamanho_declarado": len(conteudo_do_arquivo)},
        headers=cabecalhos,
    )
    endereco = resposta_sessao.json()["endereco_da_sessao"]
    cliente.put(
        endereco,
        content=conteudo_do_arquivo,
        headers={**cabecalhos, "Content-Range": f"bytes 0-{len(conteudo_do_arquivo) - 1}/200"},
    )
    cliente.patch(f"/v1/conteudos/{conteudo_id}/arquivo", headers=cabecalhos)

    conteudo = sessao.get(ConteudoDaMissao, uuid.UUID(conteudo_id))
    assert conteudo.tamanho == 200
    # Nenhuma coluna do modelo carrega bytes — só a referência opaca.
    assert isinstance(conteudo.referencia, str)


def test_conteudo_sem_envio_confirmado_nao_serve_bytes(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)

    conteudo = criar_conteudo(
        sessao,
        operador=mestre,
        missao=missao,
        tipo="video",
        ordem=1,
        corpo=None,
        endereco=None,
        autoria="propria",
        fonte=None,
    )
    sessao.commit()

    assert conteudo.referencia is None


def test_envio_que_diverge_do_tamanho_declarado_e_recusado_ao_fim(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
    sessao,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudo_id = _criar_conteudo_de_arquivo_pela_rota(cliente, cabecalhos, missao.id, "arquivo")

    # Declara 10 bytes; o que diverge é o **recebido** ao fim, acima do
    # teto de 20 MB do arquivo de apoio.
    resposta_sessao = cliente.post(
        f"/v1/conteudos/{conteudo_id}/arquivo",
        json={"tipo_mime": "application/pdf", "tamanho_declarado": 10},
        headers=cabecalhos,
    )
    endereco = resposta_sessao.json()["endereco_da_sessao"]

    tamanho_real = 21 * 1024 * 1024
    cliente.put(
        endereco,
        content=b"x" * tamanho_real,
        headers={**cabecalhos, "Content-Range": f"bytes 0-{tamanho_real - 1}/{tamanho_real}"},
    )

    resposta_confirmacao = cliente.patch(f"/v1/conteudos/{conteudo_id}/arquivo", headers=cabecalhos)

    assert resposta_confirmacao.status_code == 413
    conteudo = sessao.get(ConteudoDaMissao, uuid.UUID(conteudo_id))
    assert conteudo.referencia is None


# --- 6.4: ausência deliberada de medição de consumo de nuvem ---------------


def test_envio_confirmado_nao_gera_lancamento_nem_altera_saldo(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
    sessao,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudo_id = _criar_conteudo_de_arquivo_pela_rota(cliente, cabecalhos, missao.id, "video")

    lancamentos_antes = sessao.query(Lancamento).count()

    conteudo_do_arquivo = b"x" * (200 * 1024 * 1024)
    resposta_sessao = cliente.post(
        f"/v1/conteudos/{conteudo_id}/arquivo",
        json={"tipo_mime": "video/mp4", "tamanho_declarado": len(conteudo_do_arquivo)},
        headers=cabecalhos,
    )
    endereco = resposta_sessao.json()["endereco_da_sessao"]
    cliente.put(
        endereco,
        content=conteudo_do_arquivo,
        headers={
            **cabecalhos,
            "Content-Range": f"bytes 0-{len(conteudo_do_arquivo) - 1}/{len(conteudo_do_arquivo)}",
        },
    )
    resposta_confirmacao = cliente.patch(f"/v1/conteudos/{conteudo_id}/arquivo", headers=cabecalhos)

    assert resposta_confirmacao.status_code == 200
    assert sessao.query(Lancamento).count() == lancamentos_antes


def test_nenhuma_rota_expoe_total_de_bytes(cliente, criar_chave):
    """`RF-09-20`, `RN-09-07`: nenhum contador de bytes por missão, trilha
    ou Mestre — o desenho não constrói a rota, então ela simplesmente não
    existe."""
    chave, _ = criar_chave()
    resposta = cliente.get("/v1/missoes/consumo", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 404
