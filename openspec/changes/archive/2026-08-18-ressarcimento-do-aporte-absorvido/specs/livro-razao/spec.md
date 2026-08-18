## ADDED Requirements

### Requirement: O ajuste reverte moedas sem mexer em quantidade

O núcleo SHALL admitir **lançamento de ajuste que reverta apenas as moedas** do lançamento
original, com **quantidade zero**. É a forma que o ressarcimento usa: o bem chegou e foi
consumido, e o que volta é o dinheiro a quem o adiantou — desfazer a quantidade faria o saldo de
recurso cair por um fato que não se desfez.

O ajuste de quantidade zero SHALL seguir todas as exigências que esta capacidade já faz de
qualquer ajuste: referenciar o lançamento original, guardar motivo e autor, e deixar o original
intacto. Ele SHALL compor o **Poder Sustentador** pela cadeia de ajuste que já é derivada, e NÃO
SHALL alterar o **saldo** daquele tipo de recurso naquele ponto de apoio. (`RF-07-25`,
`RF-07-19`, `RN-07-15`, `RN-07-18`, PRD-07 §§8, 12)

#### Scenario: Ajuste de moedas não move o saldo

- **WHEN** um ajuste de quantidade zero e moedas negativas é lançado sobre um crédito
- **THEN** o saldo daquele tipo naquele ponto de apoio permanece o mesmo, e o total em moedas
  ligado àquele crédito cai pelo valor do ajuste

#### Scenario: O ajuste de moedas segue as regras de todo ajuste

- **WHEN** um ajuste de quantidade zero é lançado
- **THEN** ele referencia o lançamento original, guarda motivo e autor, e o original permanece
  gravado sem alteração

## MODIFIED Requirements

### Requirement: O saldo é derivado por tipo de recurso e ponto de apoio

O núcleo SHALL manter o **saldo de cada tipo de recurso em cada ponto de apoio** como valor
**derivado dos lançamentos**, nunca como número editável. O saldo SHALL somar os créditos,
subtrair os débitos e aplicar os ajustes daquele par tipo/ponto de apoio, e recontar os
lançamentos SHALL devolver o mesmo número. Lançamento creditado a um ponto de apoio NÃO SHALL
compor o saldo de outro ponto de apoio.

O saldo SHALL **excluir o crédito de destinação ressarcimento**: a receita destinada a ressarcir
credita reconhecimento sem creditar estoque, e não lastreia atividade alguma. O lançamento SHALL
carregar a **destinação** que herda do aporte que o gerou, para que o saldo a leia sem depender
de quem o consulta.

O núcleo SHALL distinguir, sobre esse saldo, a **quantidade reservada** — comprometida por
reservas ainda no estado reservada — e a **quantidade disponível**, que é o saldo menos a
reservada. A reserva NÃO SHALL alterar o saldo derivado: só o lançamento o move, e o débito da
baixa é o que faz o saldo cair quando o recurso é de fato consumido. (`RF-07-07`, `RN-07-36`,
`RF-07-08`, `RF-07-09`, `RN-07-38`, PRD-07 §§8, 10, 12)

#### Scenario: Saldo soma os lançamentos do par tipo e ponto de apoio

- **WHEN** dois aportes do mesmo tipo entram no mesmo ponto de apoio, com quantidades 3 e 2
- **THEN** o saldo daquele tipo naquele ponto de apoio é 5

#### Scenario: Ponto de apoio não empresta saldo a outro

- **WHEN** um aporte de um tipo entra no ponto de apoio A e nenhum entra no ponto de apoio B
- **THEN** o saldo daquele tipo no ponto de apoio B é zero, e o do ponto de apoio A é o
  aportado

#### Scenario: Recontagem devolve o mesmo saldo

- **WHEN** o saldo de um par tipo/ponto de apoio é recalculado a partir dos lançamentos
- **THEN** o número devolvido é igual ao anterior, sem depender de estado guardado à parte

#### Scenario: Ajuste entra na conta do saldo

- **WHEN** um ajuste é lançado sobre um crédito de quantidade 3, corrigindo-o em -1
- **THEN** o saldo daquele tipo naquele ponto de apoio passa a 2

#### Scenario: Reserva reduz a disponível e não o saldo

- **WHEN** uma aula reserva 4 de um tipo cujo saldo no ponto de apoio é 10
- **THEN** o saldo segue 10 e a quantidade disponível é 6

#### Scenario: A baixa é o que faz o saldo cair

- **WHEN** a atividade realizada é lançada e a reserva de 4 vira débito
- **THEN** o saldo passa a 6 e a quantidade reservada volta a zero

#### Scenario: Crédito de destinação ressarcimento fica fora do saldo

- **WHEN** entra um aporte de destinação ressarcimento de quantidade 5 num tipo cujo saldo no
  ponto de apoio é 10
- **THEN** o saldo daquele tipo naquele ponto de apoio segue 10, e a quantidade disponível não
  muda
