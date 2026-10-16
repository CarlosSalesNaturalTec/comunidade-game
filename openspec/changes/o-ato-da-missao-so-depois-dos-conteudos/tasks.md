# Tasks

## 1. O gate em `comum/trilha/Missao.tsx`

- [ ] 1.1 Extrair o bloco "conteúdo + ato" da `Missao` para um componente filho montado com
      `key={missaoPublica.id}`, que guarda o índice do conteúdo da vez em `useState` e o
      comanda no `SequenciaPaginada` por `indice`/`aoIrPara` (design — decisão 1). Verificar
      que `comum/react/SequenciaPaginada.tsx` segue intocado no `git diff --stat`.
- [ ] 1.2 Derivar o predicado do gate dos quatro casos da decisão 3 — buscando (fechado),
      falhou (aberto), lista vazia (aberto), senão `indice === lista.length - 1` — e
      condicionar a ele a renderização da `Sondagem` e do `DesafioDeDesbloqueio`, mantendo as
      condições de hoje (`e_proxima`, `!aguardando_mestre`, `desafio_de_desbloqueio`).
      Atende `RF-04-73`, `RF-05-13`, `RF-05-14`, `RF-05-89`, `RN-05-45`.
- [ ] 1.3 Deixar a entrega da produção (`entregaDaProducao`) **fora** do gate, sob
      `missao.desbloqueada` como hoje (design — decisão 5). Atende `RF-05-11`; verificar pelo
      cenário "A entrega da produção não depende do percurso do conteúdo".

## 2. Cenários do gate em `comum/trilha/trilha.test.tsx`

- [ ] 2.1 Cobrir o gate e as suas bordas numa suíte própria: o ato oculto no primeiro de
      quatro conteúdos, apresentado ao alcançar o último, apresentado de imediato na missão
      sem conteúdo algum e na de conteúdo único, e a sondagem sob a mesma regra. Atende
      `RF-04-73`, `RF-05-13`, `RF-05-89`.
- [ ] 2.2 Cobrir o reset do índice — o risco central do design: desbloquear a missão, a
      seguinte abrir no primeiro conteúdo **com o ato oculto**, e não no índice da anterior.
      Atende `RF-05-14`; cenário "A missão seguinte recomeça com o ato oculto".
- [ ] 2.3 Cobrir os dois estados em que não há conteúdo em tela: a busca que **falha** libera
      o ato junto do aviso de erro, e a busca **em curso** o mantém oculto sem piscar
      (design — decisão 4). Atende `RF-04-73`, `RF-05-13`.

## 3. Acerto dos testes já existentes das duas aplicações

- [ ] 3.1 Ajustar o **arranjo** — nunca a asserção do gate — dos testes de
      `comum/trilha/trilha.test.tsx` que alcançam o ato da missão, levando-os ao último
      conteúdo antes de procurá-lo em tela.
- [ ] 3.2 Ajustar, pelo mesmo critério, os testes da App 01 em
      `apps/app-01-aula-presencial/src/trilhas/trilhas.test.tsx` que hoje encontram o desafio
      ou a sondagem sem percorrer o conteúdo.
- [ ] 3.3 Ajustar, pelo mesmo critério, os testes da App 05 em `Missao.test.tsx`,
      `GuiaDaTrilha.test.tsx`, `Trilha.test.tsx` e `DesafioDeDesbloqueio.test.tsx`,
      confirmando que a aplicação recebe o comportamento sem mudança própria de código.
- [ ] 3.4 Conferir que os testes do conteúdo um por vez (fatia 22) e dos quatro grupos
      (fatia 27) seguem verdes **sem alteração de asserção**: é a prova de que a navegação dos
      conteúdos e a ordem dos grupos não mudaram.

## 4. Documentação

- [ ] 4.1 Virar a situação da **fatia 29** do bloco do PRD-04 em
      `openspec/cronograma-de-fatias.md` de `em andamento` para `implementado` — a linha e o
      slug já nasceram com a abertura da change. Conferir o recorte escrito ali contra o que
      foi entregue e corrigir a linha se divergir.
- [ ] 4.2 Registrar que nada mais muda: nenhuma decisão nova a gravar em documento-fonte nem
      no documento 09, nenhum PRD afetado, nenhuma mudança de situação em
      `docs/prds/index.md`, nenhuma relação nova no documento 99 e nenhum arquivo novo na
      `nav` do `mkdocs.yml` — a fatia é apresentação e não toca `docs/`.
