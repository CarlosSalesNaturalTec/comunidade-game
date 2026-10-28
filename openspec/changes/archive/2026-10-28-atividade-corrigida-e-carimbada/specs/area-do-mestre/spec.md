# Spec Delta

## MODIFIED Requirements

### Requirement: O Mestre cria as atividades da missão

A App 09 SHALL permitir ao Mestre autor criar atividade dentro de uma missão informando
**título**, **descrição**, **modalidade**, **formato**, **natureza** e **produção esperada**, e
SHALL apontar o campo em falta sem gravar quando o núcleo recusar atividade sem modalidade ou sem
formato. A aplicação SHALL apresentar as atividades já criadas **nomeando modalidade e formato em
português** — nunca o valor cru do enum — e SHALL permitir **corrigir** e **remover** cada uma,
em qualquer situação da trilha. (`RF-09-69`, `RF-09-70`, `RF-09-127`, `RF-09-128`)

#### Scenario: Mestre cria atividade

- **WHEN** o Mestre autor informa título, descrição, modalidade, formato, natureza e produção
  esperada e confirma
- **THEN** a atividade passa a existir naquela missão e a aplicação a apresenta entre as dela

#### Scenario: Atividade sem modalidade é recusada

- **WHEN** o Mestre confirma a atividade sem declarar a modalidade
- **THEN** a aplicação aponta o campo em falta e nenhuma atividade passa a existir

#### Scenario: A natureza aceita valor novo

- **WHEN** o Mestre informa natureza que não está entre as do Ciclo 01
- **THEN** a aplicação a aceita, porque a natureza é lista aberta

#### Scenario: A linha da atividade nomeia modalidade e formato em português

- **WHEN** o Mestre autor abre o bloco Atividades de uma missão com atividade em equipe com
  familiar e on-line assíncrona
- **THEN** a linha a apresenta como "Em equipe com familiar" e "On-line assíncrona", e não como
  `em_equipe_com_familiar / on_line_assincrona`

## ADDED Requirements

### Requirement: O bloco Atividades corrige cada atividade

A App 09 SHALL permitir ao Mestre autor corrigir, a partir da lista, **título**, **descrição**,
**modalidade**, **formato** e **produção esperada** de uma atividade já criada, pelo mesmo
formulário da criação, com os valores gravados já preenchidos. A **natureza** NEVER SHALL ser
oferecida na correção, e a **aula** do encontro NEVER SHALL ser campo dela; a aplicação SHALL
avisar, ao levar o formato para fora do presencial, que a aula declarada deixa de valer
(`RN-09-48`, `RN-09-49`). A correção SHALL valer em qualquer situação da trilha, publicada
inclusive, e a aplicação SHALL marcar o instante da gravação como já faz nos demais blocos da
missão. (`RF-09-127`, `RN-09-48`, `RN-09-49`, PRD-09 §§6.1, 7)

#### Scenario: O Mestre corrige o título da atividade

- **WHEN** o Mestre autor escolhe corrigir uma atividade da lista e grava outro título
- **THEN** a aplicação grava a correção no núcleo, a linha passa a exibir o título novo e a marca
  de gravação aparece

#### Scenario: O formulário de correção abre preenchido

- **WHEN** o Mestre autor escolhe corrigir uma atividade já criada
- **THEN** título, descrição, modalidade, formato e produção esperada aparecem com os valores
  gravados, e a natureza não é oferecida

#### Scenario: Levar o formato para fora do presencial avisa sobre a aula

- **WHEN** o Mestre autor corrige para on-line assíncrona uma atividade presencial que declarava
  aula
- **THEN** a aplicação avisa que a aula declarada deixa de valer antes de gravar

#### Scenario: A recusa do núcleo aponta o campo

- **WHEN** o núcleo recusa a correção por campo obrigatório vazio
- **THEN** a aplicação aponta aquele campo e nada é gravado

### Requirement: O bloco Atividades remove a atividade dizendo quantos fatos a apontam

A App 09 SHALL permitir ao Mestre autor remover uma atividade da lista e SHALL **dizer, antes de
confirmar, quantos fatos já apontam para ela** — Resultados lançados, produções entregues,
partidas de quiz, ocorrências de conduta e equipes que a declaram corrente —, buscando a contagem
**no momento em que ele pede a remoção**, nunca ao abrir a tela da trilha. Removida, a atividade
SHALL sair da lista, e a aplicação NEVER SHALL prometer que o Resultado ou o ponto já lançados
saem com ela. A recusa por **partida de quiz aberta** SHALL ser apresentada em linguagem simples,
dizendo que a partida precisa ser encerrada antes. (`RF-09-128`, `RN-09-47`, `RF-09-47`,
`RN-09-46`, PRD-09 §§6.1, 7)

#### Scenario: A confirmação diz quantos fatos apontam

- **WHEN** o Mestre autor pede a remoção de uma atividade que já tem dois Resultados lançados
- **THEN** a aplicação diz que dois Resultados seguem apontando para ela e pede confirmação antes
  de remover

#### Scenario: Atividade sem fato algum é removida direto da confirmação

- **WHEN** o Mestre autor confirma a remoção de uma atividade que nenhum fato aponta
- **THEN** a aplicação a remove e ela sai da lista da missão

#### Scenario: A contagem não é buscada ao abrir a trilha

- **WHEN** o Mestre autor abre a tela da trilha
- **THEN** a aplicação não busca contagem de fato algum até ele pedir a remoção de uma atividade

#### Scenario: Partida aberta é recusada em linguagem simples

- **WHEN** o núcleo recusa a remoção porque corre uma partida de quiz aberta sobre a atividade
- **THEN** a aplicação diz que a partida precisa ser encerrada antes, e a atividade permanece na
  lista
