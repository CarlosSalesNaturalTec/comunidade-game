# Design

## Context

O padrão está consolidado em `openspec/specs/aplicacao-da-aula-presencial`, nos três requisitos
de visor ao vivo, e o `comum/biometria` já expõe tudo o que a App 05 precisa chamar:
`prepararCaptura()`, `acoplarEspelho()` e o callback `aoMudarEstado` de `provarVivacidade()`.
Nada precisa ser construído no módulo de biometria nem no núcleo. A fatia **chama o que existe**
e sobe o componente de tela à camada comum.

Uma restrição ordena o resto: `acoplarEspelho()` sai cedo quando `elementoDeVideo` é nulo, e esse
elemento só nasce dentro de `abrirCamera()`. Logo, mostrar o espelho **exige** `prepararCaptura()`
antes do laço — e é por isso que o desfecho próprio do preparo entra nesta fatia, e não em outra.

## Goals / Non-Goals

**Goals:**

- A criança vê a própria imagem antes de a conferência julgar, e corrige posição e luz sozinha.
- Falha de preparo deixa de sair vestida da frase do rosto (`RN-05-48`).
- Uma única implementação de visor na plataforma, consumida pelas Apps 01 e 05.

**Non-Goals:**

- Medir luz ou distância para produzir orientação (fora do escopo na proposal).
- Mudar o momento em que a câmera acende, qualquer rota do núcleo ou o caminho da confirmação
  assistida.
- Criar a área detalhada de direitos da App 05.

## Decisions

**1. O `Visor` sobe a `comum/react`, com as frases por _prop_.** Pelo precedente de
`ListaDeCaminhos` na fatia 11 do PRD-05. As frases saem do componente porque o público é outro em
cada tela — a `FRASE_DO_LACO` de hoje fala com quem opera a bancada ("Confirmando que há uma
pessoa…") e o PRD-05 §10 exige linguagem de criança de 6 anos. _Descartado:_ duplicar o
componente na App 05, que deixaria duas redações do mesmo visor divergirem com o tempo.

**2. As quatro regras `.cg-visor*` vão para `comum/react/estilos.css`.** O `comum/biometria` já
fixa `video.className = "cg-visor"`, mas a regra mora no `index.css` da App 01: hoje o módulo
comum depende do CSS de **uma** aplicação. Sem a subida, o espelho na App 05 sairia sem
`max-height: 40vh`, sem `object-fit` e sem `transform: scaleX(-1)`. _Descartado:_ copiar as
regras para o `index.css` da App 05, que mantém o acoplamento e o duplica.

**3. A ordem na entrada da App 05 passa a ser a das duas telas da App 01.**

```text
[Entrar] ─▶ prepararCaptura() ─▶ acoplarEspelho(lugar) ─▶ provarVivacidade(definirEstadoDoLaco)
                  │                      │                            │
            falha PRÓPRIA          espelho ao vivo            três frases de criança
         "a câmera não pôde          + orientação                     │
          ser preparada"             + aviso                   ─▶ gerarDescritor()
                  │                                                  │
                  └──▶ caminho do adulto (RN-05-02) ◀────────── recusa da conferência
```

O espelho **não** aparece antes do toque em Entrar: o `RN-05-49` proíbe a câmera acender quando
ninguém pediu nada, e a pré-carga dos modelos da fatia 9 continua sendo só modelo.
_Descartado:_ um passo "deixe eu me ver" antes do Entrar — mais gentil, mas inventa tela e
antecipa a câmera.

**4. Redação aprovada pelo fundador em 2026-11-05, sem troca.** Não é regra de produto; é a
redação que o `RF-05-95` e o `RF-05-96` pedem em linguagem de criança. Foi rascunhada aqui,
implementada como está e aprovada:

| Situação | Frase proposta |
| --- | --- |
| Ainda sem rosto | "Ainda não achei você. Olhe para a câmera!" |
| Rosto encontrado | "Achei você! Fique assim um pouquinho…" |
| Vivacidade confirmada | "Pronto, é você!" |
| Orientação (fixa) | "Fique de frente para uma janela ou uma luz. Se estiver muito escuro, não dá para te achar." |
| Aviso (fixo) | "A câmera aparece aqui só para você se ver. Sua foto não fica guardada e não sai deste aparelho." |
| Falha de preparo | "Não consegui ligar a câmera deste aparelho. Tente de novo, ou peça ajuda a um adulto." |

A frase da recusa da conferência e as de falha de camada **não mudam**: já existem e já cumprem
o `RN-05-48`.

**5. A falha de preparo não é `Aviso tipo="erro"` vermelho que interrompe.** Segue o que o
fundador fixou em 2026-10-02 para a falha da pré-carga: não interromper vem antes do vermelho, a
frase inteira carrega a informação e o documento 15 §5 fica satisfeito sem rótulo de cor. Mas,
diferente da pré-carga, o preparo **impede** a entrada por imagem, então o caminho do adulto é
oferecido junto.

**6. A precisão no PRD-05 §11.** O marcador "nenhuma imagem real é exibida em qualquer tela"
ganha o recorte que o PRD-04 já tem no `RN-04-34`: ele trata da **representação da pessoa**, que
é sempre por avatar. O próprio critério de aceite do §12 diz "de **outra criança**", e o
invariante 12 distingue visor de quadro capturado. É conflito resolvido pelo nível superior da
hierarquia, não decisão nova — e por isso não há linha a mover no documento 09.

## Risks / Trade-offs

- **A criança só se vê depois de apertar Entrar**, e tem os 15 s do laço para se ajustar. É o
  comportamento das duas telas da App 01 e o que o `RN-05-49` permite; se na primeira turma isso
  se mostrar curto, o ajuste é do tempo do laço, não do momento do espelho.
- **Luz ruim continua reprovando** — a fatia dá à criança como **perceber** o problema, não
  corrige o problema. O estado derivado de luminância resolveria mais e foi descartado de
  propósito: criaria limiar que ninguém mediu.
- **`RF-05-57` fica atendido em parte**: o aviso entra, o acesso à área detalhada não, porque a
  App 05 não tem essa tela. Resíduo declarado na proposal.
- **A App 01 é tocada sem precisar de mudança de comportamento**, e um erro ali quebraria duas
  telas de câmera em produção. Os testes de `captura.test.tsx` e `entrada.test.tsx` da App 01
  são a rede: eles já cobrem o visor e precisam continuar verdes sem edição de asserção.
