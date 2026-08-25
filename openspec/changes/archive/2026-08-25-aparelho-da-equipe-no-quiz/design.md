## Context

Ver `proposal.md` — Why. O módulo `quiz` do núcleo já tem partida, pergunta no ar, liberação de
resultado, resposta idempotente e encerramento (`openspec/specs/quiz-ao-vivo/spec.md`); a App 03
já conduz. A fatia acrescenta a leitura que faltava ao aparelho e a tela que a consome, e não
cria tabela.

Duas restrições moldam tudo o que segue:

- **Documento 05 §5** — a plataforma não controla aparelhos no Ciclo 01, e a resposta é da
  equipe, nunca do aparelho de onde veio. Nenhuma entidade de aparelho, nenhum pareamento.
- **`RN-01-22`** — nenhuma rota é oráculo de nick de Guerreiro(a). A equipe do aparelho tem de
  sair da sessão de quem está logado, nunca de consulta por nick.

## Goals / Non-Goals

**Goals:**

- Dar ao aparelho um caminho fechado: descobrir a partida, ler a pergunta, responder uma vez,
  ver o resultado.
- Reconciliar spec e código na leitura da partida, sem alargar o que `estado_da_partida` faz.

**Non-Goals:**

- Não altera `registrar_resposta`, `abrir_partida`, `por_pergunta_no_ar`, `liberar_resultado`
  nem `encerrar_partida` — a fatia é de leitura, mais uma tela.
- Não toca a matriz de permissões: o Guerreiro(a) já tem `resposta_de_quiz_da_equipe` em leitura
  e escrita (`permissoes.py`).
- Não mexe na App 03.

## Decisions

**1. A equipe do aparelho é derivada no núcleo, não escolhida na tela.**
`GET /v1/aulas/{id}/partidas` cruza as equipes disputantes da partida com as equipes que o
Guerreiro(a) em sessão integra e devolve a única que resta. Isso implementa `RF-04-42` onde a
garantia já existe — `abrir_partida` recusa equipe com integrante já disputante por outra — em
vez de repetir a regra na tela.
_Alternativas:_ o aparelho casar por nick contra `GET /aulas/{id}/equipes` (que só devolve avatar
e nick) — descartada por aproximar o oráculo que `RN-01-22` veda; o aparelho escolher a equipe —
descartada porque abre a porta a jogar pela equipe errada, que `RF-04-42` fecha.

**2. O resultado vai na leitura que o aparelho já faz, não numa rota nova.**
`pergunta_para_equipe` passa a devolver, quando `liberada_em` não é nulo, a alternativa correta,
se a equipe daquele Guerreiro(a) acertou e qual chegou primeiro. O aparelho sonda um endereço
só e o resultado chega na sondagem seguinte à liberação, sem sincronizar duas leituras.
_Alternativa:_ abrir `estado_da_partida` ao Guerreiro(a) — descartada porque ela carrega a
contagem de respostas por equipe e o painel de quem conduz, que não são da criança.

**3. O aparelho lê a pergunta; quem conduz lê o estado. Duas leituras, dois públicos.**
É o que o código já faz e o que a spec prometia errado. A correção é da spec, não do código:
`estado_da_partida` continua restrita a `conducao_do_quiz_ao_vivo_das_suas_aulas`.

**4. O vínculo aparelho×equipe vive em `sessionStorage`, aninhado na sessão do Guerreiro(a).**
Mesmo padrão do momento de troca e da aula escolhida (`AparelhoDaAula.tsx`): estado do próprio
aparelho, que morre com o atendimento. Chave `app-01:quiz:partida`, contendo partida e equipe,
apagada ao voltar ao início junto das demais.
_Alternativa:_ `Aparelho` como entidade do núcleo com pareamento — descartada por contrariar o
documento 05 §5 e por impedir a jornada 5.9 item 6, em que um aparelho serve mais de uma equipe.

**5. O caminho do quiz não fica atrás de um momento aberto pelo Mestre.**
A troca tem `RF-04-49`, que manda escondê-la fora do momento; o quiz não tem requisito
equivalente, e inventar um seria criar regra no artefato. O caminho aparece sempre na sessão de
trabalho, e é a tela do quiz que diz não haver partida — o que também evita sondar o núcleo
antes de alguém escolher o caminho.

**6. Resposta de quiz nunca entra em fila offline.**
`RF-04-58` já a declara indisponível sem rede, e o desempate é por ordem de chegada no servidor
(documento 05 §5): resposta enfileirada chegaria fora de ordem e falsearia o bônus da primeira.
A fila local do `RF-04-23` a `RF-04-25`, quando vier, não alcança esta tela.

**7. Sondagem a cada 2 segundos**, como a tela de condução da App 03 — decisão do fundador de
2026-08-25, documento 03 §1. Sondagem que falha avisa e mantém a tela, sem derrubar a partida.

## Risks / Trade-offs

- **A criança troca de equipe entre encontros e o aparelho guarda a antiga** → a equipe nunca é
  lida do `sessionStorage` como verdade: cada abertura do caminho do quiz relê
  `GET /v1/aulas/{id}/partidas`, e o armazenado é só o que a tela corrente usa.
- **Dois aparelhos da mesma equipe respondem juntos** → o núcleo já é idempotente por (partida,
  pergunta, equipe); o segundo recebe 422 e a tela mostra "a equipe já respondeu", não erro.
- **Sondagem de 2 s com muitos aparelhos na sala** → a leitura da pergunta é uma consulta por
  partida, sem varredura; se pesar, o intervalo é parâmetro de configuração, não regra.
- **A tela do quiz sem o caminho das trilhas** → a criança entra, joga e sai sem ver a missão. É
  consequência aceita do recorte: o caminho das trilhas é fatia própria (`RF-04-29`, `RF-04-35`).

## Migration Plan

Sem migração: nenhuma tabela nasce ou muda. A rota nova é aditiva e a saída ampliada de
`GET /v1/partidas-de-quiz/{id}/pergunta` acrescenta campos anuláveis — nenhum consumidor atual
quebra, porque hoje não há consumidor.
