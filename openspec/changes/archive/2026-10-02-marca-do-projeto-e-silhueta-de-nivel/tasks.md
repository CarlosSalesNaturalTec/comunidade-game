# Tasks

> A change não fecha recorte de `RF`: executa decisões do fundador de 2026-10-02 e corrige uma
> contradição do documento 15. Cada tarefa cita a seção que atende.
>
> O manifesto do que entregar está em `comum/marca/README.md`; os parâmetros do desenho — escudo,
> eixos do Archivo e degraus de cor — descem ao documento 15 na tarefa 1.6.

## 1. Os dez arquivos em `comum/marca/`

- [x] 1.1 Desenhar `simbolo.svg` e `favicon.svg` — escudo e monograma `CG`, nos parâmetros
      decididos —, cada um na grade `48 × 48`; o favicon com afinação óptica própria, por ser o
      que renderiza a `16` px. Verificar que cada arquivo cabe no orçamento do manifesto (3 KB e
      2 KB), não traz `<text>`, filtro nem referência externa, e nenhuma cor fora da paleta
      (documento 15 §§3.2, 11.1, princípio 4)
- [x] 1.2 Desenhar `marca-horizontal.svg` e `marca-empilhada.svg` — símbolo mais "Comunidade
      Game" em Archivo convertido em curvas, uma linha na horizontal e duas na empilhada —, na
      altura `32` e na caixa `160 × 96`. Verificar que cada um cabe em 6 KB, o que exige
      precisão de coordenada de 1 a 2 casas decimais (design — decisão 1; documento 15 §4)
- [x] 1.3 Desenhar `submarca-robroders.svg` e `submarca-robo-educa.svg` — só a palavra, com a
      acentuação, sem escudo —, na altura `32`. Verificar que cada um cabe em 5 KB e que o
      acento não ultrapassa a caixa (documento 15 §4)
- [x] 1.4 Desenhar as quatro monocromáticas — `marca-horizontal-mono`, `simbolo-mono` e as duas
      das submarcas —, **em traço**, com `currentColor` e sem declarar valor de cor algum.
      Verificar que nenhuma delas carrega atributo de cor e que cabem nos orçamentos (4, 2 e
      3 KB) (design — decisão 3; documento 15 §11.1)
- [x] 1.5 Escrever o teste da pasta: para cada um dos dez arquivos, nenhuma cor fora da paleta
      do documento 15 §3, nenhum `<text>`, nenhum `<filter>`, nenhuma URL externa e nenhum
      `<script>`; as monocromáticas sem valor de cor; e o peso dentro do orçamento do manifesto
      (`comum/marca/README.md` §7)
- [x] 1.6 Gravar no documento 15 a construção da marca — escudo, monograma, eixos do Archivo,
      degraus de cor com os contrastes medidos, a área de proteção e o tamanho mínimo declarados
      pelo fundador —, retirar do §13 as linhas de logotipo e de submarcas, e mover as duas
      pendências correspondentes do documento 09 §1 para "Já decididos". Verificar que a §13 não
      perde a linha do universo dos personagens, que segue pendente
- [x] 1.7 Corrigir o `comum/marca/README.md`: o §1 afirma que a monocromática se deriva da
      colorida trocando preenchimento por `currentColor`, o que a versão em traço desmente; e
      registrar no §4 a procedência — quem desenhou, quando e sob qual licença, citando a OFL
      1.1 do Archivo que já está em `comum/fontes/`
- [x] 1.8 Declarar `./marca` em `exports` e em `files` de `comum/package.json`; verificar que
      uma aplicação importa um arquivo da marca sem caminho relativo

## 2. O cabeçalho das oito aplicações

- [x] 2.1 Entregar `comum/react/MarcaDoProjeto.tsx` — o **símbolo** e o nome do projeto em
      texto ao lado — e montá-lo **uma vez por aplicação**: no `main.tsx` das seis em React e
      no `Vitrine.astro` da App 06. Não em `Cabecalho.tsx`, que é cabeçalho **de tela** e o
      repetiria em cada uma. Verificar que o nome continua legível quando o símbolo não
      carrega e que ele não aparece em dobro (design — decisões 2 e 7; documento 15 §§5, 6.3,
      princípio 3)
- [x] 2.2 Escrever os casos do cabeçalho, cobrindo os cenários do delta de
      `camada-visual-comum`: o cabeçalho apresenta o símbolo servido pelo próprio domínio, o
      nome sobrevive à ausência da imagem, o nome não aparece em dobro, e o modo escuro recebe a
      monocromática

## 3. O favicon das sete aplicações

- [x] 3.1 Exportar de `comum/marca/` a função que copia `favicon.svg` para o `public/` de uma
      aplicação, no molde de `comum/biometria/provisionamento.ts`, e chamá-la por plugin do Vite
      na configuração das sete — pela chave `vite` no caso da App 06, que é Astro. Verificar que
      o favicon aparece no `public/` tanto em `dev` quanto em `build` (design — decisão 5)
- [x] 3.2 Remover do versionamento os sete `apps/*/public/favicon.svg` do Vite e acrescentar ao
      teste da saída do build o caso de nível 2: o favicon servido é o do projeto, vem do arquivo
      único da camada comum e nenhuma aplicação serve mais marca de terceiro

## 4. A silhueta do badge de nível

- [x] 4.1 Trocar em `comum/react/BadgeDaFamilia.tsx` a silhueta `de_nivel` de escudo para
      **losango**, mantendo a grade de `24` px, o traço de `2` px e o glifo do poder dentro.
      Atualizar o teste da silhueta e acrescentar o caso novo do delta — nenhuma silhueta de
      badge é o escudo, que passa a ser a forma da marca (documento 15 §§8.3, 8.4)
- [x] 4.2 Trocar no documento 15 §8.3 a silhueta da família "De nível" de escudo para losango, e
      registrar em uma frase por que o escudo saiu. Verificar que as outras cinco silhuetas da
      tabela não mudaram

## 5. Fechamento

- [x] 5.1 Marcar como `implementado` a linha transversal da marca no
      `openspec/cronograma-de-fatias.md`, com o slug desta change, e ajustar a linha da fatia 11
      do PRD-03, que deixa de depender da marca e passa a depender só do elenco. A situação do
      PRD-03 em `docs/prds/index.md` não muda, e nenhum arquivo nasce em `docs/`
- [x] 5.2 Atualizar o documento 99 §§1 e 8 se a relação entre documentos mudou com as seções
      novas do documento 15; verificar que os invariantes do §6 — em especial o 23, que separa
      ponto de moeda, e o 24, que proíbe significado só por cor — continuam válidos depois da
      troca da silhueta
