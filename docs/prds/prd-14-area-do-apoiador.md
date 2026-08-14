# PRD-14 — App 08: Área do Apoiador

## 1. Identificação

| Campo            | Valor                                          |
| ---------------- | ---------------------------------------------- |
| PRD              | PRD-14                                         |
| Aplicação        | App 08 — Área do Apoiador                      |
| Onda             | 5                                              |
| Situação         | aprovado                                       |
| Versão e data    | v2 — 2026-08-07                                |
| Depende de       | PRD-07, PRD-02                                 |
| Documentos-fonte | 02 §1, 03 §§1.1, 10, 04 §§1–3, 11 §8.2, 12, 14 |

## 2. Contexto e objetivo

A App 08 é o **canal próprio de quem sustenta o projeto**. Hoje o apoio existe como lançamento
feito por terceiros: um Admin registra o aporte e o Apoiador não tem onde ver o que aconteceu
com ele. Esta aplicação inverte isso — o Apoiador entra, declara o que vai aportar, acompanha
o que o apoio custeou, propõe desafios extras e vê o que os Guerreiros e Guerreiras fizeram
por causa deles.

Ela tem **duas camadas**: uma **porta pública de pré-cadastro**, que é para onde a vitrine
encaminha quem chega querendo apoiar, e a **área autenticada** de quem já foi cadastrado por
um Admin. A porta grava solicitação, aporte declarado e comprovante; ela **não cadastra
ninguém** — quem valida o comprovante e cadastra continua sendo o Admin, na App 03.

É aqui que vive a camada de jogo do adulto que sustenta o projeto (documento 14): a necessidade
publicada vira **missão**, a missão concluída rende **moeda e selo**, e a coleção de selos
compõe o **nível de sustento**, que sobe por frentes diferentes cobertas e nunca por volume de
dinheiro. **O Apoiador não pontua** — ponto é do Guerreiro(a).

No Ciclo 01 a aplicação sustenta a hipótese **H3** — se mestres e apoiadores suprem os recursos
do MVP — de dois lados: publica a necessidade em aberto para quem pode cobri-la e registra o
que foi coberto. É também onde vive a salvaguarda mais dura do projeto: **nenhum contato direto
entre Apoiador e Guerreiro(a)**. Tudo o que o Apoiador enxerga da criança é avatar, nick e o
que já é público.

## 3. Escopo

### 3.1 Dentro do escopo

- **Pré-cadastro público**, com identificação sem documento, **perfil pessoa física ou
  jurídica**, aporte declarado e comprovante anexado.
- **Acesso do Apoiador cadastrado**, por login social ou credencial de usuário e senha
  provisória.
- **Missões do Apoiador**: lista das missões abertas, derivadas das necessidades de recurso
  publicadas, com o caminho de cobrir uma delas — inteira ou em parte.
- **Nível de sustento e selos**, derivados das missões concluídas e exibidos na aplicação e no
  card público.
- **Identidade pública**: nick único e avatar — logomarca ou imagem escolhida a partir de
  **10 moedas acumuladas**, avatar padrão do projeto abaixo desse piso.
- **Meus aportes**: histórico em moedas e Poder Sustentador acumulado, lidos do ledger do PRD-07.
- **Novo aporte em dinheiro** de quem já é cadastrado, a partir de uma missão, de uma
  necessidade publicada ou por valor sugerido ou livre, sempre com comprovante. O valor
  sugerido vem da **escada do perfil declarado**.
- **Necessidades de recurso em aberto**, publicadas pelas atividades sem lastro, com o caminho
  direto para cobri-las.
- **Proposição de desafios extras**, abertos ou direcionados, com acompanhamento do fluxo de
  validação do Mestre e aprovação do Admin.
- **Efetividade do apoio** em painel vivo, agregado e por avatar, com a cobertura de ODS
  herdada das missões.
- **Acompanhamento** dos mesmos dados do painel público, com **favoritos** de Guerreiros,
  Guerreiras e Mestres e as novidades deles em destaque.
- **Envio de documentos comprobatórios** para o Admin anexar ao cadastro.
- **Registro de propostas** de evolução da plataforma, na fila única da gestão.
- **Aviso de coleta de dados** em toda tela que coleta, com acesso à área detalhada.

### 3.2 Fora do escopo

- **Autocadastro do Apoiador**: o cadastro é ato exclusivo de Admin (PRD-02).
- **Homologação do próprio aporte** e qualquer edição do ledger — é da App 03.
- **Aporte em material, serviço ou divulgação pela aplicação**: entra pelo cadastro do Admin,
  com termo de doação ou registro do material, porque depende da tabela de valoração.
- **Mais de um usuário no mesmo cadastro**: no Ciclo 01 o cadastro institucional tem um
  usuário; delegação fica para ciclo futuro.
- **Ressarcimento**: existe só para o aporte por absorção de Mestre ou Admin (PRD-07).
- **Qualquer canal de mensagem** com Guerreiro(a), família ou Mestre.
- **Acesso à App 07**, mesmo quando o Apoiador é parente da criança.
- **Relatório fechado de prestação de contas**: no Ciclo 01 o retorno é o painel vivo.
- **Catálogo de missões instanciado para o Ciclo 01**: quantidade, prazo e selo de cada missão
  dependem do catálogo de recompensas por marco e da tabela de valoração, ambos pendentes. A
  aplicação exibe as missões que a gestão publicar; não as define.
- **Recebimento do apoio em código**: a contribuição entra pelo repositório, com CLA assinado e
  _pull request_ integrado, e é homologada pelo Admin na App 03. Aqui o Apoiador vê as moedas,
  o selo e o nível que ela rendeu, como qualquer aporte.
- **Ranking de apoiadores por valor**: vedado pelo documento 14. Há coleção de selos e nível de
  sustento, nunca pódio.
- **Publicidade e patrocínio**: fora do Ciclo 01 (documento 09).
- **Notificação por e-mail**: não existe no Ciclo 01; todo retorno acontece na plataforma.
- **Recibo fiscal e dado bancário**: a plataforma não coleta CPF, CNPJ nem documento, e não
  armazena dado bancário. Quem quiser recibo escreve para a pessoa jurídica vinculada, que o
  emite fora da plataforma — e a tela de pré-cadastro diz isso.

## 4. Personas e permissões

| Persona      | O que faz nesta aplicação                                                                                                                      | O que não pode fazer                                                        |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Apoiador     | Cobre missões, declara aporte, define identidade, propõe desafios, acompanha nível de sustento, selos e efetividade, e favorita                | Homologar aporte, editar ledger, ver dado de contato ou identificar criança |
| Visitante    | Preenche o pré-cadastro na porta pública e vê as missões abertas                                                                               | Entrar na área autenticada; obter cadastro pelo envio                       |
| Admin        | Nada aqui: valida o comprovante, cadastra e anexa documentos pela App 03. **É a homologação dele que conclui a missão** e credita nível e selo | Usar esta aplicação como via de cadastro                                    |
| Mestre       | Nada aqui: valida o desafio extra pela App 09                                                                                                  | Propor desafio extra em nome de Apoiador                                    |
| Guerreiro(a) | Nada: a sua jornada é a App 05                                                                                                                 | Entrar; ser contatado por Apoiador                                          |
| Responsável  | Nada: o canal da família é a App 07                                                                                                            | Entrar com a credencial de Apoiador de um parente                           |

O Apoiador institucional opera com **um usuário**, indicado pela instituição. É esse usuário
que responde pelos atos registrados no cadastro.

## 5. Jornadas principais

### 5.1 Pré-cadastro pela porta pública

1. A pessoa chega pela vitrine — pelo botão "Entrar", pela chamada "Quero participar" ou pelo
   pedido de favoritar, que ali não existe.
2. A tela se apresenta, diz o que é a Área do Apoiador e abre o pré-cadastro.
3. Ela se identifica **sem documento**: nome ou razão social, e-mail e WhatsApp, e declara o
   **perfil** — pessoa física ou jurídica. O perfil não é verificado: define a escada que a
   tela exibe e o recorte do painel de efetividade, nada além.
4. Escolhe o que vai aportar: uma **missão aberta**, uma **necessidade publicada**, um **valor
   sugerido** da escada do seu perfil ou um **valor livre**. Cada valor aparece com o
   **equivalente em moedas** ao lado, e o valor livre aceita qualquer quantia.
5. Transfere pela chave PIX e **anexa o comprovante** em PDF, JPG ou PNG.
6. A tela diz, antes do envio, que aquilo **não cria cadastro nem acesso** e que um Admin vai
   conferir o comprovante.
7. O pedido entra na fila da App 03. Repetições da mesma origem sofrem **atraso progressivo**.
8. Quem quer apoiar **sem transferir dinheiro** — material, serviço ou divulgação — é
   encaminhado ao formulário de solicitação de participação da vitrine.

### 5.2 Primeiro acesso e identidade pública

1. Aprovado o cadastro pelo Admin, o Apoiador entra por **login social** ou pela **credencial
   de usuário e senha provisória** criada pela gestão.
2. Tendo senha provisória, a **troca é obrigatória** antes de qualquer outra tela.
3. Login de conta sem cadastro prévio é **recusado**, com a orientação de usar o pré-cadastro —
   login não cria cadastro.
4. Na primeira entrada ele define o **nick**, recusado se já estiver em uso, com sugestão de
   variações.
5. O **avatar próprio** — logomarca ou outra imagem escolhida — abre a partir de **10 moedas
   acumuladas**. Abaixo do piso, o card usa o **avatar padrão do projeto**, e a tela diz quanto
   falta para trocá-lo, sem cobrar nem insistir.
6. Homologado o aporte, o **card vai à vitrine** com avatar, nick e total de moedas em
   destaque, na moldura comum a todos os apoiadores, mais o **nível de sustento** e os
   **selos** já conquistados.
7. Avatar e nick ficam sujeitos à **auditoria por amostragem** da gestão, que pode despublicar
   com motivo.

### 5.3 Aportar de novo

1. O Apoiador cadastrado abre **Necessidades em aberto** e vê o que falta de recurso nas
   atividades previstas, com a comunidade e o valor em moedas.
2. Escolhe cobrir uma necessidade, ou declara um **valor sugerido** da escada do seu perfil ou
   um **valor livre**.
3. Transfere pela chave PIX e anexa o comprovante.
4. O aporte nasce **pendente de homologação**: não credita moeda, não compõe o Poder Sustentador
   e não dá lastro a nada.
5. O Admin homologa na App 03. Só então o valor vira moedas, credita o Poder Sustentador e a
   necessidade coberta sai da lista.
6. Recusado, o Apoiador vê o motivo em linguagem simples, dentro da plataforma.
7. Querendo aportar material ou serviço, a tela explica que aquilo entra pelo cadastro do
   Admin, com termo de doação ou registro do material.

### 5.4 Cobrir uma missão

1. O Apoiador abre **Missões** e vê as que estão abertas, agrupadas pelo **nível de
   necessidade** que sustentam: existir, acontecer, reconhecer, permanecer.
2. Cada missão mostra o que se pede, **quanto falta em moedas**, o prazo e o **selo** que
   rende. O que já foi coberto aparece como quantidade, **sem nome de quem cobriu**.
3. Ele escolhe cobrir a missão inteira ou **parte dela**, transfere pela chave PIX e anexa o
   comprovante.
4. O aporte nasce **pendente**, como qualquer outro: não credita moeda, não abate o que falta
   e não conclui missão alguma.
5. Homologado pelo Admin, o valor vira moedas e abate o que falta. **A missão conclui apenas
   quando o saldo fecha.**
6. Coberta em parte, a missão continua aberta com o restante atualizado, e quem aportou recebe
   **as moedas do que deu** — não o selo, que só vem com a conclusão.
7. Fechada por outra pessoa, a missão sai da lista e **cada um que participou recebe o selo de
   mutirão**, cada qual com as suas moedas. Ninguém recebe crédito pelo que outro deu.
8. Concluída a missão, a tela mostra o **selo novo** e, se for o caso, o **nível de sustento**
   alcançado, com a frente que falta para o próximo — uma vez, sem insistir.
9. Missão com prazo vencido sem fechar sai da lista de abertas; os aportes já homologados
   permanecem no livro-razão e as moedas, no Poder Sustentador de quem as deu.

### 5.5 Propor um desafio extra aberto

1. O Apoiador escolhe uma **trilha em andamento** e descreve o desafio.
2. Declara a **recompensa**, a **quantidade disponível**, o critério de atribuição e o
   **período de vigência**.
3. Provê o **lastro da recompensa** — sem ele o desafio não é publicado, e a tela mostra o que
   falta.
4. A proposta segue para **validação pedagógica do Mestre da trilha**.
5. Validada, vai para **aprovação de um Admin**.
6. Publicado, o desafio aparece para todos os Guerreiros e Guerreiras daquela trilha, e o
   Apoiador acompanha a quantidade de recompensas restante.
7. Recusado em qualquer etapa, ele vê o motivo. **Desafio publicado não se edita**: corrigir é
   propor de novo.

### 5.6 Propor um desafio direcionado

1. O Apoiador escolhe a modalidade **direcionado** e informa o **nick** que a família lhe cedeu.
2. Registra a **justificativa do vínculo** — parente próximo, padrinho, madrinha, amigo da
   família.
3. A aplicação **não confirma se o nick existe** e **não exibe dado algum** do destinatário: nem
   avatar, nem trilha, nem se ele está ativo.
4. Quem confere o vínculo e a existência do destinatário são o **Mestre da trilha** e o
   **Admin**, na validação e na aprovação.
5. Por isso o direcionado alcança também **quem não tem divulgação autorizada**: a família cedeu
   o nick, e a plataforma nunca o confirmou a ninguém.
6. Nick inexistente ou vínculo não comprovado faz a proposta ser recusada na validação, com o
   motivo genérico — a recusa também não revela se o nick existe.
7. Publicado, o desafio é entregue ao destinatário na App 05, e só ele recebe a recompensa.

### 5.7 Acompanhar a efetividade do apoio

1. O painel de efetividade abre com os **desafios propostos, publicados e concluídos**.
2. Cada desafio mostra **quantos Guerreiros e Guerreiras concluíram**, em que trilha e em que
   período.
3. Ao lado, as **moedas aportadas** e o que elas custearam.
4. Abaixo, a **cobertura de ODS** herdada das missões a que os desafios se vincularam,
   agregada por comunidade e ciclo.
5. O painel é **vivo**: atualiza a cada conclusão registrada. **Não há relatório fechado nem
   periodicidade no Ciclo 01.**
6. Nenhum número desce ao indivíduo identificado: quem concluiu aparece por **avatar e nick**,
   e só quando tem divulgação autorizada; sem ela, entra apenas na contagem.
7. A exceção é o **destinatário do desafio direcionado**, cujo nick o próprio Apoiador informou:
   ali ele vê se o desafio foi concluído, e **nada além disso** — nem avatar, nem trilha, nem
   evolução.

### 5.8 Acompanhar e favoritar

1. O Apoiador vê **os mesmos dados do painel público** — nada além do que qualquer visitante vê.
2. Para favoritar um Guerreiro(a), informa o **nick exato** que a família lhe cedeu.
3. A busca **não lista, não sugere e não completa** nomes. Nick sem divulgação autorizada
   devolve **a mesma resposta** de nick inexistente.
4. Mestres são favoritados a partir da própria página pública.
5. As **novidades** dos favoritos ficam em destaque por **30 dias**: criação original publicada,
   badge novo, nível novo, resultado de batalha e trilha nova publicada pelo Mestre.
6. Favoritar é **leitura**: não abre canal, não avisa a criança e não dá acesso a nada além do
   público. O destaque só existe **dentro** da aplicação — não há e-mail.
7. O favorito é removido a qualquer tempo, sem deixar rastro para a criança.

### 5.9 Enviar comprobatórios e registrar proposta

1. O Apoiador envia **currículo, portfólio, redes sociais, termos de doação e comprovantes**.
2. O documento entra na fila da App 03; ele **não vai à página pública** enquanto um Admin não o
   anexar ao cadastro.
3. Para propor evolução da plataforma, registra a proposta em texto.
4. Ela entra na **fila única da gestão**, a mesma que recebe as sugestões do Guerreiro(a), do
   responsável e do Mestre.
5. Ele acompanha o status até o retorno, com o motivo em linguagem simples quando não adotada.
6. **Proposta de Apoiador não pontua**: pontos são da criança.

## 6. Requisitos funcionais

### 6.1 Pré-cadastro e acesso

| ID         | Requisito                                                                                                         | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------------------------------- | ---------- |
| `RF-14-01` | Porta pública identifica sem documento: nome ou razão social, e-mail, WhatsApp e perfil pessoa física ou jurídica | essencial  |
| `RF-14-02` | Pré-cadastro oferece as formas de aportar: missão aberta, necessidade publicada, valor sugerido ou livre          | essencial  |
| `RF-14-03` | Cada valor é exibido com o equivalente em moedas na mesma tela, na escada do perfil declarado                     | essencial  |
| `RF-14-04` | Pré-cadastro exige anexo do comprovante em PDF, JPG ou PNG                                                        | essencial  |
| `RF-14-05` | Tela declara, antes do envio, que o pré-cadastro não cria cadastro nem acesso                                     | essencial  |
| `RF-14-06` | Envio da porta pública respeita limite por origem, com atraso progressivo a cada repetição                        | essencial  |
| `RF-14-07` | Porta pública encaminha ao formulário da vitrine quem apoia sem transferir dinheiro                               | essencial  |
| `RF-14-08` | Apoiador cadastrado entra por login social ou por credencial de usuário e senha                                   | essencial  |
| `RF-14-09` | Credencial provisória exige troca de senha antes de qualquer outra tela                                           | essencial  |
| `RF-14-10` | Login de conta sem cadastro prévio é recusado, com orientação de usar o pré-cadastro                              | essencial  |
| `RF-14-11` | Aplicação não oferece convite, delegação nem segundo acesso ao mesmo cadastro                                     | essencial  |

### 6.2 Identidade pública e comprobatórios

| ID         | Requisito                                                                              | Prioridade |
| ---------- | -------------------------------------------------------------------------------------- | ---------- |
| `RF-14-12` | Apoiador define avatar — logomarca ou imagem escolhida — e nick exibidos no card       | essencial  |
| `RF-14-13` | Nick já usado é recusado, com sugestão de variações                                    | essencial  |
| `RF-14-14` | Avatar próprio é liberado a partir de 10 moedas acumuladas em aportes homologados      | essencial  |
| `RF-14-15` | Abaixo do piso o card exibe o avatar padrão do projeto, com o nick e o total de moedas | essencial  |
| `RF-14-16` | Aplicação mostra quantas moedas faltam para liberar o avatar próprio                   | essencial  |
| `RF-14-17` | Apoiador altera avatar e nick a qualquer tempo, com reflexo na vitrine                 | desejável  |
| `RF-14-18` | Apoiador envia currículo, portfólio, redes sociais, termos de doação e comprovantes    | essencial  |
| `RF-14-19` | Documento enviado entra na fila da App 03 e só é publicado quando um Admin o anexa     | essencial  |
| `RF-14-20` | Aplicação exibe ao Apoiador o que já está publicado na sua página da vitrine           | desejável  |

### 6.3 Aportes e necessidades

| ID         | Requisito                                                                                              | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------------------ | ---------- |
| `RF-14-21` | "Meus aportes" lista os aportes homologados em moedas, com data, tipo e destino                        | essencial  |
| `RF-14-22` | Poder Sustentador é exibido como total acumulado em moedas                                             | essencial  |
| `RF-14-23` | Nenhuma tela exibe reais, salvo aquela em que se declara a transferência, sempre com moedas            | essencial  |
| `RF-14-24` | Necessidades em aberto são listadas com atividade, comunidade e o que falta em moedas                  | essencial  |
| `RF-14-25` | Apoiador declara novo aporte a partir de uma missão, de uma necessidade ou por valor sugerido ou livre | essencial  |
| `RF-14-26` | Aporte declarado exige comprovante e entra pendente, sem creditar moeda nem abater o que falta         | essencial  |
| `RF-14-27` | Apoiador acompanha a situação do aporte: pendente, homologado ou recusado com motivo                   | essencial  |
| `RF-14-28` | Aplicação não aceita aporte em material, serviço ou divulgação, e orienta procurar a gestão            | essencial  |

### 6.4 Desafios extras

| ID         | Requisito                                                                                   | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------- | ---------- |
| `RF-14-29` | Apoiador propõe desafio extra vinculado a uma trilha em andamento                           | essencial  |
| `RF-14-30` | Proposta declara recompensa, quantidade disponível, critério de atribuição e vigência       | essencial  |
| `RF-14-31` | Proposta declara a modalidade: aberto ou direcionado                                        | essencial  |
| `RF-14-32` | Direcionado exige o nick do destinatário e a justificativa do vínculo                       | essencial  |
| `RF-14-33` | Aplicação não confirma se o nick do direcionado existe nem exibe dado do destinatário       | essencial  |
| `RF-14-34` | Desafio sem lastro da recompensa não é publicado, e a tela mostra o que falta prover        | essencial  |
| `RF-14-35` | Apoiador acompanha o estado: validação do Mestre, aprovação do Admin, publicado ou recusado | essencial  |
| `RF-14-36` | Recusa em qualquer etapa é exibida com motivo em linguagem simples                          | essencial  |
| `RF-14-37` | Desafio publicado exibe a quantidade de recompensas restante                                | essencial  |
| `RF-14-38` | Desafio publicado não é editável; a correção é proposta nova                                | essencial  |
| `RF-14-39` | Nenhuma tela de desafio expõe nome real, contato ou dado de identificação de Guerreiro(a)   | essencial  |
| `RF-14-74` | Proposta de desafio extra declara os pontos extras, e a aplicação recusa valor acima de 10  | essencial  |
| `RF-14-75` | Proposta declara o formato do desafio: presencial ou on-line                                | essencial  |
| `RF-14-76` | Proposta declara o custeio: aporte do Apoiador ou saldo de recurso existente na plataforma  | essencial  |
| `RF-14-77` | Apoiador oferta item para o catálogo avulso, com nome, tipo de recurso, quantidade e lastro | essencial  |
| `RF-14-78` | Item ofertado pelo Apoiador só entra no catálogo após homologação de Admin                  | essencial  |
| `RF-14-79` | Apoiador não define o preço do item que oferta; ele vem da tabela de referência da gestão   | essencial  |
| `RF-14-80` | Apoiador acompanha o item ofertado: homologado, ativo, estoque restante e quantas trocas    | essencial  |
| `RF-14-81` | Nenhuma tela de catálogo expõe identificação de quem trocou; o retorno é agregado           | essencial  |

### 6.5 Efetividade do apoio

| ID         | Requisito                                                                            | Prioridade |
| ---------- | ------------------------------------------------------------------------------------ | ---------- |
| `RF-14-40` | Painel de efetividade atualiza a cada conclusão registrada, sem fechamento periódico | essencial  |
| `RF-14-41` | Painel exibe desafios propostos, publicados e concluídos                             | essencial  |
| `RF-14-42` | Painel exibe quantos concluíram cada desafio, em que trilha e em que período         | essencial  |
| `RF-14-43` | Painel exibe as moedas aportadas e o que elas custearam                              | essencial  |
| `RF-14-44` | Painel exibe a cobertura de ODS herdada das missões, agregada por comunidade e ciclo | essencial  |
| `RF-14-45` | Quem concluiu aparece só por avatar e nick, e apenas com divulgação autorizada       | essencial  |
| `RF-14-46` | Sem divulgação autorizada, a conclusão entra apenas na contagem agregada             | essencial  |
| `RF-14-47` | No direcionado, o proponente vê que houve conclusão, e nada além disso               | essencial  |

### 6.6 Acompanhamento e favoritos

| ID         | Requisito                                                                      | Prioridade |
| ---------- | ------------------------------------------------------------------------------ | ---------- |
| `RF-14-48` | Apoiador vê os mesmos dados do painel público, sem recorte adicional           | essencial  |
| `RF-14-49` | Apoiador favorita Guerreiro(a) informando o nick exato cedido pela família     | essencial  |
| `RF-14-50` | Busca por nick não lista, não sugere e não completa nomes                      | essencial  |
| `RF-14-51` | Nick sem divulgação autorizada devolve resposta idêntica à de nick inexistente | essencial  |
| `RF-14-52` | Apoiador favorita Mestre a partir da página pública dele                       | essencial  |
| `RF-14-53` | Novidade de favorito fica em destaque por 30 dias, nos cinco fatos definidos   | essencial  |
| `RF-14-54` | Favoritar não abre canal, não avisa a criança e não amplia o que ele enxerga   | essencial  |
| `RF-14-55` | Apoiador remove favorito a qualquer tempo                                      | essencial  |

### 6.7 Propostas e avisos

| ID         | Requisito                                                                    | Prioridade |
| ---------- | ---------------------------------------------------------------------------- | ---------- |
| `RF-14-56` | Apoiador registra proposta de evolução da plataforma na fila única da gestão | essencial  |
| `RF-14-57` | Apoiador acompanha o status da proposta, com motivo quando não adotada       | essencial  |
| `RF-14-58` | Toda tela que coleta dado traz aviso discreto, com acesso à área detalhada   | essencial  |
| `RF-14-59` | Aplicação não oferece canal de mensagem com Guerreiro(a), família ou Mestre  | essencial  |

### 6.8 Missões, níveis de sustento e selos

| ID         | Requisito                                                                                      | Prioridade |
| ---------- | ---------------------------------------------------------------------------------------------- | ---------- |
| `RF-14-60` | Aplicação lista as missões abertas agrupadas pelo nível de necessidade que sustentam           | essencial  |
| `RF-14-61` | Cada missão exibe o que se pede, quanto falta em moedas, o prazo e o selo que rende            | essencial  |
| `RF-14-62` | Missão exibe o quanto já foi coberto, em quantidade, sem identificar quem cobriu               | essencial  |
| `RF-14-63` | Apoiador cobre a missão inteira ou parte dela, sempre com comprovante                          | essencial  |
| `RF-14-64` | Aporte parcial homologado abate o que falta e mantém a missão aberta com o restante            | essencial  |
| `RF-14-65` | Missão só é concluída quando o saldo fecha, por homologação de Admin                           | essencial  |
| `RF-14-66` | Concluída a missão, cada participante recebe o selo; as moedas são as do que cada um aportou   | essencial  |
| `RF-14-67` | Aplicação exibe o nível de sustento e a frente que falta para o próximo, uma vez, sem insistir | essencial  |
| `RF-14-68` | Aplicação exibe os selos conquistados, agrupados por família                                   | essencial  |
| `RF-14-69` | Nível de sustento e selo conquistados não regridem em nenhuma hipótese                         | essencial  |
| `RF-14-70` | Nenhuma tela ordena, classifica ou compara apoiadores por valor aportado                       | essencial  |
| `RF-14-71` | Aplicação não exibe missão que não tenha necessidade de recurso publicada por trás             | essencial  |
| `RF-14-72` | Missão com prazo vencido sai da lista de abertas, sem estornar aporte já homologado            | essencial  |
| `RF-14-73` | Card e página públicos do Apoiador exibem o nível de sustento e os selos                       | desejável  |

## 7. Regras de negócio

| ID         | Regra                                                                                                                                                         | Invariante (doc 99 §6) | Fonte          |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- | -------------- |
| `RN-14-01` | O Apoiador é cadastrado exclusivamente por Admin; o pré-cadastro é solicitação, não cadastro                                                                  | 3                      | 02 §1          |
| `RN-14-02` | Login não cria cadastro: conta sem cadastro prévio é recusada                                                                                                 | 3                      | 03 §1.1        |
| `RN-14-03` | A identificação do Apoiador não usa documento: sem CPF, CNPJ ou documento de identidade                                                                       | —                      | 02 §1, 03 §10  |
| `RN-14-04` | Um usuário por cadastro no Ciclo 01, inclusive no institucional                                                                                               | —                      | 02 §1          |
| `RN-14-05` | O aporte feito pela aplicação é em dinheiro; material e serviço entram pelo Admin                                                                             | —                      | 02 §1, 03 §10  |
| `RN-14-06` | Comprovante é obrigatório no Ciclo 01; não há confirmação automática de PIX                                                                                   | —                      | 03 §10         |
| `RN-14-07` | Aporte declarado entra pendente e não credita moeda antes da homologação de Admin                                                                             | 16                     | 04 §2          |
| `RN-14-08` | Quem homologa o aporte não é o provedor: o Apoiador nunca homologa o próprio                                                                                  | —                      | 04 §1          |
| `RN-14-09` | Toda saída ao público exibe moedas; reais só na tela em que se declara a transferência                                                                        | 16                     | 04 §1          |
| `RN-14-10` | Avatar e nick são do Apoiador, sujeitos à unicidade de nick e à auditoria por amostragem                                                                      | —                      | 02 §1, 11 §8.2 |
| `RN-14-11` | O avatar próprio exige 10 moedas acumuladas; abaixo do piso vale o avatar padrão, e o direito alcançado não regride                                           | —                      | 11 §8.2        |
| `RN-14-12` | O documento comprobatório só vai à vitrine depois que um Admin o anexa ao cadastro                                                                            | —                      | 02 §1, 03 §10  |
| `RN-14-13` | Desafio extra exige validação do Mestre da trilha e aprovação de Admin antes de publicar                                                                      | —                      | 04 §3          |
| `RN-14-14` | A recompensa do desafio extra precisa estar provida antes da publicação                                                                                       | 9                      | 04 §3          |
| `RN-14-15` | Não há teto de desafios simultâneos: o controle é a aprovação caso a caso                                                                                     | —                      | 04 §3          |
| `RN-14-16` | No aberto, ninguém é barrado de disputar; o que é limitado é a quantidade de recompensas                                                                      | —                      | 04 §3          |
| `RN-14-17` | O direcionado exige justificativa do vínculo e alcança quem não tem divulgação autorizada                                                                     | 11                     | 04 §3          |
| `RN-14-18` | A plataforma não confirma ao proponente se o nick existe, nem na proposta nem na recusa                                                                       | 12                     | 03 §10, 04 §3  |
| `RN-14-19` | O desafio extra vale pontos extras, computados isoladamente da pontuação regular                                                                              | —                      | 04 §3          |
| `RN-14-20` | Nenhum contato direto com Guerreiro(a) ou família: tudo é mediado pela plataforma                                                                             | 10                     | 04 §3          |
| `RN-14-21` | A efetividade é painel vivo, agregado e por avatar, sem relatório fechado no Ciclo 01                                                                         | —                      | 04 §3          |
| `RN-14-22` | Sem divulgação autorizada, o Apoiador só recebe contagem; a exceção é a conclusão do desafio que ele mesmo direcionou, limitada ao fato de ter sido concluída | 12                     | 03 §12         |
| `RN-14-23` | O nick vem da família: a plataforma não o revela, não lista, não sugere e não completa                                                                        | 12                     | 02 §1, 03 §10  |
| `RN-14-24` | Favoritar é leitura: não abre canal, não avisa a criança e não amplia o acesso                                                                                | 10                     | 03 §10         |
| `RN-14-25` | Novidade do favorito são cinco fatos, em destaque por 30 dias, só nesta aplicação                                                                             | —                      | 03 §10         |
| `RN-14-26` | Proposta de Apoiador não pontua e segue a fila única da gestão                                                                                                | —                      | 03 §§7, 10     |
| `RN-14-27` | No Ciclo 01 não há notificação por e-mail: o retorno acontece na plataforma                                                                                   | —                      | 03 §9          |
| `RN-14-28` | A etiqueta ODS é descritiva: aparece como cobertura agregada, nunca como mérito do apoio                                                                      | 20                     | 04 §4, 11 §2.1 |
| `RN-14-29` | O Apoiador não pontua: a progressão dele corre em moedas, selos e níveis de sustento                                                                          | 21                     | 14 §1          |
| `RN-14-30` | A missão do Apoiador não é a missão da trilha nem o desafio extra, e nunca aparece em tela de criança                                                         | 21                     | 14 §1          |
| `RN-14-31` | Toda missão nasce de uma necessidade de recurso publicada; sem ela não há missão                                                                              | 9                      | 14 §5          |
| `RN-14-32` | A missão só se conclui com aporte homologado por Admin; declarar não conclui                                                                                  | 21                     | 14 §5          |
| `RN-14-33` | A missão concluída rende moeda e selo, nunca ponto                                                                                                            | 21                     | 14 §5          |
| `RN-14-34` | Na missão coletiva, cada um recebe as moedas do que aportou; ninguém recebe crédito pelo que outro deu                                                        | 16                     | 04 §1, 14 §5   |
| `RN-14-35` | O nível de sustento sobe por frentes de necessidade diferentes cobertas, nunca por volume aportado                                                            | 21                     | 14 §7          |
| `RN-14-36` | Nível de sustento e selo conquistados não regridem                                                                                                            | —                      | 14 §§7, 8      |
| `RN-14-37` | Nenhum saldo de moedas compra vantagem: nem dado de criança, nem contato, nem prioridade pedagógica, nem aprovação mais rápida de desafio                     | 21                     | 14 §9          |
| `RN-14-38` | Não há ranking de apoiadores por dinheiro: há coleção de selos e nível, nunca pódio de valor                                                                  | 21                     | 14 §9          |
| `RN-14-39` | O perfil pessoa física ou jurídica é declarado e não verificado; define escada e recorte do painel, e nada mais                                               | —                      | 02 §1, 14 §4   |
| `RN-14-40` | O degrau da escada é sugestão, não piso: o valor livre aceita qualquer quantia, com fração de duas casas                                                      | 16                     | 04 §2          |
| `RN-14-41` | Pontos do desafio extra são no máximo 10, de qualquer proponente                                                                                              | —                      | 04 §3          |
| `RN-14-42` | Item ofertado ao catálogo avulso só entra depois de homologado por Admin e com lastro                                                                         | 9                      | 02 §8.2        |
| `RN-14-43` | O preço em pontos extras é da gestão, nunca de quem oferta, e não deriva do valor em moedas                                                                   | 23                     | 02 §8.2        |
| `RN-14-44` | Ofertar item não abre dado de criança nem prioridade: o retorno é agregado, como todo o resto                                                                 | 21                     | 14 §8          |

## 8. Modelo de dados

A aplicação cria três entidades: `Favorito`, `MissaoDoApoiador` e `SeloDoApoiador`. As demais
já estão no PRD-01, no PRD-07 e no PRD-09; aqui elas são escritas ou lidas.

**`MissaoDoApoiador` não se confunde com `Missao`**, que é a da trilha e vive no PRD-09. O nome
longo é obrigatório justamente porque as duas coexistem no mesmo domínio.

```text
ESCREVE (por ato do Apoiador)              LÊ (definidos em outro PRD)
SolicitacaoDeParticipacao   (PRD-01)       Necessidade / Lancamento      (PRD-07)
Apoiador — avatar e nick    (PRD-01)       SaldoDeRecurso                (PRD-07)
Aporte (pendente)           (PRD-07)       Trilha / Missao / EtiquetaODS (PRD-09)
DesafioExtra                (PRD-01)       Guerreiro(a) — avatar e nick  (PRD-01)
Favorito                    [entidade nova] CriacaoOriginal              (PRD-09)
SugestaoOuProposta          (PRD-01)       Resultado / Badge / Nivel     (PRD-01)

PUBLICADAS PELA GESTÃO (App 03), LIDAS AQUI
MissaoDoApoiador            [entidade nova]
SeloDoApoiador              [entidade nova] — creditado na homologação
```

| Entidade           | Atributos essenciais                                                                                                                                                                                                                                                                                                    |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DesafioExtra`     | proponente, trilha, missão opcional, modalidade (aberto ou direcionado), nick do destinatário e justificativa do vínculo (só no direcionado), recompensa, quantidade disponível, critério de atribuição, pontos extras, vigência, Mestre validador, Admin aprovador, aporte de lastro, situação, etiquetas ODS herdadas |
| `Favorito`         | Apoiador, alvo (Guerreiro(a) ou Mestre), data de inclusão                                                                                                                                                                                                                                                               |
| `MissaoDoApoiador` | necessidade de recurso de origem, nível de necessidade (existir, acontecer, reconhecer, permanecer), título, o que se pede, quantidade em moedas ou itens, prazo, selo que rende, situação (aberta, concluída, vencida), Admin que publicou                                                                             |
| `SeloDoApoiador`   | Apoiador, família (frente, modalidade, ato, multiplicação), selo, missão ou aporte de origem, data do crédito                                                                                                                                                                                                           |

Imutabilidade e derivação:

- `DesafioExtra` **não é editável depois de publicado**. Corrigir é propor de novo, e a
  proposta anterior fica registrada com o desfecho que teve.
- O **nível de sustento é derivado**, nunca armazenado: sai dos níveis de necessidade das
  missões concluídas pelo Apoiador, do mesmo modo que o Poder Sustentador sai dos aportes.
  Derivado, ele não regride por edição — só cresce com missão nova concluída.
- O **quanto falta** de uma `MissaoDoApoiador` é derivado dos aportes **homologados** ligados à
  necessidade de origem. Aporte pendente não abate nada.
- `SeloDoApoiador` é **somente inserção**, creditado no ato da homologação que conclui a missão.
  Não há rota que o retire.
- O **nick do destinatário** é guardado como o Apoiador o digitou, não como referência ao
  Guerreiro(a). A ligação com a pessoa só é feita na validação do Mestre — é o que impede a
  aplicação de confirmar existência.
- A **novidade do favorito** é derivada, não armazenada: são os cinco fatos com data nos
  últimos 30 dias, lidos das entidades que os produzem.
- O **Poder Sustentador** é derivado dos aportes homologados (PRD-07); esta aplicação apenas o lê.
- O `Aporte` declarado aqui nasce **pendente**, com `origem do registro` igual a "App 08".

## 9. Contratos de API

A aplicação segue as convenções do PRD-01 — prefixo `/v1`, token de sessão, erro em corpo
único. As rotas de homologação, cadastro e anexação de documento são da App 03 (PRD-02).

| Método | Rota                                 | Autenticação | Descrição                                                            |
| ------ | ------------------------------------ | ------------ | -------------------------------------------------------------------- |
| POST   | `/v1/solicitacoes-de-participacao`   | pública      | Pré-cadastro com aporte declarado e comprovante                      |
| GET    | `/v1/vitrine/necessidades`           | pública      | Necessidades de recurso em aberto (PRD-07)                           |
| GET    | `/v1/missoes-do-apoiador`            | pública      | Missões abertas, por nível de necessidade, com o que falta em moedas |
| GET    | `/v1/eu/apoiador/sustento`           | Apoiador     | Nível de sustento, selos e a frente que falta para o próximo         |
| PUT    | `/v1/eu/apoiador/identidade`         | Apoiador     | Define ou troca avatar e nick exibidos no card                       |
| POST   | `/v1/eu/apoiador/documentos`         | Apoiador     | Envia comprobatório para o Admin anexar ao cadastro                  |
| GET    | `/v1/meus-aportes`                   | Apoiador     | Aportes homologados e Poder Sustentador, em moedas                   |
| POST   | `/v1/aportes/declarados`             | Apoiador     | Declara aporte em dinheiro, com comprovante, pendente                |
| GET    | `/v1/eu/aportes/declarados`          | Apoiador     | Situação dos aportes declarados: pendente, homologado, recusado      |
| POST   | `/v1/desafios-extras`                | Apoiador     | Propõe desafio aberto ou direcionado                                 |
| GET    | `/v1/eu/desafios-extras`             | Apoiador     | Estado de cada desafio no fluxo e quantidade restante                |
| GET    | `/v1/eu/desafios-extras/efetividade` | Apoiador     | Painel vivo: concluintes, trilhas, moedas e cobertura de ODS         |
| GET    | `/v1/eu/favoritos`                   | Apoiador     | Favoritos do Apoiador, com as novidades dos últimos 30 dias          |
| POST   | `/v1/eu/favoritos`                   | Apoiador     | Favorita por nick exato de Guerreiro(a) ou por Mestre                |
| DELETE | `/v1/eu/favoritos/{id}`              | Apoiador     | Remove o favorito                                                    |
| POST   | `/v1/sugestoes`                      | Apoiador     | Registra proposta na fila única da gestão                            |
| GET    | `/v1/eu/sugestoes`                   | Apoiador     | Status das próprias propostas                                        |

As consultas de vitrine consumidas pela tela de acompanhamento são as mesmas rotas públicas do
PRD-03, sem token de sessão e sem parâmetro que identifique o Apoiador — a chave da aplicação
é exigida nelas como em toda rota (PRD-01).

Erros previstos: comprovante ausente ou em formato não aceito (422, com os formatos válidos);
declaração de aporte em material ou serviço (422, com a orientação de procurar a gestão);
excesso de envios da porta pública (429, com o tempo de espera em linguagem simples); login sem
cadastro prévio (403, com a orientação de usar o pré-cadastro); senha provisória não trocada
(403 em qualquer rota que não seja a da troca); nick já usado na identidade (409, com
sugestões); envio de avatar próprio abaixo do piso de 10 moedas (409, com quanto falta);
desafio proposto sem lastro (409, com o que falta prover); edição de desafio publicado (405);
aporte para missão já concluída ou vencida (409, com o que aconteceu com ela); missão
inexistente ou despublicada (404);
favorito por nick inexistente **ou** sem divulgação autorizada (**404 idêntico nos dois
casos**); tentativa de homologar aporte ou de ler dado de contato de Guerreiro(a) (403). A
proposta de desafio direcionado com nick desconhecido é **aceita** e recusada depois, na
validação — não é erro de tela.

## 10. Requisitos não funcionais

- Web App responsivo **Mobile First**: o Apoiador costuma chegar pelo celular, a partir de um
  link enviado por alguém do projeto.
- **Uso raro é a condição normal**: entra-se poucas vezes por ciclo, e cada tela precisa ser
  compreensível sem aprendizado acumulado.
- **Linguagem de adulto leigo em custeio**: sem jargão contábil, com moedas explicadas na
  própria tela.
- **Rede instável**: a leitura tolera queda com o que já foi carregado; declaração de aporte e
  proposta de desafio **exigem rede**, porque geram registro com anexo — e a tela diz isso, em
  vez de simular sucesso.
- **Anexo em celular modesto**: comprovante e documento enviados por foto, com compressão e
  limite de tamanho declarado antes do envio.
- Escrita idempotente: reenviar a mesma declaração por falha de rede não gera dois aportes.
- **Acessibilidade digital**: contraste, alvos de toque grandes e leitura por voz.
- Idioma pt-BR; código aberto.

## 11. LGPD e proteção da criança

| Dado coletado                    | Finalidade                                        | Base legal         | Retenção                                      | Quem acessa             |
| -------------------------------- | ------------------------------------------------- | ------------------ | --------------------------------------------- | ----------------------- |
| Nome ou razão social             | Identificar o Apoiador e o aporte                 | consentimento      | enquanto durar o cadastro                     | gestão e público (nick) |
| E-mail                           | Dar acesso à aplicação e responder ao pedido      | consentimento      | enquanto durar o cadastro                     | gestão                  |
| WhatsApp                         | Contato da gestão com o Apoiador                  | consentimento      | enquanto durar o cadastro                     | gestão                  |
| Comprovante de transferência     | Provar o aporte e homologá-lo                     | obrigação legal    | permanente, junto ao lançamento               | gestão                  |
| Documentos comprobatórios        | Comprovar o apoio na página pública               | consentimento      | enquanto durar o cadastro                     | gestão e público        |
| Avatar e nick                    | Identidade pública do Apoiador                    | consentimento      | enquanto durar o cadastro                     | público                 |
| Perfil pessoa física ou jurídica | Definir a escada de valores e o recorte do painel | consentimento      | enquanto durar o cadastro                     | gestão                  |
| Justificativa do vínculo         | Aprovar o desafio direcionado                     | interesse legítimo | permanente, junto ao desafio                  | gestão                  |
| Proposta registrada              | Evolução da plataforma                            | consentimento      | 90 dias após o retorno; permanente se adotada | gestão                  |

- **Consentimento**: o Apoiador é adulto e se cadastra por vontade própria; o aviso de coleta
  aparece na porta pública e em toda tela que coleta, com acesso à área detalhada.
- **Sem dado fiscal e sem dado bancário**: a plataforma não coleta CPF, CNPJ nem documento de
  identidade e não armazena chave nem conta.
- **Proteção da criança é o eixo desta aplicação**: nada aqui identifica Guerreiro(a) além de
  avatar e nick, e só de quem tem divulgação autorizada. Sem contato, sem nome real, sem
  endereço, sem foto, sem canal de mensagem.
- **O nick vem da família**, nunca da plataforma. A busca é por nick exato e responde igual para
  nick inexistente e para nick sem autorização — o que impede descobrir quem existe.
- **O direcionado não vaza existência**: a aplicação não confirma o nick, e a recusa também não.
- **Efetividade sem exposição**: o painel é agregado; a identificação individual só acontece por
  avatar e nick de quem tem divulgação autorizada.
- **Direitos do Apoiador**: acesso, correção e exclusão dos próprios dados são pedidos à gestão,
  que os trata na App 03. O comprovante do aporte já homologado permanece, por ser prova
  contábil do lançamento.

## 12. Critérios de aceite e métricas

- Pré-cadastro enviado com comprovante aparece na fila da App 03 e **não cria acesso**: a mesma
  pessoa tentando entrar é recusada.
- Pré-cadastro sem comprovante não é aceito, e a tela diz quais formatos valem.
- Terceiro envio seguido da mesma origem sofre atraso, sem CAPTCHA e sem bloqueio definitivo.
- Apoiador cadastrado com senha provisória é obrigado a trocá-la antes de ver qualquer tela.
- Nick já usado é recusado com sugestões; homologado o aporte, o card aparece na vitrine com
  avatar, nick e total de moedas.
- Apoiador com 5 moedas não consegue enviar avatar próprio, vê quanto falta e aparece na vitrine
  com o avatar padrão; ao cruzar as 10 moedas, o envio abre sem intervenção da gestão.
- Aporte declarado fica pendente: não altera o Poder Sustentador nem cobre necessidade antes da
  homologação do Admin. Homologado, a necessidade sai da lista de abertas.
- Tentativa de declarar aporte em material devolve a orientação de procurar a gestão.
- Desafio proposto sem lastro não é publicado, e a tela mostra o que falta prover.
- Desafio recusado pelo Mestre aparece com motivo; desafio publicado não aceita edição.
- Desafio direcionado com nick inexistente é **aceito na tela** e recusado na validação, sem que
  nenhuma tela revele se o nick existe.
- Desafio direcionado a Guerreiro(a) sem divulgação autorizada, com vínculo comprovado, é
  publicado e entregue ao destinatário.
- Painel de efetividade muda no mesmo dia em que um Guerreiro(a) conclui o desafio, sem
  fechamento nem espera por período.
- Conclusão de quem não tem divulgação autorizada aparece na contagem e **não** aparece com
  avatar ou nick.
- Busca de nick inexistente e busca de nick sem autorização devolvem **a mesma tela**.
- Criação original publicada por um favorito aparece em destaque no dia seguinte e some depois
  de 30 dias.
- Nenhuma tela da aplicação oferece campo de mensagem, telefone ou e-mail de Guerreiro(a),
  família ou Mestre.
- Quem se declara pessoa física vê a escada que começa em 1 moeda; quem se declara pessoa
  jurídica vê a outra. Nenhum dos dois é impedido de usar o valor livre, em qualquer quantia.
- **Aporte parcial não conclui missão e não credita selo**: a missão continua aberta com o
  restante atualizado, e as moedas do aporte já estão no Poder Sustentador de quem o fez.
- **Duas pessoas fechando a mesma missão recebem cada uma as suas moedas** e ambas o selo de
  mutirão. Nenhuma delas vê o nome da outra.
- Aporte pendente não abate o que falta em nenhuma missão: a tela mostra o mesmo valor de antes
  até o Admin homologar.
- Missão que vence sem fechar sai da lista, e nenhum aporte já homologado é estornado.
- Apoiador que cobre uma missão de "acontecer" e outra de "permanecer" chega ao **nível 3**,
  enquanto quem cobriu duas de "acontecer" — ainda que por valor muito maior — fica no
  **nível 2**. É a prova de que o nível mede frentes, não dinheiro.
- Nenhuma tela lista apoiadores em ordem de valor aportado.

Hipóteses do Ciclo 01 (documento 10): este PRD **sustenta H3** — recursos supridos por mestres
e apoiadores. Ele passa a medir quantas necessidades publicadas foram cobertas por aporte de
Apoiador, em quanto tempo, e quanto do lastro do ciclo veio desta aplicação em vez do
lançamento manual da gestão.

## 13. Decisões tomadas neste PRD

| Decisão                                                                 | Gravada em    | Linha do doc 09                          |
| ----------------------------------------------------------------------- | ------------- | ---------------------------------------- |
| Efetividade é painel vivo, agregado e por avatar, sem relatório fechado | 04 §3         | Efetividade do apoio ao Apoiador         |
| Um usuário por cadastro no Ciclo 01, inclusive no institucional         | 02 §1         | Instituição com mais de um usuário       |
| O aporte feito pela App 08 é em dinheiro; material e serviço pelo Admin | 02 §1, 03 §10 | Forma do aporte feito pela App 08        |
| O direcionado alcança quem não tem divulgação, sem confirmar o nick     | 04 §3         | Direcionado a quem não tem divulgação    |
| Avatar próprio a partir de 10 moedas; abaixo do piso, avatar padrão     | 11 §8.2       | Piso do avatar personalizado             |
| "Poder Econômico" passa a se chamar "Poder Sustentador"                 | 04 §1         | Nome do poder dos provedores             |
| Missão do Apoiador, níveis de sustento e selos                          | 14 §§1, 5–9   | Missão do Apoiador                       |
| Perfil pessoa física ou jurídica, declarado e não verificado            | 02 §1, 14 §4  | Perfil pessoa física e pessoa jurídica   |
| Escadas por perfil, a de pessoa física começando em 1 moeda             | 04 §2         | Escadas de valores sugeridos por perfil  |
| Necessidade admite cobertura parcial                                    | 04 §1         | Cobertura parcial da necessidade         |
| Técnicas de gamificação vedadas no apoio                                | 14 §9         | Técnicas de gamificação vedadas no apoio |

As quatro primeiras fecharam as duas questões em aberto do PRD-14 no documento 08 e a pendência
do formato do relatório de efetividade, que também constava do PRD-07. As duas últimas vieram
da revisão do fundador: o **piso do avatar** e a **renomeação do Poder Econômico**, que alcança
todos os documentos onde o termo antigo aparecia. A entidade `Favorito` foi acrescentada ao
modelo do PRD-01, e o `DesafioExtra` — que já constava dele — teve os atributos detalhados
aqui. O `Aporte` do PRD-07 ganhou "App 08" como origem do registro.

**Na v2** nenhuma decisão nasceu aqui: todas vieram do documento 14 e dos documentos-fonte que
ele alcançou, e já estão em "Já decididos" no documento 09. As entidades `MissaoDoApoiador` e
`SeloDoApoiador` foram acrescentadas ao modelo do PRD-01, e a **cobertura parcial da
necessidade**, ao PRD-07.

**Na v3** também não: o teto de 10 pontos do desafio extra, o custeio por saldo da plataforma e
a oferta de item ao catálogo avulso vieram dos documentos 04 §3 e 02 §8.2, e estão em "Já
decididos" no documento 09. As entidades `ItemDeCatalogoAvulso` e `Troca` foram acrescentadas
ao modelo do PRD-07.

**Na v4** duas decisões alcançam esta aplicação, ambas gravadas nos documentos-fonte antes de
chegarem aqui: o **recibo emitido fora da plataforma** pela pessoa jurídica, a pedido, com a
tela de pré-cadastro declarando isso (documento 04 §2), e o **apoio em código como aporte**, por
hora declarada com o _pull request_ integrado como lastro, homologado por Admin e valorado pelo
valor-hora único da tabela de referência (documento 04 §1). A segunda abre a **segunda via para
o nível 5 de sustento**, que deixa de exigir virar Mestre.

## 14. Pendências que permanecem

- **Valores da tabela de referência** que converte acervo, kits, camisas e hora-aula em moedas:
  a tabela e quem a mantém estão decididos — é cadastro da gestão, versionado por vigência —,
  os valores por tipo não. **Não trava esta aplicação**, porque o aporte pela App 08 é em
  dinheiro, mas trava a página pública do Apoiador que doou material.
- **Catálogo de recompensas por marco** (documento 09): o que o Apoiador pode oferecer como
  recompensa de desafio extra convive com o catálogo do Ciclo 01, ainda não fechado.
- **Valores da tabela de preços do catálogo avulso**: a tabela de referência e o piso de 20
  estão decididos; os preços por tipo são cadastro da gestão. **Trava** o `RF-14-77` na
  prática, não no desenho.
- **Catálogo de missões do Ciclo 01** (documento 09): os arquétipos estão no documento 14, mas
  a quantidade, o prazo e o selo de cada missão dependem do catálogo de recompensas por marco e
  da tabela de valoração. A aplicação está pronta para exibir o que a gestão publicar.
  Quatro saíram desta lista, decididas: a **identificação fiscal de quem doa** — recibo emitido
  pela pessoa jurídica, fora da plataforma, com a tela de pré-cadastro declarando isso —, o
  **apoio em código**, que passa a ser aporte por hora declarada com o _pull request_ integrado
  como lastro e abre a segunda via para o nível 5 de sustento, a **peça de prestação de contas**,
  que é o painel vivo sem relatório fechado no Ciclo 01 (documento 04 §1), e o cadastro
  institucional, com **um usuário por cadastro** neste ciclo (documento 02 §1).

## 15. Rastreabilidade

| Requisito               | Origem                                                           |
| ----------------------- | ---------------------------------------------------------------- |
| `RF-14-01` a `RF-14-11` | 02 §1 e 03 §§1.1, 10 (pré-cadastro, identificação e acesso)      |
| `RF-14-12` a `RF-14-20` | 02 §1, 03 §10 e 11 §8.2 (identidade pública e comprobatórios)    |
| `RF-14-21` a `RF-14-28` | 04 §§1, 2 e 03 §10 (moeda, aporte declarado e necessidades)      |
| `RF-14-29` a `RF-14-39` | 04 §3 (desafios extras, modalidades e salvaguardas)              |
| `RF-14-40` a `RF-14-47` | 04 §§3, 4 (rastreio de efetividade e cobertura de ODS)           |
| `RF-14-48` a `RF-14-55` | 03 §§8, 10 e 02 §1 (painel público, nick da família e favoritos) |
| `RF-14-56` a `RF-14-59` | 03 §§7, 10 (fila única de propostas, canal fechado e aviso)      |
| `RF-14-60` a `RF-14-73` | 14 §§2, 5–9 e 04 §§1, 2 (missões, níveis de sustento e selos)    |
| `RF-14-74` a `RF-14-76` | 04 §3 (teto de pontos, formato e custeio do desafio extra)       |
| `RF-14-77` a `RF-14-81` | 02 §8.2 (catálogo avulso ofertado por Apoiador, homologado)      |
