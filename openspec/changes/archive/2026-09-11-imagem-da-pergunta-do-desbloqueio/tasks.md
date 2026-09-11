## 1. Núcleo — modelo e migração

- [x] 1.1 Acrescentar a `PerguntaDoDesbloqueio` as colunas `imagem_referencia`, `imagem_tipo`,
      `imagem_tamanho` e `substituida_em`, e trocar a unicidade de (missão, ordem) pelo índice
      parcial `WHERE substituida_em IS NULL` (`RF-09-119`, `RN-05-47`, design — decisões 1 e 4);
      verificar pelo `Base.metadata` refletido no teste do modelo.
- [x] 1.2 Escrever a revisão do Alembic que cria as quatro colunas e troca a restrição pelo
      índice parcial, com `downgrade` que a desfaz; verificar pela paridade de
      `test_migracoes.py` entre `alembic upgrade head` e `Base.metadata`.

## 2. Núcleo — regra

- [x] 2.1 Fazer `perguntas_do_desbloqueio` servir só as vigentes e
      `declarar_desafio_de_desbloqueio` **carimbar** `substituida_em` em vez de apagar, de modo
      que redeclarar depois de respondido não estoure (`RN-05-47`, design — decisão 4).
- [x] 2.2 Aceitar em `declarar_desafio_de_desbloqueio` a `imagem_referencia` de cada pergunta,
      conferindo-a contra as imagens das perguntas daquela missão antes da substituição e
      recusando com 422 a de qualquer outra origem; a pergunta que a omite nasce sem imagem
      (`RF-09-119`, design — decisões 2 e 3).
- [x] 2.3 Escrever `abrir_envio_da_imagem_da_pergunta` e `confirmar_envio_da_imagem_da_pergunta`
      no padrão de `conteudos.regra`: autoria estrita do Mestre autor (403), formatos JPG, PNG e
      WebP (422) e teto de 1 MB (413) na abertura pelo declarado e na confirmação pelo real
      (`RF-09-119`, `RF-09-115`).
- [x] 2.4 Escrever a leitura dos bytes da imagem, autorizada ao Mestre autor da trilha e ao
      Guerreiro(a) inscrito nela, com 403 aos demais e 404 na pergunta sem imagem
      (`RF-09-119`, design — decisão 5).
- [x] 2.5 Levar a referência da imagem na cópia de `duplicar_trilha`, sem copiar bytes
      (`RF-09-13`, `RF-09-119`).

## 3. Núcleo — rotas

- [x] 3.1 Acrescentar `imagem_referencia` à entrada da pergunta em
      `POST /v1/missoes/{id}/desbloqueio` e às saídas da pergunta — a do Mestre autor e a do
      Guerreiro(a) no percurso —, sem que a alternativa correta apareça na do Guerreiro(a)
      (`RF-09-119`, `RF-09-118`).
- [x] 3.2 Abrir `POST` e `PATCH /v1/perguntas-do-desbloqueio/{id}/imagem` para o envio e a
      confirmação, e `GET /v1/perguntas-do-desbloqueio/{id}/imagem` para os bytes, com o tipo
      do envio (`RF-09-119`, design — decisão 5).

## 4. Testes do núcleo

- [x] 4.1 Em `test_desbloqueio_da_missao.py`, cobrir o envio da imagem: anexar e confirmar,
      pergunta sem imagem seguindo válida, formato fora da lista (422), acima de 1 MB (413) na
      abertura e na confirmação divergente, Mestre não autor (403) e pergunta sem envio
      confirmado que não serve imagem — os cenários do requisito "A pergunta do quiz admite uma
      imagem opcional".
- [x] 4.2 Cobrir a leitura dos bytes: Guerreiro(a) inscrito e Mestre autor recebem, não
      inscrito recebe 403, pergunta sem imagem responde 404 — os cenários do requisito "A imagem
      da pergunta é servida a quem pode ver a pergunta".
- [x] 4.3 Cobrir a redeclaração: referência de volta conserva a imagem, referência omitida a
      remove, referência de outra origem recusa com 422, e redeclarar **depois de respondido**
      grava as perguntas novas sem apagar submissão alguma (`RN-05-47`).
- [x] 4.4 Em `test_duplicacao_de_trilha.py`, cobrir que a cópia traz a imagem das perguntas pela
      referência, sem copiar bytes.

## 5. Telas

- [x] 5.1 Acrescentar ao `comum/api` a leitura de bytes do núcleo, que devolve `Blob` com a
      chave da aplicação e a credencial da persona nos cabeçalhos (design — decisão 6);
      verificar pelo teste do cliente.
- [x] 5.2 Na App 09, dar a cada pergunta do `DesafioDeDesbloqueio.tsx` anexar, trocar e remover
      imagem, com teto e formatos ditos antes do envio, progresso durante e motivo da recusa sem
      perder o que foi escrito; a imagem anexada permanece ao gravar o desafio de novo
      (`RF-09-119`).
- [x] 5.3 Na App 05, exibir a imagem da pergunta antes das alternativas, com texto alternativo,
      e manter a pergunta respondível quando a imagem não carrega (`RF-09-119`, `RF-05-89`).
- [x] 5.4 Cobrir as duas telas com os cenários dos deltas de `area-do-mestre` e
      `area-do-guerreiro`: anexar, recusa explicada, corrigir texto sem perder a imagem, remover
      a imagem, exibição com texto alternativo e imagem que não carrega.

## 6. Documentação

- [x] 6.1 Registrar as três decisões do fundador de 2026-09-11 — imagem preservada na
      redeclaração, bytes servidos pelo núcleo e a substituição que não apaga pergunta
      respondida — no documento 03 §11 e no documento 09 §1; acrescentar as três rotas da imagem
      ao PRD-09 §9 e ajustar o que a decisão muda na §14; marcar a fatia 19 como implementada em
      `openspec/cronograma-de-fatias.md`, com o recorte ampliado pelo conserto da fatia 18.
      Nenhum arquivo novo em `docs/`, logo nada muda na `nav` do `mkdocs.yml`; o documento 99
      só muda se a relação entre documentos mudar.
