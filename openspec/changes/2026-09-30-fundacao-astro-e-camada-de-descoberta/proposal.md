# Proposal

Origem: **PRD-03 — Vitrine pública (App 06)**, **fatia 9** do
`openspec/cronograma-de-fatias.md`.

A fatia não fecha recorte de `RF`: ela cumpre a fundação que o **documento 03 §1,
princípio 13**, define e o **PRD-03 §10** exige — indexável por buscadores nas seções
institucionais e de comunidade. Os identificadores que ela atende ou preserva são
`RF-03-01`, `RF-03-03`, `RF-03-13`, `RF-03-14`, `RF-03-26`, `RF-03-51`, `RN-03-21`,
`RN-03-22` e `RN-03-33`.

## Why

O documento 03 §1, princípio 13, escreve a vitrine em **Astro**, "por ser a única
indexável por buscadores". A App 06 foi entregue em React com TypeScript sobre Vite, e a
indexabilidade não existe em camada nenhuma: o roteamento é de cliente sobre a History
API, o `firebase.json` reescreve `**` para `/index.html`, o `index.html` traz um único
`<title>` para o site inteiro sobre um `<div id="root">` vazio, e não há `robots.txt`
nem `sitemap.xml`. Toda URL devolve o mesmo documento sem conteúdo.

A vitrine é a superfície por onde qualquer pessoa chega ao projeto (`RF-03-01`), e o
`RF-03-03` promete página individual em endereço próprio e compartilhável. Endereço no
`pushState` não é nem indexável nem compartilhável com prévia: é histórico.

Há uma segunda razão, que a fatia 10 vai cobrar: a App 06 é Arena do cabeçalho ao rodapé
(documento 15 §6) e hoje não tem ilustração. O piso de rede e de aparelho **não é
afrouxado** (documento 15 §1, princípio 4; PRD-03 §10) — o orçamento para a ilustração
sai do JS que a saída estática deixa de baixar.

## What Changes

- **BREAKING (fundação, não contrato público):** a App 06 troca a casca React+Vite por
  **Astro com saída estática e rotas de arquivo**. `index.html`, `App.tsx`, `main.tsx`,
  `src/navegacao/*` e `vite.config.ts` saem; `comum/` e os componentes da App 06
  permanecem React e passam a ser **ilhas**. Nenhum endereço público muda.
- **Fronteira de pré-renderização**, decidida pelo fundador em 2026-09-30:
  - **Institucional** — pré-renderizado inteiro e indexável.
  - **Comunidade** — casca pré-renderizada e indexável; o dado volátil do painel chega
    por ilha e não envelhece entre publicações.
  - **Pessoa** (Guerreiro(a), Mestre, Apoiador) — ilha inteira, carregada no aparelho e
    **não indexada**. É o que o `RF-03-14` já exigia: a revogação retira o perfil "na
    leitura seguinte", e página pré-renderizada não tem leitura seguinte até a
    publicação seguinte. Pré-renderizá-la contrariaria o invariante 12 do documento 99.
- **Camada de descoberta**, na mesma fatia: `robots.txt`, `sitemap.xml` com apenas o que
  é indexável, e `<head>` por rota com título, descrição, canônica e Open Graph. Sai
  junto da migração de propósito: separá-las abriria uma janela em que a indexação já
  funciona e a exclusão das páginas de pessoa ainda não.
- **Esteiras**: `app-06-deploy.yml` e `frontend-ci.yml` passam a construir com Astro; o
  `rewrite` `**` do `firebase.json` deixa de ser a rota de tudo e vira **fallback** de
  identificador desconhecido, atrás dos arquivos reais que o Firebase Hosting serve
  primeiro.
- **Preservado sem exceção**: nenhum recurso de terceiro em tempo de execução
  (`RF-03-51`), nada guardado no aparelho (`RN-03-22`), a chave da aplicação em toda
  chamada ao núcleo (`RN-03-33`), e nenhum espaço reservado a publicidade (`RN-03-21`).
  `robots.txt` e `sitemap.xml` são arquivos do próprio domínio: não medem audiência nem
  identificam visitante.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-vitrine`: passa a declarar **como a vitrine é servida** — quais
  endereços saem em HTML real e indexável, quais são ilha não indexada, e o que o
  `robots.txt` e o `sitemap.xml` declaram. Hoje a capacidade descreve o que cada tela
  mostra e nada diz sobre entrega e descoberta, e por isso a entrega atual a cumpre
  inteira sem cumprir o PRD-03 §10. O requisito da revogação ("retira na leitura
  seguinte") ganha a consequência que faltava: a página de pessoa não é
  pré-renderizada.

## Impact

| Alvo | Efeito |
| --- | --- |
| `apps/app-06-vitrine/` | casca trocada; os cerca de sessenta componentes viram ilhas |
| `apps/app-06-vitrine/src/navegacao/` | substituído por rotas de arquivo do Astro |
| `apps/app-06-vitrine/src/testes/` | 26 arquivos de teste; os de componente seguem |
| `comum/` | **não muda** — tokens, fontes e componentes React são reusados |
| `firebase.json` | `rewrite` `**` passa a ser fallback |
| `.github/workflows/app-06-deploy.yml` | passo de build |
| `.github/workflows/frontend-ci.yml` | `build --workspaces` alcança o Astro; Biome sobre `.astro` |
| Núcleo | **nenhuma rota nova e nenhuma alteração** |
| Documentação | nenhuma decisão nova; fecha a linha da fatia 9 no cronograma |

Fora do escopo, como o PRD-03 §3.2 já exclui: qualquer tela de login, cadastro ou área
restrita, e qualquer coleta de dado do visitante. Fora do escopo desta fatia, pelo
cronograma: a Arena de fato (fatia 10) e o herói (fatia 11).
