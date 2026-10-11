# Proposal

**PRD de origem:** PRD-03 — Vitrine pública (App 06).
**Fatia:** linha sem número do bloco do PRD-03 em `openspec/cronograma-de-fatias.md` —
"Vitrine reordenada, duas seções a menos e a entrada verde". Não fecha recorte novo: **muda o
enunciado** de `RF-03-02`, `RF-03-39`, `RF-03-45` e `RF-03-46`, e **preserva** `RF-03-01`,
`RF-03-42`, `RF-03-43`, `RF-03-47`, `RF-03-51` e `RF-03-58`.
**Origem:** seis decisões do fundador de 2026-10-11, descidas pelo fluxo — documento-fonte,
documento 09 §1, PRD, change — antes de qualquer código.

## Why

A abertura da vitrine cresceu por acréscimo: cada fatia pôs a sua seção no fim da fila, e a
ordem resultante não é a ordem com que o visitante decide. Quem chega vê primeiro o
institucional e só depois o que o projeto produziu. Duas seções, além disso, não se sustentam:
a de **poderes** promete uma página individual que nunca existiu, e **"Como apoiar"** duplica,
numa seção de rolagem, a chave PIX que a porta do convite já oferece com contexto.

A reordenação é decisão de produto, não de desenho de tela — por isso ela desce pelos
documentos antes de entrar no código.

## What Changes

- **Ordem da abertura** (recorte sociedade civil) passa a ser: Ranking, Portfólio de criações
  originais, Guerreiros e Guerreiras, Apoiadores, Necessidades em aberto, Mestres, Comunidades
  Virtuais, Construir sobre a API, Quem somos, Contatos. A ordem mora na página do recorte,
  como `src/navegacao/recortes.ts` já declara — não é requisito.
- **BREAKING** — a **seção de poderes sai** da vitrine, e com ela os Mestres responsáveis que
  as fatias 2 e 7 derivaram do autor das trilhas publicadas. Isso **fecha o resíduo do
  `RF-03-39`**: o poder nunca teve página individual e deixa de precisar de uma. `RF-03-02`
  passa de seis seções com cards para **cinco** — Guerreiros e Guerreiras, Mestres, batalhas,
  apoiadores e comunidades.
- **BREAKING** — **"Como apoiar" deixa de ser exibida**. A seção `como-apoiar` do conteúdo
  institucional **continua no núcleo**, gravável pelo `PUT /conteudo-institucional/{secao}` e
  legível pelo Admin: o que sai é a tela pública. `RF-03-45` e `RF-03-46` mudam de enunciado, e
  a chave PIX passa a aparecer **num lugar só**, a porta do `RF-03-43`.
- **"Necessidades em aberto" vira seção própria** da abertura, com esse rótulo. Hoje vive
  dentro de "Como apoiar". `RF-03-47` não muda — nunca disse onde.
- **BREAKING** — a chamada **"Quero participar" passa a "Quero apoiar"** nos três lugares: o
  link do herói, a chamada ao pé das páginas individuais e o título da porta. O **caminho
  `/quero-participar` não muda** — é endereço público compartilhável, está no `sitemap.xml`, e
  o `RF-03-42` nomeia a porta, não a URL. O garfo das sete modalidades do documento 14 §10
  continua inteiro atrás dele, a pretensão de ensinar incluída.
- O **"Entrar" fica verde**, reaproveitando a família **Sucesso** do documento 15 §3.2 — sem
  família nova e sem degrau inventado. O token passa a significar "deu certo" **e** "entre
  aqui", e a §3.2 declara isso em uma frase. `.cg-botao--marca` perde o único consumidor e
  vira `.cg-botao--entrada`, nome de papel e não de família.

### Fora do escopo

O que o PRD-03 §3.2 já exclui, mais o que estas decisões não alcançam:

- A seção **batalhas** do `RF-03-02` segue sem fatia: o dado é do PRD-10 e
  `/vitrine/batalhas` não existe (decisão do fundador de 2026-09-26).
- `GET /v1/vitrine/poderes` **não é removida** do núcleo. A vitrine existe para ser construída
  por cima, e a Área do Apoiador Desenvolvedor é a porta disso; sai apenas o consumo no
  cliente. A capacidade `leitura-publica-da-vitrine` não muda.
- A entidade, as rotas e a semeadura do conteúdo institucional não mudam. A capacidade
  `conteudo-institucional` não muda.
- A ordem das seções dos recortes **pesquisadores** e **gestores públicos** não muda: a decisão
  é da abertura.
- Nenhuma família de cor nova entra no documento 15, e nenhum degrau é acrescentado à família
  Sucesso.

## Capabilities

### New Capabilities

Nenhuma. A change reorganiza e retira comportamento público já especificado.

### Modified Capabilities

- `aplicacao-da-vitrine`, em quatro operações:
  - **Removidos (2)** — a seção de poderes com as trilhas e os Mestres responsáveis; e
    "Contatos" e "Como apoiar", **substituído** em vez de alterado, porque três dos cenários
    dele descrevem comportamento que deixa de existir, não comportamento que muda.
  - **Acrescentados (4)** — a vitrine não apresenta seção nem página de poder; "Necessidades em
    aberto" é seção da abertura; "Contatos" exibe o texto publicado; e a vitrine não apresenta
    tela de "Como apoiar", com a chave PIX na porta.
  - **Modificados (3)** — o herói e o par de ações (rótulo); a chamada em toda página
    individual (rótulo, no enunciado e em cinco cenários); e a porta, que deixa de descrever a
    chave PIX como "a mesma que 'Como apoiar' publica".
  - **Renomeado (1)** — o requisito da chamada, que carrega o rótulo no próprio nome.

## Impact

**Documentação (nível 1 e 2), no mesmo PR:**

- Documento 03 §8: o poder sai de três listas (seções, páginas individuais, chamada); "Como
  apoiar" deixa de ser seção pública; o rótulo da chamada muda.
- Documento 15 §3.2 (a família Sucesso serve também o "Entrar") e §3.3 (as razões medidas).
- Documentos 02 §1, 08, 12 §4 e 14 §10: as menções ao rótulo acompanham, em uma frase cada.
- Documento 09 §1: seis linhas novas em "Já decididos".
- PRD-03: `RF-03-02`, `RF-03-39`, `RF-03-45`, `RF-03-46` e as §§2, 5.9 e 6.4.
- PRD-02 §16: a tela de edição do institucional segue valendo para três seções, uma das quais
  não tem mais tela pública.
- `openspec/cronograma-de-fatias.md`: a linha desta change.

**Código — `apps/app-06-vitrine/`:**

- `src/pages/index.astro` (ordem, duas seções fora, uma seção nova),
  `src/poderes/SecaoDePoderes.tsx` (apagado), `src/api/leituras.ts` (`listarPoderes` e o tipo
  `PoderPublico` saem), `src/abertura/Heroi.tsx`, `src/abertura/EntradaDaAbertura.tsx`,
  `src/convite/ChamadaDeParticipacao.tsx`, `src/convite/PortaDoConvite.tsx`, `src/index.css`.

**Código — `comum/`:**

- `comum/tokens.css`: `--cor-sobre-sucesso`, nos dois modos. Derivação, não primitiva nova.

**Testes:** `convite.test.tsx`, `heroi.test.tsx`, `entrada.test.tsx`,
`necessidadesEmAberto.test.tsx`, `portfolioRankingEPoderes.test.tsx`, `arena.test.tsx`,
`cardsEPagina.test.tsx`, `mestresEApoiadores.test.tsx` e a composição de teste
`src/testes/TelaDaVitrine.tsx`.

**Núcleo:** nada. Nenhuma rota, entidade ou contrato muda.

**Medição obrigatória:** as duas razões de contraste do par verde — `cal-000` sobre
`sucesso-600` no claro e `sucesso-400` com `tinta-900` no escuro. Nenhum número entra no
documento 15 sem ser medido.
