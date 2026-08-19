## 1. Decisões novas em `docs/`, antes do código

- [x] 1.1 Gravar as decisões 1 e 4 no documento 02 §8.2 — o encontro da troca é a `Aula` e o
      núcleo não verifica estado nem presença; a troca exige Guerreiro(a) da comunidade do item
      — e a decisão 3 no documento 04 §1 — o débito da troca não declara aula. Uma linha cada,
      sem repetir tabela nem número (`RF-07-35`, `RF-07-36`, `RF-07-37`).
- [x] 1.2 Mover as quatro decisões para "Já decididos" no documento 09, e aplicá-las ao PRD-07:
      a rota `POST /aulas/{id}/trocas` na §9, a `Troca` e o débito sem aula na §8, e as quatro
      linhas na §13 (`RF-07-35`, `RF-07-46`).

## 2. Modelo e migração

- [x] 2.1 Criar `backend/src/nucleo/trocas/modelo.py` com a `Troca` — item, Guerreiro(a),
      `preco_cobrado` em pontos extras, aula, Mestre que entregou, data e hora com fuso —, com
      as chaves estrangeiras para `item_de_catalogo_avulso`, `persona` e `aula` (`RF-07-35`,
      `RF-07-46`, `RF-01-27`).
- [x] 2.2 Migração Alembic da tabela `troca`, com índice por Guerreiro(a) e por aula, para a
      leitura do histórico (`RF-07-35`).

## 3. Regra da troca

- [x] 3.1 Escrever em `trocas/regra.py` a validação das quatro recusas, na ordem do spec — item
      inativo ou sem lastro reverificado por `saldo_de` no ato, estoque zero, comunidade do
      Guerreiro(a) diferente da do item, saldo disponível menor que o preço —, devolvendo a
      condição que recusou para a resposta 422 nomeá-la (`RF-07-37`, `RN-07-26`, `RN-01-40`).
- [x] 3.2 Ler o preço em `catalogo_de_tipos_de_recurso` pela vigência corrente na data e recusar
      com 422 quando não houver vigência que a cubra (`RF-07-46`, `RF-07-38`, `RN-07-29`).
- [x] 3.3 Escrever a operação única de entrega — grava a `Troca` com o preço cobrado, debita o
      saldo disponível de pontos extras sem tocar o acumulado, decrementa o estoque em uma
      unidade e emite `lancar_debito` de quantidade 1 no ponto de apoio do item com
      `aula_id=None`, valorado pela vigência do valor de referência na data —, travando a linha
      do item antes de verificar estoque e lastro (`RF-07-36`, `RN-07-27`, `RF-01-56`,
      `RN-01-39`, `RN-07-36`, design — Decisions 3, 4, 6, 7).
- [x] 3.4 Estender `ponto_extra/regra.py` com o débito do saldo disponível, recusado quando
      deixaria o saldo negativo, sem caminho algum que reduza o acumulado (`RF-01-56`,
      `RN-01-39`, `RN-01-40`).
- [x] 3.5 Escrever a leitura do histórico filtrada por persona — Guerreiro(a) só as próprias,
      Mestre as das comunidades a que está vinculado, Admin todas, Apoiador e responsável 403 —,
      sem moedas e sem reais na saída (`RF-07-35`, `RN-07-24`, `RN-07-13`).

## 4. Rotas

- [x] 4.1 Criar `trocas/rotas.py` com `POST /aulas/{id}/trocas`, exigindo Mestre em sessão
      vinculado à comunidade da aula, recusando preço declarado no corpo com 422 e devolvendo
      201 (`RF-07-35`, `RF-07-46`, `RF-01-16`).
- [x] 4.2 Acrescentar `GET /trocas` no mesmo roteador e registrá-lo em `principal.py` por
      `incluir_roteador_de_dados` (`RF-07-35`, `RF-01-01`).

## 5. Testes

- [x] 5.1 `backend/tests/test_trocas.py` — grupo do registro e das permissões: Mestre registra e
      grava os seis atributos; aula não realizada e Guerreiro(a) sem presença não impedem;
      Mestre de outra comunidade e Guerreiro(a) recebem 403; registro sem item devolve 422
      (`RF-07-35`).
- [x] 5.2 Grupo do preço: cobra a vigência corrente e grava o valor; mudança posterior da tabela
      não altera troca gravada; preço no corpo devolve 422; tipo sem preço vigente devolve 422
      (`RF-07-46`, `RF-07-38`).
- [x] 5.3 Grupo das recusas: as quatro condições, cada uma com a resposta nomeando o motivo, e o
      caso de recusa que não move troca, lançamento, estoque nem saldo. Inclui o lastro caído
      desde a ativação (`RF-07-37`, `RN-07-26`, `RN-07-30`).
- [x] 5.4 Grupo da entrega: as quatro escritas juntas com os números do cenário do spec (saldo
      100→60, estoque 5→4, saldo do tipo 5→4, acumulado 300 intacto); falha em qualquer parte
      desfaz tudo; nenhuma reserva de item é criada; estoque zerado por troca mantém o item
      cadastrado e ativo (`RF-07-36`, `RN-07-27`, `RN-01-39`).
- [x] 5.5 Grupo do histórico: Guerreiro(a) lê só as próprias, troca de outro nunca aparece,
      Mestre lê as das suas comunidades, Apoiador recebe 403, e nenhuma resposta traz moedas nem
      reais (`RF-07-35`, `RN-07-24`).
- [x] 5.6 Acrescentar em `backend/tests/test_lancamento.py` os dois cenários do delta — o
      débito da troca é gravado sem aula, e o consumo por aula soma só o débito da baixa
      (`RF-07-36`, `RF-07-16`, `RN-07-15`). O arquivo desta capacidade já existia com esse nome
      (`test_lancamento.py`, não `test_livro_razao.py`); os cenários entraram nele.

## 6. Documentação

- [x] 6.1 Atualizar `docs/prds/index.md` com a oitava fatia do PRD-07: a troca entregue, as
      quatro decisões novas e o que segue para as próximas fatias — patrimônio e desafio extra.
      Nenhum arquivo novo em `docs/`, logo a `nav` do `mkdocs.yml` não muda; o documento 99 não
      muda, porque nenhuma relação entre documentos mudou.
