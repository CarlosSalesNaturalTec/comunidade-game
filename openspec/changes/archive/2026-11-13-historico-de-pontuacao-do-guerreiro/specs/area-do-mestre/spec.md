## ADDED Requirements

### Requirement: O Mestre abre a ficha do Guerreiro(a) da comunidade do vínculo

A App 09 SHALL listar os **Guerreiros e Guerreiras ativos das comunidades do vínculo vigente**
do Mestre em sessão, por **nick e avatar** — nunca imagem real, nome civil ou contato —, e
SHALL abrir, de cada um, a **ficha** com o histórico de pontuação. Guerreiro(a) de comunidade
sem vínculo do Mestre NEVER SHALL aparecer na lista. (`RF-09-143`, `RN-09-18`, `RN-01-68`)

#### Scenario: A lista traz só a comunidade do vínculo

- **WHEN** o Mestre abre a lista de Guerreiros e Guerreiras
- **THEN** a App 09 mostra, por nick e avatar, só os ativos das comunidades do seu vínculo
  vigente

#### Scenario: A lista leva à ficha

- **WHEN** o Mestre escolhe um Guerreiro(a) da lista
- **THEN** a App 09 abre a ficha dele, com o nick, o avatar e o histórico de pontuação

### Requirement: A ficha mostra o histórico de pontuação com os saldos

A ficha do Guerreiro(a) na App 09 SHALL mostrar os **saldos** — o regular de cada trilha ou
poder e as duas contas de ponto extra, separadas e rotuladas — e, abaixo, o **histórico** do
mais recente ao mais antigo: data, origem em linguagem simples, valor com sinal, conta, trilha
ou poder e, na ocorrência de conduta, o motivo. Ponto regular e ponto extra SHALL aparecer cada
um com o seu glifo, ficha e rótulo. A lista SHALL carregar mais lançamentos sob pedido, pela
paginação do núcleo. (`RF-09-144`, documento 15 §9, invariante 24)

#### Scenario: A ficha mostra saldos e lançamentos

- **WHEN** a ficha de um Guerreiro(a) com pontuação é aberta
- **THEN** a App 09 mostra os saldos regular e extra e, abaixo, os lançamentos do mais recente
  ao mais antigo

#### Scenario: Conduta aparece com motivo e débito

- **WHEN** o histórico traz uma ocorrência de conduta
- **THEN** a linha mostra a data, o débito com sinal negativo, a trilha e o motivo

#### Scenario: Ficha sem pontuação

- **WHEN** a ficha de um Guerreiro(a) que nunca pontuou é aberta
- **THEN** a App 09 mostra os saldos em zero e o aviso de que ainda não há lançamento

#### Scenario: Recusa do núcleo aparece como tal

- **WHEN** o núcleo responde 403 à leitura do histórico
- **THEN** a App 09 mostra a causa que o núcleo declarou, sem disfarçá-la de lista vazia
