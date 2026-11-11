# Proposal

**PRD de origem:** PRD-04 (App 01), alcançando PRD-05 (App 05) e PRD-09 (App 09). **Fatia:** 33
do bloco PRD-04 em `openspec/cronograma-de-fatias.md`. **Identificadores:** `RF-04-35`,
`RF-04-72`, `RF-04-73`, `RF-05-11`, `RF-05-13`, `RF-09-25`, `RF-09-119`, `RF-09-132` — **sem
identificador novo**, como nas fatias 25 a 28: a ampliação é apresentação da mídia que esses
requisitos já exibem, e nenhum enunciado de PRD muda.

## Why

A moldura fixa de 320 × 240 px (decisão do fundador de 2026-09-17) deixa ilegível o detalhe de
imagem de conteúdo — mapa, esquema, texto fotografado —, e no aparelho da equipe da App 01 a
imagem é lida por várias crianças ao mesmo tempo. O fundador decidiu em **2026-11-11** reverter
a parte "sem ampliação" daquela decisão: **tocar na imagem a abre em tela cheia**, nas Apps 01,
05 e 09. Na tela da programação da App 01, ainda por cima, a imagem e o vídeo nem abrem: a tela
põe em `<img src>` a referência do armazenamento, sem a chave que toda rota sob `/v1` exige.

## What Changes

- **Imagem amplia ao toque.** Toda imagem exibida na moldura fixa das Apps 01, 05 e 09 passa a
  ser um controle: tocar, clicar ou acionar pelo teclado abre a imagem **inteira, sem corte, no
  maior tamanho que a tela comporta**, sobre a tela atual. Fecha pelo botão **"Fechar"**, pela
  tecla `Esc` ou pelo toque fora da imagem, e o foco volta à imagem que abriu.
- **A moldura não muda.** Tamanho fixo, `contain`, mesmo tamanho para imagem e vídeo, aviso de
  carregando e de falha: tudo segue. Muda só o NEVER da ampliação, nos specs `area-do-guerreiro`
  e `area-do-mestre`.
- **Só imagem.** Vídeo e áudio ficam na moldura, com os controles nativos — o vídeo já tem tela
  cheia própria.
- **Sem pinça e sem arrastar** dentro da imagem ampliada (decisão do fundador de 2026-11-11).
- **App 01, programação do encontro:** imagem e vídeo do conteúdo da missão passam a ser
  buscados em bytes do núcleo e exibidos na mesma moldura fixa das demais telas — pré-requisito
  para haver o que ampliar —, com a imagem ampliável. Conserto de defeito preexistente.
- **Onde alcança:** App 01 — programação do encontro e percurso do Guerreiro(a) (missão e
  desafio de desbloqueio); App 05 — conteúdo da missão e imagem da pergunta do desbloqueio;
  App 09 — pré-visualização da missão, conteúdo exibido no cadastro, imagem da pergunta na
  edição do desafio e comprovação em foto na fila de desbloqueios pendentes.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: a mídia do conteúdo da missão passa a ter a moldura fixa e a
  imagem passa a ampliar em tela cheia, no caminho das equipes e no do Guerreiro(a).
- `area-do-guerreiro`: a moldura de mídia deixa de proibir a ampliação; a imagem amplia em tela
  cheia.
- `area-do-mestre`: idem, para as quatro telas da App 09 que exibem imagem do núcleo.

## Impact

- **Código:** `comum/react/MidiaDoNucleo.tsx` e `comum/react/Dialogo.tsx` (ampliação opcional,
  pedida por quem monta), `comum/react/estilos.css`; `comum/trilha/Missao.tsx` e
  `comum/trilha/DesafioDeDesbloqueio.tsx` (Apps 01 e 05); quatro telas da App 09;
  `apps/app-01-aula-presencial/src/trilhas/TelaDaProgramacao.tsx`.
- **App 06 (vitrine):** não muda — usa o mesmo componente, mas não pede a ampliação, e a
  decisão não a alcança.
- **Backend e API:** nenhuma mudança; a imagem ampliada reaproveita os bytes já buscados.
- **Documentação:** documento 15 §12 (a moldura amplia a imagem) e a decisão registrada em
  "Já decididos" do documento 09 §1. Os PRDs 04, 05 e 09 não mudam: nenhum deles enuncia a
  moldura, que vive no documento 15 e nos specs.
