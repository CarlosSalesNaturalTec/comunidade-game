from sqlalchemy.orm import Session

from .modelo import ConteudoInstitucional, SecaoInstitucional
from .regra import publicar_secao

# Chave PIX e titular decididos no documento 04 §1 ("Doações em espécie —
# canal oficial"), publicados em "Como apoiar" (`RF-03-46`). É texto da
# seção: o Admin o edita por `PUT`, e a aplicação não escreve valor nenhum.
TEXTO_DE_COMO_APOIAR = (
    "Doações em dinheiro são feitas por PIX, em nome da pessoa jurídica vinculada ao "
    "projeto.\n\n"
    "Chave PIX (CNPJ): 51.730.395/0001-19\n"
    "Titular: Robô Educa — Kits Robóticos Educacionais\n\n"
    "Toda doação recebida é registrada no livro-razão da plataforma."
)

# RASCUNHO da nota de transparência sobre IA e do bloco "Licenças", dentro de
# "Quem somos" (`RF-03-48`, documento 01 §7, documento 03 §§1.12 e 8). O texto
# final é do fundador (PRD-03 §14); o Admin o troca por `PUT` sem nova
# implantação. O que vale para o gerado com auxílio de IA não está decidido em
# nenhum documento, e o rascunho não o afirma (design — Open Questions).
TEXTO_DE_QUEM_SOMOS = (
    "## Nota de transparência sobre IA\n\n"
    "A Comunidade Game usa inteligência artificial e diz isso às claras.\n\n"
    "Para construir a plataforma — o código e os documentos —, usamos os modelos Claude 5 e "
    "Sonnet 5, da Anthropic.\n\n"
    "Para atender as pessoas na tela — Guerreiros, Guerreiras, Mestres e Apoiadores —, usamos "
    "modelos de terceiros: hoje o Gemini, do Google, e o DeepSeek. Quem constrói não é quem "
    "responde a uma criança.\n\n"
    "A IA reescreve o conteúdo que o Mestre cadastrou, para a criança entender melhor, dentro "
    "da conversa do momento. Ela não faz perfil da criança: nada é adivinhado nem guardado "
    "sobre quem ela é. O texto reescrito por IA leva uma etiqueta visível, com link para esta "
    "nota.\n\n"
    "A voz que lê as telas em voz alta é a do próprio navegador. Ela lê texto da plataforma, "
    "nunca o nome de uma criança.\n\n"
    "Sobre o que é gerado com auxílio de IA, veja o bloco Licenças, logo abaixo.\n\n"
    "## Licenças\n\n"
    "O código da plataforma é aberto, sob a licença AGPL. O conteúdo educacional publicado, com "
    "crédito ao Mestre autor, e o conjunto de dados entregue a pesquisadores e gestores, com "
    "crédito à comunidade que o produziu, saem sob a licença CC BY-SA: quem usa pode adaptar, "
    "creditando, e o derivado herda a mesma licença."
)

SEMENTES: dict[SecaoInstitucional, str] = {
    SecaoInstitucional.quem_somos: TEXTO_DE_QUEM_SOMOS,
    SecaoInstitucional.como_apoiar: TEXTO_DE_COMO_APOIAR,
}


def semear_conteudo_institucional(sessao: Session) -> list[SecaoInstitucional]:
    """Converge as duas seções que a documentação já decidiu, **só onde a
    seção ainda não tem texto**: repetir nunca sobrescreve uma publicação.
    "Contatos" fica vazio — nenhum documento traz os contatos. Devolve as
    seções semeadas nesta chamada."""
    semeadas: list[SecaoInstitucional] = []
    for secao, texto in SEMENTES.items():
        linha = sessao.get(ConteudoInstitucional, secao)
        if linha is not None and linha.texto:
            continue
        publicar_secao(sessao, secao, texto=texto, video_url=None, autor_id=None)
        semeadas.append(secao)
    sessao.commit()
    return semeadas
