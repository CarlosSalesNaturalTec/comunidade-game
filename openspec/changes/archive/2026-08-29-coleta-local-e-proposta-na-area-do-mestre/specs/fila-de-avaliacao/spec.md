## ADDED Requirements

### Requirement: Quem propôs acompanha as próprias sugestões e propostas

O núcleo SHALL devolver à **persona autenticada** as sugestões e propostas que **ela mesma**
registrou, para que quem propõe acompanhe o status na fila única sem depender do Admin.
`RF-09-55` exige as duas metades — registrar e acompanhar —, e hoje só o Admin lê a fila.
(`RF-09-55`, `RF-01-25`, `RF-01-28`, 03 §§7, 12.2)

Cada registro SHALL sair com o **alvo** — atividade, trilha ou plataforma —, o **texto**, a
**situação** — recebida, em avaliação, adotada ou não adotada —, o **prazo** e a marca de
**em atraso** derivada dele, e, quando já houver desfecho, a **data** e, na não adotada, o
**motivo do retorno em linguagem simples**. É por esta leitura que o retorno chega a quem
propôs, **dentro da plataforma**: o núcleo NEVER SHALL enviar e-mail por causa dele.
(`RN-02-25`)

A consulta NEVER SHALL devolver sugestão de outro autor, nem o **parecer** interno da avaliação,
que é da leitura de Admin. Ela SHALL ser paginada como toda listagem do núcleo, e a leitura de
Admin da fila NEVER SHALL mudar por causa dela.

#### Scenario: O autor vê as próprias propostas em qualquer situação

- **WHEN** uma persona autenticada consulta as suas sugestões e propostas
- **THEN** o núcleo devolve as que ela registrou, com alvo, texto, situação e prazo

#### Scenario: A proposta não adotada devolve o motivo do retorno

- **WHEN** a lista inclui uma proposta concluída como não adotada
- **THEN** ela sai com a situação `não adotada`, o motivo do retorno em linguagem simples e a
  data do desfecho

#### Scenario: A proposta com prazo vencido sai marcada em atraso

- **WHEN** a lista inclui uma proposta sem desfecho cujo prazo de 7 dias já venceu
- **THEN** ela sai marcada em atraso, e a situação gravada continua sendo **recebida**

#### Scenario: A consulta não alcança proposta de outro autor

- **WHEN** uma persona consulta as suas propostas e há propostas de outras personas na fila
- **THEN** o núcleo devolve apenas as dela

#### Scenario: O parecer interno não sai por esta porta

- **WHEN** a lista inclui uma proposta já avaliada
- **THEN** o parecer da avaliação não aparece em campo algum: quem propôs recebe o motivo do
  retorno, não o parecer

#### Scenario: O retorno chega sem e-mail

- **WHEN** um Admin conclui a avaliação de uma proposta
- **THEN** quem propôs passa a ver o desfecho nesta leitura, e nenhum e-mail é enviado
