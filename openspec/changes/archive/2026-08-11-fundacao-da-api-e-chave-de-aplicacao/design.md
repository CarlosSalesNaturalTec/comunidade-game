## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta:

- O repositório não tem nenhuma pasta de código. Tudo aqui é primeira vez: primeiro
  `pyproject.toml`, primeira migração, primeiro workflow de CI de código.
- O documento 03 já decidiu o que não se reabre: Python 3.12 com FastAPI, Cloud SQL para
  PostgreSQL com PostGIS, Cloud Run em `southamerica-east1`, Ruff e pytest. E impôs uma
  restrição que molda quase tudo abaixo: **contêiner e banco portáteis**, para outra comunidade
  replicar fora do Google Cloud.
- `RN-01-32` põe a conferência da chave no caminho de **toda** chamada sob `/v1`. É o código
  mais quente do núcleo: roda antes de qualquer rota, em toda requisição, para sempre.
- A spec de `chave-de-aplicacao` exige que os três motivos de recusa sejam indistinguíveis
  **inclusive no tempo de resposta**. Isso é requisito de comportamento observável, e decide o
  algoritmo — não é detalhe de implementação.

## Goals / Non-Goals

**Goals:**

- Deixar pronto o esqueleto que as doze fatias seguintes do PRD-01 estendem sem refatorar.
- Fazer da conferência da chave um custo fixo e pequeno por requisição, sem consulta pesada.
- Fazer a semeadura das dezesseis chaves ser repetível sem estrago.

**Non-Goals:**

- **Idempotência de escrita** (PRD-01 §10). Não há rota de escrita nesta change; o cabeçalho de
  reenvio nasce na fatia que trouxer a primeira.
- **Subida ao Cloud Run.** A change entrega contêiner e migração; o que sobe é operação.
- **Extensão PostGIS.** Nenhuma coluna geográfica existe aqui; quem a habilita é a change do
  PRD-08, que tem o que georreferenciar.
- **Rotação de chave.** Revogar e reemitir é `RF-01-53`, de outra fatia.

## Decisions

### A chave viaja em cabeçalho próprio, não no `Authorization`

Cabeçalho `X-Chave-Aplicacao`. O PRD-01 §9 já reserva o `Authorization` para o **token de
sessão da persona**, e as duas credenciais são independentes: `RN-01-34` diz que uma não
substitui nem amplia a outra. Dois cabeçalhos tornam essa independência visível no contrato, e
uma rota autenticada exibe as duas exigências lado a lado.

Nome em português por coerência com as rotas, que já são `/v1/solicitacoes-de-chave` e
`/v1/chaves` — o desenvolvedor de terceiro lê um contrato só, num idioma só.

_Alternativas descartadas:_ `Authorization: ApiKey <segredo>` — colide com o token de sessão no
mesmo cabeçalho. Chave em _query string_ — vaza em log de servidor e em histórico de navegador.

### O segredo tem prefixo público e corpo secreto

Formato `cg_<ambiente>_<id>.<segredo>`, onde `<id>` identifica a chave e `<segredo>` são 256
bits aleatórios. O núcleo localiza a chave pelo `<id>` — busca por índice, não varredura — e
compara o resumo do `<segredo>`.

Sem o prefixo, conferir uma chave exigiria calcular o resumo e varrer a tabela, o que piora a
cada chave emitida e cria justamente a variação de tempo que a spec proíbe.

### O resumo é SHA-256, não uma função de senha

`RN-01-35` exige "resumo criptográfico" e não diz qual. Escolha: **SHA-256**.

O segredo tem 256 bits de entropia sorteada — não é senha humana e não sofre ataque de
dicionário, que é o problema que bcrypt e Argon2 existem para resolver. Uma função lenta aqui
custaria dezenas de milissegundos **em toda requisição da plataforma**, incluindo a consulta
pública que o PRD-01 §10 quer cacheável e tolerante a pico em dia de culminância.

_Alternativa descartada:_ Argon2id — segurança que não se ganha, ao preço de latência que se
paga sempre.

### A recusa é indistinguível por construção, não por cuidado

O caminho de recusa é **um só**, e ele sempre executa o mesmo trabalho:

```text
chamada sob /v1
  │
  ├─ extrai id e segredo do cabeçalho (ausente → id e segredo falsos)
  ├─ busca a chave pelo id            (não achou → registro falso, de valores fixos)
  ├─ calcula SHA-256 do segredo       (SEMPRE — mesmo sem chave e sem registro)
  ├─ compara em tempo constante       (SEMPRE)
  ├─ confere ambiente e situação      (SEMPRE)
  │
  └─ tudo verdadeiro? segue : 401 único
```

Chave ausente, chave inexistente, resumo divergente, ambiente errado e situação revogada
convergem para o mesmo ponto de saída, com o mesmo corpo. Não há ramo curto para nenhum deles —
é o ramo curto que produz a diferença de tempo que denuncia qual foi o motivo.

### O ambiente é conferido, não só herdado do banco

A chave grava o ambiente a que pertence, e o núcleo, que conhece o seu ambiente por
configuração de partida, recusa chave de ambiente diferente.

Bancos separados já bastariam para uma chave de desenvolvimento não abrir produção. A
conferência explícita cobre o caso que os bancos separados não cobrem: um dump de produção
restaurado em desenvolvimento, prática corriqueira e que sem isso faria chaves de produção
passarem a valer na máquina de quem desenvolve.

### Semear é convergir para um estado, não inserir

O comando de semeadura garante **uma chave vigente por aplicação e por ambiente**, com
unicidade no banco sobre esse par. Rodando de novo:

| Situação encontrada       | O que o comando faz                                     |
| ------------------------- | ------------------------------------------------------- |
| Não existe chave vigente  | emite, grava o resumo e imprime o segredo **uma vez**   |
| Já existe chave vigente   | não faz nada, não reemite e não imprime segredo algum   |

Reemitir em cada implantação derrubaria as oito aplicações a cada subida. Imprimir o segredo de
novo violaria `RN-01-35`, que o quer irrecuperável depois da primeira vez — e ele não é
recuperável nem por este comando, porque o núcleo guarda só o resumo.

### O erro é único porque os manipuladores são substituídos

FastAPI erra em três caminhos com três formatos diferentes: validação, `HTTPException` e falha
não tratada. Os três recebem manipulador próprio, para que `RF-01-27` valha também no 404 e no
500 — inclusive o 500, que passa a registrar o rastro no log e devolver ao cliente só código e
mensagem.

Corpo: `codigo`, `mensagem` e `campo`, o último presente só quando o erro se prende a um campo.

### Paginação por cursor opaco

A resposta traz os itens e o cursor da página seguinte. Sem número de página e sem total.

A spec pede listagem **estável entre chamadas consecutivas**, e paginação por deslocamento não
entrega isso: um registro inserido entre a página 1 e a 2 empurra um item para trás e ele
aparece duas vezes. Cursor sobre chave ordenada não tem esse defeito e é mais barato em tabela
grande — que é o que as séries de coleta do PRD-08 serão.

Nenhum requisito de PRD pede "ir à página 7" nem contagem total.

_Parâmetros técnicos, não números de produto:_ página padrão de 25 e teto de 100, ambos em
configuração. Não são regra de negócio e não passam pelo documento 09.

### SQLAlchemy e Alembic, com DSN comum

ORM e ferramenta de migração não estão nomeados no documento 03. Escolha do desenho, não de
produto: são bibliotecas internas, invisíveis no contrato da API, e trocá-las não muda nenhum
comportamento observável.

A conexão usa **DSN padrão de PostgreSQL**, não o conector do Cloud SQL, porque o documento 03
exige que outra comunidade replique fora do Google Cloud.

> Duas escolhas desta seção — o nome do cabeçalho e o par SQLAlchemy/Alembic — não têm origem em
> documento normativo. São revogáveis na revisão sem tocar nas specs.

### Estrutura da pasta

```text
backend/
├─ pyproject.toml          dependências, Ruff (E,F,I,UP,B) e pytest
├─ Dockerfile              contêiner portátil
├─ alembic/                migrações
├─ src/nucleo/
│  ├─ principal.py         aplicação FastAPI, prefixo /v1, manipuladores de erro
│  ├─ configuracao.py      ambiente, DSN, limites de paginação
│  ├─ erros.py             corpo único e catálogo de códigos
│  ├─ paginacao.py         contrato de cursor e filtros
│  └─ chaves/              modelo, conferência, semeadura
└─ tests/
```

## Risks / Trade-offs

| Risco                                                                              | Mitigação                                                                                                 |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Canal lateral de tempo denuncia por que a chave foi recusada                        | Caminho único que sempre calcula resumo e compara em tempo constante; teste que mede a dispersão dos casos |
| Segredo semeado se perde — não há como recuperá-lo                                  | Consequência aceita de `RN-01-35`. O comando imprime uma vez e diz isso na saída; recuperar é reemitir     |
| Middleware na frente de tudo vira gargalo                                           | Busca por índice e um SHA-256 por requisição; sem consulta extra e sem função lenta                        |
| CI sem banco não testa migração nem unicidade                                       | O workflow sobe PostgreSQL como serviço; os testes de chave rodam contra banco real                        |
| Cursor sem total frustra tela de gestão que queira "1 de 12 páginas"                | Nenhum PRD pede; se o PRD-02 vier a pedir, a contagem entra como campo opcional sem quebrar o contrato     |
| Catálogo de códigos de erro cresce desalinhado entre changes                        | O catálogo nasce em `erros.py` como fonte única; cada change acrescenta ali, não em cada rota              |

## Migration Plan

Não há dado a migrar: o banco nasce aqui.

1. Migração inicial cria `chave_de_aplicacao`, com unicidade sobre (aplicação, ambiente) entre
   as vigentes e índice pelo identificador público.
2. Comando de semeadura roda por ambiente e imprime os segredos das chaves que criou.
3. Cada aplicação do projeto recebe o seu segredo por canal fora de banda, na implantação dela.

**Reversão:** a migração desce, e o banco volta a vazio. Nenhuma aplicação depende do núcleo
ainda — esta é a primeira entrega.

## Open Questions

- **Onde a semeadura roda em produção**, quando o Cloud Run entrar: tarefa de implantação ou
  comando manual do Admin. Não muda spec, código nem tarefa desta change.
- **Quem revoga e reemite uma chave do projeto comprometida.** `RF-01-53` cobre a revogação por
  Admin, em fatia posterior; falta dizer se a chave do próprio projeto segue o mesmo caminho ou
  volta pela semeadura.
