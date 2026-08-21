## Why

**Origem: PRD-02 §10 e documento 03 §1, princípio 2.** Como os demais requisitos não
funcionais, não têm `RF-XX-nn` nem `RN-XX-nn`; a change atende o requisito
`A aplicação é inteiramente autenticada e se identifica por chave`, de
`openspec/specs/aplicacao-de-gestao/spec.md`, acrescentando o limite que faltava à única
dependência externa em tempo de execução da App 03. Autorizada pelo fundador em 2026-08-21.

O projeto na GCP foi bloqueado por suspeita de automação e reativado por recurso. **A causa
não está confirmada** e esta change não afirma tê-la encontrado. O que ela faz é fechar o
único caminho do repositório em que uma conferência automatizada alcança um endpoint de
identidade do Google, e tirar do caminho de implantação duas coisas que não deveriam estar
lá.

A conferência à mão de acessibilidade da fatia anterior percorreu as três telas com Chromium,
e a tela de entrada monta `BotaoDeEntradaGoogle`, que injeta
`https://accounts.google.com/gsi/client` e chama `initialize` com o client ID do ambiente. Com
client ID configurado, isso é navegador automatizado, em IP de datacenter, acionando o
provedor de identidade — a forma exata do que sistemas antiabuso classificam como bot. O
componente **já** tem o curto-circuito que evita isso quando não há client ID, mas nenhum
teste o trava e nenhuma regra manda usá-lo: o teste de entrada substitui o componente inteiro
por um duplo, então o curto-circuito nunca é exercitado.

## What Changes

- **O curto-circuito vira requisito e ganha teste.** Sem client ID configurado, a App 03 não
  injeta o script do provedor de identidade. Hoje o comportamento existe e pode ser removido
  sem que nada acuse.
- **A conferência à mão passa a rodar sem client ID**, gravado no runbook da App 03. Contraste,
  alvo de toque, foco e desenho da fonte se medem igual sem o botão do Google, então a regra
  não custa cobertura.
- **A versão da `firebase-tools` é fixada** no workflow de implantação da App 03, hoje em
  `@latest`, o que baixa a CLI a cada publicação e deixa o comportamento mudar sozinho entre
  duas execuções.
- **A dívida do endereço do núcleo entra no documento 09.** O workflow aponta
  `VITE_URL_DO_NUCLEO` para `https://comunidade-game-api.web.app`, marcado `TEMPORÁRIO` por
  causa do filtro corporativo que bloqueia o domínio recém-registrado. Está em produção e nada
  rastreia a volta para `api.comunidadegame.org`.

Fora do escopo: qualquer conclusão sobre a causa do bloqueio, que não está estabelecida;
mudança no fluxo de autenticação, no client ID ou nas origens autorizadas; e a volta do
endereço do núcleo, que depende do TI liberar o domínio e por isso é pendência registrada, não
tarefa.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-de-gestao`: acrescenta o requisito de que a única dependência externa em tempo de
  execução só seja acionada quando o ambiente a configurar — comportamento que o código já tem
  e que nenhum requisito nem teste sustentava.

## Impact

- `apps/app-03-gestao/src/autenticacao/` — teste novo de `BotaoDeEntradaGoogle`; o componente
  não muda, porque o curto-circuito já está lá.
- `apps/app-03-gestao/README.md` — a regra da conferência à mão.
- `.github/workflows/app-03-deploy.yml` — versão fixa da `firebase-tools`.
- `docs/09-topicos-em-aberto-e-sugestoes.md` — a dívida do endereço do núcleo e a regra da
  conferência.
- **Sem impacto** em rota, contrato de API, modelo de dados, chave de aplicação, sessão,
  client ID ou origens autorizadas. O backend não é tocado, e o `firebase.json` não muda.
- O merge em `main` dispara `app-03-deploy.yml`, porque a change toca o próprio workflow.
