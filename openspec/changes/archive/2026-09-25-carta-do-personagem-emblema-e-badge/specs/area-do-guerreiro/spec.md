# Spec Delta

## MODIFIED Requirements

### Requirement: O progresso mostra o nível e o que falta, nunca saldo de pontos

A aplicação SHALL exibir, por trilha ou poder, o **nível** do Guerreiro(a) e **quantas missões
obrigatórias faltam** para o próximo — nível é **percurso**, não saldo. SHALL exibir também os
**pontos, badges e recompensas conquistadas** por trilha ou poder, nunca de forma global, e
NEVER SHALL apresentar o nível como decorrência do total de pontos. Resultado ainda **não
lançado pelo Mestre** SHALL aparecer como **"aguardando lançamento"**, e a aplicação NEVER
SHALL lançar resultado, presença ou mérito. (`RF-05-15`, `RF-05-16`, `RF-05-18`, `RN-05-03`,
`RN-05-04`, `RN-05-06`)

O **nível** SHALL ser apresentado pelo **emblema contável** da camada comum — uma marca por nível,
moldura fechada no nível 5 —, e os **badges** pela **silhueta da família** de cada um, com o glifo do
poder. NEVER SHALL apresentar o nível apenas como numeral nem o badge apenas como texto: o emblema
existe para ser contado por uma criança de 6 anos. (`RF-05-15`, `RF-05-16`, documento 15 §§8.2, 8.3,
8.4)

#### Scenario: O progresso diz quantas faltam

- **WHEN** o Guerreiro(a) abre o progresso de uma trilha
- **THEN** vê o nível atual e quantas missões obrigatórias faltam para o próximo

#### Scenario: Nada sobe de nível por acúmulo de pontos

- **WHEN** o Guerreiro(a) acumula pontos sem desbloquear missão obrigatória
- **THEN** o nível exibido não muda

#### Scenario: O que o Mestre ainda não lançou aparece como tal

- **WHEN** o Guerreiro(a) cumpriu uma atividade cujo Resultado o Mestre ainda não lançou
- **THEN** a tela mostra "aguardando lançamento", sem creditar ponto nem avançar o nível

#### Scenario: Nenhuma tela lança resultado

- **WHEN** o Guerreiro(a) percorre qualquer tela do bloco da trilha
- **THEN** nenhuma ação de lançar resultado, presença ou mérito é oferecida

#### Scenario: O nível aparece como marcas contáveis

- **WHEN** o progresso de uma trilha em que o Guerreiro(a) está no nível 3 é apresentado
- **THEN** o emblema traz três marcas contáveis, além do numeral, e não só o numeral

#### Scenario: O badge aparece pela silhueta da família

- **WHEN** o progresso apresenta os badges conquistados
- **THEN** cada um aparece com a silhueta da família dele e o glifo do poder, não como texto solto

## ADDED Requirements

### Requirement: A Área do Guerreiro(a) apresenta a carta do próprio Guerreiro(a)

A App 05 SHALL apresentar ao Guerreiro(a) em sessão a **carta dele**, na variante Guerreiro(a) do
documento 11 §8.2: avatar, nick, badges, poderes com níveis, desempenho e criações originais. NEVER
SHALL exibir nela imagem real, nome civil, rede social nem canal de contato. (`RF-05-50`,
`RF-05-51`, documento 11 §8.2, documento 15 §8.1)

A carta SHALL ser montada a partir das leituras que a aplicação já consome, e NEVER SHALL ser
apresentada **incompleta**: faltando o que a variante exige, a Área SHALL apresentar o que tem em
outra forma. (documento 11 §8.2)

O avatar da carta SHALL ser o avatar paramétrico desenhado, caindo no avatar padrão do projeto
quando faltar. (documento 15 §§7.3, 8.1)

#### Scenario: O Guerreiro(a) vê a própria carta

- **WHEN** o Guerreiro(a) abre a Área dele
- **THEN** a carta apresenta avatar, nick, badges, poderes com níveis e criações originais

#### Scenario: A carta do Guerreiro(a) não expõe o que é vedado

- **WHEN** a carta é apresentada
- **THEN** nela não aparecem imagem real, nome civil, rede social nem canal de contato

#### Scenario: Sem avatar, a carta usa o padrão do projeto

- **WHEN** o Guerreiro(a) não tem avatar composto
- **THEN** a carta apresenta o avatar padrão do projeto, e nenhum espaço vazio no lugar dele
