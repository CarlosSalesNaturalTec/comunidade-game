# Tasks

## 1. PRD-01: os identificadores antes do código

- [x] 1.1 Revisar o PRD-01 criando `RF-01-77` (áudio como sexto tipo de produção do aluno),
      `RF-01-78` e `RN-01-60` (leitura da mídia da criação por quem pode vê-la), `RF-01-79` e
      `RN-01-61` (mídia da produção da missão guardada), `RF-01-80` e `RN-01-62` (leitura
      dessa mídia, sem rota pública) e `RF-01-81` e `RN-01-63` (leitura pública da mídia da
      criação sob o portão da listagem) — nas §§6, 7 e 9, com a §15 de rastreabilidade;
      verificar que nenhum dos nove identificadores já existia (`grep -o "R[FN]-01-[0-9]*"`)
- [x] 1.2 Conferir se a tabela de dados pessoais do PRD-01 §11 precisa de linha para a mídia
      da produção da missão, agora guardada, e acrescentá-la se precisar — risco declarado no
      `design.md`; verificar lendo a §11 e registrando no PR a conclusão, ainda que seja "não
      precisa"
- [x] 1.3 Rodar `npm run fix`, `npm run lint` e `.venv/bin/mkdocs build --strict`, porque
      `docs/` foi tocado; verificar as três saídas limpas

## 2. Áudio como sexto tipo da produção do aluno (`RF-01-77`)

- [x] 2.1 Acrescentar `audio` a `TipoDeProducaoDaCriacaoOriginal` em
      `backend/src/nucleo/criacoes_originais/modelo.py`, mantendo `native_enum=False` e
      `length=16`, e atualizar o _docstring_, que hoje afirma "os cinco valores que
      `conteudos.modelo.TipoDeConteudo` já firma" — afirmação que deixa de valer
- [x] 2.2 Tratar `audio` como tipo de mídia na regra de entrega — nasce sem bytes e os recebe
      pela sessão de envio, junto de `imagem`, `video` e `arquivo`, nunca junto de `texto` e
      `link_externo`; verificar com `uv run pytest tests/test_criacao_original.py -x`
- [x] 2.3 Conferir contra o esquema vivo se existe CHECK em `criacao_original.tipo` — a
      decisão 5 do `design.md` diz que não há; havendo, gerar a migração que o recria com seis
      valores. Verificar inspecionando o esquema do banco de teste
- [x] 2.4 Teste que a entrega com tipo `audio` é aceita e que `TipoDeConteudo` **não** ganhou
      áudio, afirmando a divergência de propósito entre os dois enums; verificar com
      `uv run pytest tests/test_criacao_original.py tests/test_conteudo.py -x`

## 3. Leitura da mídia da criação original (`RF-01-78`, `RN-01-60`)

- [x] 3.1 Escrever `ler_arquivo_da_criacao` em `criacoes_originais/regra.py` com a autorização
      — creditado, Mestre autor ou Admin —, 403 fora disso e 404 sem mídia, no molde de
      `conteudos.regra.ler_arquivo_do_conteudo`
- [x] 3.2 Expor `GET /v1/criacoes/{id_da_criacao}/arquivo` devolvendo `Response` com os bytes
      e o `tipo_mime` gravado, no molde de `GET /conteudos/{id}/arquivo`
- [x] 3.3 Testes dos cinco cenários da spec `criacao-original` — autor lê, Mestre autor lê,
      terceiro recebe 403, criação de texto dá 404, envio não confirmado dá 404; verificar com
      `uv run pytest tests/test_criacao_original_rota.py -x`

## 4. Leitura pública da mídia da criação (`RF-01-81`, `RN-01-63`)

- [x] 4.1 Expor a rota pública da mídia reaproveitando `condicoes_de_criacao_publica` de
      `vitrine/publico.py` — o mesmo objeto da listagem, nunca uma segunda cópia da regra
- [x] 4.2 Garantir que a recusa seja **404 e indistinguível** entre criação inexistente e
      criação que não passa no portão, no corpo e no código (decisão 3 do `design.md`)
- [x] 4.3 Testes dos cinco cenários da spec `leitura-publica-da-vitrine`, incluindo o da
      autorização revogada que tira a mídia do ar na leitura seguinte, sem ato de limpeza;
      verificar com `uv run pytest tests/test_vitrine.py -x`

## 5. Mídia guardada na produção da missão (`RF-01-79`, `RN-01-61`)

- [x] 5.1 Migração Alembic acrescentando `referencia` (`String(512)`) e `tamanho`
      (`Integer`), ambas _nullable_, em `producao_da_missao`, com `downgrade` que as derruba;
      verificar com `alembic upgrade head` e `alembic downgrade -1` no banco de teste
- [x] 5.2 Acrescentar os campos ao modelo e corrigir o _docstring_, que hoje afirma "sem
      coluna de foto, de áudio nem de custo" e que "a foto é descartada na leitura"
- [x] 5.3 Passar a **guardar** a foto em vez de descartá-la, e passar a aceitar o arquivo de
      áudio ao lado da transcrição, nas **duas** portas — equipe e individual —, mantendo a
      recusa de entrega em áudio **sem** transcrição (decisão 1 do `design.md`)
- [x] 5.4 Guardar os bytes que **já chegam** na requisição multipart, sem sessão de envio —
      corrigido no apply (decisão 7 do `design.md`): a foto precisa chegar inline para o OCR, e
      guardar é não descartar. Verificar que a referência e o tipo MIME ficam gravados
- [x] 5.5 Testes: foto guardada, áudio guardado, produção nasce sem mídia, devolutiva segue
      feita sobre a transcrição e nunca sobre o arquivo; verificar com
      `uv run pytest tests/test_producao_da_missao.py -x`

## 6. Leitura da mídia da produção (`RF-01-80`, `RN-01-62`)

- [x] 6.1 Escrever a autorização e a rota de leitura — integrante da equipe dona, Mestre da
      trilha ou Admin; 403 fora disso, 404 sem mídia
- [x] 6.2 Teste que afirma a **ausência** de rota pública para essa mídia, e não só a presença
      da autenticada — é a trava que impede a produção da missão de virar item de acervo por
      um `GET` a mais; verificar com `uv run pytest tests/test_producao_da_missao.py -x` — ficaram no arquivo que já existe, que é onde vivem os auxiliares de montagem da equipe
- [x] 6.3 Teste que produção gravada antes desta change responde 404, sem _backfill_
      (decisão 6 do `design.md`)

## 7. Fechamento

- [x] 7.1 Corrigir à mão o `## Purpose` de `openspec/specs/producao-da-missao/spec.md`, que
      diz "sem guardar a foto nem o áudio" — a instrução do OpenSpec é que o Purpose de uma
      capacidade existente se edita no spec consolidado, porque o delta não o carrega
- [x] 7.2 Marcar a fatia do bloco PRD-01 como `implementado` no
      `openspec/cronograma-de-fatias.md`, com o slug desta change na coluna Recorte
- [x] 7.3 Rodar uma vez, ao fechar as tarefas: `ruff format .`, `ruff check --fix .` e
      `pytest` no backend; verificar a suíte verde sem repetir o que já passou

## Workflow follow-up

- Abrir o PR com os artefatos, o código, os testes e a revisão do PRD-01, e aguardar a
  aprovação do fundador. O merge usa merge commit, nunca squash.
- Arquivar a change depois do merge, com `/opsx:archive`, consolidando os deltas em
  `openspec/specs/`.
