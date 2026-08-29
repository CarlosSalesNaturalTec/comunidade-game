## ADDED Requirements

### Requirement: O Mestre lê os Guerreiros e Guerreiras que pode vincular

O núcleo SHALL servir à persona de **Mestre em sessão** a lista dos Guerreiros e Guerreiras que
ele pode vincular a um responsável, recortada pelas **comunidades em que ele atua**: Guerreiro(a)
de comunidade em que o Mestre não atua NEVER SHALL aparecer nela. Cada item SHALL trazer o
**nick** e o **avatar**, e NEVER SHALL trazer imagem real, nome civil, data de nascimento nem
contato — a identificação do Guerreiro(a) para o Mestre é por nick e avatar. A leitura SHALL
alcançar apenas Guerreiros e Guerreiras **já cadastrados e ativos**, e NEVER SHALL criar persona
alguma. Persona de outro papel SHALL receber **403**. (`RF-09-62`, `RN-01-20`, `RN-09-18`,
invariante 12 do documento 99 §6, decisão do fundador, 2026-08-29, documento 09 §1)

#### Scenario: O Mestre vê quem pode vincular

- **WHEN** um Mestre em sessão pede os Guerreiros e Guerreiras que pode vincular
- **THEN** o núcleo devolve os ativos das comunidades em que ele atua, cada um com nick e avatar

#### Scenario: Guerreiro(a) de outra comunidade não aparece

- **WHEN** existe Guerreiro(a) ativo em comunidade na qual o Mestre em sessão não atua
- **THEN** ele não aparece na lista daquele Mestre

#### Scenario: A lista não expõe dado pessoal da criança

- **WHEN** o Mestre lê a lista
- **THEN** cada item traz nick e avatar, e nenhum traz imagem real, nome civil, nascimento ou
  contato

#### Scenario: Persona de outro papel não usa a leitura do Mestre

- **WHEN** uma persona que não é Mestre chama a leitura dos vinculáveis
- **THEN** o núcleo responde 403 e nada é devolvido
