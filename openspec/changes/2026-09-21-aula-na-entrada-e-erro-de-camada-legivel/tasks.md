## 1. A aula volta ao pedido da sessão

- [x] 1.1 `RF-04-18`, `RF-01-73` — acrescentar `aula_id` à entrada de
      `abrirSessaoPorReconhecimento`, em `apps/app-01-aula-presencial/src/api/sessoesDeGuerreiro.ts`,
      e repassar a `aulaId` que `TelaDeEntradaDoGuerreiro` já recebe como propriedade. Verificar
      que o corpo enviado carrega os três campos — nick, descritor e aula — e que nenhuma tela
      pede a aula a quem opera.

## 2. A recusa deixa de absorver falha de camada

- [x] 2.1 `RN-04-36`, `RF-01-27` — em `TelaDeEntradaDoGuerreiro.tsx`, reconhecer a recusa da
      conferência pelo código `autenticacao_biometrica_invalida` do corpo único e reservar a ela
      a frase do domínio (design — decisão 2). Verificar que a frase da recusa sai só nesse
      código.
- [x] 2.2 `RN-04-36`, `RF-01-27` — apresentar a falha de camada pelo que ela é: a `mensagem` do
      corpo único quando ele existe, e a frase própria de falha de comunicação quando não existe
      corpo (design — decisão 3). Preservar intacta a frase de falha de preparo da câmera do
      `RF-04-65`. Verificar que um 422 com campo declarado chega legível à tela.
- [x] 2.3 `RN-04-36`, `RF-04-18` — encerrar o tratamento da conferência na abertura da sessão e
      dar tratamento próprio, com frase própria, ao que roda depois dela: `GET /v1/eu`, o
      registro da presença e a entrada na sessão local (design — decisão 4). Verificar que falha
      nessa sequência não produz a frase da recusa.
- [x] 2.4 `RF-04-64`, `RN-04-34` — conferir que o retorno do laço continua calando em **todos**
      os desfechos novos, e não só nos que já existiam: o visor não pode sobreviver à frase de
      falha de camada nem à de falha posterior ao reconhecimento.

## 3. Testes

- [x] 3.1 `RF-04-18`, `RF-01-73` — em `apps/app-01-aula-presencial/src/entrada/entrada.test.tsx`,
      cobrir o cenário "A entrada declara ao núcleo a aula em curso": o pedido carrega a aula do
      encontro, e quem opera não a digitou.
- [x] 3.2 `RN-04-36`, `RF-01-27` — cobrir "Erro de validação não se disfarça de rosto que não
      confere" e "Falha depois do reconhecimento não se disfarça de recusa", com o 422 de campo
      declarado e com a falha no registro da presença depois de o rosto conferir.
- [x] 3.3 `RF-04-20`, `RN-01-22`, `RN-01-56` — conferir que os cenários já existentes da recusa
      seguem verdes: a frase única, a nova tentativa, o encaminhamento à confirmação e a
      indistinguibilidade entre as causas que o núcleo funde.

## 4. Documentação

- [x] 4.1 Marcar a linha desta change como implementada em `openspec/cronograma-de-fatias.md`.
      Nada muda em `docs/`: os documentos-fonte, o documento 09, os PRDs e o documento 99 já
      receberam, no PR de documentação que criou o `RN-04-36`, tudo o que estas decisões
      mudaram; nenhum arquivo nasce em `docs/`, e a situação do PRD-04 não muda.
