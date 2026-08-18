## Context

O livro-razão já está inteiro em `src/nucleo/livro_razao/` — `Lancamento` somente inserção, com
_listeners_ do ORM e _trigger_ no banco recusando `UPDATE` e `DELETE` —, e o saldo derivado está
na spec `livro-razao`. O padrão de módulo do núcleo é `modelo.py` / `regra.py` / `rotas.py`, com
o roteador incluído por `incluir_roteador_de_dados`, que já aplica a chave de aplicação e a cota
de leitura a toda rota sob `/v1`.

Dois vínculos existem hoje e um não existe:

```text
Aporte.lancamento_id ────────────▶ Lancamento (crédito)   ✓
Lancamento.lancamento_original_id ▶ Lancamento (ajuste)   ✓
Lancamento ──────────────────────▶ Aula                   ✗
```

A `Reserva` também não guarda o lançamento que a baixa emitiu, então não há rota alternativa: o
débito, hoje, não sabe de onde veio.

## Goals / Non-Goals

**Goals:**

- Derivar o Poder Sustentador e o movimentado dos lançamentos, de forma recontável.
- Fechar o vínculo do débito com a aula, sem ferir a imutabilidade do lançamento.
- Deixar o estorno do ressarcimento — fatia seguinte — entrar sem reescrever nenhuma derivação.

**Non-Goals:**

- Cache das rotas públicas. A §10 do PRD-07 diz que a consulta **é cacheável**; isso é
  propriedade da resposta, não trabalho desta fatia. O desenho apenas não impede o cache.
- Total consolidado guardado em tabela. O número é sempre derivado (`RN-07-15`).
- Qualquer escrita. As quatro rotas são de leitura.

## Decisions

### 1. A derivação segue a cadeia aporte → crédito → ajuste, sem coluna nova no lançamento

O Poder Sustentador de um provedor é a soma das moedas dos créditos ligados aos aportes dele,
mais a dos ajustes que referenciam esses créditos:

```text
Aporte(provedor=P) ──lancamento_id──▶ crédito ◀──lancamento_original_id── ajuste
                                        └──────────── soma ────────────────┘
```

Dois `JOIN` sobre o que já existe. **Alternativa descartada:** desnormalizar `provedor_id` em
`Lancamento` — mais rápido de somar, mas duplica um vínculo de que o `Aporte` já é dono, e cria
uma segunda verdade sobre quem proveu o quê.

É esta forma que faz o ressarcimento da fatia seguinte funcionar de graça: o estorno entra como
mais um lançamento na cadeia daquele crédito e a soma cai sozinha, sem tocar nesta derivação.

### 2. A contagem de absorções não passa perto do livro-razão

`COUNT` dos aportes do provedor com `forma = absorcao`. Lê `Aporte`, e só. É o que garante o
critério de aceite do PRD-07 §12 — o ressarcimento reverte as moedas e o selo continua contando
aquela absorção — sem nenhuma regra de exclusão a escrever: os dois números simplesmente não
compartilham fonte.

### 3. `aula_id` em `Lancamento`, anulável e indexado

Coluna anulável, porque crédito e ajuste não declaram aula e porque as fatias seguintes trarão
débitos que também não têm uma — a baixa da troca do catálogo avulso e a baixa definitiva de
recompensa entregue. Índice em `aula_id`, que é por onde `/prestacao-de-contas/aulas` agrupa.

A gravação entra em `livro_razao.regra.lancar_debito` e em
`reservas.regra.consumir_reservas_da_aula`, que já tem a aula em mãos. Nenhuma outra chamada
muda.

### 4. Nenhum preenchimento retroativo dos débitos já gravados

`Lancamento` recusa `UPDATE` no ORM **e** no banco, por _trigger_. Preencher `aula_id` em débito
já gravado exigiria derrubar essa proteção — exatamente o que `RN-07-15` proíbe. A migração
apenas cria a coluna.

Consequência assumida: débito lançado antes desta change fica sem aula e **não compõe** o consumo
por aula. O total movimentado de `/prestacao-de-contas` não é afetado, porque não depende da
aula. Nenhuma tentativa de adivinhar o vínculo por tipo, ponto de apoio e quantidade: a
correspondência não é unívoca entre aulas, e um palpite gravado no livro-razão é pior que uma
lacuna declarada.

### 5. A agregação acontece no banco

`GROUP BY` e `SUM` em SQL, não somatório em Python sobre a coleção de lançamentos. O livro-razão
cresce a cada aula de cada comunidade, e as três rotas públicas não podem carregá-lo inteiro para
somar. A recontabilidade que as specs exigem é da fórmula, não do caminho.

### 6. Dois módulos novos, sem `modelo.py`

`src/nucleo/poder_sustentador/` e `src/nucleo/prestacao_de_contas/`, cada um com `regra.py` e
`rotas.py`. Nenhum dos dois cria tabela: não há `modelo.py`. Os roteadores entram por
`incluir_roteador_de_dados`, que já lhes dá a chave e a cota.

`GET /meus-aportes` mora em `poder_sustentador/rotas.py`, e não em `aportes/`, porque devolve os
aportes **e** o Poder Sustentador do Apoiador em sessão — é leitura desta capacidade sobre o dado
daquela.

### 7. As rotas públicas ficam fora do prefixo `/vitrine`

A §9 do PRD-07 escreve `/prestacao-de-contas` e `/provedores/{id}/poder-sustentador` sem prefixo,
e `/vitrine/necessidades` com ele, na mesma tabela. Seguimos a §9 à letra. A ausência de
`exigir_persona` na rota é o que a torna pública; o prefixo `/vitrine` não é o mecanismo, é uma
convenção da vitrine.

### 8. O 404 do provedor é indistinto

`GET /provedores/{id}/poder-sustentador` responde **404** igual para identificador inexistente e
para persona de Guerreiro(a) ou de responsável, no mesmo padrão que a capacidade
`leitura-publica-da-vitrine` já usa no perfil por nick. Adulto cadastrado que nunca aportou
responde **200**, com zero em ambos os números — é o card público de um Mestre que ainda não
absorveu nada.

## Risks / Trade-offs

- **Débitos anteriores sem aula** (Decisão 4). Se já houver débito gravado em produção, o consumo
  por aula começa incompleto, e a lacuna não é recuperável sem ferir a imutabilidade. A migração
  não tem como corrigir isso; se o volume importar, é decisão do fundador, não da change.
- **Duas leituras da mesma pergunta.** `/prestacao-de-contas` devolve o movimentado por provedor
  e `/provedores/{id}/poder-sustentador` devolve o de um provedor. É a §9 do PRD que pede as
  duas; ambas usam a mesma função de `regra.py`, para não divergirem.
- **Custo da agregação sem cache.** Sem índice de apoio, o `GROUP BY` por provedor percorre os
  créditos todos. O índice de `aula_id` cobre a rota das aulas; a de provedor apoia-se no índice
  de chave estrangeira do `Aporte`. Se o volume do Ciclo 01 mostrar que não basta, cache é o
  próximo passo — e a §10 do PRD já o autoriza.
