## 1. Modelo de dados e migração

- [ ] 1.1 Criar o modelo `Aula` com comunidade, `inicio_em` e `fim_em` em
      `DateTime(timezone=True)`, `ComAutoria` e `CheckConstraint` de `fim_em > inicio_em`
      (`RF-01-20`, `RF-01-03`, design — decisões).
- [ ] 1.2 Criar o modelo `Presenca` com aula, Guerreiro(a), modo de comprovação — enumeração
      fechada de `reconhecimento` e `confirmacao` —, confirmador opcional, `ComAutoria`,
      `ComMomentoDoFato` e unicidade `(aula_id, guerreiro_id)` (`RF-01-20`, `RF-01-03`).
- [ ] 1.3 Criar o modelo `Equipe` com `aula_id` e `trilha_id` anuláveis, `CheckConstraint` de
      exatamente um dos dois preenchido, `homologado_por_id` e `homologado_em` anuláveis e
      `ComAutoria` (`RF-01-37`, `RF-01-63`, design — decisões).
- [ ] 1.4 Criar o modelo `IntegranteDaEquipe` com equipe, persona, papel em texto livre opcional
      e unicidade `(equipe_id, persona_id)` (`RF-01-37`, `RF-01-64`).
- [ ] 1.5 Escrever a nona migração Alembic na ordem do design — Migration Plan: criar `aula`,
      `presenca`, `equipe` e `integrante_da_equipe`; acrescentar `equipe_id` anulável a
      `criacao_original`; fazer o backfill de uma equipe da trilha homologada, de um integrante,
      por criação original existente; tornar `equipe_id` obrigatória e trocar a unicidade de
      `(autor_id, trilha_id)` por `(equipe_id)`. Conferir que ela sobe e desce (`RF-01-64`,
      `RN-01-13`, design — Migration Plan).

## 2. Aula agendada

- [ ] 2.1 Implementar o agendamento de aula restrito à operação `tudo` (Admin), recusando com
      403 os demais papéis (`RF-01-20`, `RF-01-16`, `RF-01-03`).
- [ ] 2.2 Implementar a recusa com 422, indicando o campo em falta, de aula sem comunidade, sem
      instante inicial ou sem instante final, e de aula cujo `fim_em` não seja posterior ao
      `inicio_em` (`RF-01-20`).
- [ ] 2.3 Implementar `aulas_vigentes`, que devolve todas as aulas cujo intervalo contém o
      momento corrente de `tempo.agora()`, e conjunto vazio quando não há nenhuma (`RF-01-32`,
      `RF-01-18`, design — decisões).
- [ ] 2.4 Verificar: Admin agenda aula com autoria gravada; Mestre recebe 403; aula sem
      comunidade recebe 422; horário final anterior ao inicial recebe 422; aula em curso aparece
      entre as vigentes e aula fora do horário não aparece; duas comunidades no mesmo horário
      devolvem duas aulas; sem aula agendada a derivação devolve vazio (`RF-01-20`, `RF-01-32`,
      `RF-01-16`).

## 3. Presença

- [ ] 3.1 Implementar o registro de presença com o modo de comprovação, exigindo o confirmador
      quando o modo for `confirmacao` e recusando com 422 na falta dele (`RF-01-20`, `RF-01-03`).
- [ ] 3.2 Implementar a recusa com 422 da presença de Guerreiro(a) em aula de comunidade
      diferente da dele (`RF-01-20`, `RN-01-05`, `RF-01-18`).
- [ ] 3.3 Implementar a idempotência: achando presença já gravada para `(aula, guerreiro)`,
      devolver a existente com o confirmador e o momento originais, sem duplicar e sem erro
      (`RF-01-20`, PRD-01 §10, design — decisões).
- [ ] 3.4 Verificar: presença por reconhecimento grava sem confirmador; presença por confirmação
      grava quem confirmou; confirmação sem confirmador recebe 422; presença em comunidade alheia
      recebe 422; reenvio da mesma presença mantém um registro só, sem erro, preservando
      confirmador e momento originais (`RF-01-20`, `RF-01-03`).

## 4. Equipe — vínculo, criação e composição

- [ ] 4.1 Implementar a criação de equipe restrita à operação do Guerreiro(a), gravando quem
      criou como primeiro integrante, e recusando com 403 a tentativa de Admin ou Mestre de
      criar equipe ou alterar composição (`RF-01-37`, `RF-01-16`, invariante 15).
- [ ] 4.2 Acrescentar à matriz de permissões a operação de escrita da equipe pelo Guerreiro(a),
      alcançando os dois tempos de vida, conforme a célula atualizada do PRD-01 §4 (`RF-01-16`,
      `RF-01-37`, `RF-01-63`).
- [ ] 4.3 Implementar a recusa com 422 de equipe sem vínculo e de equipe vinculada a aula e
      trilha ao mesmo tempo (`RF-01-37`, `RF-01-63`, design — decisões).
- [ ] 4.4 Implementar `TETO_DE_INTEGRANTES = 5` e `TETO_DE_INTEGRANTES_NAO_GUERREIROS = 1`,
      conferidos por contagem na mesma transação da inserção, recusando com 422 o sexto
      integrante e o segundo integrante cujo papel não seja Guerreiro(a) (`RF-01-38`, design —
      decisões).
- [ ] 4.5 Implementar o papel do integrante como texto livre opcional, sem efeito sobre
      pontuação nem composição (`RF-01-64`, documento 02 §§4, 5).
- [ ] 4.6 Verificar: quem cria entra como primeiro integrante; Admin e Mestre recebem 403 ao
      criar equipe ou mexer em composição; equipe sem vínculo e com os dois vínculos recebem 422;
      quinto integrante é aceito e sexto recebe 422; primeiro integrante não-Guerreiro(a) é
      aceito e segundo recebe 422; papel declarado é gravado, papel ausente é aceito e dois
      papéis diferentes creditam igual (`RF-01-37`, `RF-01-38`, `RF-01-64`, `RF-01-16`).

## 5. Equipe da aula e equipe da trilha

- [ ] 5.1 Implementar a trava da equipe da aula: encerrada a aula, recusar com 422 entrada e
      saída de integrante, e nunca devolvê-la entre as equipes de outra aula (`RF-01-37`).
- [ ] 5.2 Implementar a aceitação do mesmo Guerreiro(a) em mais de uma equipe da mesma aula
      (`RF-01-39`).
- [ ] 5.3 Implementar a trava de uma equipe da trilha por Guerreiro(a) e trilha, recusando com
      422 a entrada numa segunda equipe da mesma trilha e aceitando equipes de trilhas
      diferentes (`RN-01-44`).
- [ ] 5.4 Implementar a homologação da equipe da trilha, restrita a Mestre ou Admin, gravando
      `homologado_por_id` e `homologado_em`, e recusando com 403 a tentativa do Guerreiro(a)
      (`RF-01-63`, `RF-01-16`).
- [ ] 5.5 Acrescentar à matriz de permissões a operação de homologação da equipe da trilha pelo
      Mestre, conforme a célula atualizada do PRD-01 §4 (`RF-01-16`, `RF-01-63`).
- [ ] 5.6 Implementar a fixidez: com `homologado_em` preenchido, recusar com 422 entrada e saída
      de integrante, sem conferir onde a homologação aconteceu (`RN-01-44`, `RF-01-63`).
- [ ] 5.7 Verificar: equipe de uma aula não aparece em outra e não recebe integrante depois de
      encerrada; mesmo Guerreiro(a) em duas equipes da aula; segunda equipe da mesma trilha
      recebe 422 e equipes de trilhas diferentes convivem; Mestre homologa e a composição
      congela; entrada e saída após a homologação recebem 422; Guerreiro(a) que tenta homologar
      recebe 403; equipe da trilha ainda não homologada aceita composição (`RF-01-37`,
      `RF-01-39`, `RF-01-63`, `RN-01-44`).

## 6. Criação original e pontuação em equipe

- [ ] 6.1 Vincular `CriacaoOriginal` à equipe da trilha, mantendo `autor_id` com o sentido de
      quem entregou pela equipe, e recusar com 422 a entrega sem equipe da trilha (`RF-01-26`,
      `RF-01-64`, design — Migration Plan).
- [ ] 6.2 Implementar a recusa com 403 da entrega feita por quem não integra a equipe, e com 422
      da segunda entrega da mesma equipe na mesma trilha (`RF-01-26`, `RF-01-64`, `RN-01-44`).
- [ ] 6.3 Alterar `creditar_pontuacao_da_criacao_original` para creditar os 50 pontos regulares
      integrais a **cada** integrante da equipe, sem rateio pelo tamanho, e remover o comentário
      "sem equipe nesta fatia" de `pontuacao/regra.py` (`RF-01-21`, `RF-01-64`, 11 §5).
- [ ] 6.4 Alterar `certificar_nivel_5` e `conceder_badge_de_autoria` para alcançar cada
      integrante da equipe da trilha (`RF-01-21`, `RF-01-64`, 11 §§6, 7).
- [ ] 6.5 Verificar: entrega sem equipe recebe 422; quem não integra recebe 403; segunda entrega
      da mesma equipe recebe 422; devolução preserva equipe e integrantes; validação credita 50
      pontos, nível 5 e badge de autoria a cada um dos integrantes; equipes de tamanhos
      diferentes creditam os mesmos 50 por integrante (`RF-01-26`, `RF-01-64`, `RN-01-13`,
      `RF-01-21`).
- [ ] 6.6 Verificar que o backfill da migração preserva a autoria de toda criação original
      existente — uma equipe homologada de um integrante, com o autor original — e que a
      reversão devolve a unicidade antiga sem perda (`RN-01-13`, design — Migration Plan).

## 7. Esteira do backend

- [ ] 7.1 Rodar `ruff format --check`, `ruff check` e `pytest` com a cobertura publicada no log,
      sem limiar que bloqueie. A fatia não cria pasta de topo, então não nasce workflow novo:
      `backend-ci.yml` já cobre `backend/**`.

## 8. Documentação

- [ ] 8.1 Conferir que a decisão da equipe fixa segue registrada onde foi gravada antes desta
      change — documentos 02 §§4 e 5, 09, 99 invariante 15 e PRD-01 §§4, 6, 7, 8, 12 e 15 — e
      que a implementação não divergiu de nenhum desses textos.
- [ ] 8.2 Atualizar `docs/prds/index.md` se a situação do PRD-01 mudar ao fim desta fatia.
- [ ] 8.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR.
