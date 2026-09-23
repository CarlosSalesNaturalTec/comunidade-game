# Tasks

## 1. Núcleo — PIN de confirmação

- [ ] 1.1 Migração Alembic e modelo: `persona.pin_verificador` (JSON, nulo) e
      `sessao.erros_de_pin_seguidos` (inteiro, padrão 0) — `RF-01-75`, `RN-01-59`, design 1 e
      3. Verificar: `alembic upgrade head` e `downgrade -1` rodam no Postgres de teste.
- [ ] 1.2 Módulo `pin_de_confirmacao` (regra e rotas): derivação PBKDF2-HMAC-SHA256 com sal e
      iterações no verificador, `PUT /v1/eu/pin-de-confirmacao` (4 dígitos, só Mestre e Admin,
      operação nova na matriz) e `GET /v1/eu/pin-de-confirmacao/verificador` (só a chave do App
      01, erro `pin_nao_cadastrado` sem PIN); `GET /v1/eu` ganha `tem_pin_de_confirmacao` —
      `RF-01-75`, `RN-04-38`. Verificar: testes da 4.1.
- [ ] 1.3 Conferência do PIN e bloqueio: erros `pin_recusado`, `pin_bloqueado` e
      `pin_nao_cadastrado` em `erros.py`; função que confere na ordem bloqueio → cadastro →
      resumo, conta o erro na `Sessao`, zera no acerto e bloqueia no quinto erro seguido —
      `RN-01-59`, `RN-04-38`, design 2, 3 e 5. Verificar: testes da 4.1.
- [ ] 1.4 `POST /v1/sessoes/guerreiro/confirmacao`: com a chave do App 01 e persona Mestre ou
      Admin, exige `pin` no corpo e o confere antes de resolver o nick; nas outras origens,
      segue sem PIN — `RF-01-06`, `RN-01-59`, `RN-04-37`, design 4. Verificar: testes da 4.2.
- [ ] 1.5 `POST /v1/aulas/{id}/presencas/sem-rede`: só a chave do App 01 e o Mestre ou Admin
      com PIN cadastrado; resolve o nick pela mesma recusa indistinguível; grava a presença por
      confirmação com o operador como confirmador, sem abrir sessão — `RF-04-23`, `RF-04-25`,
      `RN-01-22`, design 6. Verificar: testes da 4.3.
- [ ] 1.6 Painel do dia: o campo `aguardando_aparelho` vira `sem_equipe` em
      `painel_do_dia/regra.py` e nos testes existentes — `RF-02-43`, design 9. Verificar:
      `uv run pytest tests/test_painel_do_dia.py -x`.

## 2. App 01 — confirmação com PIN

- [ ] 2.1 Sessão de trabalho: ao abrir com rede, busca o verificador e o guarda em
      `sessionStorage` junto do token, apagando os dois ao encerrar ou expirar; sem PIN, abre e
      avisa — `RN-04-38`, PRD-04 §5.1. Verificar: testes da 4.4.
- [ ] 2.2 `TelaDeEntradaDoGuerreiro`: a tela de "Chamar Mestre ou Admin" pede nick e PIN
      mascarado; com rede, envia o PIN na confirmação; frases próprias para PIN errado
      (mantendo o nick), PIN bloqueado (sem nova tentativa) e PIN não cadastrado; limpa o PIN a
      cada tentativa e ao fim do atendimento — `RF-04-21`, `RN-04-37`, `RN-04-36`. Verificar:
      testes da 4.4.
- [ ] 2.3 Sem rede: confere o PIN no aparelho com `SubtleCrypto` contra o verificador; só
      enfileira com o PIN conferido; conta os erros e bloqueia no quinto, com a marca em
      `sessionStorage`; sem verificador, a confirmação sem rede fica indisponível com aviso —
      `RF-04-23`, `RN-04-38`, design 7. Verificar: testes da 4.5.
- [ ] 2.4 `fila/sincronizacao.ts`: sincroniza cada item pela rota `presencas/sem-rede`, sem
      abrir sessão, mantendo o tratamento de falha de rede e de dado — `RF-04-23`, `RF-04-25`.
      Verificar: testes da 4.5.

## 3. Apps 09 e 03 — cadastro do PIN e painel

- [ ] 3.1 App 09, área do perfil: tela de cadastro e troca do PIN (4 dígitos, digitado duas
      vezes, mascarado), dizendo se já há PIN por `tem_pin_de_confirmacao` — `RF-09-121`.
      Verificar: `vitest run` do teste do perfil, com os cenários da spec `area-do-mestre`.
- [ ] 3.2 App 03: a mesma tela para o Admin, com entrada no menu — `RF-02-110`. Verificar:
      `vitest run` do teste novo, com os cenários da spec `aplicacao-de-gestao`.
- [ ] 3.3 App 03, painel do dia: rótulo, seção e estado vazio passam a "Sem equipe", lendo
      `sem_equipe`, e os testes de `painel-do-dia` e `lancamentos` se ajustam — `RF-02-43`.
      Verificar: `vitest run src/painel-do-dia src/lancamentos`.

## 4. Testes

- [ ] 4.1 `backend/tests/test_pin_de_confirmacao.py`: cadastro e troca, formato inválido,
      papel sem permissão, o PIN nunca gravado, verificador só pelo App 01, sem PIN cadastrado,
      o quinto erro bloqueia, o acerto zera, o novo login desbloqueia, o bloqueio não passa
      para outra sessão — spec `pin-de-confirmacao`.
- [ ] 4.2 `backend/tests/` da confirmação do Guerreiro(a): sem PIN no App 01, PIN errado
      recusado antes do nick (nick existente e inexistente), sem PIN cadastrado, App 05 sem
      PIN, e os cenários existentes seguindo verdes — spec `sessao-do-guerreiro`.
- [ ] 4.3 `backend/tests/` da presença sem rede: gravação com o confirmador, reenvio sem
      duplicar, nick que não resolve indistinguível, outra chave recusada, sem PIN cadastrado —
      spec `aula-e-presenca`.
- [ ] 4.4 `apps/app-01-aula-presencial/src/entrada/entrada.test.tsx` e o teste da sessão de
      trabalho: sem PIN não confirma, PIN errado mantém o nick, PIN bloqueado, verificador que
      chega e sai com a sessão, abertura sem PIN com aviso, PIN nunca em armazenamento — spec
      `aplicacao-da-aula-presencial`.
- [ ] 4.5 Testes da fila (`src/fila/`): enfileira só com o PIN conferido, PIN errado sem rede
      não enfileira, o quinto erro bloqueia com ou sem rede, a sincronização usa a rota sem
      sessão — spec `aplicacao-da-aula-presencial`.

## 5. Documentação

- [ ] 5.1 A decisão já foi gravada neste PR: documentos 03 (§§1.1, 3.2, 3.4), 08, 09 e 16;
      PRDs 01, 02, 04 e 09. Ao fechar, a fatia 16 do PRD-04 vira `implementado` em
      `openspec/cronograma-de-fatias.md`, com o slug da change. `docs/prds/index.md`, o
      documento 99 e o `mkdocs.yml` não mudam — nenhuma situação de PRD, relação entre
      documentos ou arquivo novo.
