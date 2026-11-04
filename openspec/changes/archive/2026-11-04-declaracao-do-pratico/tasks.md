# Tasks

## 1. PRD-09: os identificadores antes do código

- [x] 1.1 Revisar o PRD-09 criando `RF-09-129` (forma de comprovação aceita, uma entre as
      seis), `RF-09-130` (critério de aceite em texto livre), `RF-09-131` (título curto, campo
      próprio), `RN-09-50` (os três exigidos na declaração do prático; prático anterior segue
      valendo até a redeclaração) e `RN-09-51` (título curto de no máximo 60 caracteres, nunca
      o enunciado) — na §6.4, na §7, na linha de `Missao` da §8, na §9 e na §15 de
      rastreabilidade (origem 02 §4 e 11 §§2.2, 8.2); verificar que nenhum dos cinco já existia
      com `grep -o "R[FN]-09-[0-9]*" docs/prds/prd-09-area-do-mestre.md | sort -u`
- [x] 1.2 Conferir se a §11 (LGPD) do PRD-09 precisa de linha pelos três campos novos — são
      texto do Mestre, não dado da criança — e registrar a conclusão no PR, ainda que seja
      "não precisa"

## 2. Núcleo: as três colunas e a declaração (`RF-09-129` a `RF-09-131`, `RN-09-50`, `RN-09-51`)

- [x] 2.1 Migração Alembic acrescentando a `missao` as colunas
      `desafio_pratico_forma_de_comprovacao` (`String(16)`),
      `desafio_pratico_criterio_de_aceite` (`Text`) e `desafio_pratico_titulo_curto`
      (`String(60)`), todas anuláveis (design — decisão 4), com `downgrade` que as derruba;
      verificar com `alembic upgrade head`, `alembic downgrade -1` e o teste de paridade entre
      `head` e `Base.metadata` que já existe
- [x] 2.2 Acrescentar as três colunas a `Missao` em `backend/src/nucleo/trilhas/modelo.py`,
      importando `TipoDeProducaoDaCriacaoOriginal` de `criacoes_originais/modelo.py` para a
      forma (design — decisão 3), com comentário que cite `RF-09-129` a `RF-09-131` e a decisão
      do design, no padrão das colunas de desafio que já estão lá
- [x] 2.3 Estender `declarar_desafio_de_desbloqueio` em `trilhas/regra.py`: no prático, exigir
      forma válida entre as seis, critério não vazio e título curto não vazio e de até 60
      caracteres, com `ErroDeValidacao` por campo (`RN-09-50`, `RN-09-51`); no quiz, recusar
      com 422 qualquer um dos três que chegue, dizendo que não se aplica (design — decisão 5);
      redeclarar prático segue substituindo, e passa a exigir os três
- [x] 2.4 Acrescentar os três campos a `DeclararDesafioDeDesbloqueioEntrada` em
      `trilhas/rotas.py`, anuláveis no schema para que a recusa seja da regra e chegue ao
      Mestre por campo, e repassá-los a `declarar_desafio_de_desbloqueio`
- [x] 2.5 Fazer os três viajarem onde o enunciado do prático já viaja (design — decisão 6):
      `MissaoComDesafioDeDesbloqueioSaida` (resposta da declaração), `MissaoAoAutorSaida` de
      `GET /v1/trilhas/minhas` e `DesafioDeDesbloqueioSaida` do percurso do Guerreiro(a);
      verificar que no quiz os três vêm nulos
- [x] 2.6 Testes em `backend/tests/test_desbloqueio_da_missao.py` dos cenários do delta de
      `desbloqueio-da-missao`: prático declarado com os três; forma fora das seis, prático sem
      forma, critério em branco, título em branco e título de 80 caracteres recusados com 422;
      quiz com cada um dos três recusado; e os três campos nulos no quiz. Verificar com
      `uv run pytest tests/test_desbloqueio_da_missao.py -x`
- [x] 2.7 Testes da leitura e da compatibilidade: o Mestre autor reencontra os três em
      `GET /v1/trilhas/minhas`, o Guerreiro(a) inscrito lê forma e critério no percurso, e o
      prático gravado sem os três (linha montada direto no banco, como o prático antigo) segue
      servido com eles nulos e exige os três ao ser redeclarado. Verificar com
      `uv run pytest tests/test_desbloqueio_da_missao.py tests/test_percurso_da_trilha.py -x`

## 3. App 09: o bloco do prático (`RF-09-129` a `RF-09-131`, `RN-09-50`, `RN-09-51`)

- [x] 3.1 Estender `apps/app-09-mestre/src/trilhas/api.ts`: os três campos em
      `DeclararDesafioDeDesbloqueioEntrada` e em `MissaoDaTrilha`, com o tipo da forma
      reusando os seis valores da entrega do Guerreiro(a)
- [x] 3.2 Acrescentar a `DesafioDeDesbloqueio.tsx` a escolha da forma entre as seis pelo nome,
      o critério de aceite e o título curto, apresentados **só** no prático, com o estado
      iniciado pelo que a missão traz (reabertura) e limpo ao trocar para quiz; dizer na tela
      para que serve cada um e o teto de 60 caracteres do título, no vocabulário que o bloco
      já usa
- [x] 3.3 Mostrar a recusa do núcleo no bloco do desafio, com o motivo por campo e sem apagar
      o que o Mestre escreveu nos outros campos nem nas perguntas
- [x] 3.4 Acrescentar a forma aceita e o critério de aceite à seção de desbloqueio da
      `PreVisualizacaoDaMissao.tsx`, que já apresenta o enunciado do prático (`RF-09-25`)
- [x] 3.5 Testes em `apps/app-09-mestre/src/trilhas/trilhas.test.tsx` dos cenários do delta de
      `area-do-mestre`: os três campos aparecem ao escolher prático e saem ao escolher quiz; a
      sondagem segue sem eles; o prático declarado reabre com os três; o prático antigo abre
      com os campos vazios e como prático; a recusa por campo aparece sem limpar a tela; e a
      pré-visualização traz forma e critério. Verificar com
      `npm run test --workspace apps/app-09-mestre`

## 4. Fechamento

- [x] 4.1 Marcar a fatia 26 do bloco PRD-09 como `implementado` no
      `openspec/cronograma-de-fatias.md`, com o slug desta change na coluna Recorte, e
      conferir que nada mais em `docs/` mudou por esta change: a decisão já está gravada nos
      documentos 02 §4, 11 §§2.2, 5 e 8.2, 99 §6 e 09 §1 pelo PR de documentação de 2026-11-03,
      a situação do PRD-09 em `docs/prds/index.md` não muda e nenhum arquivo novo entra na
      `nav` do `mkdocs.yml` — a única revisão em `docs/` é a do PRD-09, da tarefa 1.1

## Workflow follow-up

- Abrir o PR com os artefatos, o código, os testes e a revisão do PRD-09, e aguardar a
  aprovação do fundador. O merge usa merge commit, nunca squash.
- Arquivar a change depois do merge, com `/opsx:archive`, consolidando os deltas em
  `openspec/specs/`.
