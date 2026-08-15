## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta:

- `paginacao.py` já traz tudo o que falta à rota: `contrato_de_listagem`, que recusa parâmetro
  desconhecido e aplica teto de tamanho, `codificar_cursor`/`decodificar_cursor` e
  `PaginaDeResultado[T]`. Nada de novo precisa nascer ali.
- `paginar_locais` é o precedente completo do cursor por par ordenado: filtra por
  `tuple_(...) > (...)`, pede `tamanho + 1` linhas e devolve cursor quando sobra a última.
- `consultar_series_do_guerreiro` hoje carrega **todas** as séries do coletor e, para cada uma,
  chama `apurar_estado_da_serie` e soma os pontos — dois acessos por série, sem teto.
- `SerieDeColeta` não tem coluna de criação própria: tem **`aberta_em`**, com
  `server_default=func.now()`, que é o análogo de `criado_em` do `Local`.
- A rota é recortada pela persona da sessão, não por comunidade declarada na requisição.

## Goals / Non-Goals

**Goals:**

- A rota entra no mesmo contrato das outras cinco listagens, sem contrato paralelo.
- O trabalho por chamada passa a ser proporcional ao **tamanho da página**, não ao total de
  séries do Guerreiro(a).

**Non-Goals:**

- Filtrar por `estado`: nenhum requisito o pede, e o filtro em SQL depende de o espelho estar
  reconciliado — o documento 02 §1 decidiu que a situação é apurada no instante da leitura.
- Totalizar os pontos na própria série: otimização sem requisito; a paginação já limita a
  agregação.
- Exigir o filtro de comunidade: a sessão já recorta mais estreito do que ele.

## Decisions

### O cursor ordena por `(aberta_em, id)`, como o de locais ordena por `(criado_em, id)`

A ordenação precisa ser **estável e total** para nenhuma série se repetir entre páginas nem
sumir. `aberta_em` sozinha não serve — duas séries abertas no mesmo instante empatariam —, e o
par com o `id` desempata. É a régua já usada em `paginar_locais`, com a coluna que a série tem.

```text
página 1 (tamanho 2)        página 2, com o cursor de S2
 S1  S2 │ S3  S4             S1  S2 │ S3  S4
 ▲───▲  └── sobra → cursor           ▲───▲
 devolvidas                          devolvidas
```

_Alternativa descartada:_ ordenar só por `aberta_em` — perde linha no empate, que é justamente
o caso de quem abre várias séries na mesma sessão de aula.

### O estado e os pontos são apurados depois de recortar a página

A ordem passa a ser **recortar → apurar → somar**, e não apurar tudo para depois recortar. É o
que torna o custo proporcional à página: a apuração de estado faz um `get` do desafio por série
e a soma dos pontos varre `registro_de_coleta`, particionada por tempo.

O efeito colateral é conhecido e aceito: **só as séries da página têm o espelho reconciliado**.
Nenhuma resposta sai errada — o estado devolvido é sempre o derivado —, e é exatamente o que o
documento 02 §1 fixou ao decidir que a situação é apurada no instante da leitura, não herdada.

_Alternativa descartada:_ apurar todas e paginar depois — mantém o custo que a change veio
resolver.

### O filtro de comunidade não é obrigatório nesta rota

`RF-01-18` pede que a consulta de dado de comunidade **aceite e aplique** filtro por comunidade.
Aqui o recorte já é a persona da sessão, que é mais estreito: a série é sempre do Guerreiro(a)
em sessão (`RN-08-04`), nunca de comunidade escolhida na requisição. Declarar
`filtro_comunidade_obrigatorio=True` faria a aplicação informar uma comunidade que o núcleo já
conhece — e que não poderia contrariar.

O filtro segue **aceito**, porque `contrato_de_listagem` já admite os universais; o que não se
faz é exigi-lo. Mesmo tratamento que `/chaves` e `/auditoria` recebem.

### `SerieDoGuerreiroSaida` não muda

O contrato do item permanece: `id`, `desafio_de_coleta_id`, `local_id`, `cadencia`, `estado` e
`pontos`. O que muda é o **envelope** — a lista crua vira `PaginaDeResultado` —, de modo que a
App 05 lê `itens` em vez da raiz, e nada mais.

## Risks / Trade-offs

- **Quebra de contrato para quem já consumisse a rota** → nenhuma aplicação a consome no Ciclo
  01: a rota nasceu na change anterior e a App 05 ainda não foi construída. Corrigir agora é
  mais barato do que depois de haver consumidor.
- **Espelho reconciliado só na página lida** → aceito e declarado acima; o estado devolvido é
  sempre o derivado, e a amostra da auditoria apura o seu próprio (documento 02 §1).
- **A soma dos pontos continua sendo uma varredura por série** → agora limitada ao tamanho da
  página. Se um dia incomodar, a saída é totalizar na série, não mudar a regra — segue anotado
  como estava.

## Migration Plan

Não há passo de banco: a mudança é de código e de contrato de saída. O deploy é o de sempre, e
o rollback é voltar a imagem anterior — a rota volta a devolver lista crua, sem perda de dado
nos dois sentidos.

## Open Questions

Nenhuma. O recorte aplica requisito vigente (`RF-01-28`, `RF-01-18`) sobre rota existente, com
o contrato de listagem já decidido e implementado; nada aqui depende de decisão do fundador.
