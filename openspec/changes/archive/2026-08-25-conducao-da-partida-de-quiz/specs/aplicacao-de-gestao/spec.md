## ADDED Requirements

### Requirement: A App 03 abre a partida sobre a atividade e as equipes da aula

A aplicação SHALL oferecer ao Mestre que conduz — e ao Admin — a abertura da partida de Quiz
ao Vivo a partir da aula em andamento, escolhendo a **atividade de competição ao vivo** sobre
a qual ela corre e as **equipes formadas na App 01** naquele encontro. A tela SHALL apresentar
as equipes por **avatar e nick**, sem dado pessoal algum, e NEVER SHALL exibir imagem real de
Guerreiro(a). Não havendo equipe formada na aula, a aplicação SHALL dizê-lo em uma frase, sem
oferecer a abertura. (`RF-02-59`, `RF-02-61`, PRD-02 §§11, 12)

#### Scenario: O Mestre abre a partida escolhendo atividade e equipes

- **WHEN** o Mestre que conduz escolhe a atividade de competição ao vivo e marca as equipes
  disputantes
- **THEN** a aplicação abre a partida e passa à tela de condução

#### Scenario: As equipes aparecem por avatar e nick

- **WHEN** a tela de abertura lista as equipes da aula
- **THEN** cada integrante aparece por avatar e nick, sem nome, idade ou imagem real

#### Scenario: Aula sem equipe formada não abre partida

- **WHEN** a aula em andamento não tem equipe formada
- **THEN** a aplicação informa em uma frase que não há equipe e não oferece a abertura

### Requirement: A tela de condução governa o ritmo da partida

A aplicação SHALL oferecer a quem conduz, na partida aberta, quatro atos: **pôr uma pergunta
no ar**, escolhida do banco da missão daquela atividade; **liberar o resultado** da pergunta
no ar; **anular** a pergunta contestada; e **encerrar** a partida. Não há tempo por pergunta —
o ritmo é de quem conduz. A tela SHALL mostrar, enquanto o resultado não está liberado,
quantas equipes já responderam, sem revelar o que responderam; liberado, SHALL mostrar a
alternativa correta, as equipes que acertaram e a primeira delas. O encerramento SHALL avisar
que a pontuação será lançada automaticamente às equipes. (`RF-02-60`, `RF-02-62`, `RF-02-72`,
`RF-02-73`, documento 05 §5)

#### Scenario: Quem conduz põe a pergunta no ar

- **WHEN** quem conduz escolhe uma pergunta do banco da missão e dá o _start_
- **THEN** a tela passa a mostrar a pergunta no ar e quantas equipes já responderam

#### Scenario: Antes de liberar, a tela não revela as respostas

- **WHEN** equipes respondem e o resultado ainda não foi liberado
- **THEN** a tela mostra apenas a contagem de quem respondeu, sem a alternativa de ninguém

#### Scenario: Liberado o resultado, a tela mostra quem acertou

- **WHEN** quem conduz libera o resultado da pergunta no ar
- **THEN** a tela mostra a alternativa correta, as equipes que acertaram e qual chegou
  primeiro

#### Scenario: A pergunta contestada é anulada

- **WHEN** quem conduz anula a pergunta contestada
- **THEN** a tela marca a pergunta como anulada e informa que ela não credita ninguém

#### Scenario: O encerramento avisa do lançamento

- **WHEN** quem conduz encerra a partida
- **THEN** a aplicação confirma o encerramento e informa que a pontuação foi lançada às
  equipes

### Requirement: A tela de condução acompanha a partida por sondagem a cada 2 segundos

A aplicação SHALL manter a tela de condução atualizada **sondando o núcleo a cada 2
segundos**, sem recarga manual e sem conexão longa (documento 03 §1, decisão do fundador de
2026-08-25). Sondagem que falha por rede NEVER SHALL derrubar a partida nem apagar o que já
está na tela: a aplicação SHALL avisar que perdeu contato e SHALL retomar o estado corrente na
sondagem seguinte. (`RF-02-60`, PRD-02 §§10, 12)

#### Scenario: A tela acompanha sem recarga

- **WHEN** a partida está aberta e equipes vão respondendo
- **THEN** a contagem na tela avança sozinha, sem que quem conduz recarregue

#### Scenario: A queda de rede não derruba a partida

- **WHEN** uma sondagem falha por rede
- **THEN** a tela avisa que perdeu contato, mantém o que já exibia e volta ao estado corrente
  na sondagem seguinte

### Requirement: O Mestre alcança a condução da partida e nada mais da gestão

A aplicação SHALL permitir ao Mestre autenticado ler o painel e conduzir a partida de quiz da
aula dele, e SHALL apresentar a recusa do núcleo em qualquer outra escrita de gestão. Mestre
que tenta conduzir a partida de uma aula que não é dele SHALL receber a recusa, dita em uma
frase, sem que a tela ofereça caminho alternativo. (`RF-02-49`, `RN-02-20`, PRD-02 §12)

#### Scenario: Mestre conduz a partida da sua aula

- **WHEN** o Mestre autenticado abre a condução da partida da aula dele
- **THEN** a aplicação oferece os quatro atos da condução

#### Scenario: Mestre de outra aula é recusado

- **WHEN** o Mestre tenta conduzir a partida de uma aula que não é dele
- **THEN** a aplicação apresenta a recusa em uma frase e não oferece caminho alternativo
