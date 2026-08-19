# Backend API — núcleo

Backend do Comunidade Game (PRD-01): Python 3.12 com FastAPI, SQLAlchemy e Alembic. Em
produção roda no Cloud Run, região `southamerica-east1` (documento 03 §1, princípio 13).

## Comandos

- `uv sync --dev` — instalar dependências
- `uv run uvicorn nucleo.principal:app --reload` — ambiente de desenvolvimento
- `uv run pytest` — suíte de testes
- `uv run ruff format .` / `uv run ruff check .` — formatação e lint

## Variáveis de ambiente (prefixo `CG_`)

Sem valor padrão — o serviço não sobe sem elas declaradas:

- `CG_IDENTIDADE_FUNDADOR` — identidade social do Admin fundador, semeada na implantação
  (`RF-01-61`).
- `CG_SESSAO_ADULTO_DURACAO`, `CG_SESSAO_GUERREIRO_DURACAO` — duração das sessões, calibradas
  no encontro real (documento 09).
- `CG_BIOMETRIA_DIMENSAO_DO_DESCRITOR`, `CG_BIOMETRIA_LIMIAR_DE_COMPARACAO`,
  `CG_BIOMETRIA_CHAVE_DE_CIFRAGEM` — parâmetros da entrada do Guerreiro(a); a chave de
  cifragem vem do **Secret Manager**, nunca hardcoded (documento 09).

Com valor padrão, ajustados em produção:

- `CG_AMBIENTE=producao`
- `CG_DSN_BANCO` — aponta para o Cloud SQL pelo **socket Unix** do conector, em
  `/cloudsql/PROJETO:REGIAO:INSTANCIA`, nunca por endereço de rede.
- `CG_GOOGLE_CLIENT_ID` — o mesmo _client ID_ que os frontends usam.
- `CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE` — bucket de produção; sem ele o núcleo cai para
  disco local, que não sobrevive a um novo deploy do Cloud Run.

## Provisionamento (uma vez por ambiente novo)

Pré-requisito: projeto do Google Cloud com faturamento — `comunidade-game-506017`, região
`southamerica-east1`.

1. **Cloud SQL para PostgreSQL** com a extensão PostGIS disponível. Anotar a string de conexão
   da instância (`PROJETO:REGIAO:INSTANCIA`), usada em `--add-cloudsql-instances`.

   A instância nasce com **IP público habilitado e nenhuma rede autorizada**. Parece
   contraditório e não é: o conector embutido no Cloud Run fala com ela pelo Cloud SQL Auth
   Proxy, que autentica por IAM e cifra o tráfego — sem rede autorizada, ninguém alcança o
   banco pela internet. A alternativa, só IP privado, exigiria _Direct VPC egress_ ou um
   conector de acesso VPC: mais peças e mais custo, sem ganho real de proteção aqui.
2. **Artifact Registry** — repositório Docker `comunidade-game` na mesma região.
3. **Secret Manager** — um segredo por variável sem valor padrão, mais
   `CG_BIOMETRIA_CHAVE_DE_CIFRAGEM` e `CG_DSN_BANCO`. O workflow lê a lista de mapeamentos
   `SECRET:CG_VAR` do segredo do repositório `GCP_SECRETOS_CG` (formato aceito por
   `gcloud run deploy --set-secrets`).
4. **Workload Identity Federation** — um _pool_ e um provedor OIDC para o repositório GitHub,
   e uma conta de serviço de deploy com papel de executor no Cloud Run, no Cloud Run Jobs e no
   Artifact Registry. Os identificadores vão para os segredos do repositório
   `GCP_WIF_PROVIDER` e `GCP_DEPLOY_SERVICE_ACCOUNT`.

5. **Conta de execução do núcleo** — `nucleo-runtime`, distinta da conta de deploy: é quem o
   contêiner **é** enquanto roda, e portanto quem lê os segredos e alcança o Cloud SQL. Sem
   declará-la, o Cloud Run usa a conta de computação padrão, que tem `roles/editor` no projeto
   inteiro — permissão demais para o núcleo que guarda dado biométrico de criança. Recebe
   **apenas** `roles/secretmanager.secretAccessor` e `roles/cloudsql.client`; os workflows a
   passam em `--service-account`.

   ```bash
   gcloud iam service-accounts create nucleo-runtime \
     --display-name="Execução do núcleo no Cloud Run"

   for PAPEL in roles/secretmanager.secretAccessor roles/cloudsql.client
   do
     gcloud projects add-iam-policy-binding comunidade-game-506017 \
       --member="serviceAccount:nucleo-runtime@comunidade-game-506017.iam.gserviceaccount.com" \
       --role="$PAPEL" --condition=None
   done
   ```

6. **Firebase Hosting**, no mesmo projeto GCP (documento 03 §1; ver design.md da change de
   implantação para o porquê). Criar os sites e mapear os alvos declarados em `firebase.json`:

   ```bash
   firebase hosting:sites:create comunidade-game-api
   firebase hosting:sites:create comunidade-game-app-03
   firebase target:apply hosting api comunidade-game-api
   firebase target:apply hosting app-03 comunidade-game-app-03
   ```

   Ligar o domínio a cada site (console do Firebase Hosting → domínio personalizado):
   `api.comunidadegame.org` ao alvo `api`, `gestao.comunidadegame.org` ao alvo `app-03`. Os
   registros DNS que o Firebase pedir entram na Cloudflare em modo **"DNS only"** (nuvem
   cinza) enquanto o certificado é emitido — o proxy da Cloudflare atrapalha a validação.

7. **Permissão de invocação do Cloud Run pelo Firebase Hosting** — o serviço sobe com
   `--no-allow-unauthenticated` (só o _rewrite_ do Firebase o alcança). O `firebase deploy`
   concede essa permissão sozinho quando publica um _rewrite_ do tipo `run` para um serviço
   do mesmo projeto — **não é passo manual**. Confirmar depois do primeiro deploy da esteira
   do núcleo (5.2, depois do primeiro `app-03-deploy.yml` ou de qualquer deploy que publique
   o alvo `api`):

   ```bash
   gcloud run services get-iam-policy nucleo-comunidade-game --region southamerica-east1
   ```

   Esperado: um vínculo `roles/run.invoker` para uma conta de serviço do Firebase Hosting
   (`service-PROJECT_NUMBER@gcp-sa-firebasehosting.iam.gserviceaccount.com`, ou equivalente —
   confira o nome real na saída, não pelo suposto aqui). **Se não aparecer**, publique o alvo
   `api` do Firebase Hosting uma vez (`firebase deploy --only hosting:api`) antes de tentar
   qualquer vínculo manual: é o deploy do Hosting que cria essa conta de serviço.

## Semeadura (uma vez por ambiente)

Depois do primeiro deploy e da primeira migração:

```bash
python -m nucleo.cli
```

Converge as 16 chaves de aplicação (8 aplicações × 2 ambientes, `RF-01-54`) e a persona Admin
do fundador (`RF-01-61`). **Os segredos das chaves aparecem uma única vez** — copie e guarde
antes de fechar o terminal, `semear_ambiente` não os recupera depois. Rodar de novo é seguro:
ambiente já semeado não emite chave nova.

A chave da App 03 do ambiente de produção vira o segredo do repositório
`APP03_CHAVE_DE_APLICACAO`, consumido pelo `app-03-deploy.yml` — é o que destrava o primeiro
build do frontend.

## Conferência que fecha a publicação

Depois do primeiro deploy de cada esteira: entrar em `gestao.comunidadegame.org` pelo login
social, criar uma Comunidade Virtual e lê-la na lista; conferir que quem não é Admin recebe a
recusa por papel, não um erro cru.
