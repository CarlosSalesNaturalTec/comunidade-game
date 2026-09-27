# Spec Delta

## MODIFIED Requirements

### Requirement: O Mestre vincula os Guerreiros e Guerreiras declarando o parentesco

A App 09 SHALL permitir que o Mestre vincule ao responsável recém-cadastrado os Guerreiros e
Guerreiras **já ativos** que ele pode alcançar, escolhidos numa lista servida pelo núcleo e
apresentada por **nick e avatar**. Cada vínculo SHALL exigir o **grau de parentesco em texto
livre**, e o grau SHALL ser declarado **por vínculo**, ainda que o mesmo responsável seja
vinculado a mais de uma criança. A aplicação NEVER SHALL exibir imagem real de Guerreiro(a) nem
oferecer caminho para criar a persona da criança a partir daqui. (`RF-09-62`, `RF-09-63`,
`RN-09-18`, invariante 12 do documento 99 §6)

Cada vínculo já criado que a aplicação apresenta SHALL identificar o **Guerreiro(a) pelo
nick**, ao lado do grau de parentesco. O parentesco sozinho NEVER SHALL bastar: ele se repete
entre irmãos, e o Mestre precisa conferir a quem cada vínculo se refere. O Guerreiro(a) sem
nick gravado SHALL ser apresentado de modo que a linha continue distinguível. (`RF-09-63`)

#### Scenario: O vínculo é criado com o grau declarado

- **WHEN** o Mestre escolhe um Guerreiro(a) da lista e informa o grau de parentesco
- **THEN** a aplicação cria o vínculo com aquele grau e o apresenta entre os já criados

#### Scenario: O vínculo apresentado identifica o Guerreiro(a) pelo nick

- **WHEN** o Mestre vincula um Guerreiro(a) e o vínculo é criado
- **THEN** a linha do vínculo apresenta o nick daquele Guerreiro(a) junto do grau declarado

#### Scenario: Dois vínculos de mesmo parentesco continuam distinguíveis

- **WHEN** o Mestre vincula o mesmo responsável a dois Guerreiros e Guerreiras, os dois com
  o parentesco "Pai"
- **THEN** as duas linhas se distinguem pelo nick de cada Guerreiro(a), e não aparecem como
  duas linhas iguais

#### Scenario: Guerreiro(a) sem nick gravado não apaga a linha

- **WHEN** o vínculo criado alcança um Guerreiro(a) que ainda não tem nick gravado
- **THEN** a linha permanece visível e sinaliza a ausência do nick, sem sumir nem ficar
  reduzida ao parentesco sozinho

#### Scenario: Cada vínculo tem o seu grau

- **WHEN** o Mestre vincula o mesmo responsável a dois Guerreiros e Guerreiras
- **THEN** cada vínculo pede e guarda o seu grau, sem que um herde o do outro

#### Scenario: Vínculo sem grau de parentesco é recusado

- **WHEN** o Mestre tenta vincular sem informar o grau de parentesco
- **THEN** a aplicação aponta o campo em falta e nenhum vínculo é criado

#### Scenario: A escolha do Guerreiro(a) é por nick e avatar

- **WHEN** o Mestre abre a lista de quem pode vincular
- **THEN** vê nick e avatar de cada Guerreiro(a), e nenhuma imagem real
