## Why

**PRD de origem:** PRD-07 — Economia de recursos e livro-razão. Primeira fatia dele e vigésima
sétima da esteira, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-07-47` e `RN-07-33` (ponto de apoio cadastrado pela gestão,
pertencente a uma comunidade), `RF-07-49` e `RN-07-34` (designação posterior do responsável pelo
acervo), `RF-07-01` e `RN-07-03` (tipo de recurso com unidade e valor de referência em moedas),
`RF-07-02` e `RN-07-04` (valor versionado por vigência, com duas casas decimais) e, do PRD-01,
`RF-01-71` (a aula declara em qual ponto de apoio acontece), `RF-01-16` (matriz de permissões),
`RF-01-03` (autoria, data e hora em toda escrita) e `RF-01-27` (erro em formato único). A
exigência da chave de aplicação (`RF-01-02`, `RN-01-32`) vale por herança do roteador e já tem
capacidade própria — esta change não a redeclara.

Esta é a fatia **sem dependência alguma**: todo o resto do PRD-07 pendura nas duas entidades que
ela cria. O saldo de recurso é por tipo **e ponto de apoio** (`RF-07-07`), e o aporte converte em
moedas **pela tabela vigente na data** (`RF-07-05`) — nenhum dos dois existe antes destas duas.

Ela também **fecha o PRD-01**. O `RF-01-71` é o único requisito dele que nunca entrou em change
alguma: a decisão de que a aula declara o ponto de apoio nasceu na abertura do PRD-07, quando a
entidade ainda não existia em lugar nenhum, e ficou explicitamente reservada para cá.

### O que foi decidido antes desta change

Três lacunas entre o requisito e o modelo de dados foram ao fundador e voltaram decididas, pelo
fluxo de sempre — documento-fonte, documento 09, PRD:

1. **O responsável pelo acervo é designado depois do cadastro**, por um Admin. O documento 05 §3
   exigia a pessoa designada, mas o `RF-07-47` pedia só nome e comunidade — e o ponto de apoio
   precisa poder nascer antes de se saber quem responde por ele. Nasce o `RF-07-49`.
2. **A designação recai sobre qualquer adulto cadastrado** — Admin, Mestre ou Apoiador —, nunca
   sobre Guerreiro(a) nem sobre responsável familiar. Nenhum documento declarava a restrição.
   Nasce a `RN-07-34`.
3. **O `ativo` do ponto de apoio nasce sem operação que o mude.** Quem desativa, e o que acontece
   com aula já agendada e com saldo ainda guardado ali, virou **pendência no documento 09** em
   vez de suposição no código.
4. **A aula e o ponto de apoio precisam ser da mesma comunidade**, e a divergência é recusada
   com **422**. Com o campo novo a aula ganha dois caminhos até a comunidade, e o invariante 4
   do documento 99 — que vincula o Guerreiro(a) à comunidade da aula em que se cadastra — ficaria
   ambíguo se os dois discordassem. É coerência derivada do modelo, não regra de produto nova:
   por isso fica registrada aqui e não vira linha em documento-fonte.

## What Changes

- Nasce o **ponto de apoio**: cadastro de **Admin**, com **nome** e **comunidade** obrigatórios,
  onde o recurso fica guardado e onde a aula acontece (`RF-07-47`, `RN-07-33`).
- O **responsável pelo acervo** é designado em operação própria de Admin, **depois** do cadastro,
  e pode ser trocado. A pessoa designada é **Admin, Mestre ou Apoiador**; Guerreiro(a) e
  responsável familiar são recusados (`RF-07-49`, `RN-07-34`).
- **BREAKING** — a **aula passa a declarar o ponto de apoio em que acontece**, obrigatório. Toda
  aula agendada de agora em diante exige o campo, e agendar sem ele é recusado com **422**
  (`RF-01-71`). O ponto de apoio declarado SHALL pertencer à **mesma comunidade** da aula.
- Nasce o **catálogo de tipos de recurso**, cadastrado por Admin, com **nome**, **natureza**
  (consumível, durável, serviço ou financeiro) e **unidade** (`RF-07-01`).
- Nasce o **valor de referência em moedas**, **versionado por vigência**: mudar o valor de um
  tipo **abre uma vigência nova** e NUNCA reescreve a anterior, de modo que o passado continue
  legível pela tabela que valia na época (`RF-07-02`, `RN-07-03`).
- A moeda é guardada com **duas casas decimais exatas**, sem ponto flutuante (`RN-07-04`).
- Rotas: `POST /pontos-de-apoio`, `PUT /pontos-de-apoio/{id}/responsavel` e
  `POST /tipos-de-recurso` — todas de Admin, todas sob chave de aplicação (PRD-07 §9).

### Fora do escopo

Nada de **movimento** entra nesta fatia: ela é cadastro. Não há lançamento, não há saldo, não há
moeda mudando de mãos. O recorte:

| Fica para                                | Porque                                                             |
| ---------------------------------------- | ------------------------------------------------------------------ |
| `Lancamento` e `SaldoDeRecurso`          | é a fatia seguinte; o saldo é derivado e pede o livro-razão inteiro |
| `RF-07-04` a `RF-07-06`, `RF-07-29`/`30` | aporte e homologação, na fatia do aporte                            |
| `RF-07-08` e `RF-07-09`                  | reserva e baixa da aula, depois que houver saldo para reservar      |
| `RF-07-10`                               | Poder Sustentador, que soma moedas aportadas                        |
| `RF-07-11` e `RF-07-48`                  | o responsável do **exemplar** tombado, na fatia do patrimônio       |
| `RF-07-42` a `RF-07-44`                  | preço de referência em **pontos extras**, com o catálogo avulso     |
| desativação de ponto de apoio            | pendência aberta no documento 09; o `ativo` existe sem operação     |

**`RF-07-03` é atendido só em parte, e de propósito.** Ele pede que o Admin cadastre tipo novo
**no ato do registro de um aporte, sem interromper o fluxo** — e não há aporte nesta fatia. O que
entra aqui é a condição do "sem interromper": o cadastro de tipo é operação **avulsa e barata**,
que não depende de nenhum outro fluxo. A composição com o registro do aporte entra na fatia do
aporte, e o requisito só se fecha lá.

**Nenhuma rota de leitura entra.** O PRD-07 §9 declara `POST /pontos-de-apoio` e
`POST /tipos-de-recurso`, e mais nenhuma sobre estas duas entidades. Listar pontos de apoio e
tipos é necessidade das telas de gestão, e a rota nasce no PRD que as declarar — artefato do
OpenSpec não inventa rota que o PRD não pediu.

## Capabilities

### New Capabilities

- `ponto-de-apoio`: o espaço físico cadastrado pela gestão, pertencente a uma comunidade, onde o
  recurso fica guardado e a aula acontece, com o responsável pelo acervo designado depois do
  cadastro.
- `catalogo-de-tipos-de-recurso`: o vocabulário do que a plataforma consome e recebe — nome,
  natureza e unidade — com o valor de referência em moedas versionado por vigência.

### Modified Capabilities

- `aula-e-presenca`: a aula passa a declarar, **obrigatoriamente**, o **ponto de apoio** em que
  acontece, e o ponto declarado precisa ser da mesma comunidade da aula. É o campo que ligará a
  reserva ao saldo certo quando o livro-razão chegar (`RF-01-71`).

## Impact

- `backend/src/nucleo/pontos_de_apoio/`: pasta nova — `modelo.py`, `regra.py` e `rotas.py` do
  ponto de apoio e da designação do responsável.
- `backend/src/nucleo/recursos/`: pasta nova — `modelo.py`, `regra.py` e `rotas.py` do tipo de
  recurso e do valor de referência versionado.
- `backend/src/nucleo/aulas/modelo.py` e `regra.py`: o campo `ponto_de_apoio_id`, obrigatório, e
  a conferência de que ele pertence à comunidade da aula.
- `backend/src/nucleo/principal.py`: registro dos dois roteadores novos.
- `backend/alembic/versions/`: migration com as três tabelas novas e o campo em `aula`.
- `backend/tests/`: cadastro por Admin e recusa a Mestre; ponto de apoio sem nome e sem
  comunidade; designação de Admin, Mestre e Apoiador; recusa de Guerreiro(a) e de responsável;
  troca do responsável; aula sem ponto de apoio recusada; aula com ponto de apoio de outra
  comunidade recusada; tipo sem unidade recusado; vigência nova que não reescreve a anterior;
  valor com mais de duas casas recusado; escrita sem chave recusada com 401.
