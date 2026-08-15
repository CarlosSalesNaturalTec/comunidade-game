## Why

**PRD de origem:** PRD-01 — núcleo do Backend API, com o recorte alcançando a rota de consulta
entregue pelo PRD-08.

**Requisitos atendidos:** `RF-01-28` (listagens paginadas, que aceitam filtro por comunidade,
período e persona) e `RF-01-18` (toda consulta de dado de comunidade aceita e aplica filtro por
comunidade), sobre a rota que atende `RF-08-17`.

`GET /v1/series-de-coleta/minhas` entrou pela change `ciclo-de-vida-da-serie` devolvendo uma
**lista crua**: sem cursor, sem tamanho de página e sem o contrato que recusa parâmetro
desconhecido. É a única listagem do núcleo fora do contrato — `/locais`, `/chaves`,
`/auditoria`, `/jogos/elenco` e `/solicitacoes-de-local/abertas` usam `PaginaDeResultado` com
`contrato_de_listagem`.

`RF-01-28` é **essencial** e já era vigente quando a rota nasceu, de modo que isto é **correção
de defeito contra requisito vigente**, não decisão nova. Nada se grava em documento-fonte e
nada se move no documento 09: a regra já está escrita, o que faltou foi aplicá-la.

O defeito não é só de forma. Sem tamanho de página, a consulta apura o estado e soma os pontos
de **todas** as séries do Guerreiro(a) a cada chamada — a agregação sobre `registro_de_coleta`
que o `design.md` da fatia anterior já apontava como o ponto a vigiar.

## What Changes

- A rota passa a devolver **`PaginaDeResultado[SerieDoGuerreiroSaida]`**, com `itens` e
  `proximo_cursor`, em vez de uma lista crua (**BREAKING** para quem já consumisse a rota; no
  Ciclo 01 nenhuma aplicação a consome ainda).
- A rota passa a declarar **`contrato_de_listagem`**, ganhando `cursor` e `tamanho` e recusando
  com **422** parâmetro que não declarou (`RF-01-28`).
- A consulta passa a **paginar por cursor**, na mesma régua das demais: ordenação estável e
  cursor opaco, apurando o estado e somando os pontos **apenas das séries da página**.
- O filtro de comunidade **não** se torna obrigatório aqui: a rota já é recortada pela persona
  da sessão, que é o recorte mais estreito que `RF-01-18` admite — a série é sempre do
  Guerreiro(a) em sessão, nunca de comunidade escolhida na requisição (`RN-08-04`).

### Fora do escopo

O que o PRD-08 §3.2 já exclui segue excluído. Além disso, e por não estar em requisito algum:

| Fica de fora                     | Porque                                                       |
| -------------------------------- | ------------------------------------------------------------ |
| Filtro por `estado` na consulta  | Nenhum requisito o pede; e filtrar estado em SQL depende da   |
|                                  | decisão de apuração registrada no documento 02 §1             |
| Totalizar os pontos na série     | Otimização sem requisito; a paginação já limita a agregação   |
| `RF-08-18`, do responsável       | Consulta das séries pela App 07, de outro recorte             |

Nenhuma pendência do documento 09 §1 alcança este recorte, e o PRD-01 §14 não registra
pendência sobre o contrato de listagem — ele está fechado desde a fatia que o criou.

## Capabilities

### New Capabilities

Nenhuma. A consulta já tem capability.

### Modified Capabilities

- `serie-de-coleta`: o requisito da consulta das séries do Guerreiro(a) passa a exigir que ela
  seja **paginada** e obedeça ao contrato de listagem do núcleo, recusando parâmetro
  desconhecido.

## Impact

- `backend/src/nucleo/coletas/regra.py`: `consultar_series_do_guerreiro` passa a receber
  `cursor` e `tamanho` e a devolver uma página, apurando estado e pontos só do que sai nela.
- `backend/src/nucleo/coletas/rotas.py`: a rota declara `contrato_de_listagem` e responde
  `PaginaDeResultado[SerieDoGuerreiroSaida]`.
- `backend/tests/`: testes do cursor, do tamanho de página e da recusa de parâmetro
  desconhecido; os testes já existentes da consulta passam a ler `itens`.
- Sem migração do Alembic e sem mudança em `docs/`: nenhuma regra nova, nenhum número novo e
  nenhuma relação entre documentos alterada.
