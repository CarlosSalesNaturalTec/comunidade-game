# Proposal

**PRD de origem:** PRD-02 §10 (camada visual comum) e PRD-04 §10, aplicando o documento 15 §§6 e
11.1.
**Cronograma:** linha `—` do bloco **Infraestrutura transversal (sem PRD)** — correção de
contradição com o documento 15 e com o invariante 24, não fatia de requisito novo, como
`2026-09-06-camada-visual-densa-e-navegacao-comum` e
`2026-09-07-bloco-recolhivel-e-marca-de-gravacao`.
**Identificadores atendidos:** `RF-04-01` (a tela inicial da App 01, que recebe os glifos).
Nenhum identificador novo: o temperamento e o sistema de ícone já são norma do documento 15, e o
que falta é cumpri-los.

## Why

O documento 15 §6 põe as Apps 01, 04, 05 e 06 no temperamento **Arena**, e o documento 09 registra
a decisão. As duas que existem — App 01 e App 05 — declaram `data-temperamento="operacao"` no
`index.html`. O invariante 24 exige que o temperamento valha para a **aplicação inteira**; as duas
aplicações das crianças declaram o temperamento das telas de operação de adulto.

A camada de tema da Arena **nunca foi escrita**. O comentário de `comum/tokens.css` diz que ela
"entra quando a primeira aplicação daquele temperamento precisar dela", e esse momento passou duas
vezes calado — a App 01 em agosto, a App 05 em seguida. O `index.css` da App 05 chega a citar
"documento 15 §6, 'caso que dimensiona' do temperamento Arena" num comentário, enquanto o
`index.html` ao lado declara Operação: a intenção era Arena desde o começo, e só a declaração
ficou para trás.

Duas medições feitas na elicitação desta fatia dizem o tamanho real do defeito, e a `proposal` as
registra para não prometer o que a change não entrega:

- `--densidade` é consumido **somente pela App 03**, em nove folhas do temperamento Operação.
- `--raio-carta` **não tem consumidor nenhum** no repositório.
- `--duracao` é consumido pelas duas Apps Arena, na regra universal de `transition-duration` do
  `index.css` de cada uma.

Ou seja: a declaração errada **não tem efeito visual hoje**, porque os tokens de tema que ela
selecionaria quase não são lidos. Corrigi-la é fechar a contradição antes de a primeira carta e o
primeiro retorno de conquista serem escritos sobre a base errada — e não é o que o fundador vai
ver na tela. O que ele vê é o **sistema de ícone do documento 15 §11.1**, que entra junto: os seis
caminhos da tela inicial da App 01 são hoje botões só de texto.

Decisão do fundador de 2026-09-25, que descartou degradê, efeito neon e emoji em favor do que o
documento 15 já define: o §3 fixa cor chapada sem gradiente, o §11.1 exige ícone SVG servido pelo
próprio domínio com rótulo junto, e o princípio 6 veda requisição a terceiro.

## What Changes

- `comum/tokens.css` ganha a camada de tema `[data-temperamento="arena"]`, com o que o documento
  15 §6 fixa em número para a Arena: **raio de carta de `12` px** e **duração de `300` ms**.
- A Arena **não declara `--densidade`**: o documento 15 §6 descreve a densidade da Arena como
  "baixa: poucos elementos, uma decisão por tela" — princípio de composição, sem número —, e o
  token só é lido pelas listas densas da Operação. Inventar um valor aqui seria criar regra num
  artefato. Entra como pendência no documento 09.
- As Apps 01 e 05 passam a declarar `data-temperamento="arena"` no `index.html`.
- `comum/react` ganha o **sistema de ícone** do documento 15 §11.1: SVG embutido, servido pelo
  próprio domínio junto do pacote da aplicação, grade de `24` px, traço de `2` px com ponta e
  junta arredondadas, sem preenchimento, cor herdada por `currentColor`, e **sempre** acompanhado
  de rótulo textual.
- Os seis caminhos da tela inicial da App 01 passam a apresentar glifo **ao lado do rótulo que já
  têm** — nunca em lugar dele:

  | Caminho             | Glifo                             |
  | ------------------- | --------------------------------- |
  | Onboarding          | pessoa com sinal de mais          |
  | Presença            | visto dentro de círculo           |
  | Equipes             | duas silhuetas lado a lado        |
  | Quiz ao Vivo        | balão de fala com interrogação    |
  | Medição do limiar   | mira com escala                   |
  | Troca por recompensa| duas flechas em sentidos opostos  |

### Fora do escopo

O que o PRD-04 §3.2 já exclui. Em particular, esta change **não** entrega:

- A **carta** do documento 15 §8.1, a ilustração em primeiro plano e a imagem de comunidade ao
  fundo, que o documento 15 §6 atribui à Arena. Elas exigem conteúdo gráfico que não existe no
  repositório e são fatia própria.
- O **retorno de progresso e conquista** da Arena: a change declara a duração que ele usará,
  não o retorno.
- Glifo nas demais telas da App 01, na App 05 e nas quatro aplicações da Operação.
- Degradê, efeito neon, sombra em botão e emoji — descartados pelo fundador, por contrariarem o
  documento 15 §3 e §11.1.
- Mudança de raio dos botões e dos caminhos: `.cg-caminho` usa `--raio-campo`, e o documento 15
  §6 fixa `12` px para a **carta**, que o caminho não é.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `camada-visual-comum`: passa a declarar **os dois** temperamentos, e a exigir que cada
  aplicação declare o que o documento 15 §6 lhe atribui; e passa a entregar o **sistema de
  ícone** do documento 15 §11.1.
- `aplicacao-da-aula-presencial`: os caminhos da tela inicial passam a apresentar glifo ao lado
  do rótulo (`RF-04-01`).

## Impact

- `comum/tokens.css` — a camada de tema da Arena.
- `comum/tokens.test.ts` — cobre os tokens declarados.
- `comum/react/` — o componente de ícone e os seis glifos.
- `comum/react/indice.ts` e `comum/package.json` — a exportação do que nasce.
- `apps/app-01-aula-presencial/index.html` e `apps/app-05-guerreiro/index.html` — a declaração do
  temperamento.
- `apps/app-01-aula-presencial/src/inicio/TelaInicial.tsx` e `src/index.css` — os caminhos com
  glifo.
- `apps/app-01-aula-presencial/src/inicio/inicio.test.tsx` — cobre a tela alterada.
- `docs/09-topicos-em-aberto-e-sugestoes.md` — a pendência do valor de densidade da Arena.
- `openspec/cronograma-de-fatias.md` — a situação desta linha.
- Sem alteração no núcleo, em rota ou em contrato de API.
