## Purpose

Governa como o adulto — Apoiador e Mestre — escolhe o próprio nick: a conferência de
disponibilidade que alcança apenas nicks de adulto, para nunca confirmar a existência do nick
de uma criança, e a rota pela qual o adulto autenticado define ou troca o seu. Para o Apoiador,
governa também o avatar próprio — liberado a partir do piso de moedas acumuladas que não
regride — e a leitura da própria identidade.

## Requirements

### Requirement: A conferência de disponibilidade alcança apenas nicks de adulto

O núcleo SHALL expor uma **conferência de disponibilidade de nick** que compara o nick
pretendido **apenas** com os nicks de persona de **adulto** — Apoiador e Mestre. A conferência
NEVER SHALL comparar com nick de Guerreiro(a), NEVER SHALL revelar que um nick pertence a um
Guerreiro(a) e NEVER SHALL variar a resposta em função da existência de nick de criança: nick
usado por um Guerreiro(a) SHALL ser devolvido como **disponível**, exatamente como um nick que
ninguém usa.

É a restrição do alcance que elimina o oráculo — a conferência é pública no pré-cadastro, e o
nick de adulto já é exibido em público no card da vitrine, enquanto o nick de criança é
informação que só a família cede. (`RF-14-13`, `RN-01-22`, `RN-14-23`, invariante 12 do
documento 99 §6, documento 02 §1)

#### Scenario: Nick livre é devolvido como disponível

- **WHEN** a conferência recebe um nick que nenhuma persona usa
- **THEN** o núcleo responde que o nick está disponível

#### Scenario: Nick de Apoiador é devolvido como indisponível

- **WHEN** a conferência recebe um nick já usado por um Apoiador
- **THEN** o núcleo responde que o nick está indisponível

#### Scenario: Nick de Mestre é devolvido como indisponível

- **WHEN** a conferência recebe um nick já usado por um Mestre
- **THEN** o núcleo responde que o nick está indisponível

#### Scenario: Nick de Guerreiro(a) é devolvido como disponível

- **WHEN** a conferência recebe um nick já usado por um Guerreiro(a)
- **THEN** o núcleo responde que o nick está disponível, sem distinguir esse caso do nick que
  ninguém usa

### Requirement: A conferência sugere variações, e as variações também só olham adulto

O núcleo SHALL devolver **sugestões de variação** do nick pretendido quando ele estiver
indisponível. Cada variação sugerida SHALL passar pela mesma conferência restrita, e o núcleo
NEVER SHALL sugerir variação já usada por um adulto. Variação já usada por um Guerreiro(a)
SHALL poder ser sugerida, porque a conferência não a enxerga — e a colisão que daí resulte é
resolvida na gravação. (`RF-14-13`, `RN-01-22`)

#### Scenario: Nick indisponível vem com variações

- **WHEN** a conferência responde que o nick está indisponível
- **THEN** ela acompanha sugestões de variação daquele nick

#### Scenario: Variação sugerida não colide com adulto

- **WHEN** o núcleo monta as sugestões de variação
- **THEN** nenhuma delas é nick já usado por Apoiador ou por Mestre

### Requirement: A conferência não substitui a unicidade, que é da gravação

O núcleo SHALL tratar a conferência de disponibilidade como **conveniência da tela**, nunca
como garantia. A unicidade global do nick SHALL continuar sendo apurada **no momento da
gravação**, contra todas as personas de todos os papéis, e a gravação de nick já usado SHALL
ser recusada mesmo que a conferência o tenha devolvido como disponível. (`RN-01-30`,
`RN-14-10`)

#### Scenario: Conferência disponível não garante gravação

- **WHEN** um nick devolvido como disponível pela conferência é gravado e já pertence a um
  Guerreiro(a)
- **THEN** o núcleo recusa a gravação, e nenhuma persona passa a ter nick repetido

#### Scenario: A recusa da gravação não revela o papel de quem tem o nick

- **WHEN** o núcleo recusa a gravação de um nick já usado
- **THEN** a recusa não informa qual persona o usa nem de que papel ela é

### Requirement: O adulto autenticado define ou troca o próprio nick

O núcleo SHALL expor rota em que a persona de **Apoiador ou Mestre em sessão** define o próprio
nick, quando ainda não o tem, ou o troca por outro. A rota SHALL exigir credencial de persona,
SHALL alcançar **apenas a própria persona** — adulto NEVER SHALL alterar o nick de outra
persona por ela — e SHALL aplicar a conferência restrita e a unicidade global. Persona de
outro papel SHALL receber **403**. (`RF-14-12`, `RN-14-10`, `RN-01-30`, PRD-01 §9)

#### Scenario: Mestre define o próprio nick no primeiro acesso

- **WHEN** um Mestre em sessão e ainda sem nick define um nick disponível
- **THEN** o núcleo grava o nick naquela persona, com autoria, data e hora

#### Scenario: Apoiador troca o próprio nick

- **WHEN** um Apoiador em sessão troca o nick por outro disponível
- **THEN** o núcleo grava o nick novo e o anterior deixa de estar em uso

#### Scenario: Adulto não altera o nick de outra persona

- **WHEN** um adulto em sessão tenta alterar o nick de outra persona
- **THEN** o núcleo recusa a operação e nada é gravado

#### Scenario: Guerreiro(a) não usa a rota do adulto

- **WHEN** uma persona de Guerreiro(a) em sessão chama a rota de identidade do adulto
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Nick já usado é recusado na troca

- **WHEN** um adulto em sessão tenta trocar o nick por um já usado por outra persona
- **THEN** o núcleo recusa a troca e o nick anterior permanece

### Requirement: O Apoiador define o próprio avatar, acima do piso de moedas

A rota de identidade do adulto SHALL aceitar o **avatar** do Apoiador em sessão ao lado do nick
— logomarca ou outra imagem escolhida —, e SHALL gravá-lo **apenas** quando o Apoiador tiver
**10 moedas ou mais acumuladas em aportes homologados**. Abaixo do piso o núcleo SHALL recusar a
gravação com **409** e **quanto falta** em moedas, e o avatar anterior SHALL permanecer como
estava. Alcançado o piso, o envio SHALL passar **sem ato algum da gestão**. O avatar SHALL ser
opaco ao núcleo, que NEVER SHALL validar a forma dele. Persona que não seja Apoiador SHALL
receber **403** ao enviar avatar por esta rota. (`RF-14-12`, `RF-14-14`, `RF-14-17`, `RN-14-10`,
`RN-14-11`, PRD-14 §§5.2, 9, PRD-01 §9)

#### Scenario: Apoiador acima do piso grava o avatar próprio

- **WHEN** um Apoiador com 10 moedas acumuladas em aportes homologados envia o avatar próprio
- **THEN** o núcleo o grava na persona dele, sem intervenção da gestão

#### Scenario: Apoiador abaixo do piso é recusado com quanto falta

- **WHEN** um Apoiador com 5 moedas acumuladas envia o avatar próprio
- **THEN** o núcleo responde 409 dizendo quantas moedas faltam, e nenhum avatar é gravado

#### Scenario: O Apoiador troca o avatar depois de já o ter

- **WHEN** um Apoiador acima do piso envia um avatar novo no lugar do que já tinha
- **THEN** o núcleo grava o novo e o anterior deixa de valer

#### Scenario: Persona de outro papel não envia avatar por esta rota

- **WHEN** uma persona que não é Apoiador envia avatar pela rota de identidade do Apoiador
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O acumulado que libera o avatar não regride

O piso do avatar próprio SHALL ser medido pela **soma, em moedas, dos aportes homologados** do
Apoiador, e NEVER SHALL ser medido pelo Poder Sustentador, que o ressarcimento pago derruba. O
direito alcançado SHALL permanecer alcançado: aporte ressarcido, ajuste no livro-razão ou queda
do Poder Sustentador NEVER SHALL retirar do Apoiador o avatar próprio já gravado nem fechar o
envio de outro. (`RF-14-14`, `RN-14-11`, documento 11 §8.2, PRD-07 §9)

#### Scenario: O ressarcimento não fecha o avatar próprio

- **WHEN** um Apoiador que cruzou as 10 moedas tem um aporte ressarcido, e o Poder Sustentador
  dele cai abaixo de 10 moedas
- **THEN** o avatar próprio dele continua gravado e o envio de outro continua aberto

#### Scenario: O piso conta o aporte homologado, não o pendente

- **WHEN** um Apoiador com 5 moedas homologadas tem outro aporte declarado ainda pendente, de
  valor que cruzaria o piso
- **THEN** o núcleo continua recusando o avatar próprio, contando apenas o que foi homologado

### Requirement: O Apoiador lê a própria identidade e o que falta para o avatar próprio

O núcleo SHALL responder à persona de **Apoiador em sessão** uma leitura da própria identidade
com o **nick**, o **avatar** que estiver gravado, o **total de moedas acumuladas** e, abaixo do
piso, **quantas moedas faltam** para liberar o avatar próprio. A leitura SHALL alcançar
**apenas a própria persona**, e persona de outro papel SHALL receber **403**. A resposta NEVER
SHALL trazer valor em reais. (`RF-14-15`, `RF-14-16`, `RN-14-09`, `RN-14-11`, PRD-14 §§5.2, 6.2)

#### Scenario: Abaixo do piso a leitura diz quanto falta

- **WHEN** um Apoiador com 5 moedas acumuladas lê a própria identidade
- **THEN** a resposta traz o nick, o total em moedas e as 5 moedas que faltam para o avatar
  próprio

#### Scenario: Acima do piso a leitura diz que o avatar próprio está liberado

- **WHEN** um Apoiador com 12 moedas acumuladas lê a própria identidade
- **THEN** a resposta traz o avatar próprio como liberado e nada a faltar

#### Scenario: A leitura não traz reais

- **WHEN** um Apoiador cujos aportes têm valor de origem em reais lê a própria identidade
- **THEN** a resposta traz apenas moedas, sem campo algum com o valor em reais
