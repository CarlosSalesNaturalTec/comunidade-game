# Design

## Context

A sondagem é hoje o `DesafioDeDesbloqueio` de `comum/trilha` com `respostaPorVoz`, embrulhado
pelo `Sondagem`: pagina as perguntas pelo `SequenciaPaginada`, com voltar e "Enviar
respostas", e chama `aoDesbloquear` assim que o núcleo aprova — o `GuiaDaTrilha` recarrega e a
sondagem sai da tela. O gabarito nunca sai do núcleo: `_saida_das_perguntas` o omite, e só
`_saida_das_perguntas_ao_autor` o traz. Na submissão, `submeter_desafio_de_desbloqueio` devolve
cedo quando já existe `DesbloqueioDaMissao` do par, sem gravar tentativa. O `GuiaDaTrilha` só
busca a próxima missão do percurso, então a sondagem respondida não tem como voltar.

## Goals / Non-Goals

**Goals:** o fluxo de `RF-05-99`, `RF-05-100` e `RF-05-101` nas Apps 01 e 05 por uma
implementação só, e a tentativa nova gravada pelo núcleo (`RN-05-56`).

**Non-Goals:** leitura do resultado vigente por alguém — nenhuma tela ou rota o consome hoje, e
o documento 10 não está fatiado; retorno por pergunta no desafio de desbloqueio ou no Quiz ao
Vivo.

## Decisions

1. **Núcleo: a sondagem já respondida grava e devolve o placar.** Em
   `submeter_desafio_de_desbloqueio`, quando o desbloqueio existe e a missão é sondagem em
   quiz, a regra confere as respostas, chama `_gravar_submissao` e devolve `aprovado=True` com
   o desbloqueio existente, `acertos` e `total`. A aferição do quiz sai para uma função
   auxiliar usada pelos dois caminhos. O quiz comum já desbloqueado segue devolvendo cedo.
   _Descartado:_ rota própria de "refazer sondagem" — o contrato da submissão já serve, e a
   tela não precisa saber se é a primeira vez.
2. **"Vale a última" é a ordem do registro, não coluna nova.** A `SubmissaoDoDesbloqueio` já
   guarda o instante; a mais recente do par é o resultado vigente. Sem migração. _Descartado:_
   marcar a vigente com campo — duplicaria o que o instante já diz.
3. **Gabarito no percurso, só da sondagem.** `PerguntaDoDesbloqueioSaida` ganha
   `alternativa_correta: int | None = None`; `_saida_do_desafio_de_desbloqueio` a preenche
   quando `missao.e_sondagem`. Mesma numeração de 1 a 4 da escolha. A leitura pública e a
   imagem da pergunta não mudam. _Descartado:_ rota de conferência por pergunta — o fundador
   escolheu o gabarito na leitura.
4. **A tela confere sozinha; o total vem do núcleo.** O retorno de cada pergunta compara a
   escolha com `alternativa_correta`; resposta falada sem alternativa é erro (`RN-05-55`). O
   total da tela final é o `acertos`/`total` da resposta da submissão, e erros é
   `total - acertos` — o núcleo segue sendo a fonte do placar gravado.
5. **O fluxo fica no `DesafioDeDesbloqueio`, sob a flag da sondagem.** `respostaPorVoz` vira
   `ehSondagem` (só a sondagem tem voz, `RN-05-54`, e agora também retorno), porque a janela de
   voz já mora ali e o fim dela é justamente o ponto em que o retorno entra. Na sondagem:
   - a pergunta da vez é renderizada **sem o `SequenciaPaginada`** — sem avançar manual, sem
     voltar e sem "Enviar respostas";
   - responder (toque ou fim da janela) grava a escolha, liga `retorno = { perguntaId,
     acertou }` e agenda, por `RETORNO_DA_SONDAGEM_MS = 2000`, avançar ou, na última,
     submeter; as alternativas ficam `disabled` enquanto há retorno;
   - o temporizador é limpo ao desmontar, para não submeter de tela que saiu;
   - submetida, a tela final substitui a pergunta: "Você acertou N e errou M.", **Refazer**
     (zera escolhas, retorno e índice) e **Concluir** (chama `aoDesbloquear`). Falha de envio
     mostra o aviso de erro e "Tentar de novo", que reenvia as mesmas escolhas.
   _Descartado:_ componente novo de sondagem — duplicaria a janela de voz e a narração por
   pergunta, que levaram duas fatias para acertar.
6. **Símbolo: dois glifos novos no `Icone`.** `acerto` (✓) e `erro` (✗), coloridos por
   `--cor-sucesso` e `--cor-erro`, com texto visualmente oculto em região `aria-live` ("Você
   acertou!" / "Não foi essa."). Forma distinta mais texto atende "nenhum significado só por
   cor" (documento 15). Com a narração ligada, o mesmo texto é falado pelo `narrar` ao abrir o
   retorno (decisão do fundador de 2026-11-10); desligada, `narrar` já cala sozinho. A fala é
   curta e cabe nos 2 s; a fala da pergunta seguinte a interrompe se ainda soar. O símbolo é grande e centralizado sobre a pergunta, em
   `comum/trilha/estilos.css`.
7. **Refazer pelo rodapé no `GuiaDaTrilha`.** O guia localiza a missão de sondagem em
   `trilhaPublica.missoes` (`e_sondagem`), busca o estado dela no percurso e, se está
   desbloqueada e não é a próxima, oferece **Refazer a sondagem** no grupo 4, ao lado de
   "Escolher outro poder". Com a submissão desligada não oferece. Ao tocar, o grupo 1 passa a
   apresentar o `Sondagem` daquela missão em lugar da `Missao`; Concluir sai desse modo e
   chama `carregar()`. Vale também no caminho da trilha completa, que já usa o mesmo
   esqueleto. _Descartado:_ abrir a sondagem como missão navegável — o percurso só aponta a
   próxima, e torná-lo navegável é recorte que a fatia 21 do PRD-04 tirou do escopo.
8. **A recarga sai do envio e vai para o Concluir.** Hoje `aoDesbloquear` roda no envio; na
   sondagem passa a rodar só no Concluir, senão a trilha recarregaria e a tela final sumiria.
   A tela da recompensa de marco (`RF-05-45`) segue entrando depois da recarga, agora depois
   do Concluir.

## Risks / Trade-offs

- [A criança vê o gabarito pelo navegador] → aceito pelo fundador; a sondagem não tranca nada.
- [Toque durante o retorno ou janela de voz aberta no fim da pergunta] → alternativas
  travadas e a janela fecha ao responder, como já fecha ao tocar (`RN-05-54`).
- [Temporizador que sobrevive à troca de trilha] → limpeza no efeito de desmontagem, coberta
  por teste com relógio falso.
- [Abandono antes da tela final perde a realização] → é o comportamento desejado: só a
  submissão grava.
