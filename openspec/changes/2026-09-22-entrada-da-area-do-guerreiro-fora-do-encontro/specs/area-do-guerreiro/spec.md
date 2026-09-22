## RENAMED Requirements

- FROM: `### Requirement: Mestre ou Admin presente abre a sessão do Guerreiro(a)`
- TO: `### Requirement: O responsável, ou Mestre ou Admin presente, abre a sessão do Guerreiro(a)`

## MODIFIED Requirements

### Requirement: O Guerreiro(a) entra na App 05 por nick e imagem

A aplicação SHALL abrir a sessão do Guerreiro(a) pedindo o **nick** e submetendo a **imagem**
à conferência biométrica do núcleo, em toda sessão. A prova de vivacidade e a extração do
descritor facial SHALL acontecer **no próprio aparelho**; ao núcleo SHALL ir apenas o
descritor, e a fotografia NEVER SHALL trafegar. (`RF-05-01`, `RN-05-01`, documento 03 §1.1)

A App 05 é usada **fora do encontro**, em aparelho que não é de ponto de apoio algum, e por isso
a conferência SHALL ser submetida **sem aula**. O limiar aplicado é o da comunidade do
Guerreiro(a), pelo critério que a capacidade `template-biometrico` define; a aplicação NEVER
SHALL pedir, escolher ou inventar uma aula para enviar. (`RN-01-57`, documento 03 §3.3)

A recusa da conferência NEVER SHALL trancar a criança fora da aplicação: ela SHALL levar sempre
ao caminho da sessão assistida, que em casa é o do responsável. (`RN-05-02`)

#### Scenario: Entrada com nick e imagem conferidos

- **WHEN** um Guerreiro(a) com imagem gravada informa o nick e apresenta o rosto à câmera
- **THEN** a aplicação obtém o descritor no aparelho, o submete à conferência e abre a sessão

#### Scenario: A conferência é submetida sem aula

- **WHEN** a aplicação submete a conferência ao núcleo
- **THEN** o pedido leva o nick e o descritor, e nenhuma aula, porque ali não há encontro

#### Scenario: A fotografia não sai do aparelho

- **WHEN** a aplicação submete a conferência ao núcleo
- **THEN** a chamada leva o descritor facial, e nenhuma imagem é enviada

#### Scenario: A recusa não diz o que falhou

- **WHEN** a conferência não encontra correspondência para o nick informado
- **THEN** a aplicação recusa a entrada sem revelar se o nick existe, e oferece o caminho da
  sessão assistida

### Requirement: O responsável, ou Mestre ou Admin presente, abre a sessão do Guerreiro(a)

A aplicação SHALL oferecer o caminho da **sessão assistida**, em que um adulto identificado
abre a sessão do Guerreiro(a), nos dois casos previstos: quando a conferência biométrica falha
e quando o Guerreiro(a) **ainda não tem imagem gravada**. O adulto que abre a sessão NEVER SHALL
operar a aplicação em nome da criança. (`RF-05-03`, `RF-05-04`, `RN-05-02`, PRD-05 §4)

Qual adulto depende de onde a criança está. Em casa é o **responsável**, e a aplicação SHALL
aceitar dele **os dois caminhos de login** que o documento 03 §1.1 lhe dá — social e usuário e
senha. Oferecer só um deles trancaria fora quem tem o outro, que é o mesmo defeito que esta
fatia corrige. No encontro, o Mestre ou o Admin presente segue abrindo a sessão como hoje.
(`RF-05-03`, `RF-05-04`, `RN-05-02`, `RF-01-74`)

O responsável abre a sessão **apenas** dos Guerreiros e Guerreiras sob a responsabilidade dele;
o núcleo é quem confere isso, e a tela SHALL apresentar a recusa por criança alheia com a
**mesma frase** da recusa por nick inexistente — distinguir as duas na tela desfaria a
indistinguibilidade que o núcleo garante. (`RN-01-58`, `RN-01-22`)

Quando a credencial do responsável ainda for **provisória**, a aplicação SHALL conduzir a
**troca de senha** no mesmo fluxo, sem devolvê-lo à tela anterior e sem exigir que ele procure
outra aplicação. O primeiro uso dessa credencial costuma ser justamente o resgate da criança
depois de uma recusa; terminar ali seria deixar os dois sem porta. (`RF-01-12`, `RF-14-09`)

#### Scenario: Conferência que falha abre pela sessão assistida

- **WHEN** a conferência biométrica de um Guerreiro(a) com imagem gravada não passa e um Mestre
  presente confirma a identidade dele
- **THEN** a sessão do Guerreiro(a) é aberta, e ele opera a aplicação normalmente

#### Scenario: Em casa, quem confirma é o responsável

- **WHEN** a conferência falha em casa e o responsável se autentica e confirma a identidade da
  criança sob a responsabilidade dele
- **THEN** a sessão do Guerreiro(a) é aberta, e o responsável não segue operando a aplicação

#### Scenario: O responsável entra pelos dois caminhos de login

- **WHEN** a tela da sessão assistida é apresentada ao responsável
- **THEN** ela oferece o login social e o de usuário e senha, e qualquer um dos dois o autentica

#### Scenario: Senha provisória se troca ali mesmo

- **WHEN** o responsável entra com uma credencial cuja senha ainda é provisória
- **THEN** a aplicação conduz a troca da senha no mesmo fluxo e, concluída, abre a sessão da
  criança sem recomeçar

#### Scenario: Criança alheia recusa com a frase de sempre

- **WHEN** o responsável tenta confirmar o nick de um Guerreiro(a) que não está sob a
  responsabilidade dele
- **THEN** a tela apresenta a mesma frase da recusa por nick inexistente, e nenhuma sessão é
  aberta

#### Scenario: Quem não tem imagem gravada entra pelo mesmo caminho

- **WHEN** um Guerreiro(a) que ainda não teve a imagem capturada no onboarding pede para entrar
  e um Admin presente confirma a identidade dele
- **THEN** a sessão é aberta, sem que nenhuma imagem seja capturada nesta aplicação

#### Scenario: Sem adulto presente não há sessão assistida

- **WHEN** a conferência falha e nenhum adulto se autentica
- **THEN** nenhuma sessão é aberta

## ADDED Requirements

### Requirement: A recusa da entrada não absorve falha de camada

A aplicação SHALL reservar a frase da recusa do reconhecimento **apenas** à recusa que o núcleo
declarou como tal. Erro que o núcleo declara no corpo único — validação, chave, freio por
origem — e falha que não chega a ele, como a de rede, NEVER SHALL ser apresentado como rosto que
não confere: a tela SHALL apresentar a causa pelo que ela é, em linguagem de criança, sem código
de erro nem termo técnico. (`RN-05-48`, `RF-01-27`, `RF-05-02`)

O tratamento da recusa SHALL alcançar **apenas a conferência**. O que roda depois dela SHALL ter
tratamento próprio, porque falha ali acontece com o rosto **já reconhecido**. (`RN-05-48`)

#### Scenario: Erro de validação não vira rosto que não confere

- **WHEN** o núcleo recusa o pedido da sessão por erro de validação
- **THEN** a tela apresenta o que aconteceu, e não a frase da recusa do reconhecimento

#### Scenario: Rede fora não vira rosto que não confere

- **WHEN** a chamada da conferência não chega a obter resposta do núcleo
- **THEN** a tela diz que não conseguiu falar com a plataforma, e não que a criança não foi
  reconhecida

#### Scenario: Nenhum código técnico chega à criança na falha de camada

- **WHEN** qualquer falha de camada é apresentada na entrada
- **THEN** a tela não exibe código de erro, nome de biblioteca nem termo técnico
