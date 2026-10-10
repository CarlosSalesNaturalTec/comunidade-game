# Design

## Context

O elenco e o herói já existem e já têm spec: `camada-visual-comum` (marca) e
`aplicacao-da-vitrine` (o requisito do herói). O manifesto do que entregar está em
`comum/marca/README.md` §§3 e 8, e a regra do personagem, no documento 15 §13.6. O porquê
está em `proposal.md`.

O que esta change decide é **mecânica**: como os arquivos novos entram sem derrubar os
antigos, como a leva nova casa visualmente com a de 2026-10-09, e como o teste do manifesto
roda em Node, que não decodifica AVIF nem WebP.

Medições feitas nos arquivos de hoje, para a leva nova não sair por estimativa:

| Medida | Valor | Como se mediu |
| --- | --- | --- |
| Keyline | `#f7f5f0` (= `--cal-050`), **≈ 3 px** a 1024 de altura | varredura da borda em `susy`, `trenell` e `robo-educa` — mediana 2–3 px, média 3,3 |
| Grade | 1024 px de lado maior, altura | `ispe` do AVIF e `VP8X` do WebP |
| Peso | 34 a 51 KB | teto do manifesto: 120 KB |
| Origens novas | JPEG 848×1264 sobre magenta chapado | mesmo formato da leva anterior |
| Proporção pós-recorte | Susy ≈ 576×1024, Otávio ≈ 357×1024 | caixa da figura medida por distância de cor |

## Goals / Non-Goals

**Goals:**

- Os dois adolescentes indistinguíveis dos quatro atuais em traço, keyline e grade.
- O renome sem janela em que a árvore referencie arquivo que não existe.
- O manifesto do elenco conferido por teste, sem dependência nova.

**Non-Goals:**

- Ferramenta versionada de produção de ativo. O documento 03 §1.2 fixa as pastas de topo e
  nenhuma é de tooling; `comum/marca/` guarda ativo, não script.
- Decodificar pixel no teste. O que exige decodificador fica na conferência de entrada.
- Variante para Trenell e Robô Educa, e variante de expressão para quem quer que seja.

## Decisions

### 1. O renome antes da escrita, e `git mv` em vez de apagar e criar

`git mv susy.avif susy-crianca.avif` para os quatro arquivos, **e só então** gravar os
`susy.{avif,webp}` novos. Conteúdo inalterado no renome faz o Git registrar **rename**, e o
histórico do arquivo da criança segue inteiro. Na ordem inversa a escrita sobrescreveria a
criança antes de ela ter cópia.

_Alternativa descartada:_ sufixar o adolescente (`susy-adolescente`) — deixaria a versão
apresentada sob sufixo, contra a regra do `README.md` §3 que esta change preserva.

### 2. O pipeline de imagem roda uma vez, por Pillow, e fica registrado em prosa

Ferramenta conferida nesta sessão: Pillow 12.3.0, com `features.check('avif')` e `webp` em
`True`, e round-trip AVIF com canal alfa testado em 50 KB. Não há `cwebp` nem `avifenc` no
ambiente. Os passos — recorte do magenta por distância de cor com a franja saindo só na faixa
de borda, recorte da figura, 3% de margem, 1024 px de lado maior, keyline de 3 px em
`cal-050` — ficam no `README.md` §8, que é onde o §6 manda o caminho inteiro morar.

_Alternativa descartada:_ versionar o script. Não há pasta onde ele caiba sem inventar uma, e
o §8 em prosa já atende o caso que o §6 descreve.

### 3. O teste do manifesto lê **cabeçalho**, não pixel

`comum/marca.test.ts` roda em Vitest sobre Node, e o monorepo não tem biblioteca de imagem —
o teste de hoje lê bytes e analisa texto. O mesmo caminho serve aqui, e foi verificado nesta
sessão contra os quatro arquivos atuais:

| O quê | De onde | Conferido |
| --- | --- | --- |
| Dimensões do WebP e bit de alfa | cabeçalho `VP8X` | `570×1024`, alfa `true`, nos quatro |
| Dimensões do AVIF | caixa `ispe` | idênticas às do WebP par a par |
| Canal alfa do AVIF | marcador `auxC` | presente nos quatro |
| Par completo e peso | `readdirSync` e `statSync` | 8 arquivos, 34–51 KB |

O teste cobre então: **par AVIF/WebP completo**, **1024 px de lado maior**, **dimensões iguais
entre o par**, **canal alfa declarado** e **peso dentro do teto**.

**O que ele não cobre, e por quê:** a **cor e a espessura do keyline** e o fundo efetivamente
transparente exigem decodificar pixel. Isso fica na **conferência de entrada** — medida com
Pillow, como foi feita nesta sessão — e o resultado se registra no `README.md` §8. A spec
mantém o keyline como requisito porque ele é regra do documento 15 §13.6; o que muda é quem
confere.

_Alternativa descartada:_ `sharp` como dependência de desenvolvimento — escolha de
dependência que os documentos não decidem, e que o desenho não toma sozinho.

### 4. Provisiona-se só o que se apresenta

`provisionarElenco` segue com quatro nomes. Os pares `-crianca` ficam versionados em
`comum/marca/elenco/` e fora do `public/`: a vitrine não os mostra, e publicá-los só
engordaria o `dist/` com ~85 KB que ninguém busca. O `saidaDoBuild.test.ts` continua falando
em oito arquivos publicados.

### 5. A ordem se trava no teste que já existe

`saidaDoBuild.test.ts` assere a **sequência literal** do `srcset` do herói. É ela que impede
alguém de reordenar as figuras sem reclamação — não é preciso mecanismo novo, só atualizar a
sequência esperada e escrever no `index.css` a razão da ordem, no lugar do "do mais novo ao
mais velho", que deixa de valer.

## Risks / Trade-offs

| Risco | Mitigação |
| --- | --- |
| O keyline da leva nova destoar da anterior | 3 px a 1024 é medida, não estimativa; conferir as seis figuras lado a lado antes de gravar |
| Franja de magenta sobrando na borda do recorte | Distância de cor aplicada só na faixa de borda, como o §8 já registra para a leva anterior |
| O keyline deixar de ser conferido com o tempo, por ficar fora do automático | Fica escrito no `README.md` §8 como passo da entrada, ao lado dos outros, e não como nota solta |
| O skate alongar a silhueta de Susy e encolher a cabeça dela na normalização por altura | O skate vai da mão ao chão, dentro da altura da figura; conferir na montagem do herói, que é onde apareceria |
| Alguém reordenar o herói e quebrar o gesto do Trenell | A razão vai no comentário do `index.css` e no requisito da spec; o teste da saída trava a sequência |

## Migration Plan

Não há migração de dado nem de rota. A ordem das tarefas é que importa: **renomear → gravar
os novos → atualizar `provisionamento.ts`, `Heroi.tsx` e os testes**. Em nenhum ponto entre
duas tarefas a árvore referencia arquivo inexistente, porque os quatro nomes base nunca
deixam de existir. Reversão é `git revert` da change inteira.
