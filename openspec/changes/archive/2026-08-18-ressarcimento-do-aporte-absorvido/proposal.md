## Why

Origem: **PRD-07 — Economia de recursos e livro-razão**, sexta fatia.

O aporte por absorção nasce **ressarcível, com situação em aberto** desde a segunda fatia, e até
hoje nada o encerra: o enum de situação declara `ressarcido` com o comentário de que é
"inalcançável nesta fatia", e todo Mestre ou Admin que sustentou atividade com o próprio bolso
está num estado terminal que não termina. Esta fatia é a que o alcança.

Ela fecha o **ciclo inteiro da absorção**: como ela nasce — assumida a partir de uma necessidade
publicada, declarando qual atende (`RF-07-28`) — e como ela termina — ressarcida, quando houver
receita destinada a isso, revertendo as moedas e preservando o selo público (`RF-07-22` a
`RF-07-25`). É o que o documento 04 §1 chama de reconhecer sem prometer: o ressarcimento não é
direito nem dívida da plataforma, é o que se faz quando alguém doa para esse fim.

Requisitos atendidos: `RF-07-22`, `RF-07-23`, `RF-07-24`, `RF-07-25`, `RF-07-28`.
Regras aplicadas: `RN-07-17`, `RN-07-18`, `RN-07-38`, `RN-07-39`.

## What Changes

**A receita destinada a ressarcir** (`RF-07-23`). O `Aporte` ganha **destinação** — `lastro` ou
`ressarcimento` —, atributo já previsto no PRD-07 §8. O aporte de destinação `ressarcimento`
credita o Poder Sustentador de quem doou, como qualquer outro, e **não vira lastro**: fica fora
do saldo de recurso e não confirma aula pendente de lastro (`RN-07-38`). É o que impede o mesmo
dinheiro de destravar uma aula e devolver a quem absorveu.

**A fila por antiguidade** (`RF-07-24`). Os aportes por absorção com situação **em aberto**,
do mais antigo ao mais novo, para o Admin decidir quais paga.

**O ressarcimento pago** (`RF-07-22`, `RF-07-25`). Entidade `Ressarcimento`, com o aporte
absorvido, o valor em reais, a **receita destinada de origem**, o Admin pagador, a data e o
**comprovante anexado** — exigido, sem o qual o registro é recusado. Pago, as **moedas
revertem** por lançamento de ajuste sobre o crédito original: o Poder Sustentador de quem
absorveu volta ao que era antes daquele aporte, e a **contagem de absorções não se move**
(`RN-07-18`) — são dois números que a quinta fatia já nasceu separando.

**Nenhum dado bancário entra na plataforma** (`RF-07-22`). A chave PIX chega ao Admin por
e-mail, fora daqui, e nenhum campo da API a aceita. O que fica é o comprovante da
transferência, anexo de acesso restrito à gestão.

**O teto da receita destinada** (`RN-07-17`). O ressarcimento declara qual receita destinada o
financia, e o núcleo recusa o pagamento que exceda o que aquela receita ainda tem em aberto —
decisão nova, tomada nesta change e gravada no documento-fonte antes de virar código.

**A absorção assumida a partir da necessidade publicada** (`RF-07-28`). O `Aporte` ganha a
**aula cuja necessidade atende**, atributo do PRD-07 §8 exclusivo da forma absorção: é como
quem cobre uma falta declara qual falta cobriu. A necessidade segue **derivada**, sem tabela a
referenciar.

**O valor em reais passa a ser exigido quando houve desembolso** (`RN-07-39`) — tipos de
natureza consumível, durável e financeira. É esse valor que o ressarcimento devolve, e hoje ele
é opcional em toda forma. Na natureza **serviço** ele fica **vazio**, e a absorção de serviço
nasce **não ressarcível** — decisão nova, tomada nesta change: quem absorve serviço dá tempo,
não dinheiro, e não há desembolso a devolver. Ela credita o Poder Sustentador e conta no selo
como qualquer outra. É o que resolve a tensão entre o `RN-07-39` — que manda a tabela de
referência fornecer o valor — e o `RN-07-24`, que veda converter moedas em reais.

Rotas, conforme o PRD-07 §9:

| Método | Rota                          | Autenticação    |
| ------ | ----------------------------- | --------------- |
| GET    | `/aportes/ressarciveis`       | Admin           |
| POST   | `/aportes/{id}/ressarcimento` | Admin           |
| GET    | `/meus-aportes/ressarciveis`  | Mestre ou Admin |

As rotas de registro existentes ganham campo, sem rota nova: `POST /aportes` aceita a
**destinação** e `POST /aportes/absorcao` aceita a **aula** cuja necessidade atende. Nenhuma das
três rotas novas é pública — comprovante e valor em reais nunca saem por rota sem persona.

## Capabilities

### New Capabilities

- `ressarcimento`: a devolução do aporte absorvido — a fila por antiguidade, o pagamento com
  comprovante contra a receita destinada que o financia, a reversão das moedas por ajuste e a
  situação que o provedor acompanha (`RF-07-22`, `RF-07-24`, `RF-07-25`, `RN-07-17`,
  `RN-07-18`).

### Modified Capabilities

- `aporte`: ganha a **destinação**, que separa o que vira lastro do que não vira (`RF-07-23`,
  `RN-07-38`); a **aula cuja necessidade atende**, na forma absorção (`RF-07-28`); e o **valor
  de origem exigido quando houve desembolso** (`RN-07-39`).
- `livro-razao`: o saldo derivado passa a **excluir o crédito de destinação ressarcimento**, que
  credita reconhecimento sem creditar estoque (`RN-07-38`); e o ajuste ganha a forma que reverte
  **moedas sem mexer em quantidade**, para que devolver dinheiro a quem absorveu não desfaça a
  chegada de um bem já consumido (`RF-07-25`).
- `poder-sustentador`: passa a **cair com o ressarcimento pago**, pela cadeia de ajuste que já
  deriva, enquanto a contagem de absorções **permanece** (`RN-07-18`).
- `necessidade-de-recurso`: a absorção que a atende passa a **declarar qual aula** cobre, sem
  mudar a derivação da necessidade (`RF-07-28`).

## Impact

- `backend/src/nucleo/aportes/` — `destinacao`, `aula_id` e a exigência de `valor_de_origem`;
  migração Alembic correspondente. O que fazer com os aportes já gravados é decisão do `design`.
- `backend/src/nucleo/livro_razao/` — a destinação herdada no lançamento e o filtro do saldo;
  o ajuste que carrega moedas com quantidade zero.
- `backend/src/nucleo/ressarcimentos/` — módulo novo.
- `backend/src/nucleo/poder_sustentador/` — nenhuma mudança de derivação: a reversão entra pela
  cadeia de ajuste que já é somada. Só testes que provem a queda.
- **Duas decisões novas de produto**, que seguem o fluxo do `CLAUDE.md` antes do código — cada
  uma gravada no **documento 04 §1**, movida para **decididos no documento 09** e aplicada ao
  **PRD-07**, tudo no mesmo PR:
  1. O **teto da receita destinada** é regra do núcleo, não juízo do Admin (`RN-07-17`).
  2. A **absorção de natureza serviço não é ressarcível** — abre exceção ao `RF-07-21`, que hoje
     manda toda absorção nascer ressarcível, e fecha a contradição entre o `RN-07-39` e o
     `RN-07-24`.
- LGPD: nenhum campo novo de dado pessoal de criança. O comprovante de ressarcimento entra na
  tabela do PRD-07 §11 como anexo restrito à gestão, no mesmo regime do comprovante do aporte.

## Fora do escopo

Reproduz o que o PRD-07 §3.2 já exclui, e o que pertence a fatias seguintes do mesmo PRD:

- **Patrimônio, ficha de vida e conferência de inventário** (`RF-07-11`, `RF-07-13`,
  `RF-07-20`, `RF-07-48`) — fatia seguinte.
- **Catálogo avulso, tabela de preços em pontos extras e troca** (`RF-07-33` a `RF-07-38`,
  `RF-07-42` a `RF-07-46`) — fatia seguinte.
- **Lastro do desafio extra** (`RF-07-15`, `RF-07-39` a `RF-07-41`) — a entidade `DesafioExtra`
  não existe no núcleo e nasce em PRD-09 ou PRD-14; a reserva de aula **ou desafio extra** do
  PRD-07 §8 espera o outro lado.
- **Empréstimo de bancada e reposição solidária** — o documento 05 adia os dois.
- **Interface de gestão de recursos** — pertence ao PRD-02 (App 03).
- **Efetividade do apoio ao Apoiador** — o ledger guarda o dado; o painel é do PRD-14.
- **Contabilidade fiscal e prestação de contas formal da pessoa jurídica.**
