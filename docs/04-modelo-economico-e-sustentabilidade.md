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

### Pessoa jurídica vinculada ao projeto

**Definição vigente.** A pessoa jurídica que representa o projeto perante terceiros é a
**Robô Educa — Kits Robóticos Educacionais**:

| | |
|---|---|
| **Razão social / nome** | Robô Educa — Kits Robóticos Educacionais |
| **CNPJ** | 51.730.395/0001-19 |
| **Responsável legal** | Carlos Antonio Sales — o mesmo **fundador e autor do projeto** ([01 §7](01-visao-valores-e-proposito.md#7-o-fundador-primeiro-admin-e-primeiro-mestre)) |

É essa pessoa jurídica que **recebe doações, assina termos e responde formalmente** pelos
aportes registrados no livro-razão — o primeiro deles, o Termo de Doação do acervo do
Goethe-Institut (abaixo).

> **Nota de governança:** existir CNPJ resolve o problema imediato — receber doação e assinar
> termo hoje —, mas **não encerra** a discussão da forma jurídica adequada para editais e
> recursos públicos, que normalmente exigem entidade sem fins lucrativos (associação, OSCIP
> ou fiscal sponsor). Os dois assuntos coexistem
> ([09 §2](09-topicos-em-aberto-e-sugestoes.md#entidade-jurídica-e-compliance)).

### Primeiro aporte registrado — acervo didático e kits do Goethe-Institut

O **Goethe-Institut (Salvador)** doou ao projeto uma coleção de **298 livros** do projeto
**Include**, da **Campus Party** (robótica educativa: mecânica, eletrônica, sensores e
programação), e **30 kits em MDF** para as trilhas do Robô Educa — e passa a ser um dos
**primeiros Apoiadores** da plataforma. Os livros são **material de apoio** das trilhas Robô
Educa e Batalha de Laser — inventário completo em
[02 §3](02-conceito-do-jogo-e-gamificacao.md#acervo-didático-de-apoio--coleção-include-e-kits-mdf-goethe-institut).

**Formalização.** A doação dos livros se deu por meio de um **Termo de Doação assinado**
entre o **Goethe-Institut (Salvador)** e a **Robô Educa — Kits Robóticos Educacionais**
(acima). O termo é o **documento comprobatório do aporte** — exatamente o tipo de artefato
que a plataforma exige de todo Apoiador
([02 §1](02-conceito-do-jogo-e-gamificacao.md#apoiadores--patrocinadores)) — e deve ficar
anexado ao cadastro do Apoiador na App 03.

É o **primeiro caso concreto** da economia descrita acima e serve de referência para todos
os aportes seguintes:

- Entra no histórico do provedor e compõe o **Poder Econômico** do Goethe-Institut, visível
  publicamente na plataforma.
- Dá **lastro material** às duas trilhas existentes: material didático de apoio e corpo do
  robô já disponíveis, sem custo adicional para o primeiro ciclo.

**Tratamento no livro-razão — regime misto (definição vigente):**

| Item | Destino | Como entra no ledger |
|---|---|---|
| **Livros da linha Alpha** (252) | **Doados ao jogador quando ele começa a trilha** | **Recompensa entregue** — baixa definitiva do acervo, como qualquer prêmio durável ([02 §8](02-conceito-do-jogo-e-gamificacao.md#8-recompensas)) |
| **Livros da linha Include I** (46) | **Acervo permanente do ponto de apoio** | **Patrimônio permanente** — sem baixa por consumo, com controle de guarda por ponto de apoio (quantos exemplares, onde, em que estado) |
| **Kits MDF** (30) | Insumo das oficinas do Robô Educa | **Consumível de atividade** — baixa conforme os kits são montados pelos jogadores |

A estratégia de guarda e conservação correspondente está em
[05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação).

> **A definir:** critério de valoração do acervo e dos kits no livro-razão (valor de mercado,
> valor simbólico ou apenas contagem física) e responsável pela guarda em cada ponto de apoio
> ([09 §1](09-topicos-em-aberto-e-sugestoes.md#1-decisões-pendentes)).

## 2. Fontes de receita

- **Doações de parceiros** (pessoas físicas e jurídicas).
- **Publicidade** - Vitrine Pública
- **Pesquisas** — os dados de território gerados pelas Comunidades Virtuais
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)) podem sustentar
  estudos e diagnósticos, sempre **anonimizados** e com retorno para a própria comunidade.
- **Editais**.
- **Campanhas de crowdfunding** para:
  - Financiamento das aulas e kits;
  - Financiamento de equipamentos (celulares, notebooks, tablets etc.).

### Doações em espécie — canal oficial

**Definição vigente.** As doações em dinheiro são feitas por **PIX**, em nome da pessoa
jurídica vinculada ao projeto (§1):

| | |
|---|---|
| **Chave PIX** | `51.730.395/0001-19` (CNPJ) |
| **Titular** | Robô Educa — Kits Robóticos Educacionais |

Regras que se aplicam a essas doações, como a qualquer outro aporte:

- Toda doação recebida é **registrada no livro-razão** e compõe o **Poder Econômico** do
  doador (§1) — dinheiro não é exceção à regra de transparência, é o caso em que ela mais
  importa.
- O doador pode ser **pessoa física ou jurídica**, e é cadastrado como Apoiador por um Admin,
  com o comprovante anexado
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#apoiadores--patrocinadores)).
- A chave é publicada na **vitrine pública (App 06)**, na seção "Como apoiar"
  ([03 §8](03-plataforma-e-arquitetura.md#8-app-06--vitrine-pública-apresentação-da-plataforma)).

## 5. Interação Apoiadores x Jogadores (desafios extras)

Aportar recurso é o começo da relação do Apoiador com a plataforma, não o fim dela. A
**interação Apoiador–Jogador** acontece por meio de **desafios extras**: durante um ciclo em
andamento, o Apoiador propõe um desafio ligado a uma trilha em curso e oferece uma
**recompensa extra** a quem o concluir
([02 §4](02-conceito-do-jogo-e-gamificacao.md#desafios-extras-propostos-por-apoiadores)).
O desafio extra pode ser **aberto** (a todos os jogadores da trilha) ou **direcionado** a
um jogador específico
([02 §4](02-conceito-do-jogo-e-gamificacao.md#desafio-extra-direcionado)).

> Um resumo prático de toda a relação do Apoiador com a plataforma está no
> **[Guia do Apoiador](12-guia-do-apoiador.md)**.

**Como funciona no ciclo:**

1. O Apoiador propõe o desafio extra, vinculado a uma **trilha em andamento**, e indica a
   recompensa que vai custear e **em que quantidade**.
2. O **Mestre da trilha valida** — o desafio precisa fazer sentido pedagógico no ponto em que
   os jogadores estão.
3. Um **Admin aprova** (ou não) a publicação
   ([03 §5](03-plataforma-e-arquitetura.md#5-app-03--gestão-administrativa)).
4. O desafio é publicado para **todos os jogadores daquela trilha** — ou, no caso do
   **desafio direcionado**, entregue ao jogador destinatário — com a recompensa, a
   quantidade disponível e o critério de atribuição visíveis desde o início.
5. Os jogadores que concluem recebem **pontos extras** e, até esgotar a quantidade ofertada,
   a **recompensa extra**.

### Definições vigentes dos desafios extras

| Questão | Definição |
|---|---|
| **Pontos** | O desafio extra **vale pontos além da recompensa**, computados **isoladamente como pontos extras** — não se misturam à pontuação regular da trilha |
| **Teto de desafios simultâneos** | **Não há teto por trilha.** O controle é qualitativo: cada desafio é **aprovado ou não por um Admin**, caso a caso, após a validação pedagógica do Mestre |
| **Exclusividade** | **Proibida nos desafios abertos**: o desafio é **aberto a todos os que concluírem** — ninguém é barrado de disputar. A exceção controlada é o **desafio direcionado** (linha abaixo) |
| **Desafio direcionado** | O Apoiador pode **direcionar um desafio a um jogador específico** — só ele recebe a recompensa se atingir os requisitos. Exige **justificativa registrada** do vínculo/interesse (ex.: parente próximo — tio(a), padrinho, madrinha) e **aprovação de um Admin**, além da validação do Mestre. Mediação total mantida: nenhum contato direto ([02 §4](02-conceito-do-jogo-e-gamificacao.md#desafio-extra-direcionado)) |
| **Quantidade de recompensas** | **Uma única** (para quem cumprir primeiro o desafio com sucesso) **ou várias** — todos que concluírem recebem, até o limite disponibilizado pelo Apoiador |

Por que o teto foi substituído por aprovação: um número fixo protegeria a trilha do excesso,
mas também barraria um bom desafio pela razão errada — a ordem de chegada. A aprovação caso a
caso protege a trilha pelo motivo certo — **o mérito pedagógico da proposta** — e mantém a
porta aberta para o Apoiador que quer contribuir de verdade.

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
  sempre **mediados pela plataforma**, como em toda relação patrocinador–aluno. O canal da
  família é exclusivo da App 07
  ([03 §9](03-plataforma-e-arquitetura.md#9-app-07--área-dos-pais-e-responsáveis)) e não é
  compartilhado com Apoiadores.
- **Lastro antes da publicação**: a recompensa extra é recurso como qualquer outro — precisa
  estar provida antes de o desafio ir ao ar (§1).
- **Curadoria do Mestre é condição, não formalidade**: desafio extra sem validação pedagógica
  vira publicidade dentro de uma trilha infantil, o que o projeto não admite.
- Recompensas seguem o cuidado de dignidade já previsto para o catálogo
  ([02 §8](02-conceito-do-jogo-e-gamificacao.md#8-recompensas)).

> **A definir:** o formato do **relatório de efetividade** entregue ao Apoiador — quais
> números, com que periodicidade e em que nível de agregação
> ([09 §1](09-topicos-em-aberto-e-sugestoes.md#1-decisões-pendentes)).

## 6. Impacto social

- **[Case 01 — Comunidade Guerreira Zeferina](10-case-01-guerreira-zeferina.md)**, Salvador
  (BA): primeiro piloto real, Ciclo 01 de **agosto a dezembro de 2026**.
- **Acervo didático de 298 livros e 30 kits MDF** doados pelo Goethe-Institut, que viram
  trilhas abertas na plataforma — material que atende turmas inteiras sem custo para o aluno,
  com o livro da linha Alpha **ficando com o jogador** (§1).
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
