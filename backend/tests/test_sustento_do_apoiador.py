from datetime import date, timedelta
from decimal import Decimal

from nucleo.aportes.modelo import FormaDeAporte, OrigemDaEscolhaDoAporte
from nucleo.aportes.regra import declarar_aporte, registrar_aporte
from nucleo.armazenamento.disco import ArmazenamentoEmDisco
from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.missoes_do_apoiador.modelo import MissaoDoApoiador, NivelDeNecessidade
from nucleo.missoes_do_apoiador.regra import publicar_missao
from nucleo.personas.modelo import Papel
from nucleo.selos_do_apoiador.modelo import FamiliaDeSelo
from nucleo.selos_do_apoiador.regra import derivar_sustento, listar_selos
from nucleo.tempo import agora


def _armazenamento(tmp_path):
    return ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))


def _concluir_missao(
    sessao,
    *,
    admin,
    apoiadores,
    comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_aula,
    criar_recurso_declarado_da_aula,
    tmp_path,
    nivel: NivelDeNecessidade,
    quantidade: Decimal = Decimal("10.00"),
) -> MissaoDoApoiador:
    """Publica uma missão nova, num tipo de recurso e ponto de apoio
    próprios (para não disputar saldo com outra missão do mesmo teste), e a
    conclui com um aporte homologado por participante."""
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, nome=f"Recurso {nivel.value}")
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=quantidade)
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()

    missao = publicar_missao(
        sessao,
        operador=admin,
        aula=aula,
        tipo=tipo,
        nivel_de_necessidade=nivel,
        titulo="Missão de teste",
        o_que_se_pede="O que se pede",
        quantidade=quantidade,
        prazo=agora().date() + timedelta(days=30),
        selo_nome=f"Selo {nivel.value}",
        selo_familia=FamiliaDeSelo.frente,
    )
    sessao.commit()

    parte = (quantidade / len(apoiadores)).quantize(Decimal("0.01"))
    for indice, apoiador in enumerate(apoiadores):
        declaracao = declarar_aporte(
            sessao,
            provedor=apoiador,
            valor_declarado=parte,
            forma=FormaDeAporte.financeira,
            origem_da_escolha=OrigemDaEscolhaDoAporte.missao,
            missao=missao,
            comprovante_conteudo=b"conteudo",
            comprovante_nome_original="comprovante.pdf",
            comprovante_tipo="application/pdf",
            armazenamento=_armazenamento(tmp_path),
        )
        sessao.commit()
        # A última parcela fecha exatamente o restante, absorvendo qualquer
        # sobra do arredondamento.
        eh_ultima = indice == len(apoiadores) - 1
        quantidade_do_aporte = quantidade - parte * (len(apoiadores) - 1) if eh_ultima else parte
        registrar_aporte(
            sessao,
            operador=admin,
            provedor=apoiador,
            tipo=tipo,
            quantidade=quantidade_do_aporte,
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2026, 6, 1),
            forma=FormaDeAporte.financeira,
            aporte_declarado=declaracao,
        )
        sessao.commit()

    sessao.refresh(missao)
    return missao


def test_primeiro_aporte_homologado_abre_nivel_1(
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

    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("1.00"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.financeira,
        valor_de_origem=Decimal("1.00"),
    )
    sessao.commit()

    sustento = derivar_sustento(sessao, apoiador_id=apoiador.id)
    assert sustento.nivel == 1
    assert sustento.nome_do_nivel == "Apoiador"


def test_frentes_diferentes_valem_mais_que_volume(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_aula,
    criar_recurso_declarado_da_aula,
    tmp_path,
):
    admin = criar_persona(Papel.admin)
    apoiador_frentes = criar_persona(Papel.apoiador)
    apoiador_volume = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()

    kwargs = dict(
        admin=admin,
        comunidade=comunidade,
        criar_ponto_de_apoio=criar_ponto_de_apoio,
        criar_tipo_de_recurso=criar_tipo_de_recurso,
        criar_valor_de_referencia=criar_valor_de_referencia,
        criar_aula=criar_aula,
        criar_recurso_declarado_da_aula=criar_recurso_declarado_da_aula,
        tmp_path=tmp_path,
    )
    _concluir_missao(
        sessao, apoiadores=[apoiador_frentes], nivel=NivelDeNecessidade.acontecer, **kwargs
    )
    _concluir_missao(
        sessao, apoiadores=[apoiador_frentes], nivel=NivelDeNecessidade.permanecer, **kwargs
    )
    _concluir_missao(
        sessao,
        apoiadores=[apoiador_volume],
        nivel=NivelDeNecessidade.acontecer,
        quantidade=Decimal("1000.00"),
        **kwargs,
    )
    _concluir_missao(
        sessao,
        apoiadores=[apoiador_volume],
        nivel=NivelDeNecessidade.acontecer,
        quantidade=Decimal("1000.00"),
        **kwargs,
    )

    assert derivar_sustento(sessao, apoiador_id=apoiador_frentes.id).nivel == 3
    assert derivar_sustento(sessao, apoiador_id=apoiador_volume.id).nivel == 2


def test_escada_para_no_nivel_4(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_aula,
    criar_recurso_declarado_da_aula,
    tmp_path,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    kwargs = dict(
        sessao=sessao,
        admin=admin,
        apoiadores=[apoiador],
        comunidade=comunidade,
        criar_ponto_de_apoio=criar_ponto_de_apoio,
        criar_tipo_de_recurso=criar_tipo_de_recurso,
        criar_valor_de_referencia=criar_valor_de_referencia,
        criar_aula=criar_aula,
        criar_recurso_declarado_da_aula=criar_recurso_declarado_da_aula,
        tmp_path=tmp_path,
    )
    _concluir_missao(nivel=NivelDeNecessidade.existir, **kwargs)
    _concluir_missao(nivel=NivelDeNecessidade.acontecer, **kwargs)
    _concluir_missao(nivel=NivelDeNecessidade.permanecer, **kwargs)

    sustento = derivar_sustento(sessao, apoiador_id=apoiador.id)
    assert sustento.nivel == 4
    assert sustento.frente_que_falta == "Vire Mestre."


def test_nivel_nao_regride_com_missao_aberta_nova(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_aula,
    criar_recurso_declarado_da_aula,
    tmp_path,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    kwargs = dict(
        sessao=sessao,
        admin=admin,
        apoiadores=[apoiador],
        comunidade=comunidade,
        criar_ponto_de_apoio=criar_ponto_de_apoio,
        criar_tipo_de_recurso=criar_tipo_de_recurso,
        criar_valor_de_referencia=criar_valor_de_referencia,
        criar_aula=criar_aula,
        criar_recurso_declarado_da_aula=criar_recurso_declarado_da_aula,
        tmp_path=tmp_path,
    )
    _concluir_missao(nivel=NivelDeNecessidade.acontecer, **kwargs)
    assert derivar_sustento(sessao, apoiador_id=apoiador.id).nivel == 2

    # Uma missão nova, ainda aberta (não concluída), não muda o nível — só o
    # concluído conta, e o já alcançado não regride (RN-14-36).
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, nome="Outro recurso")
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("5.00"))
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()
    publicar_missao(
        sessao,
        operador=admin,
        aula=aula,
        tipo=tipo,
        nivel_de_necessidade=NivelDeNecessidade.permanecer,
        titulo="Ainda aberta",
        o_que_se_pede="O que se pede",
        quantidade=Decimal("5.00"),
        prazo=agora().date() + timedelta(days=30),
        selo_nome="Selo ainda não conquistado",
        selo_familia=FamiliaDeSelo.frente,
    )
    sessao.commit()

    assert derivar_sustento(sessao, apoiador_id=apoiador.id).nivel == 2


def test_selos_agrupados_por_familia(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_aula,
    criar_recurso_declarado_da_aula,
    tmp_path,
):
    admin = criar_persona(Papel.admin)
    apoiador_um = criar_persona(Papel.apoiador)
    apoiador_dois = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()

    _concluir_missao(
        sessao,
        admin=admin,
        apoiadores=[apoiador_um, apoiador_dois],
        comunidade=comunidade,
        criar_ponto_de_apoio=criar_ponto_de_apoio,
        criar_tipo_de_recurso=criar_tipo_de_recurso,
        criar_valor_de_referencia=criar_valor_de_referencia,
        criar_aula=criar_aula,
        criar_recurso_declarado_da_aula=criar_recurso_declarado_da_aula,
        tmp_path=tmp_path,
        nivel=NivelDeNecessidade.acontecer,
    )

    selos = listar_selos(sessao, apoiador_id=apoiador_um.id)

    assert set(selos.keys()) == {FamiliaDeSelo.frente, FamiliaDeSelo.ato}
    assert selos[FamiliaDeSelo.ato][0].selo_nome == "Mutirão"


def test_rota_nega_sustento_a_quem_nao_e_apoiador(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/eu/apoiador/sustento",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
