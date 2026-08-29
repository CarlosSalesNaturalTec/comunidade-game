# App 08 — Área do Apoiador

Aplicação do Apoiador (PRD-14): entrada por login social ou por usuário e senha, e — nesta
fatia — a proposição e o acompanhamento do desafio extra. React com TypeScript sobre Vite
(documento 03 §1).

## Comandos

- `npm run dev` — ambiente de desenvolvimento
- `npm run build` — build de produção (saída estática)
- `npm run test` — suíte Vitest
- `npm run format` / `npm run check` — Biome, na esteira de `.github/workflows/`

## Variáveis de ambiente

- `VITE_CHAVE_DE_APLICACAO` — chave desta aplicação, por ambiente (documento 03 §1, princípio
  2). Pública por construção, como em toda aplicação Web do Ciclo 01. Em produção, vem do
  segredo do repositório `APP08_CHAVE_DE_APLICACAO`.
- `VITE_GOOGLE_CLIENT_ID` — _client ID_ do OAuth do Google, o mesmo que o núcleo confere em
  `google_client_id`.
- `VITE_URL_DO_NUCLEO` — endereço do Backend API. Em produção, `https://api.comunidadegame.org`.

## Implantação

Ainda não implantada: o alvo de _hosting_ do Apoiador não existe em `.firebaserc` — entra
quando uma fatia de infraestrutura o criar, como aconteceu para a App 03.
