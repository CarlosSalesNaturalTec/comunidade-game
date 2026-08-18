## 1. O débito declara a aula que o consumiu

- [x] 1.1 Acrescentar `aula_id` anulável e indexado a `Lancamento`, com a migração Alembic que
      cria a coluna e o índice e **não** preenche débito já gravado — a imutabilidade recusa o
      `UPDATE` (`RF-07-16`, `RN-07-15`, design — Decisions 3, 4)
- [x] 1.2 Passar a aula pela emissão do débito: `livro_razao.regra.lancar_debito` aceita e grava
      `aula_id`, e `reservas.regra.consumir_reservas_da_aula` informa a aula que já tem em mãos;
      crédito e ajuste seguem sem aula (`RF-07-09`, `RF-07-16`, `RN-07-36`)

## 2. Poder Sustentador e contagem de absorções

- [x] 2.1 Criar `src/nucleo/poder_sustentador/regra.py` com a derivação do Poder Sustentador pela
      cadeia aporte → crédito → ajuste, agregada em SQL e sem total guardado à parte
      (`RF-07-10`, `RN-07-15`, design — Decisions 1, 5)
- [x] 2.2 Acrescentar à mesma `regra.py` a contagem de absorções, derivada de `Aporte` com
      `forma = absorcao` e sem tocar no livro-razão (`RF-07-26`, `RN-07-19`, design —
      Decisions 2)
- [x] 2.3 Criar `src/nucleo/poder_sustentador/rotas.py` com a rota
      `GET /provedores/{id}/poder-sustentador`: pública, sem `exigir_persona`, devolvendo as
      moedas e a contagem de absorções,
      **404 indistinto** para identificador inexistente e para persona de Guerreiro(a) ou
      responsável, e 200 com zero para adulto sem aporte (`RF-07-10`, `RF-07-26`, `RN-07-05`,
      `RN-07-06`, design — Decisions 8)
- [x] 2.4 Acrescentar `GET /meus-aportes`, restrita ao Apoiador em sessão, devolvendo os aportes
      dele e o Poder Sustentador dele, em moedas e sem o valor de origem em reais (`RF-07-17`,
      `RN-07-05`)

## 3. Prestação de contas pública

- [x] 3.1 Criar `src/nucleo/prestacao_de_contas/regra.py` com o movimentado total e por provedor,
      derivado no momento da leitura e sem fechamento periódico, reaproveitando a função de
      soma da capacidade `poder-sustentador` para as duas leituras não divergirem (`RF-07-16`,
      `RN-07-31`, design — Decisions 1, 5)
- [x] 3.2 Acrescentar à mesma `regra.py` o consumo por aula e por comunidade, somado dos débitos
      pelo valor que cada um gravou — sem revalorar pela vigência corrente — e agregado pela
      comunidade do ponto de apoio da aula (`RF-07-16`, `RN-07-33`, `RN-07-36`)
- [x] 3.3 Criar `src/nucleo/prestacao_de_contas/rotas.py` com `GET /prestacao-de-contas` e
      `GET /prestacao-de-contas/aulas`, públicas, cujas saídas não carregam valor em reais,
      comprovante nem dado de Guerreiro(a) (`RF-07-16`, `RN-07-05`, `RN-07-13`, `RN-07-20`,
      design — Decisions 7)
- [x] 3.4 Registrar os dois roteadores em `principal.py` por `incluir_roteador_de_dados`, que já
      exige a chave de aplicação e a cota de leitura (`RF-01-02`, `RN-01-32`)

## 4. Testes

- [x] 4.1 Ampliar `tests/test_lancamento.py` com os cenários do delta de `livro-razao`: a baixa
      grava a aula no débito, o crédito do aporte não declara aula, a aula de lançamento gravado
      não muda (405) e somar os débitos de uma aula devolve o consumo dela (`RF-07-09`,
      `RF-07-16`, `RN-07-15`)
- [x] 4.2 Criar `tests/test_poder_sustentador.py` com os cenários de derivação da spec: o aporte
      de 3 × 0,50 sobe o Poder Sustentador em 1,50, o ajuste de -0,50 o leva a 1,00, a
      recontagem devolve o mesmo número, a baixa não desconta de ninguém, provedor sem aporte dá
      zero — e os de contagem de absorções: três absorções contam 3, o ajuste no ledger não
      apaga a absorção, quem nunca absorveu conta zero (`RF-07-10`, `RF-07-26`, `RN-07-19`)
- [x] 4.3 Criar `tests/test_poder_sustentador_rota.py`: leitura pública sem token, 401 sem chave,
      404 indistinto para Guerreiro(a) e para inexistente, nenhuma saída com reais, e em
      `/meus-aportes` — o Apoiador vê os próprios aportes, o aporte alheio fica de fora e sem
      sessão a rota não responde (`RF-07-10`, `RF-07-17`, `RF-07-26`, `RN-07-05`)
- [x] 4.4 Criar `tests/test_prestacao_de_contas.py`: o aporte novo aparece na leitura seguinte
      sem fechamento, a recontagem devolve o mesmo movimentado, o total soma 1,50 e 2,50 em
      4,00, o consumo da aula é o que o débito gravou mesmo depois de a tabela mudar, o consumo
      sai separado por comunidade e a aula agendada sem baixa não figura com consumo
      (`RF-07-16`, `RN-07-31`, `RN-07-33`)
- [x] 4.5 Criar `tests/test_prestacao_de_contas_rota.py`: visitante sem persona lê, 401 sem
      chave, e nenhuma resposta traz valor de origem em reais, comprovante ou dado de
      Guerreiro(a) (`RF-07-16`, `RN-07-05`, `RN-07-13`, `RN-07-20`)

## 5. Documentação

- [x] 5.1 Atualizar `docs/prds/index.md` com o que a quinta fatia do PRD-07 entregou. A §9 do
      PRD-07 já foi corrigida nesta change — a rota do Poder Sustentador deixou de ser
      `/provedores/{id}/poder-economico`, que contradizia o nome do conceito no documento 04 §1.
      Nada a mover no documento 09 nem nos documentos-fonte: a fatia não tomou decisão nova.
      Nenhuma relação entre documentos mudou, então o documento 99 fica como está, e nenhum
      arquivo nasceu em `docs/`, então a `nav` do `mkdocs.yml` também
