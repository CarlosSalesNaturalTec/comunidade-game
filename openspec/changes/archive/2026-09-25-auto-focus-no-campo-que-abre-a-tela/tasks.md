# Tasks

## 1. Foco inicial no campo comum

- [x] 1.1 Em `comum/react/Campo.tsx`, acrescentar a propriedade opcional de foco inicial e
      repassá-la ao `<input>`, sem alterar rótulo, erro, identificador nem estado de inválido
      (design — decisões 1, 2 e 3).

## 2. As telas da App 01 declaram o campo inicial

- [x] 2.1 Em `onboarding/TelaDeCadastro.tsx`, declarar o **nome** como campo inicial, deixando
      nick e data de nascimento sem declaração (`RF-04-07`, design — decisão 4).
- [x] 2.2 Em `onboarding/TelaDoResponsavel.tsx`, declarar o **nome do responsável** (`RF-04-60`).
- [x] 2.3 Em `entrada/TelaDeEntradaDoGuerreiro.tsx`, declarar o **nick** nas duas formas da
      entrada — a por nick e imagem e a por confirmação —, deixando o **PIN** sem declaração
      (`RF-04-18`, `RF-04-21`, `RF-04-29`, design — decisão 4).
- [x] 2.4 Em `equipes/TelaDeEquipes.tsx`, declarar o **nome da equipe**, deixando o papel sem
      declaração (`RF-04-30`, `RF-04-69`).
- [x] 2.5 Em `equipes/TrocaDoNome.tsx`, declarar o **nome novo** (`RF-04-70`).
- [x] 2.6 Em `trilhas/EquipeDaTrilha.tsx`, declarar o **nome da equipe** da formação, deixando
      o papel sem declaração (`RF-04-61`).

## 3. Testes

- [x] 3.1 Em `comum/react/Campo.test.tsx`, cobrir os quatro cenários do delta de
      `camada-visual-comum`: campo declarado abre focado, campo sem declaração não toma o foco, o
      contorno de foco continua valendo e o anúncio do campo com erro não muda. Afirmar o foco
      pelo elemento ativo do documento, não pelo atributo (design — Risks).
- [x] 3.2 Em `entrada/entrada.test.tsx`, cobrir "A entrada do Guerreiro(a) abre com o nick
      focado" nos quatro caminhos e "A confirmação por PIN também começa no nick", afirmando que
      o campo do PIN não está focado (`RF-04-18`, `RF-04-21`, `RF-04-29`).
- [x] 3.3 Em `onboarding/onboarding.test.tsx` e `onboarding/responsavel.test.tsx`, cobrir "O
      cadastro do onboarding abre com o nome focado", com os campos seguintes sem foco, e o nome
      do responsável mínimo (`RF-04-07`, `RF-04-60`).
- [x] 3.4 Em `equipes/equipes.test.tsx` e `trilhas/trilhas.test.tsx`, cobrir "A formação da equipe
      abre com o nome da equipe focado", com o papel sem foco, a troca do nome e a formação da
      equipe da trilha (`RF-04-30`, `RF-04-61`, `RF-04-69`, `RF-04-70`).
- [x] 3.5 Conferir, nos testes das telas alteradas, que nenhuma asserção de validação, recusa ou
      desfecho mudou — o cenário "O foco inicial não muda o que a tela faz" do delta.

## 4. Documentação

- [x] 4.1 Marcar a fatia 19 como implementada em `openspec/cronograma-de-fatias.md`. Nada muda em
      `docs/`, no documento 09, no documento 99, em `docs/prds/index.md` nem na `nav` do
      `mkdocs.yml`: a change não toma decisão de produto nova, não altera requisito e não cria
      arquivo em `docs/`.
