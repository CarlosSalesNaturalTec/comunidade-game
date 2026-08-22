## Context

Ver `proposal.md` — Why. `PontoDeApoio.ativo` já existe e nasce verdadeiro; o próprio
`pontos_de_apoio/modelo.py` registra em comentário que nenhuma operação o muda porque a
desativação era pendência do documento 09. O livro-razão já tem lançamento imutável com
natureza crédito, débito e ajuste, e saldo derivado por par tipo de recurso e ponto de apoio.
A App 03 já tem o módulo `pontos-de-apoio`.

## Goals / Non-Goals

**Goals:**

- Fechar a pendência com as três respostas do fundador: quem desativa, o que trava e para onde
  vai o saldo.
- Tirar o espaço inativo da escolha do agendamento sem mexer em aula passada.

**Non-Goals:**

- Conferência de inventário (`RF-07-20`), que segue pendente.
- Qualquer forma de apagar ponto de apoio: desativar não é excluir.

## Decisions

**A transferência é par de lançamentos, não ajuste.** `ajuste` corrige erro e referencia o
lançamento original; transferir move recurso que existe e está certo. Um débito na origem e um
crédito no destino, gravados na mesma operação e referenciando-se, mantêm o saldo derivado
correto nos dois espaços sem inventar natureza nova no livro-razão. Alternativa descartada:
natureza `transferencia`, que obrigaria toda apuração de saldo já escrita a conhecer um quarto
caso.

**Bloquear a desativação, em vez de cascatear.** Aula futura e saldo remanescente **impedem** a
desativação, e a recusa diz o que está prendendo. Cancelar aulas ou mover saldo por conta
própria seria a plataforma decidindo remanejamento de turma e de acervo — decisão de operação,
que é do Admin. Alternativa descartada: desativar cancelando as aulas em cascata.

**Aula futura cobre as reservas.** Reserva herda a aula que a criou, então não existe reserva
viva sem aula futura que a sustente: conferir aula futura já basta, e conferir reserva
separadamente seria a mesma pergunta feita duas vezes.

**O saldo conferido é o derivado, não uma coluna.** A conferência de "ainda há saldo" usa a
mesma apuração que `livro-razao` já expõe por par tipo de recurso e ponto de apoio. Nenhum
total materializado nasce aqui.

**A desativação é rota própria, não um `PUT` do cadastro.** `POST
/v1/pontos-de-apoio/{id}/desativacao` e a de reativação, cada uma exigindo motivo. Passar
`ativo` no corpo do cadastro deixaria a mudança de estado indistinguível de uma correção de
nome na trilha de auditoria.

## Risks / Trade-offs

**Um ponto de apoio pode ficar preso, impossível de desativar** — aulas futuras que ninguém
cancela, ou saldo sem destino porque a comunidade não tem outro ponto de apoio. Mitigação: a
recusa nomeia exatamente o que prende, e o Admin tem as duas saídas na mão — cancelar a aula é
operação que já existe, e a transferência nasce nesta fatia. A fatia não cria força bruta para
contornar.

**A transferência entre comunidades diferentes não é vedada** aqui, e nem o PRD a veda: o
lançamento carrega o ponto de apoio, e o ponto carrega a comunidade. Mitigação: fica registrada
como observação, não como regra inventada — se o fundador quiser vedar, é decisão nova, e
decisão nova não nasce em change.

## Migration Plan

Aditiva e mínima: `ponto_de_apoio` ganha **motivo** e **autoria da última mudança de estado**,
para que desativar e reativar entrem na trilha de auditoria com o porquê. A coluna `ativo` já
existe e nenhum registro muda de valor. O par de lançamentos da transferência ganha a
referência mútua. Rollback é a migração inversa; nenhum lançamento gravado é tocado, porque
lançamento é somente inserção.
