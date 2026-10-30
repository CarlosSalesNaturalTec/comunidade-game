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

### Requirement: O histórico da entrega é lido sem moedas e sem reais

O núcleo SHALL expor o histórico das entregas filtrado por persona: o Guerreiro(a) lê as
**próprias**; o **Mestre**, as das **comunidades a que está vinculado**; e o **Admin**, **todas**,
sem filtro de comunidade. A saída
SHALL trazer a recompensa, o marco, a trilha, o ponto de apoio, a data, o **tipo de recurso**
entregue, a **quantidade** e o **identificador do lançamento** da baixa — sem o que a gestão não
distingue o exemplar da linha Alpha da camisa nem mostra a baixa definitiva —, e NEVER SHALL
trazer o valor em moedas nem o valor em reais do recurso entregue: o custo segue no lançamento,
invisível para a criança (`RF-07-13`, `RN-07-05`, `RF-02-50`, `RF-02-51`, `RN-02-17`,
invariante 16, 02 §8).

O Admin lê sem recorte porque **não tem vínculo de comunidade** — a redação anterior o mandava
ler "a comunidade a que está vinculado", condição que nenhuma persona de Admin satisfaz, de
modo que a leitura dele saía sempre vazia. É o mesmo alcance que `troca-de-recompensa-avulsa`
já dá ao Admin no histórico de trocas (decisão do fundador de 2026-10-30).

#### Scenario: Guerreiro(a) lê as próprias entregas

- **WHEN** um Guerreiro(a) consulta o histórico de entregas
- **THEN** recebe apenas as suas, com recompensa, marco, trilha, ponto de apoio e data

#### Scenario: O Mestre lê as entregas das comunidades dele

- **WHEN** um Mestre vinculado a duas comunidades consulta o histórico
- **THEN** recebe as entregas das duas, e nenhuma de comunidade a que não está vinculado

#### Scenario: O Admin lê as entregas de todas as comunidades

- **WHEN** um Admin consulta o histórico de entregas
- **THEN** recebe as entregas de qualquer comunidade, sem declarar filtro algum

#### Scenario: O histórico não mostra o custo

- **WHEN** qualquer persona consulta o histórico de entregas
- **THEN** nenhum campo traz valor em moedas nem em reais

#### Scenario: A gestão distingue o recurso entregue e alcança a baixa

- **WHEN** um Admin consulta o histórico de entregas
- **THEN** cada entrega traz o tipo de recurso, a quantidade e o identificador do lançamento que
  deu a baixa definitiva
