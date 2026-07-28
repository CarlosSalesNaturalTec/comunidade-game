# 04 — Modelo Econômico e Sustentabilidade

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

**[Proposta]** Modelar isso tecnicamente como um **livro-razão (ledger)** de dupla
entrada: cada atividade consome recursos (débito) aportados por provedores (crédito). Isso
viabiliza relatórios públicos de prestação de contas por atividade, por comunidade e por
provedor — transparência auditável, essencial para captar doações e editais.

### Primeiro aporte registrado — acervo didático do Goethe-Institut

O **Goethe-Institut** doou ao projeto uma coleção de **298 livros** do projeto **Include**,
da **Campus Party** (robótica educativa: mecânica, eletrônica, sensores e programação), e
passa a ser um dos **primeiros Apoiadores** da plataforma. Os livros são **material de apoio**
das trilhas Robô Educa e Batalha de Laser — inventário completo em
[02 §3](02-conceito-do-jogo-e-gamificacao.md#acervo-didático-de-apoio--coleção-include-goethe-institut).

É o **primeiro caso concreto** da economia descrita acima e serve de referência para todos
os aportes seguintes:

- Entra no histórico do provedor e compõe o **Poder Econômico** do Goethe-Institut, visível
  publicamente na plataforma.
- Dá **lastro material** às duas trilhas existentes: material didático de apoio que já está
  disponível, sem custo adicional para o primeiro ciclo.

**O tratamento no livro-razão depende de uma decisão ainda pendente:**

| Destino do exemplar | Como entra no ledger |
|---|---|
| **Doado ao jogador** | **Recompensa entregue** — baixa definitiva do acervo, como qualquer prêmio durável ([02 §8](02-conceito-do-jogo-e-gamificacao.md#8-recompensas)) |
| **Reaproveitado entre turmas** | **Patrimônio permanente** — sem baixa por consumo, com controle de guarda por ponto de apoio (quantos exemplares, onde, em que estado) |

O encaminhamento sugerido é um **regime misto** — doação dos títulos abundantes a quem
concluir a trilha e retenção dos títulos escassos como acervo do ponto de apoio —, detalhado
com a respectiva estratégia de conservação em
[05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação).

> **A definir:** doação x reaproveitamento; critério de valoração do acervo no livro-razão
> (valor de mercado dos exemplares, valor simbólico ou apenas contagem física); e responsável
> pela guarda em cada ponto de apoio
> ([09 §1](09-topicos-em-aberto-e-sugestoes.md#1-decisões-pendentes)).

## 2. Fontes de receita

- **Doações de parceiros** (pessoas físicas e jurídicas).
- **Publicidade.**
- **Pesquisas** — os dados de território gerados pelas Comunidades Virtuais
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)) podem sustentar
  estudos e diagnósticos, sempre **anonimizados** e com retorno para a própria comunidade.
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
  ajuda de custo para estagiários + lanche).
- Em contrapartida, **ganha o direito de "interagir" com seus alunos patrocinados** (alunos
  e pais) — relação direta e humanizada entre quem financia e quem é beneficiado.
- Ao final dos módulos, **os alunos gravam vídeo com suas realizações e agradecimentos aos
  parceiros** — prestação de contas afetiva e material de divulgação.

**[Proposta]** Definir limites claros dessa "interação" patrocinador–aluno para
proteger crianças e adolescentes (comunicação sempre mediada pela plataforma/organizadores,
nunca contato direto privado). Isso protege os jovens e também os parceiros.

## 5. Interação Apoiadores x Jogadores (desafios extras)

Aportar recurso é o começo da relação do Apoiador com a plataforma, não o fim dela. A
**interação Apoiador–Jogador** acontece por meio de **desafios extras**: durante um ciclo em
andamento, o Apoiador propõe um desafio ligado a uma trilha em curso e oferece uma
**recompensa extra** a quem o concluir
([02 §4](02-conceito-do-jogo-e-gamificacao.md#desafios-extras-propostos-por-apoiadores)).

**Como funciona no ciclo:**

1. O Apoiador propõe o desafio extra, vinculado a uma **trilha em andamento**, e indica a
   recompensa que vai custear.
2. O **Mestre da trilha valida** — o desafio precisa fazer sentido pedagógico no ponto em que
   os jogadores estão.
3. O desafio é publicado para os jogadores daquela trilha, com a recompensa visível.
4. Os jogadores que concluem recebem a **recompensa extra**, além dos pontos da atividade.

**O que fica registrado no histórico do Apoiador:**

| Registro | Para que serve |
|---|---|
| **Recompensas creditadas** — o que ele custeou e entregou | Compõe o **Poder Econômico** (§1), como qualquer outro aporte |
| **Realizações dos jogadores** nos desafios que ele propôs | Mostra **o que aconteceu** por causa daquele apoio |

É essa segunda linha que muda o jogo: o histórico deixa de responder apenas *"quanto foi
aportado"* e passa a responder *"o que esse apoio produziu"*. Ao longo do tempo, torna-se
possível **rastrear a efetividade do apoio oferecido** — quais desafios engajaram, quantos
jogadores concluíram, em que trilhas o apoio rendeu mais.

Para o projeto, é o argumento de captação mais forte que existe: um Apoiador que vê o efeito
concreto do que financiou tem motivo para financiar de novo. Para o jogador, é a prova de que
há gente de fora torcendo pelo que ele está construindo.

**Salvaguardas obrigatórias:**

- **Sem contato direto** entre Apoiador e criança. Proposta, entrega e reconhecimento são
  sempre **mediados pela plataforma**, como em toda relação patrocinador–aluno (§4).
- **Lastro antes da publicação**: a recompensa extra é recurso como qualquer outro — precisa
  estar provida antes de o desafio ir ao ar (§1).
- **Curadoria do Mestre é condição, não formalidade**: desafio extra sem validação pedagógica
  vira publicidade dentro de uma trilha infantil, o que o projeto não admite.
- Recompensas seguem o cuidado de dignidade já previsto para o catálogo
  ([02 §8](02-conceito-do-jogo-e-gamificacao.md#8-recompensas)).

> **A definir:** se o desafio extra vale pontos além da recompensa; teto de desafios extras
> simultâneos por trilha (para não descaracterizar a trilha do Mestre); e se a recompensa
> extra pode ser exclusiva de um jogador ou precisa estar aberta a todos os que concluírem
> ([09 §1](09-topicos-em-aberto-e-sugestoes.md#1-decisões-pendentes)).

## 6. Impacto social

- **Cursos/Bootcamps para comunidades sem cobrança para os alunos.**
- **[Case 01 — Comunidade Guerreira Zeferina](10-case-01-guerreira-zeferina.md)**, Salvador
  (BA): primeiro piloto real, Ciclo 01 de **agosto a dezembro de 2026**.
- **Acervo didático de 298 livros** doado pelo Goethe-Institut, que vira trilhas abertas na
  plataforma — material que atende turmas inteiras sem custo para o aluno (§1).
- **Oficinas do Robô Educa desde 2018**: centenas de crianças impactadas em comunidades de
  Salvador (BA) — ver [06-robo-educa.md](06-robo-educa.md).
- **Dados para a comunidade**: as Comunidades Virtuais devolvem ao território evidência
  para tomada de decisões ([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)).
- **Multiplicadores**: alunos formados viram instrutores de novos cursos em comunidades —
  fecha o ciclo com o **Nível 5 (Mestre Aprendiz)** da gamificação
  ([02 §7](02-conceito-do-jogo-e-gamificacao.md#7-níveis-e-badges-gamificação)).

**[Proposta]** Definir **indicadores de impacto** desde o início (nº de alunos ativos,
retenção, trilhas concluídas, atividades realizadas, volume de dados de território
registrados, recursos movimentados por comunidade). Além de guiar o projeto, são
exatamente os números exigidos por editais e grandes doadores.

## 7. Sustentabilidade (síntese)

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
