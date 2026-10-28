import importlib.util
import pathlib
import uuid

import pytest
import sqlalchemy as sa

from nucleo.armazenamento.disco import ArmazenamentoEmDisco
from nucleo.conteudos.modelo import AutoriaDoConteudo, ConteudoDaMissao, TipoDeConteudo
from nucleo.conteudos.regra import (
    consultar_conteudos_da_missao,
    corrigir_conteudo,
    criar_conteudo,
    mover_conteudo,
    remover_conteudo,
)
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.livro_razao.modelo import Lancamento
from nucleo.personas.modelo import Papel
from nucleo.poderes.modelo import NaturezaDoPoder
from nucleo.trilhas.modelo import SituacaoDaTrilha


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
        json={"tipo": tipo, "autoria": "propria"},
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


# --- Conserto: o tipo do arquivo e a saída de bytes (`RF-05-11`,
# `RF-09-16`, `RF-09-17`, `RF-09-25`) --------------------------------------


def _conteudo_com_arquivo_enviado(
    cliente, cabecalhos, missao_id, *, tipo="imagem", tipo_mime="image/png", corpo=b"PNG-falso"
):
    """Cria o conteúdo, envia os bytes e confirma — o caminho inteiro por
    HTTP, como o Mestre o percorre."""
    conteudo_id = _criar_conteudo_de_arquivo_pela_rota(cliente, cabecalhos, missao_id, tipo)
    resposta_sessao = cliente.post(
        f"/v1/conteudos/{conteudo_id}/arquivo",
        json={"tipo_mime": tipo_mime, "tamanho_declarado": len(corpo)},
        headers=cabecalhos,
    )
    assert resposta_sessao.status_code == 201
    endereco = resposta_sessao.json()["endereco_da_sessao"]
    cliente.put(
        endereco,
        content=corpo,
        headers={**cabecalhos, "Content-Range": f"bytes 0-{len(corpo) - 1}/{len(corpo)}"},
    )
    assert (
        cliente.patch(f"/v1/conteudos/{conteudo_id}/arquivo", headers=cabecalhos).status_code == 200
    )
    return conteudo_id


def test_confirmacao_grava_o_tipo_apurado_no_armazenamento(
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

    conteudo_id = _conteudo_com_arquivo_enviado(cliente, cabecalhos, missao.id)

    conteudo = sessao.get(ConteudoDaMissao, uuid.UUID(conteudo_id))
    assert conteudo.tipo_do_arquivo == "image/png"


def test_mestre_autor_le_os_bytes_do_proprio_conteudo(
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
    conteudo_id = _conteudo_com_arquivo_enviado(
        cliente, cabecalhos, missao.id, corpo=b"bytes-da-imagem"
    )

    resposta = cliente.get(f"/v1/conteudos/{conteudo_id}/arquivo", headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.content == b"bytes-da-imagem"
    assert resposta.headers["content-type"].startswith("image/png")


def test_guerreiro_inscrito_le_os_bytes(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
    criar_inscricao_na_trilha,
):
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, natureza=NaturezaDoPoder.de_guerreiro)
    trilha = criar_trilha(mestre, poder=poder)
    missao = criar_missao(trilha, mestre)
    chave, _ = criar_chave()
    cabecalhos_do_mestre = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudo_id = _conteudo_com_arquivo_enviado(cliente, cabecalhos_do_mestre, missao.id)

    guerreiro = criar_persona(Papel.guerreiro)
    criar_inscricao_na_trilha(guerreiro, trilha)
    cabecalhos_do_guerreiro = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)

    resposta = cliente.get(f"/v1/conteudos/{conteudo_id}/arquivo", headers=cabecalhos_do_guerreiro)

    assert resposta.status_code == 200
    assert resposta.content == b"PNG-falso"


def test_persona_nao_autora_nem_inscrita_e_recusada_com_403(
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
    cabecalhos_do_mestre = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudo_id = _conteudo_com_arquivo_enviado(cliente, cabecalhos_do_mestre, missao.id)

    estranho = criar_persona(Papel.guerreiro)
    cabecalhos_do_estranho = _cabecalhos(chave, criar_sessao_de_teste, estranho)

    resposta = cliente.get(f"/v1/conteudos/{conteudo_id}/arquivo", headers=cabecalhos_do_estranho)

    assert resposta.status_code == 403


def test_conteudo_sem_arquivo_responde_404(
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

    # Conteúdo de texto nunca tem arquivo; o de vídeo sem envio confirmado
    # também não.
    resposta_texto = cliente.post(
        f"/v1/missoes/{missao.id}/conteudos",
        json={"tipo": "texto", "corpo": "Só texto.", "autoria": "propria"},
        headers=cabecalhos,
    )
    id_do_texto = resposta_texto.json()["id"]
    id_sem_envio = _criar_conteudo_de_arquivo_pela_rota(cliente, cabecalhos, missao.id, "video")

    assert (
        cliente.get(f"/v1/conteudos/{id_do_texto}/arquivo", headers=cabecalhos).status_code == 404
    )
    assert (
        cliente.get(f"/v1/conteudos/{id_sem_envio}/arquivo", headers=cabecalhos).status_code == 404
    )


def test_leitura_alcanca_trilha_em_rascunho_para_o_autor(
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
    conteudo_id = _conteudo_com_arquivo_enviado(cliente, cabecalhos, missao.id)

    # A trilha nunca foi publicada: a autoria basta, a publicação não é
    # exigida (`RF-09-25` — a pré-visualização é do rascunho).
    resposta = cliente.get(f"/v1/conteudos/{conteudo_id}/arquivo", headers=cabecalhos)

    assert resposta.status_code == 200


def test_conteudo_gravado_antes_da_coluna_sai_com_tipo_indeterminado(
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
    conteudo_id = _conteudo_com_arquivo_enviado(cliente, cabecalhos, missao.id)

    # Linha gravada antes da coluna existir: referência sim, tipo não.
    conteudo = sessao.get(ConteudoDaMissao, uuid.UUID(conteudo_id))
    conteudo.tipo_do_arquivo = None
    sessao.commit()

    resposta = cliente.get(f"/v1/conteudos/{conteudo_id}/arquivo", headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.headers["content-type"].startswith("application/octet-stream")


# --- fatia 24: corrigir, remover, exibir e ordenar -------------------------
#
# `RF-09-123` a `RF-09-126`, `RN-09-45` e `RN-09-46`, das quatro decisões do
# fundador de 2026-10-27.


def _tres_conteudos_de_texto(sessao, missao, mestre):
    """Três conteúdos pela regra, que já atribui a ordem — 1, 2 e 3."""
    return [
        criar_conteudo(
            sessao,
            operador=mestre,
            missao=missao,
            tipo="texto",
            corpo=f"Corpo {posicao}.",
            endereco=None,
            autoria="propria",
            fonte=None,
        )
        for posicao in (1, 2, 3)
    ]


def test_o_conteudo_novo_entra_por_ultimo(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    """`RF-09-126`: a ordem é do núcleo, e cresce — antes, todo conteúdo
    nascia com a ordem 1 que o cliente declarava."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)

    conteudos = _tres_conteudos_de_texto(sessao, missao, mestre)

    assert [conteudo.ordem for conteudo in conteudos] == [1, 2, 3]
    assert [c.corpo for c in consultar_conteudos_da_missao(sessao, missao.id)] == [
        "Corpo 1.",
        "Corpo 2.",
        "Corpo 3.",
    ]


def test_mandar_a_ordem_na_criacao_e_recusado(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
):
    """`RF-09-126`, quebra de contrato (design — decisão 2): `ordem` saiu do
    corpo, e `extra="forbid"` recusa quem insistir."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)

    resposta = cliente.post(
        f"/v1/missoes/{missao.id}/conteudos",
        json={"tipo": "texto", "ordem": 1, "corpo": "Com ordem.", "autoria": "propria"},
        headers=cabecalhos,
    )

    assert resposta.status_code == 422


def test_o_conteudo_ja_gravado_e_renumerado(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao, criar_conteudo_da_missao
):
    """`RF-09-126`: exercita o **mesmo** SQL da revisão `c4e81b2a9d60`,
    importado dela, sobre o estado de partida — todos em `ordem = 1`."""
    caminho = (
        pathlib.Path(__file__).resolve().parent.parent
        / "alembic"
        / "versions"
        / "c4e81b2a9d60_ordem_do_conteudo_da_missao.py"
    )
    especificacao = importlib.util.spec_from_file_location("revisao_da_ordem", caminho)
    revisao = importlib.util.module_from_spec(especificacao)
    especificacao.loader.exec_module(revisao)

    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    for posicao in (1, 2, 3):
        criar_conteudo_da_missao(missao, mestre, ordem=1, corpo=f"Corpo {posicao}.")

    sessao.execute(sa.text(revisao.SQL_RENUMERA_A_ORDEM))
    sessao.commit()

    conteudos = consultar_conteudos_da_missao(sessao, missao.id)
    assert [conteudo.ordem for conteudo in conteudos] == [1, 2, 3]
    assert [conteudo.corpo for conteudo in conteudos] == ["Corpo 1.", "Corpo 2.", "Corpo 3."]


def test_mestre_autor_corrige_o_corpo_do_texto(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    """`RF-09-123`: corrigir não muda a missão nem a ordem."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudo = _tres_conteudos_de_texto(sessao, missao, mestre)[1]

    corrigido = corrigir_conteudo(
        sessao,
        conteudo,
        operador=mestre,
        tipo=None,
        corpo="Corpo corrigido.",
        endereco=None,
        autoria="propria",
        fonte=None,
    )

    assert corrigido.corpo == "Corpo corrigido."
    assert corrigido.ordem == 2
    assert corrigido.missao_id == missao.id


def test_a_correcao_alcanca_a_trilha_publicada(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    """`RF-09-123`, decisão do fundador de 2026-10-27: publicada inclusive, e
    a situação não se altera."""
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, natureza=NaturezaDoPoder.de_guerreiro)
    trilha = criar_trilha(mestre, poder=poder, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    conteudo = criar_conteudo(
        sessao,
        operador=mestre,
        missao=missao,
        tipo="texto",
        corpo="Corpo publicado.",
        endereco=None,
        autoria="terceiro",
        fonte="Fonte errada.",
    )

    corrigido = corrigir_conteudo(
        sessao,
        conteudo,
        operador=mestre,
        tipo=None,
        corpo="Corpo publicado.",
        endereco=None,
        autoria="terceiro",
        fonte="Fonte certa, 2026.",
    )

    assert corrigido.fonte == "Fonte certa, 2026."
    assert trilha.situacao == SituacaoDaTrilha.publicada


def test_mestre_que_nao_e_autor_nao_corrige(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    """`RF-09-123`, `RN-09-16`: o mesmo 403 da criação."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudo = _tres_conteudos_de_texto(sessao, missao, mestre)[0]
    outro = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        corrigir_conteudo(
            sessao,
            conteudo,
            operador=outro,
            tipo=None,
            corpo="Invadido.",
            endereco=None,
            autoria="propria",
            fonte=None,
        )
    assert conteudo.corpo == "Corpo 1."


def test_admin_nao_corrige_conteudo(sessao, criar_persona, criar_poder, criar_trilha, criar_missao):
    """`RF-09-123`: o Admin audita e despublica a trilha, não a redige."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudo = _tres_conteudos_de_texto(sessao, missao, mestre)[0]
    admin = criar_persona(Papel.admin)

    with pytest.raises(PermissaoNegada):
        corrigir_conteudo(
            sessao,
            conteudo,
            operador=admin,
            tipo=None,
            corpo="Escrito pelo Admin.",
            endereco=None,
            autoria="propria",
            fonte=None,
        )


def test_a_correcao_confere_a_coerencia_do_tipo(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    """`RF-09-123`: corrigir não é porta de entrada do estado que a criação
    recusa."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudo = _tres_conteudos_de_texto(sessao, missao, mestre)[0]

    with pytest.raises(ErroDeValidacao) as erro:
        corrigir_conteudo(
            sessao,
            conteudo,
            operador=mestre,
            tipo=None,
            corpo="   ",
            endereco=None,
            autoria="propria",
            fonte=None,
        )
    assert erro.value.campo == "corpo"


def test_a_correcao_confere_a_fonte_do_terceiro(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    """`RF-09-24`: passar a autoria a terceiro sem fonte é recusado."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudo = _tres_conteudos_de_texto(sessao, missao, mestre)[0]

    with pytest.raises(ErroDeValidacao) as erro:
        corrigir_conteudo(
            sessao,
            conteudo,
            operador=mestre,
            tipo=None,
            corpo="Corpo 1.",
            endereco=None,
            autoria="terceiro",
            fonte=None,
        )
    assert erro.value.campo == "fonte"


def test_trocar_o_tipo_e_recusado(sessao, criar_persona, criar_poder, criar_trilha, criar_missao):
    """`RN-09-45`: a recusa diz o caminho — remover e cadastrar outro."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudo = _tres_conteudos_de_texto(sessao, missao, mestre)[0]

    with pytest.raises(ErroDeValidacao) as erro:
        corrigir_conteudo(
            sessao,
            conteudo,
            operador=mestre,
            tipo="video",
            corpo="Corpo 1.",
            endereco=None,
            autoria="propria",
            fonte=None,
        )
    assert erro.value.campo == "tipo"
    assert "remova este conteúdo" in str(erro.value.mensagem)
    assert conteudo.tipo == TipoDeConteudo.texto


def test_reabrir_envio_de_conteudo_confirmado_e_recusado(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
):
    """`RN-09-45`, design — decisão 5: sem esta guarda o arquivo é trocável
    pela porta dos fundos, porque a referência deriva do id do conteúdo."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudo_id = _conteudo_com_arquivo_enviado(cliente, cabecalhos, missao.id)

    resposta = cliente.post(
        f"/v1/conteudos/{conteudo_id}/arquivo",
        json={"tipo_mime": "image/png", "tamanho_declarado": 9},
        headers=cabecalhos,
    )

    assert resposta.status_code == 422
    # Os bytes do primeiro envio seguem servidos.
    assert cliente.get(f"/v1/conteudos/{conteudo_id}/arquivo", headers=cabecalhos).content == (
        b"PNG-falso"
    )


def test_o_conteudo_de_texto_e_removido(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
    sessao,
):
    """`RF-09-124`: apaga de verdade — nada aponta para o conteúdo."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudos = _tres_conteudos_de_texto(sessao, missao, mestre)
    sessao.commit()

    resposta = cliente.delete(f"/v1/conteudos/{conteudos[0].id}", headers=cabecalhos)

    assert resposta.status_code == 204
    assert [c.corpo for c in consultar_conteudos_da_missao(sessao, missao.id)] == [
        "Corpo 2.",
        "Corpo 3.",
    ]


def test_remover_conteudo_com_arquivo_apaga_os_bytes(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
    tmp_path,
):
    """`RF-09-124`, design — decisão 6: byte algum fica órfão num
    armazenamento que `RF-09-20` mantém fora da medição."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudo_id = _conteudo_com_arquivo_enviado(cliente, cabecalhos, missao.id)
    arquivo = tmp_path / "armazenamento" / "conteudos" / conteudo_id / "arquivo"
    assert arquivo.exists()

    resposta = cliente.delete(f"/v1/conteudos/{conteudo_id}", headers=cabecalhos)

    assert resposta.status_code == 204
    assert not arquivo.exists()


def test_remover_conteudo_sem_envio_confirmado_nao_falha(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
):
    """`RF-09-124`: sem referência, nenhuma remoção de arquivo é tentada."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    conteudo_id = _criar_conteudo_de_arquivo_pela_rota(cliente, cabecalhos, missao.id)

    assert cliente.delete(f"/v1/conteudos/{conteudo_id}", headers=cabecalhos).status_code == 204


def test_a_remocao_alcanca_a_trilha_publicada(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
    sessao,
):
    """`RF-09-124`, decisão do fundador de 2026-10-27."""
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, natureza=NaturezaDoPoder.de_guerreiro)
    trilha = criar_trilha(mestre, poder=poder, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    conteudo = _tres_conteudos_de_texto(sessao, missao, mestre)[0]
    sessao.commit()
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)

    resposta = cliente.delete(f"/v1/conteudos/{conteudo.id}", headers=cabecalhos)

    assert resposta.status_code == 204
    sessao.refresh(trilha)
    assert trilha.situacao == SituacaoDaTrilha.publicada


def test_quem_nao_e_o_autor_nao_remove(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao, tmp_path
):
    """`RF-09-124`: outro Mestre e o Admin são recusados, como na criação."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudo = _tres_conteudos_de_texto(sessao, missao, mestre)[0]

    for intruso in (criar_persona(Papel.mestre), criar_persona(Papel.admin)):
        with pytest.raises(PermissaoNegada):
            remover_conteudo(
                sessao,
                conteudo,
                operador=intruso,
                armazenamento=ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes")),
            )
    assert consultar_conteudos_da_missao(sessao, missao.id)[0].id == conteudo.id


def test_os_restantes_nao_sao_renumerados(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao, tmp_path
):
    """`RF-09-124`: a ordem é sequência, não índice — remover deixa lacuna, e
    é o que `remover_pergunta_do_desbloqueio` já faz no quiz."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudos = _tres_conteudos_de_texto(sessao, missao, mestre)

    remover_conteudo(
        sessao,
        conteudos[1],
        operador=mestre,
        armazenamento=ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes")),
    )

    restantes = consultar_conteudos_da_missao(sessao, missao.id)
    assert [conteudo.ordem for conteudo in restantes] == [1, 3]


def test_remocao_nao_gera_lancamento(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao, tmp_path
):
    """`RF-09-20`, `RN-09-07`: o custo de nuvem entra pela fatura do período,
    e nenhuma aplicação o apura por ato — na remoção como no envio."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudo = _tres_conteudos_de_texto(sessao, missao, mestre)[0]
    antes = sessao.query(Lancamento).count()

    remover_conteudo(
        sessao,
        conteudo,
        operador=mestre,
        armazenamento=ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes")),
    )

    assert sessao.query(Lancamento).count() == antes


def test_o_conteudo_sobe_uma_posicao(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    """`RF-09-126`: troca com o vizinho, e a leitura segue a nova ordem."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudos = _tres_conteudos_de_texto(sessao, missao, mestre)

    mover_conteudo(sessao, conteudos[1], operador=mestre, direcao="cima")

    assert [c.corpo for c in consultar_conteudos_da_missao(sessao, missao.id)] == [
        "Corpo 2.",
        "Corpo 1.",
        "Corpo 3.",
    ]


def test_mover_o_primeiro_para_cima_e_recusado(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    """`RF-09-126`: recusa em linguagem simples, sem alterar nada."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudos = _tres_conteudos_de_texto(sessao, missao, mestre)

    with pytest.raises(ErroDeValidacao) as erro:
        mover_conteudo(sessao, conteudos[0], operador=mestre, direcao="cima")

    assert "já é o primeiro" in str(erro.value.mensagem)
    assert [c.ordem for c in consultar_conteudos_da_missao(sessao, missao.id)] == [1, 2, 3]


def test_mover_o_ultimo_para_baixo_e_recusado(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    """`RF-09-126`: o outro extremo, pelo mesmo caminho."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudos = _tres_conteudos_de_texto(sessao, missao, mestre)

    with pytest.raises(ErroDeValidacao) as erro:
        mover_conteudo(sessao, conteudos[2], operador=mestre, direcao="baixo")

    assert "já é o último" in str(erro.value.mensagem)


def test_quem_nao_e_o_autor_nao_move(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    """`RF-09-126`: a mesma autoria estrita das demais escritas."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudos = _tres_conteudos_de_texto(sessao, missao, mestre)
    outro = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        mover_conteudo(sessao, conteudos[1], operador=outro, direcao="cima")
    assert [c.ordem for c in consultar_conteudos_da_missao(sessao, missao.id)] == [1, 2, 3]


def test_mover_pela_rota_grava_a_nova_ordem(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
    sessao,
):
    """`RF-09-126`: substantivo de ação, no molde de `/trilhas/{id}/publicacao`."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudos = _tres_conteudos_de_texto(sessao, missao, mestre)
    sessao.commit()
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)

    resposta = cliente.post(
        f"/v1/conteudos/{conteudos[2].id}/ordem",
        json={"direcao": "cima"},
        headers=cabecalhos,
    )

    assert resposta.status_code == 200
    assert resposta.json()["ordem"] == 2


def test_corrigir_pela_rota_devolve_o_conteudo_corrigido(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
    criar_missao,
    sessao,
):
    """`RF-09-123`: a rota devolve o conteúdo no mesmo formato da criação."""
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    conteudo = _tres_conteudos_de_texto(sessao, missao, mestre)[0]
    sessao.commit()
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)

    resposta = cliente.patch(
        f"/v1/conteudos/{conteudo.id}",
        json={"corpo": "Pela rota.", "autoria": "propria"},
        headers=cabecalhos,
    )

    assert resposta.status_code == 200
    assert resposta.json()["corpo"] == "Pela rota."
    assert resposta.json()["ordem"] == 1
