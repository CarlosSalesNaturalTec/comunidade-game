## Context

A App 03 já está de pé com quinze áreas (`openspec/specs/aplicacao-de-gestao/spec.md`), o menu
por chave de área e a camada visual comum em `comum/react`. A fatia não move contrato de API:
tudo o que ela precisa já está nas telas existentes. O único precedente do aviso é o
`AvisoDeColeta` da App 05 (`RF-05-57`), escrito em linguagem de criança.

## Goals / Non-Goals

**Goals:**

- Um aviso reutilizável, parametrizado pelo dado da tela, presente em toda tela da App 03 que
  grava dado pessoal.
- Uma área de leitura que apresente a tabela do PRD-02 §11 sem nenhuma escrita.
- As duas guardas (`RN-02-23`, `RN-02-24`) asseguradas por teste, não por convenção.

**Non-Goals:**

- Generalizar o aviso para as outras aplicações.
- Qualquer tela de auditoria: `RF-02-63` e `RF-02-70` foram ao Ciclo 02.

## Decisions

1. **O componente do aviso nasce na App 03, não em `comum/react`.** O texto do aviso é do
   público de cada aplicação — o da App 05 fala com criança, o desta fala com a gestão —, e só
   a estrutura se repetiria. Generalizar se decide quando a terceira aplicação precisar.
   _Descartada:_ mover o `AvisoDeColeta` da App 05 para `comum/react` agora, o que arrastaria
   a App 05 para dentro desta fatia.
2. **A lista de telas que recebem o aviso vem da tabela do PRD-02 §11**, uma linha de "Dado
   coletado" para cada tela onde a gestão o grava. Nada de critério próprio: tela que não grava
   dado pessoal não recebe aviso.
   _Descartada:_ pôr o aviso em toda tela da aplicação, o que o tornaria ruído e o faria perder
   a função de dizer o que **aquela** tela coleta.
3. **"Área detalhada de direitos" é uma área da aplicação, não um painel expansível.** O
   `RF-02-64` pede o *acesso à área detalhada*, e o conteúdo é a tabela inteira da §11 — longa
   demais para caber dentro de um formulário. A App 05 usa painel expansível porque ali o
   detalhe é uma frase.
   _Descartada:_ link para fora da aplicação, que no Ciclo 01 não tem destino: a vitrine
   (PRD-03) ainda não existe.
4. **A área Direitos e dados entra no menu como as demais**, por chave de área, e é alcançável
   também por todo aviso — dois caminhos para o mesmo lugar, sem estado compartilhado.
5. **`RN-02-23` e `RN-02-24` são guardas, não telas novas.** Elas se cumprem no que já existe:
   o lançamento já lista o encontro inteiro e a gestão já não tem caminho de autoria. O que a
   fatia acrescenta é a **verificação** que impede a regressão, mais a linha de texto que diz
   ao Admin onde a autoria se faz.
6. **O aviso é texto, com `role` de status e sem cor como único sinal**, no piso de
   acessibilidade WCAG 2.2 AA que a aplicação já cumpre.

## Risks / Trade-offs

- O texto do aviso e o da área repetem, na interface, o que o PRD-02 §11 normatiza. É repetição
  necessária — o Admin não lê o PRD —, mas envelhece: mudança na §11 exige mudar a tela junto.
- A guarda do `RN-02-24` é uma verificação de ausência, e verificação de ausência não pega o
  caminho que ninguém pensou em conferir. Ela cobre as áreas Atividades e Território, onde a
  fronteira de fato se confunde.
- Com `RF-02-63` no Ciclo 02, o `GET /v1/auditoria` fica sem consumidor na gestão durante o
  Ciclo 01. A rota segue testada no backend e o `RF-13-30` a consome pela App 07.
