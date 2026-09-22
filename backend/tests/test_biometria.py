from datetime import UTC, datetime

import pytest
from sqlalchemy import event, text
from sqlalchemy.exc import DBAPIError

from nucleo.biometria.cifra import cifrar_descritor, decifrar_descritor
from nucleo.biometria.modelo import AcessoAoTemplate, DesfechoDoAcesso, NaturezaDoAcesso
from nucleo.biometria.regra import (
    DIMENSAO_DO_DESCRITOR,
    TIPO_DE_CONSENTIMENTO_BIOMETRIA,
    _limiar_fora_do_encontro,
    autenticar_por_nick_e_descritor,
    gravar_ou_recadastrar_template,
)
from nucleo.comunidades.modelo import VinculoJogador
from nucleo.configuracao import Configuracao
from nucleo.erros import AcessoAoTemplateImutavel, ErroDeValidacao
from nucleo.personas.modelo import Credencial, Papel, TipoDeCredencial
from tests.conftest import descritor_de_teste

DESCRITOR = descritor_de_teste()


def _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreira_de_teste"):
    guerreiro = criar_persona(Papel.guerreiro)
    criar_nick(guerreiro, nick)
    return guerreiro


class TestCifra:
    def test_decifra_recupera_o_descritor_original(self, configuracao):
        segredo = cifrar_descritor(DESCRITOR, configuracao)
        assert decifrar_descritor(segredo, configuracao) == DESCRITOR

    def test_segredo_cifrado_nao_contem_o_descritor_em_claro(self, configuracao):
        segredo = cifrar_descritor(DESCRITOR, configuracao)
        assert "0.1" not in segredo
        assert "0.2" not in segredo


class TestGravacaoDoTemplate:
    def test_sem_consentimento_nao_grava(self, sessao, configuracao, criar_persona, criar_nick):
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick)
        mestre = criar_persona(Papel.mestre)

        with pytest.raises(ErroDeValidacao):
            gravar_ou_recadastrar_template(
                sessao, configuracao, guerreiro=guerreiro, descritor=DESCRITOR, operado_por=mestre
            )
        assert sessao.query(Credencial).filter_by(tipo=TipoDeCredencial.biometria).count() == 0

    def test_consentimento_revogado_bloqueia_gravacao(
        self, sessao, configuracao, criar_persona, criar_nick, conceder_consentimento_biometrico
    ):
        from nucleo.consentimentos.modelo import DecisaoDeConsentimento

        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick)
        mestre = criar_persona(Papel.mestre)
        admin = criar_persona(Papel.admin)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        conceder_consentimento_biometrico(
            responsavel, guerreiro, decisao=DecisaoDeConsentimento.concede
        )
        conceder_consentimento_biometrico(
            responsavel, guerreiro, decisao=DecisaoDeConsentimento.nega
        )

        with pytest.raises(ErroDeValidacao):
            gravar_ou_recadastrar_template(
                sessao, configuracao, guerreiro=guerreiro, descritor=DESCRITOR, operado_por=mestre
            )

    def test_com_consentimento_grava_cifrado_e_audita(
        self, sessao, configuracao, criar_persona, criar_nick, conceder_consentimento_biometrico
    ):
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick)
        mestre = criar_persona(Papel.mestre)
        admin = criar_persona(Papel.admin)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        conceder_consentimento_biometrico(responsavel, guerreiro)

        credencial = gravar_ou_recadastrar_template(
            sessao, configuracao, guerreiro=guerreiro, descritor=DESCRITOR, operado_por=mestre
        )
        sessao.commit()

        assert credencial.tipo == TipoDeCredencial.biometria
        assert credencial.ativa is True
        assert decifrar_descritor(credencial.segredo, configuracao) == DESCRITOR

        acesso = sessao.query(AcessoAoTemplate).filter_by(guerreiro_id=guerreiro.id).one()
        assert acesso.natureza == NaturezaDoAcesso.gravacao
        assert acesso.desfecho == DesfechoDoAcesso.sucesso
        assert acesso.acessado_por == mestre.id

    def test_recadastro_substitui_o_template_anterior(
        self, sessao, configuracao, criar_persona, criar_nick, conceder_consentimento_biometrico
    ):
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick)
        mestre = criar_persona(Papel.mestre)
        admin = criar_persona(Papel.admin)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        conceder_consentimento_biometrico(responsavel, guerreiro)

        primeira = gravar_ou_recadastrar_template(
            sessao, configuracao, guerreiro=guerreiro, descritor=DESCRITOR, operado_por=mestre
        )
        sessao.commit()

        segundo_descritor = descritor_de_teste(0.9)
        segunda = gravar_ou_recadastrar_template(
            sessao,
            configuracao,
            guerreiro=guerreiro,
            descritor=segundo_descritor,
            operado_por=mestre,
        )
        sessao.commit()

        sessao.refresh(primeira)
        assert primeira.ativa is False
        assert segunda.ativa is True
        assert segunda.id != primeira.id

        acessos = (
            sessao.query(AcessoAoTemplate)
            .filter_by(guerreiro_id=guerreiro.id)
            .order_by(AcessoAoTemplate.momento)
            .all()
        )
        assert [acesso.natureza for acesso in acessos] == [
            NaturezaDoAcesso.gravacao,
            NaturezaDoAcesso.recadastro,
        ]

    def test_dimensao_incorreta_e_recusada(
        self, sessao, configuracao, criar_persona, criar_nick, conceder_consentimento_biometrico
    ):
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick)
        mestre = criar_persona(Papel.mestre)
        admin = criar_persona(Papel.admin)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        conceder_consentimento_biometrico(responsavel, guerreiro)

        with pytest.raises(ErroDeValidacao) as excinfo:
            gravar_ou_recadastrar_template(
                sessao,
                configuracao,
                guerreiro=guerreiro,
                descritor=[0.1, 0.2],
                operado_por=mestre,
            )
        assert excinfo.value.campo == "descritor"

    def test_dimensao_da_biblioteca_e_aceita(
        self, sessao, configuracao, criar_persona, criar_nick, conceder_consentimento_biometrico
    ):
        """A dimensão que o aparelho gera é a que o núcleo aceita, em todo
        ambiente: é constante, não variável de implantação (`RF-01-05`,
        decisão do fundador, 2026-09-17)."""
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreira_dimensao")
        mestre = criar_persona(Papel.mestre)
        admin = criar_persona(Papel.admin)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        conceder_consentimento_biometrico(responsavel, guerreiro)

        credencial = gravar_ou_recadastrar_template(
            sessao,
            configuracao,
            guerreiro=guerreiro,
            descritor=descritor_de_teste(),
            operado_por=mestre,
        )
        sessao.commit()

        assert credencial.ativa is True
        assert len(decifrar_descritor(credencial.segredo, configuracao)) == DIMENSAO_DO_DESCRITOR

    def test_dimensao_e_recusada_antes_do_consentimento(
        self, sessao, configuracao, criar_persona, criar_nick
    ):
        """Sem consentimento E com dimensão errada, quem recusa é a dimensão:
        a ordem importa porque foi ela que fez um erro de dimensão chegar ao
        Mestre como recusa de consentimento (`RF-01-05`, `RF-01-07`)."""
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreiro_sem_termo")
        mestre = criar_persona(Papel.mestre)

        with pytest.raises(ErroDeValidacao) as excinfo:
            gravar_ou_recadastrar_template(
                sessao,
                configuracao,
                guerreiro=guerreiro,
                descritor=[0.1, 0.2],
                operado_por=mestre,
            )
        assert excinfo.value.campo == "descritor"
        assert "consentimento" not in str(excinfo.value.mensagem).lower()

    def test_nenhuma_variavel_de_ambiente_fixa_a_dimensao(self):
        """A dimensão saiu da `Configuracao` e virou constante: o ambiente não
        a declara mais (`RN-01-15`, decisão do fundador, 2026-09-17)."""
        assert "biometria_dimensao_do_descritor" not in Configuracao.model_fields


class TestAutenticacaoPorNickEDescritor:
    def test_nick_e_descritor_conferem(
        self,
        sessao,
        configuracao,
        criar_persona,
        criar_nick,
        criar_template_biometrico,
        montar_cenario_de_entrada,
    ):
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreiro_ok")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)
        cenario = montar_cenario_de_entrada(guerreiro)

        resultado = autenticar_por_nick_e_descritor(
            sessao, configuracao, nick="Guerreiro_ok", descritor=DESCRITOR, aula=cenario.aula
        )
        assert resultado is not None
        assert resultado.id == guerreiro.id

    def test_nick_inexistente_nao_confere(self, sessao, configuracao, montar_cenario_de_entrada):
        cenario = montar_cenario_de_entrada()
        resultado = autenticar_por_nick_e_descritor(
            sessao, configuracao, nick="ninguem", descritor=DESCRITOR, aula=cenario.aula
        )
        assert resultado is None
        assert sessao.query(AcessoAoTemplate).count() == 0

    def test_guerreiro_sem_template_nao_confere(
        self, sessao, configuracao, criar_persona, criar_nick, montar_cenario_de_entrada
    ):
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Sem_template")
        cenario = montar_cenario_de_entrada(guerreiro)

        resultado = autenticar_por_nick_e_descritor(
            sessao, configuracao, nick="Sem_template", descritor=DESCRITOR, aula=cenario.aula
        )
        assert resultado is None

    def test_descritor_que_nao_confere_e_recusado_e_audita_recusa(
        self,
        sessao,
        configuracao,
        criar_persona,
        criar_nick,
        criar_template_biometrico,
        montar_cenario_de_entrada,
    ):
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreiro_recusa")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)
        cenario = montar_cenario_de_entrada(guerreiro)

        resultado = autenticar_por_nick_e_descritor(
            sessao,
            configuracao,
            nick="Guerreiro_recusa",
            descritor=descritor_de_teste(9.0),
            aula=cenario.aula,
        )
        assert resultado is None

        acesso = sessao.query(AcessoAoTemplate).filter_by(guerreiro_id=guerreiro.id).one()
        assert acesso.natureza == NaturezaDoAcesso.comparacao_de_login
        assert acesso.desfecho == DesfechoDoAcesso.recusa

    def test_comparacao_de_login_com_sucesso_audita_sucesso(
        self,
        sessao,
        configuracao,
        criar_persona,
        criar_nick,
        criar_template_biometrico,
        montar_cenario_de_entrada,
    ):
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreiro_confere")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)
        cenario = montar_cenario_de_entrada(guerreiro)

        autenticar_por_nick_e_descritor(
            sessao, configuracao, nick="Guerreiro_confere", descritor=DESCRITOR, aula=cenario.aula
        )

        acesso = sessao.query(AcessoAoTemplate).filter_by(guerreiro_id=guerreiro.id).one()
        assert acesso.natureza == NaturezaDoAcesso.comparacao_de_login
        assert acesso.desfecho == DesfechoDoAcesso.sucesso
        assert acesso.acessado_por is None

    # `RF-01-73`, `RN-01-56`: as duas causas novas da recusa, e o limiar que
    # passa a vir do ponto de apoio da aula.
    def test_ponto_de_apoio_sem_limiar_medido_nao_reconhece_ninguem(
        self,
        sessao,
        configuracao,
        criar_persona,
        criar_nick,
        criar_template_biometrico,
        montar_cenario_de_entrada,
    ):
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreiro_sem_limiar")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)
        cenario = montar_cenario_de_entrada(guerreiro, limiar=None)

        resultado = autenticar_por_nick_e_descritor(
            sessao,
            configuracao,
            nick="Guerreiro_sem_limiar",
            descritor=DESCRITOR,
            aula=cenario.aula,
        )
        assert resultado is None

        acesso = sessao.query(AcessoAoTemplate).filter_by(guerreiro_id=guerreiro.id).one()
        assert acesso.desfecho == DesfechoDoAcesso.recusa

    def test_aula_de_outra_comunidade_nao_alcanca_o_limiar_dela(
        self,
        sessao,
        configuracao,
        criar_persona,
        criar_nick,
        criar_template_biometrico,
        montar_cenario_de_entrada,
    ):
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreiro_de_outra")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)
        montar_cenario_de_entrada(guerreiro)
        alheio = montar_cenario_de_entrada()

        resultado = autenticar_por_nick_e_descritor(
            sessao,
            configuracao,
            nick="Guerreiro_de_outra",
            descritor=DESCRITOR,
            aula=alheio.aula,
        )
        assert resultado is None

    def test_aula_nao_vigente_nao_alcanca_limiar(
        self,
        sessao,
        configuracao,
        criar_persona,
        criar_nick,
        criar_template_biometrico,
        montar_cenario_de_entrada,
    ):
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreiro_fora_de_hora")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)
        cenario = montar_cenario_de_entrada(guerreiro, vigente=False)

        resultado = autenticar_por_nick_e_descritor(
            sessao,
            configuracao,
            nick="Guerreiro_fora_de_hora",
            descritor=DESCRITOR,
            aula=cenario.aula,
        )
        assert resultado is None

    def test_cada_ponto_de_apoio_compara_com_o_proprio_limiar(
        self,
        sessao,
        configuracao,
        criar_persona,
        criar_nick,
        criar_template_biometrico,
        montar_cenario_de_entrada,
    ):
        """Dois limiares diferentes, o mesmo par de descritores: confere num
        ponto de apoio e não no outro (`RF-01-73`)."""
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreiro_dois_pontos")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)
        # `descritor_de_teste` põe o mesmo valor em todas as posições: a
        # distância entre 0.1 e 0.3 é `sqrt(1024) * 0.2`, ou seja 6.4.
        distante = descritor_de_teste(0.3)
        folgado = montar_cenario_de_entrada(guerreiro, limiar=8.0)
        apertado = montar_cenario_de_entrada(guerreiro, limiar=1.0, comunidade=folgado.comunidade)

        assert (
            autenticar_por_nick_e_descritor(
                sessao,
                configuracao,
                nick="Guerreiro_dois_pontos",
                descritor=distante,
                aula=folgado.aula,
            )
            is not None
        )
        assert (
            autenticar_por_nick_e_descritor(
                sessao,
                configuracao,
                nick="Guerreiro_dois_pontos",
                descritor=distante,
                aula=apertado.aula,
            )
            is None
        )


class TestImutabilidadeDoAcessoAoTemplate:
    def test_acesso_gravado_nao_e_editado_nem_apagado_no_orm(self, sessao, criar_persona):
        guerreiro = criar_persona(Papel.guerreiro)
        acesso = AcessoAoTemplate(
            guerreiro_id=guerreiro.id,
            acessado_por=None,
            natureza=NaturezaDoAcesso.comparacao_de_login,
            desfecho=DesfechoDoAcesso.sucesso,
        )
        sessao.add(acesso)
        sessao.commit()

        acesso.desfecho = DesfechoDoAcesso.recusa
        with pytest.raises(AcessoAoTemplateImutavel):
            sessao.commit()
        sessao.rollback()

        sessao.delete(sessao.get(AcessoAoTemplate, acesso.id))
        with pytest.raises(AcessoAoTemplateImutavel):
            sessao.commit()
        sessao.rollback()

        assert sessao.get(AcessoAoTemplate, acesso.id) is not None

    def test_update_e_delete_sao_recusados_direto_no_banco(self, conexao, sessao, criar_persona):
        guerreiro = criar_persona(Papel.guerreiro)
        acesso = AcessoAoTemplate(
            guerreiro_id=guerreiro.id,
            acessado_por=None,
            natureza=NaturezaDoAcesso.comparacao_de_login,
            desfecho=DesfechoDoAcesso.sucesso,
        )
        sessao.add(acesso)
        sessao.commit()

        with pytest.raises(DBAPIError), conexao.begin_nested():
            conexao.execute(
                text("UPDATE acesso_ao_template SET desfecho = 'recusa' WHERE id = :id"),
                {"id": str(acesso.id)},
            )

        with pytest.raises(DBAPIError), conexao.begin_nested():
            conexao.execute(
                text("DELETE FROM acesso_ao_template WHERE id = :id"), {"id": str(acesso.id)}
            )

        assert sessao.get(AcessoAoTemplate, acesso.id) is not None


def test_tipo_de_consentimento_biometrico_e_string_estavel():
    """Regressão: se este valor mudar, `consultar_consentimento_vigente_em`
    passa a não achar o consentimento gravado com o valor antigo. O valor é
    `biometria`, um dos dois do conjunto fechado que `TipoDeConsentimento`
    define (`RN-13-06`)."""
    assert TIPO_DE_CONSENTIMENTO_BIOMETRIA == "biometria"


class TestLimiarDaComunidadeForaDoEncontro:
    """`RN-01-57`: fora do encontro não há aula nem ponto de apoio, e o limiar
    vem da comunidade do vínculo vigente do Guerreiro(a)."""

    @staticmethod
    def _contar_consultas(sessao, executar):
        """Conta as idas ao banco de uma comparação. É a medida do que a
        indistinguibilidade do `RN-01-22` protege: um número que caísse quando
        o nick não existe, ou que crescesse com o tamanho da comunidade,
        deixaria sondar nick pelo relógio."""
        consultas = []
        conexao = sessao.connection()

        def _registrar(*_args, **_kwargs):
            consultas.append(1)

        event.listen(conexao.engine, "before_cursor_execute", _registrar)
        try:
            executar()
        finally:
            event.remove(conexao.engine, "before_cursor_execute", _registrar)
        return len(consultas)

    def test_a_resolucao_do_limiar_custa_o_mesmo_em_toda_causa(
        self,
        sessao,
        criar_persona,
        criar_comunidade,
        criar_ponto_de_apoio,
        criar_medicao_do_limiar,
    ):
        """`RN-01-57`, `RN-01-22`: resolver o limiar de fora do encontro custa
        **duas** consultas, exista o Guerreiro(a) ou não, tenha ele vínculo ou
        não, tenha a comunidade medição ou não.

        É o que a minha parte deste caminho pode garantir. O número **total**
        de consultas da comparação ainda difere entre nick que existe e nick
        que não existe, porque a leitura da persona, a da credencial e o
        registro de auditoria não acontecem para quem não existe — assimetria
        anterior a esta fatia, e que a auditoria torna inevitável: não há linha
        de acesso a gravar para um Guerreiro(a) que não há.
        """
        admin = criar_persona(Papel.admin)
        comunidade_medida = criar_comunidade(nome="Medida")
        ponto = criar_ponto_de_apoio(admin, comunidade_medida)
        criar_medicao_do_limiar(ponto, admin, limiar=8.0)

        com_limiar = criar_persona(Papel.guerreiro, comunidade=comunidade_medida)
        sem_medicao = criar_persona(Papel.guerreiro, comunidade=criar_comunidade(nome="Crua"))
        sem_vinculo = criar_persona(Papel.guerreiro)
        sessao.query(VinculoJogador).filter_by(
            guerreiro_id=sem_vinculo.id, data_fim=None
        ).one().data_fim = datetime.now(UTC)
        sessao.commit()

        contagens = [
            self._contar_consultas(sessao, lambda g=guerreiro: _limiar_fora_do_encontro(sessao, g))
            for guerreiro in (com_limiar, sem_medicao, sem_vinculo, None)
        ]

        assert contagens == [2, 2, 2, 2], contagens

    def test_o_numero_de_consultas_nao_separa_as_causas_entre_nicks_que_existem(
        self,
        sessao,
        configuracao,
        criar_persona,
        criar_nick,
        criar_comunidade,
        criar_template_biometrico,
    ):
        """`RN-01-58`, `RN-01-22`: vínculo encerrado e comunidade sem medição
        custam o mesmo, de ponta a ponta."""
        comunidade = criar_comunidade()
        sem_medicao = criar_persona(Papel.guerreiro, comunidade=comunidade)
        criar_nick(sem_medicao, "Sem_medicao")
        criar_template_biometrico(sem_medicao, DESCRITOR)

        sem_vinculo = criar_persona(Papel.guerreiro)
        sessao.query(VinculoJogador).filter_by(
            guerreiro_id=sem_vinculo.id, data_fim=None
        ).one().data_fim = datetime.now(UTC)
        sessao.commit()
        criar_nick(sem_vinculo, "Sem_vinculo")
        criar_template_biometrico(sem_vinculo, DESCRITOR)

        contagens = [
            self._contar_consultas(
                sessao,
                lambda nick=nick: autenticar_por_nick_e_descritor(
                    sessao, configuracao, nick=nick, descritor=DESCRITOR, aula=None
                ),
            )
            for nick in ("Sem_medicao", "Sem_vinculo")
        ]

        assert contagens[0] == contagens[1], contagens

    def test_o_numero_de_consultas_nao_cresce_com_a_comunidade(
        self,
        sessao,
        configuracao,
        criar_persona,
        criar_nick,
        criar_comunidade,
        criar_template_biometrico,
        criar_ponto_de_apoio,
        criar_medicao_do_limiar,
    ):
        """`RN-01-57`: resolver o mais frouxo é **uma** ida ao banco, tenha a
        comunidade um ponto de apoio ou cinco."""
        admin = criar_persona(Papel.admin)
        magra = criar_comunidade(nome="Magra")
        gorda = criar_comunidade(nome="Gorda")
        for comunidade, quantos in ((magra, 1), (gorda, 5)):
            for indice in range(quantos):
                ponto = criar_ponto_de_apoio(admin, comunidade, nome=f"Ponto {indice}")
                criar_medicao_do_limiar(ponto, admin, limiar=8.0)

        contagens = []
        for comunidade, nick in ((magra, "Da_magra"), (gorda, "Da_gorda")):
            guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
            criar_nick(guerreiro, nick)
            criar_template_biometrico(guerreiro, descritor_de_teste(9.0))
            contagens.append(
                self._contar_consultas(
                    sessao,
                    lambda nick=nick: autenticar_por_nick_e_descritor(
                        sessao, configuracao, nick=nick, descritor=DESCRITOR, aula=None
                    ),
                )
            )

        assert contagens[0] == contagens[1], contagens
