# aplicacao-da-vitrine Specification

## Purpose
A App 06 é a cara pública do projeto e a raiz do domínio da plataforma: a única superfície que
qualquer pessoa alcança sem se identificar, e que por isso não guarda nada de quem visita. Esta
capacidade cobre como a vitrine se apresenta sem login nem cadastro, como ela se identifica ao
núcleo mantendo o visitante anônimo, o que ela deliberadamente não faz — cookie, rastreador,
publicidade, preferência de visitante e autenticação —, os três recortes de leitura como
navegação e o botão "Entrar", que encaminha cada persona à aplicação dela.

## Requirements

### Requirement: A vitrine é pública, abre na raiz do domínio e não tem área restrita

A App 06 SHALL abrir inteira **sem login e sem cadastro**, servida na **raiz do domínio** da
plataforma. NEVER SHALL oferecer tela de cadastro, de área restrita ou de sessão própria, e
NEVER SHALL escrever qualquer coisa sobre um Guerreiro(a). (`RF-03-01`, `RN-03-01`)

#### Scenario: Visitante abre a vitrine

- **WHEN** alguém abre o endereço da raiz do domínio
- **THEN** a vitrine se apresenta inteira, sem pedir login nem cadastro

#### Scenario: Não há área restrita por onde entrar

- **WHEN** o visitante percorre a vitrine
- **THEN** nenhuma tela oferece cadastro, área restrita ou sessão da própria vitrine

### Requirement: A vitrine se identifica por chave de aplicação e o visitante segue anônimo

Toda chamada da App 06 ao núcleo SHALL levar a **chave da própria aplicação**, e NEVER SHALL
levar credencial de persona: a vitrine não tem persona autenticada. (`RN-03-33`)

#### Scenario: A aplicação se identifica com a própria chave

- **WHEN** a App 06 chama uma rota de dados do núcleo
- **THEN** a chamada leva a chave da App 06, e não a de outra aplicação

#### Scenario: Nenhuma chamada carrega credencial de persona

- **WHEN** a App 06 chama qualquer rota do núcleo
- **THEN** a chamada não leva credencial de persona alguma

### Requirement: A vitrine não guarda nada do visitante, no servidor ou no aparelho

A App 06 NEVER SHALL instalar cookie de rastreio, rastreador ou perfilamento do visitante, para
finalidade nenhuma, e NEVER SHALL guardar no aparelho preferência, escolha ou histórico de quem
visita. Havendo medição de audiência, ela SHALL ser agregada e sem identificador de visitante.
(`RF-03-51`, `RN-03-22`, PRD-03 §10)

#### Scenario: Nada é gravado no aparelho depois de uma visita inteira

- **WHEN** o visitante navega pela vitrine, troca de recorte e abre a pergunta do "Entrar"
- **THEN** nada da visita fica guardado no aparelho

#### Scenario: Nenhum rastreador de terceiro é carregado

- **WHEN** a vitrine carrega
- **THEN** nenhum cookie de rastreio, rastreador ou perfilamento é instalado

### Requirement: A vitrine não veicula publicidade nem patrocínio

A App 06 NEVER SHALL exibir publicidade ou patrocínio, e NEVER SHALL reservar espaço de tela
para eles. (`RF-03-50`, `RN-03-21`)

#### Scenario: Nenhuma tela traz anúncio

- **WHEN** o visitante percorre a vitrine
- **THEN** nenhuma tela exibe publicidade ou patrocínio, nem espaço reservado a eles

### Requirement: A vitrine oferece os três recortes de leitura, com sociedade civil como padrão

A App 06 SHALL oferecer os **três recortes de leitura** — sociedade civil, pesquisadores e
gestores públicos — e SHALL abrir no recorte **sociedade civil** sem que o visitante escolha
nada. (`RF-03-25`)

#### Scenario: A vitrine abre no recorte padrão

- **WHEN** o visitante abre a vitrine sem escolher recorte
- **THEN** ele está no recorte sociedade civil

#### Scenario: Os outros dois recortes estão alcançáveis

- **WHEN** o visitante procura outro recorte
- **THEN** pesquisadores e gestores públicos estão oferecidos na navegação

### Requirement: Trocar de recorte é navegação, e não cria área restrita nem coleta dado

A troca de recorte SHALL mudar a porta de entrada e a ordem do que é apresentado, e NEVER SHALL
mudar o conteúdo público disponível nem o direito de acesso. NEVER SHALL criar área restrita,
pedir cadastro, coletar dado do visitante ou guardar o recorte escolhido. (`RF-03-26`,
`RF-03-51`, `RN-03-22`)

#### Scenario: O recorte não muda o direito de acesso

- **WHEN** o visitante troca do recorte sociedade civil para pesquisadores
- **THEN** ele segue na mesma vitrine pública, sem cadastro e sem nada bloqueado

#### Scenario: O recorte escolhido não sobrevive à visita

- **WHEN** o visitante troca de recorte e volta à vitrine depois
- **THEN** a vitrine abre outra vez no recorte sociedade civil

### Requirement: O botão "Entrar" fica sempre visível e pergunta qual persona está entrando

A App 06 SHALL manter o botão **"Entrar"** visível em toda tela pública, e ao ser acionado ele
SHALL perguntar **quem está entrando**, apresentando as personas que têm aplicação: Guerreiro(a),
responsável, Mestre, Apoiador, gestão e o **aparelho da aula**. (`RF-03-58`, PRD-03 §5.9)

#### Scenario: O botão está em toda tela

- **WHEN** o visitante está em qualquer tela pública da vitrine
- **THEN** o botão "Entrar" está visível

#### Scenario: O botão pergunta antes de encaminhar

- **WHEN** o visitante aciona "Entrar"
- **THEN** a vitrine pergunta qual persona está entrando, sem encaminhar ninguém antes da
  resposta

### Requirement: Cada persona é encaminhada à sua aplicação, e a vitrine nunca autentica

Escolhida a persona, a App 06 SHALL encaminhar o visitante ao endereço da aplicação dela —
Guerreiro(a) à App 05, responsável à App 07, Mestre à App 09, Apoiador à App 08, gestão à App 03
e o aparelho da aula à App 01. A vitrine NEVER SHALL conferir nick, imagem, login social, senha
ou qualquer credencial: quem autentica é a aplicação de destino. (`RF-03-59`, `RN-03-27`)

#### Scenario: A persona escolhida chega à aplicação dela

- **WHEN** o visitante declara que é Mestre
- **THEN** ele é encaminhado ao endereço da App 09

#### Scenario: Nenhum campo de credencial existe na vitrine

- **WHEN** o visitante percorre a pergunta do "Entrar" inteira
- **THEN** nenhuma tela pede nick, imagem, senha ou login

### Requirement: A escolha de persona não é guardada

A App 06 NEVER SHALL guardar a persona escolhida, no servidor ou no aparelho: quem volta SHALL
encontrar a mesma pergunta. (`RF-03-60`, `RN-03-22`)

#### Scenario: A pergunta se repete na visita seguinte

- **WHEN** o visitante já escolheu uma persona antes e abre a vitrine outra vez
- **THEN** o "Entrar" pergunta novamente qual persona está entrando, sem escolha pré-marcada

### Requirement: Nenhuma tela de entrada revela nick, conta ou existência de cadastro

As telas do "Entrar" NEVER SHALL apresentar lista de nicks, sugestão, completação ou qualquer
confirmação de que uma conta existe ou não existe na plataforma. (`RF-03-61`)

#### Scenario: A entrada não lista quem existe

- **WHEN** o visitante escolhe a persona Guerreiro(a)
- **THEN** nenhum nick, conta ou cadastro é apresentado ou confirmado

### Requirement: Quem não tem cadastro recebe a orientação da sua persona, sem promessa de acesso

Para cada persona, a App 06 SHALL oferecer a orientação de quem **ainda não tem cadastro**, e
NEVER SHALL prometer acesso: entrar não cria cadastro. A orientação SHALL ser a da própria
persona — **pré-cadastro da App 08** para quem quer ser Apoiador, **formulário de participação da
vitrine** para quem quer ser Mestre, e **procurar a gestão no encontro** para responsável e
Guerreiro(a). Enquanto o formulário de participação não existir na vitrine, a orientação do
Mestre SHALL nomear o caminho em texto, e NEVER SHALL apresentar link que não resolve.
(`RF-03-62`, PRD-03 §5.9)

#### Scenario: Quem quer ser Apoiador é levado ao pré-cadastro

- **WHEN** o visitante declara que é Apoiador e diz que não tem cadastro
- **THEN** a orientação o leva ao pré-cadastro da App 08

#### Scenario: Responsável e Guerreiro(a) são orientados a procurar a gestão

- **WHEN** o visitante declara que é responsável, ou Guerreiro(a), e diz que não tem cadastro
- **THEN** a orientação é procurar a gestão no encontro, sem promessa de acesso

#### Scenario: A orientação do Mestre não oferece link quebrado

- **WHEN** o visitante declara que quer ser Mestre e o formulário de participação ainda não
  existe na vitrine
- **THEN** a orientação nomeia o formulário em texto, sem link
