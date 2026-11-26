# Design

## Context

O padrão já está em `openspec/specs/responsavel-e-vinculo` e nas duas telas: `GET
/v1/responsaveis` monta cada vinculado a partir de `vinculados_por_responsavel`, que resolve os
nicks da página inteira numa consulta em lote e devolve `(vínculo, nick)`. As Apps 03 e 09 têm
um `ListaDeResponsaveis.tsx` quase idêntico, que imprime `nick (grau)` unidos por " · ".
`Persona.nome` é anulável.

## Goals / Non-Goals

**Goals:** o nome do vinculado na resposta e nas duas listas (`RF-02-111`, `RF-09-122`).

**Non-Goals:** mexer no recorte por papel, na paginação, na permissão ou nas outras rotas de
responsável.

## Decisions

1. **Os nomes saem na mesma consulta em lote dos nicks.** `vinculados_por_responsavel` passa a
   ler `Persona.id, Persona.nome` dos Guerreiros da página junto com o `Nick`, e devolve
   `(vínculo, nick, nome)`. _Descartado:_ `sessao.get(Persona)` por vinculado, que é N+1.
2. **`nome: str`, vazio quando ausente**, como o `nick` já faz. Quem apresenta decide o que
   dizer. _Descartado:_ `str | None`, que daria dois contratos de ausência na mesma linha.
3. **Formato na tela: `nick — nome (grau)`**, cada vinculado separado por " · ", como hoje. O
   nick segue primeiro porque é o identificador do jogo; nome ausente vira "sem nome", no molde
   de `SEM_NICK`. _Descartado:_ uma linha de tabela por vinculado, que quebraria a retomada,
   ancorada na linha do responsável.
4. **Mesma decisão para Admin e Mestre**, sem campo condicional por papel (decisão do fundador
   de 2026-11-26). _Descartado:_ omitir o nome ao Mestre, que daria dois contratos na mesma rota.

## Risks / Trade-offs

- [Nome civil de criança passa a sair a um segundo papel nessa leitura] → o Mestre já o lê nos
  desbloqueios pendentes da App 09; o recorte por comunidade e autoria continua limitando quem
  aparece, e nenhuma superfície pública muda (invariante 12).
