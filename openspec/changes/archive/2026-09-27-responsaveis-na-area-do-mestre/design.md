# Design

## Context

Ver `proposal.md` — Why. O padrão está consolidado: a fatia 24 do PRD-02 entregou a mesma
tela na App 03 (`apps/app-03-gestao/src/personas/TelaDeResponsaveis.tsx` e
`ListaDeResponsaveis.tsx`), e `openspec/specs/responsavel-e-vinculo/spec.md` já fixa o que a
rota serve e a quem.

O que existe e condiciona o desenho:

- `GET /v1/responsaveis` já recorta por papel dentro de `responsaveis_visiveis`; a tela não
  filtra nada.
- `POST /v1/responsaveis/{id}/vinculos` já aceita qualquer responsável por identificador — a
  retomada não precisa de rota nova.
- A App 09 já usa `Tabela` de `comum/react` em `direitos/TelaDeDireitos.tsx`.
- A `TelaDeResponsaveis` da App 09 hoje é o fluxo inteiro num componente só: cadastro →
  vínculo → credencial, com `recomecar()` limpando tudo.

## Goals / Non-Goals

**Goals:** a área abrir na lista; o cadastro atrás de um botão; a retomada do vínculo.

**Non-Goals:** tocar o núcleo; mudar o recorte; mexer no passo de credencial provisória, que
segue como está.

## Decisions

1. **Separar a tela em área e formulário, no molde da App 03.** A `TelaDeResponsaveis` atual
   vira o formulário (`FormularioDeResponsavel`), e uma tela nova assume a área: carrega a
   lista, oferece o botão de cadastrar e abre o formulário. _Alternativa descartada:_ acrescentar
   a lista dentro do componente atual, que já carrega quatro estados de passo e ficaria ilegível.

2. **O formulário aceita um responsável já existente**, como o da App 03 — mesma prop
   `responsavelExistente`, mesma semântica. _Alternativa descartada:_ formulário separado para a
   retomada, que duplicaria o seletor e a mensagem do teto.

3. **`Cabecalho` e `Moldura` migram para a tela da área.** O formulário atual os renderiza; com
   a área por cima, quem emoldura é ela, senão a página ganha duas molduras. É o que obriga a
   decisão 1 a ser separação, e não só extração.

4. **A lista repete o padrão de `ListaDeResponsaveis` da App 03**, com `Tabela` de
   `comum/react`. _Alternativa descartada:_ extrair componente comum para `comum/`, pela mesma
   razão da fatia 21 — os dois recortes e as duas molduras diferem, e o ganho é de poucas
   linhas.

5. **Nada de filtro na tela.** A rota já devolve só o que o Mestre alcança; filtrar de novo no
   cliente duplicaria regra de negócio num frontend, contra a hierarquia de autoridade.

## Risks / Trade-offs

- [Separar o componente mexe num arquivo que duas fatias recentes já tocaram — a 21, do nick, e
  a própria estrutura do fluxo] → o nick no vínculo (`rotuloDoVinculo`) vai junto com o
  formulário, sem alteração; os testes existentes do cadastro, do vínculo e da credencial
  continuam valendo e apontam para o mesmo comportamento.
- [A área passa a fazer uma chamada ao abrir, que antes não fazia] → é a mesma chamada que a
  App 03 já faz, paginada, e a falha cai no aviso de erro sem derrubar o cadastro.
