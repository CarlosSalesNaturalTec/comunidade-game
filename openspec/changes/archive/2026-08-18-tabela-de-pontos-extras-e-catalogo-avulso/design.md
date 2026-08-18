## Context

O padrão de vigência já está consolidado em `openspec/specs/catalogo-de-tipos-de-recurso` e
implementado em `backend/src/nucleo/recursos/` (`TipoDeRecurso`, `ValorDeReferencia`): abrir
vigência nova encerra a anterior no dia de início, o passado permanece consultável e a leitura
por data devolve o que valia. Esta fatia **repete esse padrão** para uma segunda régua e
acrescenta uma entidade nova. O saldo por tipo e ponto de apoio já é derivado dos lançamentos em
`openspec/specs/livro-razao`, e o escopo por comunidade já está em
`openspec/specs/permissoes-e-escopo-de-comunidade`. Motivação: `proposal.md`. Requisitos: os
dois deltas em `specs/`.

## Goals / Non-Goals

**Goals:** a segunda régua do tipo de recurso e a entidade do item, com o lastro lido do saldo
já derivado.

**Non-Goals:** a troca, o débito de ponto extra e a baixa no livro-razão — oitava fatia. Nenhuma
rota pública nasce aqui.

## Decisions

**O preço em pontos extras mora em `backend/src/nucleo/recursos/`, ao lado do valor em moedas.**
`PrecoDeReferencia` é irmã de `ValorDeReferencia`: mesma chave para `TipoDeRecurso`, mesma
mecânica de vigência, mesma autoria. Guardar as duas juntas é o que torna visível, no código,
que são réguas independentes sobre a mesma entidade — a leitura de uma nunca toca a outra.
_Descartado:_ módulo próprio para o preço, que separaria o que o PRD-07 §8 mantém unido.

**O item nasce em `backend/src/nucleo/catalogo_avulso/`.** É entidade nova, com ciclo próprio
(cadastro, homologação, ativação, retirada) e consumidora de três módulos existentes — não cabe
em nenhum deles.

**Preço inteiro, sem casas decimais.** Ponto extra é contado em unidades no motor de pontuação
já implementado (`openspec/specs/ponto-extra`); o piso de 20 é inteiro. A moeda tem duas casas
por `RN-07-04`, o ponto extra não tem nenhuma — é a diferença que impede a conversão silenciosa
entre as réguas (`RN-07-24`).

**O lastro é lido, nunca reservado.** Ativar item **não** cria `Reserva` nem lançamento: compara
o estoque declarado com a quantidade disponível do tipo no ponto de apoio do item e grava a
marca de ativo. A reserva do PRD-07 é da aula; o item de catálogo não compromete saldo entre
encontros por `RN-07-27`. Consequência aceita: dois itens do mesmo tipo e ponto de apoio podem
estar ativos somando mais que o saldo — a troca reverifica no ato (`RF-07-37`, oitava fatia).
_Descartado:_ reservar o estoque na ativação, que contraria `RN-07-27` diretamente.

**Item sem lastro é gravado inativo, não recusado.** `RF-07-34` diz que o item só *fica ativo*
com lastro, e `RF-09-101` recusa *publicar*, não cadastrar. Espelha a aula, que nasce pendente
de lastro em vez de ser recusada. A resposta diz a quantidade que falta, como o agendamento já
faz. _Descartado:_ recusar o cadastro com 422, que perderia o item cadastrado à espera do aporte
e impediria a necessidade de recurso de nascer dele no futuro.

**As rotas seguem o padrão já em uso** — recurso no plural, ato como sub-recurso:

| Método | Rota                                        | Persona                      |
| ------ | ------------------------------------------- | ---------------------------- |
| POST   | `/tipos-de-recurso/{id}/precos-de-referencia` | Admin                      |
| GET    | `/tipos-de-recurso/{id}/precos-de-referencia` | Admin                      |
| POST   | `/catalogo-avulso`                          | Mestre ou Apoiador           |
| GET    | `/catalogo-avulso`                          | persona em sessão, por comunidade |
| POST   | `/catalogo-avulso/{id}/homologacao`         | Admin                        |
| POST   | `/catalogo-avulso/{id}/ativacao`            | Admin ou Mestre vinculado    |
| PUT    | `/catalogo-avulso/{id}/estoque`             | Admin ou Mestre vinculado    |
| DELETE | `/catalogo-avulso/{id}`                     | Admin ou Mestre vinculado    |

O `DELETE` é a **retirada** do `RF-09-102`: deixa o item inativo e preserva o registro, como a
revogação de consentimento já faz. Nada é apagado.

**A homologação e a recusa ficam no mesmo ato.** `POST .../homologacao` recebe a decisão e o
motivo; item recusado guarda o motivo e não volta a ser homologável. Espelha a homologação do
aporte do pré-cadastro, já implementada em `openspec/specs/aporte`.

## Risks / Trade-offs

- **Item ativo sem lastro corrente**, depois de uma baixa que consumiu o saldo → a troca
  reverifica o lastro no ato (`RF-07-37`); nesta fatia a marca de ativo é a do momento em que foi
  gravada.
- **Preço de referência ausente deixa o item inativo** e o motivo pode passar despercebido → a
  resposta do cadastro diz explicitamente que falta o preço, não apenas que o item está inativo.
- **Duas réguas sobre o mesmo tipo convidam à conversão** em quem ler o código depois → o delta
  de `catalogo-de-tipos-de-recurso` tem cenário que proíbe a resposta trazer equivalência, e a
  ausência de casas decimais no ponto extra torna a conversão impossível sem código explícito.

## Migration Plan

Uma migração Alembic com as duas tabelas novas — `preco_de_referencia` e `item_de_catalogo_avulso`
— sem alterar tabela existente. Nada a preencher: não há item nem preço anterior. A reversão
derruba as duas tabelas.
