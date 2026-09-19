## ADDED Requirements

### Requirement: O limiar de comparação é medido por ponto de apoio, e sem ele não se reconhece

O **limiar de comparação** SHALL ser dado de cada **ponto de apoio**, nascido de uma medição
feita no aparelho do encontro, e NEVER SHALL ser parâmetro de implantação: nenhuma variável de
ambiente SHALL declará-lo. (`RF-01-73`, documento 03 §3.3, decisão do fundador, 2026-09-18)

O núcleo SHALL gravar cada medição com o **ponto de apoio**, o **limiar**, as **duas séries de
distâncias** que o produziram, **quem mediu** e **quando**. O limiar vigente de um ponto de apoio
SHALL ser o da medição **mais recente** dele. A gravação SHALL exigir Mestre ou Admin pela
matriz de permissões, e o núcleo NEVER SHALL aceitar descritor nesta rota. (`RF-01-73`,
`RF-01-16`, `RN-01-15`)

A comparação de um Guerreiro(a) SHALL usar o limiar vigente do ponto de apoio **da aula em que a
entrada acontece**. Ponto de apoio **sem limiar medido** SHALL fazer a comparação **recusar**, e
essa recusa SHALL ser indistinguível das demais. (`RF-01-73`, `RN-01-56`, `RN-01-22`)

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

#### Scenario: A rota da medição não aceita descritor

- **WHEN** chega uma gravação de limiar com descritor no corpo
- **THEN** o núcleo a recusa e nada é gravado

## MODIFIED Requirements

### Requirement: Ao núcleo chega descritor, nunca imagem

O núcleo SHALL aceitar apenas o **descritor** gerado no aparelho e SHALL NOT aceitar fotografia
em nenhuma rota. O descritor SHALL ser recusado com 422 quando não tiver o formato esperado. O
_template_ SHALL servir exclusivamente para identificar o Guerreiro(a) — presença e autenticação
—, e nenhuma rota SHALL usá-lo para outra finalidade. (`RF-01-05`, `RN-01-15`, PRD-01 §§3.2, 11)

A **dimensão esperada** do descritor é a da biblioteca de reconhecimento facial decidida no
documento 03 §3.3, e SHALL ser fixa no núcleo, com a origem declarada junto dela. Ela NEVER
SHALL ser parâmetro de implantação: não admite calibração — ou casa com o que a aplicação gera,
ou nenhuma captura é aceita. O ambiente NEVER SHALL poder declará-la, e trocá-la é trocar de
biblioteca. (`RF-01-05`, documento 03 §3.3, decisão do fundador, 2026-09-17)

O **limiar de comparação** também NEVER SHALL ser parâmetro de implantação, por motivo oposto:
ele admite calibração, e depende da câmera e da luz de cada espaço. Ele é **medido por ponto de
apoio**, no encontro. (`RF-01-73`, decisão do fundador, 2026-09-18)

#### Scenario: Envio de imagem é recusado

- **WHEN** chega uma requisição com fotografia de Guerreiro(a) em qualquer rota do núcleo
- **THEN** o núcleo a recusa e nada é gravado

#### Scenario: Descritor malformado é recusado

- **WHEN** chega um descritor fora do formato esperado
- **THEN** o núcleo responde 422 indicando o campo em falta e nenhum _template_ é gravado

#### Scenario: O descritor que a aplicação gera é aceito

- **WHEN** chega o descritor gerado pela biblioteca do documento 03 §3.3, na dimensão dela
- **THEN** o núcleo o aceita, e a dimensão conferida é a mesma em todo ambiente

#### Scenario: A dimensão não se declara no ambiente

- **WHEN** se procura uma variável de ambiente que fixe a dimensão do descritor
- **THEN** nenhuma existe, e o valor conferido vem do próprio núcleo
