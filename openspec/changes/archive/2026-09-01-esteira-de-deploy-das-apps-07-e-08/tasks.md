## 1. Alvos de _hosting_

- [x] 1.1 Acrescentar em `.firebaserc`, no mapa do projeto `comunidade-game-506017`, os alvos
      `responsavel` → `["comunidade-game-responsavel"]` e `apoiador` →
      `["comunidade-game-apoiador"]`, ao lado dos cinco existentes. Verificar que
      `npx firebase-tools@15.28.1 target` reconhece os sete alvos e que o JSON continua
      válido (`python -m json.tool .firebaserc`). O `firebase.json` **não é tocado** — os dois
      alvos já estão lá.

## 2. Esteira de publicação da App 07

- [x] 2.1 Criar `.github/workflows/app-07-deploy.yml`, espelho de `app-05-deploy.yml`:
      `push` em `main` restrito a `apps/app-07-responsaveis/**`, `comum/**`, `firebase.json`,
      `.firebaserc` e o próprio workflow, mais `workflow_dispatch`; `concurrency`
      `app-07-deploy-${{ github.ref }}` sem `cancel-in-progress`; `permissions` com
      `contents: read` e `id-token: write`; `environment: producao`. Verificar que o YAML
      _parseia_ (`python -c "import yaml,sys; yaml.safe_load(open(...))"`) e que o `diff`
      contra `app-05-deploy.yml` mostra apenas pasta, alvo, segredo, nome e `concurrency`.
- [x] 2.2 No mesmo arquivo, o passo de build em `apps/app-07-responsaveis` com
      `VITE_CHAVE_DE_APLICACAO` do segredo `APP07_CHAVE_DE_APLICACAO`, `VITE_GOOGLE_CLIENT_ID`
      do segredo `GOOGLE_CLIENT_ID` e `VITE_URL_DO_NUCLEO` com o contorno temporário
      `https://comunidade-game-api.web.app`, acompanhado do mesmo comentário `TEMPORÁRIO` das
      outras esteiras. Verificar que as três variáveis batem com
      `apps/app-07-responsaveis/src/vite-env.d.ts` — nem sobra nem falta.
- [x] 2.3 No mesmo arquivo, autenticação por `google-github-actions/auth@v2` com
      `GCP_WIF_PROVIDER` e `GCP_DEPLOY_SERVICE_ACCOUNT`, e publicação por
      `npx --yes firebase-tools@15.28.1 deploy --only hosting:responsavel --project
      "${{ secrets.GCP_PROJECT_ID }}" --non-interactive`, com os dois comentários que
      justificam o CLI direto e a versão fixa. Verificar que o alvo citado existe em
      `.firebaserc` e em `firebase.json`.

## 3. Esteira de publicação da App 08

- [x] 3.1 Criar `.github/workflows/app-08-deploy.yml` pelas mesmas três tarefas do grupo 2,
      trocando pasta para `apps/app-08-apoiador`, alvo para `apoiador`, segredo para
      `APP08_CHAVE_DE_APLICACAO` e `concurrency` para `app-08-deploy-${{ github.ref }}`.
      Verificar que o `diff` contra `app-07-deploy.yml` mostra apenas esses quatro pontos.

## 4. Documentação

- [x] 4.1 Reescrever a seção **Implantação** do `apps/app-07-responsaveis/README.md` e do
      `apps/app-08-apoiador/README.md`, que hoje dizem "Ainda não implantada": nomear o
      workflow, o alvo de _hosting_, o segredo da chave e o endereço de produção da aplicação
      (documento 03 §1). Verificar que nenhuma das duas seções ainda contém "Ainda não
      implantada".
- [x] 4.2 Acrescentar a linha desta change à tabela **Infraestrutura transversal (sem PRD)**
      de `openspec/cronograma-de-fatias.md`, com `—` na coluna Fatia, o slug na coluna Recorte
      e `implementado` na Situação. Nada muda em `docs/`: a change não toma decisão nova, não
      altera requisito de PRD, não cria arquivo em `docs/` e não muda relação entre documentos
      — logo, nem o documento 09, nem o 99, nem `docs/prds/index.md`, nem a `nav` do
      `mkdocs.yml` são tocados.
