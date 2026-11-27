# Design

## Context

- O ato por atividade (`POST /v1/atividades/{id}/lancamentos`, `resultados/regra.py`) grava os
  Resultados numa transação; `producao` é `Text NOT NULL` e serve também a App 03 (avulsa, por
  participante e por equipe).
- O prático já tem tudo o que o julgamento precisa em `trilhas/regra.py`:
  `submeter_desafio_de_desbloqueio` (forma aceita, reabertura da recusada),
  `abrir_envio_da_comprovacao`/`confirmar_envio_da_comprovacao` (envio retomável, tetos de
  `teto_do_tipo_de_producao`) e `julgar_desafio_pratico` (dois vereditos, motivo, 5 pontos).
  A rota de julgamento também entrega as recompensas de marco (`entregar_na_aprovacao`).
- A tela da aula (`TelaDaAula.tsx`) já resolve nick → id (`resolverNick`) e tem o formulário
  da ocorrência, que é o molde pedido.

## Goals / Non-Goals

**Goals:** comprovante obrigatório em seis formas no Resultado; julgamento do prático no mesmo
ato, obrigatório quando cabe; formulário único na tela da aula; leitura dos lançados.

**Non-Goals:** leitura pelo Guerreiro(a) do comprovante do Resultado; mudança na App 03; envio
por equipe na App 09; o lançamento por aula do Admin.

## Decisions

1. **Colunas no `Resultado`, sem tabela nova.** Nascem `comprovante_tipo`
   (`TipoDeProducaoDaCriacaoOriginal`), `comprovante_referencia`, `comprovante_tamanho` e
   `comprovante_tipo_do_arquivo`; `producao` passa a anulável e guarda só texto ou endereço. A
   migração preenche `comprovante_tipo = 'texto'` nas linhas existentes — o que gravaram é
   texto — e deixa a coluna `NOT NULL`. _Descartado:_ tabela `ComprovanteDoResultado` — um por
   Resultado, sem ciclo de vida próprio.
2. **Envio antes do lançamento.** `POST /v1/atividades/{id}/lancamentos/comprovantes`
   (`tipo`, `tipo_mime`, `tamanho_declarado`) confere posse da atividade, lista e teto, e abre
   a sessão na referência `resultados/envios/{persona_id}/{envio_id}`; devolve `envio_id` e
   `endereco_da_sessao`. O participante do lançamento leva
   `comprovante: {tipo, texto?, envio_id?}`; a regra consulta o envio (`consultar_envio`), refaz
   a conferência de teto e tipo sobre o real e grava a referência. O `persona_id` na referência
   é o que recusa o envio de outra persona; referência já usada por outro Resultado → 422.
   _Descartado:_ Resultado nasce sem arquivo e recebe depois, como a comprovação do prático —
   o crédito sairia antes de o comprovante existir, e "obrigatório" viraria promessa.
3. **`producao` em texto segue aceito no corpo**, e equivale a `comprovante: {tipo: texto}`;
   vir os dois → 422. É o que deixa a App 03 intocada.
4. **Julgamento como campo do participante.** `julgamento_do_pratico: {cumpriu, publicavel,
   motivo}`. Em `lancar_resultados_da_atividade`, depois de `registrar_resultado`, a função
   nova `julgar_pratico_no_lancamento` (em `trilhas/regra.py`) decide:
   - missão sem prático, ou prático com `cumpriu=True` → julgamento presente é 422;
   - prático não cumprido e julgamento ausente → 422 `julgamento_do_pratico`;
   - declaração com `cumpriu is None` → `julgar_desafio_pratico` sobre ela (decisão 5 do
     proposal), comprovante do Resultado intocado na declaração;
   - sem declaração, ou `cumpriu=False` → grava/reabre a declaração em nome do Guerreiro(a)
     pela mesma conferência de forma de `submeter_desafio_de_desbloqueio` (inscrição, forma
     aceita, legado sem forma) e então julga.
   A rota repete o que a rota de julgamento faz depois: `entregar_na_aprovacao` quando cumpriu.
   Tudo antes do `commit` único — a recusa de qualquer parte desfaz o lote.
   Só o ato por atividade confere o prático: o lançamento **por aula**, do Admin (App 03),
   segue como estava.
5. **A declaração em nome reaproveita a mídia, sem cópia.** `comprovacao_referencia` aponta a
   mesma referência do Resultado; texto e link são copiados para `comprovacao`. A substituição
   da comprovação (`_substituir_comprovacao`) só anula colunas, nunca apaga o objeto, então a
   reabertura posterior pelo Guerreiro(a) não destrói o comprovante do Resultado.
   _Descartado:_ copiar os bytes — custo de armazenamento sem ganho.
6. **Leituras.** `GET /v1/missoes/{id}/desbloqueios/{id_do_guerreiro}` (situação do prático,
   com `exige_julgamento`), `GET /v1/aulas/{id}/resultados` (Mestre: só as atividades de que é
   autor; Admin: todas; nick do Guerreiro(a), sem nome civil) e
   `GET /v1/resultados/{id}/comprovante` (bytes). Permissão nova não: reusam
   `suas_turmas` em leitura e a posse da trilha.
7. **App 09.** O formulário entra em `TelaDaAula.tsx` no lugar da lista; ao escolher
   atividade e nick resolvido, busca a situação do prático. O envio do arquivo reusa o
   helper de envio retomável de `trilhas/api.ts`. `TelaDeLancamento.tsx` e a navegação até ela
   em `App.tsx`/`TelaDeMinhasTurmas.tsx` saem; a prop `aoAbrirLancamento` também.
8. **Livro-razão:** nada novo — o envio é armazenamento já contabilizado como o da criação
   original e da comprovação.

## Risks / Trade-offs

- **Envio órfão** quando o Mestre sobe o arquivo e desiste do lançamento → aceito; o objeto
  fica sem referência, como já acontece na criação original abandonada.
- **Aviso à criança:** a decisão de 2026-11-03 avisa o Guerreiro(a), na tela do desafio, de que
  a mídia fica guardada e pode ir à vitrine; a declaração feita pelo Mestre não passa por essa
  tela. **Decisão do fundador de 2026-11-27:** o aviso de coleta ao Mestre, na App 09, basta —
  a declaração feita pelo Mestre pode ser marcada publicável.
- **`RF-09-74` revisto:** a tela deixa de lançar a equipe de uma vez; a API mantém a lista.
