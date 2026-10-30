# Spec Delta

## MODIFIED Requirements

### Requirement: A Área do Guerreiro(a) apresenta a carta do próprio Guerreiro(a)

A App 05 SHALL apresentar ao Guerreiro(a) em sessão a **carta dele**, na variante Guerreiro(a) do
documento 11 §8.2: avatar, nick, badges, poderes com níveis, desempenho, criações originais e o
**saldo disponível de pontos extras** — o que dá para trocar por recompensa avulsa. NEVER
SHALL exibir nela imagem real, nome civil, rede social nem canal de contato. (`RF-05-50`,
`RF-05-51`, `RF-05-82`, documento 11 §8.2, documento 15 §8.1)

A carta SHALL ser montada a partir das leituras que a aplicação já consome, e NEVER SHALL ser
apresentada **incompleta**: faltando o que a variante exige, a Área SHALL apresentar o que tem em
outra forma. O saldo NEVER SHALL estar entre o que a variante exige: a leitura dele que não chega
deixa a carta sem a seção, nunca sem carta. (documento 11 §8.2)

A montagem SHALL tirar o **nick e o avatar** da leitura da sessão e o **desempenho** do ranking
logado da turma, e NEVER SHALL depender de o Guerreiro(a) ter aberto **série de coleta**: a
coleta do território é percurso de quem a escolheu, e carta é de todo Guerreiro(a). O
Guerreiro(a) que acabou de entrar na plataforma, sem coleta e sem ponto creditado, SHALL ver a
carta dele. (`RF-05-50`, `RF-05-51`, `RF-01-76`)

O avatar da carta SHALL ser o avatar paramétrico desenhado, caindo no avatar padrão do projeto
quando faltar. (documento 15 §§7.3, 8.1)

#### Scenario: O Guerreiro(a) vê a própria carta

- **WHEN** o Guerreiro(a) abre a Área dele
- **THEN** a carta apresenta avatar, nick, badges, poderes com níveis, criações originais e o saldo
  de pontos extras que dá para trocar

#### Scenario: A carta aparece sem série de coleta aberta

- **WHEN** o Guerreiro(a) em sessão nunca abriu série de coleta
- **THEN** a carta é apresentada assim mesmo, com o desempenho que ele tem

#### Scenario: Sem o saldo, a carta continua se apresentando

- **WHEN** a leitura do saldo de pontos extras não chega
- **THEN** a carta é apresentada sem a seção do saldo, e nenhuma outra forma substitui a carta

#### Scenario: A carta do Guerreiro(a) não expõe o que é vedado

- **WHEN** a carta é apresentada
- **THEN** nela não aparecem imagem real, nome civil, rede social nem canal de contato

#### Scenario: Sem avatar, a carta usa o padrão do projeto

- **WHEN** o Guerreiro(a) não tem avatar composto
- **THEN** a carta apresenta o avatar padrão do projeto, e nenhum espaço vazio no lugar dele

### Requirement: A App 05 mostra as duas contas de ponto extra, separadas

A aplicação SHALL exibir ao Guerreiro(a) em sessão o **acumulado** e o **saldo disponível** de
pontos extras **separados e rotulados**, sem somá-los e sem confundi-los com o ponto regular. A
tela SHALL dizer, em linguagem simples, que o acumulado **só cresce** e que o trocável é o
**saldo disponível**. As duas contas SHALL continuar na carteira mesmo com o saldo também
apresentado na carta: ali ele aparece como o que dá para trocar, e na carteira as duas contas
aparecem lado a lado, cada uma com o rótulo próprio. (`RF-05-82`, `RN-05-39`, `RN-05-40`,
`RN-05-42`, PRD-05 §5.6, decisão do fundador de 2026-10-30)

#### Scenario: As duas contas aparecem distintas

- **WHEN** o Guerreiro(a) abre a carteira
- **THEN** vê o acumulado e o saldo disponível como dois números rotulados, nunca somados

#### Scenario: O saldo na carta não dispensa a carteira

- **WHEN** a carteira é apresentada com a carta do Guerreiro(a)
- **THEN** o saldo aparece nas duas, com rótulo próprio em cada uma, e o acumulado continua
  aparecendo só na carteira

#### Scenario: Ponto regular não entra na carteira

- **WHEN** a carteira é exibida
- **THEN** nenhum ponto regular é somado nem apresentado como trocável

#### Scenario: A carteira é só a própria

- **WHEN** o Guerreiro(a) abre a carteira
- **THEN** nenhuma conta de outra criança é exibida
