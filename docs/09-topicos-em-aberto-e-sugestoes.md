# 09 — Tópicos em Aberto e Propostas

Este documento reúne (a) pontos que ainda dependem de decisão do fundador e (b) propostas
de novos tópicos e abordagens. Nada aqui é decisão tomada — é pauta.

## 1. Decisões pendentes

| Tema | Situação / encaminhamento |
|---|---|
| Nome do projeto | Adotado: **Comunidade Game**. Alternativa em avaliação: **Inova Comunidade**. Decidir antes de registrar domínio, marca e identidade visual. |
| Lema "GOAT / The Best / Podemos nos tornar os melhores" | Já é momento fixo da aula presencial ([05 §3](05-implantacao-e-operacao.md#3-roteiro-da-aula-presencial)). Decidir se vira também slogan oficial de comunicação e se a versão longa precisa de uma forma curta para peças gráficas (ex.: **"Vamos ser os melhores"**, **"O melhor se constrói"**). |
| Pontuação das recompensas | Kits de alimentos e demais recompensas: valores atuais são apenas sugestão ([02 §8](02-conceito-do-jogo-e-gamificacao.md#8-recompensas)). |
| Provedor de IA e de reconhecimento facial do onboarding | Custo, privacidade e processamento no dispositivo x nuvem ([08 PRD-04](08-base-para-prds.md#prd-04--app-01-onboarding-cadastro-e-registro-de-presença)). |
| Prazo de retenção da foto de presença | Definir número em dias/meses e rotina de exclusão automática. |
| **Modo Ouvinte do App 02** | O assistente acompanha o que é falado na aula. Definir formalmente: critério de acionamento, o que é transcrito e por quanto tempo é retido, base legal e forma do aviso/consentimento a jogadores e responsáveis, e a alternativa para quem recusar ([03 §2.1.1](03-plataforma-e-arquitetura.md#211-app-02--assistente-por-voz-e-modo-ouvinte)). **Prioridade alta** — envolve captação de voz de crianças. |
| Canal de comunicação com os responsáveis | Com a saída do WhatsApp do escopo ([03 §2](03-plataforma-e-arquitetura.md#2-canais--meios-de-acesso)), definir por onde a evolução do aluno chega à família: área do responsável no Web App, e-mail, ou ambos. |
| Pontuação e regras do Quiz ao Vivo | Pontos da vitória, formato de resposta (equipe x representante), critério de desempate e nº de dispositivos por equipe ([05 §4](05-implantacao-e-operacao.md#4-atividade-modelo-quiz-ao-vivo)). |
| Mecânica do jogo (App 04) | Gênero do jogo e se o progresso nele gera ou apenas consome pontos da plataforma ([08 PRD-12](08-base-para-prds.md#prd-12--app-04-jogo-em-javascript)). |
| **Acervo Include: doar ou reaproveitar** | Definir se os 298 livros doados pelo Goethe-Institut serão **doados aos jogadores** ou **reaproveitados** entre turmas. Sugestão em avaliação: **regime misto** — doar os títulos abundantes da linha Alpha a quem concluir a trilha e manter os títulos escassos da linha Include I como acervo do ponto de apoio ([05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação)). **Decisão anterior à primeira turma.** |
| Estratégia de conservação do acervo | Caso haja reaproveitamento: validar a estratégia proposta (tombamento, ficha de vida do exemplar, ritual de posse na 1ª aula, badge "Guardião do Acervo", guarda por equipe, reposição solidária) e escrever no código de conduta a **distinção entre descuido deliberado e dano acidental** ([05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação)). |
| Valoração e guarda do acervo | Como o acervo entra no livro-razão (valor de mercado, simbólico ou contagem física) e quem responde pela guarda em cada ponto de apoio ([04 §1](04-modelo-economico-e-sustentabilidade.md#primeiro-aporte-registrado--acervo-didático-do-goethe-institut)). |
| Mapeamento dos livros nas trilhas | Identificar o conteúdo de cada título e indicar **qual capítulo apoia qual ponto** das trilhas Robô Educa e Batalha de Laser. Trabalho de leitura, não de criação de trilha nova. |
| Licenças | Código (AGPL/MIT?) e conteúdo educacional (Creative Commons?). |
| Orquestrador "do explore ao merge" | Automação do fluxo de desenvolvimento com agentes de IA. Definir se entra em `CONTRIBUTING.md`/automação do repositório. |
| Uso do Slack no fluxo de desenvolvimento | Ferramenta de comunicação do time. Decidir. |
| Git como canal entre agentes e humanos | Proposta: GitHub Issues + labels como canal padrão; Discussions para debate; Projects para roadmap. |
| Submarcas | **Rôbróders** e **Robô Educa** podem nomear subprodutos (ex.: os kits "Rôbróders"). |
| Universo dos personagens | Susy, Otávio, Rôbróders e prof. Carlos Trenell — formalizar roteiro e identidade da narrativa. |
| Case Guerreira Zeferina | Documentar como referência de implantação do piloto. |

## 2. Propostas de novos tópicos **[Proposta]**

### Proteção da criança e do adolescente (prioridade máxima)
- **Já definido:** LGPD considerada em TODO o projeto; jogadores representados por avatares
  (nunca imagem real) na vitrine; **adesão em duas etapas** — cadastro livre já permite
  participar, e a **divulgação pública do histórico/perfil** exige autorização dos pais ou
  responsáveis; cards de jogadores **sem links para redes sociais nem contato direto**;
  foto de presença com **finalidade única** e alternativa para quem recusar
  ([03 §5.3](03-plataforma-e-arquitetura.md#53-requisitos-de-proteção-de-dados-lgpd-aplicada)).
- A detalhar: política de privacidade formal; papel de "encarregado de dados" (DPO).
- A detalhar: consentimento específico para vídeos de culminância e fotos de eventos com
  jogadores — vale também para o material produzido na trilha de **Social Media**
  ([02 §3](02-conceito-do-jogo-e-gamificacao.md#demais-trilhas-previstas)).
- A detalhar: **captação de voz em sala** pelo Modo Ouvinte do App 02 — a mesma exigência de
  finalidade declarada, minimização, retenção definida e alternativa para quem recusar que
  se aplica à foto de presença.
- A detalhar: **verificação e supervisão dos voluntários** recrutados entre jogadores
  Mestres Aprendizes, muitos deles ainda menores de idade
  ([05 §7](05-implantacao-e-operacao.md#7-formação-de-mestres-e-multiplicadores)).
- Mediação de toda interação adulto–criança pela plataforma (incl. patrocinadores).
- Política de salvaguarda (*safeguarding*) para atividades presenciais: verificação de
  mestres/voluntários, adulto nunca sozinho com criança, canal de denúncia.
- **Dados de território x privacidade**: registrar rua/bloco/quadra sem permitir inferir o
  endereço de uma criança específica.

### Governança open source
- `LICENSE`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `GOVERNANCE.md`.
- Modelo de decisão (quem aprova mudanças de rumo) e marca (quem pode usar o nome do
  projeto ao replicar).

### Entidade jurídica e compliance
- Forma jurídica para receber doações/editais (associação, OSCIP, fiscal sponsor).
- Prestação de contas formal conectada ao ledger de transparência
  ([04](04-modelo-economico-e-sustentabilidade.md)).

### Indicadores de impacto
- Métricas de aprendizado, retenção, atividades realizadas, dados de território
  registrados e recursos movimentados — definidas antes do piloto para permitir comparação
  (baseline).

### Acessibilidade e inclusão
- Acessibilidade digital (WCAG) e de conteúdo (linguagem simples).
- Estratégia para jogadores sem smartphone próprio (contas familiares, ponto de apoio).
- Recorte de gênero: metas de participação de meninas, coerente com a causa
  antifeminicídio; mestras mulheres como referência.

### Segurança física nas atividades
- Normas de segurança para laser, eletrônica e ferramentas nas oficinas
  ([07](07-batalha-de-laser.md#integração-com-a-plataforma-proposta)).

### Poderes alinhados aos valores
- "Poder da Ancestralidade", "Poder do Cuidado", "Poder do Território"
  ([02 §2](02-conceito-do-jogo-e-gamificacao.md#2-poderes-habilidades)).

### Currículo de temas transversais
- Como cada atividade técnica abre paralelo com outras áreas do conhecimento e com os
  temas do projeto (racismo, violência contra mulheres, identidade, povos originários) —
  um guia prático para os Mestres, não apenas princípio no papel.

### Kit de Implantação (playbook de replicação)
- O documento que torna o modelo replicável de fato
  ([05 §10](05-implantacao-e-operacao.md#10-replicabilidade)).

### Parcerias institucionais
- Escolas públicas: protocolo de parceria com secretarias de educação; alinhamento
  PNED/BNCC como argumento.
- Universidades: estagiários/extensão como força de trabalho e pesquisa.
- Instituições que possam **consumir os dados** das Comunidades Virtuais (prefeitura,
  defesa civil, associações de moradores) — devolvendo valor ao território.

## 3. Próximos passos sugeridos **[Proposta]**

1. Validar esta documentação e corrigir o que estiver incoerente com a visão do fundador.
2. Decidir os itens da tabela §1 — em especial nome do projeto, licenças e provedor de IA.
3. Rodar a Fase 1 de elicitação de PRD com o
   [PRD-01 (API)](08-base-para-prds.md#prd-01--backend-api-núcleo) e o
   [PRD-04 (Onboarding)](08-base-para-prds.md#prd-04--app-01-onboarding-cadastro-e-registro-de-presença).
4. Redigir o Código de Conduta, o termo de autorização dos responsáveis e o termo de
   consentimento para captura de imagem (necessários antes da primeira aula com
   onboarding).
5. Escrever o roteiro pedagógico da oficina do [Robô Educa](06-robo-educa.md), primeira
   trilha do piloto.
6. **Cadastrar o Goethe-Institut como Apoiador** e registrar o aporte dos 298 livros no
   inventário — é o primeiro caso real da economia de recursos
   ([04 §1](04-modelo-economico-e-sustentabilidade.md#primeiro-aporte-registrado--acervo-didático-do-goethe-institut)).
7. **Decidir doação x reaproveitamento do acervo** e, se houver reaproveitamento, tombar os
   exemplares e implantar a estratégia de conservação antes da primeira turma
   ([05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação)).
8. **Ler o acervo Include**, título a título, e mapear qual capítulo apoia qual ponto das
   trilhas Robô Educa e Batalha de Laser.
8. Documentar o case Guerreira Zeferina enquanto a memória está fresca.
