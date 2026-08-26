# Coleta do território na Área do Guerreiro(a)

Origem: **PRD-05 — App 05: Área do Guerreiro(a)**, §§3.1, 5.4, 6.4 e 9. **Segunda fatia** do
PRD-05. Atende `RF-05-30`, `RF-05-31`, `RF-05-32`, `RF-05-33`, `RF-05-34`, `RF-05-35`,
`RF-05-36`, `RF-05-37`, `RF-05-38`, `RF-05-85` e `RF-05-57`, sob `RN-05-08`, `RN-05-09`,
`RN-05-10`, `RN-05-11`, `RN-05-21` e `RN-05-24`.

## Why

A primeira fatia do PRD-05 abriu a App 05 e parou na porta: a criança entra por nick e imagem
e não faz mais nada. A coleta do território é o **primeiro ato** que ela pode exercer, e é o
único bloco do PRD-05 cujo núcleo o PRD-08 já entregou por inteiro — série, registro por
_multipart_ com origem gravada, faixa que marca "a conferir", interrupção por duas cadências,
invalidação com motivo, locais e solicitação de local. Nenhum outro bloco está nesse estado:
§6.2 e §6.5 esperam autoria e validação que a App 09 ainda não entregou.

Sem esta fatia, a coleta de dados reais — invariante 5 do documento 99 §6, e a razão de o
território ser cidadão de primeira classe no modelo de dados — continua existindo só como
regra testada no núcleo, sem nenhuma criança capaz de alcançá-la.

As quatro leituras que o núcleo ganha aqui não criam regra: derivam do que as capacidades
`serie-de-coleta`, `registro-de-coleta`, `desafio-de-coleta`, `auditoria-da-coleta` e
`solicitacao-de-local` já declaram, e que hoje não tem porta HTTP pela qual o Guerreiro(a)
chegue.

## What Changes

**Núcleo — quatro leituras, nenhuma escrita nova**

- A consulta das próprias séries passa a trazer a **próxima medição** de cada uma, derivada da
  cadência do desafio e da última medição válida (`RF-05-30`, `RN-05-10`).
- Nasce a leitura do **histórico da própria série**: cada registro com data da medição, valor
  ou mídia, origem, situação, pontos creditados e, quando invalidado, o **motivo** que o
  Mestre autor declarou (`RF-05-37`, `RF-05-38`, `RN-05-09`).
- Nasce a leitura dos **desafios de coleta que o Guerreiro(a) pode assumir**: os vigentes cuja
  granularidade exigida cabe no teto da sua Comunidade Virtual — as mesmas condições que a
  abertura da série já confere, agora legíveis antes da tentativa (`RF-05-30`, `RN-05-24`).
- Nasce a leitura das **próprias solicitações de local**, com situação e, quando recusada, o
  motivo — hoje só existe a listagem das abertas, de Admin e Mestre (`RF-05-32`, `RN-05-11`).

**App 05 — o bloco da coleta**

- Lista das séries do Guerreiro(a), com estado, próxima medição e pontos que cada uma está
  rendendo; a série **interrompida** é sinalizada com o histórico preservado e o caminho de
  retomada (`RF-05-30`, `RF-05-36`).
- **Abertura de série** sobre um desafio elegível, escolhendo o **local** entre os cadastrados
  pela gestão — decisão do fundador, 2026-08-26: a abertura é ato do Guerreiro(a) nesta
  aplicação, e é onde o local é escolhido, que é como se lê o `RF-05-31`.
- **Solicitação de local faltante** e acompanhamento da situação até a avaliação (`RF-05-32`).
- **Registro da medição** — digitado, ditado por voz, foto ou vídeo —, com a origem gravada;
  registro dentro da faixa pontua na hora, e fora da faixa entra como "a conferir", com a tela
  explicando por que **sem acusar ninguém** (`RF-05-33`, `RF-05-34`, `RF-05-35`).
- **Histórico da série**, com data e valor de cada registro, e o motivo do que foi invalidado
  (`RF-05-37`, `RF-05-38`).
- **Sem rede, o registro é recusado com o motivo**, e nada fica enfileirado no aparelho
  (`RF-05-85`).
- **Aviso discreto de coleta de dados** nas telas que coletam, com acesso à área detalhada
  (`RF-05-57`) — a coleta é o primeiro bloco da App 05 que coleta dado da criança.

## Capabilities

### New Capabilities

Nenhuma. A fatia estende capacidades existentes: a App 05 já nasceu em
`area-do-guerreiro`, e o território já está descrito pelas capacidades do PRD-08.

### Modified Capabilities

- `area-do-guerreiro`: a App 05 ganha o bloco da coleta — séries, abertura, registro,
  histórico, solicitação de local, recusa sem rede e o aviso de coleta de dados.
- `serie-de-coleta`: a consulta das próprias séries passa a declarar a **próxima medição**.
- `registro-de-coleta`: nasce a leitura do histórico da própria série pelo Guerreiro(a),
  incluindo o motivo do registro invalidado.
- `desafio-de-coleta`: nasce a leitura dos desafios vigentes que o Guerreiro(a) pode assumir.
- `solicitacao-de-local`: nasce a leitura das próprias solicitações, com situação e motivo.

## Impact

**Código**

- `backend/src/nucleo/coletas/` — as três leituras do território (séries com próxima medição,
  histórico da série, desafios elegíveis).
- `backend/src/nucleo/locais/` — a leitura das próprias solicitações.
- `apps/app-05-guerreiro/` — o bloco da coleta, consumindo `comum/`.

**API** — quatro rotas novas sob `/v1`, todas de leitura e todas restritas ao Guerreiro(a) em
sessão; nenhuma rota existente muda de contrato, e `GET /v1/series-de-coleta/minhas` apenas
acrescenta campo à saída.

**Infraestrutura** — nenhuma. A App 05 já tem endereço, esteira e chaves desde a fatia
anterior.

**Fora do escopo**, reproduzindo o que o PRD-05 §3.2 já exclui: o **cadastro de local do
território** é de Admin (App 03 e PRD-08) — aqui só se escolhe entre os cadastrados e se
solicita a inclusão do que falta; a **auditoria e a invalidação** são do Mestre autor do
desafio — aqui só se lê o motivo do que foi invalidado; a **credencial de dispositivo do
sensor** é caminho do PRD-08, não desta aplicação. Trilha, progressão, criação original,
portfólio, pontos extras, catálogo avulso e ranking são fatias próprias.

**Pendências** — a fatia não esbarra na §14 do PRD-05: as duas pendências de lá travam
`RF-05-45` e `RF-05-83`, que estão fora deste recorte.
