## 1. Modelo de dados e migração

- [x] 1.1 Criar o modelo `CriacaoOriginal` com Guerreiro(a) autor (`ComAutoria`), trilha,
      produção entregue, situação (`entregue`, `validada`, `devolvida`), `validado_por_id` e
      `validado_em` nuláveis, e `UniqueConstraint(guerreiro_id, trilha_id)` (`RF-01-26`,
      `RN-01-13`, design — decisões).
- [x] 1.2 Adicionar o valor `de_autoria` a `TipoDeBadge` (`RF-01-21`, 11 §7).
- [x] 1.3 Escrever a sétima migração Alembic criando `criacao_original` e alterando o enum de
      `TipoDeBadge` para incluir `de_autoria`, sem tocar as tabelas das fatias anteriores, e
      conferir que ela sobe e desce.

## 2. Entrega da criação original

- [x] 2.1 Implementar a entrega de uma criação original pelo próprio Guerreiro(a), exigindo
      trilha e produção declarada, recusando com 422 o que faltar; situação inicial "entregue"
      (`RF-01-26`).
- [x] 2.2 Verificar: entrega com trilha, Guerreiro(a) e produção grava o registro; entrega sem
      produção recebe 422 e nada é gravado (`RF-01-26`).

## 3. Validação e devolução

- [x] 3.1 Implementar a validação e a devolução restritas ao Mestre autor da trilha ou a um
      Admin, reaproveitando `conferir_posse_da_trilha`; Mestre que não é o autor recebe 403 e a
      situação não muda (`RF-01-26`, `RF-01-16`).
- [x] 3.2 Implementar a recusa de validar ou devolver um registro que não está com situação
      "entregue" — impede crédito duplo por chamada repetida (design — decisões).
- [x] 3.3 Verificar: Mestre autor valida e a situação muda para "validada"; Mestre autor devolve
      e a situação muda para "devolvida"; Mestre que não é o autor recebe 403; validar ou
      devolver um registro já validado ou devolvido é recusado (`RF-01-26`, `RF-01-16`).

## 4. Autoria permanente

- [x] 4.1 Verificar: devolver uma criação original entregue mantém o `autor_id` original — a
      devolução muda situação, nunca autor (`RN-01-13`).

## 5. Crédito de pontos, nível 5 e badge de autoria

- [x] 5.1 Implementar `creditar_pontuacao_da_criacao_original` em `pontuacao/regra.py`: credita
      50 pontos regulares integrais na trilha da criação, ao validar (`RF-01-21`, 11 §5, design
      — decisões).
- [x] 5.2 Implementar a certificação do nível 5 — Mestre Aprendiz — quando a criação original da
      trilha é validada e o Guerreiro(a) ainda não tem o nível 5 certificado naquela trilha
      (`RF-01-21`, 11 §6).
- [x] 5.3 Implementar a concessão do badge `de_autoria` ao validar a criação original
      (`RF-01-21`, 11 §7).
- [x] 5.4 Ligar a validação de `CriacaoOriginal` ao ponto de entrada único de crédito, na mesma
      transação da mudança de situação (design — decisões).
- [x] 5.5 Verificar: validar credita 50 pontos regulares à trilha e ao Guerreiro(a) autor;
      certifica o nível 5 uma única vez; concede o badge de autoria; devolver não credita nada
      (`RF-01-21`, 11 §§5–7).

## 6. Esteira do backend

- [x] 6.1 Rodar `ruff format --check`, `ruff check` e `pytest` com a cobertura publicada no log,
      sem limiar que bloqueie. A fatia não cria pasta de topo, então não nasce workflow novo:
      `backend-ci.yml` já cobre `backend/**`.

## 7. Documentação

- [x] 7.1 Conferir que nenhuma decisão nova desta fatia ficou fora de `docs/` — a régua de
      pontos, níveis e badges já está no documento 11 §§5–7 e não muda.
- [x] 7.2 Atualizar `docs/prds/index.md` se a situação do PRD-01 mudar ao fim desta fatia.
- [x] 7.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR.
