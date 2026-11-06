# Tasks

## 1. Decisão descida pelo fluxo (antes do código)

- [x] 1.1 Documento 03 §8: a lista da Área do Apoiador Desenvolvedor troca o item do
      assistente pelo **link da documentação da API (Swagger)**, segue com quatro coisas; §1
      não muda. Documento 09, linha "Acesso das aplicações de terceiros": registra a decisão do
      fundador de 2026-11-06 e corta corpus, recorte, freio e abertura do assistente
      (`RF-03-67`). Verificar: `grep -n -i "assistente de chat\|corpus do assistente"` em
      `docs/03-*` e `docs/09-*` não acha o assistente do Desenvolvedor.
- [x] 1.2 PRD-03: novo enunciado do `RF-03-67`; saem das §§6.6 e 7 o `RF-03-68` a `RF-03-72`,
      `RF-03-81`, `RN-03-30`, `RN-03-31`, `RN-03-38`, `RN-03-39`; §§3.1, 4, 5.8 (passos e
      exceção), 8, 9 (rota), 11 (linha da conversa), 12, 13 e 15 deixam de citá-los; §13 ganha a
      linha da retirada com a data (design, decisão 2). Verificar: `grep -n "assistente"` no
      PRD-03 só acha a linha da §13.
- [x] 1.3 Menções de uma frase: documento 08 (Área do Apoiador Desenvolvedor), PRD-11 §3.2,
      PRD-12 (linha da Área), `README.md` da raiz — trocam o assistente pela documentação da API
      (`RF-03-67`). Verificar: `grep -rn -i "assistente de chat"` em `docs/` e `README.md` vazio.

## 2. App 06 — Área do Apoiador Desenvolvedor

- [x] 2.1 `desenvolvedor/AreaDoDesenvolvedor.tsx`: sai `<ChatDoDesenvolvedor />` e o "Converse
      com o assistente" do texto de abertura; "Documentação e código" ganha o link
      "Documentação da API (Swagger)" para `${URL_DO_NUCLEO}/docs`, em nova aba, omitido sem
      `URL_DO_NUCLEO`; o comentário passa a citar as quatro coisas novas (`RF-03-67`,
      `RN-03-29`). Verificar: teste da 4.1.
- [x] 2.2 Apagar `desenvolvedor/ChatDoDesenvolvedor.tsx` e `desenvolvedor/abertura.ts`; em
      `api/desenvolvedor.ts` saem `MensagemDaConversa`, `RespostaDoAssistente`,
      `TETO_DO_HISTORICO` e `perguntarAoAssistente`, ficando a solicitação de chave; estilos do
      chat que ficarem órfãos saem do CSS. Verificar: `biome check` sem import quebrado.
- [x] 2.3 Textos que citam o assistente: `desenvolvedor/SecaoDoDesenvolvedor.tsx`, a linha
      "Conversa com o assistente do Desenvolvedor" de `coleta/AreaDetalhada.tsx` (`RF-03-52`) e
      o comentário de `descoberta/enderecos.ts` (design, decisão 7). Verificar:
      `grep -rn -i assistente apps/app-06-vitrine/src` sem ocorrência fora de testes.

## 3. Núcleo, esteira e semeadura

- [x] 3.1 Apagar `nucleo/assistente/desenvolvedor/` e `nucleo/corpus_do_desenvolvedor/`; tirar o
      roteador de `principal.py` e do `conftest.py`, as chaves do assistente e do corpus de
      `configuracao.py` e a superfície `assistente_do_desenvolvedor` de `protecao/freio.py`
      (`RN-03-30`, `RN-03-38`, `RN-03-39` retirados). Verificar: teste da 4.2.
- [x] 3.2 Apagar `tests/test_assistente_do_desenvolvedor.py`,
      `tests/test_freio_do_assistente_do_desenvolvedor.py` e `tests/test_corpus_do_desenvolvedor.py`.
      Verificar: `grep -rn "desenvolvedor" backend/tests` só acha a solicitação de chave.
- [x] 3.3 `.github/workflows/backend-deploy.yml`: saem o comentário, "Instalar uv",
      `setup-python` e "Montar o corpus"; `backend/Dockerfile` perde o `COPY` do corpus e o
      comentário; `.gitignore` perde a entrada do corpus (design, decisão 5). Verificar:
      `grep -rn corpus-do-desenvolvedor .github backend/Dockerfile .gitignore` vazio.
- [x] 3.4 `conteudo_institucional/semeadura.py`: "Construir sobre a plataforma" troca o
      assistente pela documentação da API (design, decisão 6). Verificar: teste de semeadura
      existente segue verde.

## 4. Testes

- [x] 4.1 `testes/areaDoDesenvolvedor.test.tsx` e `testes/chaveDoDesenvolvedor.test.tsx`: saem os
      casos do chat e da indisponibilidade; entram os cenários "A área abre com as quatro
      coisas", "O link da documentação da API aponta a interface do núcleo" (href
      `${URL_DO_NUCLEO}/docs`, `target="_blank"`) e "A área não oferece assistente" (nenhum
      campo de pergunta, nenhuma chamada ao núcleo ao abrir) (`RF-03-67`); a área detalhada
      não lista a conversa (`RF-03-52`).
- [x] 4.2 Núcleo: caso em teste existente da proteção ou do OpenAPI provando que
      `POST /v1/assistente-do-desenvolvedor` responde 404 e não aparece em `/openapi.json`, e
      que `/docs` responde 200 sem chave (spec `assistente-do-desenvolvedor` REMOVED;
      `protecao-das-rotas-publicas` ADDED, cenários do freio seguem verdes).

## 5. Documentação da change

- [x] 5.1 `openspec/cronograma-de-fatias.md`, bloco do PRD-03: linha "—" nova, "Assistente do
      Desenvolvedor retirado e Swagger na área", slug desta change, os identificadores
      retirados e o `RF-03-67` mudado, situação `implementado`; o parágrafo sob a tabela deixa
      de dizer que a fatia 8 trouxe a capacidade `assistente-do-desenvolvedor` como vigente.
      `docs/prds/index.md`, doc 99 e `mkdocs.yml` não mudam: situação do PRD, relação entre
      documentos e arquivos de `docs/` seguem iguais.

## Workflow follow-up

- No `/opsx:archive`, a spec `openspec/specs/assistente-do-desenvolvedor/` fica sem requisito:
  apagar a pasta.
- No PR, avisar o fundador para o Admin revisar o texto publicado de "Construir sobre a
  plataforma" em produção.
