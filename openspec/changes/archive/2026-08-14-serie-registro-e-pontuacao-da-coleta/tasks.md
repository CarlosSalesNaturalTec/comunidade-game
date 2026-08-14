## 1. O papel do poder no catálogo

- [x] 1.1 Acrescentar a coluna `papel` a `Poder`, anulável, com o valor `territorio`
      (`RN-01-54`).
- [x] 1.2 Aceitar e devolver o papel na escrita e na leitura do catálogo, restrita a Admin como
      já é (`RN-01-54`, `RF-01-62`).
- [x] 1.3 Recusar com 409 a marcação de um segundo poder com o papel `territorio`, pelo índice
      único parcial do design (`RN-01-54`).
- [x] 1.4 Expor a busca do poder de papel `territorio`, usada pelo crédito da coleta
      (`RN-08-15`).
- [x] 1.5 Verificar: Admin marca o papel; o segundo é recusado com 409; poder sem papel é
      aceito; renomear o poder não muda o papel; o papel não é deduzido do nome (`RN-01-54`).

## 2. Período de cadência

- [x] 2.1 Escrever, em `coletas/regra.py`, a função única que delimita o período civil — dia,
      semana de segunda a domingo e mês — da data da medição, no fuso de São Paulo
      (`RN-08-06`).
- [x] 2.2 Verificar: a virada das 22h de sexta em São Paulo permanece na semana da sexta, e não
      passa para a seguinte pelo armazenamento em UTC (`RN-08-06`).

## 3. Série de coleta

- [x] 3.1 Criar o modelo `SerieDeColeta` com desafio, coletor, local, cadência herdada, estado,
      data de abertura e data da última medição válida (`RF-08-07`, PRD-08 §8).
- [x] 3.2 Abrir a série pelo Guerreiro(a) em sessão, sobre desafio vigente e local da sua
      comunidade, no estado `ativa` (`RF-08-07`).
- [x] 3.3 Recusar com 403 o local de outra comunidade e a persona que não é Guerreiro(a); com
      422 o desafio fora da vigência (`RF-08-07`, `RN-08-02`).
- [x] 3.4 Conferir na abertura o teto de granularidade da comunidade contra a granularidade
      exigida do desafio, e o nível do local contra essa granularidade — 422 nos dois casos
      (`RN-08-25`).
- [x] 3.5 Atribuir a série ao Guerreiro(a) da sessão, ignorando coletor informado no corpo, e
      recusar com 409 a segunda série do mesmo par de desafio e local (`RN-08-04`).
- [x] 3.6 Registrar a operação de escrita da série em `permissoes.py`, escopada ao Guerreiro(a)
      (`RF-01-16`).
- [x] 3.7 Verificar: abertura aceita; local de outra comunidade recusado; desafio fora da
      vigência recusado; Mestre recusado; granularidade acima do teto recusada; granularidade
      dentro do teto aceita; local de nível diferente recusado; coletor informado ignorado;
      série duplicada recusada; dois Guerreiros abrem séries independentes sobre o mesmo par
      (`RF-08-07`, `RN-08-04`, `RN-08-25`).
- [x] 3.8 Verificar que a série nasce `ativa` e assim permanece após dois períodos de cadência
      sem registro, porque a transição é de entrega posterior (`RF-08-07`).

## 4. Registro de coleta

- [x] 4.1 Criar o modelo `RegistroDeColeta` reusando o mixin `ComMomentoDoFato`, com série,
      valor, unidade, origem, mídia, situação, marca "a conferir", comunidade e pontos
      creditados (`RF-08-08`, `RF-08-15`, PRD-08 §8).
- [x] 4.2 Gravar a medição enviada pelo Guerreiro(a) dono da série; recusar com 403 quem não é o
      coletor e a persona de outro papel (`RF-08-08`).
- [x] 4.3 Recusar com 422 a medição fora da vigência do desafio e a medição com data no futuro
      (`RF-08-08`, `RF-08-15`).
- [x] 4.4 Gravar a origem entre `manual` e `voz`, e recusar com 422 a origem `sensor` na rota de
      sessão, que exige credencial de dispositivo de entrega posterior (`RF-08-08`, `RN-08-23`).
- [x] 4.5 Exigir valor e unidade quando o tipo declara a forma `numero`, e mídia quando declara
      `foto` ou `video`, gravando a mídia pela `PortaDeArmazenamento` e guardando no registro
      apenas a referência (`RF-08-21`).
- [x] 4.6 Aceitar e marcar "a conferir" o valor fora da faixa esperada do tipo, qualquer que
      seja a origem, sem impedir o crédito; tipo sem faixa não produz a marca (`RF-08-12`).
- [x] 4.7 Resolver a comunidade do registro pelo vínculo do coletor **na data da medição** e
      gravá-la no registro (`RN-08-03`).
- [x] 4.8 Atualizar na série a data da última medição válida a cada registro válido
      (`RF-08-07`).
- [x] 4.9 Não expor rota de alteração nem de exclusão de registro (`RN-08-10`).
- [x] 4.10 Registrar a operação de escrita do registro em `permissoes.py`, escopada ao coletor
      da série (`RF-01-16`).
- [x] 4.11 Verificar: o coletor grava; quem não é coletor recebe 403; medição fora da vigência e
      no futuro recusadas; hora da medição distinta da hora do envio; período apurado pela
      medição; origem `sensor` recusada; mídia aceita como registro e ausência dela recusada;
      forma `numero` sem valor recusada; valor acima e abaixo da faixa marcados "a conferir";
      valor dentro da faixa e tipo sem faixa sem marca; comunidade gravada é a da data da
      medição; alteração e exclusão respondem 405; o coletor permanece após o fim do vínculo
      (`RF-08-08`, `RF-08-12`, `RF-08-15`, `RF-08-21`, `RN-08-03`, `RN-08-10`, `RN-08-11`).

## 5. Crédito ao Poder do Território

- [x] 5.1 Creditar 5 pontos regulares por registro válido ao poder de papel `territorio`, nunca
      ao poder da trilha em que o desafio nasceu, na mesma transação da gravação do registro
      (`RF-08-09`, `RN-08-05`, `RN-08-15`).
- [x] 5.2 Creditar zero ao registro que exceder a quantidade de registros que pontuam declarada
      no desafio, mantendo-o válido e informando na resposta se pontuou (`RN-08-06`).
- [x] 5.3 Recusar com 409 a gravação de registro quando nenhum poder do catálogo exerce o papel
      `territorio` (`RN-01-54`, `RN-08-15`).
- [x] 5.4 Verificar: registro válido credita 5 ao Poder do Território e nada ao poder da trilha;
      o valor não varia com o tipo de coleta; quatro registros do período creditam os quatro
      quando o desafio assim declara; o segundo registro credita zero quando só um pontua; o
      primeiro do período seguinte volta a pontuar; a contagem segue a data da medição; sem
      poder de papel `territorio` o registro é recusado com 409; o registro por mídia credita
      como o por número (`RF-08-09`, `RN-08-05`, `RN-08-06`, `RN-08-15`, `RN-01-54`).
- [x] 5.5 Verificar que nenhuma rota do contrato de leitura dos jogos credita ponto de coleta
      (`RN-08-17`, `RF-01-22`).

## 6. Migração e rotas

- [x] 6.1 Escrever a migração do Alembic: a coluna `papel` com o índice único parcial, a tabela
      `serie_de_coleta` e a `registro_de_coleta` **criada já particionada** por RANGE na data da
      medição, com as partições anuais do Ciclo 01 e a partição padrão (documento 03 §1).
- [x] 6.2 Conferir que a chave primária do registro é o par `(id, momento_do_fato)`, que o
      particionamento exige, e deixar isso explícito no modelo.
- [x] 6.3 Registrar as rotas novas no roteador de coletas e em `principal.py`, com o schema
      OpenAPI saindo completo (`RF-08-07`, `RF-08-08`).
- [x] 6.4 Verificar `downgrade` simétrico da migração.

## 7. Documentação

- [x] 7.1 Corrigir no PRD-08 a contradição com o documento 03 §7: reescrever `RF-08-15` como a
      distinção entre a hora da medição e a hora do envio, e remover a fila local da exceção de
      §5.3, da descrição da rota de §9, do requisito não funcional de §10 e do cenário de §12,
      conferindo a rastreabilidade de §15.
- [x] 7.2 Conferir que `docs/prds/index.md`, o documento 99 e a `nav` do `mkdocs.yml` não mudam
      — nenhum arquivo nasceu, nenhuma relação entre documentos mudou e o PRD-08 segue aprovado
      até a sua última fatia.
- [x] 7.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict`, com as dependências do
      `package.json` instaladas.
- [x] 7.4 Rodar `ruff format --check .`, `ruff check .` e `pytest` no backend.
