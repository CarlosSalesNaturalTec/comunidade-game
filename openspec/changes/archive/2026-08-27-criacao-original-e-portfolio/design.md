## Context

O núcleo já tem `CriacaoOriginal` (modelo, regra de entrega, validação, devolução), o crédito
dos 50 pontos com nível 5 e badge de autoria, e a leitura pública do portfólio na vitrine. O que
não existe é a exposição HTTP: nenhuma rota entrega nem valida. Ver `proposal.md — Why`.

Três padrões consolidados que esta fatia aplica sem reabrir:

| Padrão                              | Onde já está                                        |
| ----------------------------------- | ---------------------------------------------------- |
| Envio de mídia em sessão retomável  | `conteudos/rotas.py` — abrir, `PUT` no armazenamento, confirmar |
| Posse estrita do Mestre autor       | `trilhas.regra.conferir_posse_da_trilha`             |
| Autorização de divulgação vigente   | `vitrine.rotas.condicao_de_autorizacao_vigente`      |

As operações de permissão que a fatia usa já existem: `suas_criacoes` para o Guerreiro(a) e
`suas_trilhas_e_conteudos` para o Mestre.

## Goals / Non-Goals

**Goals:**

- Expor entrega, validação, devolução, portfólio e fila pelas rotas do PRD-05 §9 e do PRD-09 §9.
- Estender `CriacaoOriginal` para a modalidade individual e para os cinco tipos de produção, sem
  quebrar o registro em equipe que já existe.

**Non-Goals:**

- Reescrever a regra de crédito: ela ganha o caminho individual e mantém o de equipe intacto.
- Tocar a formação da equipe, a culminância ou a autorização de divulgação — nenhuma das três é
  escrita aqui.

## Decisions

**1. A rota da entrega é `POST /v1/culminancias/{id}/criacoes`, e o registro continua na
trilha.** O PRD-05 §9 endereça a entrega pela culminância; a spec `culminancia` já firmou que a
criação se resolve pela trilha. A rota resolve a trilha pela culminância endereçada e grava
`trilha_id` como hoje. Nenhuma coluna nova de culminância entra no registro.
_Alternativa descartada:_ `POST /v1/trilhas/{id}/criacoes` — contraria o contrato do PRD-05 §9.

**2. A modalidade individual entra com `equipe_id` opcional e `guerreiro_id` opcional, exatamente
um dos dois preenchido.** `ComAutoria.autor_id` continua gravando quem entregou; `guerreiro_id`
é quem a criação credita na modalidade individual — na de equipe os creditados seguem vindo de
`IntegranteDaEquipe`. Restrição de tabela garante o "exatamente um".
_Alternativa descartada:_ criar uma equipe de um integrante para a modalidade individual — poluiria
a homologação de equipe do App 01, que tem regra própria (`RN-01-44`).

**3. A unicidade passa a ser por autor, e a nova entrega substitui a produção enquanto não
validada.** Índice único parcial em `equipe_id` e em `guerreiro_id`. A entrega repetida antes da
validação sobrescreve a produção e devolve a situação a "entregue" — é o reenvio que a devolução
para ajuste pressupõe (`RF-05-42`), e que a regra vigente hoje recusaria com 422. Depois de
validada, a substituição é recusada com 409: refazer a produção reabriria o crédito já lançado.
_Alternativa descartada:_ versionar as entregas — o PRD não pede histórico de produção, e a
autoria, que é o que precisa persistir, já persiste no registro.

**4. Os cinco tipos de produção replicam `TipoDeConteudo`, e a mídia usa a mesma sessão retomável
de envio.** `tipo` fechado em texto, imagem, vídeo, arquivo e link externo; `producao` deixa de
ser obrigatória na coluna e passa a ser exigida pela regra conforme o tipo — corpo no texto,
endereço no link, arquivo nos três de mídia. As rotas de mídia espelham as de conteúdo:
`POST /v1/criacoes/{id}/arquivo` abre a sessão e `PATCH` a confirma.
_Alternativa descartada:_ aceitar o arquivo no mesmo POST da entrega — o projeto já decidiu a
sessão retomável para vídeo e arquivo, e a App 05 roda em rede instável.

**5. O crédito individual entra em `creditar_pontuacao_da_criacao_original`, como segundo
caminho.** Havendo `equipe_id`, itera os integrantes como hoje; havendo `guerreiro_id`, credita
uma vez a ele. Valor, nível e badge são os mesmos — a modalidade não altera o que cada pessoa
recebe.

**6. O motivo da devolução é coluna própria, preenchida só na devolução.** `motivo_da_devolucao`
nulo por padrão; a validação não o toca, e o reenvio não o apaga — o Guerreiro(a) segue lendo por
que a criação voltou enquanto ajusta.

**7. O portfólio e a vitrine compartilham a condição de exposição.** `GET /v1/eu/portfolio`
devolve as validadas com um campo de exposição derivado da mesma
`condicao_de_autorizacao_vigente` que a vitrine usa, estendida ao autor individual. Uma condição
só, dois consumidores: a divergência entre o que a App 05 promete e o que a vitrine mostra fica
impossível por construção.

## Risks / Trade-offs

- **A migração muda colunas de uma tabela com dados** (`equipe_id` de obrigatória para opcional,
  `producao` idem, unicidade trocada) → a migração é aditiva na ordem: acrescenta colunas novas
  com padrão, relaxa as restrições antigas e só então cria os índices parciais. Registro
  existente é sempre de equipe, com tipo texto — o backfill é determinístico.
- **Habilitar o reenvio muda comportamento que a spec vigente recusava com 422** → é mudança
  declarada em `specs/criacao-original/spec.md`, e o teste que hoje fixa a recusa passa a fixar a
  substituição. Sem ela, `RF-05-42` não fecha: devolver para ajuste sem permitir reenviar não é
  ajuste.
- **O filtro de exposição precisa cobrir as duas modalidades** → um Guerreiro(a) individual sem
  autorização vazaria para a vitrine se o filtro só olhasse `IntegranteDaEquipe`. O cenário está
  na spec da vitrine e vira teste.

## Migration Plan

Uma revisão Alembic sobre `criacao_original`: acrescenta `guerreiro_id`, `tipo`,
`motivo_da_devolucao` e as colunas de mídia; preenche `tipo` como texto nas linhas existentes;
relaxa `equipe_id` e `producao` para opcionais; troca a unicidade de `equipe_id` pelos dois
índices únicos parciais; acrescenta a restrição de "exatamente um entre equipe e guerreiro".
Rollback é a revisão inversa — nenhuma linha existente perde dado, porque toda ela é de equipe.
