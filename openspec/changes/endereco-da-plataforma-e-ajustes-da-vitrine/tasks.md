# Tasks

## 1. Documentação da decisão (antes do código)

- [ ] 1.1 Documento 02 §1 ("A pergunta de entrada é o que a pessoa traz") e o trecho
      correspondente do documento 08 (chamada "Quero apoiar", "abre pela pergunta…"): a porta
      abre pela doação PIX sem cadastro e em seguida pergunta o que a pessoa traz (`RF-03-78`) —
      verificar por grep que não resta "abre com essa escolha" nem "abre pela pergunta".
- [ ] 1.2 Documento 09 §1, "Já decididos": linha nova "A porta 'Quero apoiar' abre pela doação
      sem cadastro", decisão do fundador de 2026-11-12, com a troca do subtítulo da saudação —
      verificar que a tabela segue com as colunas alinhadas.
- [ ] 1.3 PRD-03: §5.5 itens 3 e 4 e o enunciado do `RF-03-78` na tabela da §6 ("Porta abre pela
      doação sem cadastro e pergunta o que a pessoa traz…") — verificar a linha de 95
      caracteres fora das tabelas.

## 2. Endereço da plataforma

- [ ] 2.1 `docs/index.md` e `README.md`: linha com o link `https://comunidadegame.org` logo após o
      parágrafo de abertura — verificar que aparece no `mkdocs build --strict` e no Lychee.

## 3. App 06 — saudação

- [ ] 3.1 `CabecalhoDaVitrine.tsx` e `testes/TelaDaVitrine.tsx`: subtítulo "Este é um jogo em que
      as partidas acontecem na vida real", e o comentário do componente ajustado (`RF-03-51`,
      `RN-03-01` preservados) — `abertura.test.tsx` passa a esperar a frase nova e roda verde.

## 4. App 06 — porta do convite

- [ ] 4.1 `PortaDoConvite.tsx`: a `<section>` "Doar sem se cadastrar" sobe ao início, com `h2`,
      antes do `h2` "Quero apoiar"; o comentário do componente cita a ordem (`RF-03-78`,
      `RF-03-43`) — verificar na tela que o garfo, as necessidades e o "voltar" seguem iguais.
- [ ] 4.2 Testes da porta: `convite.test.tsx` confere que os dois primeiros títulos são "Doar sem
      se cadastrar" e "Quero apoiar", ambos de nível 2 (cenário "A porta abre pela doação"), e
      `saidaDoBuild.test.ts` confere que "Doar sem se cadastrar" precede "Quero apoiar" em
      `quero-participar.html` — os dois rodam verdes.

## 5. Fechamento

- [ ] 5.1 `openspec/cronograma-de-fatias.md`: linha "—" nova no bloco do PRD-03, situação
      `implementado`, com o slug da change. `docs/prds/index.md` (situação do PRD não muda),
      documento 99 e `nav` do `mkdocs.yml` (nenhum arquivo novo) ficam como estão.
