## Purpose

O responsável é quem responde pela criança perante a plataforma. Esta capacidade cobre como ele
entra no núcleo — cadastrado por Admin ou Mestre, depois de se apresentar pessoalmente —, o
vínculo que o liga a Guerreiros e Guerreiras já cadastrados com o grau de parentesco declarado,
o teto de três responsáveis por criança e o recorte de leitura que esse vínculo impõe: ele
enxerga os seus, e só os seus.

## Requirements

### Requirement: Admin ou Mestre cadastra o responsável

O núcleo SHALL permitir que um Admin ou um Mestre cadastre a persona de responsável. O
responsável SHALL ser a única persona que o Mestre cadastra. O cadastro NEVER SHALL, por si só,
dar ao responsável acesso a Guerreiro(a) algum — o que ele alcança vem do vínculo, não do
cadastro.
Persona de outro papel que tentar cadastrar responsável SHALL receber **403**. (`RF-01-13`,
`RN-01-01`, PRD-01 §§4, 5.3, 9)

O cadastro SHALL receber o **nome** do responsável, e SHALL recusá-lo em branco: é sobre esse
nome que se apoia o consentimento que autoriza a captura da imagem da criança, e responsável sem
nome não sustenta a base legal do tratamento. O cadastro NEVER SHALL exigir e-mail, credencial de
acesso ou a digitalização do termo — o acesso à App 07 e o arquivo do documento continuam sendo
atos da gestão, depois do encontro. (`RF-04-60`, PRD-04 §§3.2, 11, PRD-13 §11, documento 09 —
decisão do fundador, 2026-08-24)

O cadastro SHALL aceitar o **e-mail** do responsável como campo **opcional**. Informado, o
núcleo SHALL criar, na mesma transação, a credencial de **login social** identificada por esse
e-mail, para que o responsável entre na App 07 pela conta Google. E-mail que já identifica a
credencial social ativa de outra persona SHALL ser recusado com **422**, e nada é criado.
(`RF-01-92`, `RF-01-13`, documento 03 §1.1, decisão do fundador de 2026-11-27)

#### Scenario: Mestre cadastra responsável

- **WHEN** um Mestre cadastra a persona de um responsável com o nome dela
- **THEN** o núcleo cria a persona de responsável, guarda o nome e registra a autoria do Mestre

#### Scenario: Cadastro sem nome é recusado

- **WHEN** o cadastro de responsável chega sem nome, ou com nome em branco
- **THEN** o núcleo responde 422 indicando o campo em falta, e nenhuma persona é criada

#### Scenario: O cadastro não cria acesso

- **WHEN** um responsável é cadastrado no encontro só com o nome
- **THEN** nenhuma credencial de acesso nasce com ele, e a entrada na App 07 continua dependendo
  de ato da gestão

#### Scenario: O cadastro com e-mail abre o login social

- **WHEN** um Admin ou um Mestre cadastra um responsável com nome e e-mail
- **THEN** o núcleo grava o e-mail e cria a credencial de login social com ele, e o responsável
  passa a abrir sessão pela conta Google desse e-mail

#### Scenario: E-mail de outra pessoa é recusado no cadastro

- **WHEN** o e-mail informado já identifica a credencial social ativa de outra persona
- **THEN** o núcleo responde 422 indicando o campo, e nenhuma persona nem credencial é criada

#### Scenario: Responsável recém-cadastrado não alcança ninguém

- **WHEN** um responsável acabou de ser cadastrado e ainda não tem vínculo
- **THEN** ele autentica normalmente e não enxerga Guerreiro(a) algum

#### Scenario: Papel sem permissão não cadastra responsável

- **WHEN** uma persona que não é Admin nem Mestre tenta cadastrar um responsável
- **THEN** o núcleo responde 403 e nenhuma persona é criada

### Requirement: O vínculo declara o grau de parentesco

O núcleo SHALL registrar o vínculo entre um responsável e um Guerreiro(a) com o **grau de
parentesco em texto livre**, quem o cadastrou — Admin ou Mestre — e o início da vigência. O grau
de parentesco SHALL ser exigido em cada vínculo, e cada vínculo SHALL carregar o seu, ainda que
envolvam o mesmo responsável ou o mesmo Guerreiro(a). (`RF-01-13`, `RN-01-19`, PRD-01 §8)

#### Scenario: Vínculo sem grau de parentesco é recusado

- **WHEN** um vínculo é pedido sem o grau de parentesco
- **THEN** o núcleo responde 422 indicando o campo em falta, e nenhum vínculo é criado

#### Scenario: Cada vínculo carrega o seu grau

- **WHEN** o mesmo Guerreiro(a) é vinculado a dois responsáveis com graus diferentes
- **THEN** cada vínculo guarda o grau declarado nele, sem que um sobrescreva o outro

#### Scenario: O vínculo registra quem o cadastrou

- **WHEN** um Admin ou um Mestre cria um vínculo
- **THEN** o registro guarda quem cadastrou e o início da vigência

### Requirement: O vínculo só alcança Guerreiro(a) já cadastrado

O núcleo SHALL vincular ao responsável apenas Guerreiro(a) **já cadastrado**. Nem o cadastro do
responsável nem a criação do vínculo NEVER SHALL criar a persona do Guerreiro(a): o autocadastro
da criança acontece no onboarding e é o único caminho que a cria. (`RN-01-20`, `RN-01-01`)

#### Scenario: Vínculo a Guerreiro(a) inexistente é recusado

- **WHEN** um vínculo é pedido para um Guerreiro(a) que não está cadastrado
- **THEN** o núcleo recusa o vínculo e nenhuma persona de Guerreiro(a) é criada

#### Scenario: Cadastrar responsável não cria criança

- **WHEN** um responsável é cadastrado informando as crianças sob sua responsabilidade
- **THEN** o núcleo cria apenas a persona do responsável, e o vínculo só alcança quem já existe

### Requirement: No máximo três responsáveis por Guerreiro(a)

O núcleo SHALL recusar, com **422**, o vínculo que faria o mesmo Guerreiro(a) passar de **três**
responsáveis vigentes. Os vínculos já existentes SHALL permanecer válidos, cada um com o seu grau
de parentesco. A contagem SHALL considerar apenas os vínculos **vigentes**: vínculo encerrado
NEVER SHALL ocupar vaga. (`RF-01-14`, `RN-01-19`, PRD-01 §§9, 12, documento 02 §1)

#### Scenario: O quarto vínculo é recusado

- **WHEN** um quarto responsável é vinculado a um Guerreiro(a) que já tem três vínculos vigentes
- **THEN** o núcleo responde 422, e os três vínculos existentes continuam válidos, cada um com o
  seu grau de parentesco

#### Scenario: O terceiro vínculo é aceito

- **WHEN** um terceiro responsável é vinculado a um Guerreiro(a) que tem dois vínculos vigentes
- **THEN** o núcleo cria o vínculo

#### Scenario: Vínculo encerrado abre vaga

- **WHEN** um Guerreiro(a) tem três vínculos, um deles já encerrado, e um novo responsável é
  vinculado a ele
- **THEN** o núcleo cria o vínculo, porque só os vigentes ocupam vaga

#### Scenario: O teto é por Guerreiro(a), não por responsável

- **WHEN** um mesmo responsável é vinculado a vários Guerreiros e Guerreiras
- **THEN** o núcleo aceita todos, porque o limite conta responsáveis de uma criança e não
  crianças de um responsável

### Requirement: O responsável enxerga apenas os Guerreiros e Guerreiras vinculados

O núcleo SHALL restringir o que a persona de responsável lê aos Guerreiros e Guerreiras
vinculados a ela. Consulta de dado de Guerreiro(a) sem vínculo com o responsável em sessão SHALL
ser recusada, e o resultado de uma consulta dele NEVER SHALL trazer criança que não seja sua. O
recorte SHALL valer por vínculo, e não por comunidade: dois responsáveis da mesma comunidade não
enxergam as crianças um do outro. (`RF-01-15`, `RF-01-16`, PRD-01 §4)

#### Scenario: A consulta do responsável traz só os vinculados

- **WHEN** um responsável com dois Guerreiros vinculados consulta os que estão sob sua
  responsabilidade
- **THEN** o resultado traz esses dois e nenhum outro

#### Scenario: Guerreiro(a) sem vínculo não é alcançado

- **WHEN** um responsável pede o dado de um Guerreiro(a) que não está vinculado a ele
- **THEN** o núcleo recusa a consulta e não devolve dado algum daquela criança

#### Scenario: A comunidade não amplia o alcance do responsável

- **WHEN** um responsável consulta dado de um Guerreiro(a) da mesma comunidade dos seus, sem
  vínculo com ele
- **THEN** o núcleo recusa, porque o recorte do responsável é o vínculo e não a comunidade

### Requirement: O responsável lê os próprios vinculados, com o grau de parentesco

O núcleo SHALL servir à persona de **responsável em sessão** a lista dos Guerreiros e Guerreiras
**vinculados a ela por vínculo vigente**, e cada item SHALL trazer o **grau de parentesco**
declarado naquele vínculo, para que a aplicação apresente de quem se trata sem que o responsável
precise informá-lo. A lista NEVER SHALL trazer Guerreiro(a) sem vínculo vigente com quem está em
sessão, e persona de outro papel SHALL receber **403**. (`RF-13-04`, `RF-13-05`, `RN-13-04`,
`RF-01-15`)

#### Scenario: O responsável com dois vinculados vê os dois

- **WHEN** um responsável com dois vínculos vigentes pede os seus Guerreiros e Guerreiras
- **THEN** o núcleo devolve os dois, cada um com o grau de parentesco daquele vínculo

#### Scenario: Criança de outro responsável não entra na lista

- **WHEN** existe Guerreiro(a) ativo sem vínculo com o responsável em sessão, ainda que da mesma
  comunidade
- **THEN** ele não aparece na lista daquele responsável

#### Scenario: Vínculo encerrado sai da lista

- **WHEN** um vínculo do responsável já tem fim registrado
- **THEN** o Guerreiro(a) daquele vínculo não aparece na lista

#### Scenario: Persona de outro papel não usa a leitura do responsável

- **WHEN** uma persona que não é responsável chama a leitura dos seus vinculados
- **THEN** o núcleo responde 403 e nada é devolvido

### Requirement: O Mestre lê os Guerreiros e Guerreiras que pode vincular

O núcleo SHALL servir à persona de **Mestre em sessão** a lista dos Guerreiros e Guerreiras que
ele pode vincular a um responsável, recortada pelas **comunidades em que ele atua**: Guerreiro(a)
de comunidade em que o Mestre não atua NEVER SHALL aparecer nela. Cada item SHALL trazer o
**nick** e o **avatar**, e NEVER SHALL trazer imagem real, nome civil, data de nascimento nem
contato — a identificação do Guerreiro(a) para o Mestre é por nick e avatar. A leitura SHALL
alcançar apenas Guerreiros e Guerreiras **já cadastrados e ativos**, e NEVER SHALL criar persona
alguma. Persona de outro papel SHALL receber **403**. (`RF-09-62`, `RN-01-20`, `RN-09-18`,
invariante 12 do documento 99 §6, decisão do fundador, 2026-08-29, documento 09 §1)

#### Scenario: O Mestre vê quem pode vincular

- **WHEN** um Mestre em sessão pede os Guerreiros e Guerreiras que pode vincular
- **THEN** o núcleo devolve os ativos das comunidades em que ele atua, cada um com nick e avatar

#### Scenario: Guerreiro(a) de outra comunidade não aparece

- **WHEN** existe Guerreiro(a) ativo em comunidade na qual o Mestre em sessão não atua
- **THEN** ele não aparece na lista daquele Mestre

#### Scenario: A lista não expõe dado pessoal da criança

- **WHEN** o Mestre lê a lista
- **THEN** cada item traz nick e avatar, e nenhum traz imagem real, nome civil, nascimento ou
  contato

#### Scenario: Persona de outro papel não usa a leitura do Mestre

- **WHEN** uma persona que não é Mestre chama a leitura dos vinculáveis
- **THEN** o núcleo responde 403 e nada é devolvido

### Requirement: Admin e Mestre leem quem responde por um Guerreiro(a)

O núcleo SHALL responder, a um **Admin** ou a um **Mestre** em sessão, os **responsáveis com
vínculo vigente** com um Guerreiro(a), cada um com o **grau de parentesco**, para que o
atendimento assistido escolha **qual deles está presente**. A leitura SHALL ser a mesma operação
de vínculo que a matriz de permissões já concede aos dois papéis — nenhuma `Operacao` nova — e
persona de qualquer outro papel SHALL receber **403**.

A resposta SHALL trazer apenas o que identifica o responsável para a escolha — nome e grau de
parentesco —, e NEVER SHALL trazer credencial, senha nem contato. Vínculo já encerrado NEVER
SHALL aparecer. (`RF-13-35`, `RN-13-03`, decisão do fundador de 2026-09-01)

#### Scenario: O Mestre vê quem responde pelo Guerreiro(a)

- **WHEN** um Mestre consulta os responsáveis de um Guerreiro(a)
- **THEN** o núcleo devolve os responsáveis com vínculo vigente, cada um com o grau de
  parentesco

#### Scenario: Vínculo encerrado não aparece

- **WHEN** um dos responsáveis teve o vínculo encerrado
- **THEN** ele não aparece na resposta

#### Scenario: A resposta não traz credencial nem contato

- **WHEN** um Admin consulta os responsáveis de um Guerreiro(a)
- **THEN** a resposta traz nome e grau de parentesco, e nenhuma credencial, senha ou contato

#### Scenario: Outro papel não alcança a lista

- **WHEN** um responsável, um Apoiador ou um Guerreiro(a) chama a rota
- **THEN** o núcleo responde 403

### Requirement: Admin e Mestre leem os responsáveis cadastrados, com os vinculados de cada um

O núcleo SHALL responder, a um **Admin** ou a um **Mestre** em sessão, os responsáveis
cadastrados, cada um com o **nome** e com os Guerreiros e Guerreiras **vinculados a ele por
vínculo vigente**, identificados por **nick** e **nome** e acompanhados do **grau de
parentesco** daquele vínculo. A leitura SHALL ser paginada, na mesma convenção das demais
listagens do núcleo.

O alcance SHALL depender do papel em sessão:

- ao **Admin**, todos os responsáveis cadastrados;
- ao **Mestre**, os responsáveis com vínculo vigente a Guerreiro(a) das **comunidades em que
  ele atua**, **e** os responsáveis que **ele próprio cadastrou**, ainda que estes não tenham
  vínculo algum. Responsável fora desses dois conjuntos NEVER SHALL aparecer na lista dele.

Responsável **sem vínculo vigente** SHALL aparecer na lista de quem o alcança, com a lista de
vinculados vazia: é o cadastro interrompido, e é para retomá-lo que a leitura existe. Vínculo
**encerrado** NEVER SHALL aparecer entre os vinculados. Guerreiro(a) sem nome gravado SHALL
vir com o nome vazio, e o vinculado nunca some da lista por isso.

A resposta SHALL trazer apenas o que identifica o responsável, o **acesso** dele e os
vinculados — nome do responsável; o **e-mail** da credencial de login social ativa e o
**usuário** da credencial de usuário e senha ativa, cada um vazio quando não existe; e, de cada
vinculado, nick, nome e grau de parentesco. NEVER SHALL trazer senha, hash, troca pendente nem
credencial desativada, nem imagem real, nascimento ou contato do Guerreiro(a). (`RF-01-92`,
decisão do fundador de 2026-11-27) A leitura SHALL usar a **mesma operação de vínculo** que a matriz de
permissões já concede aos dois papéis, sem `Operacao` nova, e persona de qualquer outro papel
SHALL receber **403**. (`RF-02-111`, `RF-09-122`, `RF-01-13`, `RN-01-20`, `RN-09-18`,
invariante 12 do documento 99 §6, decisões do fundador de 2026-09-26 e de 2026-11-26)

#### Scenario: O Admin vê todos os responsáveis cadastrados

- **WHEN** um Admin em sessão pede os responsáveis
- **THEN** o núcleo devolve todos os cadastrados, cada um com o nome e com os vinculados
  vigentes por nick, nome e grau de parentesco

#### Scenario: O Mestre vê os responsáveis das comunidades em que atua

- **WHEN** um Mestre em sessão pede os responsáveis
- **THEN** o núcleo devolve os que têm vínculo vigente com Guerreiro(a) de comunidade em que
  ele atua, com os vinculados por nick, nome e grau de parentesco

#### Scenario: Responsável de outra comunidade não aparece ao Mestre

- **WHEN** existe responsável vinculado apenas a Guerreiro(a) de comunidade em que o Mestre em
  sessão não atua, e que não foi cadastrado por ele
- **THEN** ele não aparece na lista daquele Mestre

#### Scenario: O Mestre reencontra o responsável que ele mesmo cadastrou sem vincular

- **WHEN** um Mestre cadastrou um responsável e saiu antes de criar qualquer vínculo, e depois
  pede os responsáveis
- **THEN** aquele responsável aparece na lista dele, com a lista de vinculados vazia

#### Scenario: Responsável sem vínculo aparece ao Admin

- **WHEN** um Admin pede os responsáveis e existe um cadastrado sem vínculo algum
- **THEN** ele aparece na lista, com a lista de vinculados vazia

#### Scenario: Vínculo encerrado não entra entre os vinculados

- **WHEN** um responsável tem um vínculo já encerrado e outro vigente
- **THEN** a lista dele traz apenas o Guerreiro(a) do vínculo vigente

#### Scenario: Guerreiro(a) sem nome gravado continua na lista

- **WHEN** um vinculado não tem nome gravado
- **THEN** ele aparece com o nick, o grau de parentesco e o nome vazio

#### Scenario: A resposta não traz credencial nem contato

- **WHEN** um Admin ou um Mestre lê a lista e um responsável tem login social e credencial de
  usuário e senha ativos
- **THEN** ele vem com o e-mail e o usuário, e nenhum responsável traz senha, hash ou a marca
  de troca pendente

#### Scenario: Responsável sem acesso vem com os dois campos vazios

- **WHEN** um responsável não tem credencial ativa alguma
- **THEN** ele aparece na lista com o e-mail e o usuário vazios

#### Scenario: Credencial desativada não aparece

- **WHEN** o login social de um responsável foi desativado pela retirada do e-mail
- **THEN** a lista traz o e-mail dele vazio

#### Scenario: A lista não expõe dado pessoal da criança

- **WHEN** a lista traz os vinculados de um responsável
- **THEN** cada vinculado traz nick, nome e grau de parentesco, e nenhum traz imagem real,
  nascimento ou contato

#### Scenario: Outro papel não alcança a lista

- **WHEN** um responsável, um Apoiador ou um Guerreiro(a) chama a rota
- **THEN** o núcleo responde 403 e nada é devolvido

### Requirement: O Admin altera a ficha do responsável

O núcleo SHALL permitir, **só ao Admin**, alterar o **nome** e o **e-mail** de um responsável.
Campo ausente mantém; nome em branco é recusado com 422. Gravar e-mail onde não havia SHALL criar
a credencial de login social; trocá-lo SHALL trocar o identificador dela; retirá-lo SHALL
desativá-la. E-mail de credencial social ativa de outra persona SHALL ser recusado com 422.
Outro papel, Mestre incluído, SHALL receber 403. (`RF-01-92`, `RF-02-121`)

#### Scenario: Admin corrige o nome

- **WHEN** um Admin altera o nome de um responsável
- **THEN** o núcleo grava o nome novo, e vínculos e credenciais seguem como estavam

#### Scenario: Admin dá o acesso pelo Google a quem não tinha

- **WHEN** um Admin grava o e-mail de um responsável cadastrado sem e-mail
- **THEN** nasce a credencial de login social com esse e-mail, e o responsável passa a entrar
  pela conta Google dele

#### Scenario: Admin troca o e-mail

- **WHEN** um Admin troca o e-mail de um responsável por um endereço livre
- **THEN** o login social passa a reconhecer o endereço novo e deixa de reconhecer o antigo

#### Scenario: Admin retira o e-mail

- **WHEN** um Admin retira o e-mail de um responsável
- **THEN** a credencial de login social dele é desativada, e a credencial de usuário e senha,
  se houver, continua valendo

#### Scenario: E-mail de outra pessoa é recusado na edição

- **WHEN** o e-mail informado já identifica a credencial social ativa de outra persona
- **THEN** o núcleo responde 422 indicando o campo, e a ficha continua como estava

#### Scenario: O Mestre não altera a ficha

- **WHEN** um Mestre, ou qualquer papel que não seja Admin, tenta alterar a ficha de um
  responsável
- **THEN** o núcleo responde 403 e nada muda

#### Scenario: Persona que não é responsável não é alcançada

- **WHEN** um Admin chama a alteração com o identificador de persona de outro papel
- **THEN** o núcleo responde 404 e nada muda
