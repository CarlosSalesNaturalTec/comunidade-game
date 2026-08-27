## MODIFIED Requirements

### Requirement: Nível é percurso por trilha ou poder e nunca regride

O núcleo SHALL manter o **nível** por trilha ou poder, derivado do **percurso das missões
obrigatórias desbloqueadas** — nunca do total de pontos acumulado (11 §6). Nesta capacidade o
núcleo SHALL certificar os níveis **1** (inscrito na trilha **e** primeira atividade realizada,
as **duas** condições), **2** (um terço das missões obrigatórias desbloqueadas), **4** (todas as
obrigatórias desbloqueadas e ao menos um Resultado com mérito extra por auxílio aos colegas) e
**5 — Mestre Aprendiz** (a criação original da trilha validada pelo Mestre autor, certificada a
**cada integrante** da equipe que a entregou). A condição "inscrito" do nível 1 SHALL ser a
`InscricaoNaTrilha` da capacidade `inscricao-na-trilha`, e NEVER SHALL ser derivada de haver
`Resultado` na trilha: quem põe o Guerreiro(a) no percurso é ato dele, não lançamento do
Mestre. Nível conquistado SHALL **nunca regredir**, inclusive quando um **débito de ponto
regular** reduz o saldo do Guerreiro(a); o badge já concedido SHALL igualmente permanecer.
(`RF-01-21`, `RF-01-64`, `RF-01-70`, `RN-01-55`, `RF-05-09`, `RN-05-43`, 11 §6)

#### Scenario: Primeira atividade realizada alcança o nível 1

- **WHEN** o Guerreiro(a) **inscrito** na trilha tem a primeira atividade dela com Resultado
  registrado
- **THEN** o núcleo certifica o nível 1 naquela trilha

#### Scenario: Resultado sem inscrição não alcança o nível 1

- **WHEN** um Guerreiro(a) não inscrito na trilha tem Resultado registrado numa atividade dela
- **THEN** o núcleo não certifica o nível 1, e o faz assim que a inscrição existir

#### Scenario: Inscrição sem atividade realizada não alcança o nível 1

- **WHEN** o Guerreiro(a) inscreve-se numa trilha e ainda não tem Resultado registrado nela
- **THEN** o núcleo não certifica o nível 1

#### Scenario: Um terço das obrigatórias desbloqueadas alcança o nível 2

- **WHEN** o Guerreiro(a) tem Resultado registrado para um terço das missões obrigatórias da
  trilha
- **THEN** o núcleo certifica o nível 2 naquela trilha

#### Scenario: Nível conquistado não regride

- **WHEN** um Guerreiro(a) já certificado num nível deixa de atender ao critério que o levou lá
- **THEN** o núcleo mantém o nível já certificado

#### Scenario: Estorno não derruba nível nem badge

- **WHEN** um estorno reduz o saldo de ponto regular de um Guerreiro(a) já certificado num nível
- **THEN** o núcleo mantém o nível certificado e os badges já concedidos

#### Scenario: Criação original validada alcança o nível 5

- **WHEN** o Mestre autor da trilha valida a criação original entregue pela equipe da trilha
- **THEN** o núcleo certifica o nível 5 — Mestre Aprendiz — naquela trilha a cada integrante da
  equipe
