## Why

**PRD de origem:** PRD-07 — Economia de recursos e livro-razão. Quarta fatia dele e trigésima
da esteira, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-07-18` (o que falta de recurso para as aulas já agendadas),
`RF-07-27` (a falta é publicada como necessidade na vitrine, na área do Apoiador e na área dos
Mestres), `RF-07-28` (Mestre ou Admin assume o aporte por absorção a partir da necessidade),
`RF-07-31` (a necessidade admite cobertura parcial e só sai da lista quando o saldo fecha) e
`RN-07-23` (cada provedor recebe as moedas do que aportou). Do PRD-03, servido por esta fatia,
`RF-03-47`. `RF-01-02`, `RF-01-03` e `RF-01-16` valem por herança do roteador e já têm
capacidade própria — esta change não os redeclara.

A fatia 3 fez a aula nascer **pendente de lastro** quando falta recurso, e fez o aporte que
fecha a diferença confirmá-la sozinho. Faltou o meio do caminho: hoje a falta existe no banco e
**não tem por onde ser vista**. Sem ela publicada, o invariante 9 tranca a aula sem oferecer
saída — o oposto do que o documento 04 §1 chama de "falta de lastro vira pedido, não recusa
silenciosa".

### O que foi decidido antes desta change

Quatro lacunas foram ao fundador e voltaram decididas, pelo fluxo de sempre — documento-fonte,
documento 09, PRD:

1. **Há uma necessidade por aula e tipo de recurso**, nunca somada por ponto de apoio: quem
   aporta escolhe qual aula destrava. Disputando o mesmo saldo, a aula de **horário inicial
   mais próximo** conta primeiro o que falta, na mesma ordem em que a confirmação da `RN-07-37`
   já atende. O `RF-07-18` falava em "as aulas" e o `RF-07-31` em "ela", uma a uma.
2. **A necessidade publicada mostra** tipo de recurso, quantidade, valor em moedas, comunidade,
   **ponto de apoio, data e horário** da aula — também na rota pública. Nenhum documento dizia
   o que a lista expõe. Não contraria invariante do documento 99 §6.
3. **A lista do Mestre filtra pela comunidade da aula**, não pelas trilhas de que ele é autor:
   a aula não guarda trilha no núcleo. Repete o precedente que o cancelamento abriu na fatia 3.
4. **A rota pública é `GET /vitrine/necessidades`**, do PRD-03 §10 e do PRD-14 §10, pelo
   prefixo que o núcleo já usa em toda leitura pública; o `GET /necessidades` do PRD-07 §9 sai,
   e a rota do Mestre acompanha a convenção.

Três lacunas do plano de execução também foram ao fundador, e ficam registradas aqui porque são
coerência derivada do modelo, não regra de produto nova — o mesmo tratamento que a fatia 3 deu
ao tudo-ou-nada da reserva:

1. **A necessidade é cálculo, não cadastro.** É derivada das aulas em pendente de lastro e do
   saldo, e identificada pelo par **aula + tipo de recurso**. O PRD-07 §8 não a lista entre as
   entidades, e o saldo — que ela lê — já é derivado e recontável (`RF-07-07`). A chave natural
   é o que dá à `MissaoDoApoiador` do PRD-14 (`RN-14-31`) para onde apontar, sem cadastro
   paralelo que possa divergir do saldo.
2. **O valor em moedas da necessidade é o da vigência da data da leitura.** O aporte é valorado
   pela vigência da **data dele** (`RF-07-05`), que ainda não existe quando a falta é publicada;
   a necessidade é painel vivo, e mostra a melhor estimativa corrente. Tipo sem vigência válida
   hoje sai sem valor em moedas, nunca com valor arbitrado.
3. **Toda aula em pendente de lastro é publicada, sem filtro de data.** A fatia 3 confirma a
   aula pendente por aporte sem olhar se a data passou, e o documento 09 já decidiu que a aula
   que passa sem desfecho espera ato de Admin. Filtrar por data aqui esconderia falta que o
   núcleo ainda considera aberta.

### O recorte

**A fatia entrega leitura, e só.** Nenhuma escrita nasce aqui: o `RF-07-28` está servido pelo
`POST /aportes/absorcao` que a fatia 2 entregou — ele já credita no ato e já dispara a
confirmação automática da aula. O que a necessidade acrescenta é chegar à tela com tipo,
quantidade e ponto de apoio prontos, trabalho da App 08 e da App 09. O PRD-07 §9 não declara
rota para o ato, o que confirma a leitura.

**O `RF-07-31` também não pede mecanismo.** Como o saldo é derivado e a reserva é tudo-ou-nada,
o aporte parcial já credita, já abate a falta e já não confirma. A cobertura parcial é o que a
derivação **mostra**, não um caminho novo de escrita. O mesmo vale para o `RN-07-23`: cada
aporte já credita o seu próprio provedor desde a fatia 2.

## What Changes

- Nasce a **necessidade de recurso**: a falta de uma aula em pendente de lastro, derivada do
  que ela declarou consumir menos o disponível no ponto de apoio dela, identificada pelo par
  **aula + tipo de recurso** (`RF-07-18`, `RF-07-27`).
- A falta é contada **na ordem do horário inicial da aula**, da mais próxima para a mais
  distante: a aula mais próxima consome primeiro o disponível, e a seguinte enxerga só o que
  sobrou. É a mesma ordem com que a `RN-07-37` confirma.
- A necessidade carrega **tipo de recurso, quantidade que falta, valor em moedas, comunidade,
  ponto de apoio, data e horário da aula** — a mesma saída na rota pública e na do Mestre.
- O **valor em moedas** sai pela vigência da data da leitura; tipo sem vigência válida hoje sai
  sem valor, nunca com valor arbitrado (`RN-07-04`, `RN-07-05`).
- A necessidade **encolhe a cada aporte homologado** e some quando o saldo fecha — junto com a
  confirmação da aula, que a fatia 3 já faz no mesmo ato (`RF-07-31`).
- Rotas: **`GET /vitrine/necessidades`** (pública, sem credencial de persona) e
  **`GET /necessidades/minhas`** (Mestre, filtrada pelas comunidades a que ele está vinculado)
  — ambas sob chave de aplicação, ambas somente leitura. A do Mestre fica **fora** do prefixo
  `/vitrine`, que o núcleo reserva à leitura sem persona, e segue a convenção das rotas
  logadas, como `/series-de-coleta/minhas`.
- **Nenhuma escrita nasce nesta fatia.** O `RF-07-28` é atendido pela absorção que já existe.
- Correção de rastreabilidade: o requisito do `aporte` que já implementa o `RF-07-29` — aporte
  declarado no pré-cadastro entra pendente, sem creditar — passa a citá-lo. **Comportamento não
  muda.**

### Fora do escopo

O PRD-07 §3.2 já exclui empréstimo de bancada, reposição solidária, entrega de dados a
pesquisadores, o painel de efetividade do Apoiador, a interface de gestão e a contabilidade
fiscal. Nada disso volta aqui.

O que é **adiado por recorte**, não excluído:

| Fica para                             | Porque                                                     |
| ------------------------------------- | ---------------------------------------------------------- |
| `RF-07-10`, `RF-07-16`, `RF-07-17`    | Poder Sustentador e prestação de contas, na fatia seguinte |
| `RF-07-26`, `RN-07-19`                | o selo público de quem absorveu, com a mesma fatia         |
| `RF-07-22` a `RF-07-25`               | o ressarcimento                                            |
| `RF-07-11`, `RF-07-13`, `RF-07-48`    | patrimônio, ficha de vida e baixa definitiva               |
| `RF-07-33` a `RF-07-38`, `RF-07-42` a `RF-07-46` | o catálogo avulso e a troca                     |
| `RF-07-15`, `RF-07-39` a `RF-07-41`   | a reserva do desafio extra, que depende do PRD-14          |
| `MissaoDoApoiador` e níveis de necessidade | entidade do PRD-14, que ainda não entrou na esteira   |
| desativação de ponto de apoio         | pendência aberta no documento 09                           |

A necessidade nasce só do braço da **aula**. O desafio extra, que a `Reserva` do PRD-07 §8
também prevê, é entidade do PRD-14 e não existe no núcleo — e o `RF-07-39` recusa a publicação
sem lastro em vez de deixá-lo pendente, de modo que ele nunca gera necessidade.

## Capabilities

### New Capabilities

- `necessidade-de-recurso`: a falta da aula pendente de lastro como derivação — a chave aula +
  tipo, a contagem na ordem do horário, os campos publicados, o valor em moedas pela vigência
  corrente, a cobertura parcial que encolhe a linha, e as duas rotas de leitura.

### Modified Capabilities

- `aporte`: correção de rastreabilidade — o requisito que já implementa o `RF-07-29` passa a
  citá-lo. Nenhum comportamento muda.

## Impact

- `backend/src/nucleo/necessidades/`: pasta nova — `regra.py` da derivação e da contagem na
  ordem do horário, `rotas.py` com as duas leituras.
- `backend/src/nucleo/principal.py`: registro do roteador de necessidades.
- `backend/src/nucleo/recursos/regra.py`: leitura do valor de referência vigente na data
  corrente, reusada pela derivação.
- Sem migration: nada de novo é gravado — a necessidade é derivada de `aula`,
  `recurso_declarado_da_aula`, `reserva` e `lancamento`, que já existem.
- `backend/tests/`: falta derivada de uma aula, ordem do horário entre aulas que disputam o
  mesmo saldo, encolhimento por aporte parcial, some quando o saldo fecha, aula confirmada fora
  da lista, filtro por comunidade na rota do Mestre, ausência de valor em moedas sem vigência,
  e a rota pública dispensando credencial de persona mas nunca a chave.
- `docs/04-modelo-economico-e-sustentabilidade.md` e
  `docs/09-topicos-em-aberto-e-sugestoes.md`: já gravados antes desta change.
- `docs/prds/prd-07-economia-e-ledger.md`: §9 com os dois endereços corrigidos.
- `docs/prds/prd-03-vitrine-publica.md`: `RF-03-47`, com os campos que a vitrine publica.
- `docs/prds/index.md`: a narrativa da fatia entregue, na entrega.
