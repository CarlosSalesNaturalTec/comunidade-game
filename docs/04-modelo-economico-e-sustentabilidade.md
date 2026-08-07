# 04 — Modelo Econômico e Sustentabilidade

## 1. A economia de recursos da plataforma

Princípio central — a "moeda" do Comunidade Game:

> **Todas as ações ocorridas na plataforma — aulas, lanches, hospedagem de servidores,
> prestadores de serviço — têm seus custos computados e atribuídos a um personagem
> (Guerreiro(a), Mestre ou Apoiador).** Assim se registra a riqueza movimentada, trazendo
> transparência sobre os recursos.

Regras derivadas:

- Os recursos das atividades — **hora-aula do mentor, lanche, recompensas, insumos** — são
  fornecidos por Mestres ou Apoiadores.
- Cada recurso alocado é **computado para o respectivo provedor** e acumulado no seu
  histórico.
- **Cada atividade só acontece se tiver os recursos providos** — não há atividade sem lastro.
  O livro-razão mantém **saldo por tipo de recurso**; agendar uma atividade **reserva** o que
  ela consome, e a realização converte a reserva em baixa.
- **Falta de lastro vira pedido, não recusa silenciosa.** Cadastrada a atividade sem saldo
  para o que ela consome, a diferença é publicada como **necessidade de recurso** em três
  lugares: na vitrine pública, na área do Apoiador e na área dos Mestres da trilha. A
  atividade fica **pendente de lastro** e só é confirmada quando a necessidade é suprida.
- **Aporte por absorção.** Faltando saldo, um Mestre ou Admin pode **prover ele mesmo** o
  recurso — dar a aula sem receber, comprar o lanche, ceder o insumo —, e faz isso **a partir
  da própria necessidade publicada**, com um ato de confirmação. A plataforma registra como
  **aporte dele**, valorado pela tabela de referência, e o crédito entra no seu Poder
  Econômico. O aporte nasce marcado como **ressarcível**, e quem absorveu ganha **destaque
  público** pelo ato.
- **Ressarcimento não é direito nem promessa.** Não há fila permanente nem expectativa de
  devolução: o ressarcimento só existe quando entra receita destinada a ele. Havendo essa
  receita, os aportes ressarcíveis são pagos **por antiguidade**, por decisão de um Admin.
  Ressarcido o aporte, as moedas **revertem** — quem recebeu de volta adiantou recurso, não
  doou —, mas o registro do ato e o destaque público **permanecem**.
- **A plataforma não guarda dado bancário.** Todo o trâmite corre na plataforma; na última
  etapa a pessoa envia a chave PIX **por e-mail ao Admin**, que faz a transferência e anexa
  o **comprovante** ao registro. Nem chave, nem banco, nem conta ficam armazenados.
- O acumulado forma o **"Poder Econômico"** do provedor, visível na plataforma: o
  reconhecimento público de quem sustenta o projeto.

### A moeda da plataforma

**Definição vigente.** A unidade de conta do livro-razão é a **moeda da plataforma**: todo
aporte — em dinheiro, material ou serviço — é convertido em moedas, e **1 moeda equivale a
R$ 10,00**.

- Nas **vitrines públicas** exibe-se a **quantidade de moedas** aportada, **nunca o valor em
  reais**.
- A moeda mede **aporte de recurso** e compõe o Poder Econômico. Não se confunde com os
  **pontos**, que são do Guerreiro(a) e vêm de realização.
- A moeda admite **fração, com duas casas** — R$ 5,00 são 0,50 moeda —, para que nenhum
  aporte pequeno se perca no arredondamento.
- **A escala é fixa.** Alterá-la depois que o livro-razão tiver histórico obriga a reconverter
  todos os aportes já registrados, sob pena de o Poder Econômico comparar réguas diferentes.
  Mudança de escala é decisão declarada, com reconversão, nunca ajuste silencioso.
- **Reais aparecem só onde se paga.** A tela de aporte mostra o valor em reais, porque é o que
  se transfere, sempre **ao lado do equivalente em moedas**. Em toda exibição de aporte
  **de alguém** — card, página, ranking — o que sai é a quantidade de moedas.

Por que assim: a plataforma é educativa e seu público inclui crianças e terceiros sem
familiaridade com custos de operação, custeio e despesas. A moeda dá a **noção visual do
montante** investido por cada apoiador em relação aos seus pares, sem expor valores
monetários isolados.

Por que **R$ 10,00** e não uma escala maior: assim o **lanche de um encontro vale cerca de 1
moeda** — âncora que uma criança entende — e a menor doação da escada de sugestão vale **5
moedas**, número inteiro e digno. Dez vezes maior, quem doa o que pode receberia meia moeda, o
contrário de reconhecer quem sustenta o projeto.

Aportes em material e serviço são convertidos em moedas por uma **tabela de referência**
mantida pela gestão: cada tipo de aporte — hora-aula, kit, livro, camisa, lanche, insumo —
tem um valor padrão, e todo aporte do mesmo tipo vale o mesmo, o que torna comparável o
Poder Econômico entre apoiadores. **Tipo novo é cadastrado na hora por um Admin**, com o seu
valor de referência, para que nenhum aporte fique represado.

### Produção executiva

**Definição vigente.** O **tempo de trabalho do fundador e dos Admins** na plataforma é
**despesa do projeto** e entra no livro-razão como qualquer outro recurso, na forma de **aporte
por absorção**. Hoje ninguém o recebe, e é por isso que precisa aparecer: sem ele, o custo real
do projeto fica subdeclarado diante de edital, doador e da própria comunidade.

| Frente                       | O que cobre                                                                                                          | Lastro do registro                                      |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| **Construção da plataforma** | Idealização, documentação e desenvolvimento do Backend API e das aplicações                                          | **Histórico de commits deste repositório**, por período |
| **Operação da plataforma**   | Manutenção em funcionamento, gestão dos recursos de _cloud_ e contatos com apoiadores, pesquisadores e poder público | Registro do próprio Admin, por período                  |

Vale para a produção executiva o que já vale para todo aporte por absorção: valoração pela
tabela de referência, marcação como **ressarcível**, destaque público pelo ato e ressarcimento
apenas quando houver receita destinada a ele.

> **A definir:** o valor-hora de referência da produção executiva e o critério que converte o
> histórico de commits e o registro do Admin em horas aportadas.

**[Proposta]** Modelar tecnicamente como um **livro-razão (ledger) de dupla entrada**: cada
atividade consome recursos (débito) aportados por provedores (crédito). Viabiliza relatórios
públicos de prestação de contas por atividade, por comunidade e por provedor — transparência
auditável, essencial para captar doações e editais.

### Pessoa jurídica vinculada ao projeto

**Definição vigente.** A pessoa jurídica que representa o projeto perante terceiros:

|                         |                                                            |
| ----------------------- | ---------------------------------------------------------- |
| **Razão social / nome** | Robô Educa — Kits Robóticos Educacionais                   |
| **CNPJ**                | 51.730.395/0001-19                                         |
| **Responsável legal**   | Carlos Antonio Sales — o mesmo fundador e autor do projeto |

É ela que **recebe doações, assina termos e responde formalmente** pelos aportes registrados
no livro-razão.

> **Nota de governança:** o CNPJ resolve o problema imediato — receber doação e assinar termo
> hoje —, mas **não encerra** a discussão da forma jurídica adequada para editais e recursos
> públicos, que normalmente exigem entidade sem fins lucrativos (associação, OSCIP ou _fiscal
> sponsor_). Os dois assuntos coexistem (documento 09).

### Primeiro aporte registrado — acervo, kits e camisas do Goethe-Institut

O **Goethe-Institut (Salvador)** doou **298 livros** do projeto **Include**, da **Campus
Party**, **30 kits em MDF** para as trilhas do Robô Educa e **50 camisas** — tornando-se um
dos **primeiros Apoiadores** da plataforma. A doação dos livros foi formalizada por **Termo
de Doação assinado** com a Robô Educa — Kits Robóticos Educacionais: o **documento
comprobatório do aporte**, exatamente o tipo de artefato que a plataforma exige de todo
Apoiador, e que fica anexado ao cadastro do Apoiador na App 03.

É o **primeiro caso concreto** da economia descrita acima: entra no histórico do provedor,
compõe o **Poder Econômico** do Goethe-Institut e dá **lastro material** às duas trilhas
existentes, sem custo adicional para o primeiro ciclo.

**Tratamento no livro-razão — regime misto (definição vigente):**

| Item                               | Destino                                                                        | Como entra no ledger                                                      |
| ---------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| **Livros da linha Alpha** (252)    | Doados ao Guerreiro(a) quando ele começa a trilha                              | **Recompensa entregue** — baixa definitiva do acervo                      |
| **Livros da linha Include I** (46) | Acervo permanente do ponto de apoio                                            | **Patrimônio permanente** — sem baixa por consumo, com controle de guarda |
| **Kits MDF** (30)                  | Insumo das oficinas do Robô Educa                                              | **Consumível de atividade** — baixa a cada montagem                       |
| **Camisas** (50)                   | Conquistadas no marco de missão que o Mestre declarar, até o limite disponível | **Recompensa entregue** — baixa definitiva na entrega                     |

Inventário completo, regime de posse e estratégia de conservação: documento 05.

Acervo, kits e camisas são valorados pela tabela de referência, como qualquer outro aporte.

## 2. Fontes de receita

- **Doações** de pessoas físicas e jurídicas.
- **Editais.**
- **Campanhas de crowdfunding** para financiar aulas, kits e equipamentos (celulares,
  notebooks, tablets).
- **Ressarcimento de recursos absorvidos** — doação destinada especificamente a devolver o
  que Mestres e Admins bancaram do próprio bolso para que a atividade acontecesse.

Os dados produzidos pela plataforma **não entram nesta lista**: sua disponibilização é
gratuita, na vitrine e sob solicitação aprovada (documento 03).

### Publicidade e patrocínio — fora do Ciclo 01

**Definição vigente.** A plataforma **não veicula publicidade nem patrocínio**. O tema fica
como **estudo para ciclo futuro**, e o que se decidir ali precisará responder antes ao que
publicidade significa em plataforma usada por criança (documento 09).

### Doações em espécie — canal oficial

**Definição vigente.** As doações em dinheiro são feitas por **PIX**, em nome da pessoa
jurídica vinculada:

|               |                                          |
| ------------- | ---------------------------------------- |
| **Chave PIX** | `51.730.395/0001-19` (CNPJ)              |
| **Titular**   | Robô Educa — Kits Robóticos Educacionais |

- Toda doação recebida é **registrada no livro-razão** e compõe o **Poder Econômico** do
  doador — dinheiro não é exceção à regra de transparência, é o caso em que ela mais importa.
- O doador é cadastrado como Apoiador por um Admin, com o comprovante anexado.
- A chave é publicada na vitrine pública, na seção "Como apoiar".

**Como o aporte entra, no Ciclo 01.** Quem chega pela vitrine faz o **pré-cadastro na Área do
Apoiador** e escolhe uma de três formas:

| Forma                     | O que é                                                                      |
| ------------------------- | ---------------------------------------------------------------------------- |
| **Necessidade publicada** | Assume uma das necessidades de recurso em aberto, pelo valor que ela declara |
| **Valor sugerido**        | Escolhe um degrau da escada abaixo                                           |
| **Valor livre**           | Informa o valor que transferiu                                               |

- **Comprovante obrigatório** — PDF, JPG ou PNG. A plataforma **não confirma PIX
  automaticamente**: quem confere é um Admin, na App 03.
- **Sem documento fiscal**: a plataforma não coleta CPF, CNPJ nem documento de identidade de
  quem aporta.
- **Homologado o aporte**, o valor é convertido em **moedas**, credita o Poder Econômico e o
  card do Apoiador passa a exibir o total na vitrine. Antes disso não há crédito nem card.

**Escada de valores sugeridos (definição vigente):**

| Valor       | Equivalente |
| ----------- | ----------- |
| R$ 50,00    | 5 moedas    |
| R$ 100,00   | 10 moedas   |
| R$ 250,00   | 25 moedas   |
| R$ 500,00   | 50 moedas   |
| R$ 1.000,00 | 100 moedas  |

A tela mostra sempre os dois lados, e o **valor livre** exibe o equivalente em moedas antes do
envio.

## 3. Interação Apoiadores × Guerreiros e Guerreiras: desafios extras

Aportar recurso é o começo da relação do Apoiador com a plataforma, não o fim. A interação
Apoiador–Guerreiro(a) acontece por **desafios extras**: durante um ciclo em andamento, o
Apoiador propõe um desafio ligado a uma trilha em curso e oferece uma **recompensa extra** a
quem o concluir.

**Como funciona no ciclo:**

1. O Apoiador propõe o desafio, vinculado a uma **trilha em andamento**, e indica a recompensa
   que vai custear e **em que quantidade**.
2. O **Mestre da trilha valida** — o desafio precisa fazer sentido pedagógico na missão em que
   os Guerreiros e Guerreiras estão.
3. Um **Admin aprova** (ou não) a publicação.
4. O desafio é publicado para todos os Guerreiros e Guerreiras daquela trilha — ou, no caso do
   direcionado, entregue ao destinatário — com recompensa, quantidade disponível e critério de
   atribuição visíveis desde o início.
5. Quem conclui recebe **pontos extras** e, até esgotar a quantidade ofertada, a recompensa.

### Definições vigentes

| Questão                          | Definição                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pontos**                       | O desafio extra vale **pontos além da recompensa**, computados **isoladamente como pontos extras** — não se misturam à pontuação regular da trilha                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Teto de desafios simultâneos** | **Não há teto por trilha.** O controle é qualitativo: cada desafio é aprovado ou não por um Admin, caso a caso, após a validação do Mestre                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Exclusividade**                | **Proibida nos desafios abertos**: ninguém é barrado de disputar. O que é limitado é a **quantidade** de recompensas, declarada de antemão                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Desafio direcionado**          | O Apoiador pode **direcionar um desafio a um Guerreiro(a) específico**, identificado **pelo nick** que a família lhe cedeu — só ele recebe a recompensa se atingir os requisitos. Exige **justificativa registrada** do vínculo (ex.: parente próximo — tio(a), padrinho, madrinha) e aprovação de Admin, além da validação do Mestre. A plataforma **não confirma ao proponente se o nick existe** nem exibe dado algum do destinatário: quem confere o vínculo são o Mestre e o Admin. Por isso o direcionado **alcança também quem não tem divulgação autorizada** |
| **Quantidade de recompensas**    | **Uma única** (para quem concluir primeiro) **ou várias** — todos que concluírem recebem, até o limite disponibilizado                                                                                                                                                                                                                                                                                                                                                                                                                                                |

Por que o teto foi substituído por aprovação: um número fixo protegeria a trilha do excesso,
mas barraria um bom desafio pela razão errada — a ordem de chegada. A aprovação caso a caso
protege a trilha pelo motivo certo: **o mérito pedagógico da proposta**.

O desafio direcionado é o caminho para o apoio de interesse direto e legítimo — por exemplo, um
parente próximo que propõe um desafio para um Guerreiro(a) da sua parentela — sem abrir exceção
nas salvaguardas. É também o caminho de quem ficou de fora dos **três responsáveis** da criança:
avós, tios, padrinhos e amigos da família participam **como Apoiadores**, acompanhando pelo nick
e propondo desafios, sem acesso à área da família.

### Rastreio de efetividade

**O que fica registrado no histórico do Apoiador:**

| Registro                                                                        | Para que serve                                               |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **Recompensas creditadas** — o que ele custeou e entregou                       | Compõe o **Poder Econômico**, como qualquer outro aporte     |
| **Realizações dos Guerreiros e Guerreiras** nos desafios que ele propôs         | Mostra **o que aconteceu** por causa daquele apoio           |
| **Etiquetas ODS** herdadas da missão, ou da trilha, a que o desafio se vinculou | Mostra **a que objetivos da Agenda 2030** o apoio contribuiu |

É a segunda linha que muda o jogo: o histórico deixa de responder apenas _"quanto foi
aportado"_ e passa a responder _"o que esse apoio produziu"_ — quais desafios engajaram,
quantos Guerreiros e Guerreiras concluíram, em que trilhas o apoio rendeu mais. Para o projeto,
é o argumento de captação mais forte que existe; para o Guerreiro(a), é a prova de que há gente
de fora torcendo pelo que ele está construindo.

### Salvaguardas obrigatórias

- **Sem contato direto** entre Apoiador e criança. Proposta, entrega e reconhecimento são
  sempre **mediados pela plataforma**. O canal da família é exclusivo da App 07 e não é
  compartilhado com Apoiadores.
- **Lastro antes da publicação**: a recompensa extra precisa estar provida antes de o desafio
  ir ao ar.
- **A curadoria do Mestre é condição, não formalidade**: desafio extra sem validação pedagógica
  vira publicidade dentro de uma trilha infantil, o que o projeto não admite.
- Recompensas seguem o cuidado de dignidade previsto para o catálogo.

**Painel vivo, não relatório fechado.** O retorno ao Apoiador é uma tela da App 08 atualizada
a cada conclusão: desafios propostos, publicados e concluídos, quantos Guerreiros e Guerreiras
concluíram cada um, em que trilhas, moedas aportadas e cobertura de ODS. Sai **agregado e por
avatar**, por desafio e por trilha. **No Ciclo 01 não há relatório fechado nem periodicidade** —
o uso do painel é o que vai dizer qual peça de prestação de contas vale construir depois.

## 4. Impacto social

- **Case 01 — Comunidade Guerreira Zeferina**, Salvador (BA): primeiro piloto real, Ciclo 01
  de agosto a dezembro de 2026.
- **Acervo de 298 livros, 30 kits MDF e 50 camisas** doados pelo Goethe-Institut, que viram
  trilhas abertas na plataforma — material que atende turmas inteiras sem custo para o aluno,
  com o livro da linha Alpha ficando com o Guerreiro(a).
- **Oficinas do Robô Educa desde 2018**: centenas de crianças impactadas em comunidades de
  Salvador (BA).
- **Dados para a comunidade**: as Comunidades Virtuais devolvem ao território evidência para
  tomada de decisões.
- **Multiplicadores**: alunos formados viram instrutores de novos cursos em comunidades.

### Aderência à Agenda 2030

O projeto declara aderência aos **Objetivos de Desenvolvimento Sustentável (ODS)** porque é a
linguagem de editais, poder público e grandes doadores. A adesão é **descritiva**: etiqueta o
que já existe, sem criar conteúdo, poder ou pontuação.

| ODS                                       | O que na plataforma corresponde                                                                                                                            |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **4** Educação de qualidade               | O projeto inteiro; meta 4.4 (habilidades técnicas) e **4.7** (cidadania, sustentabilidade e diversidade cultural), que é o objetivo dos temas transversais |
| **5** Igualdade de gênero                 | Combate ao feminicídio e à violência contra a mulher; espaço seguro para meninas; mestras como referência                                                  |
| **10** Redução das desigualdades          | Público periférico de 6 a 16 anos e primeiro contato com tecnologia sem exigir computador                                                                  |
| **11** Cidades e comunidades sustentáveis | Coletas de resíduos, iluminação, buracos na via e trânsito (metas 11.3, 11.6 e 11.7); registro de espaços e memórias do bairro (11.4)                      |
| **13** Ação climática                     | Letramento sobre a crise ambiental e as séries de temperatura e chuva — meta **13.3**, medida no lugar onde o Guerreiro(a) vive                            |
| **16** Paz, justiça e instituições        | Código de Conduta co-criado (16.7) e transparência radical do livro-razão (16.10)                                                                          |
| **17** Parcerias e meios de implementação | Apoiadores, doações registradas, código aberto e — sobretudo — a **meta 17.18**                                                                            |
| **18** Igualdade étnico-racial            | Causa antirracista, reconhecimento dos povos originários e o lema com personalidades negras e indígenas                                                    |
| **8** e **9** _(parciais)_                | Empreendedorismo e economia criativa (8.6) e acesso a TIC (9.c). Parciais porque o projeto **não se propõe a encaminhar profissionalmente**                |

O **ODS 18 — Igualdade Étnico-Racial** é **adoção voluntária do Brasil**, coordenada pelo
Ministério da Igualdade Racial com metas e indicadores aprovados pela Comissão Nacional dos
ODS. Não integra o quadro oficial de 17 objetivos da ONU, e citá-lo sem essa ressalva é erro
que custa credibilidade justamente diante de quem conhece a agenda.

#### A contribuição própria — meta 17.18

Um ciclo com uma turma não move indicador nacional, e prometer isso queima o projeto com quem
financia. O que a plataforma entrega de fato é o insumo da **meta 17.18**: dado local,
desagregado, datado e de guarda permanente sobre um território periférico — exatamente o que
falta para acompanhar qualquer ODS na escala em que as pessoas vivem. É a única afirmação de
contribuição que o projeto faz sem exagero, e a mais forte que tem.

#### Indicadores de cobertura

Medem **alcance declarado**, não impacto — e saem prontos das etiquetas ODS das trilhas, sem
lançamento manual:

- ODS distintos cobertos no ciclo e por comunidade.
- Trilhas publicadas por ODS, e proporção das que declararam etiqueta — indicador de
  transição, que o Ciclo 02 leva a 100% ao exigir a etiqueta da trilha.
- Séries de coleta ativas por ODS, com o tempo em que se mantiveram.
- Desafios extras de Apoiadores por ODS.

Publicados **agregados por comunidade e por ciclo, nunca por Guerreiro(a)**.

**[Proposta]** Definir os demais **indicadores de impacto** desde o início (nº de alunos
ativos, retenção, trilhas concluídas, atividades realizadas, volume de dados de território,
recursos movimentados por comunidade). Além de guiar o projeto, são os números exigidos por
editais e grandes doadores.

## 5. Sustentabilidade (síntese)

O projeto é sustentável quando o ciclo se fecha:

```text
Apoiadores/Parceiros aportam recursos ──► Atividades acontecem (com lastro)
        ▲                                          │
        │                                          ▼
Transparência + vídeos + Poder Econômico ◄── Guerreiros e Guerreiras aprendem, pontuam e realizam
        ▲                                          │
        └────────── novos multiplicadores ◄────────┘
```

A transparência do livro-razão e a visibilidade pública das realizações são o que renova a
confiança dos apoiadores e atrai novos recursos.
