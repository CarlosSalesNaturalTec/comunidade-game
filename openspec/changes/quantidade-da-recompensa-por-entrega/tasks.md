## 1. Núcleo

- [ ] 1.1 Em `backend/src/nucleo/recompensas_de_marco/regra.py`, `_validar_entrega`: trocar a
      contagem de entregas da recompensa pela recusa da entrega já feita **àquele**
      Guerreiro(a). A recusa responde 422 no campo `guerreiro_id`, com a mensagem "Este
      Guerreiro(a) já recebeu esta recompensa.". Ordem das recusas: durável, lastro, já
      recebeu, comunidade, marco. O docstring passa a listar as cinco (`RF-07-13`, `RF-09-76`).
- [ ] 1.2 No mesmo arquivo, tirar `quantidade_esgotada` de `PendenciaDeEntrega` e a contagem de
      `listar_entregas_pendentes`, ajustando o docstring (`RF-09-75`).
- [ ] 1.3 Em `backend/src/nucleo/recompensas_de_marco/rotas.py`, tirar `quantidade_esgotada` da
      saída da fila (`RF-09-75`).

## 2. App 09

- [ ] 2.1 Em `apps/app-09-mestre/src/recompensas/api.ts` e `FilaDeEntregasPendentes.tsx`, tirar
      o campo e a marca "quantidade declarada já esgotada", e tirar "quantidade esgotada" do
      comentário da recusa (`RF-09-75`, `RF-09-76`).
- [ ] 2.2 Em `apps/app-09-mestre/src/trilhas/DeclaracaoDeRecompensa.tsx`, trocar o rótulo do
      campo por "Quantidade por Guerreiro(a)" e acrescentar "por Guerreiro(a)" a cada
      recompensa já declarada na lista (`RF-09-71`, `RF-09-84`).

## 3. App 01

- [ ] 3.1 Em `apps/app-01-aula-presencial/src/api/entregasPendentes.ts` e
      `src/entregas/TelaDeEntregasDoEncontro.tsx`, tirar o campo, a marca de esgotada e a menção
      a ela no comentário da recusa (`RF-09-75`, `RF-09-76`).

## 4. Testes

- [ ] 4.1 `backend/tests/test_entrega_de_recompensa.py`: trocar
      `test_quantidade_esgotada_recusa_a_entrega` por dois cenários. No primeiro, a recompensa de
      quantidade 1 é entregue a três Guerreiros(as) com saldo 3, gravando três entregas com
      baixa de 1 cada. No segundo, a segunda entrega ao mesmo Guerreiro(a) responde 422 e não
      move saldo (`RF-07-13`, `RF-09-76`).
- [ ] 4.2 `backend/tests/test_entregas_pendentes.py`: trocar
      `test_quantidade_esgotada_continua_na_fila_marcada` por "entregue a um, a pendência dos
      outros segue na fila", e tirar a asserção sobre `quantidade_esgotada` (`RF-09-75`).
- [ ] 4.3 Testes das Apps 09 e 01: tirar `quantidade_esgotada` dos dados de exemplo em
      `FilaDeEntregasPendentes.test.tsx` e em `entregas.test.tsx`. Nos testes da declaração,
      cobrir o rótulo "Quantidade por Guerreiro(a)" (`RF-09-75`, `RF-09-84`).

## 5. Documentação

- [ ] 5.1 Documento 02 §8.1: acrescentar à tabela a linha "Quantidade", que diz o que cada
      Guerreiro(a) recebe por entrega, uma entrega por Guerreiro(a), e que o limite é o lastro.
      Documento 09 §1, "Já decididos": registrar a decisão do fundador de 2026-11-09 apontando o
      02 §8.1. PRD-04 §5, passo 6: trocar "quantidade esgotada" por "recompensa já entregue".
      O documento 99 não muda.
- [ ] 5.2 `openspec/cronograma-de-fatias.md`, bloco do PRD-07: na linha sem número "Quantidade
      da recompensa por entrega", trocar a situação para `implementado` e pôr o slug no
      arquivamento.
