# Tasks

> O núcleo vem antes das telas: sem a rota de leitura e sem o `id` no `ArtefatoSaida`, nenhuma
> das duas telas tem o que consumir.

## 1. O contrato no PRD-02

- [x] 1.1 Acrescentar à §9 do PRD-02 a linha de `GET /v1/conteudo-institucional`, restrita a
      Admin, e registrar na §13 as duas decisões do fundador de 2026-10-02 — a rota de leitura
      separada e o alargamento do `ArtefatoSaida` —, com as linhas correspondentes na
      rastreabilidade da §15 (`RF-02-80`, `RF-02-101`)

## 2. O núcleo

- [x] 2.1 Expor `GET /v1/conteudo-institucional` em
      `backend/src/nucleo/conteudo_institucional/rotas.py`, restrita a Admin pela mesma operação
      do `PUT`, devolvendo as três seções em ordem fixa com texto, link de vídeo, autor e data,
      reusando `SecaoPublicadaSaida`; seção nunca publicada sai sem texto, autor nem data
      (`RF-02-80`)
- [x] 2.2 Acrescentar `id` e `publicado` ao `ArtefatoSaida` de
      `backend/src/nucleo/personas/rotas.py`, com `publicado` derivado de
      `artefato_esta_publicado()` — sem campo novo no banco e sem migração (`RF-02-101`)

## 3. Testes do núcleo

- [x] 3.1 Em `backend/tests/test_conteudo_institucional_rota.py`, cobrir os cenários do delta de
      `conteudo-institucional`: Admin lê as três seções com autoria; seção nunca publicada vem
      vazia; outra persona recebe 403; e a rota pública continua sem devolver autor nem data
      (`RF-02-80`, `RF-03-45`)
- [x] 3.2 Cobrir, no teste de personas que já existe, os cenários do delta de `prova-do-apoio`: a
      listagem distingue pendente de publicado e traz o identificador; o identificador serve à
      anexação; e a leitura do próprio Apoiador segue trazendo só o dele (`RF-02-101`,
      `RF-14-20`)

## 4. A tela do conteúdo institucional

- [x] 4.1 Criar na App 03 a área do conteúdo institucional — a leitura de Admin no cliente de
      API e a tela das três seções em ordem fixa, com texto, autoria e o link de vídeo oferecido
      só em "Quem somos"; publicar substitui a versão vigente, uma seção por vez, e seção vazia
      é editável (`RF-02-80`, `RF-03-49`)
- [x] 4.2 Ligar a área à navegação da gestão e apresentar a recusa de quem não é Admin em
      linguagem legível, no molde que a aplicação já usa (`RF-02-80`)

## 5. A fila do comprobatório

- [x] 5.1 Acrescentar a `apps/app-03-gestao/src/filas/` a fila dos comprobatórios que esperam
      anexação, derivada de `GET /v1/apoiadores` filtrando por não publicado e percorrendo as
      páginas do cursor, normalizada como as filas que já existem e identificando o Apoiador, o
      rótulo e o endereço (`RF-02-101`)
- [x] 5.2 Implementar a anexação pela própria fila: anexado, o documento sai da fila; a recusa
      sai legível; a fila NUNCA oferece edição de endereço ou rótulo, e a fila vazia se explica
      como informação (`RF-02-101`, `RF-14-19`)

## 6. Testes da App 03

- [x] 6.1 Cobrir os cenários do delta de `aplicacao-de-gestao` sobre o institucional: as três
      seções aparecem com a autoria; publicar substitui a versão vigente; o campo de vídeo só
      existe em "Quem somos"; e seção nunca publicada aparece vazia e editável (`RF-02-80`,
      `RF-03-49`)
- [x] 6.2 Em `filas.test.tsx`, cobrir os cenários da fila: ela mostra o que espera; anexar
      publica e esvazia a linha; documento já publicado não aparece; e a fila vazia se explica
      (`RF-02-101`)

## 7. Documentação

- [x] 7.1 Marcar a fatia 16 do PRD-02 como `implementado` em
      `openspec/cronograma-de-fatias.md`, com o slug da change; mover para "Já decididos" do
      documento 09 §1 as duas decisões do fundador de 2026-10-02. A situação do PRD-02 em
      `docs/prds/index.md` passa a `implementado`, se esta for a última fatia aberta dele — a
      coluna da tabela, nunca parágrafo novo. Nenhuma relação entre documentos muda, nenhum
      arquivo nasce em `docs/` e a `nav` do `mkdocs.yml` fica como está
