# Design — Aportes na ficha do adulto

## Context

O padrão já existe em `openspec/specs/poder-sustentador/spec.md`, em duas leituras:

- `GET /meus-aportes`: os aportes do próprio Apoiador, sem reais;
- `GET /provedores/{id}/poder-sustentador`: pública, só moedas, com 404 indistinto para
  Guerreiro(a) e responsável.

A ficha da gestão (`personas/FichaDoAdulto.tsx`) só mostra o que vem de `GET /mestres` e de
`GET /apoiadores`. Esta fatia junta essas peças numa leitura nova, só do Admin.

## Decisions

1. **Rota nova `GET /v1/provedores/{id}/aportes`, em `poder_sustentador/rotas.py`.**
   - Reaproveita `poder_sustentador_de`, `_PAPEIS_QUE_NAO_SAO_PROVEDOR` e a resolução de nome
     do tipo e do ponto de apoio que `meus_aportes` já faz.
   - Descartado estender `GET /meus-aportes`: a spec dela proíbe reais, e ela é do Apoiador em
     sessão.
   - Descartado embutir os aportes em `GET /apoiadores` e em `GET /mestres`: as listas ficariam
     pesadas, e a ficha só precisa dos aportes de uma pessoa.
2. **Ordem das guardas: o papel antes da existência.** Quem não é Admin recebe 403 antes de
   qualquer consulta, então a recusa não revela se o identificador existe. Para o Admin, o 404
   indistinto segue o precedente da leitura pública.
3. **Comprovante como booleano.** `tem_comprovante = comprovante_referencia is not None`. A
   referência no armazenamento nunca sai (`RN-07-22`).
4. **Declarações pendentes na mesma resposta**, filtradas por `situacao == pendente` e
   ordenadas pela data, da mais recente à mais antiga. Uma chamada só por ficha aberta, sem rota
   de fila nova.
5. **Na App 03, a ficha busca ao abrir.** Ela chama a rota pelo `adulto.id` e mostra o estado
   de carregando e de erro com `EstadoDaLista` e `Aviso`. Valores e quantidades usam
   `formatarMoedas` e `formatarQuantidade`, que hoje estão em `recursos/formatacao.ts`. Os reais
   usam `Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" })`, local à ficha.

## Risks / Trade-offs

- [As declarações da App 08 ficam visíveis sem ação na gestão] → Registrado na proposta como
  risco. Homologar ou recusar pela tela é fatia própria, se o fundador decidir abri-la.
- [Os reais ganham uma primeira tela fora do pagamento] → A exceção entra no documento 04 §1 e
  no invariante 16. Um teste garante que `GET /meus-aportes` e a leitura pública seguem sem
  reais.

## Migration Plan

Nenhuma migração: todo campo já existe. O rollback é reverter o PR.
