# Design

## Context

O avatar e o objeto versionado já existem em `comum/avatar/` (capacidade `camada-visual-comum`):
`escreverAvatar`, `lerAvatar` e o catálogo `CAMADAS_DO_AVATAR`. O núcleo guarda o avatar como
texto opaco e as rotas `POST`/`PATCH /v1/guerreiros` exigem-no não vazio (capacidade
`cadastro-de-persona`). Hoje a App 03 pede esse texto num `Campo` livre.

## Goals / Non-Goals

**Goals:** sortear no aparelho, dentro do catálogo; tirar o campo dos dois modos do formulário.

**Non-Goals:** mudar o núcleo; regravar avatar de texto livre já gravado; desenhar o avatar na
lista ou na ficha da gestão.

## Decisions

1. **O sorteio mora na camada comum, não no núcleo.** `sortearAvatar(aleatorio = Math.random)`
   em `comum/avatar/objeto.ts`, exportado por `indice.ts`, escolhe um índice por camada de
   `CAMADAS_DO_AVATAR` e devolve `escreverAvatar(...)`. O catálogo vive só no front (documento 15
   §7, composição no aparelho); sortear no núcleo duplicaria o catálogo em Python.
   Descartado: o núcleo gerar quando o avatar faltar — exigiria afrouxar a rota e copiar o
   catálogo.
2. **O gerador de acaso é injetável.** O parâmetro `aleatorio` deixa o teste fixar o resultado
   sem `vi.spyOn(Math, "random")`. Não é sorteio criptográfico: não protege segredo algum.
3. **O cadastro sorteia no envio; a edição reenvia o gravado.** `FormularioDeGuerreiro` monta
   `JSON.stringify(sortearAvatar())` no `POST`; no `PATCH` envia `guerreiroExistente.avatar`, e só
   se vier vazio troca por um sorteado. O texto livre antigo não é vazio e segue intocado — a
   camada comum já o desenha como o avatar padrão.
   Descartado: sortear ao abrir o formulário e mostrar prévia — a decisão foi só retirar o campo.

## Risks / Trade-offs

- [Sorteio produz combinação pouco harmoniosa, como roupa da cor do fundo] → o contorno da roupa
  (documento 15 §7.1) já mantém o torso legível, e a criança troca na App 05.
- [Guerreiro(a) antigo com texto livre continua com o avatar padrão] → aceito: a decisão não
  pediu regravação, e a troca é da criança.
