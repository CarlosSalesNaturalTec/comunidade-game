# 08 — Tópicos em Aberto e Sugestões

Este documento reúne (a) notas soltas dos originais que foram preservadas mas precisam de
decisão, e (b) sugestões de novos tópicos e abordagens não presentes nos documentos
originais. Nada aqui é decisão tomada — é pauta.

## 1. Notas soltas dos originais (preservadas, aguardando decisão)

| Nota original | Origem | Situação / encaminhamento |
|---|---|---|
| "GOAT / The Best / Somos os melhores (mentira de quem sempre disse o contrário)" | `linhas_gerais.md` | Incorporada como lema do projeto em [01](01-visao-valores-e-proposito.md#o-lema). Decidir se vira slogan oficial de comunicação. |
| "habilidades:" / "atividades:" (itens incompletos) | `linhas_gerais.md` | Estruturados em [02](02-conceito-do-jogo-e-gamificacao.md); catálogo de poderes e tipos de atividade preenchidos com o material da implantação. |
| Orquestrador para disparar ações "do explore ao merge" | `linhas_gerais.md` | Nota de engenharia do processo de desenvolvimento (agentes de IA no fluxo dev). Definir se entra num doc `CONTRIBUTING.md`/automação do repositório. |
| "Como usar o Slack" | `linhas_gerais.md` | Idem — ferramenta de comunicação do time de desenvolvimento. |
| "Ferramentas Git utilizadas para comunicação entre os agentes e um humano. Seriam Issues?" | `linhas_gerais.md` | Sugestão: sim — GitHub Issues + labels como canal padrão em projeto open source; Discussions para debate; Projects para roadmap. |
| Dois kits de alimentos com o mesmo custo (20 pts) | `Manual de Instruções.txt` | ✅ **Decidido (jul/2026):** a pontuação de kits e demais recompensas é sugestão, a ser definida ([02 §8](02-conceito-do-jogo-e-gamificacao.md#8-recompensas)). |
| Faixas etárias divergentes (8–18 vs 6–14/14+) | `premissas.txt` vs `Implantação` | ✅ **Decidido (jul/2026):** faixa oficial de **6 a 16 anos**, com atividades em níveis de dificuldade graduais acessíveis a todas as idades ([01 §5](01-visao-valores-e-proposito.md#5-público-alvo)). |
| Nomes alternativos: Rôbróders, Robô Educa | `Implantação` | Preservados; podem nomear sub-produtos (ex.: os kits "Rôbróders"). |
| Personagens Susy, Otávio, Rôbróders e prof. Carlos Trenell | `Implantação` | Base da narrativa de comunicação; formalizar universo/roteiro dos personagens. |
| Case Guerreira Zeferina | `Implantação` | Documentar o case como referência de implantação do piloto. |

## 2. Sugestões de novos tópicos **[Sugestão nova]**

Percebidos como lacunas durante a compilação — nenhum consta dos originais:

### Proteção da criança e do adolescente (prioridade máxima)
- ✅ **Já decidido (jul/2026):** LGPD considerada em TODO o projeto; jogadores
  representados por avatares (nunca imagem real); **adesão em duas etapas** — cadastro
  livre (nome, data de nascimento, nick, avatar) já permite participar das atividades,
  e a **divulgação pública do histórico/perfil** exige autorização dos pais ou
  responsáveis; cards de jogadores **sem links para redes sociais nem contato direto** —
  apenas avatar, badges, poderes e desempenho na plataforma.
- A detalhar: política de privacidade formal; papel de "encarregado de dados" (DPO).
- A detalhar: consentimento específico para vídeos de culminância e fotos de eventos com
  jogadores.
- Mediação de toda interação adulto–criança pela plataforma (incl. patrocinadores).
- Política de salvaguarda (safeguarding) para atividades presenciais: cadastro e
  verificação de mestres/voluntários, adulto nunca sozinho com criança, canal de denúncia.

### Governança open source
- `LICENSE` (sugestão: código AGPL/MIT a decidir; conteúdo educacional Creative Commons).
- `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `GOVERNANCE.md`.
- Modelo de decisão (quem aprova mudanças de rumo) e marca (quem pode usar o nome
  "Comunidade Game" ao replicar).

### Entidade jurídica e compliance
- Forma jurídica para receber doações/editais (associação, OSCIP, fiscal sponsor).
- Prestação de contas formal conectada ao ledger de transparência
  ([04](04-modelo-economico-e-sustentabilidade.md)).

### Indicadores de impacto
- Métricas de aprendizado, retenção, encaminhamento para TI, recursos movimentados —
  definidas antes do piloto para permitir comparação (baseline).

### Acessibilidade e inclusão
- Acessibilidade digital (WCAG) e de conteúdo (linguagem simples).
- Estratégia para jogadores sem smartphone próprio (contas familiares, ponto de apoio).
- Recorte de gênero: metas de participação de meninas, coerente com a causa
  anti-feminicídio; mestras mulheres como referência.

### Segurança física nas atividades
- Normas de segurança para laser, eletrônica e ferramentas nas oficinas
  ([06](06-batalha-de-laser.md#integração-com-a-plataforma-sugestão-nova)).

### Poderes alinhados aos valores
- "Poder da Ancestralidade", "Poder do Cuidado", "Poder do Território"
  ([02 §2](02-conceito-do-jogo-e-gamificacao.md#2-poderes-habilidades)).

### Kit de Implantação (playbook de replicação)
- O documento que torna o modelo replicável de fato
  ([05 §8](05-implantacao-e-operacao.md#8-replicabilidade)).

### Parcerias institucionais
- Escolas públicas (a premissa cita escolas de ensino fundamental): protocolo de parceria
  com secretarias de educação; alinhamento PNED/BNCC como argumento.
- Universidades: estagiários/extensão como força de trabalho e pesquisa.

## 3. Próximos passos sugeridos **[Sugestão nova]**

1. Validar esta compilação e corrigir o que estiver incoerente com a visão do fundador.
2. Decidir as questões restantes da tabela §1 (licenças, orquestrador/Slack/Issues) —
   faixa etária e recompensas já decididas em jul/2026.
3. Rodar a Fase 1 de elicitação de PRD com o [PRD-01 (API)](07-base-para-prds.md#prd-01--backend-api-núcleo).
4. Redigir o Código de Conduta e o termo de autorização dos responsáveis (necessário
   antes de qualquer divulgação pública de histórico/perfil de jogadores).
5. Documentar o case Guerreira Zeferina enquanto a memória está fresca.
