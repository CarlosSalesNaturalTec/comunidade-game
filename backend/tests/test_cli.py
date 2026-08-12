from nucleo.banco import Base
from nucleo.chaves.modelo import ChaveDeAplicacao
from nucleo.chaves.semeadura import APLICACOES_DO_PROJETO
from nucleo.cli import semear
from nucleo.personas.modelo import Credencial, Papel, Persona


def test_semear_converge_chaves_e_admin_fundador(monkeypatch, engine, configuracao, capsys):
    from sqlalchemy.orm import sessionmaker

    monkeypatch.setattr("nucleo.cli.obter_configuracao", lambda: configuracao)
    fabrica = sessionmaker(bind=engine, expire_on_commit=False)
    monkeypatch.setattr("nucleo.cli.obter_fabrica_de_sessao", lambda: fabrica)

    try:
        semear()

        with fabrica() as sessao:
            chaves = sessao.query(ChaveDeAplicacao).count()
            assert chaves == len(APLICACOES_DO_PROJETO)

            admin = (
                sessao.query(Persona)
                .filter_by(papel=Papel.admin)
                .join(Credencial, Credencial.persona_id == Persona.id)
                .filter(Credencial.identificador == configuracao.identidade_fundador)
                .one()
            )
            assert admin.criada_por is None

        saida = capsys.readouterr().out
        assert "Persona Admin do fundador semeada" in saida

        semear()
        saida_segunda = capsys.readouterr().out
        assert "já existia" in saida_segunda
        assert "já está semeado" in saida_segunda

        with fabrica() as sessao:
            assert sessao.query(Persona).filter_by(papel=Papel.admin).count() == 1
    finally:
        with engine.begin() as conexao:
            for tabela in reversed(Base.metadata.sorted_tables):
                conexao.execute(tabela.delete())
