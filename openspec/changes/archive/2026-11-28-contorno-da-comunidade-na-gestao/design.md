# Design — Contorno da comunidade na gestão

## Context

Só App 03. O núcleo já tem o que a tela consome (`openspec/specs/comunidade-virtual/spec.md`,
requisito "O Admin cadastra e substitui o contorno da comunidade"):

- `PUT /v1/comunidades/{id}/contorno`, corpo `{geometria, origem_osm}`, só Admin; devolve
  `ContornoSaida` — `geometria`, `origem_osm`, `copiado_em`, `credito`, `licenca`. Recusa 422
  com `campo` igual a `geometria` ou `origem_osm`, 403 `permissao_negada`, 404.
- `GET /v1/comunidades` já devolve `contorno: ContornoSaida | null` em cada item.

A tela segue o padrão de `comunidades/` e de `conteudo-institucional/FormularioDaSecao.tsx`
(`textarea` com `cg-campo`, erro por campo vindo de `ErroDaApi.campo`).

## Goals / Non-Goals

**Goals:** a lista mostra a situação do contorno; o Admin cadastra e substitui o contorno.

**Non-Goals:** desenhar o contorno (é a vitrine, fatia 15 do PRD-03); validar a geometria na
tela; ler o OSM automaticamente.

## Decisions

1. **A ação fica no item da lista, não numa tela nova.** Um botão por comunidade, só para
   `sessao.papel === "admin"`, rotulado "Cadastrar contorno" ou "Substituir contorno" conforme
   `contorno` seja nulo ou não; abre o `FormularioDeContorno` logo abaixo do item, um por vez.
   _Descartada:_ ficha da comunidade com rota própria — a App 03 não tem ficha de comunidade, e
   criar uma é maior que a fatia.
2. **O texto colado é desembrulhado até a geometria.** O que o Admin copia do OSM costuma vir
   como `Feature` ou `FeatureCollection`, e o núcleo aceita só a geometria. O formulário envia
   `objeto.geometry` para `Feature`, `features[0].geometry` para `FeatureCollection` com **uma**
   feição, e o objeto como veio em qualquer outro caso — o núcleo recusa o que não for polígono
   ou multipolígono. Não é regra de produto: é o mesmo dado, sem o invólucro. _Descartada:_
   exigir que o Admin recorte a geometria à mão.
3. **A tela só confere vazio e JSON malformado.** Tipo, anel fechado, faixa de coordenada e
   padrão `way/`/`relation/` são do núcleo (fonte única); a mensagem 422 vai ao campo que o
   núcleo indicar, pelo `erro.campo`.
4. **Data e atribuição vêm do núcleo.** A lista exibe `origem_osm`, `copiado_em` em
   `toLocaleDateString("pt-BR")` e `credito · licenca` como chegam, sem literal na tela.
   Gravado, a lista recarrega, como já faz `aoCriar`.

## Risks / Trade-offs

- `FeatureCollection` com várias feições não é unida na tela: o núcleo a recusa, e o Admin cola
  a feição certa. Unir polígonos seria decidir geometria, que não é da gestão.
- O GeoJSON de uma relação grande pode ter centenas de KB; o `textarea` comporta, e o núcleo não
  declara limite de tamanho.
