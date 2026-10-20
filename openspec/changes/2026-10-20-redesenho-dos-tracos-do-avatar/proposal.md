# Proposal

Fatia **30 do PRD-04**, no `openspec/cronograma-de-fatias.md`. **Sem identificador novo**,
alcançando `RF-04-06`, `RF-04-07` e `RN-04-14` — pelo precedente das fatias 25 a 29, desenho e
apresentação não têm `RF`/`RN` próprio. Decisão do fundador de 2026-10-20.

## Why

O avatar é o único retrato público do Guerreiro(a), e o catálogo promete dez texturas de cabelo
dizíveis (`RF-04-06`) que o desenho não entrega: `crespo-curto`, `trancas`, `dreads` e `liso` são o
mesmo meio-arco com 1 a 2 px de diferença, e o rosto cobre o resto. A criança de 6 anos escolhe
pelo nome e recebe outro desenho.

Quatro defeitos de geometria agravam isso, e um deles anula uma camada inteira: `cabelo raspado`
cabe dentro dos quatro formatos de rosto e não desenha pixel algum — com ele, a escolha de
`cabelo_cor` também fica invisível. E a montagem abre com fundo e roupa na mesma cor, de modo que o
primeiro avatar que a criança vê não tem corpo.

Nada disso é dado: o objeto gravado referencia só ids, então **nenhum avatar migra**.

## What Changes

- **Quatro defeitos de geometria.** `raspado` passa a desenhar; as **orelhas** saem da camada 2
  para o grupo `rosto`, no mesmo tom de pele, e deixam de ser engolidas pelo cabelo; o **coque**
  encosta na touca; o **comprimento** do `liso` e do `trancas` sai de trás do rosto e de baixo da
  linha do torso.
- **As dez texturas de cabelo são redesenhadas** para terem silhueta distinta fora do rosto, com
  comprimento fora do torso. Os literais soltos dão lugar a uma lista declarativa de primitivas por
  textura, desenhada por helpers.
- **Peça de cabelo na frente da testa**, desenhada dentro do grupo `rosto` com `fill` da cor do
  cabelo. É o que torna as dez texturas reconhecíveis e o que devolve frente ao `raspado`. Mantém
  os nove grupos `data-camada` e a ordem deles; **pede uma frase no documento 15 §7.1**, que
  descreve a camada 5 como "Rosto, formato".
- **Realce de contorno no rosto:** `stroke` branco a 22% sobre a silhueta, porque a composição
  padrão do projeto — cabelo `c1` sobre pele `t1` — não tem separação alguma.
- **Contorno na camada da roupa**, em `var(--cor-superficie)`: quatro das seis cores de fundo têm
  peça de roupa de cor idêntica, porque as duas camadas leem os mesmos tokens semânticos, e o torso
  some. Escolher as duas iguais **segue permitido**, por decisão do fundador. **Pede uma frase no
  documento 15 §7.1**, cuja tabela não menciona contorno na camada 8.
- **A montagem abre com `fundo: "acao-100"`** em vez do padrão da camada, na `TelaDeCadastro`.

Nenhuma mudança no catálogo, na ordem das nove camadas, no objeto versionado do documento 15 §7.2
nem no avatar padrão do projeto (§7.3). Não há **BREAKING**.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `camada-visual-comum`: o requisito "A camada comum compõe o avatar paramétrico no próprio
  aparelho" passa a exigir que **cada traço de cada camada seja distinguível no desenho** — hoje o
  catálogo pode oferecer traço que nenhum pixel distingue — e a admitir, dentro da camada de rosto,
  as orelhas e a peça de cabelo da frente, além do contorno na camada da roupa.
- `aplicacao-da-aula-presencial`: o requisito "O caminho do onboarding cadastra o Guerreiro(a) no
  encontro" passa a exigir que a **composição de partida da montagem** abra com a cor do fundo
  diferente da cor da roupa, mantendo permitido escolher as duas iguais depois.

## Impact

- `comum/avatar/Avatar.tsx` — a geometria das camadas 2 a 5 e 8, e os helpers que a desenham.
- `comum/avatar/avatar.test.tsx` — cenários novos de visibilidade; os existentes seguem válidos.
- `apps/app-01-aula-presencial/src/onboarding/TelaDeCadastro.tsx` — a composição de partida.
- `docs/15-identidade-visual.md` §7.1 — duas frases, no mesmo PR, pelo precedente da fatia 24.
- `docs/09-topicos-em-aberto-e-sugestoes.md` §1 — a decisão de 2026-10-20.

Sem backend, sem rota, sem glifo novo, sem migração. `comum/avatar/catalogo.ts` e
`comum/avatar/objeto.ts` não mudam.

**Fica fora do escopo** a moldura do avatar, que segue circular: trocá-la pelo escudo da marca
alcança o documento 15 §8.1 e toda aplicação que exibe avatar, e é fatia própria.
