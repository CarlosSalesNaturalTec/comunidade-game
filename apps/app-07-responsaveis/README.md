# App 07 — Área dos responsáveis

Aplicação do responsável (PRD-13): entrada por login social ou por usuário e senha criada pela
gestão, a lista dos vinculados com o grau de parentesco e — nesta fatia — o painel de evolução
de cada um. React com TypeScript sobre Vite (documento 03 §1).

## Comandos

- `npm run dev` — ambiente de desenvolvimento
- `npm run build` — build de produção (saída estática)
- `npm run test` — suíte Vitest
- `npm run format` / `npm run check` — Biome, na esteira de `.github/workflows/`

## Variáveis de ambiente

- `VITE_CHAVE_DE_APLICACAO` — chave desta aplicação, por ambiente (documento 03 §1, princípio
  2). Pública por construção, como em toda aplicação Web do Ciclo 01. Em produção, vem do
  segredo do repositório `APP07_CHAVE_DE_APLICACAO`.
- `VITE_GOOGLE_CLIENT_ID` — _client ID_ do OAuth do Google, o mesmo que o núcleo confere em
  `google_client_id`.
- `VITE_URL_DO_NUCLEO` — endereço do Backend API. Em produção, `https://api.comunidadegame.org`.

## Implantação

Publicada pelo `.github/workflows/app-07-deploy.yml` em `responsavel.comunidadegame.org`, via
Firebase Hosting — alvo `responsavel` de `firebase.json`, chave do segredo
`APP07_CHAVE_DE_APLICACAO`.
