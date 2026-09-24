# Proposal

**PRD de origem:** PRD-04 — Aula presencial (App 01).
**Cronograma:** linha `—` do bloco do PRD-04 — correção de defeito preexistente, não fatia de
requisito novo, como `2026-09-18-visor-nao-contradiz-a-recusa-da-entrada` e
`2026-09-21-aula-na-entrada-e-erro-de-camada-legivel`.
**Identificadores atendidos:** `RF-04-01`, `RF-04-67`, `RF-04-68`. Nenhum identificador novo:
a separação dos caminhos já é requisito, e o que falta é a apresentação dela.

## Why

A fatia 18 separou presença, equipes, quiz e troca em caminhos próprios, mas a tela da entrada
do Guerreiro(a) continuou se apresentando com o título do caminho da presença nos quatro casos.
Quem escolhe Equipes, Quiz ao Vivo ou Troca por recompensa avulsa cai numa tela visualmente
idêntica à da presença e não tem como saber que está no caminho certo — o `RF-04-01` oferece a
escolha, e a tela seguinte a desmente.

O comportamento está correto: a entrada fora do caminho da presença não registra presença, e a
guarda do `RF-04-68` barra quem não a tem. É defeito de rótulo, não de roteamento — confirmado
pelo fundador, que concluiu a entrada pelo caminho das equipes e chegou às equipes da aula.

## What Changes

- A tela da entrada do Guerreiro(a) passa a anunciar, no título, qual caminho serve. A redação
  é a aprovada pelo fundador na elicitação de 2026-09-24:

  | caminho    | título                      |
  | ---------- | --------------------------- |
  | `presenca` | Quem está chegando?         |
  | `equipes`  | Quem vai formar equipe?     |
  | `quiz`     | Quem vai jogar o Quiz?      |
  | `troca`    | Quem vai trocar recompensa? |

- Vale nas **duas** telas da entrada — a do reconhecimento e a da confirmação por PIN —, que
  hoje repetem o mesmo título fixo.
- O subtítulo de cada uma **não** muda: ele descreve o ato, que é o mesmo nos quatro caminhos.
- Nenhuma mudança de comportamento: o que a entrada faz em cada caminho segue como está.

### Fora do escopo

O que o PRD-04 §3.2 já exclui. Em particular, esta change não altera o registro da presença, a
guarda do `RF-04-68`, a tela inicial do `RF-04-01` nem o caminho do onboarding.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: o requisito "O Guerreiro(a) entra por nick e imagem, e só o
  caminho Presença registra a presença" passa a exigir que a tela da entrada anuncie o caminho
  que serve, em vez de se apresentar igual nos quatro (`RF-04-01`, `RF-04-67`, `RF-04-68`).

## Impact

- `apps/app-01-aula-presencial/src/entrada/TelaDeEntradaDoGuerreiro.tsx` — os dois `Cabecalho`
  da tela, hoje com título fixo.
- `apps/app-01-aula-presencial/src/inicio/inicio.test.tsx` — usa hoje o título da presença como
  marcador de tela, marcador que casa com os quatro caminhos e por isso não pegou o defeito.
- `apps/app-01-aula-presencial/src/entrada/entrada.test.tsx` — cobre a tela alterada.
- `openspec/cronograma-de-fatias.md` — a linha `—` desta correção, no bloco do PRD-04.
- Sem alteração no núcleo, em rota, em contrato de API ou em `docs/`.
