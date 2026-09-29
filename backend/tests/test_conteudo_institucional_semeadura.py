from nucleo.cli import semear
from nucleo.conteudo_institucional.modelo import SecaoInstitucional
from nucleo.conteudo_institucional.regra import ler_conteudo_institucional, publicar_secao
from nucleo.conteudo_institucional.semeadura import semear_conteudo_institucional
from nucleo.personas.modelo import Papel


def test_banco_vazio_recebe_pix_titular_nota_e_licencas_e_contatos_fica_vazio(sessao):
    semeadas = semear_conteudo_institucional(sessao)

    quem_somos, contatos, como_apoiar = ler_conteudo_institucional(sessao)
    assert set(semeadas) == {SecaoInstitucional.quem_somos, SecaoInstitucional.como_apoiar}
    assert "51.730.395/0001-19" in como_apoiar.texto
    assert "Robô Educa — Kits Robóticos Educacionais" in como_apoiar.texto
    assert "## Nota de transparência sobre IA" in quem_somos.texto
    assert "## Licenças" in quem_somos.texto
    assert contatos.texto is None
    assert quem_somos.autor_id is None


def test_a_nota_declara_construcao_atendimento_e_ausencia_de_perfilamento(sessao):
    semear_conteudo_institucional(sessao)

    nota = ler_conteudo_institucional(sessao)[0].texto.split("## Licenças")[0]

    assert "Claude" in nota
    assert "Gemini" in nota and "DeepSeek" in nota
    assert "não faz perfil da criança" in nota
    assert "bloco Licenças" in nota


def test_repetir_a_semeadura_nao_altera_e_a_edicao_de_um_admin_sobrevive(sessao, criar_persona):
    semear_conteudo_institucional(sessao)
    admin = criar_persona(Papel.admin)
    publicar_secao(
        sessao,
        SecaoInstitucional.como_apoiar,
        texto="Outra chave",
        video_url=None,
        autor_id=admin.id,
    )
    sessao.commit()

    semeadas = semear_conteudo_institucional(sessao)

    assert semeadas == []
    assert ler_conteudo_institucional(sessao)[2].texto == "Outra chave"


def test_o_comando_de_implantacao_semeia_o_conteudo(monkeypatch, conexao, configuracao, capsys):
    from sqlalchemy.orm import sessionmaker

    monkeypatch.setattr("nucleo.cli.obter_configuracao", lambda: configuracao)
    fabrica = sessionmaker(
        bind=conexao, expire_on_commit=False, join_transaction_mode="create_savepoint"
    )
    monkeypatch.setattr("nucleo.cli.obter_fabrica_de_sessao", lambda: fabrica)

    semear()
    assert "Conteúdo institucional semeado" in capsys.readouterr().out

    semear()
    assert "Conteúdo institucional já existia" in capsys.readouterr().out
