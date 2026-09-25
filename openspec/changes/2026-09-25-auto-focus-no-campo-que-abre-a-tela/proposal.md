# Proposal

**PRD de origem:** PRD-04 — Aula presencial (App 01).
**Cronograma:** fatia **19** do bloco do PRD-04.
**Identificadores atendidos:** `RF-04-07`, `RF-04-18`, `RF-04-21`, `RF-04-29`, `RF-04-30`,
`RF-04-60`, `RF-04-61`, `RF-04-69`, `RF-04-70`. Nenhum identificador novo: as telas e os campos
já são requisito, e o que muda é onde o foco começa.

## Why

No encontro, cada atendimento é curto e recomeça do zero: a criança chega, a tela abre e o
primeiro gesto de quem opera é alcançar o campo que aquela tela inteira existe para preencher.
Hoje esse gesto é um toque a mais, em toda tela, em todo atendimento — nenhuma das seis
aplicações declara foco inicial em campo algum. O `RF-04-28` manda voltar à tela inicial ao fim
de cada atendimento, e por isso o custo se paga a cada Guerreiro(a) que chega.

Decisão do fundador de 2026-09-25, na elicitação desta fatia: o campo recebe o foco ao abrir a
tela, nas telas de propósito único do App 01.

## What Changes

- O `Campo` de `comum/react` passa a aceitar **foco inicial** como propriedade **opcional**.
  Nunca por padrão: foco automático em tela que tem conteúdo acima do campo faz quem usa leitor
  de tela começar a leitura no meio, saltando o que veio antes (documento 15 §5).
- A App 01 declara o foco inicial nas telas em que **preencher aquele campo é o propósito da
  tela**:

  | Tela                                                    | Campo               |
  | ------------------------------------------------------- | ------------------- |
  | Cadastro do onboarding                                  | nome                |
  | Entrada do Guerreiro(a), nos quatro caminhos            | nick                |
  | Entrada do Guerreiro(a), confirmação por PIN            | nick                |
  | Formação da equipe da aula                              | nome da equipe      |
  | Troca do nome da equipe                                 | nome novo           |
  | Equipe da trilha                                        | nick do integrante  |
  | Cadastro do responsável mínimo                          | nome do responsável |

- Os **campos seguintes da mesma tela** ficam de fora — nick e nascimento no cadastro, papel na
  equipe, PIN na confirmação. Eles já recebem o foco pelo percurso, e disputar o foco com o
  primeiro campo tiraria o foco de onde a pessoa está.
- Nenhuma mudança de comportamento, de validação, de rota ou de texto de tela.

### Fora do escopo

O que o PRD-04 §3.2 já exclui. Em particular, esta change não altera campo, validação, rótulo
nem fluxo de tela alguma, e não declara foco inicial nas outras cinco aplicações: o `Campo` ganha
a propriedade, e quem a usa é a App 01.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `camada-visual-comum`: o contrato de acessibilidade dos componentes comuns passa a cobrir o
  **foco inicial** — quem monta a tela o declara, o componente nunca o assume, e declarar foco
  não dispensa o contorno de foco visível (documento 15 §5).
- `aplicacao-da-aula-presencial`: as telas de propósito único da App 01 passam a abrir com o
  campo que a tela existe para preencher já focado (`RF-04-07`, `RF-04-18`, `RF-04-21`,
  `RF-04-29`, `RF-04-30`, `RF-04-60`, `RF-04-61`, `RF-04-69`, `RF-04-70`).

## Impact

- `comum/react/Campo.tsx` — a propriedade nova.
- `comum/react/Campo.test.tsx` — cobre o componente alterado.
- `apps/app-01-aula-presencial/src/onboarding/TelaDeCadastro.tsx` — nome.
- `apps/app-01-aula-presencial/src/onboarding/TelaDoResponsavel.tsx` — nome do responsável.
- `apps/app-01-aula-presencial/src/entrada/TelaDeEntradaDoGuerreiro.tsx` — o nick das duas
  formas da entrada.
- `apps/app-01-aula-presencial/src/equipes/TelaDeEquipes.tsx` — nome da equipe.
- `apps/app-01-aula-presencial/src/equipes/TrocaDoNome.tsx` — nome novo.
- `apps/app-01-aula-presencial/src/trilhas/EquipeDaTrilha.tsx` — nick do integrante.
- Os testes das telas alteradas, ao lado de cada uma: `onboarding/onboarding.test.tsx`,
  `onboarding/responsavel.test.tsx`, `entrada/entrada.test.tsx`, `equipes/equipes.test.tsx` e
  `trilhas/trilhas.test.tsx`.
- `openspec/cronograma-de-fatias.md` — a situação da fatia 19.
- Sem alteração no núcleo, em rota, em contrato de API, nas outras cinco aplicações ou em
  `docs/`.
