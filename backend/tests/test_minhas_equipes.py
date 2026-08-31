"""A porta HTTP das equipes de que a persona em sessão participa —
`RF-05-22`, `RF-05-23`, `RF-05-24`, `RN-05-12`, `RN-05-15`, `RN-05-21`, do
PRD-05 §9."""

from nucleo.equipes.modelo import Equipe, IntegranteDaEquipe
from nucleo.equipes.regra import declarar_escolha_da_equipe, entrar_na_equipe
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import FormatoDeAtividade, SituacaoDaTrilha


def _cabecalhos(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def test_a_leitura_reune_equipe_da_aula_e_equipe_da_trilha_com_papel(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_equipe,
    criar_nick,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)

    criador_da_aula = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(criador_da_aula, "criador-aula")
    equipe_da_aula = criar_equipe(criador_da_aula, aula=aula)

    criador_da_trilha = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(criador_da_trilha, "criador-trilha")
    equipe_da_trilha = criar_equipe(criador_da_trilha, trilha=trilha)

    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(guerreiro, "zeferina")
    entrar_na_equipe(sessao, operador=guerreiro, equipe=equipe_da_aula, papel="apoio")
    entrar_na_equipe(sessao, operador=guerreiro, equipe=equipe_da_trilha, papel="capitã")
    sessao.commit()
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/equipes", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 2

    da_aula = next(item for item in corpo if item["aula_id"] == str(aula.id))
    assert da_aula["trilha_id"] is None
    assert da_aula["meu_papel"] == "apoio"

    da_trilha = next(item for item in corpo if item["trilha_id"] == str(trilha.id))
    assert da_trilha["aula_id"] is None
    assert da_trilha["meu_papel"] == "capitã"


def test_equipe_da_aula_traz_as_atividades_com_a_corrente_marcada(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_nick,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre, formato=FormatoDeAtividade.presencial, aula=aula)

    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(guerreiro, "zeferina")
    equipe = criar_equipe(guerreiro, aula=aula)
    declarar_escolha_da_equipe(sessao, operador=guerreiro, equipe=equipe, atividade=atividade)
    sessao.commit()
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/equipes", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    atividades = corpo[0]["atividades"]
    assert len(atividades) == 1
    assert atividades[0]["atividade"]["id"] == str(atividade.id)
    assert atividades[0]["corrente"] is True


def test_integrante_aparece_so_por_avatar_e_nick(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_nick,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade, avatar="avatar-1")
    criar_nick(guerreiro, "zeferina")
    equipe = criar_equipe(guerreiro, aula=aula)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/equipes", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    corpo = resposta.json()
    integrantes = corpo[0]["integrantes"]
    assert integrantes == [{"avatar": "avatar-1", "nick": "zeferina", "papel": None}]
    assert equipe.id is not None


def test_equipe_que_nao_integra_nao_e_devolvida(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_nick,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    outro_guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(outro_guerreiro, "outra")
    criar_equipe(outro_guerreiro, aula=aula)

    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(guerreiro, "zeferina")
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/equipes", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_persona_sem_equipe_recebe_conjunto_vazio(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/equipes", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_a_leitura_nao_altera_composicao(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_nick,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(guerreiro, "zeferina")
    criar_equipe(guerreiro, aula=aula)
    token, _ = criar_sessao_de_teste(guerreiro)

    total_de_equipes_antes = sessao.query(Equipe).count()
    total_de_integrantes_antes = sessao.query(IntegranteDaEquipe).count()

    resposta = cliente.get("/v1/eu/equipes", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert sessao.query(Equipe).count() == total_de_equipes_antes
    assert sessao.query(IntegranteDaEquipe).count() == total_de_integrantes_antes
