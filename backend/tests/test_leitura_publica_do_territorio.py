import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import text

from nucleo.coletas.modelo import FormaDeRegistro, RegistroDeColeta
from nucleo.locais.modelo import NivelDoLocal
from nucleo.locais.regra import resolver_locais_publicados
from nucleo.personas.modelo import Papel

MOMENTO = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)


def test_resolve_local_publicado_a_partir_de_cada_um_dos_seis_niveis(
    sessao, criar_comunidade, criar_local
):
    """Sobe até o bairro a partir de qualquer nível abaixo dele; comunidade e
    bairro resolvem para si mesmos (`RN-08-13`, tasks — 2.2)."""
    comunidade = criar_comunidade()
    raiz = criar_local(comunidade, nivel=NivelDoLocal.comunidade, rotulo="Comunidade")
    bairro = criar_local(comunidade, nivel=NivelDoLocal.bairro, rotulo="Bairro", local_pai=raiz)
    rua = criar_local(comunidade, nivel=NivelDoLocal.rua, rotulo="Rua", local_pai=bairro)
    condominio = criar_local(
        comunidade, nivel=NivelDoLocal.condominio, rotulo="Condomínio", local_pai=rua
    )
    bloco = criar_local(comunidade, nivel=NivelDoLocal.bloco, rotulo="Bloco", local_pai=condominio)
    quadra = criar_local(comunidade, nivel=NivelDoLocal.quadra, rotulo="Quadra", local_pai=bloco)

    mapa = resolver_locais_publicados(sessao, comunidade_id=comunidade.id)
    resultado = {linha.local_id: linha.local_publicado_id for linha in sessao.query(mapa).all()}

    assert resultado[raiz.id] == raiz.id
    assert resultado[bairro.id] == bairro.id
    assert resultado[rua.id] == bairro.id
    assert resultado[condominio.id] == bairro.id
    assert resultado[bloco.id] == bairro.id
    assert resultado[quadra.id] == bairro.id


def _preparar_territorio(criar_comunidade, criar_local):
    """Comunidade com raiz e um bairro, prontos para receber locais mais
    finos e séries de coleta."""
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


def test_serie_publica_sem_chave_e_recusada(cliente, criar_comunidade):
    comunidade = criar_comunidade()
    resposta = cliente.get(f"/v1/comunidades/{comunidade.id}/series")
    assert resposta.status_code == 401


def test_serie_publica_responde_sem_token_de_sessao(
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
        f"/v1/comunidades/{comunidade.id}/series", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200


def test_resposta_publica_nao_traz_nick_nome_avatar_nem_id_do_coletor(
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
    """5.1: nenhum atributo do coletor sai — nem nick, nem nome, nem avatar,
    nem identificador (`RN-08-12`)."""
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
        f"/v1/comunidades/{comunidade.id}/series", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    corpo = resposta.text
    for guerreiro_id in guerreiros_ids:
        assert guerreiro_id not in corpo
    campos_esperados = {"momento_da_medicao", "valor", "recorte"}
    for item in resposta.json()["itens"]:
        assert set(item.keys()) == campos_esperados
        campos_do_recorte = {
            "tipo_de_coleta_id",
            "tipo_de_coleta_nome",
            "local_publicado_id",
            "local_publicado_nivel",
            "local_publicado_rotulo",
        }
        assert set(item["recorte"].keys()) == campos_do_recorte


def test_registro_de_rua_compoe_o_agregado_do_bairro_sem_expor_o_nivel_de_rua(
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
    """5.2: nenhum recorte abaixo do bairro é devolvido; registro de rua
    entra no bairro que a contém (`RN-08-13`)."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    rua = criar_local(comunidade, nivel=NivelDoLocal.rua, rotulo="Rua da Praça", local_pai=bairro)
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
        f"/v1/comunidades/{comunidade.id}/series", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    itens = resposta.json()["itens"]
    assert len(itens) == 3
    for item in itens:
        assert item["recorte"]["local_publicado_id"] == str(bairro.id)
        assert item["recorte"]["local_publicado_nivel"] == "bairro"
    assert "Rua da Praça" not in resposta.text


def test_bairro_com_piso_publica_e_bairro_abaixo_do_piso_sobe_para_comunidade(
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
    """5.3: bairro com três coletores distintos publica sozinho; com dois,
    sobe para a comunidade e some da resposta sob o próprio rótulo
    (`RF-08-28`, `RN-08-24`)."""
    comunidade, raiz, bairro_a = _preparar_territorio(criar_comunidade, criar_local)
    bairro_b = criar_local(comunidade, nivel=NivelDoLocal.bairro, rotulo="Bairro B", local_pai=raiz)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )

    for _ in range(3):
        _registrar(
            criar_persona,
            criar_serie_de_coleta,
            criar_registro_de_coleta,
            desafio=desafio,
            local=bairro_a,
            comunidade=comunidade,
        )
    for _ in range(2):
        _registrar(
            criar_persona,
            criar_serie_de_coleta,
            criar_registro_de_coleta,
            desafio=desafio,
            local=bairro_b,
            comunidade=comunidade,
        )
    # Um coletor a mais direto na comunidade: fecha o piso no topo para os
    # dois que subiram de "Bairro B" aparecerem sob "Comunidade".
    _registrar(
        criar_persona,
        criar_serie_de_coleta,
        criar_registro_de_coleta,
        desafio=desafio,
        local=raiz,
        comunidade=comunidade,
    )

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{comunidade.id}/series", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    itens = resposta.json()["itens"]
    rotulos = {item["recorte"]["local_publicado_rotulo"] for item in itens}
    assert rotulos == {"Bairro A", "Comunidade"}
    assert sum(1 for item in itens if item["recorte"]["local_publicado_rotulo"] == "Bairro A") == 3
    assert (
        sum(1 for item in itens if item["recorte"]["local_publicado_rotulo"] == "Comunidade") == 3
    )


def test_subida_nao_deixa_rastro_do_bairro_suprimido(
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
    """5.4: recorte que não alcança o piso nem na comunidade não é
    publicado — nenhuma linha vazia, contagem ou rótulo denuncia a
    supressão (`RF-08-28`, `RN-08-24`)."""
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
        f"/v1/comunidades/{comunidade.id}/series", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["itens"] == []
    assert corpo["proximo_cursor"] is None
    assert "Bairro A" not in resposta.text


def test_dois_bairros_com_os_mesmos_coletores_somam_uma_so_vez_ao_subir(
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
    """5.5: dois bairros abaixo do piso com os mesmos coletores somam
    coletores distintos uma só vez ao subir; a comunidade continua abaixo
    do piso (`RN-08-24`)."""
    comunidade, raiz, bairro_c = _preparar_territorio(criar_comunidade, criar_local)
    bairro_d = criar_local(comunidade, nivel=NivelDoLocal.bairro, rotulo="Bairro D", local_pai=raiz)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )

    guerreiro_1 = criar_persona(Papel.guerreiro, comunidade=comunidade)
    guerreiro_2 = criar_persona(Papel.guerreiro, comunidade=comunidade)
    for guerreiro in (guerreiro_1, guerreiro_2):
        for local in (bairro_c, bairro_d):
            serie = criar_serie_de_coleta(guerreiro, desafio, local)
            criar_registro_de_coleta(serie, guerreiro, comunidade.id, momento_do_fato=MOMENTO)

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{comunidade.id}/series", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    assert resposta.json()["itens"] == []


def test_parametro_nao_declarado_e_recusado_com_422(cliente, criar_chave, criar_comunidade):
    """5.7 (parte 1)."""
    comunidade = criar_comunidade()
    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{comunidade.id}/series",
        params={"nao_declarado": "x"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 422


def test_cursor_percorre_todos_os_pontos_sem_repetir_e_sem_faltar(
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
    """5.7 (parte 2): o cursor percorre todos os pontos publicáveis sem
    repetir nenhum e sem faltar nenhum (`RF-01-28`)."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    total_de_pontos = 7
    for i in range(total_de_pontos):
        _registrar(
            criar_persona,
            criar_serie_de_coleta,
            criar_registro_de_coleta,
            desafio=desafio,
            local=bairro,
            comunidade=comunidade,
            momento=MOMENTO.replace(hour=0) + timedelta(hours=i),
        )

    chave, _ = criar_chave()
    headers = {"X-Chave-Aplicacao": chave}
    coletados = []
    cursor = None
    while True:
        params = {"tamanho": "3"}
        if cursor:
            params["cursor"] = cursor
        resposta = cliente.get(
            f"/v1/comunidades/{comunidade.id}/series", params=params, headers=headers
        )
        assert resposta.status_code == 200
        corpo = resposta.json()
        coletados.extend(item["momento_da_medicao"] for item in corpo["itens"])
        cursor = corpo["proximo_cursor"]
        if cursor is None:
            break

    assert len(coletados) == total_de_pontos
    assert len(set(coletados)) == total_de_pontos


def test_periodo_recorta_pela_data_da_medicao_e_piso_e_apurado_dentro_do_periodo(
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
    """5.8: recorte com três coletores no total e dois dentro do período não
    é publicado naquele período (`RF-08-15`, `RN-08-24`)."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    dentro_do_periodo = datetime(2026, 6, 15, 12, 0, tzinfo=UTC)
    fora_do_periodo = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)

    for _ in range(2):
        _registrar(
            criar_persona,
            criar_serie_de_coleta,
            criar_registro_de_coleta,
            desafio=desafio,
            local=bairro,
            comunidade=comunidade,
            momento=dentro_do_periodo,
        )
    _registrar(
        criar_persona,
        criar_serie_de_coleta,
        criar_registro_de_coleta,
        desafio=desafio,
        local=bairro,
        comunidade=comunidade,
        momento=fora_do_periodo,
    )

    chave, _ = criar_chave()
    headers = {"X-Chave-Aplicacao": chave}

    sem_periodo = cliente.get(f"/v1/comunidades/{comunidade.id}/series", headers=headers)
    assert sem_periodo.status_code == 200
    assert len(sem_periodo.json()["itens"]) == 3

    com_periodo = cliente.get(
        f"/v1/comunidades/{comunidade.id}/series",
        params={
            "periodo_inicio": "2026-06-01T00:00:00-03:00",
            "periodo_fim": "2026-06-30T23:59:59-03:00",
        },
        headers=headers,
    )
    assert com_periodo.status_code == 200
    assert com_periodo.json()["itens"] == []


def test_registro_invalidado_fica_fora_da_agregacao(
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
    """5.9: registro com situação inválida fica fora do valor, da contagem e
    da contagem de coletores — grava a situação diretamente, já que
    `SituacaoDoRegistro` só declara `valida` nesta fatia (`RN-08-09`,
    design — Riscos)."""
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
        f"/v1/comunidades/{comunidade.id}/series", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    assert len(resposta.json()["itens"]) == 3


def test_registro_por_foto_sai_sem_valor_e_sem_midia(
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
    """5.10: registro por foto sai como ponto sem valor numérico, e nenhuma
    mídia ou referência de mídia acompanha a resposta (`RF-08-21`,
    `RN-08-16`)."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    autor_do_tipo = criar_persona(Papel.mestre)
    tipo_por_foto = criar_tipo_de_coleta(
        autor_do_tipo,
        nome="Foto do lixão",
        forma_de_registro=FormaDeRegistro.foto,
        unidade=None,
        faixa_minima=None,
        faixa_maxima=None,
    )
    desafio, _ = _montar_desafio(
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        tipo=tipo_por_foto,
    )
    for _ in range(3):
        guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
        serie = criar_serie_de_coleta(guerreiro, desafio, bairro)
        criar_registro_de_coleta(
            serie,
            guerreiro,
            comunidade.id,
            momento_do_fato=MOMENTO,
            valor=None,
            unidade=None,
            midia_referencia="registros-de-coleta/segredo-do-teste",
        )

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/comunidades/{comunidade.id}/series", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    itens = resposta.json()["itens"]
    assert len(itens) == 3
    for item in itens:
        assert item["valor"] is None
    assert "segredo-do-teste" not in resposta.text
    assert "midia" not in resposta.text.lower()


def test_leitura_publica_nao_altera_o_vinculo_de_autoria(
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
    """5.11: a leitura pública não altera o vínculo de autoria — os
    registros seguem gravados com o coletor de cada um (`RN-08-11`,
    `RN-08-12`)."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    desafio, _ = _montar_desafio(
        criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
    )
    guerreiro, serie, registro = _registrar(
        criar_persona,
        criar_serie_de_coleta,
        criar_registro_de_coleta,
        desafio=desafio,
        local=bairro,
        comunidade=comunidade,
    )

    chave, _ = criar_chave()
    cliente.get(f"/v1/comunidades/{comunidade.id}/series", headers={"X-Chave-Aplicacao": chave})

    sessao.expire_all()
    atualizado = sessao.get(RegistroDeColeta, (registro.id, registro.momento_do_fato))
    assert atualizado.autor_id == guerreiro.id
    assert serie.coletor_id == guerreiro.id


def test_comunidade_publica_traz_locais_ate_o_bairro_e_404_para_inexistente(
    cliente, criar_chave, criar_comunidade, criar_local
):
    """4.3 / RN-08-13: os locais de nível comunidade e bairro aparecem;
    nenhum de rua ou abaixo aparece; comunidade inexistente responde 404."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    rua = criar_local(comunidade, nivel=NivelDoLocal.rua, rotulo="Rua Oculta", local_pai=bairro)

    chave, _ = criar_chave()
    resposta = cliente.get(f"/v1/comunidades/{comunidade.id}", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    corpo = resposta.json()
    ids_dos_locais = {local["id"] for local in corpo["locais"]}
    assert ids_dos_locais == {str(raiz.id), str(bairro.id)}
    assert str(rua.id) not in resposta.text
    assert "Rua Oculta" not in resposta.text

    inexistente = cliente.get(
        f"/v1/comunidades/{uuid.uuid4()}", headers={"X-Chave-Aplicacao": chave}
    )
    assert inexistente.status_code == 404


def test_comunidade_publica_traz_so_os_tipos_de_coleta_com_serie_aberta(
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
):
    """4.3: só os tipos sobre os quais há série aberta na comunidade
    aparecem — não os do catálogo sem série ali."""
    comunidade, raiz, bairro = _preparar_territorio(criar_comunidade, criar_local)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo_com_serie = criar_tipo_de_coleta(mestre, nome="Com série")
    tipo_sem_serie = criar_tipo_de_coleta(mestre, nome="Sem série")
    desafio = criar_desafio_de_coleta(missao, mestre, tipo=tipo_com_serie)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_serie_de_coleta(guerreiro, desafio, bairro)

    chave, _ = criar_chave()
    resposta = cliente.get(f"/v1/comunidades/{comunidade.id}", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    nomes = {tipo["nome"] for tipo in resposta.json()["tipos_de_coleta"]}
    assert nomes == {"Com série"}
    assert tipo_sem_serie.nome not in resposta.text
