# Design

## Context

Ver `proposal.md` — Why. A App 01 já tem tudo de que esta fatia precisa: a
`TelaDeEntradaDoGuerreiro` abre a sessão pelos dois meios (nick e imagem, ou nick e PIN) e
registra a presença no mesmo ato, e a `TelaInicial` guarda o caminho escolhido em estado do
aparelho, sem roteador. O que muda é **quem registra presença** e **quem exige presença** — não
como se entra. No núcleo, a presença já é única por (aula, Guerreiro(a)) entre as não anuladas,
e a formação da equipe da aula já passa por `criar_equipe` e `entrar_na_equipe`.

## Goals / Non-Goals

**Goals:**

- Um único lugar no aparelho decide se a entrada registra presença: o caminho que a chamou.
- A falta de presença é dita como falta de presença, no aparelho e no núcleo — nunca como
  recusa do rosto nem como falha de rede (`RN-04-36`).
- A guarda do núcleo nasce na **regra** da equipe, não na rota, para valer em qualquer porta.

**Non-Goals:**

- Guarda de presença no núcleo para a equipe da **trilha**, para a resposta de quiz e para a
  troca — ver Decisões 4 e 5.
- Qualquer mudança no reconhecimento facial, no PIN, na fila local ou nas telas de trilha.

## Decisions

1. **Uma tela de entrada, com o caminho declarado.** A `TelaDeEntradaDoGuerreiro` recebe o
   caminho (`presenca` ou `equipes`) e só registra presença no primeiro. _Alternativa
   descartada:_ duas telas — duplicaria captura, visor, PIN, fila local e o tratamento de erro
   do `RN-04-36`, que é justamente onde esta aplicação já errou cinco vezes.

2. **A presença do Guerreiro(a) se lê por rota própria**, `GET /v1/aulas/{id}/presencas/eu`,
   sob a sessão dele e a operação `seus_dados` que a matriz já lhe concede. Ausência responde
   **200**, com o campo que diz não haver presença — não 404, para a tela distinguir "não tem
   presença" de "não foi possível perguntar" (`RN-04-36`). _Alternativa descartada:_ devolver a
   presença no corpo da abertura da sessão — misturaria sessão com aula e alcançaria a App 05,
   que abre sessão sem aula (`RN-01-57`).

3. **A guarda da equipe fica na regra**, em `criar_equipe` e `entrar_na_equipe`, e só quando o
   vínculo da equipe é uma **aula**. A recusa é `ErroDeValidacao` (422) com código próprio, no
   mesmo padrão de `NickDeGuerreiroEmUsoNoEncontro`, para que a tela diga a causa certa.
   _Alternativa descartada:_ conferir na rota — deixaria a regra passável por qualquer outra
   porta que venha a chamá-la.

4. **A equipe da trilha não ganha guarda no núcleo.** A rota dela não carrega a aula do
   encontro, e inventar uma (presença em qualquer aula vigente) seria regra nova, que nenhum
   requisito autoriza. No App 01 ela só é alcançada dentro do caminho das equipes, já atrás da
   guarda do aparelho. _Alternativa descartada:_ exigir `aula_id` no corpo — mudaria o contrato
   de duas rotas do PRD-04 §9 sem requisito que o peça.

5. **Quiz e troca são guardados só no aparelho.** A decisão do fundador de 2026-09-23 estende a
   exigência de presença aos dois caminhos da tela; no núcleo, a resposta de quiz já depende de
   integrar equipe — que agora exige presença — e a troca é operação do **Mestre**, não do
   Guerreiro(a). Pôr guarda de presença nessas rotas seria criar regra sobre a operação de
   outra persona.

6. **Recusado o caminho, a sessão se encerra e a tela oferece o caminho Presença.** O nick não
   é preservado na travessia: a captura seria refeita de qualquer modo, e guardar o nick de um
   atendimento recusado contraria a tela que "volta ao início sem dado do atendimento
   anterior" (`RF-04-28`).

7. **Os rótulos da tela inicial passam a Onboarding, Presença e Equipes**, e o botão de trilhas
   deixa de existir. A medição do limiar, o quiz e a troca continuam onde estão, e o estado
   `Caminho` da `TelaInicial` troca `"trilhas"` por `"presenca"` e `"equipes"`.

## Risks / Trade-offs

- [Quem chega e vai direto às equipes é barrado e tem de repetir a entrada] → A tela diz em
  linguagem simples o que falta e leva ao caminho Presença em um toque; é o preço de separar os
  dois momentos, que é o que a decisão pede.
- [Uma consulta a mais entre a abertura da sessão e a tela das equipes] → É uma leitura por
  atendimento, na mesma rede que já abriu a sessão; falha nela aparece como falha de camada, e
  não como falta de presença.
- [A guarda do núcleo pode recusar quem teve a presença anulada pela gestão no meio do
  encontro] → É o comportamento correto: a anulação existe para desfazer registro errado
  (`RF-02-36`), e quem já está na equipe não é expulso — sair e renomear seguem livres.
- [A equipe da trilha fica sem guarda no núcleo] → Registrado na spec de `equipe` como limite
  deliberado, com o aparelho como única barreira; se o fundador quiser fechá-lo, é fatia própria
  com mudança de contrato.
