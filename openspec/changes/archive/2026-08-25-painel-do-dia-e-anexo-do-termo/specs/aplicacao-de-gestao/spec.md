## ADDED Requirements

### Requirement: A App 03 abre a área Painel do dia, em leitura

A App 03 SHALL apresentar a área **Painel do dia**, que mostra o encontro em andamento numa tela
só: quem chegou, quem aguarda aparelho, as equipes com a missão de cada uma, a atividade prevista
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
- **THEN** a tela apresenta presenças, espera, equipes com missão, previsto e provido, saldo e
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

### Requirement: O painel se atualiza sozinho durante o encontro

A App 03 SHALL manter o Painel do dia atualizado **por sondagem**, sem recarga manual, no mesmo
padrão já usado na condução da partida de quiz. O operador NEVER SHALL precisar recarregar a
página para ver quem acabou de chegar ou a equipe que acabou de trocar de missão.

Caindo a rede, a tela SHALL manter legível o que já carregou e SHALL dizer que parou de
atualizar, retomando sozinha quando a rede voltar. (`RF-02-48`, PRD-02 §6.4)

#### Scenario: A chegada aparece sem recarga

- **WHEN** um Guerreiro(a) tem a presença registrada pela App 01 com o painel aberto
- **THEN** ele passa a aparecer no painel sem que ninguém recarregue a página

#### Scenario: A troca de missão aparece sem recarga

- **WHEN** uma equipe declara outra atividade da programação com o painel aberto
- **THEN** o painel passa a mostrá-la na missão nova sem recarga

#### Scenario: Sem rede, a tela avisa e não apaga o que carregou

- **WHEN** a rede cai com o painel aberto
- **THEN** a tela segue legível, diz que parou de atualizar e retoma sozinha quando a rede volta

### Requirement: A gestão anexa a digitalização do termo pela tela do painel

A App 03 SHALL oferecer ao **Admin**, a partir da lista de termos que aguardam digitalização, o
caminho para **anexar a digitalização** do termo de biometria assinado no encontro, em PDF, JPG
ou PNG (`RF-02-68`).

A tela SHALL dizer em linguagem simples a recusa de formato fora dos três e a recusa do termo
que já tem digitalização. O Mestre NEVER SHALL receber o caminho de anexar: ele lê o painel e
não escreve nele (`RN-02-20`). (`RF-02-68`, `RF-02-69`, `RN-02-20`, PRD-02 §§6.3, 6.4)

#### Scenario: O Admin anexa a digitalização a partir da pendência

- **WHEN** um Admin escolhe um termo pendente e envia a digitalização em PDF
- **THEN** a aplicação a anexa e a pendência sai da lista na atualização seguinte

#### Scenario: Formato recusado é explicado

- **WHEN** o Admin envia um arquivo que não é PDF, JPG nem PNG
- **THEN** a tela diz em linguagem simples quais formatos valem, e nada é enviado

#### Scenario: O Mestre não recebe o caminho de anexar

- **WHEN** um Mestre abre o painel com termos aguardando digitalização
- **THEN** a tela lista a pendência e não oferece a ele o caminho de anexar
