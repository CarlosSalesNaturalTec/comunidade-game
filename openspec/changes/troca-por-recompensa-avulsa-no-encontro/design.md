# Desenho — troca por recompensa avulsa no encontro

## Context

O núcleo já faz a troca inteira: `POST /v1/aulas/{id}/trocas` grava, debita o saldo, decrementa
o estoque e lança a baixa no livro-razão numa operação atômica, com as quatro recusas do
`RF-07-37`; `GET /v1/catalogo-avulso` devolve o catálogo por comunidade com preço vigente e
estoque. As duas capacidades estão consolidadas em `openspec/specs/troca-de-recompensa-avulsa/`
e `openspec/specs/catalogo-avulso/`, e **nada nelas muda**.

A App 01 já tem o que esta fatia reusa sem alterar: a sessão de trabalho do aparelho e a sessão
aninhada do Guerreiro(a), cada uma na sua chave de `sessionStorage`; a entrada por nick e imagem
da quarta fatia; e `TelaInicial`, que já recebe `tokenDeTrabalho` e guarda `sessaoDoGuerreiro`
com `token` e `persona_id`.

Falta a ponta do usuário e uma rota de leitura. Motivação em `proposal.md — Why`.

## Goals / Non-Goals

**Goals**

- Uma rota de leitura do saldo que não alcance ninguém além do próprio dono.
- Um caminho de troca que não exista fora do momento aberto pelo Mestre.
- Uma única escrita por troca, com o autor certo.

**Non-Goals**

- Estado de janela de troca no núcleo — a linha *Janela de troca da recompensa avulsa* do
  documento 09 já decidiu que não há, e o fundador a confirmou em 2026-08-25.
- Histórico de trocas no aparelho compartilhado — é da App 05 (`RF-05-85`).
- Fila local: a troca exige rede (`RF-04-57`) e não é enfileirável.

## Decisions

### 1. `GET /v1/eu/pontos-extras`, e não `/guerreiros/{id}/pontos-extras`

A rota nasce sem identificador de persona no caminho. Assim a restrição de que **ninguém lê o
saldo de outra criança** é estrutural, não uma verificação que uma fatia futura possa esquecer:
não existe requisição que aponte para outro Guerreiro(a). Segue a convenção de `/v1/eu` que o
PRD-01 §9 já usa, e a matriz não muda — `Operacao.seus_dados` é exatamente esta leitura.

Nenhum requisito pede que um adulto leia o saldo de uma criança. O Mestre que entrega vê o saldo
na tela do aparelho, ao lado dela, que é onde a jornada 5.10 o coloca.

_Descartado:_ `/guerreiros/{id}/pontos-extras` com verificação de papel — mesma resposta, com uma
superfície que só existiria para ser barrada.
_Descartado:_ acrescentar o saldo a `GET /v1/eu` — misturaria a identidade da sessão com um
número de domínio da economia, que é do PRD-07.

### 2. O momento de troca vive na memória do aparelho, e falha fechado

O estado mora em `AparelhoDaAula`, ao lado da aula escolhida, e **não** vai para
`sessionStorage`: recarregar a página fecha o momento, e o Mestre o reabre. É mais restritivo do
que "a janela reabre sozinha", que era a consequência levada ao fundador em 2026-08-25 — e
deliberadamente: o `RF-04-49` diz que fora do momento a troca não é oferecida, e o padrão de
falha que respeita esse requisito é **fechar**, nunca abrir. Vale registrar a divergência para
que ela seja uma escolha visível, não um efeito colateral.

_Descartado:_ `sessionStorage`, como a aula escolhida — sobreviveria à recarga, mas faria a
aplicação abrir a troca sem que ninguém a tivesse aberto naquele instante.

### 3. Abrir o momento é ler o catálogo; falhou a leitura, não abre

`RF-04-57` exige rede. A verificação é a própria leitura de `GET /v1/catalogo-avulso`: o Mestre
pede a abertura, a aplicação lê o catálogo, e o momento só abre com a resposta na mão. Falha de
rede — `fetch` que rejeita, sem `ErroDaApi` — mantém o momento fechado, com o aviso de que a
troca exige rede.

_Descartado:_ `navigator.onLine`, que informa a placa de rede, não o alcance do núcleo — e mente
justamente no cenário do encontro, com Wi-Fi de pé e internet fora.

### 4. Dois tokens, um por natureza de operação

| Requisição | Token | Por quê |
| --- | --- | --- |
| `GET /v1/catalogo-avulso` | do Guerreiro(a) | o núcleo filtra pela comunidade do vínculo dele; nada precisa ser declarado |
| `GET /v1/eu/pontos-extras` | do Guerreiro(a) | a rota devolve as contas de quem está em sessão |
| `POST /v1/aulas/{id}/trocas` | **de trabalho** | o autor é o Mestre que entrega (`RF-04-55`); o núcleo grava `autor_id` da persona da sessão |

O `guerreiro_id` do corpo vem de `sessaoDoGuerreiro.persona_id`, nunca de nick digitado — mesmo
desenho do recadastro da imagem na quarta fatia, e o que mantém o `RN-01-22` intacto.

A abertura do momento (decisão 3) acontece **antes** de qualquer Guerreiro(a) entrar, então a
leitura de sondagem ali usa o token de trabalho e serve **só para provar que o núcleo responde**
— inclusive quando devolve lista vazia. O catálogo **exibido** é sempre o lido sob o token da
criança, e é ele que decide o que aparece: `listar_catalogo` filtra pela comunidade do vínculo de
quem consulta, e pelo invariante 4 a comunidade dela é a da aula. Nada de comunidade é declarado
por nenhum dos dois lados.

### 5. O estoque zero é filtrado na aplicação

A spec de `catalogo-avulso` é explícita: item que zera por troca **permanece ativo**, para o
Mestre repor sem recadastrar. Logo `RF-04-54` — "item sem estoque não é oferecido" — é trabalho
da tela, e a recusa do núcleo por estoque permanece como autoridade para a corrida entre a
leitura e o envio.

Mesma divisão para `RF-04-53`: a aplicação compara saldo e preço e diz a diferença **antes** de
enviar; o 422 do núcleo é tratado para quando o saldo mudou no intervalo.

## Risks / Trade-offs

- **O saldo lido envelhece entre a tela e a confirmação** → o núcleo reverifica saldo, estoque e
  lastro no ato, e a tela trata o 422 sem repetir a entrada do Guerreiro(a).
- **Recarga no encerramento fecha o momento e o Mestre precisa reabri-lo** → aceito, e é o
  comportamento que a decisão 2 escolhe; o custo é um toque, e o inverso abriria a troca sem ato
  de ninguém.
- **A tela mostra o saldo num aparelho compartilhado, com fila atrás** → a jornada 5.10 é
  presencial e o dado é do Guerreiro(a) que está na frente da tela; a aplicação volta ao início
  ao fim do atendimento (`RF-04-28`), sem deixar o saldo anterior visível.
- **Aparelho aberto por Admin não faz troca** → é a decisão do fundador de 2026-08-25; a esteira
  do encontro precisa de um Mestre no encerramento, o que a jornada 5.10 já pressupõe.

## Arquivos

**Núcleo** — nasce `backend/src/nucleo/ponto_extra/rotas.py`, registrado em `principal.py`.
`modelo.py`, `regra.py`, `trocas/`, `catalogo_avulso/` e `permissoes.py` não mudam.

**App 01** — nascem `src/troca/TelaDeTroca.tsx`, `src/api/pontosExtras.ts`,
`src/api/catalogoAvulso.ts` e `src/api/trocas.ts`. Mudam `AparelhoDaAula.tsx` (o estado do
momento e o papel da sessão de trabalho) e `TelaInicial.tsx` (o terceiro caminho).
