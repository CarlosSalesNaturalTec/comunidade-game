## Context

A regra de `etiqueta-ods` está inteira e testada em `backend/src/nucleo/ods/regra.py`; falta a
porta HTTP e a leitura. Ver `proposal.md` — Why. As duas fatias anteriores do PRD-09 fixaram o
padrão que esta segue: módulo com `rotas.py` próprio, conferência de autoria na **regra**, e
recusa antes de qualquer escrita.

Duas restrições moldam o desenho:

- **Nenhuma entidade referencia `EtiquetaOds.id`.** O `DesafioDeColeta` resolve a etiqueta por
  derivação a cada leitura (`resolver_etiquetas_do_desafio`), e a spec vigente já exige que a
  troca acompanhe. Apagar uma etiqueta não deixa ponta solta em lugar nenhum.
- **Não há etiqueta gravada em produção.** O módulo nunca teve porta: nenhum Mestre etiquetou
  nada. Toda mudança de comportamento desta fatia é, na prática, comportamento inaugural.

## Goals / Non-Goals

**Goals:**

- Uma porta de escrita por alvo — trilha e missão —, idempotente e atômica.
- Autoria estrita aplicada na **regra**, não só na rota, para que nenhum caminho futuro escape.
- Leitura das etiquetas e da cobertura junto da trilha, sem rota nova de leitura.

**Non-Goals:**

- Alterar `EtiquetaOds`. O modelo fica como está — sem migração Alembic.
- Reabrir a agregação por poder, comunidade e ciclo, já entregue e legível na vitrine.
- Trava de publicação por falta de etiqueta — é do Ciclo 02 (ver `proposal.md` — Fora do escopo).

## Decisions

### 1. Substituir é apagar o conjunto do alvo e gravar o recebido, na mesma transação

Alternativa descartada: conciliar a lista recebida com a existente, preservando as linhas de
objetivo repetido. Custa mais código para produzir **o mesmo estado observável** — o conjunto
de objetivos —, que é o que a spec define e o que a cobertura lê.

A conciliação só se pagaria se algo apontasse para `EtiquetaOds.id` ou se a autoria por linha
importasse. Nenhum dos dois vale: nada referencia o `id`, e com a autoria estrita da decisão 2
o autor recriado é sempre o mesmo Mestre que já constava.

### 2. A autoria estrita entra dentro de `criar_etiqueta_ods`, não na rota

`criar_etiqueta_ods` troca `conferir_posse_da_trilha` por `conferir_autoria_estrita_da_trilha`
(`backend/src/nucleo/trilhas/regra.py`). Pôr a conferência na rota deixaria a regra permissiva
para qualquer chamador futuro — e a regra é o que a semeadura, os testes e as outras fatias
usam.

Consequência assumida: **um teste vigente afirma o contrário e precisa inverter** —
`test_admin_etiqueta_trilha_de_qualquer_mestre`, em `backend/tests/test_ods.py`, passa a
afirmar que o Admin é recusado. Os demais chamadores de `criar_etiqueta_ods` nos testes usam o
Mestre autor, ou um Admin que é o próprio autor da trilha do cenário — esses seguem passando,
porque a conferência estrita olha a autoria, não o papel.

### 3. Rota nova em `ods/rotas.py`, não dentro de `trilhas/rotas.py`

As duas rotas são de ODS, ainda que o caminho seja `/trilhas/{id}/ods` e `/missoes/{id}/ods`.
O módulo ganha a sua porta, como todos os outros, e `principal.py` registra o roteador pelo
`incluir_roteador_de_dados` já existente. Alternativa descartada: pendurar em `trilhas/rotas.py`
por causa do prefixo da URL — o prefixo é do recurso pai, não do dono da regra.

### 4. Todas as recusas antes de qualquer escrita

A rota confere autoria e valida **todos** os objetivos da lista recebida antes de apagar
qualquer coisa. Uma etiqueta inválida no meio da lista recusa a operação inteira e o conjunto
anterior permanece — comportamento que a spec exige e que a validação tardia entregaria só por
efeito do rollback, sem garantia de ordem.

### 5. A cobertura sai junto da trilha, com o rótulo do ciclo

`cobertura_por_trilha` já existe e devolve `set[int]`. As saídas de trilha passam a carregá-la
acompanhada de `configuracao.ciclo_rotulo` — o mesmo rótulo declarado na implantação que
`GET /vitrine/ods/cobertura` já usa. Alternativa descartada: rota própria de cobertura por
trilha, que faria a App 09 buscar duas vezes o que uma leitura resolve.

## Risks / Trade-offs

- **A confirmação reescreve linhas que o Mestre não mexeu** (novo `id` e nova data para a
  etiqueta mantida) → o estado observável definido pela spec é o **conjunto de objetivos**, não
  a identidade da linha; e a trilha de auditoria é do middleware, que registra a operação HTTP,
  não a linha tocada.
- **Admin perde uma capacidade que o código dava** → não havia porta, logo nenhum Admin a
  exerceu; e o documento 11 e a spec sempre disseram que quem declara é o Mestre autor. É o
  código alcançando a fonte, não uma retirada.
- **A leitura pública passa a expor as etiquetas** → é rótulo descritivo de trilha, sem dado de
  pessoa; a cobertura sai agregada por trilha e nunca por Guerreiro(a), como `RN-01-24` exige.

## Migration Plan

Sem migração de dados e sem migração Alembic: `EtiquetaOds` não muda e não há linha gravada em
produção. O deploy é o registro do roteador novo e as saídas ampliadas — ambos aditivos para
quem já consome `GET /v1/trilhas/{id}`.
