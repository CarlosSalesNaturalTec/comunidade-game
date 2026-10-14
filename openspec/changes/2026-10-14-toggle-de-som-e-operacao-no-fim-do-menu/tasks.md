# Tasks

Fatia 25 do PRD-04. Identificadores alcançados: `RF-04-71` e `RF-04-49`; a parte da narração
responde ao documento 15 §5.1 e não tem `RF`/`RN` no PRD-04 (ver `proposal.md`).

## 1. A camada de narração sem o estado de armar

- [ ] 1.1 Em `comum/narracao/ProvedorDeNarracao.tsx`: fazer `ligada` nascer `false` e sair
  `lerEscolhaDoAparelho`, `gravarEscolhaDoAparelho` e `CHAVE_DA_NARRACAO_NO_APARELHO` (também de
  `comum/narracao/indice.ts`); tirar `armada` e `armarNarracao` de `ContextoDeNarracaoValor` e de
  `INERTE`; chamar `armar()` dentro do `alternarNarracao` que liga; `narrar` passa a exigir
  `ligada && voz` e `ouvir` só `voz` (design — decisões 1, 2 e 3). Verificar pela compilação de
  tipos dos dois pacotes: nenhum consumidor resta citando `armada` ou a chave.
- [ ] 1.2 Em `comum/trilha/Missao.tsx`: trocar a guarda de `ControleDeOuvirOConteudo` de `ligada`
  para `disponivel` (design — decisão 3). Verificar que com o provedor ausente o controle
  continua fora da tela — é o que mantém a App 05 inalterada.
- [ ] 1.3 Ajustar `comum/narracao/ProvedorDeNarracao.test.tsx`: inverter os casos de nascer
  ligada, apagar os de armar e cobrir os cenários dos quatro requisitos acrescentados em
  `specs/narracao-por-sintese-de-fala` — nasce desligada, ligar já arma sem segundo controle,
  desligada nada fala sozinho, a escolha persiste entre atendimentos, a recarga devolve ao
  desligado e o texto longo se ouve com a narração desligada.
- [ ] 1.4 Ajustar `comum/react/narracao.test.tsx` e `comum/trilha/trilha.test.tsx` (que usa a
  chave do `localStorage`) à camada sem armar e sem persistência, mantendo a cobertura da camada
  inerte, que agora guarda também o controle de ouvir.

## 2. O botão de alternância e os quatro glifos na camada visual

- [ ] 2.1 Acrescentar os glifos `som`, `som-desligado`, `encerrar` (porta com flecha) e
  `momento-de-troca` à união `NomeDeGlifo` e ao mapa de `comum/react/Icone.tsx`, na grade de 24
  px com traço de 2 px de `currentColor` (design — decisão 8). Verificar que
  `comum/react/Icone.test.tsx`, com os quatro na lista, segue provando que nenhum ícone vem de
  domínio de terceiro e que nenhum declara cor.
- [ ] 2.2 Criar `BotaoDeAlternancia` em `comum/react` (exportado por `comum/react/indice.ts`),
  com `rotulo` obrigatório em `aria-label`, `aria-pressed` a partir de `ligado`, glifo por estado
  e o alvo de toque e o foco do `cg-botao`, mais o modificador de caixa quadrada em
  `comum/react/estilos.css` (design — decisão 4). Verificar pelos cenários de
  `specs/camada-visual-comum`: o rótulo é obrigatório e alcança o leitor de tela, o estado é
  anunciado sem depender de cor, e o alvo de toque é o dos demais botões.
- [ ] 2.3 Dar a `comum/react/Cabecalho.tsx` o slot opcional do canto, ao lado de `acao` (design —
  decisão 5). Verificar que as telas que não o passam renderizam como antes — a suíte de
  `comum/react` e as das outras aplicações cobrem isso sem alteração.
- [ ] 2.4 Escrever o teste do `BotaoDeAlternancia` e do slot novo do `Cabecalho` em
  `comum/react`, cobrindo os cenários dos dois requisitos de `specs/camada-visual-comum`,
  inclusive o glifo distinto por estado.

## 3. O alternador de som na tela inicial da App 01

- [ ] 3.1 Em `apps/app-01-aula-presencial/src/inicio/TelaInicial.tsx`: substituir
  `ControleDaNarracao` — botão de rótulo textual e parágrafo de estado — pelo
  `BotaoDeAlternancia` no slot do canto do `Cabecalho`, com os glifos `som`/`som-desligado` e o
  rótulo "Ligar a leitura das telas em voz alta" / "Desligar a leitura das telas em voz alta".
  Verificar pelos cenários do requisito "A tela inicial liga e desliga a narração do aparelho" em
  `specs/aplicacao-da-aula-presencial`.
- [ ] 3.2 Remover `ConviteParaIniciarANarracao` de
  `apps/app-01-aula-presencial/src/sessao-de-trabalho/AparelhoDaAula.tsx`, atendendo ao requisito
  removido "A App 01 arma a narração na primeira interação". Verificar que nenhuma tela da
  aplicação apresenta controle de iniciar.
- [ ] 3.3 Em `apps/app-01-aula-presencial/src/index.css`: apagar `cg-narracao`,
  `cg-narracao-convite` e `cg-narracao__estado`.
- [ ] 3.4 Ajustar o bloco "a narração das telas liga e desliga na tela inicial" de
  `apps/app-01-aula-presencial/src/inicio/inicio.test.tsx` (inclui a asserção sobre
  `localStorage`), mais `sessao-de-trabalho.test.tsx`, `precarga.test.tsx` e `quiz.test.tsx`, que
  acionam o controle de iniciar para armar a narração. Cobrir ali os cenários do alternador no
  canto do cabeçalho, da ausência dele nas demais telas e da recarga que devolve ao desligado.
- [ ] 3.5 Cobrir, no teste das trilhas da App 01, o cenário "Com a narração desligada o controle
  continua lá" do requisito do conteúdo de missão em texto.

## 4. Encerrar e abrir a troca no fim do menu

- [ ] 4.1 Em `TelaInicial.tsx`: tirar o `acao` de encerramento do `Cabecalho` e o bloco
  `cg-momento-de-troca`, e pôr os dois como cartões `cg-caminho` ao fim de `cg-caminhos`, sob o
  separador "Para quem opera o aparelho", com a abertura da troca só quando
  `podeAbrirMomentoDeTroca` e o encerramento por último, com o glifo `encerrar` (`RF-04-71`,
  `RF-04-49`, design — decisão 6). Verificar pelos dois cenários novos do requisito da tela
  inicial em `specs/aplicacao-da-aula-presencial`.
- [ ] 4.2 Levar o "Abrindo…" ao próprio cartão por `cg-caminho:disabled` e o `Aviso tipo="erro"`
  para abaixo da lista (design — decisão 7). Verificar que a falha de abertura continua anunciada
  e que nenhum cartão se desloca sob o dedo enquanto ela aparece.
- [ ] 4.3 Acrescentar o separador a `apps/app-01-aula-presencial/src/index.css`, sem alterar
  `cg-caminho`, e apagar `cg-momento-de-troca`.
- [ ] 4.4 Ajustar `inicio.test.tsx`, `troca.test.tsx` e `fila.test.tsx`, que alcançam o
  encerramento e a abertura da troca pelos rótulos antigos, e cobrir a ordem dos dois cartões, o
  separador e o aparelho que não pode abrir a troca.

## 5. Documentação

- [ ] 5.1 Em `docs/15-identidade-visual.md` §5.1, reescrever na tabela as linhas "Liga e
  desliga", "Primeiro áudio", "Onde mora o estado" e "Fala sob toque" — uma linha cada, sem
  parágrafo novo e sem tocar a §5, cuja regra "rótulo textual visível ou acessível" já cobre o
  glifo. Verificar por `npm run lint` e `mkdocs build --strict`.
- [ ] 5.2 Registrar a decisão do fundador de 2026-10-14 em "Já decididos" do
  `docs/09-topicos-em-aberto-e-sugestoes.md` §1, em uma linha.
- [ ] 5.3 Marcar a fatia 25 como `implementado` em `openspec/cronograma-de-fatias.md`. O PRD-04,
  `docs/prds/index.md`, o documento 99 e a `nav` do `mkdocs.yml` ficam intocados: nenhum
  `RF`/`RN` muda de enunciado, a situação do PRD-04 não muda, nenhuma relação entre documentos
  muda e nenhum arquivo nasce em `docs/`.
