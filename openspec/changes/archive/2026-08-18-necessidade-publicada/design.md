## Context

Ver proposal.md — Why. O que o núcleo já tem e esta fatia apenas lê:

| Peça                              | Onde                        | O que dá                                     |
| --------------------------------- | --------------------------- | -------------------------------------------- |
| `Aula.situacao`                    | `aulas/modelo.py`           | quem está em `pendente_de_lastro`            |
| `RecursoDeclaradoDaAula`           | `aulas/modelo.py`           | o que a aula precisa, por tipo               |
| `disponivel_de()`                  | `reservas/regra.py`         | saldo derivado menos reservado, por par      |
| `consultar_valor_de_referencia()`  | `recursos/regra.py`         | valor em moedas vigente numa data            |
| `confirmar_aulas_pendentes()`      | `reservas/regra.py`         | a ordem `inicio_em asc` que a fatia 3 fixou  |

Nada disso muda. A fatia é uma derivação nova sobre peças existentes e duas rotas de leitura.

## Goals / Non-Goals

**Goals:**

- Derivar a falta sem gravar nada, recontável como o saldo.
- Manter uma única definição de ordem entre a confirmação e a lista.
- Servir a mesma projeção nas duas rotas, sem valor em reais e sem dado de pessoa.

**Non-Goals:**

- Escrita de qualquer natureza — inclusive o ato de assumir a absorção, que já tem rota.
- Cache, materialização ou índice novo: o volume do Ciclo 01 não pede, e a rota é cacheável na
  borda por decisão já registrada no PRD-07 §10.
- Agrupar por comunidade, por nível de necessidade ou por missão — é PRD-14, fora da esteira.

## Decisions

### 1. Derivação pura, com chave natural — nenhuma tabela nova

A necessidade é função de `aula`, `recurso_declarado_da_aula`, `reserva` e `lancamento`, todas
já existentes, e é identificada pelo par **aula + tipo de recurso**. Sem modelo, sem migration.

Alternativas descartadas: tabela `necessidade` mantida por gatilho a cada aporte — cria número
guardado que pode divergir do saldo, que é derivado; e cache materializado — otimização sem
problema medido.

### 2. Atribuição gulosa por horário, por par tipo + ponto de apoio

Para cada par tipo/ponto de apoio, o núcleo parte do `disponivel_de()` e percorre as aulas
pendentes de lastro que declaram aquele tipo, em `inicio_em asc`, atribuindo a cada uma o menor
entre o que ela declarou e o que ainda resta:

```text
restante ← disponivel_de(tipo, ponto)
para cada aula pendente que declara o tipo, em inicio_em asc:
    atribuido ← min(declarado, restante)
    restante  ← restante − atribuido
    falta     ← declarado − atribuido
    se falta > 0: emite necessidade(aula, tipo, falta)
```

**O ponto que exige atenção:** isto **não** é um espelho fiel do que a confirmação faria. A
reserva é tudo-ou-nada entre os tipos de uma aula (fatia 3), então uma aula pendente não
consome disponível de fato — ela nada reserva enquanto faltar qualquer parcela. Espelhar isso
faria duas aulas de 10 com 6 disponíveis aparecerem **ambas** com falta 4, contando o mesmo
disponível duas vezes e mentindo sobre o total. A atribuição gulosa dá 4 e 10, cuja soma é a
falta real do conjunto — que é o que o documento 04 §1 decidiu.

Alternativa descartada: espelhar o tudo-ou-nada da reserva — soma que não fecha.

### 3. A ordem vive num lugar só

`inicio_em asc` já é a ordem de `confirmar_aulas_pendentes()`. A derivação a repete, e um teste
cobre as duas contra o mesmo cenário, para que divergirem seja falha vermelha e não silêncio.

Alternativa descartada: extrair a ordem para uma constante compartilhada — indireção maior que
o problema, com as duas funções no mesmo módulo vizinho.

### 4. Moedas pela vigência de hoje, ausência explícita

O valor sai de `consultar_valor_de_referencia(tipo, data=agora().date())`. Sem vigência válida
hoje, a necessidade sai **sem** o campo — nunca com zero, que se confundiria com gratuito.

É a única divergência consciente de `_valorar_debito()` das reservas, que **levanta erro** sem
vigência: ali o núcleo está gravando um lançamento e não pode gravar sem valor; aqui está
listando, e recusar a lista inteira por um tipo mal cadastrado esconderia todas as outras
faltas.

### 5. Duas rotas, dois regimes de credencial

`GET /vitrine/necessidades` entra no prefixo que o núcleo reserva à leitura sem persona, sob
chave de aplicação como toda rota de dados. `GET /necessidades/minhas` exige sessão de Mestre e
fica **fora** de `/vitrine`, cujo sentido é justamente a leitura sem persona; segue a convenção
das rotas logadas, como `/series-de-coleta/minhas`. As duas servem a **mesma** projeção — o
filtro por comunidade é a única diferença.

### 6. Filtro do Mestre pelo vínculo de comunidade

Reusa o vínculo que `aula-e-presenca` já confere no cancelamento. Sem campo novo e sem tocar o
PRD-01.

## Risks / Trade-offs

- **A ordem da derivação e a da confirmação divergirem numa fatia futura** → teste que fixa o
  mesmo cenário contra as duas, na Decisão 3.
- **Custo da derivação cresce com aulas pendentes × tipos declarados** → é `O(pares)` com um
  `disponivel_de()` por par tipo/ponto de apoio; no Ciclo 01 são dezenas de aulas, e a rota
  pública é cacheável (PRD-07 §10). Medir antes de otimizar.
- **Leitura sem bloqueio pode ver estado transitório** durante um aporte concorrente → a lista
  é painel vivo (`RN-07-31`), sem decisão tomada em cima dela; o bloqueio que importa está na
  escrita, onde a fatia 3 o pôs.
- **A lista pública passa a expor ponto de apoio, data e horário da aula** → é decisão do
  fundador, gravada no documento 04 §1; a resposta não leva pessoa alguma, e o freio por origem
  das rotas públicas já se aplica.

## Migration Plan

Sem migration: nada é gravado. A entrega é aditiva — duas rotas novas, nenhuma existente muda
de contrato. Rollback é remover o roteador.
