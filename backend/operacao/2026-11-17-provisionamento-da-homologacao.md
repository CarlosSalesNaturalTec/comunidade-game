# Provisionamento da homologação

Procedimento único, executado pelo fundador **antes do merge** da change
`ambiente-de-homologacao`: o merge já publica na homologação. Nomes e motivos estão no
`design.md` da change (decisões 2 a 5). Produção não muda em nenhum passo.

```bash
PROJETO=comunidade-game-506017
REGIAO=southamerica-east1
INSTANCIA=nucleo-db
SA=nucleo-runtime-homologacao@$PROJETO.iam.gserviceaccount.com
```

> **Vedado:** restaurar _backup_ de produção na base de homologação. Dado de criança, de
> responsável e de portfólio ali é só sintético; o conteúdo que pode vir de produção segue
> `2026-11-26-copia-do-conteudo-para-homologacao.md`.

## 1. Base e usuário na mesma instância

```bash
gcloud sql databases create comunidade_game_homologacao --instance=$INSTANCIA
gcloud sql users create comunidade_homologacao --instance=$INSTANCIA --password='<gerada>'
```

Usuário criado pelo `gcloud` entra no papel `cloudsqlsuperuser`, que é dono das duas bases —
e dono sempre conecta. Por isso só `REVOKE ... FROM PUBLIC` não isola: a base nova passa a ter
dono próprio e o usuário de homologação sai do papel. O usuário de produção (`comunidade`) não
muda: as migrações de produção dependem dele.

**1a.** Logado como `comunidade_homologacao`, na base `comunidade_game_homologacao` — ele
ainda é `cloudsqlsuperuser` e pode transferir para si; o `postgres` pode ser recusado:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;  -- antes do 1b, que tira a permissão
ALTER DATABASE comunidade_game_homologacao OWNER TO comunidade_homologacao;
ALTER SCHEMA public OWNER TO comunidade_homologacao;
```

**1b.** Logado como `postgres`, em qualquer base:

```sql
-- conceda antes de revogar, para não derrubar produção
GRANT CONNECT ON DATABASE comunidade_game TO comunidade;
REVOKE CONNECT ON DATABASE comunidade_game FROM PUBLIC;
REVOKE CONNECT ON DATABASE comunidade_game_homologacao FROM PUBLIC;
GRANT CONNECT ON DATABASE comunidade_game_homologacao TO comunidade_homologacao;
REVOKE cloudsqlsuperuser FROM comunidade_homologacao;
```

**1c.** Conferência — as duas colunas têm de vir `false`, e a API de produção seguir no ar:

```sql
SELECT has_database_privilege('comunidade_homologacao', 'comunidade_game', 'CONNECT')
         AS hml_entra_em_producao,
       has_database_privilege('comunidade', 'comunidade_game_homologacao', 'CONNECT')
         AS prod_entra_em_hml;
```

Prova prática: login de `comunidade_homologacao` na base `comunidade_game` é recusado.

## 2. Bucket com CORS

Copie `backend/cors-do-bucket-de-armazenamento.json` para um arquivo temporário e troque as
origens `comunidade-game-*.web.app` pelas `cg-hml-*.web.app`.

```bash
gcloud storage buckets create gs://comunidade-game-armazenamento-homologacao \
  --location=$REGIAO --uniform-bucket-level-access
gcloud storage buckets update gs://comunidade-game-armazenamento-homologacao \
  --cors-file=cors-homologacao.json
```

## 3. Conta de execução

```bash
gcloud iam service-accounts create nucleo-runtime-homologacao
gcloud projects add-iam-policy-binding $PROJETO --member=serviceAccount:$SA \
  --role=roles/cloudsql.client
gcloud storage buckets add-iam-policy-binding gs://comunidade-game-armazenamento-homologacao \
  --member=serviceAccount:$SA --role=roles/storage.objectAdmin
```

Repita na conta nova as demais permissões que a `nucleo-runtime` tem hoje, **exceto** as que
apontam para segredo ou bucket de produção. A conta de deploy precisa de
`roles/iam.serviceAccountUser` sobre ela.

## 4. Segredos

Para cada segredo que o `GCP_SECRETOS_CG` de produção lista, crie `<nome>-homologacao` — o
nome do segredo, não o da variável: a do Gemini lê `gemini-api-key`. Conceda
`roles/secretmanager.secretAccessor` à `$SA` em cada um deles, e só neles.

| Segredo                                              | Valor na homologação                                            |
| ---------------------------------------------------- | --------------------------------------------------------------- |
| DSN, chave de cifragem da biometria, chave do Gemini | **próprio**, nunca o de produção                                |
| _client ID_ do Google                                | o do cliente OAuth de homologação (passo 5)                     |
| durações das sessões                                 | copiadas de produção — parâmetro, não credencial                |
| identidade do fundador                               | copiada de produção — o fundador entra com a mesma conta Google |

- **DSN:** gere a senha do usuário com `openssl rand -hex 24` — vai dentro de URL — e monte no
  formato do de produção, com `comunidade_homologacao` e `comunidade_game_homologacao`.
- **Biometria:** 32 bytes em base64 de URL, nunca lida a de produção.
- **Gemini:** chave nova, com as mesmas restrições e a mesma conta vinculada da de produção.
- **Fora da homologação:** `CG_BIOMETRIA_DIMENSAO_DO_DESCRITOR`,
  `CG_BIOMETRIA_LIMIAR_DE_COMPARACAO` e `CG_DEEPSEEK_CHAVE_DE_API` — o núcleo não as lê mais.
  Ficam fora também do `GCP_SECRETOS_CG` de homologação do passo 6.
- Grave com `printf '%s'` ou pipe direto entre segredos: quebra de linha no fim estraga o
  valor, e nenhum valor precisa passar pela tela.

Conferência: os sete `-homologacao` têm só a `$SA` como leitora, e a `$SA` não aparece em
nenhum segredo de produção.

## 5. Sites do Firebase e login do Google

```bash
for SITE in api app-03 aula minhaarea responsavel apoiador mestre vitrine; do
  npx firebase-tools@15.28.1 hosting:sites:create cg-hml-$SITE --project $PROJETO
done
```

Site recusado por nome já tomado: escolha outro e corrija o `.firebaserc` e o prefixo
`cg-hml` nas esteiras.

O login Google da homologação usa **cliente OAuth próprio** — o de produção já está no limite
de 10 origens, e com clientes distintos o núcleo de um ambiente recusa o login do outro, porque
confere o _audience_. Em **Google Auth Platform → Clientes → Criar cliente**, tipo Aplicativo
da Web, com as origens `https://cg-hml-<site>.web.app` das seis aplicações com login (`aula`,
`app-03`, `minhaarea`, `responsavel`, `apoiador`, `mestre`) e sem URI de redirecionamento. O
ID vai para o `cg-google-client-id-homologacao` e para o `GOOGLE_CLIENT_ID` do passo 6.

## 6. _Environments_ do GitHub

Em **Settings → Environments**:

| _Environment_ | Segredos                                                                 |
| ------------- | ------------------------------------------------------------------------ |
| `producao`    | os de hoje, sem mudança                                                  |
| `homologacao` | `GCP_SECRETOS_CG` com os nomes `-homologacao`; `GOOGLE_CLIENT_ID` do cliente de homologação; os sete `APPNN_CHAVE_DE_APLICACAO` do passo 7 |

Segredo que vale igual nos dois — `GCP_PROJECT_ID`, `GCP_WIF_PROVIDER`,
`GCP_DEPLOY_SERVICE_ACCOUNT`, `GCP_CLOUDSQL_INSTANCIA` — fica no repositório. O
`GOOGLE_CLIENT_ID` do repositório segue sendo o de produção; o do _environment_ `homologacao`
tem precedência sobre ele. A regra do provedor do Workload Identity tem de aceitar o
_environment_ `homologacao`, se hoje restringe a `producao`.

Variável de _environment_ não tem a quem cair: a `APP05_DURACAO_DE_INATIVIDADE_EM_MINUTOS`,
que só existe em `producao`, é criada em `homologacao` com o mesmo valor — vazia, a App 05
encerra a sessão do Guerreiro(a) logo ao entrar.

## 7. Primeira publicação e semeadura

1. `Backend Deploy` → _Run workflow_ (publica na homologação, com migração).
2. Semeadura com `CG_AMBIENTE=homologacao`, pelo mesmo procedimento da de produção. O log
   não se apaga (documento 09, "Entrega dos segredos da semeadura").
3. As oito chaves `cg_homologacao_*` vão para os segredos do _environment_ `homologacao`.
4. _Run workflow_ nas sete esteiras das Apps.

Conferência: a vitrine de homologação abre em `https://cg-hml-vitrine.web.app`, e uma chave de
homologação apresentada ao núcleo de produção recebe 401.

## 8. Depois do merge

Dispare **Produção Deploy** com o SHA do merge, para provar o caminho de promoção.
