## 1. Preço de referência em pontos extras

- [ ] 1.1 Criar `PrecoDeReferencia` em `backend/src/nucleo/recursos/modelo.py`, ao lado de
      `ValorDeReferencia`: tipo de recurso, preço inteiro, vigência inicial e final, autoria
      (`RF-07-42`, `RF-07-43`)
- [ ] 1.2 Escrever a regra de vigência em `recursos/regra.py` — abrir vigência encerra a anterior
      no dia de início, sem sobreposição; empate no mesmo dia vale a última registrada; leitura
      por data devolve a vigência da época (`RF-07-43`)
- [ ] 1.3 Aplicar o piso de 20 pontos extras e a recusa de preço fracionário, negativo ou zero,
      com 422 indicando o piso (`RF-07-44`, `RN-07-30`)
- [ ] 1.4 Expor `POST` e `GET /tipos-de-recurso/{id}/precos-de-referencia` em `recursos/rotas.py`,
      exigindo Admin em sessão e devolvendo 403 às demais personas (`RF-07-42`, `RF-01-16`)
- [ ] 1.5 Garantir que registrar preço em pontos não toca o valor em moedas e que nenhuma resposta
      traz equivalência entre as réguas (`RF-07-38`, `RN-07-24`, `RN-07-25`)

## 2. Item do catálogo avulso

- [ ] 2.1 Criar o módulo `backend/src/nucleo/catalogo_avulso/` com `ItemDeCatalogoAvulso`: nome,
      tipo de recurso, estoque, comunidade, ponto de apoio, origem do cadastro, situação de
      homologação com motivo, marca de ativo e autoria (`RF-07-33`, `RF-09-99`, `RF-14-77`)
- [ ] 2.2 Escrever o cadastro em `catalogo_avulso/regra.py`: Mestre ou Apoiador em sessão, Mestre
      só na comunidade a que está vinculado, ponto de apoio obrigatoriamente da comunidade do
      item, estoque mínimo de 1, e recusa de campo de preço declarado (`RF-07-33`, `RF-07-45`,
      `RN-07-29`, `RN-07-33`)
- [ ] 2.3 Implementar a homologação: item de Mestre entra sem homologação, item de Apoiador nasce
      pendente e inativo, e o Admin homologa ou recusa com motivo (`RF-09-100`, `RN-14-42`,
      `RN-07-26`)
- [ ] 2.4 Implementar o lastro — quantidade disponível do tipo no ponto de apoio do item igual ou
      maior que o estoque declarado —, gravando o item inativo e dizendo o que falta em vez de
      recusar, sem criar reserva nem lançamento (`RF-07-34`, `RF-09-101`, `RN-07-26`, `RN-07-27`)
- [ ] 2.5 Implementar a ativação, que reverifica o lastro e recusa item pendente de homologação ou
      recusado (`RF-07-34`, `RN-09-37`)
- [ ] 2.6 Implementar a alteração de estoque e a retirada — ambas de Admin ou Mestre vinculado,
      com autoria; estoque acima do lastro desativa o item, e a retirada preserva o registro
      (`RF-07-33`, `RF-09-102`)
- [ ] 2.7 Implementar a leitura do catálogo por comunidade, com o preço da vigência corrente, o
      estoque e a marca de ativo; Guerreiro(a) vê a sua comunidade e só os ativos, Admin e Mestre
      vinculado pedem também os inativos (`RF-07-33`, `RF-04-50`, `RF-05-83`, `RF-09-103`,
      `RF-01-24`)
- [ ] 2.8 Expor as rotas de `catalogo_avulso/rotas.py` conforme a tabela do `design.md` e
      registrá-las na aplicação, sob `/v1` e com chave de aplicação (`RF-07-33`, `RF-01-03`)

## 3. Persistência

- [ ] 3.1 Escrever a migração Alembic com `preco_de_referencia` e `item_de_catalogo_avulso`, sem
      alterar tabela existente, e conferir que a reversão derruba as duas

## 4. Testes

- [ ] 4.1 `tests/test_preco_de_referencia.py`: primeira vigência, vigência nova preservando a
      anterior, empate no mesmo dia, leitura pela data da época, piso de 20 aceito e 19 recusado,
      alteração para abaixo do piso, preço fracionário, 403 do Mestre (`RF-07-42`, `RF-07-43`,
      `RF-07-44`, `RN-07-30`)
- [ ] 4.2 `tests/test_preco_de_referencia.py`: as duas réguas convivem sem se tocar — registrar
      preço não altera o valor em moedas, tipo com preço e sem valor, e nenhuma resposta com
      equivalência em moedas ou reais (`RF-07-38`, `RN-07-24`, `RN-07-25`)
- [ ] 4.3 `tests/test_catalogo_avulso.py`: cadastro por Mestre e por Apoiador, ponto de apoio de
      outra comunidade recusado, Mestre fora do vínculo, Guerreiro(a) recusado, estoque menor que
      1 e cadastro com preço declarado (`RF-07-33`, `RF-07-45`, `RN-07-29`)
- [ ] 4.4 `tests/test_catalogo_avulso.py`: homologação — item de Mestre dispensa, item de Apoiador
      nasce pendente e inativo mesmo com lastro, Admin homologa e ativa, Admin recusa com motivo,
      Mestre recebe 403 (`RF-09-100`, `RN-14-42`)
- [ ] 4.5 `tests/test_catalogo_avulso.py`: lastro — item com saldo igual ao estoque nasce ativo,
      saldo menor nasce inativo dizendo o que falta, saldo em outro ponto de apoio não lastreia,
      ativação reverifica, ativação sem lastro recusada, item pendente não ativa, e tipo sem preço
      vigente nasce inativo (`RF-07-34`, `RF-09-101`, `RN-07-26`)
- [ ] 4.6 `tests/test_catalogo_avulso.py`: manutenção e leitura — estoque alterado dentro e acima
      do lastro, retirada que preserva o registro, 403 do Apoiador, catálogo filtrado pela
      comunidade do Guerreiro(a), inativos só para Admin e Mestre vinculado, e nenhuma resposta
      com moedas ou reais (`RF-07-33`, `RF-09-102`, `RF-04-50`, `RF-05-83`, `RN-07-24`)

## 5. Documentação

- [ ] 5.1 Gravar as três decisões novas nos documentos-fonte: a janela de troca como garantia da
      App 01 e o lastro do item igual ou maior que o estoque declarado no documento 02 §8.2; o
      item declarando o ponto de apoio no documento 04 §1
- [ ] 5.2 Mover as três para "Já decididos" no documento 09 §1, cada uma com o documento-fonte
- [ ] 5.3 Aplicar as decisões nos PRDs: `ItemDeCatalogoAvulso` ganha o ponto de apoio no PRD-07
      §8, as decisões entram na tabela do PRD-07 §13, e o PRD-04 registra que o `RF-04-49` é
      garantia da aplicação
- [ ] 5.4 Atualizar `docs/prds/index.md` com a sétima fatia do PRD-07 e conferir que nada mudou na
      relação entre documentos (documento 99) nem na `nav` do `mkdocs.yml`, por não haver arquivo
      novo em `docs/`
