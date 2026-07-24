# 05 — Implantação e Operação

> Fontes: `Comunidade Game - Linhas Gerais 2025.txt`, `Implantação Jun 2024.rtf`, `linhas_gerais.md`, `premissas.txt`

## 1. Estratégia de implantação

O projeto será implantado **inicialmente em uma comunidade próxima à residência do
fundador** (piloto), e deve servir de **modelo de implantação para qualquer comunidade do
país**. O case de referência citado nos originais é a **Guerreira Zeferina**.

A implantação combina presença física (pontos de apoio, encontros) com presença digital
(WhatsApp, Web App), justamente porque o público-alvo tem acesso desigual a equipamentos.

## 2. Estrutura física — Pontos de apoio

- **Pontos de apoio nas comunidades**: hackerspace, fab lab, coworking.
- São a base para aulas presenciais, montagem de kits, batalhas e atividades de culminância.
- Custo operacional previsto: diária do professor para o ponto de apoio
  ([04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md#3-despesas-para-funcionamento)).

## 3. Formatos de atividade

| Formato | Descrição |
|---|---|
| Encontros presenciais | Oficinas e treinamentos nos pontos de apoio |
| Atividades on-line | Conteúdo entre encontros; trilhas |
| Desafios on-line | Semanais, pontuados |
| Desafios presenciais | Semanais, pontuados; batalhas |
| Atividades de culminância | Apresentação pública de trabalhos, encerramento de módulos |

## 4. Cursos presenciais

- **Duração:** conforme as trilhas.
- **Formato:** aulas presenciais + desafios.
- **Custos a levantar por curso:** professor + material + ajuda de custos para
  estagiários + lanche.
- **Gratuitos para os alunos** das comunidades (financiados por parceiros/doações —
  ver [04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md#4-parcerias)).
- Ao final dos módulos, alunos gravam vídeo com realizações e agradecimentos aos parceiros.

## 5. Formação de mentores

- **Formação de mentores** é linha de ação explícita do projeto.
- O caminho natural é a própria gamificação: o jogador Nível 4 (apoia os colegas) evolui
  para **Nível 5 — Instrutor**
  ([02-conceito-do-jogo-e-gamificacao.md](02-conceito-do-jogo-e-gamificacao.md#7-níveis-e-badges-gamificação)).
- **Multiplicadores** formados abrem novos cursos em novas comunidades — é o mecanismo de
  escala do projeto.
- Regra de admissão de mestres: especificar a habilidade e prová-la com conteúdo (aulas
  presenciais e/ou gravadas).
- **Estagiários** locais recebem ajuda de custo — porta de entrada remunerada para jovens
  da própria comunidade.

## 6. Comunicação e divulgação

- **Formação de equipe de divulgação nas redes sociais** (linha de ação explícita).
- Canais: Facebook, Instagram, WhatsApp, YouTube, TikTok — canais institucionais do
  projeto (os cards dos jogadores não exibem redes sociais pessoais, por definição de
  LGPD/proteção de menores).
- Narrativa/personagens: **os irmãos Susy e Otávio, os Rôbróders e o professor Carlos
  Trenell** (vídeo de apresentação da plataforma).
- O **"Poder das Redes"** conecta divulgação e formação: os próprios jogadores aprendem
  produção de conteúdo produzindo para o projeto.
- Vídeos de culminância dos alunos são material de divulgação e prestação de contas.

## 7. Papel dos responsáveis e da família

- Envio da **evolução do aluno para os responsáveis via WhatsApp**.
- **Atividades em família** valem pontuação dobrada (20 pts) — engajar a família é
  estratégia de permanência.
- **Equipe Familiar** como modalidade de equipe.

## 8. Replicabilidade

Condições já previstas nos originais para que qualquer comunidade replique o modelo:

1. **Código open source** ([03-plataforma-e-arquitetura.md](03-plataforma-e-arquitetura.md)).
2. **Backend como API aberta** para novos frontends locais.
3. **Comunidades Virtuais** como unidade de organização — cada território tem sua
   representação.
4. **Modelo econômico com lastro local**: atividades só acontecem com recursos providos
   por mestres/apoiadores da própria rede.
5. **Multiplicadores** formados pela gamificação.

**[Sugestão nova]** Criar um **"Kit de Implantação"** (playbook): passo a passo documentado
para uma nova comunidade — requisitos mínimos (ponto de apoio, 1 mestre, 1 apoiador),
checklist legal (termos de consentimento, LGPD/ECA), materiais de divulgação editáveis e
orçamento-modelo de um primeiro ciclo de oficinas. É o documento que transforma "open
source" em "replicável de fato".

**[Sugestão nova]** Definir a **entidade jurídica/governança** da iniciativa (associação,
OSCIP, coletivo com fiscal sponsor) — necessária para receber doações, firmar parcerias e
participar de editais.

## 9. Fases sugeridas de implantação do piloto **[Sugestão nova]**

| Fase | Entrega | Depende de |
|---|---|---|
| 0 — Fundação | Código de conduta, termos de consentimento, identidade visual, comunidade piloto definida | — |
| 1 — Vitrine + cadastro | Frontend público + API com cadastro de personas | PRD-01/02 ([07-base-para-prds.md](07-base-para-prds.md)) |
| 2 — Jogo mínimo | Poderes, trilha de robótica do primeiro Mestre, pontuação manual via gestão | Fase 1 |
| 3 — Primeiro ciclo presencial | Oficinas + Batalha de Laser + culminância com vídeo | Fase 2 + ponto de apoio + recursos com lastro |
| 4 — Economia visível | Livro-razão público, Poder Econômico, relatórios de transparência | Fase 3 |
| 5 — Escala | WhatsApp bot, personalização por IA, kit de implantação para 2ª comunidade | Fases 3–4 |
