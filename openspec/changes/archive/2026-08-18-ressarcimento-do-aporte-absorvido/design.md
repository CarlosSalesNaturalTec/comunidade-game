## Context

O livro-razão inteiro já está no ar: `openspec/specs/livro-razao/`, `aporte/`,
`poder-sustentador/`, `reserva-de-recurso/` e `necessidade-de-recurso/` são o consolidado. Esta
fatia acrescenta uma capacidade e mexe em três pontos já consolidados — o saldo derivado, o
ajuste e o registro do aporte. Ver `proposal.md` para a motivação.

Três fatos do que já existe moldam as decisões abaixo:

- `Lancamento` é **somente inserção**, com gatilho de banco que recusa `UPDATE` e `DELETE` fora
  do ORM. Nada nesta fatia altera lançamento gravado.
- `poder_sustentador_de` já soma o crédito do aporte **mais os ajustes que o referenciam**. A
  reversão do ressarcimento entra por esse caminho sem tocar na derivação.
- `saldo_de` agrega `quantidade` sobre `lancamento` filtrando por tipo e ponto de apoio, e
  `disponivel_de` o consome dentro do `SELECT ... FOR UPDATE` do agendamento. Qualquer coisa
  que se acrescente a esse filtro entra num caminho quente e travado.

## Goals / Non-Goals

**Goals:**

- Reverter moedas sem reverter estoque, e sem alterar as duas derivações que já existem.
- Manter a receita destinada fora do lastro sem pagar por isso no caminho travado do
  agendamento.
- Registrar as duas decisões novas nos documentos-fonte antes do código.

**Non-Goals:**

- Rever a derivação do Poder Sustentador ou da prestação de contas — elas já leem o que precisam.
- Modelagem em dupla entrada: o documento 04 a mantém proposta, fora do Ciclo 01.
- Interface de gestão do ressarcimento — PRD-02 (App 03).

## Decisions

**1. A reversão é um ajuste de quantidade zero e moedas negativas.** O lançamento carrega as
duas grandezas; separá-las é o que permite devolver dinheiro sem desfazer a chegada de um bem já
consumido. Como `saldo_de` agrega `quantidade` e `poder_sustentador_de` agrega
`valor_em_moedas`, o ajuste cai exatamente onde deve e em lugar nenhum mais — sem uma linha de
mudança em nenhuma das duas.
_Alternativas:_ ajuste que reverte quantidade e moedas — derrubaria o saldo por um consumo que
aconteceu, podendo deixá-lo negativo. Campo `revertido` no aporte — número editável, contra
`RN-07-15`.

**2. A destinação é gravada no `Lancamento`, não lida por junção com o `Aporte`.** O saldo
precisa excluir o crédito de destinação ressarcimento (`RN-07-38`), e o filtro entra no caminho
travado do agendamento. Denormalizar segue o precedente explícito do PRD-07 §8, em que o crédito
já **herda o ponto de apoio** do aporte pelo mesmo motivo: manter o saldo derivável por colunas
locais. O ajuste herda a destinação do lançamento que referencia.
_Alternativas:_ junção `lancamento → aporte` dentro de `saldo_de` — uma junção a mais sob
`FOR UPDATE`, em toda reserva. Lançar a receita destinada com quantidade zero — esconderia a
exclusão numa convenção silenciosa, e o dado da quantidade se perderia.

**3. O teto é conferido contra a receita destinada declarada, dentro da transação.** O
`Ressarcimento` referencia o aporte que o financia (PRD-07 §8), e o saldo em aberto daquela
receita é o `valor_de_origem` dela menos a soma dos ressarcimentos já pagos contra ela. A
conferência acontece sob `SELECT ... FOR UPDATE` sobre os ressarcimentos daquela receita, no
mesmo padrão que `_bloquear_par` já usa na reserva — sem isso, dois Admins pagando ao mesmo
tempo estouram o teto.
_Alternativa:_ teto agregado sobre toda a receita destinada — mais flexível, mas deixaria sem
função o campo "receita destinada de origem" do §8.

**4. O ressarcimento é uma entidade própria, em módulo novo.** Ele tem ciclo, comprovante e
pagador próprios, e o `Aporte` já é a entidade mais carregada do domínio. `situacao_de_
ressarcimento` permanece no aporte, como a fatia dois a gravou — é o que a fila consulta —, e
passa a `ressarcido` no mesmo ato.

**5. Aporte já gravado não é reescrito pela migração.** `destinacao` nasce com _default_
`lastro`, o que é verdade para tudo que existe: nenhum aporte de ressarcimento foi registrado
ainda. `aula_id` nasce nulo — as absorções anteriores não declararam necessidade e não há como
inferi-la. `valor_de_origem` continua nulo onde já é nulo: a exigência vale para o registro
novo, e a migração não inventa número que ninguém declarou. Absorção de serviço já gravada tem
`situacao_de_ressarcimento` corrigida para `nao_se_aplica` pela migração — é aplicar a decisão
nova ao passado, não inventar dado.
_Alternativa:_ exigir `valor_de_origem` retroativamente — travaria o ressarcimento das absorções
que a decisão quer justamente alcançar.

**6. A absorção de serviço não é ressarcível.** Decisão nova, tomada nesta change e gravada nos
documentos antes do código. Ela abre exceção ao `RF-07-21` e resolve a contradição entre o
`RN-07-39`, que manda a tabela de referência fornecer o valor em reais, e o `RN-07-24`, que veda
converter moedas em reais. Quem absorve serviço dá tempo: não há desembolso a devolver, e o
reconhecimento fica no Poder Sustentador e no selo.

**7. As três rotas exigem persona; nenhuma é pública.** Comprovante e valor em reais nunca
saem por rota sem persona (PRD-07 §§10, 11), e o comprovante do ressarcimento entra no mesmo
regime de acesso restrito à gestão do comprovante do aporte, que já existe.

## Risks / Trade-offs

- **A destinação denormalizada pode divergir do aporte.** → Ela é gravada num único ponto, no
  ato do lançamento, e `Lancamento` é somente inserção: não há caminho de escrita que a mude
  depois. Um teste prova que crédito e aporte concordam.
- **O filtro novo no `saldo_de` mexe no caminho quente do agendamento.** → É uma coluna local
  numa consulta que já filtra por duas outras; sem junção nova. A suíte de reserva existente é o
  que prova que o comportamento não mudou para o caso comum.
- **Dois Admins ressarcindo contra a mesma receita ao mesmo tempo.** → `FOR UPDATE` sobre os
  ressarcimentos daquela receita antes de conferir o teto, no padrão que a reserva já usa.
- **`valor_de_origem` nulo em absorção antiga bloqueia o ressarcimento dela.** → Fica bloqueado
  mesmo, e é o certo: não se paga um valor que ninguém declarou. A correção é um ajuste da
  gestão, fora desta fatia.
- **A absorção de serviço perde a possibilidade de ressarcimento.** → É o efeito pretendido da
  decisão 6. O Poder Sustentador e o selo seguem contando o ato, que é o reconhecimento que o
  documento 04 §1 promete.

## Migration Plan

Uma migração Alembic, em passo único, sem reescrita de valor:

1. `aporte.destinacao` — `NOT NULL`, _default_ `lastro`.
2. `aporte.aula_id` — nulo, FK para `aula`.
3. `lancamento.destinacao` — `NOT NULL`, _default_ `lastro`, herdada do aporte no ato.
4. `ressarcimento` — tabela nova, com `aporte_id` único.
5. `aporte.situacao_de_ressarcimento` — `nao_se_aplica` onde `forma = absorcao` e a natureza do
   tipo é `servico`.

O passo 5 é o único que toca linha existente, e não altera lançamento algum — o gatilho de
imutabilidade do `lancamento` não é atravessado. _Rollback:_ derrubar a tabela e as três
colunas; nenhum lançamento foi emitido pela fatia até a primeira operação real.

## Open Questions

Nenhuma. As duas ambiguidades encontradas — o teto da receita destinada e o valor em reais da
absorção de serviço — foram levadas ao fundador e decididas antes deste artefato.
