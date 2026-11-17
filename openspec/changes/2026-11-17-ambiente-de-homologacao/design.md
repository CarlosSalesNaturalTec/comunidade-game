# Design

## Context

Hoje há dois ambientes. `CG_AMBIENTE` é `Literal["desenvolvimento", "producao"]`, a chave tem
o formato `cg_<ambiente>_<id>.<segredo>` e a conferência recusa a chave de outro ambiente
(`chaves/conferencia.py`). A coluna `ambiente` é `String(32)`, sem enum: o terceiro valor não
pede migração. Cada `*-deploy.yml` publica em produção a cada merge em `main`, e o
`firebase.json` tem um alvo por aplicação, mais o `api`, que faz _rewrite_ para o serviço
`nucleo-comunidade-game`. O que muda está na `proposal.md`. A spec da chave está em
`openspec/specs/chave-de-aplicacao/`.

## Goals / Non-Goals

**Goals:** homologação isolada de produção nos dados, nos segredos e nas chaves; o mesmo
código nos dois ambientes; produção só por disparo manual.

**Non-Goals:** gerador de dados sintéticos; limpeza dos testes já feitos em produção; esteira
da App 04, que hoje não tem deploy; escala ou disponibilidade diferente da de produção.

## Decisions

### 1. Núcleo: um valor novo, e a guarda de arranque fora de desenvolvimento

`Ambiente` ganha `"homologacao"`. `conferir_configuracao_de_producao` passa a valer para todo
ambiente que não seja `desenvolvimento`: o disco do Cloud Run é efêmero também na
homologação, e sem bucket o serviço não sobe. A semeadura e a conferência não mudam de
código — já recebem o ambiente da configuração. A chave de terceiro segue nascendo
`producao` (`RN-01-51`): emitida na homologação, ela não abre o núcleo de homologação, e
emissão, prazo e revogação continuam testáveis.

### 2. Google Cloud: mesmo projeto, nomes com sufixo, conta de execução própria

| Recurso           | Produção (existe)                  | Homologação (novo)                             |
| ----------------- | ---------------------------------- | ---------------------------------------------- |
| Serviço Cloud Run | `nucleo-comunidade-game`           | `nucleo-comunidade-game-homologacao`           |
| Job de migração   | `nucleo-migracao`                  | `nucleo-migracao-homologacao`                  |
| Base              | `comunidade_game` na `nucleo-db`   | `comunidade_game_homologacao` na `nucleo-db`   |
| Usuário da base   | o atual                            | `comunidade_homologacao`, só com a base nova   |
| Bucket            | `comunidade-game-armazenamento`    | `comunidade-game-armazenamento-homologacao`    |
| Conta de execução | `nucleo-runtime`                   | `nucleo-runtime-homologacao`                   |
| Segredos          | os atuais                          | os mesmos nomes com sufixo `-homologacao`      |

A conta de execução própria só lê os segredos e o bucket de homologação: um defeito na
homologação não alcança dado de criança de produção. Os segredos de homologação têm
**valores próprios**, inclusive a chave de cifragem da biometria. O PostGIS é habilitado na
base nova, como foi na de produção. O CORS do bucket novo usa o mesmo arquivo
(`backend/cors-do-bucket-de-armazenamento.json`) com as origens dos sites de homologação.

Descartado: projeto GCP separado — duplica faturamento, Artifact Registry e Workload
Identity sem isolar mais do que a conta de execução já isola.

### 3. Firebase Hosting: um site por aplicação, prefixo `cg-hml-`

Sites `cg-hml-api`, `cg-hml-app-03`, `cg-hml-aula`, `cg-hml-minhaarea`, `cg-hml-responsavel`,
`cg-hml-apoiador`, `cg-hml-mestre` e `cg-hml-vitrine` — prefixo curto para caber no limite de
tamanho do identificador de site. Se algum estiver tomado, o provisionamento escolhe outro e
corrige o `.firebaserc`. O `firebase.json` ganha um alvo `<alvo>-homologacao` por alvo
existente, com a mesma configuração; o `api-homologacao` faz _rewrite_ para o serviço de
homologação, e **todos** os alvos de homologação respondem `X-Robots-Tag: noindex, nofollow`
em `**`, para que dado sintético não chegue a buscador. O cliente OAuth do Google é o mesmo,
com as origens `cg-hml-*` acrescentadas.

### 4. Esteiras: _environments_ do GitHub e um workflow de promoção

Os _environments_ `homologacao` e `producao` guardam **os mesmos nomes** de segredo com
valores diferentes: os `APPNN_CHAVE_DE_APLICACAO` e o `GCP_SECRETOS_CG`. Os nomes de serviço,
Job, bucket, conta de execução, alvo do Hosting e as URLs `*.web.app` **derivam do ambiente**
num passo do próprio workflow — sufixo `-homologacao` e prefixo `cg-hml` —, sem variável a
cadastrar e esquecer. Assim cada workflow tem um job só:

- **Gatilhos de cada `*-deploy.yml`:** `push` em `main` nos caminhos de hoje → homologação;
  `workflow_dispatch` → homologação, para republicar; `workflow_call` com as entradas
  `ambiente` e `versao` → quem a usa é o workflow de promoção.
- **`producao-deploy.yml` (novo):** `workflow_dispatch` com a entrada obrigatória `versao`
  (o `sha` validado). Chama o núcleo primeiro e, depois dele, as sete Apps, todas com
  `ambiente: producao` e checkout daquele `sha`.
- **Núcleo em produção não reconstrói imagem:** usa `nucleo:<versao>` do Artifact Registry e
  falha se ela não existir — só existe imagem que passou pela homologação. É o que garante a
  **mesma imagem**.
- **Apps em produção reconstroem do mesmo `sha`:** a chave e as URLs entram no build pelo
  Vite, então o artefato estático é por ambiente; o código é o mesmo.
- `concurrency` passa a incluir o ambiente, e o `CG_AMBIENTE` sai do bloco `env` fixo.

Descartado: canais de prévia do Firebase — expiram e não fazem _rewrite_ para outro serviço.
Descartado: um workflow por ambiente por componente — dobraria dezesseis arquivos iguais.

### 5. Ordem de entrada

O provisionamento (decisões 2 e 3, e os segredos dos _environments_) vem **antes do merge**:
o merge desta change já publica na homologação. Feito o merge, a primeira promoção a
produção é disparada à mão com o `sha` do merge, para provar o caminho novo. A semeadura da
homologação segue o mesmo procedimento da de produção, inclusive apagar o log depois — a
pendência "Entrega dos segredos da semeadura" do documento 09 vale para os dois.

### 6. Dado sintético e notificação

A homologação nasce com as oito chaves e o Admin fundador; o resto é criado testando nas
aplicações. Restaurar _backup_ de produção na base de homologação é vedado — fica escrito no
procedimento. O núcleo não envia hoje nenhuma notificação a pessoa: a regra vira linha no
`openspec/config.yaml`, para que a change que criar a primeira a suprima na homologação.

## Risks / Trade-offs

- **Instância compartilhada** → carga de teste disputa CPU com produção na `db-f1-micro`.
  Aceito pelo fundador; teste de carga não se faz na homologação.
- **Esquecer de promover** → produção fica atrás de `main`. É o custo do disparo manual
  escolhido; o workflow de promoção mostra o `sha` publicado no resumo da execução.
- **Promover `sha` não validado** → o núcleo recusa por falta de imagem; as Apps não têm essa
  trava, e a disciplina é promover o `sha` que a homologação publicou.
- **Segredo de produção colado no _environment_ errado** → mitigado por nomes de recurso com
  sufixo e conta de execução que não lê o segredo alheio: o serviço não sobe.
