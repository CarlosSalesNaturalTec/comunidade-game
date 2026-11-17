# Tasks

## 1. Sorteio na camada comum

- [ ] 1.1 Criar `sortearAvatar(aleatorio?)` em `comum/avatar/objeto.ts`, exportado por
      `comum/avatar/indice.ts`: um traço do catálogo por camada, no objeto versionado
      (`RF-02-01`, documento 15 §7). Verificar: o tipo compila e a exportação aparece no índice.
- [ ] 1.2 Cobrir em `comum/avatar/avatar.test.tsx` os três cenários do sorteio — só traços do
      catálogo na versão vigente, todo traço de cada camada alcançável (com `aleatorio`
      controlado) e a ida e volta por `lerAvatar` sem cair no padrão (`RF-02-01`). Verificar:
      `vitest run` dos testes do avatar passa.

## 2. Formulário de Guerreiro(a) na App 03

- [ ] 2.1 Em `apps/app-03-gestao/src/personas/FormularioDeGuerreiro.tsx`, retirar o estado, o
      `Campo` "Avatar" e a checagem "Escolha o avatar."; no cadastro enviar o avatar sorteado; na
      edição reenviar o gravado, sorteando só quando vazio; o aviso de coleta passa a citar nome,
      data de nascimento e nick (`RF-02-01`, `RN-02-22`, `RN-02-23`). Verificar: os testes de 2.2.
- [ ] 2.2 Ajustar `apps/app-03-gestao/src/personas/personas.test.tsx`: o preenchimento deixa de
      digitar avatar; o cadastro envia avatar do catálogo; o formulário não tem campo de avatar e
      o aviso cita só os três dados; a edição reenvia o avatar gravado e sorteia quando vazio;
      nick em uso e a ausência de imagem real seguem cobertos (`RF-02-01`, `RN-02-22`,
      `RN-02-23`). Verificar: `vitest run` da App 03 passa.

## 3. Documentação

- [ ] 3.1 Registrar a decisão e fechar a fatia: documento 15 §7 ganha uma frase (no cadastro
      pela gestão o avatar é sorteado do catálogo); documento 09 §1 ganha a linha em "Já
      decididos"; PRD-02 reescreve `RF-02-01`; documento 99 §5 inclui o PRD-02 entre os que
      aplicam o sistema de avatar; a linha da fatia 28 do cronograma vira `implementado` com o
      slug. `docs/prds/index.md` e `mkdocs.yml` não mudam. Verificar: `mkdocs build --strict` e
      `npm run lint` passam.

## Workflow follow-up

- `/opsx:verify` e `/opsx:archive` ao fim da implementação.
