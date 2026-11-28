# Tarefas — Contorno da comunidade na gestão

## 1. Cliente do núcleo

- [x] 1.1 Em `apps/app-03-gestao/src/comunidades/api.ts`, acrescentar `ContornoDaComunidade`
      (`geometria`, `origem_osm`, `copiado_em`, `credito`, `licenca`) e o campo
      `contorno?: ContornoDaComunidade | null` em `ComunidadeDaLista` — opcional no tipo para
      não reescrever as fixtures das outras áreas, lido como nulo quando ausente; criar
      `gravarContorno(idDaComunidade, {geometria, origem_osm}, token)` sobre
      `PUT /v1/comunidades/{id}/contorno` (`RF-02-122`, `RF-08-33`)

## 2. Formulário do contorno

- [x] 2.1 Criar `comunidades/FormularioDeContorno.tsx`: `textarea` do GeoJSON e `Campo` do
      elemento de origem; vazio e JSON malformado apontados no campo sem chamar o núcleo;
      desembrulho de `Feature` e de `FeatureCollection` de uma feição até a geometria (design,
      Decisão 2); 422 no campo de `erro.campo`, 403 em aviso, recusa de sessão tratada;
      rótulo de envio "Cadastrar" ou "Substituir" conforme haja contorno (`RF-02-122`,
      `RF-08-33`)

## 3. Lista e tela

- [x] 3.1 Em `ListaDeComunidades.tsx`, mostrar em cada item a situação do contorno — origem,
      data da cópia em pt-BR e `credito · licenca` do núcleo, ou "Ainda sem contorno." em
      `EstadoDaLista` — e, quando a tela informar que o operador é Admin, o botão "Cadastrar
      contorno" ou "Substituir contorno", abrindo o formulário sob o item, um por vez; estilos
      em `ListaDeComunidades.css` (`RF-02-122`, `RN-08-31`)
- [x] 3.2 Em `TelaDeComunidades.tsx`, passar à lista o `podeCriar` já calculado como permissão
      do contorno e recarregar a lista ao gravar (`RF-02-122`, PRD-02 §4)

## 4. Testes

- [x] 4.1 Em `comunidades/comunidades.test.tsx`, cobrir a situação na lista: sem contorno sai
      como informação, sem `role="alert"`; com contorno mostra origem, data e crédito com
      licença; Mestre não vê a ação (`RF-02-122`, `RN-08-31`)
- [x] 4.2 No mesmo arquivo, cobrir o formulário: Admin cadastra e a lista recarrega com o
      contorno; ação de substituir em comunidade com contorno; `Feature` e `FeatureCollection`
      de uma feição enviam só a geometria; vazio e JSON malformado apontados sem chamar
      `gravarContorno`; 422 em `geometria` e em `origem_osm` no campo certo; 403 em aviso
      (`RF-02-122`, `RF-08-33`)

## 5. Documentação

- [x] 5.1 Em `openspec/cronograma-de-fatias.md`, marcar a fatia 34 do PRD-02 como
      `implementado`, com o slug `2026-11-28-contorno-da-comunidade-na-gestao`. Nada em `docs/`
      muda: sem decisão nova, requisito novo nem arquivo novo (`RF-02-122`)
