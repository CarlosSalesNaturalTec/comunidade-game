# Proposal

**PRD de origem:** PRD-05 §6, aplicando o documento 15 §§8.1 a 8.4 e o documento 11 §8.2.
**Cronograma:** linha `—` do bloco **Infraestrutura transversal (sem PRD)**.
**Identificadores atendidos:** `RF-05-15`, `RF-05-16`, `RF-05-18`, `RF-05-50`, `RF-05-51`. Nenhum
identificador novo: a carta, o emblema, os badges e o glifo já são norma do documento 15, e o que
cada carta exibe já é norma do documento 11.

**Depende** de duas changes: a do **avatar paramétrico** — a carta exibe o avatar em círculo
ocupando metade da largura (documento 15 §8.1) — e a do **temperamento Arena**, que traz o raio de
`12` px da carta na Arena e o sistema de ícone sobre o qual o glifo de poder é desenhado.

## Why

O documento 15 §8.1 chama a carta do personagem de **átomo da interface**, comum às oito
aplicações, e fixa os valores dela; o documento 11 §8.2 diz o que cada uma das quatro variantes
exibe e o que **nunca** exibe. O §8.2 do documento 15 define o **emblema de nível contável** — uma
marca por nível, cinco e moldura fechada no Mestre Aprendiz —, o §8.3 as **seis silhuetas de
badge** e o §8.4 o **glifo de poder**.

Nenhum dos quatro existe: não há componente de carta, de emblema, de badge nem de glifo de poder em
`comum/react`. O nível aparece como número, os badges como texto, e o emblema que uma criança de 6
anos deveria **contar** não existe.

## What Changes

- `comum/react` ganha os quatro componentes, com os valores do documento 15:

  | Componente        | O que o documento fixa                                                                 |
  | ----------------- | -------------------------------------------------------------------------------------- |
  | Carta             | superfície, borda de 1 px, raio por temperamento, avatar em círculo com metade da largura, nick em Archivo `1,125` rem (§8.1) |
  | Emblema de nível  | número de marcas igual ao nível; cinco e moldura fechada no nível 5; sempre de uma trilha ou poder, nunca global (§8.2) |
  | Badge             | seis silhuetas, uma por família, legíveis a `24` px sem depender de cor (§8.3)          |
  | Glifo de poder    | dentro da silhueta e na moldura de nível, reconhecível a `24` px, com o nome do poder ao lado (§8.4) |

- A **variante Guerreiro(a)** da carta é a única entregue aqui, e ela aparece na **Área do
  Guerreiro(a)**, onde o dado que o documento 11 §8.2 exige já existe: avatar (da change do
  avatar), nick (da sessão), badges e poderes com níveis (`GET /v1/eu/progresso` e
  `GET /v1/eu/trilhas`) e criações originais (o portfólio, já entregue pela fatia 5 do PRD-05).
- O progresso da App 05 passa a apresentar o nível pelo **emblema contável** e os badges pela
  **silhueta da família**, em vez de número e texto.
- **Sem rota nova.** As leituras que a carta precisa já existem e já são consumidas pela App 05.

### Fora do escopo

- As variantes **Mestre, Apoiador e Comunidade Virtual**: cada uma tem tabela de exibição própria no
  documento 11 §8.2 e rotas próprias, e entra em fatia da aplicação que a exibe.
- Adotar a carta nas Apps 01, 03, 06, 07 e 08. Em particular, **a tela das equipes da App 01 não
  recebe carta**: a rota devolve integrante por avatar, nick e papel — sem badges, poderes nem
  desempenho —, e o fundador já decidiu, na linha "Apresentação da lista de comunidades da App 03"
  do documento 09, que **carta pela metade contraria o documento 11**. O mesmo vale aqui.
- A **rotação** da carta (documento 15 §8.1, "onde houver") e o retorno de progresso e conquista:
  fatia da Arena em primeiro plano.
- A página individual que cada card abre (documento 11 §8.2): é da vitrine, no PRD-03.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `camada-visual-comum`: passa a entregar a carta do personagem, o emblema de nível contável, as
  seis silhuetas de badge e o glifo de poder (documento 15 §§8.1 a 8.4).
- `area-do-guerreiro`: o progresso passa a apresentar nível e badges por emblema e silhueta, e a
  Área passa a apresentar a carta do próprio Guerreiro(a) (`RF-05-15`, `RF-05-16`, `RF-05-50`,
  `RF-05-51`).

## Impact

- `comum/react/` — os quatro componentes e as seis silhuetas.
- `comum/react/indice.ts` e `comum/package.json` — a exportação.
- `apps/app-05-guerreiro/src/carteira/MinhaCarteira.tsx` e `src/trilha/Progresso.tsx` — a carta, o
  emblema e as silhuetas.
- Os testes do `comum` e da App 05.
- `openspec/cronograma-de-fatias.md` — a situação desta linha, e a correção do recorte previsto: a
  fatia **não** aplica carta nas telas de equipe.
- `docs/09-topicos-em-aberto-e-sugestoes.md` — a pendência das duas famílias de badge que o
  documento 15 §8.3 declara e o núcleo ainda não tem.
- Sem alteração no núcleo, em rota ou em contrato de API.
