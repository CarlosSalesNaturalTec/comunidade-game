# Proposal

**PRD de origem:** PRD-04 — Aula presencial (App 01).
**Cronograma:** fatia **20** do bloco do PRD-04.
**Identificadores atendidos:** `RF-04-71` e `RN-04-41` — **novos**, a criar na revisão do PRD-04 —,
alcançando `RF-04-05`, `RF-04-21`, `RF-04-23`, `RF-04-28`, `RF-04-63`, `RF-04-66`, `RN-04-37` e
`RN-04-38`.

**Depende** do PR de revisão do PRD-04, que cria os dois identificadores. Mesma dependência da
fatia 14, que também nasceu de decisão nova do fundador antes de o PRD a registrar.

## Why

**Sair.** A App 01 é a única das seis aplicações sem saída da sessão. As Apps 03, 05, 07, 08 e 09
todas a oferecem; aqui o `sair` existe no aparelho — `ConteudoDoAparelho` o tem — e nunca chega à
tela. Fechar a sessão de trabalho hoje exige limpar o `sessionStorage` à mão ou fechar a aba. O
`RF-04-05` põe a sessão de trabalho na janela da aula e o `RN-04-29` a derruba com ela, mas quem
abriu não tem como encerrá-la antes: aparelho que troca de mão no encontro continua aberto no nome
de quem saiu.

**PIN na bancada.** A medição do limiar grava o número que decide se o reconhecimento facial
funciona naquele ponto de apoio (`RF-04-66`), e hoje o caminho abre com a sessão de trabalho e mais
nada — sem adulto no ato. É a mesma razão que levou o `RN-04-37` a exigir o PIN na confirmação de
identidade: o aparelho fica na mesa, aberto, e a sessão sozinha não prova presença de quem
responde pelo ato.

Decisões do fundador de 2026-09-25: a saída existe **só na tela inicial** e é confirmada pelo PIN
de quem abriu o aparelho; a bancada passa a pedir o mesmo PIN; a conferência é a que **já existe no
aparelho**, sem rota nova no núcleo; e o bloqueio de cinco erros é **um só**, compartilhado com a
confirmação de identidade.

## What Changes

- A tela inicial passa a oferecer **encerrar a sessão de trabalho**. Só ali: é a tela que aparece
  entre atendimentos, e a criança que apertasse Sair no meio do dela derrubaria a sessão do Mestre
  — que sem rede não volta, porque reabrir exige login Google.
- Encerrar pede o **PIN de quem abriu o aparelho**, conferido contra o verificador que a sessão de
  trabalho já guarda (`RN-04-38`). Não há rota nova: o núcleo não tem porta que confira PIN
  sozinho, e criar uma foi descartado pelo fundador.
- A **bancada de medição** passa a pedir o mesmo PIN antes de abrir.
- O **contador de cinco erros é o mesmo** dos três atos. PIN já bloqueado recusa os três, e errar
  em qualquer um deles conta para todos.
- PIN **bloqueado** recusa encerrar e recusa a bancada, e a tela SHALL dizer como fechar o aparelho
  mesmo assim: a sessão de trabalho vive em `sessionStorage`, e fechar a aba a encerra. Sem essa
  frase, PIN bloqueado deixaria o aparelho sem saída nenhuma.
- Quem **não tem PIN cadastrado** passa nos dois atos novos, com o aviso que o aparelho já
  apresenta desde a fatia 16 — trancar a saída e o diagnóstico por uma configuração que se resolve
  na App 09 deixaria o encontro pior do que está.
- Encerrar com a **fila local de presença não vazia** avisa antes: sincronizar exige o token de
  trabalho (`RF-04-23`, `RF-04-25`), e o que está na fila só sai quando alguém reabrir o aparelho
  naquela aula. Nada se perde — a fila vive em `localStorage` —, mas quem sai precisa saber.

### Fora do escopo

O que o PRD-04 §3.2 já exclui. Em particular:

- **Rota nova no núcleo** para conferir PIN. Descartada pelo fundador; com ela, a exigência
  passaria a valer para o núcleo, e sem ela vale para a tela.
- Mudar o que a bancada **faz** depois de aberta, ou o que a gravação do limiar leva ao núcleo.
- Mudar a confirmação de identidade do `RF-04-21`, que já pede PIN.
- Saída da sessão do **Guerreiro(a)**: ela já termina a cada atendimento pelo `RF-04-28`.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: a tela inicial passa a encerrar a sessão de trabalho com o PIN de
  quem a abriu (`RF-04-71`, `RN-04-41`), e a bancada de medição passa a exigir o mesmo PIN antes de
  abrir (`RF-04-63`, `RF-04-66`, `RN-04-41`).

## Impact

- `apps/app-01-aula-presencial/src/inicio/TelaInicial.tsx` — a saída e a guarda da bancada.
- `apps/app-01-aula-presencial/src/sessao-de-trabalho/AparelhoDaAula.tsx` — o `sair` passa à tela.
- `apps/app-01-aula-presencial/src/pin/pinDeConfirmacao.ts` — se a conferência de PIN por um ato
  qualquer precisar sair da tela da entrada para um lugar comum aos três.
- `apps/app-01-aula-presencial/src/fila/filaDePresenca.ts` — a leitura de quantos itens a fila
  guarda, para o aviso da saída.
- `apps/app-01-aula-presencial/src/inicio/inicio.test.tsx`, `src/bancada/bancada.test.tsx` e
  `src/fila/fila.test.tsx` — cobrem as telas alteradas.
- `openspec/cronograma-de-fatias.md` — a situação da fatia 20.
- `docs/prds/prd-04-aula-presencial.md` e `docs/09-topicos-em-aberto-e-sugestoes.md` — no PR de
  revisão do PRD-04, que cria `RF-04-71` e `RN-04-41` e grava a decisão nova.
- Sem alteração no núcleo, em rota ou em contrato de API.
