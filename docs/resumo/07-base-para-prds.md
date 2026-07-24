# 07 — Base para Elaboração de PRDs

> Este documento separa e estrutura o conteúdo compilado como **insumo direto para PRDs**
> (Product Requirements Documents). Cada bloco abaixo é um candidato a PRD, com escopo,
> requisitos extraídos dos originais e questões em aberto que o PRD precisará responder.

## Visão de produto (comum a todos os PRDs)

- **Produto:** plataforma educacional gamificada open source para comunidades periféricas.
- **Usuários:** Jogadores (crianças/jovens), Mestres, Apoiadores, Organizadores,
  Visitantes, Comunidades Virtuais.
- **Restrições transversais (obrigatórias em todos os PRDs):**
  - Backend como API; rotas de consulta públicas sem autenticação; escrita autenticada.
  - Frontends em domínios separados.
  - Código open source.
  - Registro de custo/lastro de recursos em todas as ações.
  - **LGPD em TODO o projeto** (definição oficial): jogadores representados por
    **avatares, nunca por imagens reais**. **Adesão em duas etapas:** cadastro livre
    (nome, data de nascimento, nick, características do avatar) já permite participar
    das atividades; a **divulgação pública do histórico e do perfil** exige autorização
    dos pais ou responsáveis.
  - **Faixa etária dos jogadores: 6 a 16 anos**, com atividades em **níveis de
    dificuldade graduais** acessíveis independentemente da idade.
  - Valores do projeto refletidos em conteúdo, conduta e representatividade
    ([01-visao-valores-e-proposito.md](01-visao-valores-e-proposito.md#3-valores-e-causas)).

---

## PRD-01 — Backend API (núcleo)

**Escopo:** modelo de domínio e API pública/privada que sustenta todos os frontends.

**Requisitos extraídos dos originais:**
- Entidades: Jogador, Mestre, Apoiador, Organizador, Comunidade Virtual, Poder, Trilha,
  Atividade, Aula/Agenda, Batalha, Equipe, Recurso, Recompensa, Ponto/Badge/Nível.
- Rotas de consulta abertas (vitrine, rankings) sem autenticação.
- Suporte a múltiplos frontends e aplicações de terceiros.
- Regra de negócio: atividade só é agendável/realizável com recursos providos (lastro).
- Regra de negócio: pontos de habilidade só via atividades realizadas propostas por Mestres.
- Regra de negócio: Mestre precisa de habilidade declarada + conteúdo comprobatório.
- Resultados de atividade: realizada / com mérito / mérito extra por auxílio; pontuação
  negativa por má conduta.

**Questões em aberto:** autenticação/autorização (papéis), versionamento da API,
multi-tenant por comunidade (uma instância nacional ou uma por comunidade?).

## PRD-02 — Frontend de Gestão

**Escopo:** aplicação autenticada para Organizadores e Mestres.

**Requisitos extraídos:** CRUDs de personas; cadastro de atividades (pontuação,
recompensas, recursos necessários); agenda de aulas on-line/presenciais; lançamento de
atividades realizadas (data, mentores, jogadores, resultados); lançamento de pontuação
negativa; gestão de recursos (aportes e consumo).

**Questões em aberto:** fluxo de aprovação de novos Mestres; quem pode lançar pontuação
negativa e com que auditoria.

## PRD-03 — Frontend de Apresentação (vitrine pública)

**Escopo:** site público, sem login, em domínio próprio.

**Requisitos extraídos:** seções Jogadores, Poderes, Mestres, Batalhas, Apoiadores,
Comunidades Virtuais com cards individuais; cards rotativos de jogadores (rotação a cada
5 s); "Quem somos" e "Contatos" editáveis; botões Criar Conta/Entrar; vídeo de
apresentação (Susy, Otávio, Rôbróders, prof. Carlos Trenell); estética de comunidade
(grafite, cores, imagens do território).

**Definições já tomadas (jul/2026):** cards de jogadores exibem **apenas** avatar (nunca
imagem real), nick, badges, poderes adquiridos e informações da plataforma/desempenho;
**sem links para redes sociais dos jogadores nem contato direto** (LGPD/proteção de
menores) — a previsão original de links sociais nos cards foi descartada. A vitrine exibe
**somente jogadores cujo responsável autorizou a divulgação** do histórico e do perfil;
jogadores sem autorização participam das atividades mas não aparecem publicamente.

## PRD-04 — Área do Jogador (jornada gamificada)

**Escopo:** experiência logada do jogador (web/app).

**Requisitos extraídos:** onboarding (nick, personagem/avatar); escolha de poder; trilhas
com desbloqueio por quiz/desafio; desafios semanais (on-line 10 pts, presencial 10 pts,
equipe 10 pts, família 20 pts); equipes mistas de até 5 e Equipe Familiar; ranking;
troca de pontos por recompensas (kits de alimentos; catálogo a expandir); pedido de ajuda
para atividades escolares; níveis 1–5 (assíduo → instrutor); badges.

**Requisitos oficiais adicionais:** onboarding com **cadastro livre** (nome, data de
nascimento, nick, características do avatar) que já habilita a participação em atividades;
estado de **perfil público** desbloqueado apenas com autorização do responsável (sem ela,
histórico e perfil não são divulgados); representação exclusivamente por avatar; desafios
com níveis de dificuldade graduais acessíveis a toda a faixa de 6 a 16 anos.

**Questões em aberto:** definição da tabela de pontos das recompensas (os valores atuais
são apenas sugestão); mecânica anti-fraude de pontos; acessibilidade para quem só tem
celular ou só WhatsApp.

## PRD-05 — Canal WhatsApp (chatbot IA)

**Escopo:** chatbot baseado em IA no WhatsApp — canal de menor barreira de acesso.

**Requisitos extraídos:** interação educacional ("converse com seu robô"); envio da
evolução do aluno para os responsáveis; participação em desafios on-line; captação de
perfil para personalização.

**Questões em aberto:** custo de API do WhatsApp; política de dados de menores em
plataforma de terceiros; fallback para quem não tem WhatsApp.

## PRD-06 — Economia de Recursos e Transparência (ledger)

**Escopo:** livro-razão de recursos aportados e consumidos; "Poder Econômico".

**Requisitos extraídos:** todo custo de toda ação atribuído a um personagem; recurso
alocado computado como "moeda" no histórico do provedor; atividade condicionada a lastro;
tipos de recurso: hora-aula, lanche, recompensas, insumos, cloud, serviços; visibilidade
pública da riqueza movimentada.

**Questões em aberto:** unidade de conta (R$? pontos?); valoração da hora-aula;
relatórios públicos por atividade/comunidade/provedor.

## PRD-07 — Comunidades Virtuais e dados do território

**Escopo:** representação digital das comunidades reais.

**Requisitos extraídos:** comunidade virtual existe na medida em que registra dados reais
(temperatura, coleta de lixo, fotos, trânsito, transporte público); vitrine por
comunidade; geração de dados para tomada de decisões (e pesquisas como fonte de receita).

**Questões em aberto:** sensores/fontes de dados; curadoria e veracidade; anonimização
para uso em pesquisas.

## PRD-08 — Conteúdo e Trilhas (autoria dos Mestres)

**Escopo:** ferramenta para Mestres criarem trilhas, conteúdos, quizzes e desafios.

**Requisitos extraídos:** trilhas mensais; conteúdo próprio e de terceiros; quiz/desafio
para desbloqueio; prova de habilidade do Mestre via conteúdo publicado; catálogo inicial de
poderes (IA/Robótica, Rima, Redes, Capoeira com ML/TensorFlow, Soft Skills, PNED/BNCC);
primeiro conteúdo: trilha de Programação e Robótica do fundador, com a
[Batalha de Laser](06-batalha-de-laser.md) como atividade de culminância.

**Questões em aberto:** formato dos conteúdos (vídeo, texto, interativo); revisão/curadoria
pedagógica; licença dos conteúdos (Creative Commons?).

## PRD-09 — Batalhas e eventos presenciais

**Escopo:** cadastro, operação e registro de batalhas (disputas de ideias e realizações).

**Requisitos extraídos:** batalhas presenciais e de projetos; culminância; estatísticas de
partida (ex.: telemetria do Nexus na Batalha de Laser); resultados alimentando ranking e
portfólio; integração Nexus → API **[Sugestão nova]**.

## PRD-10 — Personalização por IA

**Escopo:** captação de perfil e adaptação de conteúdo.

**Requisitos extraídos:** plataforma capta o perfil conforme o aluno interage e entrega
informação personalizada; usar habilidade que o aluno já possui para ensinar outros
assuntos (interdisciplinaridade); ML aplicado a conteúdos (análise de movimentos de
capoeira com TensorFlow).

**Questões em aberto:** modelo/stack de IA; limites éticos e LGPD para perfis de menores;
explicabilidade para responsáveis.

---

## Ordem sugerida de elaboração **[Sugestão nova]**

1. **PRD-01 (API)** — tudo depende dele; incluir desde já o modelo do ledger (PRD-06) no
   domínio, mesmo que a UI venha depois.
2. **PRD-03 (vitrine)** — entrega visibilidade rápida e material para captar apoiadores.
3. **PRD-02 (gestão)** — necessário para operar o primeiro ciclo presencial.
4. **PRD-04 (área do jogador)** — o jogo em si.
5. **PRD-08/09** — conteúdo do primeiro Mestre + primeira batalha.
6. **PRD-05, 06, 07, 10** — em ondas seguintes, conforme
   [05-implantacao-e-operacao.md](05-implantacao-e-operacao.md#9-fases-sugeridas-de-implantação-do-piloto-sugestão-nova).

> Dica operacional: este repositório já dispõe de skills de PRD (fases 1–5: elicitação,
> geração, revisão, patch e gestão de mudanças). Cada bloco acima pode alimentar a Fase 1
> (elicitação) diretamente.
