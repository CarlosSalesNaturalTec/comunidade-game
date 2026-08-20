# App 03 — Frontend de gestão

Aplicação de gestão do Comunidade Game (PRD-02): entrada do adulto por login social e o
cadastro de Comunidade Virtual. React com TypeScript sobre Vite (documento 03 §1).

## Comandos

- `npm run dev` — ambiente de desenvolvimento
- `npm run build` — build de produção (saída estática)
- `npm run test` — suíte Vitest
- `npm run format` / `npm run check` — Biome, na esteira de `.github/workflows/`

## Variáveis de ambiente

- `VITE_CHAVE_DE_APLICACAO` — chave desta aplicação, por ambiente (documento 03 §1, princípio
  2). **Pública por construção**: assada no _bundle_ estático no momento do build, qualquer
  visitante a lê no JavaScript servido. Coerente com o princípio 2 — a chave identifica a
  aplicação e sustenta a cota de leitura; quem protege a pessoa é a credencial da persona, que
  nunca sai do `sessionStorage`. Em produção, vem do segredo do repositório
  `APP03_CHAVE_DE_APLICACAO`, semeado pelo `python -m nucleo.cli` do backend.
- `VITE_GOOGLE_CLIENT_ID` — _client ID_ do OAuth do Google, o mesmo que o núcleo confere em
  `google_client_id`.
- `VITE_URL_DO_NUCLEO` — endereço do Backend API. Em produção, `https://api.comunidadegame.org`.

## Implantação

Publicada pelo `.github/workflows/app-03-deploy.yml` em `gestao.comunidadegame.org`, via
Firebase Hosting — alvo `app-03` de `firebase.json`. Provisionamento e ordem da primeira
execução em `backend/README.md`.
