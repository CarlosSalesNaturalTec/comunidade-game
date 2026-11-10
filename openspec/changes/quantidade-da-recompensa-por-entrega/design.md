## Context

A entrega e a fila já estão consolidadas em `openspec/specs/recompensa-de-marco/spec.md`. Em
`backend/src/nucleo/recompensas_de_marco/regra.py`, `_validar_entrega` conta as entregas da
recompensa e recusa quando a contagem chega a `quantidade`. Já `registrar_entrega` usa a mesma
`quantidade` para o lastro e para o débito de cada entrega. `listar_entregas_pendentes` repete
a contagem para marcar `quantidade_esgotada`, e as Apps 09 e 01 imprimem essa marca.

## Decisions

- **A contagem da recompensa vira conferência do par.** Sai a contagem de todas as entregas da
  recompensa. Entra a busca de uma entrega daquela recompensa **àquele** Guerreiro(a), que recusa
  com 422. A spec já exigia "uma por Guerreiro(a)", mas só a fila garantia isso (`ja_recebeu`):
  um `POST` direto, ou as Apps 01 e 09 abertas ao mesmo tempo, entregaria duas vezes. A busca
  roda sob o `FOR UPDATE` que já existe na linha da recompensa, o que serializa as entregas
  concorrentes. A ordem das recusas fica: durável, lastro, já recebeu, comunidade, marco.
  - Descartado: restrição única `(recompensa_de_marco_id, guerreiro_id)` no banco. Exigiria
    migração, e a trava de linha já basta, como basta em `catalogo_avulso`.
- **`quantidade_esgotada` sai da resposta, e não fica fixo em `false`.** Manter um campo que
  nunca muda deixaria um contrato morto. Só as Apps 09 e 01 o leem, e mudam no mesmo PR.
- **O rótulo vira "Quantidade por Guerreiro(a)"**, só na App 09, que é a única que declara. A
  lista de recompensas já declaradas, logo acima do formulário, ganha o mesmo "por
  Guerreiro(a)", para a leitura bater com a declaração.

## Risks / Trade-offs

- [O deploy chega fora de ordem] → não tem efeito. Uma app antiga lê o campo ausente como falso,
  e um núcleo antigo manda um campo que a app nova ignora.
- [Duas entregas simultâneas ao mesmo Guerreiro(a), pelas Apps 01 e 09] → a segunda espera a
  trava da linha da recompensa, encontra a primeira gravada e é recusada.
