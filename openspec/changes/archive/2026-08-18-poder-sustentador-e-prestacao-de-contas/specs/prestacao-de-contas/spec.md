## Purpose

O painel público do que a plataforma movimentou: quanto entrou, de quem veio e em que atividade
foi consumido, sempre em moedas. É a transparência que o projeto promete a quem sustenta e a
quem observa de fora, lida direto do livro-razão e sem nenhum fechamento periódico.

## ADDED Requirements

### Requirement: A prestação de contas é painel vivo, sem fechamento periódico

O núcleo SHALL derivar a prestação de contas dos **lançamentos** no momento da leitura, sem
período fechado, sem apuração agendada e sem número consolidado guardado à parte. Um lançamento
novo SHALL aparecer na leitura seguinte **sem ato humano** de fechamento ou publicação.
(`RF-07-16`, `RN-07-31`, `RN-07-15`, PRD-07 §§8, 12)

#### Scenario: O aporte novo aparece na leitura seguinte

- **WHEN** um aporte é registrado e creditado, e a prestação de contas é lida em seguida
- **THEN** o movimentado já inclui aquele crédito, sem nenhum ato de fechamento

#### Scenario: Não há período a fechar

- **WHEN** a prestação de contas é lida
- **THEN** a resposta é o estado corrente do livro-razão, sem exigir competência, mês ou ciclo
  fechado

#### Scenario: A recontagem devolve o mesmo movimentado

- **WHEN** o movimentado é recalculado a partir dos lançamentos
- **THEN** o número devolvido é igual ao anterior

### Requirement: O movimentado sai por provedor, por aula e por comunidade, em moedas

O núcleo SHALL devolver em `GET /prestacao-de-contas` o **movimentado total** e o movimentado
**por provedor**, em moedas. O núcleo SHALL devolver em `GET /prestacao-de-contas/aulas` o
**consumo por aula** e **por comunidade**, em moedas.

O consumo de uma aula SHALL ser lido dos **débitos** que aquela aula gerou, pelo valor que cada
débito gravou no ato — NÃO SHALL ser recalculado pela tabela de referência vigente na data da
leitura, sob pena de discordar do que o livro-razão registrou. A comunidade de uma aula SHALL ser
a do ponto de apoio em que ela acontece. (`RF-07-16`, `RN-07-05`, `RN-07-33`, `RN-07-36`,
PRD-07 §§8, 9)

#### Scenario: O movimentado total soma os créditos do livro-razão

- **WHEN** dois provedores creditaram 1,50 e 2,50 moedas
- **THEN** o movimentado total é 4,00 e o movimentado por provedor traz 1,50 para um e 2,50 para
  o outro

#### Scenario: O consumo da aula é o que o débito gravou

- **WHEN** uma aula deu baixa quando o valor de referência do tipo era 0,50, e depois o valor de
  referência passou a 0,80
- **THEN** o consumo daquela aula continua o que o débito gravou, e não o que a tabela corrente
  daria

#### Scenario: O consumo agrega por comunidade

- **WHEN** duas aulas de pontos de apoio de comunidades diferentes deram baixa
- **THEN** o consumo sai separado por comunidade, cada aula na comunidade do ponto de apoio dela

#### Scenario: Aula sem baixa não aparece com consumo

- **WHEN** uma aula está agendada, com reservas, e ainda não foi realizada
- **THEN** ela não figura com consumo algum: só o débito da baixa move a prestação de contas

### Requirement: A leitura da prestação de contas dispensa credencial de persona, nunca a chave

O núcleo SHALL responder às rotas desta capacidade **sem token de sessão**, e SHALL exigir em
todas elas a **chave de aplicação válida**, como em toda rota de dados sob `/v1`. A recusa por
chave ausente, inválida ou revogada SHALL ser o **401** indistinto que a capacidade
`chave-de-aplicacao` já define. Nenhuma rota desta capacidade SHALL escrever. (`RF-01-02`,
`RN-01-32`, `RN-01-33`, PRD-07 §10)

#### Scenario: Visitante sem persona lê a prestação de contas

- **WHEN** uma consulta chega com chave de aplicação válida e sem token de sessão
- **THEN** o núcleo responde com o movimentado

#### Scenario: Sem chave a rota não responde

- **WHEN** uma consulta chega sem chave de aplicação válida
- **THEN** o núcleo responde 401, sem distinguir chave ausente de chave revogada

### Requirement: Nenhuma saída pública traz reais, comprovante nem Guerreiro(a)

Nenhuma resposta desta capacidade SHALL trazer **valor em reais**, nem em campo auxiliar, nem
dado bancário, nem o **comprovante** de aporte ou de ressarcimento. Nenhuma resposta SHALL
identificar **Guerreiro(a)**: a prestação de contas alcança provedores, aulas e comunidades, e a
criança não figura nela por nome, nick, avatar nem identificador. (`RN-07-05`, `RN-07-13`,
`RN-07-20`, PRD-07 §§10, 11, invariantes 10 e 16 do documento 99 §6)

#### Scenario: O valor de origem em reais não atravessa

- **WHEN** os aportes somados têm valor de origem em reais registrado
- **THEN** a resposta traz apenas moedas, sem nenhum campo com o valor em reais

#### Scenario: O comprovante não é servido

- **WHEN** um aporte somado tem comprovante anexado
- **THEN** a resposta não traz o comprovante nem referência que dê acesso a ele

#### Scenario: A criança não aparece na prestação de contas

- **WHEN** o consumo de uma aula que teve participantes é lido
- **THEN** a resposta traz a aula, a comunidade e as moedas, e nenhum dado de Guerreiro(a)
