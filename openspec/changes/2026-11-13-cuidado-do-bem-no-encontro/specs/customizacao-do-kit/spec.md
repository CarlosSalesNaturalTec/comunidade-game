# Spec Delta

## ADDED Requirements

### Requirement: O último aprovado do kit é servido a quem julga no encontro

O núcleo SHALL servir, pela rota do **bem recebido**, os bytes do **último registro aprovado**
do kit — a customização aprovada mais recente ou, sem nenhuma, a comprovação do prático que abriu
a customização — ao **Guerreiro(a) dono** e a **Mestre vinculado à comunidade dele**. Outra persona
recebe **403**; sem "antes" com mídia, **404**. A rota da comprovação do prático não muda.
(`RF-04-81`, decisão do fundador de 2026-11-13)

#### Scenario: O Mestre da aula vê a comprovação do prático como "antes"

- **WHEN** um Mestre vinculado à comunidade do Guerreiro(a), que não é autor da trilha, pede o
  último aprovado de um kit ainda sem customização aprovada
- **THEN** o núcleo devolve os bytes da comprovação do prático, com o tipo do arquivo declarado

#### Scenario: Depois da primeira aprovação, o "antes" é a customização

- **WHEN** o kit já tem customização aprovada e o Mestre da comunidade pede o último aprovado
- **THEN** o núcleo devolve os bytes da customização aprovada mais recente

#### Scenario: Mestre de outra comunidade não vê

- **WHEN** um Mestre que não é vinculado à comunidade do Guerreiro(a) pede o último aprovado
- **THEN** o núcleo responde **403**, e nada é servido

#### Scenario: Outro Guerreiro(a) não vê

- **WHEN** um Guerreiro(a) pede o último aprovado do kit de outro
- **THEN** o núcleo responde **403**, e nada é servido

#### Scenario: Kit sem customização aberta não tem "antes"

- **WHEN** o Mestre da comunidade pede o último aprovado de um bem cuja customização não abriu
- **THEN** o núcleo responde **404**

#### Scenario: A rota da comprovação segue só do autor

- **WHEN** um Mestre da comunidade, que não é autor da trilha, pede a comprovação do prático pela
  rota da missão
- **THEN** o núcleo responde **403**, como antes desta change
