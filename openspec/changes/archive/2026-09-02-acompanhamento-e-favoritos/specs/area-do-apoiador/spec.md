## ADDED Requirements

### Requirement: A App 08 tem a área de acompanhamento, com os mesmos dados do painel público

A App 08 SHALL apresentar ao Apoiador em sessão a área **Acompanhamento**, alimentada pelas
**mesmas rotas públicas de vitrine** que qualquer visitante consulta, sem token de sessão e sem
parâmetro que identifique o Apoiador. A área NEVER SHALL exibir recorte, filtro ou dado que a
vitrine não exiba a um visitante. (`RF-14-48`, `RN-14-24`, PRD-14 §§5.8, 9)

#### Scenario: A área mostra o que a vitrine mostra

- **WHEN** o Apoiador abre a área de acompanhamento
- **THEN** a tela apresenta os mesmos Guerreiros e Guerreiras, poderes, criações e cobertura de
  ODS que a leitura pública devolve, sem nenhum acréscimo

#### Scenario: A consulta pública não identifica o Apoiador

- **WHEN** a área de acompanhamento consulta a vitrine
- **THEN** a chamada vai sem token de sessão e sem nenhum parâmetro que diga quem está olhando

### Requirement: A tela favorita por nick exato e explica de onde vem o nick

A App 08 SHALL oferecer um campo de **nick exato** para favoritar Guerreiro(a), declarando em
linguagem simples que **o nick vem da família** e que a plataforma não o revela. A tela NEVER
SHALL listar, sugerir ou completar nick, e SHALL apresentar **a mesma mensagem** para nick
inexistente e para nick sem divulgação autorizada, sem dizer qual dos dois ocorreu.
(`RF-14-49`, `RF-14-50`, `RF-14-51`, `RN-14-23`, PRD-14 §§5.8, 12)

#### Scenario: O campo é de nick exato, e a tela diz de onde ele vem

- **WHEN** o Apoiador abre o caminho de favoritar um Guerreiro(a)
- **THEN** a tela pede o nick exato e explica que ele é cedido pela família, sem oferecer lista,
  sugestão ou autocompletar

#### Scenario: As duas recusas são a mesma tela

- **WHEN** o Apoiador informa um nick que não existe, e depois um nick sem divulgação
  autorizada
- **THEN** a tela mostra a mesma mensagem nas duas vezes, sem indicar qual caso ocorreu

### Requirement: A tela lista os favoritos com as novidades em destaque

A App 08 SHALL listar os favoritos do Apoiador — Guerreiros e Guerreiras por **avatar e nick**,
Mestres por **nome e avatar** — com as **novidades dos últimos 30 dias** em destaque, cada uma
com a data do fato. A tela SHALL declarar que o destaque dura 30 dias e que ele **existe só
nesta aplicação**, sem e-mail nem aviso fora dela. Sem favorito nenhum, a tela SHALL dizer isso
e apontar o caminho de favoritar, em vez de apresentar lista vazia sem explicação.
(`RF-14-52`, `RF-14-53`, `RN-14-25`, `RN-14-27`, PRD-14 §5.8)

#### Scenario: Os favoritos aparecem com a novidade

- **WHEN** o Apoiador abre a área de acompanhamento e tem favoritos com fato recente
- **THEN** cada favorito aparece com as novidades dos últimos 30 dias e a data de cada uma

#### Scenario: A tela declara os 30 dias e o alcance do destaque

- **WHEN** a lista de favoritos é apresentada
- **THEN** ela declara que o destaque dura 30 dias e que só existe dentro da aplicação

#### Scenario: Sem favorito a tela orienta

- **WHEN** o Apoiador ainda não favoritou ninguém
- **THEN** a tela diz isso e aponta o caminho de favoritar

### Requirement: A tela remove o favorito e nenhuma tela de acompanhamento abre canal

A App 08 SHALL oferecer a remoção do favorito a qualquer tempo, com a lista refletindo a
remoção. Nenhuma tela de acompanhamento SHALL apresentar nome real, contato, campo de mensagem,
telefone ou e-mail de Guerreiro(a), família ou Mestre, e NEVER SHALL oferecer ação que aproxime
o Apoiador da criança. (`RF-14-54`, `RF-14-55`, `RN-14-20`, `RN-14-24`, PRD-14 §12, invariantes
10 e 12)

#### Scenario: Remover sai da lista

- **WHEN** o Apoiador remove um favorito
- **THEN** ele some da lista, sem prazo, carência ou confirmação de terceiro

#### Scenario: Nenhuma ação aproxima o Apoiador da criança

- **WHEN** o Apoiador percorre a área de acompanhamento
- **THEN** nenhuma tela oferece campo de mensagem, contato ou qualquer canal com Guerreiro(a),
  família ou Mestre
