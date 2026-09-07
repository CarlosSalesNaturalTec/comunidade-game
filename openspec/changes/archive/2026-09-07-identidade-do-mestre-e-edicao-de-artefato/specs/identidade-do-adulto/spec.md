## ADDED Requirements

### Requirement: O Mestre define o próprio avatar, sem piso de moedas

O núcleo SHALL expor ao **Mestre em sessão** a gravação do **próprio avatar**, no mesmo ato em
que grava o nick ou isoladamente, cada campo opcional. NEVER SHALL exigir do Mestre piso de
moedas acumuladas para o avatar — o piso é regra de marca do Apoiador (`RN-14-11`) e não o
alcança. O avatar é **opaco ao núcleo**, que não valida a forma do valor. Persona de outro
papel, e tentativa de gravar o avatar de outra persona, SHALL receber **403**. (`RF-09-114`,
`RN-14-10`, `RN-14-11`, decisão do fundador de 2026-09-06)

#### Scenario: O Mestre grava nick e avatar de uma vez

- **WHEN** o Mestre em sessão envia nick e avatar juntos
- **THEN** o núcleo grava os dois naquela persona

#### Scenario: O Mestre troca só o avatar

- **WHEN** o Mestre em sessão envia apenas o avatar
- **THEN** o avatar é trocado e o nick permanece como estava

#### Scenario: Nenhum piso de moedas alcança o Mestre

- **WHEN** o Mestre em sessão grava o avatar sem ter moeda acumulada alguma
- **THEN** o núcleo grava o avatar

#### Scenario: Outro papel não grava o avatar pela rota do Mestre

- **WHEN** persona que não é Mestre chama a rota de identidade do Mestre
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O Mestre lê a própria identidade

O núcleo SHALL servir ao **Mestre em sessão** o **nick** e o **avatar** vigentes dele, para que
a aplicação apresente o que já está gravado antes de oferecer a troca. A leitura NEVER SHALL
alcançar a identidade de outra persona e NEVER SHALL devolver moeda acumulada, piso ou
liberação de avatar, que são regra do Apoiador. (`RF-09-114`, `RN-14-11`, decisão do fundador
de 2026-09-06)

#### Scenario: O Mestre lê o que já tem

- **WHEN** o Mestre em sessão lê a própria identidade
- **THEN** recebe o nick e o avatar vigentes, e nenhum dado de moeda

#### Scenario: Mestre ainda sem nick

- **WHEN** o Mestre em sessão nunca definiu nick nem avatar
- **THEN** a leitura devolve os dois vazios, sem erro

#### Scenario: Outro papel não lê a identidade do Mestre

- **WHEN** persona que não é Mestre chama a leitura da identidade do Mestre
- **THEN** o núcleo responde 403
