# Tasks

## 1. A conferência do PIN num lugar só

- [x] 1.1 Em `apps/app-01-aula-presencial/src/pin/pinDeConfirmacao.ts`, reunir a conferência do PIN
      no aparelho e os desfechos dela — confere, erra, bloqueou, sem verificador, sem PIN cadastrado
      — de modo alcançável pelos três atos, sobre o estado e o contador que o módulo já guarda
      (`RN-04-41`, `RN-04-38`, design — decisão 1).
- [x] 1.2 Em `entrada/TelaDeEntradaDoGuerreiro.tsx`, passar a confirmação de identidade a usar essa
      conferência, sem mudar recusa, redação nem desfecho algum daquela tela (`RF-04-21`,
      `RN-04-37`).

## 2. Encerrar a sessão de trabalho pela tela inicial

- [x] 2.1 Em `sessao-de-trabalho/AparelhoDaAula.tsx`, levar o encerramento da sessão de trabalho à
      `TelaInicial`, junto do que ela já recebe (`RF-04-71`, `RF-04-05`).
- [x] 2.2 Em `inicio/TelaInicial.tsx`, apresentar o encerramento **só na tela inicial**, pedindo o
      PIN de quem abriu o aparelho e tratando os cinco desfechos: encerra, PIN errado, PIN
      bloqueado com a frase de fechar a aba, sem PIN cadastrado e fila local pendente
      (`RF-04-71`, `RN-04-41`, design — decisões 2, 3 e 4).
- [x] 2.3 Ler a contagem da fila local para o aviso, em `fila/filaDePresenca.ts`, sem alterar o que
      a fila guarda nem quando ela sincroniza (`RF-04-23`, `RF-04-25`, design — decisão 5).
- [x] 2.4 Conferir que o encerramento descarta o verificador do PIN e volta à tela de abertura sem
      dado de atendimento em tela — o `AparelhoDaAula` já apaga o estado do PIN quando a sessão
      cai, e a tarefa afirma que segue valendo pelo caminho novo (`RF-04-71`, `RF-04-28`,
      `RN-04-38`).

## 3. PIN na bancada de medição

- [x] 3.1 Em `inicio/TelaInicial.tsx`, pedir o PIN antes de abrir a `TelaDeMedicaoDoLimiar` pelo
      caminho do diagnóstico, sem preparar a câmera antes de o PIN conferir (`RF-04-63`,
      `RF-04-66`, `RN-04-41`).
- [x] 3.2 Conferir que a medição **dentro do onboarding** não muda: ali o alcance é `guerreiro`,
      depois do consentimento, e o PIN não entra no meio do fluxo do termo (`RN-04-33`,
      `RN-04-07`).

## 4. Testes

- [x] 4.1 Em `inicio/inicio.test.tsx`, cobrir os sete cenários do requisito novo: a saída existe na
      tela inicial e só nela, encerrar com PIN correto, PIN errado contando no mesmo contador, PIN
      bloqueado com a frase de fechar a aba, sem PIN cadastrado, fila pendente anunciada e fila
      preservada depois de encerrar (`RF-04-71`, `RN-04-41`).
- [x] 4.2 Em `bancada/bancada.test.tsx`, cobrir "A bancada não abre sem o PIN" e "PIN bloqueado não
      abre a bancada", afirmando que o preparo da câmera não acontece antes da conferência
      (`RF-04-63`, `RF-04-66`, `RN-04-41`).
- [x] 4.3 Em `entrada/entrada.test.tsx`, conferir que a confirmação de identidade segue com as
      mesmas recusas e o mesmo desfecho depois de passar pela conferência comum, e que o contador é
      partilhado — errar na entrada e depois na saída soma (`RF-04-21`, `RN-04-37`, `RN-04-41`).
- [x] 4.4 Em `fila/fila.test.tsx`, conferir que encerrar a sessão de trabalho não descarta a fila e
      que ela volta a sincronizar quando o aparelho reabre naquela aula (`RF-04-23`, `RF-04-25`).

## 5. Documentação

- [x] 5.1 Marcar a fatia 20 como implementada em `openspec/cronograma-de-fatias.md`.
- [x] 5.2 Conferir que o PR de revisão do PRD-04 entrou antes, com `RF-04-71` e `RN-04-41` na §6.1 e
      na §7, a decisão nova na §13 e a linha correspondente no documento 09 §1 — a change **não**
      cria os identificadores. Nada muda em `docs/prds/index.md`, no documento 99 nem na `nav` do
      `mkdocs.yml`: a situação do PRD-04 não muda, nenhuma relação entre documentos muda e nenhum
      arquivo nasce.
