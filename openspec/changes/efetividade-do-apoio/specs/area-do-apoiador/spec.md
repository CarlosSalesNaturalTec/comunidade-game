## ADDED Requirements

### Requirement: A App 08 tem a área de efetividade do apoio

A App 08 SHALL apresentar ao Apoiador em sessão a área **Efetividade**, com os desafios
propostos, publicados e concluídos, quantos concluíram cada um, a trilha e o período, as
moedas aportadas e o que custearam, e a cobertura de ODS agregada. A tela SHALL declarar, em
linguagem simples, que o painel é **vivo** e que **não há relatório fechado** no Ciclo 01.
(`RF-14-40` a `RF-14-44`, `RN-14-21`, PRD-14 §5.7)

#### Scenario: A área reúne desafios, moedas e ODS

- **WHEN** o Apoiador abre a área de efetividade
- **THEN** a tela mostra os desafios por situação, a contagem de conclusões com trilha e
  período, as moedas aportadas com o que custearam e a cobertura de ODS

#### Scenario: A tela diz que o painel é vivo

- **WHEN** a área de efetividade é apresentada
- **THEN** ela declara que o painel atualiza a cada conclusão e que não há relatório fechado

#### Scenario: Sem desafio proposto a tela orienta

- **WHEN** o Apoiador ainda não propôs nenhum desafio
- **THEN** a tela diz isso e aponta o caminho de propor, sem apresentar painel vazio sem
  explicação

### Requirement: Nenhuma tela de efetividade identifica Guerreiro(a) nem abre canal

A área de efetividade SHALL exibir quem concluiu **apenas por avatar e nick**, e só quando há
divulgação autorizada; sem ela, SHALL exibir somente a contagem. No **direcionado**, SHALL
exibir apenas que houve conclusão. NEVER SHALL apresentar nome real, contato, campo de mensagem,
telefone ou e-mail de Guerreiro(a), família ou Mestre, e NEVER SHALL oferecer ação que aproxime
o Apoiador da criança. (`RF-14-45`, `RF-14-46`, `RF-14-47`, `RN-14-20`, `RN-14-22`, PRD-14 §12,
invariantes 10 e 12)

#### Scenario: A tela mostra avatar e nick só de quem autorizou

- **WHEN** a área de efetividade lista quem concluiu um desafio aberto
- **THEN** aparecem só os avatares e nicks de quem tem divulgação autorizada, e os demais
  entram apenas na contagem

#### Scenario: O direcionado aparece só como concluído

- **WHEN** a área de efetividade mostra um desafio direcionado concluído
- **THEN** ela informa apenas que houve conclusão

#### Scenario: Nenhuma ação aproxima o Apoiador da criança

- **WHEN** o Apoiador percorre a área de efetividade
- **THEN** nenhuma tela oferece campo de mensagem, contato ou qualquer canal com Guerreiro(a),
  família ou Mestre
