## 1. Modelo de dados e migração

- [ ] 1.1 Criar o modelo `Resultado` com Guerreiro(a), atividade, data do fato, produção e
      desfecho — `realizada`, `realizada_com_merito` ou `merito_extra_por_auxilio` — como
      enumeração fechada, com `ComAutoria` (`RF-01-20`, 11 §4, design — decisões).
- [ ] 1.2 Criar o modelo `PontoRegular` por Guerreiro(a) e trilha, e o modelo `Nivel` certificado
      por Guerreiro(a), trilha e valor (1, 2 ou 4), com data de certificação (`RF-01-21`, 11 §6,
      design — decisões).
- [ ] 1.3 Criar o modelo `Badge` certificado por Guerreiro(a), trilha ou poder e tipo — `de_nivel`
      ou `de_valores_e_causas` —, com data de certificação (`RF-01-21`, 11 §7).
- [ ] 1.4 Criar o modelo `PontoExtra` por Guerreiro(a), com `acumulado` e `saldo_disponivel`
      (`RF-01-56`, 11 §5, design — decisões).
- [ ] 1.5 Escrever a sexta migração Alembic criando `resultado`, `ponto_regular`, `nivel`,
      `badge` e `ponto_extra`, sem tocar as tabelas das fatias anteriores, e conferir que ela
      sobe e desce.

## 2. Resultado

- [ ] 2.1 Implementar o registro de Resultado exigindo Guerreiro(a), atividade, data do fato e
      produção, recusando com 422 o que faltar (`RF-01-20`, 11 §§2.2, 4).
- [ ] 2.2 Implementar o lançamento do desfecho restrito ao Mestre autor da trilha da atividade e
      ao Admin, pela mesma conferência de posse da quinta fatia (`trilhas/regra.py`), recusando
      outro Mestre com 403 (`RF-01-16`, `RF-01-03`).
- [ ] 2.3 Verificar: Resultado sem atividade, sem Guerreiro(a) ou sem produção recebe 422;
      desfecho fora dos três valores recebe 422; Mestre que não é o autor recebe 403; a autoria
      de quem lançou fica gravada (`RF-01-20`, `RF-01-16`, `RF-01-03`).

## 3. Ponto regular

- [ ] 3.1 Implementar a regra de crédito: valor-base 20 se a modalidade da atividade for
      `em_equipe_com_familiar`, 10 nas demais; +5 regular se o desfecho for
      `realizada_com_merito`; +10 regular se for `merito_extra_por_auxilio` (`RF-01-21`,
      `RN-01-38`, 11 §5, design — decisões).
- [ ] 3.2 Implementar a recusa de qualquer operação de débito sobre `PontoRegular` (`RN-01-38`).
- [ ] 3.3 Verificar: Resultado "realizada" credita o valor-base pela modalidade; "realizada com
      mérito" credita o valor-base mais 5; nenhuma via debita o ponto regular (`RF-01-21`,
      `RN-01-38`).

## 4. Nível

- [ ] 4.1 Implementar a certificação do nível 1 — inscrito na trilha e primeira atividade com
      Resultado — por trilha (`RF-01-21`, 11 §6).
- [ ] 4.2 Implementar a certificação do nível 2 — um terço das missões obrigatórias com Resultado
      — por trilha (`RF-01-21`, 11 §6).
- [ ] 4.3 Implementar a certificação do nível 4 — todas as obrigatórias com Resultado e ao menos
      um Resultado `merito_extra_por_auxilio` — por trilha (`RF-01-21`, 11 §6).
- [ ] 4.4 Implementar a não regressão: nível certificado nunca é removido, mesmo que o critério
      deixe de valer depois (`RF-01-21`, 11 §6, design — decisões).
- [ ] 4.5 Verificar: primeira atividade certifica nível 1; um terço das obrigatórias certifica
      nível 2; todas as obrigatórias mais o mérito de auxílio certificam nível 4; nível já
      certificado permanece após o critério deixar de valer (`RF-01-21`, 11 §6).

## 5. Badge

- [ ] 5.1 Implementar a concessão do badge `de_nivel` a cada nível certificado (`RF-01-21`,
      11 §7).
- [ ] 5.2 Implementar a concessão do badge `de_valores_e_causas` a Resultado de atividade de
      natureza "valores e temas transversais" (`RF-01-21`, 11 §7).
- [ ] 5.3 Verificar: certificar um nível concede o badge de nível correspondente; Resultado de
      atividade de valores e causas concede o badge correspondente; nenhum badge nasce global,
      sempre vinculado a trilha ou poder (`RF-01-21`, 11 §7).

## 6. Ponto extra

- [ ] 6.1 Implementar o crédito simultâneo de `acumulado` e `saldo_disponivel` a partir de
      Resultado com desfecho `realizada_com_merito` (+5/+5) ou `merito_extra_por_auxilio`
      (+10/+10), na mesma transação do crédito ao ponto regular (`RF-01-56`, 11 §5).
- [ ] 6.2 Implementar a recusa de qualquer operação que reduza o `acumulado` ou que deixe o
      `saldo_disponivel` negativo (`RN-01-39`, `RN-01-40`).
- [ ] 6.3 Verificar: "realizada com mérito" credita 5 nas duas contas de extra; "mérito extra por
      auxílio" credita 10; nenhuma via reduz o acumulado; nenhuma via deixa o saldo negativo
      (`RF-01-56`, `RN-01-39`, `RN-01-40`).

## 7. Esteira do backend

- [ ] 7.1 Rodar `ruff format --check`, `ruff check` e `pytest` com a cobertura publicada no log,
      sem limiar que bloqueie. A fatia não cria pasta de topo, então não nasce workflow novo:
      `backend-ci.yml` já cobre `backend/**`.

## 8. Documentação

- [ ] 8.1 Conferir que nenhuma decisão nova desta fatia ficou fora de `docs/` — a régua de
      pontos, níveis e badges já está no documento 11 §§5–7 e não muda.
- [ ] 8.2 Atualizar `docs/prds/index.md` se a situação do PRD-01 mudar ao fim desta fatia.
- [ ] 8.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR.
