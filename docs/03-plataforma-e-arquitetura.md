# 03 — Plataforma e Arquitetura

## 1. Princípios de arquitetura

1. **Backend em forma de API** — o backend deve funcionar como API, de modo que os mais
   diversos formatos de frontend **e aplicações de terceiros** possam acessá-lo.
2. **Rotas de consulta abertas** — leituras públicas (vitrine, rankings, batalhas) não
   exigem autenticação. Escrita e gestão exigem.
3. **Frontends independentes** — os frontends terão **domínios diferentes** e evoluem de
   forma desacoplada do backend.
4. **Open Source** — todo o código-fonte é aberto, para permitir replicação por qualquer
   comunidade ([05-implantacao-e-operacao.md](05-implantacao-e-operacao.md#10-replicabilidade)).
5. **Registro de custos em tudo** — toda ação com custo (aula, lanche, hospedagem,
   prestadores de serviço) é computada e atribuída a um personagem; a arquitetura precisa
   suportar esse livro-razão desde o início
   ([04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md)).
6. **Dados do território como cidadão de primeira classe** — a plataforma é também uma
   base *Data Driven* das comunidades. **Todo jogador é vinculado a uma Comunidade Virtual**
   e o modelo de dados precisa acomodar **séries temporais georreferenciadas** desde o
   início, com **guarda permanente** dos dados coletados
   ([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)).
7. **Web App responsivo, Mobile First** — nesta etapa, **toda** aplicação é entregue como
   Web App responsivo projetado primeiro para o celular. Sem aplicativos nativos e sem
   aplicações construídas sobre plataformas de mensageria de terceiros (§2).

**[Proposta]** Documentar a API com OpenAPI/Swagger desde o primeiro endpoint — é
condição prática para que "aplicações de terceiros" e novos frontends realmente surjam em um
projeto open source.

## 2. Canais / Meios de acesso

> **Definição vigente desta etapa:** **todas as aplicações serão desenvolvidas como Web Apps
> responsivos, no formato *Mobile First***. Não há, nesta etapa, desenvolvimento de
> aplicações ou de recursos sobre WhatsApp, nem aplicativos nativos (Android/iOS). O
> navegador do celular é a plataforma-alvo; telas maiores são atendidas pela mesma
> aplicação responsiva.

| Canal | Uso |
|---|---|
| **Web App responsivo (Mobile First)** | Canal único de todas as aplicações: onboarding, assistente por voz, gestão, jogo, área do jogador, vitrine e área dos responsáveis |
| **Smartphone / tablet** | Dispositivo primário de acesso — é para ele que as telas são projetadas |
| **PC / Notebook** | O mesmo Web App em telas maiores; uso típico da gestão |
| **Embarcados** | Raspberry Pi; NodeMCU (ex.: acender LEDs por comandos de voz); vestíveis. São o **hardware das atividades**, não um canal de acesso à plataforma ([07-batalha-de-laser.md](07-batalha-de-laser.md)) |
| **Redes sociais** | Presença institucional e divulgação do projeto — não são canal de uso da plataforma |

O conceito **"Converse com seu robô"** perpassa os dispositivos: o robô/assistente do aluno
deve estar acessível a partir de qualquer navegador — smartphone, tablet ou computador — e
conversar com os dispositivos embarcados construídos nas oficinas
([06-robo-educa.md](06-robo-educa.md)).

Formato único de entrega: **uma base de código, sem loja de aplicativos, sem atualização
pelo usuário e sem tráfego de dados de crianças por plataformas de terceiros** — coerente com
a regra de LGPD em todo o projeto (§10).

### 2.1 Aplicações a serem desenvolvidas

**Sete aplicações** compõem o escopo desta etapa. Todas são **Web Apps responsivos, Mobile
First**, consumindo o mesmo Backend API (§1).

| # | Aplicação | Público | Especificação |
|---|---|---|---|
| **App 01** | **Onboarding** — escolha entre áudio ou texto, cadastro de novo jogador e registro de presença | Jogadores (na chegada da aula) | §3 |
| **App 02** | **Assistente por voz** — ChatBot de áudio nos moldes do Robô Educa, com **Modo Ouvinte** | Jogadores e Mestres (durante a aula) | §4 e [06-robo-educa.md](06-robo-educa.md) |
| **App 03** | **Gestão administrativa** — CRUDs, lançamentos manuais e painéis do dia | Admins e Mestres | §5 |
| **App 04** | **Jogo em JavaScript** — jogo que reaproveita a base de personagens da plataforma (engine sugerida: **Phaser.js**) | Jogadores | §6 |
| **App 05** | **Área do Jogador** — guia e apoio nas trilhas | Jogadores | §7 |
| **App 06** | **Vitrine pública** — apresentação da plataforma, sem login | Público geral / visitantes | §8 |
| **App 07** | **Área dos pais e responsáveis** — evolução do jogador, solicitações, direitos de recusa e transparência sobre os dados | Pais e responsáveis | §9 |

## 3. App 01 — Onboarding (cadastro e registro de presença)

Web App **responsivo, Mobile First**, acessível por smartphone ou tablet, usado no início de
cada aula presencial e também nas atividades on-line. Resolve dois problemas com a mesma
jornada: **cadastrar novos jogadores** e **registrar a presença** dos já cadastrados — por
conversa, sem formulário.

> O onboarding **roda continuamente** durante o encontro, e não apenas na abertura, porque a
> dinâmica da aula é assíncrona
> ([05 §3](05-implantacao-e-operacao.md#3-roteiro-da-aula-presencial)).

### 3.1 Jornada

```
[Tela de Boas-Vindas]
   ├── botão "Começar com ÁUDIO"  ──┐
   └── botão "Começar com CHAT"   ──┤
                                    ▼
                    [Interação cognitiva com IA]
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
            Jogador NOVO                    Jogador JÁ CADASTRADO
     nome, nick, nascimento/idade,        captura da imagem + nick
     comunidade virtual, avatar, foto     → comparação com a base
                    │                               │
                    ▼                               ▼
            cadastro criado +              presença registrada
            presença registrada            automaticamente
```

### 3.2 Requisitos funcionais

**Tela inicial (boas-vindas)**
- Layout Mobile First (smartphone/tablet), alto contraste, poucos elementos.
- O usuário escolhe a modalidade de interação em dois botões: **começar por áudio** e
  **começar por texto (chat)**. Ambos levam ao mesmo fluxo cognitivo — muda apenas a forma
  de conversar.

**Interação cognitiva**
- Conduzida por **Inteligência Artificial** (conversa natural, tolerante a respostas fora
  de ordem, capaz de repetir e confirmar dados).
- Modalidade áudio: captação e reprodução de som via **`mediadevices.js`**
  (`navigator.mediaDevices.getUserMedia`), reconhecimento de fala e síntese de voz — mesma
  base técnica do [Robô Educa](06-robo-educa.md).
- Modalidade chat: mesma conversa em texto, para ambientes barulhentos ou jogadores que
  preferem digitar.

**Captura de imagem**
- A imagem do jogador é captada pela câmera do dispositivo.
- **Finalidade única: identificação de presença nas aulas.** Não é avatar, não vai para a
  vitrine, não aparece em ranking, não é compartilhada.

**Novo jogador — dados coletados**

| Dado | Uso |
|---|---|
| Nome | Identificação interna e comunicação com responsáveis |
| Nick | Identidade pública do jogador |
| Data de nascimento ou idade | Adequação de conteúdo e faixa (6 a 16 anos) |
| **Comunidade Virtual** | **Vínculo obrigatório** — define a que comunidade os dados de território coletados pelo jogador serão creditados ([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)) |
| Características desejadas do avatar | Geração/montagem do avatar público |
| Foto | **Exclusivamente** registro de presença futuro |

**Vínculo com a Comunidade Virtual (regra vigente).** Nenhum jogador existe sem comunidade:
a conversa de cadastro oferece a lista das **Comunidades Virtuais já criadas pelos Admins**
(§5) e o jogador escolhe a sua. Não é o jogador quem cria a comunidade — ele a **preenche**,
registrando dados reais do território
([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)). Se o jogador não
pertencer a nenhuma comunidade cadastrada, o caso é resolvido por um Admin, que cria a nova
comunidade antes de concluir o vínculo.

Ao final, o jogador já está **ativo** e pode participar das atividades — sem exigência de
autorização do responsável nesta etapa
([02 §9](02-conceito-do-jogo-e-gamificacao.md#9-manual-do-jogador-fluxo-de-entrada)).

**Jogador já cadastrado — registro de presença**
1. Captura da imagem no momento da chegada.
2. Comparação com a base de imagens **combinada ao nick informado** (dois fatores: o nick
   restringe a busca, a imagem confirma).
3. Presença registrada automaticamente na atividade — **presencial ou on-line**.
4. Falha na identificação cai para confirmação manual por um Admin/Mestre — nunca deixa o
   jogador de fora da aula.

### 3.3 Requisitos de proteção de dados (LGPD aplicada)

A foto é **dado pessoal sensível de criança e adolescente**. Regras obrigatórias:

- **Finalidade declarada e única**: reconhecimento de presença. Qualquer outro uso exige
  nova base legal e novo consentimento.
- **Consentimento informado** do responsável para a captura e o tratamento biométrico,
  colhido de forma legível e registrado com data/hora — registrável também pela
  **App 07** (§9).
- **Minimização**: armazenar o mínimo necessário — preferir *template* biométrico
  (representação matemática não reversível) em vez da fotografia original.
- **Segurança**: armazenamento criptografado, acesso restrito e auditado (quem acessou,
  quando, por quê).
- **Retenção**: prazo definido e exclusão automática ao fim do vínculo do jogador com o
  projeto, ou a pedido do responsável.
- **Direito de recusa**: o jogador que não autoriza a foto tem **alternativa equivalente**
  de registro de presença (nick + confirmação do Mestre). Recusar biometria nunca pode
  significar exclusão da atividade. A recusa é exercível a qualquer momento pela **App 07**
  (§9).
- **Transparência**: a política de privacidade explica em linguagem simples — para o
  responsável **e para a criança** — o que é captado, por quê e por quanto tempo.

### 3.4 Requisitos não funcionais

- Funcionar em **rede instável** e em aparelhos modestos; fila local de sincronização
  quando cair a conexão.
- Tempo de registro de presença de um jogador conhecido: **poucos segundos** (a aula não
  pode travar na porta).
- Acessibilidade: a modalidade áudio atende quem ainda não lê com fluência e pessoas com
  deficiência visual.

## 4. App 02 — Assistente por voz e Modo Ouvinte

Arquitetura: **JavaScript no frontend + IA no backend**, a mesma base técnica do
[Robô Educa](06-robo-educa.md) — captação e reprodução de áudio via
`navigator.mediaDevices.getUserMedia`, reconhecimento de fala, síntese de voz e chamada ao
modelo de IA no servidor.

Dois modos de operação:

- **Modo Conversa** — o jogador fala com o robô e recebe resposta em áudio: quiz, explicação
  de conceitos, apoio às atividades escolares.
- **Modo Ouvinte** — a aplicação **acompanha o que é falado durante a aula** e, quando
  acionada, **opina sobre o tema em discussão ou responde a perguntas dirigidas a ela**.
  Funciona como um participante a mais do encontro, e não como um gravador: só se manifesta
  quando solicitado.

Requisitos obrigatórios do Modo Ouvinte (dado o público infantojuvenil):

- **Ativação explícita e visível** pelo Mestre no início da aula, com indicação permanente
  na tela de que o modo está ativo — e desligamento a qualquer momento.
- **Sem gravação persistente do áudio da turma.** O áudio é processado em janela de
  contexto transitória; persiste-se, no máximo, a transcrição estritamente necessária para
  a resposta, com prazo de retenção definido.
- **Aviso prévio a jogadores e responsáveis** de que o recurso é utilizado em aula, com
  possibilidade de recusa — vale a mesma regra de alternativa equivalente aplicada à foto
  de presença (§3.3). A recusa é registrada pelo responsável na **App 07** (§9).
- Filtros de segurança de conteúdo no nível mais restritivo, como em toda interação de IA
  com crianças — requisito obrigatório já definido para o
  [Robô Educa](06-robo-educa.md), cuja base técnica esta aplicação reaproveita.

> **Pendência registrada:** os limites de captação, retenção e consentimento do Modo Ouvinte
> ainda precisam de definição formal — ver
> [09 §1](09-topicos-em-aberto-e-sugestoes.md#1-decisões-pendentes).

## 5. App 03 — Gestão administrativa

Aplicação **web responsiva, Mobile First**, autenticada, para Admins (Organizadores/Equipe
técnica) e, conforme permissão, Mestres:

- **CRUDs de personas e do catálogo**: jogadores, mestres, apoiadores, admins, comunidades
  virtuais e **poderes**.
- **Criação das Comunidades Virtuais** — **exclusiva de Admins**. A comunidade é criada
  **vazia** e passa a ganhar corpo à medida que os jogadores vinculados registram dados
  reais do território ([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)).
- **Vínculo do jogador à comunidade** — conferência e, quando necessário, transferência de
  um jogador de uma comunidade para outra (mudança de endereço, cadastro equivocado), com
  registro de quando a mudança ocorreu, já que os dados coletados são **temporais**.
- **Cadastro de Mestres e Apoiadores** — exclusivo de Admins, com anexação dos **materiais
  ou artefatos comprobatórios** da habilidade/apoio
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#1-os-elementos-do-jogo-personas)).
- **Inclusão manual de novos Admins** por um Admin existente.
- **Cadastro de atividades** com: pontuação, recompensas e recursos necessários.
- **Agenda de aulas** (on-line e presenciais) e respectivas atividades previstas.
- **Lançamento de atividades realizadas**: data, mentores, jogadores e respectivos
  resultados (realizada / realizada com mérito / mérito extra por auxílio aos colegas).
- **Registro de presença** — automático via onboarding (§3) e ajustável manualmente.
- **Entradas manuais do dia**: presença, **infrações ocorridas nas aulas** e **pontuação
  extra ao jogador que ajudou o colega**.
- **Lançamento de pontuação negativa** (mau comportamento, agressões verbais/físicas,
  descumprimento de regras).
- **Gestão de recursos** necessários à realização de atividades (aportes de mestres e
  apoiadores, baixa de recursos consumidos).
- **Aprovação de desafios extras propostos por Apoiadores** — validação pedagógica do Mestre
  da trilha e **aprovação caso a caso por um Admin**, que é o que dispensa qualquer teto
  numérico de desafios simultâneos
  ([04 §5](04-modelo-economico-e-sustentabilidade.md#5-interação-apoiadores-x-jogadores-desafios-extras)).
- **Painéis do dia** — visão operacional do encontro em andamento: presenças confirmadas,
  atividade prevista, recursos providos e lançamentos pendentes.
- **Operação do Quiz ao Vivo** — cadastro das perguntas pelo curador da aula e condução da
  partida ([05 §4](05-implantacao-e-operacao.md#4-atividade-modelo-quiz-ao-vivo)).
- **Atendimento às solicitações dos responsáveis** recebidas pela App 07 (§9): autorização
  ou revogação de divulgação, recusa de biometria, pedidos de acesso, correção ou exclusão
  de dados — com registro de quem tratou e quando.

## 6. App 04 — Jogo em JavaScript

Jogo executado no navegador, construído sobre a **base de personagens da plataforma**: os
avatares, poderes, badges e níveis já conquistados pelos jogadores são os elementos do jogo.

> **Engine sugerida: [Phaser.js](https://phaser.io/)** — framework de jogos 2D em JavaScript
> que roda no próprio navegador, sem plugin nem instalação, e funciona bem em celular
> modesto. Escolha coerente com o restante da etapa (Web App, Mobile First) e com o objetivo
> de que o **código do jogo seja legível e alterável pelos próprios jogadores**.

**Definição vigente — o jogo não gera pontuação, apenas a consome.** O progresso obtido no
App 04 **não** produz pontos na plataforma: os pontos vêm exclusivamente das atividades
propostas pelos Mestres e da coleta de dados do território
([02 §4](02-conceito-do-jogo-e-gamificacao.md#4-atividades-e-desafios)). O jogo é um
**destino** dos pontos e das conquistas, não uma fonte. Consequências:

- O que se conquista aprendendo (poderes, badges, níveis) **desbloqueia e alimenta** o que o
  jogador pode fazer dentro do jogo.
- Jogar muito **não** sobe ninguém no ranking da plataforma — o ranking continua medindo
  aprendizado e realização na vida real.
- Elimina, por construção, a principal via de fraude de pontos: não há como automatizar
  cliques para pontuar.

Objetivos:

- Dar utilidade lúdica ao progresso obtido nas trilhas — o que se conquista aprendendo vale
  dentro do jogo.
- Servir, ele próprio, de conteúdo do **Poder da IA e Robótica**: o código é aberto e
  legível, e alterá-lo é atividade de trilha.
- Respeitar a regra de representação: personagens são **avatares, nunca imagens reais** dos
  jogadores (§10).

> **A definir:** gênero e mecânica do jogo.

## 7. App 05 — Área do Jogador

Web App de uso cotidiano do jogador, com **guia e apoio nas trilhas**: qual é o próximo
ponto da trilha, o que precisa ser feito, o que já foi conquistado e o que está bloqueado.
Reúne a jornada gamificada descrita em
[02-conceito-do-jogo-e-gamificacao.md](02-conceito-do-jogo-e-gamificacao.md) — poderes,
trilhas, desafios semanais, equipes, ranking, recompensas e registro de dados do território.

É também o instrumento de **coleta de dados da Comunidade Virtual** do jogador: as séries de
coleta ativas, quando é a próxima medição, o que já foi registrado e **quantos pontos aquela
série está rendendo enquanto se mantém ativa**
([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)).

Requisitos consolidados em
[08 PRD-05](08-base-para-prds.md#prd-05--app-05-área-do-jogador-jornada-gamificada).

## 8. App 06 — Vitrine pública (apresentação da plataforma)

Web App **responsivo, Mobile First**, de acesso público e **sem autenticação**:

- Apresenta a plataforma: **Jogadores, Poderes, Mestres, Batalhas, Apoiadores e
  Comunidades Virtuais**. Ao selecionar um item, navega para a seção específica com cards
  individuais.
- **Cards rotativos** com avatares dos jogadores, atualizados a cada 5 segundos. Os cards
  exibem **apenas** a imagem do avatar, nick, badges, poderes adquiridos e informações
  relativas à plataforma e ao desempenho do jogador. Os cards **não incluem links para
  redes sociais dos jogadores** nem qualquer canal de contato direto (proteção de
  menores/LGPD).
- **Painel público da Comunidade Virtual** — dados do território coletados pelos jogadores,
  abertos à consulta da comunidade e de instituições, em **série histórica** e
  **anonimizados quando necessário** ([§10](#10-proteção-de-dados-em-toda-a-plataforma-lgpd)).
- Seções **"Quem somos"** e **"Contatos"**, editáveis pelos Admins.
- **Como apoiar** — canais de doação do projeto, incluindo a chave PIX da pessoa jurídica
  vinculada ([04 §2](04-modelo-economico-e-sustentabilidade.md#2-fontes-de-receita)).
- Identidade visual: **background com imagem de comunidade, cores, grafite** — estética de
  território, não corporativa.
- **Vídeo de apresentação**: os irmãos Susy e Otávio, os Rôbróders e o professor Carlos
  Trenell (narrativa/personagens da trilha Robô Educa).
- É também o espaço da **publicidade** prevista como fonte de receita
  ([04 §2](04-modelo-economico-e-sustentabilidade.md#2-fontes-de-receita)) — sempre fora das
  áreas de uso das crianças e sem qualquer coleta de dados de menores para fins publicitários.

## 9. App 07 — Área dos pais e responsáveis

Web App **responsivo, Mobile First**, autenticado, de uso dos **pais e responsáveis** pelos
jogadores. É o **canal oficial da plataforma com a família** — o que resolve a comunicação da
evolução do aluno sem depender de aplicativos de mensageria de terceiros (§2).

O responsável acessa apenas os dados dos jogadores sob sua responsabilidade, com vínculo
conferido por um Admin.

**O que a aplicação entrega:**

| Função | O que o responsável faz |
|---|---|
| **Evolução do jogador** | Acompanha presença, atividades realizadas, pontos, poderes, badges, nível e progresso nas trilhas |
| **Solicitações** | Autoriza ou **revoga** a divulgação pública do perfil; pede correção de dados; pede exclusão; solicita esclarecimentos — cada pedido com protocolo e prazo de resposta |
| **Direitos de recusa** | Recusa, a qualquer tempo, a **foto de presença** (§3.3), o **Modo Ouvinte** (§4) e o uso de imagem em vídeos e fotos de eventos — sempre com **alternativa equivalente** garantida ao jogador |
| **Transparência de dados** | Vê **quais dados da criança estão armazenados**, para que servem, por quanto tempo ficam e quem os acessou |
| **Termos e consentimentos** | Lê, aceita e consulta o histórico dos termos que assinou, com data e hora |

**Regras obrigatórias:**

- **Nenhuma recusa exclui o jogador da atividade.** Todo direito de recusa tem alternativa
  equivalente prevista — a regra da foto de presença vale para todos os demais casos (§3.3).
- **A revogação vale para frente e é imediata** na parte pública: revogada a autorização, o
  perfil sai da vitrine (§8) e dos rankings públicos, sem prejuízo da participação.
- **Limite declarado do pedido de exclusão:** os **registros de dados do território** têm
  guarda permanente com autoria preservada (§10) e **não são apagados** a pedido. Isso
  precisa estar dito na tela, em linguagem simples, e no termo assinado — não descoberto
  depois.
- **Linguagem simples**, na mesma medida exigida da política de privacidade — o responsável
  precisa entender o que está autorizando (§10).
- **Sem contato direto com Apoiadores ou terceiros**: a área é canal entre família e
  plataforma, e nada mais — vale a mesma regra de mediação dos desafios extras
  ([04 §5](04-modelo-economico-e-sustentabilidade.md#5-interação-apoiadores-x-jogadores-desafios-extras)).
- Todas as solicitações caem na fila de atendimento da **App 03** (§5), com registro de quem
  tratou e quando.

> **A definir:** se o acesso do responsável é por login próprio ou por vínculo ao cadastro do
> jogador; prazos formais de resposta às solicitações; e se a área também envia notificação
> ativa (e-mail) além da consulta no Web App
> ([09 §1](09-topicos-em-aberto-e-sugestoes.md#1-decisões-pendentes)).

## 10. Proteção de dados em toda a plataforma (LGPD)

- Jogadores são representados **por seus avatares, e não por suas imagens reais**, em
  toda a plataforma (vitrine, rankings, batalhas, redes).
- Cards de jogadores **sem links para redes sociais nem contato direto** — apenas dados
  da própria plataforma (avatar, badges, poderes, desempenho).
- **Adesão em duas etapas:** o cadastro do jogador é **livre** (nome, data de nascimento,
  nick, comunidade e características do avatar) e permite participar de todas as
  atividades; a **divulgação do histórico e do perfil na plataforma** (vitrine, rankings
  públicos) só ocorre **após autorização dos pais ou responsáveis**, concedida e revogável
  pela App 07 (§9).
- A foto do jogador captada no onboarding é **dado sensível de uso restrito** (§3.3): serve
  apenas para reconhecimento de presença e **nunca** é exibida publicamente.
- **Dados do território: guarda permanente com o coletor identificado.** Os registros de
  coleta das Comunidades Virtuais são guardados de forma permanente para análises futuras
  **mantendo o vínculo com o jogador que os coletou**, mesmo depois que ele deixa o projeto —
  é o que dá procedência à série e preserva o crédito da realização
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#guarda-permanente-dos-dados-com-o-coletor-identificado)).
  A **anonimização ocorre na saída**: painéis públicos, exportações, pesquisas e entregas a
  instituições recebem dados **agregados e anonimizados**, nunca a autoria individual.
- Consequência a tratar na política de privacidade: essa retenção é **indefinida e nominal**,
  e precisa de **base legal declarada** e de resposta explícita ao pedido de exclusão feito
  pelo responsável — que não pode simplesmente apagar a série do território
  ([09 §2](09-topicos-em-aberto-e-sugestoes.md#proteção-da-criança-e-do-adolescente-prioridade-máxima)).
- **Georreferenciamento sem expor endereço de criança**: a granularidade publicada nunca
  pode permitir inferir onde um jogador específico mora
  ([09 §2](09-topicos-em-aberto-e-sugestoes.md#proteção-da-criança-e-do-adolescente-prioridade-máxima)).
- A LGPD deve ser considerada em **todos** os módulos e PRDs, não como item pontual.

**[Proposta]** Aplicar o mesmo cuidado a vídeos de culminância e fotos de eventos em que
jogadores apareçam (consentimento específico do responsável para cada divulgação, registrado
na App 07).

