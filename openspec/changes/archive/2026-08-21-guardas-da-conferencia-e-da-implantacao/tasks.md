## 1. O limite da dependência externa de identidade

- [x] 1.1 Criar o teste de `BotaoDeEntradaGoogle` que monta o componente de verdade — sem o
      duplo de `entrada.test.tsx` — e confere os dois casos: sem client ID configurado nenhum
      `<script>` do provedor é acrescentado ao documento e a tela segue apresentável; com
      client ID configurado o caminho de entrada é oferecido. Cobre os dois cenários do
      requisito "A dependência externa de identidade só é acionada quando configurada"
      (documento 03 §1 princípio 2, PRD-02 §10).

## 2. O caminho de implantação

- [x] 2.1 Fixar a versão da `firebase-tools` em `.github/workflows/app-03-deploy.yml`, hoje em
      `@latest`, mantendo a justificativa que já está no comentário sobre não usar
      `action-hosting-deploy` (design — Decisions).

## 3. Runbook e documentação

- [x] 3.1 Acrescentar ao `README.md` da App 03, na seção de conferência à mão que já existe, a
      regra de que a conferência roda sobre build com `VITE_GOOGLE_CLIENT_ID` vazio, com o
      motivo em uma linha (design — Decisions).
- [x] 3.2 Registrar no `docs/09-topicos-em-aberto-e-sugestoes.md` a decisão da conferência sem
      client ID, entre as já decididas, e a **pendência** do endereço do núcleo em produção —
      `VITE_URL_DO_NUCLEO` apontando para `comunidade-game-api.web.app` até o TI liberar
      `api.comunidadegame.org` no filtro. Nenhum arquivo novo em `docs/`, portanto nenhuma
      entrada na `nav`; `docs/prds/index.md` e o documento 99 não mudam, porque nenhum PRD
      muda de situação e nenhuma relação entre documentos muda.
