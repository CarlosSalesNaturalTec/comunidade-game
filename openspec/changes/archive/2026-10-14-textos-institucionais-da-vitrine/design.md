# Design

## Context

Ver `proposal.md` — Why. A capacidade já está consolidada em
`openspec/specs/conteudo-institucional/spec.md`: entidade, três rotas e semeadura que converge
só onde a seção não tem texto. Esta change não mexe em nenhuma delas — entrega **conteúdo** e
as decisões de documento que o conteúdo aplica.

Quatro restrições da implementação já existente moldam o texto, e nenhuma é negociada aqui:

| Restrição | Consequência |
| --------- | ------------ |
| A marcação aceita só `## ` abrindo bloco e parágrafos separados por linha em branco; o texto entra como texto, nunca HTML | Sem negrito, sem lista, sem link — o endereço sai como texto não clicável (decisão do fundador 4) |
| A apresentação preserva a quebra de linha simples dentro do parágrafo | Linhas próprias são possíveis sem lista — é como a chave PIX já sai |
| O identificador de cada bloco deriva do título | Renomear "Nota de transparência sobre IA" quebra a âncora da etiqueta das Apps 01 e 05 |
| "Quem somos" e "Contatos" renderizam no build; "Como apoiar" é lida a cada visita, na porta do convite | O texto das duas primeiras só aparece no site após redeploy da App 06 |

## Goals / Non-Goals

**Goals:**

- Descer as nove decisões do fundador de 2026-10-14 pelo fluxo: documento-fonte → documento 09
  → PRD → semeadura.
- Deixar as três seções nascendo com texto numa instalação nova.
- Fechar a pendência do texto final da nota (PRD-03 §14).

**Non-Goals:**

- Mudar contrato de rota, modelo ou migração — nada disso muda.
- Tornar o endereço clicável, ofuscá-lo ou trocá-lo por formulário (decisão 4).
- Dar a "Quem somos" alcance nos recortes de pesquisadores e gestores (decisão 3).
- Publicar o texto em produção: a semeadura não a alcança, e quem publica é o Admin.

## Decisions

1. **Os três textos moram neste `design.md`, íntegros, e entram na semeadura como constantes** —
   como já estão hoje. Alternativa descartada: arquivo de dados separado, que criaria um formato
   novo para três cadeias de texto.
2. **A nota de transparência sobre IA fica byte a byte, título incluído.** O rascunho virou
   texto final sem alteração (decisão 5), e o título é contrato. Alternativa descartada:
   melhorar a redação de passagem — mudaria uma decisão aprovada.
3. **As decisões 6 e 9 entram como parágrafos de "Licenças", não como blocos novos.** São
   licenciamento, assunto do bloco. Alternativa descartada: bloco "Marca" próprio, que
   acrescentaria âncora pública sem requisito que a peça.
4. **"Contatos" concentra o endereço num único bloco final, com as finalidades em linhas
   próprias dentro de um parágrafo.** Alternativa descartada: um bloco por finalidade, que
   repetiria o mesmo endereço quatro vezes.
5. **O documento-fonte muda antes do texto.** A decisão 6 é gravada no documento 03 §1,
   princípio 4, e o canal do recibo no documento 04 §1; só então a vitrine os aplica. É a
   hierarquia de autoridade, não preferência de ordem.
6. **Publicar em produção é operação, não código.** A tarefa final registra o que o fundador
   precisa fazer — `PUT` das três seções na App 03 e redeploy da App 06 —, e a change não
   automatiza nem dispara nada disso.

**O que fica com o fundador, depois do merge.** Dois passos manuais, nesta ordem, e nenhuma
tarefa desta change os executa: (1) publicar as três seções por
`PUT /v1/conteudo-institucional/{secao}` pela tela de edição da App 03, porque a semeadura
converge só onde a seção não tem texto e produção já foi semeada pela fatia 5 — sem isso,
"Quem somos" e "Como apoiar" seguem com o texto antigo e "Contatos" segue vazia; (2) fazer o
redeploy da App 06, sem o qual "Quem somos" e "Contatos" não mudam no site, porque renderizam
no build. "Como apoiar" é a exceção e aparece na porta do convite já na primeira visita após o
`PUT`.

**Um desvio das tarefas, resolvido na aplicação.** A tarefa 1.2 previa o endereço só no
documento 04 §1. Escrevê-lo ali com o que ele atende duplicaria assunto de outro documento, o
que a regra de fonte única proíbe: o endereço foi para o documento 03 §8, onde "Contatos" é
descrita, e o documento 04 §1 ficou com uma remissão de uma frase. O documento 99 §3 ganhou a
linha do canal, porque a remissão é relação nova entre documentos.

## Textos

### "Quem somos"

Os blocos abaixo entram **antes** de "## Nota de transparência sobre IA", que permanece como
está. "## Licenças" é substituído pela versão ao fim desta subseção.

```text
O Comunidade Game é uma plataforma educacional gamificada, de código aberto, que conecta
jovens, mestres e apoiadores para promover educação, tecnologia e cidadania em comunidades
periféricas.

A ideia é direta: a vida real tratada como partida. Quem joga são os Guerreiros e Guerreiras,
de 6 a 16 anos, que aprendem programação, robótica e inteligência artificial, registram dados
do lugar onde moram e apresentam criações próprias — com o nome deles no crédito.

## O ciclo de evolução positiva

O que a plataforma produz não sai da comunidade: volta para ela. O Guerreiro e a Guerreira
aprendem, e o que aprendem vira realização concreta. Ao registrar dados do lugar onde moram,
dão à sua comunidade evidência para decidir, em vez de apenas percepção. As conquistas ganham
visibilidade e atraem apoio; o apoio custeia novas atividades; quem chega ao topo volta como
multiplicador.

O ciclo alcança a própria plataforma: as ideias e criações dos Guerreiros e Guerreiras
realimentam trilhas, regras e aplicações. Quem joga também constrói o jogo.

## O que não se negocia

As pessoas vêm antes da tecnologia. Educação como fator transformador da sociedade. Causa
antirracista. Combate ao feminicídio e à violência contra a mulher. Reconhecimento dos povos
originários e dos seus saberes. Território e identidade: a comunidade não é cenário, é
protagonista. Letramento sobre a crise ambiental, que aqui não fica no discurso, porque é o
Guerreiro e a Guerreira que medem o clima do lugar onde vivem. E protagonismo: a criação deles
é conteúdo do jogo, não subproduto.

Isso atravessa o conteúdo, as regras e a convivência. O Código de Conduta de cada comunidade é
construído junto com os próprios Guerreiros e Guerreiras na primeira aula presencial — regra
que se combina engaja mais do que regra que se decreta.

## Onde estamos

As oficinas presenciais do Robô Educa acontecem desde 2018. O Comunidade Game é o passo
digital desse trabalho, e o primeiro case real é a Comunidade Guerreira Zeferina, no Ciclo 01,
de agosto a dezembro de 2026.

O código é aberto, e o modelo pode ser replicado em qualquer comunidade do país.

## Quem constrói

Carlos Sales — desenvolvedor, idealizador do projeto, primeiro Admin e primeiro Mestre,
responsável pelos poderes de Programação e Robótica e autor das trilhas Robô Educa e Batalha
de Laser. Habilidade de Mestre se comprova com trabalho publicado e verificável, e a regra
vale para o fundador como vale para todos.

O projeto nasce da convicção de um desenvolvedor no potencial transformador da própria
habilidade: usar software e dados para produzir impacto positivo na sociedade. A tecnologia
aqui não é fim nem vitrine — é ferramenta de intervenção social.

A pessoa jurídica vinculada ao projeto é a Robô Educa — Kits Robóticos Educacionais, que
recebe doações e assina termos.

## Transparência dos recursos

Todo aporte — dinheiro, equipamento, insumo, alimento, hora de trabalho — entra no livro-razão
da plataforma e aparece em público em moedas, nunca em reais. Nenhuma atividade acontece sem
lastro, e nenhum aporte compra vantagem: moeda alguma abre dado de criança, canal de contato
ou prioridade de qualquer espécie. Não existe ranking de apoiadores por dinheiro.

Os dados que a plataforma produz sobre o território são gratuitos. Nesta vitrine eles saem
agregados até o bairro; o conjunto completo, sempre anonimizado, vai a pesquisadores e
gestores públicos mediante solicitação aprovada por um Admin.

## Proteção de quem joga

Guerreiros e Guerreiras aparecem em público só por avatar e nick, e só quem tem autorização do
responsável aparece. Imagem real de criança nunca é exibida. Não existe contato direto entre
adulto apoiador e criança: proposta, entrega e reconhecimento passam sempre pela plataforma.

Esta vitrine não instala cookie, rastreador nem perfilamento de quem visita, e não veicula
publicidade nem patrocínio. O que a plataforma coleta, de quem, para quê e por quanto tempo
está na área "O que a plataforma coleta", aberta a qualquer visitante.
```

Bloco "Licenças", na íntegra, substituindo o atual:

```text
## Licenças

O código da plataforma é aberto, sob a licença AGPL. O conteúdo educacional publicado, com
crédito ao Mestre autor, e o conjunto de dados entregue a pesquisadores e gestores, com
crédito à comunidade que o produziu, saem sob a licença CC BY-SA: quem usa pode adaptar,
creditando, e o derivado herda a mesma licença.

O auxílio de ferramentas de inteligência artificial não altera a licença de nada: o artefato
segue a licença do que ele é, e o crédito é de quem decidiu, revisou e publicou.

A marca é reservada e não segue nenhuma das duas réguas: o nome do projeto, o logotipo, o
símbolo, as submarcas e os personagens do universo narrativo ficam fora da AGPL e da CC BY-SA.
Quem replica a plataforma usa o código inteiro e troca a marca pela sua.
```

### "Contatos"

```text
Aqui estão os caminhos para falar com o projeto. Cada um leva a uma porta diferente, e
escolher a certa economiza o seu tempo e o nosso.

Nenhum destes canais alcança um Guerreiro ou uma Guerreira. Toda interação entre adulto e
criança é mediada pela plataforma, e nisso não há exceção.

## Quero apoiar

Dinheiro, equipamento, insumo, alimento, serviço, conteúdo, código, divulgação — ou vontade de
ensinar. Comece pela chamada "Quero apoiar", presente em toda página desta vitrine: ela
pergunta o que você traz e encaminha. Quem vai transferir dinheiro faz o pré-cadastro na Área
do Apoiador; as outras formas passam pelo formulário da vitrine. As duas portas caem na mesma
fila de avaliação de um Admin.

## Quero ensinar

Mestre é cadastrado por um Admin, com habilidade comprovada por trabalho publicado e
verificável — portfólio, código, videoaulas, currículo. O primeiro passo é o formulário de
participação desta vitrine.

## Pesquisa e gestão pública

O conjunto completo de dados do território é gratuito, sai anonimizado e licenciado em CC
BY-SA, e depende de solicitação prévia aprovada por um Admin, respondida em até 7 dias. O
caminho é o formulário de solicitação de dados desta vitrine, com solicitante, instituição,
e-mail e finalidade declarada. Os recortes de pesquisadores e de gestores públicos mostram o
que se mede, com que cadência e desde quando.

## Construir sobre a plataforma

O código é aberto e a API pública pode ser consumida por outra aplicação. A seção "Construir
sobre a API" explica como solicitar a chave de aplicação, emitida por um Admin, e traz o
assistente que responde dúvidas de integração.

## Responsáveis por um Guerreiro ou Guerreira

O caminho mais curto é a gestão, no encontro presencial. O acompanhamento, a autorização de
divulgação e o desligamento da personalização por IA ficam na Área dos Responsáveis.

## Escrever para o projeto

comunidadegameorg@gmail.com

É o endereço do projeto, e atende a tudo que não tem porta própria acima. Para ajudar na
triagem, diga no assunto do que se trata:

Dados — revogar consentimento, pedir a exclusão do template biométrico ou exercer qualquer
direito sobre os dados de uma criança.
Recibo — a plataforma não emite recibo e não guarda dado fiscal de ninguém; quem precisa de um
escreve para cá com os dados fiscais, e quem emite é a pessoa jurídica vinculada.
Imprensa, parceria ou edital.
Conduta — violação do Código de Conduta na plataforma ou nas atividades presenciais. Quem
contribui com código usa o repositório público.
```

### "Como apoiar"

```text
Doações em dinheiro são feitas por PIX, em nome da pessoa jurídica vinculada ao projeto.

Chave PIX (CNPJ): 51.730.395/0001-19
Titular: Robô Educa — Kits Robóticos Educacionais

Depois de transferir, anexe o comprovante no pré-cadastro: a plataforma não confirma PIX
automaticamente — quem confere é um Admin. Não pedimos CPF, CNPJ nem documento de identidade
de quem doa.

Toda doação recebida é registrada no livro-razão da plataforma e compõe o seu Poder
Sustentador, visível em público em moedas.

A plataforma não emite recibo. Quem precisar de um escreve para comunidadegameorg@gmail.com
informando os dados fiscais, e a pessoa jurídica vinculada o emite — é o que permite comprovar
a doação sem a plataforma guardar dado fiscal de ninguém.
```

## Risks / Trade-offs

- **Renomear o título da nota quebraria a etiqueta de IA das Apps 01 e 05** → o cenário do
  delta e o teste da semeadura fixam o título; o bloco entra byte a byte.
- **Bloco mal formado não vira título, e o texto sai como parágrafo corrido** → cada bloco abre
  com `## ` em linha própria e os parágrafos ficam separados por linha em branco; o teste
  afirma a presença dos títulos.
- **E-mail cru é colhido por robô de spam** → risco aceito pela decisão 4; o endereço é uma
  caixa do Gmail, com filtro próprio.
- **A semente passa a carregar o endereço do projeto, além da chave PIX** → quem replicar a
  plataforma herda os dois. Fora do escopo desta change, registrado na pergunta aberta abaixo.
- **Mudar a semeadura não atualiza produção** → a tarefa final declara os passos manuais; a
  change não finge tê-los feito.

## Open Questions

- A semente devia nascer **neutra** para quem replica a plataforma, sem a chave PIX nem o
  endereço do Comunidade Game? Hoje já carrega a chave, e esta change acrescenta o endereço. A
  resposta não muda o delta, o desenho nem as tarefas desta fatia: ela abriria uma fatia
  própria, de parametrização da implantação.
