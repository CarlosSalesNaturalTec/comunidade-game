## Context

Ver `proposal.md` — Why. O que o código já oferece e condiciona o desenho:

- `recursos/modelo.py` traz `TipoDeRecurso` e `ValorDeReferencia`, com vigência **semiaberta**
  (`vigencia_inicio <= data < vigencia_fim`) e `NUMERIC(12, 2)` para moeda.
- `pontos_de_apoio/modelo.py` traz o `PontoDeApoio`, dimensão do saldo.
- `armazenamento/porta.py` traz a `PortaDeArmazenamento`, e `fila/rotas.py` já sobe comprovante
  por _multipart_ com `UploadFile`, guardando referência, nome original, tipo e tamanho.
- `fila/modelo.py` traz a `SolicitacaoDeParticipacao` com `aporte_declarado` e o comprovante —
  o pré-cadastro que esta fatia homologa.
- `pontuacao/modelo.py` e `consentimentos/modelo.py` trazem o padrão de **gatilho no banco** que
  recusa alteração e remoção fora do ORM.
- `erros.py` traz `PermissaoNegada` (403), `ErroDeValidacao` (422) e `NaoEncontrado` (404).

## Goals / Non-Goals

**Goals:**

- Saldo por tipo de recurso e ponto de apoio **reprodutível**: recontar devolve o mesmo número.
- Imutabilidade do lançamento garantida **fora do ORM**, não só na camada de regra.
- Conversão em moedas presa à **data do aporte**, imune a mudança posterior da tabela.

**Non-Goals:**

- Não há projeção materializada de saldo nesta fatia (ver Decisions 1).
- Não há trava de concorrência sobre o saldo: só a reserva precisa dela, e a reserva não entra.
- Não há rota de leitura de saldo, de aporte ou de lançamento.

## Decisions

**1. O saldo é agregação sobre `lancamento`, não tabela.** `SELECT SUM(quantidade) ... GROUP BY
(tipo_de_recurso_id, ponto_de_apoio_id)`, com índice composto sobre o par. É a leitura mais fiel
ao PRD-07 §8 — "o saldo é sempre derivado dos lançamentos, nunca um número editável" — e ao §10
— "recontar os lançamentos devolve o mesmo número". _Alternativa descartada:_ tabela
`saldo_de_recurso` mantida em sincronia, que nesta fatia nasceria com `quantidade reservada`
sempre zero (a `Reserva` está fora) e abriria a possibilidade de divergir da fonte. Quando a
reserva chegar e o custo da agregação pesar, a projeção materializada entra como cache com
recontagem de conferência — decisão daquela fatia, não desta.

**2. Quantidade e moedas em `NUMERIC(12, 2)`.** Mesmo tipo já usado em `ValorDeReferencia`:
decimal exato, sem ponto flutuante, com teto de dez ordens de grandeza acima do Ciclo 01
(`RN-07-04`). A quantidade é decimal e não inteira porque a unidade do tipo pode ser fracionária
— duas horas e meia de hora-aula, meio quilo de insumo. _Alternativa descartada:_ quantidade
inteira, que forçaria a gestão a inventar unidade menor para cada tipo fracionário.

**3. Imutabilidade do lançamento por gatilho no banco.** `BEFORE UPDATE` e `BEFORE DELETE` sobre
`lancamento` que levantam exceção, no mesmo padrão de `consentimentos/modelo.py` e
`ponto_extra/modelo.py`, registrados por `event.listen` no `Base.metadata`. _Alternativa
descartada:_ recusa apenas na camada de regra, que não alcança quem escreve direto no banco — e
o livro-razão é justamente o lugar em que "ninguém edita" precisa valer para todos.

**4. O 405 é consequência de não haver rota de escrita, não uma recusa programada.** A API não
declara `PUT` nem `PATCH` sobre lançamento; o FastAPI responde **405** a método não previsto em
caminho que existe, que é o que o PRD-07 §9 descreve. A garantia de que nada altera um lançamento
é a da decisão 3, no banco. _Alternativa descartada:_ declarar a rota só para recusá-la, que
publicaria no OpenAPI um contrato que o PRD não pediu.

**5. Duas pastas, na fronteira do PRD-07 §8.** `livro_razao/` guarda o `Lancamento` e a
agregação do saldo; `aportes/` guarda o `Aporte`, a conversão em moedas e as duas rotas de
registro. O aporte depende do livro-razão, nunca o contrário — o lançamento não sabe o que o
originou além da chave estrangeira, e é isso que permite ao débito da aula, na fatia seguinte,
entrar pelo mesmo caminho.

**6. Enum com valor ainda inalcançável, no precedente do `ativo`.** `SituacaoDeRessarcimento`
nasce com `nao_se_aplica`, `em_aberto` e `ressarcido`, e nada nesta fatia produz `ressarcido` —
a operação é da fatia do ressarcimento. `OrigemDoRegistro` nasce com `gestao` e `pre_cadastro`,
ambas alcançáveis. Mesma escolha que a fatia 1 fez com o `ativo` do ponto de apoio: o esquema não
fecha a porta, e nenhuma regra lê o que ainda não existe.

**7. O comprovante segue o caminho da fila.** _Multipart_ com `UploadFile`, validação do
`content_type` contra PDF, JPG e PNG, gravação pela `PortaDeArmazenamento` e guarda de
referência, nome original, tipo e tamanho no `Aporte` — os mesmos quatro campos que
`SolicitacaoDeParticipacao` já guarda. Nenhuma rota desta fatia devolve o conteúdo.

**8. A conversão lê a vigência pela data do aporte.** `valor_em_moedas = quantidade × valor de
referência vigente em `data_do_aporte``, resolvido pela mesma comparação semiaberta da fatia 1, e
**gravado no aporte**. Gravar o resultado — em vez de recalcular na leitura — é o que torna o
aporte imune à abertura de vigência posterior (`RF-07-05`, PRD-07 §12).

**9. Um aporte homologado gera exatamente um lançamento de crédito**, como o PRD-07 §8 desenha
(`Aporte 1 ── 1 Lancamento`). O ajuste é lançamento próprio, com `natureza = ajuste` e referência
ao original; ele não altera nem substitui o crédito.

**10. A solicitação de origem é única por aporte.** `UniqueConstraint` sobre
`solicitacao_de_participacao_id`, para que a mesma declaração de pré-cadastro não seja homologada
duas vezes e credite em dobro (`RN-07-21`).

## Risks / Trade-offs

- **A agregação do saldo cresce com o livro-razão** → índice composto sobre
  `(tipo_de_recurso_id, ponto_de_apoio_id)` desde a migration; o volume do Ciclo 01 é de centenas
  de lançamentos, não milhões, e a projeção materializada fica disponível para a fatia da reserva
  se medir necessário.
- **Saldo derivado dispensa trava de concorrência agora, mas não depois** → dois aportes
  simultâneos não competem, porque ninguém lê-modifica-escreve um número. A reserva vai competir,
  e a trava é decisão da fatia dela, não desta — registrado aqui para não se perder.
- **O gatilho de imutabilidade impede corrigir dado errado até por migração** → é o efeito
  pretendido; a correção é o lançamento de ajuste, e o caminho existe nesta mesma fatia.
- **`exige_comprovante` nasce em tipos já cadastrados** → a coluna entra com `server_default`
  falso, de modo que nenhum tipo existente passe a recusar aporte de surpresa.
- **A absorção não passa por homologação e credita direto** → é a decisão `RN-07-35`, gravada no
  documento 04 §1. O contrapeso é a auditoria: o aporte por absorção nasce ressarcível e em
  aberto, e o ato fica registrado com autor e momento.

## Migration Plan

Uma migration Alembic, **aditiva**, sem reescrever dado existente:

1. `lancamento` — tabela nova, com os gatilhos de `UPDATE` e `DELETE` e o índice composto.
2. `aporte` — tabela nova, com as chaves estrangeiras para `persona`, `tipo_de_recurso`,
   `ponto_de_apoio`, `lancamento` e `solicitacao_de_participacao`, e a unicidade da decisão 10.
3. `tipo_de_recurso.exige_comprovante` — coluna nova, `NOT NULL` com `server_default` falso.

Rollback: `downgrade` derruba as duas tabelas e a coluna. Nenhum dado em produção depende delas
— o livro-razão entra em operação com esta fatia.

## Open Questions

Nenhuma que altere as specs, a abordagem ou o recorte das tarefas. A pergunta sobre o **ciclo de
vida da `Aula`**, registrada na proposal, trava a fatia da reserva e não esta.
