"""O anexo da digitalização do termo impresso de biometria — `RF-02-68`,
`RN-01-12`, `RN-02-21`."""

import pytest

from nucleo.armazenamento.disco import ArmazenamentoEmDisco
from nucleo.consentimentos.modelo import AnexoDoTermo, OrigemDoConsentimento, TipoDeConsentimento
from nucleo.consentimentos.regra import anexar_digitalizacao_do_termo
from nucleo.erros import DigitalizacaoDoTermoJaAnexada, ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel


def _cabecalhos(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


@pytest.fixture
def cenario_de_biometria(criar_persona, criar_vinculo, conceder_consentimento_biometrico):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    consentimento = conceder_consentimento_biometrico(
        responsavel, guerreiro, operado_por=admin, origem=OrigemDoConsentimento.impressa
    )
    return admin, consentimento


@pytest.mark.parametrize(
    ("nome", "tipo_mime"),
    [
        ("termo.pdf", "application/pdf"),
        ("termo.jpg", "image/jpeg"),
        ("termo.png", "image/png"),
    ],
)
def test_anexo_aceito_nos_tres_formatos(sessao, cenario_de_biometria, tmp_path, nome, tipo_mime):
    admin, consentimento = cenario_de_biometria
    armazenamento = ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))

    anexo = anexar_digitalizacao_do_termo(
        sessao,
        operador=admin,
        consentimento=consentimento,
        conteudo=b"conteudo",
        nome_original=nome,
        tipo_mime=tipo_mime,
        armazenamento=armazenamento,
    )
    sessao.commit()

    assert anexo.consentimento_id == consentimento.id
    assert anexo.digitalizacao_tipo == tipo_mime


def test_formato_fora_dos_tres_e_recusado(sessao, cenario_de_biometria, tmp_path):
    admin, consentimento = cenario_de_biometria
    armazenamento = ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))

    with pytest.raises(ErroDeValidacao) as excinfo:
        anexar_digitalizacao_do_termo(
            sessao,
            operador=admin,
            consentimento=consentimento,
            conteudo=b"conteudo",
            nome_original="termo.docx",
            tipo_mime="application/msword",
            armazenamento=armazenamento,
        )
    assert excinfo.value.campo == "digitalizacao"
    assert sessao.query(AnexoDoTermo).count() == 0


def test_consentimento_de_divulgacao_nao_recebe_anexo(
    sessao, criar_persona, criar_vinculo, criar_consentimento, tmp_path
):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    consentimento = criar_consentimento(
        responsavel,
        guerreiro,
        tipo=TipoDeConsentimento.autorizacao_de_divulgacao,
        operado_por=admin,
    )
    armazenamento = ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))

    with pytest.raises(ErroDeValidacao) as excinfo:
        anexar_digitalizacao_do_termo(
            sessao,
            operador=admin,
            consentimento=consentimento,
            conteudo=b"conteudo",
            nome_original="termo.pdf",
            tipo_mime="application/pdf",
            armazenamento=armazenamento,
        )
    assert excinfo.value.campo == "consentimento_id"
    assert sessao.query(AnexoDoTermo).count() == 0


def test_segunda_digitalizacao_e_recusada(sessao, cenario_de_biometria, tmp_path):
    admin, consentimento = cenario_de_biometria
    armazenamento = ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))
    anexar_digitalizacao_do_termo(
        sessao,
        operador=admin,
        consentimento=consentimento,
        conteudo=b"primeiro",
        nome_original="termo.pdf",
        tipo_mime="application/pdf",
        armazenamento=armazenamento,
    )
    sessao.commit()

    with pytest.raises(DigitalizacaoDoTermoJaAnexada):
        anexar_digitalizacao_do_termo(
            sessao,
            operador=admin,
            consentimento=consentimento,
            conteudo=b"segundo",
            nome_original="termo-2.pdf",
            tipo_mime="application/pdf",
            armazenamento=armazenamento,
        )
    assert sessao.query(AnexoDoTermo).filter_by(consentimento_id=consentimento.id).count() == 1


def test_mestre_nao_anexa(sessao, criar_persona, cenario_de_biometria, tmp_path):
    _, consentimento = cenario_de_biometria
    mestre = criar_persona(Papel.mestre)
    armazenamento = ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))

    with pytest.raises(PermissaoNegada):
        anexar_digitalizacao_do_termo(
            sessao,
            operador=mestre,
            consentimento=consentimento,
            conteudo=b"conteudo",
            nome_original="termo.pdf",
            tipo_mime="application/pdf",
            armazenamento=armazenamento,
        )
    assert sessao.query(AnexoDoTermo).count() == 0


def test_consentimento_segue_inalterado_depois_do_anexo(sessao, cenario_de_biometria, tmp_path):
    admin, consentimento = cenario_de_biometria
    versao_antes = consentimento.versao_do_termo
    decisao_antes = consentimento.decisao
    armazenamento = ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))

    anexar_digitalizacao_do_termo(
        sessao,
        operador=admin,
        consentimento=consentimento,
        conteudo=b"conteudo",
        nome_original="termo.pdf",
        tipo_mime="application/pdf",
        armazenamento=armazenamento,
    )
    sessao.commit()

    sessao.refresh(consentimento)
    assert consentimento.versao_do_termo == versao_antes
    assert consentimento.decisao == decisao_antes


def test_anexo_pela_rota(
    cliente,
    criar_chave,
    criar_sessao_de_teste,
    criar_persona,
    criar_vinculo,
    conceder_consentimento_biometrico,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    consentimento = conceder_consentimento_biometrico(
        responsavel, guerreiro, operado_por=admin, origem=OrigemDoConsentimento.impressa
    )
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/consentimentos/{consentimento.id}/anexo",
        files={"digitalizacao": ("termo.pdf", b"conteudo", "application/pdf")},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    assert resposta.json()["consentimento_id"] == str(consentimento.id)


def test_mestre_recebe_403_pela_rota(
    cliente,
    criar_chave,
    criar_sessao_de_teste,
    criar_persona,
    criar_vinculo,
    conceder_consentimento_biometrico,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    consentimento = conceder_consentimento_biometrico(
        responsavel, guerreiro, operado_por=admin, origem=OrigemDoConsentimento.impressa
    )
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/consentimentos/{consentimento.id}/anexo",
        files={"digitalizacao": ("termo.pdf", b"conteudo", "application/pdf")},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 403


def test_rota_de_anexo_esta_no_openapi_sob_v1(cliente):
    schema = cliente.get("/openapi.json").json()

    assert "/v1/consentimentos/{id_do_consentimento}/anexo" in schema["paths"]
    assert "post" in schema["paths"]["/v1/consentimentos/{id_do_consentimento}/anexo"]
