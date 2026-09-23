## MODIFIED Requirements

### Requirement: A App 03 abre a área Painel do dia, em leitura

A App 03 SHALL apresentar a área **Painel do dia**, que mostra o encontro em andamento numa tela
só: quem chegou, quem está **sem equipe**, as equipes com a missão de cada uma, a atividade prevista
e os recursos providos, o saldo dos tipos de recurso do ponto de apoio e os lançamentos
pendentes do encontro (`RF-02-41` a `RF-02-47`, `RF-02-69`).

A área SHALL ser de **leitura**: ela NEVER SHALL oferecer botão que lance, que edite equipe ou
que altere presença. Cada pendência listada SHALL levar o operador à tela que já a resolve, e é
lá que a escrita acontece.

Fora da janela de toda aula agendada, a área SHALL dizer em uma frase que não há encontro em
andamento, sem apresentar tela vazia nem erro cru. (`RF-02-41` a `RF-02-47`, `RF-02-69`,
`RN-02-12`, PRD-02 §§6.4, 12)

#### Scenario: A área mostra o encontro em andamento

- **WHEN** um Admin abre o Painel do dia durante a janela de uma aula
- **THEN** a tela apresenta presenças, a lista "Sem equipe", equipes com missão, previsto e provido, saldo e
  lançamentos pendentes

#### Scenario: Sem encontro, a área explica em uma frase

- **WHEN** o Painel do dia é aberto fora da janela de toda aula agendada
- **THEN** a tela diz que não há encontro em andamento, sem erro cru

#### Scenario: A área não oferece escrita

- **WHEN** o operador procura lançar ou alterar algo pela tela do painel
- **THEN** a tela não oferece caminho de escrita, e leva à tela que resolve aquela pendência

#### Scenario: A tela não exibe imagem real de criança

- **WHEN** o painel apresenta presenças e equipes
- **THEN** cada Guerreiro(a) aparece por nick e avatar, e nenhuma imagem real é exibida

## ADDED Requirements

### Requirement: O Admin cadastra e troca o próprio PIN de confirmação na App 03

A App 03 SHALL oferecer ao **Admin** em sessão uma tela para cadastrar ou trocar o **próprio**
PIN de confirmação, de 4 dígitos, digitado duas vezes e mascarado. A tela SHALL dizer se o Admin
já tem PIN cadastrado — sem mostrá-lo — e para que ele serve: confirmar a identidade de um
Guerreiro(a) no App 01. PIN fora do formato ou com as duas digitações diferentes SHALL ser
recusado na própria tela, antes do envio. (`RF-02-110`, `RF-01-75`)

#### Scenario: O Admin cadastra o PIN

- **WHEN** um Admin digita duas vezes o mesmo PIN de 4 dígitos e confirma
- **THEN** a aplicação envia o PIN ao núcleo e diz que ele está cadastrado, sem mostrá-lo

#### Scenario: As duas digitações diferem

- **WHEN** as duas digitações do PIN não são iguais
- **THEN** a aplicação não envia nada e pede que o Admin digite de novo

#### Scenario: A tela diz se já há PIN

- **WHEN** um Admin que já cadastrou o PIN abre a tela
- **THEN** a tela diz que há PIN cadastrado e oferece a troca, sem exibir o PIN
