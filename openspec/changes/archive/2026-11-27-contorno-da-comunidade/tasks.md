# Tasks — Contorno da comunidade

## 1. Modelo e migração

- [x] 1.1 `comunidades/modelo.py`: `ComunidadeVirtual` ganha `contorno` (JSON),
      `contorno_origem_osm` e `contorno_copiado_em`, anuláveis (`RF-08-33`, PRD-08 §8)
- [x] 1.2 Migração Alembic que acrescenta as três colunas em `comunidade_virtual`, com
      `downgrade` que as remove (`RF-08-33`)

## 2. Regra

- [x] 2.1 `comunidades/regra.py`: `gravar_contorno` — só Admin (403), validação da geometria
      e do elemento de origem (422 com o campo), substituição e data da cópia (`RF-08-33`,
      `RN-08-32`)
- [x] 2.2 `ContornoSaida` com geometria, origem, data, crédito e licença, e
      `ComunidadePublicaSaida` levando `contorno` nulo quando não há (`RF-08-34`, `RN-08-31`)
- [x] 2.3 `coletas/regra.py`: `ComunidadeDaListaSaida` leva o mesmo `contorno`, fora da
      supressão do piso (`RF-08-34`, `RN-08-28`)

## 3. Rota

- [x] 3.1 `comunidades/rotas.py`: `PUT /comunidades/{id}/contorno` de Admin, 404 para
      comunidade inexistente, 200 com o contorno gravado (`RF-08-33`, PRD-08 §9)

## 4. Testes

- [x] 4.1 `tests/test_contorno_da_comunidade.py`: cadastro, substituição, geometria inválida
      (ponto, anel aberto, coordenada fora da faixa), origem fora do padrão, 403 para cada
      papel que não é Admin e 404 (`RF-08-33`, `RN-08-32`)
- [x] 4.2 `tests/test_contorno_na_leitura_publica.py`: lista e leitura da comunidade com e
      sem contorno, com crédito e licença; contorno presente abaixo do piso; contorno sem dado
      de coleta; exportação e dicionário sem o contorno e sob CC BY-SA (`RF-08-34`,
      `RN-08-31`, `RN-08-32`)

## 5. Documentação

- [x] 5.1 `openspec/cronograma-de-fatias.md`: fatia 1 do PRD-08 implementada, com o slug, e o
      cabeçalho do bloco volta a `implementado`; `docs/prds/index.md`: PRD-08 volta a
      `implementado`. Nenhuma decisão nova, nenhum documento-fonte a mudar.
