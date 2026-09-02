## Context

Ver `proposal.md` — Why. O que condiciona o desenho é o que a fatia 4 já deixou pronto:

- **`NecessidadeDeRecurso` é derivada, nunca gravada** (`openspec/specs/necessidade-de-recurso`):
  é o par `aula_id` + `tipo_de_recurso_id` de uma aula pendente de lastro, com a quantidade
  faltante recalculada da leitura. Não há linha para uma missão apontar.
- **`AporteDeclarado` já guarda esse par** sem vínculo, para a origem `necessidade`, e a enum
  `OrigemDaEscolhaDoAporte` já anota que a origem `missao` é de fatia futura.
- **`registrar_aporte()`** é o único caminho que credita: a homologação da declaração nasce ali,
  e é onde a conclusão da missão e o crédito dos selos precisam entrar.
- **O Poder Sustentador é derivado** dos lançamentos (`openspec/specs/poder-sustentador`); o
  nível de sustento segue o mesmo precedente.

## Goals / Non-Goals

**Goals:**

- Gravar a missão e o selo, e derivar o resto — quanto falta, coberto e nível de sustento.
- Um só ato de escrita conclui a missão e credita os selos: a homologação que já existe.

**Non-Goals:**

- Fila da gestão separada por modalidade (documento 14 §11): sem requisito de PRD.
- Nível 5 de sustento: pendência registrada no documento 09 e no PRD-14 §14.
- Job de vencimento: a missão vencida é derivada do prazo na leitura, não varrida por relógio.

## Decisions

**1. A missão aponta o par da necessidade, não uma linha.** `MissaoDoApoiador` guarda
`aula_id` + `tipo_de_recurso_id`, o mesmo par que `AporteDeclarado` já guarda, sem chave
estrangeira para uma necessidade que não existe como registro. A publicação confere que o par
está entre as necessidades derivadas no momento do ato; deixando de estar depois, a missão some
das listas (`RF-14-71`) sem nada a corrigir.
_Alternativa descartada:_ materializar `NecessidadeDeRecurso` — inverteria a decisão da fatia
que a fez derivada.

**2. O coberto da missão são os aportes homologados que vieram por ela.** `falta` = quantidade
da missão − soma das quantidades dos aportes homologados cuja declaração aponta esta missão.
É o que dá, no mesmo cálculo, o conjunto de **participantes** que recebem selo (`RF-14-66`) e a
garantia de que ninguém recebe crédito pelo que outro deu (`RN-14-34`).
_Alternativa descartada:_ derivar o coberto do faltante da necessidade — não distingue quem
cobriu, e o aporte que a gestão registra por fora passaria a "concluir" missão sem participante.

**3. Missão sem necessidade por trás não aparece, e não vira "concluída".** A leitura filtra
por três testes na ordem: situação `aberta`, prazo não vencido e par ainda entre as
necessidades derivadas. Sumir da lista não muda a situação gravada — quem tira a missão do
caminho é o Admin, pela despublicação (`RF-02-105`).

**4. A situação é gravada; o vencimento é lido.** `situacao` ∈ {`aberta`, `concluida`,
`despublicada`} é escrita por ato — homologação ou despublicação. **Vencida não é situação
gravada**: é `aberta` com prazo no passado, avaliado na leitura. Evita relógio que escreve, no
mesmo precedente do painel vivo.

**5. A conclusão e os selos entram em `registrar_aporte()`.** Homologada uma declaração de
origem `missao`, a mesma transação recalcula o que falta e, fechando o saldo, grava
`situacao = concluida` e insere um `SeloDoApoiador` por participante — o selo da missão e, com
mais de um participante, também o de mutirão. Um só ato, uma só transação: não há estado em que
a missão esteja fechada e o selo não creditado.
_Alternativa descartada:_ rota própria de conclusão para o Admin — criaria segundo ato humano
onde o PRD tem um (`RN-14-32`).

**6. `SeloDoApoiador` é somente inserção, com unicidade por (Apoiador, missão, selo).** Não há
rota de remoção (`RN-14-36`); o índice único impede o crédito duplo se a homologação for
repetida.

**7. O nível de sustento é derivado, como o Poder Sustentador.** Sai dos níveis de necessidade
das missões concluídas em que o Apoiador é participante, mais o primeiro aporte homologado para
o nível 1. Derivado, não regride por edição — só cresce (`RN-14-36`). Para no nível 4 (decisão
do fundador de 2026-09-01, pendência no documento 09).

**8. A missão declara o selo e a família a que ele pertence.** As quatro famílias do documento
14 §8 entram como enum; o Admin escolhe a família e escreve o nome do selo ao publicar. O selo
de mutirão é da família `ato` e é gravado pelo núcleo, não declarado.

**9. Rotas, na §9 do PRD-14 e na §9 do PRD-02.** `GET /v1/missoes-do-apoiador` responde às duas
personas pelo mesmo caminho: sem sessão devolve só as abertas; com sessão de Admin aceita o
filtro de situação e devolve o coberto (`RF-02-104`). `POST /v1/missoes-do-apoiador` e
`POST /v1/missoes-do-apoiador/{id}/despublicacao` exigem Admin; `GET /v1/eu/apoiador/sustento`
exige o Apoiador.

**10. Sem custo novo no livro-razão.** A missão não movimenta recurso: quem lança é o aporte
homologado, pelo caminho que `registrar_aporte()` já percorre. Publicar, despublicar e creditar
selo não geram lançamento.

## Risks / Trade-offs

- **A missão pode ficar aberta com a necessidade já suprida por fora** → some das listas pela
  decisão 3 e o Admin a despublica; nenhum aporte é aceito para missão que não aparece.
- **O coberto da missão pode divergir do faltante da necessidade** → é consequência da decisão
  2 e do que o PRD pede: a missão mede o que veio por ela; a necessidade mede o lastro.
- **Sem job de vencimento, missão vencida nunca muda de situação no banco** → a leitura é a
  autoridade, e a despublicação existe para o Admin encerrar o que ficou.
- **A escada parando no nível 4 frustra quem virou Mestre** → a tela diz que a próxima frente é
  virar Mestre, e a pendência está registrada.

## Migration Plan

Uma migração Alembic com as duas tabelas novas e a coluna `missao_do_apoiador_id` em
`aporte_declarado`, mais o valor `missao` na enum de origem da escolha. Nada é reescrito:
declaração antiga segue com a origem que tem. Sem missão publicada, a área Missões abre vazia e
o resto da App 08 não muda — o rollback é a migração para baixo.
