# Spec Delta

## MODIFIED Requirements

### Requirement: A App 05 abre na próxima missão do Guerreiro(a)

A aplicação SHALL **abrir no bloco da trilha**, e esse bloco SHALL abrir na **próxima missão**
do Guerreiro(a) em sessão, dizendo **o que fazer** e **o que ela desbloqueia**, sem que a
criança precise procurar em menu. NEVER SHALL abrir em outro bloco. O Guerreiro(a) inscrito em
**mais de uma trilha** SHALL alternar entre elas **preservando o contexto** de cada uma — a
missão aberta numa trilha continua aberta ao voltar a ela. Sem nenhuma inscrição, a tela SHALL
levar à escolha do poder, nunca a uma tela vazia sem saída. (`RF-05-08`, `RF-05-17`, PRD-05
§§5.2, 10, 12)

#### Scenario: A sessão aberta já cai na próxima missão

- **WHEN** o Guerreiro(a) inscrito abre a sessão na Área do Guerreiro(a)
- **THEN** o bloco da trilha é o que aparece, sem que ele acione caminho algum
- **AND** vê a próxima missão, o que precisa ser feito nela e o que ela desbloqueia

#### Scenario: A tela inicial já mostra o que fazer agora

- **WHEN** o Guerreiro(a) inscrito abre o bloco da trilha
- **THEN** vê a próxima missão, o que precisa ser feito nela e o que ela desbloqueia

#### Scenario: Alternar de trilha não perde o contexto

- **WHEN** o Guerreiro(a) inscrito em duas trilhas alterna para a outra e volta
- **THEN** cada trilha reabre no ponto em que ele a deixou

#### Scenario: Sem inscrição, a tela oferece o caminho

- **WHEN** um Guerreiro(a) sem nenhuma inscrição abre o bloco da trilha
- **THEN** a tela o leva à escolha do poder, em vez de mostrar tela vazia

## ADDED Requirements

### Requirement: Os caminhos da Área do Guerreiro(a) aparecem em cartão, na ordem decidida

A Área do Guerreiro(a) SHALL apresentar os quatro caminhos como **cartões em grade**, com o
glifo acima do rótulo em frase, nesta ordem: **minha carteira**, **Trilha**, **desafios e
equipes**, **coleta do território**. A ordem é decisão do fundador e NEVER SHALL depender de
quando cada bloco foi acrescentado. (`RF-05-08`, PRD-05 §§5.2, 10, decisão do fundador de
2026-10-31)

#### Scenario: Os caminhos aparecem na ordem decidida

- **WHEN** o Guerreiro(a) em sessão vê os caminhos da área
- **THEN** eles aparecem em cartão, na ordem minha carteira, Trilha, desafios e equipes, coleta
  do território

#### Scenario: Cada caminho leva o glifo junto do rótulo

- **WHEN** um caminho da área é apresentado
- **THEN** ele traz o glifo acima do rótulo em frase, e o rótulo segue sendo o nome acessível do
  cartão

### Requirement: O caminho corrente da área é anunciado como o atual

O cartão do bloco aberto SHALL ser anunciado como o atual e distinguir-se por outro sinal além
da cor. Os caminhos SHALL permanecer alcançáveis com o bloco aberto, de modo que a área se
percorra sem passar por tela de menu. (`RF-05-08`, documento 15 §5)

#### Scenario: O bloco aberto se reconhece no cartão

- **WHEN** o Guerreiro(a) abre um dos quatro blocos
- **THEN** o cartão daquele bloco é anunciado como o atual e se distingue por outro sinal além
  da cor

#### Scenario: Trocar de bloco não passa por menu

- **WHEN** o Guerreiro(a) está num bloco e aciona o cartão de outro
- **THEN** o outro bloco abre direto, sem tela intermediária de menu

### Requirement: O cartão da Trilha nomeia a próxima missão

O cartão do caminho da Trilha SHALL nomear a **próxima missão** do Guerreiro(a) — a posição e o
título dela —, para que a primeira tela diga o que fazer agora antes de qualquer rolagem. Não
havendo próxima missão a nomear, o cartão SHALL apresentar apenas o rótulo dele, nunca espaço
vazio nem rótulo truncado. (`RF-05-08`, `RF-05-17`, PRD-05 §5.2)

#### Scenario: A próxima missão aparece no cartão

- **WHEN** o Guerreiro(a) inscrito em trilha com próxima missão vê os caminhos
- **THEN** o cartão da Trilha nomeia a posição e o título da próxima missão

#### Scenario: Sem próxima missão, o cartão fica só com o rótulo

- **WHEN** o Guerreiro(a) não tem próxima missão a nomear
- **THEN** o cartão da Trilha apresenta apenas o rótulo dele, sem espaço vazio
