PRD-02 (Frontend de gestão, App 03) — fatia 26 do `openspec/cronograma-de-fatias.md`.
Atende `RF-02-58` e `RN-02-19` (necessidades em aberto) e `RF-02-45`, `RF-02-97` (saldo
disponível por ponto de apoio), todos já entregues. Decisão de exibição do fundador de
2026-11-13, no molde da fatia 20: só reorganização de tela — não cria RF, RN, rota nem
entidade nova.

## Why

Na área Recursos, cada necessidade em aberto sai como uma linha de texto com os seis campos
colados, sem separador nem rótulo: "Falta: 1.005.00 moedas" é a quantidade `1.00` seguida do
valor `5.00 moedas`, e o Admin lê um número que não existe. O saldo disponível sai como lista
aninhada, sem unidade e com o decimal cru do núcleo ("17.00"). Nenhuma das duas listas tem
título, e as duas se confundem com o formulário de aporte acima delas.

## What Changes

- Recursos ganha títulos de seção: **Necessidades em aberto** e **Saldo disponível**, no mesmo
  nível de **Missões do Apoiador**, que já tem.
- As necessidades em aberto passam a uma **tabela única** (componente `Tabela` de
  `comum/react`), uma linha por par aula + tipo de recurso, com as colunas Aula (data e
  horário), Comunidade, Ponto de apoio, Recurso, Falta e Valor. A ordem é a que o núcleo
  devolve.
- O saldo disponível passa a **uma tabela por ponto de apoio**, sob o título do ponto e da sua
  comunidade, com as colunas Recurso e Saldo — nunca somando entre pontos.
- Quantidade e saldo aparecem com a **unidade** do catálogo de tipos de recurso e no formato
  pt-BR sem zeros decimais supérfluos ("1 un", "17 un"); o valor da necessidade aparece em
  moedas no mesmo formato ("5 moedas", "1 moeda"). A aplicação só formata o número que o
  núcleo devolveu — nunca converte nem soma.
- A área passa à largura densa da `Moldura`, como as demais áreas com tabela.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-de-gestao`: os requisitos "A App 03 abre a área Recursos…" e "A área Recursos
  lista as necessidades de recurso em aberto" passam de lista a tabela, com título de seção,
  unidade e número formatado.

## Impact

- `apps/app-03-gestao/src/recursos/`: `TelaDeRecursos.tsx`, `ListaDeNecessidades.tsx`,
  `ListaDeSaldosDisponiveis.tsx` e `recursos.test.tsx`; um módulo pequeno de formatação de
  número na mesma pasta.
- Nenhuma rota, migração, entidade nem mudança no núcleo; nenhuma mudança em `docs/` além da
  linha do cronograma.
