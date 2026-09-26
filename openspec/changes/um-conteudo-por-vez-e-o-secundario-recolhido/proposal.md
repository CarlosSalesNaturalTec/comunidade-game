# Proposal

## Why

A leitura da trilha empilha numa tela só o conteúdo inteiro da missão e todas as perguntas do
desafio, e ainda intercala metadado — crédito e licença do Mestre autor — e o aviso da missão
seguinte, que adianta o que a criança ainda não desbloqueou. É a densidade da Operação numa
aplicação da Arena, que o documento 15 §6 define por poucos elementos e uma decisão por tela,
e quem tem 6 anos rola a tela até reencontrar onde parou.

Fatia 22 do PRD-04, decisão do fundador de 2026-09-26 (documento 09 §1, documento 15 §§6.1,
6.4). É **apresentação**: não cria nem altera requisito de produto, como a fatia 19.

## What Changes

- Os **conteúdos da missão** passam a sair **um por vez**, com botão de avançar, na ordem do
  autor (`RF-05-11`, `RF-04-73`).
- As **perguntas do desafio de desbloqueio e da sondagem** passam a sair **uma por vez**, com
  botão de avançar. A **submissão continua sendo do conjunto**, numa vez só, porque o critério
  de aprovação é dos 60% sobre o total (`RF-05-13`, `RF-05-14`, `RN-05-45`).
- Os **conteúdos da missão do dia** no caminho das Equipes passam a sair **um por vez**
  (`RF-04-35`). Entrou no recorte por decisão do fundador de 2026-09-26: a linha do cronograma
  não listava o `RF-04-35`, e o documento 15 §6.4 vale para a Arena inteira.
- O **crédito e a licença da trilha** saem do fluxo de leitura para um **bloco recolhível de
  resumo neutro** (`RF-05-11`).
- O **aviso da missão seguinte trancada** sai do fluxo de leitura para um **bloco recolhível
  de resumo neutro** (`RF-05-08`, `RF-05-10`, `RF-04-72`).
- O **bloco recolhível** deixa de ser exclusivo do temperamento Operação: ganha na Arena um uso
  próprio e único, o de tirar da leitura o que é secundário.

Não é **BREAKING**: recolher não é apagar. O `RF-05-08` segue entregando o que a missão
desbloqueia e o `RF-05-10` segue exibindo o motivo do bloqueio — este último em dois lugares, e
o aviso dentro da própria missão trancada não é tocado.

Fora de escopo, declarado: o **Quiz ao Vivo**, onde quem passa a pergunta é o Mestre
(`RF-04-41` a `RF-04-44`) e botão de avançar no aparelho da equipe mentiria sobre quem comanda;
e a linha **"Fonte: X"** do conteúdo de terceiro, que é atribuição de autoria alheia, não o
crédito do Mestre autor que a decisão mandou recolher.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `camada-visual-comum`: o bloco recolhível deixa de ser só das telas da Operação e ganha o uso
  da Arena, com resumo neutro.
- `area-do-guerreiro`: o conteúdo da missão e as perguntas do desafio passam a um por vez, e o
  crédito com a licença passa a recolhido.
- `aplicacao-da-aula-presencial`: o mesmo no percurso do Guerreiro(a) e no conteúdo da missão
  do dia das equipes, e a missão seguinte trancada passa a recolhida.

## Impact

| Onde | O que muda |
| ---- | ---------- |
| `comum/trilha/Missao.tsx` | conteúdos um por vez; crédito e licença em bloco recolhível |
| `comum/trilha/DesafioDeDesbloqueio.tsx` | perguntas uma por vez; submissão do conjunto intacta |
| `comum/trilha/GuiaDaTrilha.tsx` | missão seguinte em bloco recolhível |
| `comum/react/BlocoRecolhivel.tsx` | admite o uso da Arena |
| `apps/app-01-aula-presencial/src/trilhas/TelaDaProgramacao.tsx` | conteúdos do dia um por vez |
| `openspec/cronograma-de-fatias.md` | a linha da fatia 22 ganha o `RF-04-35` |

Alcança **App 01 e App 05**, porque os componentes de trilha são de `comum/`, promovidos na
fatia 21 — decisão do fundador de que as duas mudam juntas, para a mesma criança não ver telas
diferentes na aula e em casa.

Sem rota nova, sem entidade nova, sem mudança no núcleo. Nenhuma pasta nova, logo nenhuma
esteira de CI nova.
