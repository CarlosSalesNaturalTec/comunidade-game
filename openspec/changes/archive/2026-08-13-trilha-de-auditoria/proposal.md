## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Décima primeira fatia, na ordem do
documento 99 §9.

**Requisitos atendidos:** `RF-01-29` (entidade `Auditoria` e a trilha consultável por Admin).

A décima fatia (Quiz ao Vivo) já registrou que `RF-01-29` era **"o último recorte do PRD-01
inteiramente destravado"** ao lado dela — os requisitos que restam depois esperam os números
da proteção das rotas públicas, o livro-razão do PRD-07, o território do PRD-08 ou a entrega
do conjunto de dados, todos pendentes no documento 09 §1. `RF-01-29` não depende de nenhum
deles: fecha sozinha.

### Interpretação aplicada, confirmada pelo fundador

O PRD-01 tem duas frases sobre o alcance da trilha: `RF-01-29` diz "das ações de **Admin**", a
rota no §9 diz "das ações de **gestão**", e o critério de aceite do §12 diz **"toda escrita
bem-sucedida gera registro de auditoria com autor, papel e data e hora"** — sem restringir a
persona. O próprio código das dez fatias já resolveu essa tensão a favor da leitura ampla: o
mixin `ComAutoria` (`backend/src/nucleo/autoria.py`) grava autor, papel e momento em **toda**
entidade escrita por **qualquer** papel, não só pelo Admin.

Esta fatia aplica a mesma leitura: a trilha audita **toda escrita bem-sucedida, de qualquer
persona**; "das ações de Admin"/"de gestão" descreve **quem lê** a trilha (`GET
/v1/auditoria`, rota de Admin no PRD-01 §9), não quem é auditado. Não é regra nova nem número
inventado — é a leitura que já está em vigor no código; fica registrada aqui para não
precisar ser refeita a cada fatia.

## What Changes

- Nasce a entidade **`Auditoria`**, somente inserção (mesmo padrão de `Consentimento` e
  `acesso_ao_template`: _listener_ de mapeador + trigger que recusa `UPDATE` e `DELETE`), com
  autor, papel do autor, ação, entidade afetada, data e hora e origem (a aplicação da chave
  que fez a chamada).
- Nasce um **middleware central** de auditoria: grava uma linha por chamada de escrita
  (`POST`/`PUT`/`PATCH`/`DELETE`) bem-sucedida sob `/v1`, lendo o contexto que
  `exigir_persona` e `exigir_chave_de_aplicacao` já resolvem. Nenhuma rota — presente ou
  futura — precisa declarar nada para entrar na trilha; o mesmo raciocínio que já vale para a
  matriz de permissões (design da segunda fatia): infraestrutura que não se esquece, em vez
  de disciplina de quem escreve rota depois.
- Nasce a rota **`GET /v1/auditoria`**, Admin, paginada e filtrável pelo contrato único de
  listagem (`contrato_de_listagem`, já existente em `paginacao.py`), com os filtros
  universais (período, persona) e os filtros de domínio (ação, entidade afetada).
- **Escrita anterior a esta fatia não ganha entrada retroativa.** A trilha passa a existir a
  partir de quando o middleware sobe; as dez fatias já entregues seguem auditáveis pelas
  colunas de autoria que cada uma já grava nas próprias entidades (`ComAutoria`,
  `acesso_ao_template`, `quem_confirmou`, `revogada_por` etc.), só não aparecem em
  `GET /v1/auditoria`.

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; regras de pontuação, cadência
de coleta e valoração de aporte; captura da imagem, conversa de cadastro e geração do
descritor no aparelho; exclusão do _template_; telemetria da Batalha de Laser e
personalização por IA.

O que é do PRD-01 mas de outra fatia:

| Fica para                                              | Porque                                        |
| -------------------------------------------------------- | ---------------------------------------------- |
| `RF-01-33`, `RF-01-34`, `RF-01-43`, `RF-01-22`            | documento 09, "Números da proteção das rotas públicas" |
| `RF-01-49` a `RF-01-53`, `RF-01-55`                       | documento 09, "Números da proteção das rotas públicas" |
| `RF-01-25`, `RF-01-46`, `RF-01-47`                        | fila de avaliação e entrega do conjunto de dados |
| `RF-01-23`, `RF-01-24`                                    | território (PRD-08) e livro-razão (PRD-07)     |
| `RF-01-31`                                                | PRD-01 §14, pendência declarada                |

Reconstruir a coluna `origem` retroativa das dez fatias já entregues também fica fora: nenhuma
delas guarda hoje qual chave fez a chamada, e não há como inferir isso depois do fato.

## Capabilities

### New Capabilities

- `auditoria`: a entidade `Auditoria` somente inserção, o middleware central que grava uma
  linha por escrita bem-sucedida sob `/v1` com autor, papel, ação, entidade afetada, data e
  hora e origem, e a rota `GET /v1/auditoria`, de Admin, paginada e filtrável.

### Modified Capabilities

Nenhuma. O Admin já alcança a nova rota por `Operacao.tudo`, herdado desde a segunda fatia —
sem entrada nova na matriz de permissões, como o precedente do Quiz ao Vivo já registrou para
uma operação que já existia no enum.

## Impact

- `backend/src/nucleo/`: módulo novo `auditoria/` (`Auditoria`, o middleware de escrita e a
  rota de consulta), lendo `personas`, `sessoes`, `chaves` e `paginacao` já existentes.
  **Nenhuma alteração em rota já entregue**: o middleware é transversal, não retrofita nada.
- `backend/src/nucleo/principal.py`: registra o middleware novo e inclui o roteador de
  auditoria.
- `backend/alembic/`: migração para a tabela `auditoria`, somente inserção.
- `docs/`: nenhuma mudança de documento-fonte — a interpretação de `RF-01-29` fica registrada
  nesta proposta, sem alterar texto do PRD-01. `docs/prds/index.md` não muda de situação: o
  PRD-01 segue "aprovado", fatiado em changes.

## Questão que fica para o `design.md`

**Como o middleware deriva "ação" e "entidade afetada" de forma genérica.** O PRD-01 §8
nomeia as duas colunas sem prescrever a fonte; a escolha entre usar o nome da rota FastAPI, o
método HTTP mais o caminho, ou um mapeamento explícito por rota é desenho de execução, não
regra de produto — vai para o `design.md`.
