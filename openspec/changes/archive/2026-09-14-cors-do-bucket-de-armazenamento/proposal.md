## Why

Origem: **PRD-09 — Área do Mestre**. Não é fatia numerada: é a linha `—` do bloco PRD-09 do
`openspec/cronograma-de-fatias.md`, conserto de provisionamento das fatias 19 e 20, no mesmo
lugar de `2026-09-10-bucket-de-armazenamento-em-producao`. Atende `RF-09-19`, `RF-09-119` e
`RF-09-115`.

Anexar imagem a uma pergunta do quiz **falha em produção**, com a frase genérica "Não foi
possível enviar a imagem. Tente novamente em instantes.". O envio tem três passos, e o segundo
— o `PUT` dos bytes — vai do navegador **direto ao Cloud Storage**, que é terceira origem. O
bucket `comunidade-game-armazenamento` nunca recebeu configuração de CORS: o provisionamento do
`backend/README.md` §2 cria o bucket e concede IAM, e nada mais. Sem ela, o navegador barra o
_preflight_ do `Content-Range` e nenhum byte sai da tela.

O CORS corrigido no núcleo (commit `2d487c7`) **não alcança este caminho**: ele vale para a rota
local do adaptador de disco, em desenvolvimento. Em produção o `PUT` nunca toca o núcleo. É por
isso que a suíte segue verde — o teste de `RF-09-119` percorre os três passos com o adaptador de
disco, por cliente de teste, onde não existe navegador nem _preflight_.

O mesmo defeito expôs um segundo: a camada de acesso comum **engole o motivo** da recusa no
envio de bytes, contrariando `RF-01-02`, e foi o que fez este erro chegar ao Mestre sem dizer o
que houve.

## What Changes

- O bucket de produção passa a **admitir o envio a partir das aplicações do projeto**: a
  configuração de CORS nasce como arquivo versionado no repositório, e o `backend/README.md` §2
  a aplica na mesma sequência que já cria o bucket e concede o papel (`RF-09-19`).
- A abertura da sessão retomável passa a **declarar a origem** que enviará os bytes
  (`ArmazenamentoNoCloudStorage.abrir_sessao`), como o protocolo do armazenamento espera de um
  envio feito pelo navegador (`RF-09-19`).
- A camada de acesso comum passa a **entregar o erro do núcleo também no envio de bytes**, em
  vez de substituí-lo sempre pela mesma frase própria (`RF-01-02`). O Mestre passa a ler o
  motivo — formato recusado, teto de 1 MB, sessão expirada — em vez da frase genérica.

Fora do escopo, pelo que o PRD-09 §3.2 já exclui: nada muda no protocolo de envio retomável, na
lista fechada de formatos (`RF-09-115`), no teto de 1 MB por imagem, nas rotas do núcleo nem na
submissão do quiz pelo Guerreiro(a). Também não entra aqui, e **vira fatia própria**, o defeito
da retomada de arquivo maior que a parte de envio — a imagem de 1 MB é parte única e não é
alcançada por ele.

## Capabilities

### New Capabilities

Nenhuma. A change conserta o que `conteudo-da-missao` e `camada-de-acesso-comum` já exigem.

### Modified Capabilities

- `conteudo-da-missao`: o requisito da sessão retomável passa a exigir que o endereço devolvido
  seja **alcançável pela aplicação que vai enviar** — hoje ele diz que os bytes vão direto ao
  armazenamento, e em produção eles não chegam lá. A imagem da pergunta segue por referência, em
  `desbloqueio-da-missao`, que remete a este mesmo padrão e por isso não recebe delta.
- `camada-de-acesso-comum`: o requisito do corpo de erro único passa a cobrir, em cenário, o
  **envio de bytes** — hoje os cenários só alcançam a chamada comum ao núcleo.

## Impact

- `backend/README.md` §2 — a configuração de CORS entra ao lado do `create` e do
  `add-iam-policy-binding`, e o arquivo versionado que ela aplica.
- `backend/src/nucleo/armazenamento/nuvem.py` — a origem declarada na abertura da sessão.
- `comum/api/cliente.ts` — `enviarParteComProgresso` deixa de descartar o corpo do erro.
- Testes: `backend/tests/` para o adaptador de nuvem e `comum/testes/` para a camada de acesso.
  O caminho do navegador contra o bucket **não é testável na esteira** — é configuração de
  infraestrutura, e a verificação é a conferência descrita nas tarefas.
- Documentação: a linha `—` do bloco PRD-09 no `openspec/cronograma-de-fatias.md`. Nenhuma
  decisão nova de produto: o documento 03 §11 e o `RF-09-119` já decidem o que esta change faz
  funcionar, e por isso nada muda em `docs/` nem no documento 09.
- Migração: nenhuma. Nenhum envio foi gravado por este caminho em produção.
