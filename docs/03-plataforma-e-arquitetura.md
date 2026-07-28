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
   base *Data Driven* das comunidades; o modelo de dados precisa acomodar séries temporais
   georreferenciadas desde o início
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
| **Web App responsivo (Mobile First)** | Canal único de todas as aplicações: onboarding, assistente por voz, gestão, jogo e área do jogador |
| **Smartphone / tablet** | Dispositivo primário de acesso — é para ele que as telas são projetadas |
| **PC / Notebook** | O mesmo Web App em telas maiores; uso típico da gestão |
| **Embarcados** | Raspberry Pi; NodeMCU (ex.: acender LEDs por comandos de voz); vestíveis. São o **hardware das atividades**, não um canal de acesso à plataforma ([07-batalha-de-laser.md](07-batalha-de-laser.md)) |
| **Redes sociais** | Presença institucional e divulgação do projeto ([05 §8](05-implantacao-e-operacao.md#8-comunicação-e-divulgação)) — não são canal de uso da plataforma |

O conceito **"Converse com seu robô"** perpassa os dispositivos: o robô/assistente do aluno
deve estar acessível a partir de qualquer navegador — smartphone, tablet ou computador — e
conversar com os dispositivos embarcados construídos nas oficinas
([06-robo-educa.md](06-robo-educa.md)).

**Por que essa restrição.** Um único formato de entrega (Web App responsivo) mantém a
barreira de acesso baixa sem multiplicar bases de código, dispensa loja de aplicativos e
atualização pelo usuário, e evita submeter dados de crianças a plataformas de terceiros —
coerente com a regra de LGPD em todo o projeto (§4).

### 2.1 Aplicações a serem desenvolvidas

Cinco aplicações compõem o escopo desta etapa. Todas são **Web Apps responsivos, Mobile
First**, consumindo o mesmo Backend API (§1).

| # | Aplicação | Público | Especificação |
|---|---|---|---|
| **App 01** | **Onboarding** — escolha entre áudio ou texto, cadastro de novo aluno e registro de presença | Jogadores (na chegada da aula) | §5 |
| **App 02** | **Assistente por voz** — ChatBot de áudio nos moldes do Robô Educa, com **Modo Ouvinte** | Jogadores e Mestres (durante a aula) | §2.1.1 e [06-robo-educa.md](06-robo-educa.md) |
| **App 03** | **Gestão administrativa** — CRUDs, lançamentos manuais e painéis do dia | Admins e Mestres | §3 e §2.1.2 |
| **App 04** | **Jogo em JavaScript** — jogo que reaproveita a base de personagens da plataforma | Jogadores | §2.1.3 |
| **App 05** | **Área do Jogador** — guia e apoio nas trilhas | Jogadores | §2.1.4 |

> A **vitrine pública** (§4) já está especificada e permanece no escopo do produto, como
> frontend público sem login. Ela não integra a numeração acima porque não é uma aplicação
> nova desta etapa.

Correspondência com os frontends já descritos neste documento: **App 01 = Frontend 03**
(§5), **App 03 = Frontend 01** (§3), **vitrine = Frontend 02** (§4). Os apps 02, 04 e 05
são novos e estão detalhados a seguir.

#### 2.1.1 App 02 — Assistente por voz e Modo Ouvinte

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
  de presença (§5.3).
- Filtros de segurança de conteúdo no nível mais restritivo, como em toda interação de IA
  com crianças (§7).

> **Pendência registrada:** os limites de captação, retenção e consentimento do Modo Ouvinte
> ainda precisam de definição formal — ver
> [09 §1](09-topicos-em-aberto-e-sugestoes.md#1-decisões-pendentes).

#### 2.1.2 App 03 — Gestão administrativa

Detalhamento completo em §3. Escopo específico desta etapa:

- **CRUDs** de mestres, poderes, jogadores e apoiadores.
- **Entradas manuais**: registro de presença, infrações ocorridas nas aulas (pontuação
  negativa) e pontuação extra para o jogador que ajudou o colega.
- **Painéis do dia** — visão operacional do encontro em andamento: quem está presente, qual
  a atividade prevista, quais recursos foram providos, quais lançamentos ainda faltam.

#### 2.1.3 App 04 — Jogo em JavaScript

Jogo executado no navegador, construído sobre a **base de personagens da plataforma**: os
avatares, poderes, badges e níveis já conquistados pelos jogadores são os elementos do jogo.
Objetivos:

- Dar utilidade lúdica ao progresso obtido nas trilhas — o que se conquista aprendendo vale
  dentro do jogo.
- Servir, ele próprio, de conteúdo do **Poder da IA e Robótica**: o código é aberto e
  legível, e alterá-lo é atividade de trilha.
- Respeitar a regra de representação: personagens são **avatares, nunca imagens reais** dos
  jogadores (§4).

> **A definir:** gênero e mecânica do jogo, e se o progresso no jogo gera pontuação na
> plataforma ou apenas a consome.

#### 2.1.4 App 05 — Área do Jogador

Web App de uso cotidiano do jogador, com **guia e apoio nas trilhas**: qual é o próximo
ponto da trilha, o que precisa ser feito, o que já foi conquistado e o que está bloqueado.
Reúne a jornada gamificada descrita em
[02-conceito-do-jogo-e-gamificacao.md](02-conceito-do-jogo-e-gamificacao.md) — poderes,
trilhas, desafios semanais, equipes, ranking, recompensas e registro de dados do território.
Requisitos consolidados em
[08 PRD-05](08-base-para-prds.md#prd-05--app-05-área-do-jogador-jornada-gamificada).

## 3. Frontend 01 — Gestão (App 03)

Aplicação **web responsiva, Mobile First**, autenticada, para Admins (Organizadores/Equipe
técnica) e, conforme permissão, Mestres:

- **CRUDs de personas e do catálogo**: jogadores, mestres, apoiadores, admins, comunidades
  virtuais e **poderes**.
- **Cadastro de Mestres e Apoiadores** — exclusivo de Admins, com anexação dos **materiais
  ou artefatos comprobatórios** da habilidade/apoio
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#1-os-elementos-do-jogo-personas)).
- **Inclusão manual de novos Admins** por um Admin existente.
- **Cadastro de atividades** com: pontuação, recompensas e recursos necessários.
- **Agenda de aulas** (on-line e presenciais) e respectivas atividades previstas.
- **Lançamento de atividades realizadas**: data, mentores, jogadores e respectivos
  resultados (realizada / realizada com mérito / mérito extra por auxílio aos colegas).
- **Registro de presença** — automático via onboarding (§5) e ajustável manualmente.
- **Entradas manuais do dia**: presença, **infrações ocorridas nas aulas** e **pontuação
  extra ao jogador que ajudou o colega**.
- **Lançamento de pontuação negativa** (mau comportamento, agressões verbais/físicas,
  descumprimento de regras).
- **Gestão de recursos** necessários à realização de atividades (aportes de mestres e
  apoiadores, baixa de recursos consumidos).
- **Painéis do dia** — visão operacional do encontro em andamento: presenças confirmadas,
  atividade prevista, recursos providos e lançamentos pendentes.
- **Operação do Quiz ao Vivo** — cadastro das perguntas pelo curador da aula e condução da
  partida ([05 §4](05-implantacao-e-operacao.md#4-atividade-modelo-quiz-ao-vivo)).

## 4. Frontend 02 — Apresentação da Plataforma (vitrine pública)

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
  abertos à consulta da comunidade e de instituições.
- Seções **"Quem somos"** e **"Contatos"**, editáveis pelos Admins.
- Identidade visual: **background com imagem de comunidade, cores, grafite** — estética de
  território, não corporativa.
- **Botões "Criar Conta" e "Entrar".**
- **Vídeo de apresentação**: os irmãos Susy e Otávio, os Rôbróders e o professor Carlos
  Trenell (narrativa/personagens da comunicação do projeto).

**LGPD em todo o projeto:**

- Jogadores são representados **por seus avatares, e não por suas imagens reais**, em
  toda a plataforma (vitrine, rankings, batalhas, redes).
- Cards de jogadores **sem links para redes sociais nem contato direto** — apenas dados
  da própria plataforma (avatar, badges, poderes, desempenho).
- **Adesão em duas etapas:** o cadastro do jogador é **livre** (nome, data de nascimento,
  nick e características do avatar) e permite participar de todas as atividades; a
  **divulgação do histórico e do perfil na plataforma** (vitrine, rankings públicos) só
  ocorre **após autorização dos pais ou responsáveis**.
- A foto do jogador captada no onboarding é **dado sensível de uso restrito** (§5): serve
  apenas para reconhecimento de presença e **nunca** é exibida publicamente.
- A LGPD deve ser considerada em **todos** os módulos e PRDs, não como item pontual.

**[Proposta]** Aplicar o mesmo cuidado a vídeos de culminância e fotos de eventos em que
jogadores apareçam (consentimento específico do responsável para cada divulgação).

## 5. Frontend 03 — Onboarding (cadastro e registro de presença)

> Corresponde à **App 01** de §2.1.

Web App **responsivo, Mobile First**, acessível por smartphone ou tablet, usado no início de
cada aula presencial e também nas atividades on-line. Resolve dois problemas com a mesma
jornada: **cadastrar novos jogadores** e **registrar a presença** dos já cadastrados — por
conversa, sem formulário.

### 5.1 Jornada

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
     características do avatar, foto      → comparação com a base
                    │                               │
                    ▼                               ▼
            cadastro criado +              presença registrada
            presença registrada            automaticamente
```

### 5.2 Requisitos funcionais

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
| Características desejadas do avatar | Geração/montagem do avatar público |
| Foto | **Exclusivamente** registro de presença futuro |

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

### 5.3 Requisitos de proteção de dados (LGPD aplicada)

A foto é **dado pessoal sensível de criança e adolescente**. Regras obrigatórias:

- **Finalidade declarada e única**: reconhecimento de presença. Qualquer outro uso exige
  nova base legal e novo consentimento.
- **Consentimento informado** do responsável para a captura e o tratamento biométrico,
  colhido de forma legível e registrado com data/hora.
- **Minimização**: armazenar o mínimo necessário — preferir *template* biométrico
  (representação matemática não reversível) em vez da fotografia original.
- **Segurança**: armazenamento criptografado, acesso restrito e auditado (quem acessou,
  quando, por quê).
- **Retenção**: prazo definido e exclusão automática ao fim do vínculo do jogador com o
  projeto, ou a pedido do responsável.
- **Direito de recusa**: o jogador que não autoriza a foto tem **alternativa equivalente**
  de registro de presença (nick + confirmação do Mestre). Recusar biometria nunca pode
  significar exclusão da atividade.
- **Transparência**: a política de privacidade explica em linguagem simples — para o
  responsável **e para a criança** — o que é captado, por quê e por quanto tempo.

### 5.4 Requisitos não funcionais

- Funcionar em **rede instável** e em aparelhos modestos; fila local de sincronização
  quando cair a conexão.
- Tempo de registro de presença de um jogador conhecido: **poucos segundos** (a aula não
  pode travar na porta).
- Acessibilidade: a modalidade áudio atende quem ainda não lê com fluência e pessoas com
  deficiência visual.

## 6. Dashboard (Backend API + Frontend)

Estrutura de navegação prevista:

- **Jogadores** — lista de jogadores; classificação/ranking.
- **Mestres** — professores e seus artefatos comprobatórios.
- **Poderes (habilidades)** — catálogo (ver [02-conceito-do-jogo-e-gamificacao.md](02-conceito-do-jogo-e-gamificacao.md#2-poderes-habilidades)).
- **Trilhas** — progressão e desbloqueio de poderes.
- **Apoiadores / Mantenedores.**
- **Comunidades Virtuais** — dados do território e painéis.
- **Apoio/Auxiliar nas atividades escolares** — o aluno pede ajuda para tarefas da escola.

## 7. Inteligência e personalização

Características previstas para a plataforma:

- Na medida em que o aluno interage, a plataforma **capta seu perfil e se adapta** para
  entregar informação personalizada e relevante.
- **Interdisciplinaridade dirigida**: captar uma habilidade que o aluno já possui e
  utilizá-la para ensinar outros assuntos.
- **IA conversacional** no onboarding (App 01) e no "converse com seu robô" (App 02) — com
  filtros de segurança de conteúdo no nível mais restritivo, por se tratar de crianças.
- **Envio de resultados com a evolução do aluno aos responsáveis pela própria plataforma**
  (área do responsável no Web App e/ou e-mail), sem dependência de aplicativos de
  mensageria de terceiros.
- Componentes de ML aplicados a conteúdos (ex.: análise de movimentos da capoeira com
  TensorFlow — contador de polichinelos/movimentos corretos).

**[Proposta]** Definir uma política de uso de IA e dados de menores (o que é coletado,
onde fica, quem acessa, retenção) alinhada à LGPD — além de obrigação legal, é coerente com
a premissa de "letramento contra os riscos da IA": a plataforma deve ser exemplo do que
ensina.

## 8. Kits e hardware educacional

- **Kits para ensino de programação e robótica** — o diferencial "sem exigência de um
  computador": o aluno monta o robô com material reciclado ou kit, personaliza e acessa a
  plataforma a partir do celular ([06-robo-educa.md](06-robo-educa.md)).
- **Professor Auxiliar / Ensino personalizado** — o robô/assistente como tutor.
- **Plataforma para letramento digital.**
- Hardware de referência das atividades: NodeMCU/ESP8266, sensores, LEDs, Raspberry Pi
  (projeto completo de exemplo em [07-batalha-de-laser.md](07-batalha-de-laser.md)).
- **Sensores de território** para as Comunidades Virtuais (temperatura, pluviômetro) —
  podem ser construídos pelos próprios jogadores como atividade.

## 9. Notas de engenharia (a desenvolver)

Anotações sobre o processo de desenvolvimento do próprio software (detalhamento em
[09-topicos-em-aberto-e-sugestoes.md](09-topicos-em-aberto-e-sugestoes.md)):

- Orquestrador para disparar ações "do explore ao merge" (automação do fluxo de
  desenvolvimento com agentes).
- Como usar o Slack no fluxo.
- Ferramentas Git para comunicação entre agentes e humanos — seriam Issues?
