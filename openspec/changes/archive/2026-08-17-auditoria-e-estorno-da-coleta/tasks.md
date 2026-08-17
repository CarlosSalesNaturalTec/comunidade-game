## 1. O débito de ponto regular no núcleo

- [x] 1.1 Estreitar o listener de `PontoRegular` em `backend/src/nucleo/pontuacao/modelo.py`:
      deixa de recusar a redução, passa a recusar o **total negativo**, e mantém a recusa de
      remoção. Atualizar o docstring, que hoje afirma que `total` nunca decresce (`RF-01-57`,
      `RF-01-69`, `RN-01-55`, design — decisão 2)
- [x] 1.2 Criar `debitar_ponto_regular` em `backend/src/nucleo/pontuacao/regra.py`, ao lado de
      `creditar_ponto_regular`: exige exatamente uma trilha **ou** um poder, exige valor
      positivo e **para o saldo em zero** quando o débito excede o total (`RF-01-57`,
      `RF-01-69`, `RN-01-55`)
- [x] 1.3 Ajustar o docstring de `creditar_ponto_regular`, que hoje diz "só credita — nunca
      debita, em nenhuma operação" (`RF-01-57`)
- [x] 1.4 Garantir que nenhum caminho de nível ou badge recalcule para baixo a partir do saldo,
      e cobrir com teste que o débito não derruba nível nem badge (`RF-01-70`, `RN-01-55`)
- [x] 1.5 Reescrever o teste que hoje prova "ponto regular não decresce" para provar "não fica
      negativo", e acrescentar o teste da recusa de `DELETE`, que segue valendo (`RF-01-69`)

## 2. Modelo e migração

- [x] 2.1 Acrescentar `invalidada` a `SituacaoDoRegistro` em
      `backend/src/nucleo/coletas/modelo.py`, e atualizar o docstring que hoje diz "só `valida`
      nesta fatia" (`RF-08-13`, `RN-08-10`)
- [x] 2.2 Acrescentar a `RegistroDeColeta` os campos `auditado_em`, `auditado_por_id` e
      `motivo_da_invalidacao`, todos nulos (`RF-08-13`, `RF-08-29`, design — decisão 3)
- [x] 2.3 Escrever a migração do Alembic: colunas novas pelo pai da tabela particionada,
      restrição de `CHECK` de `situacao` derrubada e recriada com o valor novo, e
      `CREATE OR REPLACE FUNCTION recusar_debito_de_ponto_regular` com a trava estreita
      (design — Migration Plan)
- [x] 2.4 Escrever a revisão `down` da migração, que recria a função anterior e derruba as
      colunas (design — Migration Plan)
- [x] 2.5 Conferir que `Base.metadata.create_all()`, caminho que os testes usam, produz a mesma
      trava que a migração — o evento de DDL de `pontuacao.modelo` acompanha a mudança

## 3. A composição da amostra

- [x] 3.1 Implementar em `backend/src/nucleo/coletas/regra.py` a seleção dos **10% dos registros
      da semana por série, com o mínimo de um**, arredondando para baixo, sobre os ainda não
      auditados e em ordem de `momento_do_fato` (`RN-08-20`, design — decisões 5 e 6)
- [x] 3.2 Incluir na amostra **todos** os registros "a conferir" não auditados, fora do
      percentual e sem consumir as vagas dele (`RN-08-20`, `RN-08-26`)
- [x] 3.3 Restringir a amostra às séries dos desafios de que o Mestre é **autor**, e apurar o
      estado de cada série **no instante do pedido**, deixando de fora interrompida e encerrada
      (`RN-08-20`, PRD-08 §5.5)
- [x] 3.4 Excluir da amostra o registro que já tem `auditado_em`, para que a auditoria termine
      (design — decisão 3)

## 4. Confirmação e invalidação

- [x] 4.1 Implementar a **confirmação**: credita o "a conferir" pela régua do registro válido,
      reapurando a quantidade que pontua no período; não credita registro já válido; não credita
      duas vezes; grava `auditado_em` e `auditado_por_id` (`RF-08-29`, `RN-08-26`, design —
      decisão 4)
- [x] 4.2 Implementar a **invalidação**: exige motivo, estorna `pontos_creditados` — zero
      inclusive —, marca a situação `invalidada` e mantém o registro gravado (`RF-08-13`,
      `RN-08-09`, design — decisão 1)
- [x] 4.3 Fazer a invalidação **terminal**: confirmação de registro invalidado é recusada, e
      invalidar de novo não estorna segunda vez (`RN-08-10`)
- [x] 4.4 Garantir que a invalidação **não** recredite nenhum outro registro do período, ainda
      que a vaga fique livre (design — decisão 4)

## 5. Permissões e rotas

- [x] 5.1 Declarar em `backend/src/nucleo/permissoes.py` a operação de auditoria da coleta,
      escopada ao **Mestre autor do desafio** (`RF-08-13`, `RF-08-29`)
- [x] 5.2 Expor `GET /auditoria/amostra` no roteador de coletas, devolvendo a amostra do Mestre
      em sessão (`RN-08-20`, PRD-08 §9)
- [x] 5.3 Expor `POST /registros/{id}/confirmacao` e `POST /registros/{id}/invalidacao`,
      recusando com **403** quem não é o Mestre autor e com **422** a invalidação sem motivo
      (`RF-08-13`, `RF-08-29`, PRD-08 §9)
- [x] 5.4 Ligar as rotas em `backend/src/nucleo/principal.py` e conferir que elas aparecem no
      OpenAPI

## 6. Saída pública

- [x] 6.1 Excluir o registro `invalidada` da agregação do painel público, da exportação e da
      cobertura de ODS, conferindo que a guarda de situação já existente nessas consultas
      alcança o valor novo (`RN-08-09`, `RN-08-12`)

## 7. Testes e fechamento

- [x] 7.1 Testes da amostra: os 10% com trinta registros, o piso de um com quatro, série sem
      registro fora, série de desafio alheio fora, série interrompida e encerrada fora, e
      "a conferir" já auditado que não volta
- [x] 7.2 Testes da confirmação: credita o "a conferir", não credita registro já válido, credita
      zero quando o período esgotou, e não credita duas vezes
- [x] 7.3 Testes da invalidação: estorna o valor exato, estorna zero no "a conferir" e no
      excedente, recusa sem motivo, mantém o registro consultável, não recredita a vaga liberada
      e é terminal
- [x] 7.4 Testes do débito: para em zero, não derruba nível nem badge, e a troca de recompensa
      segue sem alcançar o ponto regular
- [x] 7.5 Testes de permissão: 403 do Mestre que não é autor do desafio e 403 do Guerreiro(a)
      sobre o próprio registro
- [x] 7.6 Rodar `ruff format --check .`, `ruff check .` e `pytest` na pasta `backend/`
- [x] 7.7 Conferir que `docs/` não precisa de mudança nesta change — as decisões já entraram nos
      commits `8225312` e `4738651` — e rodar `npm run lint` e `mkdocs build --strict` para
      confirmar que o site segue de pé
