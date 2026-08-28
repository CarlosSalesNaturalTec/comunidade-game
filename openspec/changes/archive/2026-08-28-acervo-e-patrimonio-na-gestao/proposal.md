# Acervo e patrimônio na gestão

**PRD de origem:** PRD-02 — Frontend de gestão (App 03).
**Fatia:** 12 do bloco PRD-02 do `openspec/cronograma-de-fatias.md`.
**Atende:** `RF-02-52`, `RF-02-53`, `RF-02-55`, `RN-02-18`.

## Why

O núcleo já tomba o exemplar permanente e mantém a ficha de vida desde a fatia 9 do PRD-07
(`openspec/specs/patrimonio/spec.md`), mas a gestão não tem por onde fazer nem ler nada disso: a
App 03 não abre o acervo. Sem esta fatia, o controle do acervo didático que a §3.1 do PRD-02
promete existe só como rota, e a regra do documento 05 §3 — perda e dano se anotam, e nunca
viram débito ao Guerreiro(a) nem à família — não tem superfície onde ser praticada.

## What Changes

### Recorte ajustado — decisão do fundador nesta change

O cronograma previa também `RF-02-96` (desativar e reativar ponto de apoio, com o inativo
distinguido na lista). Ele já foi entregue pela change `2026-08-21-desativacao-do-ponto-de-apoio`,
e está na spec `aplicacao-de-gestao` e no `MudarSituacaoDoPontoDeApoio.tsx`. Sai do recorte, e a
linha da fatia 12 no cronograma é corrigida nesta mesma change.

Entra em seu lugar a **designação do responsável pelo acervo** pela App 03 (`RF-07-49`): o
`RF-02-52` exige que o exemplar seja tombado com o responsável designado, o núcleo o deriva do
ponto de apoio (`RN-07-10`) e a aplicação não tinha como designá-lo — a lista de pontos de apoio
apenas dizia se havia ou não um. Sem isso o campo que o `RF-02-52` nomeia ficaria sempre vazio.

### App 03

- **Acervo** — área nova, sob a comunidade escolhida, com a lista dos exemplares tombados:
  título, número de tombo, ponto de apoio, estado de conservação corrente e o responsável
  derivado, com o nome resolvido (`RF-02-52`).
- **Tombamento** pelo Admin, com título, número de tombo, ponto de apoio e estado de
  conservação, apresentando no campo as recusas do núcleo — tombo repetido no mesmo ponto de
  apoio, campo em falta (`RF-02-52`).
- **Ficha de vida** de cada exemplar, aberta em ordem do tempo, com o teor de cada anotação, o
  estado de conservação apurado e quem anotou (`RF-02-53`).
- **Anotação** de cuidado, perda ou dano por Admin ou Mestre, com o estado de conservação
  apurado; a tela diz, ao anotar perda ou dano, que nada é debitado ao Guerreiro(a) nem à
  família, e não pede nem oferece campo para identificar culpado (`RF-02-55`).
- A área **nunca oferece** retirada, empréstimo, devolução ou transferência de exemplar
  (`RN-02-18`).
- **Pontos de Apoio** — o Admin designa e troca o responsável pelo acervo entre os Mestres e
  Apoiadores cadastrados, e a lista passa a mostrar o **nome** do designado (`RF-02-52`,
  `RF-07-49`).

### Núcleo

Nenhuma mudança. `POST /v1/itens-patrimoniais`, `GET /v1/itens-patrimoniais`,
`POST /v1/itens-patrimoniais/{id}/ficha-de-vida` e `PUT /v1/pontos-de-apoio/{id}/responsavel` já
existem e ficam como estão.

### O que fica para depois — e por quê

Nada disto é exclusão nova: o PRD-02 §3.1 mantém tudo em escopo, e a fatia apenas não alcança.

| Adiado                                              | Motivo                                                          |
| --------------------------------------------------- | ---------------------------------------------------------------- |
| Aporte de origem no tombamento                       | não está no `RF-02-52` e não há rota de listagem de aportes      |
| Admin como responsável pelo acervo                   | não há `GET /v1/admins`; o núcleo aceita, a tela ainda não lista |
| Conferência de inventário (`RF-02-56`)               | travada pela mesma pendência do `RF-07-20`, no documento 09      |
| Entregas confirmadas (`RF-02-50`, `RF-02-51`)        | fatia própria, que esta change acrescenta ao cronograma          |

Empréstimo de bancada, guarda por equipe e reposição do acervo permanente continuam fora do
escopo do Ciclo 01 (PRD-02 §3.2).

## Capabilities

### New Capabilities

Nenhuma. O `patrimonio` já é capacidade consolidada; esta fatia é a superfície dele na gestão.

### Modified Capabilities

- `aplicacao-de-gestao`: nasce a área Acervo — lista dos exemplares, tombamento, ficha de vida e
  anotação de cuidado, perda ou dano —, sem caminho de retirada, empréstimo, devolução ou
  transferência; a área Pontos de Apoio passa a designar e trocar o responsável pelo acervo e a
  mostrar o nome dele.

## Impact

- `apps/app-03-gestao/src/acervo/` — área nova (`api.ts`, telas, teste).
- `apps/app-03-gestao/src/pontos-de-apoio/` — designação do responsável e o nome na lista.
- `apps/app-03-gestao/src/App.tsx` — a área Acervo na navegação.
- Documentação: a linha da fatia 12 no `openspec/cronograma-de-fatias.md`, corrigida no recorte e
  marcada como implementada, e a linha nova das entregas confirmadas. Nenhuma decisão nova, logo
  nada muda nos documentos-fonte, no documento 09, no documento 99 nem no PRD-02.
