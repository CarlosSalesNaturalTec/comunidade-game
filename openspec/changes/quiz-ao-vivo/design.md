# Design — Quiz ao Vivo

## Context

Ver `proposal.md` — Why. O que este desenho precisa acomodar, do que já está no código:

- `PontoRegular` é **uma linha por (Guerreiro(a), trilha)**, com `total` somado, **sem detalhe
  por evento**. O decremento é recusado em dois lugares — evento do ORM e gatilho no Postgres,
  ambos da sexta fatia (`RN-01-38`). O docstring de `pontuacao/modelo.py` registra que o
  detalhe por evento "fica para quando o crédito precisar de estorno".
- `Equipe` e `IntegranteDaEquipe` existem desde a nona fatia, nos dois tempos de vida.
- `Aula` existe desde a nona fatia, com comunidade, data e horários — **sem trilha**.
- `Atividade.natureza` é `String(64)` aberta desde a quinta fatia, no mesmo padrão de
  `Consentimento.tipo`.
- As duas operações do quiz já estão no enum de `permissoes.py` desde a segunda fatia.

A tensão central: o Mestre **anula pergunta**, e ponto regular **nunca se debita**.

## Goals / Non-Goals

**Goals**

- Apurar o quiz sem nunca precisar de estorno, e portanto sem introduzir histórico por evento
  em `PontoRegular`.
- Ordem de chegada determinística, imune ao relógio do cliente.
- Encerramento idempotente: repetir a chamada não credita duas vezes.

**Non-Goals**

- Sincronização em tempo real entre os aparelhos — é da App 03 com o App 01 (documento 05 §5).
- Rotas HTTP: esta fatia é entidade e regra, como as fatias 5 a 9.
- Histórico por evento de `PontoRegular` — segue adiado, e este desenho existe justamente para
  não precisar dele.

## Decisions

### 1. O crédito nasce no encerramento da partida, nunca por pergunta

A anulação e a proibição de débito só coexistem se **nada for creditado enquanto a lista de
perguntas válidas ainda puder mudar**. Por isso a apuração roda uma vez, na transição
`aberta → encerrada`, lendo as respostas das perguntas não anuladas.

O documento 11 §5 já lança o quiz como automático **da partida**, não da pergunta — o desenho
segue o documento, não o contorna. E a spec exige partida aberta para anular, de modo que
depois do encerramento a lista é imutável por construção.

Consequência: o placar ao vivo que a App 03 exibe é **derivado das respostas**, não de
`PontoRegular`. Leitura, não crédito.

- _Alternativa descartada:_ creditar a cada acerto e estornar na anulação — exige débito,
  proibido por `RN-01-38` e barrado pelo gatilho do Postgres.
- _Alternativa descartada:_ creditar a cada acerto e travar a anulação por completo — contraria
  o documento 05 §5, que dá a anulação ao Mestre.

### 2. A ordem de chegada é do servidor, e o desempate exato é determinístico

`RespostaDeQuiz.momento_de_chegada` é carimbado pelo núcleo no momento da gravação; nenhum
instante declarado pelo chamador é aceito. A "primeira a acertar" sai da ordenação por
`(momento_de_chegada, id)` — o `id` entra só para desempatar o caso de dois carimbos idênticos,
e torna a apuração reproduzível em vez de arbitrária.

- _Alternativa descartada:_ sequência monotônica dedicada — resolveria o empate exato com mais
  garantia, ao custo de uma sequência no banco e de divergência com o caminho de
  `create_all()` dos testes; a precisão de microssegundo do `timestamptz` torna o empate
  improvável, e o desempate por `id` cobre o resto.

### 3. A partida guarda a atividade, e a trilha vem dela

`PartidaDeQuiz` referencia `aula_id` e `atividade_id`. A trilha é derivada por
`atividade → missao → trilha` na apuração, e **não** é copiada para a partida: copiá-la abriria
divergência se a missão da atividade mudasse. `Aula` não é alterada.

- _Alternativa descartada:_ `trilha_id` na partida, denormalizado — ganho de uma junção em troca
  de duas fontes de verdade para o mesmo fato.

### 4. As equipes disputantes são materializadas na abertura

A partida guarda a lista de equipes que disputam (`EquipeNaPartida`), fixada na abertura. É
onde a recusa do Guerreiro(a) repetido é verificada uma vez só — em vez de reavaliar a cada
resposta, quando a composição da equipe da aula já pode ter mudado.

A verificação lê `IntegranteDaEquipe` das equipes declaradas e recusa com 422 se a interseção
entre quaisquer duas não for vazia (`RF-01-39`).

### 5. O crédito reaproveita o caminho da criação original

A apuração chama `creditar_ponto_regular` por integrante, exatamente como
`creditar_pontuacao_da_criacao_original` já faz — mesmo ponto de entrada, mesmo respeito ao
gatilho. O que muda é a régua do valor, que é própria do quiz e não passa por
`_valor_regular`, calculada sobre a atividade e o desfecho do resultado.

Apuração por equipe: `min(10, acertos + bonus)`, com `bonus` contando as perguntas em que a
equipe foi a primeira a acertar. O teto é da **partida**, aplicado antes do crédito, e o valor
apurado vai **integral a cada integrante**, sem rateio.

### 6. Idempotência do encerramento

O encerramento é aceito apenas na transição `aberta → encerrada`; a segunda chamada devolve 422
sem tocar em `PontoRegular`. Como o crédito acontece na mesma transação da transição, não há
janela em que a partida esteja encerrada e o crédito ainda não tenha ocorrido.

## Risks / Trade-offs

- **A App 03 precisa de placar ao vivo, e ele não sai de `PontoRegular`** → o placar é derivado
  das respostas da partida, e a rota que o expõe é do PRD-02. O núcleo entrega a apuração
  parcial como leitura; o crédito continua só no encerramento.
- **Partida que nunca é encerrada nunca credita** → é o comportamento correto, não um defeito:
  sem encerramento a lista de perguntas válidas segue mutável. A App 03 é responsável por
  encerrar, e o painel do dia mostra as partidas abertas.
- **Carimbo do servidor sob rede instável penaliza quem tem conexão pior** → é a regra escrita
  no documento 05 §5, não escolha deste desenho. Registrado aqui porque é a consequência real
  de "ordem de chegada no servidor".
- **Dois carimbos idênticos ao microssegundo** → desempate por `id`, determinístico e
  reproduzível, embora não signifique nada no mundo físico.

## Migration Plan

Migração aditiva, sem alteração de tabela existente:

1. `pergunta_de_quiz` — autor, enunciado, alternativas e a correta.
2. `partida_de_quiz` — `aula_id`, `atividade_id`, situação, autoria da abertura e do
   encerramento.
3. `equipe_na_partida` — a lista fixada na abertura, com unicidade por (partida, equipe).
4. `resposta_de_quiz` — `partida_id`, `pergunta_id`, `equipe_id`, alternativa,
   `momento_de_chegada`, com **unicidade por (partida, pergunta, equipe)**, que é o que torna o
   reenvio inofensivo.

Reversão: `downgrade` derruba as quatro tabelas. Nenhuma linha de `ponto_regular`,
`equipe`, `aula` ou `atividade` é tocada pela migração, de modo que a reversão não perde
crédito já concedido — o que foi creditado por uma partida permanece, como qualquer ponto
regular.

## Open Questions

Nenhuma. O que restava — a trilha do ponto e o controle de aparelhos — foi decidido pelo
fundador e gravado nos documentos-fonte antes desta change.
