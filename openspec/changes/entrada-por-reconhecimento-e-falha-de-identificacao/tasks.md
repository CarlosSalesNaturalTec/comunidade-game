## 1. Núcleo — o modo reconhecimento ganha quem o produza

- [ ] 1.1 `aulas/rotas.py`: `POST /v1/aulas/{id}/presencas` passa a exigir também
      `exigir_chave_de_aplicacao` e a decidir o modo pela **aplicação declarada na chave** —
      `reconhecimento` aceito só quando ela é `app-01-aula-presencial`, 403 nas demais, no lugar
      da recusa incondicional de hoje. A constante da aplicação segue o precedente de
      `personas/rotas.py` (`RF-04-18`, `RF-09-45`, design — decisão 1). Verificação: 201 com modo
      reconhecimento pela chave da App 01 e 403 pela chave da App 09.
- [ ] 1.2 `aulas/rotas.py`: no modo reconhecimento a rota **não preenche o confirmador**, e
      `ConfirmarPresencaEntrada` deixa de tratá-lo como obrigatório para esse modo.
      `registrar_presenca` não muda (`RF-04-18`, `RF-01-20`, design — decisão 2). Verificação: a
      presença gravada por reconhecimento volta com `confirmador_id` nulo, e a por confirmação
      volta com o adulto da sessão.
- [ ] 1.3 Conferir que a resposta da rota devolve o `momento_do_fato` **gravado**, não o
      enviado, quando a presença já existia — é o sinal de que o cliente depende (`RF-04-19`,
      design — decisão 3). Verificação: reenvio com momento diferente devolve o momento original,
      sem segundo registro.

## 2. App 01 — a entrada por nick e imagem

- [ ] 2.1 `api/sessoesDeGuerreiro.ts`: cliente de `POST /v1/sessoes/guerreiro`, com nick e
      descritor, ao lado do de confirmação que já existe (`RF-04-18`, `RF-04-29`). Verificação:
      teste do cliente pelo componente que o chama, precedente de `api/guerreiros.ts`.
- [ ] 2.2 `api/presencas.ts` (novo): cliente de `POST /v1/aulas/{id}/presencas` nos dois modos,
      sempre com o **token da sessão de trabalho** (`RF-04-18`, `RF-04-21`, design — decisão 2).
      Verificação: teste mostra que o token do Guerreiro(a) nunca é o usado nesta chamada.
- [ ] 2.3 `TelaDeEntradaDoGuerreiro.tsx`: nick, depois vivacidade e descritor pelo módulo de
      biometria já existente, depois a sessão, depois a presença por reconhecimento — a ordem do
      design — decisão 5. Sem câmera, cai direto na confirmação humana, sem tentativa de captura
      (`RF-04-18`, `RF-04-29`, `RN-04-03`, `RN-04-12`). Verificação: nenhuma requisição do teste
      carrega fotografia; sem câmera a captura não é oferecida.
- [ ] 2.4 A mesma tela avisa a **presença já registrada** comparando o momento do fato devolvido
      com o enviado, e volta à tela inicial (`RF-04-19`, PRD-04 §5.4). Verificação: o segundo
      reconhecimento do mesmo Guerreiro(a) mostra o aviso e não emite segunda escrita.

## 3. App 01 — a falha e o recadastro

- [ ] 3.1 A recusa do núcleo vira **nova tentativa** com uma frase única, igual para nick
      inexistente, ausência de _template_ e descritor que não confere; persistindo, a tela
      oferece a confirmação de Mestre ou Admin (`RF-04-20`, `RN-01-22`, `RN-04-09`). Verificação:
      as telas de recusa das três causas são indistinguíveis no teste.
- [ ] 3.2 A confirmação humana passa a **registrar a presença** no modo confirmação, com o adulto
      da sessão de trabalho como confirmador, além de abrir a sessão (`RF-04-21`). Verificação: a
      presença gravada aponta quem confirmou.
- [ ] 3.3 Tela de recadastro da imagem de referência, atrás da sessão do Guerreiro(a) aberta por
      confirmação presencial, tomando o identificador do `GET /v1/quem-sou` daquela sessão e
      enviando só o descritor (`RF-04-22`, `RN-01-22`, design — decisão 4). Verificação: nenhuma
      rota de nick para identificador é chamada; o teste cobre a substituição concluída.

## 4. Testes

- [ ] 4.1 `tests/` do núcleo, presença: os cenários da spec de `aula-e-presenca` — reconhecimento
      pela App 01 sem confirmador, 403 do modo reconhecimento por outra chave, confirmação com
      confirmador, reenvio que devolve o registro e o momento originais, e a recusa de presença
      em comunidade alheia continuando válida (`RF-04-18`, `RF-04-19`, `RF-04-21`).
- [ ] 4.2 `tests/` do núcleo, matriz: nenhuma operação de escrita de presença é concedida ao
      Guerreiro(a), e a tentativa dele pela rota é recusada (`RF-04-18`, design — decisão 1).
- [ ] 4.3 `entrada.test.tsx` da App 01: os cenários da spec de `aplicacao-da-aula-presencial` —
      entrada por nick e imagem com presença no mesmo ato, presença já constante, três recusas
      indistinguíveis, queda para a confirmação humana com presença, aparelho sem câmera e
      ausência de fotografia em qualquer requisição (`RF-04-18` a `RF-04-22`, `RF-04-29`).
- [ ] 4.4 Teste de recadastro da imagem na App 01, cobrindo que o identificador vem da sessão e
      não de consulta por nick (`RF-04-22`, `RN-01-22`).

## 5. Documentação

- [ ] 5.1 No mesmo PR: PRD-04 §9 corrigido no código da presença duplicada — idempotente e sem
      erro, no lugar do 409 — e §13 com as duas decisões do fundador de 2026-08-24 (quem escreve
      a presença por reconhecimento; a duplicata que o núcleo devolve e a aplicação avisa); as
      linhas correspondentes no documento 09; `docs/prds/index.md` com a quarta fatia do PRD-04.
      Nenhum arquivo novo em `docs/`, logo a `nav` do `mkdocs.yml` não muda; a relação entre
      documentos não muda, logo o documento 99 não muda.
