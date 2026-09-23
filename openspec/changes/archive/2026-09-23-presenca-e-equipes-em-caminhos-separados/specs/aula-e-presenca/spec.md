# Spec Delta

## ADDED Requirements

### Requirement: O Guerreiro(a) em sessão lê se tem presença registrada na aula

O núcleo SHALL expor `GET /v1/aulas/{id}/presencas/eu`, sob a **sessão do Guerreiro(a)** e sob a
chave de aplicação, devolvendo se a persona em sessão tem presença **não anulada** naquela aula.
É essa leitura que permite ao App 01 recusar o caminho das equipes a quem ainda não registrou a
presença, em vez de descobri-lo só na recusa da formação (`RF-04-68`, `RN-04-40`).

O Guerreiro(a) lido SHALL ser sempre o da sessão — o identificador vem do contexto, nunca do
cliente (invariante 15) —, e a resposta NEVER SHALL trazer dado pessoal além do **momento do
fato** e do **modo de comprovação** da própria presença. Ausência de presença SHALL ser resposta
normal, nunca erro; presença **anulada** SHALL ser lida como ausência. Aula inexistente SHALL
responder 404. (`RF-04-68`, `RN-04-40`, `RN-01-22`, `RF-02-36`)

#### Scenario: Quem registrou a presença a lê

- **WHEN** um Guerreiro(a) em sessão lê a própria presença numa aula em que foi registrado
- **THEN** o núcleo responde que há presença, com o momento do fato e o modo de comprovação

#### Scenario: Quem não registrou recebe resposta, não erro

- **WHEN** um Guerreiro(a) em sessão lê a própria presença numa aula em que não foi registrado
- **THEN** o núcleo responde que não há presença, sem erro

#### Scenario: Presença anulada é lida como ausência

- **WHEN** a presença do Guerreiro(a) naquela aula foi anulada pela gestão
- **THEN** o núcleo responde que não há presença

#### Scenario: A leitura é sempre da própria persona

- **WHEN** se procura na rota um modo de pedir a presença de outro Guerreiro(a)
- **THEN** nenhum existe: o Guerreiro(a) lido vem do contexto da sessão

#### Scenario: Aula inexistente não abre oráculo

- **WHEN** a leitura aponta uma aula que não existe
- **THEN** o núcleo responde 404 e nada devolve sobre presença alguma
