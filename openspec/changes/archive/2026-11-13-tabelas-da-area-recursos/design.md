# Design

## Context

A área Recursos já existe (`openspec/specs/aplicacao-de-gestao/spec.md`, requisitos da área
Recursos) e já lê o que precisa: as necessidades de `GET /v1/vitrine/necessidades`, o saldo de
`GET /v1/pontos-de-apoio/{id}/saldos` e o catálogo de `GET /v1/tipos-de-recurso`, que traz a
`unidade`. A fatia só muda a apresentação; o componente `Tabela` de `comum/react` já serve
Personas e Direitos.

## Goals / Non-Goals

**Goals:** cada campo da necessidade e do saldo na sua célula, com unidade e número legível, e
as duas seções com título.

**Non-Goals:** rota, campo ou ordenação nova; mexer no formulário de aporte, nas aulas
confirmadas pelo aporte ou em Missões do Apoiador.

## Decisions

1. **Tabela única para as necessidades e uma tabela por ponto para o saldo** — escolha do
   fundador em 2026-11-13. Descartado: agrupar as necessidades por aula; tabela única de saldo
   com coluna de ponto.
2. **Nenhuma coluna recolhida.** O `recolhida` da `Tabela` esconde a coluna abaixo de 768 px,
   e a spec exige todos os campos; a rolagem horizontal fica confinada ao componente.
3. **Unidade pelo catálogo já carregado.** `TelaDeRecursos` já tem `tipos`; passa a expor
   `unidadeDoTipoDeRecurso(id)`, e as duas listas a recebem por prop. Tipo fora do catálogo
   mostra o número sem unidade. Descartado: acrescentar a unidade às rotas do núcleo.
4. **Formatação num módulo da pasta** — `recursos/formatacao.ts`, com `formatarQuantidade(valor,
   unidade?)` e `formatarMoedas(valor)`: `Number(valor).toLocaleString("pt-BR", {
   maximumFractionDigits: 2 })`, "moeda" no singular quando o valor é 1, o texto cru do núcleo
   se não for número. Só formata; não converte nem soma (`RN-02-19`). Descartado: importar o
   `formatarMoedas` da App 08, que recebe reais e converte.
5. **Títulos `h2` por seção e `h3` por ponto de apoio** ("Centro comunitário — Guerreira
   Zeferina"); `ListaDeSaldosDisponiveis` recebe `nomeDaComunidade`.
6. **`Moldura variante="densa"`** na área, como em Direitos, para a tabela de seis colunas
   caber no desktop.

## Risks / Trade-offs

- No celular, a tabela de necessidades rola de lado dentro do próprio contêiner — aceito pela
  decisão 2.
