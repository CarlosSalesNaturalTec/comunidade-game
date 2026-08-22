## Purpose

O que as oito aplicações compartilham para falar com o núcleo sem que cada uma o reimplemente:
os dois cabeçalhos de toda chamada, o corpo de erro único do PRD-01, a distinção entre recusa
de chave e recusa de sessão, e a guarda da sessão do adulto. É a irmã de `camada-visual-comum`
— aquela cobre o que se vê, esta cobre o que se fala com o núcleo.

## ADDED Requirements

### Requirement: A camada leva os dois cabeçalhos em toda chamada ao núcleo

A camada de acesso SHALL enviar, em toda chamada a rota de dados do núcleo, a **chave de
aplicação** de quem a consome e, quando houver sessão aberta, a **credencial da persona**. Os
dois cabeçalhos são credenciais independentes, e a camada NEVER SHALL derivar um do outro.
(`RF-01-02`, `RN-01-32`, `RN-01-34`)

#### Scenario: Chamada sem sessão leva só a chave

- **WHEN** uma aplicação chama uma rota de dados antes de qualquer sessão aberta
- **THEN** a chamada leva a chave de aplicação e nenhum cabeçalho de sessão

#### Scenario: Chamada com sessão leva os dois

- **WHEN** uma aplicação com sessão aberta chama uma rota de dados
- **THEN** a chamada leva a chave de aplicação e a credencial da persona

### Requirement: Cada aplicação declara a própria chave e o próprio endereço do núcleo

A camada de acesso SHALL ler a chave de aplicação e o endereço do núcleo da configuração da
aplicação que a consome, e NEVER SHALL trazer valor embutido. A chave é por aplicação **e por
ambiente**, e a mesma camada servida a duas aplicações SHALL apresentar chaves diferentes.
(`RF-01-54`, `RN-01-33`, documento 03 §1)

#### Scenario: Duas aplicações apresentam chaves diferentes

- **WHEN** a App 03 e a App 09 chamam a mesma rota do núcleo
- **THEN** cada chamada leva a chave da sua própria aplicação, e não a da outra

#### Scenario: Configuração ausente não é suprida por padrão embutido

- **WHEN** a aplicação é construída sem a chave configurada
- **THEN** a camada não substitui o valor em falta por um embutido

### Requirement: A camada distingue a recusa da chave da recusa da sessão

A camada de acesso SHALL reconhecer separadamente a recusa da **chave** e a recusa da
**sessão**, porque a primeira é falha de implantação e a segunda devolve o adulto à entrada. A
camada NEVER SHALL tratar uma como a outra. (`RN-01-34`)

#### Scenario: Recusa de chave é reconhecida como falha de implantação

- **WHEN** o núcleo recusa a chave de aplicação
- **THEN** a camada a distingue como recusa de chave, e a aplicação não devolve o adulto à
  entrada

#### Scenario: Recusa de sessão devolve à entrada

- **WHEN** o núcleo recusa a credencial da persona por ausente ou inválida
- **THEN** a camada a distingue como recusa de sessão, e a aplicação devolve o adulto à entrada

### Requirement: A camada apresenta o erro do núcleo no corpo único do PRD-01

A camada de acesso SHALL entregar a quem a consome o erro do núcleo com o **código**, a
**mensagem** e o **campo** quando houver, preservando o corpo único da API, para que a tela
possa apontar o campo em falta sem interpretar texto. (`RF-01-02`, convenções da API)

#### Scenario: Erro de validação chega com o campo

- **WHEN** o núcleo recusa uma escrita por campo obrigatório em falta
- **THEN** a camada entrega o código, a mensagem e o nome do campo, e a tela o aponta

#### Scenario: O corpo do erro não é reinterpretado

- **WHEN** o núcleo devolve um erro de código desconhecido pela aplicação
- **THEN** a camada o entrega como veio, sem substituir a mensagem por texto próprio

### Requirement: A sessão do adulto é guardada por aplicação e não vaza entre elas

A camada de acesso SHALL guardar a sessão do adulto no armazenamento de sessão do navegador,
restrito à aplicação que a abriu, e SHALL restaurá-la ao reabrir a aplicação enquanto ela
durar. A sessão aberta numa aplicação NEVER SHALL abrir sessão em outra. (`RF-01-09`,
`RN-01-34`)

#### Scenario: A sessão sobrevive à recarga da página

- **WHEN** o adulto com sessão aberta recarrega a aplicação
- **THEN** a camada restaura a sessão e ele não passa de novo pela entrada

#### Scenario: A sessão de uma aplicação não abre a outra

- **WHEN** o adulto abre sessão na App 03 e em seguida abre a App 09
- **THEN** a App 09 apresenta a entrada, porque a sessão da App 03 não a alcança

#### Scenario: O encerramento apaga a sessão guardada

- **WHEN** o adulto encerra a própria sessão
- **THEN** a camada apaga o que guardou, e a reabertura da aplicação apresenta a entrada
