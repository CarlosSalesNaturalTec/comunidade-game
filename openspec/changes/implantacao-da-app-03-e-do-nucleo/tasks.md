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
      **Corrigido em 20/08/2026**: o Firebase Hosting **não se autentica** ao proxiar o
      _rewrite_, então `--no-allow-unauthenticated` devolvia 403 a todo tráfego. O serviço
      aceita invocação não autenticada, e a proteção segue onde o documento 03 §1 princípio 2
      sempre a colocou — chave, credencial da persona, cota e freio, não a rede.

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
- [x] 3.3 Aplicar ao alvo o endereço `gestao.comunidadegame.org`, com os registros em modo
      "DNS only" enquanto o certificado é emitido (03 §1 p3). Ação no console do Firebase
      Hosting e no DNS da Cloudflare — não é declarável em workflow. Vai para o runbook (4.1)
      e é executada pelo fundador na 5.2. **Conferido em 20/08/2026**: entrada bem-sucedida
      por `https://gestao.comunidadegame.org/` pela rede móvel, fora da rede corporativa
      cujo filtro motivou o contorno por `.web.app` na 3.2.

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
- [x] 5.2 Acompanhar o fundador na primeira execução na ordem do `design.md` — núcleo,
      migração, semeadura, chave da App 03 como segredo do repositório, build, publicação — e
      conferir que a semeadura repetida converge sem emitir chave nova (`RF-01-54`,
      `RF-01-61`). **Feito em 19–20/08/2026**, pelo Cloud Shell: os workflows não podiam
      disparar porque `workflow_dispatch` só aparece depois de o arquivo existir em `main`.
      Núcleo no ar, migração aplicada, 8 chaves de produção e a persona Admin semeadas. A
      execução expôs cinco defeitos, todos corrigidos nos commits desta change. Publicação da
      App 03 fica para o merge, que destrava as duas esteiras.
- [x] 5.3 Conferir a cadeia de ponta a ponta em produção: entrar na App 03 pelo login social,
      criar uma Comunidade Virtual e lê-la na lista; conferir que quem não é Admin recebe a
      recusa por papel (03 §1 p2). **Primeira tentativa em 20/08/2026**: o login recusou com
      `401 chave_invalida` — sexto defeito da implantação. O `backend-deploy.yml` nunca
      declarava `CG_AMBIENTE`, então o serviço rodava com o padrão `desenvolvimento` e
      conferia contra esse ambiente a chave semeada em `producao` (`RN-01-34`). Corrigido
      nesta change: a esteira declara `CG_AMBIENTE=producao` no serviço e no Job de migração,
      e a recusa passa a dizer no log qual das quatro conferências falhou.
      **Conferido pelo fundador em 20/08/2026**, depois do deploy do núcleo: entrada pelo
      login social, Comunidade Virtual criada e lida na lista, e a conta sem cadastro
      recebendo a recusa por papel. Conferido nos dois endereços — `.web.app` e
      `gestao.comunidadegame.org`, este pela rede móvel —, e o log do Cloud Run mostra a
      cadeia inteira em 2xx: `POST /v1/sessoes/social` 201, `GET /v1/eu` 200,
      `GET /v1/comunidades` 200 e `DELETE /v1/sessoes/atual` 204.

## 6. Documentação

- [x] 6.1 Gravar as decisões novas nos documentos-fonte: o padrão de endereço das oito
      aplicações no documento 03 §1; a consequência de `min-instances=0` sobre o freio no
      documento 03 §8; e as quatro decisões — endereços, `min-instances`, runbook fora do
      MkDocs e domínio registrado fora do Google Cloud — na tabela de já decididos do
      documento 09. **Nenhum arquivo novo em `docs/`**, nenhuma entrada na `nav` do
      `mkdocs.yml`, nenhum PRD alterado e nenhuma relação entre documentos mudada — o
      documento 99 e `docs/prds/index.md` ficam como estão.

## 7. Resíduos levados ao fundador

- [ ] 7.1 **A semeadura grava segredo em log.** `RF-01-54` manda imprimir a chave uma vez, e
      rodar isso como Cloud Run Job põe os segredos no Cloud Logging em claro, onde ficam.
      Não é defeito desta change — é consequência de onde o comando roda. Decisão do fundador:
      ou a semeadura corre em terminal interativo, ou entrega os segredos por outro caminho.
      Enquanto não se decide, o log é apagado à mão depois de cada semeadura.
