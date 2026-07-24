# 04 — Modelo Econômico e Sustentabilidade

> Fontes: `linhas_gerais.md`, `Comunidade Game - Linhas Gerais 2025.txt`, `Implantação Jun 2024.rtf`, `premissas.txt`

## 1. A economia de recursos da plataforma

Princípio central (a "moeda" do Comunidade Game):

> **Todas as ações ocorridas na plataforma — aulas, lanches, até a hospedagem de servidores
> e prestadores de serviços — deverão ter seus custos computados e atribuídos a um
> personagem (Jogador, Mestre ou Apoiador).** Assim se registra a riqueza movimentada pela
> plataforma, trazendo transparência sobre os recursos.

Regras derivadas:

- Os recursos necessários para realizar atividades — **hora-aula do mentor, lanche,
  recompensas, insumos (LEDs, baterias, papel etc.)** — são fornecidos por Mestres ou
  Apoiadores.
- Cada recurso alocado em atividades é **computado para o respectivo provedor**, como
  "moeda" aportada na plataforma e **acumulada no histórico do provedor**.
- **Cada atividade só acontece se tiver os recursos necessários** providos por Mestre ou
  Apoiador — não há atividade sem lastro.
- O acumulado de aportes forma o **"Poder Econômico"** do provedor, visível na plataforma
  ([02-conceito-do-jogo-e-gamificacao.md](02-conceito-do-jogo-e-gamificacao.md#2-poderes-habilidades)):
  o reconhecimento público de quem sustenta o projeto.

**[Sugestão nova]** Modelar isso tecnicamente como um **livro-razão (ledger)** de dupla
entrada: cada atividade consome recursos (débito) aportados por provedores (crédito). Isso
viabiliza relatórios públicos de prestação de contas por atividade, por comunidade e por
provedor — transparência auditável, essencial para captar doações e editais.

## 2. Fontes de receita

- **Doações de parceiros** (pessoas físicas e jurídicas).
- **Publicidade.**
- **Pesquisas** (geração de dados para tomada de decisões — com os devidos cuidados de
  anonimização).
- **Projetos** e **editais**.
- **Monetizações web.**
- **Campanhas de crowdfunding** para:
  - Financiamento das aulas e kits;
  - Financiamento de equipamentos (celulares, notebooks, tablets etc.).
- **Venda de kits** de robótica ("Compre o Kit" na jornada do aluno) — para públicos que
  podem pagar, subsidiando as comunidades atendidas gratuitamente.

## 3. Despesas para funcionamento

- Hora do professor nas aulas presenciais.
- Hora do professor na gravação de conteúdo.
- Diária do professor para ponto de apoio.
- Prêmios/consumíveis.
- Prêmios/duráveis.
- Despesas com plataforma (cloud).
- Custos de cursos presenciais: professor + material + ajuda de custo para estagiários +
  lanche.

## 4. Parcerias

Modelo de parceria previsto:

- O parceiro **financia a implementação de cursos presenciais** (professor + material +
  ajuda de custos para estagiários + lanche).
- Em contrapartida, **ganha o direito de "interagir" com seus alunos patrocinados** (alunos
  e pais) — relação direta e humanizada entre quem financia e quem é beneficiado.
- Ao final dos módulos, **os alunos gravam vídeo com suas realizações e agradecimentos aos
  parceiros** — prestação de contas afetiva e material de divulgação.

**[Sugestão nova]** Definir limites claros dessa "interação" patrocinador–aluno para
proteger crianças e adolescentes (comunicação sempre mediada pela plataforma/organizadores,
nunca contato direto privado). Isso protege os jovens e também os parceiros.

## 5. Impacto social

- **Cursos/Bootcamps para comunidades sem cobrança para os alunos.**
- **Case real: Guerreira Zeferina** (referência de implantação/piloto).
- **Caça-talentos**: identificar jovens talentos e encaminhá-los (premissa de
  encaminhamento para a área de TI e economia criativa).
- **Multiplicadores**: alunos formados viram instrutores de novos cursos em comunidades —
  fecha o ciclo com o Nível 5 da gamificação
  ([02-conceito-do-jogo-e-gamificacao.md](02-conceito-do-jogo-e-gamificacao.md#7-níveis-e-badges-gamificação)).

**[Sugestão nova]** Definir **indicadores de impacto** desde o início (nº de alunos ativos,
retenção, trilhas concluídas, jovens encaminhados para cursos/empregos de TI, recursos
movimentados por comunidade). Além de guiar o projeto, são exatamente os números exigidos
por editais e grandes doadores.

## 6. Sustentabilidade (síntese)

O projeto é sustentável quando o ciclo se fecha:

```
Apoiadores/Parceiros aportam recursos ──► Atividades acontecem (com lastro)
        ▲                                          │
        │                                          ▼
Transparência + vídeos + Poder Econômico ◄── Jogadores aprendem, pontuam e realizam
        ▲                                          │
        └────────── novos multiplicadores ◄────────┘
```

A transparência do livro-razão e a visibilidade pública das realizações são o que renova a
confiança dos apoiadores e atrai novos recursos.
