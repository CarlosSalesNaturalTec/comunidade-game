# Proposal

## Why

É a **fatia 12 do PRD-03** (`openspec/cronograma-de-fatias.md`), e ela atende o `RF-03-08`,
parcial desde 2026-09-28, mais identificadores **novos** — `RF-03-84`, `RF-03-85` e `RN-03-41`
a `RN-03-43` —, criados na revisão do PRD-03 que entra nesta change, aplicando a decisão do
fundador de 2026-11-03 (documento 09 §1, documento 99 §6, invariante 5).

O invariante 5 do documento 99 declara que **o portfólio é o acervo**: reúne as comprovações
aprovadas dos desafios práticos e a criação da culminância, e em público exibe só o aprovado e
autorizado. A seção pública cumpre metade disso. Ela tem **uma** fonte, exibe trilha, data e
autoria **sem título**, e o campo `producao` chega no payload de `CriacaoPublicaSaida` e **não
é desenhado** — a linha não abre nada. As quatro changes de 2026-11-04 fecharam o outro lado:
`publicavel` existe, a comprovação está gravada e o título curto do prático é declarado pelo
Mestre. Falta quem leia.

## What Changes

- **O acervo público ganha a segunda fonte**: as comprovações de desafio prático julgadas
  **cumpridas e publicáveis**, ao lado da criação da culminância validada, em **uma só lista**
  decrescente por data, com a paginação de dez do `RF-03-82` percorrendo as duas sem pular nem
  repetir item. A seção **mantém o nome** "Portfólio de criações originais". (`RF-03-84`)
- **A linha traz o título em destaque** e preserva trilha, data e autoria por nick, com o que o
  `RF-03-08` sai inteiro pela primeira vez. O título é o **curto declarado pelo Mestre** na
  comprovação e o **nome da trilha** na criação da culminância, que não tem campo de título no
  modelo; quando o título é a trilha, a linha **não a repete** (decisões do fundador de
  2026-11-04). (`RF-03-08`, `RN-03-43`)
- **A linha abre a produção na própria linha**, expandindo: imagem, áudio, vídeo e o corpo do
  texto, link externo como link de saída e arquivo como transferência. Sem endereço novo — a
  criação não tem página individual (decisão do fundador de 2026-10-11), e são os nicks que
  abrem página (`RF-03-03`). (`RF-03-85`)
- **O portão público passa a exigir aprovação do Mestre** além da autorização do responsável:
  criação **validada**, ou comprovação julgada **cumpriu e publicável** com comprovação
  gravada. A entrega presencial, a declaração não julgada e a julgada não publicável **nunca**
  vão a público. (`RN-03-41`)
- **A produção das atividades da missão nunca é item de acervo**: ela passou a guardar mídia,
  e não tem ato de aprovação (documento 99 §6, invariante 5). Está nomeado para não ser
  suposto. (`RN-03-42`)
- `GET /v1/vitrine/criacoes` passa a devolver, por item, o **identificador**, a **fonte**, o
  **título** e o **tipo** da produção — **aditivo**, nenhum campo sai nem muda de sentido —, e
  nasce `GET /v1/vitrine/comprovacoes/{id}/arquivo`, os bytes da comprovação pública sob o
  **mesmo portão** da listagem, pelo precedente da rota de bytes da criação.
- Revisão do **PRD-03** (§§6.1, 7, 9, 12, 14 e 15) com os cinco identificadores novos e o
  fechamento da pendência do título, única da §14.

**Fora do escopo** — o PRD-03 §3.2 segue valendo, e isto está nomeado para não ser suposto: o
**acervo na área do Guerreiro(a)**, que exibe tudo e é do PRD-05; o **badge de autoria**, que o
documento 02 §4 mantém só na culminância; a **seção de batalhas** do `RF-03-02`, sem dado até
o PRD-10; e qualquer **escrita** pela vitrine (`RN-03-01`).

## Capabilities

### New Capabilities

Nenhuma. A fatia amplia capacidades existentes.

### Modified Capabilities

- `leitura-publica-da-vitrine`: o portfólio público deixa de ter uma fonte e um portão só, e
  deixa de sair sem título — o requisito de hoje **proíbe** o título ("NEVER SHALL trazer
  título"). Ganha a comprovação aprovada como segunda fonte, o portão com os dois vereditos do
  Mestre e a rota de bytes dela.
- `aplicacao-da-vitrine`: a linha do portfólio passa a trazer o título e a abrir a produção; o
  requisito de hoje manda sair **sem título** e nada diz sobre abrir a produção.

## Impact

- **Núcleo**: `vitrine/publico.py` (o portão da comprovação pública, ao lado de
  `condicoes_de_criacao_publica`, e a derivação do título) e `vitrine/rotas.py` (a listagem
  unida, o payload de `CriacaoPublicaSaida` e a rota de bytes da comprovação).
- **Contratos**: `GET /v1/vitrine/criacoes` ganha quatro campos por item — aditivo, e sem
  BREAKING; nasce `GET /v1/vitrine/comprovacoes/{id}/arquivo`, com a recusa em **404 em todos
  os casos**, como a rota irmã, para não virar oráculo sobre quais crianças têm divulgação
  autorizada. A rota pública da vitrine é a mesma que terceiros constroem por cima (PRD-03 §8).
- **Dados**: **nenhuma migração** — a fatia só lê o que as changes de 2026-11-04 gravaram.
  Nenhum campo novo no modelo: o título da culminância é o nome da trilha, por decisão do
  fundador de 2026-11-04.
- **Aplicações**: **App 06** — `portfolio/SecaoDoPortfolio.tsx`, a abertura da produção em
  componente próprio, `api/leituras.ts` e o estilo da seção.
- **PRDs**: identificadores novos a partir de `RF-03-84` e `RN-03-41`, livres hoje; nenhum
  enunciado existente muda. A §14 do PRD-03 fica **sem pendência**.
- **Documentação**: a decisão já está no documento 99 §6 (invariante 5) e no documento 09 §1 —
  esta change não a reescreve. Acrescenta ao documento 09 §1 as **cinco decisões** de
  2026-11-04 que delimitaram esta fatia e fecha a linha 12 do cronograma.
