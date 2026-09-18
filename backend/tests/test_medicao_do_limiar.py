"""A medição do limiar por ponto de apoio (`RF-01-73`, `RF-04-66`, `RN-04-35`,
`RN-01-56`, decisão do fundador, 2026-09-18)."""

import pytest

from nucleo.biometria.modelo import MedicaoDoLimiar
from nucleo.biometria.regra import (
    MINIMO_DE_MEDICOES_POR_SERIE,
    MINIMO_DE_PESSOAS_NO_TETO,
    consultar_limiar_vigente,
    gravar_medicao_do_limiar,
    limiar_proposto,
)
from nucleo.erros import ErroDeValidacao
from nucleo.personas.modelo import Papel

PISO = [4.0, 5.0, 6.0, 5.5, 4.5, 6.2, 5.8, 6.4]
TETO = [11.0, 12.0, 13.0, 11.5, 12.5, 14.0, 11.2, 12.8]


def _corpo(aula_id, piso=None, teto=None, pessoas=2) -> dict:
    return {
        "aula_id": str(aula_id),
        "distancias_do_piso": piso if piso is not None else PISO,
        "distancias_do_teto": teto if teto is not None else TETO,
        "pessoas_no_teto": pessoas,
    }


class TestValorProposto:
    def test_e_o_ponto_medio_entre_o_maior_piso_e_o_menor_teto(self):
        """`RN-04-35`: equidistante das duas formas de errar."""
        assert limiar_proposto(PISO, TETO) == (6.4 + 11.0) / 2

    def test_o_nucleo_calcula_e_o_aparelho_nao_envia(self, sessao, criar_persona):
        """O limiar não está no corpo da rota: é calculado das séries."""
        from nucleo.biometria.rotas import GravarMedicaoDoLimiarEntrada

        assert "limiar" not in GravarMedicaoDoLimiarEntrada.model_fields


class TestCriterioDeConclusao:
    def test_serie_curta_nao_grava(
        self, sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
    ):
        admin = criar_persona(Papel.admin)
        ponto = criar_ponto_de_apoio(admin, criar_comunidade())
        with pytest.raises(ErroDeValidacao):
            gravar_medicao_do_limiar(
                sessao,
                ponto_de_apoio_id=ponto.id,
                distancias_do_piso=PISO[:-1],
                distancias_do_teto=TETO,
                pessoas_no_teto=2,
                operado_por=admin,
            )

    def test_teto_de_uma_pessoa_so_nao_grava(
        self, sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
    ):
        admin = criar_persona(Papel.admin)
        ponto = criar_ponto_de_apoio(admin, criar_comunidade())
        with pytest.raises(ErroDeValidacao):
            gravar_medicao_do_limiar(
                sessao,
                ponto_de_apoio_id=ponto.id,
                distancias_do_piso=PISO,
                distancias_do_teto=TETO,
                pessoas_no_teto=1,
                operado_por=admin,
            )

    def test_series_que_se_sobrepoem_nao_gravam(
        self, sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
    ):
        """`RN-04-35`: sem folga não existe limiar viável, e gravar um número
        ali seria gravar um erro."""
        admin = criar_persona(Papel.admin)
        ponto = criar_ponto_de_apoio(admin, criar_comunidade())
        with pytest.raises(ErroDeValidacao) as erro:
            gravar_medicao_do_limiar(
                sessao,
                ponto_de_apoio_id=ponto.id,
                distancias_do_piso=[4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0],
                distancias_do_teto=TETO,
                pessoas_no_teto=2,
                operado_por=admin,
            )
        assert "sobrepõem" in str(erro.value.mensagem)
        assert sessao.query(MedicaoDoLimiar).count() == 0

    def test_os_minimos_sao_os_do_rn_04_35(self):
        assert MINIMO_DE_MEDICOES_POR_SERIE == 8
        assert MINIMO_DE_PESSOAS_NO_TETO == 2


class TestLimiarVigente:
    def test_medicao_nova_substitui_a_anterior_sem_apaga_la(
        self, sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
    ):
        """`RF-01-73`: o vigente é o da medição mais recente, e a anterior
        continua consultável."""
        admin = criar_persona(Papel.admin)
        ponto = criar_ponto_de_apoio(admin, criar_comunidade())
        primeira = gravar_medicao_do_limiar(
            sessao,
            ponto_de_apoio_id=ponto.id,
            distancias_do_piso=PISO,
            distancias_do_teto=TETO,
            pessoas_no_teto=2,
            operado_por=admin,
        )
        sessao.commit()
        segunda = gravar_medicao_do_limiar(
            sessao,
            ponto_de_apoio_id=ponto.id,
            distancias_do_piso=[1.0] * 8,
            distancias_do_teto=[20.0] * 8,
            pessoas_no_teto=3,
            operado_por=admin,
        )
        sessao.commit()

        assert consultar_limiar_vigente(sessao, ponto_de_apoio_id=ponto.id) == segunda.limiar
        assert segunda.limiar != primeira.limiar
        assert sessao.query(MedicaoDoLimiar).count() == 2

    def test_ponto_de_apoio_nunca_medido_nao_tem_limiar(
        self, sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
    ):
        admin = criar_persona(Papel.admin)
        ponto = criar_ponto_de_apoio(admin, criar_comunidade())
        assert consultar_limiar_vigente(sessao, ponto_de_apoio_id=ponto.id) is None


class TestRotaDeGravacao:
    def test_mestre_grava_e_a_resposta_traz_o_limiar_calculado(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste, montar_cenario_de_entrada
    ):
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        mestre = criar_persona(Papel.mestre, criada_por=admin)
        token, _ = criar_sessao_de_teste(mestre)
        cenario = montar_cenario_de_entrada(limiar=None)

        resposta = cliente.post(
            "/v1/medicoes-do-limiar",
            json=_corpo(cenario.aula.id),
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )
        assert resposta.status_code == 201
        corpo = resposta.json()
        assert corpo["limiar"] == limiar_proposto(PISO, TETO)
        assert corpo["ponto_de_apoio_id"] == str(cenario.ponto_de_apoio.id)
        assert corpo["medido_por"] == str(mestre.id)

    def test_descritor_no_corpo_e_recusado(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste, montar_cenario_de_entrada
    ):
        """`RN-01-15`: a rota da medição nunca aceita descritor."""
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        token, _ = criar_sessao_de_teste(admin)
        cenario = montar_cenario_de_entrada(limiar=None)

        resposta = cliente.post(
            "/v1/medicoes-do-limiar",
            json=_corpo(cenario.aula.id) | {"descritor": [0.1] * 1024},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )
        assert resposta.status_code == 422

    def test_series_que_se_sobrepoem_sao_recusadas_na_rota(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste, montar_cenario_de_entrada
    ):
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        token, _ = criar_sessao_de_teste(admin)
        cenario = montar_cenario_de_entrada(limiar=None)

        resposta = cliente.post(
            "/v1/medicoes-do-limiar",
            json=_corpo(cenario.aula.id, piso=[4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0]),
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )
        assert resposta.status_code == 422

    def test_guerreiro_nao_grava_medicao(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste, montar_cenario_de_entrada
    ):
        """`RF-01-16`: restrita a Mestre e Admin pela matriz."""
        chave, _ = criar_chave()
        guerreiro = criar_persona(Papel.guerreiro)
        token, _ = criar_sessao_de_teste(guerreiro)
        cenario = montar_cenario_de_entrada(limiar=None)

        resposta = cliente.post(
            "/v1/medicoes-do-limiar",
            json=_corpo(cenario.aula.id),
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )
        assert resposta.status_code == 403


class TestRotaDeConsulta:
    def test_lista_traz_o_vigente_e_marca_quem_nao_tem(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste, montar_cenario_de_entrada
    ):
        """`RF-02-109`, `RN-01-56`: quem não tem limiar é justamente o que a
        App 03 destaca."""
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        token, _ = criar_sessao_de_teste(admin)
        medido = montar_cenario_de_entrada(limiar=7.5)
        sem_limiar = montar_cenario_de_entrada(limiar=None)

        resposta = cliente.get(
            "/v1/pontos-de-apoio/limiares",
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )
        assert resposta.status_code == 200
        por_id = {linha["ponto_de_apoio_id"]: linha for linha in resposta.json()}
        assert por_id[str(medido.ponto_de_apoio.id)]["medicao"]["limiar"] == 7.5
        assert por_id[str(sem_limiar.ponto_de_apoio.id)]["medicao"] is None

    def test_nao_existe_rota_de_edicao_do_limiar(self, cliente, criar_chave):
        """`RF-02-109`: a tela é de consulta — corrigir é medir de novo, na
        App 01. O contrato publicado é onde isso se confere."""
        chave, _ = criar_chave()
        esquema = cliente.get("/openapi.json").json()
        caminhos_do_limiar = {
            caminho: set(metodos)
            for caminho, metodos in esquema["paths"].items()
            if "limiar" in caminho
        }
        assert "/v1/medicoes-do-limiar" in caminhos_do_limiar
        assert caminhos_do_limiar["/v1/medicoes-do-limiar"] == {"post"}
        for metodos in caminhos_do_limiar.values():
            assert not metodos & {"put", "patch", "delete"}
