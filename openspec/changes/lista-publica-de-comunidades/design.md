## Context

A rota `GET /comunidades` é a última do PRD-08 §9 que não existe. O terreno em volta dela já
está construído: `GET /comunidades/{id}` e `GET /comunidades/{id}/series` são públicas,
`territorio_piso_de_coletores_distintos` já está na `Configuracao`, e `paginar_serie_publica` já
aplica o piso sobre o resultado inteiro antes de paginar. Esta fatia reusa as três coisas.

O que ela traz de novo é a **apuração dos quatro indicadores**, que nunca teve código porque
nunca teve definição. As três decisões que a destravaram estão na proposal e já percorreram o
fluxo até o PRD.

## Goals / Non-Goals

**Goals**

- Listar as comunidades com os quatro indicadores do documento 02 §1, em rota pública.
- Aplicar o piso de coletores **suprimindo o indicador, nunca a comunidade**.
- Deixar escrito, na mesma capacidade, por que o piso trata a lista de um jeito e o recorte da
  série de outro.

**Non-Goals**

- Não cria indicador novo, ordenação por indicador nem filtro por faixa de valor.
- Não toca na série pública nem na exportação: são outras rotas, já entregues.
- Não introduz calendário de ciclo — a decisão foi explicitamente evitá-lo.

## Decisions

### 1. O piso suprime o indicador, e não a linha — ao contrário da série pública

A mesma capacidade passa a ter dois tratamentos para "abaixo do piso", e a diferença é
deliberada:

```text
  SÉRIE PÚBLICA                          LISTA DE COMUNIDADES
  recorte = bairro                       recorte = comunidade
  ┌──────────────────────┐               ┌──────────────────────┐
  │ bairro abaixo do piso│               │ comunidade abaixo    │
  └──────────┬───────────┘               └──────────┬───────────┘
             │ soma ao nível acima                  │ não há nível acima
             ▼                                      ▼
  ┌──────────────────────┐               ┌──────────────────────┐
  │ comunidade           │               │ fica na lista,       │
  │ ainda abaixo? some   │               │ indicadores nulos    │
  └──────────────────────┘               └──────────────────────┘
```

A regra do documento 02 §1 é "soma-se ao nível acima até alcançar o piso". Na série há para
onde subir; na lista, a comunidade **é** o topo. Suprimir a comunidade inteira apagaria do mapa
justamente quem está começando — e o painel público existe para mostrar que ela começou. Some o
número, que é o que poderia isolar um coletor; fica o nome, que não isola ninguém.

O risco que o piso protege continua coberto: com dois coletores, "registros válidos = 47"
poderia ser lido contra um deles. Nome e localização da comunidade não têm essa propriedade.

### 2. Continuidade se apura sobre períodos vencidos, nunca sobre períodos futuros

A fração é `períodos com ao menos um registro válido ÷ períodos de cadência vencidos`. O
denominador conta só o que **já venceu** entre `aberta_em` e o instante da consulta — série
recém-aberta, sem nenhum período vencido, teria denominador zero.

Essa série **fica fora da média**, em vez de entrar como zero. Entrar como zero puniria a
comunidade por ter aberto uma série ontem, que é exatamente o comportamento que o projeto quer
premiar. É a mesma escolha que a auditoria já faz ao apurar série ativa "no instante da
amostra": o indicador olha o que aconteceu, não o que ainda não teve chance de acontecer.

Comunidade em que **nenhuma** série tem período vencido devolve continuidade **nula**, não
zero — não há sobre o que tirar média, e nulo é o valor que diz isso sem mentir.

### 3. O período do registro se resolve pela data da medição, não pela do registro

`RF-08-15` e `RN-01-…` já mandam usar a **hora da medição** em toda regra dependente de tempo, e
`paginar_serie_publica` já o faz. A continuidade segue a mesma régua: o registro feito às 15h de
uma medição das 14h de ontem conta para o período de **ontem**.

### 4. A cadência vem da série, não do desafio

`SerieDeColeta.cadencia` é herdada do desafio na abertura, precisamente para que a apuração não
dependa de o desafio permanecer inalterado. A continuidade lê a cadência da **série**, como o
modelo já previu.

### 5. O piso é apurado antes da paginação

Mesma decisão que `paginar_serie_publica` tomou, pela mesma razão: se o piso recaísse sobre a
página, a mesma comunidade sairia com indicadores numa página e sem eles noutra. A apuração
roda sobre o conjunto inteiro, e o cursor recorta o resultado já decidido.

### 6. A contagem de coletores distintos que decide o piso não sai na resposta

Ela é insumo da decisão, não indicador. Devolvê-la seria devolver, para a comunidade abaixo do
piso, exatamente o número que o piso existe para esconder — "2 coletores" é mais revelador que
qualquer um dos quatro.

## Risks / Trade-offs

- **Custo da continuidade.** Ela exige, por série, a contagem de períodos distintos com registro
  válido. No volume do Ciclo 01 — uma comunidade, dezenas de séries — a consulta agregada
  resolve sem índice novo. Se o número de séries crescer, o caminho é materializar a apuração
  por série, não mudar a definição.
- **"Ao fim do ciclo" no nome de um indicador apurado agora.** O nome ficou como está, por
  decisão: renomear era opção descartada. A resposta declara o rótulo do ciclo para que o leitor
  saiba a que período os números se referem, e o documento 02 §1 registra a régua.
- **Dois tratamentos do piso na mesma capacidade.** É o principal risco de leitura futura, e a
  mitigação é textual: a spec põe os dois lado a lado, com um cenário que afirma que o recorte
  da série **continua** sendo suprimido.

### 7. A apuração dos quatro indicadores vive em `coletas/regra.py`, não em `comunidades/regra.py`

Desvio de implementação em relação às `tasks`: `coletas/regra.py` já importa
`comunidades/regra.py` (para `resolver_vinculo_na_data`), e a apuração dos indicadores precisa
de `apurar_estado_da_serie` e dos períodos de cadência, que vivem em `coletas`. Colocar as
funções em `comunidades/regra.py` fecharia um ciclo de import entre os dois módulos, que o
Python não resolve.

A solução segue o padrão que o próprio módulo já usa para `paginar_serie_publica` e
`exportar_serie_do_territorio`: a apuração pública que depende de `coletas` interno vive em
`coletas/regra.py`, tomando `ComunidadeVirtual` só como parâmetro (de `comunidades.modelo`, sem
ciclo), e `comunidades/rotas.py` importa de lá — como já importa `PontoDaSeriePublicaSaida` e as
demais. Nenhum requisito muda; só o arquivo em que a função mora.

## Migration Plan

Nenhuma migração de banco. A change é somente leitura: não cria tabela, não altera coluna e não
escreve. Nenhum dado precisa ser retroagido — os indicadores são derivados do que já está
gravado.

## Open Questions

Nenhuma. As três que existiam foram decididas antes da change e gravadas no documento 02 §1, no
documento 09 e no PRD-08.
