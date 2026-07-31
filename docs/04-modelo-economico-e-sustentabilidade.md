# 04 — Modelo Econômico e Sustentabilidade

## 1. A economia de recursos da plataforma

Princípio central — a "moeda" do Comunidade Game:

> **Todas as ações ocorridas na plataforma — aulas, lanches, hospedagem de servidores,
> prestadores de serviço — têm seus custos computados e atribuídos a um personagem (Jogador,
> Mestre ou Apoiador).** Assim se registra a riqueza movimentada, trazendo transparência sobre
> os recursos.

Regras derivadas:

- Os recursos das atividades — **hora-aula do mentor, lanche, recompensas, insumos** — são
  fornecidos por Mestres ou Apoiadores.
- Cada recurso alocado é **computado para o respectivo provedor** e acumulado no seu
  histórico.
- **Cada atividade só acontece se tiver os recursos providos** — não há atividade sem lastro.
- O acumulado forma o **"Poder Econômico"** do provedor, visível na plataforma: o
  reconhecimento público de quem sustenta o projeto.

**[Proposta]** Modelar tecnicamente como um **livro-razão (ledger) de dupla entrada**: cada
atividade consome recursos (débito) aportados por provedores (crédito). Viabiliza relatórios
públicos de prestação de contas por atividade, por comunidade e por provedor — transparência
auditável, essencial para captar doações e editais.

### Pessoa jurídica vinculada ao projeto

**Definição vigente.** A pessoa jurídica que representa o projeto perante terceiros:

| | |
|---|---|
| **Razão social / nome** | Robô Educa — Kits Robóticos Educacionais |
| **CNPJ** | 51.730.395/0001-19 |
| **Responsável legal** | Carlos Antonio Sales — o mesmo fundador e autor do projeto |

É ela que **recebe doações, assina termos e responde formalmente** pelos aportes registrados
no livro-razão.

> **Nota de governança:** o CNPJ resolve o problema imediato — receber doação e assinar termo
> hoje —, mas **não encerra** a discussão da forma jurídica adequada para editais e recursos
> públicos, que normalmente exigem entidade sem fins lucrativos (associação, OSCIP ou *fiscal
> sponsor*). Os dois assuntos coexistem (documento 09).

### Primeiro aporte registrado — acervo e kits do Goethe-Institut

O **Goethe-Institut (Salvador)** doou **298 livros** do projeto **Include**, da **Campus
Party**, e **30 kits em MDF** para as trilhas do Robô Educa — tornando-se um dos **primeiros
Apoiadores** da plataforma. A doação dos livros foi formalizada por **Termo de Doação
assinado** com a Robô Educa — Kits Robóticos Educacionais: o **documento comprobatório do
aporte**, exatamente o tipo de artefato que a plataforma exige de todo Apoiador, e que fica
anexado ao cadastro do Apoiador na App 03.

É o **primeiro caso concreto** da economia descrita acima: entra no histórico do provedor,
compõe o **Poder Econômico** do Goethe-Institut e dá **lastro material** às duas trilhas
existentes, sem custo adicional para o primeiro ciclo.

**Tratamento no livro-razão — regime misto (definição vigente):**

| Item | Destino | Como entra no ledger |
|---|---|---|
| **Livros da linha Alpha** (252) | Doados ao jogador quando ele começa a trilha | **Recompensa entregue** — baixa definitiva do acervo |
| **Livros da linha Include I** (46) | Acervo permanente do ponto de apoio | **Patrimônio permanente** — sem baixa por consumo, com controle de guarda |
| **Kits MDF** (30) | Insumo das oficinas do Robô Educa | **Consumível de atividade** — baixa a cada montagem |

Inventário completo, regime de posse e estratégia de conservação: documento 05.

> **A definir:** critério de valoração do acervo e dos kits no livro-razão (valor de mercado,
> valor simbólico ou apenas contagem física) e responsável pela guarda em cada ponto de apoio.

## 2. Fontes de receita

- **Doações** de pessoas físicas e jurídicas.
- **Publicidade** na vitrine pública.
- **Pesquisas** — os dados de território das Comunidades Virtuais podem sustentar estudos e
  diagnósticos, sempre **anonimizados** e com retorno para a própria comunidade.
- **Editais.**
- **Campanhas de crowdfunding** para financiar aulas, kits e equipamentos (celulares,
  notebooks, tablets).

### Doações em espécie — canal oficial

**Definição vigente.** As doações em dinheiro são feitas por **PIX**, em nome da pessoa
jurídica vinculada:

| | |
|---|---|
| **Chave PIX** | `51.730.395/0001-19` (CNPJ) |
| **Titular** | Robô Educa — Kits Robóticos Educacionais |

- Toda doação recebida é **registrada no livro-razão** e compõe o **Poder Econômico** do
  doador — dinheiro não é exceção à regra de transparência, é o caso em que ela mais importa.
- O doador é cadastrado como Apoiador por um Admin, com o comprovante anexado.
- A chave é publicada na vitrine pública, na seção "Como apoiar".

## 3. Interação Apoiadores × Jogadores: desafios extras

Aportar recurso é o começo da relação do Apoiador com a plataforma, não o fim. A interação
Apoiador–Jogador acontece por **desafios extras**: durante um ciclo em andamento, o Apoiador
propõe um desafio ligado a uma trilha em curso e oferece uma **recompensa extra** a quem o
concluir.

**Como funciona no ciclo:**

1. O Apoiador propõe o desafio, vinculado a uma **trilha em andamento**, e indica a recompensa
   que vai custear e **em que quantidade**.
2. O **Mestre da trilha valida** — o desafio precisa fazer sentido pedagógico no ponto em que
   os jogadores estão.
3. Um **Admin aprova** (ou não) a publicação.
4. O desafio é publicado para todos os jogadores daquela trilha — ou, no caso do direcionado,
   entregue ao destinatário — com recompensa, quantidade disponível e critério de atribuição
   visíveis desde o início.
5. Quem conclui recebe **pontos extras** e, até esgotar a quantidade ofertada, a recompensa.

### Definições vigentes

| Questão | Definição |
|---|---|
| **Pontos** | O desafio extra vale **pontos além da recompensa**, computados **isoladamente como pontos extras** — não se misturam à pontuação regular da trilha |
| **Teto de desafios simultâneos** | **Não há teto por trilha.** O controle é qualitativo: cada desafio é aprovado ou não por um Admin, caso a caso, após a validação do Mestre |
| **Exclusividade** | **Proibida nos desafios abertos**: ninguém é barrado de disputar. O que é limitado é a **quantidade** de recompensas, declarada de antemão |
| **Desafio direcionado** | O Apoiador pode **direcionar um desafio a um jogador específico** — só ele recebe a recompensa se atingir os requisitos. Exige **justificativa registrada** do vínculo (ex.: parente próximo — tio(a), padrinho, madrinha) e aprovação de Admin, além da validação do Mestre |
| **Quantidade de recompensas** | **Uma única** (para quem concluir primeiro) **ou várias** — todos que concluírem recebem, até o limite disponibilizado |

Por que o teto foi substituído por aprovação: um número fixo protegeria a trilha do excesso,
mas barraria um bom desafio pela razão errada — a ordem de chegada. A aprovação caso a caso
protege a trilha pelo motivo certo: **o mérito pedagógico da proposta**.

O desafio direcionado é o caminho para o apoio de interesse direto e legítimo — por exemplo,
um parente próximo que propõe um desafio para um jogador da sua parentela — sem abrir exceção
nas salvaguardas.

### Rastreio de efetividade

**O que fica registrado no histórico do Apoiador:**

| Registro | Para que serve |
|---|---|
| **Recompensas creditadas** — o que ele custeou e entregou | Compõe o **Poder Econômico**, como qualquer outro aporte |
| **Realizações dos jogadores** nos desafios que ele propôs | Mostra **o que aconteceu** por causa daquele apoio |

É a segunda linha que muda o jogo: o histórico deixa de responder apenas *"quanto foi
aportado"* e passa a responder *"o que esse apoio produziu"* — quais desafios engajaram,
quantos jogadores concluíram, em que trilhas o apoio rendeu mais. Para o projeto, é o
argumento de captação mais forte que existe; para o jogador, é a prova de que há gente de fora
torcendo pelo que ele está construindo.

### Salvaguardas obrigatórias

- **Sem contato direto** entre Apoiador e criança. Proposta, entrega e reconhecimento são
  sempre **mediados pela plataforma**. O canal da família é exclusivo da App 07 e não é
  compartilhado com Apoiadores.
- **Lastro antes da publicação**: a recompensa extra precisa estar provida antes de o desafio
  ir ao ar.
- **A curadoria do Mestre é condição, não formalidade**: desafio extra sem validação pedagógica
  vira publicidade dentro de uma trilha infantil, o que o projeto não admite.
- Recompensas seguem o cuidado de dignidade previsto para o catálogo.

> **A definir:** formato do **relatório de efetividade** entregue ao Apoiador — quais números,
> com que periodicidade e em que nível de agregação.

## 4. Impacto social

- **Case 01 — Comunidade Guerreira Zeferina**, Salvador (BA): primeiro piloto real, Ciclo 01
  de agosto a dezembro de 2026.
- **Acervo de 298 livros e 30 kits MDF** doados pelo Goethe-Institut, que viram trilhas
  abertas na plataforma — material que atende turmas inteiras sem custo para o aluno, com o
  livro da linha Alpha ficando com o jogador.
- **Oficinas do Robô Educa desde 2018**: centenas de crianças impactadas em comunidades de
  Salvador (BA).
- **Dados para a comunidade**: as Comunidades Virtuais devolvem ao território evidência para
  tomada de decisões.
- **Multiplicadores**: alunos formados viram instrutores de novos cursos em comunidades.

**[Proposta]** Definir **indicadores de impacto** desde o início (nº de alunos ativos,
retenção, trilhas concluídas, atividades realizadas, volume de dados de território, recursos
movimentados por comunidade). Além de guiar o projeto, são os números exigidos por editais e
grandes doadores.

## 5. Sustentabilidade (síntese)

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
