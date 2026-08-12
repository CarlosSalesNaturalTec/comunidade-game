## Purpose

O poder é a dimensão por onde a progressão acumula — pontos, níveis e badges são por trilha ou
poder, nunca globais — e é a ele que toda trilha se vincula. Esta capacidade cobre o catálogo
cadastrado por Admin, a distinção entre o poder que o Guerreiro(a) conquista e o que é derivado
do aporte, e a representação do que vigora no ciclo corrente.

## Requirements

### Requirement: O catálogo de poderes é cadastrado por Admin

O núcleo SHALL manter o catálogo de poderes a que as trilhas se vinculam. Cadastrar, alterar e
desativar poder SHALL exigir persona **Admin** em sessão; persona de qualquer outro papel SHALL
receber **403**, inclusive o Mestre, que escolhe entre os poderes cadastrados e NEVER SHALL criar
poder novo ao escrever a trilha. Toda escrita SHALL gravar autoria, data e hora, como já vale
para as demais escritas do núcleo. (`RF-01-62`, `RN-01-43`, `RF-01-03`, `RF-01-16`, PRD-01 §4)

#### Scenario: Admin cadastra um poder

- **WHEN** um Admin em sessão cadastra um poder com nome e descrição
- **THEN** o núcleo grava o poder no catálogo com o autor, a data e a hora com fuso

#### Scenario: Mestre não cadastra poder

- **WHEN** um Mestre em sessão tenta cadastrar, alterar ou desativar um poder
- **THEN** o núcleo responde 403 e o catálogo permanece como estava

#### Scenario: Poder sem nome é recusado

- **WHEN** um Admin tenta cadastrar um poder sem nome
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

### Requirement: Só poder de Guerreiro(a) recebe trilha

O núcleo SHALL registrar, em cada poder do catálogo, se ele é **poder de Guerreiro(a)** — o que
se conquista realizando e a que a trilha se vincula — ou **derivado do aporte**, caso do Poder
Sustentador, que mede o quanto Mestres e Apoiadores investiram. O núcleo SHALL recusar o vínculo
de uma trilha a poder derivado do aporte, porque o Apoiador não pontua e a progressão de quem
apoia corre por moedas, selos e níveis de sustento. (`RN-01-43`, documento 99 §6 invariante 21,
02 §2)

#### Scenario: Trilha se vincula a poder de Guerreiro(a)

- **WHEN** uma trilha é vinculada a um poder registrado como poder de Guerreiro(a)
- **THEN** o núcleo aceita o vínculo

#### Scenario: Trilha no Poder Sustentador é recusada

- **WHEN** uma trilha é vinculada a um poder registrado como derivado do aporte
- **THEN** o núcleo responde 422 e a trilha permanece sem poder vinculado

### Requirement: O catálogo distingue o poder vigente do poder de ciclo futuro

O núcleo SHALL registrar, em cada poder, se ele vigora no ciclo corrente ou se é direção do
projeto sem trilha prevista, como o documento 02 §2 marca. A distinção SHALL ser legível por quem
consulta o catálogo. Esta capacidade NEVER SHALL criar trava de publicação por vigência: as
travas da trilha são conferidas pela aplicação que publica. (`RF-01-62`, 02 §2)

#### Scenario: Poder de ciclo futuro fica no catálogo, distinguido

- **WHEN** um Admin cadastra um poder como direção do projeto, sem trilha prevista para o ciclo
- **THEN** o núcleo o guarda no catálogo e a consulta o distingue dos poderes vigentes

#### Scenario: A vigência não bloqueia o vínculo de trilha

- **WHEN** uma trilha é vinculada a um poder de Guerreiro(a) marcado como de ciclo futuro
- **THEN** o núcleo aceita o vínculo, porque a trava de publicação não é desta capacidade
