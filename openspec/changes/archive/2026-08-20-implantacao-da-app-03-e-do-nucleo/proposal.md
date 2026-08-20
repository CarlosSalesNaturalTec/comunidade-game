## Why

O núcleo e a App 03 rodam só em `localhost`. O documento 03 §1 põe cada frontend em
**endereço próprio** (princípio 3) e fixa a hospedagem do Ciclo 01 — FastAPI no **Cloud Run**,
**Cloud SQL** com PostGIS, saída estática no **Firebase Hosting**, tudo em
`southamerica-east1` (princípio 13). Do que isso exige, o repositório tem **uma** peça: o
`backend/Dockerfile`. Não há workflow de deploy, não há `firebase.json`, não há nada que
publique.

Publicar **agora** é a escolha barata. A parte da plataforma com maior chance de quebrar na
primeira ida a produção não são as telas — é a cadeia: OAuth do Google com origem autorizada,
origem aberta do núcleo, chave por ambiente, PostGIS no Cloud SQL e a semeadura das chaves e
do Admin fundador. Descobrir onde ela falha com a App 03 no menor tamanho que ela jamais terá
— login e um cadastro — custa uma fatia; descobrir com vinte telas prontas custa uma
reescrita. Feita uma vez, toda fatia seguinte de qualquer PRD nasce publicável.

**Esta change não tem `RF-XX-nn` nem `RN-XX-nn`, e não é de um PRD.** Ela é infraestrutura de
implantação: não altera comportamento de produto, não tem delta de spec e declara
`skip_specs: true`. A autoridade dela está um nível acima dos PRDs — o documento 03 §1,
princípios 2, 3 e 13 —, o que a hierarquia do `CLAUDE.md` admite, mas que é exceção à regra de
rastreabilidade e precisa do **aval explícito do fundador antes do `/opsx:apply`**. É o mesmo
caminho da change `isolamento-transacional-dos-testes`.

Ela executa em produção, pela primeira vez, o que `RF-01-54` e `RF-01-61` já implementaram: as
chaves por aplicação e ambiente e a persona Admin do fundador, semeadas na implantação.

## What Changes

**Quatro decisões novas do fundador**, gravadas nos documentos-fonte no mesmo PR:

| Decisão                                                            | Gravada em    |
| ------------------------------------------------------------------ | ------------- |
| Padrão de endereço das oito aplicações e do núcleo                 | 03 §1, doc 09 |
| Cloud Run com `min-instances=0`, e o que isso faz ao freio         | 03 §8, doc 09 |
| Runbook de implantação fora de `docs/` e fora do MkDocs            | doc 09        |
| Domínio registrado fora do Google Cloud; `.com.br` no Registro.br  | doc 09        |

O padrão de endereço, que vale para as oito e nasce inteiro aqui:

| Endereço                        | Aplicação                       |
| ------------------------------- | ------------------------------- |
| `comunidadegame.org`            | App 06 — vitrine (já decidido)  |
| `api.comunidadegame.org`        | Backend API                     |
| `gestao.comunidadegame.org`     | App 03 — gestão                 |
| `aula.comunidadegame.org`       | App 01 — aula presencial        |
| `minhaarea.comunidadegame.org`  | App 05 — persona primária       |
| `responsavel.comunidadegame.org`| App 07 — responsáveis           |
| `apoiador.comunidadegame.org`   | App 08 — apoiador               |
| `mestre.comunidadegame.org`     | App 09 — mestre                 |
| `jogo.comunidadegame.org`       | App 04 — jogo                   |

`minhaarea.` em vez de `guerreiro.` porque o documento 02 §1 trata a persona primária por
**Guerreiro ou Guerreira**: o endereço não congela o masculino.

O que a change entrega:

- **Esteira de implantação do núcleo** em `.github/workflows/`, disparada por push em `main`
  no caminho de `backend/`: imagem, publicação no Artifact Registry, migração Alembic e
  deploy no Cloud Run com `--max-instances=1 --min-instances=0`, região
  `southamerica-east1` e os `CG_*` vindos do Secret Manager.
- **Esteira de implantação da App 03**, disparada no caminho de `apps/app-03-gestao/` e de
  `comum/`: build do Vite com os `VITE_*` e publicação no Firebase Hosting.
- **`firebase.json`** com um alvo de hospedagem por aplicação, para as sete que virão não
  precisarem refazê-lo.
- **Migração como passo próprio** da esteira, não no arranque do contêiner: com
  `min-instances=0` o arranque acontece a cada partida a frio, e migração não pode.
- **Runbook de implantação** em `backend/README.md` e no README da App 03 — ordem dos passos,
  variáveis, semeadura e o que fazer com os 16 segredos. **Nenhum arquivo novo em `docs/`** e
  nenhuma entrada na `nav` do `mkdocs.yml`.
- **`min-instances=0` é escolha de custo com preço declarado**: `max-instances=1` mantém o
  invariante de que a cota e o freio nunca se **multiplicam**, mas o contador em memória
  **reinicia** quando o contêiner dorme. O documento 03 §8 passa a dizer isso, em vez de
  deixar a consequência implícita em "apenas em memória".

Fora do escopo, sem exclusão nova: a publicação das outras sete aplicações, que não existem;
o `.com.br` defensivo, que depende do CNPJ; e qualquer ambiente além dos dois do documento 03
§1 — desenvolvimento em contêiner local e produção no Cloud Run.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

Nenhuma. A change não altera comportamento observável do núcleo nem da App 03:
`.openspec.yaml` declara `skip_specs: true`. O que ela muda é **onde** eles rodam.

## Impact

- `.github/workflows/` — dois workflows novos, cada um disparado só pelo caminho que cobre,
  como os quatro que já existem.
- `firebase.json` na raiz e a configuração de alvos de hospedagem.
- `backend/Dockerfile` — o que faltar para produção; `backend/README.md` — o runbook.
- `apps/app-03-gestao/README.md` — as variáveis de build e de onde elas vêm.
- `docs/03-plataforma-e-arquitetura.md` §§1 e 8, e `docs/09-topicos-em-aberto-e-sugestoes.md`
  — as quatro decisões novas.
- **Sem impacto** em rota, contrato de API, modelo de dados, migração existente ou requisito
  de PRD. `backend/src/` só é tocado se o _spike_ do design apontar necessidade.

**Atos do fundador, fora da esteira**, sem os quais a última tarefa não fecha: registro de
`comunidadegame.org`, provisionamento do Cloud SQL, _client ID_ do Google com as origens
autorizadas, credenciais de deploy como segredos do repositório e a execução única da
semeadura, que devolve os 16 segredos de chave.
