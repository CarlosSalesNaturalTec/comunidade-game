# Spec Delta

## MODIFIED Requirements

### Requirement: Os caminhos da Área do Guerreiro(a) aparecem em cartão, na ordem decidida

A Área do Guerreiro(a) SHALL apresentar os caminhos como **cartões em coluna**, um por linha,
com o glifo ao lado do rótulo em frase, nesta ordem: **Trilha**, **minha carteira**, **desafios
e equipes**, **coleta do território** e **sair**. A ordem é decisão do fundador e NEVER SHALL
depender de quando cada bloco foi acrescentado. (`RF-05-08`, PRD-05 §§5.2, 10, documento 15
§6.5, decisão do fundador de 2026-10-31)

#### Scenario: Os caminhos aparecem na ordem decidida

- **WHEN** o Guerreiro(a) em sessão vê os caminhos da área
- **THEN** eles aparecem em cartão, um por linha, na ordem Trilha, minha carteira, desafios e
  equipes, coleta do território e sair

#### Scenario: Cada caminho leva o glifo junto do rótulo

- **WHEN** um caminho da área é apresentado
- **THEN** ele traz o glifo ao lado do rótulo em frase, e o rótulo segue sendo o nome acessível
  do cartão

## ADDED Requirements

### Requirement: A App 05 abre no menu dos caminhos

A aplicação SHALL **abrir no menu dos caminhos** e NEVER SHALL apresentar o conteúdo de um bloco
antes de o Guerreiro(a) acionar o caminho dele. O **cartão da Trilha** SHALL dizer o que fazer
agora, nomeando a próxima missão, para que a primeira tela responda à pergunta sem depender de
toque. (`RF-05-08`, PRD-05 §§5.2, 10, 12, decisão do fundador de 2026-10-31)

#### Scenario: A sessão aberta cai no menu, sem conteúdo de bloco

- **WHEN** o Guerreiro(a) inscrito abre a sessão na Área do Guerreiro(a)
- **THEN** vê o menu dos caminhos, e nenhum conteúdo de bloco aparece na tela

#### Scenario: O menu já diz o que fazer agora

- **WHEN** o Guerreiro(a) inscrito com próxima missão vê o menu
- **THEN** o cartão da Trilha nomeia a próxima missão, sem que ele acione caminho algum

### Requirement: Acionada, a Trilha abre na próxima missão do Guerreiro(a)

Acionado o caminho da Trilha, o bloco SHALL abrir na **próxima missão** do Guerreiro(a) em
sessão, dizendo **o que fazer** e **o que ela desbloqueia**. O Guerreiro(a) inscrito em **mais
de uma trilha** SHALL alternar entre elas **preservando o contexto** de cada uma. Sem nenhuma
inscrição, o bloco SHALL levar à escolha do poder, nunca a uma tela vazia sem saída.
(`RF-05-08`, `RF-05-17`, PRD-05 §§5.2, 12)

#### Scenario: A tela da trilha mostra o que fazer agora

- **WHEN** o Guerreiro(a) inscrito aciona o caminho da Trilha
- **THEN** vê a próxima missão, o que precisa ser feito nela e o que ela desbloqueia

#### Scenario: Alternar de trilha não perde o contexto

- **WHEN** o Guerreiro(a) inscrito em duas trilhas alterna para a outra e volta
- **THEN** cada trilha reabre no ponto em que ele a deixou

#### Scenario: Sem inscrição, a tela oferece o caminho

- **WHEN** um Guerreiro(a) sem nenhuma inscrição aciona o caminho da Trilha
- **THEN** a tela o leva à escolha do poder, em vez de mostrar tela vazia

### Requirement: Cada caminho da área abre em tela própria, sem o menu

Acionado um caminho, a aplicação SHALL apresentar o conteúdo dele em **tela própria**, e essa
tela NEVER SHALL repetir os caminhos da área. A tela de conteúdo SHALL oferecer **um caminho de
volta ao menu**, que SHALL levar ao menu **de qualquer profundidade** alcançada dentro do bloco,
e não ao passo anterior da navegação interna dele. (`RF-05-08`, PRD-05 §§5.2, 10, decisão do
fundador de 2026-10-31)

#### Scenario: O conteúdo do bloco ocupa a tela sozinho

- **WHEN** o Guerreiro(a) aciona um dos caminhos da área
- **THEN** o conteúdo daquele bloco ocupa a tela, e os caminhos da área não aparecem nela

#### Scenario: Voltar salta ao menu de qualquer profundidade

- **WHEN** o Guerreiro(a) desce na navegação interna de um bloco e aciona o caminho de volta
- **THEN** encontra o menu dos caminhos, e não o passo anterior dentro do bloco

#### Scenario: Trocar de bloco passa pelo menu

- **WHEN** o Guerreiro(a) está num bloco e quer outro
- **THEN** volta ao menu e aciona o cartão do outro bloco

### Requirement: A saída da sessão é um caminho do menu, e só existe nele

A saída da sessão SHALL ser apresentada como **cartão de caminho**, igual aos demais e na
**última posição** do menu. Ela SHALL existir **somente no menu**: nenhuma tela de conteúdo
SHALL oferecer saída da sessão, para que o único comando de navegação ali seja o de voltar.
(`RF-05-05`, `RF-05-08`, decisão do fundador de 2026-10-31)

#### Scenario: Sair é o último cartão do menu

- **WHEN** o Guerreiro(a) em sessão vê o menu dos caminhos
- **THEN** a saída da sessão é o último cartão, apresentada como os demais caminhos

#### Scenario: A tela de conteúdo não oferece saída

- **WHEN** o Guerreiro(a) está numa tela de conteúdo de qualquer bloco
- **THEN** não encontra ali caminho de sair da sessão, apenas o de voltar ao menu

### Requirement: O aviso de inatividade alcança o menu e as telas de conteúdo

O aviso que antecede o encerramento por inatividade e o caminho de continuar a sessão SHALL
aparecer **em qualquer tela da área** — no menu e nas telas de conteúdo. A sessão NEVER SHALL
encerrar por inatividade sem que o aviso tenha sido apresentado na tela em que o Guerreiro(a)
está. (`RF-05-05`, `RF-05-71`, PRD-05 §10)

#### Scenario: O aviso aparece dentro de um bloco

- **WHEN** a inatividade atinge o limite com o Guerreiro(a) numa tela de conteúdo
- **THEN** ele vê ali o aviso e o caminho de continuar a sessão, sem voltar ao menu

#### Scenario: Continuar a sessão não tira o Guerreiro(a) da tela

- **WHEN** o Guerreiro(a) aciona continuar a partir de uma tela de conteúdo
- **THEN** a sessão segue aberta e ele permanece na mesma tela

## REMOVED Requirements

### Requirement: A App 05 abre na próxima missão do Guerreiro(a)

**Reason**: Decisão do fundador de 2026-10-31, que reverte em parte a fatia 11 do mesmo dia. O
requisito mandava a aplicação abrir no bloco da trilha e proibia abrir em qualquer outro
(`NEVER SHALL abrir em outro bloco`); a área passa a abrir no **menu dos caminhos**, sem
conteúdo de bloco algum à vista.

**Migration**: A intenção do `RF-05-08` — a primeira tela dizer o que fazer agora — passa aos
requisitos "A App 05 abre no menu dos caminhos", pelo cartão da Trilha que nomeia a próxima
missão, e "Acionada, a Trilha abre na próxima missão do Guerreiro(a)", que preserva o que fazer,
o que a missão desbloqueia, a alternância entre trilhas do `RF-05-17` e a saída para a escolha
do poder de quem não tem inscrição.

### Requirement: O caminho corrente da área é anunciado como o atual

**Reason**: Com o menu e o conteúdo em telas separadas, não há caminho corrente a anunciar: a
tela que mostra os caminhos não tem bloco aberto, e a que tem bloco aberto não mostra caminhos.
O requisito previa também que os caminhos permanecessem alcançáveis com o bloco aberto — o
oposto do que a decisão do fundador de 2026-10-31 determina.

**Migration**: A navegação entre blocos passa pelo menu, conforme "Cada caminho da área abre em
tela própria, sem o menu". A regra de marcar item corrente por sinal além da cor (documento 15
§5) permanece vigente nas áreas que têm navegação persistente, pelo componente de navegação de
áreas das Apps 03 e 09.
