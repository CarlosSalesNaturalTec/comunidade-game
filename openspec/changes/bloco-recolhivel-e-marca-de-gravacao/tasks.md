## 1. `comum/react` — os dois componentes

- [ ] 1.1 `BlocoRecolhivel.tsx`: sobre `details`/`summary` nativo, nasce fechado a cada
      montagem, recebe título e resumo de quem o monta e apresenta o resumo na linha fechada;
      marcador nativo suprimido em favor de rótulo textual que diz o estado; sem animação de
      altura (documento 15 §6.1, design — decisões 1, 2 e 3).
- [ ] 1.2 `MarcaDeGravacao.tsx`: apresentação pura que recebe o instante da última gravação e o
      formata em texto persistente; instante nulo não apresenta marca; sem cor como portadora
      de sentido e sem movimento (documento 15 §6.2, design — decisões 4 e 5).
- [ ] 1.3 `estilos.css` recebe o estilo dos dois, na camada semântica e de tema dos tokens, e
      `indice.ts` os exporta (documento 15 §12).

## 2. Área do Mestre — a tela da trilha recolhe

- [ ] 2.1 `ListaDeMissoes.tsx`: os dez blocos por missão passam a `BlocoRecolhivel`, cada um
      com o resumo do seu estado — quantos itens guarda, ou que não guarda nenhum. A linha da
      missão (posição, título, sondagem, etapa, obrigatoriedade) e a ação "Pré-visualizar
      missão" ficam fora do recolhimento (documento 15 §6.1, design — decisão 6).
- [ ] 2.2 `TelaDaTrilha.tsx`: etiquetas ODS da trilha, cobertura de ODS e culminância passam a
      `BlocoRecolhivel`, com o resumo de cada uma; cabeçalho, publicação e "Nova missão"
      permanecem sempre visíveis (documento 15 §6.1, design — decisão 6).
- [ ] 2.3 Os componentes de bloco que hoje trazem título próprio — `EtiquetasOds`,
      `Bibliografia`, `TemplateDaMissao`, `DeclaracaoDeRecompensa`, `DesafioDeDesbloqueio` —
      deixam de montar o seu `h3`/`h4`, que passa a ser o título do bloco recolhível, para a
      tela não ter dois títulos por bloco (design — decisão 2).

## 3. Área do Mestre — as escritas declaram que gravaram

- [ ] 3.1 As cinco escritas que acontecem no próprio bloco — cadência de retomada, desafio de
      desbloqueio, etiquetas ODS da trilha, etiquetas ODS da missão e recompensa de marco —
      guardam o instante do retorno sem erro e montam `MarcaDeGravacao` (documento 15 §6.2,
      design — decisão 5).
- [ ] 3.2 As seis escritas em formulário que fecha ao gravar — atividade, conteúdo,
      bibliografia, desafio de coleta, culminância e missão — devolvem o instante pelo mesmo
      `onSalvo` que já leva o dado, e o bloco que permanece o guarda e apresenta a marca
      (documento 15 §6.2, design — decisão 5).
- [ ] 3.3 Escrita recusada ou falha não produz marca: conferir que o instante só é registrado
      no caminho de sucesso, e que a recusa segue aparecendo como já aparece (documento 15
      §6.2).
- [ ] 3.4 `TemplateDaMissao.tsx`: o campo "O que você quer ensinar nesta missão?" ganha, em uma
      linha, a nota de que o tópico não é guardado — só o que o Mestre aceitar vira registro
      (`RN-09-33`).

## 4. Testes

- [ ] 4.1 `comum/react/BlocoRecolhivel.test.tsx`: nasce fechado com o resumo na linha; o
      conteúdo não é alcançável antes de abrir; abrir e fechar pelo controle; bloco vazio diz
      que não há nenhum; o controle é anunciado com rótulo textual e com o estado — os quatro
      cenários do requisito do bloco recolhível.
- [ ] 4.2 `comum/react/MarcaDeGravacao.test.tsx`: instante nulo não apresenta marca; instante
      presente apresenta o momento em texto; instante novo substitui o anterior — os cenários
      do requisito da marca de gravação que não dependem da tela.
- [ ] 4.3 `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`: os testes da tela passam a abrir o
      bloco antes de agir, como o usuário faz; acrescentar que a escrita bem-sucedida deixa a
      marca no bloco e que a recusada não deixa — os cenários "bloco grava e declara a
      gravação" e "a escrita que falha não deixa marca".

## 5. Documentação

- [ ] 5.1 Marcar a fatia transversal como implementada em `openspec/cronograma-de-fatias.md`,
      com o slug da change. Nada mais muda em `docs/`: as duas decisões já foram gravadas no
      documento 15 §§6.1 e 6.2, no documento 09 §1 e no documento 99, e a fatia não cria
      requisito, não muda a situação de PRD nenhum e não cria arquivo novo.
