# Design

## Context

Ver `proposal.md` — Why. O padrão da tela já está consolidado: `comum/trilha/Missao.tsx`
monta o conteúdo em `SequenciaPaginada` (`comum/react`) e, abaixo dela, o ato da missão. O
`GuiaDaTrilha` é quem busca a trilha publicada e compõe os quatro grupos (fatia 27).

Duas restrições do código de hoje moldam o desenho:

1. **`Missao` não sabe em que conteúdo está.** O índice vive dentro do `SequenciaPaginada`.
2. **O índice é zerado pela `key={missaoPublica.id}`** do paginador. `Missao` **não** remonta
   quando a missão avança — só o paginador remonta, pela `key`.

A favor: a sequência do conteúdo é **de mão única**. `Missao` não passa `rotuloDeVoltar`, de
propósito ("o conteúdo da missão não tem o que corrigir"), então alcançar o último conteúdo é
**monotônico** — o ato aparece uma vez e não pisca nem some.

## Goals / Non-Goals

**Goals:**

- Condicionar o ato ao último conteúdo sem alterar a navegação dos conteúdos.
- Preservar **exatamente** a semântica de reset de hoje: missão nova começa no conteúdo 1.
- Manter `comum/react` intocado, para não alcançar o quiz do desbloqueio nem a programação.

**Non-Goals:**

- Qualquer mudança no `SequenciaPaginada`, inclusive propriedade nova.
- Estado "concluído", "Rever conteúdo" e ocultar conteúdo já visto — fora do escopo.
- Gatilhar a entrega da produção da App 05, que é de outro estado da missão.

## Decisions

### 1. O índice sobe para um componente filho com `key`, não para a `Missao`

O ato e o conteúdo passam a ser montados por um filho de `Missao`, com
`key={missaoPublica.id}`, que guarda o índice em `useState` e o comanda no paginador por
`indice`/`aoIrPara`.

**Por quê:** é o que preserva o reset. Um `useState` solto em `Missao` sobreviveria à troca de
missão — `Missao` não remonta — e a missão nova abriria no índice da anterior (clampado pelo
paginador), **com o ato liberado de cara**. Passar a `key` ao filho move a fronteira de
remontagem para onde o estado agora mora.

- _Alternativa descartada:_ `useEffect` que zera o índice ao mudar `missaoPublica.id` — um
  render a mais com o índice velho, e é justamente nesse render que o ato apareceria.
- _Alternativa descartada:_ `key` na própria `Missao`, posta pelo `GuiaDaTrilha` — remontaria
  também o aviso de missão opcional e o de `aguardando_mestre`, que não têm por que piscar.

### 2. `comum/react/SequenciaPaginada.tsx` não é tocado

O paginador **já** aceita índice comandado de fora, e o `DesafioDeDesbloqueio` já usa esse
par nas perguntas do quiz. Não há propriedade nova a criar.

**Por quê:** o paginador é compartilhado com o quiz do desbloqueio e com o conteúdo do dia da
programação (`TelaDaProgramacao.tsx`). Mexer nele para um gate que é da missão espalharia o
risco por três telas que não mudam de comportamento.

### 3. O gate é um predicado derivado, não estado próprio

Com a lista de conteúdos ordenada e o índice da vez, o gate é:

```text
conteúdo ainda sendo buscado  ──▶  fechado
busca falhou                  ──▶  ABERTO   (decisão 4)
lista vazia                   ──▶  ABERTO
caso contrário                ──▶  indice === lista.length - 1
```

**Por quê:** não há estado a sincronizar nem a invalidar, e a lista vazia cai naturalmente no
mesmo predicado sem caso especial espalhado. Deriva de um lugar só.

- _Alternativa descartada:_ um booleano `viuTudo` acumulado — exigiria reset próprio, o mesmo
  problema que a decisão 1 resolve, e a mão única torna o acúmulo desnecessário.

### 4. Conteúdo que falha abre o gate; conteúdo carregando o mantém fechado

Decisão do fundador de 2026-10-16. O gate existe para garantir que o conteúdo foi percorrido;
conteúdo que não pode ser servido não tem o que guardar, e mantê-lo fechado deixaria a missão
sem saída — o ato é justamente o caminho adiante. Carregando, fica fechado para o ato não
aparecer e sumir quando a lista chega.

### 5. A entrega da produção fica fora do gate

Ela é renderizada sob `missao.desbloqueada`; o ato, sob `missao.e_proxima`. São estados
distintos da missão, e gatilhá-la seria decisão nova — levada ao fundador e descartada.

## Risks / Trade-offs

- **Regressão no reset do índice** → é o risco central. Cenário dedicado: desbloquear a missão
  e conferir que a seguinte abre no conteúdo 1 com o ato oculto.
- **O ato some de telas que hoje o têm, em rede ruim** → mitigado pela decisão 4: só fica
  oculto enquanto carrega, nunca na falha.
- **A App 05 muda sem ter sido pedida** → é o precedente das fatias 22, 27 e 28, e é
  deliberado: a mesma criança não pode ver telas diferentes na aula e em casa.
- **Teste existente que assuma o ato visível no primeiro conteúdo** → conferir
  `comum/trilha/trilha.test.tsx` e ajustar o arranjo, nunca a asserção do gate.
