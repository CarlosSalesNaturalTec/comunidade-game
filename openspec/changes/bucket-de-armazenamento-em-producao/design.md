# Design — bucket de armazenamento em produção

## Context

Motivação em `proposal.md` — Why. O que o desenho precisa saber:

- `armazenamento/fabrica.py` escolhe pelo ambiente e **não tem fallback**: em produção é sempre
  `ArmazenamentoNoCloudStorage`. O nome vazio derruba o construtor, não a primeira operação.
- O que o bucket guarda **não é foto de criança**: o documento 03 §1 determina que foto e áudio
  da produção são **descartados na leitura**, guardando-se só a transcrição. O bucket recebe
  conteúdo de missão, artefato comprobatório, anexo do termo, criação original e afins.
- `CG_AMBIENTE` e `CG_GEMINI_MODELO` já são o precedente de parâmetro não secreto declarado em
  `--set-env-vars`.
- O adaptador usa `create_resumable_upload_session` do próprio Cloud Storage (`RF-09-19`), que
  exige criar objeto — não basta permissão de leitura.

## Goals / Non-Goals

**Goals:**

- As oito capacidades que dependem de armazenamento voltam a funcionar em produção.
- Configuração de produção ausente se anuncia no arranque, não numa requisição de usuário.
- O README deixa de afirmar um fallback que não existe.

**Non-Goals:**

- Não mudar a porta, o protocolo de envio retomável nem nenhuma rota.
- Não migrar dado: não há dado a migrar — nenhum envio foi gravado.
- Não estender a falha cedo às portas de IA: ali a indisponibilidade é comportamento previsto
  (`RF-09-91`, `RN-04-21`, `RN-05-35`), não defeito de configuração.

## Decisions

**1. O nome do bucket vai para `--set-env-vars`, não para o Secret Manager.** Nome de bucket
não é segredo — está em toda URL de objeto assinado. O critério é o mesmo que o workflow já
aplica a `CG_AMBIENTE` e `CG_GEMINI_MODELO`, e mantém a troca de bucket como uma linha de diff
revisável.

**2. Em produção, bucket não declarado impede o arranque, com mensagem que nomeia a variável.**
Hoje a falta vira `IndexError` numa requisição qualquer — a pior combinação: tarde, ilegível e
sofrida pelo usuário. A validação acontece na construção da configuração ou da porta, e a
mensagem diz qual variável falta e em que ambiente. Este é o segundo defeito que uma variável
de produção esquecida escondeu; a guarda vale para o próximo. _Descartado:_ cair para disco
quando o bucket falta — é o que o README afirma hoje, e é pior: aceita o envio, responde
sucesso e perde o arquivo no deploy seguinte. Falhar é mais honesto. _Descartado:_ validar só
no `healthcheck` — o serviço subiria e a falha continuaria chegando ao usuário primeiro.

**3. A permissão da `nucleo-runtime` é concedida no bucket, não no projeto.** Ela precisa
criar, ler e remover objeto — inclusive sessão de envio retomável —, e nada disso exige alcance
de projeto. Vincular o papel ao bucket mantém a conta no mesmo desenho enxuto que o README item
5 defende: ela nasceu justamente para não ter `roles/editor`.

## Risks / Trade-offs

- **A falha cedo pode derrubar o serviço num deploy futuro se alguém remover a variável.** → É
  o comportamento pretendido, e o Cloud Run mantém a revisão anterior servindo quando a nova
  não sobe. Melhor não subir do que subir quebrado.
- **O Job de migração usa a mesma configuração e também passaria a exigir a variável.** → O
  workflow declara as duas etapas com o mesmo conjunto; a variável entra nas duas, como
  `CG_GEMINI_MODELO`.
- **Bucket novo, sem nada dentro, não recupera o que já se perdeu.** → Nada se perdeu: os
  envios nunca começaram.

## Open Questions

Duas decisões do fundador, ambas travando as tarefas:

- **Nome do bucket.** A convenção dos sites do Firebase é `comunidade-game-*`.
- **Versionamento e ciclo de vida.** O bucket guarda artefato comprobatório e conteúdo
  produzido em comunidade; se há prazo de guarda ou exigência de versão anterior, é regra de
  negócio e vem do documento-fonte, não daqui.
