import pytest

from nucleo.conteudo_institucional.modelo import SecaoInstitucional
from nucleo.conteudo_institucional.regra import ler_conteudo_institucional, publicar_secao
from nucleo.erros import ErroDeValidacao
from nucleo.personas.modelo import Papel


def test_as_tres_secoes_saem_em_ordem_fixa_mesmo_sem_publicacao(sessao):
    secoes = ler_conteudo_institucional(sessao)

    assert [linha.secao for linha in secoes] == [
        SecaoInstitucional.quem_somos,
        SecaoInstitucional.contatos,
        SecaoInstitucional.como_apoiar,
    ]
    assert all(linha.texto is None and linha.video_url is None for linha in secoes)


def test_publicar_grava_texto_autor_e_data_e_a_nova_versao_substitui(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    primeira = publicar_secao(
        sessao, SecaoInstitucional.contatos, texto="Antigo", video_url=None, autor_id=admin.id
    )
    assert primeira.autor_id == admin.id
    assert primeira.publicado_em is not None

    publicar_secao(
        sessao, SecaoInstitucional.contatos, texto="Novo", video_url=None, autor_id=admin.id
    )

    contatos = ler_conteudo_institucional(sessao)[1]
    assert contatos.texto == "Novo"


@pytest.mark.parametrize("texto", ["", "   "])
def test_texto_ausente_ou_vazio_e_recusado(sessao, criar_persona, texto):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as erro:
        publicar_secao(
            sessao, SecaoInstitucional.contatos, texto=texto, video_url=None, autor_id=admin.id
        )

    assert erro.value.campo == "texto"


def test_video_so_em_quem_somos_e_so_em_https(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    publicar_secao(
        sessao,
        SecaoInstitucional.quem_somos,
        texto="Quem somos",
        video_url="https://videos.exemplo.org/apresentacao",
        autor_id=admin.id,
    )
    assert ler_conteudo_institucional(sessao)[0].video_url == (
        "https://videos.exemplo.org/apresentacao"
    )

    for secao, link in [
        (SecaoInstitucional.contatos, "https://videos.exemplo.org/a"),
        (SecaoInstitucional.quem_somos, "http://videos.exemplo.org/a"),
        (SecaoInstitucional.quem_somos, "https://"),
    ]:
        with pytest.raises(ErroDeValidacao) as erro:
            publicar_secao(sessao, secao, texto="Texto", video_url=link, autor_id=admin.id)
        assert erro.value.campo == "video_url"


def test_publicar_sem_o_link_o_retira(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    publicar_secao(
        sessao,
        SecaoInstitucional.quem_somos,
        texto="Quem somos",
        video_url="https://videos.exemplo.org/a",
        autor_id=admin.id,
    )

    publicar_secao(
        sessao, SecaoInstitucional.quem_somos, texto="Quem somos", video_url=None, autor_id=admin.id
    )

    assert ler_conteudo_institucional(sessao)[0].video_url is None
