## ADDED Requirements

### Requirement: O responsável lê os próprios vinculados, com o grau de parentesco

O núcleo SHALL servir à persona de **responsável em sessão** a lista dos Guerreiros e Guerreiras
**vinculados a ela por vínculo vigente**, e cada item SHALL trazer o **grau de parentesco**
declarado naquele vínculo, para que a aplicação apresente de quem se trata sem que o responsável
precise informá-lo. A lista NEVER SHALL trazer Guerreiro(a) sem vínculo vigente com quem está em
sessão, e persona de outro papel SHALL receber **403**. (`RF-13-04`, `RF-13-05`, `RN-13-04`,
`RF-01-15`)

#### Scenario: O responsável com dois vinculados vê os dois

- **WHEN** um responsável com dois vínculos vigentes pede os seus Guerreiros e Guerreiras
- **THEN** o núcleo devolve os dois, cada um com o grau de parentesco daquele vínculo

#### Scenario: Criança de outro responsável não entra na lista

- **WHEN** existe Guerreiro(a) ativo sem vínculo com o responsável em sessão, ainda que da mesma
  comunidade
- **THEN** ele não aparece na lista daquele responsável

#### Scenario: Vínculo encerrado sai da lista

- **WHEN** um vínculo do responsável já tem fim registrado
- **THEN** o Guerreiro(a) daquele vínculo não aparece na lista

#### Scenario: Persona de outro papel não usa a leitura do responsável

- **WHEN** uma persona que não é responsável chama a leitura dos seus vinculados
- **THEN** o núcleo responde 403 e nada é devolvido
