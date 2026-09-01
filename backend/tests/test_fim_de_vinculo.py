from datetime import UTC, datetime, timedelta

import pytest

from nucleo.aulas.modelo import Aula, ModoDeComprovacao, Presenca
from nucleo.biometria.modelo import ApagamentoDeTemplate, GatilhoDeApagamento
from nucleo.comunidades.modelo import ComunidadeVirtual
from nucleo.erros import VinculoDoGuerreiroJaEncerrado
from nucleo.personas.modelo import Papel
from nucleo.pontos_de_apoio.modelo import PontoDeApoio
from nucleo.vinculo_do_guerreiro.modelo import FimDeVinculo, OrigemDoFimDeVinculo
from nucleo.vinculo_do_guerreiro.regra import (
    MESES_SEM_ATIVIDADE_PARA_VARREDURA,
    encerrar_vinculo,
    varrer_vinculos_vencidos,
)

MOTIVO = "Pedido de saída da família."


def _guerreiro_criado_ha(sessao, criar_persona, meses: int):
    guerreiro = criar_persona(Papel.guerreiro)
    guerreiro.criada_em = datetime.now(UTC) - timedelta(days=meses * 31)
    sessao.commit()
    return guerreiro


def _registrar_presenca_ha(sessao, criar_persona, guerreiro, dias: int):
    autor = criar_persona(Papel.mestre)
    comunidade = ComunidadeVirtual(
        nome="Comunidade da Presença", localizacao="Bairro", granularidade_maxima="bairro"
    )
    sessao.add(comunidade)
    sessao.flush()
    ponto = PontoDeApoio(
        nome="Ponto da Presença",
        comunidade_virtual_id=comunidade.id,
        autor_id=autor.id,
        papel_do_autor=autor.papel.value,
    )
    sessao.add(ponto)
    sessao.flush()
    momento = datetime.now(UTC) - timedelta(days=dias)
    aula = Aula(
        comunidade_virtual_id=comunidade.id,
        ponto_de_apoio_id=ponto.id,
        inicio_em=momento,
        fim_em=momento + timedelta(hours=1),
        autor_id=autor.id,
        papel_do_autor=autor.papel.value,
    )
    sessao.add(aula)
    sessao.flush()
    presenca = Presenca(
        aula_id=aula.id,
        guerreiro_id=guerreiro.id,
        modo=ModoDeComprovacao.confirmacao,
        confirmador_id=autor.id,
        momento_do_fato=momento,
        autor_id=autor.id,
        papel_do_autor=autor.papel.value,
    )
    sessao.add(presenca)
    sessao.commit()


class TestEncerrarVinculo:
    def test_admin_encerra_com_motivo(self, sessao, criar_persona):
        admin = criar_persona(Papel.admin)
        guerreiro = criar_persona(Papel.guerreiro)

        fim = encerrar_vinculo(sessao, guerreiro=guerreiro, encerrado_por=admin, motivo=MOTIVO)
        sessao.commit()

        assert fim.origem == OrigemDoFimDeVinculo.admin
        assert fim.encerrado_por == admin.id
        assert fim.motivo == MOTIVO
        assert fim.momento is not None

    def test_vinculo_ja_encerrado_recusa_segundo_encerramento(self, sessao, criar_persona):
        admin = criar_persona(Papel.admin)
        guerreiro = criar_persona(Papel.guerreiro)
        encerrar_vinculo(sessao, guerreiro=guerreiro, encerrado_por=admin, motivo=MOTIVO)
        sessao.commit()

        with pytest.raises(VinculoDoGuerreiroJaEncerrado):
            encerrar_vinculo(sessao, guerreiro=guerreiro, encerrado_por=admin, motivo="De novo.")

        assert sessao.query(FimDeVinculo).filter_by(guerreiro_id=guerreiro.id).count() == 1

    def test_encerramento_marca_apagamento_em_30_dias(
        self, sessao, criar_persona, criar_template_biometrico
    ):
        admin = criar_persona(Papel.admin)
        guerreiro = criar_persona(Papel.guerreiro)
        criar_template_biometrico(guerreiro)

        encerrar_vinculo(sessao, guerreiro=guerreiro, encerrado_por=admin, motivo=MOTIVO)
        sessao.commit()

        apagamento = sessao.query(ApagamentoDeTemplate).filter_by(guerreiro_id=guerreiro.id).one()
        assert apagamento.gatilho == GatilhoDeApagamento.fim_do_vinculo
        diferenca = apagamento.apagar_em - apagamento.criado_em
        assert abs(diferenca - timedelta(days=30)) < timedelta(seconds=5)

    def test_encerramento_nao_apaga_nenhum_outro_dado(self, sessao, criar_persona):
        admin = criar_persona(Papel.admin)
        guerreiro = criar_persona(Papel.guerreiro)
        nome_antes, nascimento_antes = guerreiro.nome, guerreiro.nascimento

        encerrar_vinculo(sessao, guerreiro=guerreiro, encerrado_por=admin, motivo=MOTIVO)
        sessao.commit()

        do_banco = sessao.get(type(guerreiro), guerreiro.id)
        assert do_banco.nome == nome_antes
        assert do_banco.nascimento == nascimento_antes

    def test_fim_de_vinculo_e_somente_insercao(self, sessao, criar_persona):
        from nucleo.erros import FimDeVinculoImutavel

        admin = criar_persona(Papel.admin)
        guerreiro = criar_persona(Papel.guerreiro)
        fim = encerrar_vinculo(sessao, guerreiro=guerreiro, encerrado_por=admin, motivo=MOTIVO)
        sessao.commit()

        fim.motivo = "Editado."
        with pytest.raises(FimDeVinculoImutavel):
            sessao.commit()
        sessao.rollback()


class TestVarreduraDosDozeMeses:
    def test_doze_meses_sem_nenhum_registro_encerra_o_vinculo(self, sessao, criar_persona):
        guerreiro = _guerreiro_criado_ha(
            sessao, criar_persona, MESES_SEM_ATIVIDADE_PARA_VARREDURA + 1
        )

        encerrados = varrer_vinculos_vencidos(sessao)
        sessao.commit()

        assert encerrados == 1
        fim = sessao.query(FimDeVinculo).filter_by(guerreiro_id=guerreiro.id).one()
        assert fim.origem == OrigemDoFimDeVinculo.varredura
        assert fim.encerrado_por is None

    def test_coleta_recente_segura_o_vinculo(
        self,
        sessao,
        criar_persona,
        criar_comunidade,
        criar_local,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_missao,
        criar_trilha,
        criar_serie_de_coleta,
        criar_registro_de_coleta,
    ):
        guerreiro = _guerreiro_criado_ha(
            sessao, criar_persona, MESES_SEM_ATIVIDADE_PARA_VARREDURA + 1
        )
        autor = criar_persona(Papel.mestre)
        comunidade = criar_comunidade()
        local = criar_local(comunidade)
        trilha = criar_trilha(autor)
        missao = criar_missao(trilha, autor)
        desafio = criar_desafio_de_coleta(missao, autor)
        serie = criar_serie_de_coleta(guerreiro, desafio, local)
        criar_registro_de_coleta(
            serie,
            autor,
            comunidade_virtual_id=comunidade.id,
            momento_do_fato=datetime.now(UTC) - timedelta(days=60),
        )

        encerrados = varrer_vinculos_vencidos(sessao)
        sessao.commit()

        assert encerrados == 0
        assert sessao.query(FimDeVinculo).filter_by(guerreiro_id=guerreiro.id).count() == 0

    def test_persona_criada_recentemente_nao_e_encerrada(self, sessao, criar_persona):
        guerreiro = _guerreiro_criado_ha(sessao, criar_persona, 1)

        encerrados = varrer_vinculos_vencidos(sessao)
        sessao.commit()

        assert encerrados == 0
        assert sessao.query(FimDeVinculo).filter_by(guerreiro_id=guerreiro.id).count() == 0

    def test_varredura_repetida_nao_grava_duas_vezes(self, sessao, criar_persona):
        _guerreiro_criado_ha(sessao, criar_persona, MESES_SEM_ATIVIDADE_PARA_VARREDURA + 1)

        primeira = varrer_vinculos_vencidos(sessao)
        sessao.commit()
        segunda = varrer_vinculos_vencidos(sessao)
        sessao.commit()

        assert primeira == 1
        assert segunda == 0
        assert sessao.query(FimDeVinculo).count() == 1

    def test_presenca_recente_segura_o_vinculo(self, sessao, criar_persona):
        guerreiro = _guerreiro_criado_ha(
            sessao, criar_persona, MESES_SEM_ATIVIDADE_PARA_VARREDURA + 1
        )
        _registrar_presenca_ha(sessao, criar_persona, guerreiro, dias=30)

        encerrados = varrer_vinculos_vencidos(sessao)
        sessao.commit()

        assert encerrados == 0

    def test_varredura_marca_apagamento_em_30_dias(
        self, sessao, criar_persona, criar_template_biometrico
    ):
        guerreiro = _guerreiro_criado_ha(
            sessao, criar_persona, MESES_SEM_ATIVIDADE_PARA_VARREDURA + 1
        )
        criar_template_biometrico(guerreiro)

        varrer_vinculos_vencidos(sessao)
        sessao.commit()

        apagamento = sessao.query(ApagamentoDeTemplate).filter_by(guerreiro_id=guerreiro.id).one()
        assert apagamento.gatilho == GatilhoDeApagamento.fim_do_vinculo
