## ADDED Requirements

### Requirement: O Mestre autor lê os desafios de coleta das suas missões

O núcleo SHALL devolver ao **Mestre autor** os desafios de coleta declarados em cada missão das
**suas próprias trilhas**, junto da leitura da trilha própria que ele já usa para autorar —
a mesma em que as atividades e as etiquetas ODS já vêm aninhadas. Sem essa leitura o Mestre não
vê o que já declarou nem o que ainda falta para a trilha publicar. (`RF-09-27`, `RF-09-28`,
`RF-09-04`, `RN-08-14`)

Cada desafio SHALL sair com o **tipo de coleta** escolhido — nome, forma de registro e unidade
quando houver —, a **cadência**, a **vigência**, a **granularidade exigida** e **quantos
registros do período pontuam**: os mesmos cinco atributos que a criação exige.

A leitura NEVER SHALL alcançar desafio de missão de trilha de outro autor, seja qual for a
situação dela, e NEVER SHALL exigir que a trilha esteja publicada — o rascunho é justamente onde
o desafio é declarado. Esta leitura é do **autor**, e não substitui a rota de Admin, que lista
os desafios de trilha publicada com as séries ativas, nem a do Guerreiro(a), que lista os que
ele pode assumir; nenhuma das duas muda.

#### Scenario: O Mestre autor vê o desafio que declarou na missão

- **WHEN** um Mestre autor consulta as suas trilhas depois de declarar um desafio de coleta numa
  missão
- **THEN** o desafio vem aninhado naquela missão, com tipo, cadência, vigência, granularidade
  exigida e quantos registros do período pontuam

#### Scenario: Missão sem desafio vem sem nenhum

- **WHEN** uma missão da trilha do Mestre ainda não tem desafio de coleta declarado
- **THEN** ela vem com a lista de desafios vazia, e a trilha continua sendo servida

#### Scenario: O rascunho serve o desafio como a trilha publicada

- **WHEN** o Mestre consulta uma trilha ainda em rascunho com desafio declarado
- **THEN** o desafio vem na leitura, porque é no rascunho que ele é escrito

#### Scenario: A leitura não alcança trilha de outro autor

- **WHEN** um Mestre consulta as suas trilhas e há desafios em missões de trilhas de outro Mestre
- **THEN** nenhum desafio de trilha alheia aparece na resposta
