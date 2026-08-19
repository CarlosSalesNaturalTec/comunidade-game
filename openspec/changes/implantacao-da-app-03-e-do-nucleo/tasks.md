<!-- Esta change não tem RF-XX-nn nem RN-XX-nn: a autoridade dela é o documento 03 §1,
     princípios 2, 3 e 13, e o §8. Cada tarefa cita a âncora que atende. Ver proposal.md — Why. -->

## 1. Endereço do núcleo — o que precisa ser conferido antes de escrever esteira

- [x] 1.1 Conferir se `southamerica-east1` aceita mapeamento de domínio do Cloud Run (plano A)
      e, não aceitando, se o _rewrite_ do Firebase Hosting alcança o serviço na região (plano
      B). Registrar o resultado no `design.md`, em Decisions. Se A e B falharem, **parar e
      perguntar ao fundador** antes do plano C, que sai do _free tier_ (03 §1 p3, design —
      Decisions). **Feito**: plano A falha — a região não está na lista de mapeamento nativo
      do Cloud Run —, plano B confirmado. `api.comunidadegame.org` nasce como alvo do Firebase
      Hosting com _rewrite_ para o serviço, não como mapeamento de domínio do Cloud Run.

## 2. Esteira de implantação do núcleo

- [x] 2.1 Ajustar `backend/Dockerfile` para produção: porta vinda de `PORT`, como o Cloud Run
      exige, e usuário sem privilégio (03 §1 p13).
- [x] 2.2 Criar `.github/workflows/backend-deploy.yml`, disparado por push em `main` no
      caminho `backend/**`, com autenticação por Workload Identity Federation: build da
      imagem, publicação no Artifact Registry e deploy no Cloud Run com
      `--region southamerica-east1 --max-instances=1 --min-instances=0`, os `CG_*` do Secret
      Manager e o conector do Cloud SQL (03 §1 p13, 03 §8, design — Decisions).
- [x] 2.3 Acrescentar à mesma esteira o passo de migração como Cloud Run Job
      (`alembic upgrade head`), executado **antes** do deploy do serviço e nunca no
      `entrypoint` (design — Decisions).
- [x] 2.4 Deixar o serviço acessível apenas pelo _rewrite_ do Firebase Hosting (plano B
      confirmado em 1.1): sem necessidade de URL pública própria nem certificado do Cloud Run
      — quem serve `api.comunidadegame.org` e o certificado é o Firebase Hosting (03 §1 p3).
      **Feito**: deploy com `--no-allow-unauthenticated`; a permissão de invocação da conta
      de serviço do Firebase Hosting é IAM fora do repositório, registrada no runbook (4.1).

## 3. Esteira de implantação da App 03

- [x] 3.1 Criar `firebase.json` na raiz com **um alvo de hospedagem por aplicação**, já
      nomeando os nove endereços da proposal, e apenas os alvos da App 03 e do núcleo com
      conteúdo real: `app-03` aponta para uma pasta de build existente, `api` traz apenas
      `rewrites` para o serviço do Cloud Run por nome e região — sem pasta de build própria
      (03 §1 p3, design — Decisions). **Feito**: `firebase.json` com os nove alvos e
      `.firebaserc` com o projeto `comunidade-game-506017`. O mapeamento de cada alvo a um
      site real do Firebase Hosting (`firebase hosting:sites:create` +
      `firebase target:apply`) precisa de site já criado — vai para o runbook (4.1), não é
      declarável em código sem o site existir.
- [x] 3.2 Criar `.github/workflows/app-03-deploy.yml`, disparado por push em `main` nos
      caminhos `apps/app-03-gestao/**` e `comum/**`: build do Vite com `VITE_CHAVE_DE_APLICACAO`,
      `VITE_GOOGLE_CLIENT_ID` e `VITE_URL_DO_NUCLEO` vindos de segredos do repositório, e
      publicação no alvo `app-03` do Firebase Hosting (03 §1 p2, p3).
- [ ] 3.3 Aplicar ao alvo o endereço `gestao.comunidadegame.org`, com os registros em modo
      "DNS only" enquanto o certificado é emitido (03 §1 p3). Ação no console do Firebase
      Hosting e no DNS da Cloudflare — não é declarável em workflow. Vai para o runbook (4.1)
      e é executada pelo fundador na 5.2.

## 4. Runbook de implantação

- [x] 4.1 Escrever em `backend/README.md` o runbook do núcleo: provisionamento (Cloud SQL com
      PostGIS disponível, Artifact Registry, Secret Manager, Workload Identity Federation), a
      lista dos `CG_*` exigidos, a semeadura (`python -m nucleo.cli`) com o aviso de que os 16
      segredos aparecem **uma vez só**, e a conferência manual que fecha a publicação
      (`RF-01-54`, `RF-01-61`, design — Risks).
- [x] 4.2 Escrever no `README.md` da App 03 de onde vem cada `VITE_*` e registrar que a chave
      de aplicação é **pública por construção** no _bundle_ estático (03 §1 p2, design —
      Decisions).

## 5. Primeira execução — a ordem é obrigatória

- [x] 5.1 Conferir que `comunidadegame.org` está registrado e que os nameservers respondem.
      **Bloqueia 2.4 e 3.3**: publicar em endereço provisório obrigaria a refazer as origens
      autorizadas do OAuth (design — Risks). **Feito em 19/08/2026**: domínio registrado, sem
      `hold`, nameservers da Cloudflare respondendo, e o projeto do Google Cloud criado com
      faturamento configurado (ver design — Context).
- [ ] 5.2 Acompanhar o fundador na primeira execução na ordem do `design.md` — núcleo,
      migração, semeadura, chave da App 03 como segredo do repositório, build, publicação — e
      conferir que a semeadura repetida converge sem emitir chave nova (`RF-01-54`,
      `RF-01-61`).
- [ ] 5.3 Conferir a cadeia de ponta a ponta em produção: entrar na App 03 pelo login social,
      criar uma Comunidade Virtual e lê-la na lista; conferir que quem não é Admin recebe a
      recusa por papel (03 §1 p2).

## 6. Documentação

- [x] 6.1 Gravar as decisões novas nos documentos-fonte: o padrão de endereço das oito
      aplicações no documento 03 §1; a consequência de `min-instances=0` sobre o freio no
      documento 03 §8; e as quatro decisões — endereços, `min-instances`, runbook fora do
      MkDocs e domínio registrado fora do Google Cloud — na tabela de já decididos do
      documento 09. **Nenhum arquivo novo em `docs/`**, nenhuma entrada na `nav` do
      `mkdocs.yml`, nenhum PRD alterado e nenhuma relação entre documentos mudada — o
      documento 99 e `docs/prds/index.md` ficam como estão.
