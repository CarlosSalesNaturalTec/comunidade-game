# Design

## Context

Ver `proposal.md` — Why. O que molda a abordagem é o que já existe:

| Peça | Estado hoje |
| --- | --- |
| `DesbloqueioDaMissao` | uma linha por par Guerreiro(a)–missão, com `aprovado: bool \| None` (`None` = declarado e não julgado), `julgado_por_id` e as quatro colunas da comprovação |
| `julgar_desafio_pratico` | recebe `aprovado: bool`; aprovado marca a linha, reprovado **apaga** a linha; recusa julgar o que já tem `aprovado` |
| `JulgarDesafioPraticoEntrada` | `extra="forbid"`, campo único `aprovado: bool` |
| `GET /v1/missoes/desbloqueios-pendentes` | já devolve `criterio_de_aceite` e `comprovacao_entregue` — a fatia 13 os pôs lá, e nenhuma tela os desenha |
| `GET /v1/.../comprovacao` | rota de bytes da comprovação, servida ao Guerreiro(a) e ao Mestre autor (fatia 13) |
| `derivar_percurso` | `aguardando_mestre = aprovado is None`; a próxima missão é a de menor posição com `aprovado is not True` |
| `MissaoNoPercursoSaida` | já carrega `comprovacao_entregue` |
| Bancada da App 09 | `TelaDeDesbloqueiosPendentes.tsx` — nick, missão, hora e dois botões |
| Tela do prático | `comum/trilha/DesafioDeDesbloqueio.tsx`, consumida pela App 05; já reapresenta a comprovação entregue |
| Crédito de ponto regular | `pontuacao.regra.creditar_ponto_regular`, com `creditar_pontuacao_da_criacao_original` como molde de via própria; `trilhas/regra.py` **já importa** `..pontuacao.regra` |
| Valor dos 5 pontos | já na tabela do documento 11 §5 — não é número novo |

As seis decisões do fundador de 2026-11-04 que recortam a fatia estão nas decisões 1 a 6.

## Goals / Non-Goals

**Goals:**

- A produção entregue e o critério à vista do Mestre na bancada, pela leitura que já existe.
- Os dois vereditos, o motivo e os 5 pontos no núcleo, com as recusas de cada um.
- O veredito e o motivo chegando ao Guerreiro(a) — nada *write-only*.

**Non-Goals:**

- A **vitrine** lendo o `publicavel` e a linha do portfólio (fatia 12 do PRD-03). Aqui o
  veredito nasce e é servido; quem o consome em público é ela.
- O **badge** de autoria e o **nível**: o julgamento não os toca.
- A conclusão do desafio extra (fatia 23).
- Reescrever o requisito da recompensa em `area-do-guerreiro` ("no prático só depois do
  Mestre"): "passou" lá é o `cumpriu` daqui, e o comportamento não muda — delta por vocabulário
  seria churn sem contrato novo.

## Decisions

### 1. `aprovado` vira `cumpriu`, e `publicavel` nasce ao lado — duas colunas, não um enum

Decisão do fundador, 2026-11-04: os dois vereditos são independentes em significado, e
`cumpriu` sem `publicavel` é julgamento válido. Duas colunas anuláveis dizem isso direto;
`cumpriu is None` segue sendo "declarado e não julgado", que é o que `derivar_percurso` e a
bancada já leem — a lógica de três estados não muda de forma, só de nome.

_Alternativa descartada:_ um enum de veredito (`cumprido_e_publicavel`, `cumprido`,
`nao_cumprido`) — amarra os dois eixos num valor só e obriga a reescrever todo teste de
`aprovado is None`, sem ganho.

_Alternativa descartada:_ manter `aprovado` e só acrescentar `publicavel` — deixaria no banco
um nome que a regra nova desmente, e é exatamente o tipo de resíduo que este bloco já consertou
quatro vezes.

### 2. A reprovação para de apagar: a linha guarda o veredito e o motivo

Decisão do fundador, 2026-11-04. O motivo em linguagem simples só serve se a criança o ler, e
apagar a linha o destruiria no ato. A linha reprovada passa a ser **devolutiva**, como a criação
original devolvida (`motivo_da_devolucao`), não reprovação persistida: entregar de novo volta
`cumpriu`, `publicavel`, `motivo` e `julgado_em` a nulo e substitui a comprovação, sem segundo
registro — a unicidade `(guerreiro_id, missao_id)` continua valendo e não precisa mudar.

Consequência em `derivar_percurso`: `cumpriu is False` não é desbloqueada e não é
`aguardando_mestre`, e a missão volta a ser a **próxima** dele — que é o que o percurso já
calcula, porque `cumpriu is not True` é o predicado da próxima. Nenhuma linha muda ali.

_Alternativa descartada:_ guardar o motivo numa tabela de julgamentos, com histórico de
tentativas — contaria fracassos, que `RN-05-20` proíbe apresentar, exportar ou contar.

### 3. A idempotência do crédito vem do estado terminal, não de uma coluna nova

`cumpriu is True` é terminal: julgar de novo é recusado com 422, e a entrega está encerrada.
O único caminho a um segundo crédito seria reprovar → reabrir → cumprir, que credita **uma**
vez. Então não nasce coluna de "já pontuado": o invariante é o estado, e o teste o exercita.

`julgado_em` é o que separa o julgado por esta regra do julgado **antes** dela — a linha antiga
tem `cumpriu=True` com `julgado_em` nulo, e por isso não recebe crédito retroativo (decisão do
fundador, 2026-11-04) nem pode ser rejulgada. Sem *backfill*: a migração não credita nada e não
mexe em saldo nenhum.

_Alternativa descartada:_ coluna `pontuado_em` — segundo lugar para a mesma verdade, e
divergiria de `creditar_pontuacao_da_criacao_original`, que também se apoia no estado
(`situacao != entregue` barra o crédito duplo).

### 4. O crédito é via própria em `pontuacao/regra.py`, no molde da criação original

Nasce `creditar_pontuacao_do_desbloqueio_pratico`, chamada por
`trilhas.regra.julgar_desafio_pratico` na mesma transação, com a constante
`VALOR_DO_DESBLOQUEIO_PRATICO = 5` ao lado das demais do documento 11 §5. `trilhas/regra.py` já
importa `..pontuacao.regra`, e `pontuacao.regra` importa só `trilhas.modelo` — nenhum ciclo
novo. A função **não** chama `certificar_nivel_5` nem `conceder_badge_de_autoria`: é a diferença
deliberada em relação à criação original, e o documento 02 §4 a exige.

_Alternativa descartada:_ creditar dentro de `julgar_desafio_pratico` com
`creditar_ponto_regular` direto — espalharia a régua do documento 11 §5 fora de `pontuacao/`,
onde as outras quatro fontes moram.

### 5. O veredito e o motivo saem pelo percurso, não por rota nova

Decisão do fundador, 2026-11-04: a fatia alcança também a App 05. `MissaoNoPercursoSaida` já
carrega `comprovacao_entregue`, e é a leitura que a tela do prático consome — os campos do
julgamento entram no mesmo payload, sem segunda chamada e sem rota nova. É a lição da fatia 13,
que trouxe a leitura dos bytes para dentro dela em vez de deixá-la para esta.

_Alternativa descartada:_ `GET /v1/eu/missoes/{id}/julgamento` — uma chamada por missão só para
ler três campos que o percurso já atravessa.

### 6. `livro-razao` fica fora, e a linha 27 do cronograma se corrige

Decisão do fundador, 2026-11-04. A linha prevê delta nessa capacidade; lendo-a, ela é o registro
contábil de **recursos e moedas** — lançamento, ajuste, saldo por ponto de apoio — e nada diz de
ponto regular, que é inteiramente de `pontos-niveis-e-badges`. Nenhum requisito contábil muda, e
o julgamento não tem custo a lançar. Era estimativa de planejamento: a mesma change corrige a
linha, como `CLAUDE.md` manda fazer com recorte que divergiu.

## Risks / Trade-offs

- **O contrato do julgamento quebra** sob `extra="forbid"`: `aprovado` sai e entram `cumpriu`,
  `publicavel` e `motivo`. Mitigação: o único cliente é a App 09, que entra no mesmo PR, e a
  rota só é alcançável por Mestre autor em sessão.
- **A reversão do apagamento deixa comprovação guardada por mais tempo** — a mídia da entrega
  reprovada não é mais removida no julgamento. É o preço de a criança poder ler o motivo e
  rever o que entregou; a guarda e o aviso de que a mídia fica guardada já são requisito
  (`RF-05-92`, `RN-05-51`), e a revogação do consentimento segue despersonalizando como sempre.
  O que **não** se perde: a mídia continua servida só ao Guerreiro(a) e ao Mestre autor.
- **Renomear `aprovado` alcança teste e leitura já escritos** — `test_desbloqueio_da_missao.py`,
  `test_percurso_da_trilha.py` e `test_criacao_original_rota.py` o citam. É churn conhecido e
  mecânico, e a alternativa (nome que a regra desmente) custa mais depois.
- **Dois vereditos num ato só** significam que a recusa de um não grava o outro: o julgamento é
  atômico. É o que evita a linha com `publicavel=True` e `cumpriu` nulo, estado que nenhuma
  leitura saberia explicar.
