# Design

## Context

O núcleo da leitura pública do território está pronto e consolidado em
`openspec/specs/leitura-publica-do-territorio/spec.md`: a série agregada por tipo de coleta ×
local com o piso de coletores, a lista de comunidades com os quatro indicadores e a ficha da
comunidade. A App 06 tem esqueleto, recortes e carta do Guerreiro(a) desde as fatias 1 e 2.

O que falta é o que esta fatia decide: por onde a **metodologia** viaja na resposta da série,
de onde sai o **estado** do recorte, onde entra a **vitalidade** da comunidade sem virar um
quinto indicador, e como a **representação visual** cresce sem inventar forma por tipo de
coleta. Motivação e recorte estão na `proposal.md`; os requisitos, nas specs do delta.

Restrição que molda tudo: a série é **individual** (uma por coletor) e o piso de coletores
suprime recorte antes de publicar. Qualquer número novo tem de ser apurado **sobre o mesmo
conjunto já publicado**, nunca sobre as séries brutas.

## Goals / Non-Goals

**Goals:**

- A metodologia e o estado do recorte saem na mesma consulta da série, sem leitura extra e sem
  mudar de valor de uma página para outra.
- A vitalidade sai nas duas rotas de comunidade, declaradamente fora da regra dos quatro
  indicadores.
- A variante Comunidade Virtual e a representação visual nascem na camada comum, como as
  demais variantes da carta.

**Non-Goals:**

- Rota nova, entidade nova ou migração. `GET /v1/comunidades/{id}/ods` não é criado.
- Mexer na exportação do território (`exportacao-do-territorio`), que tem contrato e cabeçalhos
  próprios.
- Forma visual por tipo de coleta — o catálogo não a declara.

## Decisions

### 1. A metodologia viaja ao lado dos itens, não dentro de cada ponto

A resposta da série passa a ter envelope próprio — `itens`, `proximo_cursor` e **`recortes`** —,
no mesmo padrão que `ListaDeComunidadesSaida` já usa para o rótulo do ciclo. Cada ponto continua
carregando a chave do recorte (tipo de coleta e local publicado), e o bloco `recortes` traz a
metodologia de **todos** os recortes publicáveis do período consultado, apurada antes do corte
de página e repetida em cada página.

Por que: metodologia dentro do ponto se repetiria por medição e, pior, apurada sobre a página
daria contagem diferente a cada cursor. _Alternativas descartadas:_ metodologia em cada ponto
(tráfego e divergência entre páginas); rota separada de metodologia (leitura a mais na tela que
o freio por origem já aperta).

### 2. A metodologia se apura sobre a consulta de registros publicáveis, estendida

`_consulta_de_registros_publicaveis` passa a carregar também `serie_de_coleta_id` e `origem`, e
a metodologia agrega **sobre ela**: contagem de registros válidos, primeira e última medição,
conjunto de origens e conjunto de cadências das séries dos registros publicados. O piso e a
subida de nível continuam com **uma régua só**.

_Alternativa descartada:_ apurar a partir das séries da comunidade — publicaria cadência,
origem e estado de recorte que o piso suprimiu, e é exatamente o que `RN-08-24` impede.

### 3. O estado do recorte vem das séries que o compõem, no instante da consulta

Recorte é **ativo** quando ao menos uma das séries dos registros publicados dele está em estado
ativo; **inativo** quando nenhuma está. A apuração é no instante da consulta, a mesma régua que
o indicador "séries ativas" e a auditoria por amostragem já usam.

_Alternativa descartada:_ considerar todas as séries do par tipo × local, inclusive as sem
registro publicado — revelaria a existência de série num recorte que o piso não deixou sair.

### 4. A vitalidade é campo próprio, fora dos quatro indicadores e fora da supressão

O número de Guerreiros e Guerreiras vinculados sai em `GET /v1/comunidades` e em
`GET /v1/comunidades/{id}` como campo próprio, apurado pelo **vínculo vigente** — o mesmo filtro
que as demais leituras por comunidade usam, nunca a coluna direta da persona. Não entra na
supressão por piso: o piso é de **coletores distintos** no recorte publicado, e vinculado não é
coletor.

_Alternativa descartada:_ quinto indicador do documento 02 §1 — contraria o documento-fonte, que
fixa quatro.

### 5. A variante Comunidade Virtual e a representação visual nascem em `comum/`

A união `DadosDaCarta` ganha a variante, e `cartaEstaCompleta` passa a decidir **por variante**:
para a Comunidade Virtual, faltando séries ativas ou vinculados, a tela apresenta em outra
forma, como a regra da carta pela metade já manda. A representação visual entra como componente
próprio de `comum/react/`, em SVG paramétrico, recebendo apenas contagens.

_Alternativa descartada:_ desenhar só dentro da App 06 — a carta é da camada comum desde o
documento 11 §8.2, e a App 03 tem lista de comunidades que a reaproveita depois.

### 6. A representação cresce por contagem, com forma única para todo tipo de coleta

O desenho é o contorno da comunidade com uma camada por **tipo de coleta ativo**, nomeado em
texto; a presença de cada camada é a participação daquele tipo nos registros válidos publicados
da comunidade, e o **detalhe** do contorno é o número de bairros publicados. Comunidade sem
registro sai só com nome e contorno. Camada de recorte inativo permanece, marcada.

Nada disso é número inventado: toda medida do desenho é razão entre contagens que a resposta já
traz. _Alternativa descartada:_ termômetro, pluviômetro e mapa de vias como formas próprias —
exigiria campo de forma no catálogo de tipos de coleta, que é decisão nova (documento 09).

### 7. A tela lê no máximo três rotas por página, e nenhuma por card

A seção de comunidades monta os cards com **uma** leitura (`/v1/comunidades`). A página da
comunidade faz três (`/v1/comunidades/{id}`, `/v1/comunidades/{id}/series` e
`/v1/vitrine/ods/cobertura`), e a cobertura é **filtrada na tela** pela comunidade. O endereço
próprio da página é `/comunidades/<id>`, no mesmo padrão de `/guerreiros/<nick>` da fatia 2.

Por que importa: o freio por origem das rotas públicas é por janela, e uma leitura por card
repetiria o erro que a fatia 2 já evitou na carta do Guerreiro(a).

## Risks / Trade-offs

- **O bloco `recortes` se repete em cada página** → é por recorte, não por ponto; o número de
  recortes é o de tipos de coleta × bairros publicados, e o piso já o reduz.
- **Recorte que subiu ao nível da comunidade mistura cadências e origens** → o bloco publica o
  **conjunto** delas, sem eleger uma cadência única que não existe no dado.
- **Vitalidade em comunidade muito pequena** → é contagem de vinculados, sem nick, avatar ou
  identificador, e nenhuma superfície pública diz a comunidade de um Guerreiro(a): não há
  cruzamento que identifique alguém.
- **Mudança de envelope da série** → nenhuma aplicação consome hoje `/v1/comunidades/{id}/series`;
  o contrato de paginação (cursor, tamanho, 422 em parâmetro não declarado) fica inalterado.
- **A representação visual pode virar decoração** → toda medida dela deriva de contagem
  publicada, e o teste cobre comunidade vazia, comunidade com dado e recorte inativo.

## Migration Plan

Sem migração: os campos são aditivos e nenhuma entidade muda. Leitura pública não tem custo de
operação, logo não há lançamento no livro-razão. Reversão é reverter o commit.
