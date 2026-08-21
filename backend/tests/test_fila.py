from datetime import timedelta

import pytest
from sqlalchemy import select

from nucleo.armazenamento.disco import ArmazenamentoEmDisco
from nucleo.erros import ConjuntoDeDadosNaoLiberado, DocumentoPessoalRecusado, ErroDeValidacao
from nucleo.fila.modelo import (
    PretensaoDeParticipacao,
    SituacaoDaSolicitacao,
    SituacaoDaSugestao,
    SolicitacaoDeParticipacao,
    TipoDeAlvo,
)
from nucleo.fila.regra import (
    PRAZO_DE_AVALIACAO,
    PRAZO_DE_DESCARTE_DA_TRANSCRICAO_NAO_ADOTADA,
    avaliar_solicitacao_de_chave,
    avaliar_solicitacao_de_dados,
    avaliar_solicitacao_de_participacao,
    avaliar_sugestao,
    contem_documento_pessoal,
    esta_em_atraso,
    liberar_conjunto_de_dados,
    registrar_solicitacao_de_chave,
    registrar_solicitacao_de_dados,
    registrar_solicitacao_de_participacao,
    registrar_sugestao,
)
from nucleo.personas.modelo import Nick, Papel, Persona
from nucleo.personas.regra import conferir_disponibilidade_de_nick
from nucleo.personas.regra import criar_persona as criar_persona_do_nucleo
from nucleo.ponto_extra.modelo import PontoExtra
from nucleo.pontuacao.modelo import Badge, TipoDeBadge
from nucleo.tempo import agora


def test_solicitacao_de_participacao_nasce_recebida_com_prazo_de_sete_dias(sessao):
    solicitacao = registrar_solicitacao_de_participacao(
        sessao,
        nome_ou_razao_social="Fulana de Tal",
        email="fulana@example.org",
        whatsapp="+55 11 90000-0000",
        pretensao=PretensaoDeParticipacao.mestre,
        apresentacao="Quero ser Mestre na comunidade.",
    )
    sessao.commit()

    assert solicitacao.situacao == SituacaoDaSolicitacao.recebida
    diferenca = solicitacao.prazo - solicitacao.registrado_em
    assert abs(diferenca - PRAZO_DE_AVALIACAO) < timedelta(seconds=5)


def test_registro_nao_cria_persona_nem_credencial(sessao):
    registrar_solicitacao_de_participacao(
        sessao,
        nome_ou_razao_social="Fulana de Tal",
        email="fulana@example.org",
        whatsapp="+55 11 90000-0000",
        pretensao=PretensaoDeParticipacao.mestre,
        apresentacao="Quero ser Mestre na comunidade.",
    )
    sessao.commit()

    assert sessao.query(Persona).count() == 0


def test_aprovacao_da_solicitacao_de_participacao_nao_cria_persona(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    solicitacao = registrar_solicitacao_de_participacao(
        sessao,
        nome_ou_razao_social="Fulana de Tal",
        email="fulana@example.org",
        whatsapp="+55 11 90000-0000",
        pretensao=PretensaoDeParticipacao.mestre,
        apresentacao="Quero ser Mestre na comunidade.",
    )
    sessao.commit()
    total_de_personas_antes = sessao.query(Persona).count()

    avaliada = avaliar_solicitacao_de_participacao(
        sessao,
        solicitacao,
        situacao=SituacaoDaSolicitacao.aceita,
        avaliado_por=admin,
        parecer="Perfil compatível com a proposta.",
    )
    sessao.commit()

    assert avaliada.situacao == SituacaoDaSolicitacao.aceita
    assert avaliada.avaliado_por_id == admin.id
    assert avaliada.decidido_em is not None
    assert sessao.query(Persona).count() == total_de_personas_antes


@pytest.mark.parametrize(
    "campo_com_documento",
    [
        "CPF 529.982.247-25",
        "meu CNPJ é 11.222.333/0001-81",
        "RG 12.345.678-9",
    ],
)
def test_documento_pessoal_e_recusado(sessao, campo_com_documento):
    with pytest.raises(DocumentoPessoalRecusado):
        registrar_solicitacao_de_participacao(
            sessao,
            nome_ou_razao_social="Fulana de Tal",
            email="fulana@example.org",
            whatsapp="+55 11 90000-0000",
            pretensao=PretensaoDeParticipacao.mestre,
            apresentacao=campo_com_documento,
        )
    assert sessao.query(SolicitacaoDeParticipacao).count() == 0


def test_texto_livre_sem_documento_e_aceito(sessao):
    solicitacao = registrar_solicitacao_de_participacao(
        sessao,
        nome_ou_razao_social="Fulana de Tal",
        email="fulana@example.org",
        whatsapp="+55 11 90000-0000",
        pretensao=PretensaoDeParticipacao.mestre,
        apresentacao="Trabalho na área há 12345 anos, código 987.654 do meu projeto.",
    )
    sessao.commit()
    assert solicitacao.id is not None


def test_contem_documento_pessoal_ignora_numero_qualquer_sem_digito_verificador():
    assert not contem_documento_pessoal("Telefone 123.456.789-00")


def test_comprovante_vai_para_a_porta_de_armazenamento_e_linha_guarda_so_a_referencia(
    sessao, tmp_path
):
    porta = ArmazenamentoEmDisco(str(tmp_path))
    conteudo = b"comprovante em bytes"

    solicitacao = registrar_solicitacao_de_participacao(
        sessao,
        nome_ou_razao_social="Apoiadora de Tal",
        email="apoiadora@example.org",
        whatsapp="+55 11 90000-0000",
        pretensao=PretensaoDeParticipacao.apoiador,
        apresentacao="Quero apoiar a comunidade.",
        aporte_declarado="R$ 500,00 em material escolar",
        comprovante_conteudo=conteudo,
        comprovante_nome_original="comprovante.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=porta,
    )
    sessao.commit()

    assert solicitacao.comprovante_referencia is not None
    assert solicitacao.comprovante_nome_original == "comprovante.pdf"
    assert solicitacao.comprovante_tipo == "application/pdf"
    assert solicitacao.comprovante_tamanho == len(conteudo)
    assert porta.ler(referencia=solicitacao.comprovante_referencia) == conteudo

    # A linha nunca guarda os bytes — só a referência (`RN-01-28`).
    linha = sessao.execute(
        select(SolicitacaoDeParticipacao).where(SolicitacaoDeParticipacao.id == solicitacao.id)
    ).scalar_one()
    for coluna in SolicitacaoDeParticipacao.__table__.columns:
        assert coluna.name != "comprovante_conteudo"
    assert linha.comprovante_referencia == solicitacao.comprovante_referencia


def test_comprovante_fora_da_pretensao_apoiador_e_recusado(sessao, tmp_path):
    porta = ArmazenamentoEmDisco(str(tmp_path))
    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_solicitacao_de_participacao(
            sessao,
            nome_ou_razao_social="Fulano de Tal",
            email="fulano@example.org",
            whatsapp="+55 11 90000-0000",
            pretensao=PretensaoDeParticipacao.mestre,
            apresentacao="Quero ser Mestre.",
            comprovante_conteudo=b"bytes",
            armazenamento=porta,
        )
    assert excinfo.value.campo == "comprovante"


def test_nick_gravado_no_pre_cadastro_sem_criar_persona(sessao):
    solicitacao = registrar_solicitacao_de_participacao(
        sessao,
        nome_ou_razao_social="Apoiadora de Tal",
        email="apoiadora@example.org",
        whatsapp="+55 11 90000-0000",
        pretensao=PretensaoDeParticipacao.apoiador,
        apresentacao="Quero apoiar a comunidade.",
        nick="ApoiadoraPretendida",
    )
    sessao.commit()

    assert solicitacao.nick == "ApoiadoraPretendida"
    assert sessao.query(Persona).count() == 0
    assert sessao.query(Nick).filter_by(valor="ApoiadoraPretendida").first() is None


def test_nick_de_adulto_em_uso_e_recusado_no_pre_cadastro(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    criar_persona_do_nucleo(sessao, papel=Papel.apoiador, criada_por=admin, nick="JaEmUso")
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_solicitacao_de_participacao(
            sessao,
            nome_ou_razao_social="Outra Apoiadora",
            email="outra@example.org",
            whatsapp="+55 11 90000-0000",
            pretensao=PretensaoDeParticipacao.apoiador,
            apresentacao="Quero apoiar a comunidade.",
            nick="JaEmUso",
        )
    assert excinfo.value.campo == "nick"
    assert sessao.query(SolicitacaoDeParticipacao).count() == 0


def test_nick_declarado_em_solicitacao_de_mestre_e_recusado(sessao):
    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_solicitacao_de_participacao(
            sessao,
            nome_ou_razao_social="Fulana de Tal",
            email="fulana@example.org",
            whatsapp="+55 11 90000-0000",
            pretensao=PretensaoDeParticipacao.mestre,
            apresentacao="Quero ser Mestre na comunidade.",
            nick="NickDeMestre",
        )
    assert excinfo.value.campo == "nick"
    assert sessao.query(SolicitacaoDeParticipacao).count() == 0


def test_nick_reservado_sai_como_indisponivel_na_conferencia(sessao):
    registrar_solicitacao_de_participacao(
        sessao,
        nome_ou_razao_social="Apoiadora de Tal",
        email="apoiadora@example.org",
        whatsapp="+55 11 90000-0000",
        pretensao=PretensaoDeParticipacao.apoiador,
        apresentacao="Quero apoiar a comunidade.",
        nick="NickReservado",
    )
    sessao.commit()

    assert conferir_disponibilidade_de_nick(sessao, "NickReservado") is False


def test_segunda_solicitacao_com_o_mesmo_nick_e_recusada(sessao):
    primeira = registrar_solicitacao_de_participacao(
        sessao,
        nome_ou_razao_social="Apoiadora de Tal",
        email="apoiadora@example.org",
        whatsapp="+55 11 90000-0000",
        pretensao=PretensaoDeParticipacao.apoiador,
        apresentacao="Quero apoiar a comunidade.",
        nick="NickDisputado",
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_solicitacao_de_participacao(
            sessao,
            nome_ou_razao_social="Outra Apoiadora",
            email="outra@example.org",
            whatsapp="+55 11 90000-0000",
            pretensao=PretensaoDeParticipacao.apoiador,
            apresentacao="Quero apoiar a comunidade também.",
            nick="NickDisputado",
        )
    assert excinfo.value.campo == "nick"
    assert sessao.query(SolicitacaoDeParticipacao).count() == 1
    assert primeira.nick == "NickDisputado"


def test_reserva_vencida_libera_o_nick(sessao):
    solicitacao = registrar_solicitacao_de_participacao(
        sessao,
        nome_ou_razao_social="Apoiadora de Tal",
        email="apoiadora@example.org",
        whatsapp="+55 11 90000-0000",
        pretensao=PretensaoDeParticipacao.apoiador,
        apresentacao="Quero apoiar a comunidade.",
        nick="NickAVencer",
    )
    solicitacao.prazo = agora() - timedelta(seconds=1)
    sessao.commit()

    assert conferir_disponibilidade_de_nick(sessao, "NickAVencer") is True
    assert solicitacao.situacao == SituacaoDaSolicitacao.recebida


def test_solicitacao_recusada_libera_o_nick(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    solicitacao = registrar_solicitacao_de_participacao(
        sessao,
        nome_ou_razao_social="Apoiadora de Tal",
        email="apoiadora@example.org",
        whatsapp="+55 11 90000-0000",
        pretensao=PretensaoDeParticipacao.apoiador,
        apresentacao="Quero apoiar a comunidade.",
        nick="NickARecusar",
    )
    sessao.commit()

    avaliar_solicitacao_de_participacao(
        sessao,
        solicitacao,
        situacao=SituacaoDaSolicitacao.recusada,
        avaliado_por=admin,
        parecer="Perfil incompatível com a proposta.",
    )
    sessao.commit()

    assert conferir_disponibilidade_de_nick(sessao, "NickARecusar") is True


def test_reserva_nao_impede_o_cadastro_de_um_guerreiro_com_o_mesmo_nick(
    sessao, criar_comunidade, criar_aula, criar_persona
):
    registrar_solicitacao_de_participacao(
        sessao,
        nome_ou_razao_social="Apoiadora de Tal",
        email="apoiadora@example.org",
        whatsapp="+55 11 90000-0000",
        pretensao=PretensaoDeParticipacao.apoiador,
        apresentacao="Quero apoiar a comunidade.",
        nick="NickCobicado",
    )
    sessao.commit()

    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    guerreiro = criar_persona_do_nucleo(
        sessao, papel=Papel.guerreiro, criada_por=None, aula=aula, nick="NickCobicado"
    )
    sessao.commit()

    assert guerreiro.papel == Papel.guerreiro
    assert sessao.query(Nick).filter_by(valor="NickCobicado").one().persona_id == guerreiro.id


def test_solicitacao_de_dados_sem_finalidade_e_recusada(sessao):
    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_solicitacao_de_dados(
            sessao,
            solicitante="Pesquisadora de Tal",
            instituicao="Universidade de Teste",
            email="pesquisadora@example.org",
            finalidade_declarada="   ",
            recorte_pedido="Comunidade de Teste, 2026",
        )
    assert excinfo.value.campo == "finalidade_declarada"


def test_conjunto_de_dados_nao_sai_sem_aprovacao_registrada(sessao):
    solicitacao = registrar_solicitacao_de_dados(
        sessao,
        solicitante="Pesquisadora de Tal",
        instituicao="Universidade de Teste",
        email="pesquisadora@example.org",
        finalidade_declarada="Pesquisa acadêmica sobre evasão escolar.",
        recorte_pedido="Comunidade de Teste, 2026",
    )
    sessao.commit()

    with pytest.raises(ConjuntoDeDadosNaoLiberado):
        liberar_conjunto_de_dados(solicitacao)


def test_aprovacao_da_solicitacao_de_dados_exige_compromisso_de_nao_reidentificar(
    sessao, criar_persona
):
    admin = criar_persona(Papel.admin)
    solicitacao = registrar_solicitacao_de_dados(
        sessao,
        solicitante="Pesquisadora de Tal",
        instituicao="Universidade de Teste",
        email="pesquisadora@example.org",
        finalidade_declarada="Pesquisa acadêmica sobre evasão escolar.",
        recorte_pedido="Comunidade de Teste, 2026",
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        avaliar_solicitacao_de_dados(
            sessao,
            solicitacao,
            situacao=SituacaoDaSolicitacao.aceita,
            avaliado_por=admin,
            parecer="Finalidade compatível com política pública.",
        )
    assert excinfo.value.campo == "compromisso_de_nao_reidentificar"


def test_solicitacao_de_dados_aprovada_libera_o_conjunto(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    solicitacao = registrar_solicitacao_de_dados(
        sessao,
        solicitante="Pesquisadora de Tal",
        instituicao="Universidade de Teste",
        email="pesquisadora@example.org",
        finalidade_declarada="Pesquisa acadêmica sobre evasão escolar.",
        recorte_pedido="Comunidade de Teste, 2026",
    )
    sessao.commit()

    avaliar_solicitacao_de_dados(
        sessao,
        solicitacao,
        situacao=SituacaoDaSolicitacao.aceita,
        avaliado_por=admin,
        parecer="Finalidade compatível com política pública.",
        compromisso_de_nao_reidentificar=True,
    )
    sessao.commit()

    liberar_conjunto_de_dados(solicitacao)  # não levanta


def test_recusa_da_solicitacao_de_dados_grava_motivo_autor_e_data(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    solicitacao = registrar_solicitacao_de_dados(
        sessao,
        solicitante="Pesquisadora de Tal",
        instituicao="Universidade de Teste",
        email="pesquisadora@example.org",
        finalidade_declarada="Recorte incompatível com pesquisa.",
        recorte_pedido="Dados individuais identificáveis",
    )
    sessao.commit()

    avaliada = avaliar_solicitacao_de_dados(
        sessao,
        solicitacao,
        situacao=SituacaoDaSolicitacao.recusada,
        avaliado_por=admin,
        parecer="Recorte pedido permite reidentificação.",
    )
    sessao.commit()

    assert avaliada.situacao == SituacaoDaSolicitacao.recusada
    assert avaliada.parecer == "Recorte pedido permite reidentificação."
    assert avaliada.avaliado_por_id == admin.id
    assert avaliada.decidido_em is not None


def test_solicitacao_de_chave_nao_emite_chave_no_registro(sessao):
    solicitacao = registrar_solicitacao_de_chave(
        sessao,
        solicitante="Desenvolvedora de Tal",
        contato="dev@example.org",
        o_que_pretende_construir="Um painel comunitário.",
    )
    sessao.commit()

    assert solicitacao.situacao == SituacaoDaSolicitacao.recebida
    assert solicitacao.prazo is not None


def test_avaliacao_de_solicitacao_de_chave_nao_cria_persona_nem_emite_chave(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    solicitacao = registrar_solicitacao_de_chave(
        sessao,
        solicitante="Desenvolvedora de Tal",
        contato="dev@example.org",
        o_que_pretende_construir="Um painel comunitário.",
    )
    sessao.commit()
    total_de_personas_antes = sessao.query(Persona).count()

    avaliada = avaliar_solicitacao_de_chave(
        sessao,
        solicitacao,
        situacao=SituacaoDaSolicitacao.aceita,
        avaliado_por=admin,
        parecer="Aprovado.",
    )
    sessao.commit()

    assert avaliada.situacao == SituacaoDaSolicitacao.aceita
    assert sessao.query(Persona).count() == total_de_personas_antes
    assert avaliada.chave_id is None


def test_sugestao_registrada_guarda_autor_persona_e_alvo(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)

    sugestao = registrar_sugestao(
        sessao,
        autor=guerreiro,
        alvo_tipo=TipoDeAlvo.plataforma,
        texto="Podíamos ter um mural de recados entre as trilhas.",
    )
    sessao.commit()

    assert sugestao.autor_id == guerreiro.id
    assert sugestao.papel_do_autor == Papel.guerreiro.value
    assert sugestao.alvo_tipo == TipoDeAlvo.plataforma
    assert sugestao.texto == "Podíamos ter um mural de recados entre as trilhas."
    assert sugestao.situacao == SituacaoDaSugestao.recebida


def test_sugestao_de_atividade_ou_trilha_exige_alvo_id(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_sugestao(
            sessao,
            autor=guerreiro,
            alvo_tipo=TipoDeAlvo.trilha,
            texto="Sugestão sobre uma trilha específica.",
        )
    assert excinfo.value.campo == "alvo_id"


def test_registrar_sugestao_nao_credita_ponto_algum(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)

    registrar_sugestao(
        sessao,
        autor=guerreiro,
        alvo_tipo=TipoDeAlvo.plataforma,
        texto="Sugestão qualquer.",
    )
    sessao.commit()

    assert sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).first() is None
    assert (
        sessao.query(Badge)
        .filter_by(guerreiro_id=guerreiro.id, tipo=TipoDeBadge.de_protagonismo)
        .first()
        is None
    )


def test_sugestao_adotada_credita_vinte_extras_e_o_badge_sem_ponto_regular(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    sugestao = registrar_sugestao(
        sessao, autor=guerreiro, alvo_tipo=TipoDeAlvo.plataforma, texto="Proposta de evolução."
    )
    sessao.commit()

    avaliar_sugestao(
        sessao,
        sugestao,
        situacao=SituacaoDaSugestao.adotada,
        avaliado_por=admin,
        parecer="Ótima ideia, vamos adotar.",
    )
    sessao.commit()

    conta_extra = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).one()
    assert conta_extra.acumulado == 20
    assert conta_extra.saldo_disponivel == 20

    badge = (
        sessao.query(Badge)
        .filter_by(guerreiro_id=guerreiro.id, tipo=TipoDeBadge.de_protagonismo)
        .one()
    )
    assert badge.trilha_id is None
    assert badge.poder_id is None

    assert sugestao.creditado_em is not None


def test_sugestao_nao_adotada_nao_credita_nada_e_grava_motivo_e_descarte(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    sugestao = registrar_sugestao(
        sessao, autor=guerreiro, alvo_tipo=TipoDeAlvo.plataforma, texto="Proposta de evolução."
    )
    sessao.commit()

    avaliar_sugestao(
        sessao,
        sugestao,
        situacao=SituacaoDaSugestao.nao_adotada,
        avaliado_por=admin,
        parecer="Já existe recurso equivalente.",
        motivo_do_retorno="Já temos algo parecido — obrigado pela ideia!",
    )
    sessao.commit()

    assert sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).first() is None
    assert (
        sessao.query(Badge)
        .filter_by(guerreiro_id=guerreiro.id, tipo=TipoDeBadge.de_protagonismo)
        .first()
        is None
    )
    assert sugestao.motivo_do_retorno == "Já temos algo parecido — obrigado pela ideia!"
    assert (
        sugestao.descartar_em == sugestao.decidido_em + PRAZO_DE_DESCARTE_DA_TRANSCRICAO_NAO_ADOTADA
    )


def test_sugestao_nao_adotada_sem_motivo_e_recusada(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    sugestao = registrar_sugestao(
        sessao, autor=guerreiro, alvo_tipo=TipoDeAlvo.plataforma, texto="Proposta de evolução."
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        avaliar_sugestao(
            sessao,
            sugestao,
            situacao=SituacaoDaSugestao.nao_adotada,
            avaliado_por=admin,
        )
    assert excinfo.value.campo == "motivo_do_retorno"


def test_regravar_adotada_nao_credita_duas_vezes(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    sugestao = registrar_sugestao(
        sessao, autor=guerreiro, alvo_tipo=TipoDeAlvo.plataforma, texto="Proposta de evolução."
    )
    sessao.commit()

    avaliar_sugestao(
        sessao, sugestao, situacao=SituacaoDaSugestao.adotada, avaliado_por=admin, parecer="Ok."
    )
    sessao.commit()
    avaliar_sugestao(
        sessao,
        sugestao,
        situacao=SituacaoDaSugestao.adotada,
        avaliado_por=admin,
        parecer="Reavaliação.",
    )
    sessao.commit()

    conta_extra = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).one()
    assert conta_extra.acumulado == 20
    assert conta_extra.saldo_disponivel == 20
    assert (
        sessao.query(Badge)
        .filter_by(guerreiro_id=guerreiro.id, tipo=TipoDeBadge.de_protagonismo)
        .count()
        == 1
    )


def test_segunda_sugestao_adotada_do_mesmo_autor_nao_repete_o_badge(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    primeira = registrar_sugestao(
        sessao, autor=guerreiro, alvo_tipo=TipoDeAlvo.plataforma, texto="Primeira proposta."
    )
    segunda = registrar_sugestao(
        sessao, autor=guerreiro, alvo_tipo=TipoDeAlvo.plataforma, texto="Segunda proposta."
    )
    sessao.commit()

    avaliar_sugestao(
        sessao, primeira, situacao=SituacaoDaSugestao.adotada, avaliado_por=admin, parecer="Ok."
    )
    sessao.commit()
    avaliar_sugestao(
        sessao, segunda, situacao=SituacaoDaSugestao.adotada, avaliado_por=admin, parecer="Ok."
    )
    sessao.commit()

    conta_extra = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).one()
    assert conta_extra.acumulado == 40
    assert (
        sessao.query(Badge)
        .filter_by(guerreiro_id=guerreiro.id, tipo=TipoDeBadge.de_protagonismo)
        .count()
        == 1
    )


def test_prazo_vencido_sem_desfecho_esta_em_atraso_e_permanece_aberta(sessao):
    solicitacao = registrar_solicitacao_de_chave(
        sessao,
        solicitante="Desenvolvedora de Tal",
        contato="dev@example.org",
        o_que_pretende_construir="Um painel comunitário.",
    )
    solicitacao.prazo = agora() - timedelta(seconds=1)
    sessao.commit()

    assert esta_em_atraso(solicitacao)
    assert solicitacao.situacao == SituacaoDaSolicitacao.recebida


def test_prazo_ainda_correndo_nao_esta_em_atraso(sessao):
    solicitacao = registrar_solicitacao_de_chave(
        sessao,
        solicitante="Desenvolvedora de Tal",
        contato="dev@example.org",
        o_que_pretende_construir="Um painel comunitário.",
    )
    sessao.commit()

    assert not esta_em_atraso(solicitacao)


def test_solicitacao_com_desfecho_nunca_esta_em_atraso_mesmo_apos_o_prazo(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    solicitacao = registrar_solicitacao_de_chave(
        sessao,
        solicitante="Desenvolvedora de Tal",
        contato="dev@example.org",
        o_que_pretende_construir="Um painel comunitário.",
    )
    solicitacao.prazo = agora() - timedelta(seconds=1)
    avaliar_solicitacao_de_chave(
        sessao, solicitacao, situacao=SituacaoDaSolicitacao.aceita, avaliado_por=admin
    )
    sessao.commit()

    assert not esta_em_atraso(solicitacao)
