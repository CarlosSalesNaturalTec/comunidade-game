# Spec Delta

## ADDED Requirements

### Requirement: O elenco admite variante, e o nome base é a versão que se apresenta

Um personagem do elenco SHALL poder ter mais de um arquivo — variante por **faixa etária**
ou por **expressão**. O arquivo de **nome base** SHALL ser sempre a versão que as aplicações
apresentam; a variante leva **sufixo** no mesmo nome. Trocar qual versão se apresenta SHALL
trocar qual arquivo leva o nome base, e NEVER SHALL deixar a versão apresentada sob sufixo.
(documento 15 §13.6)

#### Scenario: A versão apresentada é a do nome base

- **WHEN** uma aplicação pede a figura de um personagem do elenco
- **THEN** ela recebe o arquivo de nome base, sem sufixo

#### Scenario: A variante não substitui o que se apresenta

- **WHEN** um personagem tem variante além da versão apresentada
- **THEN** a variante leva sufixo no mesmo nome, e o nome base segue com a versão que as
  aplicações apresentam

### Requirement: Cada arquivo do elenco cumpre o manifesto da marca

Todo arquivo do elenco SHALL sair em **par AVIF com reserva WebP**, a **1024 px de lado
maior**, com **fundo transparente** e o **keyline `cal-050`** gravado no arquivo, dentro do
teto de peso que o manifesto da marca fixa. A pose SHALL admitir **adereço que caracteriza o
personagem**, sem afrouxar contorno, preenchimento, fundo nem keyline. (documento 15 §13.6)

#### Scenario: O par de formatos está completo

- **WHEN** os arquivos do elenco são conferidos
- **THEN** cada personagem e cada variante têm o AVIF e o WebP, nenhum sozinho

#### Scenario: O keyline está no arquivo, e não no CSS

- **WHEN** a borda da figura é examinada
- **THEN** o filete `cal-050` está gravado nos pixels do arquivo, por fora da silhueta

#### Scenario: Grade e peso cabem no manifesto

- **WHEN** um arquivo do elenco entra no repositório
- **THEN** o lado maior é 1024 px, o fundo é transparente e o peso cabe no teto do manifesto

### Requirement: Só o que se apresenta é servido pelo domínio da aplicação

A camada comum SHALL provisionar ao domínio de uma aplicação **apenas** os arquivos do elenco
que aquela aplicação apresenta. Variante guardada no repositório e não apresentada NEVER
SHALL ser publicada. (documento 15 §1, princípio 6; documento 15 §13.6)

#### Scenario: A variante guardada não vai ao ar

- **WHEN** a aplicação é publicada
- **THEN** o domínio serve as figuras que ela apresenta, e nenhuma variante que ela não usa
