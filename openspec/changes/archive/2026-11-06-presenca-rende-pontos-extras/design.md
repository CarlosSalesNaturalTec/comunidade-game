# Design

## Context

- A presença nasce em `aulas/regra.registrar_presenca`, idempotente por (aula, Guerreiro(a)),
  e é anulada em `aulas/regra.anular_presenca`, que só marca `anulada_em` (spec
  `aula-e-presenca`).
- O ponto extra vive em `ponto_extra/` (spec `ponto-extra`): `creditar_ponto_extra` e
  `debitar_ponto_extra`, este só no saldo. A redução do acumulado é recusada em duas camadas —
  um _listener_ `before_update` do ORM e o gatilho `trg_ponto_extra_acumulado_so_cresce` no
  banco.
- O piso de 20 está em `recursos/regra.PISO_DE_PONTOS_EXTRAS` e no `CHECK`
  `ck_preco_de_referencia_piso_minimo` (spec `catalogo-de-tipos-de-recurso`).

## Goals / Non-Goals

**Goals:** creditar e estornar na mesma transação da presença; deixar o estorno da presença como
a única porta de redução do acumulado, nas duas camadas; subir o piso sem reescrever histórico.

**Non-Goals:** mudar a App 01 ou a App 03; rota nova; crédito retroativo.

## Decisions

1. **A presença guarda o que creditou.** Nasce em `presenca` a coluna
   `pontos_extras_creditados` (inteiro, não nulo, padrão 0). A presença nova grava 5; a
   migração deixa as existentes em 0. A anulação estorna **o valor da coluna**, não a
   constante: é o que torna a presença anterior à regra inerte sem comparar datas (`RN-01-65`)
   e mantém o estorno certo se o valor da fonte mudar um dia. O valor 5 vive numa constante de
   `ponto_extra/regra.py`, ao lado dos adicionais de mérito.
   — _Descartado:_ comparar `registrado_em` com a data de corte — data fixa no código e frágil
   no reenvio fora de linha.
2. **O corte é o registro no núcleo**, não o `momento_do_fato`: a presença que o App 01 envia
   depois da entrega, de uma aula anterior a ela, credita. O documento 09 fala em presença
   "registrada".
3. **O estorno é uma função própria**, `estornar_ponto_extra_da_presenca`, que tira o valor do
   acumulado e `min(valor, saldo)` do saldo. `debitar_ponto_extra` segue intacto e segue
   recusando saldo insuficiente — a troca não herda o piso em zero.
4. **A porta do acumulado é um marcador local à transação.** A função do estorno executa
   `SET LOCAL cg.estorno_de_presenca = 'on'` antes de gravar; o gatilho só admite
   `NEW.acumulado < OLD.acumulado` quando `current_setting('cg.estorno_de_presenca', true) =
   'on'`, e o _listener_ do ORM lê o mesmo marcador em `connection.info`. O `SET LOCAL` morre
   no fim da transação, então nenhuma outra escrita da mesma conexão herda a porta. O `DELETE`
   segue recusado sempre.
   — _Descartado:_ tirar a trava do banco e confiar só na regra — a spec exige a recusa em
   qualquer via, inclusive fora do ORM.
5. **Piso e preços na mesma migração, nesta ordem:** (a) para cada vigência aberta com preço
   menor que 25, gravar `vigencia_fim` = data da migração e inserir vigência de 25 com início
   na mesma data, `autor_id` da vigência substituída e `papel_do_autor = "migracao"`; (b)
   trocar o `CHECK` por `preco_em_pontos_extras >= 25` com `NOT VALID`, porque as vigências
   encerradas de 20 a 24 ficam no histórico. Feito (a) antes de (b), nenhuma linha abaixo de
   25 volta a ser atualizada: só a vigência aberta recebe `vigencia_fim`. O modelo declara o
   `CHECK` de 25, que vale inteiro no banco criado do zero (testes).
   — _Descartado:_ atualizar o preço da vigência aberta no lugar — apagaria o preço que a
   troca antiga cobrou (`RF-07-46`).
6. **Sem livro-razão:** ponto extra não é custo nem aporte; nada a lançar.

## Risks / Trade-offs

- [`autor_id` da vigência criada pela migração aponta para quem registrou a anterior] →
  `papel_do_autor = "migracao"` distingue a linha na auditoria; não há persona de sistema no
  núcleo.
- [Anulação em massa derruba o acumulado lido pela vitrine e pelo App 04] → é o efeito
  decidido; só o Admin anula, com motivo gravado.
- [`NOT VALID` deixa o banco com linhas que o `CHECK` novo não validou] → são só vigências
  encerradas, que nenhuma rota altera.
