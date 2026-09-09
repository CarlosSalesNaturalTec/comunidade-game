## 1. Ordem dos blocos da missão

- [ ] 1.1 Reordenar os nove `BlocoRecolhivel` de `ListaDeMissoes.tsx` para template da missão,
      conteúdo, bibliografia, cadência de retomada, atividades, desafio de desbloqueio,
      recompensa pelo desbloqueio, desafios de coleta e ODS da missão, mantendo a
      pré-visualização depois de todos e sem tocar os `useState` nem o `gravadoEm` do
      componente (`RF-09-25`, design — decisão 6). Verifica-se abrindo uma missão: a ordem dos
      títulos é essa, e cada bloco continua abrindo, gravando e mostrando a marca de gravação.

## 2. Paginação da trilha por etapa do ciclo

- [ ] 2.1 Agrupar as missões por `etapa_do_ciclo` em `TelaDaTrilha.tsx` e navegar entre as
      quatro etapas, com a etapa aberta em estado local e a contagem de missões visível em
      cada uma; as quatro aparecem sempre, inclusive as vazias (`RF-09-03`, design — decisão 3).
      Verifica-se abrindo trilha com missões em etapas diferentes: cada missão aparece só na
      etapa dela, e a etapa sem missão declara que está vazia.
- [ ] 2.2 Passar à `ListaDeMissoes` apenas as missões da etapa aberta, mantendo dentro dela a
      ordem crescente da posição (`RF-09-02`, `RF-09-03`, design — decisão 3).
- [ ] 2.3 Fazer o formulário de nova missão nascer com a etapa aberta pré-selecionada, ainda
      alterável antes de confirmar (`RF-09-03`, design — decisão 4). Verifica-se pedindo nova
      missão na etapa de marcos: o campo já vem em marcos.

## 3. Painel permanente das travas de publicação

- [ ] 3.1 Derivar na `TelaDaTrilha` as três travas pendentes — missão de sondagem, desafio de
      coleta em alguma missão e culminância — do payload que a tela já tem, refazendo-as a cada
      declaração do Mestre, como `coberturaDaTrilha` já faz (`RF-09-06`, `RF-09-07`, `RF-09-82`,
      design — decisão 1).
- [ ] 3.2 Apresentar o painel onde a publicação é oferecida — trilha em rascunho ou
      despublicada —, nomeando cada trava pendente em linguagem simples ou declarando que não
      falta nada, sem desabilitar o botão de publicar e sem depender da etapa aberta
      (`RF-09-06`, `RF-09-07`, `RF-09-08`, design — decisões 2 e 5). A recusa do núcleo continua
      apresentada como hoje.

## 4. Testes

- [ ] 4.1 Em `trilhas.test.tsx`, cobrir a paginação por etapa: missões separadas pela etapa
      declarada, ordem da posição dentro da etapa, etapa sem missão continua visível e nova
      missão nasce na etapa aberta (`RF-09-02`, `RF-09-03`).
- [ ] 4.2 Em `trilhas.test.tsx`, cobrir o painel de pendências: as três travas apontadas antes
      de qualquer tentativa, a trava declarada sai do painel sem recarregar a tela, o painel
      declara a trilha pronta, e publicar com trava pendente leva o pedido ao núcleo e
      apresenta a recusa dele (`RF-09-06`, `RF-09-07`, `RF-09-08`, `RF-09-82`).
- [ ] 4.3 Em `trilhas.test.tsx`, cobrir a ordem dos blocos da missão: template abre, ODS fecha
      os blocos, pré-visualização vem depois de todos, desbloqueio antes da recompensa e
      bibliografia logo depois do conteúdo (`RF-09-25`).

## 5. Documentação

- [ ] 5.1 Marcar a fatia 17 do PRD-09 como implementada em `openspec/cronograma-de-fatias.md`,
      com o slug desta change. Nada mais muda em `docs/`: a change não toma decisão nova, não
      altera requisito de PRD nem relação entre documentos, e não cria arquivo — o documento 09,
      o PRD-09, `docs/prds/index.md`, o documento 99 e a `nav` do `mkdocs.yml` ficam como estão.
