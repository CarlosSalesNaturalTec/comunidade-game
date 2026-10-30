# Design

## Context

Ver `proposal.md` — Why. O que já existe e molda o desenho:

- `GET /v1/recompensas-de-marco/pendentes` e `POST /v1/recompensas-de-marco/{id}/entregas`
  servem hoje a App 09, recortando pela comunidade e exigindo o ponto de apoio escolhido.
- A App 01 opera sob **sessão de trabalho** — `tokenDeTrabalho`, com `personaIdDeTrabalho` e
  `papelDeTrabalho` —, e já tem o precedente do cartão só do Mestre na **chave do momento de
  troca** (`RF-04-49`), ao lado da medição, que é guardada pelo PIN e não pelo papel.
- A `Aula` declara **ponto de apoio obrigatório** (`RF-01-71`), e a `Presenca` já traz
  `aula_id`, `guerreiro_id` e `anulada_em`.

Depende da change `2026-10-30-vinculo-do-mestre-com-a-comunidade`: a conferência de que a
aula é de uma comunidade do Mestre usa o vínculo que ela cria.

## Goals / Non-Goals

**Goals:**

- O Mestre entrega no aparelho que já está aberto, sem trocar de aplicação.
- A lista do encontro é curta: quem está na frente dele.

**Non-Goals:**

- Mudar a App 09, que mantém a fila da comunidade e a escolha do ponto de apoio.
- Abrir caminho de entrega à criança: o ato é do Mestre, como sempre foi.
- Qualquer coisa no vínculo do Mestre — é a change de que esta depende.

## Decisions

### 1. Recorte por parâmetro, não rota nova

`GET /v1/recompensas-de-marco/pendentes` ganha `aula_id` opcional. Sem ele, a fila é das
comunidades do Mestre, como hoje; com ele, é de quem tem presença registrada e não anulada
naquela aula.

**Alternativa descartada:** `GET /v1/aulas/{id}/entregas-pendentes`. Seria uma segunda rota
para a mesma leitura, com a mesma saída e a mesma regra de alcance — e o recorte por aula é
filtro, não recurso novo.

### 2. O ponto de apoio vem da aula, e a entrada passa a ser exclusiva

`POST /v1/recompensas-de-marco/{id}/entregas` passa a aceitar **ou** `ponto_de_apoio_id`
**ou** `aula_id`, nunca os dois e nunca nenhum — 422 em ambos os desvios. Com `aula_id`, o
ponto de apoio é o declarado na aula, e o lastro é reverificado contra o saldo dele, pela
mesma conferência de hoje.

Isso **altera o documento 02 §8.1**, que manda o Mestre escolher o ponto de apoio sem
distinguir as duas aplicações. A alteração é decisão do fundador de 2026-10-30, registrada no
`docs/09` §1: a escolha segue na App 09, fora de encontro; no encontro, o ponto de apoio é o
da aula, porque é nele que o encontro acontece e a Arena é de uma decisão por tela
(documento 15 §6).

**Alternativa descartada:** manter o seletor também na App 01, preenchido com o da aula. O
fundador decidiu pelo automático.

### 3. A tela nasce na App 01, sem promover o componente da App 09 a `comum/`

**Alternativa descartada:** promover `FilaDeEntregasPendentes` a `comum/`, pelo precedente
das fatias 21 e 29 do PRD-04. Descartada porque as duas telas coincidem só na lista: a da App
09 tem seletor de ponto de apoio, roda sob credencial de persona e recorta por comunidade; a
da App 01 não tem seletor, roda sob a sessão de trabalho e recorta por aula. O que sobraria
em comum é a linha da pendência, pequena demais para justificar a promoção — e promover agora
amarraria duas telas que o PRD trata como momentos distintos.

### 4. O cartão é do Mestre, no molde da chave da troca

O caminho aparece quando `papelDeTrabalho` é Mestre, exatamente como `podeAbrirMomentoDeTroca`
(`RF-04-49`). Aparelho aberto por Admin não o mostra — e, mesmo que mostrasse, o núcleo
recusaria (`RN-02-17`). A guarda é das duas pontas, como já é na troca.

## Risks / Trade-offs

- **A mesma entrega alcançável por duas aplicações** — Mestre na App 09 e Mestre na App 01
  podem confirmar a mesma pendência. → O núcleo já recusa a segunda: a entrega é única por par
  recompensa e Guerreiro(a), e a conferência não muda. A fila da App 01 relê depois de cada
  confirmação, como a da App 09 já faz.
- **A criança sem presença registrada não é alcançável no encontro** — falha de biometria a
  deixa de fora da fila curta. → Decisão do fundador; o Mestre alcança a pendência pela App 09,
  que mantém a comunidade inteira. Fica dito na tela que a fila é do encontro.
- **`aula_id` e `ponto_de_apoio_id` exclusivos** mudam um contrato já publicado em OpenAPI. →
  A App 09 segue enviando `ponto_de_apoio_id` e não muda; nenhum consumidor externo existe.

## Migration Plan

Não se aplica: nenhuma entidade nova, nenhuma coluna, nenhuma migração Alembic. A mudança de
contrato da rota de entrega é aditiva para a App 09, que continua enviando o que já enviava.

## Open Questions

Nenhuma. As duas travas do recorte foram decididas pelo fundador em 2026-10-30 e estão no
`docs/09` §1, linha "Entrega da recompensa de marco no encontro".
