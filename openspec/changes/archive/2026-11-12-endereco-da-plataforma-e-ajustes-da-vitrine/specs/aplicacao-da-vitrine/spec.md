# Spec Delta

## RENAMED Requirements

- FROM: `### Requirement: A porta abre com o garfo do que a pessoa traz e encaminha`
- TO: `### Requirement: A porta pergunta o que a pessoa traz e encaminha`

## MODIFIED Requirements

### Requirement: A porta pergunta o que a pessoa traz e encaminha

A porta SHALL perguntar **o que a pessoa traz**, logo depois da doação sem cadastro, e SHALL
encaminhar conforme a resposta:
quem traz **dinheiro** ao **pré-cadastro da App 08**; quem traz **insumo, equipamento ou
alimento, serviço, conteúdo educacional, código, divulgação** ou a **pretensão de ensinar** ao
**formulário de solicitação de participação da vitrine**. A porta SHALL nomear, em cada
modalidade, o comprobatório que ela pede. O encaminhamento NEVER SHALL exigir campo que o
formulário não tem, e a escolha da modalidade NEVER SHALL ser guardada. (`RF-03-78`,
`RF-03-42`, documento 14 §§10, 11, documento 02 §1, decisões do fundador de 2026-09-29 e de
2026-11-12)

#### Scenario: Quem traz dinheiro vai ao pré-cadastro

- **WHEN** o visitante declara na porta que vai aportar em dinheiro
- **THEN** a porta o encaminha ao pré-cadastro da App 08, nomeando o comprovante da
  transferência

#### Scenario: Quem traz material, serviço, conteúdo, código, divulgação ou quer ensinar vai ao formulário

- **WHEN** o visitante declara na porta qualquer modalidade que não é dinheiro
- **THEN** a porta o encaminha ao formulário de solicitação de participação da vitrine, nomeando
  o comprobatório daquela modalidade

#### Scenario: A escolha da modalidade não sobrevive à recarga

- **WHEN** o visitante escolhe uma modalidade e recarrega a porta
- **THEN** a porta volta à pergunta, sem lembrar a escolha

### Requirement: A porta oferece também doar pela chave PIX e ver as necessidades em aberto

A porta SHALL oferecer, a quem não quer se cadastrar agora, os dois caminhos que dispensam
cadastro: **doar pela chave PIX** da pessoa jurídica vinculada, a que o conteúdo institucional
guarda na seção "Como apoiar", e **ver as necessidades de recurso em aberto**. A doação SHALL
ser a **primeira seção** da porta, antes de "Quero apoiar" e do que é ser Apoiador, com título
do mesmo nível. A chave PIX SHALL vir do que o núcleo devolve, e nenhum valor SHALL ficar
escrito na aplicação. Sendo a porta o **único** lugar público onde a chave aparece, a porta
NEVER SHALL deixar de oferecê-la quando o núcleo a devolve. (`RF-03-43`, `RF-03-46`,
`RF-03-78`, PRD-03 §5.5, decisões do fundador de 2026-10-11 e de 2026-11-12)

#### Scenario: Quem não quer se cadastrar encontra o PIX

- **WHEN** o visitante abre a porta e o núcleo devolve a seção "Como apoiar" publicada
- **THEN** a porta mostra a chave PIX e o titular, sem pedir cadastro

#### Scenario: A porta abre pela doação

- **WHEN** o visitante abre a porta
- **THEN** o primeiro título da página é "Doar sem se cadastrar", seguido do título "Quero
  apoiar", ambos do mesmo nível

#### Scenario: A porta mostra o que falta hoje

- **WHEN** o visitante abre a porta e há necessidade de recurso em aberto
- **THEN** a porta lista as necessidades em aberto

#### Scenario: A chave publicada é a que o Admin editou

- **WHEN** o Admin republica "Como apoiar" com outra chave
- **THEN** a porta mostra a chave nova, sem depender de nova versão da aplicação
