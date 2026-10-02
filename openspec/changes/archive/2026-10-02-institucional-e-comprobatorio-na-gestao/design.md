# Design

## Context

O núcleo já tem quase tudo. A capacidade `conteudo-institucional` declara no próprio texto que
"a tela de edição é da App 03", e `prova-do-apoio` já governa o documento pendente e o ato de
anexação. O que falta é a App 03 — e, em dois pontos, o contrato de leitura que as telas exigem.

Duas restrições moldam o desenho:

- A leitura pública do institucional **não pode** devolver o autor (`RF-03-45`), e está sob o
  prefixo `/vitrine`, que responde sem token de sessão.
- `GET /v1/apoiadores` devolve `PaginaDeResultado[AdultoSaida]` — **paginada por cursor** — e o
  `AdultoSaida` é compartilhado com `GET /v1/mestres`.

## Goals / Non-Goals

**Goals:**

- As duas telas de Admin de pé, sobre o que o núcleo já faz.
- Fechar as duas lacunas de contrato com a menor mudança possível.

**Non-Goals:**

- Rota nova para a fila dos comprobatórios: o fundador escolheu alargar o que já existe.
- Edição do endereço ou do rótulo do artefato na fila — isso é da tela de artefatos do cadastro.
- Qualquer mudança na rota pública do institucional ou na leitura do próprio Apoiador.
- `RF-02-85` e a homologação do aporte declarado: já entregues pelas fatias 3 e 11.

## Decisions

### 1. O Admin lê por rota própria, não por parâmetro na rota pública

`GET /v1/conteudo-institucional`, sob `exigir_permissao(Operacao.conteudo_institucional, "le")`,
no molde do `PUT` que já está ali. A alternativa — um parâmetro na rota pública que inclua o
autor — foi descartada: a rota pública responde sem token de sessão, e qualquer caminho que a
faça devolver o autor é um vazamento esperando acontecer. Rota separada mantém o `RF-03-45`
verdadeiro por construção, e não por cuidado de quem chama.

A saída reusa o `SecaoPublicadaSaida` que o `PUT` já devolve — o mesmo corpo, pela mesma razão:
é a mesma informação.

### 2. `ArtefatoSaida` ganha `id` e `publicado`; nenhuma rota nasce

Decisão do fundador, 2026-10-02. A fila da gestão deriva de `GET /v1/apoiadores`, filtrando por
`publicado == false`. A alternativa — `GET /v1/apoiadores/artefatos-pendentes` — foi descartada
por ser rota nova no núcleo dentro de uma fatia de App 03, e por acrescentar linha ao PRD-02 §9
para servir uma fila que a listagem já pode dar.

### 3. `publicado` é derivado, nunca gravado

Vem do `artefato_esta_publicado()` que `prova-do-apoio` já usa na leitura do próprio Apoiador.
Campo novo no banco seria uma segunda fonte da mesma verdade, e nenhuma migração é necessária.

### 4. A fila entra em `filas/`; o institucional nasce em pasta própria

A fila do comprobatório é mais uma fila da mesa de comando: entra em
`apps/app-03-gestao/src/filas/`, normalizada em `ItemDeFila` como as sete que já estão lá. O
institucional não é fila nem cadastro — nasce em pasta própria, com a tela das três seções.

### 5. A fila vazia e o carregamento são informação, não erro

`role="status"`, no molde do `EstadoDaLista` que o repositório já justifica assim. Vale também
para a fila que não tem nada esperando — estado comum, não falha.

## Risks / Trade-offs

- **A fila paga a paginação da listagem.** Derivar os pendentes de `GET /v1/apoiadores` obriga a
  percorrer as páginas para não perder documento em página seguinte. No Ciclo 01, com uma
  comunidade, o número de Apoiadores é pequeno e o custo é irrelevante; se crescer, a rota
  dedicada da decisão 2 volta à mesa — e volta como fatia, não como emenda.
- **`AdultoSaida` é compartilhado com `GET /v1/mestres`**, que passa a trazer `id` e `publicado`
  nos artefatos também. A mudança é **aditiva** e coerente: o artefato do Mestre tem o mesmo
  estado de publicação. Nenhum consumidor quebra, e a App 09 pode ignorar os dois campos.
- **O texto institucional é publicado por quem tem `Operacao.tudo`.** A tela não introduz
  permissão nova; se o fundador quiser um papel intermediário publicando institucional, é
  decisão de produto e não entra aqui.
