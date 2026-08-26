from datetime import UTC, datetime

from nucleo.consentimentos.modelo import DecisaoDeConsentimento, TipoDeConsentimento
from nucleo.consentimentos.regra import autorizacao_de_divulgacao_vigente
from nucleo.personas.modelo import Papel

TIPO = TipoDeConsentimento.autorizacao_de_divulgacao


def test_concessao_unica_torna_a_autorizacao_vigente(
    sessao, criar_persona, criar_vinculo, criar_consentimento
):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)

    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.concede)

    assert autorizacao_de_divulgacao_vigente(sessao, guerreiro.id) is True


def test_decisao_mais_recente_do_responsavel_e_a_que_vale(
    sessao, criar_persona, criar_vinculo, criar_consentimento
):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)

    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.concede)
    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.nega)
    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.concede)

    assert autorizacao_de_divulgacao_vigente(sessao, guerreiro.id) is True


def test_recusa_de_um_responsavel_derruba_a_autorizacao(
    sessao, criar_persona, criar_vinculo, criar_consentimento
):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    responsavel_a = criar_persona(Papel.responsavel, criada_por=admin)
    responsavel_b = criar_persona(Papel.responsavel, criada_por=admin)
    criar_vinculo(responsavel_a, guerreiro, cadastrado_por=admin)
    criar_vinculo(responsavel_b, guerreiro, cadastrado_por=admin)

    criar_consentimento(responsavel_a, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.concede)
    criar_consentimento(responsavel_b, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.nega)

    assert autorizacao_de_divulgacao_vigente(sessao, guerreiro.id) is False


def test_sem_decisao_nenhuma_nao_ha_autorizacao(sessao, criar_persona, criar_vinculo):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)

    assert autorizacao_de_divulgacao_vigente(sessao, guerreiro.id) is False


def test_vigencia_responde_por_data_anterior(
    sessao, criar_persona, criar_vinculo, criar_consentimento
):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)

    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.concede)
    sessao.commit()
    momento_intermediario = datetime.now(UTC)

    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.nega)

    assert autorizacao_de_divulgacao_vigente(sessao, guerreiro.id, em=momento_intermediario) is True
    assert autorizacao_de_divulgacao_vigente(sessao, guerreiro.id) is False


def _autenticar(cliente, criar_chave, criar_sessao_de_teste, persona):
    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(persona)
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def test_eu_declara_divulgacao_vigente_para_o_guerreiro(
    cliente, criar_chave, criar_sessao_de_teste, criar_persona, criar_vinculo, criar_consentimento
):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.concede)

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, guerreiro)
    resposta = cliente.get("/v1/eu", headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.json()["divulgacao_autorizada"] is True


def test_eu_sem_decisao_declara_nao_vigente(
    cliente, criar_chave, criar_sessao_de_teste, criar_persona
):
    guerreiro = criar_persona(Papel.guerreiro)

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, guerreiro)
    resposta = cliente.get("/v1/eu", headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.json()["divulgacao_autorizada"] is False


def test_eu_declara_revogacao_de_um_responsavel(
    cliente, criar_chave, criar_sessao_de_teste, criar_persona, criar_vinculo, criar_consentimento
):
    admin = criar_persona(Papel.admin)
    responsavel_a = criar_persona(Papel.responsavel, criada_por=admin)
    responsavel_b = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel_a, guerreiro, cadastrado_por=admin)
    criar_vinculo(responsavel_b, guerreiro, cadastrado_por=admin)
    criar_consentimento(responsavel_a, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.concede)
    criar_consentimento(responsavel_b, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.nega)

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, guerreiro)
    resposta = cliente.get("/v1/eu", headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.json()["divulgacao_autorizada"] is False


def test_eu_nao_revela_quem_decidiu(
    cliente, criar_chave, criar_sessao_de_teste, criar_persona, criar_vinculo, criar_consentimento
):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.concede)

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, guerreiro)
    corpo = cliente.get("/v1/eu", headers=cabecalhos).json()

    assert "responsavel_id" not in corpo
    assert "decidido_em" not in corpo
    assert "motivo" not in corpo


def test_eu_de_outro_papel_nao_declara_divulgacao(
    cliente, criar_chave, criar_sessao_de_teste, criar_persona
):
    mestre = criar_persona(Papel.mestre)

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, mestre)
    resposta = cliente.get("/v1/eu", headers=cabecalhos)

    assert resposta.status_code == 200
    assert "divulgacao_autorizada" not in resposta.json()
