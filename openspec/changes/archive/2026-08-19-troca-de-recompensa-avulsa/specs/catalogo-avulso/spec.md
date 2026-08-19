## MODIFIED Requirements

### Requirement: O estoque é alterado e o item é retirado do catálogo, com autoria

Alterar o estoque de um item e **retirar** o item do catálogo SHALL exigir persona **Admin** ou
**Mestre vinculado à comunidade** do item; persona de qualquer outro papel SHALL receber **403**.
A retirada SHALL deixar o item **inativo** e NEVER SHALL apagar o item nem o seu histórico.
Estoque alterado para quantidade maior que o lastro disponível SHALL deixar o item **inativo**,
e a resposta SHALL dizer a quantidade que falta. Toda alteração SHALL gravar autoria, data e
hora com fuso.

Além desse caminho de gestão, o estoque SHALL decrescer **uma unidade por troca entregue**, sem
persona alterando-o e sem passar pela verificação de papel acima — o decremento é parte da
operação única da troca. Item que chega a **estoque zero** por troca NÃO SHALL ser retirado nem
marcado inativo por isso: ele permanece cadastrado e ativo, e deixa de ser trocável pela recusa
por estoque, para que o Mestre reponha o estoque sem recadastrar o item. (`RF-07-33`,
`RF-09-102`, `RF-07-34`, `RF-07-36`, `RF-07-37`, `RF-01-16`, `RF-01-27`)

#### Scenario: Mestre altera o estoque do item

- **WHEN** um Mestre vinculado à comunidade altera o estoque de um item para quantidade coberta
  pelo lastro
- **THEN** o núcleo grava o estoque novo com autor, data e hora com fuso, e o item permanece
  ativo

#### Scenario: Estoque acima do lastro desativa o item

- **WHEN** um Mestre altera o estoque de um item ativo para quantidade maior que o saldo
  disponível do tipo no ponto de apoio do item
- **THEN** o núcleo grava o estoque novo, deixa o item inativo e diz a quantidade que falta

#### Scenario: Mestre retira o item do catálogo

- **WHEN** um Mestre vinculado à comunidade retira um item do catálogo
- **THEN** o núcleo deixa o item inativo, preservando o registro, com autor, data e hora com fuso

#### Scenario: Apoiador não altera item já cadastrado

- **WHEN** um Apoiador em sessão tenta alterar o estoque de um item do catálogo
- **THEN** o núcleo responde 403 e o item permanece como estava

#### Scenario: A troca decrementa o estoque em uma unidade

- **WHEN** uma troca de um item de estoque 5 é entregue
- **THEN** o estoque do item passa a 4, sem alteração de gestão e sem mudar a marca de ativo

#### Scenario: Estoque zerado por troca não retira o item

- **WHEN** a última unidade em estoque de um item ativo é trocada
- **THEN** o item permanece cadastrado e ativo com estoque zero, e a próxima troca é recusada
  por falta de estoque
