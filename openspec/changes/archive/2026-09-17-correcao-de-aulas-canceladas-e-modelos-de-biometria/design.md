## Context

Ver proposal.md — Why. Dois defeitos, tratados em blocos independentes (não compartilham
código; a esteira do backend e a do frontend rodam cada uma no seu bloco).

Para os modelos da Human: `comum/biometria/biometria.ts` já declara
`modelBasePath: "/modelos-de-biometria/"` e é a única porta de entrada da biblioteca (`vite
build` resolve `@vladmandic/human` para o ESM de navegador via `alias`, em cada
`vite.config.ts` de app). Falta só o arquivo existir sob esse caminho no `public/` de cada app
que consome o módulo — hoje `app-01-aula-presencial` e `app-05-guerreiro`. Os cinco modelos
habilitados em `biometria.ts` (`face.detector`, `face.mesh`, `face.description`,
`face.antispoof`, `face.liveness`) são exatamente os cinco do relato: `blazeface`, `facemesh`,
`faceres`, `antispoof`, `liveness`.

## Goals / Non-Goals

**Goals:**
- `aulas_vigentes` para de considerar aula cancelada.
- Os cinco modelos da Human chegam ao navegador a partir do próprio build, sem 404, para os
  dois apps que os usam.

**Non-Goals:**
- Não resolve a pendência de peso do bundle do PRD-04 §14 — só provisiona os arquivos que já
  eram esperados; carregamento tardio/lazy é otimização posterior, fora deste recorte.
- Não move a hospedagem dos modelos para CDN externa ou bucket próprio — descartado na
  exploração que antecedeu esta change (ver Decisions).
- Não altera `comum/biometria/biometria.ts`, `TelaDeCaptura.tsx` nem
  `TelaDeEntradaDoGuerreiro.tsx`: nenhum dos três tem defeito de lógica: o `modelBasePath` já
  está certo.

## Decisions

- **Excluir `cancelada` no filtro SQL de `aulas_vigentes`**, em vez de filtrar em Python depois
  da query: mesma função, mesma assinatura, só mais uma cláusula no `.filter(...)` já existente
  em `backend/src/nucleo/aulas/regra.py:213`. Sem alternativa considerada — é a forma direta
  que a própria função já usa para os outros dois critérios (início e fim).

- **Modelos embarcados no build (`public/modelos-de-biometria/`), copiados de
  `node_modules/@vladmandic/human/models/`** — não CDN pública de terceiro, não bucket próprio.
  Motivo: documento 03 §3.4 já exige funcionar em rede instável e aparelho modesto; somar uma
  dependência de rede a um domínio de terceiro (CDN) ou a um serviço a mais para operar
  (bucket) vai contra esse requisito não funcional, e nenhum dos dois ganha algo que o build
  embarcado não tem — só o custo de decidir esse é um passo de infraestrutura novo, não uma
  correção de bug. Alternativas descartadas: CDN pública (jsdelivr/unpkg) — mais um domínio a
  alcançar exatamente onde a rede falha; bucket do Cloud Storage do projeto — mesmo problema de
  rede, com o custo adicional de operar um serviço novo, sem ganho sobre o build embarcado.

- **Onde mora o passo de cópia**: um módulo em `comum/biometria/` (não em cada app) que resolve
  o caminho de instalação de `@vladmandic/human` — o mesmo padrão que `vite.config.ts` já usa
  com `createRequire(import.meta.url).resolve(...)` para o alias do ESM — e copia os arquivos
  dos cinco modelos (cada um com o `.json` e o(s) `.bin` companheiro(s)) para um diretório de
  destino recebido por parâmetro. Cada app chama esse módulo num plugin Vite próprio
  (hook `buildStart`, que roda tanto em `vite build` quanto em `vite dev`), apontando o destino
  para o próprio `public/modelos-de-biometria/`. Alternativa descartada: um script npm
  `postinstall` do monorepo — dispara uma vez por instalação de dependências, não a cada
  branch/checkout que troque a versão do pacote, e no CI de PR o passo precisa rodar sempre que
  o build roda, não só quando `npm install` roda.

## Risks / Trade-offs

- **Cada modelo pode ter mais de um arquivo binário além do `.json`** (convenção de
  particionamento do tfjs `GraphModel`) — copiar só o `.json` deixaria o modelo quebrado do
  mesmo jeito, só que sem 404 no arquivo principal. → A tarefa de implementação confere, para
  cada um dos cinco, quais arquivos o `.json` referencia (campo `weightsManifest` do próprio
  modelo) e copia todos, não só o nome citado no relato do bug.
- **Peso do bundle sobe** com os modelos embarcados — é a pendência já registrada no PRD-04
  §14, não nova. → Fica registrada como está; lazy-load do módulo de biometria (que já só é
  importado dentro de `TelaDeCaptura`/`TelaDeEntradaDoGuerreiro`, nunca no bundle inicial) é
  otimização possível depois, sem mudar esta correção.
- **Divergência de versão entre o modelo copiado e o que `@vladmandic/human` espera**, se a
  dependência for atualizada sem repetir a cópia. → O passo de cópia roda a cada build
  (`buildStart`), então nunca fica desatualizado enquanto o build for a única forma de gerar o
  `public/` servido.

## Migration Plan

Sem migração de dado. Ordem de entrega dentro da mesma change, sem dependência entre os dois
blocos:
1. Backend: filtro em `aulas_vigentes`, teste novo, delta de spec.
2. Frontend: módulo de cópia em `comum/biometria/`, plugin Vite nos dois `vite.config.ts`,
   build real conferindo que os cinco modelos aparecem em `dist/modelos-de-biometria/` (e, no
   servidor de `vite dev`, em resposta a `GET /modelos-de-biometria/*.json`).
