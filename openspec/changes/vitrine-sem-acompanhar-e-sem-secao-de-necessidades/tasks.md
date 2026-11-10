# Tasks

## 1. Decisão descida pelo fluxo (antes do código)

- [ ] 1.1 Documento 03 §8: o item "Sem favoritos" passa a dizer que a vitrine **não oferece**
      ação de favoritar nem de acompanhar — acompanhar é função de quem se cadastra, na Área do
      Apoiador; "Como apoiar" diz que a chave PIX **e** as necessidades chegam ao visitante pela
      porta da chamada; a tabela de recortes tira "as necessidades em aberto" do recorte padrão
      (`RF-03-40` retirado, `RF-03-43`, `RF-03-47`). Verificar: `grep -n "favoritar ou
      acompanhar\|seção própria da abertura"` em `docs/03-*` vazio.
- [ ] 1.2 Documento 09 §1, "Já decididos": linha nova com as duas decisões do fundador de
      2026-11-10; as linhas "Ordem das seções da abertura da vitrine" (sem "Necessidades em
      aberto") e "'Necessidades em aberto' é seção própria" (revogada em 2026-11-10, as
      necessidades ficam na porta) ajustadas no lugar. Verificar: leitura das três linhas.
- [ ] 1.3 PRD-03: sai o `RF-03-40` da §6.4; §5.4 item 5 e §5.5 item 1 deixam de citar a seção
      própria e o pedido de favoritar; §3 (linha das necessidades) aponta a porta; §13 registra a
      retirada do `RF-03-40` com a data. Verificar: `grep -n "RF-03-40"` no PRD-03 só acha a
      linha da §13.

## 2. App 06 — páginas individuais

- [ ] 2.1 `convite/ChamadaDeParticipacao.tsx`: saem o botão "Quero acompanhar" e o parágrafo
      `cg-chamada__ajuda`; o comentário deixa de citar o `RF-03-40` (`RF-03-39`, `RN-03-25`,
      design — decisão 1). Estilo de `cg-chamada__ajuda` que ficar órfão sai do CSS.
      Verificar: teste da 4.1.

## 3. App 06 — abertura

- [ ] 3.1 `pages/index.astro`: sai a seção "Necessidades em aberto" e o import; o comentário do
      topo deixa de falar em necessidades como seção. `institucional/SecoesInstitucionais.tsx`:
      apaga `NecessidadesEmAberto` e o import de `ListaDeNecessidades`. Verificar: teste da 4.3.
- [ ] 3.2 `necessidades/useNecessidades.ts`: o comentário passa a dizer que a porta é a única
      consumidora (design — decisão 2). `testes/TelaDaVitrine.tsx`: sai a seção, para a
      composição de teste seguir igual à página servida. Verificar: `biome check` sem import
      órfão.

## 4. Testes

- [ ] 4.1 `testes/convite.test.tsx`: os quatro casos das páginas individuais afirmam "Quero
      apoiar" visível e **nenhum** botão "Quero acompanhar" (`RF-03-39`); saem os dois casos de
      "acompanhar chega à mesma porta" (`RF-03-40`); o caso do `RF-03-41` deixa de afirmar o
      parágrafo "A vitrine não guarda favoritos".
- [ ] 4.2 `testes/semRastro.test.tsx`: o caso do `RF-03-38`/`RN-03-15`/`RN-03-16` passa a
      acionar "Quero apoiar" na página do Guerreiro(a), em vez de "Quero acompanhar", e segue
      afirmando aparelho vazio após escolha de modalidade e recusa.
- [ ] 4.3 `testes/necessidadesEmAberto.test.tsx`: sai o caso "a seção da abertura aparece por
      si"; o caso da leitura única passa a afirmar uma leitura na porta; os casos do
      `RF-03-47`, `RF-03-10`, `RN-03-18` e do `RF-03-45` seguem, exercitados na porta, mais um
      caso afirmando que a abertura **não** tem cabeçalho "Necessidades em aberto".
      `testes/portfolioERanking.test.tsx` e `testes/saidaDoBuild.test.ts`: a ordem esperada
      passa a nove seções, sem "Necessidades em aberto".

## 5. Documentação

- [ ] 5.1 `openspec/cronograma-de-fatias.md`: linha "—" nova no bloco do PRD-03 com o slug da
      change e situação `implementado`. `docs/prds/index.md` e documento 99 não mudam — a
      situação do PRD-03 e a relação entre documentos ficam iguais; `mkdocs.yml` não muda, sem
      arquivo novo em `docs/`.
