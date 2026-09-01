from sqlalchemy.orm import Session

from ..configuracao import Configuracao
from ..consentimentos.modelo import TipoDeConsentimento
from ..tempo import agora
from .modelo import Termo

# Texto aprovado pelo fundador em 2026-09-01 (proposal.md — "Decisões novas
# do fundador"), semeado na versão que `Configuracao.consentimento_versao_
# vigente_do_termo` já carimba (`RF-13-34`, `RN-13-19`, design — Migration
# Plan). A redação completa do termo de autorização única e do termo
# biométrico segue pendente de revisão jurídica (documento 09 §1, linha
# "Redação dos termos") — trocá-la é semear versão nova, sem tocar em
# registro já gravado.
TEXTO_DO_TERMO_2026_08 = (
    "Autorização única de divulgação\n\n"
    "Ao conceder esta autorização, você permite que a Comunidade Game mostre publicamente "
    "o avatar e o apelido do(a) Guerreiro(a), e que a evolução dele — pontos, poderes, "
    "badges e criações originais — apareça na vitrine da plataforma. A imagem real, o nome "
    "civil e qualquer dado de contato nunca são mostrados. Você pode revogar esta "
    "autorização a qualquer momento; a revogação vale a partir do registro dela, sem "
    "apagar o que já foi publicado.\n\n"
    "Entrega dos dados a pesquisadores e gestores públicos\n\n"
    "Os dados produzidos pela participação do(a) Guerreiro(a) na Comunidade Game podem ser "
    "entregues, de graça, a pesquisadores e a gestores públicos que peçam o conjunto "
    "completo da plataforma. Essa entrega sai sempre anonimizada — sem nome, sem apelido e "
    "sem qualquer vínculo com quem produziu o dado. Cada pedido é aprovado, um a um, por "
    "um Admin: quem pede se identifica, declara para que vai usar o dado e assume o "
    "compromisso de não tentar descobrir de quem ele é. A resposta ao pedido sai em até 7 "
    "dias. O pedido, a resposta do Admin e o que foi entregue ficam registrados. Quem "
    "recebe o conjunto de dados precisa creditar a Comunidade Game, e qualquer trabalho "
    "feito a partir dele segue sob a mesma licença Creative Commons CC BY-SA. Esta é uma "
    "declaração de transparência sobre como os dados são usados — não é uma decisão "
    "separada, e não há como recusar só essa parte."
)


def semear_termo_vigente(sessao: Session, configuracao: Configuracao) -> Termo | None:
    """Converge para um `Termo` de `autorizacao_de_divulgacao` na versão
    vigente da configuração. Versão já semeada não é tocada — idempotente,
    no mesmo padrão de `chaves.semeadura.semear_ambiente` (design —
    Migration Plan)."""
    versao = configuracao.consentimento_versao_vigente_do_termo
    ja_existe = (
        sessao.query(Termo)
        .filter_by(tipo=TipoDeConsentimento.autorizacao_de_divulgacao, versao=versao)
        .first()
    )
    if ja_existe is not None:
        return None

    termo = Termo(
        tipo=TipoDeConsentimento.autorizacao_de_divulgacao,
        versao=versao,
        texto=TEXTO_DO_TERMO_2026_08,
        vigente_desde=agora(),
    )
    sessao.add(termo)
    sessao.commit()
    return termo
