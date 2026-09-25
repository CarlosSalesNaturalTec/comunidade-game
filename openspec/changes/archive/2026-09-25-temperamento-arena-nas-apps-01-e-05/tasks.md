# Tasks

## 1. A camada de tema da Arena

- [x] 1.1 Em `comum/tokens.css`, declarar `[data-temperamento="arena"]` com raio de carta de `12`
      px e duração de `300` ms, ao lado da camada da Operação, sem declarar densidade e com o
      motivo em comentário (design — decisões 1 e 2).
- [x] 1.2 Em `comum/tokens.test.ts`, cobrir os cenários "A Arena tem camada de tema própria", "As
      aplicações da Operação seguem como estão" e "Menos movimento vence o temperamento" do delta
      de `camada-visual-comum`.

## 2. As duas aplicações da Arena declaram o temperamento

- [x] 2.1 Em `apps/app-01-aula-presencial/index.html` e `apps/app-05-guerreiro/index.html`, trocar
      a declaração para o temperamento Arena (design — decisão 6, invariante 24).
- [x] 2.2 Conferir que as quatro aplicações da Operação seguem declarando Operação, e que nenhuma
      folha das Apps 01 e 05 lê o token de densidade — a medição da `proposal` diz que só a App 03
      o lê, e a tarefa confirma que segue verdade no momento da implementação.

## 3. O sistema de ícone da camada comum

- [x] 3.1 Em `comum/react`, criar o componente de ícone do documento 15 §11.1 — grade de `24` px,
      traço de `2` px com ponta e junta arredondadas, sem preenchimento, `currentColor`, tamanho
      escolhido entre os quatro da §11.1 e rótulo sempre por quem o usa (design — decisões 3 e 4).
- [x] 3.2 Desenhar os seis glifos da tabela da `proposal` — onboarding, presença, equipes, quiz,
      medição do limiar e troca —, cada um sem cor declarada no arquivo.
- [x] 3.3 Exportar o componente e os glifos em `comum/react/indice.ts`, acrescentando o que
      precisar em `comum/package.json`.
- [x] 3.4 Cobrir, em teste do `comum`, os três cenários do requisito do ícone: nenhum ícone vem de
      fora, o ícone acompanha o tema e o ícone não aparece sozinho.

## 4. Os caminhos da tela inicial da App 01

- [x] 4.1 Em `apps/app-01-aula-presencial/src/inicio/TelaInicial.tsx`, apresentar o glifo de cada
      caminho ao lado do rótulo que já existe, sem alterar rótulo, ordem nem condição de exibição
      de nenhum deles (`RF-04-01`, design — decisão 4).
- [x] 4.2 Em `apps/app-01-aula-presencial/src/index.css`, acomodar o glifo no `.cg-caminho` sem
      mexer no raio nem no alvo de toque de `48` px (design — decisão 5).
- [x] 4.3 Em `apps/app-01-aula-presencial/src/inicio/inicio.test.tsx`, cobrir o cenário "Cada
      caminho leva glifo ao lado do rótulo", afirmando que os seis rótulos seguem alcançáveis por
      texto — os testes localizam os caminhos pelo rótulo, e o glifo não pode roubar essa
      localização (`RF-04-01`).

## 5. Documentação

- [x] 5.1 Marcar a linha desta fatia como implementada em `openspec/cronograma-de-fatias.md`.
- [x] 5.2 Registrar no documento 09 §1 a pendência do **valor de densidade do temperamento Arena**,
      que o documento 15 §6 descreve sem número (design — decisão 2). Já registrada na elicitação
      desta fatia, com o texto que a decisão 2 fixou: a tarefa conferiu, e nada havia a reescrever. Nada muda em
      `docs/prds/index.md`, no documento 99 nem na `nav` do `mkdocs.yml`: nenhum arquivo nasce e
      nenhuma relação entre documentos muda. O documento 15 **não** muda — a change o cumpre, não
      o altera.
