## Why

Origem: **PRD-07 — Economia de recursos e livro-razão**, quinta fatia.

As quatro fatias anteriores construíram o livro-razão inteiro — aporte, lançamento, saldo,
reserva, baixa e necessidade publicada — e **ninguém consegue ver nada disso**. O provedor não
sabe quanto sustentou, o visitante não sabe o que a plataforma movimentou e o Apoiador não tem
a leitura dos próprios aportes que o documento 04 §1 promete como "reconhecimento público de
quem sustenta o projeto".

Esta fatia é a superfície de leitura do que já está gravado. É também o que torna a hipótese
**H3** do Ciclo 01 verificável — lastro registrado contra recursos necessários às atividades
previstas —, a métrica de ciclo declarada na §12 do PRD-07.

Requisitos atendidos: `RF-07-10`, `RF-07-16`, `RF-07-17`, `RF-07-26`.
Regras aplicadas: `RN-07-05`, `RN-07-15`, `RN-07-19`, `RN-07-31`.

## What Changes

**O Poder Sustentador do provedor** (`RF-07-10`), derivado dos **lançamentos** do livro-razão —
não da soma de `Aporte.valor_em_moedas`. É o que mantém o número recontável a partir da fonte
única (`RN-07-15`) e o que permite ao ressarcimento de fatia futura revertê-lo por lançamento,
sem reescrever a derivação.

**A contagem de absorções** exibida na página pública do Mestre ou Admin (`RF-07-26`), derivada
dos **aportes** de forma `absorcao` — e por isso um número **independente** do Poder
Sustentador. O PRD-07 §12 exige que o ressarcimento pago devolva o Poder Sustentador ao valor
anterior **e** que o selo continue contando aquela absorção: são dois números que se separam, e
nascem separados (`RN-07-19`).

**As rotas públicas de prestação de contas** (`RF-07-16`), painel vivo sem fechamento periódico
(`RN-07-31`), sempre em moedas e nunca em reais (`RN-07-05`).

**A leitura do próprio Apoiador** (`RF-07-17`): seus aportes e seu Poder Sustentador, sem
edição.

**O lançamento de débito passa a declarar a aula que o consumiu.** O PRD-07 §8 já define `aula`
entre os atributos de `Lancamento`; as fatias anteriores não precisaram dela e não a
implementaram. Sem esse elo não há caminho algum do lançamento até a aula — nem `Lancamento`
nem `Reserva` guardam a referência —, e `GET /prestacao-de-contas/aulas` não sai. A alternativa
de derivar o consumo pelas reservas consumidas foi descartada: revaloraria o consumo pela
tabela de referência de hoje, discordando do que o débito gravou no dia.

O lado do crédito **não** muda: o caminho até o provedor já existe por `Aporte.lancamento_id`.

Rotas, conforme o PRD-07 §9:

| Método | Rota                                | Autenticação |
| ------ | ----------------------------------- | ------------ |
| GET    | `/prestacao-de-contas`              | pública      |
| GET    | `/prestacao-de-contas/aulas`        | pública      |
| GET    | `/provedores/{id}/poder-economico`  | pública      |
| GET    | `/meus-aportes`                     | Apoiador     |

As três rotas públicas dispensam credencial de persona e seguem exigindo a chave de aplicação,
como toda rota de dados sob `/v1`. Provedor é sempre adulto (`RN-07-06`): nenhum dado de
criança atravessa esta superfície, e o portão de autorização de divulgação — que é do
Guerreiro(a) — não se aplica aqui. Documento 03 §8 e documento 04 §1 já põem a página pública
de Mestres e Apoiadores e o Poder Sustentador como exibição por padrão.

## Capabilities

### New Capabilities

- `poder-sustentador`: o acumulado do provedor em moedas, derivado dos lançamentos, e a
  contagem de absorções, derivada dos aportes — com as leituras por provedor, a pública e a do
  próprio Apoiador (`RF-07-10`, `RF-07-17`, `RF-07-26`, `RN-07-19`).
- `prestacao-de-contas`: o painel público do movimentado por provedor, por aula e por
  comunidade, em moedas (`RF-07-16`, `RN-07-05`, `RN-07-31`).

### Modified Capabilities

- `livro-razao`: o lançamento de débito passa a declarar a aula que o consumiu, o que torna o
  consumo por aula derivável do próprio ledger (`RF-07-16`, `RN-07-15`, PRD-07 §8).

## Impact

- `backend/src/nucleo/livro_razao/` — `aula_id` em `Lancamento` e a migração Alembic
  correspondente; o que fazer com os débitos já gravados é decisão do `design`.
- `backend/src/nucleo/reservas/` — a baixa passa a gravar a aula no lançamento que emite.
- Dois módulos novos no backend, para as duas capacidades novas.
- Rotas públicas novas: entram na cota por faixa de chave e no freio por origem que a
  capacidade `protecao-das-rotas-publicas` já define; nada muda nela.
- Nenhuma decisão nova de produto: a fatia aplica o que os documentos 03 §8 e 04 §1 e o PRD-07
  já decidiram. Nada a mover no documento 09 nem nos documentos-fonte.

## Fora do escopo

Reproduz o que o PRD-07 §3.2 já exclui, e o que pertence a fatias seguintes do mesmo PRD:

- **Ressarcimento** (`RF-07-22` a `RF-07-25`) — fatia seguinte. O estorno que reverte as moedas
  não existe ainda; esta fatia apenas não impede que ele entre depois como lançamento.
- **Assumir a absorção a partir da necessidade publicada** (`RF-07-28`) — é escrita, e vai com
  a fatia do ressarcimento.
- **Patrimônio, ficha de vida e conferência de inventário** (`RF-07-11`, `RF-07-13`,
  `RF-07-20`, `RF-07-48`), **catálogo avulso** (`RF-07-33` a `RF-07-38`, `RF-07-42` a
  `RF-07-46`) e **lastro do desafio extra** (`RF-07-15`, `RF-07-39` a `RF-07-41`) — fatias
  seguintes.
- **Interface de gestão de recursos** — pertence ao PRD-02 (App 03).
- **Efetividade do apoio ao Apoiador** — o ledger guarda o dado; o painel é do PRD-14.
- **Contabilidade fiscal e prestação de contas formal da pessoa jurídica.**
