# 09 — Tópicos em Aberto e Propostas

Este documento reúne (a) pontos que ainda dependem de decisão do fundador e (b) propostas
de novos tópicos e abordagens. Nada aqui é decisão tomada — é pauta.

## 1. Decisões pendentes

| Tema | Situação / encaminhamento |
|---|---|
| Nome do projeto | Adotado: **Comunidade Game**. Alternativa em avaliação: **Inova Comunidade**. Decidir antes de registrar domínio, marca e identidade visual. |
| Lema "GOAT / The Best / Somos os melhores" | Já é momento fixo da aula presencial ([05 §3](05-implantacao-e-operacao.md#3-roteiro-da-aula-presencial)). Decidir se vira também slogan oficial de comunicação. |
| Pontuação das recompensas | Kits de alimentos e demais recompensas: valores atuais são apenas sugestão ([02 §8](02-conceito-do-jogo-e-gamificacao.md#8-recompensas)). |
| Provedor de IA e de reconhecimento facial do onboarding | Custo, privacidade e processamento no dispositivo x nuvem ([08 PRD-04](08-base-para-prds.md#prd-04--onboarding-cadastro-e-registro-de-presença)). |
| Prazo de retenção da foto de presença | Definir número em dias/meses e rotina de exclusão automática. |
| Licenças | Código (AGPL/MIT?) e conteúdo educacional (Creative Commons?). |
| Orquestrador "do explore ao merge" | Automação do fluxo de desenvolvimento com agentes de IA. Definir se entra em `CONTRIBUTING.md`/automação do repositório. |
| Uso do Slack no fluxo de desenvolvimento | Ferramenta de comunicação do time. Decidir. |
| Git como canal entre agentes e humanos | Proposta: GitHub Issues + labels como canal padrão; Discussions para debate; Projects para roadmap. |
| Sub-marcas | **Rôbróders** e **Robô Educa** podem nomear sub-produtos (ex.: os kits "Rôbróders"). |
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
  jogadores.
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
  anti-feminicídio; mestras mulheres como referência.

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
  ([05 §9](05-implantacao-e-operacao.md#9-replicabilidade)).

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
   [PRD-04 (Onboarding)](08-base-para-prds.md#prd-04--onboarding-cadastro-e-registro-de-presença).
4. Redigir o Código de Conduta, o termo de autorização dos responsáveis e o termo de
   consentimento para captura de imagem (necessários antes da primeira aula com
   onboarding).
5. Escrever o roteiro pedagógico da oficina do [Robô Educa](06-robo-educa.md), primeira
   atividade do piloto.
6. Documentar o case Guerreira Zeferina enquanto a memória está fresca.
