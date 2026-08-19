## Context

Ver `proposal.md` — Why. O que o desenho precisa saber do estado atual:

- `TipoDeRecurso.natureza` já existe com as quatro naturezas (`recursos/modelo.py`), mas
  `duravel` é hoje **só rótulo**: a única leitura de natureza fora dos modelos é
  `aportes/regra.py:21`, que agrupa consumível, durável e financeiro para exigir valor de
  origem. Nem `reservas/regra.py` nem `catalogo_avulso/regra.py` a consultam.
- O agendamento valida os recursos declarados em `aulas/regra.py:72-83`, **antes** de criar a
  `Aula`, e só depois chama `tentar_reservar_recursos`, cujo retorno decide entre `confirmada` e
  `pendente_de_lastro`.
- `PontoDeApoio.responsavel_id` já existe e é nulo até a designação (`ponto-de-apoio`).
- A imutabilidade de histórico já tem precedente consolidado no `Lancamento`
  (`livro-razao`): somente inserção, recusada a alterar também fora do ORM.

## Goals / Non-Goals

**Goals:**

- Dar comportamento à natureza `durável`: saldo inerte, com as duas recusas que o guardam.
- Entregar o tombamento e a ficha de vida com a imutabilidade que o `Lancamento` já pratica.
- Garantir, por construção, que nenhum caminho de código transforme perda ou dano em débito.

**Non-Goals:**

- Não introduz dimensão nova no `SaldoDeRecurso`: o saldo durável continua derivado dos
  lançamentos como qualquer outro — apenas ninguém o consome.
- Não modela empréstimo, retirada, devolução nem transferência (`RN-07-11`).
- Não toca `necessidades/regra.py`: tipo durável nunca chega a ser declarado por aula, logo
  nunca produz necessidade.

## Decisions

**1. A recusa do tipo durável no agendamento entra em `aulas/regra.py`, não em
`reservas/regra.py`.** `tentar_reservar_recursos` devolve `bool`, e `False` significa "pendente
de lastro" — semântica errada para a natureza, que é recusa definitiva com **422**. A validação
entra no laço de `recursos_declarados` que já existe em `aulas/regra.py:72-83`, ao lado das
recusas de tipo inexistente e quantidade não positiva, antes de a `Aula` ser criada. É o que
faz o cenário "tipo durável não vira aula pendente de lastro" sair de graça.
_Alternativa descartada:_ recusar dentro de `tentar_reservar_recursos` — obrigaria a distinguir
dois motivos de falha num retorno booleano.

**2. A ficha de vida é entidade filha `AnotacaoDaFichaDeVida`, somente inserção.** O PRD-07 §8
a descreve como atributo do `ItemPatrimonial`, mas o conteúdo — "quem cuidou dele e as perdas e
danos anotados" — é histórico, e histórico em coluna não se audita. Segue o padrão do
`Lancamento`: sem rota de alteração nem de remoção, e a mesma trava de banco que o `livro-razao`
já usa fora do ORM.
_Alternativa descartada:_ campo JSON no item — perde autoria por anotação e a garantia de
somente inserção.

**3. O estado de conservação vive no `ItemPatrimonial` e é reescrito pela anotação.** A ficha
guarda o estado **apurado em cada anotação**, imutável; o item guarda o **corrente**, derivável
da última anotação. A redundância é deliberada: a leitura do acervo por comunidade não pode
depender de subconsulta por item.

**4. O responsável não é coluna do item — é junção com `PontoDeApoio.responsavel_id`.** É o que
faz a troca do responsável alcançar todos os exemplares sem escrita alguma, como o `RN-07-10`
exige ("a responsabilidade sobrevive à troca de turma e de Mestre"). Corrige o PRD-07 §8, que o
listava como atributo do item.
_Alternativa descartada:_ copiar o responsável no tombamento — congelaria o valor e exigiria
varredura a cada troca.

**5. O tombo é único por ponto de apoio, por índice composto no banco.** `UNIQUE
(ponto_de_apoio_id, numero_de_tombo)`. Único globalmente exigiria coordenação entre pontos de
apoio que a gestão não tem; único por item não seria unicidade alguma.

**6. O teto do aporte é conferido sob o mesmo bloqueio que a reserva já usa.** O tombamento lê
`COUNT(*)` dos itens do aporte com `SELECT ... FOR UPDATE` sobre o aporte, à imagem do
`_bloquear_par` de `reservas/regra.py`, para que dois tombamentos concorrentes não passem o
teto juntos. Item sem aporte de origem não entra na contagem.

**7. Perda e dano não têm caminho para débito porque não há caminho a construir.** A anotação
não chama `livro_razao`, não chama `ponto_extra` e não recebe Guerreiro(a) como parâmetro. O
teste que fixa o `RF-07-48` verifica a ausência: depois da anotação, nenhum `Lancamento` novo e
nenhum `PontoExtra` alterado.

**8. Rotas.** `POST /v1/itens-patrimoniais` (Admin), `GET /v1/itens-patrimoniais` (gestão,
filtrada por comunidade) e `POST /v1/itens-patrimoniais/{id}/ficha-de-vida` (Admin ou Mestre).
A rota da anotação é filha do item, como `/aulas/{id}/trocas` é filha da aula — a anotação não
existe sem o exemplar. Entram na §9 do PRD-07, hoje sem rota de patrimônio alguma.

## Risks / Trade-offs

- **A decisão 1 muda comportamento de uma rota já entregue** (o agendamento passa a ter um 422
  novo) → nenhum teste da suíte usa `duravel` (zero ocorrências em `backend/tests/`), e nenhum
  tipo durável existe em fixture; o caminho novo não cruza nenhum caso verde.
- **Saldo durável fica sem consumidor algum** e cresce sem nunca baixar → é o efeito pretendido
  pelo `RN-07-07`, e a conferência de inventário (`RF-07-20`, fatia futura) é o instrumento que
  o confronta com os itens tombados. Até lá, `COUNT(ItemPatrimonial)` contra a quantidade
  aportada é a única aferição, e ela é derivável.
- **Tipo cadastrado com a natureza errada trava a operação** — um "livro" único marcado durável
  impediria a baixa definitiva da linha Alpha → é cadastro da gestão, registrado na proposal:
  livro Alpha consumível, livro Include I durável. A recusa no cadastro do item de catálogo
  (decisão 3 da proposal) faz o erro aparecer cedo, e não em produção.

## Migration Plan

1. Migração Alembic: `item_patrimonial` (com `UNIQUE (ponto_de_apoio_id, numero_de_tombo)` e
   índice por ponto de apoio) e `anotacao_da_ficha_de_vida`, com a trava de somente inserção nos
   mesmos moldes da do `lancamento`.
2. Nenhum dado existente muda: as duas recusas incidem sobre caminhos que nenhum registro atual
   percorre, e não há tipo de natureza durável cadastrado.
3. Rollback é a queda das duas tabelas e a remoção das duas validações — sem perda de dado
   anterior à fatia.
