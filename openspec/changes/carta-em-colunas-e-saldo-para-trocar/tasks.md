# Tasks

## 1. Documentos-fonte — a decisão nasce aqui, antes do código

- [ ] 1.1 No documento 11 §8.2, acrescentar à linha **Guerreiro(a)** da tabela o saldo de pontos
      extras que dá para trocar, e escrever em uma frase que ele é de **tela logada** e nunca de
      superfície pública (`RF-05-82`, invariantes 8, 12 e 23). Verificar que a coluna "o que nunca
      exibe" não foi alterada e que nenhuma outra linha da tabela mudou.
- [ ] 1.2 No documento 15, registrar o alinhamento centralizado da identidade e o arranjo em colunas
      com símbolo acima do rótulo na §8.1; a estrela cheia na frase de desempenho e a vazada na
      seção do saldo na §9; e as três razões medidas na tabela da §3.3 — `ponto-500` sobre `cal-000`
      `1,82:1`, `ponto-700` sobre `tinta-800` `2,34:1` e `ponto-400` sobre `tinta-800` `10,58:1`.
      Verificar que os pisos declarados na própria §3.3 são atendidos pelos valores que ficam em uso.
- [ ] 1.3 Mover a decisão para "Já decididos" no documento 09 §1, com a data de 2026-10-30 e os seis
      pontos elicitados, e conferir os invariantes do documento 99 §6 — em especial o 24 (ponto
      regular, ponto extra e moeda nunca se confundem na tela) e o 23 (só o extra se troca).
- [ ] 1.4 No PRD-05 §9, registrar que `RF-05-82` passa a ser atendido também pela carta, sem que a
      carteira deixe de mostrar as duas contas. Verificar que nenhuma regra nova nasceu no PRD: o
      que ele faz é apontar o documento 11 §8.2 já alterado em 1.1.

## 2. Tokens e peças de desenho em `comum/`

- [ ] 2.1 Dar a `--cor-ponto-contorno` o valor `var(--ponto-400)` no bloco do tema escuro de
      `comum/tokens.css`, e verificar pelo `comum/tokens.test.ts` que o token existe nos dois temas
      e que o contorno deixou de repetir o valor do preenchimento (documento 15 §§3.3, 9).
- [ ] 2.2 Extrair o traçado da estrela cheia de `comum/react/TrioDeEstrelas.tsx` para uma peça
      própria, composta três vezes pelo trio e uma vez pela carta, com preenchimento e contorno
      vindos dos tokens da família ponto (documento 15 §9, design — decisão 2). Verificar que
      `TrioDeEstrelas.test.tsx` segue verde sem alteração de asserção.
- [ ] 2.3 Acrescentar a `comum/react/Icone.tsx` os glifos **medalha**, **pincel** e **estrela
      vazada**, na grade de `24` px com traço de `2` px e `currentColor`, e cobri-los em
      `Icone.test.tsx` com o cenário de que nenhum deles é silhueta de família de badge, o escudo da
      marca ou o círculo da moeda (documento 15 §§8.3, 8.4, 9, 11.1, invariante 24).

## 3. A carta em `comum/react`

- [ ] 3.1 Centralizar avatar, identificação e frase de desempenho em `.cg-carta`, nas quatro
      variantes, e pôr a estrela cheia ao lado da frase na variante Guerreiro(a) (documento 11 §8.2,
      documento 15 §§8.1, 9). Verificar que a carta do Apoiador passa a cumprir o "avatar
      centralizado" que o §8.2 já exigia e que o CSS não cumpria.
- [ ] 3.2 Pôr as seções da variante Guerreiro(a) em colunas — símbolo acima, rótulo no meio,
      conteúdo abaixo —, com duas por linha no celular e todas em linha a partir do marco de `768`
      px, alinhadas pelo topo e sem trilha vazia quando houver três seções (documento 15 §4, design
      — decisão 3).
- [ ] 3.3 Acrescentar a `CartaDeGuerreiro` o campo opcional do saldo de pontos extras, **fora** de
      `guerreiroEstaCompleto`, e apresentar a quarta seção com a estrela vazada e o rótulo que diz
      ser o saldo que dá para trocar (`RF-05-82`, design — decisão 1). Verificar que a carta
      continua se apresentando quando o campo está ausente.
- [ ] 3.4 Cobrir em `comum/react/carta.test.tsx` os cenários dos deltas de `camada-visual-comum`: a
      identidade centralizada nas quatro variantes, as colunas nas duas larguras, o arranjo com três
      seções, a estrela cheia na frase e a vazada na seção do saldo, o acumulado que não entra na
      seção, e a ausência do saldo que não torna a carta incompleta. As asserções passam a se apoiar
      em rótulo e papel acessível, não na ordem dos nós (design — risco 1).

## 4. A montagem e as três telas

- [ ] 4.1 Em `comum/carta/api.ts`, ler `GET /v1/eu/pontos-extras`, e em `CartaDoGuerreiro.tsx`
      montar a quarta seção dentro da leitura em paralelo que já existe, com a falha dela deixando o
      campo ausente e a recusa de sessão seguindo tratada como recusa de sessão (`RF-05-82`,
      `RF-05-50`, design — decisão 7). Verificar que o acumulado devolvido pela rota não chega à
      carta.
- [ ] 4.2 Cobrir em `apps/app-05-guerreiro/src/carteira/MinhaCarta.test.tsx` que a carta da Área
      traz a seção do saldo, e em `MinhaCarteira.test.tsx` que o bloco de apoio **continua** com o
      acumulado, o saldo e o aviso que explica a diferença (`RF-05-82`, `RN-05-39`, `RN-05-40`,
      decisão do fundador de 2026-10-30).
- [ ] 4.3 Verificar, por teste em `apps/app-06-vitrine`, que o adaptador da carta pública não ganhou
      o campo do saldo, que a carta pública não apresenta seção alguma de saldo e que ela continua
      se apresentando com as três seções (`RF-03-06`, `RF-01-21`, invariantes 8 e 12).
- [ ] 4.4 Verificar, por teste no desfecho da presença da App 01, que a carta ali apresenta a quarta
      seção, por montar a mesma carta da Área do Guerreiro(a) (`RF-04-67`, `RF-05-50`).

## 5. Fechamento da fatia

- [ ] 5.1 Marcar a fatia como `implementado` em `openspec/cronograma-de-fatias.md`, trocando o
      recorte previsto pelo slug da change. A situação do PRD-05 não muda, então `docs/prds/index.md`
      fica como está; o documento 99 também, porque nenhuma relação entre documentos mudou e nenhum
      arquivo novo entrou em `docs/`.
