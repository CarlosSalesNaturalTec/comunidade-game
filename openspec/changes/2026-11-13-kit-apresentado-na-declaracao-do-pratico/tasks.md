# Tasks

## 1. Contrato da App 09

- [ ] 1.1 Em `apps/app-09-mestre/src/trilhas/api.ts`, acrescentar `KitApresentado`
      (`recompensa_de_marco_id`, `tipo_de_recurso_nome`), `desafio_pratico_kit_apresentado` em
      `MissaoDaTrilha` e `kit_apresentado_id?: string | null` em
      `DeclararDesafioDeDesbloqueioEntrada` (`RF-09-141`)

## 2. Tela

- [ ] 2.1 Em `ListaDeMissoes.tsx`, repassar à `DesafioDeDesbloqueio` as recompensas de marco da
      trilha, os tipos de recurso e as missões, e dizer o kit no resumo recolhido do prático
      (`RF-09-141`)
- [ ] 2.2 Em `DesafioDeDesbloqueio.tsx`, a escolha do kit só no prático, com "nenhum kit", o
      rótulo por tipo de recurso e missão do marco e o texto de ajuda; a escolha vazia aponta o
      bloco da recompensa pelo desbloqueio (`RF-09-141`)
- [ ] 2.3 Em `DesafioDeDesbloqueio.tsx`, reabrir o kit da leitura, incluir como opção o kit
      declarado ausente da lista, e mandar `kit_apresentado_id` em toda declaração do prático e
      nunca no quiz (`RF-09-141`)

## 3. Testes

- [ ] 3.1 Em `src/trilhas/trilhas.test.tsx`, cenários de "A App 09 declara, opcional, o kit que
      o prático apresenta": opções pelas recompensas da trilha, kit opcional, trilha sem
      recompensa, quiz sem o campo, sondagem sem a escolha (`RF-09-141`)
- [ ] 3.2 No mesmo arquivo, cenários de "A App 09 reabre o kit declarado e o reenvia": reabertura,
      correção do critério reenviando o kit, kit fora da lista preservado, recusa com motivo e
      resumo do bloco (`RF-09-141`)

## 4. Documentação

- [ ] 4.1 Marcar a fatia 31 do PRD-09 como `implementado` em `openspec/cronograma-de-fatias.md`,
      com o slug da change. Sem decisão nova: `docs/`, documento 09, documento 99 e `mkdocs.yml`
      não mudam; `docs/prds/index.md` só se a situação do PRD-09 mudar
