# Tasks

## 1. Os helpers de primitivas e a estrutura declarativa

- [x] 1.1 Em `comum/avatar/Avatar.tsx`, acrescentar os helpers de primitiva — `bolhas`, `mecha`,
      `contas`, `onda` e `traco` —, com as formas simples (`elipse`, `circulo`, `caminho`)
      aplicadas direto. `bolhas` distribui círculos num arco de elipse; `onda` monta a mecha a
      partir da linha de centro oscilante; `traco` sai em `rgba(0,0,0,0.22)`, sem cor nova.
      Verificação: os helpers compilam e `vitest run comum/avatar` segue verde com as formas
      antigas ainda em uso. (`RF-04-07`)
- [x] 1.2 Trocar os três dicionários de literais (`MASSAS_DE_CABELO`, `COMPRIMENTOS_DE_CABELO` e
      o novo de frente) por **uma** estrutura por textura, com as listas `massa`, `comprimento` e
      `frente`, e a função que as desenha. Verificação: as dez texturas continuam resolvendo, e
      textura desconhecida continua caindo no padrão da camada. (`RF-04-06`, `RF-04-07`)

## 2. As nove camadas, com as correções de geometria

- [x] 2.1 Mover as **orelhas** do grupo `tom` para o grupo `rosto`, antes da silhueta, no mesmo
      tom de pele. Verificação: o cenário "O avatar se compõe pelas nove camadas do catálogo"
      segue verde, e o teste novo de orelha visível sob black power passa. (`RF-04-07`)
- [x] 2.2 Desenhar a **peça da frente** dentro do grupo `rosto`, depois da silhueta, em `<g>`
      próprio com `fill` da cor do cabelo. Verificação: o SVG continua com nove `g[data-camada]`
      filhos diretos, na ordem do documento 15 §7.1. (`RF-04-07`)
- [x] 2.3 Acrescentar o **realce de contorno** à silhueta do rosto, em `rgba(255,255,255,0.22)`.
      Verificação: o `outerHTML` segue sem casar `/https?:|url\(/`. (`RF-04-07`)
- [x] 2.4 Acrescentar o **contorno** ao grupo `roupa`, em `var(--cor-superficie)`, sem alterar os
      fios de detalhe que cada peça já traz. Verificação: as cinco peças desenham, e o contorno
      aparece nas quatro combinações de cor coincidente. (`RF-04-07`)

## 3. As dez texturas de cabelo

- [x] 3.1 Redesenhar as quatro texturas **crespas** — `black-power`, `crespo-curto`, `trancas` e
      `dreads` — com silhueta própria fora do rosto, comprimento acima da linha do torso ou fora
      da largura dele, e peça da frente. Verificação: as quatro diferem entre si e do rosto nu no
      desenho resultante. (`RF-04-06`)
- [x] 3.2 Redesenhar `cacheado`, `ondulado` e `liso` com a mesma regra, e **`raspado`** com massa
      que ultrapassa a silhueta do rosto mais a linha do cabelo na frente. Verificação: trocar a
      cor do cabelo muda o desenho **também** sob `raspado` — é o cenário "Nenhuma camada fica
      anulada pelo traço escolhido". (`RF-04-06`)
- [x] 3.3 Redesenhar `coque`, com o coque encostando na touca e a amarração marcada, e `rabo`, com
      a cauda saindo de trás da cabeça e o laço marcado. Verificação: nenhuma forma solta —
      coque e cauda tocam a massa. (`RF-04-06`)
- [x] 3.4 Conferir as dez texturas contra os **quatro formatos de rosto** e os **oito tons de
      pele**, com cabelo `c1` sobre pele `t1` incluída. Verificação: nenhuma combinação deixa
      textura invisível nem peça da frente fora da cabeça. (`RF-04-06`, `RF-04-07`)

## 4. A composição de partida da montagem

- [x] 4.1 Em `apps/app-01-aula-presencial/src/onboarding/TelaDeCadastro.tsx`, abrir a montagem com
      `escreverAvatar({ fundo: "acao-100" })`. Verificação: a tela abre com fundo e roupa de cores
      diferentes, e escolher as duas iguais continua aceito e gravado. (`RF-04-06`, `RF-04-07`)
- [x] 4.2 Conferir que o `padrao` da camada de fundo segue `marca-100` e que
      `AVATAR_PADRAO_DO_PROJETO` não mudou. Verificação: os cenários do documento 15 §7.2 e §7.3
      em `avatar.test.tsx` passam sem alteração. (`RF-04-07`)

## 5. Testes

- [x] 5.1 Em `comum/avatar/avatar.test.tsx`, acrescentar os cenários de **distinguibilidade**:
      trocar traço muda o desenho, nenhum traço desenha igual a outro da mesma camada, e a troca
      de cor do cabelo aparece sob qualquer textura. Verificação: `vitest run comum/avatar`.
      (`RF-04-06`)
- [x] 5.2 Acrescentar os cenários da **peça da frente** (nove grupos na ordem, com a peça dentro
      do rosto) e do **contorno da roupa** nas quatro combinações de cor coincidente.
      Verificação: `vitest run comum/avatar`. (`RF-04-07`)
- [x] 5.3 Em `apps/app-01-aula-presencial/src/onboarding/onboarding.test.tsx`, acrescentar os dois
      cenários da composição de partida — abre com cores diferentes, e escolher iguais é aceito.
      Verificação: `vitest run apps/app-01-aula-presencial`. (`RF-04-06`)

## 6. Documentação

- [x] 6.1 No `docs/15-identidade-visual.md` §7.1: uma frase admitindo, na camada 5, as orelhas e a
      peça de cabelo da frente; uma frase declarando o contorno na camada 8. Registrar a decisão de
      2026-10-20 em `docs/09-topicos-em-aberto-e-sugestoes.md` §1. Marcar a fatia 30 como
      implementada em `openspec/cronograma-de-fatias.md`. Sem arquivo novo em `docs/`, então a
      `nav` do `mkdocs.yml` não muda; `docs/prds/index.md` e o documento 99 não mudam, porque a
      situação do PRD-04 e as relações entre documentos seguem as mesmas. Verificação:
      `npm run lint` e `mkdocs build --strict`.
