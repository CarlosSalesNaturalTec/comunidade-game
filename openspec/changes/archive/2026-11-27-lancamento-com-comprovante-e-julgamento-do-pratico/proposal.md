# Proposal

**Origem:** PRD-09, fatia 41 de `openspec/cronograma-de-fatias.md`, aberta por esta change.
**Identificadores:** `RF-09-43`, `RF-09-44`, `RF-09-49`, `RF-09-74` (revisto), `RF-09-117`,
`RF-09-133` a `RF-09-135`, `RN-09-16`, `RN-09-18`, `RN-09-52` a `RN-09-55`, e os novos
`RF-09-148` a `RF-09-151` e `RN-09-64` a `RN-09-66`, a criar na revisão do PRD-09.
**Decisões do fundador de 2026-11-27**, em `/opsx:propose`:

1. A seção **Lançar resultado de uma atividade**, na tela Presença e ocorrência, deixa de listar
   as atividades com um botão **Lançar** ao lado e vira **formulário no molde da ocorrência de
   conduta**: um _select_ escolhe a atividade, e o Guerreiro(a) é informado **pelo nick**, nunca
   pelo identificador.
2. O lançamento passa a ser **um Guerreiro(a) por envio** — revisão do `RF-09-74` na App 09. A
   API segue aceitando a lista, que a App 03 usa.
3. O campo de texto **Produção** sai da tela: a produção passa a ser o **comprovante** do
   Resultado, **obrigatório**, numa das **seis formas** — texto, imagem, áudio, vídeo, arquivo
   ou link externo. A regra "toda atividade exige produção" (documento 11 §2.2) fica intacta.
4. No mesmo envio, o Mestre registra o **julgamento do desafio prático da missão da
   atividade** — cumpriu, publicável e motivo. É **obrigatório** sempre que aquela missão tem
   desafio prático que o Guerreiro(a) ainda **não cumpriu**.
5. Havendo declaração do Guerreiro(a) aguardando o Mestre, o julgamento recai **sobre ela**.
   Não havendo — ou estando recusada —, o Mestre **declara em nome do Guerreiro(a)** usando o
   comprovante do lançamento e julga no mesmo ato. Comprovante em forma **diferente** da que o
   prático aceita é **recusado**.
6. O comprovante é lido pelo **Mestre autor** e pelo **Admin**: a tela da aula passa a mostrar
   os resultados lançados nela, com o comprovante. A leitura pelo Guerreiro(a) fica para fatia
   própria.

## Why

Hoje a seção lista as atividades com um botão cada, leva a uma segunda tela que pede o
**identificador técnico** do Guerreiro(a) — o que o `RN-09-18` e a própria tela vizinha já
evitam — e um campo **Produção** de texto livre que nada comprova. O julgamento do desafio
prático fica numa bancada separada, longe do encontro em que o Mestre viu a criança cumprir, e
quem escolheu entregar ao Mestre no encontro depende de ele lembrar de ir até lá.

## What Changes

- **Núcleo — comprovante do Resultado:** `Resultado` ganha o **tipo do comprovante** e as
  colunas da mídia; `producao` passa a guardar só o texto ou o endereço. Texto e link vão no
  próprio lançamento; imagem, áudio, vídeo e arquivo sobem **antes**, por sessão de envio
  retomável aberta pelo Mestre, e o lançamento referencia o envio concluído. Mesma lista de
  tipos e mesmos tetos da criação original. O campo `producao` em texto continua aceito, como
  comprovante em texto, para a App 03 seguir funcionando sem mudança.
- **Núcleo — julgamento no lançamento:** cada participante do ato por atividade aceita
  `julgamento_do_pratico`. Exigido quando a missão tem prático não cumprido pelo Guerreiro(a);
  recusado (422) quando não há o que julgar. Julga a declaração pendente pela regra já vigente,
  ou grava a declaração **em nome do Guerreiro(a)** com o comprovante e a julga — tudo na mesma
  transação do Resultado.
- **Núcleo — leituras:** a situação do prático de um Guerreiro(a) numa missão, para a tela
  saber se pede o julgamento; os resultados de uma aula, com o comprovante; e os bytes do
  comprovante — ao Mestre autor e ao Admin.
- **App 09:** a seção vira formulário único na tela da aula — atividade, nick, comprovante,
  momento, desfecho e, quando exigido, o julgamento com o critério de aceite e a entrega do
  Guerreiro(a) à vista. `TelaDeLancamento.tsx` sai. Nasce a lista **Lançados nesta aula**.
- **Documentação:** documento 11 §4 (o que é a produção do Resultado), documento 09 §1 (a
  decisão, com a revisão do `RF-09-74`), PRD-09 (requisitos novos e revistos), cronograma.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `resultado-de-atividade`: a produção vira comprovante em seis formas, com mídia por envio
  prévio; o ato por atividade aceita o julgamento do prático e o exige quando cabe; nascem as
  leituras dos resultados da aula e dos bytes do comprovante.
- `desbloqueio-da-missao`: o prático passa a admitir a declaração feita pelo Mestre autor em
  nome do Guerreiro(a), no lançamento, com o comprovante na forma aceita; e a leitura da
  situação do prático de um Guerreiro(a) para o Mestre autor.
- `area-do-mestre`: a tela do lançamento — _select_, nick, um por envio, comprovante,
  julgamento e a lista dos lançados.

## Impact

- **Backend:** `nucleo/resultados/` (modelo, regra, rotas), `nucleo/trilhas/regra.py` (declarar
  em nome, situação do prático), uma migração Alembic.
- **App 09:** `turmas/TelaDaAula.tsx`, `turmas/api.ts`, `App.tsx` (rota da tela removida),
  `turmas/turmas.test.tsx`; `TelaDeLancamento.tsx` removida.
- **App 03:** nenhuma mudança — `producao` em texto segue aceito.
- **Fora do escopo:** leitura do comprovante pelo Guerreiro(a) na App 05; lançamento por
  equipe na App 09; o lançamento por aula do Admin; edição de Resultado (`RF-09-47`).
