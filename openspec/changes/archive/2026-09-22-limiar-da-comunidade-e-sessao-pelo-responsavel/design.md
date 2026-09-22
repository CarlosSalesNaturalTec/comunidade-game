## Context

Ver `proposal.md` — Why. O que já está consolidado e não se reabre: a comparação vive em
`autenticar_por_nick_e_descritor`, o limiar vigente de um ponto de apoio é o da medição mais
recente, e a recusa é única para todas as causas, no corpo **e no tempo**. Esta fatia acrescenta
um segundo caminho de resolução do limiar e um segundo tipo de confirmador, sem mudar nenhuma
das três coisas acima.

## Goals / Non-Goals

- **Goal**: o núcleo passa a reconhecer fora do encontro e a aceitar o responsável como
  confirmador, com escopo.
- **Non-Goal**: a App 05 e qualquer tela. Fatia seguinte.
- **Non-Goal**: a App 01, que não muda — mas cuja change precisa entrar **antes** desta.
- **Non-Goal**: rever quem mede o limiar, como se mede, ou a bancada.

## Decisions

**1. A ausência da aula é o discriminador, e não a chave de aplicação.** `aula_id` vira
opcional; presente, vale o caminho do encontro; ausente, o da comunidade.
_Alternativa descartada_: exigir a aula conforme a aplicação que chamou, para que a App 01 nunca
caísse calada no caminho errado. A capacidade `permissoes-e-escopo-de-comunidade` já determina
que a conferência **nunca** dependa de qual aplicação fez a chamada, e abrir exceção a isso para
proteger um cliente de si mesmo sai caro demais. O que fecha a janela é a **ordem** — a change
da App 01 entra antes — e o teste dela, que afirma o envio da aula.
_Alternativa descartada_: um campo discriminador explícito no corpo. Seria melhor API, mas
mudaria o contrato que a change da App 01 já está especificada para cumprir, acoplando as duas.

**2. O mais frouxo é `max`, sobre pontos de apoio ativos.** "Confere se couber no limiar de
algum espaço da comunidade" é `max` dos limiares vigentes. `PontoDeApoio.ativo` filtra: espaço
que a comunidade encerrou não empresta número.
_Alternativa descartada_: o mais recente da comunidade — mudaria sozinho quando outro espaço
remedisse, sem relação com a criança.

**3. O tempo constante se estende ao caminho novo.** A comparação já calcula distância contra um
_template_ de descarte para igualar o tempo quando o nick não existe. O caminho da comunidade
faz mais consultas que o da aula, então a resolução do limiar SHALL percorrer trabalho
equivalente nos dois — inclusive quando recusa por falta de vínculo ou de medição. É a parte
mais delicada da fatia, e é o que o cenário de tempo do delta cobre.

**4. O escopo do responsável é conferido na regra, não na rota.** A rota confere a matriz pelo
papel, como hoje; a regra que resolve o nick passa a receber quem confirma e a conferir o
vínculo. Assim a recusa por escopo nasce no mesmo lugar que a recusa por nick inexistente, e sai
idêntica a ela sem esforço de sincronização entre dois pontos do código.
_Alternativa descartada_: conferir na rota, antes de resolver o nick — separaria as duas recusas
em lugares diferentes, que é como se deixa uma divergir da outra.

**5. Operação nova, em vez de estender a do Mestre.** `confirmacao_de_identidade_do_guerreiro`
continua sendo a do Mestre e do Admin, sem escopo. O responsável recebe operação própria, com
escopo, seguindo a convenção que a matriz já usa (`aportes_seus`, `suas_turmas`,
`guerreiros_sob_sua_responsabilidade`).
_Alternativa descartada_: dar a mesma operação ao responsável e filtrar depois — daria, por um
descuido de ordem, confirmação sem escopo a quem não pode tê-la.

## Risks / Trade-offs

- **O limiar emprestado erra mais que o medido no lugar** → é o custo assumido na decisão do
  fundador, e o que o compensa é o responsável poder abrir a sessão quando a comparação recusa.
  Sem a fatia seguinte, esta sozinha deixa a criança sem porta em casa.
- **O tempo constante entre dois caminhos de custo diferente é difícil de garantir** → o cenário
  existe no delta e a conferência é por teste; se o desvio for grande, o caminho da aula absorve
  trabalho equivalente em vez de o da comunidade ser aliviado.
- **Escopo novo na matriz é superfície de autorização nova** → cenário próprio para papel certo
  com vínculo ausente, e para vínculo encerrado.

## Migration Plan

Sem migração de banco: nenhuma entidade nasce, e `VinculoResponsavel` já guarda o vínculo com
`fim` nulo como vigente. Tornar `aula_id` opcional só amplia o que a rota aceita, então clientes
existentes seguem funcionando. Rollback é reverter o _commit_.

**Ordem obrigatória**: a change `2026-09-21-aula-na-entrada-e-erro-de-camada-legivel` entra
antes. Enquanto a App 01 não enviar a aula, tornar o campo opcional a faria comparar pelo limiar
da comunidade sem avisar ninguém.
