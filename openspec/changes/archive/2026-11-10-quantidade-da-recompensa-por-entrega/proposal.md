PRD-07 (Economia de recursos e ledger), conserto da fatia 10 do `openspec/cronograma-de-fatias.md`
— linha sem número no bloco do PRD-07. Alcança `RF-07-13`, `RF-09-71`, `RF-09-75`, `RF-09-76` e
`RF-09-84`, já entregues, e aplica a decisão do fundador de 2026-11-09. Não cria rota nem
entidade, e não precisa de migração.

## Why

O núcleo lê a **quantidade** da recompensa de marco de dois jeitos contraditórios. O lastro e a
baixa no livro-razão a tratam como **o que cada Guerreiro(a) recebe**. A recusa "quantidade
esgotada" a trata como **teto da turma**, contando as entregas já feitas.

Na aula inaugural de 2026-11-07 isso travou as entregas. O Mestre declarou **1** por item ("1
livro"): a primeira entrega passou e todas as outras foram recusadas como esgotadas, embora o
saldo estivesse no ponto de apoio. Declarar 30 erraria para o outro lado: a primeira entrega
debitaria 30 unidades para um Guerreiro(a) só.

O documento 02 §8.1 não prevê teto. As duas garantias que ele dá já bastam: **uma entrega por
Guerreiro(a)** e **lastro reverificado no ato**. A decisão do fundador (2026-11-09) fixa a
quantidade como **o que cada Guerreiro(a) recebe por entrega**.

## What Changes

- **Documento 02 §8.1**: a tabela ganha a linha "Quantidade", que diz o que cada Guerreiro(a)
  recebe por entrega. O limite do total é o lastro do ponto de apoio.
- **Documento 09 §1**: a decisão entra em "Já decididos".
- **PRD-04 §5**: o passo 6 do fluxo das entregas do encontro perde "quantidade esgotada" da
  lista de recusas.
- **Núcleo**: a entrega deixa de recusar por "quantidade esgotada". No lugar, recusa a segunda
  entrega ao **mesmo** Guerreiro(a). Não é regra nova: a spec já dizia "uma por Guerreiro(a)",
  e até aqui só a fila garantia isso.
- **BREAKING**: `GET /v1/entregas-pendentes` deixa de devolver `quantidade_esgotada`. Só as
  Apps 09 e 01 consomem o campo, e as duas mudam neste PR.
- **Apps 09 e 01**: a fila de entregas pendentes deixa de mostrar a marca de "esgotada".
- **App 09**: na declaração da recompensa, o rótulo do campo passa de "Quantidade" a
  "Quantidade por Guerreiro(a)", para o Mestre não declarar o total da turma.
- **Cronograma**: uma linha sem número no bloco do PRD-07.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `recompensa-de-marco`: quatro requisitos mudam.
  - "O Mestre autor declara qual marco concede qual recompensa": a quantidade passa a ser o que
    cada Guerreiro(a) recebe.
  - "O Mestre da comunidade confirma a entrega": sai a leitura de N como total.
  - "Cinco condições recusam a entrega antes de qualquer escrita" sai. Quatro requisitos tomam o
    lugar dele: as recusas, o lastro no ato, "uma entrega por Guerreiro(a), sem teto da turma" e
    o marco alcançado. A troca existe porque um requisito modificado não pode perder
    cenário.
  - "O marco alcançado vira pendência de entrega para o Mestre": sai a pendência marcada como
    esgotada.
  - "O Guerreiro(a) lê as recompensas que conquistou": a lista do que a leitura não antecipa
    perde a quantidade esgotada.
- `area-do-mestre`: dois requisitos mudam.
  - "O Mestre declara a recompensa que o desbloqueio da missão libera": a quantidade é declarada
    por Guerreiro(a).
  - "A App 09 apresenta ao Mestre as entregas de recompensa pendentes": a recusa traduzida deixa
    de citar a quantidade esgotada.

## Impact

- **Núcleo**: em `backend/src/nucleo/recompensas_de_marco/regra.py`, `_validar_entrega`, a
  dataclass `PendenciaDeEntrega` e `listar_entregas_pendentes`. Em `rotas.py`, a resposta da
  fila.
- **App 09**: `src/recompensas/api.ts`, `FilaDeEntregasPendentes.tsx` e
  `src/trilhas/DeclaracaoDeRecompensa.tsx`.
- **App 01**: `src/api/entregasPendentes.ts` e `src/entregas/TelaDeEntregasDoEncontro.tsx`.
- **Testes**: `backend/tests/test_entrega_de_recompensa.py`,
  `backend/tests/test_entregas_pendentes.py` e os testes das duas filas e da declaração.
- **Documentação**: documentos 02 e 09, PRD-04 e cronograma.
- **Dados**: nenhuma correção. As recompensas da Guerreira Zeferina foram declaradas com 1 por
  item, e a entrega já feita debitou 1. As entregas travadas passam sem mudar nada no banco.
- **Fora do escopo**: o "esgotado" do desafio extra (App 05), que é outra regra, e tudo o que o
  PRD-07 §3.2 já exclui.
