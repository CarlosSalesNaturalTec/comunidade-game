from nucleo.cli import semear
from nucleo.conteudo_institucional.modelo import SecaoInstitucional
from nucleo.conteudo_institucional.regra import ler_conteudo_institucional, publicar_secao
from nucleo.conteudo_institucional.semeadura import semear_conteudo_institucional
from nucleo.personas.modelo import Papel

# O título do bloco da nota é contrato: o identificador derivado dele é a
# âncora para onde aponta a etiqueta do texto reescrito por IA das Apps 01 e 05
# (documento 03 §7.1). Mudar esta constante é mudar contrato, não redação.
TITULO_DA_NOTA = "## Nota de transparência sobre IA"


def test_banco_vazio_recebe_as_tres_secoes_com_texto_e_sem_video(sessao):
    semeadas = semear_conteudo_institucional(sessao)

    quem_somos, contatos, como_apoiar = ler_conteudo_institucional(sessao)
    assert set(semeadas) == set(SecaoInstitucional)

    assert "51.730.395/0001-19" in como_apoiar.texto
    assert "Robô Educa — Kits Robóticos Educacionais" in como_apoiar.texto
    assert "Comunidade Game é uma plataforma educacional gamificada" in quem_somos.texto
    assert TITULO_DA_NOTA in quem_somos.texto
    assert "## Licenças" in quem_somos.texto
    assert "comunidadegameorg@gmail.com" in contatos.texto

    for secao in (quem_somos, contatos, como_apoiar):
        assert secao.texto
        assert secao.video_url is None
        assert secao.autor_id is None


def test_a_apresentacao_abre_quem_somos_antes_da_nota(sessao):
    semear_conteudo_institucional(sessao)

    texto = ler_conteudo_institucional(sessao)[0].texto

    assert texto.index("plataforma educacional gamificada") < texto.index(TITULO_DA_NOTA)
    assert not texto.startswith(TITULO_DA_NOTA)


def test_a_nota_declara_construcao_atendimento_e_ausencia_de_perfilamento(sessao):
    semear_conteudo_institucional(sessao)

    nota = ler_conteudo_institucional(sessao)[0].texto.split("## Licenças")[0]

    assert "Claude" in nota
    assert "Gemini" in nota and "DeepSeek" in nota
    assert "não faz perfil da criança" in nota
    assert "bloco Licenças" in nota


def test_o_titulo_da_nota_e_a_ancora_da_etiqueta_de_ia(sessao):
    semear_conteudo_institucional(sessao)

    texto = ler_conteudo_institucional(sessao)[0].texto

    # A linha inteira, e não só a presença da frase: um título com outro texto
    # geraria outro identificador e quebraria a etiqueta das Apps 01 e 05.
    assert TITULO_DA_NOTA in texto.split("\n")


def test_licencas_declara_o_auxilio_de_ia_e_a_marca_reservada(sessao):
    semear_conteudo_institucional(sessao)

    licencas = ler_conteudo_institucional(sessao)[0].texto.split("## Licenças")[1]

    assert "AGPL" in licencas and "CC BY-SA" in licencas
    assert "não altera a licença" in licencas
    assert "marca é reservada" in licencas
    assert "troca a marca pela sua" in licencas


def test_contatos_traz_um_endereco_unico_que_nao_alcanca_crianca(sessao):
    semear_conteudo_institucional(sessao)

    contatos = ler_conteudo_institucional(sessao)[1].texto

    assert contatos.count("comunidadegameorg@gmail.com") == 1
    assert "Nenhum destes canais alcança um Guerreiro ou uma Guerreira" in contatos
    for assunto in ("Dados —", "Recibo —", "edital", "Conduta —"):
        assert assunto in contatos


def test_como_apoiar_declara_o_comprovante_e_a_ausencia_de_recibo(sessao):
    semear_conteudo_institucional(sessao)

    como_apoiar = ler_conteudo_institucional(sessao)[2].texto

    assert "anexe o comprovante no pré-cadastro" in como_apoiar
    assert "não confirma PIX automaticamente" in como_apoiar
    assert "não emite recibo" in como_apoiar
    assert "comunidadegameorg@gmail.com" in como_apoiar


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
