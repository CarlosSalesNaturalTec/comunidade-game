# Spec Delta

## ADDED Requirements

### Requirement: O institucional é servido em HTML real, e a vitrine sai como arquivo estático

A App 06 SHALL ser publicada como **saída estática**, sem runtime de servidor, e cada
endereço institucional — a abertura, a área detalhada de coleta, a porta do convite e as
seções publicadas — SHALL ser servido com **o conteúdo já no documento**, legível por
quem não executa script. O conteúdo SHALL ser o publicado na App 03 no momento da
publicação do site.

O endereço que não corresponde a arquivo publicado SHALL continuar sendo atendido pela
aplicação no aparelho, sem erro de servidor: nenhum endereço público hoje alcançável
SHALL deixar de responder. (PRD-03 §10, `RF-03-01`, `RF-03-45`, `RF-03-52`, documento 03
§1, princípio 13)

#### Scenario: A abertura chega com conteúdo sem executar script

- **WHEN** a raiz do domínio é buscada por um agente que não executa script
- **THEN** o documento devolvido já traz o conteúdo institucional daquela tela

#### Scenario: A área detalhada de coleta chega com conteúdo sem executar script

- **WHEN** o endereço da área detalhada é buscado por um agente que não executa script
- **THEN** o documento devolvido já traz o que a plataforma coleta, de quem, para quê e
  por quanto tempo

#### Scenario: Endereço sem arquivo publicado continua respondendo

- **WHEN** um endereço público é aberto e não há arquivo publicado para ele
- **THEN** a aplicação no aparelho o resolve e apresenta a tela, sem erro de servidor

### Requirement: A página da comunidade sai com casca em HTML real e o painel carregado no aparelho

A página de cada Comunidade Virtual SHALL ser servida com a **casca no documento** —
nome, território e o texto que a descreve —, para que seja indexável, e o **painel do
território** SHALL ser carregado no aparelho a cada visita.

O que o painel apresenta NEVER SHALL vir do documento servido: séries, cobertura da
Agenda 2030, número de vinculados e indicadores SHALL refletir a leitura do núcleo
naquela visita, e nunca o que valia quando o site foi publicado. Enquanto o painel não
chega, a página SHALL declarar que está carregando, e a casca SHALL permanecer legível.
(PRD-03 §10, `RF-03-02`, `RF-03-15`, `RF-03-03`)

#### Scenario: A casca chega sem executar script

- **WHEN** o endereço de uma comunidade é buscado por um agente que não executa script
- **THEN** o documento devolvido traz o nome e o território daquela comunidade

#### Scenario: O painel reflete a leitura da visita, não a da publicação

- **WHEN** uma série do território muda no núcleo depois da publicação do site e o
  visitante abre a página daquela comunidade
- **THEN** o painel apresenta o valor corrente, e nenhum valor da publicação anterior

#### Scenario: A casca permanece legível enquanto o painel carrega

- **WHEN** a página da comunidade abre e a leitura do núcleo ainda não voltou
- **THEN** o nome e o território seguem visíveis, e o painel declara que está carregando

### Requirement: A página de pessoa é carregada no aparelho e nunca é indexada

A página individual de **Guerreiro(a), Mestre e Apoiador** SHALL ser carregada no
aparelho a cada visita, e NEVER SHALL ser servida com o conteúdo já no documento.

Essas páginas SHALL declarar a buscadores que **não devem ser indexadas**, e NEVER SHALL
constar do `sitemap.xml`. A exclusão SHALL valer para o endereço individual, e nunca
para as seções institucionais ou de comunidade.

Para o Guerreiro(a), é o que sustenta a revogação: conteúdo posto no documento na
publicação do site sobreviveria à revogação até a publicação seguinte, contra o
`RF-03-14` e o invariante 12 do documento 99. Para Mestre e Apoiador, é decisão do
fundador de 2026-09-30. (PRD-03 §10, `RF-03-03`, `RF-03-07`, `RF-03-13`, `RF-03-14`,
`RN-03-02`, `RN-03-18`)

#### Scenario: A página de Guerreiro(a) não traz o perfil no documento

- **WHEN** o endereço de um Guerreiro(a) com autorização vigente é buscado por um agente
  que não executa script
- **THEN** o documento devolvido não traz avatar, nick, badges, poderes nem desempenho

#### Scenario: A revogação vale no mesmo instante, sem nova publicação

- **WHEN** o responsável revoga a autorização e alguém abre o endereço direto da página,
  sem que o site tenha sido publicado de novo
- **THEN** a página responde "não encontrado"

#### Scenario: As três páginas de pessoa declaram que não se indexa

- **WHEN** o endereço individual de um Guerreiro(a), de um Mestre ou de um Apoiador é
  buscado
- **THEN** a resposta declara a buscadores que aquele endereço não deve ser indexado

#### Scenario: A exclusão não alcança o institucional nem a comunidade

- **WHEN** um endereço institucional ou de comunidade é buscado
- **THEN** nada na resposta pede que ele deixe de ser indexado

### Requirement: Cada endereço indexável declara título, descrição e canônica próprios

Cada endereço indexável SHALL declarar **título e descrição próprios**, que digam o que
aquela tela é, e **endereço canônico** apontando para ele mesmo. NEVER SHALL haver um
único título para o site inteiro.

O que o endereço declara para compartilhamento SHALL ser o mesmo conteúdo público da
tela, e NEVER SHALL revelar nick, nome ou qualquer dado de Guerreiro(a). (PRD-03 §10,
`RF-03-03`, `RF-03-06`, `RF-03-61`)

#### Scenario: Duas telas indexáveis não repetem o mesmo título

- **WHEN** a abertura e a área detalhada de coleta são buscadas
- **THEN** cada uma declara título e descrição próprios, diferentes entre si

#### Scenario: A prévia de compartilhamento não revela dado de Guerreiro(a)

- **WHEN** um endereço indexável é compartilhado e a prévia é montada
- **THEN** a prévia traz só conteúdo público da tela, sem nick nem nome de Guerreiro(a)

### Requirement: O site declara robots.txt e sitemap.xml, e ambos só alcançam o indexável

A App 06 SHALL publicar, no próprio domínio, um `robots.txt` e um `sitemap.xml`. O
`sitemap.xml` SHALL listar **apenas** os endereços institucionais e de comunidade, e
NEVER SHALL listar endereço individual de pessoa nem endereço de formulário.

Nenhum dos dois SHALL exigir requisição a domínio de terceiro, medir audiência,
identificar visitante ou guardar qualquer coisa no aparelho. (PRD-03 §10, `RF-03-51`,
`RN-03-21`, `RN-03-22`, documento 15 §1, princípio 6)

#### Scenario: O sitemap lista o institucional e as comunidades

- **WHEN** o `sitemap.xml` é buscado e há três comunidades publicadas
- **THEN** ele lista os endereços institucionais e os das três comunidades

#### Scenario: O sitemap não lista pessoa nem formulário

- **WHEN** o `sitemap.xml` é buscado
- **THEN** nenhum endereço individual de Guerreiro(a), Mestre ou Apoiador aparece nele,
  e nenhum endereço de formulário tampouco

#### Scenario: A descoberta não introduz terceiro nem medição

- **WHEN** qualquer tela pública é aberta
- **THEN** nenhuma requisição sai para domínio de terceiro e nada é guardado no aparelho

## MODIFIED Requirements

### Requirement: Quem não tem autorização vigente não aparece, e a revogação o retira na leitura seguinte

A App 06 NEVER SHALL exibir em card, página, portfólio ou ranking um Guerreiro(a) sem
autorização de divulgação vigente. Revogada a autorização, ele SHALL desaparecer das quatro
superfícies **na leitura seguinte**, e o endereço direto da página dele SHALL responder "não
encontrado". A vitrine NEVER SHALL guardar em cache no aparelho o que leu de um Guerreiro(a), de
modo que a revogação não sobreviva à leitura seguinte.

Pela mesma razão, o que a vitrine mostra de um Guerreiro(a) NEVER SHALL ser posto no
documento servido na publicação do site: conteúdo publicado dessa forma sobreviveria à
revogação até a publicação seguinte, e não há leitura seguinte que o retire. (`RF-03-13`,
`RF-03-14`, `RN-03-02`, `RN-03-03`, `RN-03-22`, PRD-03 §§5.7, 10)

#### Scenario: Sem autorização, não aparece em lugar nenhum

- **WHEN** um Guerreiro(a) não tem autorização vigente
- **THEN** ele não está em card, página, portfólio nem ranking, nem por endereço direto

#### Scenario: A revogação vale na leitura seguinte

- **WHEN** o responsável revoga a autorização e o visitante recarrega a vitrine
- **THEN** o Guerreiro(a) já não aparece em nenhuma das quatro superfícies

#### Scenario: A revogação não espera a publicação seguinte do site

- **WHEN** o responsável revoga a autorização e o visitante recarrega a vitrine sem que o
  site tenha sido publicado de novo
- **THEN** o Guerreiro(a) já não aparece em nenhuma das quatro superfícies

#### Scenario: A criação em equipe permanece com os demais autores

- **WHEN** um dos creditados de uma criação em equipe tem a autorização revogada
- **THEN** a vitrine apresenta o que o núcleo devolver, sem citar o revogado
