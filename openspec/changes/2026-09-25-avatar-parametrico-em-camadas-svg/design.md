# Design

## Context

Ver `proposal.md` — Why. As specs alteradas são `camada-visual-comum`, que ganha o contrato do
avatar, e `aplicacao-da-aula-presencial`, no cadastro do onboarding e na tela das equipes.

O documento 15 §7 é a fonte e já decide quase tudo: as nove camadas, a ordem, o objeto versionado,
o avatar padrão e a regra de traço desconhecido. Esta fatia decide **onde** isso mora, **como** a
criança escolhe e **o que acontece com o avatar já gravado**.

## Goals / Non-Goals

**Goals:**

- Catálogo, renderizador, objeto versionado e avatar padrão em `comum/`.
- O onboarding compõe o avatar em vez de descrevê-lo.
- As telas de equipe das Apps 01 e 05 desenham o avatar.

**Non-Goals:**

- Carta, emblema, badge e glifo de poder.
- Adotar o avatar nas outras aplicações e no App 04.
- Avatar do Apoiador, que é logomarca.
- Migrar dado gravado.

## Decisions

1. **`comum/avatar/`, pasta própria, não `comum/react/`.** O catálogo e o renderizador são
   conteúdo e desenho de domínio, não o contrato de acessibilidade dos componentes. É a mesma
   distinção que separa `comum/biometria` de `comum/react`. O documento 03 §1.2 recebe a linha.
   _Descartado:_ `comum/react/`.

2. **Nenhuma migração de dado.** O §7.2 manda traço desconhecido cair no padrão da camada, e o
   avatar gravado hoje é `{ formaDeTratamento, caracteristicasDoAvatar }` — objeto sem nenhum traço
   conhecido, que por essa regra cai **inteiro** no padrão e desenha o avatar padrão do projeto.
   Nada quebra, e nenhum cadastro precisa ser reescrito. _Descartado:_ revisão de banco traduzindo
   texto livre em traços — não há como adivinhar "cabelo crespo curto" a partir de uma frase ditada,
   e errar o palpite seria pior que o padrão.

3. **A forma de tratamento continua no mesmo campo `avatar` do núcleo, ao lado do objeto.** O
   núcleo guarda `avatar` como texto opaco e a App 01 já grava as duas coisas juntas ali; separá-las
   exigiria campo novo no núcleo, que é outra fatia e outro PRD. O objeto do §7.2 é aninhado, e a
   forma de tratamento fica fora dele — o §7 exige que ela **seja** campo próprio, não que more em
   outra coluna. _Descartado:_ coluna nova na persona.

4. **A escolha no onboarding é camada por camada, com o nome dizível de cada traço, e nasce no
   avatar padrão.** Assim a criança vê um avatar completo desde o primeiro toque e vai trocando o
   que quiser, em vez de montar do zero nove vezes. _Pendência:_ como isso acontece **por conversa**
   com uma criança de 6 anos, que é o que o `RF-04-06` pede — a modalidade áudio precisa saber
   escolher pelo nome dito. Entra no documento 09; a fatia entrega a escolha na tela, e a conversa
   por áudio sobre o catálogo é da fatia do roteiro da IA.

5. **O renderizador é SVG embutido, composto em ordem de camada.** Mesma razão do sistema de ícone:
   `currentColor` não vale aqui, mas o princípio 6 veda requisição a terceiro, e o §7 exige
   composição sem rede. _Descartado:_ imagem servida pelo núcleo — o avatar é do aparelho, e o App
   04 joga offline com o catálogo guardado.

## Risks / Trade-offs

- **O catálogo nascer pobre e parecer que a representatividade foi cumprida** → a ordem das escalas
  é requisito na spec, com cenário próprio, e a cobertura de cada camada vem da tabela do §7.1, não
  de escolha de quem implementa.
- **Peso dos nove SVG no primeiro carregamento**, contra o alvo de celular modesto (documento 15
  princípio 4) → o catálogo é traço, não ilustração; o desenho fica em traço simples e o peso entra
  como item de conferência ao fechar a fatia.
- **Avatar antigo caindo no padrão parecer perda de dado** → o texto ditado continua gravado no
  campo; ele deixa de ser a fonte do desenho, e nada é apagado.
