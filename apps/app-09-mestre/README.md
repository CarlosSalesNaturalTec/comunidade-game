# App 09 — Área do Mestre

Aplicação do Mestre (PRD-09): entrada por login social e a autoria de trilha, missão e
atividade. React com TypeScript sobre Vite (documento 03 §1).

## Comandos

- `npm run dev` — ambiente de desenvolvimento
- `npm run build` — build de produção (saída estática)
- `npm run test` — suíte Vitest
- `npm run format` / `npm run check` — Biome, na esteira de `.github/workflows/`

## Variáveis de ambiente

- `VITE_CHAVE_DE_APLICACAO` — chave desta aplicação, por ambiente (documento 03 §1, princípio
  2). Pública por construção, como em toda aplicação Web do Ciclo 01 (App 03 §
  "Variáveis de ambiente"). Em produção, vem do segredo do repositório
  `APP09_CHAVE_DE_APLICACAO`.
- `VITE_GOOGLE_CLIENT_ID` — _client ID_ do OAuth do Google, o mesmo que o núcleo confere em
  `google_client_id`.
- `VITE_URL_DO_NUCLEO` — endereço do Backend API. Em produção, `https://api.comunidadegame.org`.

## Implantação

Publicada pelo `.github/workflows/app-09-deploy.yml` em `mestre.comunidadegame.org`, via
Firebase Hosting — alvo `mestre` de `firebase.json`.
