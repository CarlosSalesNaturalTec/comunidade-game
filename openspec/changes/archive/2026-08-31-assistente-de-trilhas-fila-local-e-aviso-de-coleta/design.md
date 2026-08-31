## Context

Ver `proposal.md` — Why. O que o desenho encontra pronto:

- **`producao-da-missao`** (fatia 9) já resolveu, no núcleo, o problema de forma da fatia 10:
  porta abstrata, adaptador local fora de produção, Gemini em produção, `None` como
  indisponibilidade e mídia lida em memória, sem tocar `armazenamento`, disco ou log. O
  assistente reusa a forma, não o contrato.
- **`aula-e-presenca`** já é idempotente no par aula e Guerreiro(a): o reenvio devolve o
  registro existente, preserva o `momento_do_fato` original e não erra. É a metade do núcleo de
  que a fila local precisa — e ela já está de pé.
- A App 01 já reconhece a queda de rede **tela a tela**, pela falha da chamada
  (`TelaDaPartida`, `TelaDaProgramacao`), sem `navigator.onLine`.
- **`conteudo-da-missao`** (fatia 6 do PRD-09) é o corpus: `ConteudoDaMissao`, com `missao_id`,
  `ordem`, `tipo` e `corpo`, servida pela trilha publicada.

Restrições que apertam o desenho: o PRD-04 §9 **veda rota que confira nick** (`RN-01-22`), e a
`RN-04-12` **veda dado de imagem no aparelho compartilhado**. As duas decidem a fila local.

## Goals / Non-Goals

**Goals:**

- Uma entidade `ConsultaAoAssistente` que sirva **as duas** portas — a da equipe, agora, e a
  individual do apoio escolar da App 05 depois — sem migração nova quando aquela chegar.
- Fila local que não invente rota, não invente regra e não guarde dado que a `RN-04-12` proíbe.
- Aviso de coleta e área detalhada que **não dependam** da vitrine (PRD-03), que ainda não
  existe.

**Non-Goals:**

- Busca semântica, índice vetorial ou memória de conversa entre atendimentos.
- Medir custo do modelo por consulta: nenhum consumo de nuvem é lançado (`RF-09-90`).
- Fila local de qualquer fato que não seja presença.

## Decisions

### 1. Módulo `assistente` próprio, com a forma de `producoes` e contrato próprio

`backend/src/nucleo/assistente/` com `modelo.py`, `regra.py`, `rotas.py`, `porta.py`,
`local.py`, `nuvem.py` e `fabrica.py`. A porta é `PortaDoAssistente`, com contrato próprio —
pergunta e corpus entram, desfecho e resposta saem —, e a fábrica escolhe pelo ambiente com a
mesma chave e o mesmo modelo do `template_de_missao` (documento 03 §1.12).

Alternativas: reusar `PortaDaProducaoDaMissao` — descartada, o contrato é outro (não há
produção esperada, há corpus); um módulo `ia/` comum às três portas — descartada, refatoração
de código já entregue, fora do recorte da fatia.

### 2. O corpus vai inteiro no prompt, montado no núcleo

A `regra` resolve equipe → `atividade_corrente_id` → `Atividade.missao_id` → `Missao.trilha_id`
e `Missao.posicao`, e monta o corpus com o `corpo` dos `ConteudoDaMissao` das missões daquela
trilha com **posição ≤ à da missão corrente**, na ordem da posição e da `ordem` do conteúdo.
Conteúdo de tipo **texto** entra pelo corpo; **link externo**, **imagem**, **vídeo** e
**arquivo** entram apenas pelo título da missão a que pertencem — o núcleo não busca arquivo
nem segue link para responder.

A `posicao ≤` é a leitura do "já percorridas" que o estado existente permite: a equipe da
trilha não tem registro de missão concluída — o percurso de `desbloqueio-da-missao` é do
Guerreiro(a), não da equipe —, e a posição é a ordem que o Mestre autor declarou.

Alternativas: índice vetorial com recuperação por trecho — descartada, nenhum documento decide
provedor de _embedding_ e o corpus de uma trilha cabe no prompt; derivar "concluída" da
interseção dos percursos dos integrantes — descartada, faria o corpus mudar conforme quem
pergunta, na mesma equipe.

### 3. O desfecho da consulta vem do próprio modelo, num campo do JSON

O adaptador pede ao modelo um JSON com `desfecho` — `respondida`, `fora_do_corpus` ou
`tarefa_escolar` — e `resposta`. A regra grava os três do mesmo jeito e devolve 200 nos três: a
recusa e o encaminhamento são resposta, não erro (`RF-04-37`, `RF-04-38`, PRD-04 §9). O texto da
recusa e o do encaminhamento são **do núcleo**, fixos, e não do modelo — o modelo classifica, a
plataforma é quem fala com a criança.

Alternativa: uma passada de classificação antes da resposta — descartada, dobra latência e custo
num encontro presencial.

### 4. O áudio vai ao modelo multimodal, transcrito e respondido na mesma passada

`multipart/form-data` com `texto` **ou** `arquivo`, exatamente como `POST
/v1/equipes/{id}/producao`. Os bytes são lidos em memória na rota, passam à porta e saem de
escopo ao fim da chamada — sem `armazenamento`, sem disco, sem log (`RF-04-40`, `RN-04-21`).

Alternativa: transcrever no navegador pela Web Speech API — descartada, o documento 03 §4.2 põe
a IA no backend, e o suporte da API varia demais entre os aparelhos modestos do ponto de apoio.

### 5. Indisponibilidade é 503 e não grava nada

`ConsultaAoAssistenteIndisponivel`, 503, no molde de `LeituraDaProducaoIndisponivel`. Sem
resposta não há consulta: gravar a pergunta sozinha guardaria uma conversa que não aconteceu, e
a pergunta falada teria de ser refeita de todo jeito, porque o áudio já foi descartado.

### 6. `ConsultaAoAssistente` nasce com os dois vínculos e o discriminador do assistente

Colunas: `equipe_id` e `guerreiro_id` anuláveis, com `CheckConstraint` de exatamente um —
precedente exato de `ProducaoDaMissao` —, `assistente` (`trilhas` | `apoio_escolar`),
`pergunta`, `resposta` e `desfecho`, mais `ComAutoria`, que grava o integrante que perguntou.
**Uma migração**, com a tabela inteira: a porta individual da App 05 depois só acrescenta rota.

Operação nova na matriz: `consulta_ao_assistente`, do Guerreiro(a), escreve e lê. A rota exige
integrância na equipe, como `registrar_producao` já faz — a matriz sozinha não distingue
integrante de não-integrante.

### 7. A fila local guarda o nick e sincroniza refazendo a sequência que já existe

O item da fila é `{ aula_id, nick, momento_do_fato }`. Voltando a rede, a aplicação refaz, por
item, a sequência que a entrada por confirmação **já usa hoje**: `POST
/v1/sessoes/guerreiro/confirmacao` (que resolve o nick no núcleo, sem devolvê-lo nem exigir
identificador), `GET /v1/eu` e `POST /v1/aulas/{id}/presencas` com o `momento_do_fato` da fila.
Nenhuma rota nova, nenhum contrato novo.

Alternativas: aceitar presença por nick na rota de presença — descartada, a recusa revelaria se
o nick existe, e o PRD-04 §9 veda o oráculo por quem quer que pergunte; guardar no aparelho a
lista de Guerreiros da aula para resolver o nick sem rede — descartada, poria nick e
identificador de criança no aparelho compartilhado, e não há rota que sirva essa lista à App 01.

### 8. A fila vive em `localStorage`, chaveada pela aula, e some ao sincronizar

`localStorage`, não memória: recarregar a página na queda perderia a presença de quem já entrou.
A chave inclui a `aula_id`, e o item é removido assim que o núcleo o aceita — inclusive quando o
núcleo devolve o registro que já existia, que é sucesso (`RF-04-25`). Nada além de
`{ aula_id, nick, momento_do_fato }` é gravado.

### 9. "Sem rede" segue sendo falha de chamada, agora elevada ao aparelho

O estado sai de cada tela e passa a viver em `AparelhoDaAula`, que já guarda a sessão de
trabalho: as telas o consultam e o marcam. É o que permite o aviso em toda tela (`RF-04-23`,
`RF-04-24`) sem repetir a detecção cinco vezes. A sincronização dispara na transição de sem rede
para com rede e no `online` do navegador.

Alternativa: `navigator.onLine` como fonte — descartada, ele diz que há rede local, não que o
núcleo responde; fica como gatilho de nova tentativa, nunca como verdade.

### 10. A área detalhada é tela da própria App 01

Conteúdo do PRD-04 §11, em linguagem de criança, numa rota interna da aplicação, alcançável do
aviso da tela inicial e do aviso da tela de captura. Sem chamada ao núcleo: é texto da
aplicação, e precisa abrir com a rede fora.

Alternativa: apontar para a nota de transparência da vitrine — descartada, é do PRD-03 e ainda
não existe. Quando existir, o link pode substituir ou complementar a tela; a decisão é da fatia
que entregar a nota.

## Risks / Trade-offs

- **O corpus cresce com a trilha e pode estourar o limite do prompt** → a montagem trunca pela
  posição mais recente para trás, mantendo sempre a missão corrente inteira, e o teto entra
  como constante do módulo.
- **O modelo pode classificar mal o desfecho** — responder o que devia recusar, ou recusar o que
  devia responder → a transcrição de pergunta e resposta fica gravada, que é justamente o que o
  PRD-04 §11 destina a "melhorar o conteúdo e auditar o uso da IA"; a auditoria por amostragem
  não tem `RF` no PRD-04 e fica fora.
- **A sincronização abre sessão de Guerreiro(a) que ninguém usará** (decisão 7) → o token expira
  sozinho e a aplicação o descarta no ato; é o preço de não abrir oráculo de nick.
- **Nick errado digitado pelo Mestre na queda só falha na volta da rede** → é o item que a fila
  mostra como falha ao Mestre presente, com nova tentativa; sem rede não há como conferir.
- **`localStorage` do aparelho compartilhado guarda nick de criança até sincronizar** → nick é
  identidade pública (PRD-04 §11), o item some ao sincronizar, e nem imagem, nem descritor, nem
  nome vão para lá.
- **Duas telas novas com texto longo (área detalhada) num aparelho operado de pé** → o aviso é
  discreto e a área é o destino de um toque, nunca um passo obrigatório do atendimento.

## Migration Plan

Uma migração Alembic: a tabela `consulta_ao_assistente`. Nada a converter — a entidade nasce
vazia. Fora de produção o adaptador local responde sem credencial, como `producoes.local`, e a
esteira do backend roda sem chave de Gemini.
