# Design — Avatar na fila de entregas e aulas sem as canceladas

## Context

Fatia 34 do PRD-09. Dois ajustes de apresentação em **Minhas turmas** da App 09, sem núcleo:

- `FilaDeEntregasPendentes.tsx` imprime `({pendencia.guerreiro_avatar})`, e o campo é o
  objeto do avatar serializado (`{"formaDeTratamento":…,"avatar":{"v":1,…}}`), lido por
  `lerAvatar` de `comum/avatar`.
- `TelaDeMinhasTurmas.tsx` lista `turmas.itens` inteiro, inclusive `situacao: "cancelada"`.

## Goals / Non-Goals

**Goals:** desenhar o avatar na fila (`RF-09-75`, `RN-09-18`); tirar a aula cancelada da
lista (`RF-09-42`).

**Non-Goals:** mudar a rota `GET` da fila ou de Minhas turmas; corrigir a fila do encontro na
App 01 (PRD-04), que tem o mesmo defeito; mexer no espaçamento entre período e situação da
aula.

## Decisions

1. **Reusar `Avatar` de `comum/avatar`**, como `TelaDeGuerreiros.tsx` já faz na App 09
   (`<Avatar avatar={…} tamanho={32} /> {nick}`). O componente aceita o texto cru e o resolve
   com `lerAvatar`, caindo no avatar padrão quando o texto é inválido — não há parse na tela.
   É `aria-hidden`; quem identifica o Guerreiro(a) é o nick.
2. **Filtrar na tela, não no núcleo.** `situacao` já vem na resposta; filtrar no cliente
   mantém a rota igual para quem a consome e não exige teste de backend. O filtro roda ao
   gravar o estado (`turmas.itens.filter(…)`), e a mensagem de lista vazia passa a valer
   também quando só havia canceladas.

## Risks / Trade-offs

- Aula cancelada some sem aviso → o Mestre não tem ação nela; aceito por decisão do fundador.
- O mesmo JSON segue na App 01 até fatia própria — registrado na proposta.
