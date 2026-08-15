## 1. Parâmetro do piso

- [x] 1.1 Acrescentar à `Configuracao` o piso de coletores distintos do recorte publicado, com
      **três** como valor inicial, no padrão dos demais parâmetros de implantação
      (`RF-08-28`, `RN-08-24`)

## 2. Resolução do local publicado

- [x] 2.1 Escrever, em `locais/regra.py`, a consulta que resolve o **ancestral de nível bairro**
      de um local — ou a própria comunidade, quando a série está direto nela — por CTE
      recursiva sobre `local_pai_id` (`RN-08-13`, design — Decisions)
- [x] 2.2 Cobrir com teste a subida a partir de cada um dos seis níveis, inclusive local de
      nível comunidade e local de nível bairro, que resolvem para si mesmos (`RN-08-13`)

## 3. Agregação da série pública

- [x] 3.1 Escrever, em `coletas/regra.py`, a consulta que rotula cada registro de situação
      **válida** da comunidade com o par (tipo de coleta, local publicado), recortando pelo
      período sobre a **data da medição** (`RF-08-16`, `RF-08-15`, `RN-08-09`)
- [x] 3.2 Apurar `COUNT(DISTINCT coletor)` por recorte e **subir** ao nível da comunidade o
      recorte abaixo do piso, sem deixar rastro do recorte suprimido (`RF-08-28`, `RN-08-24`)
- [x] 3.3 Reapurar a contagem no nível da comunidade sobre a **união dos coletores distintos**
      que ali chegaram, e **suprimir** o recorte que ainda não alcança o piso (`RF-08-28`,
      `RN-08-24`, design — Decisions)
- [x] 3.4 Ordenar de forma estável por tipo, local publicado, data da medição e id do registro,
      e paginar por cursor opaco sobre essa quádrupla (`RF-01-28`, design — Decisions)

## 4. Rotas públicas

- [x] 4.1 Expor a rota de leitura da **série pública** da comunidade, sem dependência de
      persona e sob o contrato de listagem, com `cursor`, `tamanho`, `periodo_inicio` e
      `periodo_fim`, recusando com 422 o parâmetro não declarado (`RF-08-16`, `RF-01-28`,
      `RF-01-02`, `RN-01-32`)
- [x] 4.2 Montar a saída de cada ponto com a data e hora da medição, o valor quando houver, o
      tipo de coleta e o local publicado — **sem coletor, sem contagem de coletores e sem
      mídia** (`RN-08-12`, `RN-08-16`, `RF-08-21`)
- [x] 4.3 Expor a rota de leitura pública da **comunidade**, com os locais de nível comunidade e
      bairro e os tipos de coleta ativos nela, respondendo 404 para comunidade inexistente
      (`RF-08-16`, `RN-08-13`)
- [x] 4.4 Registrar as duas rotas em `principal.py`, sob o prefixo de versão e sem
      `exigir_persona` (`RF-01-02`, `RN-01-32`)

## 5. Verificação contra os critérios de aceite do PRD-08 §12

- [x] 5.1 Consulta pública de uma série **não devolve nick, nome, avatar** nem identificador de
      Guerreiro(a) — critério de aceite do PRD-08 §12 (`RN-08-12`)
- [x] 5.2 Consulta pública **não devolve local abaixo do bairro**, e registro gravado em rua
      compõe o agregado do bairro que a contém — critério de aceite do PRD-08 §12 (`RN-08-13`)
- [x] 5.3 Recorte de tipo e bairro com **três coletores distintos** é publicado; com **dois**,
      sobe para a comunidade e o bairro não aparece na resposta (`RF-08-28`, `RN-08-24`)
- [x] 5.4 Recorte que não alcança o piso **nem no nível da comunidade** não é publicado
      (`RF-08-28`, `RN-08-24`)
- [x] 5.5 Dois bairros abaixo do piso com **os mesmos coletores** somam coletores distintos uma
      só vez ao subir, e o recorte da comunidade continua abaixo do piso (`RN-08-24`)
- [x] 5.6 Consulta **com chave e sem token de sessão** responde; **sem chave** responde 401
      indistinto (`RF-01-02`, `RN-01-32`, `RN-01-33`)
- [x] 5.7 Parâmetro não declarado é recusado com **422**, e o cursor percorre todos os pontos
      publicáveis sem repetir nenhum e sem faltar nenhum (`RF-01-28`)
- [x] 5.8 Período recorta pela **data da medição**, e o piso é apurado **dentro do período**
      consultado: recorte com três coletores no total e dois no período não é publicado
      (`RF-08-15`, `RN-08-24`)
- [x] 5.9 Registro de situação **invalidada** fica fora do valor, da contagem e da contagem de
      coletores, gravando a situação diretamente enquanto a fatia da auditoria não existir
      (`RN-08-09`, design — Riscos)
- [x] 5.10 Registro por **foto** sai como ponto, com data da medição e sem valor, e **nenhuma
      mídia ou referência de mídia** acompanha a resposta (`RF-08-21`, `RN-08-16`)
- [x] 5.11 A leitura pública **não altera** o vínculo de autoria: os registros seguem gravados
      com o coletor de cada um (`RN-08-11`, `RN-08-12`)

## 6. Esteira e documentação

- [x] 6.1 `ruff format --check .`, `ruff check .` e `pytest` passam em `backend/`
- [x] 6.2 Atualizar `docs/prds/index.md` na nota de situação do PRD-08, refletindo o que resta
      dele — nenhuma decisão de produto nova foi tomada, de modo que documento-fonte, documento
      09, documento 99 e a `nav` do `mkdocs.yml` não mudam
- [x] 6.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR
