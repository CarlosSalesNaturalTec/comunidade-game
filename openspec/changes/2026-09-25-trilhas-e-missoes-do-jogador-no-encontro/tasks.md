# Tasks

## 0. Antes de começar

- [ ] 0.1 Confirmar com o fundador a **trava da `proposal`**: o percurso no encontro é de leitura
      apenas, sem responder à sondagem nem ao desafio de desbloqueio. Sem essa resposta as tarefas 3
      e 4 não começam, porque o recorte muda.
- [ ] 0.2 Conferir que os PRs de revisão do **documento 03 §3** e do **PRD-04** entraram, com o
      `RF-04-72` criado e `RF-04-01`, `RF-04-67` e `RN-04-40` alterados — a change **não** cria
      identificador nem altera documento normativo.
- [ ] 0.3 Conferir que a change do **temperamento Arena** entrou antes: o delta da tela inicial aqui
      já traz o parágrafo do glifo (design — decisão 7).

## 1. Promover os componentes de trilha para `comum/`

- [ ] 1.1 Criar `comum/trilha/` com `GuiaDaTrilha`, `Missao`, `Sondagem` e `DesafioDeDesbloqueio`,
      vindos de `apps/app-05-guerreiro/src/trilha/`, e a fatia do cliente de API que eles usam —
      `listarMinhasTrilhas`, `obterMissaoNoPercurso`, `obterTrilhaPublica`, `lerArquivoDoConteudo` e
      `lerImagemDaPergunta` (`RF-05-08`, `RF-05-10`, `RF-05-17`, design — decisões 1 e 2).
- [ ] 1.2 Tornar **opcional** o que escreve — a entrega da produção e a submissão do desbloqueio —,
      de modo que quem monta o componente decida se oferece (design — decisão 3).
- [ ] 1.3 Exportar a pasta em `comum/package.json` e conferir o `comum/tsconfig.json`.
- [ ] 1.4 Em `apps/app-05-guerreiro/src/trilha/` e `src/api/trilha.ts`, passar a consumir o que foi
      promovido, **ligando** a escrita, sem mudar comportamento algum da App 05 (`RF-05-13`,
      `RF-05-14`, `RF-05-74`).
- [ ] 1.5 Rodar os testes de trilha da App 05 e confirmar que passam sem alteração de asserção — é o
      que prova que a promoção não mudou o que a App 05 faz (design — Risks).

## 2. O caminho das trilhas na App 01

- [ ] 2.1 Em `apps/app-01-aula-presencial/src/api/`, acrescentar as leituras que faltam nesta
      aplicação: as trilhas do Guerreiro(a) e as equipes dele com as atividades de cada uma, por
      `GET /v1/eu/equipes` (`RF-04-72`, `RF-04-35`, design — decisão 4).
- [ ] 2.2 Em `entrada/TelaDeEntradaDoGuerreiro.tsx`, acrescentar `trilhas` ao tipo do caminho e ao
      mapa de títulos, e oferecer no desfecho da presença o acesso às trilhas ao lado de voltar ao
      início, sem reabrir sessão (`RF-04-67`, `RF-04-72`, design — decisão 5).
- [ ] 2.3 Em `inicio/TelaInicial.tsx`, acrescentar o caminho das trilhas, atrás da entrada do
      Guerreiro(a) e da `GuardaDePresenca`, como os das equipes, do quiz e da troca (`RF-04-72`,
      `RF-04-01`, `RN-04-40`).

## 3. A tela do percurso no encontro

- [ ] 3.1 Em `apps/app-01-aula-presencial/src/trilhas/`, montar a tela do percurso sobre os
      componentes promovidos: uma trilha abre direto, mais de uma apresenta a lista, nenhuma diz que
      inscrever-se acontece na App 05 (`RF-04-72`, design — decisão 6).
- [ ] 3.2 Apresentar, junto do percurso, as atividades das equipes do Guerreiro(a) na aula em curso,
      com enunciado próprio para "não integra equipe no encontro", distinto do de encontro sem
      programação declarada (`RF-04-72`, `RF-04-35`).
- [ ] 3.3 Não ligar a escrita nos componentes promovidos, e conferir que a tela não oferece
      sondagem, desbloqueio nem entrega individual (design — decisão 3).
- [ ] 3.4 Tratar a ausência de rede como os demais caminhos que pedem o Guerreiro(a), sem
      enfileirar nada (`RF-04-58`, `RF-04-68`).

## 4. Testes

- [ ] 4.1 Em teste do `comum`, cobrir os componentes promovidos com a escrita ligada e desligada —
      é o contrato novo da decisão 3.
- [ ] 4.2 Em `apps/app-01-aula-presencial/src/trilhas/trilhas.test.tsx`, cobrir os nove cenários do
      requisito novo: uma trilha, mais de uma, nenhuma, sondagem como missão atual, seguinte
      trancada com motivo, atividades pela equipe, sem equipe na aula, tela sem escrita e sem rede
      (`RF-04-72`, `RF-04-35`).
- [ ] 4.3 Em `entrada/entrada.test.tsx`, cobrir "O desfecho da presença oferece as trilhas" e o
      título próprio do caminho das trilhas nas duas formas da entrada (`RF-04-67`, `RF-04-72`).
- [ ] 4.4 Em `inicio/inicio.test.tsx`, cobrir "A tela inicial leva às trilhas de quem já tem
      presença", "Sem presença, o caminho das trilhas não abre" e "O caminho da presença continua
      não levando às equipes" (`RF-04-72`, `RF-04-01`, `RN-04-40`).

## 5. Documentação

- [ ] 5.1 Marcar a fatia 21 como implementada em `openspec/cronograma-de-fatias.md`.
- [ ] 5.2 Acrescentar ao **documento 03 §1.2** a linha que descreve `comum/trilha/`, porque a
      estrutura de pastas é definida ali (design — decisão 1).
- [ ] 5.3 Conferir que a decisão nova do fundador está gravada no documento 09 §1 e no documento 03
      §3, e que o PRD-04 traz o `RF-04-72` — tudo pelos PRs de revisão, não por esta change. Nada
      muda em `docs/prds/index.md` nem na `nav` do `mkdocs.yml`: a situação do PRD-04 não muda e
      nenhum arquivo nasce em `docs/`. O documento 99 §8 recebe ajuste **se** a relação entre o
      PRD-04 e o PRD-05 mudar de forma — conferir ao fechar.
