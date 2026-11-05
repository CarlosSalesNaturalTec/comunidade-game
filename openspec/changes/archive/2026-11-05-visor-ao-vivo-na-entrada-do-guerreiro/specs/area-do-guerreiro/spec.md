# Spec Delta

## ADDED Requirements

### Requirement: A entrada apresenta o visor ao vivo da câmera

A entrada SHALL apresentar o **visor ao vivo** da câmera enquanto a conferência acontece — o
fluxo que mostra a pessoa a si mesma, que nada guarda e nada reexibe. O visor SHALL aparecer
**somente depois** de o Guerreiro(a) pedir a entrada, nunca ao abrir a tela. A **imagem
capturada** NEVER SHALL ser exibida, antes ou depois de gerar o descritor. (`RF-05-95`,
`RN-05-53`, `RN-05-49`, documento 03 §3.3, documento 99 §6 invariante 12)

#### Scenario: O visor mostra a criança a si mesma

- **WHEN** o Guerreiro(a) pede a entrada e a câmera é preparada
- **THEN** o visor ao vivo aparece na tela antes de a conferência julgar, e segue visível
  enquanto o laço corre

#### Scenario: A tela abre sem câmera acesa

- **WHEN** a tela de entrada é aberta e ninguém pediu a entrada ainda
- **THEN** nenhum visor aparece e a câmera permanece desligada

#### Scenario: O quadro capturado não volta à tela

- **WHEN** o descritor é gerado a partir do quadro aprovado
- **THEN** nenhum quadro congelado é devolvido à tela, e o visor desaparece com a câmera

### Requirement: O laço do reconhecimento é dito em linguagem de criança

A entrada SHALL dizer, enquanto o laço corre, o que ele está vendo: que ainda não encontrou
rosto, que encontrou e está confirmando, e que confirmou. O retorno SHALL ser **abstrato** —
nunca a fotografia — e SHALL estar em **linguagem de criança de 6 anos**, sem termo técnico e
sem código de erro. (`RF-05-95`, `RF-05-02`, PRD-05 §10)

#### Scenario: A criança sabe que ainda não foi encontrada

- **WHEN** o laço corre sem encontrar rosto no visor
- **THEN** a tela diz que ainda não a achou e o que fazer, e não fica apenas anunciando que
  está reconhecendo

#### Scenario: A criança sabe que foi encontrada

- **WHEN** o laço encontra o rosto e passa a confirmar que há uma pessoa
- **THEN** a tela diz que a achou e pede que ela continue assim

#### Scenario: Nenhum termo técnico aparece no retorno do laço

- **WHEN** qualquer das situações do laço é apresentada
- **THEN** a frase não traz termo técnico, nome de biblioteca nem código de erro

### Requirement: A entrada orienta sobre luz e enquadramento

A entrada SHALL trazer **frase fixa** que orienta sobre luz e enquadramento, apresentada junto
do visor, de modo que a criança corrija a posição e a iluminação por conta própria. A aplicação
NEVER SHALL medir a luz nem julgar a distância do rosto para produzir essa orientação: a frase é
fixa, e quem julga o enquadramento é quem se vê no visor. (`RF-05-96`, documento 03 §3.3)

#### Scenario: A orientação aparece com o visor

- **WHEN** o visor ao vivo aparece na entrada
- **THEN** a frase de orientação sobre luz e enquadramento está visível junto dele

#### Scenario: Nenhum limiar de luz é aplicado

- **WHEN** a entrada apresenta a orientação
- **THEN** ela é a mesma frase em qualquer condição de luz, e nenhuma medição de luminância ou
  de tamanho do rosto decide o que é dito

### Requirement: A entrada avisa o que faz com a imagem

A entrada SHALL trazer o **aviso discreto** de que a câmera aparece só para a pessoa se ver, de
que a foto não fica guardada e de que ela não sai do aparelho. O aviso SHALL estar em linguagem
de criança. (`RF-05-57`, `RF-05-02`, PRD-05 §11)

#### Scenario: O aviso acompanha a tela que abre a câmera

- **WHEN** a entrada que abre a câmera é apresentada
- **THEN** o aviso do que acontece com a imagem está na tela, em linguagem de criança

## MODIFIED Requirements

### Requirement: A recusa da entrada não absorve falha de camada

A aplicação SHALL reservar a frase da recusa do reconhecimento **apenas** à recusa que o núcleo
declarou como tal. Erro que o núcleo declara no corpo único — validação, chave, freio por
origem — e falha que não chega a ele, como a de rede, NEVER SHALL ser apresentado como rosto que
não confere: a tela SHALL apresentar a causa pelo que ela é, em linguagem de criança, sem código
de erro nem termo técnico. (`RN-05-48`, `RF-01-27`, `RF-05-02`)

O tratamento da recusa SHALL alcançar **apenas a conferência**. O que roda depois dela SHALL ter
tratamento próprio, porque falha ali acontece com o rosto **já reconhecido**. Alcança também a
falha que a camada de sessão **guarda em vez de propagar**: desfecho sem frase na tela é a mesma
falha silenciosa por outro caminho, e NEVER SHALL acontecer. (`RN-05-48`)

A falha do **preparo do aparelho** — câmera que não abre e modelo que não carrega — SHALL ter
desfecho próprio, distinto da recusa da conferência, porque ali ninguém chegou a apresentar
rosto algum e a frase do rosto culparia a criança por algo que não é dela. O desfecho SHALL
dizer que a câmera não pôde ser preparada e SHALL continuar oferecendo o caminho do adulto do
`RN-05-02`. (`RN-05-48`, `RF-05-02`)

#### Scenario: Erro de validação não vira rosto que não confere

- **WHEN** o núcleo recusa o pedido da sessão por erro de validação
- **THEN** a tela apresenta o que aconteceu, e não a frase da recusa do reconhecimento

#### Scenario: Rede fora não vira rosto que não confere

- **WHEN** a chamada da conferência não chega a obter resposta do núcleo
- **THEN** a tela diz que não conseguiu falar com a plataforma, e não que a criança não foi
  reconhecida

#### Scenario: Falha depois do reconhecimento não vira recusa

- **WHEN** o núcleo confere o rosto e, em seguida, a abertura da sessão no aparelho não se
  completa
- **THEN** a tela diz que o reconhecimento deu certo mas a entrada não terminou, e NEVER que a
  criança não foi reconhecida

#### Scenario: Nenhuma tentativa termina sem frase

- **WHEN** a entrada falha por um caminho que a camada de sessão guarda em vez de propagar
- **THEN** a tela ainda assim apresenta um desfecho, e não fica muda

#### Scenario: Nenhum código técnico chega à criança na falha de camada

- **WHEN** qualquer falha de camada é apresentada na entrada
- **THEN** a tela não exibe código de erro, nome de biblioteca nem termo técnico

#### Scenario: Câmera que não abre não vira rosto que não confere

- **WHEN** o preparo da câmera ou dos modelos não se conclui, antes de qualquer rosto ser
  apresentado
- **THEN** a tela diz que a câmera não pôde ser preparada, oferece o caminho do adulto e NEVER
  apresenta a frase do rosto que não confere
