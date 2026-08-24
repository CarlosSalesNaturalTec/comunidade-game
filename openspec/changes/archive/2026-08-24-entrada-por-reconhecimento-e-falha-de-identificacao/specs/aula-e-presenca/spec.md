## ADDED Requirements

### Requirement: A App 01 registra a presença por reconhecimento sob a sessão de trabalho

O núcleo SHALL aceitar o registro de presença no modo **reconhecimento** quando a chave de
aplicação declarar a **App 01** e quem estiver em sessão for o **Mestre ou o Admin da sessão de
trabalho do aparelho**. A presença assim gravada SHALL ficar **sem confirmador**: a sessão de
trabalho autentica a escrita e NEVER SHALL constar como quem confirmou, pela mesma distinção que
o autocadastro do encontro já observa. O Guerreiro(a) NEVER SHALL ganhar operação de escrita de
presença na matriz de permissões — a presença é fato do encontro, não ato dele.

A mesma rota SHALL continuar aceitando o modo **confirmação** pela App 01, gravando quem
confirmou. Permanecem valendo, sem alteração, a unicidade por aula e Guerreiro(a) e a recusa de
presença em comunidade alheia. (`RF-04-18`, `RF-04-21`, `RF-01-20`, `RF-01-03`, PRD-04 §9,
documento 09, 2026-08-24)

#### Scenario: A entrada por reconhecimento grava a presença sem confirmador

- **WHEN** a App 01, na sessão de trabalho do aparelho, registra a presença de um Guerreiro(a)
  reconhecido na chegada
- **THEN** o núcleo grava a presença com modo reconhecimento e sem confirmador

#### Scenario: A confirmação humana pela App 01 grava quem confirmou

- **WHEN** a App 01 registra, no modo confirmação, a presença de um Guerreiro(a) cuja
  identificação falhou
- **THEN** o núcleo grava a presença com modo confirmação e o adulto da sessão de trabalho como
  confirmador

#### Scenario: A sessão de trabalho não vira autora da presença

- **WHEN** se lê uma presença gravada por reconhecimento pela App 01
- **THEN** ela não aponta confirmador algum, ainda que a escrita tenha sido autenticada por um
  Mestre ou Admin

#### Scenario: O Guerreiro(a) não alcança a rota por conta própria

- **WHEN** um Guerreiro(a) em sessão tenta registrar a própria presença
- **THEN** o núcleo recusa, porque nenhuma operação de presença lhe é concedida na matriz

### Requirement: A presença já registrada é devolvida, e é a aplicação que avisa

O núcleo SHALL responder ao reenvio da presença de um par aula e Guerreiro(a) já registrado
**devolvendo o registro existente**, sem duplicar, sem alterá-lo e **sem erro** — tanto para a
criança que volta à porta no mesmo encontro quanto para o reenvio da fila local. O núcleo NEVER
SHALL distinguir os dois casos por código de resposta: a resposta SHALL permitir que o cliente
reconheça o registro anterior pelo **momento do fato** já gravado.

Avisar a criança de que a presença dela já constava é comportamento da **aplicação**, não do
núcleo. (`RF-04-19`, `RF-01-20`, PRD-01 §10, PRD-04 §§5.4, 9, documento 09, 2026-08-24)

#### Scenario: A criança que volta à porta no mesmo encontro

- **WHEN** chega a presença de um Guerreiro(a) que já a tem naquela aula
- **THEN** o núcleo devolve o registro existente, com o modo e o momento do fato originais, e
  nada é gravado

#### Scenario: O momento do fato original é preservado

- **WHEN** o reenvio traz um momento do fato diferente do gravado
- **THEN** o núcleo mantém o momento original e o devolve, sem sobrescrevê-lo

## MODIFIED Requirements

### Requirement: O Mestre registra presença apenas por confirmação

O núcleo SHALL aceitar do **Mestre** o registro de presença de um Guerreiro(a) na aula
**somente no modo confirmação**, gravando-o como quem confirmou. O modo **reconhecimento** é da
**App 01**, e a recusa SHALL ser decidida pela **aplicação declarada na chave**, não pela rota
inteira nem pelo papel de quem está em sessão: chegando o modo reconhecimento por qualquer
aplicação que não seja a App 01, a tentativa SHALL receber **403**.

A distinção pela chave é o que permite ao mesmo Mestre registrar presença por confirmação na
App 09 e, na App 01, autenticar a presença por reconhecimento da criança reconhecida na porta —
sem que nenhuma das duas aplicações alcance o que é da outra.

O recorte é o que concilia o `RF-09-45`, que dá a presença ao Mestre, com o PRD-01 §4, que não
a lista entre as escritas de gestão dele (`RF-01-17`): o Mestre a alcança pela **confirmação de
identidade do Guerreiro(a)**, operação que a matriz já lhe concede, e não por escrita de gestão
nova.

Permanecem valendo, sem alteração, a unicidade por aula e Guerreiro(a) e a recusa de presença
em comunidade alheia. (`RF-09-45`, `RF-01-20`, `RF-01-17`, `RF-01-03`, `RF-04-18`)

#### Scenario: O Mestre confirma a presença que faltou

- **WHEN** o Mestre registra, no modo confirmação, a presença de um Guerreiro(a) da comunidade
  dele numa aula
- **THEN** o núcleo grava a presença com modo confirmação e o Mestre como confirmador

#### Scenario: O Mestre não registra presença por reconhecimento

- **WHEN** o Mestre tenta registrar presença no modo reconhecimento por uma chave que não é a
  da App 01
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: O reenvio da mesma presença não duplica

- **WHEN** o Mestre confirma novamente a presença de um Guerreiro(a) que já a tem naquela aula
- **THEN** o núcleo devolve a presença já gravada, sem duplicar e sem erro
