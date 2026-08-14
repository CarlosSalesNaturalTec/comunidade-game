## Context

Ver `proposal.md` — Why. O que restringe o desenho é o que já está de pé:

- `backend/src/nucleo/coletas/` tem `TipoDeColeta` e `DesafioDeColeta`, com a **forma de
  registro**, a **faixa esperada**, a **cadência**, a **vigência**, a **granularidade exigida** e
  **quantos registros do período pontuam**. Nada disso se redefine aqui.
- `comunidades/` guarda a `granularidade_maxima` da comunidade e o `VinculoJogador` com
  histórico; `locais/` guarda a hierarquia de seis níveis, com `ORDEM_DOS_NIVEIS` já declarada.
- `tempo.py` tem o mixin **`ComMomentoDoFato`**, escrito para o fato que chega depois de
  acontecer — `momento_do_fato` informado por quem registra, `momento_do_registro` marcado pelo
  núcleo. É exatamente o par que `RF-08-15` exige, e não se escreve outro.
- `armazenamento/` expõe a `PortaDeArmazenamento` com `gravar`, `ler` e `remover`, com disco no
  ambiente local e Cloud Storage em produção. `fila/regra.py` é o precedente de uso, no
  comprovante de aporte.
- `pontuacao/regra.py` reúne as funções de crédito por fonte — resultado, quiz, criação
  original. A coleta entra como mais uma.
- Os testes rodam contra **PostgreSQL de verdade** (`conftest.py`), de modo que recurso próprio
  do banco é testável e não precisa de dialeto de compatibilidade.

## Goals / Non-Goals

**Goals:**

- Guarda permanente do registro, com o coletor identificado e a hora da medição preservada.
- Particionamento por tempo da tabela de registros desde a primeira linha — depois de gravada,
  a tabela não se reparticiona sem migração de dados.
- Um só ponto no núcleo que apure o período de cadência, porque a entrega seguinte — a
  interrupção por dois períodos — vai apurá-lo com a mesma régua.

**Non-Goals:**

- Transição de estado da série, invalidação, estorno e amostra de auditoria: entregas
  seguintes, e o desenho só precisa não atrapalhá-las.
- Consulta e agregação de séries, públicas ou do coletor: entrega seguinte.
- Autenticação por credencial de dispositivo: entrega seguinte, e a origem `sensor` já nasce
  recusada na rota de sessão.

## Decisions

### A tabela de registros é particionada por RANGE na data da medição, com partição padrão

O documento 03 §1 manda as séries temporais ficarem no próprio PostgreSQL **particionadas por
tempo**. A chave é a **data da medição**, não a do registro: é ela que ordena a série e por ela
que toda consulta futura vai recortar período.

As partições são **anuais**, criadas na migração para os anos do Ciclo 01, mais uma **partição
padrão** que recebe o que cair fora delas. A padrão existe porque a guarda é permanente e o
Ciclo 01 roda sem agendador: sem ela, uma medição de data inesperada seria **recusada pelo
banco**, e perder dado de território é pior que guardá-lo numa partição menos eficiente.

**Consequência que a entrega seguinte herda:** o PostgreSQL exige que a chave de particionamento
faça parte da chave primária, então a primária do registro é o par **`(id, momento_do_fato)`**.
Quem apontar para o registro — a `Invalidacao` da entrega seguinte — aponta para o par, não para
o `id` sozinho. Fica registrado aqui para não ser descoberto lá.

_Alternativas descartadas:_ partição mensal — multiplica objetos no banco sem ganho num ciclo de
cinco meses; tabela comum, particionando depois — reparticionar exige migrar dado já gravado, e
o documento 03 pede o particionamento desde o início; particionar pela data do registro — a
consulta por período recorta pela medição, e as duas divergem por desenho.

### O período de cadência é civil, no fuso do projeto

Cadência **diária**, **semanal** e **mensal** delimitam, respectivamente, o **dia civil**, a
**semana civil de segunda a domingo** e o **mês civil** em que a medição aconteceu — apurados no
fuso de **São Paulo**, onde o projeto roda (documento 03 §1), e não em UTC, que é como o núcleo
armazena. A diferença é real: medição das 22h de sexta em São Paulo cai no sábado em UTC, e
mudaria de semana.

Um Guerreiro(a) de 8 anos precisa saber se já registrou "esta semana" sem fazer conta. Janela
deslizante ancorada na vigência do desafio seria mais uniforme e menos previsível para quem
registra.

A apuração vive em **uma função só**, em `coletas/regra.py`, porque a entrega seguinte conta
"dois períodos seguidos sem registro" com a mesma régua.

_Alternativas descartadas:_ janela deslizante a partir do início da vigência — exige aritmética
para saber em que período se está; períodos em UTC — desloca a virada da semana para o meio da
noite de sexta, num produto cujo usuário é criança.

### O papel do poder é coluna do catálogo, com índice parcial garantindo um só

`RN-01-54` manda declarar o papel. Ele nasce como coluna **`papel`** em `poder`, anulável — a
maioria dos poderes não exerce papel algum —, com um **índice único parcial** sobre as linhas em
que o papel é `territorio`. É o mesmo recurso que `credencial` já usa para garantir uma
credencial ativa por identificador, e põe a garantia no banco em vez de numa conferência de
aplicação que corre em duas requisições simultâneas.

O crédito da coleta busca o poder pelo papel. **Não** há recuo para busca por nome: sem poder de
papel `territorio` no catálogo, o registro é recusado com 409, como a spec exige. Recusar é
melhor que gravar sem creditar — o registro é imutável, e um crédito não feito não se conserta
depois sem violar `RN-08-10`.

_Alternativas descartadas:_ identificador declarado na implantação — põe regra de negócio na
configuração da operação; semeadura com identificador fixo — a implantação de outra comunidade
replica a plataforma e cadastra o próprio catálogo; busca por nome — o nome é rótulo alterável
por Admin, exatamente o que a decisão do fundador recusou.

### A comunidade do registro se resolve pelo histórico do vínculo, não pelo vigente

`RN-08-03` prende o registro à comunidade vigente do coletor **na data da medição**. O
`VinculoJogador` já é entidade com histórico e um só vigente, mas o helper que existe hoje —
`unir_vinculo_vigente` — só alcança o vigente. Entra uma consulta nova, que localiza o vínculo
cujo intervalo de início e fim contém a data da medição.

A comunidade resolvida é **gravada no registro**, e não derivada na leitura. É o que faz o
filtro por comunidade de `RF-01-18` continuar correto depois de uma transferência, e o que
sustenta a guarda permanente quando o vínculo se encerra.

_Alternativa descartada:_ derivar a comunidade na leitura, a partir do vínculo corrente —
reescreveria a história do território a cada transferência de Guerreiro(a).

### A imutabilidade se faz pela ausência de rota, não por conferência

Registro não tem rota de alteração nem de exclusão. O 405 das specs é o que o roteador já
responde a método não declarado num caminho existente — não se escreve conferência para produzir
o que a ausência de rota produz sozinha.

A `situacao` é o único campo mutável, e nesta entrega nada a move: ela nasce `valida` e a
`invalidada` é da entrega seguinte. A marca **"a conferir"** é campo à parte, não um estado da
situação, justamente porque o registro marcado **credita normalmente** — misturá-la à situação
faria a amostra de auditoria da entrega seguinte confundir "estranho" com "inválido".

### A mídia reusa a porta de armazenamento, e o registro guarda só a referência

Foto e vídeo vão pela `PortaDeArmazenamento`, como o comprovante de aporte em `fila/regra.py`:
disco no ambiente local, Cloud Storage em produção. O registro guarda a **referência**, nunca o
conteúdo — o documento 03 §1 põe os arquivos no Cloud Storage e o banco fica com a série.

## Risks / Trade-offs

- **A partição padrão acumula, se a plataforma passar dos anos criados na migração** → a
  migração cria os anos do Ciclo 01 e a padrão recebe o resto; a entrega que estender o
  calendário cria as partições novas antes de a padrão crescer. Escolha consciente: guardar em
  partição pior é melhor que recusar a medição.
- **A chave primária composta contamina quem apontar para o registro** → registrada acima, na
  decisão do particionamento, para a entrega da invalidação já nascer com o par.
- **O crédito e o registro precisam cair juntos** → a gravação do registro e o crédito de pontos
  correm na **mesma transação**; registro gravado sem crédito não se conserta, porque o registro
  é imutável.
- **O fuso civil e o armazenamento em UTC divergem** → a conversão acontece num só ponto, a
  função de apuração de período, e os testes cobrem a virada das 22h de sexta.
- **Séries de dois Guerreiros sobre o mesmo local são indistinguíveis na leitura pública** → não
  é problema desta entrega: a saída pública, com o piso de três coletores, é entrega posterior.

## Migration Plan

Uma migração do Alembic, na ordem: a coluna `papel` em `poder`, com o índice único parcial; a
tabela `serie_de_coleta`; a tabela `registro_de_coleta` **criada já particionada**, com as
partições anuais e a padrão. Nenhuma das três tem dado prévio a converter — a `papel` nasce nula
em todo poder já cadastrado, e o Admin declara o papel do Território no catálogo antes da
primeira coleta, que é o que a spec de `catalogo-de-poderes` recusa com 409 se faltar.

Rollback é o `downgrade` simétrico: derrubar as duas tabelas e a coluna. Não há dado de outra
entrega a preservar.

## Open Questions

Nenhuma que possa ser respondida depois sem mexer nas specs ou nas tarefas. As duas que
apareceram — como identificar o Poder do Território e o que fazer com a fila offline — foram
decididas pelo fundador antes deste desenho e estão em `proposal.md`.
