from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nucleo.aportes.modelo import FormaDeAporte, SituacaoDeRessarcimento
from nucleo.fila.modelo import (
    PretensaoDeParticipacao,
    SituacaoDaSolicitacao,
    SolicitacaoDeParticipacao,
)
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.personas.modelo import Papel
from nucleo.poder_sustentador.regra import (
    contagem_de_absorcoes_de,
    moedas_acumuladas_de,
    poder_sustentador_de,
)


def test_o_aporte_sobe_o_poder_sustentador_exatamente_no_que_valeu(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("1.50"),
    )
    criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        credito,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("1.50"),
        forma=FormaDeAporte.material,
    )

    assert poder_sustentador_de(sessao, provedor_id=apoiador.id) == Decimal("1.50")


def test_o_ajuste_sobre_o_credito_move_o_poder_sustentador(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("1.50"),
    )
    criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        credito,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("1.50"),
        forma=FormaDeAporte.material,
    )
    criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.ajuste,
        quantidade=Decimal("-1.00"),
        valor_em_moedas=Decimal("-0.50"),
        lancamento_original=credito,
        motivo_do_ajuste="Corrige valor a maior.",
    )

    assert poder_sustentador_de(sessao, provedor_id=apoiador.id) == Decimal("1.00")


def test_a_recontagem_devolve_o_mesmo_numero(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal("7.00"),
        valor_em_moedas=Decimal("7.00"),
    )
    criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        credito,
        quantidade=Decimal("7.00"),
        valor_em_moedas=Decimal("7.00"),
        forma=FormaDeAporte.material,
    )

    primeira = poder_sustentador_de(sessao, provedor_id=apoiador.id)
    segunda = poder_sustentador_de(sessao, provedor_id=apoiador.id)

    assert primeira == segunda == Decimal("7.00")


def test_o_consumo_da_aula_nao_desconta_de_ninguem(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
    criar_aula,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)

    credito = criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal("4.00"),
        valor_em_moedas=Decimal("4.00"),
    )
    criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        credito,
        quantidade=Decimal("4.00"),
        valor_em_moedas=Decimal("4.00"),
        forma=FormaDeAporte.material,
    )
    criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.debito,
        quantidade=Decimal("4.00"),
        valor_em_moedas=Decimal("4.00"),
        aula=aula,
    )

    assert poder_sustentador_de(sessao, provedor_id=apoiador.id) == Decimal("4.00")


def test_provedor_sem_aporte_tem_poder_sustentador_zero(sessao, criar_persona):
    apoiador = criar_persona(Papel.apoiador)

    assert poder_sustentador_de(sessao, provedor_id=apoiador.id) == Decimal("0")


def test_cada_absorcao_conta_uma_vez(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    for _ in range(3):
        credito = criar_lancamento(
            admin, tipo, ponto_de_apoio, natureza=NaturezaDoLancamento.credito
        )
        criar_aporte(admin, mestre, tipo, ponto_de_apoio, credito, forma=FormaDeAporte.absorcao)
    for _ in range(2):
        credito = criar_lancamento(
            admin, tipo, ponto_de_apoio, natureza=NaturezaDoLancamento.credito
        )
        criar_aporte(admin, mestre, tipo, ponto_de_apoio, credito, forma=FormaDeAporte.financeira)

    assert contagem_de_absorcoes_de(sessao, provedor_id=mestre.id) == 3


def test_o_ajuste_no_ledger_nao_apaga_a_absorcao(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal("2.00"),
        valor_em_moedas=Decimal("2.00"),
    )
    criar_aporte(
        admin,
        mestre,
        tipo,
        ponto_de_apoio,
        credito,
        quantidade=Decimal("2.00"),
        valor_em_moedas=Decimal("2.00"),
        forma=FormaDeAporte.absorcao,
    )
    criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.ajuste,
        quantidade=Decimal("-1.00"),
        valor_em_moedas=Decimal("-1.00"),
        lancamento_original=credito,
        motivo_do_ajuste="Corrige valor.",
    )

    assert poder_sustentador_de(sessao, provedor_id=mestre.id) == Decimal("1.00")
    assert contagem_de_absorcoes_de(sessao, provedor_id=mestre.id) == 1


def test_quem_nunca_absorveu_conta_zero(sessao, criar_persona):
    apoiador = criar_persona(Papel.apoiador)

    assert contagem_de_absorcoes_de(sessao, provedor_id=apoiador.id) == 0


def test_moedas_acumuladas_soma_os_aportes_homologados(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    for valor in (Decimal("3.00"), Decimal("5.00")):
        credito = criar_lancamento(
            admin,
            tipo,
            ponto_de_apoio,
            natureza=NaturezaDoLancamento.credito,
            quantidade=valor,
            valor_em_moedas=valor,
        )
        criar_aporte(
            admin,
            apoiador,
            tipo,
            ponto_de_apoio,
            credito,
            quantidade=valor,
            valor_em_moedas=valor,
            forma=FormaDeAporte.financeira,
        )

    assert moedas_acumuladas_de(sessao, provedor_id=apoiador.id) == Decimal("8.00")


def test_moedas_acumuladas_deixa_solicitacao_pendente_fora_da_conta(sessao, criar_persona):
    apoiador = criar_persona(Papel.apoiador)
    # O aporte declarado no pré-cadastro só vira `Aporte` — e só então entra
    # na conta — quando um Admin o homologa; enquanto isso é só a
    # solicitação, fora da tabela que `moedas_acumuladas_de` soma
    # (`RN-14-11`, design — Decisions 1).
    sessao.add(
        SolicitacaoDeParticipacao(
            situacao=SituacaoDaSolicitacao.recebida,
            nome_ou_razao_social=apoiador.nome or "Apoiador",
            email="apoiador@example.com",
            whatsapp="11999999999",
            pretensao=PretensaoDeParticipacao.apoiador,
            apresentacao="Aporte declarado ainda pendente de homologação.",
            aporte_declarado="R$ 100,00",
            prazo=datetime.now(UTC) + timedelta(days=30),
        )
    )
    sessao.commit()

    assert moedas_acumuladas_de(sessao, provedor_id=apoiador.id) == Decimal("0")


def test_moedas_acumuladas_nao_regride_com_ressarcimento_pago(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal("10.00"),
        valor_em_moedas=Decimal("10.00"),
    )
    aporte = criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        credito,
        quantidade=Decimal("10.00"),
        valor_em_moedas=Decimal("10.00"),
        forma=FormaDeAporte.absorcao,
        ressarcivel=True,
        situacao_de_ressarcimento=SituacaoDeRessarcimento.em_aberto,
    )

    # O ressarcimento paga e emite o ajuste de quantidade zero que reverte
    # as moedas do crédito original — é o que derruba o Poder Sustentador
    # sem tocar no acumulado (`ressarcimentos.regra.registrar_ressarcimento`).
    criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.ajuste,
        quantidade=Decimal("0"),
        valor_em_moedas=Decimal("-10.00"),
        lancamento_original=credito,
        motivo_do_ajuste=f"Ressarcimento do aporte {aporte.id}",
    )
    aporte.situacao_de_ressarcimento = SituacaoDeRessarcimento.ressarcido
    sessao.commit()

    assert poder_sustentador_de(sessao, provedor_id=apoiador.id) == Decimal("0")
    assert moedas_acumuladas_de(sessao, provedor_id=apoiador.id) == Decimal("10.00")
