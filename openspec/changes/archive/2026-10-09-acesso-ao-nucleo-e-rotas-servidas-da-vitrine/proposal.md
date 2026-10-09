# Proposal

## Why

Origem: **PRD-03 — Vitrine pública (App 06)**. **Não é fatia nova**: é correção de
regressão da fatia 9 (`2026-09-30-fundacao-astro-e-camada-de-descoberta`), que o
cronograma marca como implementado. Decisão do fundador de 2026-10-09: change
corretiva própria, não reabertura da fatia 9, e os dois defeitos no mesmo recorte —
têm a mesma origem e separá-los deixaria a vitrine meio quebrada entre dois PRs.

A migração para Astro deixou a vitrine publicada em dois pedaços quebrados, e os dois
defeitos saíram do mesmo commit (`80692a3`):

1. **Nenhuma ilha alcança o núcleo no navegador.** O commit apagou
   `apps/app-06-vitrine/src/main.tsx`, que continha a única chamada de
   `configurarAcessoAoNucleo` do lado do cliente. Hoje a função só é chamada em
   `src/build/dados.ts`, que roda em Node no `astro build` e sai do _bundle_ de
   cliente. No navegador a configuração fica nula, a camada de acesso lança antes de
   qualquer requisição sair, e **toda** seção que lê dado mostra "Não foi possível
   carregar os cards agora". O institucional escapa porque vem do build.

2. **Nove de dez endereços caem na casca de pessoa.** A fatia 9 fixou
   `build.format: "file"` apostando que o arquivo real é servido antes do `rewrite`.
   O Firebase Hosting serve arquivo real antes do `rewrite`, mas só por
   correspondência exata ou índice de diretório: `/pesquisadores` não corresponde a
   `pesquisadores.html` sem `cleanUrls`, que não existe no repositório. O pedido cai
   no último `rewrite` (`**` → `/app.html`), a casca não casa nenhum prefixo de
   pessoa e responde "Endereço não encontrado". Só `/` escapa, porque o Firebase
   serve `index.html` na raiz nativamente.

Nenhum requisito novo: a change **restaura** comportamento que o PRD-03 já exige.
Não é recusa do núcleo — CORS é aberto, a chave `app-06-vitrine` está semeada e as
rotas existem.

## What Changes

- **Defeito 1** — a App 06 passa a configurar o acesso ao núcleo também no
  navegador, no gargalo único por onde toda ilha já passa. Restaura `RF-03-02`,
  `RF-03-03`, `RF-03-04`, `RF-03-07`, `RF-03-08`, `RF-03-10`, `RF-03-15`, `RF-03-22`,
  `RF-03-47` e `RN-03-33`.
- **Defeito 2** — o alvo `vitrine` do `firebase.json` passa a servir cada rota
  publicada no endereço público dela. Restaura `RF-03-25`, `RF-03-26`, `RF-03-15`,
  `RF-03-42`, `RF-03-52`, `RF-03-53`, `RF-03-67`, `RF-03-77`, `RF-03-27` a
  `RF-03-35` e o PRD-03 §10 — hoje o `sitemap.xml` convida o buscador a dez
  endereços que respondem com a casca `noindex`.
- **Dois pontos cegos do CI fechados**, sem os quais a regressão volta na fatia
  seguinte:
  - nenhum teste cruza **arquivo emitido × caminho servido** — `saidaDoBuild` lê
    `dist/pesquisadores.html` direto do disco e nunca pergunta por qual endereço se
    chega até ele; `hospedagem` lê o `firebase.json` e confere `rewrites` e ordem;
  - nenhum teste exercita uma ilha **sem** configurar o acesso — `semRastro` é o
    único que chega à camada de rede, e ele mesmo fornece o que a produção não
    fornece.
- Nenhuma mudança de `comum/`: a camada de acesso se comportou como a spec dela
  manda — recusou partir sem configuração, em vez de chamar com chave vazia.

**Sem BREAKING**: os dois ajustes restauram contrato publicado, não o alteram.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-vitrine`: duas requirements **novas** na capacidade existente,
  que dizem o que a regressão atravessou sem ser vista. Nenhuma requirement vigente
  muda de comportamento — o que faltava era a afirmação, não a regra:
  - a de saída estática cobre hoje só o caso **negativo** — "endereço sem arquivo
    publicado continua respondendo"; falta o **positivo**, que o endereço com arquivo
    publicado é servido por aquele arquivo e não pela casca de pessoa;
  - a da chave de aplicação exige que toda chamada leve a chave, mas não que a
    configuração alcance o **navegador**, onde as ilhas vivem.

## Impact

| Alvo | O que muda |
| --- | --- |
| `apps/app-06-vitrine/src/api/nucleo.ts` | configuração do acesso ao núcleo no cliente |
| `firebase.json` (alvo `vitrine`) | cada rota publicada servida no endereço público dela |
| `apps/app-06-vitrine/src/descoberta/enderecos.ts` | a casca de pessoa barrada no endereço novo que a correção cria (design — decisão 3) |
| `apps/app-06-vitrine/src/testes/` | os dois pontos cegos acima |
| `openspec/cronograma-de-fatias.md` | linha sem número no bloco do PRD-03, com o slug |

Nada no `backend/`, em `comum/`, nas outras sete aplicações, nos PRDs ou nos
documentos 01–16: nenhuma decisão nova é tomada, e nenhuma relação entre documentos
muda. As nove seções de leitura da vitrine, as três páginas de pessoa, a página de
comunidade, os dois formulários públicos, a porta do convite e a Área do Apoiador
Desenvolvedor voltam a funcionar em produção.
