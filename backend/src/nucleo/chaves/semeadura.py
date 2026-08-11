from sqlalchemy.orm import Session

from ..configuracao import Ambiente
from .modelo import ChaveDeAplicacao, NaturezaDaChave, SituacaoDaChave
from .segredo import calcular_resumo, gerar_segredo, montar_chave_completa

# As oito aplicações do projeto (documento 03 §1.2) — nenhuma outra é semeada aqui.
APLICACOES_DO_PROJETO = (
    "app-01-aula-presencial",
    "app-03-gestao",
    "app-04-arena",
    "app-05-guerreiro",
    "app-06-vitrine",
    "app-07-responsaveis",
    "app-08-apoiador",
    "app-09-mestre",
)


def semear_ambiente(sessao: Session, ambiente: Ambiente) -> dict[str, str]:
    """Converge para uma chave vigente por aplicação do projeto no ambiente dado.

    Aplicação já semeada não é tocada: não reemite, não duplica e não reimprime
    segredo (RN-01-35). Devolve o segredo em claro só das chaves recém-criadas.
    """
    segredos_emitidos: dict[str, str] = {}

    for aplicacao in APLICACOES_DO_PROJETO:
        ja_existe = (
            sessao.query(ChaveDeAplicacao)
            .filter_by(aplicacao=aplicacao, ambiente=ambiente, situacao=SituacaoDaChave.vigente)
            .first()
        )
        if ja_existe is not None:
            continue

        chave = ChaveDeAplicacao(
            aplicacao=aplicacao,
            ambiente=ambiente,
            natureza=NaturezaDaChave.do_projeto,
            resumo_do_segredo="",
        )
        sessao.add(chave)
        sessao.flush()

        segredo = gerar_segredo()
        chave.resumo_do_segredo = calcular_resumo(segredo)
        segredos_emitidos[aplicacao] = montar_chave_completa(ambiente, str(chave.id), segredo)

    sessao.commit()
    return segredos_emitidos
