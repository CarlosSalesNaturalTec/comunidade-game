# Tasks

## 1. A camada `comum/narracao`

- [ ] 1.1 Criar `comum/narracao/narracao.ts`: tipos mínimos da síntese do navegador, o tipo
      `Fala` com `texto` e `nick` **e mais nada** (design — decisão 2), `existeSinteseDeFala()`,
      a escolha de voz pt-BR depois de `voiceschanged` preferindo a local (design — decisão 5),
      `falar`, `cancelar` e `armar`
- [ ] 1.2 Criar `comum/narracao/ProvedorDeNarracao.tsx` e o gancho de consumo: estado ligado
      (em `localStorage`, leitura e escrita em `try/catch`, padrão **ligado**), estado armado e
      a voz; sem provedor montado o gancho não fala (design — decisão 3)
- [ ] 1.3 Exportar em `comum/narracao/indice.ts`
- [ ] 1.4 Testar em `comum/narracao/narracao.test.ts`, com `speechSynthesis` falso instalado
      por `vi.stubGlobal` no padrão de `comum/fala/fala.test.ts`: fala o texto declarado;
      substitui `{nick}`; **não existe caminho** para outro dado pessoal; nasce ligada sem
      escolha guardada; `localStorage` que lança não derruba a camada; sem voz pt-BR fica em
      silêncio sem erro; e cancelar interrompe a fala em curso.
      `npx vitest run comum/narracao` verde

## 2. Os componentes comuns declaram a narração deles

- [ ] 2.1 `comum/react/Cabecalho.tsx`: narrar o `titulo` ao montar, com prop `narracao`
      opcional que o substitui e admite calar. O **subtítulo não é narrado** por padrão
      (design — decisão 4)
- [ ] 2.2 `comum/react/Aviso.tsx`: narrar o conteúdo ao montar, com a mesma prop opcional
- [ ] 2.3 Garantir que texto que existir **só** para a narração saia `aria-hidden`, e que o
      texto já visível na tela **não** seja escondido do leitor de tela (design — decisão 8)
- [ ] 2.4 Testar em `comum/react`: o cabeçalho fala o título; a narração declarada substitui o
      título falado sem mudar o escrito; o componente calado não fala; e sem provedor montado
      nada fala. `npx vitest run comum/react` verde

## 3. A App 01 liga, desliga e arma

- [ ] 3.1 `apps/app-01-aula-presencial/src/App.tsx`: montar `ProvedorDeNarracao` ao lado do
      `ProvedorDeSessao`
- [ ] 3.2 `apps/app-01-aula-presencial/src/inicio/TelaInicial.tsx`: o controle de ligar e
      desligar, com rótulo textual e alvo de toque de 48 px. Conferir que encerrar a sessão de
      trabalho **não** apaga a escolha — ela não é chave da sessão
- [ ] 3.3 `apps/app-01-aula-presencial/src/sessao-de-trabalho/AparelhoDaAula.tsx`: o controle
      de **iniciar** antes da primeira fala, que chama a síntese com enunciado vazio dentro do
      próprio gesto e marca o provedor como armado; não apresentado com a narração desligada
      (design — decisão 6)
- [ ] 3.4 Testar em `apps/app-01-aula-presencial/src/inicio/inicio.test.tsx` e
      `sessao-de-trabalho.test.tsx`: o controle está na tela inicial; a escolha sobrevive ao
      atendimento seguinte e a encerrar a sessão de trabalho; carregada e sem gesto nada fala e
      o iniciar aparece; desligada, o iniciar não aparece.
      `npx vitest run apps/app-01-aula-presencial -t "narração"` verde

## 4. O enunciado do Quiz ao Vivo

- [ ] 4.1 `apps/app-01-aula-presencial/src/quiz/TelaDaPartida.tsx`: falar o enunciado no mesmo
      ponto em que `perguntaIdConhecidaRef` detecta pergunta nova — **nunca** num efeito sobre
      o objeto da pergunta, que a sondagem recria a cada 2 s (design — decisão 7). Não falar
      alternativas, resultado nem avisos de rede
- [ ] 4.2 Testar em `apps/app-01-aula-presencial/src/quiz/quiz.test.tsx`: a pergunta nova é
      falada uma vez; a sondagem que devolve a mesma pergunta **não** fala de novo; o resultado
      liberado não é falado. `npx vitest run apps/app-01-aula-presencial -t "quiz"` verde

## 5. Ouvir o conteúdo de missão em texto

- [ ] 5.1 `comum/trilha/Missao.tsx`: botão de alto-falante com rótulo textual junto do conteúdo
      do tipo `texto`, que fala o corpo ao ser acionado; não apresentado para imagem, vídeo,
      link e arquivo, nem com a narração desligada
- [ ] 5.2 Confirmar que o conteúdo **não** é falado ao entrar na tela
- [ ] 5.3 Testar em `comum/trilha/trilha.test.tsx`: o controle aparece só no conteúdo em texto;
      acioná-lo fala o corpo; o conteúdo não é falado sozinho.
      `npx vitest run comum/trilha` verde

## 6. Roteiro das telas da App 01

- [ ] 6.1 Percorrer as telas da App 01 e conferir o que cada uma passa a falar pelo `Cabecalho`
      e pelo `Aviso`; declarar `narracao` própria onde o texto escrito não for o que convém
      ouvir, e calar onde a fala não ajudar
- [ ] 6.2 Onde houver saudação a quem chegou, usar o marcador `{nick}` — **nunca** o nome
      (`RN` da fronteira, design — decisão 2)
- [ ] 6.3 Conferir tela a tela, com a narração ligada, que nenhuma fala rótulo de botão nem
      texto de interface

## 7. Fechamento

- [ ] 7.1 Marcar a fatia 23 como implementada em `openspec/cronograma-de-fatias.md`, e
      registrar ali que **as outras sete aplicações seguem sem roteiro** — a camada existe e
      está inerte nelas
- [ ] 7.2 Rodar uma vez os pacotes tocados:
      `npx vitest run comum apps/app-01-aula-presencial` e
      `npx biome check comum apps/app-01-aula-presencial` verdes
- [ ] 7.3 Conferir que a App 05 não regrediu — ela consome `comum/react` e `comum/trilha` e
      **não** monta o provedor: `npx vitest run apps/app-05-guerreiro` verde, e nenhuma tela
      dela passa a falar
