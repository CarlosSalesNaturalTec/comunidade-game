## MODIFIED Requirements

### Requirement: O limiar de comparação é medido por ponto de apoio, e sem ele não se reconhece

O **limiar de comparação** SHALL ser dado de cada **ponto de apoio**, nascido de uma medição
feita no aparelho do encontro, e NEVER SHALL ser parâmetro de implantação: nenhuma variável de
ambiente SHALL declará-lo. (`RF-01-73`, documento 03 §3.3, decisão do fundador, 2026-09-18)

O núcleo SHALL gravar cada medição com o **ponto de apoio**, o **limiar**, as **duas séries de
distâncias** que o produziram, **quem mediu** e **quando**. O limiar vigente de um ponto de apoio
SHALL ser o da medição **mais recente** dele. A gravação SHALL exigir Mestre ou Admin pela
matriz de permissões, e o núcleo NEVER SHALL aceitar descritor nesta rota. (`RF-01-73`,
`RF-01-16`, `RN-01-15`)

A comparação de um Guerreiro(a) **no encontro** SHALL usar o limiar vigente do ponto de apoio
**da aula em que a entrada acontece**. Ponto de apoio **sem limiar medido** SHALL fazer a
comparação **recusar**, e essa recusa SHALL ser indistinguível das demais. (`RF-01-73`,
`RN-01-56`, `RN-01-22`)

A comparação **fora do encontro** — o pedido que não traz aula — SHALL usar o **maior** limiar
vigente entre os pontos de apoio **ativos** da comunidade do **vínculo vigente** do
Guerreiro(a). É o mais frouxo deles: o valor é **emprestado**, medido em espaço que não é o
daquela câmera, e a escolha é a que não tranca a criança fora da aplicação, já que o responsável
abre a sessão quando a comparação recusa. Ponto de apoio **inativo** NEVER SHALL entrar na
conta. Guerreiro(a) **sem vínculo vigente**, e comunidade **sem nenhum ponto de apoio com limiar
medido**, SHALL fazer a comparação recusar, de forma indistinguível das demais.
(`RN-01-57`, `RN-01-56`, `RN-01-22`, documento 03 §3.3, decisão do fundador, 2026-09-21)

A **resolução do limiar** fora do encontro SHALL custar o mesmo qualquer que seja o desfecho —
Guerreiro(a) inexistente, vínculo encerrado, comunidade sem medição ou comparação que confere —
e SHALL NOT variar com **quantos** pontos de apoio a comunidade tem. Um custo que crescesse com
a comunidade, ou que caísse quando o nick não existe, deixaria sondar nick pelo relógio.
(`RN-01-22`, `RN-01-57`)

Toda comparação SHALL continuar sendo auditada, inclusive a que recusa por ausência de limiar.
(`RN-01-14`)

#### Scenario: O limiar não se declara no ambiente

- **WHEN** se procura uma variável de ambiente que fixe o limiar de comparação
- **THEN** nenhuma existe, e o valor usado vem da medição do ponto de apoio

#### Scenario: A medição grava o limiar com as séries que o produziram

- **WHEN** Mestre ou Admin confirma o limiar ao fim de uma medição concluída
- **THEN** o núcleo grava o limiar, as duas séries de distâncias, quem mediu e quando, e passa a
  usá-lo como vigente daquele ponto de apoio

#### Scenario: Medição nova substitui a anterior sem apagá-la

- **WHEN** um ponto de apoio já medido recebe uma medição nova
- **THEN** o limiar vigente passa a ser o da medição nova, e a anterior continua consultável

#### Scenario: Ponto de apoio sem limiar não reconhece ninguém

- **WHEN** chega um pedido de sessão por nick e imagem numa aula cujo ponto de apoio não tem
  limiar medido
- **THEN** o núcleo recusa de forma indistinguível das demais recusas, a comparação é auditada e
  a entrada acontece pela confirmação humana

#### Scenario: Fora do encontro vale o mais frouxo da comunidade

- **WHEN** chega um pedido sem aula de um Guerreiro(a) cuja comunidade tem dois pontos de apoio
  ativos com limiares medidos diferentes
- **THEN** a comparação usa o maior dos dois

#### Scenario: Ponto de apoio inativo não empresta limiar

- **WHEN** o maior limiar da comunidade é o de um ponto de apoio desativado
- **THEN** ele fica fora da conta, e vale o maior entre os ativos

#### Scenario: Comunidade sem medição alguma não reconhece fora do encontro

- **WHEN** chega um pedido sem aula de um Guerreiro(a) cuja comunidade não tem ponto de apoio
  algum com limiar medido
- **THEN** o núcleo recusa de forma indistinguível das demais recusas, e a comparação é auditada

#### Scenario: O limiar emprestado não atravessa comunidade

- **WHEN** chega um pedido sem aula e existem limiares medidos em outra comunidade
- **THEN** nenhum deles é considerado: a busca parte do vínculo vigente do próprio Guerreiro(a)

#### Scenario: A rota da medição não aceita descritor

- **WHEN** chega uma gravação de limiar com descritor no corpo
- **THEN** o núcleo a recusa e nada é gravado
