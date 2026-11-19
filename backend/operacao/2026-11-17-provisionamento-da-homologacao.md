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

> **Vedado:** restaurar _backup_ ou copiar qualquer dado de produção na base de homologação.
> A homologação guarda só dado sintético, criado testando nas aplicações.

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

Para cada segredo que o `GCP_SECRETOS_CG` de produção lista, crie `<nome>-homologacao` com
**valor próprio** — nunca o de produção —, inclusive a chave de cifragem da biometria e o DSN,
que aponta para `comunidade_game_homologacao` com o usuário `comunidade_homologacao`. Conceda
`roles/secretmanager.secretAccessor` à `$SA` em cada um deles, e só neles.

## 5. Sites do Firebase e login do Google

```bash
for SITE in api app-03 aula minhaarea responsavel apoiador mestre vitrine; do
  npx firebase-tools@15.28.1 hosting:sites:create cg-hml-$SITE --project $PROJETO
done
```

Site recusado por nome já tomado: escolha outro e corrija o `.firebaserc` e o prefixo
`cg-hml` nas esteiras. No cliente OAuth do Google, acrescente as origens
`https://cg-hml-*.web.app` das seis aplicações com login.

## 6. _Environments_ do GitHub

Em **Settings → Environments**:

| _Environment_ | Segredos                                                                 |
| ------------- | ------------------------------------------------------------------------ |
| `producao`    | os de hoje, sem mudança                                                  |
| `homologacao` | `GCP_SECRETOS_CG` com os nomes `-homologacao`; os sete `APPNN_CHAVE_DE_APLICACAO` do passo 7 |

Segredo que vale igual nos dois — `GCP_PROJECT_ID`, `GCP_WIF_PROVIDER`,
`GCP_DEPLOY_SERVICE_ACCOUNT`, `GCP_CLOUDSQL_INSTANCIA`, `GOOGLE_CLIENT_ID` — fica no
repositório. A regra do provedor do Workload Identity tem de aceitar o _environment_
`homologacao`, se hoje restringe a `producao`.

## 7. Primeira publicação e semeadura

1. `Backend Deploy` → _Run workflow_ (publica na homologação, com migração).
2. Semeadura com `CG_AMBIENTE=homologacao`, pelo mesmo procedimento da de produção, e o log
   apagado em seguida (documento 09, "Entrega dos segredos da semeadura").
3. As oito chaves `cg_homologacao_*` vão para os segredos do _environment_ `homologacao`.
4. _Run workflow_ nas sete esteiras das Apps.

Conferência: a vitrine de homologação abre em `https://cg-hml-vitrine.web.app`, e uma chave de
homologação apresentada ao núcleo de produção recebe 401.

## 8. Depois do merge

Dispare **Produção Deploy** com o SHA do merge, para provar o caminho de promoção.
