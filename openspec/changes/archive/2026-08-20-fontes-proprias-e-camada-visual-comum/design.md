## Context

Ver `proposal.md` — Why. Os requisitos estão em `specs/camada-visual-comum/spec.md` e no delta
de `specs/aplicacao-de-gestao/spec.md`.

Estado de partida: `comum/` tem um arquivo — `tokens.css`, com as três camadas do documento 15
§12 completas e corretas —, nenhum build, nenhum `tsconfig.json` e nenhum teste. A App 03 tem
três telas de marcação nua e um `index.css` que já resolve o essencial global (caixa, foco
visível, `--duracao` em `0ms`). O que está decidido e **não se reabre**: React com TypeScript
sobre Vite, `comum/` como pacote de espaço de trabalho, Biome e Vitest na esteira, temperamento
Operação, e as três camadas de token (documentos 03 §1 e 15 §§6, 12).

**Spike executado antes deste desenho**, porque a decisão 1 dependia dele: um espaço de
trabalho mínimo com `comum/react/*.tsx` sem build e uma aplicação Vite consumindo-o pelo mapa
de `exports`. Resultado medido: `vite build` transforma os módulos e emite o pacote;
`vitest run` passa; e um erro de tipo introduzido dentro de `comum/` **é apontado pelo `tsc -b`
da aplicação**, com ou sem `include` explícito da pasta. Nenhuma referência de projeto é
necessária.

## Goals / Non-Goals

**Goals:**

- Deixar o piso do documento 15 §5 cumprido **por construção**, não por disciplina de quem
  escreve cada tela.
- Fundar a camada de forma que a segunda aplicação a consuma sem reescrita.
- Manter `comum/` consumível pelo jogo, que não é React.

**Non-Goals:**

- Biblioteca de componentes com variantes além do que as três telas usam.
- Ícone em SVG: o documento 15 §5 aceita **rótulo textual** para não comunicar por cor
  sozinha, e é o que esta fatia usa. A grade de ícones do §11.1 nasce quando houver ícone
  acionável, que estas telas não têm.
- Temperamento Arena e a carta do §8.1 — sem aplicação que os peça.
- Reescrever `api/`, `ContextoDeSessao` ou o armazenamento da sessão.

## Decisions

**`comum/` continua sem build próprio; a aplicação compila a fonte.** O mapa de `exports`
aponta para `./react/indice.ts`, e o Vite de cada aplicação transforma o TypeScript. Medido no
spike acima, inclusive a checagem de tipo atravessando a fronteira do pacote. Alternativas
descartadas: build próprio com `tsup` ou Vite em modo biblioteca — passo a mais no
`npm run dev` e no CI, sem ganho; referências de projeto do TypeScript — o spike mostra que não
são necessárias.

**`comum/` ganha `tsconfig.json` e Vitest próprios mesmo assim.** Arquivo que nenhuma aplicação
importe ainda não entraria no programa de ninguém e apodreceria sem aviso. Alternativa
descartada: confiar na checagem que vem pelas aplicações — cobre só o que já é usado.

**O `@font-face` é escrito no repositório, e os quatro `.woff2` são copiados para
`comum/fontes/`.** O pacote do Fontsource **não** vira dependência. Três motivos, todos
verificados no pacote publicado: ele declara a família como `'Archivo Variable'`, e o token do
documento 15 diz `Archivo`; o CSS dele declara todos os subconjuntos — vietnamita, cirílico,
grego —, o que põe 18 arquivos na saída onde o documento 15 §4 pede latino e latino estendido;
e uma fonte que não muda não precisa de dependência de tempo de instalação. Alternativas
descartadas: importar o CSS do pacote — os três problemas acima; baixar no build — rede no CI e
no `npm run dev`, contra a independência de cada aplicação.

**A procedência das fontes fica escrita junto dos arquivos.** `comum/fontes/README.md` registra
família, versão, origem e a data da cópia, e a licença OFL de cada família acompanha os
arquivos, como ela exige. É o que permite atualizar a fonte daqui a um ano sabendo de onde ela
veio.

**Archivo entra pelo arquivo do eixo de largura** (decisão do fundador), que carrega peso
`100–900` **e** largura `62%–125%` no mesmo arquivo. Custa 88 KB contra 34 KB do arquivo só de
peso. Alternativa descartada: começar pelo eixo de peso e trocar quando a carta chegar —
reabriria o documento 15 §4 numa fatia futura.

**Os componentes são React, não folha de estilo com nomes de classe.** `aria-describedby`,
`aria-invalid` e a distinção entre `alert` e `status` são marcação; CSS não os alcança, e é
justamente onde as telas de hoje falham. Alternativa descartada: camada só de CSS — deixaria a
fiação de acessibilidade para cada aplicação repetir e errar.

**`comum/react` é entrada separada de `comum/tokens.css` e `comum/fontes.css` no mapa de
`exports`.** O jogo consome as duas primeiras e ignora a terceira, que é o quinhão que o
documento 03 §1.2 lhe reserva. Alternativa descartada: um pacote só, com React na raiz —
amarraria o jogo em Phaser a um framework que ele não usa.

**O `Campo` gera o próprio identificador e amarra rótulo, erro e estado.** Quem usa passa
rótulo, valor e erro; o componente cuida de `id`, `aria-describedby` e `aria-invalid`. É o que
torna o requisito verdadeiro por construção, e não por lembrança de quem escreve a tela.

**O `Aviso` separa o que interrompe do que informa.** Erro e recusa em `role="alert"`;
andamento em `role="status"`. Ambos levam rótulo textual que identifica a natureza do aviso sem
depender da cor.

**A largura de leitura entra como token semântico** (`--largura-de-leitura`), com o valor que o
documento 15 §4 já fixa. Nenhum valor novo é criado: o token passa a carregar um número que já
era normativo e que nenhuma camada expressava.

**O `min-height` global de `index.css` sai.** Hoje ele alcança todo `button` e todo `input` da
página, inclusive o botão que o Google Identity Services desenha por conta própria. O alvo de
toque passa a ser responsabilidade do componente, que sabe o que está dimensionando.

**`firebase.json` ganha regra de cache para os arquivos com impressão digital.** Esta é a
primeira fatia a pôr binário no `dist`, e a fonte é o pior candidato a ser rebaixada para uma
hora de cache: o nome dela já carrega o resumo do conteúdo, então a validade longa é segura e
some no dia em que o arquivo mudar. Alternativa descartada: deixar o padrão — refetch de 121 KB
de fonte a cada hora, no celular modesto que o PRD-02 §10 nomeia.

**O que o Vitest prova e o que ele não prova.** Em jsdom dá para provar a fiação: papéis,
`aria-describedby`, `aria-invalid`, a família aplicada pelo token e a supressão do movimento.
**Não** dá para provar contraste, pixel de alvo de toque nem o desenho da fonte — jsdom não
tem layout nem rasterizador. Esses três saem por conferência à mão, uma vez, registrada nas
tarefas. Não se escreve teste que passe verde sem provar o que afirma.

## Risks / Trade-offs

**Seis componentes fundados para oito aplicações a partir da evidência de três telas** → só
entra o que as três telas usam, sem variante especulativa; a sétima aplicação que precisar de
algo diferente amplia a camada com o caso na mão.

**224 KB de fonte na saída, contra o "celular modesto" do PRD-02 §10** → o `unicode-range`
reduz a 121 KB o que o aparelho em português pede, a impressão digital no nome permite cache
longo, e o texto aparece na família de reserva enquanto o arquivo não chega.

**A camada nasce sem uma segunda aplicação para exercitá-la** → é o mesmo risco que a fatia do
esqueleto assumiu, e a mitigação é a mesma: o que é da App 03 fica na pasta dela, e só sobe
para `comum/` o que já se repete.

**Erro de tipo dentro de `comum/` quebra o build de todas as aplicações que o importam** → é o
comportamento desejado, e o `tsconfig.json` próprio de `comum/` antecipa a falha antes de ela
alcançar as aplicações.

**Copiar binário para o repositório fixa a fonte numa versão** → é o preço de não depender de
terceiro em tempo de instalação; o `README.md` de `comum/fontes/` guarda a procedência para que
a atualização seja deliberada.

## Migration Plan

Nada a migrar: não há dado, rota, contrato nem armazenamento envolvido. A App 03 troca a
marcação das telas e o resultado é visual. Reversão é reverter o merge.
