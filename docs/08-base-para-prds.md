# 08 — Base para Elaboração de PRDs

> **Este é o único documento extenso entre os 01–13.** Ele estrutura o conteúdo do projeto
> como insumo direto para os PRDs (_Product Requirements Documents_): cada bloco abaixo é
> candidato a um PRD, com escopo, requisitos e questões em aberto que o PRD precisará
> responder. A rastreabilidade entre conceitos, documentos-fonte e PRDs está no documento 99.

## Visão de produto (comum a todos os PRDs)

- **Produto:** plataforma educacional gamificada open source para comunidades periféricas.
- **Primeira implantação (contexto de todos os PRDs):** Case 01 — Comunidade Guerreira
  Zeferina, Salvador (BA), **Ciclo 01 de ago a dez/2026**. O MVP do ciclo é: credenciamento de
  jogadores, cadastro da comunidade digital e **trilhas 1 e 2 em operação**. Todo PRD deve
  poder ser respondido com a pergunta _"isto é necessário para o Ciclo 01?"_ — o que não for, é
  onda seguinte.
- **Posicionamento:** educacional e _tech first_, com paralelos obrigatórios para outras áreas
  do conhecimento e para valores e temas necessários à sociedade (racismo, violência contra
  mulheres, identidade, povos originários).
- **Usuários:** Jogadores (crianças e jovens), Mestres, Apoiadores, Admins, Visitantes,
  Comunidades Virtuais.
- **Fora de escopo:** encaminhamento profissional. A plataforma forma repertório e habilidade;
  não intermedeia colocação no mercado.

### Restrições transversais (obrigatórias em todos os PRDs)

- Backend como API; rotas de consulta públicas sem autenticação; escrita autenticada.
- **Todas as aplicações desta etapa são Web Apps responsivos, Mobile First.** Não há aplicativo
  nativo nem aplicação construída sobre WhatsApp ou outra mensageria de terceiros.
- Frontends em domínios separados; código open source.
- Registro de custo e lastro de recursos em todas as ações.
- **Governança de personas:** só o **Jogador** tem autocadastro. **Mestres e Apoiadores são
  cadastrados exclusivamente por Admins**, com habilidade ou apoio comprovados por materiais ou
  artefatos publicados na plataforma. Pessoas e instituições podem **solicitar** inclusão como
  Mestre ou Apoiador pela vitrine — solicitação registrada não é cadastro, e a avaliação é
  sempre de um Admin. **Novos Admins são incluídos manualmente** por um Admin existente.
- **LGPD em todo o projeto:** jogadores representados por **avatares, nunca por imagens reais**.
  A **foto captada no onboarding** é dado sensível de finalidade única (registro de presença),
  com consentimento, minimização, criptografia, retenção definida e alternativa para quem
  recusar. **Adesão em duas etapas:** o cadastro livre (nome, data de nascimento ou idade, nick
  e características do avatar) já permite participar das atividades; a **divulgação
  pública do histórico e do perfil** exige autorização dos pais ou responsáveis. **Toda
  aplicação indica visualmente**, de forma discreta, o que coleta e quais são os direitos do
  usuário, com acesso a uma **área detalhada** sobre destino e uso de cada dado.
- **Coproprietariedade dos dados publicados:** em produção, a entidade responsável pela
  plataforma é coproprietária, com o jogador que gerou o dado; havendo monetização, ambos são
  remunerados.
- **Faixa etária dos jogadores: 6 a 16 anos**, com atividades em **níveis de dificuldade
  graduais** acessíveis independentemente da idade. A convivência entre idades é tratada com
  **papéis de mediação, nunca com segmentação por faixa**.
- **Protagonismo e autoria do jogador como requisito de produto:** criações originais com
  autoria creditada e vitrine pública; papéis ativos e crédito individual preservado nas
  equipes; **canal de sugestões do jogador** para a evolução contínua da plataforma.
- **Transparência sobre IA:** a plataforma declara publicamente que seus artefatos (código,
  documentação, conteúdo) são construídos com auxílio de IA, sob idealização e direção humanas.
- **Comunidade Virtual obrigatória:** criada **vazia por um Admin**, com **todo jogador
  vinculado a uma delas** no cadastro, pela **comunidade default** que o Admin define para o
  onboarding. Os dados de território são **temporais** e **guardados permanentemente com o
  jogador coletor identificado** (sem anonimização no armazenamento); a
  anonimização se aplica **na saída** — painéis públicos, exportações e pesquisas.
- **Toda trilha contém desafios de coleta de dados reais** e **termina em criação original**.
- Valores do projeto refletidos em conteúdo, conduta e representatividade.
- **Modelo de gamificação como fonte normativa:** anatomia da trilha, taxonomia de atividades,
  motor de pontuação, níveis, badges, recompensas e reflexos no ecossistema seguem o documento 11.
- **Mestres de qualquer área do conhecimento** — inclusive humanas, artes, esportes e cultura:
  nenhum modelo de dados ou fluxo pode pressupor habilidade técnica de TI.

### Aplicações desta etapa e seus PRDs

| Aplicação                                                    | PRD    |
| ------------------------------------------------------------ | ------ |
| **App 01** — Onboarding (áudio ou texto, cadastro, presença) | PRD-04 |
| **App 02** — Assistente por voz e Modo Ouvinte               | PRD-06 |
| **App 03** — Gestão administrativa                           | PRD-02 |
| **App 04** — Jogo em JavaScript                              | PRD-12 |
| **App 05** — Área do Jogador                                 | PRD-05 |
| **App 06** — Vitrine pública                                 | PRD-03 |
| **App 07** — Área dos pais e responsáveis                    | PRD-13 |
| **App 08** — Área do Apoiador                                | PRD-14 |
| **App 09** — Área do Mestre                                  | PRD-09 |

---

## PRD-01 — Backend API (núcleo)

**Escopo:** modelo de domínio e API pública/privada que sustenta todos os frontends.

**Requisitos:**

- Entidades: Jogador, Mestre, Apoiador, Admin, Comunidade Virtual, Poder, Trilha, Atividade,
  Aula/Agenda, Presença, Batalha, Equipe, Recurso, Recompensa, Ponto/Badge/Nível, Registro de
  dado do território, Pergunta de quiz, Partida de quiz, **Criação original do jogador**,
  **Sugestão ou proposta de evolução** e **Solicitação de participação como Mestre ou
  Apoiador**.
- Rotas de consulta abertas (vitrine, rankings, painéis de comunidade) sem autenticação.
- Suporte a múltiplos frontends e a aplicações de terceiros.
- Papéis e permissões: Admin (total), Mestre (conteúdo e lançamentos das suas atividades),
  Jogador (próprios dados), Visitante (leitura pública).
- Regra de negócio: **cadastro de Mestre e Apoiador restrito a Admin**, com anexos
  comprobatórios obrigatórios — currículo, portfólios, redes sociais e documentos externos —;
  **inclusão de Admin apenas por outro Admin**.
- Regra de negócio: **solicitação de participação** como Mestre ou Apoiador, aberta a pessoas e
  instituições pela rota pública da vitrine: gravada com data, dados de contato, pretensão
  (Mestre ou Apoiador), justificativa e status de avaliação; **não gera cadastro**.
- Regra de negócio: **Comunidade Virtual criada apenas por Admin**, nascendo vazia; **todo
  jogador tem vínculo obrigatório a exatamente uma**, atribuída pela **comunidade default do
  onboarding**, com histórico das transferências — o dado coletado pertence à comunidade
  vigente na data do registro.
- Regra de negócio: **equipe é grupo livre de até 5 pessoas**; um jogador pode integrar
  **várias equipes** e pontua em todas as atividades em que participa; a composição admite **no
  máximo 1 familiar com 17 anos ou mais**, conforme a atividade, o desafio ou a batalha
  determinar. Equipes são cadastradas por Admin.
- Regra de negócio: **coproprietariedade dos dados publicados** entre a entidade responsável
  pela plataforma e o jogador que gerou o dado; monetizados, o resultado é rateado **50% / 50%**,
  com a parte do jogador paga **ao responsável legal**.
- Regra de negócio: **registro de dado do território é uma série temporal** — cadência, janela
  de validade, jogador coletor e comunidade. **Série ativa gera pontos recorrentes; série
  interrompida cessa o cômputo**, sem perda dos pontos já creditados.
- Regra de negócio: **dados do território têm guarda permanente e mantêm o vínculo com o
  jogador coletor**, inclusive após o encerramento do vínculo dele com o projeto. A anonimização
  é aplicada **na saída**.
- Regra de negócio: atividade só é agendável e realizável com recursos providos (lastro).
- Regra de negócio: pontos de habilidade só vêm de atividades realizadas propostas por Mestres.
  O **App 04 consome pontos e não os gera**.
- Regra de negócio: **desafio extra** exige validação do Mestre da trilha **e aprovação de um
  Admin**; gera **pontos extras** computados isoladamente, nas duas modalidades — **aberto** (a
  todos, com quantidade de recompensas declarada, uma ou várias, por ordem de conclusão) e
  **direcionado** (a um jogador específico, único elegível à recompensa, com justificativa do
  vínculo registrada e aprovada).
- Entidades e permissões da **área do responsável**: vínculo responsável ↔ jogador,
  consentimentos versionados com data e hora, solicitações com protocolo e status.
- Resultados de atividade: realizada / com mérito / mérito extra por auxílio; pontuação negativa
  por má conduta.
- Regra de negócio: **níveis 1 a 5 por trilha ou poder**; a conclusão do Nível 5 marca o jogador
  como **Mestre Aprendiz**, apto ao treinamento de multiplicador e ao voluntariado nos pontos de
  apoio.
- **Poder do Território** no catálogo de poderes: progressão e badges próprios por sustentar
  séries de coleta.
- Regra de negócio: **criação original com autoria creditada** — a criação carrega o autor ou
  autores por toda a vida do registro, individual ou em equipe (com o papel de cada membro), e
  alimenta o portfólio público quando autorizada.
- Regra de negócio: **sugestões e propostas de evolução** — registradas pelo jogador (App 05),
  pelo responsável (App 07), pelo Apoiador (App 08) e pelo Mestre (App 09), com autor, persona,
  data e status de avaliação pela gestão, em fila única.

**Questões em aberto:** estratégia de autenticação; versionamento da API; multi-tenant por
comunidade (uma instância nacional ou uma por comunidade?).

**Fontes:** docs 02, 03, 04, 11.

## PRD-02 — App 03: Frontend de Gestão

**Escopo:** aplicação autenticada da gestão — Admins e, conforme permissão, Mestres. A
**fronteira com a App 09** é o critério: aqui ficam cadastros, aprovações de Admin, painéis do
dia e filas; a autoria de trilhas e os lançamentos das atividades do próprio Mestre ficam lá.

**Requisitos:** CRUDs de mestres, poderes, jogadores, apoiadores, admins, equipes e comunidades
virtuais; **criação das Comunidades Virtuais — exclusiva de Admin, nascendo vazias — e gestão do
vínculo e transferência de jogadores entre comunidades**; **definição da comunidade default do
onboarding e liberação do App 01**, sem a qual a aplicação de onboarding não opera; **cadastro
de equipes** conforme o plano de aulas e a formação livre dos jogadores, com a composição
permitida pela atividade (só jogadores ou com no máximo 1 familiar de 17 anos ou mais);
cadastro de Mestres e Apoiadores com upload dos artefatos comprobatórios — **currículo,
portfólios, redes sociais, documentos externos e termos de doação**; **fila de solicitações de
participação como Mestre ou Apoiador** vindas do formulário público da App 06, com avaliação,
status e registro de quem tratou; **cadastro dos locais do território e fila de solicitações de
novo local** vindas da App 05, com alerta das que estão em aberto; inclusão manual de Admins;
cadastro de atividades (pontuação, recompensas, recursos necessários); **cadastro de desafios de
coleta com cadência e regra de pontuação recorrente**; agenda de aulas on-line e presenciais;
lançamento de atividades realizadas (data, mentores, jogadores, resultados); **entradas
manuais** — presença, infrações ocorridas nas aulas e pontuação extra a quem ajudou o colega;
conferência e ajuste de presenças vindas do onboarding; gestão de recursos (aportes e consumo);
**painéis do dia** com a visão operacional do encontro (presenças, atividade prevista, recursos
providos, lançamentos pendentes, **saldo de kits MDF**); **operação do Quiz ao Vivo**;
**controle do acervo didático** — entrega dos exemplares da linha Alpha na abertura da trilha
(baixa definitiva), tombamento e empréstimo de bancada dos exemplares permanentes, estado de
conservação e devoluções pendentes no painel do dia; **validação de desafios extras propostos
por Apoiadores** pelo Mestre da trilha e aprovação caso a caso por Admin; **fila de solicitações
dos responsáveis** vindas da App 07 (autorizações, revogações, recusas, acesso, correção e
exclusão de dados), com registro de quem tratou e quando; **fila única de avaliação das
sugestões e propostas** vindas das Apps 05 (jogador), 07 (responsável), 08 (Apoiador) e 09
(Mestre), com status e retorno a quem propôs.

**Painel do dia em encontro assíncrono:** como os jogadores chegam e avançam em ritmos
diferentes, o painel precisa mostrar em tempo real **quem já chegou, em que ponto de trilha cada
equipe está, quem está aguardando aparelho e quais lançamentos ainda faltam** — é o instrumento
que substitui o controle visual de uma turma em bloco.

**Questões em aberto:** quem pode lançar pontuação negativa e com que auditoria; trilha de
auditoria das ações de Admin; se o Quiz ao Vivo é módulo desta aplicação ou aplicação separada.

**Fontes:** docs 03, 04, 05.

## PRD-03 — App 06: Vitrine pública

**Escopo:** site público, sem login, em domínio próprio.

**Requisitos:** seções Jogadores, Poderes, Mestres, Batalhas, Apoiadores e Comunidades Virtuais
com cards individuais; **página individual detalhada** aberta a partir de cada card — jogador,
Mestre, poder, apoiador e comunidade —, com a composição do documento 11; cards rotativos de
jogadores (rotação a cada 5 s); painel público de dados por comunidade **em série histórica**;
"Quem somos" e "Contatos" editáveis; seção **"Como
apoiar"** com a chave PIX do projeto; espaço de **publicidade** fora das áreas de uso das
crianças; vídeo de apresentação (Susy, Otávio, Rôbróders, prof. Carlos Trenell); estética de
comunidade (grafite, cores, imagens do território); **portfólio de criações originais** dos
jogadores autorizados, com o nick dos autores; **nota de transparência sobre IA** nas seções
institucionais.

**Formulário de solicitação de participação:** pessoas e instituições
interessadas em participar como **Mestre ou Apoiador** preenchem um formulário público —
identificação, contato, pretensão, área de habilidade ou tipo de apoio, links comprobatórios e
justificativa. A solicitação é **gravada em banco de dados** e disponibilizada para avaliação
por um Admin na App 03 (PRD-02). O envio **não cria cadastro nem acesso**; a resposta é
registrada com status.

**Definições vigentes:** cards de jogadores exibem **apenas** avatar (nunca imagem real), nick,
badges, poderes adquiridos e desempenho na plataforma; **sem links para redes sociais dos
jogadores nem contato direto** — a página individual do jogador segue a mesma restrição. A
vitrine exibe **somente jogadores cujo responsável autorizou a divulgação**; jogadores sem
autorização participam das atividades mas não aparecem publicamente. As páginas de **Mestres e
Apoiadores** exibem **currículo, portfólios, redes sociais e documentos comprobatórios
externos**. Aportes aparecem em **moedas da plataforma**, nunca em reais.

**Fontes:** docs 02, 03, 04, 11 (composição dos cards, páginas individuais e representação
visual da comunidade).

## PRD-04 — App 01: Onboarding (cadastro e registro de presença)

**Escopo:** Web App responsivo Mobile First que cadastra novos jogadores e registra a presença
dos já cadastrados, por **áudio ou texto**, com IA.

**Requisitos:**

- Tela inicial em que o usuário escolhe: **começar por áudio** ou **começar por texto (chat)**.
- Interação cognitiva conduzida por **IA**, tolerante a respostas fora de ordem, capaz de
  repetir e confirmar dados.
- Captação e reprodução de áudio via `navigator.mediaDevices.getUserMedia`, com reconhecimento
  e síntese de fala.
- Captura da **imagem do jogador** pela câmera do dispositivo.
- **Novo jogador:** salvar nome, nick, data de nascimento ou idade, características do avatar
  e foto. O jogador fica **ativo** ao final, sem exigir autorização do responsável nesta etapa.
- **Vínculo à comunidade:** atribuído automaticamente pela **comunidade default** que o Admin
  define na App 03 — o jogador **não informa a comunidade**, o que encurta a conversa de
  cadastro.
- **Disponibilidade condicionada:** o App 01 só abre depois que um Admin define a comunidade
  default e **libera o funcionamento da aplicação** na App 03.
- **Jogador já cadastrado:** capturar imagem, comparar com a base **somada ao nick informado** e
  **registrar presença automaticamente** na atividade — presencial ou on-line.
- Fallback manual (Admin ou Mestre confirma) quando a identificação falhar.
- Operação com rede instável: fila local e sincronização posterior.
- Registro de presença de jogador conhecido em poucos segundos.

**Requisitos de proteção de dados (obrigatórios):** finalidade única da foto (presença);
consentimento informado do responsável registrado; preferência por _template_ biométrico não
reversível; criptografia e acesso auditado; prazo de retenção com exclusão automática;
**alternativa de presença sem biometria** para quem recusar.

**Questões em aberto:** provedor de IA e de reconhecimento facial (custo, privacidade,
processamento no dispositivo × nuvem); política de retenção em números; roteiro exato da conversa
de cadastro.

**Fontes:** docs 02, 03, 06.

## PRD-05 — App 05: Área do Jogador (jornada gamificada)

**Escopo:** experiência logada do jogador, com **guia e apoio nas trilhas** — qual é o próximo
ponto, o que precisa ser feito, o que já foi conquistado e o que está bloqueado.

**Requisitos:** escolha de poder; trilhas com desbloqueio por quiz ou desafio, seguindo a
anatomia e o motor de pontuação do documento 11; desafios semanais (on-line 10 pts, presencial
10 pts, equipe 10 pts, equipe com familiar 20 pts); **desafios extras propostos por Apoiadores**
— abertos ou direcionados —, vinculados à trilha em andamento, com pontos extras e recompensa
em quantidade declarada; **equipes** — grupos livres de até 5, participação em mais de uma, com
a pontuação de todas as atividades em que colaborar; **séries de coleta de dados do território**
— próxima medição, histórico do que já foi registrado, situação da série (ativa ou interrompida)
e pontos que ela está rendendo; ranking; troca de pontos por recompensas; pedido de ajuda para
atividades escolares; níveis 1–5 (assíduo → **Mestre Aprendiz**); badges por trilha e por poder;
**portfólio de criações originais do jogador**, com autoria creditada; **canal de sugestões**,
com acompanhamento do status de avaliação.

**Autonomia no encontro assíncrono:** a App 05 é o que permite ao jogador saber **o que fazer em
seguida sem depender do Mestre**. Precisa funcionar em **aparelho compartilhado do ponto de
apoio** (troca rápida de sessão) e mostrar com clareza o próximo ponto e o que está bloqueado.

**Requisitos adicionais:** estado de **perfil público** desbloqueado apenas com autorização do
responsável; representação exclusivamente por avatar; desafios com níveis de dificuldade
graduais acessíveis a toda a faixa de 6 a 16 anos; **acervo do jogador** — o livro da linha Alpha
recebido na abertura da trilha (que é dele, sem devolução) e os exemplares permanentes em uso de
bancada, com a **ficha de vida do livro** e o badge **Guardião do Acervo**.

**Questões em aberto:** tabela de pontos das recompensas (os valores atuais são apenas
sugestão); mecânica antifraude de pontos; acessibilidade para quem só tem celular, com aparelho
compartilhado ou sem dados móveis.

**Fontes:** docs 02, 03, 05, 11.

## PRD-06 — App 02: Assistente por voz e Modo Ouvinte

**Escopo:** Web App de áudio nos moldes do Robô Educa — **JavaScript no frontend + IA no
backend** — com dois modos de operação.

**Requisitos:**

- **Modo Conversa:** interação educacional por voz ("converse com seu robô") — quiz, explicação
  de conceitos e apoio às atividades escolares.
- **Modo Ouvinte:** a aplicação acompanha o que é falado durante a aula e, **quando acionada**,
  opina sobre o tema em discussão ou responde a perguntas dirigidas a ela.
- Captação e reprodução de áudio via `navigator.mediaDevices.getUserMedia`; reconhecimento de
  fala e síntese de voz em pt-BR.
- Ativação do Modo Ouvinte pelo Mestre, com **indicação visível e permanente** de que está ativo
  e desligamento a qualquer momento.
- **Sem gravação persistente do áudio da turma**; retenção mínima e definida da transcrição
  estritamente necessária.
- Aviso prévio a jogadores e responsáveis, com **direito de recusa e alternativa equivalente**.
- Filtros de segurança de conteúdo no nível mais restritivo.
- Captação de perfil para personalização (PRD-11).
- Registro de dados do território **por voz**, alimentando as séries da Comunidade Virtual sem
  exigir digitação.

**Questões em aberto:** provedor e custo do modelo de IA; processamento de áudio no
dispositivo × nuvem; base legal e prazo de retenção da transcrição de aula com menores;
critério de acionamento do Modo Ouvinte (palavra-chave, botão do Mestre ou ambos);
comportamento em salas barulhentas.

**Fontes:** docs 03, 06.

## PRD-07 — Economia de Recursos e Transparência (ledger)

**Escopo:** livro-razão de recursos aportados e consumidos; "Poder Econômico".

**Requisitos:** todo custo de toda ação atribuído a um personagem; atividade condicionada a
lastro; tipos de recurso: hora-aula, lanche, recompensas, insumos, cloud, serviços;
visibilidade pública da riqueza movimentada.

**Moeda da plataforma como unidade de conta:** todo aporte — dinheiro, material ou serviço — é
convertido em **moedas**, com **1 moeda = R$ 100,00**. O ledger guarda as duas
faces (moedas e valor de origem), mas **toda saída pública exibe apenas moedas**: é plataforma
educativa, com público infantil e terceiros sem familiaridade com custeio, e o que se quer
mostrar é o **montante relativo entre apoiadores**, nunca o valor monetário isolado.

**Coproprietariedade dos dados publicados:** a entidade responsável pela plataforma e o jogador
que gerou o dado são coproprietários; havendo monetização, o ledger registra o rateio **50% /
50%**, com a parte do jogador paga **ao responsável legal**.

**Recursos duráveis (patrimônio) e empréstimo:** além dos consumíveis, o ledger precisa tratar
material que **não se consome no uso e é reaproveitado a cada turma** — o caso concreto é o
acervo de 298 livros doado pelo Goethe-Institut:

- Registro por **exemplar tombado**: título, número de tombo, ponto de apoio, estado de
  conservação e movimentações entre pontos.
- **Empréstimo e devolução** vinculados a jogador e a módulo ou trilha, com histórico de quem
  usou cada exemplar e devoluções pendentes no painel do dia.
- O aporte credita o Poder Econômico do Apoiador **uma única vez**, sem baixa por consumo.
- Suporte ao **regime misto**: linha Alpha doada ao jogador na abertura da trilha (baixa
  definitiva, tratada como recompensa entregue), linha Include I como patrimônio permanente e
  kits MDF como consumível de atividade, com saldo de estoque.
- **Perda ou dano não gera débito para o jogador nem para a família**: gera uma **necessidade de
  reposição** a ser aportada por Apoiador.
- **Doações em espécie (PIX)** registradas como aporte financeiro do doador, com comprovante
  anexado.

**Desafios extras e rastreio de efetividade:** o ledger precisa registrar não só o aporte, mas
**o que aconteceu por causa dele**:

- **Desafio extra** como entidade: Apoiador proponente, trilha vinculada, Mestre validador,
  **Admin aprovador**, recompensa oferecida, **quantidade disponível**, critério de atribuição,
  **pontos extras**, período de vigência, **modalidade (aberto ou direcionado)** e — no
  direcionado — jogador destinatário e justificativa do vínculo aprovada.
- Recompensa extra **creditada no histórico do Apoiador** e computada no Poder Econômico, com
  lastro exigido **antes** da publicação do desafio.
- **Realizações dos jogadores** naquele desafio vinculadas ao histórico do Apoiador — base dos
  relatórios de **efetividade do apoio ao longo do tempo**.
- Nenhum dado de contato de jogador exposto ao Apoiador: o relatório é **agregado e por avatar**.

**Questões em aberto:** valoração da hora-aula, do acervo, dos kits e das camisas doados —
critério que define a conversão desses aportes em moedas; relatórios públicos por atividade,
comunidade e provedor; **formato do relatório de efetividade** entregue ao Apoiador;
periodicidade e forma de pagamento do rateio da monetização dos dados.

**Fontes:** docs 04, 05.

## PRD-08 — Comunidades Virtuais e dados do território

**Escopo:** representação digital da comunidade real em que o jogador vive, construída pelos
próprios jogadores — a base _Data Driven_ da plataforma.

**Requisitos:**

- **Criação exclusiva por Admin**, com a comunidade nascendo **vazia** (nome, localização,
  granularidade), e **marcação de qual delas é a comunidade default do onboarding**.
- **Vínculo obrigatório do jogador a uma comunidade**, atribuído no onboarding pela comunidade
  default e alterável apenas pela gestão, com data da mudança preservada.
- A comunidade virtual **existe na medida em que dados reais são registrados**.
- Atividades de coleta: temperatura local, precipitação pluviométrica, coleta de resíduos,
  buracos na via, iluminação, trânsito, transporte público, fotos, vídeos e memórias.
- **Toda trilha tem ao menos um desafio de coleta.**
- **Série temporal como unidade do modelo**: cadência declarada, registros datados, jogador
  coletor, comunidade e estado da série (ativa / interrompida / retomada).
- **Pontuação recorrente enquanto a série durar** e cessação do cômputo na interrupção, sem
  perda dos pontos já creditados.
- **Guarda permanente** dos registros **com o jogador coletor identificado** — o vínculo autoria
  ↔ registro não é removido nem anonimizado no armazenamento.
- **Anonimização na saída**: exportações, painéis públicos, pesquisas e entregas a instituições
  recebem dados agregados e anonimizados.
- **Granularidade hierárquica**: comunidade → bairro → rua → condomínio → bloco → quadra.
- **Locais cadastrados previamente por Admin**; o jogador seleciona o local do dado e, faltando
  um, solicita a inclusão pela App 05. A solicitação é aprovada pelo **Mestre da trilha** ou por
  um **Admin**, ambos alertados das solicitações em aberto.
- Cada registro alimenta e "constrói" visualmente a comunidade digital.
- **Poder do Território**: as séries sustentadas alimentam a progressão e os badges desse poder.
- Painéis públicos por comunidade; dados como insumo para tomada de decisões por moradores,
  associações, escolas, poder público e pesquisas.
- Exportação e API aberta dos dados agregados e anonimizados.

**Questões em aberto:** fontes e sensores (registro manual × sensor construído pelo jogador ×
API pública); curadoria e **veracidade dos dados**; cadência e valor em pontos por tipo de
coleta; **janela de tolerância** antes de considerar a série interrompida; teto de pontos por
período; georreferenciamento sem expor endereço de criança; tecnologia de armazenamento das
séries temporais.

**Fontes:** docs 02, 03, 11.

## PRD-09 — App 09: Área do Mestre (autoria e operação)

**Escopo:** Web App autenticado dos Mestres cadastrados — onde o Mestre **cria** trilhas,
conteúdos, quizzes e desafios e **conduz** as suas atividades. É a bancada de trabalho de quem
ensina; a gestão administrativa segue na App 03.

**Requisitos de operação do Mestre:**

- **Minhas atividades e turmas**: lançamento de resultados, presenças e méritos das atividades
  que ele propôs — e apenas delas.
- **Validação pedagógica dos desafios extras** propostos por Apoiadores para as suas trilhas,
  etapa obrigatória antes da aprovação do Admin.
- **Aprovação das solicitações de novo local** dos jogadores das suas trilhas, com alerta das
  solicitações em aberto.
- **Publicação dos artefatos comprobatórios** da sua habilidade, com currículo, portfólio e
  redes sociais, que alimentam a sua página na vitrine (PRD-03).
- **Registro de propostas** de evolução da plataforma, na mesma fila da gestão que recebe as
  sugestões dos jogadores.
- **Sem cadastro pelo app**: o cadastro de Mestre segue exclusivo de Admin; quem ainda não é
  Mestre usa o formulário de solicitação da vitrine.

**Requisitos de autoria:** trilhas seguindo a **anatomia formal do documento 11** — em modelo **agnóstico
de área do conhecimento**, apto a trilhas de humanas, artes, esportes e cultura tanto quanto às
técnicas —, incluindo a **paginação da trilha pelas etapas do ciclo**; conteúdo próprio e de
terceiros; quiz ou desafio para desbloqueio; **publicação dos artefatos que comprovam a
habilidade do Mestre**; catálogo inicial de poderes: **IA/Robótica e Poder do Território** nesta
etapa — Redes, Soft Skills, PNED/BNCC, Rima e Capoeira ficam para ciclo futuro; **banco de
perguntas do Quiz ao Vivo** cadastrado aqui pelo Mestre curador, com a partida conduzida na
App 03; paralelos obrigatórios com outras áreas do conhecimento e com os valores do projeto.

**Coleta de dados como requisito de toda trilha:** a ferramenta deve **impedir a publicação de
uma trilha sem ao menos um desafio de coleta de dados reais**. O Mestre define, no desafio, **o
que se mede, com que cadência e por quanto tempo** — os três parâmetros que a série temporal
precisa para existir e para pontuar de forma recorrente.

**Criação original como fechamento de toda trilha:** a culminância é a apresentação pública de
uma criação original do jogador ou da equipe, com autoria creditada. **[Proposta]** Tratar como
regra dura na ferramenta, no mesmo padrão da coleta de dados: impedir a publicação de uma trilha
cuja culminância não preveja a criação original.

**Primeiras trilhas (conteúdo já existente):** Robô Educa (1ª) e Batalha de Laser (2ª), ambas de
autoria do Mestre fundador. São o conteúdo de validação do módulo: se a ferramenta modela essas
duas, modela as demais.

**Material de apoio impresso:** o modelo de trilha precisa suportar **bibliografia de apoio por
ponto de trilha**. Requisitos: vincular um ponto de trilha a **título e capítulo recomendados**;
indicar ao jogador se há **exemplar disponível no seu ponto de apoio**; e creditar o **Apoiador
que forneceu o material** onde ele é indicado.

**Questões em aberto:** formato dos conteúdos (vídeo, texto, interativo); revisão e curadoria
pedagógica; licença dos conteúdos (Creative Commons?); forma de acesso do Mestre e permissões
que ele mantém na App 03.

**Fontes:** docs 02, 03, 05, 06, 07, 11.

## PRD-10 — Batalhas e eventos presenciais

**Escopo:** cadastro, operação e registro de batalhas (disputas de ideias e realizações).

**Requisitos:** batalhas presenciais e de projetos; culminância; estatísticas de partida (ex.:
telemetria do Nexus na Batalha de Laser); resultados alimentando ranking e portfólio; integração
Nexus → API **[Proposta]**, seguindo o padrão de integração de batalhas físicas com o backend.
Batalhas são marcos de trilha de **qualquer área** (disputa de laser, batalha de rima, roda de
capoeira), não apenas técnicas.

**Fontes:** docs 02, 07, 11.

## PRD-11 — Personalização por IA

**Escopo:** captação de perfil e adaptação de conteúdo.

**Requisitos:** a plataforma capta o perfil conforme o aluno interage e entrega informação
personalizada; usa habilidade que o aluno já possui para ensinar outros assuntos
(interdisciplinaridade); filtros de segurança de conteúdo no nível mais restritivo em toda
interação com crianças.

**Fora desta etapa:** a visão computacional aplicada à análise de movimentos de capoeira
(captação sugerida com MediaPipe, TensorFlow como alternativa para classificar os movimentos)
acompanha a trilha de Capoeira, que fica para ciclo futuro.

**Questões em aberto:** modelo e stack de IA; limites éticos e LGPD para perfis de menores;
explicabilidade para responsáveis.

**Fontes:** docs 02, 03.

## PRD-12 — App 04: Jogo em JavaScript

**Escopo:** jogo executado no navegador, construído sobre a **base de personagens da
plataforma**.

**Requisitos:** uso dos avatares, poderes, badges e níveis já conquistados como elementos do
jogo — a composição dos cards e o contrato do jogo com o motor (leitura de progresso + débito de
pontos, nunca crédito) seguem o documento 11; representação exclusivamente por **avatar, nunca
por imagem real**; código aberto e legível, apto a virar conteúdo de trilha do Poder da IA e
Robótica — **alterá-lo é atividade de trilha**; execução em navegador de celular modesto e
tolerância a rede instável.

**Definição vigente — o jogo consome pontuação, não a gera.** Os pontos vêm das atividades
propostas pelos Mestres e da coleta de dados do território. Em termos de API: o App 04 tem
**acesso de leitura ao progresso e de débito de pontos**, e nenhum endpoint de crédito — o que
elimina, por construção, a fraude por automação de cliques.

**Sugestão técnica:** engine **Phaser.js** — jogos 2D em JavaScript rodando no próprio
navegador, sem instalação, com desempenho adequado a aparelhos modestos e código legível o
bastante para virar material de trilha.

**Questões em aberto:** gênero e mecânica do jogo; o que exatamente os pontos compram dentro do
jogo; modo offline; multiplayer local nas aulas presenciais.

**Fontes:** docs 03, 11.

## PRD-13 — App 07: Área dos pais e responsáveis

**Escopo:** Web App autenticado dos pais e responsáveis, canal oficial da plataforma com a
família. Substitui a comunicação por mensageria de terceiros, fora do escopo desta etapa.

**Requisitos:**

- **Vínculo responsável ↔ jogadores**, conferido por Admin; o responsável só enxerga os
  jogadores sob sua responsabilidade.
- **Evolução do jogador**: presença, atividades realizadas, pontos, poderes, badges, nível e
  progresso nas trilhas.
- **Autorização de divulgação pública** do histórico e do perfil — concessão e **revogação**,
  com efeito imediato na vitrine e nos rankings públicos.
- **Direitos de recusa** exercíveis a qualquer tempo: foto de presença (PRD-04), Modo Ouvinte em
  sala (PRD-06) e uso de imagem em vídeos e fotos de eventos — **sempre com alternativa
  equivalente**, nunca com exclusão da atividade.
- **Transparência de dados**: quais dados da criança estão armazenados, para que servem, por
  quanto tempo ficam e **quem os acessou**.
- **Solicitações com protocolo e status**: acesso, correção, exclusão e esclarecimentos —
  encaminhadas à fila de atendimento da App 03 (PRD-02).
- **Limite explícito do pedido de exclusão**: os registros de dados do território têm guarda
  permanente com autoria preservada e **não são apagados**; a tela e o termo precisam dizer isso
  antes do aceite.
- **Termos e consentimentos versionados**, com data e hora e histórico consultável, incluindo a
  declaração de **coproprietariedade dos dados publicados** e o que ela implica em caso de
  monetização.
- **Registro de propostas** de evolução da plataforma pelo responsável, com acompanhamento do
  status, na mesma fila da gestão que recebe as sugestões dos jogadores.
- **Linguagem simples**, no mesmo padrão exigido da política de privacidade.
- **Sem qualquer canal com Apoiadores ou terceiros.**

**Por que é MVP e não onda seguinte:** a hipótese **H2** do Ciclo 01 mede exatamente quantos
responsáveis tomam conhecimento do tratamento de dados e aceitam os termos. Sem esta aplicação,
H2 não é mensurável — é anedota.

**Questões em aberto:** login próprio do responsável × vínculo ao cadastro do jogador; prazos
formais de resposta; notificação ativa (e-mail) além da consulta no Web App; como atender
responsável sem smartphone ou sem e-mail.

**Fontes:** docs 02, 03, 10.

## PRD-14 — App 08: Área do Apoiador

**Escopo:** Web App autenticado dos Apoiadores já cadastrados por Admin — canal próprio de
quem sustenta o projeto, sem nenhum contato com jogadores ou famílias.

**Requisitos:**

- **Meus aportes**: histórico do que aportou, em **moedas da plataforma**, e Poder Econômico
  acumulado; leitura do mesmo ledger do PRD-07, sem edição.
- **Proposição de desafios extras** — abertos ou direcionados —, com recompensa, quantidade
  declarada, período e, no direcionado, destinatário e justificativa do vínculo. O
  acompanhamento mostra o estado no fluxo: validação do Mestre da trilha → aprovação de Admin
  → publicado, com **lastro exigido antes da publicação**.
- **Relatório de efetividade** dos desafios propostos, **agregado e por avatar** — nunca com
  dado de contato ou identificação de jogador.
- **Envio de documentos comprobatórios** — currículo, portfólio, redes sociais, termos de
  doação e comprovantes —, que um Admin anexa ao cadastro e que alimentam a página pública do
  Apoiador na vitrine (PRD-03).
- **Registro de propostas** de evolução da plataforma, com acompanhamento do status, na mesma
  fila de avaliação da gestão que recebe as sugestões e propostas das Apps 05, 07 e 09.
- **Sem cadastro pelo app**: quem ainda não é Apoiador usa o formulário de solicitação da
  vitrine; o cadastro segue exclusivo de Admin.

**Questões em aberto:** forma de acesso e autenticação do Apoiador; se instituição tem mais de
um usuário no mesmo cadastro; periodicidade do relatório de efetividade.

**Fontes:** docs 03, 04, 12.

---

## Ordem de elaboração

Os PRDs são escritos em cinco ondas, um de cada vez, na sequência abaixo. A situação de cada
um está na página de PRDs; o mapa de arquivos e dependências, no documento 99.

| Onda | PRDs, em ordem                         | Por que nesta ordem                                                                                                |
| ---- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 1    | PRD-08, PRD-07, PRD-01                 | Território e ledger definem as entidades que o Backend API consolida — o PRD-01 escrito antes teria de ser refeito |
| 2    | PRD-02, PRD-04                         | O App 01 não opera enquanto um Admin não definir a comunidade default e liberar a aplicação na App 03              |
| 3    | PRD-09, PRD-05                         | Sem autoria de trilha não há o que a Área do Jogador guie; as trilhas 1 e 2 são o teste do modelo de autoria       |
| 4    | PRD-13, PRD-03                         | A vitrine só exibe jogador cujo responsável autorizou, e a autorização nasce na App 07                             |
| 5    | PRD-06, PRD-14, PRD-10, PRD-12, PRD-11 | Dependem de decisões ainda em aberto ou de fluxos que só existem depois das ondas anteriores                       |
