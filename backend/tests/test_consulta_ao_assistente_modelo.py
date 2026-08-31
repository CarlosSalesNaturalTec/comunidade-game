"""A entidade `ConsultaAoAssistente` — `RF-04-36`, `RF-04-40`, design —
decisão 6."""

import pytest
from sqlalchemy.exc import IntegrityError

from nucleo.assistente.modelo import ConsultaAoAssistente, DesfechoDaConsulta, TipoDeAssistente
from nucleo.personas.modelo import Papel


def test_consulta_com_equipe_e_sem_guerreiro_e_aceita(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_equipe
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    equipe = criar_equipe(guerreiro, aula=aula)

    consulta = ConsultaAoAssistente(
        equipe_id=equipe.id,
        guerreiro_id=None,
        assistente=TipoDeAssistente.trilhas,
        desfecho=DesfechoDaConsulta.respondida,
        pergunta="O que é uma variável?",
        resposta="É um espaço na memória para guardar um valor.",
        autor_id=guerreiro.id,
        papel_do_autor=guerreiro.papel.value,
    )
    sessao.add(consulta)
    sessao.flush()
    assert consulta.id is not None


def test_consulta_com_os_dois_vinculos_e_recusada_pelo_banco(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_equipe
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    equipe = criar_equipe(guerreiro, aula=aula)

    consulta = ConsultaAoAssistente(
        equipe_id=equipe.id,
        guerreiro_id=guerreiro.id,
        assistente=TipoDeAssistente.trilhas,
        desfecho=DesfechoDaConsulta.respondida,
        pergunta="Pergunta qualquer",
        resposta="Resposta qualquer",
        autor_id=guerreiro.id,
        papel_do_autor=guerreiro.papel.value,
    )
    sessao.add(consulta)
    with pytest.raises(IntegrityError):
        sessao.flush()
    sessao.rollback()


def test_consulta_sem_nenhum_vinculo_e_recusada_pelo_banco(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)

    consulta = ConsultaAoAssistente(
        equipe_id=None,
        guerreiro_id=None,
        assistente=TipoDeAssistente.trilhas,
        desfecho=DesfechoDaConsulta.respondida,
        pergunta="Pergunta qualquer",
        resposta="Resposta qualquer",
        autor_id=guerreiro.id,
        papel_do_autor=guerreiro.papel.value,
    )
    sessao.add(consulta)
    with pytest.raises(IntegrityError):
        sessao.flush()
    sessao.rollback()
