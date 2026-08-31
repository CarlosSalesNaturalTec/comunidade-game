# Esqueleto da App 07 e evolução do Guerreiro(a)

Origem: **PRD-13 — Área dos pais e responsáveis (App 07)**, §§4, 5.1, 5.2, 6.1, 6.2 e 9.
**Fatias 1 e 2** do PRD-13 no `openspec/cronograma-de-fatias.md`.

Atende `RF-13-01` a `RF-13-12`, `RN-13-01` a `RN-13-04`, `RN-13-20` e `RN-13-21`.
`RF-13-09` é atendido **em parte** — motivo e data da ocorrência —, pelo motivo da §_Fora do
escopo_ abaixo.

## Why

O responsável é a única persona cadastrada no núcleo que ainda não tem porta: a
`sessao-do-adulto` já abre a sessão dele pelos três caminhos, a matriz de permissões já lhe dá
`guerreiros_sob_sua_responsabilidade`, o `VinculoResponsavel` já existe e a chave
`app-07-responsaveis` já está semeada — e não há aplicação que consuma nada disso. Das oito
aplicações, a App 07 é a única sem pasta.

As duas fatias andam juntas porque a primeira sozinha entrega uma tela de lista e nada mais: o
que justifica o responsável entrar é ver como a criança está. A fatia 2 é a razão de existir da
fatia 1.

## What Changes

### A App 07 nasce, com a entrada e o recorte do vínculo (PRD-13 §§4, 6.1)

`apps/app-07-responsaveis/` entra no monorepo consumindo `comum/` como as outras cinco
aplicações, com a esteira de CI da pasta já alcançada por `apps/**`:

- entrada por login social ou por usuário e senha criada pela gestão (`RF-13-01`, `RN-13-01`);
- troca obrigatória da senha provisória antes de qualquer outra tela (`RF-13-02`);
- recusa do login sem cadastro prévio, com a orientação de procurar a gestão no encontro
  (`RF-13-03`, `RN-13-02`);
- lista apenas dos vinculados, cada um com o grau de parentesco declarado (`RF-13-04`,
  `RN-13-04`), com alternância entre eles sem sair da aplicação (`RF-13-05`);
- nenhuma tela de cadastro de responsável, de criação ou de edição de vínculo (`RF-13-06`,
  `RN-13-01`).

Nada disso é regra nova no núcleo: a `sessao-do-adulto` já decide os três caminhos de entrada e
a trava da senha provisória, e o `responsavel-e-vinculo` já recorta a leitura pelo vínculo e já
impõe o teto de três responsáveis (`RN-13-03`). Falta o cliente — e falta a rota que serve a
lista.

### O núcleo passa a servir a lista e a evolução ao responsável (PRD-13 §§6.2, 9)

Três leituras novas, todas sob a sessão do responsável e recortadas pelo vínculo vigente:

| Rota                                 | Atende                                                       |
| ------------------------------------ | ------------------------------------------------------------ |
| `GET /v1/eu/guerreiros`              | `RF-13-04`, `RF-13-05`, `RN-13-04`                           |
| `GET /v1/eu/guerreiros/{id}/evolucao` | `RF-13-07`, `RF-13-08`, `RF-13-10` a `RF-13-12`, `RN-13-20` |
| `GET /v1/eu/guerreiros/{id}/ocorrencias` | `RF-13-09` (em parte), `RN-13-21`                        |

O que a evolução entrega:

- **presença, atividades realizadas, pontos, poderes, badges e nível** (`RF-13-07`);
- **progresso da trilha como percurso** — missões concluídas e o que falta —, nunca como saldo
  de pontos (`RF-13-08`), reaproveitando a mesma apuração que já serve `GET /v1/eu/progresso`;
- **criações originais validadas**, com título, trilha e data (`RF-13-10`);
- **ocorrência de conduta** com motivo e data (`RF-13-09`, `RN-13-21`), sujeita à guarda do
  motivo pelo ciclo que o `ocorrencia-de-conduta` já impõe.

O que a evolução nunca entrega, e é conferido em teste: **consulta ao assistente e transcrição
de apoio escolar** (`RF-13-11`, `RN-13-20`) e **dado de qualquer outra criança**, nem em equipe
nem em ranking (`RF-13-12`). Guerreiro(a) sem vínculo com o responsável em sessão recebe 403,
pela guarda que o `responsavel-e-vinculo` já tem.

### O estado da reparação fica registrado como lacuna

`RF-13-09` pede também o **estado da reparação**. A reparação está decidida (documento 13 §3 e
documento 09 §1), mas nenhum PRD tem requisito que a registre: o núcleo não tem entidade,
estado nem devolução de pontos por reparação cumprida, e a App 07 só pode exibir o que existe.
Esta change entrega a ocorrência com motivo e data, e leva a lacuna à §14 do PRD-13 e ao
documento 09 (decisão do fundador, 2026-08-31).

## Capabilities

### New Capabilities

- `area-dos-responsaveis`: a App 07 — a entrada do responsável pelos três caminhos, a trava da
  senha provisória, a lista dos vinculados com o grau de parentesco, a alternância entre eles,
  a ausência de cadastro e de vínculo na aplicação e o painel de evolução de cada vinculado.
- `evolucao-do-guerreiro`: a leitura consolidada que o núcleo serve ao responsável — presença,
  atividades, pontos, poderes, badges, nível, progresso como percurso, criações validadas e
  ocorrências de conduta —, recortada pelo vínculo e vedada ao histórico do assistente e do
  apoio escolar.

### Modified Capabilities

- `responsavel-e-vinculo`: ganha a **rota** pela qual o responsável lê os próprios vinculados,
  com o grau de parentesco de cada vínculo. O recorte já é requisito; o que falta é a leitura
  que o exerce (`RF-13-04`, `RF-13-05`).

## Impact

- **Código novo**: `apps/app-07-responsaveis/` e a leitura da evolução no `backend/src/nucleo/`,
  com as rotas do responsável.
- **Código lido**: `responsaveis/` (vínculo e recorte), `trilhas/` (progresso), `pontuacao/`
  (pontos, níveis e badges), `aulas/` (presença), `resultados/` (atividades realizadas),
  `criacoes_originais/`, `ocorrencias_de_conduta/`, `personas/` e `autenticacao` (sessão do
  adulto), `comum/` (camadas de acesso e visual).
- **Documentação**: a §14 do PRD-13 e o documento 09 recebem a lacuna do estado da reparação;
  `docs/prds/index.md` passa o PRD-13 a em implementação.
- **Fora do escopo**, como o PRD-13 §3.2 já exclui: autocadastro do responsável, cadastro e
  edição do vínculo, consentimento biométrico, tratamento das solicitações, qualquer canal com
  Apoiadores ou terceiros, conteúdo de trilha e lançamento de resultado, histórico do apoio
  escolar e do assistente, notificação por e-mail e a entrega de dados a pesquisadores. Fora
  destas fatias, mas dentro do PRD-13: a autorização única, as solicitações e direitos, os
  termos e o histórico de acessos — inclusive o registro de leitura do termo da jornada 5.1 —,
  o atendimento assistido, as propostas e o aviso de coleta — fatias 3 a 6. Fora por falta de
  requisito: o **estado da reparação** de `RF-13-09`, pelo motivo dito acima.
