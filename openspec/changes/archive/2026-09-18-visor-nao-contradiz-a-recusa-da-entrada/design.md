## Context

O padrão já está consolidado em `openspec/specs/aplicacao-da-aula-presencial/spec.md`: o visor
aparece **enquanto a captura acontece** (`RF-04-64`, `RN-04-34`). Duas das três telas de câmera
do App 01 já o aplicam condicionando o visor ao momento — `TelaDeCaptura` e
`TelaDeMedicaoDoLimiar` passam o estado do laço só quando estão capturando. Esta change leva a
terceira ao mesmo padrão; não há desenho novo a decidir.

## Decisions

1. **A tela de entrada adota a mesma condição das outras duas**, em vez de limpar o estado do
   laço em cada ponto de saída. Limpar em cada saída depende de não esquecer nenhum caminho —
   e são cinco: falha de preparo, vivacidade reprovada, recusa do núcleo, erro de rede e
   presença já registrada. Condicionar a apresentação é uma verificação só, e é o que as
   telas irmãs já fazem.

   Descartada: limpar o estado no `catch` e antes de cada `return`. Corrige o sintoma
   observado e deixa os outros caminhos abertos.

   Descartada: reescrever a tela com máquina de estado, como as irmãs. É a forma certa, e é
   escopo maior que o defeito — fica para quando a tela mudar por requisito.

2. **A frase da recusa não entra nesta change.** Ela é a frase única do `RN-01-22`, e mexer
   nela para "explicar melhor" abriria o oráculo que o requisito veda.
