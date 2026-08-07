# PRD-03 — App 06: Vitrine pública

## 1. Identificação

| Campo            | Valor                                             |
| ---------------- | ------------------------------------------------- |
| PRD              | PRD-03                                            |
| Aplicação        | App 06 — Vitrine pública                          |
| Onda             | 4                                                 |
| Situação         | em revisão                                        |
| Versão e data    | v2 — 2026-08-07                                   |
| Depende de       | PRD-01, PRD-13                                    |
| Documentos-fonte | 02 §§1, 4, 03 §§8, 12, 04 §§1, 2, 4, 11 §§8.1–8.3 |

## 2. Contexto e objetivo

A vitrine é **a cara pública do projeto**: o lugar onde a criação do Guerreiro(a) vira
reconhecimento, onde o apoio vira prova e onde o dado do território deixa de ser planilha
interna e passa a ser bem público da comunidade. Não tem login, não tem cadastro e não escreve
nada sobre criança alguma — é superfície de leitura, e é essa restrição que a torna segura.

O que muda na operação do Ciclo 01: os Guerreiros e Guerreiras cujo responsável autorizou
aparecem com avatar, nick e portfólio; os painéis do território ficam abertos a moradores,
associações, escolas, pesquisadores e poder público; e a plataforma ganha suas **portas de
entrada de gente nova** — o formulário de quem quer ser Mestre ou Apoiador, o formulário de quem
quer o conjunto de dados e a chamada **"Quero participar"**, que leva ao pré-cadastro da Área do
Apoiador. Nenhuma delas cadastra ninguém: todas viram fila na App 03.

A vitrine é consequência, não causa. Ela só existe na medida em que a App 07 (PRD-13) produziu
autorizações, os Mestres publicaram trilhas (PRD-09), as séries de coleta correram (PRD-08) e o
livro-razão registrou aportes (PRD-07). Se a autorização for revogada, ela desaparece dali na
hora — o sentido do fluxo é sempre esse.

## 3. Escopo

### 3.1 Dentro do escopo

- **Seis seções com cards**: Guerreiros e Guerreiras, Poderes, Mestres, Batalhas, Apoiadores e
  Comunidades Virtuais, cada card abrindo a **página individual** do personagem.
- **Cards rotativos** de Guerreiros e Guerreiras, com troca a cada 5 segundos.
- **Consulta por nick exato**, para quem recebeu o nick da família — sem lista, sem sugestão e
  sem completação.
- **Portfólio de criações originais** dos Guerreiros e Guerreiras autorizados, com autoria por
  nick.
- **Rankings públicos**, apenas com pontos regulares e apenas de quem tem divulgação
  autorizada.
- **Painel público da Comunidade Virtual** — séries históricas do território, agregadas até o
  bairro, com a representação visual que cresce conforme a comunidade é preenchida.
- **Metodologia legível** de cada série: o que se mede, cadência declarada, período coberto,
  origem da medição, número de registros válidos.
- **Painel de cobertura da Agenda 2030** por comunidade e por ciclo, com destaque para a meta
  17.18 e a ressalva de que o ODS 18 é adoção voluntária do Brasil.
- **Três recortes de leitura** — sociedade civil (padrão), pesquisadores e gestores públicos —,
  sobre os mesmos dados públicos.
- **Formulário de solicitação de participação** como Mestre ou Apoiador.
- **Formulário de solicitação de dados** para pesquisadores e gestores públicos.
- **Chamada "Quero participar"** em **toda página individual** e no pedido de favoritar,
  levando à porta da Área do Apoiador — pré-cadastro e caminho de apoio.
- **Card de Apoiador padronizado**: moldura comum, avatar centralizado, nick e **total de
  moedas em destaque**.
- **Necessidades de recurso em aberto** das atividades sem lastro, com o caminho para apoiar.
- **Seções institucionais** — "Quem somos", "Contatos" e "Como apoiar" com a chave PIX —, a
  **nota de transparência sobre IA** e o vídeo de apresentação.
- **Área detalhada de dados**, explicando o que a plataforma coleta, de quem, para quê e o que
  a vitrine **não** coleta do visitante.

### 3.2 Fora do escopo

- **Login, cadastro e qualquer área restrita** — a aplicação inteira é pública.
- **Favoritos e qualquer preferência do visitante**: não são guardados nem no servidor nem no
  aparelho. Acompanhar alguém é função da App 08 (PRD-14).
- **Pré-cadastro de Apoiador**: a tela é da App 08 (PRD-14); aqui fica só a chamada que leva
  até ela.
- **Avaliação das solicitações**, **validação do comprovante** e **entrega do conjunto de
  dados**: são atos de Admin na App 03 (PRD-02).
- **Edição do conteúdo institucional**: também da App 03; aqui só se exibe o que foi
  publicado.
- **O jogo** (App 04, PRD-12), que consome os mesmos cards mas é outra aplicação.
- **Qualquer canal de contato com Guerreiro(a) ou família**, inclusive formulário, comentário
  ou reação.
- **Notificação por e-mail**: não existe no Ciclo 01, nem para quem preencheu formulário.
- **Publicidade e patrocínio**: não existem no Ciclo 01 — o tema é estudo para ciclo futuro
  (documento 09). Rastreamento do visitante não existe em ciclo nenhum.
- **Dado abaixo do bairro**: rua, condomínio, bloco e quadra só saem na entrega aprovada.

## 4. Personas e permissões

| Persona          | O que faz nesta aplicação                                          | O que não pode fazer                                                  |
| ---------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------- |
| Visitante        | Navega, consulta nick exato, solicita participação e pede dados    | Entrar, favoritar, comentar, contatar criança, ver quem não autorizou |
| Pesquisador      | Lê séries e metodologia e pede o conjunto completo pelo formulário | Baixar o conjunto direto da vitrine ou ver o coletor                  |
| Gestor público   | Lê o painel do território e a cobertura da Agenda 2030 por ciclo   | O mesmo do pesquisador                                                |
| Admin            | Nada aqui: publica o conteúdo institucional pela App 03            | Editar a vitrine por dentro dela                                      |
| Mestre, Apoiador | Aparecem com a prova pública de habilidade ou de apoio             | Editar a própria página pela vitrine                                  |
| Guerreiro(a)     | Aparece por avatar e nick, se o responsável autorizou              | Entrar, editar ou retirar a própria exibição                          |
| Responsável      | Nada aqui: concede e revoga na App 07                              | Alterar o que aparece sem passar pela autorização                     |

Não há persona autenticada nesta aplicação. Toda escrita listada acima — as duas solicitações —
é ato público e anônimo do ponto de vista da plataforma: gera registro na fila, nunca acesso.

## 5. Jornadas principais

### 5.1 Sociedade civil — o recorte padrão

1. O visitante abre a vitrine e cai no recorte **sociedade civil**, sem escolher nada.
2. Vê a narrativa do projeto, o vídeo de apresentação e os **cards rotativos** dos Guerreiros e
   Guerreiras autorizados, trocando a cada 5 segundos.
3. Clica em um card e abre a **página individual**: trajetória nas trilhas, badges e níveis por
   poder, portfólio de criações e participação em batalhas.
4. Navega para Poderes, Mestres, Batalhas, Apoiadores e Comunidades Virtuais pelo mesmo padrão
   de card e página.
5. Em "Como apoiar", encontra a chave PIX e as **necessidades de recurso em aberto** das
   atividades sem lastro.
6. Trocando de recorte, continua na mesma vitrine: muda a porta de entrada e a ordem, não o
   conteúdo nem o direito de acesso.

### 5.2 Pesquisador — série histórica e metodologia

1. O pesquisador escolhe o recorte **pesquisadores** e chega direto às séries por comunidade.
2. Cada série declara **o que se mede, a cadência do desafio, o período coberto, a origem da
   medição** — registro manual ou sensor construído na trilha — e o **número de registros
   válidos**.
3. Os dados aparecem agregados **até o bairro**, sem nick, nome, avatar ou código de coletor.
4. Precisando do conjunto completo, ele abre o **formulário de solicitação de dados** e declara
   quem é, a instituição e a finalidade do uso.
5. O pedido é gravado e cai na fila da App 03; a tela diz que **não há entrega automática** e
   que a aprovação é de um Admin.
6. A entrega, quando aprovada, é gratuita e anonimizada, e sai fora da vitrine.

### 5.3 Gestor público — o território por ciclo

1. O gestor escolhe o recorte **gestores públicos** e vê o painel do território por comunidade
   e por ciclo, com a evolução no tempo.
2. Ao lado, o **painel de cobertura da Agenda 2030**: quais objetivos as trilhas daquela
   comunidade tocaram, agregados por ciclo.
3. A tela destaca a **meta 17.18** como a contribuição própria do projeto — dado local
   desagregado do território — e registra que o **ODS 18 é adoção voluntária do Brasil**, não
   objetivo oficial da ONU.
4. A cobertura nunca aparece por Guerreiro(a): é sempre da comunidade e do ciclo.
5. Querendo a base para uma decisão de política pública, ele usa o mesmo formulário do
   pesquisador.

### 5.4 Quem quer ser Mestre ou Apoiador

1. A pessoa ou instituição abre o **formulário de solicitação de participação**.
2. Preenche o obrigatório — nome, e-mail, WhatsApp, pretensão (Mestre ou Apoiador) e
   apresentação em texto livre — e, se quiser, instituição representada e links comprobatórios.
3. A tela diz, antes do envio, que **a solicitação não cria cadastro nem acesso** e que quem
   avalia é um Admin, com **prazo de 7 dias**.
4. Enviado, o pedido é gravado e cai na fila da App 03. A tela confirma o registro e informa
   que o retorno virá pelo contato declarado — **não há notificação por e-mail automática**.
5. Repetindo o envio muitas vezes, o visitante encontra **espera crescente** antes de conseguir
   enviar de novo, com o motivo explicado em linguagem simples.

### 5.5 Quem quer participar, entrar ou apoiar

1. **Toda página individual** — de Guerreiro(a), Mestre, poder, apoiador ou comunidade — traz a
   chamada **"Quero participar"**. O pedido de favoritar leva ao mesmo lugar.
2. A chamada é **do projeto**: não oferece apoiar aquela pessoa, e a tela seguinte não carrega
   o nome nem o nick de quem estava sendo visto.
3. Ela abre a **porta da Área do Apoiador**, que explica o que é ser Apoiador — aportar, propor
   desafios extras, acompanhar favoritos — e leva ao **pré-cadastro**, onde a pessoa se
   identifica sem documento, escolhe o que vai aportar e anexa o comprovante.
4. A mesma tela mostra o caminho de quem não quer se cadastrar agora: **doar pela chave PIX** e
   ver as **necessidades de recurso em aberto**.
5. A tela diz que o pré-cadastro **não cria cadastro nem acesso**: um Admin valida o
   comprovante, com prazo de 7 dias, e só então o card aparece na vitrine.
6. Quem desiste volta à navegação sem preencher nada, e nada é gravado sobre a visita.

### 5.6 Procurar alguém pelo nick

1. Um parente ou amigo recebeu **da família** o nick da criança e o digita na busca.
2. A busca aceita **nick exato**: não lista, não sugere e não completa.
3. Havendo divulgação autorizada, abre a página pública daquele Guerreiro(a).
4. Não havendo — nick inexistente ou sem autorização —, a resposta é **a mesma**: "não
   encontrado", sem revelar qual dos dois casos ocorreu.
5. Tentativas repetidas encontram **atraso progressivo** por origem, que é o que impede
   varredura de nicks.

### 5.7 Autorização revogada durante a visita

1. O responsável revoga a autorização na App 07.
2. Na primeira leitura seguinte, o card, a página individual, o portfólio e o ranking já não
   trazem aquele Guerreiro(a).
3. Um endereço direto para a página dele responde **"não encontrado"**, como se nunca tivesse
   existido publicamente.
4. As criações em equipe permanecem, com os demais autores creditados e o revogado ausente.
5. Nada some do território: as séries continuam, agregadas e sem coletor, como sempre
   estiveram.

## 6. Requisitos funcionais

### 6.1 Navegação, cards e páginas

| ID         | Requisito                                                                                                               | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------------------------------------- | ---------- |
| `RF-03-01` | Vitrine abre sem login e sem cadastro, em domínio próprio                                                               | essencial  |
| `RF-03-02` | Aplicação exibe as seis seções com cards: Guerreiros e Guerreiras, poderes, Mestres, batalhas, apoiadores e comunidades | essencial  |
| `RF-03-03` | Cada card abre a página individual do personagem, com a composição do documento 11                                      | essencial  |
| `RF-03-04` | Cards de Guerreiros e Guerreiras rotacionam a cada 5 segundos                                                           | essencial  |
| `RF-03-05` | Card e página de Guerreiro(a) exibem só avatar, nick, badges, poderes e desempenho                                      | essencial  |
| `RF-03-06` | Nenhuma tela exibe imagem real, nome civil, rede social ou contato de Guerreiro(a)                                      | essencial  |
| `RF-03-07` | Página de Mestre e de Apoiador exibe currículo, portfólios, redes sociais e comprobatórios                              | essencial  |
| `RF-03-55` | Card de Apoiador exibe avatar, nick e o total de moedas aportadas em destaque                                           | essencial  |
| `RF-03-56` | Cards de Apoiador seguem moldura comum, com avatar centralizado em proporção fixa                                       | essencial  |
| `RF-03-57` | Apoiador sem aporte homologado não aparece na vitrine                                                                   | essencial  |
| `RF-03-08` | Portfólio exibe as criações originais autorizadas, com título, trilha, data e autoria por nick                          | essencial  |
| `RF-03-09` | Ranking público exibe apenas pontos regulares e apenas quem tem divulgação autorizada                                   | essencial  |
| `RF-03-10` | Aporte de Apoiador é exibido em moedas da plataforma, nunca em reais                                                    | essencial  |
| `RF-03-11` | Busca por nick exato devolve a página pública; nick inexistente e nick sem autorização têm a mesma resposta             | essencial  |
| `RF-03-12` | Aplicação não oferece listagem, sugestão ou completação de nicks                                                        | essencial  |
| `RF-03-13` | Guerreiro(a) sem autorização vigente não aparece em card, página, portfólio ou ranking                                  | essencial  |
| `RF-03-14` | Revogação da autorização retira o perfil do público na leitura seguinte                                                 | essencial  |

### 6.2 Território, séries e ODS

| ID         | Requisito                                                                                       | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------------- | ---------- |
| `RF-03-15` | Painel da comunidade exibe as séries históricas do território, agregadas até o bairro           | essencial  |
| `RF-03-16` | Painel nunca exibe nick, nome, avatar ou código de coletor                                      | essencial  |
| `RF-03-17` | Cada série declara o que mede, a cadência, o período coberto e a origem da medição              | essencial  |
| `RF-03-18` | Cada série informa o número de registros válidos do período                                     | essencial  |
| `RF-03-19` | Série interrompida aparece sinalizada como inativa, sem sumir do painel                         | essencial  |
| `RF-03-20` | Comunidade recém-criada aparece como território vazio, com nome e contorno                      | desejável  |
| `RF-03-21` | Representação visual da comunidade cresce conforme os registros acumulam                        | desejável  |
| `RF-03-22` | Painel de cobertura da Agenda 2030 agrega por comunidade e por ciclo                            | essencial  |
| `RF-03-23` | Painel destaca a contribuição à meta 17.18 e registra o ODS 18 como adoção voluntária do Brasil | essencial  |
| `RF-03-24` | Nenhuma etiqueta ODS aparece vinculada a um Guerreiro(a)                                        | essencial  |
| `RF-03-25` | Aplicação oferece os três recortes de leitura, com sociedade civil como padrão                  | essencial  |
| `RF-03-26` | Troca de recorte é navegação: não cria área restrita, cadastro nem coleta de dado               | essencial  |

### 6.3 Formulários públicos

| ID         | Requisito                                                                                        | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------------ | ---------- |
| `RF-03-27` | Formulário de participação exige nome, e-mail, WhatsApp, pretensão e apresentação                | essencial  |
| `RF-03-28` | Formulário de participação aceita instituição e links comprobatórios como opcionais              | essencial  |
| `RF-03-29` | Tela declara, antes do envio, que a solicitação não cria cadastro nem acesso                     | essencial  |
| `RF-03-30` | Tela informa o prazo de resposta de 7 dias e que quem avalia é um Admin                          | essencial  |
| `RF-03-31` | Solicitação enviada é gravada e entra na fila da App 03, com confirmação na tela                 | essencial  |
| `RF-03-32` | Formulário de dados exige solicitante, instituição, e-mail e finalidade declarada                | essencial  |
| `RF-03-33` | Tela do formulário de dados declara que a entrega é gratuita, anonimizada e depende de aprovação | essencial  |
| `RF-03-34` | Nenhum formulário devolve dado, arquivo ou acesso no ato do envio                                | essencial  |
| `RF-03-35` | Envio repetido da mesma origem encontra atraso progressivo, com o motivo explicado               | essencial  |
| `RF-03-36` | Consulta por nick tem limite por origem e janela, com atraso progressivo                         | essencial  |
| `RF-03-37` | Nenhuma proteção de abuso exige cadastro, login ou CAPTCHA do visitante                          | essencial  |

### 6.4 Convite ao acompanhamento

| ID         | Requisito                                                                                    | Prioridade |
| ---------- | -------------------------------------------------------------------------------------------- | ---------- |
| `RF-03-38` | Vitrine não guarda favorito nem preferência do visitante, no servidor ou no aparelho         | essencial  |
| `RF-03-39` | Toda página individual traz a chamada "Quero participar", que leva à Área do Apoiador        | essencial  |
| `RF-03-40` | Ação de favoritar ou acompanhar leva à mesma porta                                           | essencial  |
| `RF-03-41` | A chamada não vincula o apoio à pessoa exibida, e a tela seguinte não carrega quem era vista | essencial  |
| `RF-03-42` | Porta apresenta o que é ser Apoiador e leva ao pré-cadastro da App 08                        | essencial  |
| `RF-03-43` | Porta oferece também doar pela chave PIX e ver as necessidades de recurso em aberto          | essencial  |
| `RF-03-44` | Recusar o convite devolve o visitante à navegação, sem gravar nada sobre a visita            | essencial  |

### 6.5 Institucional e transparência

| ID         | Requisito                                                                              | Prioridade |
| ---------- | -------------------------------------------------------------------------------------- | ---------- |
| `RF-03-45` | Seções "Quem somos", "Contatos" e "Como apoiar" exibem o conteúdo publicado na App 03  | essencial  |
| `RF-03-46` | "Como apoiar" exibe a chave PIX da pessoa jurídica vinculada                           | essencial  |
| `RF-03-47` | Vitrine publica as necessidades de recurso em aberto das atividades sem lastro         | essencial  |
| `RF-03-48` | Nota de transparência sobre IA aparece nas seções institucionais                       | essencial  |
| `RF-03-49` | Vitrine exibe o vídeo de apresentação e a identidade visual de comunidade              | desejável  |
| `RF-03-50` | Vitrine não exibe publicidade nem patrocínio                                           | essencial  |
| `RF-03-51` | Vitrine não instala cookie, rastreador ou perfilamento do visitante                    | essencial  |
| `RF-03-52` | Área detalhada explica o que a plataforma coleta, de quem, para quê e por quanto tempo | essencial  |
| `RF-03-53` | Área detalhada declara que a vitrine não coleta dado do visitante                      | essencial  |

## 7. Regras de negócio

| ID         | Regra                                                                                     | Invariante (doc 99 §6) | Fonte       |
| ---------- | ----------------------------------------------------------------------------------------- | ---------------------- | ----------- |
| `RN-03-01` | A vitrine é pública, sem login, e não escreve nada sobre Guerreiro(a)                     | 1                      | 03 §§1.1, 8 |
| `RN-03-02` | Só aparece publicamente o Guerreiro(a) com autorização vigente do responsável             | 12                     | 03 §12      |
| `RN-03-03` | A revogação vale para frente e é imediata no que é público                                | 11                     | 03 §9       |
| `RN-03-04` | Guerreiro(a) aparece só por avatar e nick, sem imagem real, nome civil ou contato         | 12                     | 03 §12      |
| `RN-03-05` | Não há canal de contato entre visitante e Guerreiro(a) ou família                         | 10                     | 02 §1       |
| `RN-03-06` | A consulta é por nick exato, sem listagem, sugestão ou completação                        | 12                     | 02 §1       |
| `RN-03-07` | Nick inexistente e nick sem autorização recebem a mesma resposta                          | 12                     | 03 §8       |
| `RN-03-08` | Rota pública tem limite por origem e atraso progressivo, sem CAPTCHA nem cadastro         | —                      | 03 §8       |
| `RN-03-09` | A saída pública agrega até o bairro; rua e abaixo só na entrega aprovada por Admin        | 7, 17                  | 02 §1       |
| `RN-03-10` | O painel público nunca identifica o coletor, nem por código                               | 7                      | 02 §1       |
| `RN-03-11` | Solicitação de participação não cria cadastro nem acesso, e a avaliação é de Admin        | 3                      | 02 §1       |
| `RN-03-12` | O prazo de resposta ao solicitante é de 7 dias                                            | —                      | 02 §1       |
| `RN-03-13` | Solicitação de dados não entrega nada no ato: a entrega exige aprovação de Admin          | 17                     | 03 §12.3    |
| `RN-03-14` | A entrega do conjunto é gratuita e anonimizada em qualquer granularidade aprovada         | 17                     | 03 §12.3    |
| `RN-03-15` | A vitrine não guarda favorito nem preferência do visitante, em lugar nenhum               | —                      | 03 §8       |
| `RN-03-16` | Favoritar é função da App 08, de Apoiador cadastrado, e lá é leitura: não abre contato    | 10                     | 03 §10      |
| `RN-03-17` | O convite não cria cadastro nem acesso: cadastrar Apoiador é ato de Admin                 | 3                      | 02 §1       |
| `RN-03-25` | A chamada de participação é do projeto e nunca vincula apoio a um Guerreiro(a) específico | 10                     | 03 §8       |
| `RN-03-26` | Card de Apoiador só existe com aporte homologado, e exibe o total em moedas               | 16                     | 04 §2       |
| `RN-03-18` | Aporte é exibido em moedas da plataforma, nunca em reais                                  | 16                     | 04 §1       |
| `RN-03-19` | A etiqueta ODS é descritiva, agregada por comunidade e ciclo, nunca por Guerreiro(a)      | 20                     | 11 §2.1     |
| `RN-03-20` | O ODS 18 é citado como adoção voluntária do Brasil, não como objetivo da ONU              | 20                     | 04 §4       |
| `RN-03-21` | A vitrine não veicula publicidade nem patrocínio no Ciclo 01                              | —                      | 04 §2       |
| `RN-03-22` | A vitrine não instala cookie, rastreador ou perfilamento, para nenhuma finalidade         | —                      | 04 §2       |
| `RN-03-23` | Toda tela indica o que a plataforma coleta, com acesso à área detalhada                   | —                      | 03 §12      |

## 8. Modelo de dados

A aplicação **não escreve no domínio** além das duas solicitações públicas e **não cria
entidade nenhuma**. Também **não persiste nada do visitante** — nem no servidor, nem no
aparelho: sem favoritos, sem preferência de recorte, sem histórico de navegação.

```text
ESCREVE (ato público, sem cadastro)     LÊ (definidos em outro PRD)
SolicitacaoDeParticipacao  (PRD-01)     Guerreiro(a) / Avatar / Nick    (PRD-01)
SolicitacaoDeDados         (PRD-01)     Ponto / Nivel / Badge / Poder   (PRD-01)
                                        Consentimento (estado vigente)  (PRD-01)
NÃO PERSISTE                            CriacaoOriginal / Trilha        (PRD-09)
Nada do visitante — sem favorito,       Batalha                         (PRD-10)
preferência ou histórico               Mestre / Apoiador / Aporte      (PRD-07)
                                        ComunidadeVirtual / SerieDeColeta (PRD-08)
                                        EtiquetaODS                     (PRD-01)
                                        Conteúdo institucional          (PRD-02)
```

| Entidade                    | Atributos essenciais                                                                                                         |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `SolicitacaoDeParticipacao` | nome, e-mail, WhatsApp, pretensão, apresentação, instituição e links opcionais, situação, prazo, quem avaliou, parecer, data |
| `SolicitacaoDeDados`        | solicitante, instituição, e-mail, finalidade declarada, recorte pedido, situação, quem avaliou, desfecho, data e o que saiu  |

Derivações e imutabilidade:

- **Nada aqui é fonte de verdade.** Card, página, ranking e painel são projeções de leitura do
  que os PRDs 01, 07, 08, 09 e 10 gravaram.
- A **elegibilidade pública** de um Guerreiro(a) é derivada do estado vigente do
  `Consentimento` — a mesma derivação do PRD-13, e a mesma lista que o App 04 consome.
- A **agregação até o bairro** é aplicada na consulta, não no armazenamento: o registro
  continua com local fino e coletor identificado (PRD-08).
- **Novidade de favorito é da App 08** (PRD-14) e não tem projeção aqui.

## 9. Contratos de API

A aplicação segue as convenções do PRD-01 — prefixo `/v1`, erro em corpo único — e consome
**apenas rotas públicas, sem token**. As rotas de avaliação e entrega são da App 03 (PRD-02).

| Método | Rota                                 | Autenticação | Descrição                                                   |
| ------ | ------------------------------------ | ------------ | ----------------------------------------------------------- |
| GET    | `/v1/vitrine/guerreiros`             | pública      | Cards dos Guerreiros e Guerreiras com divulgação autorizada |
| GET    | `/v1/vitrine/guerreiros/{nick}`      | pública      | Página pública por nick exato                               |
| GET    | `/v1/vitrine/mestres`                | pública      | Cards e páginas de Mestres, com os comprobatórios           |
| GET    | `/v1/vitrine/apoiadores`             | pública      | Cards e páginas de Apoiadores, com aportes em moedas        |
| GET    | `/v1/vitrine/poderes`                | pública      | Poderes, trilhas e Mestres de cada um                       |
| GET    | `/v1/vitrine/batalhas`               | pública      | Batalhas, resultados e estatísticas de partida              |
| GET    | `/v1/vitrine/criacoes`               | pública      | Portfólio de criações originais autorizadas                 |
| GET    | `/v1/vitrine/rankings`               | pública      | Rankings por pontos regulares, só de quem autorizou         |
| GET    | `/v1/vitrine/conteudo-institucional` | pública      | "Quem somos", "Contatos", "Como apoiar" e a nota sobre IA   |
| GET    | `/v1/comunidades`                    | pública      | Comunidades com indicadores agregados (PRD-08)              |
| GET    | `/v1/comunidades/{id}/series`        | pública      | Séries históricas agregadas até o bairro, com metodologia   |
| GET    | `/v1/comunidades/{id}/ods`           | pública      | Cobertura de ODS da comunidade, por ciclo                   |
| GET    | `/v1/vitrine/ods/cobertura`          | pública      | Cobertura agregada de todas as comunidades do ciclo         |
| GET    | `/v1/vitrine/necessidades`           | pública      | Necessidades de recurso em aberto (PRD-07)                  |
| POST   | `/v1/solicitacoes-de-participacao`   | pública      | Registra pedido de inclusão como Mestre ou Apoiador         |
| POST   | `/v1/solicitacoes-de-dados`          | pública      | Registra pedido do conjunto de dados                        |

Nenhuma rota desta aplicação aceita ou devolve preferência de visitante: não há parâmetro de
favorito, de perfil ou de sessão anônima.

Erros previstos: nick não encontrado ou sem autorização (**404 idêntico nos dois casos**, sem
revelar qual ocorreu); campo obrigatório ausente no formulário (422, com o campo em falta);
excesso de consultas ou de envios da mesma origem (429, com o tempo de espera em linguagem
simples); pedido de granularidade abaixo do bairro em rota pública (422, com a orientação de
usar o formulário de solicitação de dados); tentativa de escrita em qualquer outra rota (405).

## 10. Requisitos não funcionais

- Web App responsivo **Mobile First**: a maior parte das visitas vem de celular, inclusive as
  da própria comunidade.
- **Celular modesto e rede instável**: os cards rotativos e a representação visual da
  comunidade não podem travar a página nem consumir dados desnecessariamente.
- **Cacheável e tolerante a pico** — dia de culminância e de batalha concentram acesso, e a
  vitrine é a superfície onde isso aparece.
- **Sem rastreador de terceiros**, inclusive de métricas: se houver medição de audiência, ela é
  agregada e sem identificador de visitante.
- **Acessibilidade digital**: contraste, alvos de toque grandes, leitura por voz e conteúdo
  legível sem depender da rotação dos cards.
- **Linguagem simples** em toda tela pública, inclusive nas mensagens de erro e de espera.
- **Indexável por buscadores** nas seções institucionais e de comunidade; a página individual
  de Guerreiro(a) **não é indexada**, para que a exposição não sobreviva à revogação.
- Idioma pt-BR; código aberto.

## 11. LGPD e proteção da criança

| Dado coletado                        | Finalidade                             | Base legal                   | Retenção                           | Quem acessa        |
| ------------------------------------ | -------------------------------------- | ---------------------------- | ---------------------------------- | ------------------ |
| Nenhum dado do visitante             | —                                      | —                            | —                                  | —                  |
| Dados da solicitação de participação | Avaliar quem pede para entrar          | consentimento                | até o desfecho e o registro dele   | gestão             |
| Dados da solicitação de dados        | Avaliar e registrar a entrega          | consentimento                | permanente, como prova do que saiu | gestão             |
| Avatar, nick e desempenho exibidos   | Reconhecimento público do Guerreiro(a) | consentimento do responsável | enquanto a autorização durar       | qualquer visitante |
| Séries do território exibidas        | Bem público e evidência sobre o lugar  | interesse público            | permanente, agregado               | qualquer visitante |

- **A vitrine não coleta nada de quem visita.** Sem login, sem cadastro, sem cookie de
  rastreio, sem perfilamento — e a área detalhada diz isso com todas as letras.
- **Exibição depende de autorização vigente**, concedida na App 07. Revogou, sai — e o endereço
  direto passa a responder "não encontrado".
- **Nunca por Guerreiro(a) no território**: o dado do lugar sai agregado até o bairro e sem
  código de coletor. Rua e abaixo só na entrega aprovada, que é anonimizada.
- **Sem canal de contato**, sem comentário e sem reação: a mediação adulto–criança não tem
  brecha aqui.
- **Sem publicidade e sem patrocínio**: nada é vendido nesta superfície no Ciclo 01, e o tema
  só volta como estudo, com as salvaguardas de plataforma usada por criança escritas antes.
- **Quem preencheu formulário não vira cadastro** e não recebe e-mail da plataforma no Ciclo
  01: o retorno é dado pelo contato que ele mesmo declarou.

## 12. Critérios de aceite e métricas

- A vitrine abre inteira sem login, e nenhuma tela oferece cadastro ou área restrita.
- Guerreiro(a) com autorização aparece em card, página e ranking; sem autorização, não aparece
  em nenhum dos três, nem por endereço direto.
- Revogada a autorização na App 07, o perfil some da vitrine na leitura seguinte e o endereço
  direto responde "não encontrado".
- Busca por nick inexistente e por nick sem autorização devolvem **a mesma resposta**.
- Repetir a busca por nick a partir da mesma origem produz espera crescente, sem CAPTCHA e sem
  pedir cadastro.
- O painel da comunidade mostra série agregada até o bairro; pedir granularidade menor pela
  rota pública é recusado com orientação de usar o formulário.
- Nenhuma tela pública exibe nick, avatar ou código de coletor junto de uma medição.
- Cada série exibida declara o que mede, cadência, período, origem e número de registros
  válidos.
- O painel de ODS agrega por comunidade e ciclo, destaca a meta 17.18 e registra a ressalva do
  ODS 18; nenhuma etiqueta aparece ligada a um Guerreiro(a).
- Formulário de participação enviado gera item na fila da App 03, com os cinco campos
  obrigatórios, e a tela informa os 7 dias.
- Formulário de dados enviado não devolve arquivo nem link: a tela declara a aprovação de Admin
  como condição.
- Toda página individual traz a chamada "Quero participar"; clicando nela, a tela seguinte não
  cita a pessoa que estava sendo vista e leva ao pré-cadastro da App 08.
- Pedir para favoritar chega à mesma porta; recusar devolve à navegação sem gravar nada.
- Card de Apoiador exibe avatar, nick e total de moedas na moldura comum; quem não teve aporte
  homologado não aparece.
- Depois de navegar e recarregar, a vitrine está idêntica à primeira visita: nenhum favorito,
  nenhuma preferência, nenhum dado no armazenamento local.
- Nenhuma tela exibe anúncio, peça patrocinada ou espaço reservado a anunciante.
- Auditoria da página confirma ausência de cookie e de requisição a rastreador de terceiros.

Hipóteses do Ciclo 01 (documento 10): este PRD **não sustenta hipótese própria** — ele é a
superfície onde o efeito de **H2** fica visível (só aparece quem teve autorização) e onde o
lastro de **H3** é publicado em moedas. A métrica que ele passa a permitir é a **cobertura de
ODS por comunidade e ciclo**, base do indicador de impacto do documento 04.

## 13. Decisões tomadas neste PRD

| Decisão                                                                  | Gravada em | Linha do doc 09                           |
| ------------------------------------------------------------------------ | ---------- | ----------------------------------------- |
| Saída pública agrega até o bairro; rua e abaixo só na entrega aprovada   | 02 §1      | Granularidade da saída pública            |
| Limite por origem com atraso progressivo nas rotas públicas, sem CAPTCHA | 03 §8      | Proteção das rotas públicas da vitrine    |
| Vitrine sem favoritos: o pedido vira convite a se cadastrar e apoiar     | 03 §8      | Favoritos apenas na App 08                |
| Novidade dos favoritos na App 08: cinco fatos, em destaque por 30 dias   | 03 §10     | O que conta como "novidade" dos favoritos |
| Chamada "Quero participar" em toda página individual                     | 03 §8      | Chamada "Quero participar" nos perfis     |
| Card de Apoiador com avatar, nick, moedas em destaque e moldura comum    | 11 §8.2    | Identidade pública do Apoiador            |
| Pré-cadastro do Apoiador, com aporte declarado e comprovante             | 02 §1      | Pré-cadastro do Apoiador                  |

Duas dessas decisões **restringem regras anteriores**: a saída pública ia até a rua, e a
vitrine tinha favoritos guardados no aparelho do visitante. A primeira foi propagada ao PRD-08,
que a aplicava, e aos documentos 02, 03 e 08; a segunda concentrou o acompanhamento na App 08 e
transformou a ação de favoritar em porta de entrada para o cadastro e o apoio.

Uma quinta decisão retirou a **publicidade** da lista de receitas (documento 04 §2) e a mandou
para estudo de ciclo futuro, mantendo a edição do conteúdo institucional como ato de Admin no
PRD-02. O PRD-01 ganhou a rota pública da solicitação de participação, que existia como
entidade e não como contrato.

## 14. Pendências que permanecem

- **Nota de transparência sobre IA**: texto final, localização exata e a conexão com a linha
  "Licenças" quanto a conteúdo gerado com auxílio de IA. Trava o `RF-03-48` no texto, não no
  desenho.
- **Formato de exportação e licença de uso do conjunto** entregue sob solicitação, e o critério
  que o Admin aplica ao aprovar ou recusar. O recorte de pesquisadores promete a licença que
  ainda não existe.
- **Agregação mínima dentro do bairro**, para comunidade com pouquíssimos coletores — o corte
  no bairro resolve a rua, não o caso extremo.
- **Nome do projeto e domínio próprio**: a vitrine é a primeira peça que depende da decisão
  entre Comunidade Game e Inova Comunidade.

## 15. Rastreabilidade

| Requisito               | Origem                                                         |
| ----------------------- | -------------------------------------------------------------- |
| `RF-03-01` a `RF-03-14` | 03 §8 (vitrine), 11 §§8.1, 8.2 (cards e páginas) e 03 §12      |
| `RF-03-55` a `RF-03-57` | 11 §8.2 (card e moldura do Apoiador) e 04 §2 (aporte)          |
| `RF-03-15` a `RF-03-21` | 02 §1 (série e granularidade) e 11 §8.3 (representação visual) |
| `RF-03-22` a `RF-03-24` | 04 §4 (Agenda 2030 e meta 17.18) e 11 §2.1 (etiqueta ODS)      |
| `RF-03-25` e `RF-03-26` | 03 §8 (três recortes de leitura)                               |
| `RF-03-27` a `RF-03-31` | 02 §1 (solicitação de participação, dados mínimos e prazo)     |
| `RF-03-32` a `RF-03-34` | 03 §12.3 (entrega sob solicitação aprovada)                    |
| `RF-03-35` a `RF-03-37` | 03 §8 (proteção das rotas públicas)                            |
| `RF-03-38` a `RF-03-44` | 03 §§8, 10 (chamada e sem favoritos) e 02 §1 (pré-cadastro)    |
| `RF-03-45` a `RF-03-49` | 03 §8 (institucional), 04 §1 (PIX e lastro) e 01 §7 (IA)       |
| `RF-03-50` e `RF-03-51` | 04 §2 (sem publicidade) e 03 §8 (sem rastreamento)             |
| `RF-03-52` e `RF-03-53` | 03 §12 (aviso de coleta e área detalhada)                      |
