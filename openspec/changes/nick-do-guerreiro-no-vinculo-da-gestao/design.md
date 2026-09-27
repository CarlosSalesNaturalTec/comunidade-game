# Design

## Context

Ver `proposal.md` — Why. O padrão da tela já está consolidado em
`openspec/specs/aplicacao-de-gestao/spec.md`; esta fatia só corrige uma linha de
apresentação. Nada no núcleo muda.

Dois fatos do estado atual decidem o desenho:

- `listarGuerreiros` já popula o estado `guerreiros` com `{ id, nick, … }`, usado pelo
  seletor de Guerreiro(a) do mesmo formulário.
- `criarVinculo` devolve `guerreiro_id`, que a tela hoje descarta.

O cruzamento é local: nenhuma consulta nova, nenhum campo novo no contrato.

## Goals / Non-Goals

**Goals:** a linha do vínculo confirmado identificar o Guerreiro(a).

**Non-Goals:** carregar Guerreiro(a) fora da página já carregada; reordenar, agrupar ou
paginar a lista de vínculos; mexer no seletor, que já está correto.

## Decisions

1. **Cruzar em memória, pelo estado `guerreiros`** — e não pedir o nick ao núcleo. O
   seletor só oferece Guerreiros e Guerreiras dessa mesma lista, então todo vínculo criado
   na sessão tem o nick carregado. _Alternativa descartada:_ devolver o nick em
   `VinculoSaida` — mudaria contrato do núcleo para um dado que a tela já tem.

2. **Formato da linha: `<nick> — <grau de parentesco>`.** O nick vem primeiro porque é ele
   que distingue as linhas; o parentesco qualifica. _Alternativa descartada:_ parentesco
   primeiro, que mantém a ambiguidade na leitura de cima para baixo.

3. **Sem correspondência no estado, a linha cai para o parentesco com marca explícita de
   Guerreiro(a) não identificado** — nunca some e nunca fica com o rótulo mudo de hoje. O
   caso é improvável (exigiria a lista mudar sob o formulário), mas o silêncio é
   exatamente o defeito que esta fatia corrige. `GuerreiroSaida.nick` é `str` não nulo no
   núcleo, então nick vazio só ocorreria por dado inconsistente; o mesmo caminho o cobre.

## Risks / Trade-offs

- [A lista de Guerreiros e Guerreiras é paginada, e o formulário só carrega a primeira
  página] → o seletor tem a mesma limitação hoje e ela não é desta fatia; o vínculo nunca
  alcança quem não estava no seletor. Fica registrado como limite conhecido, não como
  regressão.
