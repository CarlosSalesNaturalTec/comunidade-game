# Design

## Context

Os padrões que esta fatia reaproveita já estão consolidados: a declaração do prático e o
julgamento com motivo (`desbloqueio-da-missao`), a sessão de envio retomável da comprovação
(`trilhas.regra.abrir_envio_da_comprovacao`), o crédito só extra (`ponto-extra`), a fila do
encontro restrita a quem tem presença (`recompensa-de-marco`, `RF-09-75`) e o acervo público
montado de várias fontes sob um portão (`leitura-publica-da-vitrine`). O que é novo: o vínculo
kit ↔ prático, o registro de customização, a pontuação do bem por encontro e a terceira fonte do
acervo.

## Goals / Non-Goals

**Goals:** servir, com contrato estável, tudo o que as fatias 31 (PRD-09), 34 e 35 (PRD-04), 18
(PRD-05) e 14 (PRD-03) vão consumir.

**Non-Goals:** nenhuma tela; nenhum agrupamento de entregas em "robô" (escolha do Mestre, decisão
de 2026-11-12); nenhuma conferência automática de rosto na mídia.

## Decisions

1. **O kit é uma coluna da missão.** `missao.desafio_pratico_kit_id`, chave estrangeira anulável
   para `recompensa_de_marco`, recebida como `kit_apresentado_id` em
   `declarar_desafio_de_desbloqueio` e apagada quando o desafio vira quiz, como os outros campos
   do prático. Recompensa de outra trilha é 422. Sem _backfill_. Descartado: tabela de ligação
   — um prático apresenta no máximo um kit.
2. **O bem é a entrega, não a recompensa.** O item de conservação e de customização é a
   `EntregaDeRecompensa` — o par Guerreiro(a) × recompensa que já existe. A customização está
   **aberta** para a entrega quando há `DesbloqueioDaMissao` com `cumpriu` verdadeiro, do mesmo
   Guerreiro(a), numa missão prática cujo `desafio_pratico_kit_id` é a recompensa da entrega. É
   derivada na leitura, sem coluna de estado; o "último aprovado" é o registro aprovado mais
   recente, ou, sem nenhum, a comprovação daquele desbloqueio.
3. **Módulo novo `cuidado_do_bem/`** com dois modelos:
   - `RegistroDeCustomizacao`: entrega, Guerreiro(a), descrição, mídia (referência, tamanho,
     tipo), `situacao` (pendente, aprovado, reprovado, cancelado, expirado), motivo, aula,
     julgador e data do julgamento, com `ComAutoria` gravando quem registrou — o Guerreiro(a)
     ou o Mestre que capturou. Índice único parcial em (`entrega_de_recompensa_id`) com
     `situacao = 'pendente'`: um pendente por kit, também no banco.
   - `PontuacaoDoBem`: aula, entrega, Guerreiro(a), `fonte` (conservação ou customização) e o
     registro, quando a fonte é customização, com `ComAutoria`. **Unicidade em (`aula_id`,
     `entrega_de_recompensa_id`)** — é ela que garante a `RN-01-66` em qualquer via. A regra
     confere antes, para recusar com 422 dizendo por qual caminho o bem já pontuou; o
     `IntegrityError` restante também vira 422.
   Descartado: guardar a conservação como `Resultado` — ele é de atividade, e o bem não é.
4. **Mestre da aula = Mestre vinculado à comunidade da aula**, como na fila de entregas do
   encontro (`listar_entregas_pendentes` com `aula_id`), e o Guerreiro(a) precisa de presença
   não anulada nela. Descartado: exigir `MestreDaAula` — o aparelho é aberto por qualquer Mestre
   da comunidade, e a fila do encontro já segue essa regra.
5. **A mídia segue a sessão de envio da comprovação**: referência
   `customizacoes/{id}/midia`, só `image/*` e `video/*` da lista de formatos aceitos, teto do
   tipo de produção correspondente, e a referência só é gravada depois de o armazenamento
   confirmar o tamanho. Envia quem gravou o registro, enquanto ele estiver pendente; enviar de
   novo substitui. O registro só pode ser julgado com a mídia confirmada.
6. **Rotas** (prefixo da API já vigente):

   | Método | Rota                                   | Quem                               |
   | ------ | -------------------------------------- | ---------------------------------- |
   | GET    | `/eu/customizacoes`                    | Guerreiro(a): kits abertos e registros |
   | POST   | `/eu/customizacoes`                    | Guerreiro(a) registra              |
   | POST   | `/aulas/{id}/customizacoes`            | Mestre da aula captura             |
   | POST   | `/customizacoes/{id}/envios`           | quem registrou abre o envio        |
   | POST   | `/customizacoes/{id}/envios/confirmacao` | quem registrou confirma          |
   | GET    | `/customizacoes/{id}/arquivo`          | Guerreiro(a) dono e Mestre da comunidade |
   | POST   | `/customizacoes/{id}/cancelamento`     | Guerreiro(a) dono                  |
   | POST   | `/customizacoes/{id}/julgamento`       | Mestre da aula, com `aula_id`      |
   | POST   | `/aulas/{id}/conservacoes`             | Mestre da aula                     |
   | GET    | `/aulas/{id}/fila-do-cuidado`          | Mestre da aula                     |
   | GET    | `/vitrine/customizacoes/{id}/arquivo`  | público, sob o portão do acervo    |

7. **Crédito na mesma transação** do julgamento ou da validação, por
   `ponto_extra.regra.creditar_ponto_extra` com valor 1 (`PONTOS_EXTRAS_DO_CUIDADO_DO_BEM`),
   depois de gravada a `PontuacaoDoBem` — se a unicidade falhar, nada é creditado.
8. **A expiração é o terceiro efeito de `encerrar_ciclo`**: um `UPDATE` de Core de pendente para
   expirado, no mesmo padrão do expurgo da ocorrência de conduta, devolvido como
   `customizacoes_expiradas` na resposta do encerramento.
9. **Terceira fonte do acervo**: `FonteDoAcervo.customizacao_do_kit`; `montar_itens_do_acervo`
   recebe os registros aprovados filtrados por `condicoes_de_customizacao_publica` (aprovado,
   mídia confirmada, autorização vigente), com título = descrição, tipo = imagem ou vídeo pelo
   tipo do arquivo e trilha = a da recompensa. A paginação por `(data de aprovação, id)` passa a
   juntar as três fontes.

## Risks / Trade-offs

- [Descrição longa como título quebra a linha da vitrine] → o núcleo devolve o texto inteiro; o
  corte visual é da fatia 14 do PRD-03.
- [Prático aprovado antes da declaração do kit] → abre a customização do mesmo jeito: a
  condição é o prático aprovado que **hoje** declara o kit, e a comprovação dele é o primeiro
  registro.
- [Registro capturado pelo Mestre sem presença confirmada na hora] → a captura exige presença
  não anulada naquela aula, como o julgamento.

## Migration Plan

Uma revisão Alembic: coluna `desafio_pratico_kit_id` em `missao`, tabelas
`registro_de_customizacao` e `pontuacao_do_bem` com os enums, a unicidade e o índice parcial.
Rollback pelo `downgrade` da mesma revisão; nenhum dado existente é alterado.
