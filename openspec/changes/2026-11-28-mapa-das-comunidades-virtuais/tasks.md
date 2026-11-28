# Tarefas — Mapa das Comunidades Virtuais

## 1. Recorte e estilo

- [x] 1.1 Criar `apps/app-06-vitrine/scripts/gerar-recorte-do-osm.sh`: Overpass pela área da
      relação 362362 (município de Salvador), `osmtogeojson` em versão exata e tippecanoe até o zoom
      15, saída em `public/mapa/salvador.pmtiles` (`RN-03-45`, design — Decisões 1 e 2)
- [ ] 1.2 Gerar e versionar `public/mapa/salvador.pmtiles` com o script (`RN-03-45`)
- [x] 1.3 Criar `public/mapa/estilo.json`: fonte `pmtiles:///mapa/salvador.pmtiles`, camadas de
      mar, município, água, áreas verdes e ruas, sem camada de texto, glifo nem sprite
      (`RN-03-45`, design — Decisão 3)

## 2. Motor e componente

- [x] 2.1 Acrescentar `maplibre-gl` e `pmtiles` ao `package.json` da App 06 (`RF-03-89`)
- [x] 2.2 Criar `src/mapa/motorDoMapa.ts`: registra o protocolo `pmtiles://`, monta o mapa com o
      estilo próprio, desenha os contornos, os marcadores de nome com link, o clique no contorno,
      o enquadramento e o controle de atribuição (`RF-03-89`, `RF-03-90`, `RF-03-92`, `RN-03-44`)
- [x] 2.3 Criar `src/mapa/MapaDeComunidades.tsx`: importa o motor por `import()` dinâmico, modos
      `listagem` e `destaque`, crédito e licença do núcleo em texto abaixo do mapa, não monta sem
      contorno (`RF-03-89` a `RF-03-92`, `RN-03-46`)

## 3. Telas

- [x] 3.1 Em `src/api/leituras.ts`, acrescentar `contorno` a `ComunidadeNaLista` e a
      `ComunidadePublica`, e a leitura de todas as páginas de comunidades para o mapa
      (`RF-03-89`, `RF-03-91`, design — Decisão 5)
- [x] 3.2 Em `territorio/SecaoDeComunidades.tsx`, o mapa da listagem acima da lista, navegando
      para `caminhoDaComunidade` (`RF-03-89`, `RF-03-90`)
- [x] 3.3 Em `territorio/PaginaDaComunidade.tsx`, o mapa em destaque junto da representação
      visual, que fica (`RF-03-91`, `RF-03-20`, `RN-03-46`)

## 4. Testes

- [x] 4.1 `src/mapa/mapa.test.tsx`, com o motor substituído: listagem desenha os contornos com
      nome e o marcador abre a página; sem contorno não monta mapa nem erro; crédito e licença em
      texto; o motor recebe só contorno e nome — nenhum local, ponto ou coletor; o estilo e a fonte
      apontam só para a origem da App 06, sem `http` de terceiro em `estilo.json` (`RF-03-89`,
      `RF-03-90`, `RF-03-92`, `RN-03-44`, `RN-03-45`)
- [x] 4.2 Em `testes/territorioECobertura.test.tsx`, a página com contorno mostra o mapa e segue
      com a representação visual; a recém-criada mostra território vazio e mapa; a sem contorno
      fica como antes (`RF-03-91`, `RF-03-20`, `RN-03-46`)
- [ ] 4.3 Verificar na homologação, depois do merge, que `/mapa/salvador.pmtiles` responde `206` a
      requisição com `Range`; falhando, levar a hospedagem ao fundador (design — Riscos)

## 5. Documentação

- [x] 5.1 Documento 03 §8: a forma do fundo em uma frase. Documento 09 §1: "Forma do fundo do
      mapa" em "Já decididos". Sem arquivo novo em `docs/` nem relação nova no documento 99
- [ ] 5.2 `openspec/cronograma-de-fatias.md`: fatia 15 do PRD-03 como `implementado`, com o slug,
      quando a tarefa 1.2 fechar (o slug já está na linha)
