# Design

## Context

- A narração (`comum/narracao/`) fala o enunciado e as alternativas a cada pergunta alcançada,
  pela identidade da pergunta (spec `narracao-por-sintese-de-fala`). `falar()` não avisa o fim.
- A transcrição (`comum/fala/`) já existe pela Web Speech API, com uma fala por abertura,
  `continuous` e `interimResults` desligados (change `2026-09-11-pergunta-falada-transcrita-no-aparelho`).
- A sondagem é `comum/trilha/Sondagem.tsx`, que monta `DesafioDeDesbloqueio` — a mesma tela nas
  Apps 01 e 05. As escolhas vivem em `escolhas: Record<string, number>` e vão juntas na submissão
  (`RF-05-89`).
- No núcleo, `RespostaDoDesbloqueioEntrada` exige `alternativa_escolhida: int`, e
  `RespostaDaSubmissao.alternativa_escolhida` é `NOT NULL`. `Missao.e_sondagem` marca a sondagem.

## Goals / Non-Goals

**Goals:** janela de escuta de 5 s após a fala da pergunta, só na sondagem e só com o áudio
ligado; ligação à alternativa aproximada; resposta literal sem alternativa aceita pelo núcleo.

**Non-Goals:** voz em outro quiz; leitura das respostas pelo Mestre; prazo de guarda da
transcrição (pendência no documento 09).

## Decisions

1. **Fim da fala por identidade.** `falar()` recebe `aoTerminar` opcional, ligado ao `onend` do
   `SpeechSynthesisUtterance`; a camada guarda o enunciado corrente e só chama `aoTerminar` se o
   que terminou é ele e não houve `onerror` (cancelamento no Chrome chega como erro
   `interrupted`/`canceled`). `narrar(fala, { aoTerminar })` repassa. _Descartado:_ estimar a
   duração pelo tamanho do texto — abriria o microfone com a voz ainda falando.
2. **Janela com prazo em `comum/fala/`.** Função nova `escutarPorJanela({ duracaoMs, aoParcial,
   aoEncerrar })`: `continuous` e `interimResults` **ligados**, `stop()` ao fim do prazo, e
   `aoEncerrar(transcricao)` uma vez só, com o texto acumulado (vazio no silêncio ou erro
   `no-speech`). Devolve o encerrador, seguro de chamar duas vezes;
   `encerrar(true)` fecha **sem** entregar (o toque vence a voz). Fim do navegador antes do
   prazo não antecipa a entrega. `iniciarTranscricao` não
   muda. A duração é constante `JANELA_DA_SONDAGEM_MS = 5000`, da decisão do fundador.
3. **Permissão no toque que liga.** Ao ligar, `alternarNarracao` chama
   `navigator.mediaDevices.getUserMedia({ audio: true })` e para todas as faixas na hora — só
   pede a permissão, nada é captado. Negada ou sem a API, guarda `microfonePermitido = false` no
   contexto, sem aviso; a sondagem lê esse estado e segue por toque.
4. **Ligação à alternativa: função pura `ligarFalaAAlternativa(transcricao, alternativas)`** em
   `comum/trilha/`, que devolve o número da alternativa ou `null`. Normaliza (minúsculas, NFD sem
   acento, sem pontuação); reconhece primeiro **letra** (`b`, `letra b`), **número** (`2`, `dois`)
   e **ordinal** (`segunda`); senão, compara por coeficiente de Dice sobre bigramas e aceita a
   melhor se `≥ 0,6` e ao menos `0,15` acima da segunda. Os dois limiares são constantes técnicas
   de aproximação, testadas com casos, não regra de produto. _Descartado:_ mandar ao modelo de IA
   — custo e rede numa resposta que não define nível.
5. **Estado da resposta.** `escolhas` passa a `Record<string, number | { falada: string }>`.
   `Sondagem` passa `respostaPorVoz` ao `DesafioDeDesbloqueio`; só com ele, `narracao.ligada`,
   `existeTranscricaoDeFala()` e `microfonePermitido`, o efeito da fala da pergunta passa
   `aoTerminar` que abre a janela. Toque numa alternativa durante a janela chama o encerrador e
   vale a escolha. Ao fim: marca, cancela a janela e avança; na última, chama `submeter()`.
   Retornar à pergunta anterior refala e reabre a janela, pela regra de identidade que já existe.
6. **Componente `JanelaDeEscuta`** em `comum/trilha/`: `<progress max={5000} value={ms decorridos}>`
   com `aria-label` ("Tempo para responder") — mede **o tempo da janela**, recomeça vazio a cada
   pergunta e não tem relação com a posição no quiz —, avançando por relógio de 100 ms, e a transcrição parcial num parágrafo
   `aria-live="polite"` — texto da tela, não frase só para voz (spec da narração).
7. **Contrato do núcleo.** `RespostaDoDesbloqueioEntrada`: `alternativa_escolhida: int | None =
   None` e `resposta_falada: str | None = Field(default=None, max_length=500)`. A regra exige
   exatamente uma das duas e só aceita `resposta_falada` se `missao.e_sondagem`; senão 422. O
   limite de 500 é guarda de entrada (5 s de fala ficam bem abaixo), não regra de produto.
8. **Modelo e migração.** `RespostaDaSubmissao.alternativa_escolhida` vira nulável, coluna nova
   `resposta_falada: Text` nulável, e `CHECK ((alternativa_escolhida IS NULL) <>
   (resposta_falada IS NULL))`. `acertou = False` quando sem alternativa. Migração Alembic nova,
   reversível (o `downgrade` apaga as respostas faladas antes de voltar o `NOT NULL`).
9. **Custo.** A transcrição roda no navegador, sob a conta do navegador e não da plataforma
   (documento 09 §1, "Transcrição da fala"): nenhum lançamento no livro-razão.

## Risks / Trade-offs

- **Áudio da criança vai ao Google no Chrome** → aceito pelo fundador em 2026-11-07; registrado no
  documento 03 §1.12 e no documento 09. Nada fica na plataforma além do texto.
- **Ligação errada marca alternativa que a criança não quis** → a sondagem não define nível
  (`RN-05-34`); o histórico guarda o que foi marcado.
- **`onend` do Chrome às vezes não dispara** em falas longas → sem aviso, a janela não abre e a
  sondagem segue por toque; nada trava.
- **Safari exige permissão própria do reconhecimento** → o primeiro `start()` pode pedir de novo;
  negado, cai no caminho por toque.
