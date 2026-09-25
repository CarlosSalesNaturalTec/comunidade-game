# Design

## Context

Ver `proposal.md` — Why. A spec alterada é `aplicacao-da-aula-presencial`, no requisito da medição
("O Mestre mede no aparelho a distância entre descritores") e num requisito novo para o
encerramento da sessão de trabalho.

O mecanismo do PIN já existe inteiro, entregue pela fatia 16: `pin/pinDeConfirmacao.ts` guarda o
verificador por persona em `sessionStorage`, confere o PIN no aparelho por PBKDF2-HMAC-SHA256 pelo
`SubtleCrypto`, conta os erros seguidos e marca o bloqueio. `AparelhoDaAula` já busca o verificador
ao abrir a sessão de trabalho e já apaga o estado quando a sessão cai. Esta fatia **não** cria
mecanismo: dá dois usos novos ao que existe.

## Goals / Non-Goals

**Goals:**

- Encerrar a sessão de trabalho pela tela inicial, com PIN.
- Exigir o mesmo PIN para abrir a bancada de medição.
- Um contador de erros para os três atos.

**Non-Goals:**

- Rota nova no núcleo para conferir PIN — descartada pelo fundador.
- Mudar a confirmação de identidade, que já pede PIN.
- Mudar o que a bancada faz depois de aberta.
- Encerrar a sessão do Guerreiro(a), que já termina a cada atendimento.

## Decisions

1. **A conferência do PIN sai da `TelaDeEntradaDoGuerreiro` para um lugar alcançável pelos três
   atos.** Hoje ela vive dentro da função `confirmar` daquela tela, junto do fluxo de abertura de
   sessão. Com três atos conferindo o mesmo PIN contra o mesmo contador, a conferência e o desfecho
   dela — confere, erra, bloqueou, sem verificador, sem PIN cadastrado — passam a ser um só lugar,
   ao lado do módulo que já guarda o estado. _Descartado:_ repetir o laço de conferência em cada
   tela, que faria três cópias do contador e três redações da mesma recusa.

2. **Só a tela inicial oferece o encerramento.** É a tela que aparece entre atendimentos
   (`RF-04-28`), e fora dela quem está com o aparelho é uma criança no meio do atendimento dela.
   _Descartado:_ saída no `Cabecalho` de toda tela, como a `NavegacaoDeAreas` faz nas aplicações da
   Operação — ali quem opera é sempre o adulto, e aqui não.

3. **PIN bloqueado recusa o encerramento, e a tela diz que fechar a aba encerra a sessão.** É o que
   fecha o laço sem abrir um oráculo: isentar o encerramento do contador daria tentativas ilimitadas
   para descobrir um PIN de quatro dígitos, e o PIN descoberto serviria depois à confirmação de
   identidade. Recusar sem dizer nada trancaria o aparelho. A frase é verdadeira — a sessão de
   trabalho vive em `sessionStorage` — e é a única saída que não enfraquece o bloqueio.
   _Descartado:_ isentar o encerramento do contador compartilhado; _descartado:_ recusar sem
   alternativa.

4. **Sem PIN cadastrado, os dois atos novos passam.** Quem não tem PIN também não confirma
   identidade nenhuma hoje — nenhuma porta se abre com isso —, e trancar a saída e o diagnóstico
   por uma configuração que se resolve na App 09 pioraria o encontro. O aviso de PIN não cadastrado
   já está na tela desde a fatia 16 (`RN-04-38`). Decisão do fundador de 2026-09-25.

5. **O aviso da fila lê a contagem, não o conteúdo.** A saída precisa dizer quantas presenças
   aguardam, e nada além: `FilaDePresencaPendente` já apresenta a lista a quem opera na tela
   inicial. _Descartado:_ impedir o encerramento com fila pendente — a fila sobrevive, e travar a
   saída por causa dela inventaria regra que o `RF-04-23` não pede.

6. **O PIN da bancada é guarda de tela, e a spec o declara.** O núcleo guarda
   `POST /v1/medicoes-do-limiar` pela permissão de quem grava, e continua a guardá-la assim.
   Declarar isso na spec é o que impede a leitura futura de tomar a exigência por conferência do
   núcleo — a classe de defeito que o invariante 25 e o princípio 16 do documento 03 existem para
   fechar, e que já apareceu cinco vezes neste mesmo caminho.

## Risks / Trade-offs

- **Criança encerrando a sessão do Mestre** → a saída fica só na tela inicial e atrás do PIN; as
  duas juntas fazem do encerramento um ato de adulto.
- **Aparelho sem saída com PIN bloqueado** → a recusa diz que fechar a aba encerra a sessão
  (decisão 3). O caso exige cinco erros seguidos e não se cria com um toque.
- **Fila pendente perdida por saída no fim do encontro** → a fila vive em `localStorage` e
  sobrevive; o aviso diz o que é preciso para sincronizá-la. O cenário "Encerrar não descarta a
  fila" fecha a regressão.
- **A exigência lida como garantia do núcleo** → declarada na spec como guarda de tela
  (decisão 6).
