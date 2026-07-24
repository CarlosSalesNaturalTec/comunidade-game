# 08 — Base para Elaboração de PRDs

> Este documento estrutura o conteúdo do projeto como **insumo direto para PRDs**
> (Product Requirements Documents). Cada bloco abaixo é um candidato a PRD, com escopo,
> requisitos e questões em aberto que o PRD precisará responder.

## Visão de produto (comum a todos os PRDs)

- **Produto:** plataforma educacional gamificada open source para comunidades periféricas.
- **Posicionamento:** educacional e *tech first*, com paralelos obrigatórios para outras
  áreas do conhecimento e para valores e temas necessários à sociedade (racismo, violência
  contra mulheres, identidade, povos originários).
- **Usuários:** Jogadores (crianças/jovens), Mestres, Apoiadores, Admins
  (Organizadores/Equipe técnica), Visitantes, Comunidades Virtuais.
- **Fora de escopo:** encaminhamento profissional. A plataforma forma repertório e
  habilidade; não intermedeia colocação no mercado.
- **Restrições transversais (obrigatórias em todos os PRDs):**
  - Backend como API; rotas de consulta públicas sem autenticação; escrita autenticada.
  - Frontends em domínios separados.
  - Código open source.
  - Registro de custo/lastro de recursos em todas as ações.
  - **Governança de personas:** só o **Jogador** tem autocadastro. **Mestres e Apoiadores
    são cadastrados exclusivamente por Admins**, com habilidade/apoio comprovados por
    materiais ou artefatos publicados na plataforma. **Novos Admins são incluídos
    manualmente** por um Admin existente.
  - **LGPD em TODO o projeto**: jogadores representados por **avatares, nunca por imagens
    reais** na vitrine. A **foto captada no onboarding** é dado sensível de finalidade
    única (registro de presença), com consentimento, minimização, criptografia, retenção
    definida e alternativa para quem recusar. **Adesão em duas etapas:** cadastro livre
    (nome, data de nascimento/idade, nick, características do avatar) já permite participar
    das atividades; a **divulgação pública do histórico e do perfil** exige autorização
    dos pais ou responsáveis.
  - **Faixa etária dos jogadores: 6 a 16 anos**, com atividades em **níveis de
    dificuldade graduais** acessíveis independentemente da idade.
  - Valores do projeto refletidos em conteúdo, conduta e representatividade
    ([01-visao-valores-e-proposito.md](01-visao-valores-e-proposito.md#3-valores-e-causas)).

---

## PRD-01 — Backend API (núcleo)

**Escopo:** modelo de domínio e API pública/privada que sustenta todos os frontends.

**Requisitos:**
- Entidades: Jogador, Mestre, Apoiador, Admin, Comunidade Virtual, Poder, Trilha,
  Atividade, Aula/Agenda, Presença, Batalha, Equipe, Recurso, Recompensa,
  Ponto/Badge/Nível, Registro de dado do território.
- Rotas de consulta abertas (vitrine, rankings, painéis de comunidade) sem autenticação.
- Suporte a múltiplos frontends e aplicações de terceiros.
- Papéis e permissões: Admin (total), Mestre (conteúdo e lançamentos das suas atividades),
  Jogador (próprios dados), Visitante (leitura pública).
- Regra de negócio: **cadastro de Mestre/Apoiador restrito a Admin**, com anexos
  comprobatórios obrigatórios; **inclusão de Admin apenas por outro Admin**.
- Regra de negócio: atividade só é agendável/realizável com recursos providos (lastro).
- Regra de negócio: pontos de habilidade só via atividades realizadas propostas por Mestres.
- Resultados de atividade: realizada / com mérito / mérito extra por auxílio; pontuação
  negativa por má conduta.

**Questões em aberto:** estratégia de autenticação; versionamento da API; multi-tenant por
comunidade (uma instância nacional ou uma por comunidade?).

## PRD-02 — Frontend de Gestão

**Escopo:** aplicação autenticada para Admins e Mestres.

**Requisitos:** CRUDs de personas; cadastro de Mestres/Apoiadores com upload dos artefatos
comprobatórios; inclusão manual de Admins; cadastro de atividades (pontuação, recompensas,
recursos necessários); agenda de aulas on-line/presenciais; lançamento de atividades
realizadas (data, mentores, jogadores, resultados); conferência e ajuste de presenças
vindas do onboarding; lançamento de pontuação negativa; gestão de recursos (aportes e
consumo).

**Questões em aberto:** quem pode lançar pontuação negativa e com que auditoria; trilha de
auditoria das ações de Admin.

## PRD-03 — Frontend de Apresentação (vitrine pública)

**Escopo:** site público, sem login, em domínio próprio.

**Requisitos:** seções Jogadores, Poderes, Mestres, Batalhas, Apoiadores, Comunidades
Virtuais com cards individuais; cards rotativos de jogadores (rotação a cada 5 s); painel
público de dados por comunidade; "Quem somos" e "Contatos" editáveis; botões Criar
Conta/Entrar; vídeo de apresentação (Susy, Otávio, Rôbróders, prof. Carlos Trenell);
estética de comunidade (grafite, cores, imagens do território).

**Definições vigentes:** cards de jogadores exibem **apenas** avatar (nunca imagem real),
nick, badges, poderes adquiridos e informações da plataforma/desempenho; **sem links para
redes sociais dos jogadores nem contato direto** (LGPD/proteção de menores). A vitrine
exibe **somente jogadores cujo responsável autorizou a divulgação** do histórico e do
perfil; jogadores sem autorização participam das atividades mas não aparecem publicamente.
Os perfis de Mestres exibem os artefatos que comprovam suas habilidades.

## PRD-04 — Onboarding: cadastro e registro de presença

**Escopo:** interface web mobile-first (smartphone/tablet) que cadastra novos jogadores e
registra presença dos já cadastrados, por **voz ou chat**, com IA — detalhamento em
[03 §5](03-plataforma-e-arquitetura.md#5-frontend-03--onboarding-cadastro-e-registro-de-presença).

**Requisitos:**
- Tela de boas-vindas com **botão start por áudio** e **botão start por chat**.
- Interação cognitiva conduzida por **IA**, tolerante a respostas fora de ordem, capaz de
  repetir e confirmar dados.
- Captação e reprodução de áudio via **`mediadevices.js`**
  (`navigator.mediaDevices.getUserMedia`) + reconhecimento e síntese de fala.
- Captura da **imagem do jogador** pela câmera do dispositivo.
- **Novo jogador:** salvar nome, nick, data de nascimento ou idade, características
  desejadas do avatar e foto. O jogador fica **ativo** ao final, sem exigir autorização do
  responsável nesta etapa.
- **Jogador já cadastrado:** capturar imagem, comparar com a base de imagens **somada ao
  nick informado**, e **registrar presença automaticamente** na atividade — presencial ou
  on-line.
- Fallback manual (Admin/Mestre confirma) quando a identificação falhar.
- Operação com rede instável: fila local e sincronização posterior.

**Requisitos de proteção de dados (obrigatórios):** finalidade única da foto (presença);
consentimento informado do responsável registrado; preferência por *template* biométrico
não reversível; criptografia e acesso auditado; prazo de retenção com exclusão automática;
**alternativa de presença sem biometria** para quem recusar.

**Questões em aberto:** provedor de IA e de reconhecimento facial (custo, privacidade,
processamento no dispositivo x nuvem); política de retenção em números; roteiro exato da
conversa de cadastro.

## PRD-05 — Área do Jogador (jornada gamificada)

**Escopo:** experiência logada do jogador (web/app).

**Requisitos:** escolha de poder; trilhas com desbloqueio por quiz/desafio; desafios
semanais (on-line 10 pts, presencial 10 pts, equipe 10 pts, família 20 pts); equipes
mistas de até 5 e Equipe Familiar; registro de dados do território; ranking; troca de
pontos por recompensas (kits de alimentos; catálogo a expandir); pedido de ajuda para
atividades escolares; níveis 1–5 (assíduo → instrutor); badges.

**Requisitos adicionais:** estado de **perfil público** desbloqueado apenas com
autorização do responsável (sem ela, histórico e perfil não são divulgados); representação
exclusivamente por avatar; desafios com níveis de dificuldade graduais acessíveis a toda a
faixa de 6 a 16 anos.

**Questões em aberto:** definição da tabela de pontos das recompensas (os valores atuais
são apenas sugestão); mecânica anti-fraude de pontos; acessibilidade para quem só tem
celular ou só WhatsApp.

## PRD-06 — Canal WhatsApp (chatbot IA)

**Escopo:** chatbot baseado em IA no WhatsApp — canal de menor barreira de acesso.

**Requisitos:** interação educacional ("converse com seu robô"); envio da evolução do
aluno para os responsáveis; participação em desafios on-line; captação de perfil para
personalização.

**Questões em aberto:** custo de API do WhatsApp; política de dados de menores em
plataforma de terceiros; fallback para quem não tem WhatsApp.

## PRD-07 — Economia de Recursos e Transparência (ledger)

**Escopo:** livro-razão de recursos aportados e consumidos; "Poder Econômico".

**Requisitos:** todo custo de toda ação atribuído a um personagem; recurso alocado
computado como "moeda" no histórico do provedor; atividade condicionada a lastro; tipos de
recurso: hora-aula, lanche, recompensas, insumos, cloud, serviços; visibilidade pública da
riqueza movimentada.

**Questões em aberto:** unidade de conta (R$? pontos?); valoração da hora-aula;
relatórios públicos por atividade/comunidade/provedor.

## PRD-08 — Comunidades Virtuais e dados do território

**Escopo:** representação digital da comunidade real em que o jogador vive, construída
pelos próprios jogadores — a base *Data Driven* da plataforma
([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)).

**Requisitos:**
- A comunidade virtual **existe na medida em que dados reais são registrados**.
- Atividades de coleta: temperatura local, precipitação pluviométrica, coleta de resíduos,
  buracos na via, iluminação, trânsito, transporte público, fotos e memórias.
- **Granularidade hierárquica** do registro: comunidade → bairro → rua → condomínio →
  bloco → quadra.
- Cada registro alimenta e "constrói" visualmente a comunidade digital.
- Painéis públicos por comunidade; dados como **insumo para tomada de decisões** por
  moradores, associações, escolas, poder público e pesquisas.
- Exportação/API aberta dos dados agregados e anonimizados.

**Questões em aberto:** fontes e sensores (registro manual x sensor construído pelo
jogador x API pública); curadoria e veracidade dos dados; georreferenciamento sem expor
endereço de criança; modelo de séries temporais.

## PRD-09 — Conteúdo e Trilhas (autoria dos Mestres)

**Escopo:** ferramenta para Mestres criarem trilhas, conteúdos, quizzes e desafios.

**Requisitos:** trilhas mensais; conteúdo próprio e de terceiros; quiz/desafio para
desbloqueio; **publicação dos artefatos que comprovam a habilidade do Mestre**; catálogo
inicial de poderes (IA/Robótica, Rima, Redes, Capoeira com ML/TensorFlow, Soft Skills,
PNED/BNCC); paralelos obrigatórios com outras áreas do conhecimento e com os valores do
projeto; primeiro conteúdo: trilha de Programação e Robótica do fundador, com o
[Robô Educa](06-robo-educa.md) como primeira atividade e a
[Batalha de Laser](07-batalha-de-laser.md) como culminância.

**Questões em aberto:** formato dos conteúdos (vídeo, texto, interativo); revisão/curadoria
pedagógica; licença dos conteúdos (Creative Commons?).

## PRD-10 — Batalhas e eventos presenciais

**Escopo:** cadastro, operação e registro de batalhas (disputas de ideias e realizações).

**Requisitos:** batalhas presenciais e de projetos; culminância; estatísticas de partida
(ex.: telemetria do Nexus na Batalha de Laser); resultados alimentando ranking e
portfólio; integração Nexus → API **[Proposta]**.

## PRD-11 — Personalização por IA

**Escopo:** captação de perfil e adaptação de conteúdo.

**Requisitos:** plataforma capta o perfil conforme o aluno interage e entrega informação
personalizada; usar habilidade que o aluno já possui para ensinar outros assuntos
(interdisciplinaridade); ML aplicado a conteúdos (análise de movimentos de capoeira com
TensorFlow); filtros de segurança de conteúdo no nível mais restritivo em toda interação
com crianças.

**Questões em aberto:** modelo/stack de IA; limites éticos e LGPD para perfis de menores;
explicabilidade para responsáveis.

---

## Ordem sugerida de elaboração **[Proposta]**

1. **PRD-01 (API)** — tudo depende dele; incluir desde já o modelo do ledger (PRD-07) e
   das Comunidades Virtuais (PRD-08) no domínio, mesmo que a UI venha depois.
2. **PRD-04 (onboarding)** — é a porta de entrada real das aulas presenciais; sem ele não
   há cadastro nem registro de presença.
3. **PRD-03 (vitrine)** — entrega visibilidade rápida e material para captar apoiadores.
4. **PRD-02 (gestão)** — necessário para operar o primeiro ciclo presencial.
5. **PRD-05 (área do jogador)** — o jogo em si.
6. **PRD-09/10** — conteúdo do primeiro Mestre + primeira batalha.
7. **PRD-06, 07, 08, 11** — em ondas seguintes, conforme
   [05-implantacao-e-operacao.md](05-implantacao-e-operacao.md#10-fases-sugeridas-de-implantação-do-piloto-proposta).

> Dica operacional: este repositório já dispõe de skills de PRD (fases 1–5: elicitação,
> geração, revisão, patch e gestão de mudanças). Cada bloco acima pode alimentar a Fase 1
> (elicitação) diretamente.
