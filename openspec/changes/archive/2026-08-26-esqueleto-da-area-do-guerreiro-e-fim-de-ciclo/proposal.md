# Esqueleto da Área do Guerreiro(a) e fim de ciclo

Duas fatias num PR só, por decisão do fundador. Elas não compartilham código nem PRD.

**Fatia A** — origem: **PRD-05 — App 05: Área do Guerreiro(a)**, §6.1. Primeira fatia do
PRD-05. Atende `RF-05-01`, `RF-05-02`, `RF-05-03`, `RF-05-04`, `RF-05-05`, `RF-05-06`,
`RF-05-07` e `RF-05-71`, sob `RN-05-01` e `RN-05-02`.

**Fatia D** — origem: **PRD-02 — Frontend de gestão**, §§6.1 e 9. Atende `RF-02-99` e
`RF-02-100`, sob `RN-02-30`.

## Why

**Fatia A.** O PRD-05 está liberado pelo documento 99 §9 desde a quinta entrega e não tem
uma linha de código. Seis dos seus oito blocos de requisito já têm regra pronta e testada no
núcleo — coleta, criação original, recompensas, acervo, sugestões e apoio escolar —, e nenhum
deles alcança uma criança, porque não existe aplicação onde ela entre. Abrir a pasta com o
bloco da entrada é o menor recorte que destrava todos os outros: a sessão do Guerreiro(a) é
pré-requisito de cada tela do PRD-05.

O núcleo não precisa de nada novo aqui. `POST /v1/sessoes/guerreiro`,
`POST /v1/sessoes/guerreiro/confirmacao`, `DELETE /v1/sessoes/atual` e `GET /v1/eu` estão no
ar desde a change `sessao-do-guerreiro-e-biometria`, com os quatro requisitos da capacidade
`sessao-do-guerreiro` — inclusive a duração declarada na implantação, sem padrão no código.
É o mesmo desenho que a primeira fatia do PRD-04 usou para o App 01: a porta existia, faltava
quem batesse nela.

**Fatia D.** O fim de ciclo foi decidido na elicitação de 2026-08-25 e gravado no documento 09
— ato isolado de Admin, que encerra o ciclo corrente e nada mais. Nenhuma linha de código
existe. Sem ele, o motivo da ocorrência de conduta — descrição de má conduta de criança, o
texto mais sensível do produto — **não tem como ser apagado nunca**: a capacidade
`ocorrencia-de-conduta` já declara que o motivo tem guarda limitada ao ciclo, e não há gatilho
que a cumpra. É dívida de LGPD, não funcionalidade nova.

## What Changes

**Fatia A — App 05, entrada e sessão**

- Nasce `apps/app-05-guerreiro`, **aplicação separada** (documento 03 §1.2), com endereço
  próprio: alvo de _hosting_ no `firebase.json` e no `.firebaserc`, e workflow
  `app-05-deploy.yml`. O `frontend-ci.yml` já cobre `apps/**` — a esteira de verificação não
  muda.
- Entrada por nick e imagem contra a conferência biométrica do núcleo (`RF-05-01`,
  `RN-05-01`). A prova de vivacidade e o descritor facial saem portados de
  `apps/app-01-aula-presencial/src/biometria/`; ao núcleo vai só o descritor.
- Recusa de aparelho sem câmera, explicada em linguagem de criança de 6 anos (`RF-05-02`).
- Sessão assistida por Mestre ou Admin presente, nos dois casos previstos: conferência que
  falhou (`RF-05-03`) e Guerreiro(a) que ainda não tem imagem gravada (`RF-05-04`,
  `RN-05-02`).
- Encerramento ao sair e por inatividade, com aviso um minuto antes e opção de continuar
  (`RF-05-05`, `RF-05-71`), e troca de sessão entre duas crianças sem reiniciar a aplicação
  (`RF-05-07`).
- Nenhuma imagem de Guerreiro(a) fica no aparelho compartilhado (`RF-05-06`).
- A aplicação nasce **inteiramente autenticada**: não há tela de visitante.

**Fatia D — fim de ciclo**

- Nasce o ato de Admin que encerra o ciclo corrente, isolado: **não** declara o ciclo
  seguinte, que é declaração à parte na implantação (`RF-02-99`).
- O ato expurga o motivo das ocorrências de conduta do ciclo, preservando valor, data e autor
  do lançamento (`RF-02-100`) — cumpre a guarda que a capacidade `ocorrencia-de-conduta` já
  declara e nunca teve como executar.
- As ocorrências expurgadas saem do **ranking público**; o débito permanece no saldo, porque
  o débito não desfaz percurso (`RF-02-100`).
- O encerramento **não congela indicador**: os quatro da lista pública de comunidades seguem
  apurados no instante da consulta (`RN-02-30`).
- A App 03 ganha a tela do ato, com a confirmação que o seu caráter irreversível exige.

## Capabilities

### New Capabilities

- `area-do-guerreiro`: a App 05 — nesta fatia, só a entrada e a sessão no aparelho
  compartilhado do ponto de apoio, incluindo os dois caminhos de sessão assistida, o
  encerramento por inatividade e a garantia de que nenhuma imagem fica no aparelho.
- `fim-de-ciclo`: o ato de Admin que encerra o ciclo corrente — o seu isolamento (não declara
  o ciclo seguinte), a irreversibilidade e a proibição de congelar indicador.

### Modified Capabilities

- `ocorrencia-de-conduta`: o expurgo do motivo ganha caminho de execução. A capacidade já
  declara que o motivo tem guarda pelo ciclo e que o campo é anulável; falta dizer **quem**
  anula e como isso convive com a regra de somente inserção, que hoje recusa todo `UPDATE`.
- `leitura-publica-da-vitrine`: o ranking público deixa de contar o débito das ocorrências de
  ciclo encerrado.
- `aplicacao-de-gestao`: a App 03 ganha a tela do encerramento do ciclo.

## Impact

**Código**

- Nova pasta `apps/app-05-guerreiro`, consumindo `comum/` (tokens, fontes, cliente de API,
  componentes) — nenhuma dependência nova de topo.
- `backend/src/nucleo/ocorrencias_de_conduta/` — o caminho do expurgo, contra as travas de
  imutabilidade do ORM e do _trigger_.
- `backend/src/nucleo/vitrine/` — o ranking passa a descontar as ocorrências expurgadas.
- `apps/app-03-gestao/` — a tela do ato.

**Infraestrutura**

- `firebase.json`, `.firebaserc` e `.github/workflows/app-05-deploy.yml`: o endereço e a
  esteira de deploy da App 05. Duas chaves de aplicação novas — uma por ambiente — semeadas
  na implantação, como toda aplicação do projeto.

**Fora do escopo**, reproduzindo o que os PRDs já excluem: nesta fatia a App 05 não percorre
trilha, não registra coleta, não entrega criação e não consulta ranking — cada um é fatia
própria. O cadastro do Guerreiro(a) e a captura da imagem continuam no App 01 (PRD-05 §3.2), e
a formação de equipe também. O ato de fim de ciclo não declara o ciclo seguinte, não congela
indicador e não desfaz débito.

**Pendências** — nenhuma das duas fatias esbarra na §14 do PRD-05 nem na do PRD-02. As duas
pendências do PRD-05 travam `RF-05-45` e `RF-05-83`, que estão fora deste recorte. A duração
da sessão do Guerreiro(a) é parâmetro de implantação, já exigido pelo núcleo sem valor padrão.
