# Design

## Context

`ListaDeGuerreiros.tsx` monta a `Tabela` de `comum/react` com cinco colunas: Nick (cabeçalho da
linha), Avatar (recolhida, texto fixo), Comunidade, Início do vínculo (recolhida) e Ações.
`GET /v1/guerreiros` já devolve `nome` em `GuerreiroDaLista`; a tela só não o usa.

## Goals / Non-Goals

**Goals:** nome ao lado do nick; remover Avatar e Início do vínculo (`RF-02-15`, `RN-02-22`).

**Non-Goals:** mudar contrato do núcleo, ficha, formulário ou outra aplicação.

## Decisions

1. **Nome em coluna própria, logo após o Nick, sem `recolhida`.** O nick segue cabeçalho da
   linha — é o identificador único no jogo —, e o nome fica visível também abaixo de 768 px,
   porque é a razão da change. Ordem final: Nick, Nome, Comunidade, Ações.
2. **`vinculo_iniciado_em` continua no tipo e no teste de vínculo.** `comVinculo` usa o campo
   para decidir se há vínculo vigente; só a coluna sai. `formatarData` deixa de ter uso e sai.
3. **Comentário do componente** troca "só nick e avatar" por "nick e nome, sem imagem real",
   deixando dito que a App 03 não é superfície pública (invariante 12).

## Risks / Trade-offs

- Nome civil na tela da gestão → aceito: a App 03 é só do Admin, que já o cadastra e o vê na
  edição; nenhuma superfície pública muda.
