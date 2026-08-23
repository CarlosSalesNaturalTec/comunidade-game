# Minhas turmas e lançamentos do Mestre

Origem: **PRD-09 — Área do Mestre**, §6.6. Quarta fatia do PRD-09.

Atende `RF-09-42`, `RF-09-43`, `RF-09-44`, `RF-09-45`, `RF-09-46`, `RF-09-49`, `RF-09-73` e
`RF-09-74`, sob `RF-01-57`, `RF-01-16`, `RF-01-20`, `RN-01-52` e `RN-01-55`.

## Why

O PRD-09 se chama "autoria **e operação**". As três fatias anteriores fecharam a autoria: o
Mestre escreve trilha, missão e atividade, etiqueta os ODS e publica. **A operação nunca foi
ligada** — hoje um Mestre autor não lista as próprias turmas, não lança a atividade que
propôs e não registra presença no encontro dele.

Não é regra que falta: é porta. Três permissões do Mestre estão na matriz de `permissoes.py`
— `suas_turmas`, `lancamentos_e_pontuacao_negativa_das_suas_atividades` e
`painel_do_dia_na_app_03` — e **nenhuma rota exige nenhuma das três**.
`resultados.regra.registrar_resultado` e `aulas.regra.registrar_presenca` estão escritos,
testados e inalcançáveis por HTTP.

Junto vem a metade que falta do `RF-01-57`. Ele nomeia **dois** fatos desfeitos que debitam
ponto regular: o estorno de registro de coleta invalidado e a **ocorrência de conduta
lançada**. O estorno entrou na change `auditoria-e-estorno-da-coleta`; a conduta nunca
entrou — a spec `pontos-niveis-e-badges` já a registra como "de entrega posterior", e o
`docstring` de `debitar_ponto_regular` confessa "hoje só o estorno". Esta fatia é a entrega
posterior.

O calendário pesa: o Ciclo 01 corre de agosto a dezembro de 2026. Sem esta fatia, a primeira
turma não tem como ser conduzida pelo Mestre que a ministra.

## What Changes

### A leitura das próprias turmas (`RF-09-42`, `RF-09-73`)

`GET /v1/minhas-turmas` devolve ao Mestre em sessão as aulas das suas comunidades e as
atividades **que ele autorou**, separadas pelo `formato` da atividade — presencial do
encontro e on-line entre encontros. Exige `Operacao.suas_turmas`, hoje sem rota alguma.

### O lançamento por atividade (`RF-09-43`, `RF-09-44`, `RF-09-49`, `RF-09-74`)

`POST /v1/atividades/{id}/lancamentos` abre a porta de `registrar_resultado`, que já grava o
desfecho, credita ponto regular e extra e reavalia nível e badge. A recusa do `RF-09-49` já
está dentro dele: `conferir_posse_da_trilha` responde **403** ao Mestre que não é o autor. A
rota aceita a **lista de participantes** de uma vez, o que atende o lançamento da equipe
inteira do `RF-09-74`.

**Não se confunde com `POST /v1/aulas/{id}/lancamentos`**, que existe e continua como está:
aquele é do Admin, é **por aula**, converte as reservas em baixa e leva a aula a realizada
(`RF-02-33`, `RF-02-35`). São dois atos distintos, e o PRD-01 §4 autoriza o Mestre em
"lançamentos e pontuação negativa das suas atividades".

### A presença registrada pelo Mestre, só por confirmação (`RF-09-45`)

`POST /v1/aulas/{id}/presencas` abre a porta de `registrar_presenca`, já idempotente por
aula e Guerreiro(a). O Mestre a alcança **apenas no modo confirmação**, sob
`Operacao.confirmacao_de_identidade_do_guerreiro`, que já está na matriz; o modo
reconhecimento continua sendo do App 01.

O recorte resolve a divergência entre o `RF-09-45`, que dá a presença ao Mestre, e o PRD-01
§4, que não a lista entre as escritas dele — o `RF-01-17` fecha com "sem escrever nas demais
rotas de gestão". Prevalece o PRD-01, e a confirmação de identidade que a matriz já concede é
o caminho legítimo. **Não abre escrita de gestão nova e não altera a matriz.**

### A ocorrência de conduta (`RF-09-46`, fecha `RF-01-57`)

Entidade nova no núcleo, somente inserção, no padrão do `Lancamento` do livro-razão: valor,
data, autor, motivo em texto livre, a aula, a **atividade** e o Guerreiro(a). Ela é a **segunda
causa** de `debitar_ponto_regular`.

Precisa ser entidade porque `PontoRegular` é um `total` corrente, sem histórico, autor nem
motivo — e o `RN-01-52` exige apagar **o motivo** ao fim do ciclo preservando o lançamento
com valor, data e autor. Só cabe em casa própria.

A régua vem da tabela do documento 11 §5, **única fonte do valor**: **5 pontos por ocorrência**,
com **teto de 10 por Guerreiro(a) e por aula presencial**. Quem lança **não arbitra o valor** —
requisição que o traga é recusada. O teto é por pessoa: a ocorrência de um não consome o teto
de outro.

A ocorrência declara a **atividade**, e é dela que a trilha do débito é derivada — atividade →
missão → trilha. É o que dá sentido a "pontuação negativa das **suas atividades**" do PRD-01 §4
e o que faz a recusa de atividade alheia valer também aqui.

O motivo é **texto livre**, sem item do Código de Conduta e sem catálogo: o item é do
`RF-02-38`, da App 03. O débito não deixa o saldo negativo e não derruba nível nem badge
(`RN-01-55`), regras que `debitar_ponto_regular` já aplica.

### A área Minhas turmas na App 09

Lista das turmas separada por formato, tela de lançamento com os participantes e o desfecho
de cada um, confirmação de presença e lançamento da ocorrência de conduta com motivo.

### A pendência que a fatia devolve ao documento 09

O `RN-01-52` **não tem gatilho**: "ao fim do ciclo" pressupõe um fim de ciclo, e o ciclo não
é entidade — é rótulo de configuração (`configuracao.ciclo_rotulo`). Nada no núcleo sabe que
um ciclo terminou. A entidade nasce com o motivo anulável e a leitura preparada para não
devolvê-lo quando apagado, mas **quem apaga** entra no documento 09 como pendência de
decisão. Nenhuma rota de expurgo se inventa aqui.

O mesmo gatilho falta a uma segunda regra: o documento 11 §5 manda a ocorrência **sair do
ranking ao fim do ciclo**, e o ranking público é derivado do ponto regular já debitado. As duas
consequências do fim de ciclo entram na mesma pendência.

### A correção no índice dos PRDs

`docs/prds/index.md` dá o `RF-01-57` por entregue na change `auditoria-e-estorno-da-coleta`,
mas só o estorno foi. Esta fatia fecha a outra metade e o índice passa a dizê-lo.

## Capabilities

### New Capabilities

- `ocorrencia-de-conduta`: o registro somente inserção da conduta lançada pelo Mestre ou pelo
  Admin — valor, data, autor, motivo, aula e Guerreiro(a) —, o débito de ponto regular que
  ele produz e a retenção do motivo pelo ciclo (`RF-09-46`, `RF-01-57`, `RN-01-52`,
  `RN-01-55`).

### Modified Capabilities

- `aula-e-presenca`: ganha a leitura das turmas do próprio Mestre, separada pelo formato da
  atividade, e a porta HTTP da presença, restrita ao modo confirmação quando quem registra é
  o Mestre (`RF-09-42`, `RF-09-45`, `RF-09-73`).
- `resultado-de-atividade`: ganha a porta HTTP do lançamento **por atividade**, do Mestre
  autor, com a lista de participantes num ato só — distinta do lançamento por aula, do Admin,
  que permanece inalterado (`RF-09-43`, `RF-09-44`, `RF-09-49`, `RF-09-74`).
- `pontos-niveis-e-badges`: a ocorrência de conduta deixa de ser "de entrega posterior" e
  passa a ser causa exercitável de débito de ponto regular (`RF-01-57`, `RN-01-55`).
- `area-do-mestre`: ganha a área Minhas turmas — lista, lançamento, presença e ocorrência de
  conduta (`RF-09-42` a `RF-09-46`, `RF-09-73`, `RF-09-74`).

## Impact

**Backend** — `backend/src/nucleo/`:

- `ocorrencias_de_conduta/` (pasta nova): `modelo.py`, `regra.py`, `rotas.py`.
- `pontuacao/regra.py`: `debitar_ponto_regular` passa a servir a segunda causa.
- `resultados/rotas.py` (arquivo novo) e `aulas/rotas.py`: as duas portas novas.
- `principal.py`: dois roteadores novos.
- Migração de banco para a entidade nova.

**Frontend** — `apps/app-09-mestre/`: a área Minhas turmas. Sem pasta nova, sem esteira nova.

**Documentação, no mesmo PR**: `docs/prds/index.md` (situação do PRD-09 e a correção do
`RF-01-57`) e `docs/09-topicos-em-aberto-e-sugestoes.md` §1 (a pendência do expurgo do
motivo).

**Fora do escopo**, conforme o PRD-09 §3.2 e a decisão do fundador nesta fatia: `RF-09-47`
(correção por ajuste que referencia o original — `Resultado` não tem o campo, e a
imutabilidade já vale de fato porque não há rota de edição), `RF-09-50` (o painel do dia é
operado na App 03) e `RF-02-37`/`RF-02-38` (a porta do Admin para a infração e o item do
Código de Conduta é fatia da App 03; o núcleo desta fatia serve as duas).
