# Spec Delta

## ADDED Requirements

### Requirement: O Mestre autor corrige a atividade que já criou

O núcleo SHALL aceitar do **Mestre autor da trilha** a correção de uma `Atividade` de trilha já
gravada, alcançando **título**, **descrição**, **modalidade**, **formato** e **produção
esperada**. A correção SHALL valer em **qualquer situação da trilha** — rascunho, publicada ou
despublicada —, e NEVER SHALL alterar `Resultado`, produção, partida de quiz ou ocorrência de
conduta já gravados, nem estornar ponto, badge ou nível já creditados (`RF-09-47`).

As recusas da criação SHALL valer na correção: título vazio, modalidade ou formato fora dos
valores do documento 11 §4 e produção esperada vazia SHALL responder **422**. A autoria SHALL
ser **estrita** — Mestre que não é o autor e **Admin** SHALL receber **403**: o Admin audita e
despublica a trilha, não a redige. (`RF-09-127`, `RF-09-69`, `RF-09-70`, PRD-09 §§6.1, 7)

#### Scenario: O Mestre autor corrige o título da atividade

- **WHEN** o Mestre autor corrige o título de uma atividade de missão da própria trilha
- **THEN** o núcleo grava o título corrigido, e a atividade segue na mesma missão

#### Scenario: A correção alcança a trilha publicada

- **WHEN** o Mestre autor corrige a produção esperada de uma atividade de trilha já publicada
- **THEN** o núcleo grava a correção, e a situação da trilha permanece publicada

#### Scenario: O Resultado já lançado não é tocado pela correção

- **WHEN** o Mestre autor corrige a modalidade de uma atividade que já tem Resultado lançado
- **THEN** o núcleo grava a correção, e o Resultado e o ponto já creditado permanecem como estavam

#### Scenario: Correção sem título é recusada

- **WHEN** o Mestre autor corrige uma atividade deixando o título vazio
- **THEN** o núcleo responde **422** indicando o campo e nada é alterado

#### Scenario: Modalidade fora dos valores previstos é recusada na correção

- **WHEN** chega uma correção com modalidade que não é individual, em equipe nem em equipe com
  familiar
- **THEN** o núcleo responde **422** e nada é alterado

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha corrige atividade de missão dela
- **THEN** o núcleo responde **403** e nada é alterado

#### Scenario: Admin não corrige atividade de trilha

- **WHEN** um Admin corrige uma atividade de trilha
- **THEN** o núcleo responde **403** e nada é alterado

### Requirement: A natureza de uma atividade não se altera

O núcleo NEVER SHALL aceitar a troca da **natureza** de uma atividade já gravada: trocá-la é
**remover** a atividade e **cadastrar outra**. A natureza não é rótulo — é porta de
elegibilidade: a Partida de Quiz só corre sobre atividade de natureza **competição ao vivo**, e
o badge de **valores e causas** é concedido no lançamento do Resultado quando a natureza é essa.
O campo SHALL ser recusado na correção com **422**. (`RN-09-49`, `RF-09-127`, PRD-09 §7)

#### Scenario: Correção que declara natureza é recusada

- **WHEN** chega uma correção de atividade declarando natureza
- **THEN** o núcleo responde **422** e nada é alterado

#### Scenario: A natureza gravada sobrevive à correção dos demais campos

- **WHEN** o Mestre autor corrige o título e o formato de uma atividade de natureza competição
  ao vivo
- **THEN** a natureza permanece competição ao vivo, e a partida de quiz já corrida sobre ela
  segue resolvendo a atividade

### Requirement: Corrigir o formato para fora do presencial limpa a aula declarada

O núcleo SHALL **limpar a aula** declarada na atividade quando a correção levar o **formato**
para fora do presencial. Atividade on-line ou assíncrona com aula declarada é exatamente o
estado que a criação já recusa com **422**, e a correção NEVER SHALL fazê-lo nascer pela porta
de trás. A **aula** SHALL ficar fora dos campos da correção: declará-la segue sendo da criação.
(`RN-09-48`, `RF-09-73`, documento 05 §4)

#### Scenario: O formato sai do presencial e a aula é limpa

- **WHEN** o Mestre autor corrige para on-line assíncrona uma atividade presencial que declarava
  a aula do encontro
- **THEN** o núcleo grava o formato novo e a atividade passa a não declarar aula alguma

#### Scenario: O formato segue presencial e a aula permanece

- **WHEN** o Mestre autor corrige o título de uma atividade presencial que declara a aula
- **THEN** a aula declarada permanece a mesma

#### Scenario: Correção que declara aula é recusada

- **WHEN** chega uma correção de atividade declarando a aula do encontro
- **THEN** o núcleo responde **422** e nada é alterado

### Requirement: A atividade de trilha removida é carimbada, não apagada

O núcleo SHALL aceitar do **Mestre autor da trilha** a remoção de uma `Atividade` de trilha, em
**qualquer situação da trilha**, **carimbando-a**: ela SHALL sair de toda leitura de autoria e
de execução e SHALL permanecer guardada, porque cinco tabelas a apontam — `resultado`,
`producao_da_missao`, `partida_de_quiz`, `ocorrencia_de_conduta` e
`equipe.atividade_corrente_id` — e `RF-09-47` veda editar ou remover Resultado gravado.

Os quatro **fatos** gravados SHALL permanecer intactos e SHALL seguir resolvendo a atividade que
nomeiam; nenhum ponto, badge ou nível SHALL ser estornado. A autoria SHALL ser **estrita**, como
na correção: outro Mestre e **Admin** SHALL receber **403**. Missão SHALL poder ficar com
**nenhuma** atividade — nenhuma trava de publicação exige atividade (`RF-09-06`, `RF-09-07`,
`RF-09-82`). (`RF-09-128`, `RN-09-47`, `RF-09-47`, PRD-09 §§6.1, 7)

#### Scenario: A atividade removida sai da leitura e permanece guardada

- **WHEN** o Mestre autor remove uma atividade que já tem Resultado lançado
- **THEN** a atividade deixa de aparecer entre as da missão, e o Resultado e o ponto creditado
  permanecem como estavam

#### Scenario: A remoção alcança a trilha publicada

- **WHEN** o Mestre autor remove uma atividade de missão de trilha já publicada
- **THEN** o núcleo carimba a atividade, e a situação da trilha permanece publicada

#### Scenario: A missão pode ficar sem atividade alguma

- **WHEN** o Mestre autor remove a única atividade de uma missão
- **THEN** o núcleo a carimba, e a missão segue válida e publicável

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha remove atividade de missão dela
- **THEN** o núcleo responde **403** e nada é alterado

#### Scenario: Admin não remove atividade de trilha

- **WHEN** um Admin remove uma atividade de trilha
- **THEN** o núcleo responde **403** e nada é alterado

### Requirement: A remoção trata o estado vivo da atividade

O núcleo SHALL **zerar a escolha corrente** das equipes que apontavam a atividade removida — o
painel do dia NEVER SHALL anunciar como missão corrente a missão de atividade carimbada — e
SHALL **recusar com 422** a remoção enquanto houver **Partida de Quiz aberta** sobre ela:
partida em curso se encerra antes, e não se apaga por baixo da turma. Partida **encerrada** é
fato passado e NEVER SHALL impedir a remoção. (`RF-09-128`, `RN-09-47`, `RF-02-42`, `RF-04-35`,
documento 02 §5)

#### Scenario: A escolha corrente da equipe é zerada

- **WHEN** o Mestre autor remove uma atividade que uma equipe da aula declarou estar trabalhando
- **THEN** o núcleo carimba a atividade e a equipe passa a não declarar atividade corrente alguma

#### Scenario: Partida de quiz aberta impede a remoção

- **WHEN** o Mestre autor remove uma atividade sobre a qual corre uma partida de quiz aberta
- **THEN** o núcleo responde **422** dizendo que a partida precisa ser encerrada antes, e nada é
  alterado

#### Scenario: Partida encerrada não impede a remoção

- **WHEN** o Mestre autor remove uma atividade cuja única partida de quiz já foi encerrada
- **THEN** o núcleo carimba a atividade, e a partida encerrada segue resolvendo a atividade que
  nomeia

### Requirement: Nenhum fato novo aponta atividade carimbada

O núcleo SHALL recusar com **422** todo fato novo sobre atividade carimbada: lançamento de
`Resultado`, entrega de **produção da missão**, abertura de **Partida de Quiz** e lançamento de
**ocorrência de conduta**. A atividade carimbada NEVER SHALL aparecer nas leituras de autoria e
de execução — as missões da trilha do Mestre, a leitura pública da trilha, os **semanais** do
Guerreiro(a) (`RF-05-19`), a programação do encontro e as atividades da equipe (`RF-04-35`).
Leitura que parte de um fato gravado SHALL continuar resolvendo a atividade carimbada, porque é
dela que o fato fala. (`RF-09-128`, `RN-09-47`)

#### Scenario: Lançamento de Resultado sobre atividade carimbada é recusado

- **WHEN** o Mestre lança Resultado numa atividade que ele já removeu
- **THEN** o núcleo responde **422** e nada é gravado

#### Scenario: Entrega de produção sobre atividade carimbada é recusada

- **WHEN** o Guerreiro(a) entrega a produção de uma atividade carimbada
- **THEN** o núcleo responde **422** e nada é gravado

#### Scenario: Abertura de partida sobre atividade carimbada é recusada

- **WHEN** o Mestre abre partida de quiz sobre uma atividade carimbada
- **THEN** o núcleo responde **422** e nenhuma partida é aberta

#### Scenario: Ocorrência de conduta sobre atividade carimbada é recusada

- **WHEN** o Mestre lança ocorrência de conduta escolhendo uma atividade carimbada
- **THEN** o núcleo responde **422** e nada é gravado

#### Scenario: A atividade carimbada sai das missões da trilha

- **WHEN** o Mestre autor ou o Guerreiro(a) lê uma missão de que uma atividade foi removida
- **THEN** as atividades da missão vêm sem ela

#### Scenario: O fato gravado segue resolvendo a atividade

- **WHEN** a evolução do Guerreiro(a) é lida a partir de um Resultado cuja atividade foi
  carimbada
- **THEN** a leitura resolve a atividade e devolve a missão e o ponto dela, como antes da remoção

### Requirement: A correção e a remoção não alcançam a atividade avulsa

O núcleo SHALL recusar com **422** a correção e a remoção de **atividade avulsa** — a que
declara `poder_id` e não pertence a missão alguma. A avulsa é cadastro da gestão, privativo do
Admin pela App 03, com campos obrigatórios e âncora de ponto próprios (`RF-02-29`); esta
capacidade é da atividade **de trilha**. (`RF-09-127`, `RF-09-128`, `RF-02-29`)

#### Scenario: Correção de atividade avulsa é recusada

- **WHEN** chega uma correção de atividade que declara poder e não pertence a missão alguma
- **THEN** o núcleo responde **422** e nada é alterado

#### Scenario: Remoção de atividade avulsa é recusada

- **WHEN** chega a remoção de uma atividade avulsa
- **THEN** o núcleo responde **422** e nada é alterado

### Requirement: O núcleo diz quantos fatos apontam para a atividade

O núcleo SHALL servir ao **Mestre autor da trilha**, **sob demanda**, quantos fatos já apontam
para uma atividade de trilha: `Resultado`, produção da missão, partida de quiz (com quantas
estão **abertas**) e ocorrência de conduta, além de quantas equipes a declaram **corrente**. É o
que a aplicação diz ao Mestre **antes** de ele confirmar a remoção.

A contagem SHALL ser leitura própria, **nunca** embutida na leitura das trilhas do Mestre: contar
cinco tabelas por atividade faria cada abertura da tela da trilha pagar a conta de uma remoção
que quase nunca acontece — o mesmo motivo de `RN-09-46`. Autoria **estrita**: outro Mestre e
Admin SHALL receber **403**. (`RF-09-128`, `RN-09-46`)

#### Scenario: O Mestre autor lê os fatos da atividade

- **WHEN** o Mestre autor pede os fatos de uma atividade que tem dois Resultados lançados e uma
  partida encerrada
- **THEN** o núcleo devolve as contagens por tipo de fato, com nenhuma partida aberta

#### Scenario: Atividade sem fato algum

- **WHEN** o Mestre autor pede os fatos de uma atividade recém-criada
- **THEN** o núcleo devolve todas as contagens em zero

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha pede os fatos de uma atividade dela
- **THEN** o núcleo responde **403**
