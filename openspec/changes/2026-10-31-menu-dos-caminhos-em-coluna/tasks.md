# Tasks

## 1. Poda da lista de caminhos no `comum`

- [x] 1.1 Em `comum/react/ListaDeCaminhos.tsx`, remover o tipo `DisposicaoDeCaminhos`, a
      propriedade `disposicao`, a propriedade `caminhoAtual`, o parâmetro `atual` do
      `CartaoDeCaminho` e o `aria-current` do botão; a lista passa a emitir sempre
      `cg-caminhos`, sem variante. Verificação: `tsc` não acusa referência órfã e nenhum
      `aria-current` resta no arquivo (`RF-05-08`, specs `camada-visual-comum` — "A camada
      comum entrega a lista de caminhos em cartão, um por linha", design — decisão 6).
- [x] 1.2 Em `comum/react/estilos.css`, remover `.cg-caminhos--grade`, as regras de grade do
      cartão, o bloco `@media (min-width: 768px)` da grade e `.cg-caminho[aria-current]`,
      ajustando o comentário do bloco para a disposição única. Verificação: `grep -c
      "cg-caminhos--grade\|cg-caminho\[aria-current\]"` devolve zero no repositório
      (`RF-05-08`, design — decisão 6).
- [x] 1.3 Reescrever `comum/react/ListaDeCaminhos.test.tsx`: saem os casos de grade e de caminho
      corrente; ficam os cenários "A lista mantém o glifo ao lado do rótulo", "O cartão alcança
      o alvo de toque" e "O glifo não substitui o rótulo". Verificação: `vitest run
      ListaDeCaminhos` passa (specs `camada-visual-comum`).

## 2. Menu e telas de conteúdo na Área do Guerreiro(a)

- [x] 2.1 Em `AreaDoGuerreiro.tsx`, trocar o estado `bloco: Bloco` por `caminho: Caminho` com
      valor inicial `"menu"`, e passar a escolher a tela em vez da aba: havendo caminho, a tela
      do bloco; não havendo, o menu. Verificação: abrindo a sessão, nenhum conteúdo de bloco é
      renderizado (`RF-05-08`, specs `area-do-guerreiro` — "A App 05 abre no menu dos
      caminhos", design — decisão 1).
- [x] 2.2 Montar a tela de conteúdo de cada um dos quatro blocos com `Cabecalho` cujo título
      nomeia o bloco e cuja ação é **Voltar**, ligada a `definirCaminho("menu")`, sem passar
      `aoVoltar` para dentro dos blocos. Verificação: de qualquer profundidade interna, o
      Voltar devolve ao menu (`RF-05-08`, specs — "Cada caminho da área abre em tela própria,
      sem o menu", design — decisão 2).
- [x] 2.3 Reordenar os caminhos para Trilha, minha carteira, desafios e equipes, coleta do
      território, e acrescentar o quinto cartão **Sair** com glifo `encerrar` e `aoAcionar:
      sair`; retirar a ação `Sair` do `Cabecalho` do menu e a propriedade `rotulo` da
      `ListaDeCaminhos`. Verificação: o menu lista cinco cartões nessa ordem e o cabeçalho dele
      não tem ação (`RF-05-05`, `RF-05-08`, specs — "Os caminhos da Área do Guerreiro(a)
      aparecem em cartão, na ordem decidida" e "A saída da sessão é um caminho do menu, e só
      existe nele", design — decisões 3 e 4).
- [x] 2.4 Renderizar o aviso de inatividade e o botão Continuar **nos dois ramos** — menu e tela
      de conteúdo —, mantendo o efeito de inatividade onde está. Verificação: com o aviso
      disparado dentro de um bloco, ele aparece ali e Continuar não tira o Guerreiro(a) da tela
      (`RF-05-05`, `RF-05-71`, specs — "O aviso de inatividade alcança o menu e as telas de
      conteúdo", design — decisão 5).
- [x] 2.5 Manter o `useProximaMissao` e o `conteudoExtra` do cartão da Trilha intactos, agora na
      primeira posição. Verificação: o cartão nomeia posição e título da próxima missão, e
      recua ao rótulo sozinho quando não há (`RF-05-08`, `RF-05-17`, spec vigente "O cartão da
      Trilha nomeia a próxima missão").
- [x] 2.6 Reescrever `AreaDoGuerreiro.test.tsx` para o comportamento novo, cobrindo os cenários
      das specs: abre no menu sem conteúdo de bloco; o menu diz o que fazer agora; a Trilha
      acionada abre na próxima missão, alterna preservando contexto e leva à escolha do poder
      sem inscrição; o conteúdo ocupa a tela sozinho; o Voltar salta ao menu de qualquer
      profundidade; o Sair é o último cartão e não existe na tela de conteúdo; o aviso de
      inatividade aparece dentro de um bloco. Verificação: `vitest run AreaDoGuerreiro` passa
      (`RF-05-05`, `RF-05-08`, `RF-05-17`, `RF-05-71`).
- [x] 2.7 Conferir os consumidores restantes da `ListaDeCaminhos` na App 01 e retirar a
      propriedade `disposicao` se ela estiver sendo passada. Verificação: `vitest run` da App 01
      passa sem alteração de comportamento (design — Non-Goals).

## 3. Documentação da decisão

- [x] 3.1 Em `docs/15-identidade-visual.md` §6.5 — documento-fonte —, reduzir à disposição única:
      sai a tabela das duas disposições, sai o parágrafo que justifica a grade e sai o parágrafo
      final do caminho corrente e do "sem passo de menu antes do conteúdo". Verificação: o §6.5
      não menciona mais grade nem caminho corrente, e o texto ficou menor.
- [x] 3.2 Em `docs/09-topicos-em-aberto-e-sugestoes.md` §1, acrescentar a linha da decisão de
      2026-10-31 e **corrigir** a linha "Tela inicial da Área do Guerreiro(a) e o cartão de
      caminho", que hoje afirma o contrário. Verificação: as duas linhas não se contradizem.
- [x] 3.3 Em `docs/prds/prd-05-area-do-guerreiro.md`, reenunciar o `RF-05-08` na §6.2 e ajustar
      a §5.2 item 1, o bullet de desempenho da §10 e o critério de aceite da §12. Verificação: o
      PRD não manda mais a tela inicial abrir na próxima missão sem toque, e o `RF-05-08`
      continua existindo como essencial.
- [x] 3.4 Marcar a fatia 12 como implementada em `openspec/cronograma-de-fatias.md`.
      `docs/prds/index.md` não muda — a situação do PRD-05 é a mesma — e o documento 99 não
      muda, porque nenhuma relação entre documentos e nenhum invariante da §6 é tocado; não
      nasce arquivo em `docs/`, então a `nav` do `mkdocs.yml` fica como está. Verificação:
      `openspec validate --all` passa.
