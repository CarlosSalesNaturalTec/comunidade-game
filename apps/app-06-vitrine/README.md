# App 06 — Vitrine pública

A cara pública do projeto (PRD-03) e a raiz do domínio da plataforma: a única aplicação que
qualquer pessoa abre sem se identificar. Nesta fatia, o esqueleto — os três recortes de leitura
como navegação e o botão "Entrar", que encaminha cada persona à aplicação dela. React com
TypeScript sobre Vite, no temperamento **Arena** (documentos 03 §1 e 15 §6).

**A vitrine não guarda nada de quem visita**: sem login, sem cadastro, sem cookie, sem
rastreador e sem preferência no aparelho (`RF-03-51`, `RN-03-22`). Por isso ela não depende de
`comum/autenticacao`, que guarda sessão, nem monta o provedor de narração, que guarda a
preferência do aparelho.

## Comandos

- `npm run dev` — ambiente de desenvolvimento
- `npm run build` — build de produção (saída estática)
- `npm run test` — suíte Vitest
- `npm run format` / `npm run check` — Biome, na esteira de `.github/workflows/`

## Variáveis de ambiente

- `VITE_CHAVE_DE_APLICACAO` — chave desta aplicação, por ambiente (documento 03 §1, princípio
  2). Pública por construção, como em toda aplicação Web do Ciclo 01. Em produção, vem do
  segredo do repositório `APP06_CHAVE_DE_APLICACAO`.
- `VITE_URL_DO_NUCLEO` — endereço do Backend API. Em produção, `https://api.comunidadegame.org`.
- `VITE_URL_DA_APP_01_AULA`, `VITE_URL_DA_APP_03_GESTAO`, `VITE_URL_DA_APP_05_GUERREIRO`,
  `VITE_URL_DA_APP_07_RESPONSAVEL`, `VITE_URL_DA_APP_08_APOIADOR` e `VITE_URL_DA_APP_09_MESTRE`
  — os seis destinos do "Entrar" (documento 03 §1.1). Uma por ambiente, e nenhuma gravada no
  código: as esteiras de publicação usam hoje os endereços `*.web.app`. Sem endereço, a tela
  nomeia o destino em texto, sem link quebrado.

Não há `VITE_GOOGLE_CLIENT_ID`: a vitrine nunca autentica ninguém (`RN-03-27`).

## Implantação

Publicada pelo `.github/workflows/app-06-deploy.yml` na raiz de `comunidadegame.org`, via
Firebase Hosting — alvo `vitrine` de `firebase.json`, chave do segredo
`APP06_CHAVE_DE_APLICACAO`.
