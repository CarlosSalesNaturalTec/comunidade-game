# Proposal

Origem: **PRD-05** (Área do Guerreiro(a)), **fatia 14** do
`openspec/cronograma-de-fatias.md`.

Identificadores **novos**, a criar na revisão do PRD-05: `RF-05-95`, `RF-05-96` e `RN-05-53`.
Alcança `RF-05-01`, `RF-05-02`, `RF-05-57` (em parte), `RN-05-01`, `RN-05-48` e `RN-05-49`.

## Why

A entrada da App 05 abre a câmera e **não mostra nada**: chama `provarVivacidade()` sem o
callback de estado e nunca acopla o espelho. A criança aperta Entrar e fica até 15 s diante de
"Reconhecendo…", com a câmera acesa e invisível, para receber ao fim "tente de novo, com o
rosto bem posicionado" — sem nunca ter tido como saber qual posicionamento era o certo. É o que
o documento 03 §3.3 chama de capturar às cegas, e é o pior lugar da plataforma para isso: a App
05 é usada em casa, com câmera e luz desconhecidas, sob **limiar emprestado** do ponto de apoio
mais frouxo da comunidade, cuja imprecisão o mesmo §3.3 declara assumida. As duas telas de
câmera da App 01 já mostram o visor; esta é a única que não.

Não é decisão nova: o visor ao vivo já é regra do documento 03 §3.3 e do invariante 12 do
documento 99. É **resíduo declarado** — a fatia `2026-09-18-visor-ao-vivo-e-backend-da-biometria`
do PRD-04 deixou de fora "o espelho do App 05, por ser recorte do PRD-05", e ele nunca veio.

## What Changes

- A entrada da App 05 passa a apresentar o **visor ao vivo** da câmera, acoplado **depois do
  toque em Entrar** — nunca antes, porque o `RN-05-49` proíbe a câmera acender sem que alguém
  tenha pedido algo (`RF-05-95`, `RN-05-53`).
- O retorno do laço passa a ser dito, nas três situações que `EstadoDaVivacidade` já distingue,
  em **linguagem de criança de 6 anos** (`RF-05-95`, PRD-05 §10). O tipo **não ganha valor
  novo**.
- A entrada passa a trazer **frase fixa de orientação** sobre luz e enquadramento, e o **aviso
  discreto** de que a câmera aparece só para a pessoa se ver e que a foto não sai do aparelho
  (`RF-05-96`, `RF-05-57` em parte).
- A falha de **preparo** da câmera ou dos modelos ganha desfecho próprio, separado da recusa da
  conferência. Hoje ela cai no `catch` genérico e sai vestida da frase do rosto, o que o
  `RN-05-48` proíbe ao listar "preparo do aparelho" entre as falhas que aparecem como o que são.
  É **correção de defeito**, e é consequência obrigatória do visor: acoplar o espelho exige
  `prepararCaptura()` antes.
- O `Visor` e as regras `.cg-visor*` **sobem da App 01 ao `comum/react`**, com as frases do laço
  declaradas por quem usa o componente; a App 01 passa a consumi-las, sem mudança de
  comportamento. O `comum/biometria` já fixa `video.className = "cg-visor"`, mas a regra só
  existe no `index.css` da App 01: sem a subida, o espelho na App 05 sairia sem `max-height`,
  sem `object-fit` e sem `scaleX(-1)` — a criança se moveria para a direita e se veria ir para
  a esquerda.
- O PRD-05 §11 ganha a precisão que o PRD-04 já tem no `RN-04-34`: o marcador "nenhuma imagem
  real é exibida" trata da **representação da pessoa**, que é sempre por avatar, e não alcança o
  visor ao vivo. O próprio critério de aceite do §12 já diz "de **outra criança**", e o
  invariante 12 distingue o visor do quadro capturado. É conflito de nível resolvido pelo nível
  superior, não decisão nova.

## Capabilities

### New Capabilities

Nenhuma. A fatia não cria comportamento de sistema novo: aplica à App 05 o visor que a
`aplicacao-da-aula-presencial` já tem e sobe o componente à camada comum.

### Modified Capabilities

- `area-do-guerreiro`: a entrada ganha o visor ao vivo, o retorno abstrato do laço em linguagem
  de criança, a frase de orientação e o aviso discreto; e a falha de preparo passa a ter
  desfecho próprio, distinto da recusa da conferência.
- `camada-visual-comum`: a camada passa a entregar o visor da câmera, com as frases do laço
  declaradas por quem o usa, e a garantia de que só o fluxo ao vivo aparece ali.

## Impact

- `comum/react`: nasce o `Visor`, com as quatro regras de CSS vindas da App 01 e as frases por
  _prop_.
- `comum/biometria`: só o `className` do elemento de vídeo, que deixa de depender do CSS de uma
  aplicação. Nenhuma função muda de assinatura; `acoplarEspelho`, `prepararCaptura` e o
  callback de `provarVivacidade` já existem e são o que faltava ser chamado.
- `apps/app-05-guerreiro/src/entrada/TelaDeEntradaDoGuerreiro.tsx`: o espelho, as frases, a
  orientação, o aviso e a separação do preparo.
- `apps/app-01-aula-presencial`: passa a consumir o `Visor` comum; `src/captura/Visor.tsx` e as
  regras `.cg-visor*` do `index.css` saem de lá.
- **Núcleo: nada.** Nenhuma rota, nenhum contrato e nenhuma migração. A fotografia continua sem
  trafegar, e ao núcleo continua indo apenas o descritor.
- Documentação no mesmo PR: os três identificadores novos e a precisão do §11 no PRD-05, e a
  fatia 14 marcada como implementada no cronograma. O documento 99 não muda — a relação entre
  documentos é a mesma, e o invariante 12 já cobre o visor.

## Fora do escopo

Reproduz o que o PRD já exclui, mais o que a fatia 14 recorta no cronograma:

- **Estado novo de luminosidade ou de distância** derivado da Human — luminância média do
  quadro, tamanho da caixa do rosto. Criaria limiar de luz que ninguém mediu, e o documento 03
  §3.3 é expresso em que limiar não medido não reconhece ninguém. O olho da criança basta,
  desde que ela veja a imagem.
- **A área detalhada de direitos da App 05**, que o `RF-05-57` pede junto do aviso discreto. A
  App 05 não tem essa tela — só a App 01 tem —, e criá-la é fatia própria. Fica como resíduo
  declarado: esta fatia entrega o aviso, não o acesso ao detalhamento.
- Qualquer mudança no caminho da **confirmação assistida** (`RF-05-03`, `RF-05-04`), que não
  abre câmera.
- O **acervo do Guerreiro(a)** e o que mais o PRD-05 §3.2 põe no Ciclo 02.
