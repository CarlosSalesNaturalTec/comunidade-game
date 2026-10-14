from sqlalchemy.orm import Session

from .modelo import ConteudoInstitucional, SecaoInstitucional
from .regra import publicar_secao

# Os três textos institucionais decididos pelo fundador em 2026-10-14, com a
# redação aprovada no `design.md` da change. São texto da seção: o Admin os
# troca por `PUT` sem nova implantação, e a aplicação não escreve valor nenhum.
# A semeadura não alcança banco já semeado — em produção quem publica é o Admin.

# Chave PIX e titular decididos no documento 04 §1 ("Doações em espécie —
# canal oficial"), publicados em "Como apoiar" (`RF-03-46`). O comprovante e a
# regra do recibo vêm do mesmo §1; o endereço, do documento 03 §8.
TEXTO_DE_COMO_APOIAR = (
    "Doações em dinheiro são feitas por PIX, em nome da pessoa jurídica vinculada ao "
    "projeto.\n\n"
    "Chave PIX (CNPJ): 51.730.395/0001-19\n"
    "Titular: Robô Educa — Kits Robóticos Educacionais\n\n"
    "Depois de transferir, anexe o comprovante no pré-cadastro: a plataforma não confirma "
    "PIX automaticamente — quem confere é um Admin. Não pedimos CPF, CNPJ nem documento de "
    "identidade de quem doa.\n\n"
    "Toda doação recebida é registrada no livro-razão da plataforma e compõe o seu Poder "
    "Sustentador, visível em público em moedas.\n\n"
    "A plataforma não emite recibo. Quem precisar de um escreve para "
    "comunidadegameorg@gmail.com informando os dados fiscais, e a pessoa jurídica vinculada "
    "o emite — é o que permite comprovar a doação sem a plataforma guardar dado fiscal de "
    "ninguém."
)

# Canal único do projeto e os caminhos de cada público, em "Contatos"
# (`RF-03-45`, documento 03 §8). O endereço sai como texto, sem link: a
# marcação do institucional não tem link. Nenhum canal alcança um Guerreiro(a)
# — documento 99 §6, invariante 10.
TEXTO_DE_CONTATOS = (
    "Aqui estão os caminhos para falar com o projeto. Cada um leva a uma porta diferente, e "
    "escolher a certa economiza o seu tempo e o nosso.\n\n"
    "Nenhum destes canais alcança um Guerreiro ou uma Guerreira. Toda interação entre adulto "
    "e criança é mediada pela plataforma, e nisso não há exceção.\n\n"
    "## Quero apoiar\n\n"
    "Dinheiro, equipamento, insumo, alimento, serviço, conteúdo, código, divulgação — ou "
    "vontade de ensinar. Comece pela chamada “Quero apoiar”, presente em toda página desta "
    "vitrine: ela pergunta o que você traz e encaminha. Quem vai transferir dinheiro faz o "
    "pré-cadastro na Área do Apoiador; as outras formas passam pelo formulário da vitrine. "
    "As duas portas caem na mesma fila de avaliação de um Admin.\n\n"
    "## Quero ensinar\n\n"
    "Mestre é cadastrado por um Admin, com habilidade comprovada por trabalho publicado e "
    "verificável — portfólio, código, videoaulas, currículo. O primeiro passo é o formulário "
    "de participação desta vitrine.\n\n"
    "## Pesquisa e gestão pública\n\n"
    "O conjunto completo de dados do território é gratuito, sai anonimizado e licenciado em "
    "CC BY-SA, e depende de solicitação prévia aprovada por um Admin, respondida em até 7 "
    "dias. O caminho é o formulário de solicitação de dados desta vitrine, com solicitante, "
    "instituição, e-mail e finalidade declarada. Os recortes de pesquisadores e de gestores "
    "públicos mostram o que se mede, com que cadência e desde quando.\n\n"
    "## Construir sobre a plataforma\n\n"
    "O código é aberto e a API pública pode ser consumida por outra aplicação. A seção "
    "“Construir sobre a API” explica como solicitar a chave de aplicação, emitida por um "
    "Admin, e traz o assistente que responde dúvidas de integração.\n\n"
    "## Responsáveis por um Guerreiro ou Guerreira\n\n"
    "O caminho mais curto é a gestão, no encontro presencial. O acompanhamento, a autorização "
    "de divulgação e o desligamento da personalização por IA ficam na Área dos "
    "Responsáveis.\n\n"
    "## Escrever para o projeto\n\n"
    "comunidadegameorg@gmail.com\n\n"
    "É o endereço do projeto, e atende a tudo que não tem porta própria acima. Para ajudar na "
    "triagem, diga no assunto do que se trata:\n\n"
    "Dados — revogar consentimento, pedir a exclusão do template biométrico ou exercer "
    "qualquer direito sobre os dados de uma criança.\n"
    "Recibo — a plataforma não emite recibo e não guarda dado fiscal de ninguém; quem precisa "
    "de um escreve para cá com os dados fiscais, e quem emite é a pessoa jurídica vinculada.\n"
    "Imprensa, parceria ou edital.\n"
    "Conduta — violação do Código de Conduta na plataforma ou nas atividades presenciais. "
    "Quem contribui com código usa o repositório público."
)

# A apresentação institucional de "Quem somos", dos documentos 01 e 04
# (`RF-03-45`). Abre a seção: a nota de transparência vem depois dela.
APRESENTACAO_DE_QUEM_SOMOS = (
    "O Comunidade Game é uma plataforma educacional gamificada, de código aberto, que conecta "
    "jovens, mestres e apoiadores para promover educação, tecnologia e cidadania em "
    "comunidades periféricas.\n\n"
    "A ideia é direta: a vida real tratada como partida. Quem joga são os Guerreiros e "
    "Guerreiras, de 6 a 16 anos, que aprendem programação, robótica e inteligência "
    "artificial, registram dados do lugar onde moram e apresentam criações próprias — com o "
    "nome deles no crédito.\n\n"
    "## O ciclo de evolução positiva\n\n"
    "O que a plataforma produz não sai da comunidade: volta para ela. O Guerreiro e a "
    "Guerreira aprendem, e o que aprendem vira realização concreta. Ao registrar dados do "
    "lugar onde moram, dão à sua comunidade evidência para decidir, em vez de apenas "
    "percepção. As conquistas ganham visibilidade e atraem apoio; o apoio custeia novas "
    "atividades; quem chega ao topo volta como multiplicador.\n\n"
    "O ciclo alcança a própria plataforma: as ideias e criações dos Guerreiros e Guerreiras "
    "realimentam trilhas, regras e aplicações. Quem joga também constrói o jogo.\n\n"
    "## O que não se negocia\n\n"
    "As pessoas vêm antes da tecnologia. Educação como fator transformador da sociedade. "
    "Causa antirracista. Combate ao feminicídio e à violência contra a mulher. "
    "Reconhecimento dos povos originários e dos seus saberes. Território e identidade: a "
    "comunidade não é cenário, é protagonista. Letramento sobre a crise ambiental, que aqui "
    "não fica no discurso, porque é o Guerreiro e a Guerreira que medem o clima do lugar "
    "onde vivem. E protagonismo: a criação deles é conteúdo do jogo, não subproduto.\n\n"
    "Isso atravessa o conteúdo, as regras e a convivência. O Código de Conduta de cada "
    "comunidade é construído junto com os próprios Guerreiros e Guerreiras na primeira aula "
    "presencial — regra que se combina engaja mais do que regra que se decreta.\n\n"
    "## Onde estamos\n\n"
    "As oficinas presenciais do Robô Educa acontecem desde 2018. O Comunidade Game é o passo "
    "digital desse trabalho, e o primeiro case real é a Comunidade Guerreira Zeferina, no "
    "Ciclo 01, de agosto a dezembro de 2026.\n\n"
    "O código é aberto, e o modelo pode ser replicado em qualquer comunidade do país.\n\n"
    "## Quem constrói\n\n"
    "Carlos Sales — desenvolvedor, idealizador do projeto, primeiro Admin e primeiro Mestre, "
    "responsável pelos poderes de Programação e Robótica e autor das trilhas Robô Educa e "
    "Batalha de Laser. Habilidade de Mestre se comprova com trabalho publicado e "
    "verificável, e a regra vale para o fundador como vale para todos.\n\n"
    "O projeto nasce da convicção de um desenvolvedor no potencial transformador da própria "
    "habilidade: usar software e dados para produzir impacto positivo na sociedade. A "
    "tecnologia aqui não é fim nem vitrine — é ferramenta de intervenção social.\n\n"
    "A pessoa jurídica vinculada ao projeto é a Robô Educa — Kits Robóticos Educacionais, "
    "que recebe doações e assina termos.\n\n"
    "## Transparência dos recursos\n\n"
    "Todo aporte — dinheiro, equipamento, insumo, alimento, hora de trabalho — entra no "
    "livro-razão da plataforma e aparece em público em moedas, nunca em reais. Nenhuma "
    "atividade acontece sem lastro, e nenhum aporte compra vantagem: moeda alguma abre dado "
    "de criança, canal de contato ou prioridade de qualquer espécie. Não existe ranking de "
    "apoiadores por dinheiro.\n\n"
    "Os dados que a plataforma produz sobre o território são gratuitos. Nesta vitrine eles "
    "saem agregados até o bairro; o conjunto completo, sempre anonimizado, vai a "
    "pesquisadores e gestores públicos mediante solicitação aprovada por um Admin.\n\n"
    "## Proteção de quem joga\n\n"
    "Guerreiros e Guerreiras aparecem em público só por avatar e nick, e só quem tem "
    "autorização do responsável aparece. Imagem real de criança nunca é exibida. Não existe "
    "contato direto entre adulto apoiador e criança: proposta, entrega e reconhecimento "
    "passam sempre pela plataforma.\n\n"
    "Esta vitrine não instala cookie, rastreador nem perfilamento de quem visita, e não "
    "veicula publicidade nem patrocínio. O que a plataforma coleta, de quem, para quê e por "
    "quanto tempo está na área “O que a plataforma coleta”, aberta a qualquer visitante.\n\n"
)

# A nota de transparência sobre IA (`RF-03-48`, documento 01 §7, documento 03
# §§1.12 e 8). O rascunho da fatia 5 virou TEXTO FINAL por decisão do fundador
# de 2026-10-14, e as linhas abaixo não mudaram um caractere.
#
# O TÍTULO É CONTRATO: o identificador derivado dele —
# `nota-de-transparencia-sobre-ia` — é a âncora para onde aponta a etiqueta do
# texto reescrito por IA das Apps 01 e 05 (documento 03 §7.1). Renomeá-lo
# quebra o link, e o teste da semeadura o afirma.
NOTA_SOBRE_IA = (
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
)

# As três réguas do que é aberto, mais as duas decisões do fundador de
# 2026-10-14: o auxílio de IA não altera a licença, e a marca é reservada —
# ambas do documento 03 §1, princípio 4. Fecha a remissão da nota, que
# apontava para cá sem que o bloco respondesse (`RF-03-48`).
LICENCAS = (
    "## Licenças\n\n"
    "O código da plataforma é aberto, sob a licença AGPL. O conteúdo educacional publicado, "
    "com crédito ao Mestre autor, e o conjunto de dados entregue a pesquisadores e gestores, "
    "com crédito à comunidade que o produziu, saem sob a licença CC BY-SA: quem usa pode "
    "adaptar, creditando, e o derivado herda a mesma licença.\n\n"
    "O auxílio de ferramentas de inteligência artificial não altera a licença de nada: o "
    "artefato segue a licença do que ele é, e o crédito é de quem decidiu, revisou e "
    "publicou.\n\n"
    "A marca é reservada e não segue nenhuma das duas réguas: o nome do projeto, o logotipo, "
    "o símbolo, as submarcas e os personagens do universo narrativo ficam fora da AGPL e da "
    "CC BY-SA. Quem replica a plataforma usa o código inteiro e troca a marca pela sua."
)

TEXTO_DE_QUEM_SOMOS = APRESENTACAO_DE_QUEM_SOMOS + NOTA_SOBRE_IA + LICENCAS

SEMENTES: dict[SecaoInstitucional, str] = {
    SecaoInstitucional.quem_somos: TEXTO_DE_QUEM_SOMOS,
    SecaoInstitucional.contatos: TEXTO_DE_CONTATOS,
    SecaoInstitucional.como_apoiar: TEXTO_DE_COMO_APOIAR,
}


def semear_conteudo_institucional(sessao: Session) -> list[SecaoInstitucional]:
    """Converge as **três** seções, **só onde a seção ainda não tem texto**:
    repetir nunca sobrescreve uma publicação. Nenhuma nasce com vídeo — o de
    apresentação ainda não existe (`RF-03-49`). Devolve as seções semeadas
    nesta chamada."""
    semeadas: list[SecaoInstitucional] = []
    for secao, texto in SEMENTES.items():
        linha = sessao.get(ConteudoInstitucional, secao)
        if linha is not None and linha.texto:
            continue
        publicar_secao(sessao, secao, texto=texto, video_url=None, autor_id=None)
        semeadas.append(secao)
    sessao.commit()
    return semeadas
