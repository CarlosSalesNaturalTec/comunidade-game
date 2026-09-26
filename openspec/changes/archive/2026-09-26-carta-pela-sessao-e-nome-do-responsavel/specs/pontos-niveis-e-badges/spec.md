# Spec Delta

## MODIFIED Requirements

### Requirement: O ranking da turma é lido em sessão e alcança quem não autorizou divulgação

O núcleo SHALL expor, ao **Guerreiro(a) em sessão**, o ranking da **sua própria Comunidade
Virtual**, ordenado pelo **ponto regular** já creditado e filtrável **por trilha ou por poder**.
Diferente do ranking público, este SHALL alcançar **a turma inteira** — com ou sem autorização
de divulgação vigente —, porque a tela é logada e restrita à comunidade de quem pergunta. A
posição do próprio Guerreiro(a) SHALL estar sempre presente na resposta, ainda que fora da
página consultada. (`RF-05-52`, `RF-05-53`, `RF-05-84`, `RN-05-16`, `RN-05-21`, documento 03 §12)

A comunidade do ranking SHALL ser **derivada do vínculo vigente de quem consulta**, e NEVER
SHALL ser declarada por quem pergunta: o núcleo já confere esse vínculo para recusar
comunidade alheia, e pedir de fora um dado que ele tem obriga cada tela a descobri-lo por
outra leitura antes de poder perguntar. Quem não tem vínculo vigente SHALL receber recusa, e
não ranking vazio. (`RF-05-52`, `RN-05-16`, `RN-05-21`)

A saída SHALL trazer, de cada Guerreiro(a), **apenas avatar, nick, posição e ponto regular**;
NEVER SHALL trazer ponto extra, nome civil, imagem real ou qualquer outro dado pessoal. A
ocorrência de conduta de **ciclo já encerrado** SHALL ficar fora da contagem, pela mesma
derivação que o ranking público já aplica — a regra é uma só, e este ranking não a duplica.
(`RN-05-18`, `RF-02-100`, invariante 12)

O ranking público de `leitura-publica-da-vitrine` NEVER SHALL ser alterado por esta leitura:
ele continua alcançando só quem autorizou a divulgação.

#### Scenario: O ranking logado traz a turma inteira

- **WHEN** um Guerreiro(a) em sessão consulta o ranking da sua comunidade
- **THEN** a resposta inclui também os colegas **sem** autorização de divulgação vigente

#### Scenario: A comunidade vem do vínculo, não da pergunta

- **WHEN** um Guerreiro(a) em sessão consulta o ranking sem declarar comunidade alguma
- **THEN** o núcleo devolve o ranking da comunidade do vínculo vigente dele

#### Scenario: Ranking sem série de coleta aberta

- **WHEN** o Guerreiro(a) que consulta nunca abriu série de coleta
- **THEN** o ranking vem assim mesmo, porque a comunidade não depende da coleta

#### Scenario: Sem vínculo vigente não há ranking

- **WHEN** quem consulta não tem vínculo de comunidade vigente
- **THEN** o núcleo recusa a leitura, em vez de devolver ranking vazio

#### Scenario: A própria posição vem sempre

- **WHEN** o Guerreiro(a) que consulta está fora da faixa de posições devolvida
- **THEN** a resposta traz assim mesmo a posição dele

#### Scenario: A própria posição existe sem ponto creditado

- **WHEN** o Guerreiro(a) que consulta ainda não tem ponto regular algum
- **THEN** a resposta traz a posição dele com zero ponto regular, e não a omite

#### Scenario: Ordena por ponto regular e ignora o extra

- **WHEN** um Guerreiro(a) tem mais ponto extra que os colegas e menos ponto regular
- **THEN** a posição dele é calculada só pelo ponto regular

#### Scenario: Filtra por trilha ou por poder

- **WHEN** a consulta declara uma trilha ou um poder
- **THEN** a ordenação considera apenas o ponto regular creditado naquela trilha ou naquele
  poder

#### Scenario: Nenhum dado pessoal de colega aparece

- **WHEN** o ranking é devolvido
- **THEN** cada colega aparece só por avatar, nick, posição e ponto regular

#### Scenario: Ranking de outra comunidade é recusado

- **WHEN** um Guerreiro(a) em sessão tenta alcançar o ranking de uma comunidade que não é a
  dele
- **THEN** não há como pedi-lo: a leitura só devolve a comunidade do vínculo vigente de quem
  pergunta, e nenhuma posição de comunidade alheia chega a ele

#### Scenario: Papel que não é Guerreiro(a) não lê este ranking

- **WHEN** um Mestre, um Admin ou um Apoiador consulta esta rota
- **THEN** o núcleo responde 403 — a leitura da gestão é o ranking público

#### Scenario: O ranking público continua filtrado

- **WHEN** a mesma comunidade é consultada na rota pública da vitrine
- **THEN** só aparecem os Guerreiros e Guerreiras com autorização de divulgação vigente
