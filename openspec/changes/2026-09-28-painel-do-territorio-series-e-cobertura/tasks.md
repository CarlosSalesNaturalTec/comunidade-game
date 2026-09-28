# Tasks

## 1. Núcleo — metodologia e estado do recorte

- [ ] 1.1 Estender `_consulta_de_registros_publicaveis` em `backend/src/nucleo/coletas/regra.py`
      para carregar também `serie_de_coleta_id` e `origem`, mantendo uma régua só de piso e
      subida de nível; verificar que os testes de `test_leitura_publica_do_territorio.py`
      seguem verdes sem mudança de comportamento (`RN-08-24`, `RN-08-13`)
- [ ] 1.2 Apurar a metodologia por recorte publicado — nome e unidade do tipo, cadências,
      período coberto, origens e registros válidos — sobre a mesma consulta, e o estado
      ativo/inativo a partir das séries dos registros publicados (`RF-03-17`, `RF-03-18`,
      `RF-03-19`, `RN-03-10`)
- [ ] 1.3 Trocar o envelope de `GET /v1/comunidades/{id}/series` por `itens`, `proximo_cursor` e
      `recortes`, com a metodologia apurada sobre o período inteiro antes do corte de página;
      verificar que cursor, tamanho e o 422 de parâmetro não declarado continuam idênticos
      (`RF-03-17`, `RF-03-18`, `RF-01-28`)

## 2. Núcleo — vitalidade da comunidade

- [ ] 2.1 Contar os Guerreiros e Guerreiras vinculados pelo vínculo vigente em
      `backend/src/nucleo/comunidades/regra.py` e devolver o número em `GET /v1/comunidades/{id}`
      (`RF-03-02`, documento 11 §8.2)
- [ ] 2.2 Devolver o mesmo número em `GET /v1/comunidades`, ao lado dos quatro indicadores e
      **fora** da supressão por piso, sem que nenhum quinto indicador do documento 02 §1 saia
      (`RF-03-02`, `RN-08-28`, `RN-08-29`)

## 3. Camada comum — carta e representação visual

- [ ] 3.1 Acrescentar a variante Comunidade Virtual a `comum/react/CartaDoPersonagem.tsx` e
      fazer `cartaEstaCompleta` decidir por variante, de modo que comunidade sem indicadores
      caia em outra forma de apresentação (`RF-03-02`, documento 11 §8.2)
- [ ] 3.2 Criar em `comum/react/` a representação visual do território em SVG paramétrico:
      contorno com nome na comunidade vazia, uma camada por tipo de coleta ativo com presença
      proporcional aos registros válidos, detalhe pelo número de bairros publicados e camada de
      recorte inativo marcada (`RF-03-19`, `RF-03-20`, `RF-03-21`, documento 11 §8.3)

## 4. App 06 — território, cobertura e bloco do gestor

- [ ] 4.1 Acrescentar a `apps/app-06-vitrine/src/api/leituras.ts` as leituras da lista de
      comunidades, da ficha, da série com metodologia e da cobertura de ODS, com os tipos do
      que as telas leem (`RF-03-15`, `RF-03-22`)
- [ ] 4.2 Entregar a seção Comunidades Virtuais com um card por comunidade pela carta nova, uma
      única leitura da lista, e o caminho próprio `/comunidades/<id>` no padrão de
      `nickDoCaminho` (`RF-03-02`, `RF-03-15`)
- [ ] 4.3 Entregar a página da comunidade com as séries agregadas até o bairro, a metodologia e
      os registros válidos por recorte, o sinal de inativo legível sem depender de cor e a
      representação visual (`RF-03-15` a `RF-03-21`, `RN-03-09`, `RN-03-10`)
- [ ] 4.4 Entregar a seção de cobertura da Agenda 2030 por comunidade e ciclo, com o destaque da
      meta 17.18 e o ODS 18 como adoção voluntária do Brasil, sem etiqueta ligada a pessoa
      (`RF-03-22` a `RF-03-24`, `RN-03-19`, `RN-03-20`)
- [ ] 4.5 Entregar o bloco em destaque do recorte de gestores públicos, antes do painel, com os
      usos concretos do dado, o caminho para pedir o conjunto completo e os dois limites
      declarados (`RF-03-63` a `RF-03-65`, `RN-03-28`)

## 5. Testes

- [ ] 5.1 Em `backend/tests/test_leitura_publica_do_territorio.py`: metodologia do recorte com
      tipo, unidade, cadências, período e origens; contagem de registros válidos sem os
      invalidados; metodologia recortada pelo período pedido; recorte inativo só quando nenhuma
      série dele está ativa, permanecendo na resposta; nenhuma série individual nem coletor na
      saída (`RF-03-17` a `RF-03-19`, `RN-03-10`)
- [ ] 5.2 Em `backend/tests/test_lista_publica_de_comunidades.py` e `test_comunidade_rota.py`: o
      número de vinculados nas duas rotas, apurado pelo vínculo vigente, presente também na
      comunidade abaixo do piso, e a resposta sem nick, avatar ou identificador de pessoa
      (`RF-03-02`, `RF-03-16`, `RN-08-28`)
- [ ] 5.3 Em `comum/react/carta.test.tsx` e no teste da representação visual: os cinco campos da
      variante Comunidade Virtual, a comunidade sem indicadores caindo em outra forma, o
      território vazio, o crescimento por contagem e a camada inativa que permanece
      (`RF-03-02`, `RF-03-19` a `RF-03-21`)
- [ ] 5.4 Em `apps/app-06-vitrine/src/testes/`: card e página da comunidade por endereço próprio,
      painel com metodologia e sinal de inativo, ausência de qualquer recorte abaixo do bairro e
      de identificação de coletor, cobertura por comunidade e ciclo sem etiqueta por pessoa, e o
      bloco do gestor abrindo o recorte com os dois limites (`RF-03-15` a `RF-03-24`, `RF-03-63`
      a `RF-03-65`, `RN-03-09`, `RN-03-10`, `RN-03-28`)

## 6. Documentação

- [ ] 6.1 Marcar a fatia 3 do PRD-03 como implementada em `openspec/cronograma-de-fatias.md`,
      com o slug da change e o que ela levou de núcleo; corrigir no PRD-03 §9 a linha de
      `GET /v1/comunidades/{id}/ods`, que não é criada; e registrar no documento 09 §1 as quatro
      decisões do fundador de 2026-09-28. `docs/prds/index.md`, o documento 99 e a `nav` do
      `mkdocs.yml` não mudam — nenhum arquivo nasce e nenhuma relação entre documentos muda
