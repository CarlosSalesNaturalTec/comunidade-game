# Tasks

## 1. Dados

- [x] 1.1 `aulas/modelo.py`: coluna `pontos_extras_creditados` (inteiro, não nulo, padrão 0) em
      `Presenca` (`RF-01-82`, `RN-01-65`, design — decisão 1).
- [x] 1.2 `ponto_extra/modelo.py`: o _listener_ e o gatilho admitem a redução do acumulado só
      sob o marcador `cg.estorno_de_presenca` da transação; o `DELETE` segue recusado
      (`RN-01-39`, `RN-01-64`, design — decisão 4).
- [x] 1.3 `recursos/modelo.py` e `recursos/regra.py`: piso de 25 no `CHECK` e em
      `PISO_DE_PONTOS_EXTRAS`, com as docstrings (`RF-07-44`, `RN-07-30`).
- [x] 1.4 Migração Alembic: a coluna da presença, com as existentes em 0; a função e o gatilho
      novos do ponto extra; as vigências de 25 para todo preço aberto abaixo de 25, encerrando
      a anterior; e o `CHECK` de 25 `NOT VALID`, nessa ordem (`RF-07-50`, `RN-01-65`, design —
      decisões 1, 4 e 5).

## 2. Regra

- [x] 2.1 `ponto_extra/regra.py`: constante `PONTOS_EXTRAS_DA_PRESENCA = 5` e
      `estornar_ponto_extra_da_presenca`, que liga o marcador, tira o valor do acumulado e até
      o valor do saldo, parando em zero (`RF-01-83`, `RN-01-64`, design — decisões 3 e 4).
- [x] 2.2 `aulas/regra.registrar_presenca`: a presença nova credita 5 extras e grava o valor na
      coluna; a devolvida pelo reenvio não credita (`RF-01-82`, `RF-01-20`).
- [x] 2.3 `aulas/regra.anular_presenca`: estorna o valor da coluna na mesma transação, sem
      recusar por saldo; coluna em 0 não toca o ponto extra (`RF-01-83`, `RN-01-65`,
      `RF-02-36`).

## 3. App 05

- [x] 3.1 `MinhaCarteira.tsx` e o teste dela: o aviso troca "O acumulado só cresce" por "Trocar
      não diminui o acumulado" (`RF-01-56`, `RN-05-40`).

## 4. Testes

- [x] 4.1 `tests/test_ponto_extra.py`: o estorno tira das duas contas, para o saldo em zero, e
      a redução do acumulado fora do estorno segue recusada pelo ORM e por SQL direto
      (`RN-01-39`, `RN-01-64`; cenários "Acumulado nunca decresce", "Anulação estorna das
      duas contas", "Estorno com o saldo já trocado para em zero").
- [x] 4.2 `tests/test_presenca_do_mestre.py`: crédito nos dois modos, reenvio sem crédito
      duplo, anulação que estorna, presença correta depois da anulação, presença com coluna
      em 0 que não estorna (`RF-01-82`, `RF-01-83`, `RN-01-65`; cenários da capacidade
      `ponto-extra` e "A anulação estorna os extras da presença").
- [x] 4.3 `tests/test_preco_de_referencia.py`: 25 aceito, 24 recusado com o piso no erro,
      vigência nova abaixo de 25 recusada (`RF-07-44`, `RN-07-30`); e os testes que registram
      preço entre 20 e 24 ou somam extras depois de uma presença passam aos valores novos.
- [x] 4.4 `tests/test_migracoes.py`: a migração eleva o preço aberto de 20 a 25 e não toca o de
      40, e a consulta por data anterior lê o preço antigo (`RF-07-50`, `RF-07-43`).

## 5. Documentação

- [x] 5.1 PRD-01: `RF-01-82`, `RF-01-83`, `RN-01-64`, `RN-01-65` nas §§6, 7 e 15, e o
      enunciado de `RF-01-56` e `RN-01-39` com a exceção do estorno. PRD-07: `RF-07-50` e o
      piso de 25 em `RF-07-44`, `RN-07-30` e nas §§13 e 15. PRDs 04 (`RN-04-24`), 05 (§2 e
      §14), 09 e 14: o acumulado com a exceção e o piso de 25. Documentos-fonte, 09 §1 e 99 §6
      já foram atualizados antes da change; `docs/prds/index.md` e a `nav` não mudam.
- [ ] 5.2 `openspec/cronograma-de-fatias.md`: a linha da fatia passa a `implementado`, com o
      slug arquivado.
