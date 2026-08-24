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
do PRD-01. Antes disso, a change `auditoria-e-estorno-da-coleta` entregou a primeira das duas
causas de débito do `RF-01-57` — o estorno de registro de coleta invalidado (`RF-01-69`,
`RF-01-70`, `RN-01-55`) — e a queda da credencial de dispositivo ao **encerramento da série**
(`RF-01-68`). A segunda causa, a ocorrência de conduta lançada, fechou só na quarta fatia do
PRD-09.

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

A pendência de **quem desativa um ponto de apoio** foi fechada depois, fora das dez fatias: a
change `desativacao-do-ponto-de-apoio` deu ao Admin as operações de **desativar e reativar**,
sempre com motivo, bloqueadas por **aula futura** — a recusa diz quantas — e por **saldo
remanescente**, que sai por **transferência** entre pontos de apoio, gravada como par de
débito e crédito, nunca como ajuste (`RF-07-47`, `RF-07-19`). O agendamento de aula passa a
recusar ponto de apoio inativo, sem que aula já agendada perca o vínculo com ele, e a App 03
ganhou as três telas — desativar, reativar e transferir saldo.

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

O PRD-02 recebeu a segunda fatia: a change `cadastro-de-personas` expôs as quatro rotas de
cadastro de persona — `POST /v1/guerreiros`, `/v1/mestres`, `/v1/apoiadores`, `/v1/admins` —, a
edição do Guerreiro(a), o artefato comprobatório obrigatório de Mestre e Apoiador (`RF-02-04`) e
o caminho pelo qual o Admin grava o nick do adulto quando a escolha dele colidiu, atendendo
`RF-02-01` a `RF-02-07`. As telas de cadastro, o vínculo do responsável e a credencial
provisória entraram na App 03. As filas de avaliação, o painel do dia, o Quiz ao Vivo e a
publicação em endereço próprio seguem pendentes — o PRD-02 continua **aprovado**.

O PRD-02 recebeu a terceira fatia: a change `avaliacao-da-participacao-e-do-pre-cadastro`
abriu a fila de avaliação — leitura e desfecho da solicitação de participação, restritos a
Admin, com o atraso derivado do prazo de 7 dias (`RF-02-18`, `RF-02-19`, `RF-02-65`). A App
03 ganhou a área **Filas**, com filtro por natureza — participação, ainda a única naquele
momento. Aceitar abre o cadastro pré-preenchido de Mestre ou Apoiador, sem criar acesso; a
homologação do aporte declarado entrou na mesma tela, sobre `POST /aportes` já existente
(`RF-02-20`, `RF-02-84`). `GET /tipos-de-recurso` entrou fora do previsto na proposal, para o
seletor da homologação. O painel do dia, o Quiz ao Vivo, os lançamentos e as outras três
naturezas da fila seguiam pendentes.

O PRD-02 recebeu a quarta fatia: a change `avaliacao-de-dados-de-chave-e-de-sugestao` fechou
as três naturezas que faltavam na área Filas — dados, chave e sugestão —, cada uma com
leitura paginada e desfecho de Admin (`RF-02-77`, `RF-02-78`, `RF-02-87`, `RF-02-88`,
`RF-02-25`, `RF-02-26`). O desfecho da solicitação de chave destravou a emissão de
`POST /chaves`, inalcançável até aqui; a sugestão adotada credita 20 pontos extras e o
badge de protagonismo na mesma operação (`RF-01-56`). A App 03 ganhou o **painel das
chaves emitidas**, ao lado das Filas, com prazo, URL apresentada e revogação com motivo
(`RF-02-90` a `RF-02-92`). O PRD-02 §9 recebeu a rota de desfecho da chave que faltava, e
o `RF-02-93` duplicado foi corrigido — a amostra semanal de coleta passa a `RF-02-98` —,
decisões do fundador em 2026-08-22. As filas fecham o PRD-02 §6.2; o painel do dia, o Quiz
ao Vivo e os lançamentos seguem pendentes — o PRD-02 continua **aprovado**.

O PRD-02 recebeu a quinta fatia: a change `catalogo-de-poderes-e-tela-da-gestao` abriu a
porta HTTP do catálogo de poderes — `POST /poderes`, `GET /poderes`, `PUT /poderes/{id}` e
`POST /poderes/{id}/desativacao` —, fechando o PRD-02 §6.1 (`RF-02-10`, `RF-01-62`,
`RN-01-43`, `RN-01-54`). A alteração nunca alcança natureza nem papel, e a desativação retira
o poder da escolha de novas trilhas sem desfazer o vínculo das trilhas já criadas. A App 03
ganhou a área **Poderes**, ao lado de Comunidades, com cadastro, edição e desativação — o
caminho que destrava a autoria de trilha do PRD-09 e o crédito da coleta do território
(`RN-08-15`). O painel do dia, o Quiz ao Vivo e os lançamentos seguem pendentes — o PRD-02
continua **aprovado**.

A **identidade da persona** foi decidida em 2026-08-21, antes de virar código: o cadastro do
adulto e a forma do artefato comprobatório estão no documento 02 §1, as cinco linhas no
documento 09, e o PRD-01 §8 ganhou a linha da `Persona`. O `RF-02-01` perdeu a **situação**,
que nenhum documento-fonte definia, e o `RF-02-02` e o `RF-02-03` passam de artefato **anexado**
a **link declarado**. Os atributos entraram no núcleo com a fatia de cadastro de personas da
App 03, que atende `RF-02-01` a `RF-02-07`.

O **nick de adulto** foi decidido em 2026-08-21, fechando a pendência "Conferência do nick no
pré-cadastro" do documento 09: nick e avatar passam a ser atributos opcionais de Apoiador **e
Mestre**, a unicidade global do nick alcança os três papéis que o têm, e a conferência de
disponibilidade que a porta pública usa varre **só nicks de adulto** — nunca o de Guerreiro(a),
o oráculo que a pendência vedava. `RN-01-30` e o modelo do PRD-01 §8 já refletem a decisão; o
documento 02 §1, o documento 11 §8.2 e o documento 09 também. `RF-14-12`, `RF-14-13` e o `RF-09-66`
do Mestre a aplicam. O caminho de código entrou em duas changes: `nick-de-adulto` entregou o
núcleo; `cadastro-de-personas` expôs as rotas de cadastro de cada papel e o caminho em que o
Admin grava o nick quando a escolha do adulto colidiu.

O PRD-09 recebeu a primeira fatia: a change `esqueleto-da-area-do-mestre-e-autoria-da-trilha`
abriu a porta HTTP da autoria — `POST /trilhas`, `GET /trilhas/minhas`,
`POST /trilhas/{id}/missoes`, `POST /missoes/{id}/atividades` e `POST /missoes/{id}/retomada` —,
reexpondo `trilhas/regra.py` sem reescrever nenhuma recusa (`RF-09-01` a `RF-09-04`,
`RF-09-69`, `RF-09-70`, `RF-09-80`, `RF-09-81`, `RF-09-83`, `RF-09-101`). Destrava, sem
tocá-las, três rotas órfãs de fatias anteriores do PRD-07 e do PRD-01: `POST
/desafios-de-coleta`, `POST /trilhas/{id}/recompensas-de-marco` e `POST /aulas/{id}/lancamentos`.
A `Missao` ganhou **título**, **etapa do ciclo** e **cadência de retomada**; a `Atividade`
ganhou **título** e **descrição** (PRD-09 §8). Nasceu a **App 09** — a segunda aplicação do
repositório —, com a entrada do Mestre por login social e a autoria de trilha, missão e
atividade de ponta a ponta; a fatia também subiu para `comum/` o cliente do núcleo e a sessão
do adulto, até então só dentro da App 03, para servir as duas. Publicação e travas, culminância,
template de missão, conteúdo e bibliografia, banco do Quiz, minhas turmas e lançamentos seguem
pendentes — o PRD-09 continua **aprovado**.

A segunda fatia, `culminancia-e-publicacao-da-trilha`, tirou a trilha do rascunho perpétuo:
nasceu o módulo `culminancias` (`RF-09-29`, `RF-09-30`) e `SituacaoDaTrilha` ganhou o terceiro
valor, `despublicada` — decisão do fundador em 2026-08-22 que fecha o `RF-09-11` e confirma o
PRD-09 §8. `POST /trilhas/{id}/publicacao` confere as três travas juntas e recusa nomeando
todas as pendentes de uma vez (`RF-09-05` a `RF-09-08`, `RF-09-82`); a mesma rota republica a
trilha despublicada, sempre pelo Mestre autor, sem aprovação de Admin. `POST
/trilhas/{id}/despublicacao` é privativa do Admin, sempre com motivo, que o Mestre autor lê em
`GET /trilhas/minhas`; `GET /trilhas/{id}` passa a servir, em leitura pública, a trilha
publicada, com a licença CC BY-SA e o crédito ao Mestre autor (`RF-09-09`, `RF-09-10`). A
App 09 ganhou a tela da culminância e a ação de publicar. Etiqueta ODS, edição de trilha
publicada, duplicar trilha, desafio de desbloqueio e validação da criação original seguem
pendentes — o PRD-09 continua **aprovado**.

A terceira fatia, `etiqueta-ods-da-trilha-e-da-missao`, fechou o PRD-09 §6.1 abrindo a porta
HTTP do módulo `ods` — regra inteira e testada desde a change `apoio-escolar-e-etiqueta-ods`,
sem rota alguma até aqui. `POST /trilhas/{id}/ods` e `POST /missoes/{id}/ods` recebem a
**lista completa** de etiquetas do alvo e **substituem** o conjunto que havia, numa operação
idempotente que recusa por inteiro quando qualquer objetivo da lista é inválido — o conjunto
anterior fica intacto (`RF-09-92`, `RF-09-98`). Lista vazia deixa o alvo sem etiqueta, legal no
Ciclo 01 (`RF-09-93`), e a substituição é **escopada ao alvo**: a da trilha nunca alcança as
etiquetas das missões dela, o que preserva a precedência do `RF-01-45`. Apagar não deixa ponta
solta porque nada guarda chave estrangeira para a etiqueta — o desafio de coleta a resolve por
derivação a cada leitura, e a fatia trava em teste o que a spec já previa: trocar a etiqueta da
missão troca a do desafio, sem reprocessar pontuação (`RF-08-25`, `RN-08-21`). A declaração
passa a exigir **autoria estrita** do Mestre autor, e o Admin recebe 403: não é decisão nova, é
o código alcançando o documento 11, que sempre disse que quem declara é o Mestre autor. As
saídas de trilha e de missão passam a devolver as etiquetas declaradas e a **cobertura de ODS
da trilha**, com o rótulo do ciclo (`RF-09-94`, `RN-01-24`), e a App 09 ganhou a tela de ODS
dentro da trilha e dentro da missão. Destrava a base de `GET /vitrine/ods/cobertura`, que
estava no ar sobre tabela que ninguém podia alimentar. A trava de publicação sem etiqueta é do
Ciclo 02 por texto do `RF-09-96`. Template de missão, conteúdo e bibliografia, banco do Quiz,
minhas turmas e lançamentos, edição de trilha publicada, duplicar trilha, desafio de
desbloqueio e validação da criação original seguem pendentes — o PRD-09 continua **aprovado**.

A quarta fatia, `minhas-turmas-e-lancamentos-do-mestre`, liga a operação que a autoria vinha sem
porta. `GET /minhas-turmas` lê as aulas das comunidades do Mestre em sessão e as atividades de
que é autor, separadas por formato — presencial do encontro e on-line entre encontros
(`RF-09-42`, `RF-09-73`). `POST /atividades/{id}/lancamentos` abre
`resultados.regra.registrar_resultado` ao Mestre autor, com a lista de participantes numa
operação só, sem consumir reserva nem mudar a situação da aula — distinto do lançamento por
aula, do Admin, que permanece inalterado (`RF-09-43`, `RF-09-44`, `RF-09-49`, `RF-09-74`).
`POST /aulas/{id}/presencas` abre `registrar_presenca` ao Mestre só no modo confirmação, pela
operação `confirmacao_de_identidade_do_guerreiro` que a matriz já lhe concedia (`RF-09-45`).
Nasce o módulo `ocorrencias_de_conduta` — entidade somente inserção, com o motivo anulável para
o expurgo futuro —, que fecha a segunda causa do `RF-01-57`: debita 5 pontos regulares por
ocorrência, com teto de 10 por Guerreiro(a) e por aula, sem que quem lança arbitre o valor
(`RF-09-46`, `RN-01-55`). A App 09 ganhou a área **Minhas turmas** — lista, lançamento,
confirmação de presença e ocorrência de conduta. Fica pendente, e volta ao documento 09, o
gatilho do fim de ciclo, do qual dependem o expurgo do motivo (`RN-01-52`) e a saída da
ocorrência do ranking público. Template de missão, conteúdo e bibliografia, banco do Quiz,
edição de trilha publicada, duplicar trilha, desafio de desbloqueio e validação da criação
original seguem pendentes — o PRD-09 continua **aprovado**.

A quinta fatia, `banco-do-quiz-ao-vivo`, abre a porta do banco de perguntas do módulo `quiz`,
escrito e testado desde a change `quiz-ao-vivo` sem uma única rota. `PerguntaDeQuiz` ganha
`missao_id` e `trilha_id` — a trilha derivada da missão e persistida, nunca declarada pelo
cliente —, e `cadastrar_pergunta` passa a exigir o vínculo (`RF-09-39`). `POST /v1/perguntas`
abre o cadastro ao Mestre e ao Admin, sem tocar nas recusas de alternativa que já existiam
(`RF-09-36`, `RF-09-37`); `GET /v1/perguntas/minhas` lê o banco do próprio Mestre, filtrável
por trilha e por missão (`RF-09-40`). A App 09 ganhou a área **Banco do Quiz** — cadastro com
as quatro alternativas e a correta, e lista filtrável por trilha e missão. Decisão do fundador,
2026-08-23: a `PerguntaDeQuiz` não tem situação — nasce disponível e assim permanece, e a
anulação segue sendo da partida, nunca dela (documento 09). Fica pendente o `RF-09-41`: o banco
cadastrado só fica disponível para a partida quando a condução, na App 03, tiver porta — o que
depende da formação de equipe da App 01. Template de missão, conteúdo e bibliografia, edição de
trilha publicada, duplicar trilha, desafio de desbloqueio e validação da criação original
seguem pendentes — o PRD-09 continua **aprovado**.

O PRD-04 recebeu a primeira fatia: a change `esqueleto-da-aula-presencial-e-equipe-da-aula`
abriu a **App 01** — a sessão de trabalho do aparelho, aberta por Mestre ou Admin e amarrada à
janela da aula agendada, sem aula não abre e mais de uma pergunta uma única vez (`RF-04-02`,
`RF-04-03`, `RF-04-05`), a tela inicial com os dois caminhos e a **formação da equipe da aula**
— criar, entrar com o papel declarado e sair, sem aprovação de terceiro (`RF-04-30` a
`RF-04-34`, `RF-04-59`). É a terceira aplicação do repositório. `equipes/regra.py`, escrito e
testado desde a change `aula-presenca-e-equipe`, ganhou a porta HTTP que faltava — destrava,
sem tocá-la, a fila de validação da criação original do Mestre (PRD-09 §6.4) e o `RF-09-41`,
que dependia de haver quem formasse equipe.

Sem câmera nesta fatia — a entrada do Guerreiro(a) é por confirmação de Mestre ou Admin, o
caminho que o `RF-04-15` já previa para quem não tem _template_. Implementá-la revelou que a
rota de confirmação exigia um identificador de persona sem rota alguma capaz de resolvê-lo a
partir do nick, e que criar essa rota, mesmo restrita a Mestre ou Admin, violaria o invariante
de `persona-e-credencial` que veda o oráculo de nick de Guerreiro(a) por quem quer que pergunte
— corrigido recebendo o nick e resolvendo-o internamente, com recusa indistinguível entre nick
inexistente e nick de outro papel. A conferência de disponibilidade de nick do onboarding, que
o PRD-04 §9 declarava pública, e a confirmação humana, que ele não detalhava, foram corrigidas
ao mesmo invariante — a versão do PRD é anterior à decisão de `nick-de-adulto` (documento 09,
2026-08-21). A matriz do PRD-01 §4 ganhou a operação que falta para o Mestre autenticar o
autocadastro do Guerreiro(a) pela sessão de trabalho, texto que o PRD-04 §9 já previa; o código
entra na fatia do onboarding, junto da câmera, do consentimento e da fila local sem rede, que
seguem pendentes.

A segunda fatia, `cadastro-do-guerreiro-no-encontro`, entregou o **caminho do onboarding**: a
jornada 5.3, a criança que chega sem o responsável. `POST /v1/guerreiros` passou a atender dois
caminhos pela **aplicação declarada na chave** — App 01 leva ao autocadastro do encontro, sem
autor; qualquer outra, ao caminho da gestão, de Admin. O cadastro nasce ativo, sem imagem, e a
**presença do dia é gravada na mesma transação** (`RF-04-15`, `RF-04-17`). Decisão do fundador,
2026-08-24: a **faixa de 6 a 16 anos** passa a ser exigida na regra do núcleo, retroativa ao
caminho da gestão — requisito de tela não protege invariante de plataforma. Segunda decisão do
mesmo dia: nenhuma rota de consulta ganha alcance total sobre nick de Guerreiro(a); a recusa de
**gravação** do cadastro do encontro é quem devolve as variações, o que tira `GET
/v1/guerreiros/nick/disponivel` da lista de rotas do PRD-04 §9. Terceira decisão: a **App 01
passa a cadastrar o responsável mínimo** no ato do encontro, sem o que a primeira turma inteira
cairia na jornada 5.3 por acidente de implementação — o código dela é da fatia seguinte, junto
do consentimento e da câmera, que seguem pendentes.

A coluna **Onda** é a ordem em que os PRDs foram **escritos**, e o motivo de cada onda está
no documento 08. Ela não é a ordem em que o código entra: essa está no documento 99 §9.

O **PRD-06 — Assistente por voz e Modo Ouvinte** foi extinto: o App 02 passou a fazer parte do
App 01 e o Modo Ouvinte saiu do produto. O que restou dele está no PRD-04.
