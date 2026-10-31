# Proposal

Origem: **PRD-05 — Área do Guerreiro(a)**, **fatia 12** do `openspec/cronograma-de-fatias.md`.
Identificadores: **reenuncia o `RF-05-08`** e alcança `RF-05-17`. Sem identificador novo, pelo
precedente de `2026-09-25-temperamento-arena-nas-apps-01-e-05`. Decisão do fundador de
2026-10-31, elicitada em `/opsx:explore`.

## Why

A fatia 11 (`2026-10-31-tela-inicial-da-area-do-guerreiro`), do mesmo dia, pôs a Área do
Guerreiro(a) a abrir no bloco da trilha, com os quatro caminhos em grade convivendo com o
conteúdo na mesma tela. Em uso, o fundador recusou o arranjo por três motivos: o conteúdo de um
bloco aparece antes de a criança escolher alguma coisa; a tela acumula menu e conteúdo; e os
cartões saem com alturas diferentes, porque `.cg-caminhos--grade` fixa `align-items: start` e
cada rótulo quebra num número diferente de linhas.

A decisão é **reverter em parte a fatia 11**: a área passa a abrir no **menu dos caminhos**, e
cada caminho abre em **tela própria**, sem menu, com **Voltar**. É o idioma que a App 01 já usa
na tela inicial dela, de modo que as duas aplicações que a criança toca passam a navegar igual.

Isso **reenuncia o `RF-05-08`**, hoje "Tela inicial abre na próxima missão": a trilha deixa de
abrir sem toque. A intenção do requisito — a primeira tela dizer **o que fazer agora** — é
preservada pelo **cartão da Trilha, que nomeia a próxima missão**, entregue pela fatia 11 e que
esta fatia mantém intacto e promove à primeira posição. O requisito é reescrito, nunca removido.

## What Changes

- **BREAKING (comportamento):** a área **abre no menu**, não no bloco da trilha. Nenhum conteúdo
  de bloco aparece de imediato. Cai o `NEVER SHALL abrir em outro bloco` da spec vigente.
- Cada caminho abre em **tela própria, sem o menu**, com `Cabecalho` cuja ação é **Voltar**. O
  Voltar **salta ao menu** de qualquer profundidade — de Progresso, Retomadas, Catálogo ou
  Histórico da série volta-se ao menu, nunca um passo atrás na navegação interna do bloco.
- Disposição **coluna**, um cartão por linha com o glifo ao lado. É o que o documento 15 §6.5 já
  manda para o caso em que os caminhos **são** a tela, e resolve **por eliminação** o defeito das
  alturas desiguais.
- **Ordem nova:** Trilha, minha carteira, desafios e equipes, coleta do território, Sair.
- **Sair vira o quinto cartão**, igual aos demais e na última posição, com o glifo `encerrar` que
  já existe. **Sem `fieldset`** de agrupamento. Existe **somente no menu**; o `Cabecalho` do menu
  fica sem ação, e o da tela de conteúdo leva o Voltar.
- O **aviso de inatividade** e o encerramento por inatividade continuam valendo em **todas** as
  telas, menu e conteúdo — hoje vivem fora do bloco e não podem sumir ao abrir um caminho.
- **BREAKING (API do componente):** `ListaDeCaminhos` perde a disposição **grade** e a propriedade
  de **caminho corrente**, ambas sem consumidor depois desta fatia. Saem com elas a classe
  `.cg-caminhos--grade` e o `aria-current` do cartão. A regra de item corrente por peso de fonte
  do documento 15 §5 **continua viva** no `NavegacaoDeAreas`, que as Apps 03 e 09 usam.
- Os três glifos da fatia 11 — carteira, desafios e coleta — **ficam**, aproveitados em coluna.

Fora do escopo, pelo PRD-05 §3.2: acervo do Guerreiro(a), canal de sugestões e apoio escolar por
assistente de IA, todos do Ciclo 02. Nada se constrói dentro dos blocos: Trilha, Carteira,
Desafios e Coleta mantêm o conteúdo e a navegação interna que já têm.

**Consequência aceita, declarada pelo fundador e não defeito:** cinco cartões de `6` rem com os
espaçamentos dão ~`576` px, então num aparelho de 360×640 — o celular modesto do PRD-05 §10 — a
coleta do território e o Sair nascem **abaixo da dobra**. Agora os caminhos **são** a tela, rolar
é o esperado, e o Sair longe do polegar protege contra toque acidental de criança.

## Capabilities

### New Capabilities

Nenhuma. A fatia muda comportamento já especificado.

### Modified Capabilities

- `area-do-guerreiro`: a área abre no menu e não no bloco da trilha; os caminhos passam a coluna,
  na ordem nova e com o Sair em quinto; cada caminho abre em tela própria com Voltar que salta ao
  menu; o Sair só existe no menu; o aviso de inatividade acompanha todas as telas. Sai o requisito
  do caminho corrente, que deixa de ter objeto.
- `camada-visual-comum`: a lista de caminhos passa a ter **uma** disposição e perde o caminho
  corrente.

## Impact

- `comum/react/ListaDeCaminhos.tsx` — sai `DisposicaoDeCaminhos`, sai `caminhoAtual`, sai o
  `aria-current` do `CartaoDeCaminho`.
- `comum/react/estilos.css` — saem `.cg-caminhos--grade`, as regras de grade do cartão, o
  `@media (min-width: 768px)` da grade e o `.cg-caminho[aria-current]`.
- `comum/react/ListaDeCaminhos.test.tsx` — os testes de grade e de caminho corrente saem.
- `apps/app-05-guerreiro/src/entrada/AreaDoGuerreiro.tsx` — menu ⇄ tela de conteúdo, Voltar, Sair
  em cartão, aviso de inatividade nas duas; e `AreaDoGuerreiro.test.tsx` acompanha.
- `apps/app-01-aula-presencial` — **não muda de comportamento**: já usa coluna e nunca declarou
  caminho corrente. Só deixa de passar a propriedade `disposicao` se a passar.
- Núcleo, rotas e contratos: **nada muda**. O cartão da Trilha segue lendo
  `proxima_missao_titulo` e `proxima_missao_posicao` de `GET /v1/eu/trilhas`.
- Documentação no mesmo PR: documento 15 §6.5 (documento-fonte), documento 09 §1 (linha nova que
  corrige a da fatia 11), PRD-05 §§5.2, 6.2, 10 e 12, e a linha da fatia 12 no cronograma.
