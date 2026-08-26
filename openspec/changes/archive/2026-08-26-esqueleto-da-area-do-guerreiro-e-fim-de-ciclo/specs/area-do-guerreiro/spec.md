## Purpose

A App 05 — a aplicação em que o Guerreiro(a) percorre a própria trilha, registra a coleta do
território e cuida do que conquistou. Nesta fatia, só a porta de entrada: a sessão no aparelho
compartilhado do ponto de apoio, que é a condição normal de uso e o pré-requisito de toda tela
do PRD-05.

## ADDED Requirements

### Requirement: O Guerreiro(a) entra na App 05 por nick e imagem

A aplicação SHALL abrir a sessão do Guerreiro(a) pedindo o **nick** e submetendo a **imagem**
à conferência biométrica do núcleo, em toda sessão. A prova de vivacidade e a extração do
descritor facial SHALL acontecer **no próprio aparelho**; ao núcleo SHALL ir apenas o
descritor, e a fotografia NEVER SHALL trafegar. (`RF-05-01`, `RN-05-01`, documento 03 §1.1)

#### Scenario: Entrada com nick e imagem conferidos

- **WHEN** um Guerreiro(a) com imagem gravada informa o nick e apresenta o rosto à câmera
- **THEN** a aplicação obtém o descritor no aparelho, o submete à conferência e abre a sessão

#### Scenario: A fotografia não sai do aparelho

- **WHEN** a aplicação submete a conferência ao núcleo
- **THEN** a chamada leva o descritor facial, e nenhuma imagem é enviada

#### Scenario: A recusa não diz o que falhou

- **WHEN** a conferência não encontra correspondência para o nick informado
- **THEN** a aplicação recusa a entrada sem revelar se o nick existe, e oferece o caminho da
  sessão assistida

### Requirement: O aparelho sem câmera recusa a entrada e explica o motivo

A aplicação SHALL recusar a entrada em aparelho sem câmera disponível e SHALL explicar a recusa
em **linguagem de criança de 6 anos**, sem termo técnico e sem código de erro exposto. A recusa
SHALL dizer o que a criança pode fazer — procurar um Mestre no ponto de apoio. (`RF-05-02`,
`RN-05-01`, PRD-05 §10)

#### Scenario: Aparelho sem câmera não entra

- **WHEN** a aplicação é aberta em aparelho sem câmera, ou com o acesso à câmera negado
- **THEN** a entrada é recusada, e a tela explica em linguagem simples o que aconteceu e o que
  fazer

#### Scenario: Nenhum código técnico chega à criança

- **WHEN** qualquer recusa de entrada é apresentada
- **THEN** a tela não exibe código de erro, nome de biblioteca nem termo técnico

### Requirement: Mestre ou Admin presente abre a sessão do Guerreiro(a)

A aplicação SHALL oferecer o caminho da **sessão assistida**, em que um Mestre ou um Admin
presente se autentica e abre a sessão do Guerreiro(a), nos dois casos previstos: quando a
conferência biométrica falha e quando o Guerreiro(a) **ainda não tem imagem gravada**. O adulto
que abre a sessão NEVER SHALL operar a aplicação em nome da criança. (`RF-05-03`, `RF-05-04`,
`RN-05-02`, PRD-05 §4)

#### Scenario: Conferência que falha abre pela sessão assistida

- **WHEN** a conferência biométrica de um Guerreiro(a) com imagem gravada não passa e um Mestre
  presente confirma a identidade dele
- **THEN** a sessão do Guerreiro(a) é aberta, e ele opera a aplicação normalmente

#### Scenario: Quem não tem imagem gravada entra pelo mesmo caminho

- **WHEN** um Guerreiro(a) que ainda não teve a imagem capturada no onboarding pede para entrar
  e um Admin presente confirma a identidade dele
- **THEN** a sessão é aberta, sem que nenhuma imagem seja capturada nesta aplicação

#### Scenario: Sem adulto presente não há sessão assistida

- **WHEN** a conferência falha e nenhum Mestre ou Admin se autentica
- **THEN** nenhuma sessão é aberta

### Requirement: A sessão encerra ao sair e por inatividade, com aviso antes

A aplicação SHALL encerrar a sessão quando o Guerreiro(a) sair e quando a sessão expirar por
inatividade, voltando em ambos os casos ao pedido de nick. **Um minuto antes** do encerramento
por inatividade a aplicação SHALL avisar, oferecendo a opção de continuar; escolhida a opção, a
contagem recomeça. A duração é a **declarada na implantação**, sem valor padrão no código.
(`RF-05-05`, `RF-05-71`, `RF-01-04`)

#### Scenario: Sair volta ao pedido de nick

- **WHEN** o Guerreiro(a) encerra a própria sessão
- **THEN** a aplicação volta ao pedido de nick, sem nenhum dado dele na tela

#### Scenario: O aviso precede o encerramento por inatividade

- **WHEN** falta um minuto para a sessão expirar por inatividade
- **THEN** a aplicação avisa e oferece a opção de continuar

#### Scenario: Continuar recomeça a contagem

- **WHEN** o Guerreiro(a) escolhe continuar diante do aviso
- **THEN** a sessão segue aberta e a contagem de inatividade recomeça

#### Scenario: Sem resposta ao aviso a sessão encerra

- **WHEN** o aviso é apresentado e o minuto passa sem resposta
- **THEN** a sessão encerra e a aplicação volta ao pedido de nick

### Requirement: O aparelho compartilhado não guarda nada de quem passou por ele

A aplicação NEVER SHALL armazenar imagem de Guerreiro(a) no aparelho compartilhado — nem a
fotografia da conferência, nem o descritor dela. Encerrada uma sessão, a tela seguinte NEVER
SHALL exibir dado do Guerreiro(a) anterior, e a troca de sessão entre duas crianças SHALL
acontecer **sem reiniciar a aplicação**. (`RF-05-06`, `RF-05-07`, PRD-05 §§10, 12)

#### Scenario: Nenhuma imagem fica no aparelho

- **WHEN** a conferência biométrica termina, tendo passado ou não
- **THEN** nenhuma imagem e nenhum descritor do Guerreiro(a) permanece armazenado no aparelho

#### Scenario: A tela seguinte não mostra a criança anterior

- **WHEN** uma sessão encerra e outro Guerreiro(a) informa o nick
- **THEN** nenhum dado do Guerreiro(a) anterior aparece em nenhuma tela

#### Scenario: Trocar de sessão não reinicia a aplicação

- **WHEN** dois Guerreiros e Guerreiras usam o mesmo aparelho, um após o outro
- **THEN** a troca acontece dentro da aplicação em execução, sem recarga nem reinício

### Requirement: A App 05 é inteiramente autenticada

A aplicação NEVER SHALL apresentar tela de conteúdo a visitante: toda tela além do pedido de
nick SHALL exigir sessão de Guerreiro(a) aberta. Uma sessão NEVER SHALL alcançar os dados de
outro Guerreiro(a). (`RF-05-01`, PRD-05 §4)

#### Scenario: Visitante não alcança tela nenhuma

- **WHEN** a aplicação é aberta sem sessão
- **THEN** a única tela apresentada é o pedido de nick

#### Scenario: A sessão alcança apenas os próprios dados

- **WHEN** a aplicação, com sessão aberta, consulta dados no núcleo
- **THEN** a resposta traz apenas dados do Guerreiro(a) daquela sessão
