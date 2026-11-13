# Design

## Context

`PontoRegular` guarda **uma linha por par** Guerreiro(a) × trilha ou poder, somada a cada
crédito; `PontoExtra`, **uma linha por Guerreiro(a)** com acumulado e saldo disponível. Não há
registro por evento — o próprio docstring de `PontoRegular` adiava o "detalhe por evento". Todo
movimento passa por cinco funções: `creditar_ponto_regular`, `debitar_ponto_regular`
(`pontuacao/regra.py`), `creditar_ponto_extra`, `debitar_ponto_extra` e
`estornar_ponto_extra_da_presenca` (`ponto_extra/regra.py`). São elas o ponto único onde o
lançamento nasce.

O padrão de tabela somente inserção, recusada no ORM e por gatilho no banco, já existe em
`consentimentos.modelo`, `ponto_regular` e `ponto_extra`. A escolha dos Guerreiros(as) da
comunidade do Mestre já existe em `responsaveis.regra.guerreiros_vinculaveis`
(`GET /v1/guerreiros/vinculaveis`).

## Goals / Non-Goals

**Goals:** lançamento por movimento, linha de saldo anterior, duas rotas de leitura, ficha nas
Apps 09, 03 e 05.

**Non-Goals:** reconstruir o passado; filtro, busca ou exportação; histórico na App 07, na
vitrine ou nos jogos.

## Decisions

1. **Tabela `lancamento_de_pontuacao`**, somente inserção, em `nucleo/historico_de_pontuacao/`:
   `id`, `guerreiro_id`, `conta` (`regular` | `extra`), `trilha_id` | `poder_id` (só na
   regular, um dos dois — mesma `CheckConstraint` de `ponto_regular`), `origem` (enum),
   `referencia_id` (UUID do fato, anulável só na linha de saldo anterior), `detalhe` (título do
   fato — atividade, missão, item — anulável), `valor` (inteiro com sinal: na regular, o que
   moveu o total; na extra, o que moveu o **saldo disponível**), `valor_no_acumulado` (só na
   extra) e `registrado_em` (`now()` do banco). Gatilho `BEFORE UPDATE OR DELETE` recusa no
   banco e `before_update`/`before_delete` no ORM (`RN-01-67`).
   _Descartado:_ derivar o histórico por `UNION` das tabelas de fato a cada leitura — não fecha
   com o total (piso em zero, regras que mudaram de vigência) e cresce a cada fonte nova.

2. **As cinco funções recebem `origem`, `referencia_id` e `detalhe` obrigatórios** e gravam o
   lançamento depois do `flush` da conta, com o valor **efetivamente movido** (diferença entre
   o total antes e depois) — o piso em zero sai certo sem regra à parte (`RN-01-67`). Os
   chamadores (`resultados`, `coletas`, `quiz`, `criacoes_originais`, `trilhas`,
   `ocorrencias_de_conduta`, `aulas`, `cuidado_do_bem`, `fila`, `trocas`, e a fonte dupla
   `creditar_ponto_extra_do_resultado`) passam a origem. Parâmetro obrigatório faz o
   esquecimento falhar no teste, não em produção.

3. **Origens** (enum `OrigemDoLancamento`): `resultado`, `merito_do_resultado`,
   `criacao_original`, `partida_de_quiz`, `registro_de_coleta`, `estorno_de_coleta`,
   `desafio_pratico`, `ocorrencia_de_conduta`, `presenca`, `estorno_de_presenca`,
   `cuidado_do_bem` (conservação e customização — a mesma função credita as duas, distinguidas
   pelo `detalhe`), `proposta_adotada`, `troca`, `saldo_anterior`. O rótulo em linguagem
   simples é das apps.

4. **Motivo da conduta lido na hora, nunca copiado.** O lançamento guarda só a
   `referencia_id` da ocorrência; a leitura faz `LEFT JOIN` em `ocorrencia_de_conduta` e traz o
   `motivo` atual. Copiar o texto burlaria a guarda pelo ciclo (spec `ocorrencia-de-conduta`):
   apagado lá, some aqui.

5. **Linha de saldo anterior na migração Alembic** (`RF-01-90`): um `INSERT … SELECT` de
   `ponto_regular` (uma linha por conta, `valor = total`) e outro de `ponto_extra`
   (`valor = saldo_disponivel`, `valor_no_acumulado = acumulado`), com `registrado_em` da
   migração. No `downgrade`, a tabela cai inteira.

6. **Rotas** em `historico_de_pontuacao/rotas.py`, com o mesmo serviço de leitura:
   - `GET /v1/eu/historico-de-pontuacao` — só papel Guerreiro(a); sem identificador.
   - `GET /v1/guerreiros/{id}/historico-de-pontuacao` — Admin, ou Mestre cujo
     `comunidades_do_mestre` contenha a comunidade do `VinculoJogador` vigente do Guerreiro(a);
     qualquer outro caso, **403** (`RN-01-68`).
   Resposta: `{ saldos: { regular: [{trilha_id, poder_id, nome, total}], extra: {acumulado,
   saldo_disponivel} }, itens: [...], proximo_cursor }`. Ordem `registrado_em DESC, id DESC`,
   cursor sobre esse par, pelo `contrato_de_listagem` (`paginacao.py`). Os saldos vêm na
   primeira página e se repetem nas demais (leitura barata, sem estado).

7. **Componente comum `HistoricoDePontuacao`** em `comum/pontuacao/` (saldos + lista + "carregar
   mais"), recebendo a função de busca: as três apps mudam só a rota. Glifo e ficha de ponto
   regular e extra são os de `comum` já usados na carteira (documento 15 §9).
   - **App 09**: caminho novo "Guerreiros e Guerreiras" → lista por
     `GET /v1/guerreiros/vinculaveis` → ficha.
   - **App 03**: `ListaDeGuerreiros` ganha a ação "Ficha", que abre `FichaDoGuerreiro`.
   - **App 05**: `MinhaCarteira` ganha a entrada "Como cheguei aqui" para o histórico.

## Risks / Trade-offs

- **Função esquecida grava movimento sem lançamento** → parâmetro obrigatório e um teste que
  confere, por Guerreiro(a), soma dos lançamentos = total da conta após cada fluxo.
- **Volume** → um lançamento por movimento; índice `(guerreiro_id, registrado_em DESC, id)`.
- **Saldo anterior esconde o passado** → aceito pelo fundador; a linha é rotulada como tal.
- **Mestre com vínculo em mais de uma comunidade** → a regra usa o conjunto inteiro de
  `comunidades_do_mestre`, como a lista de vinculáveis.
