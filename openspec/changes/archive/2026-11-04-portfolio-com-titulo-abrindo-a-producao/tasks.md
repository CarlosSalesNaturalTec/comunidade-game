# Tasks

## 1. Núcleo — o portão da comprovação pública

- [x] 1.1 Em `backend/src/nucleo/vitrine/publico.py`, criar
      `condicoes_de_comprovacao_publica(sessao)` ao lado de `condicoes_de_criacao_publica`:
      `cumpriu` e `publicavel` verdadeiros, comprovação gravada — `comprovacao` ou
      `comprovacao_referencia` — e autorização de divulgação vigente do Guerreiro(a), por
      `condicao_de_autorizacao_vigente`. Uma função só, usada pela listagem e pela rota de
      bytes (`RN-03-41`, `RN-01-63`, design — decisão 5).
- [x] 1.2 Na mesma unidade, a derivação do título e da trilha de cada fonte: na comprovação,
      `Missao.desafio_pratico_titulo_curto` e o nome da trilha da missão; na criação, o nome da
      trilha nos dois lugares, por `nomes_de_trilha`, que já existe (`RN-03-43`, design —
      decisão 3).

## 2. Núcleo — a listagem unida do acervo

- [x] 2.1 Em `vitrine/rotas.py`, `CriacaoPublicaSaida` ganha `id`, `fonte`, `titulo` e `tipo`,
      aditivos, e segue levando `trilha_id`, `trilha`, `validada_em`, `producao` e `autores`
      (`RF-03-85`).
- [x] 2.2 `listar_criacoes_publicas` passa a ler as duas fontes: cada consulta com o mesmo
      recorte de cursor e `tamanho + 1` itens, junção por `(data, id)` decrescente em memória e
      corte em `tamanho`; a data é a validação, na criação, e `julgado_em`, na comprovação
      (`RF-03-84`, `RF-03-83`, design — decisão 1).
- [x] 2.3 O cursor passa a gravar `aprovado_em` e a aceitar também a chave antiga
      `validado_em`, para que ninguém no meio da paginação receba 422 na implantação (design —
      decisão 2).
- [x] 2.4 Em `backend/tests/test_vitrine.py`, os cenários do delta de
      `leitura-publica-da-vitrine`: a comprovação aprovada no acervo com título curto, trilha,
      data e autoria; as duas fontes na mesma lista ordenadas entre si; o título da criação
      igual ao nome da trilha; a travessia por cursor com as duas fontes intercaladas no tempo,
      sem pular nem repetir item; e os quatro cenários do portão — não julgada, cumprida e não
      publicável, entrega presencial e sem autorização vigente —, mais a revogação que retira a
      comprovação na leitura seguinte (`RF-03-84`, `RF-03-85`, `RN-03-41`, `RN-03-43`).

## 3. Núcleo — os bytes da comprovação pública

- [x] 3.1 Em `vitrine/rotas.py`, `GET /vitrine/comprovacoes/{id}/arquivo`, sem sessão, sob
      `condicoes_de_comprovacao_publica`, devolvendo os bytes com
      `comprovacao_tipo_do_arquivo`; recusa em **404 em todos os casos**, como a rota irmã da
      criação (`RF-03-85`, `RN-03-41`, design — decisão 5).
- [x] 3.2 Em `backend/tests/test_vitrine.py`, os três cenários da rota de bytes: servida sem
      sessão para a comprovação aprovada de quem autorizou, 404 na julgada não publicável e
      404 na de quem não tem autorização vigente (`RF-03-85`).
- [x] 3.3 Ainda em `test_vitrine.py`, o cenário de `RN-03-42`: mídia enviada na produção de
      atividade da missão não aparece no acervo nem é servida por rota pública de bytes.

## 4. App 06 — a linha com título e a abertura da produção

- [x] 4.1 Em `apps/app-06-vitrine/src/api/leituras.ts`, o tipo do item do acervo com `id`,
      `fonte`, `titulo` e `tipo`, e a busca em bytes da comprovação e da criação por
      `lerArquivoDoNucleo` (`RF-03-85`).
- [x] 4.2 Novo `portfolio/ProducaoDoAcervo.tsx`: estado de aberto/fechado em `useState`
      próprio, imagem, áudio e vídeo por `comum/react/MidiaDoNucleo` com `token` nulo, texto do
      próprio item, link externo como link de saída e arquivo como transferência nomeada pelo
      título; falha dita em linguagem simples, sem revelar o motivo da recusa (`RF-03-85`,
      `RN-03-02`, design — decisões 6 e 7).
- [x] 4.3 Em `portfolio/SecaoDoPortfolio.tsx`, a linha passa a ter o título como identificação,
      a data de aprovação, a autoria por nick e a trilha **só** quando a fonte não é a criação
      da culminância; a seção mantém o nome "Portfólio de criações originais" e `idDe` passa a
      usar `fonte` e `id` (`RF-03-08`, `RF-03-84`, `RN-03-43`, design — decisão 4).
- [x] 4.4 O estilo da linha e da produção aberta, no piso de acessibilidade do PRD-03 §10 —
      conteúdo legível sem depender de animação —, e sem `ListaDeRegistros` mudar.
- [x] 4.5 Em `src/testes/portfolioERanking.test.tsx`, os cenários do delta de
      `aplicacao-da-vitrine`: a linha com título, data e autoria; o título curto e a trilha da
      comprovação; a criação da culminância sem repetir a trilha; o item mais recente abrindo a
      seção; os seis tipos abrindo na linha, incluindo o áudio e o vídeo sem tocar sozinhos; o
      fechar que recolhe; a recarga que volta todas recolhidas, sem nada gravado no aparelho; e
      a mídia indisponível dita em linguagem simples (`RF-03-08`, `RF-03-85`, `RN-03-02`,
      `RN-03-22`).

## 5. Documentação

- [x] 5.1 Revisar o **PRD-03**: `RF-03-84` e `RF-03-85` na §6.1, `RN-03-41` a `RN-03-43` na §7,
      a §9 com a rota de bytes nova e a nota da segunda fonte em `/v1/vitrine/criacoes`, os
      critérios da §12 que a linha e a abertura mudam, a §14 **sem pendência** — a do título
      fica fechada — e a §15 com os cinco identificadores novos.
- [x] 5.2 No `docs/09-topicos-em-aberto-e-sugestoes.md` §1, acrescentar à linha do acervo as
      **cinco decisões do fundador de 2026-11-04** que delimitaram esta fatia — o título da
      culminância é o nome da trilha, uma rota com as fontes unidas, a linha preserva trilha e
      data, a produção abre na própria linha, e a trilha não se repete quando é o título — sem
      reescrever a decisão de 2026-11-03, que já está lá.
- [x] 5.3 Marcar a fatia 12 do PRD-03 como `implementado` em
      `openspec/cronograma-de-fatias.md`, com o slug da change no lugar do recorte previsto.
      `docs/prds/index.md` **não** muda: o PRD-03 já consta como implementado. O documento 99
      também não: nenhuma relação entre documentos muda, e o invariante 5 já declara o acervo.
      Nenhum arquivo novo em `docs/`, logo nada entra na `nav` do `mkdocs.yml`.
