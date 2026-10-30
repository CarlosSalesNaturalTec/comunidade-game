# Proposal

**Origem:** PRD-04 — **fatia 31** do bloco do PRD-04 em
`openspec/cronograma-de-fatias.md` ("Entregas pendentes do encontro na App 01").

**Atende:** `RF-09-75`, `RF-09-76` e `RF-07-13` na App 01, no molde do `RF-04-55`; alcança
`RF-04-01`, `RF-04-71`, `RF-04-49` e `RN-02-17`. **Sem identificador novo**, pelo precedente
das fatias 25 a 30 do PRD-04.

**Decisão do fundador, 2026-10-30**, em `docs/09-topicos-em-aberto-e-sugestoes.md` §1, linha
"Entrega da recompensa de marco no encontro".

**Depende** da change `2026-10-30-vinculo-do-mestre-com-a-comunidade`: sem o vínculo do Mestre
a fila sai vazia e a confirmação é recusada em qualquer das duas aplicações.

## Why

A tela da recompensa diz à criança: _"Peça ao seu Mestre no próximo encontro — é ele que
confirma a entrega."_ No encontro, porém, confirmar a entrega **só existe na App 09**, e o
Mestre que está no encontro opera a App 01. Para entregar o kit que a criança acabou de
conquistar, ele teria de largar o aparelho da aula e entrar noutra aplicação, com a criança
na frente.

A troca por recompensa **avulsa** já é presencial ali (`RF-04-55`: "o Mestre entrega o item na
hora e confirma a entrega"). A recompensa **de marco** — a que se conquista, e que a tela da
criança promete — não tem par disso.

## What Changes

- A tela inicial da App 01 ganha, no grupo **"Para quem opera o aparelho"**, o caminho das
  **entregas pendentes do encontro**, ao lado da chave do momento de troca e antes do
  encerramento, que segue sendo o último do grupo.
- O caminho aparece **apenas quando quem abriu a sessão de trabalho é Mestre**, no mesmo molde
  da chave do momento de troca (`RF-04-49`) — o Admin nunca confirma (`RN-02-17`).
- A fila do encontro alcança **somente quem tem presença registrada naquela aula**, e não a
  comunidade inteira: quem o Mestre tem à frente é quem chegou.
- Confirmada a entrega, o recurso sai do **ponto de apoio da aula**, sem seletor — a aula já o
  declara obrigatoriamente (`RF-01-71`) e é nele que o encontro acontece.
- **A App 09 não muda**: mantém em Minhas turmas a fila da **comunidade** inteira, com a
  escolha do ponto de apoio.

## Capabilities

### New Capabilities

Nenhuma. A fila e a confirmação já são comportamento de `recompensa-de-marco`; o que nasce é
o recorte por encontro e o caminho na App 01.

### Modified Capabilities

- `recompensa-de-marco`: a fila ganha o **recorte por aula** — as pendências de quem tem
  presença registrada naquela aula —, e a confirmação passa a aceitar que o ponto de apoio
  seja o **da aula** em vez de escolhido (`RF-09-75`, `RF-09-76`, `RF-07-13`).
- `aplicacao-da-aula-presencial`: o grupo de quem opera o aparelho passa a ter **quatro**
  atos, e a App 01 passa a apresentar e confirmar as entregas pendentes do encontro
  (`RF-04-01`, `RF-04-71`, `RF-04-49`).

## Impact

**Núcleo (`backend/`)** — `recompensas_de_marco/regra.py` e `rotas.py`: a fila passa a aceitar
o recorte por aula, e a entrega, o ponto de apoio derivado dela. Nenhuma entidade nova e
nenhuma migração.

**App 01 (`apps/app-01-aula-presencial/`)** — o caminho novo na `TelaInicial` e a tela da fila
do encontro, sob a sessão de trabalho.

**App 09** — nenhuma mudança.

**Documentação, no mesmo PR** — o **documento 02 §8.1**, cuja tabela manda o Mestre escolher o
ponto de apoio sem distinguir as duas aplicações, passa a dizer que a escolha é da App 09 e
que no encontro o ponto de apoio é o da aula; o PRD-04 §5 ganha o fluxo, e o PRD-07 e o PRD-09
acompanham a distinção. A decisão já está gravada no `docs/09` §1.

**Fora do escopo** — a fila da comunidade na App 09, que já existe e não muda; o catálogo de
qual marco entrega o quê, que segue pendente no PRD-05 §14 e no PRD-09 §14; e qualquer
alteração no vínculo do Mestre, que é a change de que esta depende.
