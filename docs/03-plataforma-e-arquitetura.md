# 03 — Plataforma e Arquitetura

## 1. Princípios de arquitetura

1. **Backend em forma de API** — para que os mais diversos frontends **e aplicações de
   terceiros** possam acessá-lo.
2. **Rotas de consulta abertas** — leituras públicas (vitrine, rankings, batalhas) não exigem
   autenticação. Escrita e gestão exigem.
3. **Frontends independentes** — em **domínios diferentes**, evoluindo desacoplados do
   backend.
4. **Open Source** — todo o código-fonte é aberto, para permitir replicação por qualquer
   comunidade.
5. **Registro de custos em tudo** — toda ação com custo (aula, lanche, hospedagem,
   prestadores) é computada e atribuída a um personagem; a arquitetura precisa suportar esse
   livro-razão desde o início.
6. **Dados do território como cidadão de primeira classe** — o modelo de dados precisa
   acomodar **séries temporais georreferenciadas** desde o início, com **guarda permanente**.
7. **Web App responsivo, Mobile First** — nesta etapa, **toda** aplicação é entregue como Web
   App projetado primeiro para o celular. Sem aplicativos nativos e sem aplicações construídas
   sobre plataformas de mensageria de terceiros.
8. **Plataforma em evolução contínua, com os jogadores** — os jogadores propõem melhorias pela
   Área do Jogador e alteram o código do jogo como atividade de trilha; a arquitetura precisa
   comportar essa evolução permanente.
9. **Construção assistida por IA, sob direção humana** — os artefatos da plataforma são
   construídos com auxílio de ferramentas de IA; a idealização, o contexto humano e social e
   as decisões são humanas, e a transparência sobre esse uso é pública.

**[Proposta]** Documentar a API com OpenAPI/Swagger desde o primeiro endpoint — condição
prática para que aplicações de terceiros e novos frontends realmente surjam.

## 2. Canais e meios de acesso

> **Definição vigente desta etapa:** **todas as aplicações são Web Apps responsivos, Mobile
> First**. Não há desenvolvimento sobre WhatsApp nem aplicativos nativos (Android/iOS). O
> navegador do celular é a plataforma-alvo; telas maiores são atendidas pela mesma aplicação.

| Canal                                 | Uso                                                                                                      |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Web App responsivo (Mobile First)** | Canal único de todas as aplicações                                                                       |
| **Smartphone / tablet**               | Dispositivo primário — é para ele que as telas são projetadas                                            |
| **PC / Notebook**                     | O mesmo Web App em telas maiores; uso típico da gestão                                                   |
| **Embarcados**                        | Raspberry Pi, NodeMCU, vestíveis. São o **hardware das atividades**, não um canal de acesso à plataforma |
| **Redes sociais**                     | Presença institucional e divulgação — não são canal de uso da plataforma                                 |

O conceito **"Converse com seu robô"** perpassa os dispositivos: o assistente do aluno deve
estar acessível a partir de qualquer navegador e conversar com os dispositivos embarcados
construídos nas oficinas.

Formato único de entrega: **uma base de código, sem loja de aplicativos, sem atualização pelo
usuário e sem tráfego de dados de crianças por plataformas de terceiros**.

### 2.1 As sete aplicações desta etapa

| #          | Aplicação                                                                                     | Público                              | Seção |
| ---------- | --------------------------------------------------------------------------------------------- | ------------------------------------ | ----- |
| **App 01** | **Onboarding** — cadastro de novo jogador e registro de presença, por áudio ou texto          | Jogadores (na chegada da aula)       | §3    |
| **App 02** | **Assistente por voz** — ChatBot de áudio nos moldes do Robô Educa, com **Modo Ouvinte**      | Jogadores e Mestres (durante a aula) | §4    |
| **App 03** | **Gestão administrativa** — CRUDs, lançamentos manuais e painéis do dia                       | Admins e Mestres                     | §5    |
| **App 04** | **Jogo em JavaScript** — sobre a base de personagens da plataforma                            | Jogadores                            | §6    |
| **App 05** | **Área do Jogador** — guia e apoio nas trilhas                                                | Jogadores                            | §7    |
| **App 06** | **Vitrine pública** — apresentação da plataforma, sem login                                   | Público geral                        | §8    |
| **App 07** | **Área dos pais e responsáveis** — evolução do jogador, solicitações e transparência de dados | Pais e responsáveis                  | §9    |

## 3. App 01 — Onboarding (cadastro e registro de presença)

Usado no início de cada aula presencial e também nas atividades on-line. Resolve dois
problemas com a mesma jornada: **cadastrar novos jogadores** e **registrar a presença** dos já
cadastrados — por conversa, sem formulário.

> O onboarding **roda continuamente** durante o encontro, e não apenas na abertura, porque a
> dinâmica da aula é assíncrona.

### 3.1 Jornada

```text
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

**Tela inicial** — layout Mobile First, alto contraste, poucos elementos. Dois botões:
**começar por áudio** e **começar por texto (chat)**. Ambos levam ao mesmo fluxo cognitivo.

**Interação cognitiva** — conduzida por **IA**: conversa natural, tolerante a respostas fora
de ordem, capaz de repetir e confirmar dados. Na modalidade áudio, captação e reprodução via
`navigator.mediaDevices.getUserMedia`, reconhecimento de fala e síntese de voz — mesma base
técnica do Robô Educa. Na modalidade chat, a mesma conversa em texto, para ambientes
barulhentos ou jogadores que preferem digitar.

**Captura de imagem** — pela câmera do dispositivo, com **finalidade única: identificação de
presença**. Não é avatar, não vai para a vitrine, não aparece em ranking, não é compartilhada.

#### Novo jogador — dados coletados

| Dado                        | Uso                                                                                       |
| --------------------------- | ----------------------------------------------------------------------------------------- |
| Nome                        | Identificação interna e comunicação com responsáveis                                      |
| Nick                        | Identidade pública do jogador                                                             |
| Data de nascimento ou idade | Adequação de conteúdo e faixa (6 a 16 anos)                                               |
| **Comunidade Virtual**      | **Vínculo obrigatório** — define a que comunidade os dados de território serão creditados |
| Características do avatar   | Geração do avatar público                                                                 |
| Foto                        | **Exclusivamente** registro de presença futuro                                            |

**Vínculo com a Comunidade Virtual (regra vigente).** Nenhum jogador existe sem comunidade: a
conversa oferece a lista das comunidades já criadas pelos Admins e o jogador escolhe a sua. Se
nenhuma servir, o caso é escalado a um Admin, que cria a comunidade antes de concluir o
vínculo.

Ao final, o jogador já está **ativo** e pode participar das atividades — sem exigência de
autorização do responsável nesta etapa.

#### Jogador já cadastrado — registro de presença

1. Captura da imagem na chegada.
2. Comparação com a base **combinada ao nick informado** (dois fatores: o nick restringe a
   busca, a imagem confirma).
3. Presença registrada automaticamente na atividade — presencial ou on-line.
4. Falha na identificação cai para confirmação manual por Admin/Mestre — nunca deixa o jogador
   de fora da aula.

### 3.3 Requisitos de proteção de dados (LGPD aplicada)

A foto é **dado pessoal sensível de criança e adolescente**. Regras obrigatórias:

- **Finalidade declarada e única**: reconhecimento de presença. Qualquer outro uso exige nova
  base legal e novo consentimento.
- **Consentimento informado** do responsável para a captura e o tratamento biométrico, colhido
  de forma legível e registrado com data e hora.
- **Minimização**: preferir _template_ biométrico (representação matemática não reversível) à
  fotografia original.
- **Segurança**: armazenamento criptografado, acesso restrito e auditado.
- **Retenção**: prazo definido e exclusão automática ao fim do vínculo do jogador com o
  projeto, ou a pedido do responsável.
- **Direito de recusa**: quem não autoriza a foto tem **alternativa equivalente** de registro
  de presença (nick + confirmação do Mestre). Recusar biometria nunca pode significar exclusão
  da atividade.
- **Transparência**: política de privacidade em linguagem simples — para o responsável **e
  para a criança**.

### 3.4 Requisitos não funcionais

- Funcionar em **rede instável** e em aparelhos modestos, com fila local de sincronização.
- Registro de presença de jogador conhecido em **poucos segundos** — a aula não pode travar na
  porta.
- Acessibilidade: a modalidade áudio atende quem ainda não lê com fluência e pessoas com
  deficiência visual.

## 4. App 02 — Assistente por voz e Modo Ouvinte

Arquitetura: **JavaScript no frontend + IA no backend**, a mesma base técnica do Robô Educa.
Dois modos de operação:

- **Modo Conversa** — o jogador fala com o robô e recebe resposta em áudio: quiz, explicação
  de conceitos, apoio às atividades escolares.
- **Modo Ouvinte** — a aplicação **acompanha o que é falado durante a aula** e, quando
  acionada, **opina sobre o tema em discussão ou responde a perguntas dirigidas a ela**.
  Funciona como um participante a mais, não como um gravador: só se manifesta quando
  solicitada.

Requisitos obrigatórios do Modo Ouvinte, dado o público infantojuvenil:

- **Ativação explícita e visível** pelo Mestre no início da aula, com indicação permanente na
  tela e desligamento a qualquer momento.
- **Sem gravação persistente do áudio da turma.** O áudio é processado em janela de contexto
  transitória; persiste-se, no máximo, a transcrição estritamente necessária, com prazo de
  retenção definido.
- **Aviso prévio a jogadores e responsáveis**, com possibilidade de recusa e alternativa
  equivalente — mesma regra da foto de presença.
- Filtros de segurança de conteúdo no nível mais restritivo.

> **Pendência registrada:** os limites de captação, retenção e consentimento do Modo Ouvinte
> ainda precisam de definição formal (documento 09).

## 5. App 03 — Gestão administrativa

Aplicação autenticada, para Admins e — conforme permissão — Mestres:

- **CRUDs de personas e catálogo**: jogadores, mestres, apoiadores, admins, comunidades
  virtuais e poderes.
- **Criação das Comunidades Virtuais** — **exclusiva de Admins**, nascendo vazias.
- **Vínculo do jogador à comunidade** — conferência e transferência entre comunidades
  (mudança de endereço, cadastro equivocado), com registro da data, já que os dados coletados
  são temporais.
- **Cadastro de Mestres e Apoiadores** — exclusivo de Admins, com anexação dos artefatos
  comprobatórios.
- **Inclusão manual de novos Admins** por um Admin existente.
- **Cadastro de atividades** com pontuação, recompensas e recursos necessários.
- **Agenda de aulas** (on-line e presenciais) e atividades previstas.
- **Lançamento de atividades realizadas**: data, mentores, jogadores e resultados.
- **Registro de presença** — automático via onboarding e ajustável manualmente.
- **Entradas manuais do dia**: presença, infrações ocorridas nas aulas e pontuação extra ao
  jogador que ajudou o colega.
- **Lançamento de pontuação negativa.**
- **Gestão de recursos** necessários às atividades (aportes e baixa de consumo).
- **Aprovação de desafios extras propostos por Apoiadores**, após validação pedagógica do
  Mestre da trilha.
- **Painéis do dia** — visão operacional do encontro em andamento: presenças confirmadas,
  atividade prevista, recursos providos e lançamentos pendentes.
- **Operação do Quiz ao Vivo** — cadastro das perguntas pelo curador e condução da partida.
- **Atendimento às solicitações dos responsáveis** vindas da App 07, com registro de quem
  tratou e quando.
- **Fila de avaliação das sugestões dos jogadores** vindas da App 05.

## 6. App 04 — Jogo em JavaScript

Jogo executado no navegador, construído sobre a **base de personagens da plataforma**: os
avatares, poderes, badges e níveis já conquistados são os elementos do jogo.

> **Engine sugerida: [Phaser.js](https://phaser.io/)** — framework de jogos 2D em JavaScript
> que roda no navegador, sem plugin nem instalação, e funciona bem em celular modesto. Escolha
> coerente com Web App / Mobile First e com o objetivo de que o **código seja legível e
> alterável pelos próprios jogadores**.

**Definição vigente — o jogo não gera pontuação, apenas a consome.** Os pontos vêm
exclusivamente das atividades propostas pelos Mestres e da coleta de dados do território. O
jogo é um **destino** dos pontos, não uma fonte. Consequências:

- O que se conquista aprendendo (poderes, badges, níveis) **desbloqueia e alimenta** o que o
  jogador pode fazer dentro do jogo.
- Jogar muito **não** sobe ninguém no ranking — o ranking mede aprendizado e realização na
  vida real.
- Elimina, por construção, a principal via de fraude de pontos: não há como automatizar
  cliques para pontuar.

Objetivos: dar utilidade lúdica ao progresso das trilhas; servir de conteúdo do **Poder da IA
e Robótica**, já que alterar o código é atividade de trilha — o jogador é um dos construtores
do próprio jogo; e respeitar a regra de representação por **avatares, nunca imagens reais**.

> **A definir:** gênero e mecânica do jogo.

## 7. App 05 — Área do Jogador

Web App de uso cotidiano do jogador, com **guia e apoio nas trilhas**: qual é o próximo ponto,
o que precisa ser feito, o que já foi conquistado e o que está bloqueado. Reúne a jornada
gamificada — poderes, trilhas, desafios semanais, equipes, ranking, recompensas e registro de
dados do território.

É também o instrumento de **coleta de dados da Comunidade Virtual**: as séries ativas, quando
é a próxima medição, o que já foi registrado e **quantos pontos aquela série está rendendo**.

E é o **canal de sugestões do jogador**: ideias de melhoria para atividades, trilhas e para a
própria plataforma são registradas aqui e caem na fila de avaliação da gestão — o mesmo
mecanismo de evolução pactuada do Código de Conduta, estendido à plataforma inteira.

## 8. App 06 — Vitrine pública

Web App de acesso público e **sem autenticação**:

- Apresenta **Jogadores, Poderes, Mestres, Batalhas, Apoiadores e Comunidades Virtuais**, com
  navegação para seções específicas com cards individuais.
- **Cards rotativos** com avatares dos jogadores, atualizados a cada 5 segundos. Exibem
  **apenas** avatar, nick, badges, poderes adquiridos e desempenho na plataforma — **sem links
  para redes sociais dos jogadores** nem qualquer canal de contato direto.
- **Painel público da Comunidade Virtual** — dados do território em **série histórica**,
  agregados e anonimizados, abertos à consulta da comunidade e de instituições.
- **Portfólio de criações originais** — as criações dos jogadores autorizados, com o nick do
  autor (ou dos autores, em equipe).
- Seções **"Quem somos"** e **"Contatos"**, editáveis pelos Admins — incluindo a **nota de
  transparência sobre IA**.
- **"Como apoiar"** — canais de doação, incluindo a chave PIX da pessoa jurídica vinculada.
- Identidade visual: **background com imagem de comunidade, cores, grafite** — estética de
  território, não corporativa.
- **Vídeo de apresentação**: os irmãos Susy e Otávio, os Rôbróders e o professor Carlos
  Trenell (narrativa da trilha Robô Educa).
- É também o espaço da **publicidade** prevista como fonte de receita — sempre fora das áreas
  de uso das crianças e sem coleta de dados de menores para fins publicitários.

## 9. App 07 — Área dos pais e responsáveis

Web App autenticado, **canal oficial da plataforma com a família** — o que resolve a
comunicação da evolução do aluno sem depender de aplicativos de mensageria de terceiros. O
responsável acessa apenas os dados dos jogadores sob sua responsabilidade, com vínculo
conferido por um Admin.

| Função                      | O que o responsável faz                                                                                                                                 |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Evolução do jogador**     | Acompanha presença, atividades realizadas, pontos, poderes, badges, nível e progresso nas trilhas                                                       |
| **Solicitações**            | Autoriza ou **revoga** a divulgação pública do perfil; pede correção ou exclusão de dados; solicita esclarecimentos — cada pedido com protocolo e prazo |
| **Direitos de recusa**      | Recusa, a qualquer tempo, a **foto de presença**, o **Modo Ouvinte** e o uso de imagem em vídeos e fotos de eventos                                     |
| **Transparência de dados**  | Vê **quais dados da criança estão armazenados**, para que servem, por quanto tempo ficam e quem os acessou                                              |
| **Termos e consentimentos** | Lê, aceita e consulta o histórico dos termos assinados, com data e hora                                                                                 |

**Regras obrigatórias:**

- **Nenhuma recusa exclui o jogador da atividade.** Todo direito de recusa tem alternativa
  equivalente.
- **A revogação vale para frente e é imediata** na parte pública: o perfil sai da vitrine e
  dos rankings, sem prejuízo da participação.
- **Limite declarado do pedido de exclusão:** os **registros de dados do território** têm
  guarda permanente com autoria preservada e **não são apagados** a pedido. Isso precisa estar
  dito na tela, em linguagem simples, e no termo assinado — não descoberto depois.
- **Linguagem simples**, na mesma medida exigida da política de privacidade.
- **Sem contato direto com Apoiadores ou terceiros**: a área é canal entre família e
  plataforma, e nada mais.
- Todas as solicitações caem na fila de atendimento da App 03, com registro de tratamento.

> **A definir:** se o acesso é por login próprio ou por vínculo ao cadastro do jogador; prazos
> formais de resposta; se há notificação ativa por e-mail além da consulta no Web App.

## 10. Proteção de dados em toda a plataforma (LGPD)

- Jogadores são representados **por avatares, nunca por imagens reais**, em toda a plataforma.
- Cards de jogadores **sem links para redes sociais nem contato direto**.
- **Adesão em duas etapas:** o cadastro é **livre** (nome, data de nascimento, nick,
  comunidade e características do avatar) e permite participar de todas as atividades; a
  **divulgação pública do histórico e do perfil** só ocorre **após autorização dos pais ou
  responsáveis**, concedida e revogável pela App 07.
- A foto captada no onboarding é **dado sensível de uso restrito**: serve apenas para
  reconhecimento de presença e **nunca** é exibida publicamente.
- **Dados do território: guarda permanente com o coletor identificado**, mesmo depois que o
  jogador deixa o projeto — é o que dá procedência à série e preserva o crédito da realização.
  A **anonimização ocorre na saída**: painéis públicos, exportações, pesquisas e entregas a
  instituições recebem dados **agregados e anonimizados**.
- Consequência a tratar na política de privacidade: essa retenção é **indefinida e nominal**,
  e precisa de **base legal declarada** e de resposta explícita ao pedido de exclusão feito
  pelo responsável.
- **Georreferenciamento sem expor endereço de criança**: a granularidade publicada nunca pode
  permitir inferir onde um jogador específico mora.
- A LGPD deve ser considerada em **todos** os módulos e PRDs, não como item pontual.

**[Proposta]** Aplicar o mesmo cuidado a vídeos de culminância e fotos de eventos em que
jogadores apareçam, com consentimento específico do responsável para cada divulgação.
