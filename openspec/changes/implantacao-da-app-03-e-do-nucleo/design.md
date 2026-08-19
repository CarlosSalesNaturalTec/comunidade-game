## Context

Ver `proposal.md` — Why. O que o repositório tem hoje: `backend/Dockerfile` (build simples,
`uvicorn` na porta 8000), quatro workflows em `.github/workflows/` — nenhum de deploy —, e a
App 03 lendo `VITE_CHAVE_DE_APLICACAO`, `VITE_GOOGLE_CLIENT_ID` e `VITE_URL_DO_NUCLEO` de
variável de ambiente do Vite. O núcleo já responde a qualquer origem sem cookie credenciado, e
`registrar_premissa_de_conteiner_unico()` já registra no log a premissa do contêiner único.

Restrições que moldam tudo: provedores e região fixados pelo documento 03 §1 princípio 13;
**dois ambientes**, e o de desenvolvimento é contêiner local — não há ambiente de ensaio na
nuvem; e o freio das rotas públicas conta em memória (documento 03 §8).

## Goals / Non-Goals

**Goals:**

- Núcleo e App 03 alcançáveis nos endereços da `proposal.md`, publicados por push em `main`.
- Publicação repetível: a segunda ida a produção não pede nenhum ato manual.
- O `firebase.json` já pronto para as sete aplicações que virão, sem refazê-lo por app.

**Non-Goals:**

- Ambiente de ensaio na nuvem — o documento 03 §1 fixa dois ambientes, e o de
  desenvolvimento é local.
- Observabilidade, alarme, painel de métricas e política de retenção de log.
- Escala, réplica de leitura e backup automatizado do Cloud SQL.
- Publicar as outras sete aplicações, que ainda não existem.

## Decisions

**A esteira autentica por Workload Identity Federation, não por chave de conta de serviço.**
A alternativa — chave JSON num segredo do repositório — põe uma credencial de longa duração,
sem expiração, num lugar de onde ela nunca é rotacionada. Descartada.

**A migração é passo próprio da esteira (Cloud Run Job), não `entrypoint` do contêiner.**
Com `min-instances=0` o contêiner arranca a cada partida a frio: migração no `entrypoint`
rodaria dezenas de vezes por dia e atrasaria a primeira resposta. Alternativa descartada:
`alembic upgrade head` no `CMD`, mais simples e errado pelo mesmo motivo.

**O endereço do núcleo passa por um _spike_, com plano B declarado.** O mapeamento de domínio
do Cloud Run não existe em toda região, e não afirmamos que `southamerica-east1` está na
lista. A primeira tarefa do `tasks.md` é conferir, nesta ordem:

| Plano | Caminho                                       | Custo             |
| ----- | --------------------------------------------- | ----------------- |
| A     | Mapeamento de domínio do próprio Cloud Run    | nenhum            |
| B     | _Rewrite_ do Firebase Hosting para o serviço  | nenhum            |
| C     | Balanceador de carga externo global           | **sai do _free tier_** |

O plano C **não é executado sem decisão do fundador**: o custo do ciclo é aporte por absorção
dele. Se A e B falharem, a tarefa para e pergunta.

**Os `CG_*` vêm do Secret Manager, montados como variável de ambiente do serviço.** É onde o
documento 09 já pôs a chave que cifra o _template_ biométrico; o resto dos segredos segue o
mesmo caminho, em vez de inventar um segundo. O `CG_DSN_BANCO` usa o soquete Unix do conector
do Cloud SQL, e não endereço de rede — o banco não ganha IP público.

**A chave de aplicação de um frontend estático é pública por construção.** `VITE_*` é assado
no _bundle_ no momento do build: quem abrir o JavaScript da App 03 lê a chave dela. Isso é
coerente com o documento 03 §1 princípio 2 — a chave **identifica a aplicação** e sustenta a
cota; quem protege a pessoa é a credencial da persona, que nunca sai do `sessionStorage`.
Registrado aqui para ser escolha consciente e não descuido; **não altera o documento 03**.
Consequência prática: a chave da App 03 é segredo do repositório porque o build precisa dela,
não porque ela permaneça secreta depois.

**A ordem da primeira execução é obrigatória e está no `tasks.md`**, porque o build do
frontend depende de um segredo que só nasce no deploy do backend:

```text
1. núcleo no ar          → 2. migração        → 3. semeadura (uma vez)
   Cloud Run                 Cloud Run Job        16 chaves + Admin fundador
                                                        │
   6. App 03 publicada  ←  5. build do Vite  ←  4. chave da App 03 vira
      Firebase Hosting        com os VITE_*        segredo do repositório
```

Da segunda vez em diante, os passos 3 e 4 não se repetem: a semeadura converge — a mesma
`semear_ambiente` já devolve vazio quando o ambiente está semeado.

**O PostGIS entra no provisionamento, não nesta change.** O documento 03 declara a extensão,
mas nenhuma migração de hoje usa geometria — não há coluna georreferenciada no núcleo ainda.
A instância nasce com a extensão disponível para as fatias de território; a esteira não a
habilita.

## Risks / Trade-offs

**Deploy vai direto a produção, sem ensaio** → é consequência dos dois ambientes do documento
03, não escolha desta change. Mitigação: o runbook do `backend/README.md` fecha com uma
conferência manual curta — entrar pela App 03, criar uma comunidade, ler a lista — e o Cloud
Run mantém a revisão anterior, para o retorno ser um comando de tráfego, não um novo build.

**`min-instances=0` reinicia o freio por origem a cada partida a frio** → o invariante que
importa continua de pé: com `max-instances=1` os limites nunca se multiplicam. Mitigação
possível é só uma — pagar o contêiner ligado —, e o fundador decidiu não pagar no Ciclo 01. A
mitigação real é **declarar**: o documento 03 §8 passa a dizer a consequência, em vez de
deixá-la implícita em "apenas em memória".

**Partida a frio atrasa a primeira chamada** → Python com FastAPI e SQLAlchemy leva alguns
segundos. Aceitável para uma aplicação de gestão operada por Admin; **não** seria aceitável
para a App 01 no meio da aula, e essa é a fatia em que o `min-instances` volta à pauta.

**A troca de domínio depois mexe no OAuth de novo** → se a primeira publicação sair nos
endereços `*.web.app`, o _client ID_ do Google autoriza aqueles, e migrar para
`comunidadegame.org` obriga a refazer as origens autorizadas, com uma janela em que o login
quebra. Mitigação: a tarefa do DNS **bloqueia** até o domínio estar registrado, em vez de
publicar num endereço provisório.

**Os 16 segredos de chave aparecem uma vez só** → `semear_ambiente` não os recupera depois. Se
forem perdidos, a saída é revogar e reemitir. Mitigação: o runbook diz, no passo da semeadura,
onde guardá-los antes de fechar o terminal.

## Open Questions

- Qual _tier_ da instância do Cloud SQL. Não muda o desenho nem as tarefas — muda a conta, e é
  o piso de custo do ciclo, já que o banco cobra ligado enquanto o Cloud Run em zero não cobra.
  Pergunta ao fundador no momento do provisionamento.
