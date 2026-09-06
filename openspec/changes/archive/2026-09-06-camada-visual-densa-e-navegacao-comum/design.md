## Context

`openspec/specs/camada-visual-comum/spec.md` já fixa o piso da §5 do documento 15 — alvo de
toque, foco visível, erro associado ao campo, nada só por cor — e as duas famílias servidas do
próprio domínio. O que falta é a **§6**: o temperamento Operação declara tabela em primeira
classe e a camada comum não tem tabela; e a **§4**: os marcos de largura e a grade de colunas
estão escritos no documento e não estão no token.

As oito aplicações consomem `comum/` sem construtor de estilo — CSS puro, propriedades
personalizadas, sem framework (documento 03 §1.2). O desenho abaixo se mantém nisso.

## Goals / Non-Goals

**Goals:** a densidade progressiva da Operação a partir do marco já declarado; os marcos e a
grade em token; `Tabela`, `Dialogo` e `NavegacaoDeAreas` em `comum/react`; saída da sessão uma
vez só nas Apps 03 e 09; fim das três cópias da tabela de direitos.

**Non-Goals:** o temperamento Arena; qualquer requisito de produto novo; a tela de personas,
que é fatia própria; redesenhar tela que já cumpre o piso — a adoção da navegação é a única
mudança de tela desta fatia.

## Decisions

1. **A densidade progressiva usa o marco de `768` px que o documento 15 §4 já declara.** Não
   nasce marco novo, e o piso do PRD-02 §10 — em pé, no celular — continua sendo o que
   dimensiona. Abaixo do marco, a `Tabela` mostra as colunas essenciais e rola na horizontal
   dentro do próprio contêiner; a partir dele, mostra as demais. _Descartado:_ marco próprio da
   Operação — inventaria número que o documento não tem.

2. **`Tabela` é `table` semântica, não grade de `div`.** Cabeçalho em `th` com escopo, legenda
   opcional em `caption` e rolagem horizontal **dentro** do componente, para a página nunca
   rolar de lado. _Descartado:_ lista de fichas empilhadas em toda largura — contraria a §6, que
   põe a tabela em primeira classe justamente na Operação.

3. **`Dialogo` é o elemento `dialog` nativo, aberto por `showModal`.** O navegador entrega foco
   preso, fechamento por `Esc` e camada superior sem `z-index`. O componente acrescenta o
   rótulo acessível, o fechamento explícito por botão — ícone nunca sozinho (§5) — e a devolução
   do foco ao elemento que o abriu. _Descartado:_ sobreposição em `div` com `role="dialog"` —
   reimplementaria o que o navegador já faz, com mais chance de erro de acessibilidade.

4. **`NavegacaoDeAreas` recebe as áreas e a saída, e desenha as duas em regiões separadas.** A
   área corrente é marcada por `aria-current`, e a saída fica ao fim da navegação, com rótulo
   textual. Cada aplicação continua dona da sua lista de áreas — o componente não a conhece.
   _Descartado:_ deixar a saída em cada tela e apenas estilizá-la — é o defeito relatado.

5. **A largura densa é variante da `Moldura`, não `Moldura` nova.** A de leitura, de 64
   caracteres, segue o padrão de toda tela de texto; a densa vale onde há tabela. _Descartado:_
   soltar a largura de leitura para todo mundo — perderia a §4 em tela de texto corrido.

6. **A tabela de direitos das três aplicações passa a usar `Tabela`.** É a mesma marcação em
   três arquivos; consolidá-la é o teste de que o componente serve. _Descartado:_ deixar as
   cópias e só acrescentar o componente — a duplicata permaneceria e cresceria.

## Risks / Trade-offs

- **28 telas perdem a ação "Sair" ao mesmo tempo.** Se alguma delas usava o `acao` do
  `Cabecalho` para outra coisa, o conflito aparece na compilação, não em silêncio: o teste de
  cada aplicação confere que a saída existe **uma** vez.
- **`dialog` exige `showModal`, que não existe em ambiente de teste sem polyfill.** A
  configuração de teste de `comum/` passa a provê-lo; sem isso, o teste do `Dialogo` falha por
  ambiente, não por comportamento.
