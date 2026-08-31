## ADDED Requirements

### Requirement: As equipes de que a persona em sessão participa são alcançáveis numa só leitura

O núcleo SHALL servir, em `GET /v1/eu/equipes`, **todas** as equipes de que o Guerreiro(a) **em
sessão** é integrante — as da **aula** e as da **trilha** —, cada uma com o **papel** que ele
declarou nela, o vínculo que ela tem (aula ou trilha) e as **atividades** daquela equipe: para
a equipe da aula, as atividades da programação do encontro, marcando a corrente; para a equipe
da trilha, as atividades das missões daquela trilha.

Os integrantes SHALL sair **apenas por avatar e nick**, no mesmo contrato da leitura das
equipes da aula, e a leitura NEVER SHALL devolver nome, data de nascimento, imagem, _template_
biométrico nem qualquer outro dado pessoal. A leitura SHALL alcançar apenas as equipes da
persona da sessão, identificada pelo contexto e nunca por identificador vindo do cliente, e
NEVER SHALL devolver equipe que ela não integra. Persona sem nenhuma equipe SHALL receber
**200** com conjunto vazio, nunca erro.

A rota é de **leitura apenas**: nenhuma escrita de equipe nasce dela, e formar, entrar, sair e
homologar seguem nas rotas já vigentes desta capacidade. (`RF-05-22`, `RF-05-23`, `RF-05-24`,
`RN-05-12`, `RN-05-15`, `RN-05-21`)

#### Scenario: A leitura reúne equipe da aula e equipe da trilha

- **WHEN** um Guerreiro(a) em sessão integra uma equipe de aula e uma equipe de trilha e
  consulta as próprias equipes
- **THEN** o núcleo devolve as duas, cada uma com o vínculo que tem e o papel dele nela

#### Scenario: Cada equipe traz as atividades dela

- **WHEN** a leitura devolve uma equipe de aula com programação declarada no encontro
- **THEN** vêm as atividades daquela programação, com a corrente marcada

#### Scenario: Só avatar e nick de cada integrante

- **WHEN** a leitura devolve os integrantes de uma equipe
- **THEN** cada integrante traz avatar e nick, e nenhum outro dado pessoal

#### Scenario: Equipe que não integra não é devolvida

- **WHEN** existem outras equipes na mesma aula e na mesma trilha que o Guerreiro(a) não
  integra
- **THEN** o núcleo devolve apenas as equipes de que ele é integrante

#### Scenario: Persona sem equipe recebe conjunto vazio

- **WHEN** o Guerreiro(a) em sessão não integra nenhuma equipe
- **THEN** o núcleo responde 200 com conjunto vazio, nunca erro

#### Scenario: A leitura não altera composição

- **WHEN** a leitura das próprias equipes é feita
- **THEN** nenhuma equipe é criada, alterada nem homologada por ela
