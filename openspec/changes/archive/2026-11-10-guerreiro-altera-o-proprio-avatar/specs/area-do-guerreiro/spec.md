## ADDED Requirements

### Requirement: A App 05 deixa o Guerreiro(a) alterar o próprio avatar

A carteira da App 05, onde a carta do Guerreiro(a) é apresentada, SHALL oferecer o caminho para
**mudar o próprio avatar**. Ele SHALL abrir a montagem do avatar da camada comum **já com o
avatar vigente** do Guerreiro(a) — o que a leitura da sessão devolve, ou o avatar padrão do
projeto quando ele faltar —, com todas as nove camadas disponíveis, a qualquer tempo e sem
limite de vezes. (`RF-05-51`, decisão do fundador de 2026-11-10, documento 15 §§7, 7.3)

Trocar traço na montagem NEVER SHALL gravar nada: a troca SHALL ser gravada só quando o
Guerreiro(a) pedir, pela rota `PATCH /v1/eu/avatar`, e voltar sem salvar SHALL manter o avatar
vigente. Gravada a troca, a App 05 SHALL voltar à carteira com a **carta redesenhada** pelo
avatar novo. (`RF-05-51`, `RF-05-50`)

A forma de tratamento e qualquer outro campo que viaje ao lado do objeto do documento 15 §7.2
no avatar gravado SHALL ser **preservados** na troca: alterar o avatar NEVER SHALL apagar nem
mudar a forma de tratamento. (`RF-05-51`, documento 15 §7)

Recusa de sessão SHALL seguir o tratamento que toda tela da App 05 já dá a ela, e qualquer
outra falha da gravação SHALL ser dita em linguagem de criança, mantendo a montagem aberta com
o que foi escolhido, para tentar de novo. (`RN-05-48`, PRD-05 §10)

O avatar segue sendo o **único retrato** do Guerreiro(a): a montagem NEVER SHALL usar câmera,
imagem real nem o _template_ biométrico. (`RN-05-15`, documento 15 §7)

#### Scenario: A montagem abre no avatar vigente

- **WHEN** o Guerreiro(a) em sessão abre o caminho de mudar o avatar, na carteira
- **THEN** a montagem aparece com as nove camadas, cada uma no traço do avatar que ele tem hoje

#### Scenario: Sem avatar gravado, a montagem parte do avatar padrão

- **WHEN** a leitura da sessão não traz avatar, ou traz um que não é objeto do catálogo
- **THEN** a montagem abre no avatar padrão do projeto

#### Scenario: Salvar grava e redesenha a carta

- **WHEN** o Guerreiro(a) troca traços e pede para salvar
- **THEN** a App 05 grava o avatar novo pela rota do núcleo e volta à carteira, com a carta
  desenhando o avatar novo

#### Scenario: Voltar sem salvar não grava

- **WHEN** o Guerreiro(a) troca traços e volta sem salvar
- **THEN** nenhuma requisição de gravação sai e a carta segue com o avatar vigente

#### Scenario: A forma de tratamento sobrevive à troca

- **WHEN** o avatar gravado traz a forma de tratamento ao lado do objeto e o Guerreiro(a) troca
  o avatar
- **THEN** o texto gravado leva o objeto novo e a mesma forma de tratamento de antes

#### Scenario: Falha na gravação mantém o que foi escolhido

- **WHEN** a gravação falha por motivo que não é recusa de sessão
- **THEN** a App 05 diz que não conseguiu salvar, em linguagem de criança, e a montagem segue
  aberta com os traços escolhidos
