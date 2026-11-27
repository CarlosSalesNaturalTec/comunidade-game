"""Lançamento com comprovante e julgamento do prático (fatia 41 do PRD-09):
`RF-09-148` a `RF-09-151`, `RN-09-64` a `RN-09-66`."""

import uuid
from datetime import UTC, datetime

import pytest

from nucleo.armazenamento.disco import ArmazenamentoEmDisco
from nucleo.criacoes_originais.modelo import TipoDeProducaoDaCriacaoOriginal
from nucleo.erros import ArquivoAcimaDoTeto, ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.resultados.modelo import DesfechoDoResultado, Resultado
from nucleo.resultados.regra import (
    ComprovanteDeclarado,
    JulgamentoDeclarado,
    ResultadoDeclarado,
    abrir_envio_do_comprovante,
    lancar_atividade_realizada,
    lancar_resultados_da_atividade,
    ler_arquivo_do_comprovante,
    listar_resultados_da_aula,
    referencia_do_envio_do_comprovante,
)
from nucleo.trilhas.modelo import DesbloqueioDaMissao, TipoDeDesafioDeDesbloqueio
from nucleo.trilhas.regra import situacao_do_pratico

MOMENTO = datetime(2026, 11, 27, 10, 0, tzinfo=UTC)
FOTO = b"\xff\xd8\xff" + b"0" * 64


@pytest.fixture
def armazenamento(tmp_path):
    return ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))


@pytest.fixture
def cenario(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
):
    """Mestre autor, Guerreiro(a) inscrito e uma atividade numa missão sem
    desafio; `pratico(forma)` transforma a missão num prático."""
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)
    criar_inscricao_na_trilha(guerreiro, trilha)

    def pratico(forma=TipoDeProducaoDaCriacaoOriginal.imagem):
        missao.tipo_do_desafio_de_desbloqueio = TipoDeDesafioDeDesbloqueio.pratico
        missao.desafio_pratico_forma_de_comprovacao = forma
        missao.desafio_pratico_criterio_de_aceite = "Só a produção, sem rosto."
        sessao.commit()

    return {
        "mestre": mestre,
        "guerreiro": guerreiro,
        "trilha": trilha,
        "missao": missao,
        "atividade": atividade,
        "aula": aula,
        "pratico": pratico,
    }


def _enviar(armazenamento, persona, envio_id, conteudo=FOTO, tipo_mime="image/jpeg"):
    referencia = referencia_do_envio_do_comprovante(persona.id, envio_id)
    chave = armazenamento.chave_da_sessao(referencia)
    armazenamento.receber_parte(chave=chave, inicio=0, conteudo=conteudo)
    armazenamento.concluir_sessao(chave=chave, referencia=referencia)


def _abrir_e_enviar(sessao, armazenamento, c, tipo="imagem", tipo_mime="image/jpeg"):
    envio_id, _ = abrir_envio_do_comprovante(
        sessao,
        operador=c["mestre"],
        atividade=c["atividade"],
        tipo=tipo,
        tipo_mime=tipo_mime,
        tamanho_declarado=len(FOTO),
        armazenamento=armazenamento,
    )
    _enviar(armazenamento, c["mestre"], envio_id)
    return envio_id


def _lancar(sessao, c, *, comprovante=None, producao=None, julgamento=None, armazenamento=None):
    gravados, _ = lancar_resultados_da_atividade(
        sessao,
        operador=c["mestre"],
        aula=c["aula"],
        atividade=c["atividade"],
        resultados=[
            ResultadoDeclarado(
                guerreiro_id=c["guerreiro"].id,
                atividade=c["atividade"],
                momento_do_fato=MOMENTO,
                producao=producao,
                desfecho=DesfechoDoResultado.realizada,
                comprovante=comprovante,
                julgamento=julgamento,
            )
        ],
        armazenamento=armazenamento,
    )
    sessao.commit()
    return gravados[0]


# --- comprovante (`RF-09-149`, `RN-09-64`) ----------------------------------


def test_comprovante_em_texto_e_em_link_vao_no_corpo(sessao, cenario):
    resultado = _lancar(sessao, cenario, comprovante=ComprovanteDeclarado("texto", "Fiz o robô."))
    assert resultado.comprovante_tipo == TipoDeProducaoDaCriacaoOriginal.texto
    assert resultado.producao == "Fiz o robô."


def test_comprovante_em_link_exige_o_endereco(sessao, cenario):
    with pytest.raises(ErroDeValidacao) as erro:
        _lancar(sessao, cenario, comprovante=ComprovanteDeclarado("link_externo", " "))
    assert erro.value.campo == "comprovante"


def test_producao_em_texto_simples_vale_como_comprovante_em_texto(sessao, cenario):
    resultado = _lancar(sessao, cenario, producao="Produção antiga.")
    assert resultado.comprovante_tipo == TipoDeProducaoDaCriacaoOriginal.texto
    assert resultado.producao == "Produção antiga."


def test_sem_comprovante_e_sem_producao_e_recusado(sessao, cenario):
    with pytest.raises(ErroDeValidacao) as erro:
        _lancar(sessao, cenario)
    assert erro.value.campo == "producao"


def test_comprovante_e_producao_juntos_sao_recusados(sessao, cenario):
    with pytest.raises(ErroDeValidacao):
        _lancar(sessao, cenario, producao="x", comprovante=ComprovanteDeclarado("texto", "y"))


def test_forma_fora_das_seis_e_recusada(sessao, cenario):
    with pytest.raises(ErroDeValidacao):
        _lancar(sessao, cenario, comprovante=ComprovanteDeclarado("escultura", "x"))


def test_foto_entra_pelo_envio_previo(sessao, cenario, armazenamento):
    envio_id = _abrir_e_enviar(sessao, armazenamento, cenario)
    resultado = _lancar(
        sessao,
        cenario,
        comprovante=ComprovanteDeclarado("imagem", envio_id=envio_id),
        armazenamento=armazenamento,
    )
    assert resultado.comprovante_tipo == TipoDeProducaoDaCriacaoOriginal.imagem
    assert resultado.comprovante_tamanho == len(FOTO)
    assert resultado.comprovante_tipo_do_arquivo == "image/jpeg"
    assert resultado.producao is None


def test_envio_nao_concluido_e_recusado(sessao, cenario, armazenamento):
    envio_id, _ = abrir_envio_do_comprovante(
        sessao,
        operador=cenario["mestre"],
        atividade=cenario["atividade"],
        tipo="imagem",
        tipo_mime="image/jpeg",
        tamanho_declarado=10,
        armazenamento=armazenamento,
    )
    with pytest.raises(ErroDeValidacao) as erro:
        _lancar(
            sessao,
            cenario,
            comprovante=ComprovanteDeclarado("imagem", envio_id=envio_id),
            armazenamento=armazenamento,
        )
    assert "não terminou" in erro.value.mensagem
    assert sessao.query(Resultado).count() == 0


def test_envio_de_outra_persona_e_recusado(sessao, cenario, armazenamento, criar_persona):
    outro = criar_persona(Papel.mestre)
    envio_id = uuid.uuid4()
    armazenamento.abrir_sessao(
        referencia=referencia_do_envio_do_comprovante(outro.id, envio_id),
        tipo_mime="image/jpeg",
        tamanho_declarado=len(FOTO),
    )
    _enviar(armazenamento, outro, envio_id)
    with pytest.raises(ErroDeValidacao):
        _lancar(
            sessao,
            cenario,
            comprovante=ComprovanteDeclarado("imagem", envio_id=envio_id),
            armazenamento=armazenamento,
        )


def test_envio_reusado_e_recusado(sessao, cenario, armazenamento, criar_persona, criar_atividade):
    envio_id = _abrir_e_enviar(sessao, armazenamento, cenario)
    _lancar(
        sessao,
        cenario,
        comprovante=ComprovanteDeclarado("imagem", envio_id=envio_id),
        armazenamento=armazenamento,
    )
    cenario["atividade"] = criar_atividade(cenario["missao"], cenario["mestre"], titulo="Outra")
    with pytest.raises(ErroDeValidacao) as erro:
        _lancar(
            sessao,
            cenario,
            comprovante=ComprovanteDeclarado("imagem", envio_id=envio_id),
            armazenamento=armazenamento,
        )
    assert "já é comprovante" in erro.value.mensagem


def test_midia_escrita_no_corpo_e_recusada(sessao, cenario):
    with pytest.raises(ErroDeValidacao) as erro:
        _lancar(sessao, cenario, comprovante=ComprovanteDeclarado("video", "um vídeo"))
    assert "envio do arquivo" in erro.value.mensagem


def test_abrir_envio_confere_tipo_teto_forma_e_posse(sessao, cenario, armazenamento, criar_persona):
    comum = {
        "atividade": cenario["atividade"],
        "armazenamento": armazenamento,
    }
    with pytest.raises(ErroDeValidacao):
        abrir_envio_do_comprovante(
            sessao,
            operador=cenario["mestre"],
            tipo="imagem",
            tipo_mime="image/gif",
            tamanho_declarado=10,
            **comum,
        )
    with pytest.raises(ArquivoAcimaDoTeto):
        abrir_envio_do_comprovante(
            sessao,
            operador=cenario["mestre"],
            tipo="imagem",
            tipo_mime="image/jpeg",
            tamanho_declarado=21 * 1024 * 1024,
            **comum,
        )
    with pytest.raises(ErroDeValidacao):
        abrir_envio_do_comprovante(
            sessao,
            operador=cenario["mestre"],
            tipo="texto",
            tipo_mime="image/jpeg",
            tamanho_declarado=10,
            **comum,
        )
    with pytest.raises(PermissaoNegada):
        abrir_envio_do_comprovante(
            sessao,
            operador=criar_persona(Papel.mestre),
            tipo="imagem",
            tipo_mime="image/jpeg",
            tamanho_declarado=10,
            **comum,
        )


# --- julgamento no lançamento (`RF-09-150`, `RN-09-65`, `RN-09-66`) ----------


def test_pratico_pendente_sem_julgamento_e_recusado(sessao, cenario):
    cenario["pratico"](TipoDeProducaoDaCriacaoOriginal.texto)
    with pytest.raises(ErroDeValidacao) as erro:
        _lancar(sessao, cenario, comprovante=ComprovanteDeclarado("texto", "Fiz."))
    assert erro.value.campo == "julgamento_do_pratico"
    sessao.rollback()
    assert sessao.query(Resultado).count() == 0


def test_julgamento_sem_pratico_a_julgar_e_recusado(sessao, cenario):
    with pytest.raises(ErroDeValidacao) as erro:
        _lancar(
            sessao,
            cenario,
            comprovante=ComprovanteDeclarado("texto", "Fiz."),
            julgamento=JulgamentoDeclarado(cumpriu=True),
        )
    assert erro.value.campo == "julgamento_do_pratico"


def test_julgamento_de_pratico_ja_cumprido_e_recusado(sessao, cenario, criar_desbloqueio_da_missao):
    cenario["pratico"]()
    criar_desbloqueio_da_missao(cenario["guerreiro"], cenario["missao"], cumpriu=True)
    assert not situacao_do_pratico(
        sessao, missao=cenario["missao"], guerreiro_id=cenario["guerreiro"].id
    ).exige_julgamento
    with pytest.raises(ErroDeValidacao):
        _lancar(
            sessao,
            cenario,
            comprovante=ComprovanteDeclarado("texto", "Fiz."),
            julgamento=JulgamentoDeclarado(cumpriu=True),
        )


def test_quiz_nao_pede_julgamento(sessao, cenario):
    cenario["missao"].tipo_do_desafio_de_desbloqueio = TipoDeDesafioDeDesbloqueio.quiz
    sessao.commit()
    resultado = _lancar(sessao, cenario, comprovante=ComprovanteDeclarado("texto", "Fiz."))
    assert resultado.id is not None


def test_declaracao_pendente_e_julgada_com_a_entrega_do_guerreiro(
    sessao, cenario, armazenamento, criar_desbloqueio_da_missao
):
    cenario["pratico"](TipoDeProducaoDaCriacaoOriginal.texto)
    pendente = criar_desbloqueio_da_missao(
        cenario["guerreiro"], cenario["missao"], cumpriu=None, comprovacao="O que eu fiz."
    )
    _lancar(
        sessao,
        cenario,
        comprovante=ComprovanteDeclarado("texto", "Visto no encontro."),
        julgamento=JulgamentoDeclarado(cumpriu=True, publicavel=True),
    )
    sessao.refresh(pendente)
    assert pendente.cumpriu is True
    assert pendente.publicavel is True
    assert pendente.comprovacao == "O que eu fiz."
    assert pendente.julgado_por_id == cenario["mestre"].id


def test_entrega_presencial_pendente_cumprida_dispensa_motivo(
    sessao, cenario, criar_desbloqueio_da_missao
):
    cenario["pratico"]()
    pendente = criar_desbloqueio_da_missao(
        cenario["guerreiro"], cenario["missao"], cumpriu=None, entrega_presencial=True
    )
    _lancar(
        sessao,
        cenario,
        comprovante=ComprovanteDeclarado("texto", "Conferi."),
        julgamento=JulgamentoDeclarado(cumpriu=True),
    )
    sessao.refresh(pendente)
    assert pendente.cumpriu is True


def test_sem_declaracao_o_mestre_declara_em_nome_com_a_foto(sessao, cenario, armazenamento):
    cenario["pratico"](TipoDeProducaoDaCriacaoOriginal.imagem)
    envio_id = _abrir_e_enviar(sessao, armazenamento, cenario)
    resultado = _lancar(
        sessao,
        cenario,
        comprovante=ComprovanteDeclarado("imagem", envio_id=envio_id),
        julgamento=JulgamentoDeclarado(cumpriu=True, publicavel=True),
        armazenamento=armazenamento,
    )
    declaracao = (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=cenario["guerreiro"].id, missao_id=cenario["missao"].id)
        .one()
    )
    assert declaracao.cumpriu is True
    assert declaracao.publicavel is True
    assert declaracao.comprovacao_referencia == resultado.comprovante_referencia
    assert declaracao.comprovacao_tipo_do_arquivo == "image/jpeg"


def test_declaracao_recusada_e_reaberta_pelo_lancamento(
    sessao, cenario, criar_desbloqueio_da_missao
):
    cenario["pratico"](TipoDeProducaoDaCriacaoOriginal.texto)
    recusada = criar_desbloqueio_da_missao(
        cenario["guerreiro"],
        cenario["missao"],
        cumpriu=False,
        julgado_por=cenario["mestre"],
        julgado_em=MOMENTO,
        comprovacao="Primeira.",
    )
    _lancar(
        sessao,
        cenario,
        comprovante=ComprovanteDeclarado("texto", "Agora sim."),
        julgamento=JulgamentoDeclarado(cumpriu=True, publicavel=True),
    )
    sessao.refresh(recusada)
    assert recusada.cumpriu is True
    assert recusada.comprovacao == "Agora sim."
    assert sessao.query(DesbloqueioDaMissao).count() == 1


def test_comprovante_em_forma_diferente_da_aceita_e_recusado(sessao, cenario):
    cenario["pratico"](TipoDeProducaoDaCriacaoOriginal.video)
    with pytest.raises(ErroDeValidacao) as erro:
        _lancar(
            sessao,
            cenario,
            comprovante=ComprovanteDeclarado("texto", "Fiz."),
            julgamento=JulgamentoDeclarado(cumpriu=True),
        )
    assert "video" in erro.value.mensagem
    sessao.rollback()
    assert sessao.query(Resultado).count() == 0
    assert sessao.query(DesbloqueioDaMissao).count() == 0


def test_pratico_anterior_a_forma_aceita_nasce_sem_comprovacao(sessao, cenario):
    cenario["pratico"](None)
    with pytest.raises(ErroDeValidacao) as erro:
        _lancar(
            sessao,
            cenario,
            comprovante=ComprovanteDeclarado("texto", "Fiz."),
            julgamento=JulgamentoDeclarado(cumpriu=True, publicavel=True),
        )
    assert erro.value.campo == "publicavel"
    sessao.rollback()
    _lancar(
        sessao,
        cenario,
        comprovante=ComprovanteDeclarado("texto", "Fiz."),
        julgamento=JulgamentoDeclarado(cumpriu=True),
    )
    declaracao = sessao.query(DesbloqueioDaMissao).one()
    assert declaracao.cumpriu is True
    assert declaracao.comprovacao is None


def test_guerreiro_nao_inscrito_e_recusado(sessao, cenario, criar_persona, criar_comunidade):
    cenario["pratico"](TipoDeProducaoDaCriacaoOriginal.texto)
    cenario["guerreiro"] = criar_persona(Papel.guerreiro, comunidade=criar_comunidade())
    with pytest.raises(ErroDeValidacao):
        _lancar(
            sessao,
            cenario,
            comprovante=ComprovanteDeclarado("texto", "Fiz."),
            julgamento=JulgamentoDeclarado(cumpriu=True),
        )


def test_julgamento_negativo_sem_motivo_desfaz_o_resultado(sessao, cenario):
    cenario["pratico"](TipoDeProducaoDaCriacaoOriginal.texto)
    with pytest.raises(ErroDeValidacao) as erro:
        _lancar(
            sessao,
            cenario,
            comprovante=ComprovanteDeclarado("texto", "Fiz."),
            julgamento=JulgamentoDeclarado(cumpriu=False),
        )
    assert erro.value.campo == "motivo"
    sessao.rollback()
    assert sessao.query(Resultado).count() == 0


def test_lancamento_por_aula_do_admin_segue_sem_julgamento(sessao, cenario, criar_persona):
    cenario["pratico"](TipoDeProducaoDaCriacaoOriginal.texto)
    _, gravados = lancar_atividade_realizada(
        sessao,
        operador=criar_persona(Papel.admin),
        aula=cenario["aula"],
        resultados=[
            ResultadoDeclarado(
                guerreiro_id=cenario["guerreiro"].id,
                atividade=cenario["atividade"],
                momento_do_fato=MOMENTO,
                producao="Feito.",
                desfecho=DesfechoDoResultado.realizada,
            )
        ],
    )
    assert len(gravados) == 1


# --- leituras (`RF-09-151`) --------------------------------------------------


def test_mestre_ve_so_os_resultados_das_atividades_dele(
    sessao, cenario, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    _lancar(sessao, cenario, comprovante=ComprovanteDeclarado("texto", "Meu."))
    outro = criar_persona(Papel.mestre)
    atividade_alheia = criar_atividade(criar_missao(criar_trilha(outro), outro), outro)
    lancar_resultados_da_atividade(
        sessao,
        operador=outro,
        aula=cenario["aula"],
        atividade=atividade_alheia,
        resultados=[
            ResultadoDeclarado(
                guerreiro_id=cenario["guerreiro"].id,
                atividade=atividade_alheia,
                momento_do_fato=MOMENTO,
                producao="Alheio.",
                desfecho=DesfechoDoResultado.realizada,
            )
        ],
    )
    sessao.commit()

    do_mestre = listar_resultados_da_aula(sessao, operador=cenario["mestre"], aula=cenario["aula"])
    assert [r.producao for r, _ in do_mestre] == ["Meu."]
    do_admin = listar_resultados_da_aula(
        sessao, operador=criar_persona(Papel.admin), aula=cenario["aula"]
    )
    assert len(do_admin) == 2


def test_bytes_do_comprovante_ao_autor_e_403_aos_demais(
    sessao, cenario, armazenamento, criar_persona
):
    envio_id = _abrir_e_enviar(sessao, armazenamento, cenario)
    resultado = _lancar(
        sessao,
        cenario,
        comprovante=ComprovanteDeclarado("imagem", envio_id=envio_id),
        armazenamento=armazenamento,
    )
    arquivo = ler_arquivo_do_comprovante(
        sessao, operador=cenario["mestre"], resultado=resultado, armazenamento=armazenamento
    )
    assert arquivo.bytes_do_arquivo == FOTO
    assert arquivo.tipo_mime == "image/jpeg"
    with pytest.raises(PermissaoNegada):
        ler_arquivo_do_comprovante(
            sessao,
            operador=criar_persona(Papel.mestre),
            resultado=resultado,
            armazenamento=armazenamento,
        )


# --- rotas -------------------------------------------------------------------


def _cabecalhos(chave, criar_sessao_de_teste, persona):
    token, _ = criar_sessao_de_teste(persona)
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def test_rotas_do_lancamento_com_foto_e_julgamento(
    cliente, sessao, cenario, criar_chave, criar_sessao_de_teste, criar_nick
):
    cenario["pratico"](TipoDeProducaoDaCriacaoOriginal.imagem)
    criar_nick(cenario["guerreiro"], "zeferina")
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, cenario["mestre"])
    guerreiro_id = cenario["guerreiro"].id

    situacao = cliente.get(
        f"/v1/missoes/{cenario['missao'].id}/desbloqueios/{guerreiro_id}", headers=cabecalhos
    )
    assert situacao.status_code == 200
    assert situacao.json()["exige_julgamento"] is True
    assert situacao.json()["estado"] == "sem_declaracao"
    assert situacao.json()["forma_aceita"] == "imagem"

    aberto = cliente.post(
        f"/v1/atividades/{cenario['atividade'].id}/lancamentos/comprovantes",
        json={"tipo": "imagem", "tipo_mime": "image/jpeg", "tamanho_declarado": len(FOTO)},
        headers=cabecalhos,
    )
    assert aberto.status_code == 201
    enviado = cliente.put(
        aberto.json()["endereco_da_sessao"],
        content=FOTO,
        headers={**cabecalhos, "Content-Range": f"bytes 0-{len(FOTO) - 1}/{len(FOTO)}"},
    )
    assert enviado.status_code == 200

    lancado = cliente.post(
        f"/v1/atividades/{cenario['atividade'].id}/lancamentos",
        json={
            "aula_id": str(cenario["aula"].id),
            "participantes": [
                {
                    "guerreiro_id": str(guerreiro_id),
                    "momento_do_fato": MOMENTO.isoformat(),
                    "desfecho": "realizada",
                    "comprovante": {"tipo": "imagem", "envio_id": aberto.json()["envio_id"]},
                    "julgamento_do_pratico": {"cumpriu": True, "publicavel": True},
                }
            ],
        },
        headers=cabecalhos,
    )
    assert lancado.status_code == 201, lancado.text
    assert lancado.json()["resultados"][0]["comprovante_tipo"] == "imagem"

    lidos = cliente.get(f"/v1/aulas/{cenario['aula'].id}/resultados", headers=cabecalhos)
    assert lidos.status_code == 200
    linha = lidos.json()[0]
    assert linha["nick"] == "zeferina"
    assert linha["tem_arquivo"] is True
    assert "nome" not in linha

    arquivo = cliente.get(f"/v1/resultados/{linha['id']}/comprovante", headers=cabecalhos)
    assert arquivo.status_code == 200
    assert arquivo.content == FOTO

    depois = cliente.get(
        f"/v1/missoes/{cenario['missao'].id}/desbloqueios/{guerreiro_id}", headers=cabecalhos
    )
    assert depois.json()["estado"] == "cumpriu"
    assert depois.json()["exige_julgamento"] is False


def test_rotas_de_leitura_recusam_quem_nao_e_autor_nem_admin(
    cliente, sessao, cenario, criar_chave, criar_sessao_de_teste, criar_persona
):
    resultado = _lancar(sessao, cenario, comprovante=ComprovanteDeclarado("texto", "Fiz."))
    chave, _ = criar_chave()
    alheio = _cabecalhos(chave, criar_sessao_de_teste, criar_persona(Papel.mestre))
    guerreiro = _cabecalhos(chave, criar_sessao_de_teste, cenario["guerreiro"])
    autor = _cabecalhos(chave, criar_sessao_de_teste, cenario["mestre"])

    assert (
        cliente.get(
            f"/v1/missoes/{cenario['missao'].id}/desbloqueios/{cenario['guerreiro'].id}",
            headers=alheio,
        ).status_code
        == 403
    )
    assert (
        cliente.get(f"/v1/resultados/{resultado.id}/comprovante", headers=guerreiro).status_code
        == 403
    )
    assert (
        cliente.get(f"/v1/aulas/{cenario['aula'].id}/resultados", headers=guerreiro).status_code
        == 403
    )
    assert (
        cliente.get(f"/v1/resultados/{resultado.id}/comprovante", headers=autor).status_code == 404
    )
