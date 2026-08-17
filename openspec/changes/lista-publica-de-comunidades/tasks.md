## 1. Períodos de cadência da série

- [x] 1.1 Escrever, em `coletas/regra.py`, a apuração dos **períodos de cadência vencidos** de
      uma série entre `aberta_em` e o instante da consulta, a partir da `cadencia` da própria
      série (`RN-08-29`, design — Decisions 4)
- [x] 1.2 Escrever a contagem de **períodos distintos com ao menos um registro válido**,
      recortando pela **data da medição** e excluindo registro invalidado (`RN-08-29`,
      `RN-08-09`, `RF-08-15`, design — Decisions 3)
- [x] 1.3 Cobrir com teste a série sem período vencido, a série com todos os períodos cumpridos
      e a série com período vencido sem registro (`RN-08-29`)

## 2. Apuração dos quatro indicadores

- [x] 2.1 Escrever, em `comunidades/regra.py`, a contagem de **séries abertas** da comunidade,
      qualquer que seja o estado (`RF-08-30`, `RN-08-29`)
- [x] 2.2 Escrever a contagem de **séries ativas no instante da consulta**, sem aproveitar
      apuração anterior (`RF-08-30`, `RN-08-29`)
- [x] 2.3 Escrever a contagem de **registros válidos** das séries da comunidade, excluindo o
      invalidado (`RF-08-30`, `RN-08-29`, `RN-08-09`)
- [x] 2.4 Escrever a **continuidade** como média, entre as séries com ao menos um período
      vencido, da fração apurada em 1.2 — e **nula** quando nenhuma série tem período vencido
      (`RN-08-29`, design — Decisions 2)
- [x] 2.5 Cobrir com teste a comunidade recém-criada, que sai com as três contagens em zero e a
      continuidade nula (`RF-08-30`)

## 3. Piso de coletores sobre a lista

- [x] 3.1 Apurar `COUNT(DISTINCT coletor)` por comunidade e, abaixo do piso declarado, devolver
      os **quatro indicadores nulos**, mantendo nome e localização (`RF-08-31`, `RN-08-28`)
- [x] 3.2 Garantir que a supressão alcança os **quatro**, sem subconjunto que escape
      (`RF-08-31`, `RN-08-28`)
- [x] 3.3 Não devolver a contagem de coletores distintos na resposta (`RN-08-12`, design —
      Decisions 6)
- [x] 3.4 Cobrir com teste a comunidade com dois coletores e piso três, a comunidade com três e
      piso três, e a comunidade sem coletor algum (`RF-08-31`, `RN-08-28`)

## 4. Rota

- [x] 4.1 Criar `GET /comunidades` em `comunidades/rotas.py`, pública — sem dependência de
      persona e com a chave de aplicação exigida pelo registro do roteador (`RF-08-30`,
      `RF-01-02`, `RN-01-32`)
- [x] 4.2 Paginar pelo contrato de listagem do núcleo, com ordenação **estável** por nome, e
      recusar parâmetro não declarado com **422** (`RF-01-28`)
- [x] 4.3 Aplicar o piso **antes** do corte de página (`RF-08-31`, design — Decisions 5)
- [x] 4.4 Devolver o **rótulo do ciclo corrente** da `Configuracao` junto da lista
      (`RN-08-29`)
- [x] 4.5 Cobrir com teste a consulta sem chave recusada com 401, a consulta sem sessão aceita,
      o parâmetro não declarado recusado com 422 e a supressão que não depende da página
      (`RF-01-02`, `RN-01-32`, `RF-01-28`, `RF-08-31`)
- [x] 4.6 Cobrir com teste que **nenhum campo da resposta identifica coletor** (`RN-08-12`)

## 5. Documentação e fechamento

- [x] 5.1 Conferir que `docs/prds/index.md` reflete o PRD-08 como implementado ao fim desta
      fatia, e que a `nav` do `mkdocs.yml` não mudou (nenhum arquivo novo em `docs/`)
- [x] 5.2 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict`
- [x] 5.3 Rodar `ruff format --check .`, `ruff check .` e `pytest` no `backend/`
- [x] 5.4 Rodar `/opsx:verify` antes de arquivar
