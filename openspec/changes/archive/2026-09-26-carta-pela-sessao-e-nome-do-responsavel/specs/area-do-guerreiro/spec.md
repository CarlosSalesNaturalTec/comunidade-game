# Spec Delta

## MODIFIED Requirements

### Requirement: A Área do Guerreiro(a) apresenta a carta do próprio Guerreiro(a)

A App 05 SHALL apresentar ao Guerreiro(a) em sessão a **carta dele**, na variante Guerreiro(a) do
documento 11 §8.2: avatar, nick, badges, poderes com níveis, desempenho e criações originais. NEVER
SHALL exibir nela imagem real, nome civil, rede social nem canal de contato. (`RF-05-50`,
`RF-05-51`, documento 11 §8.2, documento 15 §8.1)

A carta SHALL ser montada a partir das leituras que a aplicação já consome, e NEVER SHALL ser
apresentada **incompleta**: faltando o que a variante exige, a Área SHALL apresentar o que tem em
outra forma. (documento 11 §8.2)

A montagem SHALL tirar o **nick e o avatar** da leitura da sessão e o **desempenho** do ranking
logado da turma, e NEVER SHALL depender de o Guerreiro(a) ter aberto **série de coleta**: a
coleta do território é percurso de quem a escolheu, e carta é de todo Guerreiro(a). O
Guerreiro(a) que acabou de entrar na plataforma, sem coleta e sem ponto creditado, SHALL ver a
carta dele. (`RF-05-50`, `RF-05-51`, `RF-01-76`)

O avatar da carta SHALL ser o avatar paramétrico desenhado, caindo no avatar padrão do projeto
quando faltar. (documento 15 §§7.3, 8.1)

#### Scenario: O Guerreiro(a) vê a própria carta

- **WHEN** o Guerreiro(a) abre a Área dele
- **THEN** a carta apresenta avatar, nick, badges, poderes com níveis e criações originais

#### Scenario: A carta aparece sem série de coleta aberta

- **WHEN** o Guerreiro(a) em sessão nunca abriu série de coleta
- **THEN** a carta é apresentada assim mesmo, com o desempenho que ele tem

#### Scenario: A carta do Guerreiro(a) não expõe o que é vedado

- **WHEN** a carta é apresentada
- **THEN** nela não aparecem imagem real, nome civil, rede social nem canal de contato

#### Scenario: Sem avatar, a carta usa o padrão do projeto

- **WHEN** o Guerreiro(a) não tem avatar composto
- **THEN** a carta apresenta o avatar padrão do projeto, e nenhum espaço vazio no lugar dele

### Requirement: A App 05 mostra o ranking da turma com a própria posição sempre visível

A aplicação SHALL exibir o ranking da Comunidade Virtual do Guerreiro(a), **por trilha ou por
poder**, somente com **pontos regulares**, alcançando **a turma inteira** — inclusive quem não
tem divulgação autorizada. A **própria posição** SHALL estar sempre visível, ainda que fora da
faixa exibida. De cada colega a tela SHALL mostrar **apenas avatar, nick e posição**.
(`RF-05-52`, `RF-05-53`, `RF-05-84`, `RN-05-16`, `RN-05-18`, `RN-05-21`)

A tela NEVER SHALL descobrir a comunidade do Guerreiro(a) por outra leitura antes de pedir o
ranking, e NEVER SHALL condicionar o ranking a ter **série de coleta** aberta: a comunidade
vem do vínculo vigente, derivada pelo núcleo. (`RF-05-52`, `RN-05-16`)

#### Scenario: A turma inteira aparece

- **WHEN** o Guerreiro(a) abre o ranking
- **THEN** vê os colegas da sua comunidade, inclusive os sem divulgação autorizada

#### Scenario: O ranking abre sem série de coleta aberta

- **WHEN** o Guerreiro(a) que nunca abriu série de coleta abre o ranking
- **THEN** a tela apresenta o ranking da turma dele, e nada pede que ele abra uma coleta

#### Scenario: A própria posição nunca some

- **WHEN** o Guerreiro(a) está fora das primeiras posições exibidas
- **THEN** a tela mostra assim mesmo em que posição ele está

#### Scenario: A alternância entre trilha e poder mantém a leitura

- **WHEN** o Guerreiro(a) troca o recorte entre trilha e poder
- **THEN** o ranking é reordenado pelo ponto regular daquele recorte

#### Scenario: Nenhum dado pessoal de colega na tela

- **WHEN** o ranking é exibido
- **THEN** cada colega aparece só por avatar, nick e posição, sem imagem real nem nome civil

#### Scenario: Ponto extra não aparece no ranking

- **WHEN** o ranking é exibido
- **THEN** nenhuma posição considera ou mostra ponto extra
