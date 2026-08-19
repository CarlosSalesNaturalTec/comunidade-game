# PRDs — Documentos de Requisitos de Produto

Esta pasta reúne os **PRDs** (_Product Requirements Documents_) do Comunidade Game, derivados
do documento 08 e escritos um a um, na ordem das ondas abaixo. Cada PRD segue o
[modelo de PRD](00-modelo-de-prd.md) e vale para o **Ciclo 01** (Guerreira Zeferina,
ago–dez/2026).

O PRD é artefato **derivado**: ele aplica as regras dos documentos 01–15 e não cria regra
própria. As regras de escrita, o fluxo de decisão das pendências e o processo de entrega estão
no `CLAUDE.md`, na raiz do repositório; o mapa de dependências entre PRDs está no documento 99.

## Situação da esteira

| PRD                                       | Assunto                                | Aplicação | Onda | Situação     |
| ----------------------------------------- | -------------------------------------- | --------- | ---- | ------------ |
| [PRD-08](prd-08-comunidades-virtuais.md)  | Comunidades Virtuais e território      | —         | 1    | implementado |
| [PRD-07](prd-07-economia-e-ledger.md)     | Economia de recursos e ledger          | —         | 1    | aprovado     |
| [PRD-01](prd-01-backend-api.md)           | Backend API (núcleo)                   | —         | 1    | implementado |
| [PRD-02](prd-02-frontend-de-gestao.md)    | Frontend de gestão                     | App 03    | 2    | aprovado     |
| [PRD-04](prd-04-aula-presencial.md)       | Aula presencial (onboarding e trilhas) | App 01    | 2    | aprovado     |
| [PRD-09](prd-09-area-do-mestre.md)        | Área do Mestre (autoria e operação)    | App 09    | 3    | aprovado     |
| [PRD-05](prd-05-area-do-guerreiro.md)     | Área do Guerreiro(a)                   | App 05    | 3    | aprovado     |
| [PRD-13](prd-13-area-dos-responsaveis.md) | Área dos pais e responsáveis           | App 07    | 4    | aprovado     |
| [PRD-03](prd-03-vitrine-publica.md)       | Vitrine pública                        | App 06    | 4    | aprovado     |
| [PRD-14](prd-14-area-do-apoiador.md)      | Área do Apoiador                       | App 08    | 5    | aprovado     |
| [PRD-10](prd-10-batalhas.md)              | Batalhas e eventos presenciais         | —         | 5    | aprovado     |
| [PRD-12](prd-12-jogo-em-javascript.md)    | App 04: Jogo em JavaScript             | App 04    | 5    | aprovado     |
| [PRD-11](prd-11-personalizacao-por-ia.md) | Personalização por IA                  | —         | 5    | aprovado     |

Situações possíveis: **não iniciado**, **em elicitação**, **em redação**, **em revisão**,
**aprovado** e **implementado**. O link para o documento aparece nesta tabela quando ele entra
na pasta.

O PRD-01 volta a **implementado**: a change `ponto-de-apoio-e-tabela-de-referencia`, primeira
fatia do PRD-07, entregou o `PontoDeApoio` e fechou o `RF-01-71` — a aula passa a declarar
**em qual ponto de apoio acontece**, exigido e da mesma comunidade dela. Era a última pendência
do PRD-01. Antes disso, a change `auditoria-e-estorno-da-coleta` entregou o débito de ponto
regular por fato desfeito (`RF-01-57`, `RF-01-69`, `RF-01-70`, `RN-01-55`) e a queda da
credencial de dispositivo ao **encerramento da série** (`RF-01-68`).

O PRD-07 segue em implementação. A primeira fatia entregou, além do `PontoDeApoio`, o
catálogo de **tipos de recurso** e o **valor de referência em moedas** versionado por vigência
(`RF-07-01`, `RF-07-02`), com o **responsável pelo acervo designado depois do cadastro**
(`RF-07-49`, `RN-07-34`).

A segunda fatia entregou o **livro-razão** — lançamento imutável, de natureza crédito, débito
ou ajuste, recusado a alterar ou remover também fora do ORM (`RF-07-19`, `RN-07-15`), e o saldo
por tipo de recurso **e ponto de apoio**, sempre derivado dos lançamentos e recontável
(`RF-07-07`, `RN-07-36`) — e o **aporte**: registro pelo Admin, valorado pela vigência da
tabela **na data do aporte** (`RF-07-04`, `RF-07-05`, `RN-07-03`), a absorção de Mestre ou
Admin que credita no ato, sem homologação, e nasce **ressarcível** (`RF-07-06`, `RF-07-21`,
`RN-07-35`), o comprovante em PDF, JPG ou PNG (`RN-07-22`) e a homologação do aporte declarado
no pré-cadastro, que credita só nesse ato (`RF-07-30`, `RN-07-21`).

A terceira fatia entregou a **reserva** — o vínculo entre a aula e o recurso que ela consome,
que compromete o saldo sem movimentá-lo (`RF-07-08`, `RN-07-01`). O agendamento passa a
declarar os recursos consumidos e a reservá-los no ponto de apoio da aula: havendo disponível
para todos, a aula nasce **confirmada**; faltando qualquer parcela, nasce **pendente de
lastro**, sem reserva alguma. O **lançamento da atividade realizada** grava os resultados dos
participantes e, na mesma operação, converte cada reserva em **baixa** — um débito por reserva
— e leva a aula a **realizada** (`RF-07-09`, `RF-02-35`, `RN-07-36`). O **cancelamento**, de
Admin ou Mestre da comunidade da aula, **libera** as reservas (`RF-01-72`, `RF-02-95`) — fecha
o `RF-01-72` do PRD-01, a primeira escrita de gestão do Mestre. A reserva nunca expira por
decurso de prazo. O **aporte que fecha a diferença confirma a aula pendente de lastro no mesmo
ato**, sem ato humano de confirmação (`RN-07-37`) — o `RF-02-67` deixa de atribuir esse ato à
App 03 e passa a apenas mostrá-lo.

A quarta fatia entregou a **necessidade de recurso** publicada: a falta de uma aula pendente de
lastro, derivada — sem tabela nova — do que ela declarou consumir menos o disponível no ponto
de apoio, uma por par **aula e tipo de recurso**, contada na ordem do horário inicial da aula
(`RF-07-18`, `RF-07-27`, `RN-07-37`). A necessidade sai com tipo, quantidade que falta, valor em
moedas pela vigência corrente, comunidade, ponto de apoio, data e horário — em
**`GET /vitrine/necessidades`**, pública, e **`GET /necessidades/minhas`**, do Mestre, filtrada
pelo vínculo de comunidade (`RF-03-47`). A **cobertura parcial** abate a falta a cada aporte
homologado e a necessidade só sai da lista quando o saldo fecha, o que já confirma a aula no
mesmo ato (`RF-07-31`, `RN-07-23`).

A quinta fatia entregou a superfície de leitura do livro-razão: o **Poder Sustentador** do
provedor, derivado da cadeia aporte → crédito → ajuste e nunca da soma dos aportes
(`RF-07-10`, `RN-07-15`), e a **contagem de absorções**, derivada só dos aportes de forma
absorção e por isso independente do Poder Sustentador (`RF-07-26`, `RN-07-19`) — em
**`GET /provedores/{id}/poder-sustentador`**, pública, e **`GET /meus-aportes`**, do Apoiador
em sessão (`RF-07-17`). A **prestação de contas pública** — movimentado total e por provedor
em **`GET /prestacao-de-contas`**, consumo por aula e por comunidade em
**`GET /prestacao-de-contas/aulas`** — é painel vivo, sem fechamento periódico (`RF-07-16`,
`RN-07-31`). O **lançamento de débito** passa a declarar a **aula** que o consumiu, gravada
no ato da baixa; débito lançado antes desta fatia fica sem aula, por ser somente inserção
(`RN-07-15`).

A sexta fatia entregou o **ressarcimento**, fechando o ciclo inteiro do aporte por absorção:
como ele nasce e como termina. O aporte ganha **destinação** — lastro ou ressarcimento —, e a
receita destinada a ressarcir credita o Poder Sustentador de quem doou sem virar lastro
(`RF-07-23`, `RN-07-38`). A absorção passa a poder declarar a **aula cuja necessidade atende**
(`RF-07-28`) e a exigir o **valor de origem em reais** quando houve desembolso — consumível,
durável ou financeira; a absorção de **serviço** nasce **não ressarcível**, decisão nova desta
fatia que fecha a contradição entre o `RN-07-39` e o `RN-07-24` (`RF-07-21`). O Admin lê a fila
de aportes ressarcíveis por antiguidade em **`GET /aportes/ressarciveis`** e registra o
pagamento, com comprovante exigido, em **`POST /aportes/{id}/ressarcimento`** — recusado se o
valor exceder o que a **receita destinada** ainda cobre, decisão nova que torna o teto regra do
núcleo (`RN-07-17`). O pagamento reverte as moedas por **lançamento de ajuste de quantidade
zero**, sem mexer no saldo de recurso nem na contagem de absorções (`RF-07-25`, `RN-07-18`).
Quem absorveu acompanha a própria situação em **`GET /meus-aportes/ressarciveis`**.

A sétima fatia entregou a **régua de preço em pontos extras** — `PrecoDeReferencia`, irmã do
valor em moedas, mesma vigência semiaberta, com o **piso de 20 pontos** e sem conversão
alguma entre as duas réguas (`RF-07-42` a `RF-07-44`, `RN-07-24`, `RN-07-25`, `RN-07-30`) — e o
**item do catálogo avulso**: cadastrado por Mestre, sem homologação, ou por Apoiador, pendente
até um Admin decidir (`RF-09-100`, `RN-14-42`); ativo só com **lastro igual ou maior que o
estoque declarado** no seu ponto de apoio, decisão nova desta fatia (`RF-07-34`, `RN-07-26`); e
sem preço próprio — lê sempre a vigência corrente do seu tipo de recurso (`RF-07-45`,
`RN-07-29`). Três decisões novas: a **janela de troca** do `RF-04-49` é garantia da App 01, não
regra do núcleo; o **lastro do item** é o saldo igual ou maior que o estoque; e o
`ItemDeCatalogoAvulso` **declara o ponto de apoio**, como a `Aula` já declara.

A oitava fatia entregou a **troca de recompensa avulsa** — o único débito de ponto extra do
Ciclo 01. O `PontoExtra` ganha a operação de débito do **saldo disponível**, sem tocar o
**acumulado** (`RF-01-56`, `RN-01-39`, `RN-01-40`); o `ItemDeCatalogoAvulso` tem o **estoque**
decrementado pela entrega, fora do caminho de gestão, e chega a zero sem ser retirado nem
desativado (`RF-07-36`, `RF-07-37`). A `Troca` grava item, Guerreiro(a), **preço cobrado na
vigência corrente** — que a mudança posterior da tabela não reescreve —, o encontro, o Mestre
que entregou e a data (`RF-07-35`, `RF-07-46`). Quatro recusas protegem a operação, todas antes
de qualquer escrita: item inativo ou sem lastro reverificado no ato, estoque zero, Guerreiro(a)
de comunidade diferente da do item, e saldo disponível menor que o preço (`RF-07-37`,
`RN-07-26`, `RN-07-30`). A entrega é **uma operação só**, sem reserva de item entre encontros
(`RN-07-27`), em **`POST /aulas/{id}/trocas`**, restrita ao Mestre vinculado à comunidade da
aula, com histórico em **`GET /trocas`**, filtrado por persona. Quatro decisões novas: o
encontro que a troca registra é a `Aula` do PRD-01, sem verificação de estado nem presença; a
rota nasce sob `/aulas/{id}/trocas`; o débito emitido pela troca **não declara aula** — só o da
baixa de reserva declara —; e a troca exige que o Guerreiro(a) seja da comunidade do item.

O documento 09 mantém a pendência de **quem desativa um ponto de apoio**. **Empréstimo de
bancada e reposição solidária saíram do escopo** — o documento 05 já os adiava, e o PRD
divergia da fonte. No Ciclo 01 ficam o tombamento, a ficha de vida e a conferência de
inventário. Seguem para as próximas fatias o **patrimônio** e o **desafio extra** — este
último ainda sem a entidade `DesafioExtra`, que nasce em PRD-09 ou PRD-14.

O PRD-08 volta a **implementado**: a change `lista-publica-de-comunidades` entregou o
`GET /comunidades` com os quatro indicadores do documento 02 §1 (`RF-08-30`, `RF-08-31`),
última fatia do PRD-08. A pendência que a travava foi decidida — comunidade abaixo do piso sai
na lista sem os indicadores —, e com ela veio o cálculo dos quatro indicadores, que estava
apenas nomeado. A entrega do conjunto abaixo do bairro segue fora do escopo — corre fora da
plataforma no Ciclo 01.

A coluna **Onda** é a ordem em que os PRDs foram **escritos**, e o motivo de cada onda está
no documento 08. Ela não é a ordem em que o código entra: essa está no documento 99 §9.

O **PRD-06 — Assistente por voz e Modo Ouvinte** foi extinto: o App 02 passou a fazer parte do
App 01 e o Modo Ouvinte saiu do produto. O que restou dele está no PRD-04.
