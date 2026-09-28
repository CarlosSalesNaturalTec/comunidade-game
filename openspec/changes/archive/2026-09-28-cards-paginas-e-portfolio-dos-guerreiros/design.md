# Design

## Context

Ver `proposal.md` — _Why_. O que molda o desenho:

- A carta do personagem já existe em `comum/react/CartaDoPersonagem.tsx`, variante
  `guerreiro`, com exatamente os campos do documento 11 §8.2 e com `cartaEstaCompleta`
  decidindo quando ela **não** se apresenta. A App 06 não cria carta nova.
- `openspec/specs/leitura-publica-da-vitrine` já traz o portão da divulgação, a recusa
  indistinta por nick e a projeção mínima de avatar e nick, usada também pelo contrato dos
  jogos. O que muda é o **tamanho da projeção** nas duas rotas de Guerreiro(a).
- `openspec/specs/protecao-das-rotas-publicas` já freia a consulta por nick (30 por 10 minutos,
  atraso crescente) e `comum/api` já entrega `tempoDeEsperaEmSegundos` ao cliente. Nada muda no
  freio: a fatia só o torna legível.
- A navegação por endereço real da fatia 1 (`src/navegacao/`) existe e não guarda nada.

## Goals / Non-Goals

**Goals:**

- Uma página de cards sai de **uma** resposta do núcleo, sem consulta por Guerreiro(a).
- Card e página vêm da **mesma** projeção — divergir seria dois contratos para uma carta.
- Nada da visita fica no aparelho, para que a revogação valha na leitura seguinte.

**Non-Goals:**

- Mudar a projeção mínima que a autoria das criações e o elenco dos jogos usam.
- Rota nova, entidade nova ou migração.
- Cache, memória de rolagem, favorito ou qualquer preferência do visitante.

## Decisions

### 1. A composição é montada no núcleo, em consultas por conjunto

Pontos e posição, níveis, badges e criações de **todos** os Guerreiros e Guerreiras da página
saem em consultas por conjunto de identificadores, no molde de `buscar_avatares_e_nicks`, e são
distribuídos em memória. _Alternativa descartada:_ uma consulta por Guerreiro(a) — é N+1 e, do
lado do cliente, seria barrada pelo próprio freio da consulta por nick.

### 2. O núcleo devolve o **nome do poder**, não o `trilha_id`

Hoje a rota por nick devolve nível e badge com `trilha_id` cru, e quem consome teria de cruzar
com `/vitrine/poderes`. A projeção passa a trazer o nome do poder e a família do badge já
resolvidos. _Alternativa descartada:_ cruzar no aparelho, como a App 05 faz em
`comum/carta/CartaDoGuerreiro` — lá a leitura é de **um** Guerreiro(a) em sessão; aqui
multiplicaria por card e poria a regra de composição no cliente.

### 3. O desempenho é a posição do ranking público, na mesma derivação já existente

`pontuacao.regra.consulta_de_ranking(exigir_divulgacao=True)` é a derivação que o
`/vitrine/rankings` já usa, e é dela que sai a posição da carta — inclusive o recorte por
comunidade, quando a consulta o carrega, para que posição e listagem nunca discordem.
_Alternativa descartada:_ calcular posição só na rota de ranking e deixar a carta com pontos —
o §8.2 pede desempenho, e pontos sem posição não é desempenho.

### 4. A criação entra na carta sob a mesma condição da rota pública

Uma criação só compõe a carta quando **todos** os creditados nela têm autorização vigente — a
condição que `/vitrine/criacoes` já aplica, reaproveitada, não reescrita. Uma regra só para as
duas saídas.

### 5. A rotação comanda o paginador, e o visitante também

A seção usa `SequenciaPaginada` de `comum/react` com a posição **comandada de fora**: um
temporizador de 5 s avança a posição, e os controles do próprio paginador deixam o visitante
avançar sozinho. É o que faz a rotação **não** ser a única via ao conteúdo (documento 15 §§5,
8.1). Com `prefers-reduced-motion`, o temporizador não é armado e ficam só os controles.
_Alternativa descartada:_ carrossel próprio com botões — reescreveria o que o `comum` já tem.

### 6. Só a página individual ganha endereço próprio

`/guerreiros/<nick>` é endereço de primeira classe, porque o `RF-03-03` e a jornada §5.6 o
exigem compartilhável e alcançável direto. As demais seções seguem dentro do recorte, sem
endereço próprio: a fatia 1 já decidiu que o recorte é o caminho. A resolução de caminho de
`src/navegacao/recortes.ts` passa a reconhecer o prefixo antes de cair no recorte padrão.

### 7. Estado só em memória

Nada do que a vitrine lê é guardado em `localStorage`, `sessionStorage` ou cookie, e a leitura
se refaz a cada visita — é o que faz a revogação valer na leitura seguinte (`RF-03-14`) e o que
a `aplicacao-da-vitrine` já exige da aplicação inteira.

### 8. O 429 é tela, não erro

O freio chega como `ErroDaApi` com `tempoDeEsperaEmSegundos`; a busca o trata como resposta
esperada e diz o motivo e a espera em linguagem simples. Erro de rede e 404 continuam distintos
— e o 404 diz "não encontrado", igual para nick inexistente e nick sem autorização.

## Risks / Trade-offs

- **A listagem enriquecida fica mais cara por página** → as consultas são por conjunto e a
  página continua limitada pelo tamanho de paginação; nenhuma consulta nova por item.
- **Card e página divergirem com o tempo** → a projeção é uma só, montada em um lugar só, e a
  spec exige que as duas rotas devolvam a mesma composição.
- **`RF-03-08` sem título e `RF-03-02` sem os Mestres do poder** → declarado nos dois artefatos
  e na linha 2 do cronograma; o título depende de decisão do fundador sobre o modelo, e os
  Mestres, da fatia 7.
- **A rotação de 5 s atrapalhar quem lê devagar** → a posição é comandada de fora e os
  controles do paginador sempre estão lá; `prefers-reduced-motion` desarma o temporizador.
