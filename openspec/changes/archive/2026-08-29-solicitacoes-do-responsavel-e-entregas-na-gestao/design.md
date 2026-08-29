## Context

Ver `proposal.md` — Why. O que o núcleo já tem e esta fatia reaproveita: a fila única de
avaliação (`openspec/specs/fila-de-avaliacao/`), com as quatro solicitações do PRD-01 §8, o
prazo de 7 dias gravado no registro e o atraso derivado; o papel `responsavel`, com a operação
`solicitacoes_e_propostas` na escrita e `guerreiros_sob_sua_responsabilidade` na leitura
(`openspec/specs/permissoes-e-escopo-de-comunidade/`); a sessão por credencial de usuário e
senha (`openspec/specs/sessao-do-adulto/`); e a entrega da recompensa de marco com a baixa
definitiva num lançamento só (`openspec/specs/recompensa-de-marco/`). Na App 03, a área Filas
já tem lista e tela de avaliação para quatro filas, e a área Acervo já resolve nome de ponto de
apoio e de persona por mapa montado na própria tela.

O que falta é a quinta solicitação do PRD-01 §8 e as duas telas.

## Goals / Non-Goals

**Goals:**

- A solicitação de direitos existe no núcleo, nasce pelo responsável e é tratada pelo Admin.
- A gestão trata a fila e lê as entregas confirmadas sem escrever nenhuma delas.

**Non-Goals:**

- Telas da App 07 — são da fatia 4 do PRD-13.
- Execução do pedido de exclusão (despersonalização e apagamento do _template_): também do
  PRD-13, e esta fatia grava apenas o desfecho.
- Notificação por e-mail: o Ciclo 01 responde na própria plataforma (03 §9).

## Decisions

**Módulo próprio `solicitacoes_do_responsavel/`, e não uma quinta natureza dentro de `fila/`.**
A fila única existe para o que chega sem criar acesso (`RN-01-03`); a solicitação de direitos
vem de persona autenticada, tem rota, papel e vocabulário próprios. _Alternativa descartada:_
acrescentar o modelo a `fila/modelo.py`, que obrigaria a mexer no requisito das quatro naturezas
sem ganho.

**Campos com o vocabulário do PRD-13 — `tratado_por`, `desfecho`, `tratado_em` —, sem o mixin
`EmAvaliacao`.** O mixin nomeia avaliação (`avaliado_por`, `parecer`, `decidido_em`), e aqui o
ato é tratamento. _Alternativa descartada:_ reusar o mixin e renomear na saída, que deixaria o
modelo falando um domínio e a API outro.

**O prazo vem da constante já existente `PRAZO_DE_AVALIACAO` (`fila.regra`), importada.** São os
mesmos 7 dias de `RN-01-49` e de `RN-13-14`, promessa única da plataforma (03 §9); duplicar a
constante convidaria à divergência.

**O protocolo é o identificador do registro.** É o que as quatro naturezas já fazem —
`SolicitacaoSaida(id, prazo)` —, e nenhum documento define formato de protocolo. Inventar
máscara seria criar regra fora do PRD.

**A situação reusa `SituacaoDaSolicitacao` (recebida, em avaliação, aceita, recusada).** O
PRD-13 §9 diz que o pedido de exclusão **é aceito** e respondido no desfecho, o que cabe nesse
vocabulário. _Alternativa descartada:_ vocabulário novo, que inventaria termo de domínio.

**O atraso é derivado, como no restante da fila** — `prazo < agora` e sem desfecho —, nunca
gravado.

**A duplicata é barrada na regra, por consulta.** Mesmo responsável, mesmo Guerreiro(a), mesmo
tipo, sem desfecho: 409 do domínio, no precedente das demais guardas do núcleo. _Alternativa
descartada:_ índice único parcial no banco, que devolveria erro sem a mensagem do domínio.

**A fila do Admin devolve o nick do responsável e o do Guerreiro(a), além dos identificadores.**
A gestão não tem rota que liste responsáveis, e sem o nick a tela mostraria UUID. O nick de
adulto já existe no núcleo.

**`GET /v1/entregas` ganha três campos na saída** — tipo de recurso, quantidade e o
identificador do lançamento —, em vez de rota nova. Sem eles a gestão não separa o exemplar
Alpha da camisa nem alcança a baixa; o custo continua fora da saída, no lançamento.

**As duas telas da App 03 seguem o padrão da pasta.** A fila entra em `filas/`, com lista e tela
de tratamento no molde de `AvaliacaoDeDados`; as entregas entram em `acervo/`, resolvendo nome
de tipo de recurso, de ponto de apoio e de persona por mapa montado na tela, como
`ListaDoAcervo` já faz.

## Risks / Trade-offs

- **A fila nasce alimentada só pela rota do responsável, sem tela da App 07 até a fatia 4 do
  PRD-13** → a rota é exercida por teste de ponta a ponta e a fila da gestão trata o que ela
  gravar; nenhuma das duas depende da App 07 para funcionar.
- **Desfecho de exclusão gravado sem a execução do pedido** → a spec fixa o limite em requisito
  próprio, com cenário que prova que nada é apagado por esse ato, para que a fatia 4 do PRD-13
  não encontre efeito já presumido.
- **Três campos novos na saída de `GET /v1/entregas`, lida também pelo Guerreiro(a)** → são
  identificador e quantidade, nunca valor; a proibição de moedas e reais segue no requisito
  modificado e no teste que já existe.
