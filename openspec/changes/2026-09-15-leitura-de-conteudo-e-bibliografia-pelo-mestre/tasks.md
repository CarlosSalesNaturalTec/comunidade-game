## 1. Núcleo — conteúdo e bibliografia na leitura das trilhas próprias

- [ ] 1.1 `RF-09-14`, `RF-09-15`: em `backend/src/nucleo/trilhas/rotas.py`,
      `listar_minhas_trilhas_rota` passa a chamar `_saida_da_missao` com
      `conteudos=consultar_conteudos_da_missao(sessao_bd, missao.id)`, igual a
      `obter_trilha_publica_rota` (design — decisão 1). Missão sem conteúdo sai com lista
      vazia. Verificar pela resposta de `GET /v1/trilhas/minhas` trazendo texto, imagem e
      vídeo já gravados de uma missão de trilha em rascunho.
- [ ] 1.2 `RF-09-21`: na mesma rota, montar a bibliografia de cada missão com
      `consultar_bibliografia_da_missao` e `saida_da_bibliografia_publica(sessao_bd,
      bibliografia, ponto_de_apoio_id=None)` por entrada (design — decisão 2). Missão sem
      bibliografia sai com lista vazia. Verificar pela resposta trazendo duas entradas, uma
      vinculada a exemplar e outra não.
- [ ] 1.3 `RF-09-22`, `RF-09-23`: confirmar que, com `ponto_de_apoio_id=None`, a entrada
      vinculada a exemplar sai com `disponivel: null` e `apoiador_nome` presente quando o
      exemplar tem aporte de origem (design — decisão 2). Verificar com um exemplar que tem
      aporte de origem de Apoiador e outro sem aporte.

## 2. App 09 — reabrir conteúdo e bibliografia declarados

- [ ] 2.1 `RF-09-14`, `RF-09-15`, `RF-09-21`: em `apps/app-09-mestre/src/trilhas/api.ts`,
      remover o comentário que descreve a ausência de `conteudos` em `GET /trilhas/minhas`
      como intencional (design — decisão 5). Verificar que o tipo da missão não precisa
      mudar — `conteudos` e `bibliografia` já são opcionais e a leitura passa a preenchê-los.
- [ ] 2.2 `RF-09-14`, `RF-09-15`: verificar que `ListaDeMissoes.tsx` e
      `PreVisualizacaoDaMissao.tsx` apresentam o conteúdo vindo da leitura sem alteração de
      código — ambos já leem `missao.conteudos ?? []`. Cobrir por teste que uma missão
      carregada da listagem (sem passar por `onSalvo`) já exibe o conteúdo gravado.
- [ ] 2.3 `RF-09-21`, `RF-09-22`, `RF-09-23`: em `Bibliografia.tsx`, trocar o ternário
      booleano de `entrada.disponivel` por três estados — disponível, não disponível e
      indeterminado (`disponivel == null`) —, mostrando no terceiro caso que a disponibilidade
      depende do ponto de apoio de cada Guerreiro(a), sem afirmar nem negar (design —
      decisão 3). Verificar que uma entrada vinda da leitura do Mestre (sempre indeterminada)
      nunca aparece como "não disponível".

## 3. Testes

- [ ] 3.1 `backend/tests/test_trilha_rota.py`: `GET /v1/trilhas/minhas` devolve o conteúdo
      (texto, imagem, vídeo, arquivo e link) e a bibliografia (com e sem vínculo de exemplar)
      já gravados de missões de trilha do Mestre autor, inclusive em rascunho; conteúdo com
      envio ainda não confirmado sai sem referência de arquivo; missão sem conteúdo ou sem
      bibliografia sai com lista vazia, nunca com erro — os cenários de `trilha-e-missao` no
      delta.
- [ ] 3.2 `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`: a tela reabre conteúdo e
      bibliografia declarados em sessão anterior sem depender de `onSalvo`/`onSalva`, a
      pré-visualização reflete o mesmo dado, e a entrada de bibliografia com disponibilidade
      indeterminada não aparece como "não disponível" — os cenários de `area-do-mestre` no
      delta.

## 4. Documentação

- [ ] 4.1 Marcar a linha desta change como `implementado` em
      `openspec/cronograma-de-fatias.md`, com o slug. Nenhum PRD muda — a change aplica
      requisitos que já existem —, nenhuma relação entre documentos muda e nenhum arquivo novo
      entra em `docs/`, de modo que o documento 99, `docs/prds/index.md` e a `nav` do
      `mkdocs.yml` seguem como estão.
