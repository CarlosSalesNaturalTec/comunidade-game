## 1. Decisões novas nos documentos-fonte, antes do código

- [x] 1.1 Gravar no **documento 04 §1** as duas decisões desta change — o **teto da receita
      destinada** como regra do núcleo (`RN-07-17`) e a **absorção de serviço não ressarcível**,
      exceção ao `RF-07-21` que fecha a contradição entre o `RN-07-39` e o `RN-07-24` —, movê-las
      para "já decididos" no **documento 09** e aplicá-las ao **PRD-07** (§§6, 7, 13 e 14)
      (design — Decisions 3, 6)

## 2. Destinação do aporte e do lançamento

- [x] 2.1 Criar o enum `DestinacaoDoAporte` (`lastro`, `ressarcimento`) e a coluna `destinacao`
      em `Aporte` e em `Lancamento`, `NOT NULL` com _default_ `lastro`, gravada no ato e herdada
      pelo lançamento do aporte que o gera (`RF-07-23`, `RN-07-38`, design — Decisions 2, 5)
- [x] 2.2 Filtrar `livro_razao.regra.saldo_de` pela destinação `lastro`, mantendo a coluna local
      e sem junção nova sob o `FOR UPDATE` do agendamento; o crédito de destinação ressarcimento
      deixa de compor saldo e disponível (`RF-07-23`, `RN-07-38`, design — Decisions 2)
- [x] 2.3 Aceitar `destinacao` em `POST /aportes`, recusando com 422 o valor fora dos dois
      previstos e a destinação `ressarcimento` em aporte de forma absorção; a confirmação
      automática de aula pendente de lastro passa a ignorar o aporte de destinação ressarcimento
      (`RF-07-23`, `RN-07-38`, `RN-07-37`)

## 3. A absorção assumida a partir da necessidade publicada

- [x] 3.1 Acrescentar `aula_id` anulável a `Aporte` e aceitá-la em `POST /aportes/absorcao`,
      recusando com 422 aula inexistente, tipo que a aula não consome e declaração da aula em
      aporte de outra forma (`RF-07-28`, design — Decisions 5)
- [x] 3.2 Exigir `valor_de_origem` na absorção de natureza consumível, durável ou financeira, e
      deixá-lo vazio na natureza serviço, que passa a nascer **não ressarcível** com situação
      `nao_se_aplica` (`RN-07-39`, `RF-07-21`, `RN-07-24`, design — Decisions 6)

## 4. O ajuste que reverte moedas sem mexer em quantidade

- [x] 4.1 Admitir em `livro_razao.regra.lancar_ajuste` o ajuste de **quantidade zero** com
      moedas negativas, herdando a destinação do lançamento referenciado e mantendo motivo,
      autor e a intocabilidade do original (`RF-07-25`, `RF-07-19`, `RN-07-15`, design —
      Decisions 1)

## 5. O ressarcimento

- [x] 5.1 Criar `src/nucleo/ressarcimentos/modelo.py` com a entidade `Ressarcimento` — aporte
      absorvido (único), valor em reais, receita destinada de origem, Admin pagador, data e
      comprovante —, **sem campo algum de dado bancário** (`RF-07-22`, PRD-07 §11)
- [x] 5.2 Criar `src/nucleo/ressarcimentos/regra.py` com a fila por antiguidade — absorções
      ressarcíveis em aberto, da mais antiga à mais nova, com o saldo de receita destinada em
      aberto (`RF-07-24`, `RN-07-17`)
- [x] 5.3 Acrescentar à mesma `regra.py` o registro do ressarcimento: `FOR UPDATE` sobre o
      aporte da receita declarada, conferência do teto, exigência do comprovante em PDF, JPG ou
      PNG, e recusa de aporte não ressarcível, já ressarcido ou de origem em aporte de
      destinação lastro (`RF-07-22`, `RN-07-17`, design — Decisions 3)
- [x] 5.4 Emitir, no mesmo ato e na mesma transação, o ajuste que reverte as moedas do crédito
      do aporte e levar a situação do aporte a `ressarcido`; o saldo de recurso e a contagem de
      absorções não se movem (`RF-07-25`, `RN-07-18`, design — Decisions 1, 4)
- [x] 5.5 Criar `src/nucleo/ressarcimentos/rotas.py` com `GET /aportes/ressarciveis` e
      `POST /aportes/{id}/ressarcimento`, restritas a Admin, e `GET /meus-aportes/ressarciveis`,
      restrita a Mestre ou Admin e filtrada pelo provedor em sessão; nenhuma delas pública e
      nenhuma servindo o comprovante (`RF-07-22`, `RF-07-24`, design — Decisions 7)

## 6. Migração

- [x] 6.1 Migração Alembic em passo único: `aporte.destinacao`, `aporte.aula_id`,
      `lancamento.destinacao`, a tabela `ressarcimento` e a correção de
      `situacao_de_ressarcimento` para `nao_se_aplica` nas absorções de natureza serviço já
      gravadas — sem tocar em lançamento algum (design — Decisions 5, Migration Plan)

## 7. Testes

- [x] 7.1 `tests/test_aporte_destinacao.py` — a doação destinada credita o Poder Sustentador e
      fica fora do saldo, não confirma aula pendente de lastro e não abate necessidade; aporte
      sem destinação nasce lastro; absorção com destinação ressarcimento é recusada
      (`RF-07-23`, `RN-07-38`)
- [x] 7.2 `tests/test_aporte_absorcao_necessidade.py` — a absorção declara a aula que atende,
      abate a falta parcialmente e confirma a aula ao fechar; tipo fora da lista da aula é 422;
      valor em reais exigido nas naturezas com desembolso e vazio no serviço, que nasce não
      ressarcível (`RF-07-28`, `RN-07-39`)
- [x] 7.3 `tests/test_ressarcimento_fila.py` — a fila sai da mais antiga à mais nova, o aporte
      ressarcido some dela, o aporte da gestão e a absorção de serviço nunca entram, e o Mestre
      recebe 403 (`RF-07-24`)
- [x] 7.4 `tests/test_ressarcimento_registro.py` — registro sem comprovante é 422; aporte não
      ressarcível, já ressarcido ou receita de origem em aporte de lastro são 422; valor acima
      do que a receita cobre é 422 e nada é gravado; nenhum campo aceita chave PIX, banco ou
      conta; Mestre recebe 403 (`RF-07-22`, `RN-07-17`)
- [x] 7.5 `tests/test_ressarcimento_reversao.py` — o Poder Sustentador volta ao valor anterior
      ao aporte, a contagem de absorções segue contando, o saldo do tipo no ponto de apoio não
      se move, o aporte e o crédito permanecem intactos e a situação passa a `ressarcido`
      (`RF-07-25`, `RN-07-18`)
- [x] 7.6 `tests/test_meus_aportes_ressarciveis.py` — o Mestre lê a situação só dos próprios
      aportes, não alcança os de outro provedor e não tem operação de escrita; Apoiador recebe
      403 (`RF-07-24`, `RN-07-17`)
- [x] 7.7 `tests/test_ressarcimento_rota.py`, além do escopo original — o fluxo completo pelas
      três rotas HTTP novas, e a fixture `app` de `conftest.py`, que montava a aplicação de teste
      roteador a roteador, ficou sem `roteador_de_ressarcimentos`: sem este teste as três rotas
      responderiam 404 em qualquer ambiente que reusasse aquela fixture (`RF-07-22`, `RF-07-24`)

## 8. Documentação

- [x] 8.1 Atualizar `docs/prds/index.md` com o que a sexta fatia entregou, e conferir que as
      duas decisões da tarefa 1.1 estão gravadas no documento 04 §1, movidas no documento 09 e
      aplicadas ao PRD-07. O documento 99 e a `nav` do `mkdocs.yml` não mudam: nenhum arquivo
      novo em `docs/` e nenhuma relação nova entre documentos
