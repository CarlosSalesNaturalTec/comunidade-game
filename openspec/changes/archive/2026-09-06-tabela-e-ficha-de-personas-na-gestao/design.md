## Context

`openspec/specs/aplicacao-de-gestao/spec.md` já traz a área Personas, o cadastro de adulto com
artefato obrigatório e a gravação do nick de quem está sem ele. Esta fatia não acrescenta ato
nenhum: ela **apresenta** o que o núcleo já serve e a tela descartava. `Tabela` e `Dialogo` vêm
prontos da fatia transversal `camada-visual-densa-e-navegacao-comum`.

## Goals / Non-Goals

**Goals:** as três listas de persona em tabela; a ficha de leitura do adulto com os artefatos;
o caminho de gravar o nick alcançável; as classes órfãs eliminadas.

**Non-Goals:** editar cadastro de adulto, trocar nick já gravado, digitar nick no cadastro,
qualquer rota nova no núcleo.

## Decisions

1. **A ficha é de leitura, e é diálogo, não área nova.** O Admin abre, confere a prova e
   fecha, sem perder a lista nem o filtro em que estava. _Descartado:_ área própria com
   endereço, que a App 03 não tem — a navegação dela é por estado, não por rota.

2. **O nick vazio é coluna, não recado no meio da linha.** "Sem nick — não aparece em
   superfície pública" vira o conteúdo da célula de nick, e o ato de gravá-lo é oferecido pela
   ficha. _Descartado:_ botão na própria linha da tabela — cada linha ganharia altura de
   formulário e a densidade da §6 se perderia.

3. **O artefato aparece com rótulo e endereço, e o endereço é link.** É o que `RN-02-01`
   define: prova verificável por quem a lê. _Descartado:_ mostrar só a contagem de artefatos —
   não permitiria conferir nada, que é justamente a queixa.

4. **`ListaDeGuerreiros` entra junto.** Usa as mesmas classes órfãs e a mesma marcação de
   lista; deixá-la de fora manteria vivo o CSS que esta fatia apaga. _Descartado:_ tratar só
   os adultos — sobraria metade do defeito.
