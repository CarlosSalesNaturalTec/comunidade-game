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
| [PRD-07](prd-07-economia-e-ledger.md)     | Economia de recursos e ledger          | —         | 1    | implementado |
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

O PRD-07 vai a **implementado**. A primeira fatia entregou, além do `PontoDeApoio`, o
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

A nona fatia entregou o **patrimônio** — o `ItemPatrimonial` tombado por Admin num ponto de
apoio, com **aporte de origem opcional** que, quando declarado, precisa ser de tipo **durável**
e não pode exceder a quantidade aportada (`RF-07-11`, `RN-07-07`). O **número de tombo** é
digitado por quem tomba, nunca gerado pelo núcleo, e **único por ponto de apoio**; o
**responsável não é campo do item** — deriva do responsável designado no `PontoDeApoio`, o que
corrige o PRD-07 §8. A **ficha de vida**, `AnotacaoDaFichaDeVida`, é histórico somente
inserção, à imagem do `Lancamento`: cada anotação grava o teor — cuidado, perda ou dano — e o
estado de conservação apurado, sem caminho de código para perda ou dano virarem débito
(`RF-07-48`, `RN-07-09`). Decisão nova de fundo: **o saldo de natureza durável fica inerte** —
não é reservável pela aula nem lastreia item do catálogo avulso, e o único destino dele é o
tombamento; duas recusas novas o guardam, no agendamento e no cadastro do item de catálogo
avulso. Em **`POST /itens-patrimoniais`** (Admin), **`GET /itens-patrimoniais`** (gestão,
filtrada por comunidade) e **`POST /itens-patrimoniais/{id}/ficha-de-vida`** (Admin ou Mestre).

A décima fatia entregou a **recompensa de marco e a entrega** — a terceira e última saída de
recurso do livro-razão, e a única que a criança conquista sem pagar nada. O **Mestre autor**
declara, na trilha, qual missão concede qual tipo de recurso e em que quantidade
(`RF-09-71`, `RN-09-26`, `RN-09-39`); só a **missão** é aceita como marco, porque é a única
espécie que o núcleo hoje sabe verificar alcançada. A `RecompensaDeMarco` **não** tem ponto de
apoio nem situação de entrega própria — a trilha é bem comum, e o lastro **deixa de ser exigido
na publicação** (`RF-09-72`, `RN-09-27`, corrige PRD-09). A entrega é confirmada pelo **Mestre
vinculado à comunidade do Guerreiro(a)**, que escolhe o ponto de apoio de onde o recurso sai; o
Admin nunca confirma, o que corrige `RF-02-50` e `RF-02-51` do PRD-02 para **mostrar** a entrega,
não escrevê-la (`RF-07-13`, `RF-09-76`). Cinco recusas protegem a operação, todas antes de
qualquer escrita: tipo de recurso durável, lastro reverificado no ato contra o ponto de apoio da
entrega, quantidade da recompensa esgotada pela contagem de entregas, Mestre não vinculado à
comunidade do Guerreiro(a), e marco não alcançado — conferido contra o percurso que a capacidade
de pontos, níveis e badges já deriva, sem duplicar a consulta (`RN-07-07`, `RN-09-26`,
invariante 9). A entrega grava a `EntregaDeRecompensa` e emite o débito **numa operação só**,
**sem aula** — como o débito da troca —, e nunca toca ponto regular nem extra do Guerreiro(a)
(`RN-07-08`, `RN-07-15`, `RN-07-36`). Em **`POST` e `GET /trilhas/{id}/recompensas-de-marco`**,
**`POST /recompensas-de-marco/{id}/entregas`** e **`GET /entregas`**, filtrado por persona.

Com a recompensa de marco entregue, esgota-se o que resta de essencial e desimpedido, e o
PRD-07 **fecha em dez fatias**. Sobram dois resíduos, e nenhum é fatia deste PRD. A
**conferência de inventário** (`RF-07-20`, desejável) volta ao documento 09 como pendência de
decisão, com os cinco pontos que o requisito não decide; até ela vir, a conferência do Ciclo 01
corre fora da plataforma. O **desafio extra** (`RF-07-15` e `RF-07-39` a `RF-07-41`) espera a
entidade `DesafioExtra`, cujos atributos o PRD-14 §8 define, e entra com a fatia do desafio
extra do PRD-09 ou do PRD-14. O documento 09 mantém ainda a pendência de **quem desativa um
ponto de apoio**, e **empréstimo de bancada e reposição solidária saíram do escopo** — o
documento 05 já os adiava, e o PRD divergia da fonte.

O PRD-08 volta a **implementado**: a change `lista-publica-de-comunidades` entregou o
`GET /comunidades` com os quatro indicadores do documento 02 §1 (`RF-08-30`, `RF-08-31`),
última fatia do PRD-08. A pendência que a travava foi decidida — comunidade abaixo do piso sai
na lista sem os indicadores —, e com ela veio o cálculo dos quatro indicadores, que estava
apenas nomeado. A entrega do conjunto abaixo do bairro segue fora do escopo — corre fora da
plataforma no Ciclo 01.

O PRD-02 recebeu a primeira fatia: a change `esqueleto-da-gestao-e-cadastro-de-comunidade`
abriu a **App 03** — entrada do adulto por login social, sessão em `sessionStorage` e o
**cadastro de Comunidade Virtual de ponta a ponta** (`RF-02-11`, `RN-02-04`). É também a
primeira pasta de frontend do repositório: nasceram `comum/`, com os tokens de design do
documento 15 §12, e a esteira de CI das pastas de JavaScript. O núcleo passou a responder a
**qualquer origem, sem cookie credenciado**, para que um frontend em endereço próprio o alcance
(documento 03 §1, princípio 2). Os demais cadastros do PRD-02 §6.1, as filas de avaliação, o
painel do dia, o Quiz ao Vivo e a publicação em endereço próprio seguem pendentes.

A **identidade da persona** foi decidida em 2026-08-21, antes de virar código: o cadastro do
adulto e a forma do artefato comprobatório estão no documento 02 §1, as cinco linhas no
documento 09, e o PRD-01 §8 ganhou a linha da `Persona`. O `RF-02-01` perdeu a **situação**,
que nenhum documento-fonte definia, e o `RF-02-02` e o `RF-02-03` passam de artefato **anexado**
a **link declarado**. Os atributos entram no núcleo com a fatia de cadastro de personas da
App 03, que atende `RF-02-01` a `RF-02-07`.

O **nick de adulto** foi decidido em 2026-08-21, fechando a pendência "Conferência do nick no
pré-cadastro" do documento 09: nick e avatar passam a ser atributos opcionais de Apoiador **e
Mestre**, a unicidade global do nick alcança os três papéis que o têm, e a conferência de
disponibilidade que a porta pública usa varre **só nicks de adulto** — nunca o de Guerreiro(a),
o oráculo que a pendência vedava. `RN-01-30` e o modelo do PRD-01 §8 já refletem a decisão; o
documento 02 §1, o documento 11 §8.2 e o documento 09 também. `RF-14-12`, `RF-14-13` e o `RF-09-66`
do Mestre a aplicam. O caminho de código entra em três changes: a primeira, `nick-de-adulto`,
entrega o núcleo; `cadastro-de-personas` expõe as rotas de cadastro de cada papel e o caminho
em que o Admin grava o nick quando a escolha do adulto colidiu; `desativacao-do-ponto-de-apoio`
fecha, à parte, a pendência "Desativação de ponto de apoio" do mesmo documento 09.

A coluna **Onda** é a ordem em que os PRDs foram **escritos**, e o motivo de cada onda está
no documento 08. Ela não é a ordem em que o código entra: essa está no documento 99 §9.

O **PRD-06 — Assistente por voz e Modo Ouvinte** foi extinto: o App 02 passou a fazer parte do
App 01 e o Modo Ouvinte saiu do produto. O que restou dele está no PRD-04.
