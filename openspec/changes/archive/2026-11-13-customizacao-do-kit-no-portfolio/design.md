# Design

## Context

O núcleo já entrega a terceira fonte (`leitura-publica-da-vitrine`: "O registro aprovado da
customização é a terceira fonte do acervo público" e "A mídia da customização pública é servida
sob o mesmo portão da listagem"): `GET /v1/vitrine/criacoes` e a carta de
`GET /v1/vitrine/guerreiros/{nick}` trazem itens com `fonte: "customizacao_do_kit"`, `titulo`
igual à descrição, `trilha` da recompensa e `tipo` imagem ou vídeo. A App 06 desenha o acervo
por um único caminho — `linhaDoAcervo` + `ProducaoDoAcervo` + `lerArquivoDoAcervo` —, entregue
pelas fatias 12 e 13 (`aplicacao-da-vitrine`).

## Goals / Non-Goals

**Goals:** a App 06 reconhecer a terceira fonte nas três superfícies sem bifurcar o caminho
único do acervo.

**Non-Goals:** qualquer mudança de núcleo ou de contrato; rótulo ou selo que distinga a fonte
na linha — o PRD não o pede (`RF-03-88` só fixa título e trilha).

## Decisions

1. **A rota de bytes sai de um mapa fonte → recorte**, tipado por `FonteDoAcervo`
   (`Record<FonteDoAcervo, string>`), no lugar do ternário que manda toda fonte não-criação
   para `comprovacoes`. O `Record` faz o compilador acusar a próxima fonte esquecida — foi
   exatamente o ternário que deixou esta passar em silêncio.
   Descartado: estender o ternário — repete o defeito.
2. **`linhaDoAcervo` não muda de regra**: já omite a trilha só em `criacao_original`, o que
   para a customização dá descrição como título e trilha ao lado da data, como o `RF-03-88`
   pede. A mudança ali é só de comentário ("duas" → "três" fontes).
3. **A carta e a página não ganham código**: consomem `criacoes` como chegam; a cobertura vem
   de teste com item da terceira fonte.

## Risks / Trade-offs

- [Núcleo envia fonte desconhecida no futuro] → o `Record` só protege em tempo de compilação;
  em tempo de execução, rota inexistente vira 404 e a linha diz que a produção não está
  disponível, sem quebrar (requisito "A produção que o núcleo não serve não vira linha
  quebrada").
