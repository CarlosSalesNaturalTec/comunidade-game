# Tasks

## 1. Formatação

- [ ] 1.1 Criar `apps/app-03-gestao/src/recursos/formatacao.ts` com `formatarQuantidade` e
      `formatarMoedas` — pt-BR sem zeros supérfluos, unidade opcional, singular "moeda",
      texto cru quando não for número, sem conversão (`RF-02-58`, `RF-02-45`, `RN-02-19`)

## 2. Telas

- [ ] 2.1 `ListaDeNecessidades.tsx`: título "Necessidades em aberto" e `Tabela` com as colunas
      Aula, Comunidade, Ponto de apoio, Recurso, Falta (com unidade) e Valor (em moedas, ou
      "Sem valor de referência vigente"), na ordem do núcleo, sem coluna recolhida; mantém os
      textos de carregando e de lista vazia; recebe `unidadeDoTipoDeRecurso` (`RF-02-58`,
      `RN-02-19`)
- [ ] 2.2 `ListaDeSaldosDisponiveis.tsx`: título "Saldo disponível", um `h3` por ponto de apoio
      com o nome da comunidade e uma `Tabela` Recurso | Saldo (com unidade), sem soma entre
      pontos; mantém os textos de carregando e de sem saldo; recebe `nomeDaComunidade` e
      `unidadeDoTipoDeRecurso` (`RF-02-45`, `RF-02-97`)
- [ ] 2.3 `TelaDeRecursos.tsx`: `Moldura variante="densa"`, `unidadeDoTipoDeRecurso` derivado de
      `tipos` e repassado às duas listas, `nomeDaComunidade` repassado ao saldo (`RF-02-58`,
      `RF-02-45`)

## 3. Testes

- [ ] 3.1 `formatacao.test.ts`: `1.00` + `un` → `1 un`; `17.00` → `17`; `1.50` → `1,5`;
      `5.00` → `5 moedas`; `1.00` → `1 moeda`; valor não numérico volta cru (`RN-02-19`)
- [ ] 3.2 `recursos.test.tsx`: ajustar os cenários de necessidade e de saldo à tabela — falta e
      valor em células separadas (`1 un` e `5 moedas`), tipo sem vigência sem moedas, lista
      vazia em texto, títulos de seção, `h3` do ponto com a comunidade, saldo `17 un` e sem
      soma entre dois pontos (`RF-02-58`, `RF-02-45`, `RF-02-97`)

## 4. Documentação

- [ ] 4.1 Marcar a fatia 26 do PRD-02 como implementada em `openspec/cronograma-de-fatias.md`,
      com o slug da change; a change não muda `docs/`, PRD, documento 09 nem documento 99
