## Purpose

Governa como o adulto — Apoiador e Mestre — escolhe o próprio nick: a conferência de
disponibilidade que alcança apenas nicks de adulto, para nunca confirmar a existência do nick
de uma criança, e a rota pela qual o adulto autenticado define ou troca o seu.

## ADDED Requirements

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
