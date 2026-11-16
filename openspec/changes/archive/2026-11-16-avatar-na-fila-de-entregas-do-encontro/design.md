# Design — Avatar na fila de entregas do encontro

## Context

Fatia 36 do PRD-04. `TelaDeEntregasDoEncontro.tsx` imprime `({pendencia.guerreiro_avatar})`,
e o campo é o objeto do avatar serializado, que `lerAvatar` de `comum/avatar` lê.

## Goals / Non-Goals

**Goals:** desenhar o avatar na fila do encontro (`RF-09-75`, `RF-04-55`).

**Non-Goals:** mudar a rota da fila do encontro ou o ato da entrega (`RF-09-76`).

## Decisions

1. **Reusar `Avatar` de `comum/avatar`**, como a fatia 34 do PRD-09 fez na App 09 e como
   `TelaDeEquipes.tsx` já faz na App 01. O componente aceita o texto cru e cai no avatar padrão
   quando ele é inválido; é `aria-hidden`, e o nick identifica o Guerreiro(a).

## Risks / Trade-offs

- Nenhum além do visual: o teste que conferia o texto do avatar na linha passa a conferir o
  desenho.
