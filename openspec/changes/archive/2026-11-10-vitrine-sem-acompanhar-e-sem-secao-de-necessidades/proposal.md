# Proposal

**PRD de origem:** PRD-03 — Vitrine pública (App 06). **Fatia:** nenhuma numerada — linha "—"
nova no bloco do PRD-03 do `openspec/cronograma-de-fatias.md`, como as demais correções por
decisão do fundador. **Desfaz** parte da fatia 6
(`2026-09-29-convite-ao-acompanhamento-e-necessidades`) e a seção própria decidida em
2026-10-11.

**Identificadores:** retira `RF-03-40`; preserva, sem mudar enunciado, `RF-03-38`, `RF-03-39`,
`RF-03-41` a `RF-03-44`, `RF-03-47`, `RN-03-15`, `RN-03-16` e `RN-03-25`.

## Why

Duas decisões do fundador de 2026-11-10:

1. **Sai o botão "Quero acompanhar"** das quatro páginas individuais da vitrine — Guerreiro(a),
   Mestre, Apoiador e Comunidade Virtual. Ele levava à mesma porta que "Quero apoiar" e não
   acompanhava nada: era um segundo botão para o mesmo destino. A vitrine segue sem favorito
   (`RN-03-15`) e acompanhar segue sendo função do Apoiador cadastrado, na App 08 (`RN-03-16`).
2. **Sai a seção "Necessidades em aberto" da abertura.** As necessidades continuam públicas na
   **porta do convite** (`/quero-participar`, `RF-03-43`), com tudo o que o `RF-03-47` pede.

Decisão nova desce pelo fluxo antes do código: documento 03 §8 → documento 09 → PRD-03 →
change.

## What Changes

- **Documentação (antes do código):** documento 03 §8 (o item "Sem favoritos" deixa de levar
  quem pede para acompanhar à porta; "Como apoiar" deixa de apontar a seção própria; a tabela
  de recortes perde "as necessidades em aberto" do recorte padrão); documento 09 — linha nova
  da decisão de 2026-11-10, e as linhas "Ordem das seções da abertura da vitrine" e
  "'Necessidades em aberto' é seção própria" ajustadas; PRD-03 (retirada do `RF-03-40`,
  §§3, 5.4 item 5, 5.5 item 1, 6.4 e a linha de rastreabilidade da §13); linha nova do
  cronograma.
- **App 06 — páginas individuais:** `ChamadaDeParticipacao` passa a ter **só** "Quero apoiar";
  saem o botão "Quero acompanhar" e o parágrafo que o explicava. Vale para as quatro páginas,
  porque o componente é um só.
- **App 06 — abertura:** sai a seção "Necessidades em aberto" de `pages/index.astro` e o
  componente `NecessidadesEmAberto`. `ListaDeNecessidades` e `useNecessidades` **ficam**: a
  porta do convite os usa.
- **Núcleo:** nada muda. `GET /v1/vitrine/necessidades` segue pública — a porta da vitrine e a
  App 08 a consomem.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-vitrine`: o requisito da chamada nas páginas individuais é substituído por um
  sem ação de acompanhar; o cenário de "sem rastro" deixa de acionar o botão; sai o requisito
  da seção própria das necessidades, e o de "Como apoiar" passa a pôr as necessidades na
  porta do convite.

## Impact

- **Código (App 06):** `convite/ChamadaDeParticipacao.tsx`, `institucional/SecoesInstitucionais.tsx`,
  `pages/index.astro`, a composição de teste `testes/TelaDaVitrine.tsx` e os testes
  `convite`, `semRastro`, `necessidadesEmAberto`, `portfolioERanking` e `saidaDoBuild`.
- **API, núcleo, esteira e configuração:** sem mudança.
- **Achado fora do escopo, levado ao fundador:** o `RF-14-52` ("Apoiador favorita Mestre a
  partir da página pública dele") nunca teve caminho de tela — o botão da vitrine levava à
  porta, não favoritava, e a App 08 só favorita Guerreiro(a) por nick. A remoção não piora
  nada, mas a lacuna segue aberta no PRD-14.
