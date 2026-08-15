## 1. Consulta paginada

- [ ] 1.1 Passar `consultar_series_do_guerreiro` a receber `cursor` e `tamanho` e a devolver
      `PaginaDeResultado[SerieDoGuerreiroSaida]`, mantendo a recusa de persona de outro papel
      (`RF-08-17`, `RF-01-28`).
- [ ] 1.2 Paginar por cursor no par `(aberta_em, id)`, com `tuple_(...) > (...)`, `limit
      tamanho + 1` e cursor devolvido só quando sobrar linha — a mesma régua de
      `paginar_locais` (`RF-01-28`, design — o cursor ordena por `(aberta_em, id)`).
- [ ] 1.3 Apurar o estado e somar os pontos **depois** de recortar a página, e não antes, para
      o custo ficar proporcional ao tamanho dela (design — o estado e os pontos são apurados
      depois de recortar).
- [ ] 1.4 Mover `SerieDoGuerreiroSaida` de `rotas.py` para `regra.py`, como `LocalSaida` já
      fica, porque quem passa a montar a página é a regra — sem isso a regra importaria a rota.
      Os campos do item não mudam (design — `SerieDoGuerreiroSaida` não muda).

## 2. Rota

- [ ] 2.1 Declarar `contrato_de_listagem()` na rota e responder
      `PaginaDeResultado[SerieDoGuerreiroSaida]`, sem exigir o filtro de comunidade
      (`RF-01-28`, `RF-01-18`, design — o filtro de comunidade não é obrigatório).
- [ ] 2.2 Conferir que a rota segue sob chave de aplicação e sessão de Guerreiro(a), com 403
      para persona de outro papel (`RF-08-17`, `RN-08-04`).

## 3. Testes

- [ ] 3.1 Ajustar os testes existentes da consulta para lerem `itens` em vez da raiz, sem
      perder o que já cobriam (`RF-08-17`).
- [ ] 3.2 Testar que a página devolve o tamanho pedido e o cursor seguinte quando há mais
      séries do que cabem nela (`RF-01-28`).
- [ ] 3.3 Testar que percorrer as páginas pelo cursor, até ele vir nulo, devolve cada série uma
      única vez — sem repetição e sem falta (`RF-01-28`).
- [ ] 3.4 Testar que parâmetro que a rota não declara é recusado com 422, em vez de ignorado
      (`RF-01-28`).
- [ ] 3.5 Testar que o tamanho acima do teto é recusado com 422 (`RF-01-28`).
- [ ] 3.6 Testar que a consulta segue devolvendo só as séries do Guerreiro(a) da sessão e 403
      para outro papel, agora sob o contrato de listagem (`RN-08-04`, `RF-08-17`).

## 4. Fechamento

- [ ] 4.1 Rodar `ruff format --check .`, `ruff check .` e `pytest` no `backend/`, com as três
      passando.
- [ ] 4.2 Conferir que nenhuma outra listagem do núcleo ficou fora do contrato, para a correção
      não deixar um segundo caso do mesmo defeito (`RF-01-28`).
- [ ] 4.3 Documentação: nada a alterar em `docs/` — a change aplica `RF-01-28` e `RF-01-18`, já
      vigentes, sem regra nova, sem linha a mover no documento 09, sem mudança de situação em
      `docs/prds/index.md` e sem arquivo novo na `nav` do `mkdocs.yml`.
