## ADDED Requirements

### Requirement: O Admin altera os dados e os artefatos de Mestre e Apoiador

O núcleo SHALL expor rota de **Admin** que altera **nome**, **e-mail** e **WhatsApp** de um
Mestre ou de um Apoiador, sob as mesmas validações do cadastro. Trocar o e-mail SHALL trocar o
identificador da credencial de login social do adulto; e-mail já usado por outra credencial
ativa SHALL ser recusado com **422**. O núcleo SHALL expor rotas de Admin que **incluem**,
**corrigem** e **removem** artefato comprobatório do adulto; a remoção que o deixaria sem artefato
algum SHALL ser recusada com **422**. A rota NEVER SHALL alterar nick, papel nem termos de doação,
e NEVER SHALL ser alcançada por quem não é Admin. (`RF-02-117`, `RF-02-02`, `RF-02-03`,
`RF-02-04`, `RN-02-01`, documento 02 §1)

#### Scenario: Admin corrige o e-mail do Apoiador

- **WHEN** um Admin altera o e-mail de um Apoiador para um endereço livre
- **THEN** o núcleo grava o e-mail novo, e o login social passa a reconhecer o endereço novo e
  não mais o antigo

#### Scenario: E-mail de outra pessoa é recusado

- **WHEN** o e-mail informado já identifica a credencial ativa de outra persona
- **THEN** o núcleo responde 422 e nada é alterado

#### Scenario: O último artefato não sai

- **WHEN** o Admin tenta remover o único artefato comprobatório de um Mestre
- **THEN** o núcleo responde 422 e o artefato permanece

#### Scenario: Nick não muda por aqui

- **WHEN** a alteração chega com um campo de nick
- **THEN** o núcleo responde 422 e o nick vigente permanece

#### Scenario: Quem não é Admin não altera

- **WHEN** um Mestre ou um Apoiador chama a rota de alteração de outro adulto
- **THEN** o núcleo responde 403

### Requirement: O Admin exclui só o adulto nunca usado

O núcleo SHALL expor rota de **Admin** que exclui um Mestre ou um Apoiador **apenas se nunca
usado** — nenhuma linha de nenhuma tabela aponta para a persona além do nick, das credenciais,
das sessões e dos artefatos comprobatórios dela, que saem junto. A conferência SHALL ser feita
pelas chaves estrangeiras do esquema, de modo que tabela nova entre nela sem alteração da rota.
Adulto usado SHALL ser recusado com **422**, com mensagem que aponta a desativação. (`RF-02-118`,
`RN-02-34`)

#### Scenario: Cadastro feito por engano sai

- **WHEN** o Admin exclui um Apoiador que nunca entrou, nunca aportou e nada referencia
- **THEN** a persona, o nick, a credencial e os artefatos dela deixam de existir

#### Scenario: Apoiador com aporte não sai

- **WHEN** o Admin tenta excluir um Apoiador com aporte homologado
- **THEN** o núcleo responde 422, indica a desativação, e o aporte e a persona permanecem

#### Scenario: Mestre com trilha não sai

- **WHEN** o Admin tenta excluir um Mestre autor de uma trilha
- **THEN** o núcleo responde 422 e a persona permanece

### Requirement: O Admin desativa e reativa o adulto

O núcleo SHALL expor rotas de **Admin** que **desativam** e **reativam** um Mestre ou um
Apoiador. A desativação SHALL revogar as credenciais e encerrar as sessões abertas do adulto e
SHALL tirá-lo das superfícies públicas, sem apagar nem alterar nada do que ele produziu —
aporte, trilha, lançamento, selo. A reativação SHALL devolver a credencial de login social e a
presença pública. A listagem da gestão SHALL continuar trazendo o desativado, com a marca
`ativo` falsa. (`RF-02-119`, `RN-02-35`, PRD-14 §11)

#### Scenario: Desativado perde o acesso

- **WHEN** o Admin desativa um Apoiador com sessão aberta
- **THEN** a sessão deixa de valer e o próximo login dele é recusado

#### Scenario: O que ele fez permanece

- **WHEN** o Admin desativa um Apoiador com aporte homologado
- **THEN** o aporte, o lançamento no livro-razão e o comprovante seguem inalterados

#### Scenario: Reativado volta a entrar

- **WHEN** o Admin reativa o Apoiador desativado
- **THEN** o login social dele volta a abrir sessão e ele volta às superfícies públicas
