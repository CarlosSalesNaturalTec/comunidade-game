## 1. Base do domínio

- [ ] 1.1 Acrescentar as características do avatar à `Persona` de Guerreiro(a), como texto
      estruturado opaco ao núcleo, sem validação de forma (`RN-01-10`, design — Decisions).
- [ ] 1.2 Migração do Alembic para a coluna do avatar, aceitando nulo, com `downgrade`
      (`RN-01-10`).
- [ ] 1.3 Fechar o `tipo` do consentimento no conjunto `autorizacao_de_divulgacao` e
      `biometria`, recusando com 422 o valor fora dele (`RF-01-19`, `RN-01-12`).
- [ ] 1.4 Migração do Alembic para a restrição do `tipo`, falhando alto diante de valor
      existente fora do conjunto, com `downgrade` (`RF-01-19`, design — Risks).
- [ ] 1.5 Escrever a expressão de **autorização vigente**: decisão mais recente de cada
      responsável vinculado, com a recusa prevalecendo, respondendo também por data
      (`RF-01-19`, `RN-01-12`, `RN-01-10`, `RN-13-07`).
- [ ] 1.6 Acrescentar o eixo do **ciclo** à agregação de cobertura de ODS, com o rótulo
      declarado (`RF-01-42`, `RF-01-43`).
- [ ] 1.7 Declarar `CG_CICLO_ROTULO` em `Configuracao`, com `Ciclo 01` como valor inicial
      (`RF-01-43`, design — Decisions).

## 2. Projeção pública

- [ ] 2.1 Criar `vitrine/publico.py` com os tipos de saída pública e a conversão de domínio
      em saída: avatar, nick e progressão, e nada de pessoal (`RN-01-10`, `RN-01-11`).
- [ ] 2.2 Prender o portão da divulgação à **consulta**, não a pós-filtro, de modo que
      paginação e posição de ranking operem sobre o conjunto já visível (`RN-01-10`).

## 3. Rotas da vitrine

- [ ] 3.1 Criar o roteador `vitrine/rotas.py` e registrá-lo por `incluir_roteador_de_dados`,
      herdando chave e cota sem declarar nada (`RF-01-02`, `RN-01-32`).
- [ ] 3.2 `GET /v1/vitrine/guerreiros` — cards de quem tem autorização vigente, paginado e
      filtrável por comunidade (`RF-01-02`, `RF-01-28`, `RN-01-10`, `RN-01-11`).
- [ ] 3.3 `GET /v1/vitrine/guerreiros/{nick}` — perfil por nick exato, com o 404 indistinto
      resolvido em consulta única e o freio `consulta_por_nick` declarado (`RF-01-33`,
      `RF-01-34`, `RN-01-22`, `RF-01-65`).
- [ ] 3.4 `GET /v1/vitrine/rankings` — ordenação por ponto regular, posição calculada sobre o
      conjunto exibido, filtro por comunidade (`RF-01-21`, `RF-01-28`, `RN-01-10`).
- [ ] 3.5 `GET /v1/vitrine/poderes` — poderes com as trilhas vinculadas, sem filtro por
      comunidade sobre a trilha (`RF-01-62`, `RN-01-42`).
- [ ] 3.6 `GET /v1/vitrine/criacoes` — portfólio com autoria creditada, exibido só quando
      todos os creditados têm autorização vigente (`RF-01-26`, `RN-01-13`, `RN-01-10`).
- [ ] 3.7 `GET /v1/vitrine/ods/cobertura` — cobertura agregada por comunidade e ciclo, sem
      recorte por Guerreiro(a) (`RF-01-43`, `RN-01-24`).

## 4. Contrato de leitura dos jogos

- [ ] 4.1 Criar o módulo `jogos/` com roteador e prefixo próprios, registrado por
      `incluir_roteador_de_dados` (`RF-01-22`, `RF-01-02`).
- [ ] 4.2 Leitura do progresso do personagem — pontos regulares, acumulado de pontos extras,
      poderes, badges e níveis —, montada pela mesma projeção da vitrine (`RF-01-22`,
      `RF-01-59`, `RN-01-10`).
- [ ] 4.3 Prender o elenco ao mesmo portão da divulgação, com 404 indistinto para quem não
      autorizou (`RN-01-10`, `RF-01-22`).
- [ ] 4.4 Garantir que o saldo disponível **não entre** na estrutura da projeção do
      progresso, em vez de ser omitido na saída (`RF-01-59`, `RN-01-41`).

## 5. Verificação

- [ ] 5.1 Testar a expressão de autorização vigente isoladamente, nos cinco cenários da spec
      de `consentimento`, antes de qualquer rota usá-la (`RF-01-19`, `RN-13-07`).
- [ ] 5.2 Consulta pública responde sem token de sessão e recusa com 401 sem chave, sem
      diferenciar ausente, inválida e revogada (`RF-01-02`, `RN-01-32`).
- [ ] 5.3 Guerreiro(a) sem autorização não aparece em card, ranking, criação nem elenco, e a
      listagem não deixa posição vazia nem contagem que o denuncie (`RN-01-10`).
- [ ] 5.4 Revogação tira do público na chamada seguinte, sem prejuízo da participação
      (`RN-01-10`, `RN-01-21`).
- [ ] 5.5 Nick inexistente e nick sem autorização devolvem 404 de corpo idêntico; nick
      parcial não alcança ninguém (`RF-01-33`, `RF-01-34`, `RN-01-22`).
- [ ] 5.6 Nenhuma saída pública traz nome, contato, imagem ou valor em reais (`RN-01-11`).
- [ ] 5.7 Ranking exclui quem não autorizou sem abrir buraco na numeração (`RF-01-21`,
      `RN-01-10`).
- [ ] 5.8 Criação com integrante sem autorização não aparece no portfólio (`RF-01-26`,
      `RN-01-13`).
- [ ] 5.9 Cobertura de ODS sai por comunidade e ciclo, com o rótulo, e não aceita recorte por
      Guerreiro(a) (`RF-01-43`, `RN-01-24`).
- [ ] 5.10 **Teste de ausência**: percorrer `app.routes` sob o prefixo dos jogos e afirmar
      que todo método é `GET` ou `HEAD`; tentativa de crédito por caminho de jogo devolve 404
      (`RF-01-22`, `RN-01-06`).
- [ ] 5.11 **Teste de ausência**: nenhuma resposta de rota de jogo traz o saldo disponível
      nem permite deduzi-lo, e trocar ponto extra não altera o acumulado lido pelo jogo
      (`RF-01-59`, `RN-01-41`).
- [ ] 5.12 Substituir as rotas de teste de `consulta_por_nick` em `tests/conftest.py` pela
      rota real, agora que ela existe (`RF-01-65`).
- [ ] 5.13 `ruff format --check .`, `ruff check .` e `pytest` passam em `backend/`.

## 6. Documentação

- [ ] 6.1 Confirmar com o fundador se o rótulo de ciclo recebe linha no PRD-01 §13 e no
      documento 09; se sim, gravar a decisão no documento-fonte (03), mover a linha no
      documento 09 e aplicar ao PRD-01. Se não, `docs/` não muda por este item.
- [ ] 6.2 Conferir que nenhum outro documento de `docs/` mudou por esta change: não houve
      decisão nova além do item acima, `docs/prds/index.md` segue com o PRD-01 "aprovado" e
      as relações entre documentos não mudaram — logo o documento 99 e a `nav` do
      `mkdocs.yml` seguem como estão.
- [ ] 6.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR.
