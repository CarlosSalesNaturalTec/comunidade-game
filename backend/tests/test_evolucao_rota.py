from datetime import UTC, datetime

from nucleo.criacoes_originais.modelo import SituacaoDaCriacaoOriginal
from nucleo.personas.modelo import Papel
from nucleo.resultados.modelo import DesfechoDoResultado
from nucleo.resultados.regra import registrar_resultado
from nucleo.trilhas.modelo import SituacaoDaTrilha
from tests.conftest import criar_aula_para_resultado

MOMENTO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def _montar_vinculo(sessao, criar_persona, criar_vinculo, grau="mãe"):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, grau_de_parentesco=grau, cadastrado_por=admin)
    return admin, responsavel, guerreiro


def test_responsavel_com_dois_vinculados_ve_os_dois_com_parentesco(
    cliente, criar_chave, criar_persona, criar_vinculo, criar_nick, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro1 = criar_persona(Papel.guerreiro)
    guerreiro2 = criar_persona(Papel.guerreiro)
    criar_nick(guerreiro1, "guerreiro-um")
    criar_nick(guerreiro2, "guerreiro-dois")
    criar_vinculo(responsavel, guerreiro1, grau_de_parentesco="mãe", cadastrado_por=admin)
    criar_vinculo(responsavel, guerreiro2, grau_de_parentesco="avó", cadastrado_por=admin)
    outro_guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        "/v1/eu/guerreiros",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 2
    ids = {item["id"] for item in corpo}
    assert ids == {str(guerreiro1.id), str(guerreiro2.id)}
    assert str(outro_guerreiro.id) not in ids
    parentescos = {item["id"]: item["grau_de_parentesco"] for item in corpo}
    assert parentescos[str(guerreiro1.id)] == "mãe"
    assert parentescos[str(guerreiro2.id)] == "avó"


def test_papel_que_nao_e_responsavel_recebe_403(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/eu/guerreiros",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_evolucao_e_ocorrencias_de_crianca_sem_vinculo_recebem_403(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro_nao_vinculado = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(responsavel)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    resposta_evolucao = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro_nao_vinculado.id}/evolucao", headers=cabecalhos
    )
    resposta_ocorrencias = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro_nao_vinculado.id}/ocorrencias", headers=cabecalhos
    )

    assert resposta_evolucao.status_code == 403
    assert resposta_evolucao.json().get("guerreiro_id") is None
    assert resposta_ocorrencias.status_code == 403


def test_evolucao_traz_o_consolidado_do_vinculado(
    cliente,
    criar_chave,
    criar_persona,
    criar_vinculo,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    sessao,
):
    chave, _ = criar_chave()
    admin, responsavel, guerreiro = _montar_vinculo(sessao, criar_persona, criar_vinculo)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada, nome="Trilha do Painel")
    criar_inscricao_na_trilha(guerreiro, trilha)
    missao = criar_missao(trilha, mestre, titulo="Missão do Painel")
    atividade = criar_atividade(missao, mestre, titulo="Atividade do Painel")
    aula = criar_aula_para_resultado(sessao, mestre)
    registrar_resultado(
        sessao,
        operador=mestre,
        aula=aula,
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=MOMENTO,
        producao="Produção.",
        desfecho=DesfechoDoResultado.realizada,
    )
    sessao.commit()
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/evolucao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["atividades"]) == 1
    assert corpo["atividades"][0]["atividade_titulo"] == "Atividade do Painel"
    assert len(corpo["trilhas"]) == 1
    assert corpo["trilhas"][0]["trilha_nome"] == "Trilha do Painel"


def test_resposta_nao_traz_consulta_ao_assistente_transcricao_nem_dado_de_outra_crianca(
    cliente,
    criar_chave,
    criar_persona,
    criar_vinculo,
    criar_sessao_de_teste,
    criar_trilha,
    criar_criacao_original,
    criar_equipe,
    adicionar_integrante,
    sessao,
):
    """`RF-13-11`, `RF-13-12`, `RN-13-20`: a resposta inteira, em texto, não
    contém a chave de consulta ao assistente, transcrição de apoio escolar
    nem o `id` de um terceiro integrante da equipe."""
    chave, _ = criar_chave()
    admin, responsavel, guerreiro = _montar_vinculo(sessao, criar_persona, criar_vinculo)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    outro_guerreiro = criar_persona(Papel.guerreiro)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    adicionar_integrante(equipe, outro_guerreiro)
    criar_criacao_original(
        trilha, guerreiro, equipe=equipe, situacao=SituacaoDaCriacaoOriginal.validada
    )
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/evolucao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo_em_texto = resposta.text
    assert "assistente" not in corpo_em_texto.lower()
    assert "apoio_escolar" not in corpo_em_texto.lower()
    assert str(outro_guerreiro.id) not in corpo_em_texto
