# 15 — Identidade Visual das Aplicações

Define o sistema visual das oito aplicações: paleta, tipografia, medida, acessibilidade, avatar,
carta do personagem, emblemas, ícone, gráfico de série e as fichas de ponto e moeda.

> Este documento define **como as aplicações se parecem**. **O que cada card mostra e como o
> território cresce visualmente** continua no documento 11.

## 1. Princípios

1. **Estética de território, não corporativa** — grafite, cor chapada, imagem de comunidade.
2. **O visual representa dado real, nunca decoração** — nada na tela enfeita sem informar.
3. **A cor nunca carrega significado sozinha** — sempre com glifo, forma, numeral ou rótulo.
4. **O celular modesto é o alvo, não o caso extremo** — peso de arquivo é requisito de projeto.
5. **Uma identidade só** — as oito aplicações se reconhecem entre si; muda o temperamento (§6),
   nunca a marca nem a paleta.
6. **Fonte, ícone e ilustração são servidos pelo próprio domínio** — nenhuma requisição a
   terceiro, porque a vitrine não admite rastreador algum.

## 2. As quatro referências e o que cada uma aporta

| Referência            | Papel no sistema                                                                                                   | O que não se aproveita                                          |
| --------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| **Gorillaz**          | Base ilustrativa: personagem no lugar da pessoa real, traço de tinta, contorno grosso, cor chapada, colagem urbana | Estética adulta e noturna; nada impróprio para 6 anos           |
| **Clash Royale**      | Átomo de interface: a carta como unidade, hierarquia legível a um metro, botão grande e tátil, retrato             | Loja, baú, moeda comprável e urgência fabricada — todas vedadas |
| **League of Legends** | Progressão: emblema em degraus contáveis, moldura que diz o quanto se avançou, ficha com atributos visíveis        | Ornamento medieval pesado, que custa banda e trai o território  |
| **Atari River Raid**  | Sotaque: pixel art de paleta mínima e peso quase zero, código simples de ler e alterar                             | Pixel em texto corrido, ilegível em tela pequena                |

O traço do Gorillaz é a **base**; a carta é o **átomo**; o emblema é a **progressão**; o pixel é
**sotaque**, restrito aos sprites do App 04 e a micro-recompensas — nunca a texto.

## 3. Paleta

Cor chapada, sem gradiente. Toda razão de contraste abaixo é medida e vale para o fundo de
apoio da própria coluna.

### 3.1 Neutros

| Token       | Valor     | Uso                                                |
| ----------- | --------- | -------------------------------------------------- |
| `tinta-900` | `#10141F` | Texto principal no claro; fundo no escuro          |
| `tinta-800` | `#1C2333` | Superfície de carta no escuro                      |
| `tinta-700` | `#2E3850` | Texto secundário no claro                          |
| `tinta-500` | `#5C6885` | Texto de apoio; **borda que informa**              |
| `tinta-300` | `#A8B2C6` | Texto de apoio no escuro                           |
| `tinta-200` | `#CFD6E3` | Separador decorativo — nunca sinal único           |
| `tinta-100` | `#E7EBF2` | Fundo de campo desabilitado                        |
| `cal-050`   | `#F7F5F0` | Fundo no claro — parede caiada, não branco clínico |
| `cal-000`   | `#FFFFFF` | Superfície de carta no claro                       |

### 3.2 Marca, ação e estados

| Família                        | 700       | 600       | 500       | 400       | 100       |
| ------------------------------ | --------- | --------- | --------- | --------- | --------- |
| **Marca** — laranja território | `#B33C00` | `#C94800` | `#F25C05` | `#FF7A2E` | `#FFE3D1` |
| **Ação** — azul azulejo        | `#123E8A` | `#1750AE` | `#1D63D1` | `#5B93EA` | `#DCE8FB` |
| **Ponto** do Guerreiro(a)      | `#7A5500` | `#996B00` | `#F2B705` | `#FFCE3D` | `#FFF1CC` |
| **Moeda** do Apoiador          | `#0B5D57` | `#0E7A72` | `#12A093` | `#3FC7B9` | `#D3F1EE` |
| **Sucesso**                    | —         | `#1B7A3D` | —         | `#4ECB80` | —         |
| **Atenção**                    | —         | `#8A5A00` | —         | `#E8A93B` | —         |
| **Erro**                       | —         | `#C02626` | —         | `#F27A7A` | —         |

**Regra de uso por modo:** o claro usa o degrau 600 ou 700 para texto e preenchimento; o escuro
usa o 400. O degrau 500 é a cor de identidade da família — usada em preenchimento **com
contorno no degrau 700**, nunca sozinha contra o fundo.

### 3.3 Contraste medido

| Par                                    | Razão   | Piso  |
| -------------------------------------- | ------- | ----- |
| `tinta-900` sobre `cal-050`            | 16,88:1 | 4,5:1 |
| `tinta-500` sobre `cal-050`            | 5,11:1  | 4,5:1 |
| `acao-600` sobre `cal-050`             | 6,90:1  | 4,5:1 |
| `cal-000` sobre `acao-600`             | 7,51:1  | 4,5:1 |
| `cal-000` sobre `marca-600`            | 4,76:1  | 4,5:1 |
| `tinta-900` sobre `ponto-500`          | 10,12:1 | 4,5:1 |
| `cal-000` sobre `moeda-600`            | 5,19:1  | 4,5:1 |
| `cal-050` sobre `tinta-900`            | 16,88:1 | 4,5:1 |
| `acao-400` sobre `tinta-900`           | 5,96:1  | 4,5:1 |
| `tinta-500` sobre `cal-050` (borda)    | 5,11:1  | 3:1   |
| `ponto-700` sobre `cal-050` (contorno) | 6,16:1  | 3:1   |
| `moeda-700` sobre `cal-050` (contorno) | 7,09:1  | 3:1   |
| `tinta-500` sobre `tinta-900` (borda)  | 3,30:1  | 3:1   |

## 4. Tipografia e medida

| Papel        | Família                        | Por quê                                                                      |
| ------------ | ------------------------------ | ---------------------------------------------------------------------------- |
| **Texto**    | **Atkinson Hyperlegible Next** | Desenhada para baixa visão; separa `l` de `I` e `O` de `0`; licença livre    |
| **Destaque** | **Archivo**                    | Variável, com eixo de largura, para título e numeral de carta; licença livre |

Duas famílias no máximo, variáveis, **subconjunto latino e latino estendido**, servidas pelo
próprio domínio. O App 04 usa as mesmas: o pixel fica nos sprites, nunca no texto.

| Medida                  | Valor                                                                              |
| ----------------------- | ---------------------------------------------------------------------------------- |
| Escala tipográfica      | `0,75 · 0,875 · 1 · 1,125 · 1,375 · 1,75 · 2,25` rem                               |
| Corpo mínimo de leitura | `1` rem (16 px); nunca abaixo em texto lido por criança                            |
| Entrelinha              | `1,5` em texto corrido; `1,2` em título                                            |
| Pesos                   | `400` corpo · `500` rótulo · `600` título · `700` numeral de carta                 |
| Escala de espaçamento   | `4 · 8 · 12 · 16 · 24 · 32 · 48 · 64` px                                           |
| Alvo de toque           | **≥ 48 px**, com ao menos 8 px entre alvos vizinhos                                |
| Raio                    | `4` (campo) · `12` (carta) · `999` (ficha e pastilha)                              |
| Largura de leitura      | Máximo `64` caracteres por linha                                                   |
| Marcos de largura       | `768` · `1024` · `1280` px — o celular é o padrão, e não tem marco                 |
| Colunas                 | `4` no celular · `8` a partir de 768 · `12` a partir de 1024, com calha de `16` px |

## 5. Acessibilidade

**Piso declarado: WCAG 2.2, nível AA.** Aplica-se às oito aplicações.

- Contraste de **4,5:1** em texto e **3:1** em componente, borda que informa e estado de foco.
- **Alvo de toque de 48 px** — dedo de criança em tela pequena é a régua.
- **Nenhum significado por cor sozinha**: sempre glifo, forma, numeral ou rótulo junto.
- **Foco sempre visível**, com contorno de 2 px em `marca-500` no claro e `marca-400` no escuro.
- **`prefers-reduced-motion` respeitado** — sem exceção, inclusive na rotação dos cards.
- **Conteúdo legível sem depender de movimento**: quem não vê a rotação acessa o mesmo conteúdo.
- **Ícone nunca sozinho**: todo ícone acionável leva rótulo textual visível ou acessível.
- **Sem CAPTCHA**, que é barreira de acessibilidade.

## 6. Os dois temperamentos

Um sistema, dois modos de aplicação. Ambos consomem os mesmos tokens de cor e tipografia: o que
muda é densidade, raio, peso e presença de ilustração.

| Eixo                | **Operação** — Apps 03, 07, 08 e 09                                                                             | **Arena** — Apps 01, 04, 05 e 06                                  |
| ------------------- | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Densidade           | Alta: tabela, lote e painel do dia em primeira classe                                                           | Baixa: poucos elementos, uma decisão por tela                     |
| Ilustração          | Só onde é dado — avatar, carta, território                                                                      | Em primeiro plano; a carta domina a tela                          |
| Cor                 | Neutro dominante; cor reservada a ação e estado                                                                 | Cor chapada e imagem de comunidade ao fundo                       |
| Raio de carta       | `4` px                                                                                                          | `12` px                                                           |
| Movimento           | Nenhum decorativo; `200` ms                                                                                     | Retorno de progresso e conquista; `300` ms                        |
| Caso que dimensiona | Operado em pé, no celular, entre as bancadas; e o uso raro, que precisa ser entendido sem aprendizado acumulado | Criança de 6 anos, em aparelho compartilhado, podendo não digitar |

Toda transição usa `ease-in-out`, e o temperamento é da aplicação inteira: a App 06 é Arena do
cabeçalho ao rodapé, inclusive no painel do território e nos rankings.

O Apoiador precisa reconhecer, na App 08, o mesmo jogo que o filho joga na App 05 — é por isso
que os temperamentos não separam marca nem paleta.

## 7. Avatar do Guerreiro(a)

O avatar é o **único retrato público** do Guerreiro(a), e no onboarding ele nasce de
características ditas em voz alta por uma criança de 6 anos. Daí as quatro exigências:

1. **Paramétrico, em camadas SVG**, montado de catálogo fechado.
2. **Cada traço tem nome dizível em português simples** — "cabelo black power", não "modelo 7".
3. **Composto no próprio aparelho**, sem rede — o App 04 joga com o catálogo guardado.
4. **Sem marca de gênero no traço**: a forma de tratamento é campo próprio, e todo item do
   catálogo é livre para qualquer pessoa.

### 7.1 Camadas, na ordem de composição

| #   | Camada        | O que varia                                                                                |
| --- | ------------- | ------------------------------------------------------------------------------------------ |
| 1   | Fundo         | Cor chapada da paleta                                                                      |
| 2   | Tom de pele   | Escala de oito degraus, **aberta pelo mais retinto**                                       |
| 3   | Cabelo        | Black power, crespo curto, tranças, dreads, cacheado, ondulado, liso, raspado, coque, rabo |
| 4   | Cor do cabelo | Escala própria, incluindo cor fantasia                                                     |
| 5   | Rosto         | Formato                                                                                    |
| 6   | Olhos         | Formato e cor                                                                              |
| 7   | Boca          | Formato                                                                                    |
| 8   | Roupa         | Camisa, regata, jaqueta, moletom, camisa do projeto                                        |
| 9   | Acessório     | Óculos, boné, tiara, fone, lenço, ou nenhum                                                |

**A representatividade é construção, não opção.** A escala de tons de pele abre pelo mais
retinto e a variedade de texturas de cabelo crespo vem antes da lisa — é a causa antirracista
do projeto virando mecânica, e não declaração.

### 7.2 Forma do valor

O núcleo guarda o avatar como texto opaco. A forma acordada é um objeto pequeno e versionado:

```json
{
  "v": 1,
  "fundo": "marca-100",
  "tom": "t2",
  "cabelo": "black-power",
  "cabelo_cor": "c1",
  "rosto": "r3",
  "olhos": "o2",
  "boca": "b1",
  "roupa": "camisa-projeto",
  "acessorio": "nenhum"
}
```

Traço desconhecido cai no padrão da camada, e nunca quebra a renderização — é o que permite
crescer o catálogo sem migrar avatar de ninguém.

### 7.3 Avatar padrão do projeto

Mesmo sistema, composição fixa e neutra, em cores da marca. É o que o card do Apoiador exibe
abaixo do piso de moedas, e o que ocupa o lugar de qualquer avatar que falte.

## 8. Carta, emblemas e badges

### 8.1 A carta é o componente comum às oito aplicações

A carta do personagem é o átomo da interface, nas quatro variantes já normatizadas —
Guerreiro(a), Mestre, Apoiador e Comunidade Virtual. **A composição de cada uma — o que exibe,
o que nunca exibe e a moldura comum — está no documento 11.** Aqui ficam só os valores:

| Elemento            | Valor                                                                    |
| ------------------- | ------------------------------------------------------------------------ |
| Superfície          | `cal-000` no claro, `tinta-800` no escuro                                |
| Borda               | `tinta-500`, 1 px                                                        |
| Raio                | `4` px na Operação, `12` px na Arena                                     |
| Proporção do avatar | Quadrado, recortado em círculo, ocupando metade da largura da carta      |
| Nick                | Archivo, `1,125` rem                                                     |
| Rotação             | Onde houver, respeita `reduced-motion` e nunca é a única via ao conteúdo |

### 8.2 Emblema de nível — a marca é contável

O nível de uma trilha ou poder aparece como **número de marcas na moldura, igual ao nível**: um
traço no nível 1, cinco no nível 5. Contável por uma criança de 6 anos, e legível sem cor.

| Nível | Moldura                                              |
| ----- | ---------------------------------------------------- |
| 1     | Uma marca                                            |
| 2     | Duas marcas                                          |
| 3     | Três marcas                                          |
| 4     | Quatro marcas                                        |
| 5     | Cinco marcas e moldura fechada — **Mestre Aprendiz** |

O emblema é sempre de uma trilha ou poder, nunca global — a moldura carrega o nome do poder.

### 8.3 Badges — uma silhueta por família

Cada família do documento 11 tem **forma própria**, legível a 24 px, para que a leitura não
dependa de cor:

| Família             | Silhueta                |
| ------------------- | ----------------------- |
| De nível            | Escudo                  |
| De conquista        | Estrela                 |
| De valores e causas | Coração                 |
| De território       | Gota                    |
| De autoria          | Folha com canto dobrado |
| De protagonismo     | Hexágono                |

### 8.4 Glifo de poder

A silhueta diz a **família** do badge, não o poder: dois badges de nível são ambos escudo. O que
os separa é o **glifo do poder**, desenhado no sistema de ícone da §11.

| Regra        | Valor                                                                             |
| ------------ | --------------------------------------------------------------------------------- |
| Onde aparece | Dentro da silhueta do badge, na moldura de nível e na seção de poderes da vitrine |
| Legibilidade | Reconhecível a `24` px, em traço, sem depender de cor                             |
| Cobertura    | Um por poder do catálogo; poder sem glifo cai no genérico e nunca quebra a tela   |
| Rótulo       | O glifo acompanha o nome do poder, nunca o substitui                              |

O poder **não tem cor própria**: cor é da grandeza (§9) e do estado, e distribuí-la pelo
catálogo inteiro gastaria a paleta e furaria o piso de contraste.

## 9. Ponto, ponto extra e moeda

São três grandezas distintas e **nunca podem ser confundidas na tela**:

| Grandeza          | Glifo            | Ficha           | Cor         | Rótulo          |
| ----------------- | ---------------- | --------------- | ----------- | --------------- |
| **Ponto regular** | Estrela cheia    | Pastilha cheia  | `ponto-500` | "pontos"        |
| **Ponto extra**   | Estrela vazada   | Pastilha vazada | `ponto-500` | "pontos extras" |
| **Moeda**         | Círculo de moeda | Ficha circular  | `moeda-500` | "moedas"        |

- Toda ficha leva **contorno no degrau 700** da sua família, para ter limite discernível.
- Do ponto extra, a superfície pública mostra o **acumulado**; a tela de troca mostra o **saldo
  disponível**, e os dois nunca aparecem sem rótulo que os separe.
- **Real não aparece** fora da tela onde se paga, e ali sempre ao lado do equivalente em moedas.

## 10. Etiqueta de conteúdo gerado por IA

Bloco reescrito por IA abre com etiqueta visível, em linguagem simples, com **ícone e texto** —
nunca só cor, nunca só ícone —, contorno em `atencao-600` no claro e `atencao-400` no escuro, e
link para a nota de transparência da vitrine.

## 11. Ícone e gráfico

### 11.1 Ícone

Todo ícone é SVG servido pelo próprio domínio, e leva rótulo junto — a §5 não abre exceção.

| Medida   | Valor                                                                           |
| -------- | ------------------------------------------------------------------------------- |
| Grade    | `24` px de desenho, com traço de `2` px                                         |
| Tamanhos | `16` (pastilha) · `24` (linha e rótulo) · `32` (carta) · `48` (destaque)        |
| Traço    | Ponta e junta arredondadas, sem preenchimento — a silhueta de badge é a exceção |
| Cor      | `currentColor`, herdada do texto que o ícone acompanha                          |

O `currentColor` é o que faz a camada semântica da §12 alcançar o ícone sem repetir cor
nenhuma: trocar o tema troca o ícone junto, e nenhum arquivo guarda valor de cor.

### 11.2 Gráfico de série

Vale para as séries do território na App 05, o painel público da App 06 e a efetividade
na App 08. O documento 11 diz que dado cada elemento representa; aqui ficam cor, forma e
medida.

| Regra            | Valor                                                                      |
| ---------------- | -------------------------------------------------------------------------- |
| Forma            | Linha para série no tempo, barra para comparação — **nunca setor (pizza)** |
| Cor de série     | Degrau 600 no claro e 400 no escuro, **fora das famílias ponto e moeda**   |
| Distinção        | Além da cor, cada série leva marcador de ponto e rótulo próprios           |
| Legenda          | Abaixo do gráfico, com a unidade escrita por extenso                       |
| Leitura de valor | Ponto focalizável por teclado, com valor, data e unidade                   |
| Grade            | `tinta-200`, sem sombra e sem área preenchida sob a linha                  |
| Série inativa    | Traço interrompido e rótulo "série inativa" — o dado permanece             |

Nenhuma biblioteca de gráfico está escolhida (documento 09), e estas regras valem para qualquer
uma que venha a ser adotada.

## 12. Tokens

Os tokens são propriedades personalizadas de CSS, independentes de framework, em três camadas:

| Camada        | O que guarda                                      | Exemplo                                    |
| ------------- | ------------------------------------------------- | ------------------------------------------ |
| **Primitiva** | Os valores das §§3 e 4                            | `--cor-marca-500`                          |
| **Semântica** | O papel de cada valor                             | `--cor-acao`, `--cor-borda`                |
| **Tema**      | O que muda entre claro e escuro, Operação e Arena | `--densidade`, `--raio-carta`, `--duracao` |

Aplicação consome **apenas a camada semântica e a de tema** — nunca a primitiva direto. O
arquivo nasce junto da primeira pasta de aplicação, compartilhado pelas oito.

## 13. O que este documento não define

| Assunto                                                      | Onde está                     |
| ------------------------------------------------------------ | ----------------------------- |
| Logotipo e marca gráfica do projeto                          | Pendente (documento 09)       |
| Universo dos personagens — Susy, Otávio, Rôbróders e Trenell | Pendente (documento 09)       |
| Submarcas Rôbróders e Robô Educa                             | Pendente (documento 09)       |
| Framework de frontend das aplicações                         | Documento 03 §1               |
| O que cada card mostra e como o território cresce            | Documento 11                  |
| Peça gráfica impressa                                        | Não há a produzir no Ciclo 01 |
