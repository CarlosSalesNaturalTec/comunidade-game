## 1. Tokens

- [x] 1.1 Declarar em `comum/tokens.css` os **marcos de largura** (`768`, `1024`, `1280`) e a
      **grade de colunas** (`4` · `8` · `12`, calha de `16` px) do documento 15 §4, hoje
      ausentes, mais a largura de área densa que a tabela consome; a largura de leitura de 64
      caracteres permanece intacta (documento 15 §4, design — decisões 1 e 5).
- [x] 1.2 Acrescentar ao bloco `:root[data-temperamento="operacao"]` o que a densidade
      progressiva muda a partir do marco de `768` px, sem tocar no que vale abaixo dele
      (documento 15 §6, design — decisão 1).

## 2. `comum/react` — componentes novos

- [x] 2.1 `Tabela.tsx`: marcação semântica de tabela, `th` com escopo, `caption` opcional,
      rolagem horizontal confinada ao componente e recolhimento de colunas abaixo do marco
      (design — decisões 1 e 2).
- [x] 2.2 `Dialogo.tsx`: sobre o elemento `dialog` nativo por `showModal`, com rótulo
      acessível, fechamento por botão rotulado e devolução do foco ao elemento que o abriu
      (design — decisão 3).
- [x] 2.3 `NavegacaoDeAreas.tsx`: recebe as áreas, a área corrente e a saída da sessão;
      marca a corrente por `aria-current` e por sinal que não seja só cor, e apresenta a saída
      **uma única vez** ao fim da navegação (design — decisão 4).
- [x] 2.4 `Moldura.tsx` ganha a largura de área densa como variante, mantendo a de leitura
      como padrão; `estilos.css` recebe o estilo dos três componentes novos e `indice.ts` os
      exporta (design — decisão 5).
- [x] 2.5 Prover `HTMLDialogElement.showModal` na configuração de teste de `comum/`, sem o
      que o teste do diálogo falha por ambiente (design — Risks).

## 3. App 03 — navegação e saída única

- [x] 3.1 `App.tsx` adota `NavegacaoDeAreas` com as 16 áreas e a saída da sessão.
      `.cg-navegacao`/`.cg-navegacao__item` permanecem em `index.css`: a tela de Personas
      (fatia 18, fora do escopo desta) ainda os usa para a sub-navegação de tipo de persona,
      que esta fatia não toca — só o comentário do bloco foi corrigido para não atribuí-lo à
      navegação de áreas, que agora é o `NavegacaoDeAreas` de `comum/react`.
- [x] 3.2 Remover a ação "Sair" das 16 telas de área (`TelaDeComunidades`, `TelaDePoderes`,
      `TelaDePontosDeApoio`, `TelaDoAcervo`, `TelaDaAgenda`, `TelaDeRecursos`,
      `TelaDeAtividades`, `TelaDePersonas`, `TelaDeTerritorio`, `TelaDeFilas`, `TelaDeChaves`,
      `TelaDoPainelDoDia`, `TelaDeLancamentos`, `TelaDeQuiz`, `TelaDeEncerramentoDeCiclo`,
      `TelaDeDireitos`), deixando o `acao` do `Cabecalho` livre para a ação da própria tela.

## 4. App 09 — navegação e saída única

- [x] 4.1 `App.tsx` adota `NavegacaoDeAreas` com as 12 áreas, o alerta de solicitações em
      aberto e a saída da sessão; as classes órfãs `.cg-navegacao-de-area` e
      `.cg-navegacao-de-area__alerta`, usadas sem definição em CSS nenhum, deixam de existir.
- [x] 4.2 Remover a ação "Sair" das telas de área — a lista original desta tarefa tinha 9 e
      faltava `TelaDeDesafiosExtras`, que também montava a ação; as 10 telas
      (`TelaDeAutoria`, `TelaDeMinhasTurmas`, `TelaDoBancoDeQuiz`,
      `TelaDeDesbloqueiosPendentes`, `TelaDeCriacoesAValidar`, `TelaDeTerritorio`,
      `TelaDeDesafiosExtras`, `TelaDePropostas`, `TelaDeRecursos`, `TelaDeDireitos`) perderam a
      ação, cumprindo o requisito "nenhuma dentro das telas de área".

## 5. Consolidação da tabela duplicada

- [x] 5.1 Trocar por `Tabela` a marcação da tabela de direitos das Apps 03, 08 e 09, e apagar
      `.cg-tabela-de-direitos` dos três `index.css`, hoje idênticas (design — decisão 6).

## 6. Testes

- [x] 6.1 `comum/react`: a tabela anuncia a célula com o cabeçalho da coluna e confina a
      rolagem; o diálogo prende o foco, fecha por escape e devolve o foco ao elemento de
      origem; a navegação marca a área corrente por `aria-current` e apresenta uma única
      saída (cenários "Leitura por tecnologia assistiva", "Tabela mais larga que a tela", "O
      foco não escapa do diálogo aberto", "Fechar devolve o foco", "A área corrente é
      reconhecível sem cor").
- [x] 6.2 Apps 03 e 09: percorrer as áreas e conferir que existe **exatamente uma** saída da
      sessão, sempre no mesmo lugar, e nenhuma dentro das telas de área (cenário "A saída
      existe uma vez").
- [x] 6.3 Tokens: os marcos declarados são os do documento 15 §4 e nenhum outro (cenário
      "Nenhum marco fora do documento"); a `Tabela` mostra as colunas essenciais e confina a
      rolagem abaixo do marco, e mostra as demais a partir dele (cenários "A área é inteira
      operável no celular em pé", "A partir do marco, aparece o que estava recolhido").

## 7. Documentação

- [x] 7.1 Documento 15 §6: acrescentar a linha da **densidade progressiva** ao quadro dos
      temperamentos, mantendo o caso que dimensiona a Operação. Documento 09 §1: registrar em
      *Já decididos* a decisão do fundador de 2026-09-06 (não havia pendência prévia sobre o
      tema — a linha nasce decidida, como outras da mesma tabela). Marcar a fatia transversal
      como implementada em `openspec/cronograma-de-fatias.md`. Nenhum arquivo novo em `docs/`,
      logo nenhuma entrada nova na `nav` do `mkdocs.yml`; a relação entre documentos não muda,
      logo o documento 99 não é tocado.
