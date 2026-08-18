## 1. Modelo do livro-razão

- [x] 1.1 Criar `backend/src/nucleo/livro_razao/modelo.py` com `NaturezaDoLancamento` (crédito,
      débito, ajuste) e `Lancamento` — tipo de recurso, ponto de apoio, quantidade e moedas em
      `NUMERIC(12, 2)`, autor, momento com fuso, referência ao lançamento original e motivo do
      ajuste (`RF-07-19`, `RN-07-04`, `RF-01-03`, design — Decisions 2, 9)
- [x] 1.2 Registrar os gatilhos `BEFORE UPDATE` e `BEFORE DELETE` sobre `lancamento`, no padrão de
      `consentimentos/modelo.py`, e o erro próprio em `erros.py` (`RN-07-15`, design — Decisions 3)
- [x] 1.3 Escrever `saldo_de(sessao, tipo, ponto_de_apoio)` em `livro_razao/regra.py`, por
      agregação sobre os lançamentos, sem tabela de saldo (`RF-07-07`, `RN-07-36`,
      design — Decisions 1)
- [x] 1.4 Escrever `lancar_ajuste(...)` em `livro_razao/regra.py`: só Admin, exige motivo e
      lançamento original existente, e não toca no original (`RF-07-19`, `RF-01-16`)

## 2. Modelo do aporte

- [x] 2.1 Acrescentar `exige_comprovante` a `TipoDeRecurso`, com padrão falso
      (`RN-07-22`, design — Migration Plan)
- [x] 2.2 Criar `backend/src/nucleo/aportes/modelo.py` com `FormaDeAporte`,
      `OrigemDoRegistro`, `SituacaoDeRessarcimento` e `Aporte` — provedor, tipo, quantidade,
      ponto de apoio de entrada, valor em moedas, valor de origem, período apurado, comprovante,
      admin homologador, solicitação de origem e lançamento gerado (`RF-07-04`, `RF-07-21`,
      `RF-07-32`, `RN-07-36`, design — Decisions 6)
- [x] 2.3 Declarar a unicidade de `solicitacao_de_participacao_id` no `Aporte` (`RN-07-21`,
      design — Decisions 10)
- [x] 2.4 Gerar a migration Alembic aditiva com as duas tabelas, os gatilhos, o índice composto
      `(tipo_de_recurso_id, ponto_de_apoio_id)` e a coluna nova em `tipo_de_recurso`
      (design — Migration Plan)

## 3. Regra do aporte

- [x] 3.1 Escrever a resolução da vigência e a conversão em moedas pela **data do aporte**,
      gravando o resultado no aporte (`RF-07-05`, `RN-07-03`, design — Decisions 8)
- [x] 3.2 Escrever `registrar_aporte(...)`: só Admin, campos obrigatórios com 422 indicando o
      campo em falta, quantidade maior que zero e ponto de apoio exigido em qualquer natureza
      (`RF-07-04`, `RN-07-02`, `RN-07-36`, `RF-01-16`, `RF-01-27`)
- [x] 3.3 Recusar com 403 o aporte cujo provedor seja a própria persona que o registra
      (`RN-07-16`)
- [x] 3.4 Recusar com 422 o aporte de tipo inexistente, apontando na resposta a rota de cadastro
      do tipo (`RF-07-03`, PRD-07 §9)
- [x] 3.5 Recusar com 422 o aporte cuja data não seja coberta por vigência alguma do tipo
      (`RF-07-05`)
- [x] 3.6 Aceitar período apurado e data anteriores à entrada do livro-razão no ar, com
      comprovante anexado (`RF-07-32`)
- [x] 3.7 Aceitar a solicitação de participação de origem, marcar a origem como pré-cadastro e
      recusar com 422 a segunda homologação da mesma solicitação (`RF-07-30`, `RN-07-21`)
- [x] 3.8 Gerar o lançamento de crédito no ponto de apoio declarado ao homologar o aporte
      (`RF-07-04`, `RF-07-07`)

## 4. Absorção

- [x] 4.1 Escrever `registrar_aporte_por_absorcao(...)`: só Mestre ou Admin, em nome de quem
      proveu, creditando no ato e deixando o homologador vazio (`RF-07-06`, `RN-07-06`,
      `RN-07-35`)
- [x] 4.2 Fazer o aporte por absorção nascer ressarcível, com situação **em aberto**, e o da
      gestão nascer com **não se aplica** (`RF-07-21`)

## 5. Comprovante

- [x] 5.1 Validar o `content_type` do comprovante contra PDF, JPG e PNG, recusando o resto com
      422 (`RN-07-22`)
- [x] 5.2 Gravar o comprovante pela `PortaDeArmazenamento` e guardar referência, nome original,
      tipo e tamanho, no padrão de `fila/rotas.py` (`RN-07-22`, design — Decisions 7)
- [x] 5.3 Recusar com 422 o aporte de tipo que exige comprovante quando ele não vier
      (`RN-07-22`)

## 6. Rotas

- [x] 6.1 Criar `aportes/rotas.py` com `POST /aportes` e `POST /aportes/absorcao`, em
      _multipart_, sob chave de aplicação e credencial de persona (PRD-07 §9, `RF-01-02`)
- [x] 6.2 Criar `livro_razao/rotas.py` com `POST /lancamentos/{id}/ajuste` (`RF-07-19`,
      PRD-07 §9)
- [x] 6.3 Registrar os dois roteadores em `principal.py`, sob o prefixo de versão, e conferir que
      nenhuma rota de leitura ou de edição de lançamento foi publicada no OpenAPI
      (design — Decisions 4)

## 7. Verificação pelos critérios de aceite do PRD-07 §12

- [x] 7.1 Aporte de quantidade 3 com valor de referência 0,50 resulta em **1,50 moeda**
      (`RF-07-05`, PRD-07 §12)
- [x] 7.2 Alterar o valor de referência de um tipo **não** altera o valor em moedas de aporte já
      registrado (`RF-07-05`, PRD-07 §12)
- [x] 7.3 Saldo aportado a um ponto de apoio **não** aparece no saldo de outro ponto de apoio
      (`RF-07-07`, PRD-07 §12)
- [x] 7.4 Recontar os lançamentos devolve o mesmo saldo, sem depender de estado guardado à parte
      (`RF-07-07`, PRD-07 §10)
- [x] 7.5 Aporte por absorção nasce com situação de ressarcimento **em aberto** e credita sem
      homologação (`RF-07-21`, `RN-07-35`, PRD-07 §12)
- [x] 7.6 Aporte registrado pelo próprio provedor é recusado com 403, e a absorção em nome
      próprio não é (`RN-07-16`, `RN-07-35`)
- [x] 7.7 Edição de lançamento responde 405, e remoção direta no banco é recusada pelo gatilho
      (`RF-07-19`, `RN-07-15`)
- [x] 7.8 Ajuste referencia o original, exige motivo e entra na conta do saldo (`RF-07-19`)
- [x] 7.9 Comprovante fora de PDF, JPG e PNG é recusado, e tipo que exige comprovante recusa
      aporte sem ele (`RN-07-22`)
- [x] 7.10 Solicitação de participação com aporte declarado **não** credita nada; o registro pelo
      Admin credita, e a segunda homologação da mesma solicitação é recusada (`RF-07-30`,
      `RN-07-21`)
- [x] 7.11 Aporte com período apurado retroativo é aceito e valorado pela vigência da data do
      aporte (`RF-07-32`)
- [x] 7.12 Escrita sem chave de aplicação é recusada com 401, e sem credencial de persona também
      (`RF-01-02`, `RN-01-32`)
- [x] 7.13 `ruff format --check .`, `ruff check .` e `pytest` passam em `backend/`

## 8. Documentação e esteira

- [x] 8.1 Atualizar em `docs/prds/index.md` o parágrafo do PRD-07 com o que esta fatia entregou e
      o que segue pendente — nenhuma decisão nova foi tomada nesta change, e as duas que a abrem
      já estão gravadas nos documentos 04 e 09 e no PRD
- [x] 8.2 Conferir que o documento 99 não precisa de ajuste — nenhuma relação entre documentos
      muda — e que nenhum arquivo novo entrou em `docs/`, de modo que a `nav` do `mkdocs.yml`
      segue como está
- [x] 8.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR
