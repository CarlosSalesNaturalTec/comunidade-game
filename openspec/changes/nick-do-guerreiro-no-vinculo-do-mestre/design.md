# Design

## Context

Ver `proposal.md` — Why. O mesmo desenho já decidido na change
`nick-do-guerreiro-no-vinculo-da-gestao` (fatia 23 do PRD-02), aplicado à App 09. O padrão
da tela está consolidado em `openspec/specs/area-do-mestre/spec.md`; o núcleo não muda.

`listarGuerreirosVinculaveis` já popula o estado `guerreiros` com `{ id, nick, avatar }`,
usado pelo seletor da mesma tela, e `criarVinculo` já devolve `guerreiro_id`, que a tela
descarta.

## Goals / Non-Goals

**Goals:** a linha do vínculo confirmado identificar o Guerreiro(a).

**Non-Goals:** alterar o recorte do que o Mestre alcança, que `RF-09-62` e `RN-09-18` já
fixam; mexer no seletor, que já está correto.

## Decisions

1. **Cruzar em memória, pelo estado `guerreiros`** — mesma decisão 1 da fatia 23 do
   PRD-02, pelas mesmas razões. _Alternativa descartada:_ devolver o nick em `VinculoSaida`,
   que mudaria contrato do núcleo para um dado que a tela já tem.

2. **Formato da linha: `<nick> — <grau de parentesco>`**, sem o avatar. O seletor usa
   `nick — avatar` porque ali o avatar ajuda a escolher; na confirmação o que distingue é o
   nick, e repetir o avatar alongaria a linha sem ganho. _Alternativa descartada:_ repetir
   `nick — avatar — parentesco`.

3. **Sem correspondência no estado, a linha cai para o parentesco com marca explícita de
   Guerreiro(a) não identificado** — mesma decisão 3 da fatia 23 do PRD-02. Aqui o caso é
   um pouco menos remoto, porque `recomecar()` limpa `guerreiros` e `vinculos` juntos, mas
   o tratamento é o mesmo.

4. **Não extrair componente comum para `comum/`.** São duas listas de três linhas em
   aplicações distintas, e o fundador decidiu uma fatia por aplicação. _Alternativa
   descartada:_ componente compartilhado, que acoplaria as duas telas por um ganho de
   poucas linhas.

## Risks / Trade-offs

- [As duas changes corrigem o mesmo defeito em arquivos distintos e podem divergir na
  redação da linha] → o formato está fixado na decisão 2 das duas, idêntico; divergência
  aparece na revisão do segundo PR.
