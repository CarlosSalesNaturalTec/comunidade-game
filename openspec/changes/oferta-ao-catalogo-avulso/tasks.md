## 1. Leitura das próprias ofertas no núcleo

- [ ] 1.1 Em `backend/src/nucleo/catalogo_avulso/regra.py`, acrescentar `listar_ofertas_do_apoiador`,
      que devolve os itens cujo autor é o Apoiador em sessão, em toda situação, e recusa com 403
      persona de qualquer outro papel; e `contar_trocas_por_item`, a contagem agregada das trocas
      entregues de cada item (`RF-14-80`, `RF-14-81`, `RN-14-44`, design — decisões 1 e 2)
- [ ] 1.2 Em `backend/src/nucleo/catalogo_avulso/rotas.py`, acrescentar `GET /v1/eu/catalogo-avulso`
      com saída própria — a do item mais `quantidade_de_trocas` —, sem persona, nick, aula ou data
      de troca individual, e verificar a rota no OpenAPI (`RF-14-80`, `RF-14-81`, `RN-14-42`,
      `RN-14-43`, design — decisões 1 e 3)

## 2. Área de catálogo avulso na App 08

- [ ] 2.1 Criar `apps/app-08-apoiador/src/catalogoAvulso/api.ts` com `ofertarItem`
      (`POST /v1/catalogo-avulso`, sem campo de preço) e `listarMinhasOfertas`
      (`GET /v1/eu/catalogo-avulso`) (`RF-14-77`, `RF-14-79`, `RF-14-80`)
- [ ] 2.2 Criar `apps/app-08-apoiador/src/catalogoAvulso/TelaDeOferta.tsx` com nome, tipo de
      recurso, quantidade, comunidade e ponto de apoio por identificador, sem campo algum de
      preço, declarando que o preço vem da tabela de referência da gestão e que o item entra
      pendente até a homologação do Admin, com o `AvisoDeColeta` da área de direitos
      (`RF-14-77` a `RF-14-79`, `RN-14-42`, `RN-14-43`, `RF-14-58`, design — decisão 4)
- [ ] 2.3 Criar `apps/app-08-apoiador/src/catalogoAvulso/TelaDeMinhasOfertas.tsx` com a situação
      da homologação, o motivo da recusa em linguagem simples, a marca de ativo, o estoque
      restante, o preço em pontos extras, quantas trocas e o que falta de lastro ou de preço no
      item inativo — sem nome, nick, avatar, aula ou data de troca, e sem campo de contato
      (`RF-14-80`, `RF-14-81`, `RN-14-44`, `RF-14-59`)
- [ ] 2.4 Em `apps/app-08-apoiador/src/App.tsx`, acrescentar as áreas "Ofertar item" e
      "Minhas ofertas" à navegação, verificando pela navegação renderizada (`RF-14-77`,
      `RF-14-80`, design — decisão 5)

## 3. Testes

- [ ] 3.1 Em `backend/tests/test_catalogo_avulso.py`, cobrir a rota nova: o item pendente, o
      recusado com motivo, o inativo por falta de lastro e o inativo por falta de preço de
      referência aparecem para quem ofertou; item de outro proponente não aparece; Mestre, Admin,
      Guerreiro(a) e responsável recebem 403; a resposta não traz moedas nem reais (`RF-14-80`,
      `RN-14-42`, `RN-14-43`)
- [ ] 3.2 Em `backend/tests/test_catalogo_avulso.py`, cobrir a contagem de trocas: item sem troca
      vem com zero, item com três trocas entregues vem com três, e a resposta não traz persona,
      nick, aula nem data de troca individual (`RF-14-80`, `RF-14-81`, `RN-14-44`)
- [ ] 3.3 Criar `apps/app-08-apoiador/src/catalogoAvulso/catalogoAvulso.test.tsx`: a tela de
      oferta não tem campo de preço e declara a tabela da gestão e a homologação do Admin; a
      lista mostra pendente, recusado com motivo, ativo com estoque restante e trocas, e o que
      falta no inativo; nenhuma das duas exibe identificação de quem trocou nem campo de contato
      (`RF-14-77` a `RF-14-81`, `RN-14-42` a `RN-14-44`)

## 4. Documentação

- [ ] 4.1 Marcar a fatia 9 como implementada em `openspec/cronograma-de-fatias.md`, com o slug da
      change, e corrigir o recorte daquela linha: a pendência dos valores da tabela de preços é de
      dado — preço por tipo é cadastro da gestão —, não trava de desenho, como a §14 do PRD-14
      registra (decisão do fundador de 2026-09-02); mudar a situação do PRD-14 para "implementado"
      em `docs/prds/index.md`. Nenhum documento-fonte, o documento 09, o documento 99, o PRD-14 e
      a `nav` do `mkdocs.yml` mudam: a change não tomou decisão nova nem criou arquivo em `docs/`
