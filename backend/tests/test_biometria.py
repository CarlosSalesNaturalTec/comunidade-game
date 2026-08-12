import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from nucleo.biometria.cifra import cifrar_descritor, decifrar_descritor
from nucleo.biometria.modelo import AcessoAoTemplate, DesfechoDoAcesso, NaturezaDoAcesso
from nucleo.biometria.regra import (
    TIPO_DE_CONSENTIMENTO_BIOMETRIA,
    autenticar_por_nick_e_descritor,
    gravar_ou_recadastrar_template,
)
from nucleo.erros import AcessoAoTemplateImutavel, ErroDeValidacao
from nucleo.personas.modelo import Credencial, Papel, TipoDeCredencial

DESCRITOR = [0.1, 0.2, 0.3, 0.4]


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

        segundo_descritor = [0.9, 0.8, 0.7, 0.6]
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


class TestAutenticacaoPorNickEDescritor:
    def test_nick_e_descritor_conferem(
        self, sessao, configuracao, criar_persona, criar_nick, criar_template_biometrico
    ):
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreiro_ok")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)

        resultado = autenticar_por_nick_e_descritor(
            sessao, configuracao, nick="Guerreiro_ok", descritor=DESCRITOR
        )
        assert resultado is not None
        assert resultado.id == guerreiro.id

    def test_nick_inexistente_nao_confere(self, sessao, configuracao):
        resultado = autenticar_por_nick_e_descritor(
            sessao, configuracao, nick="ninguem", descritor=DESCRITOR
        )
        assert resultado is None
        assert sessao.query(AcessoAoTemplate).count() == 0

    def test_guerreiro_sem_template_nao_confere(
        self, sessao, configuracao, criar_persona, criar_nick
    ):
        _guerreiro_com_nick(criar_persona, criar_nick, nick="Sem_template")

        resultado = autenticar_por_nick_e_descritor(
            sessao, configuracao, nick="Sem_template", descritor=DESCRITOR
        )
        assert resultado is None

    def test_descritor_que_nao_confere_e_recusado_e_audita_recusa(
        self, sessao, configuracao, criar_persona, criar_nick, criar_template_biometrico
    ):
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreiro_recusa")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)

        resultado = autenticar_por_nick_e_descritor(
            sessao, configuracao, nick="Guerreiro_recusa", descritor=[9.0, 9.0, 9.0, 9.0]
        )
        assert resultado is None

        acesso = sessao.query(AcessoAoTemplate).filter_by(guerreiro_id=guerreiro.id).one()
        assert acesso.natureza == NaturezaDoAcesso.comparacao_de_login
        assert acesso.desfecho == DesfechoDoAcesso.recusa

    def test_comparacao_de_login_com_sucesso_audita_sucesso(
        self, sessao, configuracao, criar_persona, criar_nick, criar_template_biometrico
    ):
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreiro_confere")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)

        autenticar_por_nick_e_descritor(
            sessao, configuracao, nick="Guerreiro_confere", descritor=DESCRITOR
        )

        acesso = sessao.query(AcessoAoTemplate).filter_by(guerreiro_id=guerreiro.id).one()
        assert acesso.natureza == NaturezaDoAcesso.comparacao_de_login
        assert acesso.desfecho == DesfechoDoAcesso.sucesso
        assert acesso.acessado_por is None


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

    def test_update_e_delete_sao_recusados_direto_no_banco(self, engine, sessao, criar_persona):
        guerreiro = criar_persona(Papel.guerreiro)
        acesso = AcessoAoTemplate(
            guerreiro_id=guerreiro.id,
            acessado_por=None,
            natureza=NaturezaDoAcesso.comparacao_de_login,
            desfecho=DesfechoDoAcesso.sucesso,
        )
        sessao.add(acesso)
        sessao.commit()

        with engine.connect() as conexao, pytest.raises(DBAPIError):
            conexao.execute(
                text("UPDATE acesso_ao_template SET desfecho = 'recusa' WHERE id = :id"),
                {"id": str(acesso.id)},
            )
            conexao.commit()

        with engine.connect() as conexao, pytest.raises(DBAPIError):
            conexao.execute(
                text("DELETE FROM acesso_ao_template WHERE id = :id"), {"id": str(acesso.id)}
            )
            conexao.commit()

        assert sessao.get(AcessoAoTemplate, acesso.id) is not None


def test_tipo_de_consentimento_biometrico_e_string_estavel():
    """Regressão: se este valor mudar, `consultar_consentimento_vigente_em`
    passa a não achar o consentimento gravado com o valor antigo."""
    assert TIPO_DE_CONSENTIMENTO_BIOMETRIA == "captura_biometrica"
