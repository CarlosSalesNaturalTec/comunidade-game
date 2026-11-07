# Spec Delta

## ADDED Requirements

### Requirement: A coluna de criações originais da carta lista o acervo com título e data

Na carta do Guerreiro(a), a coluna "Criações originais" SHALL listar o **acervo público** dele —
a criação da culminância e as comprovações aprovadas do prático —, um item por linha, com o
**título** e a **data** de aprovação, do mais recente ao mais antigo. O título SHALL seguir o
`RN-03-43`. A coluna NEVER SHALL abrir a produção: é o resumo, e a produção abre no portfólio
abaixo da carta. (`RF-03-05`, `RF-03-86`, `RN-03-43`, decisão do fundador, 2026-11-07)

#### Scenario: A comprovação aprovada aparece na carta

- **WHEN** o visitante abre a página de um Guerreiro(a) que só tem comprovações aprovadas do
  prático
- **THEN** a coluna "Criações originais" lista cada uma pelo título curto do desafio e pela data,
  e não diz que não há criação validada

#### Scenario: A criação da culminância aparece pelo nome da trilha

- **WHEN** o Guerreiro(a) tem a criação da culminância validada
- **THEN** a coluna a lista com o nome da trilha como título e a data de validação

#### Scenario: A coluna abre pelo item mais recente

- **WHEN** a coluna lista mais de um item
- **THEN** o mais recente vem primeiro

#### Scenario: Sem item no acervo público, a coluna diz que não há

- **WHEN** o Guerreiro(a) não tem item aprovado e autorizado no acervo
- **THEN** a coluna diz em uma frase que não há criação original ainda

### Requirement: A página do Guerreiro(a) mantém o portfólio abaixo da carta, com a linha da vitrine

A página do Guerreiro(a) SHALL manter o **portfólio** abaixo da carta, com os mesmos itens da
coluna, na mesma ordem, e cada item na **linha do portfólio da vitrine**: título, data, trilha
fora da criação da culminância e autoria por nick. A linha SHALL **abrir a produção** como a
linha do portfólio da vitrine. (`RF-03-87`, `RF-03-85`, `RN-03-43`, decisão do fundador,
2026-11-07)

#### Scenario: O portfólio da página traz as duas fontes

- **WHEN** o visitante abre a página de um Guerreiro(a) com uma criação da culminância e uma
  comprovação aprovada
- **THEN** o portfólio abaixo da carta traz as duas, a mais recente primeiro

#### Scenario: A linha da página abre a produção

- **WHEN** o visitante aciona a produção de uma linha do portfólio da página
- **THEN** a produção abre na própria linha, como no portfólio da vitrine

#### Scenario: A linha da página é a da vitrine

- **WHEN** um item aparece no portfólio da página e no portfólio da vitrine
- **THEN** as duas linhas trazem o mesmo título, data, trilha e autoria
