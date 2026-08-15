import csv
import io
import uuid
from datetime import UTC, datetime

from sqlalchemy import text

from nucleo.locais.modelo import NivelDoLocal
from nucleo.personas.modelo import Papel

MOMENTO = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)


def _preparar_territorio(criar_comunidade, criar_local):
    comunidade = criar_comunidade()
    raiz = criar_local(comunidade, nivel=NivelDoLocal.comunidade, rotulo="Comunidade")
    bairro = criar_local(comunidade, nivel=NivelDoLocal.bairro, rotulo="Bairro A", local_pai=raiz)
    return comunidade, raiz, bairro


def _montar_desafio(
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    **kwargs,
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = kwargs.pop("tipo", None) or criar_tipo_de_coleta(mestre, **kwargs.pop("tipo_kwargs", {}))
    desafio = criar_desafio_de_coleta(missao, mestre, tipo=tipo, **kwargs)
    return desafio, tipo


def _registrar(
    criar_persona,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
    *,
    desafio,
    local,
    comunidade,
    momento=None,
    valor=25.0,
):
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    serie = criar_serie_de_coleta(guerreiro, desafio, local)
    registro = criar_registro_de_coleta(
        serie, guerreiro, comunidade.id, momento_do_fato=momento or MOMENTO, valor=valor
    )
    return guerreiro, serie, registro


def _ler_csv(texto: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO(texto)))


def test_exportacao_sem_chave_e_recusada(cliente, criar_comunidade):
    comunidade = criar_comunidade()
    resposta = cliente.get(f"/v1/comunidades/{comunidade.id}/exportacao")
    assert resposta.status_code == 401


def test_exportacao_com_chave_e_sem_token_de_sessao_responde(
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """4.9: exportação com chave e sem token de sessão responde."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    for _ in range(3):
        _registrar(
            criar_persona,
            criar_serie_de_coleta,
            criar_registro_de_coleta,
            desafio=desafio,
            local=bairro,
            comunidade=comunidade,
        )

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{comunidade.id}/exportacao", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    assert resposta.headers["content-type"].startswith("text/csv")


def test_exportacao_de_comunidade_inexistente_responde_404(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{uuid.uuid4()}/exportacao", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 404


def test_csv_traz_cabecalho_declarado_e_uma_tabela_por_arquivo(
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """4.1: cabeçalho na primeira linha, sem envelope em volta."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    for _ in range(3):
        _registrar(
            criar_persona,
            criar_serie_de_coleta,
            criar_registro_de_coleta,
            desafio=desafio,
            local=bairro,
            comunidade=comunidade,
        )

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{comunidade.id}/exportacao", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    linhas = resposta.text.strip().splitlines()
    assert linhas[0] == "momento_da_medicao,tipo_de_coleta,local_nivel,local_rotulo,valor"
    assert len(linhas) == 4  # cabeçalho + 3 registros
    assert not resposta.text.strip().startswith("{")
    assert not resposta.text.strip().startswith("[")


def test_csv_nao_traz_nick_nome_avatar_nem_identificador_de_guerreiro(
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """4.2: nenhum atributo do coletor, nem contagem de coletores."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    guerreiros_ids = []
    for _ in range(3):
        guerreiro, _, _ = _registrar(
            criar_persona,
            criar_serie_de_coleta,
            criar_registro_de_coleta,
            desafio=desafio,
            local=bairro,
            comunidade=comunidade,
        )
        guerreiros_ids.append(str(guerreiro.id))

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{comunidade.id}/exportacao", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    for guerreiro_id in guerreiros_ids:
        assert guerreiro_id not in resposta.text
    linhas = _ler_csv(resposta.text)
    campos_esperados = {
        "momento_da_medicao",
        "tipo_de_coleta",
        "local_nivel",
        "local_rotulo",
        "valor",
    }
    assert set(linhas[0].keys()) == campos_esperados


def test_registro_de_rua_compoe_o_agregado_do_bairro_na_exportacao(
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """4.3: registro de rua compõe o agregado do bairro; nenhum rótulo
    abaixo do bairro aparece."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    rua = criar_local(comunidade, nivel=NivelDoLocal.rua, rotulo="Rua Oculta", local_pai=bairro)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    for _ in range(3):
        _registrar(
            criar_persona,
            criar_serie_de_coleta,
            criar_registro_de_coleta,
            desafio=desafio,
            local=rua,
            comunidade=comunidade,
        )

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{comunidade.id}/exportacao", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    linhas = _ler_csv(resposta.text)
    assert len(linhas) == 3
    for linha in linhas:
        assert linha["local_rotulo"] == "Bairro A"
        assert linha["local_nivel"] == "bairro"
    assert "Rua Oculta" not in resposta.text


def test_piso_de_coletores_vale_na_exportacao(
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """4.4: bairro abaixo do piso sobe ao nível da comunidade; o que não
    alcança o piso nem no topo fica fora."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    for _ in range(2):
        _registrar(
            criar_persona,
            criar_serie_de_coleta,
            criar_registro_de_coleta,
            desafio=desafio,
            local=bairro,
            comunidade=comunidade,
        )

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{comunidade.id}/exportacao", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    assert resposta.text.strip().splitlines() == [
        "momento_da_medicao,tipo_de_coleta,local_nivel,local_rotulo,valor"
    ]
    assert "Bairro A" not in resposta.text


def test_registro_invalidado_fica_fora_da_exportacao(
    sessao,
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """4.5: registro invalidado não compõe linha, valor nem contagem."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    for _ in range(3):
        _registrar(
            criar_persona,
            criar_serie_de_coleta,
            criar_registro_de_coleta,
            desafio=desafio,
            local=bairro,
            comunidade=comunidade,
        )
    _, _, registro_invalido = _registrar(
        criar_persona,
        criar_serie_de_coleta,
        criar_registro_de_coleta,
        desafio=desafio,
        local=bairro,
        comunidade=comunidade,
    )
    sessao.execute(
        text("UPDATE registro_de_coleta SET situacao = 'invalidada' WHERE id = :id"),
        {"id": str(registro_invalido.id)},
    )
    sessao.commit()

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{comunidade.id}/exportacao", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    assert len(_ler_csv(resposta.text)) == 3


def test_periodo_recorta_pela_data_da_medicao_e_periodo_coberto_e_o_do_conjunto(
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
    sobrescrever_configuracao,
):
    """4.6: o período recorta pela data da medição, e o período coberto
    declarado é o do conjunto, não o do pedido. Piso rebaixado para 1: o
    que se testa aqui é o recorte por período, não o piso de coletores,
    já coberto em `test_piso_de_coletores_vale_na_exportacao`."""
    sobrescrever_configuracao(territorio_piso_de_coletores_distintos=1)
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    primeiro = datetime(2026, 6, 5, 12, 0, tzinfo=UTC)
    segundo = datetime(2026, 6, 20, 12, 0, tzinfo=UTC)
    fora = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    for momento in (primeiro, segundo, fora):
        _registrar(
            criar_persona,
            criar_serie_de_coleta,
            criar_registro_de_coleta,
            desafio=desafio,
            local=bairro,
            comunidade=comunidade,
            momento=momento,
        )

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{comunidade.id}/exportacao",
        params={
            "periodo_inicio": "2026-01-01T00:00:00-03:00",
            "periodo_fim": "2026-12-31T23:59:59-03:00",
        },
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 200
    assert len(_ler_csv(resposta.text)) == 3
    # Pedido pelo ano inteiro; o período coberto declarado é só o que o
    # conjunto de fato contém — a data da primeira e da última medição.
    assert resposta.headers["X-Periodo-Coberto-Inicio"] == fora.isoformat()
    assert resposta.headers["X-Periodo-Coberto-Fim"] == segundo.isoformat()

    com_periodo = cliente.get(
        f"/v1/comunidades/{comunidade.id}/exportacao",
        params={
            "periodo_inicio": "2026-06-01T00:00:00-03:00",
            "periodo_fim": "2026-06-30T23:59:59-03:00",
        },
        headers={"X-Chave-Aplicacao": chave},
    )
    assert com_periodo.status_code == 200
    assert len(_ler_csv(com_periodo.text)) == 2
    assert com_periodo.headers["X-Periodo-Coberto-Inicio"] == primeiro.isoformat()
    assert com_periodo.headers["X-Periodo-Coberto-Fim"] == segundo.isoformat()


def test_conjunto_vazio_declara_periodo_vazio(cliente, criar_chave, criar_comunidade):
    comunidade = criar_comunidade()
    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{comunidade.id}/exportacao", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    assert resposta.headers["X-Periodo-Coberto-Inicio"] == ""
    assert resposta.headers["X-Periodo-Coberto-Fim"] == ""
    assert _ler_csv(resposta.text) == []


def test_cabecalhos_declaram_licenca_e_endereco_do_dicionario(
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """4.8: a saída declara a licença CC BY-SA; o cabeçalho endereça a rota
    irmã do dicionário de dados."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    for _ in range(3):
        _registrar(
            criar_persona,
            criar_serie_de_coleta,
            criar_registro_de_coleta,
            desafio=desafio,
            local=bairro,
            comunidade=comunidade,
        )

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{comunidade.id}/exportacao", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    assert resposta.headers["X-Licenca"] == "CC BY-SA"
    endereco = resposta.headers["X-Dicionario-De-Dados"]
    assert endereco.startswith(f"/v1/comunidades/{comunidade.id}/exportacao/dicionario")

    dicionario = cliente.get(endereco, headers={"X-Chave-Aplicacao": chave})
    assert dicionario.status_code == 200


def test_dicionario_descreve_exatamente_os_campos_do_csv(
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """4.7: todo campo do CSV tem entrada no dicionário, e os dois
    conjuntos de campos coincidem exatamente."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    for _ in range(3):
        _registrar(
            criar_persona,
            criar_serie_de_coleta,
            criar_registro_de_coleta,
            desafio=desafio,
            local=bairro,
            comunidade=comunidade,
        )

    chave, _ = criar_chave()
    exportacao = cliente.get(
        f"/v1/comunidades/{comunidade.id}/exportacao", headers={"X-Chave-Aplicacao": chave}
    )
    campos_do_csv = set(exportacao.text.strip().splitlines()[0].split(","))

    dicionario = cliente.get(
        f"/v1/comunidades/{comunidade.id}/exportacao/dicionario",
        headers={"X-Chave-Aplicacao": chave},
    )
    assert dicionario.status_code == 200
    corpo = dicionario.json()
    campos_do_dicionario = {campo["campo"] for campo in corpo["campos"]}
    assert campos_do_dicionario == campos_do_csv
    for campo in corpo["campos"]:
        assert campo["unidade"]
        assert campo["cadencia"]
        assert campo["origem"]


def test_dicionario_declara_licenca_e_meta_17_18_com_periodo_coberto(
    cliente,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    _registrar(
        criar_persona,
        criar_serie_de_coleta,
        criar_registro_de_coleta,
        desafio=desafio,
        local=bairro,
        comunidade=comunidade,
    )
    _registrar(
        criar_persona,
        criar_serie_de_coleta,
        criar_registro_de_coleta,
        desafio=desafio,
        local=bairro,
        comunidade=comunidade,
    )
    _registrar(
        criar_persona,
        criar_serie_de_coleta,
        criar_registro_de_coleta,
        desafio=desafio,
        local=bairro,
        comunidade=comunidade,
    )

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{comunidade.id}/exportacao/dicionario",
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["licenca"] == "CC BY-SA"
    assert "17.18" in corpo["contribuicao_meta_17_18"]
    assert corpo["periodo_coberto_inicio"] is not None
    assert corpo["periodo_coberto_fim"] is not None


def test_dicionario_sem_chave_e_recusada_e_comunidade_inexistente_responde_404(
    cliente, criar_chave, criar_comunidade
):
    comunidade = criar_comunidade()
    sem_chave = cliente.get(f"/v1/comunidades/{comunidade.id}/exportacao/dicionario")
    assert sem_chave.status_code == 401

    chave, _ = criar_chave()
    inexistente = cliente.get(
        f"/v1/comunidades/{uuid.uuid4()}/exportacao/dicionario",
        headers={"X-Chave-Aplicacao": chave},
    )
    assert inexistente.status_code == 404
