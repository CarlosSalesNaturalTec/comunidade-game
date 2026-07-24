# 03 — Plataforma e Arquitetura

> Fontes: `linhas_gerais.md`, `Comunidade Game - Linhas Gerais 2025.txt`, `Implantação Jun 2024.rtf`

## 1. Princípios de arquitetura

1. **Backend em forma de API** — o backend deve funcionar como API, de modo que os mais
   diversos formatos de frontend **e aplicações de terceiros** possam acessá-lo.
2. **Rotas de consulta abertas** — leituras públicas (vitrine, rankings, batalhas) não
   exigem autenticação. Escrita e gestão exigem.
3. **Frontends independentes** — os frontends terão **domínios diferentes** e evoluem de
   forma desacoplada do backend.
4. **Open Source** — todo o código-fonte é aberto, para permitir replicação por qualquer
   comunidade ([05-implantacao-e-operacao.md](05-implantacao-e-operacao.md#replicabilidade)).
5. **Registro de custos em tudo** — toda ação com custo (aula, lanche, hospedagem,
   prestadores de serviço) é computada e atribuída a um personagem; a arquitetura precisa
   suportar esse livro-razão desde o início
   ([04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md)).

**[Sugestão nova]** Documentar a API com OpenAPI/Swagger desde o primeiro endpoint — é
condição prática para que "aplicações de terceiros" e novos frontends realmente surjam em um
projeto open source.

## 2. Canais / Meios de acesso

| Canal | Uso |
|---|---|
| **WhatsApp** | ChatBot baseado em IA — principal canal de baixa barreira (não exige computador); envio de resultados/evolução do aluno aos responsáveis |
| **Web App** | Plataforma completa (vitrine + área do jogador + gestão) |
| **Facebook** | Presença e divulgação |
| **App Android** | "Converse com seu robô" no smartphone/tablet |
| **PC / Notebook** | Web App |
| **Embarcados** | Raspberry Pi; NodeMCU (ex.: acender LEDs por comandos de voz); vestíveis |

O conceito **"Converse com seu robô"** perpassa os dispositivos: o robô/assistente do aluno
deve estar acessível de smartphone, web, WhatsApp e dispositivos embarcados.

## 3. Frontend 01 — Gestão

Aplicação autenticada para Organizadores/Equipe técnica (e Mestres, conforme permissão):

- **CRUDs de personas**: jogadores, mestres, apoiadores, organizadores, comunidades virtuais.
- **Cadastro de atividades** com: pontuação, recompensas e recursos necessários.
- **Agenda de aulas** (on-line e presenciais) e respectivas atividades previstas.
- **Lançamento de atividades realizadas**: data, mentores, jogadores e respectivos
  resultados (realizada / realizada com mérito / mérito extra por auxílio aos colegas).
- **Lançamento de pontuação negativa** (mau comportamento, agressões verbais/físicas,
  descumprimento de regras).
- **Gestão de recursos** necessários à realização de atividades (aportes de mestres e
  apoiadores, baixa de recursos consumidos).

## 4. Frontend 02 — Apresentação da Plataforma (vitrine pública)

Acesso público, **sem autenticação**:

- Apresenta a plataforma: **Jogadores, Poderes, Mestres, Batalhas, Apoiadores e
  Comunidades Virtuais**. Ao selecionar um item, navega para a seção específica com cards
  individuais.
- **Cards rotativos** com avatares dos jogadores, atualizados a cada 5 segundos.
  **Definição oficial (jul/2026):** os cards exibem **apenas** a imagem do avatar, nick,
  badges, poderes adquiridos e informações relativas à plataforma e ao desempenho do
  jogador. Os cards **não incluem links para redes sociais dos jogadores** nem qualquer
  canal de contato direto (a versão original previa links para Instagram, WhatsApp,
  YouTube, TikTok e e-mail — substituída por esta definição, por proteção de menores/LGPD).
- Seções **"Quem somos"** e **"Contatos"**, editáveis pelos Organizadores/Equipe técnica.
- Identidade visual: **background com imagem de comunidade, cores, grafite** — estética de
  território, não corporativa.
- **Botões "Criar Conta" e "Entrar".**
- **Vídeo de apresentação**: os irmãos Susy e Otávio, os Rôbróders e o professor Carlos
  Trenell (narrativa/personagens da comunicação do projeto).

**Definição oficial (jul/2026) — LGPD em todo o projeto:**

- Jogadores são representados **por seus avatares, e não por suas imagens reais**, em
  toda a plataforma (vitrine, rankings, batalhas, redes).
- Cards de jogadores **sem links para redes sociais nem contato direto** — apenas dados
  da própria plataforma (avatar, badges, poderes, desempenho).
- **Adesão em duas etapas:** o cadastro do jogador é **livre** (nome, data de nascimento,
  nick e características do avatar) e permite participar de todas as atividades; a
  **divulgação do histórico e do perfil na plataforma** (vitrine, rankings públicos) só
  ocorre **após autorização dos pais ou responsáveis**.
- A LGPD deve ser considerada em **todos** os módulos e PRDs, não como item pontual.

**[Sugestão nova]** Complemento a detalhar no PRD da vitrine: aplicar o mesmo cuidado a
vídeos de culminância e fotos de eventos em que jogadores apareçam (consentimento
específico do responsável para cada divulgação).

## 5. Dashboard (Backend API + Frontend)

Estrutura de navegação prevista:

- **Jogadores** — lista de jogadores; classificação/ranking.
- **Mestres** — professores.
- **Poderes (habilidades)** — catálogo (ver [02-conceito-do-jogo-e-gamificacao.md](02-conceito-do-jogo-e-gamificacao.md#2-poderes-habilidades)).
- **Trilhas** — progressão e desbloqueio de poderes.
- **Apoiadores / Mantenedores.**
- **Apoio/Auxiliar nas atividades escolares** — o aluno pede ajuda para tarefas da escola.

## 6. Inteligência e personalização

Características previstas para a plataforma:

- Na medida em que o aluno interage, a plataforma **capta seu perfil e se adapta** para
  entregar informação personalizada e relevante.
- **Interdisciplinaridade dirigida**: captar uma habilidade que o aluno já possui e
  utilizá-la para ensinar outros assuntos.
- **Envio de resultados com a evolução do aluno para os responsáveis via WhatsApp.**
- Componentes de ML aplicados a conteúdos (ex.: análise de movimentos da capoeira com
  TensorFlow — contador de polichinelos/movimentos corretos).

**[Sugestão nova]** Definir uma política de uso de IA e dados de menores (o que é coletado,
onde fica, quem acessa, retenção) alinhada à LGPD — além de obrigação legal, é coerente com
a premissa de "letramento contra os riscos da IA": a plataforma deve ser exemplo do que
ensina.

## 7. Kits e hardware educacional

- **Kits para ensino de programação e robótica** — o diferencial "sem exigência de um
  computador": o aluno compra/recebe o kit, monta e personaliza seu robô, e acessa a
  plataforma a partir dele ou do celular.
- **Professor Auxiliar / Ensino personalizado** — o robô/assistente como tutor.
- **Plataforma para letramento digital.**
- Hardware de referência das atividades: NodeMCU/ESP8266, sensores, LEDs, Raspberry Pi
  (projeto completo de exemplo em [06-batalha-de-laser.md](06-batalha-de-laser.md)).

## 8. Notas de engenharia (dos originais, a desenvolver)

Anotações soltas registradas em `linhas_gerais.md` sobre o processo de desenvolvimento do
próprio software (a detalhar em [08-topicos-em-aberto-e-sugestoes.md](08-topicos-em-aberto-e-sugestoes.md)):

- Orquestrador para disparar ações "do explore ao merge" (automação do fluxo de
  desenvolvimento com agentes).
- Como usar o Slack no fluxo.
- Ferramentas Git para comunicação entre agentes e humanos — seriam Issues?
