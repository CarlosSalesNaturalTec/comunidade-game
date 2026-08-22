## Context

Ver `proposal.md` — Why. O que já está consolidado e esta fatia apenas estende:
`openspec/specs/persona-e-credencial/spec.md` (atributo nick, unicidade global, vedação a
descobrir nick) e `openspec/specs/fila-de-avaliacao/spec.md` (solicitação de participação).
A restrição de alcance é o coração da fatia: o nick de adulto já é público no card da vitrine,
o de criança é informação que só a família cede.

## Goals / Non-Goals

**Goals:**

- Uma única conferência de disponibilidade, servindo as duas portas em que o adulto escolhe.
- Unicidade global apurada na gravação, sem depender da conferência.

**Non-Goals:**

- Reservar nick de Guerreiro(a) ou mexer no caminho de cadastro da criança (PRD-04).
- Rota que grava o avatar do Mestre — é do PRD-09; aqui nasce só o atributo.

## Decisions

**Uma rota pública de conferência, não duas.** `GET /v1/nicks/disponibilidade`, com chave de
aplicação e sem credencial de persona, serve o pré-cadastro e a tela do adulto autenticado. A
resposta é a mesma nos dois casos porque o alcance é o mesmo — restringir por papel de quem
pergunta seria justamente o que a spec passou a proibir. Alternativa descartada: uma rota
pública e outra autenticada, que duplicaria a regra sem mudar a resposta.

**A reserva não é estado novo: é o `prazo` que a solicitação já tem.** `EmAvaliacao` grava
`prazo = envio + 7 dias` e a fila já deriva o atraso de `decidido_em is None and prazo < agora`
(`RN-01-49`). O nick reservado é o complemento exato disso — `decidido_em is None and prazo >=
agora` —, então a reserva sai derivada, sem coluna de vencimento, sem job de expiração e sem
tabela nova. Alternativa descartada: entidade `ReservaDeNick` com vencimento próprio, que
duplicaria um prazo que já existe e poderia divergir dele.

**Rota simétrica para o Mestre.** `PUT /v1/eu/mestre/identidade`, ao lado do
`PUT /v1/eu/apoiador/identidade` que o PRD-01 §9 já declara. Alternativa descartada: uma rota
única `PUT /v1/eu/identidade` derivando o papel da sessão — mais enxuta, mas renomearia rota
já declarada no PRD, o que é churn maior do que somar uma irmã.

**A colisão na gravação responde 422**, nomeando o campo `nick`, como toda recusa de campo
inválido em `convencoes-da-api`. A mensagem NÃO diz de quem é o nick nem de que papel — é o que
mantém a recusa indistinguível.

**A reserva do pré-cadastro não alcança a criança.** A reserva vale na conferência de adulto; a
unicidade da gravação corre contra personas, e reserva não é persona. Um Guerreiro(a) cadastrado
com um nick reservado leva o nick, e o Apoiador cai na colisão já prevista, resolvida pelo Admin
na change de cadastro de personas. Alternativa descartada pelo fundador: fazer a reserva barrar
o cadastro da criança, o que faria o cadastro de um Guerreiro(a) falhar por causa de um
formulário público que qualquer pessoa envia.

**A unicidade global já está pronta; o que falta é a caixa.** `Nick` é tabela própria com
índice único em `valor`, alcançando qualquer papel — o Mestre já entra sem migração, e
`Persona.avatar` também já existe para qualquer papel. O que muda é tornar o índice
**insensível a caixa**: hoje "Zeferina" e "zeferina" seriam nicks distintos, e a conferência
viraria teatro.

## Risks / Trade-offs

**A conferência pode dar disponível e a gravação recusar** — é aceito por decisão do fundador,
e é exatamente o caso em que o nick pretendido pertence a uma criança. Mitigação: a recusa é
tratada pelo Admin, por contato fora da plataforma, na change de cadastro de personas; nenhuma
tela promete que o disponível é definitivo.

**A reserva pública de sete dias é vetor de negação** — um visitante pode enviar solicitações
para reservar nicks cobiçados. Mitigação: o freio por origem de `RF-01-65` já limita o envio do
formulário a 3 por hora com atraso progressivo, e a reserva expira sozinha. Não se acrescenta
trava nova aqui.

**Persona de adulto sem nick passa a existir** — toda superfície pública que exibe adulto
precisa lidar com a ausência. Mitigação: nesta fatia o núcleo apenas permite o estado; quem
consome (card do Apoiador, card do Mestre) trata a ausência nas fatias das aplicações.

## Migration Plan

Migração aditiva e curta, porque o modelo já cobre a maior parte: `Nick` e `Persona.avatar` já
alcançam qualquer papel, e o `prazo` da solicitação já existe. Muda apenas o índice único de
`nick.valor`, que passa a ser insensível a caixa, e nasce a coluna `nick` em
`solicitacao_de_participacao`, nula. Nenhuma persona existente muda de estado. Rollback é a
migração inversa; o único cuidado é que, se dois nicks que diferem só na caixa já existirem,
o índice novo falha — conferir antes de aplicar em produção.
