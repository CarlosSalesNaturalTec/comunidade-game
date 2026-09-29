# Spec Delta

## MODIFIED Requirements

### Requirement: A vitrine não guarda nada do visitante, no servidor ou no aparelho

A App 06 NEVER SHALL instalar cookie de rastreio, rastreador ou perfilamento do visitante, para
finalidade nenhuma, e NEVER SHALL guardar no aparelho preferência, escolha ou histórico de quem
visita. NEVER SHALL guardar **favorito** ou pessoa acompanhada, em lugar nenhum — nem no
servidor, nem no aparelho, nem em parâmetro de rota —, porque favoritar é função de **Apoiador
cadastrado na App 08**, e lá é leitura: não abre canal de contato. Havendo medição de audiência,
ela SHALL ser agregada e sem identificador de visitante. (`RF-03-38`, `RF-03-51`, `RN-03-15`,
`RN-03-16`, `RN-03-22`, PRD-03 §10)

#### Scenario: Nada é gravado no aparelho depois de uma visita inteira

- **WHEN** o visitante navega pela vitrine, troca de recorte e abre a pergunta do "Entrar"
- **THEN** nada da visita fica guardado no aparelho

#### Scenario: Nenhum rastreador de terceiro é carregado

- **WHEN** a vitrine carrega
- **THEN** nenhum cookie de rastreio, rastreador ou perfilamento é instalado

#### Scenario: Pedir para acompanhar não cria favorito

- **WHEN** o visitante aciona a ação de acompanhar em uma página individual e depois recarrega
  a vitrine
- **THEN** nenhum favorito e nenhuma pessoa acompanhada existem em lugar nenhum, e a vitrine
  está idêntica à primeira visita

### Requirement: "Contatos" e "Como apoiar" exibem o que foi publicado, e "Como apoiar" traz a chave PIX

A App 06 SHALL exibir a seção **"Contatos"** e a seção **"Como apoiar"** com o texto publicado,
na ordem do recorte, sem publicidade nem patrocínio. Em "Como apoiar" SHALL aparecer a **chave
PIX da pessoa jurídica vinculada**, com o titular, e as **necessidades de recurso em aberto**.
A exibição SHALL vir do que o núcleo devolve, e nenhum valor SHALL ficar escrito na aplicação.
(`RF-03-45`, `RF-03-46`, `RF-03-47`, `RN-03-21`)

#### Scenario: A chave PIX aparece em "Como apoiar"

- **WHEN** o visitante abre "Como apoiar" com o texto semeado
- **THEN** a tela mostra a chave PIX e o titular

#### Scenario: A chave publicada é a que o Admin editou

- **WHEN** o Admin republica "Como apoiar" com outra chave
- **THEN** a tela mostra a chave nova, sem depender de nova versão da aplicação

#### Scenario: Seção não publicada diz isso

- **WHEN** "Contatos" não tem texto publicado
- **THEN** a tela diz que o conteúdo ainda não foi publicado

#### Scenario: As necessidades em aberto aparecem em "Como apoiar"

- **WHEN** o visitante abre "Como apoiar" e há necessidade de recurso em aberto
- **THEN** a tela lista as necessidades, sem depender de passar pela porta do convite

## ADDED Requirements

### Requirement: Toda página individual traz a chamada "Quero participar", e acompanhar leva à mesma porta

A App 06 SHALL apresentar, em **toda página individual** que publica, a chamada **"Quero
participar"**, e SHALL apresentar na mesma página a **ação de acompanhar ou favoritar**, que
SHALL levar à **mesma porta** da chamada. As duas SHALL abrir a porta do convite sem exigir
cadastro, login ou dado do visitante. (`RF-03-39`, `RF-03-40`, PRD-03 §5.5)

#### Scenario: A página do Guerreiro(a) convida

- **WHEN** o visitante abre a página individual de um Guerreiro(a) com autorização vigente
- **THEN** a página traz a chamada "Quero participar" e a ação de acompanhar

#### Scenario: A página da comunidade convida

- **WHEN** o visitante abre a página de uma Comunidade Virtual
- **THEN** a página traz a chamada "Quero participar" e a ação de acompanhar

#### Scenario: Acompanhar chega à porta do convite

- **WHEN** o visitante aciona a ação de acompanhar
- **THEN** a porta do convite abre, a mesma que a chamada "Quero participar" abre

### Requirement: A chamada é do projeto e a porta não sabe quem estava sendo visto

A chamada SHALL ser **do projeto**, e NEVER SHALL oferecer apoiar, apadrinhar ou favorecer a
pessoa ou a comunidade exibida na página de origem. A porta NEVER SHALL receber nick, nome,
identificador ou qualquer marca de quem estava sendo visto — nem no endereço, nem em parâmetro,
nem em estado da aplicação —, e nenhuma tela dela SHALL citar essa pessoa. (`RF-03-41`,
`RN-03-25`, PRD-03 §5.5)

#### Scenario: A porta não cita a pessoa da página de origem

- **WHEN** o visitante aciona a chamada na página individual de um Guerreiro(a)
- **THEN** a porta abre sem citar o nick nem o nome de quem estava sendo visto, e o endereço da
  porta não os carrega

#### Scenario: A chamada não vincula o apoio a quem está na tela

- **WHEN** o visitante lê a chamada em uma página individual
- **THEN** ela convida a participar do projeto, e não a apoiar a pessoa ou a comunidade da
  página

### Requirement: A porta abre com o garfo do que a pessoa traz e encaminha

A porta SHALL abrir perguntando **o que a pessoa traz** e SHALL encaminhar conforme a resposta:
quem traz **dinheiro** ao **pré-cadastro da App 08**; quem traz **insumo, equipamento ou
alimento, serviço, conteúdo educacional, código, divulgação** ou a **pretensão de ensinar** ao
**formulário de solicitação de participação da vitrine**. A porta SHALL nomear, em cada
modalidade, o comprobatório que ela pede. O encaminhamento NEVER SHALL exigir campo que o
formulário não tem, e a escolha da modalidade NEVER SHALL ser guardada. (`RF-03-42`, documento 14
§§10, 11, documento 02 §1, decisão do fundador de 2026-09-29)

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

### Requirement: A porta apresenta o que é ser Apoiador e declara que nada ali cria acesso

A porta SHALL apresentar o que é ser Apoiador — **aportar**, **propor desafios extras** e
**acompanhar favoritos** — e SHALL declarar, **antes de qualquer envio**, que nada ali cria
cadastro nem acesso: quem cadastra Apoiador é um **Admin**, que confere o comprovante, com prazo
de **7 dias**. A porta NEVER SHALL pedir credencial, senha ou documento do visitante.
(`RF-03-42`, `RN-03-17`, PRD-03 §5.5)

#### Scenario: A porta explica o papel antes de encaminhar

- **WHEN** o visitante abre a porta
- **THEN** a tela explica que o Apoiador aporta, propõe desafios extras e acompanha favoritos

#### Scenario: A porta declara que não cria cadastro nem acesso

- **WHEN** o visitante lê a porta
- **THEN** a tela diz que nada ali cria cadastro nem acesso, que um Admin avalia e que o prazo
  é de 7 dias

### Requirement: A porta oferece também doar pela chave PIX e ver as necessidades em aberto

A porta SHALL oferecer, a quem não quer se cadastrar agora, os dois caminhos que dispensam
cadastro: **doar pela chave PIX** da pessoa jurídica vinculada, a mesma que "Como apoiar"
publica, e **ver as necessidades de recurso em aberto**. A chave PIX SHALL vir do que o núcleo
devolve, e nenhum valor SHALL ficar escrito na aplicação. (`RF-03-43`, `RF-03-46`, PRD-03 §5.5)

#### Scenario: Quem não quer se cadastrar encontra o PIX

- **WHEN** o visitante abre a porta com "Como apoiar" publicado
- **THEN** a porta mostra a chave PIX e o titular, sem pedir cadastro

#### Scenario: A porta mostra o que falta hoje

- **WHEN** o visitante abre a porta e há necessidade de recurso em aberto
- **THEN** a porta lista as necessidades em aberto

### Requirement: Recusar o convite devolve o visitante à navegação, sem gravar nada

A porta SHALL oferecer a saída de quem desiste, que SHALL devolver o visitante à navegação
pública. A recusa NEVER SHALL gravar nada sobre a visita, em lugar nenhum, e NEVER SHALL
insistir, repetir o convite nem impedir a saída. (`RF-03-44`, `RF-03-38`, `RN-03-15`,
PRD-03 §5.5)

#### Scenario: Quem desiste volta à navegação

- **WHEN** o visitante abre a porta e aciona a saída
- **THEN** ele volta à navegação pública, sem ter preenchido nada

#### Scenario: A recusa não deixa marca

- **WHEN** o visitante recusa o convite e depois recarrega a vitrine
- **THEN** nada da recusa foi gravado, e a vitrine está idêntica à primeira visita

### Requirement: A vitrine publica as necessidades de recurso em aberto, sem pessoa e sem reais

A App 06 SHALL publicar as **necessidades de recurso em aberto** com **tipo de recurso**,
**quantidade que falta**, **valor em moedas**, **comunidade**, **ponto de apoio**, **data e
horário da aula**. Necessidade cujo tipo está sem vigência de referência SHALL aparecer **sem
valor em moedas**, e NEVER SHALL aparecer com valor arbitrado pela aplicação. Nenhuma linha
SHALL exibir valor em reais, e nenhuma SHALL identificar Guerreiro(a), responsável ou provedor.
Não havendo necessidade em aberto, a tela SHALL dizer isso. (`RF-03-47`, `RF-03-10`, `RN-03-18`)

#### Scenario: A necessidade sai com o que o PRD pede

- **WHEN** a vitrine publica uma necessidade em aberto
- **THEN** a linha traz tipo de recurso, quantidade que falta, valor em moedas, comunidade,
  ponto de apoio e a data com o horário da aula

#### Scenario: Nenhuma linha traz reais nem pessoa

- **WHEN** o visitante lê as necessidades em aberto
- **THEN** nenhuma linha exibe valor em reais e nenhuma identifica Guerreiro(a), responsável ou
  provedor

#### Scenario: Tipo sem vigência aparece sem moedas

- **WHEN** a necessidade chega do núcleo sem valor em moedas
- **THEN** a linha aparece sem o valor, e a aplicação não arbitra nenhum

#### Scenario: Sem necessidade em aberto a tela diz isso

- **WHEN** não há necessidade de recurso em aberto
- **THEN** a tela diz que nenhuma necessidade está em aberto
