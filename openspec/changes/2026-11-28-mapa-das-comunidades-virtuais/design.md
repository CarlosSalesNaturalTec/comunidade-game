# Design — Mapa das Comunidades Virtuais

## Context

- O núcleo já devolve `contorno` (`geometria`, `origem_osm`, `copiado_em`, `credito`, `licenca`)
  em `GET /v1/comunidades` e `GET /v1/comunidades/{id}`, nulo sem contorno
  (`openspec/specs/leitura-publica-do-territorio/spec.md`). Nada muda no backend.
- A App 06 é Astro com ilhas React, publicada no alvo `vitrine` do Firebase Hosting; hoje não tem
  biblioteca de mapa. A seção usa `ListaDeRegistros` (paginada) e a página usa `useLeitura`.
- Decisões do fundador de 2026-11-28: MapLibre GL + PMTiles; recorte do município de Salvador;
  arquivo no Firebase Hosting da App 06.

## Goals / Non-Goals

**Goals:** mapa na listagem e na página; fundo servido pela própria App 06; crédito e licença.

**Non-Goals:** ponto de coleta, local ou coletor no mapa; leitura do OSM em tempo de execução;
rotina de atualização do recorte (a frequência é pendência do documento 09).

## Decisions

1. **Origem do recorte: `pmtiles extract` do mapa-base do Protomaps.** O script
   `apps/app-06-vitrine/scripts/gerar-recorte-do-osm.sh` recorta de uma compilação diária datada
   do mapa-base Protomaps (derivado do OSM, ODbL) só a caixa do município de Salvador, até o zoom
   15, com a CLI `pmtiles` em **versão exata**. A caixa é o envoltório da relação do município no
   OSM, fixada no script com o identificador da relação; a data da compilação fica no script e no
   nome do commit. Roda só na geração — em tempo de execução nada sai para terceiro (`RN-03-45`).
   _Descartada:_ Planetiler local — baixa o extrato regional inteiro e exige Java para um recorte
   municipal.
2. **O arquivo vai versionado em `apps/app-06-vitrine/public/mapa/salvador.pmtiles`.** O Astro o
   copia para `dist/`, e o deploy existente o publica na mesma origem. Atualizar o recorte é rodar
   o script e abrir PR — ato revisado. _Descartada:_ gerar no deploy — a compilação datada do
   Protomaps não fica disponível para sempre, e o deploy quebraria sem revisão.
3. **Estilo próprio, sem rótulo de texto.** `public/mapa/estilo.json` desenha só fundo, água,
   áreas verdes, quadras e ruas, com cores dos tokens do documento 15. Sem camada de texto não há
   glifo nem sprite a hospedar. O **nome** da comunidade sai como marcador HTML do MapLibre no
   centro do envoltório do contorno, que é também um link para a página — caminho acessível por
   teclado e leitor de tela.
4. **Um componente, um motor.** `src/mapa/MapaDeComunidades.tsx` recebe a lista de
   `{id, nome, contorno}`, o modo (`listagem` ou `destaque`) e a navegação. O MapLibre e o protocolo
   `pmtiles://` ficam isolados em `src/mapa/motorDoMapa.ts`, importado por `import()` dinâmico: a
   página não carrega o MapLibre antes de precisar, e os testes substituem o motor, já que o jsdom
   não tem WebGL. Na listagem, clicar no preenchimento do contorno navega; o enquadramento é o
   envoltório de todos os contornos; no destaque, o da comunidade.
5. **A listagem lê todas as páginas para o mapa.** O mapa percorre `GET /v1/comunidades` pelo
   cursor, com o tamanho de página do teto, e desenha só quem tem contorno; no Ciclo 01 é uma
   leitura só. A lista segue com a própria paginação. Sem contorno algum, o mapa não monta
   (`RF-03-89`).
6. **Crédito e licença em texto fora da tela do mapa.** Abaixo do mapa, "© colaboradores do
   OpenStreetMap · ODbL", vindos de `credito` e `licenca` do núcleo, e o controle de atribuição do
   MapLibre com o mesmo texto (`RF-03-92`). O texto fora da tela é o que o leitor de tela e o teste
   alcançam.

## Risks / Trade-offs

- **Firebase Hosting e requisição parcial (Range).** O PMTiles lê o arquivo por faixas de bytes. Se
  o Hosting responder 200 sem faixa, o fundo não carrega: a tarefa de verificação confere `206` na
  homologação; falhando, a hospedagem volta ao fundador (a opção de Cloud Storage foi preterida).
- **Tamanho do repositório.** Cada recorte novo soma alguns megabytes ao histórico; aceitável à
  frequência de atualização, ainda a decidir.
- **Peso do MapLibre.** Cerca de 800 KB, carregado só quando há contorno a desenhar.
