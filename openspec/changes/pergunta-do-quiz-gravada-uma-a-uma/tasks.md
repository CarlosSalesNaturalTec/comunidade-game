## 1. Regra da pergunta no núcleo

- [ ] 1.1 Extrair de `_conferir_perguntas_do_quiz` a conferência de **uma** pergunta e fazer os
      dois chamadores usarem a mesma — a declaração do todo e a escrita isolada —, de modo que
      a exigência de enunciado, quatro alternativas e correta não divirja entre eles
      (`RN-09-44`, `RN-09-43`). Verificar pelos testes já verdes da declaração.
- [ ] 1.2 Escrever em `trilhas/regra.py` `acrescentar_pergunta_do_desbloqueio`, com posse do
      Mestre autor, conferência de completude e inserção em `max(ordem) + 1` das vigentes
      (`RF-09-120`, `RN-09-44`, design — decisões 3 e 4).
- [ ] 1.3 Escrever `corrigir_pergunta_do_desbloqueio`: sem resposta gravada, atualiza a linha no
      lugar conservando id, `ordem` e imagem; havendo `RespostaDaSubmissao` apontando a
      pergunta, carimba `substituida_em` e insere a nova na mesma `ordem`, copiando as três
      colunas da imagem (`RF-09-120`, `RN-05-47`, design — decisão 2).
- [ ] 1.4 Escrever `remover_pergunta_do_desbloqueio`, que carimba a pergunta sem renumerar as
      demais e recusa com 422 a remoção da **única** pergunta do quiz (`RF-09-120`, `RN-09-43`,
      design — decisões 3 e 5).

## 2. Rotas

- [ ] 2.1 Publicar em `trilhas/rotas.py` as três rotas — `POST
      /v1/missoes/{id}/perguntas-do-desbloqueio`, `PUT /v1/perguntas-do-desbloqueio/{id}` e
      `DELETE /v1/perguntas-do-desbloqueio/{id}` —, cada uma devolvendo a pergunta como ficou,
      id inclusive, no schema ao autor que a declaração já usa (`RF-09-120`, design —
      decisão 1). A declaração do desafio inteiro não muda.
- [ ] 2.2 Conferir que a rota de abertura do envio da imagem aceita pergunta criada
      isoladamente, sem exigir declaração prévia do desafio (`RF-09-119`, `RF-09-120`).

## 3. Tela da App 09

- [ ] 3.1 Acrescentar em `trilhas/api.ts` as três funções cliente das rotas novas, com os tipos
      de entrada e saída da pergunta (`RF-09-120`).
- [ ] 3.2 Dar a cada pergunta de `DesafioDeDesbloqueio.tsx` gravação, marca de gravação e erro
      próprios, e fazer a recusa do núcleo chegar com o motivo na pergunta recusada, sem apagar
      o que está escrito nas outras (`RF-09-120`, `RN-09-44`).
- [ ] 3.3 Fazer o anexo da imagem em pergunta ainda não gravada ser um gesto só: grava a
      pergunta, emenda o envio com o id que voltou e, incompleta, mostra o que falta sem abrir
      envio (`RF-09-120`, `RN-09-44`, `RF-09-119`, design — decisão 6).
- [ ] 3.4 Conferir que o bloco da **sondagem** herda os três comportamentos acima sem texto
      próprio novo, já que é o mesmo componente (`RF-09-81`, `RF-09-120`).

## 4. Testes

- [ ] 4.1 Em `backend/tests/test_desbloqueio_da_missao.py`, cobrir os cenários da escrita por
      pergunta: acrescentar ao fim sem tocar nas demais, corrigir sem tocar nas demais,
      incompleta recusada com 422, sem correta recusada com 422, não autor recusado com 403,
      corrigir pergunta já respondida sem apagar a tentativa, corrigir conservando a imagem,
      remover uma, remover a única recusada com 422, pergunta nova aceitando imagem e a
      sondagem tratada como qualquer quiz (`RF-09-120`, `RN-09-44`, `RN-05-47`, `RN-09-43`).
- [ ] 4.2 No mesmo arquivo, cobrir a convivência dos dois caminhos: declarar o desafio inteiro
      sobre um quiz que vinha sendo gravado pergunta a pergunta, e a recusa por campo fora do
      contrato quando o corpo da declaração devolve o identificador da pergunta (`RF-09-118`,
      `RF-09-120`).
- [ ] 4.3 Em `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`, cobrir os cenários de tela:
      gravar uma pergunta sem gravar as outras, a recusa de uma não derrubar as demais, anexar
      imagem a pergunta nova gravando-a sozinha, anexar a pergunta incompleta dizendo o que
      falta, e a sondagem gravando pergunta a pergunta (`RF-09-120`, `RN-09-44`, `RF-09-81`).

## 5. Documentação

- [ ] 5.1 Gravar a decisão nova no documento-fonte — `docs/03-plataforma-e-arquitetura.md` §11,
      onde já moram as regras de autoria e da imagem da pergunta — e a linha correspondente em
      `docs/09-topicos-em-aberto-e-sugestoes.md` §1, "Já decididos": a pergunta se grava
      isoladamente, completa, e a declaração do desafio inteiro continua ao lado (decisão do
      fundador, 2026-09-12).
- [ ] 5.2 Aplicar a decisão em `docs/prds/prd-09-area-do-mestre.md`: `RF-09-120` e `RN-09-44`
      nas tabelas de requisitos e regras, as três rotas na §9 e as origens na rastreabilidade
      §15. `docs/prds/index.md` só muda se a situação do PRD-09 mudar; o doc 99 só muda se a
      relação entre documentos mudar.
- [ ] 5.3 Marcar a fatia 20 como `implementado` em `openspec/cronograma-de-fatias.md`, com o
      slug desta change no Recorte. Nenhum arquivo novo em `docs/`, logo a `nav` do
      `mkdocs.yml` não muda.
