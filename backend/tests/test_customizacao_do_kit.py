"""Customização do kit recebido (`RF-01-84` a `RF-01-86`, `RF-04-80` a
`RF-04-83`, `RF-05-102`, `RF-05-103`, `RN-01-66`)."""

import pytest
from sqlalchemy.exc import IntegrityError

from nucleo.cuidado_do_bem.modelo import (
    FonteDaPontuacaoDoBem,
    PontuacaoDoBem,
    RegistroDeCustomizacao,
    SituacaoDoRegistroDeCustomizacao,
)
from nucleo.personas.modelo import Papel
from nucleo.ponto_extra.modelo import PontoExtra
from nucleo.pontuacao.modelo import PontoRegular


def _registrar(cliente, cenario, descricao="Pintei o robô de azul e pus asas de EVA."):
    return cliente.post(
        "/v1/eu/customizacoes",
        json={
            "entrega_de_recompensa_id": str(cenario.entrega_do_kit.id),
            "descricao": descricao,
        },
        headers=cenario.do_guerreiro,
    )


def _enviar(cliente, cabecalhos, registro_id, conteudo=b"PNG-de-teste", tipo="image/png"):
    sessao_de_envio = cliente.post(
        f"/v1/customizacoes/{registro_id}/envios",
        json={"tipo_mime": tipo, "tamanho_declarado": len(conteudo)},
        headers=cabecalhos,
    )
    assert sessao_de_envio.status_code == 201, sessao_de_envio.text
    cliente.put(
        sessao_de_envio.json()["endereco_da_sessao"],
        content=conteudo,
        headers={**cabecalhos, "Content-Range": f"bytes 0-{len(conteudo) - 1}/{len(conteudo)}"},
    )
    return cliente.post(f"/v1/customizacoes/{registro_id}/envios/confirmacao", headers=cabecalhos)


def _registrar_com_midia(cliente, cenario):
    registro = _registrar(cliente, cenario)
    assert registro.status_code == 201, registro.text
    confirmado = _enviar(cliente, cenario.do_guerreiro, registro.json()["id"])
    assert confirmado.status_code == 200, confirmado.text
    return confirmado.json()


def _julgar(cliente, cenario, registro_id, aprovado=True, motivo=None, aula=None):
    return cliente.post(
        f"/v1/customizacoes/{registro_id}/julgamento",
        json={"aula_id": str((aula or cenario.aula).id), "aprovado": aprovado, "motivo": motivo},
        headers=cenario.do_mestre,
    )


def _extras(sessao, guerreiro):
    sessao.expire_all()
    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).first()
    return (conta.acumulado, conta.saldo_disponivel) if conta else (0, 0)


# ---------------------------------------------------------------------------
# Abertura
# ---------------------------------------------------------------------------


def test_kit_recebido_e_pratico_aprovado_abrem_a_customizacao(cliente, cenario):
    resposta = _registrar(cliente, cenario)

    assert resposta.status_code == 201, resposta.text
    assert resposta.json()["situacao"] == "pendente"
    assert resposta.json()["tem_midia"] is False


def test_pratico_aguardando_julgamento_mantem_fechada(cliente, sessao, cenario):
    cenario.desbloqueio.cumpriu = None
    sessao.commit()

    resposta = _registrar(cliente, cenario)

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "entrega_de_recompensa_id"


def test_kit_que_nenhum_pratico_declara_nao_abre(cliente, cenario):
    resposta = cliente.post(
        "/v1/eu/customizacoes",
        json={
            "entrega_de_recompensa_id": str(cenario.entrega_do_livro.id),
            "descricao": "Encapei o livro.",
        },
        headers=cenario.do_guerreiro,
    )

    assert resposta.status_code == 422


def test_recompensa_que_ele_nao_recebeu_nao_abre(cliente, sessao, cenario, criar_persona):
    outro = criar_persona(Papel.guerreiro, comunidade=cenario.comunidade)

    resposta = cliente.post(
        "/v1/eu/customizacoes",
        json={
            "entrega_de_recompensa_id": str(cenario.entrega_do_kit.id),
            "descricao": "Não é meu.",
        },
        headers=cenario.cabecalhos(outro),
    )

    assert resposta.status_code == 422
    assert sessao.query(RegistroDeCustomizacao).count() == 0


# ---------------------------------------------------------------------------
# Registro, mídia e captura
# ---------------------------------------------------------------------------


def test_registro_em_casa_com_foto_fica_pronto_para_julgar(cliente, cenario):
    registro = _registrar_com_midia(cliente, cenario)

    assert registro["tem_midia"] is True
    assert registro["tipo_do_arquivo"] == "image/png"


@pytest.mark.parametrize("descricao", [None, "   "])
def test_descricao_em_branco_e_recusada(cliente, sessao, cenario, descricao):
    resposta = _registrar(cliente, cenario, descricao=descricao)

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "descricao"
    assert sessao.query(RegistroDeCustomizacao).count() == 0


def test_formato_que_nao_e_foto_nem_video_e_recusado(cliente, cenario):
    registro = _registrar(cliente, cenario).json()

    resposta = cliente.post(
        f"/v1/customizacoes/{registro['id']}/envios",
        json={"tipo_mime": "audio/mpeg", "tamanho_declarado": 10},
        headers=cenario.do_guerreiro,
    )

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "tipo_mime"


def test_o_mestre_da_aula_captura_na_hora(cliente, sessao, cenario):
    resposta = cliente.post(
        f"/v1/aulas/{cenario.aula.id}/customizacoes",
        json={
            "guerreiro_id": str(cenario.guerreiro.id),
            "entrega_de_recompensa_id": str(cenario.entrega_do_kit.id),
            "descricao": "Ele colou olhos novos.",
        },
        headers=cenario.do_mestre,
    )
    assert resposta.status_code == 201, resposta.text
    confirmado = _enviar(cliente, cenario.do_mestre, resposta.json()["id"])

    assert confirmado.status_code == 200, confirmado.text
    registro = sessao.get(RegistroDeCustomizacao, resposta.json()["id"])
    assert registro.guerreiro_id == cenario.guerreiro.id
    assert registro.autor_id == cenario.mestre.id


def test_captura_de_quem_nao_esta_na_aula_e_recusada(
    cliente, cenario, criar_aula, criar_ponto_de_apoio
):
    outra_aula = criar_aula(cenario.mestre, cenario.comunidade, ponto_de_apoio=cenario.ponto)

    resposta = cliente.post(
        f"/v1/aulas/{outra_aula.id}/customizacoes",
        json={
            "guerreiro_id": str(cenario.guerreiro.id),
            "entrega_de_recompensa_id": str(cenario.entrega_do_kit.id),
            "descricao": "Olhos novos.",
        },
        headers=cenario.do_mestre,
    )

    assert resposta.status_code == 422


def test_outro_guerreiro_nao_registra_por_ele(cliente, cenario, criar_persona):
    outro = criar_persona(Papel.guerreiro, comunidade=cenario.comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{cenario.aula.id}/customizacoes",
        json={
            "guerreiro_id": str(cenario.guerreiro.id),
            "entrega_de_recompensa_id": str(cenario.entrega_do_kit.id),
            "descricao": "Por ele.",
        },
        headers=cenario.cabecalhos(outro),
    )

    assert resposta.status_code == 403


def test_segundo_pendente_do_mesmo_kit_e_recusado(cliente, cenario):
    assert _registrar(cliente, cenario).status_code == 201

    resposta = _registrar(cliente, cenario, descricao="Outra pintura.")

    assert resposta.status_code == 422


def test_o_banco_recusa_dois_pendentes_do_mesmo_kit(sessao, cenario):
    for _ in range(2):
        sessao.add(
            RegistroDeCustomizacao(
                entrega_de_recompensa_id=cenario.entrega_do_kit.id,
                guerreiro_id=cenario.guerreiro.id,
                descricao="Por fora da regra.",
                autor_id=cenario.guerreiro.id,
                papel_do_autor="guerreiro",
            )
        )
    with pytest.raises(IntegrityError):
        sessao.commit()
    sessao.rollback()


def test_a_midia_e_servida_ao_dono_e_ao_mestre_e_nao_a_outro(cliente, cenario, criar_persona):
    registro = _registrar_com_midia(cliente, cenario)
    outro = criar_persona(Papel.guerreiro, comunidade=cenario.comunidade)
    rota = f"/v1/customizacoes/{registro['id']}/arquivo"

    do_dono = cliente.get(rota, headers=cenario.do_guerreiro)
    do_mestre = cliente.get(rota, headers=cenario.do_mestre)
    de_outro = cliente.get(rota, headers=cenario.cabecalhos(outro))

    assert do_dono.status_code == 200
    assert do_dono.content == b"PNG-de-teste"
    assert do_mestre.status_code == 200
    assert de_outro.status_code == 403


# ---------------------------------------------------------------------------
# Leitura própria e cancelamento
# ---------------------------------------------------------------------------


def test_o_guerreiro_le_os_kits_abertos_e_os_registros(cliente, cenario):
    _registrar(cliente, cenario)

    corpo = cliente.get("/v1/eu/customizacoes", headers=cenario.do_guerreiro).json()

    assert [kit["entrega_de_recompensa_id"] for kit in corpo["kits_abertos"]] == [
        str(cenario.entrega_do_kit.id)
    ]
    ultimo = corpo["kits_abertos"][0]["ultimo_aprovado"]
    assert ultimo["fonte"] == "comprovacao_do_pratico"
    assert ultimo["id"] == str(cenario.desbloqueio.id)
    assert corpo["registros"][0]["situacao"] == "pendente"


def test_o_guerreiro_cancela_o_pendente_e_registra_de_novo(cliente, cenario):
    registro = _registrar(cliente, cenario).json()

    cancelado = cliente.post(
        f"/v1/customizacoes/{registro['id']}/cancelamento", headers=cenario.do_guerreiro
    )

    assert cancelado.json()["situacao"] == "cancelado"
    assert _registrar(cliente, cenario, descricao="Agora com rodas.").status_code == 201


def test_registro_julgado_nao_se_cancela(cliente, cenario):
    registro = _registrar_com_midia(cliente, cenario)
    _julgar(cliente, cenario, registro["id"])

    resposta = cliente.post(
        f"/v1/customizacoes/{registro['id']}/cancelamento", headers=cenario.do_guerreiro
    )

    assert resposta.status_code == 422


# ---------------------------------------------------------------------------
# Julgamento
# ---------------------------------------------------------------------------


def test_aprovado_credita_1_extra_e_vira_ultimo_aprovado(cliente, sessao, cenario):
    registro = _registrar_com_midia(cliente, cenario)

    julgado = _julgar(cliente, cenario, registro["id"])

    assert julgado.status_code == 200, julgado.text
    assert julgado.json()["situacao"] == "aprovado"
    assert _extras(sessao, cenario.guerreiro) == (1, 1)
    assert sessao.query(PontoRegular).filter_by(guerreiro_id=cenario.guerreiro.id).count() == 0
    corpo = cliente.get("/v1/eu/customizacoes", headers=cenario.do_guerreiro).json()
    assert corpo["kits_abertos"][0]["ultimo_aprovado"]["id"] == registro["id"]


def test_reprovado_sem_motivo_e_recusado_e_com_motivo_permite_reenviar(cliente, sessao, cenario):
    registro = _registrar_com_midia(cliente, cenario)

    sem_motivo = _julgar(cliente, cenario, registro["id"], aprovado=False)
    com_motivo = _julgar(
        cliente, cenario, registro["id"], aprovado=False, motivo="Apareceu o seu rosto."
    )

    assert sem_motivo.status_code == 422
    assert sem_motivo.json()["campo"] == "motivo"
    assert com_motivo.json()["situacao"] == "reprovado"
    assert com_motivo.json()["motivo_do_julgamento"] == "Apareceu o seu rosto."
    assert _extras(sessao, cenario.guerreiro) == (0, 0)
    assert _registrar(cliente, cenario, descricao="Foto só do kit.").status_code == 201


def test_registro_sem_midia_nao_e_julgado(cliente, cenario):
    registro = _registrar(cliente, cenario).json()

    assert _julgar(cliente, cenario, registro["id"]).status_code == 422


def test_guerreiro_sem_presenca_na_aula_nao_e_julgado(cliente, cenario, criar_aula):
    registro = _registrar_com_midia(cliente, cenario)
    outra_aula = criar_aula(cenario.mestre, cenario.comunidade, ponto_de_apoio=cenario.ponto)

    resposta = _julgar(cliente, cenario, registro["id"], aula=outra_aula)

    assert resposta.status_code == 422


def test_mestre_de_outra_comunidade_nao_julga(
    cliente, cenario, criar_persona, criar_comunidade, criar_vinculo_do_mestre
):
    registro = _registrar_com_midia(cliente, cenario)
    alheio = criar_persona(Papel.mestre)
    criar_vinculo_do_mestre(alheio, criar_comunidade("Outra"))

    resposta = cliente.post(
        f"/v1/customizacoes/{registro['id']}/julgamento",
        json={"aula_id": str(cenario.aula.id), "aprovado": True},
        headers=cenario.cabecalhos(alheio),
    )

    assert resposta.status_code == 403


def test_registro_julgado_nao_se_julga_de_novo(cliente, sessao, cenario):
    registro = _registrar_com_midia(cliente, cenario)
    _julgar(cliente, cenario, registro["id"])

    resposta = _julgar(cliente, cenario, registro["id"])

    assert resposta.status_code == 422
    assert _extras(sessao, cenario.guerreiro) == (1, 1)


def test_aprovacao_grava_a_pontuacao_do_bem_pela_customizacao(cliente, sessao, cenario):
    registro = _registrar_com_midia(cliente, cenario)
    _julgar(cliente, cenario, registro["id"])

    pontuacao = sessao.query(PontuacaoDoBem).one()

    assert pontuacao.fonte == FonteDaPontuacaoDoBem.customizacao
    assert pontuacao.aula_id == cenario.aula.id
    assert str(pontuacao.registro_de_customizacao_id) == registro["id"]
    assert sessao.get(RegistroDeCustomizacao, registro["id"]).situacao == (
        SituacaoDoRegistroDeCustomizacao.aprovado
    )


# ---------------------------------------------------------------------------
# O "antes" do kit, pela rota do bem (`RF-04-81`, decisão de 2026-11-13)
# ---------------------------------------------------------------------------


def _rota_do_antes(entrega):
    return f"/v1/entregas-de-recompensa/{entrega.id}/ultimo-aprovado/arquivo"


def _gravar_comprovacao(configuracao, cenario, corpo=b"PNG-do-pratico"):
    from nucleo.armazenamento.fabrica import obter_porta_de_armazenamento

    obter_porta_de_armazenamento(configuracao).gravar(
        referencia=cenario.desbloqueio.comprovacao_referencia, conteudo=corpo
    )


def _mestre_nao_autor(cenario, criar_persona, criar_vinculo_do_mestre):
    outro = criar_persona(Papel.mestre)
    criar_vinculo_do_mestre(outro, cenario.comunidade)
    return cenario.cabecalhos(outro)


def test_mestre_nao_autor_ve_a_comprovacao_do_pratico_como_antes(
    cliente, configuracao, cenario, criar_persona, criar_vinculo_do_mestre
):
    _gravar_comprovacao(configuracao, cenario)
    do_mestre_da_aula = _mestre_nao_autor(cenario, criar_persona, criar_vinculo_do_mestre)

    resposta = cliente.get(_rota_do_antes(cenario.entrega_do_kit), headers=do_mestre_da_aula)

    assert resposta.status_code == 200, resposta.text
    assert resposta.content == b"PNG-do-pratico"
    assert resposta.headers["content-type"].startswith("image/png")


def test_depois_da_primeira_aprovacao_o_antes_e_a_customizacao(
    cliente, configuracao, cenario, criar_persona, criar_vinculo_do_mestre
):
    _gravar_comprovacao(configuracao, cenario)
    registro = _registrar_com_midia(cliente, cenario)
    assert _julgar(cliente, cenario, registro["id"]).status_code == 200

    resposta = cliente.get(
        _rota_do_antes(cenario.entrega_do_kit),
        headers=_mestre_nao_autor(cenario, criar_persona, criar_vinculo_do_mestre),
    )

    assert resposta.status_code == 200, resposta.text
    assert resposta.content == b"PNG-de-teste"


def test_o_antes_nao_e_servido_a_mestre_de_outra_comunidade_nem_a_outro_guerreiro(
    cliente, configuracao, cenario, criar_persona, criar_comunidade, criar_vinculo_do_mestre
):
    _gravar_comprovacao(configuracao, cenario)
    alheio = criar_persona(Papel.mestre)
    criar_vinculo_do_mestre(alheio, criar_comunidade())
    outro_guerreiro = criar_persona(Papel.guerreiro, comunidade=cenario.comunidade)
    rota = _rota_do_antes(cenario.entrega_do_kit)

    assert cliente.get(rota, headers=cenario.cabecalhos(alheio)).status_code == 403
    assert cliente.get(rota, headers=cenario.cabecalhos(outro_guerreiro)).status_code == 403
    assert cliente.get(rota, headers=cenario.do_guerreiro).status_code == 200


def test_bem_sem_customizacao_aberta_nao_tem_antes(cliente, cenario):
    resposta = cliente.get(_rota_do_antes(cenario.entrega_do_livro), headers=cenario.do_mestre)

    assert resposta.status_code == 404


def test_a_rota_da_comprovacao_segue_so_do_autor(
    cliente, configuracao, cenario, criar_persona, criar_vinculo_do_mestre
):
    _gravar_comprovacao(configuracao, cenario)
    rota = f"/v1/missoes/{cenario.montagem.id}/desbloqueios/{cenario.guerreiro.id}/comprovacao"

    resposta = cliente.get(
        rota, headers=_mestre_nao_autor(cenario, criar_persona, criar_vinculo_do_mestre)
    )

    assert resposta.status_code == 403
