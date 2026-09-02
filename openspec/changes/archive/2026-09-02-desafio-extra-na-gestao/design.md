## Context

O que já existe e esta fatia só usa: `DesafioExtra` e `ConclusaoDeDesafioExtra`
(`nucleo/desafios_extras/`), com `lastro_provido`, `motivo_de_lastro_faltante`,
`conferir_publicacao_com_lastro`, `conferir_editavel` e `quantidade_restante` já escritos e
testados pela fatia 1 do PRD-14 — a guarda de publicação foi deixada lá **para esta fatia
chamar**. Do PRD-07 já existem `reservas.regra.disponivel_de`, `quantidade_reservada` e
`_bloquear_par` (`SELECT ... FOR UPDATE` sobre o par tipo de recurso e ponto de apoio), e a
matriz de permissões concede ao Admin `Operacao.tudo`. Na App 03, a área **Filas** já tem filtro
por natureza, `ListaDeFilas` e o molde de tela de avaliação com parecer obrigatório.

A restrição que mais aperta o desenho: a `Reserva` nasceu presa à aula (`aula_id` **NOT NULL**,
FK para `aula`), e o PRD-07 §8 descreve a entidade como "aula **ou desafio extra**". É a única
mudança estrutural da fatia.

## Goals / Non-Goals

**Goals:**

- Tirar o `DesafioExtra` de `em_validacao_do_mestre` pela ponta do Admin: fila, aprovação,
  recusa, publicação e encerramento (`RF-02-27`, `RF-02-28`, `RN-02-10`, `RN-02-11`,
  `RF-02-106`).
- Fazer a publicação comprometer a recompensa e o encerramento devolvê-la (`RF-07-39`,
  `RF-07-40`), sem afrouxar a regra de que reserva não sai por prazo.

**Non-Goals:**

- A validação do Mestre da trilha (fatia 15 do PRD-09) e o ato de registrar a conclusão — com a
  baixa da reserva e o crédito dos pontos extras — que o cronograma deixa para uma fatia do
  PRD-09 ainda sem número.
- Qualquer mudança na App 08 ou nas rotas do proponente: a leitura do Apoiador já devolve
  situação, motivo da recusa e quantidade restante.
- Trilha de auditoria desta aplicação, adiada ao Ciclo 02.

## Decisions

1. **O encerramento é fato gravado no desafio, não um quinto estado.** `DesafioExtra` ganha
   `encerrado_em` e `admin_encerrador_id`; `SituacaoDoDesafioExtra` continua com os quatro
   valores que `RF-14-35` enumera e que a App 08 já apresenta. Alternativa descartada: um valor
   `encerrado` no enum — mudaria `RF-14-35` e a tela do Apoiador, já entregues, para registrar
   um fato que uma data registra melhor.

2. **`Reserva.aula_id` passa a opcional e nasce `desafio_extra_id`, com XOR no banco.**
   `CheckConstraint` exigindo exatamente um dos dois preenchido, mais índice em
   `desafio_extra_id`. Alternativa descartada: tabela própria de reserva do desafio — duplicaria
   `disponivel_de` e `quantidade_reservada`, e o PRD-07 §8 descreve **uma** entidade.

3. **Aprovar e reservar é um ato só, sob o bloqueio que já existe.** `aprovar_desafio_extra`
   chama `_bloquear_par` antes de conferir a disponível, na mesma transação em que grava
   `publicado` e a `Reserva` — o mesmo caminho do agendamento concorrente. Sem isso duas
   aprovações simultâneas reservariam o mesmo saldo.

4. **A ordem das guardas da aprovação é situação → natureza → lastro → disponível**, para que o
   erro devolvido seja o que o Admin precisa resolver primeiro: 409 de situação, 422 do tipo
   durável (`RN-07-07`), 422 do lastro faltante com o texto que
   `motivo_de_lastro_faltante` já produz, 422 de disponível insuficiente.

5. **A quantidade reservada é `quantidade_disponivel` do desafio**, convertida em `Decimal` — a
   recompensa é aquela quantidade do `tipo_de_recurso` no `ponto_de_apoio` da proposta, o mesmo
   par que `lastro_provido` já consulta no custeio por saldo.

6. **Uma rota por ato, no molde da fila que já existe**, e as duas leituras separadas em vez de
   um filtro por situação, porque a §9 do PRD-02 declara `/pendentes` e a lista dos publicados
   serve a outra tela:
   - `GET /v1/desafios-extras/pendentes` — Admin, os `em_aprovacao_do_admin`;
   - `POST /v1/desafios-extras/{id}/aprovacao` — Admin, entrada `{situacao, motivo}`, no mesmo
     formato de `POST /v1/solicitacoes-de-participacao/{id}/avaliacao`;
   - `GET /v1/desafios-extras/publicados` — Admin, com a quantidade restante;
   - `POST /v1/desafios-extras/{id}/encerramento` — Admin.
     As quatro sob `Operacao.tudo`, como as demais rotas de gestão.

7. **A App 03 ganha uma sexta natureza na área Filas, não uma área nova** — a própria spec da
   gestão proíbe abrir área separada para natureza de fila. `TelaDeFilas` ganha a natureza, e
   `AvaliacaoDoDesafioExtra.tsx` traz as duas listas (pendentes e publicados) e as três saídas.
   Nenhuma mudança em `App.tsx`.

8. **A guarda de conclusão em desafio encerrado fica em
   `registrar_conclusao_de_desafio_extra`**, ao lado da guarda de "só publicado recebe
   conclusão" que já está lá — é consequência direta de `RF-07-40`: liberada a reserva, não há
   recompensa a entregar.

## Risks / Trade-offs

- **A fila nasce vazia em produção** enquanto a fatia 15 do PRD-09 não entregar a validação do
  Mestre. É a sequência que o cronograma escolheu; os testes montam o estado
  `em_aprovacao_do_admin` direto pelo ORM, sem antecipar rota do PRD-09.
- **Migração sobre coluna existente**: `aula_id` deixa de ser `NOT NULL`. Nenhuma linha
  existente muda de valor, e o `CheckConstraint` de XOR mantém a garantia que o `NOT NULL`
  dava às reservas de aula.
- **Recompensa durável recusada na publicação, não na proposta**: quem propôs pela App 08 só
  descobre a recusa no desfecho do Admin. Alertar antes exigiria mudar a rota da proposta, que
  é do PRD-14 e está fora desta fatia; o motivo da recusa fica registrado e a App 08 já o lê.
- **Encerramento sem volta**: não há desencerramento. A correção é proposta nova, como já vale
  para o desafio publicado (`RF-14-38`).
