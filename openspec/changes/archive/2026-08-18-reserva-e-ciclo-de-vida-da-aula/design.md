## Context

Ver `proposal.md` — Why. O que o código já tem, e que condiciona o desenho:

- `Lancamento` é somente inserção, com gatilho no banco, e o saldo é **agregação** sobre ele —
  não há tabela de saldo (change `aporte-lancamento-e-saldo`, Decisions 1 e 3).
- `Aula` tem comunidade, ponto de apoio, início e fim; **não tem situação, não tem recursos
  declarados e não tem rota** — `agendar_aula()` é regra alcançável só por teste.
- `Resultado` liga Guerreiro(a) e atividade; **não conhece aula** e não tem rota.
- `aportes.regra` credita pela vigência da tabela na data do aporte e chama `lancar_credito`.

O `PontoDeApoio` é a dimensão do saldo, e a `Aula` já o declara desde a fatia 1 — é por ele que
a reserva encontra o escopo certo.

## Goals / Non-Goals

**Goals:**

- Fazer o saldo **descer**: a fatia 2 construiu o crédito, esta constrói o consumo.
- Manter o saldo derivado como única verdade, mesmo com reserva no meio.
- Dar à `Aula` o ciclo de vida que o PRD-01 §8 já descrevia e o núcleo nunca teve.

**Non-Goals:**

- Projeção materializada de saldo. Segue agregação, como na fatia 2.
- Concorrência distribuída. O Ciclo 01 opera em um processo por comunidade, e a garantia é a
  transação do banco.
- Qualquer leitura da falta. `GET /necessidades` é da fatia seguinte.

## Decisions

**1. A declaração do recurso e a reserva dele são entidades separadas.** Nasce
`recurso_declarado_da_aula` (aula, tipo de recurso, quantidade) e, à parte, `reserva` (aula,
tipo, quantidade, ponto de apoio, estado). A declaração é o que a aula **precisa** e vive desde
o agendamento; a reserva é o que ela **comprometeu** e só existe quando há lastro. É o que
permite a uma aula pendente de lastro lembrar o que lhe falta, para o aporte fechá-la depois.
_Alternativa descartada:_ um quarto estado "pendente" na `reserva` — o PRD-07 §8 declara
exatamente três (reservada, consumida, liberada), e inventar valor de enumeração é criar regra.

**2. A quantidade reservada é agregação sobre `reserva`, como o saldo é sobre `lancamento`.**
`disponivel(tipo, ponto) = saldo(tipo, ponto) − SUM(reserva.quantidade WHERE estado =
reservada)`. Nenhum número guardado, nenhuma sincronia a manter, e recontar devolve o mesmo
resultado. Índice composto sobre `(tipo_de_recurso_id, ponto_de_apoio_id, estado)`.
_Alternativa descartada:_ tabela `saldo_de_recurso` com as duas colunas do PRD-07 §8 — o §8
descreve o conceito, não a forma de guardar, e o §10 exige que recontar devolva o mesmo número.

**3. A reserva NÃO é lançamento.** Ela não entra em `lancamento` em estado algum. Só o débito da
baixa entra, e é ele que faz o saldo cair. _Alternativa descartada:_ lançamento de natureza
"reserva", que exigiria excluí-lo da soma do saldo em toda consulta e corromperia a leitura de
que "crédito soma, débito subtrai, ajuste entra pelo sinal".

**4. A reserva é tudo-ou-nada, avaliada e gravada na mesma transação.** O agendamento lê a
disponível de cada tipo declarado e, faltando qualquer parcela, não grava reserva alguma
(proposal — decisões derivadas 1). A leitura e a escrita correm na mesma transação, com
`SELECT ... FOR UPDATE` sobre as linhas de `lancamento` e `reserva` do par tipo/ponto de apoio,
para que dois agendamentos simultâneos não reservem o mesmo saldo. _Alternativa descartada:_
checar depois de gravar e desfazer, que deixaria janela de saldo negativo.

**5. A confirmação automática mora na regra do aporte, não na do agendamento.** Depois de
`lancar_credito`, `aportes.regra` varre as aulas pendentes de lastro **daquele ponto de apoio**,
ordenadas pelo horário inicial, e confirma as que couberem (`RN-07-37`). Fica no aporte porque é
o crédito que muda o mundo; o agendamento só lê o que já existe. _Alternativa descartada:_
tarefa periódica, que confirmaria a aula em momento sem autor e sem ato, contra a auditabilidade
que o livro-razão exige.

**6. `POST /aulas/{id}/reservas` é idempotente e serve o caminho explícito.** Ela tenta a reserva
de uma aula pendente de lastro; havendo disponível, confirma a aula como o aporte faria. Aula já
confirmada devolve o estado corrente sem duplicar reserva. É a retentativa da PRD-07 §9 e a
saída para aula cujos recursos foram declarados depois do agendamento. _Alternativa descartada:_
rota que aceita a lista de recursos no corpo, que duplicaria a declaração feita no agendamento.

**7. O lançamento da atividade é uma operação, não N.** `POST /aulas/{id}/lancamentos` recebe os
resultados de todos os participantes e, na mesma transação, grava os `Resultado`, converte cada
reserva em débito e leva a aula a **realizada**. É o que o documento 04 §1 chama de "o mesmo ato
que registra o resultado de cada participante". _Alternativa descartada:_ manter
`registrar_resultado` como ato individual e dar baixa no primeiro deles, que faria o saldo
depender da ordem de chegada dos resultados.

**8. `Resultado.aula_id` nasce obrigatório, e a migração é destrutiva por vacuidade.** A tabela
`resultado` não tem linha em ambiente algum além dos testes — o núcleo nunca expôs rota que a
escrevesse. A coluna entra `NOT NULL` sem etapa de preenchimento. _Alternativa descartada:_
coluna anulável com preenchimento posterior, que carregaria para sempre um caso que nunca
existiu.

**9. A situação da aula é enumeração fechada de cinco valores**, no padrão `native_enum=False`
já usado em `NaturezaDoLancamento` e `DesfechoDoResultado`. `prevista` existe no PRD-01 §8 e
nasce **sem transição que a produza**: com o agendamento sempre avaliando o lastro, toda aula
nasce `confirmada` ou `pendente_de_lastro`. O valor fica declarado e sem uso, como o `ativo` do
ponto de apoio na fatia 1, em vez de ser suprimido do modelo que o PRD declara.

**10. O cancelamento confere o vínculo de comunidade, sem campo novo.** Mestre cancela se tiver
vínculo com a comunidade da aula — a mesma conferência que `equipes` e `quiz` já fazem. O núcleo
não guarda "Mestre responsável pela aula": o PRD-02 §8 lista o campo, o PRD-01 §8 não.

## Risks / Trade-offs

- **Agregação de reserva sobre agregação de lançamento** → duas somas por tipo declarado a cada
  agendamento. Com o volume do Ciclo 01 — dezenas de aulas por comunidade — é irrelevante, e o
  índice composto cobre as duas. A projeção materializada entra quando o custo aparecer, com
  recontagem de conferência.
- **`FOR UPDATE` sobre `lancamento`** → serializa agendamentos concorrentes no mesmo par
  tipo/ponto de apoio. É o preço de não reservar duas vezes o mesmo saldo, e o escopo do bloqueio
  é o par, não a tabela.
- **A aula pendente de lastro fica sem saída nesta fatia** → só o `POST /aulas/{id}/reservas` a
  destrava, e só se alguém aportar por fora. É recorte declarado na proposal, não defeito.
- **`Resultado` passa a exigir aula** → nenhum chamador existe fora dos testes, mas os testes de
  `test_resultado.py` e os de pontuação que criam resultado precisam passar a criar aula antes.
- **A ordem de desempate é derivada, não normativa** → se a operação mostrar que a ordem certa é
  outra, muda-se aqui e no spec de `aporte`, sem tocar em PRD.

## Migration Plan

Uma migração do Alembic, na cabeça atual:

1. `CREATE TABLE recurso_declarado_da_aula` e `CREATE TABLE reserva`, com o índice composto da
   Decisions 2.
2. `ALTER TABLE aula ADD COLUMN situacao` — `NOT NULL`, com `server_default` `'confirmada'` para
   as linhas existentes (aula sem recurso declarado é aula confirmada, Decisions 4), removido o
   default depois do preenchimento.
3. `ALTER TABLE aula ADD COLUMN cancelamento_motivo` anulável, e a autoria do cancelamento pela
   trilha de auditoria já existente.
4. `ALTER TABLE resultado ADD COLUMN aula_id NOT NULL` (Decisions 8).

`downgrade` derruba as duas tabelas e as três colunas. Não há dado a preservar: nenhuma das
entidades tocadas tem linha em produção — o Ciclo 01 ainda não entrou no ar.
