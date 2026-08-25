from datetime import date
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import (
    Aporte,
    FormaDeAporte,
    OrigemDoRegistro,
    SituacaoDeRessarcimento,
)
from nucleo.aportes.regra import registrar_aporte, registrar_aporte_por_absorcao
from nucleo.armazenamento.disco import ArmazenamentoEmDisco
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.fila.modelo import PretensaoDeParticipacao
from nucleo.fila.regra import registrar_solicitacao_de_participacao
from nucleo.livro_razao.modelo import Lancamento, NaturezaDoLancamento
from nucleo.livro_razao.regra import saldo_de
from nucleo.personas.modelo import Papel
from nucleo.recursos.modelo import NaturezaDoRecurso


@pytest.fixture
def cenario(sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, nome="Lanche", natureza=NaturezaDoRecurso.consumivel)
    return admin, apoiador, ponto_de_apoio, tipo


def test_admin_registra_um_aporte_material(sessao, cenario, criar_valor_de_referencia):
    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("0.50"))

    aporte = registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("3"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
    )
    sessao.commit()

    assert aporte.provedor_id == apoiador.id
    assert aporte.valor_em_moedas == Decimal("1.50")
    assert aporte.autor_id == admin.id
    lancamento = sessao.get(Lancamento, aporte.lancamento_id)
    assert lancamento.natureza == NaturezaDoLancamento.credito
    assert lancamento.tipo_de_recurso_id == tipo.id
    assert lancamento.ponto_de_apoio_id == ponto_de_apoio.id
    assert saldo_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    ) == Decimal("3.00")


def test_aporte_de_servico_tambem_declara_o_ponto_de_apoio(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, nome="Hora-aula", natureza=NaturezaDoRecurso.servico)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("2.00"))

    aporte = registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("1"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.servico,
    )
    sessao.commit()

    assert aporte.ponto_de_apoio_id == ponto_de_apoio.id
    assert saldo_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    ) == Decimal("1.00")


def test_mestre_nao_registra_aporte_pela_rota_da_gestao(
    sessao, cenario, criar_valor_de_referencia, criar_persona
):
    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo)
    mestre = criar_persona(Papel.mestre, criada_por=admin)

    with pytest.raises(PermissaoNegada):
        registrar_aporte(
            sessao,
            operador=mestre,
            provedor=apoiador,
            tipo=tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2026, 6, 1),
            forma=FormaDeAporte.material,
        )
    assert sessao.query(Aporte).count() == 0


def test_quantidade_zero_e_recusada(sessao, cenario, criar_valor_de_referencia):
    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_aporte(
            sessao,
            operador=admin,
            provedor=apoiador,
            tipo=tipo,
            quantidade=Decimal("0"),
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2026, 6, 1),
            forma=FormaDeAporte.material,
        )
    assert excinfo.value.campo == "quantidade"
    assert sessao.query(Aporte).count() == 0


def test_aporte_sem_ponto_de_apoio_e_recusado(sessao, cenario, criar_valor_de_referencia):
    admin, apoiador, _ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_aporte(
            sessao,
            operador=admin,
            provedor=apoiador,
            tipo=tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=None,
            data_do_aporte=date(2026, 6, 1),
            forma=FormaDeAporte.material,
        )
    assert excinfo.value.campo == "ponto_de_apoio_id"
    assert sessao.query(Aporte).count() == 0


def test_conversao_pela_tabela_vigente(sessao, cenario, criar_valor_de_referencia):
    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("0.50"))

    aporte = registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("3"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
    )
    sessao.commit()

    assert aporte.valor_em_moedas == Decimal("1.50")


def test_valor_novo_nao_reescreve_aporte_ja_registrado(
    sessao, cenario, criar_valor_de_referencia, criar_persona
):
    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("0.50"))

    aporte = registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("3"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
    )
    sessao.commit()

    criar_valor_de_referencia(
        admin, tipo, valor_em_moedas=Decimal("9.00"), vigencia_inicio=date(2026, 7, 1)
    )
    sessao.commit()
    sessao.refresh(aporte)

    assert aporte.valor_em_moedas == Decimal("1.50")


def test_data_do_aporte_anterior_a_vigencia_mais_antiga_e_recusada(
    sessao, cenario, criar_valor_de_referencia
):
    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo, vigencia_inicio=date(2026, 1, 1))

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_aporte(
            sessao,
            operador=admin,
            provedor=apoiador,
            tipo=tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2025, 1, 1),
            forma=FormaDeAporte.material,
        )
    assert excinfo.value.campo == "data_do_aporte"
    assert sessao.query(Aporte).count() == 0


def test_admin_registra_aporte_em_nome_de_si_mesmo_e_recusado(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo)

    with pytest.raises(PermissaoNegada):
        registrar_aporte(
            sessao,
            operador=admin,
            provedor=admin,
            tipo=tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2026, 6, 1),
            forma=FormaDeAporte.material,
        )
    assert sessao.query(Aporte).count() == 0


def test_mestre_absorve_um_recurso(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))

    aporte = registrar_aporte_por_absorcao(
        sessao,
        operador=mestre,
        tipo=tipo,
        quantidade=Decimal("2"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        valor_de_origem=Decimal("20.00"),
    )
    sessao.commit()

    assert aporte.provedor_id == mestre.id
    assert aporte.admin_homologador_id is None
    assert aporte.ressarcivel is True
    assert aporte.situacao_de_ressarcimento == SituacaoDeRessarcimento.em_aberto
    assert saldo_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    ) == Decimal("2.00")


def test_admin_absorve_um_recurso_em_nome_proprio(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo)

    aporte = registrar_aporte_por_absorcao(
        sessao,
        operador=admin,
        tipo=tipo,
        quantidade=Decimal("1"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        valor_de_origem=Decimal("10.00"),
    )
    sessao.commit()

    assert aporte.provedor_id == admin.id


def test_apoiador_nao_absorve(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo)

    with pytest.raises(PermissaoNegada):
        registrar_aporte_por_absorcao(
            sessao,
            operador=apoiador,
            tipo=tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2026, 6, 1),
        )
    assert sessao.query(Aporte).count() == 0


def test_aporte_da_gestao_nao_nasce_ressarcivel(sessao, cenario, criar_valor_de_referencia):
    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo)

    aporte = registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("1"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
    )
    sessao.commit()

    assert aporte.situacao_de_ressarcimento == SituacaoDeRessarcimento.nao_se_aplica
    assert aporte.ressarcivel is False


def test_comprovante_em_pdf_e_aceito(sessao, cenario, criar_valor_de_referencia, tmp_path):
    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo)
    armazenamento = ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))

    aporte = registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("1"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
        comprovante_conteudo=b"conteudo do comprovante",
        comprovante_nome_original="comprovante.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=armazenamento,
    )
    sessao.commit()

    assert aporte.comprovante_referencia is not None
    assert armazenamento.ler(referencia=aporte.comprovante_referencia) == b"conteudo do comprovante"


def test_comprovante_em_formato_nao_previsto_e_recusado(
    sessao, cenario, criar_valor_de_referencia, tmp_path
):
    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo)
    armazenamento = ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_aporte(
            sessao,
            operador=admin,
            provedor=apoiador,
            tipo=tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2026, 6, 1),
            forma=FormaDeAporte.material,
            comprovante_conteudo=b"conteudo",
            comprovante_nome_original="comprovante.txt",
            comprovante_tipo="text/plain",
            armazenamento=armazenamento,
        )
    assert excinfo.value.campo == "comprovante"
    assert sessao.query(Aporte).count() == 0


def test_tipo_que_exige_comprovante_recusa_aporte_sem_ele(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, exige_comprovante=True)
    criar_valor_de_referencia(admin, tipo)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_aporte(
            sessao,
            operador=admin,
            provedor=apoiador,
            tipo=tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2026, 6, 1),
            forma=FormaDeAporte.material,
        )
    assert excinfo.value.campo == "comprovante"
    assert sessao.query(Aporte).count() == 0


def test_aporte_retroativo_com_comprovante(sessao, cenario, criar_valor_de_referencia, tmp_path):
    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(
        admin, tipo, valor_em_moedas=Decimal("1.00"), vigencia_inicio=date(2020, 1, 1)
    )
    armazenamento = ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))

    aporte = registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("1"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2021, 3, 1),
        forma=FormaDeAporte.material,
        periodo_apurado=date(2021, 3, 1),
        comprovante_conteudo=b"conteudo",
        comprovante_nome_original="comprovante.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=armazenamento,
    )
    sessao.commit()

    assert aporte.data_do_aporte == date(2021, 3, 1)
    assert aporte.valor_em_moedas == Decimal("1.00")


def test_aporte_de_tipo_inexistente_aponta_o_cadastro_do_tipo(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_aporte(
            sessao,
            operador=admin,
            provedor=apoiador,
            tipo=None,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2026, 6, 1),
            forma=FormaDeAporte.material,
        )
    assert excinfo.value.campo == "tipo_de_recurso_id"
    assert "tipos-de-recurso" in excinfo.value.mensagem
    assert sessao.query(Aporte).count() == 0


def test_registro_pelo_admin_homologa_e_credita(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))

    solicitacao = registrar_solicitacao_de_participacao(
        sessao,
        nome_ou_razao_social="Apoiadora de Tal",
        email="apoiadora@example.org",
        whatsapp="+55 11 90000-0000",
        pretensao=PretensaoDeParticipacao.apoiador,
        apresentacao="Quero apoiar.",
        aporte_declarado="R$ 100,00 em material.",
    )
    sessao.commit()
    apoiador = criar_persona(Papel.apoiador)

    assert saldo_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    ) == Decimal("0")

    aporte = registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("1"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
        solicitacao_de_participacao=solicitacao,
    )
    sessao.commit()

    assert aporte.origem_do_registro == OrigemDoRegistro.pre_cadastro
    assert aporte.solicitacao_de_participacao_id == solicitacao.id
    assert saldo_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    ) == Decimal("1.00")


def test_mesma_solicitacao_nao_credita_duas_vezes(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo)

    solicitacao = registrar_solicitacao_de_participacao(
        sessao,
        nome_ou_razao_social="Apoiadora de Tal",
        email="apoiadora@example.org",
        whatsapp="+55 11 90000-0000",
        pretensao=PretensaoDeParticipacao.apoiador,
        apresentacao="Quero apoiar.",
    )
    sessao.commit()
    apoiador = criar_persona(Papel.apoiador)

    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("1"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
        solicitacao_de_participacao=solicitacao,
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_aporte(
            sessao,
            operador=admin,
            provedor=apoiador,
            tipo=tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2026, 6, 1),
            forma=FormaDeAporte.material,
            solicitacao_de_participacao=solicitacao,
        )
    assert excinfo.value.campo == "solicitacao_de_participacao_id"
    assert sessao.query(Aporte).count() == 1


def test_aporte_que_fecha_a_falta_confirma_a_aula(
    sessao, cenario, criar_valor_de_referencia, criar_aula, criar_recurso_declarado_da_aula
):
    from nucleo.aulas.modelo import SituacaoDaAula
    from nucleo.comunidades.modelo import ComunidadeVirtual
    from nucleo.reservas.modelo import EstadoDaReserva, Reserva

    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    comunidade = sessao.get(ComunidadeVirtual, ponto_de_apoio.comunidade_virtual_id)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("5.00"))
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()

    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("5"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
    )
    sessao.commit()

    sessao.refresh(aula)
    assert aula.situacao == SituacaoDaAula.confirmada
    reserva = sessao.query(Reserva).filter_by(aula_id=aula.id).one()
    assert reserva.estado == EstadoDaReserva.reservada
    assert reserva.quantidade == Decimal("5.00")


def test_aporte_insuficiente_nao_confirma_nada(
    sessao, cenario, criar_valor_de_referencia, criar_aula, criar_recurso_declarado_da_aula
):
    from nucleo.aulas.modelo import SituacaoDaAula
    from nucleo.comunidades.modelo import ComunidadeVirtual
    from nucleo.reservas.modelo import Reserva

    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    comunidade = sessao.get(ComunidadeVirtual, ponto_de_apoio.comunidade_virtual_id)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("5.00"))
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()

    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("2"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
    )
    sessao.commit()

    sessao.refresh(aula)
    assert aula.situacao == SituacaoDaAula.pendente_de_lastro
    assert sessao.query(Reserva).filter_by(aula_id=aula.id).count() == 0


def test_aporte_em_outro_ponto_de_apoio_nao_confirma_a_aula(
    sessao,
    cenario,
    criar_valor_de_referencia,
    criar_aula,
    criar_recurso_declarado_da_aula,
    criar_ponto_de_apoio,
):
    from nucleo.aulas.modelo import SituacaoDaAula
    from nucleo.comunidades.modelo import ComunidadeVirtual

    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    comunidade = sessao.get(ComunidadeVirtual, ponto_de_apoio.comunidade_virtual_id)
    outro_ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade, nome="Outro Ponto")
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("5.00"))
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()

    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("5"),
        ponto_de_apoio=outro_ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
    )
    sessao.commit()

    sessao.refresh(aula)
    assert aula.situacao == SituacaoDaAula.pendente_de_lastro


def test_aula_de_horario_mais_proximo_e_atendida_primeiro(
    sessao, cenario, criar_valor_de_referencia, criar_aula, criar_recurso_declarado_da_aula
):
    from datetime import UTC, datetime, timedelta

    from nucleo.aulas.modelo import SituacaoDaAula
    from nucleo.comunidades.modelo import ComunidadeVirtual

    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    comunidade = sessao.get(ComunidadeVirtual, ponto_de_apoio.comunidade_virtual_id)
    agora = datetime.now(UTC)

    aula_distante = criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=agora + timedelta(days=5),
        fim_em=agora + timedelta(days=5, hours=1),
    )
    aula_proxima = criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=agora + timedelta(days=1),
        fim_em=agora + timedelta(days=1, hours=1),
    )
    criar_recurso_declarado_da_aula(aula_distante, tipo, quantidade=Decimal("6.00"))
    criar_recurso_declarado_da_aula(aula_proxima, tipo, quantidade=Decimal("6.00"))
    aula_distante.situacao = SituacaoDaAula.pendente_de_lastro
    aula_proxima.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()

    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("6"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
    )
    sessao.commit()

    sessao.refresh(aula_proxima)
    sessao.refresh(aula_distante)
    assert aula_proxima.situacao == SituacaoDaAula.confirmada
    assert aula_distante.situacao == SituacaoDaAula.pendente_de_lastro


def test_absorcao_tambem_confirma_a_aula_pendente(
    sessao, cenario, criar_valor_de_referencia, criar_aula, criar_recurso_declarado_da_aula
):
    from nucleo.aulas.modelo import SituacaoDaAula
    from nucleo.comunidades.modelo import ComunidadeVirtual

    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    comunidade = sessao.get(ComunidadeVirtual, ponto_de_apoio.comunidade_virtual_id)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("5.00"))
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()

    registrar_aporte_por_absorcao(
        sessao,
        operador=admin,
        tipo=tipo,
        quantidade=Decimal("5"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        valor_de_origem=Decimal("50.00"),
    )
    sessao.commit()

    sessao.refresh(aula)
    assert aula.situacao == SituacaoDaAula.confirmada
