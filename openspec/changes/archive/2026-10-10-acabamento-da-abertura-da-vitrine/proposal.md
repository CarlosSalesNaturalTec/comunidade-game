# Proposal

**PRD de origem:** PRD-03 — Vitrine pública (App 06).
**Linha no cronograma:** linha `—` do bloco do PRD-03, criada por esta change — mesma
natureza das duas últimas (`2026-10-09-acesso-ao-nucleo-e-rotas-servidas-da-vitrine` e
`2026-10-10-elenco-adolescente-e-composicao-do-heroi`): acabamento da abertura, sem recorte
novo de requisito.
**Recorte:** **não fecha `RF` nenhum**. Atende ou preserva `RF-03-01`, `RF-03-25`,
`RF-03-26`, `RF-03-51`, `RF-03-58` e `RN-03-21`.

## Why

A abertura da vitrine no celular não cumpre o que os documentos 15 §§4 e 6 já mandam, e o
fundador viu isso numa visita pela tela de um aparelho de 360 px, em 2026-10-10:

1. **A faixa de topo encosta no corte do visor.** Em `layouts/Vitrine.astro` a marca, o
   cabeçalho e a navegação de recortes ficam **fora** do `<main class="cg-moldura">`, o único
   elemento com respiro lateral e largura de leitura. O símbolo da marca sai cortado e o
   botão "Entrar" transborda a tela. A calha de 16 px do documento 15 §4 não existe ali.
2. **"Comunidade Game" aparece duas vezes** no topo — na `MarcaDoProjeto` e no `h1` do
   cabeçalho.
3. **Os links dos recortes saem crus**: `.cg-recortes__item` não declara `color` nem
   `text-decoration`, então o navegador aplica o roxo sublinhado dele; com o alvo de toque
   desenhado como caixa, os três quebram em duas linhas.
4. **As duas ações da abertura não se leem como par**: "Entrar" fica no cabeçalho, vazado e
   espremido na borda; "Quero participar" fica no herói, cheio e azul.
5. **A frase do projeto domina o elenco**, que é justamente o que o documento 15 §6 manda pôr
   em primeiro plano na Arena: a frase sai a `1,375 rem` e o elenco, a 96 px de altura no
   celular.

Nada disso é requisito novo: é o documento 15 aplicado à tela que já existe.

## What Changes

Seis decisões do fundador de 2026-10-10, mais duas aprovadas na mesma sessão. Todas já
tomadas — nenhuma lacuna preenchida por suposição.

- **Saudação.** O subtítulo do cabeçalho passa a **"Boas-vindas! Tudo aqui é aberto — sem
  cadastro e sem login."** A promessa do `RF-03-51` e do `RN-03-01` fica **dentro** da
  saudação, não é substituída por ela. "Boas-vindas", e não "Bem-vindo": o projeto evita o
  masculino genérico em toda parte.
- **BREAKING (spec) — par de ações no herói.** "Entrar" e "Quero participar" passam a ser um
  **par lado a lado** no herói. O "Entrar" **migra, não se repete**: onde há herói ele é do
  herói; nas demais telas públicas segue no cabeçalho. **Um só por tela, sempre.** Reverte em
  parte a decisão de 2026-10-09 gravada na spec — o que ficou proibido ali foi a
  **duplicação**, e migrar não duplica. O `RF-03-58` segue cumprido: ele exige o botão
  visível em toda tela pública, não que ele more no cabeçalho.
- **Cores diferentes, mesmo padrão.** Os dois botões são **cheios**, de mesma altura, raio e
  peso. "Quero participar" na família **Ação**; "Entrar" na família **Marca**. Os três tokens
  do laranja já existem em `comum/tokens.css` e nunca tinham sido usados; o contraste está
  medido no documento 15 §3.3. Nenhum token novo.
- **Só na App 06.** `comum/react/Cabecalho.tsx` e `comum/react/Botao.tsx` **não se mexem** —
  são de oito aplicações.
- **Rótulo do recorte padrão** passa de "Sociedade civil" para **"Início"**. É **troca de
  rótulo apenas**: o recorte continua se chamando *sociedade civil* no domínio, a chave segue
  `sociedade-civil`, e **nenhum documento normativo muda**.
- **Navegação dos recortes em uma linha só**, fonte menor, sem o link cru do navegador. O
  corrente segue marcado por **peso e filete**, nunca só por cor, e o alvo de toque de 48 px
  vem do respiro, não do tamanho da fonte.
- **Herói: frase menor, elenco maior.** A frase cai um degrau da escala; o elenco **sangra até
  a borda** do visor e cresce cerca de 70 % no celular. A **ordem das quatro figuras não
  muda**.
- **O `h1` duplicado sai** do cabeçalho da vitrine: o nome fica na marca, como nas outras sete
  aplicações, e a saudação passa a ser a primeira frase do topo.
- **A faixa de topo entra na moldura**, com o mesmo respiro e a mesma largura de leitura do
  `<main>`. Tratado como **defeito**, não como decisão.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-vitrine`: dois requisitos mudam de texto.
  - **A abertura tem herói, com ilustração em primeiro plano** — a proibição de repetir o
    "Entrar" vira a regra do **par de ações** e da **migração**: o herói apresenta as duas
    ações, e o "Entrar" continua sendo **um só na tela**.
  - **O botão "Entrar" fica sempre visível e pergunta qual persona está entrando** — ganha
    **onde** ele mora: no herói, na tela que tem herói; no cabeçalho, nas demais. E que é um
    só por tela.

O que **não** vira requisito, de propósito: a saudação, o rótulo "Início", o tamanho da
frase, o tamanho do elenco, a estética da navegação e o respiro da faixa de topo. São
aplicação do documento 15 §§4, 5 e 6 e de requisitos que já existem — nenhum deles é regra
nova, e inventar requisito para eles seria criar regra dentro de um artefato do OpenSpec. O
respiro e a navegação em uma linha ficam guardados por **teste**, não por spec.

## Impact

**Código — `apps/app-06-vitrine/` apenas:**

| Arquivo | O que muda |
| --- | --- |
| `src/componentes/CabecalhoDaVitrine.tsx` | saudação; fim do `h1` duplicado; "Entrar" condicional |
| `src/abertura/Heroi.tsx` | o par de ações; a frase um degrau menor |
| `src/layouts/Vitrine.astro` | faixa de topo dentro da moldura; diz ao cabeçalho se a tela tem herói |
| `src/navegacao/recortes.ts` | rótulo "Início" — a chave `sociedade-civil` **não** muda |
| `src/index.css` | `.cg-recortes`, `.cg-heroi__frase`, `.cg-heroi__elenco`, o par de ações |

**Não muda:** `comum/`, o backend, nenhuma rota, nenhum contrato de API.

**Testes que andam junto** (`src/testes/`): `TelaDaVitrine.tsx` **espelha a marcação do
cabeçalho à mão** e é guardada por `saidaDoBuild.test.ts` — as duas se movem em sincronia.
Afirmam por nome sobre "Sociedade civil" ou "Entrar": `abertura`, `entrada`, `heroi`,
`avisoDeColeta`, `portfolioRankingEPoderes`, `semRastro`, `entradaSemEnderecoPublicado` e
`formularioDeParticipacao`. Em `heroi.test.tsx` o caso "não repete o Entrar" **muda de
sentido**: passa a afirmar que o "Entrar" é **um só na tela**.

**Documentação no mesmo PR:** só a linha `—` nova no `openspec/cronograma-de-fatias.md`.
Nenhuma regra de negócio nova foi decidida, então o documento 09 e os documentos-fonte não
mudam; `docs/prds/index.md` não muda, porque a situação do PRD-03 é a mesma; `mkdocs.yml` não
muda, porque nenhum arquivo nasce em `docs/`.

**Ritmo de verificação:** a change não toca `docs/` nem `.md` da raiz — `npm run lint` e
`mkdocs build --strict` ficam de fora. Rodam Biome e Vitest da App 06.
