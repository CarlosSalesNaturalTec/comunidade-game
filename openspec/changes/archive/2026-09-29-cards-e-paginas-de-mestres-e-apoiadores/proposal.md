# Proposal

Origem: **PRD-03 — Vitrine pública (App 06)**, **fatia 7** do
`openspec/cronograma-de-fatias.md`, "Cards e páginas de Mestres e Apoiadores".

Atende `RF-03-02` (parte), `RF-03-07`, `RF-03-10`, `RF-03-55`, `RF-03-56`, `RF-03-57`,
`RF-03-66`, `RN-03-18` e `RN-03-26`. As duas decisões novas acrescentam ao PRD-03 os
identificadores `RF-03-79`, `RF-03-80`, `RN-03-36` e `RN-03-37`, que esta fatia também atende. Fecha a pendência do `RF-14-52` — a página pública de
onde o Apoiador favorita o Mestre — e o pedaço que a fatia 2 deixou em aberto na seção de
poderes: os Mestres responsáveis de cada poder.

## Why

Das seis seções de cards do `RF-03-02`, a vitrine já publica Guerreiros e Guerreiras,
poderes e comunidades. **Mestres e Apoiadores não existem em público**: não há rota, não há
card e não há página individual. É a ausência que segura três coisas ao mesmo tempo — a
prova pública de habilidade e de apoio que o `RF-03-07` exige, o lastro em moedas que o
documento 04 §2 manda mostrar, e o alvo do favorito de Mestre do `RF-14-52`, que o PRD-14
deixou esperando por esta fatia.

## What Changes

- **Duas rotas públicas novas** no núcleo: `GET /v1/vitrine/mestres` e
  `GET /v1/vitrine/apoiadores`, cada uma com o par listagem e leitura individual, sem token
  de sessão e sob a chave de aplicação, como as demais rotas da vitrine.
- **As variantes Mestre e Apoiador da carta** na camada visual comum — as duas que a fatia
  transversal de 2026-09-25 deixou "em fatia própria de cada uma".
- **Duas seções e duas páginas individuais** na App 06, com a chamada "Quero participar" que
  o `RF-03-39` pede em toda página individual — o requisito saiu parcial da fatia 6
  justamente por faltarem estas duas.
- **Os Mestres responsáveis na seção de poderes**, derivados do autor das trilhas publicadas
  de cada poder, cada um com link para a página individual do Mestre.
- **Portão de publicação do Apoiador**: só aparece quem tem aporte homologado (`RF-03-57`),
  o total sai sempre em moedas e nunca em reais (`RF-03-10`, `RN-03-18`, `RN-03-26`), e
  abaixo do piso de 10 moedas o card usa o avatar padrão do projeto (`RF-03-66`).

**Quatro decisões do fundador de 2026-09-29** entram com esta fatia. Duas são decisão nova e
descem pelo fluxo da hierarquia — documento-fonte, documento 09 e PRD — antes de virar
código:

1. **Adulto sem nick aparece pelo nome.** O nick é opcional para Mestre e Apoiador, e o
   documento 11 §8.2 exige nick nas duas variantes da carta. A vitrine passa a exibir o
   **nome** da persona quando não houver nick. Muda o documento 11 §8.2 e acrescenta ao
   PRD-03 o `RF-03-79` e o `RN-03-36`.
2. **A efetividade do Apoiador sai em público com trilha e período.** A capacidade
   `efetividade-do-apoio` é do próprio Apoiador; a projeção pública leva os desafios extras
   propostos, quantos foram concluídos, a trilha e o período — nunca nick, avatar ou dado de
   quem concluiu, nunca reais. Muda o documento 11 §8.2 e acrescenta ao PRD-03 o `RF-03-80`
   e o `RN-03-37`.
3. As **áreas de habilidade do Mestre** derivam da área do conhecimento das trilhas
   publicadas de autoria dele — deriva de dado que já existe, sem campo novo.
4. Os **Mestres responsáveis do poder** derivam do autor das trilhas publicadas do poder, e
   a seção leva o link para a página individual de cada um.

## Capabilities

### New Capabilities

- (nenhuma)

### Modified Capabilities

- `leitura-publica-da-vitrine`: as duas rotas públicas novas de Mestre e de Apoiador, o
  portão do aporte homologado, o total em moedas, o piso do avatar, o nome no lugar do nick
  ausente, a projeção pública da efetividade e os Mestres responsáveis na leitura de poderes.
- `camada-visual-comum`: as variantes **Mestre** e **Apoiador** da carta, com o que o
  documento 11 §8.2 atribui a cada uma, a moldura comum do Apoiador e o avatar padrão no
  lugar do que falte.
- `aplicacao-da-vitrine`: as seções e as páginas individuais de Mestre e de Apoiador, a
  chamada "Quero participar" nelas e os Mestres responsáveis na seção de poderes.

`favorito-do-apoiador` **não muda**: esta fatia fecha a pendência do `RF-14-52` entregando o
alvo público do favorito, sem tocar em requisito daquela capacidade.

## Impact

- **Núcleo:** `backend/src/nucleo/vitrine/` — rotas e projeções novas; leitura de
  `Persona`, `Nick`, `ArtefatoComprobatorio`, `Trilha`, `Poder`, `Aporte`, `SeloDoApoiador`
  e `DesafioExtra`, mais `moedas_acumuladas_de` e `contagem_de_absorcoes_de`, que já
  existem. **Nenhuma entidade nova e nenhuma escrita.**
- **Camada comum:** as duas variantes da carta, e nada mais.
- **App 06:** seções, páginas individuais e a seção de poderes já existente.
- **Documentação:** documento 11 §8.2 (as duas decisões novas), documento 09 §1, PRD-03,
  `docs/prds/index.md` e a linha da fatia 7 no cronograma.

## Fora do escopo

O que o PRD-03 §3.2 já exclui, e mais, por recorte da fatia:

- **A seção de batalhas** do `RF-03-02` — o dado é do PRD-10 e `/vitrine/batalhas` não
  existe (decisão do fundador de 2026-09-26, registrada no cronograma).
- **A Área do Apoiador Desenvolvedor** (`RF-03-67` a `RF-03-77`), que é a fatia 8.
- **Qualquer escrita sobre Mestre ou Apoiador** — editar a própria página é ato das Apps 09
  e 08, nunca da vitrine (PRD-03 §4).
- **A página individual do poder.** A seção de poderes recebe os Mestres responsáveis; o
  poder segue sem página própria, como a fatia 6 registrou.
