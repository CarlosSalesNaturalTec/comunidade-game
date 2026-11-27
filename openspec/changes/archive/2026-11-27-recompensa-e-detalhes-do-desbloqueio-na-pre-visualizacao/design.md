# Design

## Context

A pré-visualização (`PreVisualizacaoDaMissao.tsx`) segue o requisito "O Mestre pré-visualiza a
missão como o Guerreiro(a) a verá" de `openspec/specs/area-do-mestre/spec.md`, e espelha a tela
da App 05. A missão já chega de `GET /v1/trilhas/minhas` com `desafio_pratico_titulo_curto` e
`desafio_pratico_kit_apresentado` (com `tipo_de_recurso_nome`); as recompensas de marco e os
tipos de recurso já estão carregados em `ListaDeMissoes`, que os passa ao bloco "Recompensa
pelo desbloqueio".

## Decisions

1. **Trecho do autor, separado.** A App 05 não mostra recompensa, título curto, kit nem corte
   na missão. Os itens novos vão num trecho próprio, depois do desafio, sob o rótulo "O que só
   você vê", para a ficha não sugerir que o Guerreiro(a) os lê ali. Descartada: misturá-los ao
   desafio, que tornaria a ficha infiel à App 05.
2. **Recompensa pelo nome, sem quantidade** — decisão do fundador de 2026-11-27. Nomes
   repetidos (dois lançamentos do mesmo tipo) aparecem uma vez. Tipo sem nome no catálogo cai
   em "Recurso", o mesmo texto de reserva de `DesafioDeDesbloqueio.tsx`.
3. **Dados por props, sem leitura nova.** `ListaDeMissoes` repassa à pré-visualização as
   recompensas já filtradas pela missão e o catálogo de tipos. Descartada: nova chamada ao
   núcleo ao abrir a ficha.
4. **Textos do corte reaproveitados.** As duas frases do quiz e da sondagem são as que o
   formulário do desafio já exibe; a sondagem nunca mostra o corte (`RN-05-46`).
