# Tasks

## 1. O cartão de caminho na camada comum

- [ ] 1.1 Criar `comum/react/ListaDeCaminhos.tsx` com `disposicao: "coluna" | "grade"`,
      `caminhoAtual` opcional e um caminho por item (chave, rótulo em frase, glifo, conteúdo
      extra opcional); o cartão corrente recebe `aria-current="true"` e nenhum cartão o recebe
      sem `caminhoAtual` declarado. Exportar em `comum/react/indice.ts` (`RF-05-08`, design —
      decisões 1 e 4)
- [ ] 1.2 Mover `.cg-caminhos` e `.cg-caminho` de `apps/app-01-aula-presencial/src/index.css`
      para `comum/react/estilos.css` **com os mesmos valores e tokens**, acrescentando o
      modificador de grade — `repeat(2, minmax(0, 1fr))` e, em `@media (min-width: 768px)`,
      `grid-auto-flow: column` — e o glifo acima do rótulo na grade. Deixar
      `cg-caminhos__operacao` e `cg-caminhos__grupo` na App 01, e corrigir ali o comentário que
      afirma "nunca acima" (design — decisões 2, 3 e 7)
- [ ] 1.3 Acrescentar ao `comum/react/Icone.tsx` os glifos `carteira`, `desafios` e `coleta`, na
      grade de `24` px com traço de `2` px e `currentColor`, sem preenchimento e sem repetir
      silhueta de família de badge, escudo da marca, círculo da moeda ou estrela da grandeza
      ponto — a carteira **sem moeda dentro** (design — decisão 6)
- [ ] 1.4 Cobrir em `comum/react/` os cenários dos três requisitos do delta de
      `camada-visual-comum`: a grade em duas colunas e o glifo acima, a coluna com o glifo ao
      lado, o alvo de toque, o rótulo que o glifo não substitui, o caminho corrente anunciado
      sem depender de cor e a ausência de corrente sem `caminhoAtual`; e, no teste do `Icone`,
      que os três glifos novos existem e não declaram cor

## 2. A App 01 passa a consumir o componente

- [ ] 2.1 Trocar os `<button className="cg-caminho">` de
      `apps/app-01-aula-presencial/src/inicio/TelaInicial.tsx` pelo `ListaDeCaminhos` em
      `disposicao="coluna"`, preservando rótulos, glifos, ordem, estado desabilitado e o
      `fieldset` "para quem opera o aparelho" com os caminhos dele (design — decisão 1,
      Non-Goals)
- [ ] 2.2 Conferir em `apps/app-01-aula-presencial/src/inicio/inicio.test.tsx` que rótulo, ordem
      e glifo de cada caminho seguem iguais, que o grupo de operação continua declarado por
      `fieldset`/`legend` e que a disposição é a coluna — a App 01 não muda de aparência
      (`RF-04-01`, `RF-04-71`, Risks)

## 3. A tela inicial da Área do Guerreiro(a)

- [ ] 3.1 Em `apps/app-05-guerreiro/src/entrada/AreaDoGuerreiro.tsx`, trocar o bloco padrão de
      `"coleta"` para `"trilha"` (`RF-05-08`)
- [ ] 3.2 Trocar a `nav` de `Botao` pelo `ListaDeCaminhos` em `disposicao="grade"`, com
      `caminhoAtual` no bloco aberto e a ordem minha carteira, Trilha, desafios e equipes, coleta
      do território; remover `cg-area-do-guerreiro__blocos` do `index.css` da App 05, que nunca
      teve regra (`RF-05-08`, design — decisões 3 e 4)
- [ ] 3.3 Compor o rótulo do cartão da Trilha com a próxima missão vinda de
      `listarMinhasTrilhas` — posição e título da **primeira** trilha da lista —, caindo para o
      rótulo sozinho quando a leitura falhar ou não houver próxima missão (`RF-05-08`,
      `RF-05-17`, design — decisão 5)
- [ ] 3.4 Cobrir em `apps/app-05-guerreiro/src/entrada/AreaDoGuerreiro.test.tsx` os cenários do
      delta de `area-do-guerreiro`: a sessão aberta cai no bloco da trilha sem acionar caminho
      algum, a ordem dos quatro cartões, o glifo junto do rótulo, o cartão do bloco aberto
      anunciado como atual, trocar de bloco sem tela intermediária, a próxima missão nomeada no
      cartão e o recuo ao rótulo sozinho sem próxima missão ou com leitura falhada
- [ ] 3.5 Conferir que o temporizador de inatividade, o aviso de um minuto e o Sair no
      `Cabecalho` seguem intactos — a tela inicial não é tela nova de sessão, e a saída não muda
      de lugar (design — Non-Goals, decisão 4)

## 4. Documentação

- [ ] 4.1 Marcar a fatia 11 do bloco PRD-05 de `openspec/cronograma-de-fatias.md` como
      implementada. Em `docs/` nada muda: a fatia não toma decisão nova de produto — aplica o
      `RF-05-08` já escrito —, não altera requisito do PRD-05, não mexe na relação entre
      documentos nem cria arquivo, e a situação do PRD-05 em `docs/prds/index.md` não muda
