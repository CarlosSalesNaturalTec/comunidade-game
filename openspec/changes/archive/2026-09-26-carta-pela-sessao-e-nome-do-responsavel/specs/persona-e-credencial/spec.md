# Spec Delta

## ADDED Requirements

### Requirement: A sessão devolve ao Guerreiro(a) o próprio nick e o próprio avatar

A leitura da sessão SHALL devolver ao **Guerreiro(a) em sessão** o **nick** e o **avatar**
dele, além do que já devolve a todos os papéis. É a única identificação que o Guerreiro(a)
tem de si mesmo em leitura logada, e sem ela nenhuma tela consegue apresentá-lo sem depender
de outra leitura que fale de terceiros. (`RF-01-76`)

A leitura NEVER SHALL devolver nick ou avatar de quem não é o próprio consultante, e NEVER
SHALL devolver imagem real, nome civil ou canal de contato — nem do Guerreiro(a), nem de
ninguém. (`RN-01-20`, invariantes 9 e 10)

Para os demais papéis a leitura SHALL permanecer como está: nick e avatar do adulto seguem
nas leituras de identidade que já os servem, e esta não passa a duplicá-las. (`RF-01-76`)

#### Scenario: O Guerreiro(a) em sessão recebe a própria identidade

- **WHEN** um Guerreiro(a) em sessão consulta a leitura da sessão
- **THEN** a resposta traz o nick e o avatar dele, junto do papel e das permissões que já
  vinham

#### Scenario: Guerreiro(a) sem avatar composto

- **WHEN** o Guerreiro(a) em sessão ainda não tem avatar composto
- **THEN** a resposta traz o nick e declara o avatar ausente, e a ausência não impede a
  leitura

#### Scenario: Adulto não recebe campo de Guerreiro(a)

- **WHEN** um Mestre, um Admin, um Apoiador ou um responsável consulta a leitura da sessão
- **THEN** a resposta não traz nick nem avatar de Guerreiro(a) algum

#### Scenario: A leitura não expõe dado vedado

- **WHEN** a leitura da sessão é devolvida a um Guerreiro(a)
- **THEN** nela não aparecem imagem real, nome civil nem canal de contato
