# painel-do-dia Specification

## Purpose

A leitura agregada do encontro em andamento, servida ao Mestre e ao Admin: quem chegou, em que
missão cada equipe está, quem ainda aguarda aparelho, o que foi previsto e provido, o saldo do
ponto de apoio e o que falta lançar antes de a aula acabar. É o instrumento de controle do
encontro do documento 05 §4.

## Requirements

### Requirement: O painel do dia é a leitura do encontro em andamento

O núcleo SHALL expor **`GET /v1/painel-do-dia`** (PRD-02 §9), que devolve, **numa leitura só**,
o estado da aula em andamento — aquela cuja janela de data e horários contém o instante da
consulta, na comunidade de quem consulta.

O painel SHALL ser **inteiramente derivado**: fora a escolha corrente da equipe, ele NEVER SHALL
ter entidade, coluna ou registro próprio, e cada campo SHALL ser recomputado a cada consulta a
partir do que os domínios já gravaram.

Ler o painel SHALL ser ato de **Admin** ou de **Mestre**; o Mestre SHALL alcançar apenas as
aulas das comunidades a que está vinculado (`RN-02-20`). Guerreiro(a), responsável e Apoiador
SHALL receber **403**. Fora da janela de qualquer aula, o painel SHALL devolver **200 com o
encontro vazio**, e não erro — é o dia sem encontro. (`RF-02-41` a `RF-02-47`, `RF-02-69`,
`RN-02-20`, PRD-02 §§6.4, 9, 12)

#### Scenario: O painel devolve o encontro em andamento numa leitura

- **WHEN** um Admin consulta o painel do dia durante a janela de uma aula
- **THEN** o núcleo devolve aquela aula com presenças, equipes, previsto e provido, saldo e
  lançamentos pendentes, sem exigir outra consulta

#### Scenario: Fora de qualquer janela o painel volta vazio

- **WHEN** o painel é consultado num instante fora da janela de toda aula agendada
- **THEN** o núcleo responde 200 com o encontro vazio, e não erro

#### Scenario: O Mestre lê apenas o encontro da comunidade dele

- **WHEN** um Mestre consulta o painel e há aula em andamento em outra comunidade
- **THEN** aquela aula não aparece para ele

#### Scenario: Guerreiro(a) não lê o painel

- **WHEN** um Guerreiro(a) em sessão consulta o painel do dia
- **THEN** o núcleo responde 403 e nada é devolvido

### Requirement: O painel lista quem chegou e quem ainda aguarda aparelho

O painel SHALL listar os Guerreiros e Guerreiras com **presença registrada** naquela aula, com o
**modo de comprovação** de cada uma — a que a App 01 registrou por reconhecimento e a que foi
confirmada por Mestre ou Admin — sem que a gestão precise lançar coisa alguma para vê-las
(`RF-02-41`, PRD-02 §12).

O painel SHALL listar à parte quem **aguarda aparelho**: o Guerreiro(a) com presença registrada
naquela aula e **ainda sem equipe formada** nela. É lista **derivada**, e NEVER SHALL existir
entidade, coluna ou fila explícita de espera — no Ciclo 01 a plataforma não controla aparelhos
(documento 05 §5), e o aparelho é da equipe (documento 05 §4). Quem entra numa equipe SHALL
deixar a lista no mesmo instante, sem ato de ninguém. (`RF-02-43`, decisão do fundador,
2026-08-25)

#### Scenario: A presença do reconhecimento aparece sem lançamento manual

- **WHEN** a App 01 registra a presença de um Guerreiro(a) por reconhecimento
- **THEN** ele aparece no painel como chegado, com o modo de comprovação, sem lançamento da
  gestão

#### Scenario: A presença confirmada mostra quem confirmou

- **WHEN** a presença foi confirmada por um Mestre depois de falha de identificação
- **THEN** o painel a mostra com o modo de comprovação e quem confirmou

#### Scenario: Presente sem equipe aparece aguardando aparelho

- **WHEN** um Guerreiro(a) tem presença registrada e não integra equipe alguma daquela aula
- **THEN** ele aparece na lista de quem aguarda aparelho

#### Scenario: Entrar numa equipe tira da espera

- **WHEN** um Guerreiro(a) que aguardava aparelho entra numa equipe da aula
- **THEN** a consulta seguinte não o traz mais na lista de espera, e ninguém precisou marcá-lo

#### Scenario: Quem não chegou não aparece em lista alguma

- **WHEN** um Guerreiro(a) da comunidade não tem presença registrada naquela aula
- **THEN** ele não aparece nem como chegado nem como aguardando aparelho

### Requirement: O painel mostra cada equipe com a missão em que ela está

O painel SHALL listar as **equipes formadas na App 01** naquela aula, cada uma com os seus
integrantes e com a **missão em que ela está** — a da atividade da programação que a equipe
declarou como corrente. Equipe que ainda não declarou escolha SHALL aparecer **sem missão**, e
não com erro nem com missão suposta pelo núcleo.

A gestão SHALL ler a composição e NEVER SHALL alterá-la: a composição é dos Guerreiros e
Guerreiras, formada na App 01 (documento 02 §5, `RF-02-09`). (`RF-02-42`, `RF-02-08`, `RN-02-07`,
PRD-02 §6.4)

#### Scenario: A equipe sai com a missão que declarou

- **WHEN** uma equipe da aula declarou a atividade da programação que está trabalhando
- **THEN** o painel a mostra com a missão daquela atividade

#### Scenario: Duas equipes em trilhas diferentes saem cada uma com a sua

- **WHEN** duas equipes do mesmo encontro declararam atividades de trilhas diferentes
- **THEN** o painel mostra cada uma com a missão que ela declarou

#### Scenario: Equipe sem escolha aparece sem missão

- **WHEN** uma equipe formada ainda não declarou atividade alguma
- **THEN** ela aparece no painel sem missão, e o núcleo não supõe nenhuma

#### Scenario: Trocar de atividade muda o que o painel mostra

- **WHEN** a equipe declara outra atividade da programação durante o encontro
- **THEN** a consulta seguinte do painel a mostra na missão nova

### Requirement: O painel mostra o previsto, o provido e o saldo do ponto de apoio

O painel SHALL mostrar a **atividade prevista** da aula e os **recursos providos** — as reservas
que o agendamento constituiu, com tipo de recurso e quantidade (`RF-02-44`).

O painel SHALL mostrar o **saldo dos tipos de recurso do ponto de apoio da aula**, derivado dos
lançamentos como todo saldo do livro-razão (`RN-07-36`). Os tipos SHALL vir do **catálogo
configurável** da gestão: o núcleo NEVER SHALL fixar tipo de recurso em código. "Kits MDF" e
"exemplares da linha Alpha" são exemplo de operação, não catálogo — decisão do fundador,
2026-08-25, que corrige o texto do `RF-02-45`. (`RF-02-44`, `RF-02-45`, `RN-07-36`, PRD-02 §6.4)

#### Scenario: O previsto e o provido saem juntos

- **WHEN** o painel é consultado numa aula que reservou dois tipos de recurso
- **THEN** ele mostra a atividade prevista e as duas reservas, com tipo e quantidade

#### Scenario: O saldo é o do ponto de apoio da aula

- **WHEN** o painel mostra o saldo de um tipo de recurso
- **THEN** o valor é o saldo daquele tipo no ponto de apoio em que a aula acontece

#### Scenario: Tipo novo do catálogo aparece sem tocar em código

- **WHEN** a gestão cadastra um tipo de recurso novo e ele tem saldo no ponto de apoio da aula
- **THEN** o painel passa a mostrá-lo, sem que nenhum tipo esteja fixado no núcleo

#### Scenario: Aula sem recurso declarado mostra o previsto e nenhuma reserva

- **WHEN** a aula não declarou recurso algum
- **THEN** o painel mostra a atividade prevista e nenhuma reserva, sem erro

### Requirement: O painel lista o que falta lançar antes de a aula terminar

O painel SHALL listar os **lançamentos pendentes do encontro** — o que precisa ser lançado antes
de a aula terminar. São pendências enquanto a aula não passa a **realizada**: o **lançamento da
atividade realizada**, que é ato por aula (`RF-07-09`), e a **digitalização do termo de
biometria** assinado no encontro e ainda não anexada (`RF-02-69`).

O painel SHALL apenas **listar**: ele NEVER SHALL lançar, e cada pendência SHALL ser resolvida
na rota que já a atende. Lançada a atividade realizada, a pendência SHALL sair da lista na
consulta seguinte, sem ato de ninguém.

`RF-02-46` e `RF-02-47` enunciam o mesmo requisito, em redação duplicada — decisão do fundador,
2026-08-25, que os consolida num só. (`RF-02-46`, `RF-02-47`, `RF-02-69`, `RN-02-12`,
PRD-02 §§6.4, 12)

#### Scenario: A atividade não lançada é pendência do encontro

- **WHEN** o painel é consultado numa aula em andamento cuja atividade realizada não foi lançada
- **THEN** o lançamento da atividade realizada aparece entre as pendências

#### Scenario: Termo de biometria sem digitalização é pendência

- **WHEN** um Guerreiro(a) do encontro tem consentimento de biometria e nenhuma digitalização
  anexada
- **THEN** o painel o lista entre os termos que aguardam digitalização

#### Scenario: Anexada a digitalização, a pendência sai

- **WHEN** um Admin anexa a digitalização do termo
- **THEN** a consulta seguinte do painel não traz mais aquele termo entre as pendências

#### Scenario: Lançada a atividade, a pendência sai

- **WHEN** o Admin lança a atividade realizada e a aula passa a realizada
- **THEN** a consulta seguinte não traz mais aquele lançamento entre as pendências

#### Scenario: O painel não lança

- **WHEN** o painel é consultado
- **THEN** nenhuma escrita acontece por causa da consulta, e as pendências seguem como estavam

### Requirement: O painel nunca expõe imagem real nem dado pessoal de criança

O painel SHALL apresentar cada Guerreiro(a) por **nick e avatar**, e NEVER SHALL devolver
imagem real, descritor biométrico, nome civil, data de nascimento nem endereço — vale aqui o que
vale em toda tela de gestão (`RN-02-22`, invariante 12 do documento 99 §6).

A pendência de digitalização do termo SHALL nomear o Guerreiro(a) pelo **nick**, e NEVER SHALL
devolver o conteúdo da digitalização já anexada: o painel diz que falta, não serve o arquivo.
(`RN-02-22`, `RF-02-69`, PRD-02 §§11, 12)

#### Scenario: O painel apresenta a criança por nick e avatar

- **WHEN** o painel devolve as presenças e as equipes do encontro
- **THEN** cada Guerreiro(a) aparece por nick e avatar, e nenhuma imagem real é devolvida

#### Scenario: O painel não devolve descritor biométrico

- **WHEN** o painel devolve a lista de termos que aguardam digitalização
- **THEN** nenhum descritor biométrico e nenhuma digitalização acompanham a resposta
