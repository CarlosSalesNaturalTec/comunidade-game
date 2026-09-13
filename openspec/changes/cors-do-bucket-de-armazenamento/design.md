# Design — CORS do bucket de armazenamento

## Context

Motivação em `proposal.md` — Why. O que o desenho precisa saber:

- O envio tem três passos, e só o segundo sai do núcleo: `POST` abre a sessão (núcleo), `PUT`
  manda os bytes (**armazenamento**), `PATCH` confirma (núcleo). Em produção o segundo passo vai
  a `storage.googleapis.com` — origem diferente da aplicação, e fora do alcance do
  `CORSMiddleware` do núcleo.
- Duas aplicações enviam bytes hoje: a App 09 (conteúdo da missão, imagem da pergunta) e a App
  05 (criação original). Ambas em endereço próprio (documento 03 §1).
- O deploy dos frontends registra um **contorno temporário**: o filtro web da rede corporativa
  bloqueia `*.comunidadegame.org` por domínio recém-registrado, e as aplicações hoje respondem
  em `.web.app`. O endereço definitivo continua sendo o do documento 03 §1.
- O adaptador de disco, usado em desenvolvimento e na esteira, devolve endereço **relativo**: o
  `PUT` vai ao próprio núcleo e já é atendido pelo `CORSMiddleware` desde o commit `2d487c7`.
  Só o adaptador de nuvem tem este problema.
- Provisionamento neste repositório é **runbook no `backend/README.md`**, não passo de workflow
  — é assim com o bucket, o Artifact Registry, o Cloud SQL e os segredos.

## Goals / Non-Goals

**Goals:**

- O `PUT` dos bytes partindo das aplicações do projeto deixa de ser barrado pelo navegador.
- A configuração que permite isso fica **conferível em diff**, não só na memória de quem a
  aplicou.
- A recusa que traga corpo de erro chega ao Mestre com o motivo, em todo o caminho de envio.

**Non-Goals:**

- Não mudar o protocolo retomável, as rotas do núcleo, a lista de formatos nem o teto por tipo.
- Não tornar o bucket legível publicamente: CORS autoriza o **navegador a enviar**, e nada tem a
  ver com quem pode ler o objeto — isso segue no IAM, concedido no bucket.
- Não consertar a retomada de arquivo maior que a parte de envio: é fatia própria.

## Decisions

**1. A configuração de CORS entra como arquivo versionado, aplicado por linha no README.**
Decisão do fundador, 2026-09-13. O arquivo fica ao lado do `create` e do
`add-iam-policy-binding` que já provisionam o bucket, e a linha que o aplica entra na mesma
sequência do `backend/README.md` §2. Assim a configuração vigente se lê no diff, e a troca dela
é revisável como qualquer outra. _Descartado:_ aplicar no `backend-deploy.yml` a cada deploy —
garante que nunca diverge, mas amplia o que o deploy faz e exige dar à conta de implantação
permissão de administração do bucket, que ela hoje não precisa. _Descartado:_ só instrução
escrita, sem arquivo — é o desenho de hoje, e é o que deixou a falta passar despercebida.

**2. A lista de origens nomeia as aplicações que enviam bytes, nos dois endereços.** App 09 e
App 05, no endereço definitivo do documento 03 §1 **e** no `.web.app` em que hoje respondem —
a mesma duplicidade que o workflow do frontend já carrega enquanto o filtro web não libera o
domínio. Aplicação que não envia bytes não entra: a lista é de quem faz `PUT`, não de quem
existe. _Descartado:_ `*` como origem — o bucket guarda artefato comprobatório e criação
original, e autorizar qualquer página a enviar a uma sessão cujo endereço vazou é folga sem
ganho. Quando o filtro web liberar o domínio, sai o endereço temporário e fica o definitivo —
uma linha de diff, como a do workflow.

**3. A abertura da sessão declara a origem que vai enviar.** O cliente do armazenamento admite
declarar, ao abrir a sessão retomável, a origem de quem enviará os bytes; sem isso a sessão
nasce sem a marca que o protocolo espera de um envio feito pelo navegador. A origem vem da
requisição que pediu a sessão — é a aplicação que está falando com o núcleo naquele momento —,
e não de constante no código: repetir a lista em dois lugares é a duplicidade que o `CLAUDE.md`
proíbe, e o bucket segue sendo quem decide, porque só ele admite ou recusa. _Descartado:_ fixar
uma origem no adaptador — quebraria a App 05 ao consertar a App 09.

**4. A verificação é de configuração, não de esteira.** Nenhum teste automatizado alcança o
_preflight_ do navegador contra um bucket real: a esteira usa o adaptador de disco, e mesmo o de
nuvem seria exercitado por cliente HTTP, que não faz CORS. O que a esteira cobre é o que é
código — que a sessão é aberta declarando a origem recebida. O que resta é conferência manual,
descrita na tarefa: aplicar a configuração, ler de volta o que o bucket guarda e anexar o
resultado à change, como `2026-09-10-bucket-de-armazenamento-em-producao` fez com o IAM.

**5. A camada de acesso distingue recusa de falha.** No envio de bytes há dois desfechos ruins
diferentes: a resposta **existe** e traz o corpo de erro único da API — e aí ela chega a quem
consome como qualquer outra recusa, com código e mensagem —; ou a resposta **não existe**,
porque o navegador barrou ou a rede caiu, e aí a camada diz que o envio falhou, sem inventar
uma recusa do núcleo. Hoje os dois viram a mesma frase própria, e é por isso que este defeito
chegou ao Mestre mudo. Nenhuma tela precisa mudar: elas já sabem apresentar a recusa que a
camada entrega.

## Risks / Trade-offs

- **Arquivo versionado não é configuração aplicada: os dois podem divergir.** → É o mesmo risco
  de todo o §2 do README, aceito no mesmo desenho. A conferência da decisão 4 lê de volta o que
  o bucket guarda, e a divergência aparece ali; um passo de deploy é o caminho se isto voltar a
  morder.
- **Aplicar a configuração exige permissão de administração do bucket, que a conta de execução
  não tem.** → É intencional (`2026-09-10-bucket-de-armazenamento-em-producao` — decisão 3): a
  aplicação da configuração é ato de provisionamento, feito por quem provisiona, não pelo
  serviço em execução.
- **O endereço temporário `.web.app` fica na lista depois de o domínio ser liberado.** → Sai na
  mesma troca que tira o contorno do workflow do frontend; enquanto os dois responderem, os dois
  precisam estar lá.
- **Nada garante que o defeito era só este.** → A primeira tarefa é confirmar, no navegador, que
  a falha do envio é a barrada do _preflight_ contra o armazenamento, antes de aplicar qualquer
  conserto. Se for outra, a change para e o recorte se corrige.

## Migration Plan

Nenhuma migração de dado: nenhum envio foi gravado por este caminho em produção. A ordem é
aplicar a configuração ao bucket, depois publicar o núcleo com a origem declarada e as
aplicações com a camada de acesso corrigida — a configuração primeiro porque é ela que
desbloqueia, e o resto funciona com ela no lugar. Reversão: a configuração anterior do bucket
era vazia, e devolvê-la é uma linha; o código reverte por `git revert` como qualquer change.
