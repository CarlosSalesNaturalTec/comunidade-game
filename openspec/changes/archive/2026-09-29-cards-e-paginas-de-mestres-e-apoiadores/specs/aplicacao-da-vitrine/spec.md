# Spec Delta

## ADDED Requirements

### Requirement: A seção de Mestres apresenta cada Mestre em card e em página

A App 06 SHALL apresentar a seção **Mestres**, com um card por Mestre na variante Mestre da
carta, e cada card SHALL abrir a **página individual do Mestre** em endereço próprio,
alcançável direto e compartilhável.

A página SHALL detalhar o que o documento 11 §8.2 atribui a ela: as **habilidades**, as
**trilhas de autoria**, a **prova pública** — currículo, portfólios, redes sociais e
documentos comprobatórios externos, cada um como link com rótulo — e **quantas vezes ele
sustentou atividade que estava sem recurso**.

Mestre cuja leitura não devolve o que a variante exige SHALL ser apresentado em outra forma,
nunca em carta incompleta. A App 06 NEVER SHALL oferecer edição da página: editar é ato do
próprio Mestre, na App 09. (`RF-03-02`, `RF-03-03`, `RF-03-07`, PRD-03 §4, documento 11 §8.2)

#### Scenario: Cada Mestre sai em card

- **WHEN** a seção de Mestres é aberta e o núcleo devolve três Mestres
- **THEN** três cards aparecem, cada um com avatar, nick, áreas de habilidade, comprobatórios,
  trilhas de autoria e o selo de sustento

#### Scenario: O card abre a página do Mestre em endereço próprio

- **WHEN** o visitante abre o card de um Mestre
- **THEN** a página daquele Mestre abre em endereço próprio, e o mesmo endereço, aberto
  direto, leva à mesma página

#### Scenario: A página traz a prova pública como link

- **WHEN** o visitante abre a página de um Mestre com currículo e portfólio declarados
- **THEN** os dois aparecem como link, cada um com o rótulo do que aponta

#### Scenario: A vitrine não edita a página do Mestre

- **WHEN** o visitante abre a página de um Mestre
- **THEN** nenhuma ação de editar, acrescentar ou remover é apresentada

### Requirement: A seção de Apoiadores apresenta cada Apoiador em card e em página

A App 06 SHALL apresentar a seção **Apoiadores**, com um card por Apoiador na variante
Apoiador da carta, e cada card SHALL abrir a **página individual do Apoiador** em endereço
próprio, alcançável direto e compartilhável.

A página SHALL detalhar o que o documento 11 §8.2 atribui a ela: os **aportes em moedas**, o
**nível de sustento** e os **selos**, os **desafios extras propostos com a efetividade deles**
— trilha, período e quantos concluíram — e a **prova do apoio**, como link com rótulo.

A seção NEVER SHALL apresentar Apoiador sem aporte homologado, NEVER SHALL exibir valor em
reais e NEVER SHALL ordenar, classificar ou comparar Apoiadores por valor aportado: a ordem é
alfabética pela identificação que o card exibe. (`RF-03-02`, `RF-03-03`, `RF-03-07`,
`RF-03-10`, `RF-03-55`, `RF-03-56`, `RF-03-57`, `RF-03-66`, `RF-03-80`, `RN-03-18`,
`RN-03-26`, `RN-03-37`, `RN-14-38`)

#### Scenario: Cada Apoiador com aporte homologado sai em card

- **WHEN** a seção de Apoiadores é aberta e o núcleo devolve dois Apoiadores
- **THEN** dois cards aparecem, cada um com avatar, nick e o total de moedas em destaque, na
  moldura comum

#### Scenario: Quem não teve aporte homologado não está lá

- **WHEN** a seção de Apoiadores é aberta
- **THEN** nenhum Apoiador sem aporte homologado aparece, e nenhum espaço vazio o anuncia

#### Scenario: A seção não é um pódio

- **WHEN** a seção de Apoiadores é aberta com Apoiadores de totais diferentes
- **THEN** os cards aparecem em ordem alfabética, sem posição, pódio ou comparação por valor

#### Scenario: A página traz os desafios propostos com a efetividade

- **WHEN** o visitante abre a página de um Apoiador que propôs um desafio extra concluído
- **THEN** a página traz a trilha, o período e quantos concluíram, e nenhum dado de quem
  concluiu

## MODIFIED Requirements

### Requirement: A seção de poderes apresenta cada poder com as trilhas dele

A App 06 SHALL apresentar a seção **poderes**, com cada poder e as **trilhas** vinculadas a ele,
e a página do poder com as mesmas trilhas. Cada poder SHALL apresentar também os **Mestres
responsáveis** do documento 11 §8.2 — os autores das trilhas publicadas daquele poder —, cada
um com **link para a página individual do Mestre**. Poder sem trilha publicada SHALL ser
apresentado **sem espaço vazio** no lugar dos Mestres. (`RF-03-02`, documento 11 §8.2,
decisões do fundador de 2026-09-28 e 2026-09-29)

#### Scenario: O poder aparece com as trilhas

- **WHEN** o visitante abre a seção de poderes
- **THEN** cada poder aparece com as trilhas vinculadas a ele

#### Scenario: O poder aparece com os Mestres responsáveis

- **WHEN** o visitante abre a seção de poderes e um poder tem duas trilhas publicadas de
  Mestres diferentes
- **THEN** aquele poder aparece com os dois Mestres, cada um levando à página individual dele

#### Scenario: A seção não promete o que ainda não tem

- **WHEN** o visitante abre um poder que não tem trilha publicada alguma, e portanto nenhum
  Mestre responsável
- **THEN** nenhum espaço vazio ou promessa de Mestres responsáveis é apresentado

### Requirement: Toda página individual traz a chamada "Quero participar", e acompanhar leva à mesma porta

A App 06 SHALL apresentar, em **toda página individual** que publica, a chamada **"Quero
participar"**, e SHALL apresentar na mesma página a **ação de acompanhar ou favoritar**, que
SHALL levar à **mesma porta** da chamada. As duas SHALL abrir a porta do convite sem exigir
cadastro, login ou dado do visitante. Com as páginas de Mestre e de Apoiador publicadas, a
chamada SHALL aparecer nas **quatro** páginas individuais que a vitrine tem — Guerreiro(a),
comunidade, Mestre e Apoiador. (`RF-03-39`, `RF-03-40`, PRD-03 §5.5)

#### Scenario: A página do Guerreiro(a) convida

- **WHEN** o visitante abre a página individual de um Guerreiro(a) com autorização vigente
- **THEN** a página traz a chamada "Quero participar" e a ação de acompanhar

#### Scenario: A página da comunidade convida

- **WHEN** o visitante abre a página de uma Comunidade Virtual
- **THEN** a página traz a chamada "Quero participar" e a ação de acompanhar

#### Scenario: A página do Mestre convida

- **WHEN** o visitante abre a página individual de um Mestre
- **THEN** a página traz a chamada "Quero participar" e a ação de acompanhar

#### Scenario: A página do Apoiador convida

- **WHEN** o visitante abre a página individual de um Apoiador
- **THEN** a página traz a chamada "Quero participar" e a ação de acompanhar

#### Scenario: Acompanhar chega à porta do convite

- **WHEN** o visitante aciona a ação de acompanhar
- **THEN** a porta do convite abre, a mesma que a chamada "Quero participar" abre
