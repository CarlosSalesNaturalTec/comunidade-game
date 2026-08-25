# Troca por recompensa avulsa no encontro

Origem: **PRD-04 — App 01: Aula presencial**, §§5.10 e 6.3. Quinta fatia do PRD-04.

Atende `RF-04-49`, `RF-04-50`, `RF-04-51`, `RF-04-52`, `RF-04-53`, `RF-04-54`, `RF-04-55`,
`RF-04-56` e `RF-04-57` — o §6.3 inteiro. Sob `RN-04-23`, `RN-04-24`, `RN-04-25`, `RN-04-26`,
`RN-04-27`, `RN-04-28` e `RN-04-29`, e sob `RF-01-22`, `RN-01-39`, `RN-01-40` e `RN-01-41` do
núcleo. Atende também `RF-05-82`, do PRD-05, pela rota de leitura que nasce aqui. Invariantes 9
e 23 do documento 99 §6.

## Why

O ponto extra tem duas contas, e a plataforma só sabe mostrar uma.

```text
  ponto_extra/modelo.py   acumulado          jogos/rotas.py:112 lê        ✅
                          saldo_disponivel   nenhuma rota o devolve       ❌

  trocas/rotas.py         POST /aulas/{id}/trocas    nenhum cliente chama ❌
                          GET  /trocas               nenhum cliente chama ❌
```

O `saldo_disponivel` é creditado por `ponto_extra/regra.py`, debitado por `trocas/regra.py`,
protegido contra negativo por `CheckConstraint` e por gatilho no banco — e **invisível por
HTTP**. O único número de ponto extra que sai do núcleo hoje é o `acumulado`, no contrato de
leitura dos jogos, que é justamente o número que o `RF-04-51` proíbe de mostrar na tela da
troca.

Do outro lado, a troca inteira já está escrita e testada desde a change
`2026-08-18-tabela-de-pontos-extras-e-catalogo-avulso` e a
`2026-08-19-troca-de-recompensa-avulsa`: `POST /v1/aulas/{id}/trocas` grava a troca, debita o
saldo, decrementa o estoque e lança a baixa no livro-razão numa operação só, com as quatro
recusas do `RF-07-37` no lugar. **Nenhum cliente a chama.** O catálogo por comunidade, com
preço vigente e estoque, também já é lido por `GET /v1/catalogo-avulso`.

Falta a ponta em que a criança está. Enquanto ela não existe, o invariante 23 — *ponto regular
nunca se gasta; só o extra se troca* — é regra sem espelho: nada na plataforma exibe a distinção
entre acumulado e saldo a quem ela pertence. E o §6.3 do PRD-04 é a única seção do PRD sem uma
única linha entregue.

Esta fatia é também a última do PRD-04 que **não depende de outra aplicação**. O que sobra do
§6.2 — conteúdo da missão (`RF-04-35`), assistente de trilhas (`RF-04-36` a `RF-04-40`) e a
partida no aparelho (`RF-04-41` a `RF-04-44`) — espera a autoria de conteúdo da App 09 e a
condução da partida da App 03, como a §14 do PRD-04 já registra.

## What Changes

### O saldo disponível ganha quem o leia (`RF-04-51`, `RF-05-82`)

Nasce `GET /v1/eu/pontos-extras`, sob a **sessão do próprio Guerreiro(a)**, devolvendo as duas
contas: `acumulado` e `saldo_disponivel`. Persona de qualquer outro papel recebe **403**.

A rota entra pela convenção de `/v1/eu` que o PRD-01 §9 já usa, e não recebe identificador de
persona no caminho: **não há como apontá-la para outra criança**. Isso não é decisão nova, é o
recorte mínimo que atende `RF-04-51` e `RF-05-82` sem alcançar o que nenhum requisito pediu —
nenhum adulto lê o saldo de uma criança, nem o Mestre que entrega o item. A matriz de permissões
não muda: `Operacao.seus_dados` já é a leitura do Guerreiro(a) sobre si.

Ela também **não contradiz o invariante 8**, que veda o saldo às rotas de jogo: `RN-01-41` fala
do contrato de leitura dos jogos, público e sem persona, e esta rota exige sessão da própria
criança. A `jogos/rotas.py` segue lendo só o `acumulado`, sem uma linha alterada.

### O momento de troca, que só existe quando o Mestre o abre (`RF-04-49`, `RF-04-57`)

Decisão do fundador, 2026-08-25: a troca é oferecida **apenas com Mestre na sessão de trabalho
do aparelho**. O `RF-04-05` deixa Mestre **ou Admin** abrir o aparelho, mas o núcleo recusa a
troca de Admin com 403, e o `RF-04-49` e o `RF-04-55` são do Mestre. Aparelho aberto por Admin
não oferece o momento de troca — sem tela morta que só falharia no envio.

O momento é **estado do aparelho, sem registro no núcleo** — a linha *Janela de troca da
recompensa avulsa* do documento 09 já o decidiu, e o fundador a confirmou em 2026-08-25 para
o Ciclo 01. Ele nasce fechado e não sobrevive à recarga da página: fora dele a troca não é
oferecida, e o padrão de falha é fechar, nunca abrir. Sem rede o momento não abre (`RF-04-57`),
pelo mesmo motivo por que o cadastro não abre no `RF-04-24`: a operação inteira é do núcleo.

### O catálogo e o saldo na tela da criança (`RF-04-50`, `RF-04-54`, `RF-04-56`)

Aberto o momento, o Guerreiro(a) entra pelo nick e pela imagem — o caminho de entrada que a
quarta fatia entregou — e vê o catálogo avulso da sua comunidade, com preço em pontos extras e
estoque restante, e o próprio saldo disponível.

O item com **estoque zero não é oferecido**. A spec do `catalogo-avulso` é explícita: o item que
zera por troca **permanece ativo e cadastrado**, para o Mestre repor sem recadastrar, e a próxima
troca é recusada pela regra de estoque. Filtrar o que não dá para trocar é, portanto, trabalho da
aplicação — a mesma recusa, dita antes de a criança escolher.

Nenhuma tela desta fatia exibe ponto regular como moeda (`RF-04-56`, invariante 23).

### A troca, num ato só (`RF-04-52`, `RF-04-55`)

Decisão do fundador, 2026-08-25: o `POST /v1/aulas/{id}/trocas` sai **sob a sessão de trabalho
do aparelho**, e o `guerreiro_id` vem do `persona_id` da sessão aninhada do Guerreiro(a) — nunca
de um nick digitado nem de uma busca. É o mesmo desenho da presença por reconhecimento da quarta
fatia, com uma diferença que importa: lá a sessão de trabalho autenticava **sem se tornar
autora**, porque a presença é fato do encontro; aqui o Mestre **é** o autor, porque a entrega é
ato dele (`RF-04-55`), e o núcleo já grava `autor_id` com a persona da sessão.

A confirmação da entrega pelo Mestre **é** o envio: uma requisição, uma operação atômica no
núcleo — troca gravada, saldo debitado, estoque decrementado, baixa lançada no livro-razão. Não
há reserva, fila nem promessa (`RN-04-27`).

### A recusa por saldo, dita em pontos (`RF-04-53`)

O núcleo recusa com 422 dizendo **qual** das quatro condições barrou, mas não a diferença
numérica. Com o saldo lido pela rota nova e o preço vindo do catálogo, a aplicação diz a
diferença em pontos antes do envio, e nunca em reais nem em moedas (`RN-04-28`). A recusa do
núcleo continua sendo a autoridade: a tela impede o que sabe que não passa, e trata o 422 quando
o saldo mudou entre a leitura e o envio.

## Capabilities

### New Capabilities

Nenhuma. As três capacidades tocadas já existem e são consolidadas.

### Modified Capabilities

- `ponto-extra`: o saldo disponível ganha a rota de leitura que nunca teve, restrita ao próprio
  Guerreiro(a) em sessão; o contrato de leitura dos jogos segue vedado ao saldo, sem alteração.
- `aplicacao-da-aula-presencial`: entra o terceiro caminho da tela inicial — o momento de troca,
  aberto e fechado pelo Mestre, indisponível ao Admin e sem rede; entram a leitura do catálogo e
  do saldo pela criança, a recusa antecipada por estoque e por saldo, e o registro da troca sob a
  sessão de trabalho do aparelho.
- `troca-de-recompensa-avulsa`: nenhum requisito muda; a capacidade é citada porque a fatia lhe dá
  o primeiro cliente. Sem delta próprio.

## Impact

**Núcleo** — nasce `ponto_extra/rotas.py`, com uma única rota de leitura, registrada em
`principal.py`. `ponto_extra/modelo.py`, `ponto_extra/regra.py`, `trocas/` e `catalogo_avulso/`
**não mudam**: as regras de que esta fatia depende já estão escritas, testadas e consolidadas.
`permissoes.py` não muda.

**App 01** — nasce a tela do momento de troca, com o catálogo, o saldo e a confirmação da
entrega; a tela inicial ganha o terceiro caminho, visível só com Mestre no aparelho e com o
momento aberto; nascem os módulos de API do catálogo, do saldo e da troca. O módulo de biometria
e a entrada por nick e imagem da quarta fatia são reusados sem alteração.

**Documentação** — PRD-04 §9 ganha as três rotas do §6.3, que a tabela não tinha; PRD-04 §13
recebe as duas decisões de 2026-08-25; PRD-07 §9 ganha a rota de leitura do saldo; documento 09
recebe as linhas correspondentes; `docs/prds/index.md` registra a fatia.

**Fora desta fatia** — o histórico de trocas do Guerreiro(a) (`GET /v1/trocas`) fica fora: o
`RF-04-27` fecha o atendimento e a tela volta ao início, e quem lê o histórico é a App 05
(`RF-05-85`), não o aparelho compartilhado. A **fila local sem rede** (`RF-04-23` a
`RF-04-25`, `RF-04-58`) segue fora, e o `RF-04-57` é o que a alcança aqui: a troca exige rede e
não entra em fila. O §3.2 do PRD-04 já exclui a loja entre encontros, a reserva e a entrega
diferida, e nada disso entra.
