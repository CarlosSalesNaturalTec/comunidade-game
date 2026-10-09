# Spec Delta

## ADDED Requirements

### Requirement: Cada endereço público com arquivo publicado é servido por aquele arquivo

A App 06 SHALL servir cada endereço público para o qual exista arquivo publicado com o
documento **daquela rota**, e NEVER SHALL atendê-lo pela casca da página de pessoa. Vale
para os três recortes de leitura, a área detalhada de coleta, a porta do convite, os
dois formulários públicos, a Área do Apoiador Desenvolvedor e a página de cada
comunidade. (PRD-03 §10, `RF-03-15`, `RF-03-25`, `RF-03-26`, `RF-03-42`, `RF-03-52`,
`RF-03-67`)

#### Scenario: Um recorte de leitura abre no endereço próprio

- **WHEN** o visitante abre o endereço de pesquisadores ou de gestores públicos
- **THEN** a tela daquele recorte abre, com as seções que o PRD-03 §5 lhe dá, e nenhuma
  mensagem de endereço não encontrado

#### Scenario: A página da comunidade abre no endereço que o sitemap declara

- **WHEN** um endereço de comunidade listado no `sitemap.xml` é aberto
- **THEN** o documento devolvido é o daquela comunidade, e não o da casca de pessoa

#### Scenario: A casca de pessoa atende só o que não tem arquivo publicado

- **WHEN** um endereço público com arquivo publicado é aberto
- **THEN** a casca de pessoa não o atende, e a etiqueta de não indexar não alcança aquele
  documento

#### Scenario: O endereço público não depende da extensão do arquivo

- **WHEN** o visitante abre um endereço público sem a extensão do arquivo que o serve
- **THEN** a tela abre naquele endereço, que é o mesmo que a canônica e o `sitemap.xml`
  declaram

### Requirement: A configuração de acesso ao núcleo alcança as seções no navegador

A configuração que a App 06 declara — chave de aplicação e endereço do núcleo — SHALL
alcançar o código executado **no navegador**, e não apenas o da publicação do site. Toda
seção que lê dado na visita SHALL conseguir chamar o núcleo. (`RF-03-02`, `RF-03-15`,
`RN-03-33`)

#### Scenario: Uma seção de leitura alcança o núcleo na visita

- **WHEN** uma seção que lê dado é apresentada ao visitante
- **THEN** a chamada ao núcleo sai levando a chave da App 06, e a seção apresenta o que
  foi lido

#### Scenario: A leitura que falha falha pelo núcleo, e não pela configuração

- **WHEN** uma seção que lê dado é apresentada e o núcleo não responde
- **THEN** a seção declara que não conseguiu carregar por causa da resposta do núcleo, e
  nunca porque a configuração de acesso não a alcançou

#### Scenario: O conteúdo da publicação não supre a leitura da visita

- **WHEN** a abertura é apresentada com o institucional que veio da publicação
- **THEN** as seções que leem na visita também apresentam o que leram, e a tela não fica
  com o institucional de pé e todas as demais seções em erro
