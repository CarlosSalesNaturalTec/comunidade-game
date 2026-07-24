# 03 — Plataforma e Arquitetura

## 1. Princípios de arquitetura

1. **Backend em forma de API** — o backend deve funcionar como API, de modo que os mais
   diversos formatos de frontend **e aplicações de terceiros** possam acessá-lo.
2. **Rotas de consulta abertas** — leituras públicas (vitrine, rankings, batalhas) não
   exigem autenticação. Escrita e gestão exigem.
3. **Frontends independentes** — os frontends terão **domínios diferentes** e evoluem de
   forma desacoplada do backend.
4. **Open Source** — todo o código-fonte é aberto, para permitir replicação por qualquer
   comunidade ([05-implantacao-e-operacao.md](05-implantacao-e-operacao.md#9-replicabilidade)).
5. **Registro de custos em tudo** — toda ação com custo (aula, lanche, hospedagem,
   prestadores de serviço) é computada e atribuída a um personagem; a arquitetura precisa
   suportar esse livro-razão desde o início
   ([04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md)).
6. **Dados do território como cidadão de primeira classe** — a plataforma é também uma
   base *Data Driven* das comunidades; o modelo de dados precisa acomodar séries temporais
   georreferenciadas desde o início
   ([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)).

**[Proposta]** Documentar a API com OpenAPI/Swagger desde o primeiro endpoint — é
condição prática para que "aplicações de terceiros" e novos frontends realmente surjam em um
projeto open source.

## 2. Canais / Meios de acesso

| Canal | Uso |
|---|---|
| **WhatsApp** | ChatBot baseado em IA — principal canal de baixa barreira (não exige computador); envio de resultados/evolução do aluno aos responsáveis |
| **Web App** | Plataforma completa (vitrine + área do jogador + gestão + onboarding) |
| **Facebook** | Presença e divulgação |
| **App Android** | "Converse com seu robô" no smartphone/tablet |
| **PC / Notebook** | Web App |
| **Embarcados** | Raspberry Pi; NodeMCU (ex.: acender LEDs por comandos de voz); vestíveis |

O conceito **"Converse com seu robô"** perpassa os dispositivos: o robô/assistente do aluno
deve estar acessível de smartphone, web, WhatsApp e dispositivos embarcados
([06-robo-educa.md](06-robo-educa.md)).

## 3. Frontend 01 — Gestão

Aplicação autenticada para Admins (Organizadores/Equipe técnica) e, conforme permissão,
Mestres:

- **CRUDs de personas**: jogadores, mestres, apoiadores, admins, comunidades virtuais.
- **Cadastro de Mestres e Apoiadores** — exclusivo de Admins, com anexação dos **materiais
  ou artefatos comprobatórios** da habilidade/apoio
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#1-os-elementos-do-jogo-personas)).
- **Inclusão manual de novos Admins** por um Admin existente.
- **Cadastro de atividades** com: pontuação, recompensas e recursos necessários.
- **Agenda de aulas** (on-line e presenciais) e respectivas atividades previstas.
- **Lançamento de atividades realizadas**: data, mentores, jogadores e respectivos
  resultados (realizada / realizada com mérito / mérito extra por auxílio aos colegas).
- **Registro de presença** — automático via onboarding (§5) e ajustável manualmente.
- **Lançamento de pontuação negativa** (mau comportamento, agressões verbais/físicas,
  descumprimento de regras).
- **Gestão de recursos** necessários à realização de atividades (aportes de mestres e
  apoiadores, baixa de recursos consumidos).

## 4. Frontend 02 — Apresentação da Plataforma (vitrine pública)

Acesso público, **sem autenticação**:

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

Interface **web acessível por smartphone ou tablet**, usada no início de cada aula
presencial e também on-line. Resolve dois problemas com a mesma jornada: **cadastrar novos
jogadores** e **registrar a presença** dos já cadastrados — por conversa, sem formulário.

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

**Tela de boas-vindas**
- Layout mobile-first (smartphone/tablet), alto contraste, poucos elementos.
- Dois botões de início: **start com áudio** e **start com chat**. Ambos levam ao mesmo
  fluxo cognitivo — muda apenas a modalidade de interação.

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
- **IA conversacional** no onboarding, no "converse com seu robô" e no WhatsApp — com
  filtros de segurança de conteúdo no nível mais restritivo por se tratar de crianças.
- **Envio de resultados com a evolução do aluno para os responsáveis via WhatsApp.**
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
