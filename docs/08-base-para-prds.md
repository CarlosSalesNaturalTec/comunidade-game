# 08 — Base para Elaboração de PRDs

> Este documento estrutura o conteúdo do projeto como **insumo direto para PRDs**
> (Product Requirements Documents). Cada bloco abaixo é um candidato a PRD, com escopo,
> requisitos e questões em aberto que o PRD precisará responder.

## Visão de produto (comum a todos os PRDs)

- **Produto:** plataforma educacional gamificada open source para comunidades periféricas.
- **Primeira implantação (contexto de todos os PRDs):**
  **[Case 01 — Comunidade Guerreira Zeferina](10-case-01-guerreira-zeferina.md)**, Salvador
  (BA), **Ciclo 01 de ago a dez/2026**. O MVP do ciclo é: credenciamento de jogadores,
  cadastro da comunidade digital e **trilhas 1 e 2 em operação**. Todo PRD deve poder ser
  respondido com a pergunta *"isto é necessário para o Ciclo 01?"* — o que não for, é onda
  seguinte.
- **Posicionamento:** educacional e *tech first*, com paralelos obrigatórios para outras
  áreas do conhecimento e para valores e temas necessários à sociedade (racismo, violência
  contra mulheres, identidade, povos originários).
- **Usuários:** Jogadores (crianças/jovens), Mestres, Apoiadores, Admins
  (Organizadores/Equipe técnica), Visitantes, Comunidades Virtuais.
- **Fora de escopo:** encaminhamento profissional. A plataforma forma repertório e
  habilidade; não intermedeia colocação no mercado.
- **Restrições transversais (obrigatórias em todos os PRDs):**
  - Backend como API; rotas de consulta públicas sem autenticação; escrita autenticada.
  - **Todas as aplicações desta etapa são Web Apps responsivos, Mobile First.** Não há
    aplicativo nativo nem aplicação construída sobre WhatsApp ou outra plataforma de
    mensageria de terceiros
    ([03 §2](03-plataforma-e-arquitetura.md#2-canais--meios-de-acesso)).
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
  - **Comunidade Virtual obrigatória:** a comunidade é **criada vazia por um Admin** e
    **todo jogador é vinculado a uma delas** no cadastro. Os dados de território são
    **temporais**, **guardados permanentemente com o jogador coletor identificado** (sem
    anonimização no armazenamento); a anonimização se aplica **na saída** — painéis públicos,
    exportações e pesquisas
    ([02 §1](02-conceito-do-jogo-e-gamificacao.md#guarda-permanente-dos-dados-com-o-coletor-identificado)).
  - **Toda trilha contém desafios de coleta de dados reais**
    ([02 §3](02-conceito-do-jogo-e-gamificacao.md#regra-vigente-toda-trilha-coleta-dados-reais)).
  - Valores do projeto refletidos em conteúdo, conduta e representatividade
    ([01-visao-valores-e-proposito.md](01-visao-valores-e-proposito.md#3-valores-e-causas)).
  - **Modelo de gamificação integrado como fonte normativa:** a anatomia da trilha, a
    taxonomia de atividades, o motor de pontuação, níveis, badges, recompensas e os
    reflexos no ecossistema (vitrine, cards, representação visual da comunidade, contrato
    dos jogos) seguem o **[doc 11](11-modelo-de-gamificacao.md)** — a
    [matriz de rastreabilidade](11-modelo-de-gamificacao.md#9-matriz-de-rastreabilidade--prds)
    indica quais conceitos cada PRD implementa.
  - **Mestres de qualquer área do conhecimento** — inclusive humanas, artes, esportes e
    cultura: nenhum modelo de dados ou fluxo pode pressupor habilidade técnica de TI
    ([02 §1](02-conceito-do-jogo-e-gamificacao.md#mestres-persona-secundária)).

### Aplicações desta etapa e seus PRDs

As **sete aplicações** definidas em
[03 §2.1](03-plataforma-e-arquitetura.md#21-aplicações-a-serem-desenvolvidas) correspondem
aos PRDs abaixo:

| Aplicação | PRD |
|---|---|
| **App 01** — Onboarding (áudio ou texto, cadastro, presença) | PRD-04 |
| **App 02** — Assistente por voz e Modo Ouvinte | PRD-06 |
| **App 03** — Gestão administrativa | PRD-02 |
| **App 04** — Jogo em JavaScript | PRD-12 |
| **App 05** — Área do Jogador (guia das trilhas) | PRD-05 |
| **App 06** — Vitrine pública | PRD-03 |
| **App 07** — Área dos pais e responsáveis | PRD-13 |

---

## PRD-01 — Backend API (núcleo)

**Escopo:** modelo de domínio e API pública/privada que sustenta todos os frontends.

**Requisitos:**
- Entidades: Jogador, Mestre, Apoiador, Admin, Comunidade Virtual, Poder, Trilha,
  Atividade, Aula/Agenda, Presença, Batalha, Equipe, Recurso, Recompensa,
  Ponto/Badge/Nível, Registro de dado do território, Pergunta de quiz e Partida de quiz.
- Rotas de consulta abertas (vitrine, rankings, painéis de comunidade) sem autenticação.
- Suporte a múltiplos frontends e aplicações de terceiros.
- Papéis e permissões: Admin (total), Mestre (conteúdo e lançamentos das suas atividades),
  Jogador (próprios dados), Visitante (leitura pública).
- Regra de negócio: **cadastro de Mestre/Apoiador restrito a Admin**, com anexos
  comprobatórios obrigatórios; **inclusão de Admin apenas por outro Admin**.
- Regra de negócio: **Comunidade Virtual criada apenas por Admin**, nascendo vazia; **todo
  Jogador tem vínculo obrigatório a exatamente uma Comunidade Virtual**, com histórico das
  transferências (o dado coletado pertence à comunidade vigente na data do registro).
- Regra de negócio: **registro de dado do território é uma série temporal** — cadência,
  janela de validade, jogador coletor e comunidade. **Série ativa gera pontos recorrentes;
  série interrompida cessa o cômputo**, sem perda dos pontos já creditados
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#registro-temporal-e-pontuação-enquanto-a-coleta-durar)).
- Regra de negócio: **dados do território têm guarda permanente e mantêm o vínculo com o
  jogador coletor** — sem anonimização no armazenamento, inclusive após o encerramento do
  vínculo do jogador com o projeto. A anonimização é aplicada **na saída** (painéis públicos,
  exportações, pesquisas)
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#guarda-permanente-dos-dados-com-o-coletor-identificado)).
- Regra de negócio: atividade só é agendável/realizável com recursos providos (lastro).
- Regra de negócio: pontos de habilidade só via atividades realizadas propostas por Mestres.
  O **App 04 (jogo) consome pontos e não os gera**
  ([03 §6](03-plataforma-e-arquitetura.md#6-app-04--jogo-em-javascript)).
- Regra de negócio: **desafio extra** exige validação do Mestre da trilha **e aprovação de um
  Admin**; gera **pontos extras** computados isoladamente; nas duas modalidades — **aberto**
  (a todos, com **quantidade de recompensas** declarada, uma ou várias, por ordem de
  conclusão) e **direcionado** (a um jogador específico, único elegível à recompensa, com
  **justificativa do vínculo registrada** e aprovada pelo Admin)
  ([04 §5](04-modelo-economico-e-sustentabilidade.md#5-interação-apoiadores-x-jogadores-desafios-extras),
  [02 §4](02-conceito-do-jogo-e-gamificacao.md#desafio-extra-direcionado)).
- Entidades e permissões da **área do responsável**: vínculo responsável ↔ jogador,
  consentimentos versionados com data/hora, solicitações com protocolo e status
  ([PRD-13](#prd-13--app-07-área-dos-pais-e-responsáveis)).
- Resultados de atividade: realizada / com mérito / mérito extra por auxílio; pontuação
  negativa por má conduta.
- Regra de negócio: **níveis 1 a 5 por trilha/poder**; a conclusão do Nível 5 marca o
  jogador como **Mestre Aprendiz**, apto ao treinamento de multiplicador e ao voluntariado
  nos pontos de apoio ([02 §7](02-conceito-do-jogo-e-gamificacao.md#7-níveis-e-badges-gamificação)).
- **Poder do Território** no catálogo de poderes: progressão e badges próprios por
  sustentar séries de coleta de dados do território
  ([02 §2](02-conceito-do-jogo-e-gamificacao.md#2-poderes-habilidades)).

**Questões em aberto:** estratégia de autenticação; versionamento da API; multi-tenant por
comunidade (uma instância nacional ou uma por comunidade?).

## PRD-02 — App 03: Frontend de Gestão

**Escopo:** aplicação autenticada para Admins e Mestres.

**Requisitos:** CRUDs de mestres, poderes, jogadores e apoiadores (além de admins e
comunidades virtuais); **criação das Comunidades Virtuais — exclusiva de Admin, nascendo
vazias — e gestão do vínculo/transferência de jogadores entre comunidades**
([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)); cadastro de
Mestres/Apoiadores com upload dos artefatos comprobatórios (incluindo **termos de doação**);
inclusão manual de Admins; cadastro de atividades (pontuação, recompensas, recursos
necessários); **cadastro de desafios de coleta com cadência e regra de pontuação
recorrente**; agenda de aulas on-line/presenciais; lançamento de atividades
realizadas (data, mentores, jogadores, resultados); **entradas manuais** — registro de
presença, infrações ocorridas nas aulas e pontuação extra ao jogador que ajudou o colega;
conferência e ajuste de presenças vindas do onboarding; gestão de recursos (aportes e
consumo); **painéis do dia** com a visão operacional do encontro em andamento (presenças,
atividade prevista, recursos providos, lançamentos pendentes, **saldo de kits MDF**);
**operação do Quiz ao Vivo**
([05 §4](05-implantacao-e-operacao.md#4-atividade-modelo-quiz-ao-vivo)); **controle do
acervo didático** — entrega dos exemplares da linha Alpha na abertura da trilha (baixa
definitiva), tombamento e empréstimo de bancada dos exemplares permanentes, estado de
conservação e devoluções pendentes no painel do dia
([05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação)); **validação de
desafios extras propostos por Apoiadores** pelo Mestre da trilha **e aprovação caso a caso
por Admin**
([04 §5](04-modelo-economico-e-sustentabilidade.md#5-interação-apoiadores-x-jogadores-desafios-extras));
**fila de solicitações dos responsáveis** vindas da App 07 (autorizações, revogações,
recusas, acesso, correção e exclusão de dados), com registro de quem tratou e quando
([PRD-13](#prd-13--app-07-área-dos-pais-e-responsáveis)).

**Painel do dia em encontro assíncrono:** como os jogadores chegam e avançam em ritmos
diferentes ([05 §3](05-implantacao-e-operacao.md#definição-vigente-o-encontro-é-assíncrono)),
o painel precisa mostrar, em tempo real, **quem já chegou, em que ponto de trilha cada equipe
está, quem está aguardando aparelho e quais lançamentos ainda faltam** — é o instrumento que
substitui o controle visual de uma turma em bloco.

**Questões em aberto:** quem pode lançar pontuação negativa e com que auditoria; trilha de
auditoria das ações de Admin; se o Quiz ao Vivo é módulo desta aplicação ou aplicação
separada.

## PRD-03 — App 06: Vitrine pública (apresentação da plataforma)

**Escopo:** site público, sem login, em domínio próprio
([03 §8](03-plataforma-e-arquitetura.md#8-app-06--vitrine-pública-apresentação-da-plataforma)).

**Requisitos:** seções Jogadores, Poderes, Mestres, Batalhas, Apoiadores, Comunidades
Virtuais com cards individuais; cards rotativos de jogadores (rotação a cada 5 s); painel
público de dados por comunidade **em série histórica**; "Quem somos" e "Contatos" editáveis;
seção **"Como apoiar"** com a chave PIX do projeto
([04 §2](04-modelo-economico-e-sustentabilidade.md#doações-em-espécie--canal-oficial));
espaço de **publicidade** fora das áreas de uso das crianças; vídeo de apresentação (Susy,
Otávio, Rôbróders, prof. Carlos Trenell); estética de comunidade (grafite, cores, imagens do
território).

**Definições vigentes:** cards de jogadores exibem **apenas** avatar (nunca imagem real),
nick, badges, poderes adquiridos e informações da plataforma/desempenho; **sem links para
redes sociais dos jogadores nem contato direto** (LGPD/proteção de menores). A vitrine
exibe **somente jogadores cujo responsável autorizou a divulgação** do histórico e do
perfil; jogadores sem autorização participam das atividades mas não aparecem publicamente.
Os perfis de Mestres exibem os artefatos que comprovam suas habilidades.

**Fonte normativa dos reflexos:** o mapeamento elemento do motor → vitrine, a composição
dos **cards de cada personagem** e a **representação visual da Comunidade Virtual**
(dado registrado → elemento visual) estão em
[11 §8](11-modelo-de-gamificacao.md#8-reflexos-no-ecossistema).

## PRD-04 — App 01: Onboarding (cadastro e registro de presença)

**Escopo:** Web App responsivo Mobile First (smartphone/tablet) que cadastra novos jogadores
e registra a presença dos já cadastrados, por **áudio ou texto**, com IA — detalhamento em
[03 §3](03-plataforma-e-arquitetura.md#3-app-01--onboarding-cadastro-e-registro-de-presença).

**Requisitos:**
- Tela inicial em que o usuário escolhe a interação: **começar por áudio** ou **começar por
  texto (chat)**.
- Interação cognitiva conduzida por **IA**, tolerante a respostas fora de ordem, capaz de
  repetir e confirmar dados.
- Captação e reprodução de áudio via **`mediadevices.js`**
  (`navigator.mediaDevices.getUserMedia`) + reconhecimento e síntese de fala.
- Captura da **imagem do jogador** pela câmera do dispositivo.
- **Novo jogador:** salvar nome, nick, data de nascimento ou idade, **Comunidade Virtual de
  vínculo (obrigatória, escolhida entre as já criadas pelos Admins)**, características
  desejadas do avatar e foto. O jogador fica **ativo** ao final, sem exigir autorização do
  responsável nesta etapa.
- **Vínculo à comunidade:** a conversa oferece a lista de comunidades existentes; se nenhuma
  servir, o caso é escalado a um Admin, que cria a comunidade antes de concluir o cadastro
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)).
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

## PRD-05 — App 05: Área do Jogador (jornada gamificada)

**Escopo:** experiência logada do jogador, com **guia e apoio nas trilhas** — qual é o
próximo ponto, o que precisa ser feito, o que já foi conquistado e o que está bloqueado.

**Requisitos:** escolha de poder; trilhas com desbloqueio por quiz/desafio, seguindo a
anatomia e o motor de pontuação do
[modelo de gamificação](11-modelo-de-gamificacao.md); desafios
semanais (on-line 10 pts, presencial 10 pts, equipe 10 pts, família 20 pts); **desafios
extras propostos por Apoiadores** — abertos ou **direcionados ao jogador** —, vinculados à
trilha em andamento, com **pontos extras** e recompensa extra em quantidade declarada
([04 §5](04-modelo-economico-e-sustentabilidade.md#5-interação-apoiadores-x-jogadores-desafios-extras));
equipes mistas de até 5 e Equipe Familiar; **séries de coleta de dados do território** —
próxima medição, histórico do que já foi registrado, situação da série (ativa/interrompida) e
pontos que ela está rendendo
([02 §1](02-conceito-do-jogo-e-gamificacao.md#registro-temporal-e-pontuação-enquanto-a-coleta-durar));
ranking; troca de pontos por recompensas (kits de alimentos; catálogo a expandir); pedido de
ajuda para atividades escolares; níveis 1–5 (assíduo → **Mestre Aprendiz**, apto ao
treinamento de multiplicador); badges por trilha e por poder.

**Autonomia no encontro assíncrono:** a App 05 é o que permite ao jogador saber **o que fazer
em seguida sem depender do Mestre** — requisito direto da dinâmica assíncrona dos encontros
presenciais ([05 §3](05-implantacao-e-operacao.md#definição-vigente-o-encontro-é-assíncrono)).
Precisa funcionar em **aparelho compartilhado do ponto de apoio** (troca rápida de sessão) e
mostrar com clareza o próximo ponto da trilha e o que está bloqueado.

**Requisitos adicionais:** estado de **perfil público** desbloqueado apenas com
autorização do responsável (sem ela, histórico e perfil não são divulgados); representação
exclusivamente por avatar; desafios com níveis de dificuldade graduais acessíveis a toda a
faixa de 6 a 16 anos; **acervo do jogador** — o **livro da linha Alpha recebido na abertura
da trilha** (que é dele, sem devolução) e os exemplares permanentes em uso de bancada, com a
**ficha de vida do livro** (quem cuidou dele antes) e o badge **Guardião do Acervo**
([05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação)).

**Questões em aberto:** definição da tabela de pontos das recompensas (os valores atuais
são apenas sugestão); mecânica antifraude de pontos; acessibilidade para quem só tem
celular, com aparelho compartilhado ou sem dados móveis (uso no ponto de apoio).

## PRD-06 — App 02: Assistente por voz e Modo Ouvinte

**Escopo:** Web App de áudio nos moldes do [Robô Educa](06-robo-educa.md) — **JavaScript no
frontend + IA no backend** — com dois modos de operação
([03 §4](03-plataforma-e-arquitetura.md#4-app-02--assistente-por-voz-e-modo-ouvinte)).

**Requisitos:**
- **Modo Conversa:** interação educacional por voz ("converse com seu robô") — quiz,
  explicação de conceitos e apoio às atividades escolares.
- **Modo Ouvinte:** a aplicação acompanha o que é falado durante a aula e, **quando
  acionada**, opina sobre o tema em discussão ou responde a perguntas dirigidas a ela.
- Captação e reprodução de áudio via `navigator.mediaDevices.getUserMedia`; reconhecimento
  de fala e síntese de voz em pt-BR.
- Ativação do Modo Ouvinte pelo Mestre, com **indicação visível e permanente** de que está
  ativo e desligamento a qualquer momento.
- **Sem gravação persistente do áudio da turma**; retenção mínima e definida da transcrição
  estritamente necessária.
- Aviso prévio a jogadores e responsáveis, com **direito de recusa e alternativa
  equivalente** de participação na aula.
- Filtros de segurança de conteúdo no nível mais restritivo.
- Captação de perfil para personalização ([PRD-11](#prd-11--personalização-por-ia)).
- Registro de dados do território **por voz**, alimentando as séries da Comunidade Virtual
  sem exigir digitação ([06-robo-educa.md](06-robo-educa.md#5-ganchos-com-a-plataforma)).
- Envio da evolução do aluno aos responsáveis pela própria plataforma — entregue pela
  **App 07** ([PRD-13](#prd-13--app-07-área-dos-pais-e-responsáveis)).

**Questões em aberto:** provedor e custo do modelo de IA; processamento de áudio no
dispositivo x nuvem; base legal e prazo de retenção da transcrição de aula com menores;
critério de acionamento do Modo Ouvinte (palavra-chave, botão do Mestre ou ambos);
comportamento em salas barulhentas.

## PRD-07 — Economia de Recursos e Transparência (ledger)

**Escopo:** livro-razão de recursos aportados e consumidos; "Poder Econômico".

**Requisitos:** todo custo de toda ação atribuído a um personagem; recurso alocado
computado como "moeda" no histórico do provedor; atividade condicionada a lastro; tipos de
recurso: hora-aula, lanche, recompensas, insumos, cloud, serviços; visibilidade pública da
riqueza movimentada.

**Recursos duráveis (patrimônio) e empréstimo:** além dos consumíveis, o ledger precisa
tratar material que **não se consome no uso e é reaproveitado a cada turma** — o caso
concreto é o acervo de 298 livros doado pelo Goethe-Institut. Requisitos:

- Registro por **exemplar tombado**: título, número de tombo, ponto de apoio, estado de
  conservação e movimentações entre pontos.
- **Empréstimo e devolução** vinculados a jogador e a módulo/trilha, com histórico de quem
  usou cada exemplar e devoluções pendentes no painel do dia.
- O aporte credita o Poder Econômico do Apoiador **uma única vez**, sem baixa por consumo.
- Suporte ao **regime misto** já decidido: **linha Alpha doada ao jogador na abertura da
  trilha** (baixa definitiva, tratada como recompensa entregue), **linha Include I como
  patrimônio permanente** e **kits MDF como consumível de atividade**, com saldo de estoque
  ([04 §1](04-modelo-economico-e-sustentabilidade.md#primeiro-aporte-registrado--acervo-didático-e-kits-do-goethe-institut)).
- **Perda ou dano não gera débito para o jogador nem para a família**: gera uma
  **necessidade de reposição** a ser aportada por Apoiador
  ([05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação)).
- **Doações em espécie (PIX)** registradas como aporte financeiro do doador, com comprovante
  anexado ([04 §2](04-modelo-economico-e-sustentabilidade.md#doações-em-espécie--canal-oficial)).

**Desafios extras de Apoiadores e rastreio de efetividade:** o ledger precisa registrar não
só o aporte, mas **o que aconteceu por causa dele**
([04 §5](04-modelo-economico-e-sustentabilidade.md#5-interação-apoiadores-x-jogadores-desafios-extras)).
Requisitos:

- **Desafio extra** como entidade: Apoiador proponente, trilha vinculada, Mestre validador,
  **Admin aprovador**, recompensa oferecida, **quantidade disponível**, critério de
  atribuição (ordem de conclusão), **pontos extras**, período de vigência, **modalidade
  (aberto ou direcionado)** e — no direcionado — **jogador destinatário e justificativa do
  vínculo aprovada** ([02 §4](02-conceito-do-jogo-e-gamificacao.md#desafio-extra-direcionado)).
- Recompensa extra **creditada no histórico do Apoiador** e computada no Poder Econômico,
  com lastro exigido **antes** da publicação do desafio.
- **Realizações dos jogadores** naquele desafio vinculadas ao histórico do Apoiador — a base
  para relatórios de **efetividade do apoio ao longo do tempo** (quantos concluíram, em que
  trilhas, com que retenção).
- Nenhum dado de contato de jogador exposto ao Apoiador: o relatório é **agregado e por
  avatar**, respeitando a regra de mediação e a LGPD.

**Questões em aberto:** unidade de conta (R$? pontos?); valoração da hora-aula; valoração de
acervo e kits doados (valor de mercado, simbólico ou apenas contagem física); relatórios
públicos por atividade/comunidade/provedor; **formato do relatório de efetividade** entregue
ao Apoiador (quais números, com que periodicidade, em que nível de agregação).

## PRD-08 — Comunidades Virtuais e dados do território

**Escopo:** representação digital da comunidade real em que o jogador vive, construída
pelos próprios jogadores — a base *Data Driven* da plataforma
([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)).

**Requisitos:**
- **Criação exclusiva por Admin**, com a comunidade nascendo **vazia** (nome, localização,
  granularidade) — não há autocadastro de comunidade.
- **Vínculo obrigatório do jogador a uma comunidade**, colhido no onboarding e alterável
  apenas pela gestão, com data da mudança preservada.
- A comunidade virtual **existe na medida em que dados reais são registrados**.
- Atividades de coleta: temperatura local, precipitação pluviométrica, coleta de resíduos,
  buracos na via, iluminação, trânsito, transporte público, fotos e memórias.
- **Toda trilha tem ao menos um desafio de coleta**
  ([02 §3](02-conceito-do-jogo-e-gamificacao.md#regra-vigente-toda-trilha-coleta-dados-reais)).
- **Série temporal como unidade do modelo**: cadência declarada, registros datados, jogador
  coletor, comunidade e estado da série (ativa / interrompida / retomada).
- **Pontuação recorrente enquanto a série durar** e cessação do cômputo na interrupção, sem
  perda dos pontos já creditados
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#registro-temporal-e-pontuação-enquanto-a-coleta-durar)).
- **Guarda permanente** dos registros, para avaliações e análises futuras, **com o jogador
  coletor identificado** — o vínculo autoria ↔ registro não é removido nem anonimizado no
  armazenamento.
- **Anonimização na saída**: exportações, painéis públicos, pesquisas e entregas a
  instituições recebem dados agregados e anonimizados; a autoria individual não sai da
  plataforma.
- **Granularidade hierárquica** do registro: comunidade → bairro → rua → condomínio →
  bloco → quadra.
- Cada registro alimenta e "constrói" visualmente a comunidade digital — mapeamento
  dado → elemento visual em
  [11 §8.3](11-modelo-de-gamificacao.md#83-representação-visual-da-comunidade-virtual).
- **Poder do Território**: as séries sustentadas pelo jogador alimentam a progressão e os
  badges desse poder ([02 §2](02-conceito-do-jogo-e-gamificacao.md#2-poderes-habilidades)).
- Painéis públicos por comunidade; dados como **insumo para tomada de decisões** por
  moradores, associações, escolas, poder público e pesquisas.
- Exportação/API aberta dos dados agregados e anonimizados.

**Questões em aberto:** fontes e sensores (registro manual x sensor construído pelo
jogador x API pública); curadoria e **veracidade dos dados**; cadência e valor em pontos por
tipo de coleta; **janela de tolerância** antes de considerar a série interrompida; teto de
pontos por período; georreferenciamento sem expor endereço de criança; tecnologia de
armazenamento das séries temporais.

## PRD-09 — Conteúdo e Trilhas (autoria dos Mestres)

**Escopo:** ferramenta para Mestres criarem trilhas, conteúdos, quizzes e desafios.

**Requisitos:** trilhas mensais seguindo a **anatomia formal do
[modelo de gamificação](11-modelo-de-gamificacao.md#2-anatomia-da-trilha)** — em modelo
**agnóstico de área do conhecimento**, apto a trilhas de humanas, artes, esportes e cultura
tanto quanto às técnicas — incluindo a **paginação da trilha pelas etapas do ciclo**
([11 §2.3](11-modelo-de-gamificacao.md#23-distribuição-da-trilha-pelas-etapas-do-ciclo));
conteúdo próprio e de terceiros; quiz/desafio para
desbloqueio; **publicação dos artefatos que comprovam a habilidade do Mestre**; catálogo
inicial de poderes: **IA/Robótica e Poder do Território** nesta etapa — **Redes, Soft
Skills, PNED/BNCC, Rima e Capoeira ficam para ciclo futuro**
([02 §3](02-conceito-do-jogo-e-gamificacao.md#demais-trilhas-previstas)); banco de perguntas
do **Quiz ao Vivo** cadastrado pelo curador da aula; **fluxo de desafio extra proposto por
Apoiador** — aberto ou **direcionado** —, com validação obrigatória do Mestre da trilha e
**aprovação de Admin** antes da publicação
([02 §4](02-conceito-do-jogo-e-gamificacao.md#desafios-extras-propostos-por-apoiadores));
paralelos obrigatórios com outras áreas do conhecimento e com os valores do projeto.

**Coleta de dados como requisito de toda trilha:** a ferramenta deve **impedir a publicação
de uma trilha sem ao menos um desafio de coleta de dados reais**
([02 §3](02-conceito-do-jogo-e-gamificacao.md#regra-vigente-toda-trilha-coleta-dados-reais)).
O Mestre define, no desafio, **o que se mede, com que cadência e por quanto tempo** — os três
parâmetros que a série temporal precisa para existir e para pontuar de forma recorrente.

**Primeiras trilhas (conteúdo já existente):** **[Robô Educa](06-robo-educa.md)** (1ª) e
**[Batalha de Laser](07-batalha-de-laser.md)** (2ª), ambas de autoria do Mestre fundador
([02 §3](02-conceito-do-jogo-e-gamificacao.md#as-duas-primeiras-trilhas-da-plataforma)).
São o conteúdo de validação do módulo: se a ferramenta modela essas duas, modela as demais.

**Material de apoio impresso:** o modelo de trilha precisa suportar **bibliografia de apoio
por ponto de trilha** — a coleção Include doada pelo Goethe-Institut apoia as duas trilhas
acima
([02 §3](02-conceito-do-jogo-e-gamificacao.md#acervo-didático-de-apoio--coleção-include-e-kits-mdf-goethe-institut)).
Requisitos: vincular um ponto de trilha a **título e capítulo recomendados**;
indicar ao jogador se há **exemplar disponível no seu ponto de apoio**; e creditar o
**Apoiador que forneceu o material** onde ele é indicado.

**Questões em aberto:** formato dos conteúdos (vídeo, texto, interativo); revisão/curadoria
pedagógica; licença dos conteúdos (Creative Commons?).

## PRD-10 — Batalhas e eventos presenciais

**Escopo:** cadastro, operação e registro de batalhas (disputas de ideias e realizações).

**Requisitos:** batalhas presenciais e de projetos; culminância; estatísticas de partida
(ex.: telemetria do Nexus na Batalha de Laser); resultados alimentando ranking e
portfólio; integração Nexus → API **[Proposta]** — padrão de integração de batalhas
físicas com o backend em
[11 §8.4](11-modelo-de-gamificacao.md#84-jogos-sobre-o-backend-app-04-e-terceiros).
Batalhas são marcos de trilha de **qualquer área** (disputa de laser, batalha de rima,
roda de capoeira), não apenas técnicas
([11 §2](11-modelo-de-gamificacao.md#2-anatomia-da-trilha)).

## PRD-11 — Personalização por IA

**Escopo:** captação de perfil e adaptação de conteúdo.

**Requisitos:** plataforma capta o perfil conforme o aluno interage e entrega informação
personalizada; usar habilidade que o aluno já possui para ensinar outros assuntos
(interdisciplinaridade); filtros de segurança de conteúdo no nível mais restritivo em toda
interação com crianças.

**Fora desta etapa:** a visão computacional aplicada à **análise de movimentos de capoeira**
(captação sugerida com MediaPipe, TensorFlow como alternativa para classificar os movimentos)
acompanha a trilha de Capoeira, que fica para **ciclo futuro**
([02 §3](02-conceito-do-jogo-e-gamificacao.md#demais-trilhas-previstas)).

**Questões em aberto:** modelo/stack de IA; limites éticos e LGPD para perfis de menores;
explicabilidade para responsáveis.

## PRD-12 — App 04: Jogo em JavaScript

**Escopo:** jogo executado no navegador, construído sobre a **base de personagens da
plataforma**
([03 §6](03-plataforma-e-arquitetura.md#6-app-04--jogo-em-javascript)).

**Requisitos:** uso dos avatares, poderes, badges e níveis já conquistados como elementos do
jogo — a composição dos **cards dos personagens** e o **contrato do jogo com o motor**
(leitura de progresso + débito de pontos, nunca crédito) seguem
[11 §8.2](11-modelo-de-gamificacao.md#82-cards-dos-personagens) e
[11 §8.4](11-modelo-de-gamificacao.md#84-jogos-sobre-o-backend-app-04-e-terceiros);
representação exclusivamente por **avatar, nunca por imagem real**; código aberto e
legível, apto a virar conteúdo de trilha do Poder da IA e Robótica; execução em navegador de
celular modesto e tolerância a rede instável.

**Definição vigente — o jogo consome pontuação, não a gera.** O progresso no App 04 **não
produz pontos na plataforma**: os pontos vêm das atividades propostas pelos Mestres e da
coleta de dados do território. O jogo lê o progresso do jogador (poderes, badges, níveis) e
pode consumir pontos, mas **nunca escreve pontuação**
([03 §6](03-plataforma-e-arquitetura.md#6-app-04--jogo-em-javascript)). Em termos de API:
o App 04 tem **acesso de leitura ao progresso e de débito de pontos**, e nenhum endpoint de
crédito — o que também elimina, por construção, a fraude por automação de cliques.

**Sugestão técnica:** engine **Phaser.js** — jogos 2D em JavaScript rodando no próprio
navegador, sem instalação, com desempenho adequado a aparelhos modestos e código legível o
bastante para virar material de trilha
([03 §6](03-plataforma-e-arquitetura.md#6-app-04--jogo-em-javascript)).

**Questões em aberto:** gênero e mecânica do jogo; o que exatamente os pontos compram dentro
do jogo; modo offline; multiplayer local nas aulas presenciais.

## PRD-13 — App 07: Área dos pais e responsáveis

**Escopo:** Web App autenticado dos **pais e responsáveis**, canal oficial da plataforma com
a família ([03 §9](03-plataforma-e-arquitetura.md#9-app-07--área-dos-pais-e-responsáveis)).
Substitui a comunicação por mensageria de terceiros, fora do escopo desta etapa.

**Requisitos:**
- **Vínculo responsável ↔ jogador(es)**, conferido por Admin; o responsável só enxerga os
  jogadores sob sua responsabilidade.
- **Evolução do jogador**: presença, atividades realizadas, pontos, poderes, badges, nível e
  progresso nas trilhas.
- **Autorização de divulgação pública** do histórico e do perfil — concessão e **revogação**,
  com efeito imediato na vitrine e nos rankings públicos
  ([02 §9](02-conceito-do-jogo-e-gamificacao.md#9-manual-do-jogador-fluxo-de-entrada)).
- **Direitos de recusa** exercíveis a qualquer tempo: foto de presença (PRD-04), Modo Ouvinte
  em sala (PRD-06) e uso de imagem em vídeos e fotos de eventos — **sempre com alternativa
  equivalente** garantida ao jogador, nunca com exclusão da atividade.
- **Transparência de dados**: quais dados da criança estão armazenados, para que servem, por
  quanto tempo ficam e **quem os acessou**.
- **Solicitações com protocolo e status**: acesso, correção, exclusão e esclarecimentos —
  encaminhadas à fila de atendimento da App 03 ([PRD-02](#prd-02--app-03-frontend-de-gestão)).
- **Limite explícito do pedido de exclusão**: os registros de dados do território têm guarda
  permanente com autoria preservada e **não são apagados**; a tela e o termo precisam dizer
  isso antes do aceite
  ([03 §10](03-plataforma-e-arquitetura.md#10-proteção-de-dados-em-toda-a-plataforma-lgpd)).
- **Termos e consentimentos versionados**, com data/hora e histórico consultável.
- **Linguagem simples**, no mesmo padrão exigido da política de privacidade.
- **Sem qualquer canal com Apoiadores ou terceiros** — é canal exclusivo entre família e
  plataforma, sob a mesma regra de mediação dos desafios extras
  ([04 §5](04-modelo-economico-e-sustentabilidade.md#5-interação-apoiadores-x-jogadores-desafios-extras)).

**Por que é MVP e não onda seguinte:** a hipótese **H2** do Ciclo 01 mede exatamente quantos
responsáveis tomam conhecimento do tratamento de dados e aceitam os termos
([10 §3](10-case-01-guerreira-zeferina.md#3-hipóteses-do-ciclo-01-formuladas-em-jul2026)).
Sem esta aplicação, H2 não é mensurável — é anedota.

**Questões em aberto:** login próprio do responsável x vínculo ao cadastro do jogador; prazos
formais de resposta às solicitações; notificação ativa (e-mail) além da consulta no Web App;
como atender responsável sem smartphone ou sem e-mail.

---

## Ordem sugerida de elaboração **[Proposta]**

1. **PRD-01 (API)** — tudo depende dele; incluir desde já o modelo do ledger (PRD-07) e
   das Comunidades Virtuais (PRD-08) no domínio, mesmo que a UI venha depois.
2. **PRD-04 (onboarding)** — é a porta de entrada real das aulas presenciais; sem ele não
   há cadastro nem registro de presença.
3. **PRD-03 (App 06 — vitrine)** — entrega visibilidade rápida e material para captar
   apoiadores.
4. **PRD-02 (App 03 — gestão)** — necessário para operar o primeiro ciclo presencial,
   inclusive a criação das Comunidades Virtuais, os painéis do dia e o Quiz ao Vivo.
5. **PRD-13 (App 07 — área dos responsáveis)** — condição para medir a hipótese H2 do Ciclo
   01 e para dar efeito prático aos direitos de recusa já prometidos.
6. **PRD-06 (App 02 — assistente por voz)** — reaproveita a base do Robô Educa, já em
   produção, e entra em uso já nas primeiras aulas.
7. **PRD-05 (App 05 — área do jogador)** — a jornada gamificada em si.
8. **PRD-09/10** — conteúdo do primeiro Mestre + primeira batalha.
9. **PRD-12 (App 04 — jogo)**, **PRD-07, 08 e 11** — em ondas seguintes, conforme
   [05-implantacao-e-operacao.md](05-implantacao-e-operacao.md#11-fases-sugeridas-de-implantação-do-piloto-proposta).

> Dica operacional: este repositório já dispõe de skills de PRD (fases 1–5: elicitação,
> geração, revisão, patch e gestão de mudanças). Cada bloco acima pode alimentar a Fase 1
> (elicitação) diretamente.
