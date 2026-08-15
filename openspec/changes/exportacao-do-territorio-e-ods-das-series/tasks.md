## 1. Cobertura de ODS vinda da coleta

- [x] 1.1 Somar, em `ods/regra.py`, a segunda fonte da cobertura por comunidade: a união das
      etiquetas dos **desafios de coleta com série aberta** por Guerreiro(a) daquela comunidade,
      dentro de `cobertura_por_comunidade` (`RF-08-26`, `RF-08-25`)
- [x] 1.2 Estender `comunidades_com_cobertura` para alcançar a comunidade cuja única atividade é
      a coleta, sem a qual ela seria calculada e nunca perguntada (`RF-08-26`, design —
      Decisions)
- [x] 1.3 Não filtrar por estado da série: ativa, interrompida e encerrada contam igual
      (`RF-08-26`, design — Decisions)

## 2. Consulta da exportação

- [x] 2.1 Reusar `_consulta_de_registros_publicaveis` na exportação, com os mesmos argumentos de
      comunidade, período e piso — sem reimplementar corte, piso ou supressão (`RN-08-12`,
      `RN-08-13`, `RF-08-28`, `RN-08-24`, design — Decisions)
- [x] 2.2 Apurar o **período coberto** da primeira e da última medição efetivamente contidas no
      conjunto, depois do piso, devolvendo período vazio para conjunto vazio (`RF-08-27`)

## 3. Serialização e rotas

- [x] 3.1 Serializar o conjunto em **CSV**, uma tabela por arquivo, com cabeçalho declarado na
      primeira linha e o local saindo como rótulo e nível (`RF-08-19`, documento 03 §12.3)
- [x] 3.2 Expor a rota pública de exportação da comunidade, sem dependência de persona,
      aceitando período e respondendo 404 para comunidade inexistente (`RF-08-19`, `RF-01-02`,
      `RN-01-32`)
- [x] 3.3 Devolver em cabeçalhos de resposta a **licença CC BY-SA**, o **período coberto** e o
      endereço da rota irmã de metadados (`RF-08-27`, design — Decisions)
- [x] 3.4 Expor a rota irmã que devolve o **dicionário de dados** — cada campo com unidade,
      cadência e origem — e a **declaração da contribuição à meta 17.18** com o período coberto
      (`RF-08-19`, `RF-08-27`, documento 03 §12.3, documento 04 §4)
- [x] 3.5 Registrar as rotas em `principal.py`, sob o prefixo de versão e sem `exigir_persona`
      (`RF-01-02`, `RN-01-32`) — já cobertas pelo roteador de comunidades, incluído sob `/v1`
      em `principal.py`

## 4. Verificação contra os critérios de aceite do PRD-08 §12

- [x] 4.1 O CSV traz cabeçalho declarado na primeira linha e uma tabela por arquivo, sem
      envelope em volta (`RF-08-19`)
- [x] 4.2 O conjunto exportado **não traz nick, nome, avatar** nem identificador de
      Guerreiro(a), nem a contagem de coletores — critério de aceite do PRD-08 §12 (`RN-08-12`)
- [x] 4.3 O conjunto **não desce abaixo do bairro**: registro de rua compõe o agregado do bairro
      que o contém (`RN-08-13`)
- [x] 4.4 O **piso de coletores** vale igual na exportação: recorte abaixo do piso sobe, e o que
      não o alcança nem no topo fica fora do conjunto (`RF-08-28`, `RN-08-24`)
- [x] 4.5 Registro de situação **invalidada** fica fora do conjunto, gravando a situação
      diretamente enquanto a fatia da auditoria não existir (`RN-08-09`)
- [x] 4.6 O período recorta pela **data da medição**, e o **período coberto declarado** é o do
      conjunto, não o do pedido: pedido de um ano com medições em dois meses declara dois meses
      (`RF-08-15`, `RF-08-27`)
- [x] 4.7 Todo campo do CSV tem entrada no dicionário de dados, e o dicionário não descreve
      campo ausente (`RF-08-19`)
- [x] 4.8 A saída declara a **licença CC BY-SA** e a **contribuição à meta 17.18** com o período
      coberto (`RF-08-27`)
- [x] 4.9 Exportação **com chave e sem token de sessão** responde; **sem chave** responde 401
      indistinto; comunidade inexistente responde 404 (`RF-01-02`, `RN-01-32`)
- [x] 4.10 A cobertura de comunidade **soma trilha e coleta**, e o objetivo etiquetado nas duas
      fontes aparece **uma só vez** (`RF-08-26`, design — Riscos)
- [x] 4.11 Comunidade **sem Resultado** e com série aberta sobre desafio etiquetado aparece na
      cobertura pública, com o objetivo do desafio (`RF-08-26`)
- [x] 4.12 Série **interrompida ou encerrada** continua cobrindo o objetivo do desafio
      (`RF-08-26`, design — Decisions)
- [x] 4.13 A cobertura continua **sem recorte por Guerreiro(a)**, em qualquer eixo (`RN-08-22`,
      invariante 20 do documento 99 §6)

## 5. Esteira e documentação

- [x] 5.1 `ruff format --check .`, `ruff check .` e `pytest` passam em `backend/`
- [x] 5.2 Atualizar `docs/prds/index.md` na nota de situação do PRD-08 — nenhuma decisão de
      produto nova foi tomada, de modo que documento-fonte, documento 09, documento 99 e a `nav`
      do `mkdocs.yml` não mudam
- [x] 5.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR
