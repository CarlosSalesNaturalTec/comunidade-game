# Tasks

## 1. Reproduzir o defeito antes de corrigi-lo

- [x] 1.1 Em `apps/app-01-aula-presencial/src/inicio/inicio.test.tsx`, trocar o marcador de tela
      do caminho das equipes pelo título próprio dele e confirmar que o teste **falha** no
      código atual — é o que prova que o marcador antigo casava com os quatro caminhos e deixou
      o defeito passar (`RF-04-01`, `RF-04-67`, design — decisão 4).

## 2. Título por caminho na entrada do Guerreiro(a)

- [x] 2.1 Em `apps/app-01-aula-presencial/src/entrada/TelaDeEntradaDoGuerreiro.tsx`, declarar o
      mapa `Record<CaminhoDaEntrada, string>` com as quatro redações da tabela da `proposal`,
      junto das demais constantes de mensagem do módulo (design — decisão 1).
- [x] 2.2 Usar o mapa no `Cabecalho` da tela de confirmação por PIN e no da tela de
      reconhecimento, mantendo os subtítulos como estão; verificar que a tarefa 1.1 passa a
      valer (`RF-04-01`, `RF-04-67`, `RF-04-68`, design — decisões 2 e 3).

## 3. Testes

- [x] 3.1 Em `inicio.test.tsx`, cobrir a entrada pelos caminhos das equipes, do quiz e da troca,
      afirmando que cada um se anuncia pelo título próprio e que o caminho da presença conserva
      o dele — o cenário "A entrada anuncia o caminho que serve" do delta (`RF-04-01`,
      `RF-04-67`, `RF-04-68`).
- [x] 3.2 Em `apps/app-01-aula-presencial/src/entrada/entrada.test.tsx`, conferir que as
      asserções que hoje localizam a tela pelo título continuam válidas com o título por
      caminho, ajustando as que se apoiavam no texto fixo (`RF-04-01`).

## 4. Documentação

- [x] 4.1 Acrescentar ao bloco do PRD-04 em `openspec/cronograma-de-fatias.md` a linha `—` desta
      correção, com o slug da change e a situação; nada muda em `docs/`, no documento 09, no
      documento 99, em `docs/prds/index.md` nem na `nav` do `mkdocs.yml`, porque a change não
      toma decisão nova, não altera requisito e não cria arquivo.
