## 1. Base compartilhada da contagem

- [x] 1.1 Criar o módulo `backend/src/nucleo/protecao/` com a janela deslizante em memória —
      mapa de chave de contagem para fila de instantes, descartando na leitura o que saiu da
      janela (design — Decisions).
- [x] 1.2 Implementar a identificação da origem por resumo criptográfico do endereço de rede
      com sal, sem gravar nada e sem cookie ou identificador persistente (`RN-01-45`).
- [x] 1.3 Implementar a rotação do sal por período, retendo o sal anterior por uma janela para
      não zerar o freio de quem está sendo freado (`RN-01-45`, design — Decisions).
- [x] 1.4 Acrescentar a `Configuracao` os parâmetros da cota, dos limites por origem, do atraso
      inicial, do crescimento e do teto, com padrão igual ao documento 03 §8 (`RF-01-55`,
      `RF-01-65`).
- [x] 1.5 Registrar na subida a linha de log que declara a premissa de contêiner único, para
      que a violação apareça em produção (design — Risks).

## 2. Cota de leitura por faixa da chave

- [x] 2.1 Implementar a dependency da cota, lendo a `natureza` de `ContextoDaChave` para
      escolher a faixa e contando apenas `GET` e `HEAD` (`RF-01-55`).
- [x] 2.2 Declarar a dependency da cota em `incluir_roteador_de_dados`, **depois** de
      `exigir_chave_de_aplicacao`, para que a chave inválida receba 401 antes de a cota contar
      (`RF-01-55`, `RF-01-48`, delta de `chave-de-aplicacao`).
- [x] 2.3 Verificar que leitura dentro da cota é processada e que a que excede recebe 429
      (`RF-01-55`).
- [x] 2.4 Verificar que a faixa de terceiro é recusada no volume em que a do projeto ainda é
      processada (`RF-01-55`).
- [x] 2.5 Verificar que a escrita não consome a cota, mesmo em volume que esgotaria a leitura
      (`RF-01-55`).
- [x] 2.6 Verificar que a janela deslizante libera a chave sem intervenção humana (`RF-01-55`).
- [x] 2.7 Verificar que chave desconhecida e chave revogada recebem 401 e nunca 429, em
      qualquer volume (`RF-01-48`, delta de `chave-de-aplicacao`).

## 3. Freio por origem

- [x] 3.1 Implementar a fábrica de dependency do freio, recebendo a superfície e aplicando o
      limite e a janela dela (`RF-01-65`, `RN-01-27`).
- [x] 3.2 Implementar o atraso progressivo por origem — valor inicial, crescimento a cada
      repetição e teto (`RF-01-65`, `RN-01-27`).
- [x] 3.3 Verificar que a origem dentro do limite é processada e que a que excede recebe 429
      com o tempo de espera (`RF-01-65`).
- [x] 3.4 Verificar que o tempo de espera cresce a cada repetição e para no teto (`RN-01-27`).
- [x] 3.5 Verificar que origens distintas não dividem o mesmo freio e que as superfícies contam
      em separado (`RF-01-65`).
- [x] 3.6 Verificar que nenhuma resposta do freio exige CAPTCHA, login ou dado do visitante
      (`RN-01-27`).
- [x] 3.7 Verificar que nada do freio chega ao banco: nem endereço de rede, nem resumo, nem
      preferência (`RN-01-45`).
- [x] 3.8 Verificar que a solicitação de chave não recebe freio por origem em nenhum volume
      (`RN-01-46`, `RN-01-36`).

## 4. Contrato do 429

- [x] 4.1 Acrescentar o erro de excesso ao módulo de erros, respondendo 429 com o corpo único
      já existente, sem alterar o formato de `CorpoDeErro` (`RF-01-27`, `RF-01-55`).
- [x] 4.2 Informar o tempo de espera no cabeçalho `Retry-After` e em linguagem simples na
      mensagem do corpo (`RF-01-65`, design — Decisions).
- [x] 4.3 Verificar que a mensagem do 429 está em português do Brasil e é legível por quem não
      conhece o sistema (`RF-01-27`).

## 5. Documentação e esteira

- [x] 5.1 Conferir que `docs/` não precisa de alteração: a decisão já entrou nos documentos 03
      e 09 e nos PRDs 01 e 03 antes desta change, `docs/prds/index.md` não muda de situação, o
      documento 99 não teve relação alterada e nenhum arquivo novo entrou na `nav`.
- [x] 5.2 Rodar `ruff format --check .`, `ruff check .` e `pytest` no `backend/`, e
      `npm run fix`, `npm run lint` e `mkdocs build --strict` na raiz, antes de abrir o PR.
