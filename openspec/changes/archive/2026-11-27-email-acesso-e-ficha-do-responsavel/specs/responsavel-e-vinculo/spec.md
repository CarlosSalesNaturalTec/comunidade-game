## MODIFIED Requirements

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

## ADDED Requirements

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
