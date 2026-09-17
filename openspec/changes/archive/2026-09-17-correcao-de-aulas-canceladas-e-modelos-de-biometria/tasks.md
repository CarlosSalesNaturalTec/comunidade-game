## 1. Backend — aula cancelada não é vigente

- [x] 1.1 Em `backend/src/nucleo/aulas/regra.py`, `aulas_vigentes` passa a excluir
  `Aula.situacao == SituacaoDaAula.cancelada` do filtro (`RF-01-32`).
- [x] 1.2 Em `backend/tests/test_aula.py`, teste novo ao lado de
  `test_aula_fora_do_horario_nao_e_vigente`: cria aula em curso, cancela com `cancelar_aula`, e
  confere que `aulas_vigentes` não a devolve mais (`RF-01-32`, scenario "Aula cancelada não é
  vigente"). Roda com `uv run pytest tests/test_aula.py -x`.

## 2. Frontend — modelos da Human provisionados no build

- [x] 2.1 Módulo novo em `comum/biometria/` que, a partir do caminho de instalação de
  `@vladmandic/human` (resolvido por `createRequire`, mesmo padrão do `alias` em
  `vite.config.ts`), localiza os cinco modelos habilitados em `biometria.ts` — `blazeface`,
  `facemesh`, `faceres`, `antispoof`, `liveness` —, lê o `weightsManifest` de cada `.json` para
  descobrir os arquivos de peso companheiros, e copia o conjunto completo para um diretório de
  destino recebido por parâmetro.
- [x] 2.2 Teste (Vitest) desse módulo: copia exatamente os arquivos dos cinco modelos
  esperados (incluindo os pesos companheiros) para um diretório temporário, e nenhum outro
  arquivo do diretório de modelos da Human vai junto.
- [x] 2.3 Plugin Vite em `apps/app-01-aula-presencial/vite.config.ts` (hook `buildStart`, para
  rodar em `vite build` e em `vite dev`) chamando o módulo de 2.1 com destino
  `public/modelos-de-biometria/`. Verificar com `vite build` que os cinco modelos aparecem em
  `dist/modelos-de-biometria/`.
- [x] 2.4 Mesmo plugin em `apps/app-05-guerreiro/vite.config.ts`, mesmo destino relativo ao
  próprio app. Mesma verificação com `vite build`.

## 3. Verificação dos dois sintomas relatados

- [x] 3.1 Com `vite dev` em `app-01-aula-presencial`: onboarding → `TelaDeCaptura` conclui a
  captura sem 404 nos `.json` dos modelos; entrada por nick em trilha e em quiz ao vivo →
  `tentarReconhecimento` completa (aprovando ou recusando a vivacidade) sem o
  `TypeError: Cannot read properties of undefined (reading 'inputNodes')`. Cobre os dois
  sintomas do relato original, que nasceram da mesma causa (2.1–2.4). Verificado com Human
  real em Chromium headless contra o `vite dev`: os cinco `.json` respondem 200
  (`carregados: [blazeface, antispoof, liveness, facemesh, faceres]`, `naoCarregados: []`) e
  `human.detect()` conclui sem lançar.

## 4. Documentação

- [x] 4.1 Em `openspec/cronograma-de-fatias.md`, muda a situação da linha desta change (bloco
  PRD-04) de `em andamento` para `implementado` — nenhum outro documento muda: o PRD-04 §14
  mantém a pendência de peso do bundle (não resolvida por esta correção), e o delta de
  `aula-e-presenca` desta change é o que sincroniza a spec consolidada ao arquivar.
