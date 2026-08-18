## 1. Ponto de apoio

- [x] 1.1 Criar `pontos_de_apoio/modelo.py` com `PontoDeApoio` — `nome`, `comunidade_virtual_id`
      obrigatórios, `responsavel_id` anulável e `ativo` com _default_ verdadeiro, sobre
      `ComAutoria` (`RF-07-47`, `RN-07-33`, `RF-01-03`, design — Decisions 6)
- [x] 1.2 Comentar no `ativo` que ele existe **sem operação que o mude**, apontando a pendência
      do documento 09 (design — Decisions 6, Risks)
- [x] 1.3 Escrever `pontos_de_apoio/regra.py` — cadastro restrito a **Admin**, com 403 para
      qualquer outro papel e 422 para nome ou comunidade em falta e para comunidade inexistente
      (`RF-07-47`, `RF-01-16`, `RF-01-27`)
- [x] 1.4 Escrever a **designação do responsável**: operação de Admin, aceita persona de papel
      `admin`, `mestre` ou `apoiador`, recusa `guerreiro` e `responsavel` com 422, e substitui o
      designado anterior (`RF-07-49`, `RN-07-34`, `RF-01-16`)
- [x] 1.5 Criar `pontos_de_apoio/rotas.py` com `POST /pontos-de-apoio` e
      `PUT /pontos-de-apoio/{id}/responsavel`, no padrão de rota de Admin de `locais/rotas.py`
      (`RF-07-47`, `RF-07-49`, PRD-07 §9)
- [x] 1.6 Cobrir com teste o cadastro por Admin, a recusa ao Mestre, o cadastro sem nome, o
      cadastro sem comunidade e a comunidade inexistente (`RF-07-47`, `RF-01-16`, `RF-01-27`)
- [x] 1.7 Cobrir com teste o ponto de apoio que nasce sem responsável, a designação de Admin, de
      Mestre e de Apoiador, a recusa de Guerreiro(a) e de responsável familiar, a troca que
      substitui o anterior e a recusa ao Mestre que tenta designar (`RF-07-49`, `RN-07-34`)

## 2. Catálogo de tipos de recurso

- [x] 2.1 Criar `recursos/modelo.py` com `TipoDeRecurso` — `nome`, `natureza` entre as quatro
      previstas e `unidade` —, sobre `ComAutoria` (`RF-07-01`, `RF-01-03`)
- [x] 2.2 Escrever `recursos/regra.py` — cadastro restrito a **Admin**, 403 para outro papel e
      422 para nome, natureza ou unidade em falta e para natureza fora das quatro
      (`RF-07-01`, `RF-01-16`, `RF-01-27`)
- [x] 2.3 Manter o cadastro de tipo como operação **avulsa**, sem dependência de outro fluxo — é
      a condição do "sem interromper o fluxo" que a fatia do aporte fechará (`RF-07-03`,
      proposal — Fora do escopo)
- [x] 2.4 Criar `POST /tipos-de-recurso` em `recursos/rotas.py` (`RF-07-01`, PRD-07 §9)
- [x] 2.5 Cobrir com teste o cadastro por Admin, a recusa ao Mestre, o tipo sem unidade e a
      natureza fora das quatro previstas (`RF-07-01`, `RF-01-16`, `RF-01-27`)

## 3. Valor de referência versionado

- [x] 3.1 Acrescentar `ValorDeReferencia` a `recursos/modelo.py` — `valor_em_moedas` em
      `Numeric(12, 2)`, `vigencia_inicio` e `vigencia_fim` anulável —, com `CHECK` de valor não
      negativo e de `vigencia_fim >= vigencia_inicio` (`RF-07-02`, `RN-07-04`, design —
      Decisions 1 e 2)
- [x] 3.2 Escrever o registro de valor: abrir vigência nova **encerra a vigente no dia de início
      da nova** e NUNCA reescreve nem apaga a anterior (`RF-07-02`, `RN-07-03`, design —
      Decisions 2)
- [x] 3.3 Escrever a consulta **por data** no intervalo semiaberto `inicio <= data < fim`,
      ordenada por `vigencia_inicio DESC, criado_em DESC`, tomando a primeira (`RF-07-02`,
      design — Decisions 2)
- [x] 3.4 Recusar com 422, **na regra e antes do banco**, valor negativo e valor com mais de duas
      casas decimais, sem arredondar em silêncio (`RN-07-04`, `RF-01-27`, design — Decisions 1)
- [x] 3.5 Restringir o registro de valor de referência a **Admin**, com 403 para outro papel
      (`RF-07-02`, `RF-01-16`)
- [x] 3.6 Cobrir com teste a primeira vigência, o valor novo que encerra a anterior sem a
      reescrever, a consulta dentro da vigência encerrada, a consulta no dia da virada, a
      consulta depois da última abertura e as duas vigências abertas no mesmo dia (`RF-07-02`,
      `RN-07-03`, design — Risks)
- [x] 3.7 Cobrir com teste o valor negativo recusado, o valor de três casas recusado e a
      comparação com `Decimal`, nunca com literal `float` (`RN-07-04`, design — Risks)

## 4. Ponto de apoio na aula

- [x] 4.1 Acrescentar `ponto_de_apoio_id` a `aulas/modelo.py`, FK **não anulável** (`RF-01-71`,
      design — Decisions 3)
- [x] 4.2 Exigir o ponto de apoio em `aulas.regra.agendar_aula`, com 422 indicando o campo em
      falta (`RF-01-71`, `RF-01-27`)
- [x] 4.3 Conferir na regra que o ponto de apoio é da **mesma comunidade** da aula, recusando com
      422 (`RF-01-71`, `RN-07-33`, invariante 4 do documento 99 §6, proposal — decisão 4,
      design — Decisions 4)
- [x] 4.4 Atualizar os testes existentes de aula, que hoje agendam sem ponto de apoio
      (`tests/test_aula.py` e o que mais chamar `agendar_aula`) (`RF-01-71`)
- [x] 4.5 Cobrir com teste a aula sem ponto de apoio recusada e a aula com ponto de apoio de
      outra comunidade recusada (`RF-01-71`, `RN-07-33`)

## 5. Migration e registro

- [x] 5.1 Gerar a revisão do Alembic encadeada em `a7b8c9d0e1f2`, com as três tabelas novas e
      `aula.ponto_de_apoio_id` `NOT NULL` (design — Migration Plan)
- [x] 5.2 Escrever no docstring da revisão que ela **falha em base com aulas gravadas**, e que o
      remédio é cadastrar o ponto de apoio antes — não afrouxar a coluna (design — Decisions 3,
      Risks)
- [x] 5.3 Registrar os dois roteadores em `principal.py`, sob a chave de aplicação que o registro
      já exige (`RF-01-02`, `RN-01-32`)
- [x] 5.4 Cobrir com teste que a escrita sem chave de aplicação é recusada com 401 (`RF-01-02`,
      `RN-01-32`)

## 6. Documentação e fechamento

- [x] 6.1 Passar o PRD-01 a **implementado** em `docs/prds/index.md` — o `RF-01-71` era o último
      requisito aberto dele — e conferir que a `nav` do `mkdocs.yml` não muda (nenhum arquivo novo
      em `docs/`)
- [x] 6.2 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict`
- [x] 6.3 Rodar `ruff format --check .`, `ruff check .` e `pytest` no `backend/`
- [x] 6.4 Rodar `/opsx:verify` antes de arquivar
