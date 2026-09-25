# Tasks

## 1. O catálogo e o renderizador em `comum/`

- [x] 1.1 Criar `comum/avatar/` com o **catálogo fechado** das nove camadas do documento 15 §7.1,
      cada traço com nome dizível em português, a escala de tons de pele aberta pelo mais retinto e
      as texturas crespas antes das lisas (design — decisões 1 e 5).
- [x] 1.2 Implementar o **renderizador** que compõe as camadas na ordem do §7.1, em SVG embutido,
      sem requisição alguma (design — decisão 5).
- [x] 1.3 Implementar a leitura e a escrita do **objeto versionado** do §7.2, com traço desconhecido
      caindo no padrão da camada e sem quebrar a renderização (design — decisão 2).
- [x] 1.4 Implementar o **avatar padrão do projeto** do §7.3, usado no lugar de qualquer avatar que
      falte, na mesma moldura e sem marca de diferença.
- [x] 1.5 Exportar a pasta em `comum/package.json`.
- [x] 1.6 Cobrir, em teste do `comum`, os sete cenários do delta de `camada-visual-comum`.

## 2. O onboarding compõe o avatar

- [x] 2.1 Em `apps/app-01-aula-presencial/src/onboarding/TelaDeCadastro.tsx`, trocar o campo de
      texto livre pela escolha no catálogo, camada por camada, nascendo no avatar padrão
      (`RF-04-07`, design — decisão 4).
- [x] 2.2 Gravar no campo `avatar` o objeto versionado do §7.2, mantendo a forma de tratamento em
      campo próprio ao lado dele (`RF-04-07`, design — decisão 3).
- [x] 2.3 Conferir que a composição não dispara requisição alguma.

## 3. As telas de equipe desenham o avatar

- [x] 3.1 Em `apps/app-01-aula-presencial/src/equipes/TelaDeEquipes.tsx` e
      `src/trilhas/EquipeDaTrilha.tsx`, desenhar o avatar de cada integrante ao lado do nick, sem
      exibir dado pessoal algum (`RF-04-34`, `RN-04-14`).
- [x] 3.2 Em `apps/app-05-guerreiro/src/desafios/MinhasEquipes.tsx` e
      `src/carteira/MinhaCarteira.tsx`, o mesmo (`RF-05-23`). **Feito em
      `MinhasEquipes.tsx`**, que recebe os integrantes com o campo `avatar`.
      **Não feito em `MinhaCarteira.tsx`**: a tela não mostra integrante algum —
      mostra o *próprio* perfil público —, e `GET /v1/eu` não devolve o `avatar`
      do Guerreiro(a) em sessão. Desenhar ali o padrão do projeto diria à criança
      que aquele é o avatar dela, o que é falso, e servir o avatar próprio é rota
      do PRD-01, fora desta fatia. Levado ao documento 09 §1 como pendência, em
      vez de resolvido por suposição.

## 4. Testes

- [x] 4.1 Em `onboarding/onboarding.test.tsx`, cobrir "O avatar nasce do catálogo, não de texto
      livre", "O que se grava é o objeto versionado" e "Compor não depende de rede" (`RF-04-07`).
- [x] 4.2 Em `equipes/equipes.test.tsx` e `trilhas/trilhas.test.tsx`, cobrir "O avatar aparece
      desenhado ao lado do nick" e "Avatar que falta cai no padrão do projeto" (`RF-04-34`).
- [x] 4.3 Nos testes da App 05 que hoje mencionam avatar, cobrir o avatar desenhado dos integrantes
      (`RF-05-23`).
- [x] 4.4 Cobrir o avatar gravado no formato antigo — `{ formaDeTratamento,
      caracteristicasDoAvatar }` — caindo no padrão do projeto sem quebrar tela alguma (design —
      decisão 2).

## 5. Documentação

- [x] 5.1 Marcar a linha desta fatia como implementada em `openspec/cronograma-de-fatias.md`.
- [x] 5.2 Acrescentar ao **documento 03 §1.2** a linha de `comum/avatar/` (design — decisão 1).
- [x] 5.3 Registrar no documento 09 §1 a pendência da **escolha do avatar por conversa** na
      modalidade áudio do onboarding (`RF-04-06`, design — decisão 4). O documento 15 **não** muda:
      a change o cumpre. Nada muda em `docs/prds/index.md` nem no documento 99, e nenhum arquivo
      nasce em `docs/`.
