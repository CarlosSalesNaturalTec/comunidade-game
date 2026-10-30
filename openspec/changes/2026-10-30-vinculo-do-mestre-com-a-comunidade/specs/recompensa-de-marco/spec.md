# Spec Delta

## MODIFIED Requirements

### Requirement: O marco alcançado vira pendência de entrega para o Mestre

O núcleo SHALL expor ao **Mestre em sessão** a fila das **entregas pendentes**: cada par de
Guerreiro(a) e recompensa de marco cujo **marco ele desbloqueou** e cuja **entrega ainda não foi
confirmada**. Cada pendência SHALL trazer o Guerreiro(a) pelo **nick e avatar**, a trilha, a
missão que é o marco, o **tipo de recurso** e a **quantidade**.

A fila SHALL alcançar apenas os Guerreiros e Guerreiras das **Comunidades Virtuais a que o
Mestre está vinculado** — a mesma condição que a entrega já exige — e NEVER SHALL se limitar às
trilhas de autoria dele: quem entrega é quem está no encontro, não quem escreveu a trilha.
Estando o Mestre vinculado a mais de uma comunidade, a fila SHALL trazer as pendências de
**todas elas**. Mestre sem vínculo com comunidade alguma SHALL receber fila **vazia**, nunca
erro. Persona que não é Mestre SHALL ser recusada com **403**.

Confirmada a entrega, a pendência SHALL **sair** da fila. A pendência cuja quantidade declarada
já se esgotou nas entregas anteriores SHALL continuar na fila, marcada com o motivo, porque é o
Mestre quem precisa saber que falta recompensa a entregar — a fila diz o que o Guerreiro(a)
conquistou, e a recusa segue acontecendo no ato. A saída NEVER SHALL trazer valor em moedas nem
em reais, nem imagem real de Guerreiro(a). (`RF-09-75`, `RF-09-76`, `RN-09-26`, invariantes 12 e
16, PRD-09 §12)

#### Scenario: Marco desbloqueado aparece como pendência do Mestre

- **WHEN** um Guerreiro(a) da comunidade do Mestre desbloqueia a missão declarada como marco com
  recompensa
- **THEN** a fila do Mestre passa a trazer aquela pendência, com o nick e o avatar do
  Guerreiro(a), a trilha, o marco, o tipo de recurso e a quantidade

#### Scenario: A fila reúne as pendências de todas as comunidades do Mestre

- **WHEN** um Mestre vinculado a duas comunidades consulta a fila, e há marco desbloqueado com
  recompensa em cada uma delas
- **THEN** a fila traz as pendências das duas

#### Scenario: Entrega confirmada sai da fila

- **WHEN** o Mestre confirma a entrega daquela recompensa àquele Guerreiro(a)
- **THEN** a pendência deixa de aparecer na fila dele

#### Scenario: A fila é da comunidade, não da autoria

- **WHEN** um Guerreiro(a) da comunidade do Mestre desbloqueia o marco de uma trilha escrita por
  outro Mestre
- **THEN** a pendência aparece na fila dele assim mesmo

#### Scenario: Guerreiro(a) de outra comunidade não aparece

- **WHEN** um Guerreiro(a) de Comunidade Virtual diversa das do Mestre desbloqueia um marco com
  recompensa
- **THEN** a pendência não aparece na fila daquele Mestre

#### Scenario: Mestre sem vínculo recebe fila vazia

- **WHEN** um Mestre sem vínculo com comunidade alguma consulta a fila
- **THEN** recebe a fila vazia, e nenhum erro

#### Scenario: Quem não é Mestre não lê a fila

- **WHEN** uma persona que não é Mestre consulta a fila de entregas pendentes
- **THEN** o núcleo responde 403 e nada da fila é servido

#### Scenario: A fila não mostra custo nem imagem real

- **WHEN** o Mestre consulta a fila de entregas pendentes
- **THEN** nenhum campo traz valor em moedas ou em reais, e o Guerreiro(a) aparece por nick e
  avatar
