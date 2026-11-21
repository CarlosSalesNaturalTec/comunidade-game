# Design

## Context

A entrega vive em `openspec/specs/recompensa-de-marco` e em `recompensas_de_marco/regra.py`
(`registrar_entrega`, `_validar_entrega`). O disponível já existe como `disponivel_de` em
`reservas/regra.py`. O julgamento do prático é `julgar_desafio_pratico`, em `trilhas/regra.py`,
e o marco alcançado é derivado por `missoes_desbloqueadas_pelo_guerreiro`.

## Goals / Non-Goals

**Goals:** lastro pelo disponível; ponto de apoio da aula anterior; entrega na aprovação; App 09
sem seletor de ponto e com o aviso.

**Non-Goals:** necessidade da recompensa (fatia 14); a entrega por aula da App 01, que já tira
o recurso da aula do encontro e só passa a conferir o disponível.

## Decisions

1. **`_validar_entrega` troca `saldo_de` por `disponivel_de`.** A ordem das recusas não muda.
2. **`aula_de_referencia_da_comunidade(sessao, comunidade_id, momento)` em `aulas/regra.py`**:
   a aula de `inicio_em` mais recente até o momento, não cancelada. Fica em `aulas` porque a
   fatia 14 usa a mesma regra para o ponto de apoio da necessidade.
3. **`registrar_entrega` perde o parâmetro `ponto_de_apoio`**: com `aula`, o ponto é o dela;
   sem, é o da aula de referência da comunidade do vínculo vigente do Guerreiro(a). Sem vínculo
   ou sem aula anterior, recusa com 422 no campo `aula_id`. A rota troca o validador "um dos
   dois" por `extra="forbid"` com `aula_id` opcional: quem envia `ponto_de_apoio_id` recebe 422.
4. **Entrega na aprovação, orquestrada na rota do julgamento**, que conhece as duas pontas:
   antes de julgar, lê as missões desbloqueadas; depois de julgar "cumpriu", chama
   `entregar_na_aprovacao(sessao, operador, guerreiro, trilha, desbloqueadas_antes)`, em
   `recompensas_de_marco/regra.py`. Ela pega as recompensas da trilha cujo marco entrou no
   percurso com este julgamento e tenta `registrar_entrega` de cada uma num `SAVEPOINT`: a
   recusa (`ErroDeValidacao` ou `PermissaoNegada`) desfaz só aquela entrega e a deixa na fila,
   sem desfazer o julgamento. Descartada: chamar a entrega de dentro de
   `julgar_desafio_pratico` — `recompensas_de_marco.regra` já importa `trilhas.regra`, e o
   inverso criaria ciclo.
5. **`JulgamentoDoPraticoSaida` ganha `recompensas_entregues`**, a lista de ids, vazia quando
   nada foi entregue.
6. **App 09**: a fila tira o seletor e a carga dos pontos de apoio e envia só o Guerreiro(a); a
   bancada mostra "Recompensa entregue." quando a lista vem preenchida.

## Risks / Trade-offs

- A aula de referência é a da **comunidade**, não a do ponto onde o kit de fato está: comunidade
  com mais de um ponto de apoio tira do ponto da última aula, como o fundador decidiu.
- O Mestre autor que não é da comunidade aprova sem entregar; a entrega espera o Mestre
  vinculado, na fila.
