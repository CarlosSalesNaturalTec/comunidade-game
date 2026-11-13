# Design

## Context

O padrão já está em `openspec/specs/area-do-mestre/spec.md` ("A App 09 declara a forma, o
critério e o título curto do prático" e "A App 09 reabre os três campos do prático já
declarado") e em `desbloqueio-da-missao` ("O desafio prático declara, opcional, o kit que
apresenta"). O núcleo recebe `kit_apresentado_id` em `POST /v1/missoes/{id}/desbloqueio`,
recusa com 422 por campo a recompensa de outra trilha e o kit no quiz, e devolve
`desafio_pratico_kit_apresentado` (`recompensa_de_marco_id`, `tipo_de_recurso_nome`) em `GET
/v1/trilhas/minhas` e na resposta da declaração. A `TelaDaTrilha` já carrega
`listarRecompensasDeMarco(trilha.id)` e a `ListaDeMissoes` já tem os tipos de recurso.

## Goals / Non-Goals

**Goals:** a escolha, a reabertura e o reenvio do kit no bloco do prático (`RF-09-141`).

**Non-Goals:** qualquer mudança de núcleo; as telas da customização e da conservação.

## Decisions

1. **As opções vêm das recompensas de marco já carregadas pela `TelaDaTrilha`**, repassadas
   pela `ListaDeMissoes` à `DesafioDeDesbloqueio` junto dos tipos de recurso e das missões, sem
   leitura nova. O rótulo é "tipo de recurso (quantidade) — marco de _missão_". Recompensa
   declarada na mesma sessão entra na lista pelo `onDeclararRecompensa` que já existe.
   - Descartado: filtrar por tipo de recurso ou pela posição da missão — o núcleo não distingue
     kit, e a regra é que quem diz é o Mestre autor.
2. **O kit vive no estado do formulário** como `recompensa_de_marco_id | ""`, inicializado da
   leitura, e vai em toda declaração do prático (`null` quando "nenhum"); no quiz vai ausente.
   É o que impede corrigir o critério de apagar o kit, já que a declaração substitui.
3. **Kit declarado fora da lista** — a leitura auxiliar das recompensas falhou — entra como
   opção própria, rotulada pelo `tipo_de_recurso_nome` da leitura, para a tela não reabrir em
   "nenhum" e apagá-lo na próxima gravação.
4. **A recusa reaproveita o aviso único do bloco**, que já mostra a mensagem do `ErroDaApi`.

## Risks / Trade-offs

- A lista das recompensas é auxiliar e pode falhar em silêncio → a decisão 3 preserva o kit, e
  a escolha vazia aponta o bloco da recompensa.
