# Design

## Context

Ver `proposal.md` — Why. As specs alteradas são `camada-visual-comum`, que já declara a camada de
tema da Operação e a densidade progressiva dela, e `aplicacao-da-aula-presencial`, no requisito da
tela inicial.

O documento 15 §6 é a fonte do temperamento e o §11.1 a do sistema de ícone; nenhum dos dois
precisa de decisão nova. O que esta fatia decide é **onde** a camada de tema da Arena mora, **como**
o glifo é servido e **o que fica de fora** por falta de norma numérica.

## Goals / Non-Goals

**Goals:**

- A camada de tema da Arena existe, com os valores que o documento 15 fixa.
- As Apps 01 e 05 declaram o temperamento que o documento 15 lhes atribui.
- O sistema de ícone do §11.1 existe na camada comum e aparece nos caminhos da App 01.

**Non-Goals:**

- Carta, ilustração em primeiro plano e imagem de comunidade ao fundo.
- Retorno de progresso e conquista.
- Glifo fora dos caminhos da tela inicial da App 01.
- Qualquer alteração de paleta: o invariante 24 veda mudar marca e paleta por temperamento.

## Decisions

1. **A Arena entra como terceira camada de `comum/tokens.css`, ao lado da Operação.** O arquivo já
   declara as três camadas do documento 15 §12 — primitiva, semântica e tema — e a de tema já tem
   um seletor por temperamento. _Descartado:_ folha própria por temperamento, que faria cada
   aplicação escolher o que importar e abriria a porta para uma importar as duas.

2. **A Arena declara `--raio-carta` e `--duracao`, e não declara `--densidade`.** São os dois
   valores que o documento 15 §6 fixa em número para a Arena. A densidade da Arena é descrita como
   composição — "poucos elementos, uma decisão por tela" —, sem número, e o token é lido somente
   pelas nove folhas densas da App 03. Declarar um valor aqui seria criar regra num artefato, o que
   o `config.yaml` veda. _Registrado como pendência no documento 09_, para o fundador fixar quando
   a primeira tela da Arena precisar do token.

3. **O glifo é SVG embutido em componente React, não arquivo buscado por `<img src>`.** O §11.1
   exige `currentColor`, e uma imagem externa não herda cor do texto; embutido, o SVG é servido
   pelo próprio domínio junto do pacote da aplicação, o que o princípio 6 pede. É também o que
   dispensa requisição e cabeçalho — o mesmo problema que `MidiaDoNucleo` resolve para mídia do
   núcleo, aqui inexistente porque o glifo é do projeto. _Descartado:_ sprite SVG único com
   `<use>`, que reintroduz uma requisição e não ganha nada em seis glifos.

4. **O glifo entra ao lado do rótulo dos caminhos, nunca no lugar dele.** O documento 15 §5 não
   abre exceção: ícone acionável leva rótulo. Os caminhos já são frases inteiras — "Presença —
   entrar com o nick e registrar a presença de hoje" —, e o glifo é o que a criança reconhece antes
   de ler a frase. O glifo é decorativo para a tecnologia assistiva, que anuncia o rótulo.

5. **Nada muda de raio nos botões e nos caminhos.** `.cg-caminho` usa `--raio-campo`, e o `12` px
   do documento 15 §6 é da **carta** do §8.1, que o caminho não é. Aumentar o raio do caminho
   porque "parece carta" seria inventar aplicação para um número normativo.

6. **A declaração do temperamento fica no `index.html`, onde já está.** As seis aplicações já
   declaram `data-temperamento` na raiz do documento, que é o que o `tokens.css` seleciona; a
   correção é de valor, não de lugar.

## Risks / Trade-offs

- **A change parece maior do que é, visualmente.** Corrigir a declaração não muda nada na tela
  hoje: `--densidade` só é lido pela App 03 e `--raio-carta` não tem consumidor. O que aparece é o
  glifo. Fica declarado na `proposal` para a expectativa não se formar errada — e é o que torna a
  fatia da carta e a do retorno de conquista honestas quando vierem.
- **Traço dos seis glifos divergindo do que o fundador espera** → os conceitos estão na tabela da
  `proposal`; o desenho de cada um é conferido no aparelho do encontro antes de a fatia fechar.
- **Regressão de contraste no glifo** → `currentColor` herda a cor do texto, que já cumpre os
  `4,5:1` medidos do documento 15 §3.3; nenhum glifo declara cor própria, e o teste afirma isso.
