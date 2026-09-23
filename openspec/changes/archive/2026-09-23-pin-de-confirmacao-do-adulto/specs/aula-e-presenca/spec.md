## ADDED Requirements

### Requirement: A presença confirmada sem rede sincroniza pelo nick, sem abrir sessão

O núcleo SHALL aceitar, pela rota `POST /v1/aulas/{id}/presencas/sem-rede`, a presença que o
App 01 confirmou **sem rede**: o corpo traz o **nick** do Guerreiro(a) e a **hora do fato**, e
nada mais. A rota SHALL exigir a **chave do App 01** e o **Mestre ou Admin da sessão de
trabalho**, com PIN cadastrado; a conferência do PIN já aconteceu no aparelho, contra o
verificador desse mesmo adulto. A presença SHALL ser gravada no modo **confirmação**, com esse
adulto como **quem confirmou** e com a hora do fato recebida.

A rota NEVER SHALL abrir sessão do Guerreiro(a): sem rede não se abre caminho das trilhas, e a
sincronização não pode abrir o que a queda não abriu. Nick que não resolve a um Guerreiro(a)
SHALL ser recusado com **401**, indistinguível da recusa por nick de outro papel, como na
confirmação. Valem sem alteração a unicidade por aula e Guerreiro(a), com o reenvio devolvido
sem erro, e a recusa de presença em comunidade alheia. (`RF-04-23`, `RF-04-25`, `RN-04-13`,
`RN-04-38`, `RN-01-22`, PRD-04 §9)

#### Scenario: A presença da fila é registrada com quem confirmou

- **WHEN** o Mestre da sessão de trabalho sincroniza a presença de um nick existente com a hora
  do fato das 14h
- **THEN** o núcleo grava a presença por confirmação, com o Mestre como confirmador e a hora das
  14h, e nenhuma sessão de Guerreiro(a) é aberta

#### Scenario: O reenvio não duplica

- **WHEN** a mesma presença da fila chega duas vezes
- **THEN** o núcleo mantém um único registro e não responde erro

#### Scenario: Nick que não resolve é recusado sem revelar o motivo

- **WHEN** a fila traz um nick inexistente ou de um Mestre
- **THEN** o núcleo responde 401, com o mesmo código e a mesma mensagem nos dois casos

#### Scenario: Só o App 01 sincroniza

- **WHEN** o pedido chega com a chave de outra aplicação
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Adulto sem PIN cadastrado não sincroniza

- **WHEN** o adulto da sessão de trabalho não tem PIN cadastrado
- **THEN** o núcleo responde o erro de PIN não cadastrado e nada é gravado
