# Tasks

## 1. Núcleo — o "antes" do kit

- [x] 1.1 Em `backend/src/nucleo/cuidado_do_bem/regra.py`, `ler_arquivo_do_ultimo_aprovado`:
      resolve a entrega, calcula o último aprovado por `ultimo_registro_aprovado`, autoriza o
      Guerreiro(a) dono e o Mestre da comunidade dele (403 aos demais) e lê os bytes da
      customização ou da comprovação do prático conforme a `fonte`; 404 sem customização aberta
      ou sem mídia (`RF-04-81`, decisão de 2026-11-13). Verificação: tarefa 1.3.
- [x] 1.2 Em `cuidado_do_bem/rotas.py`, `GET /v1/entregas-de-recompensa/{id}/ultimo-aprovado/arquivo`,
      devolvendo os bytes com o tipo do arquivo (`RF-04-81`). Verificação: tarefa 1.3 e a rota no
      OpenAPI.
- [x] 1.3 Testes em `backend/tests/test_customizacao_do_kit.py`: os seis cenários do delta de
      `customizacao-do-kit` — comprovação como "antes" a Mestre não autor, customização aprovada
      como "antes", 403 a Mestre de outra comunidade e a outro Guerreiro(a), 404 sem customização
      aberta, rota da comprovação ainda 403 ao não autor (`RF-04-81`). Verificação:
      `uv run pytest tests/test_customizacao_do_kit.py -x` verde.

## 2. App 01 — cliente e tela

- [x] 2.1 `apps/app-01-aula-presencial/src/api/cuidadoDoBem.ts`: tipos da fila do cuidado e
      chamadas de leitura da fila, julgamento, validação da conservação, captura, abertura e
      confirmação do envio e URLs de mídia do pendente e do último aprovado, todas sob o token
      de trabalho (`RF-04-81` a `RF-04-84`). Verificação: tarefa 2.6.
- [x] 2.2 Glifo `cuidado` em `comum/react/Icone.tsx`, só se nenhum existente couber, e o item
      "Customizações a julgar" no grupo de quem opera em `inicio/TelaInicial.tsx`, depois das
      entregas, só com `papelDeTrabalho === "mestre"` (`RF-04-81`). Verificação: tarefa 2.6.
- [x] 2.3 `cuidado/TelaDoCuidadoNoEncontro.tsx`: a fila por Guerreiro(a), nick e avatar, um bloco
      por bem com as ações da tabela da decisão 3 do design, registro pendente e último aprovado
      lado a lado por `MidiaDoNucleo`, estado vazio sem erro (`RF-04-81`, `RF-04-84`, §5.13).
      Verificação: tarefa 2.6.
- [x] 2.4 Julgamento e conservação na tela: aprovar; reprovar com motivo obrigatório; validar a
      conservação; confirmação do ponto extra e, na aprovação, do acervo; recusa do núcleo como
      vem; fila relida depois de cada ato (`RF-04-82`, `RF-04-83`, `RF-04-84`, `RN-01-66`).
      Verificação: tarefa 2.6.
- [x] 2.5 Captura na hora em kit aberto sem pendente: arquivo de imagem ou vídeo, descrição por
      voz transcrita no aparelho ou por texto, registro, envio retomável com progresso e
      retomada do registro pendente sem mídia (`RF-04-82`, §5.13.3). Verificação: tarefa 2.6.
- [x] 2.6 Testes em `cuidado/cuidado.test.tsx` e no teste de `inicio/`: caminho só a Mestre;
      fila com quem chegou e estado vazio; antes e agora lado a lado; aprovar confirma extra e
      acervo; reprovar sem motivo não envia; recusa do núcleo como vem; conservação confirma o
      extra; bem que já pontuou não oferece nada; kit fechado sem captura; captura vira pendente
      (`RF-04-81` a `RF-04-84`). Verificação: `npx vitest run` no recorte, verde.

## 3. Documentação

- [x] 3.1 Documento 09 §1, linha "Customização do kit recebido": uma frase com a decisão de
      2026-11-13 — a comprovação do prático, quando é o último aprovado, é servida ao Mestre da
      comunidade do Guerreiro(a) para o julgamento. `openspec/cronograma-de-fatias.md`: fatia 34
      do PRD-04 com o slug `2026-11-13-cuidado-do-bem-no-encontro` e situação "implementado". O
      PRD-04 e `docs/prds/index.md` não mudam (o requisito já diz "último registro aprovado", e
      a fatia 35 segue aberta); o documento 99 não muda. Verificação: `npm run lint` e
      `mkdocs build --strict` verdes.
