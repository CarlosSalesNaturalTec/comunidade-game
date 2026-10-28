# Proposal

## Why

**Origem: requisito não funcional da esteira de implantação do núcleo.** Como os demais da
classe, não tem `RF-XX-nn` nem `RN-XX-nn`. A change não cria regra: aplica ao
`backend-deploy.yml` a decisão de 2026-08-21, registrada no `design.md` da change
`2026-08-21-guardas-da-conferencia-e-da-implantacao` — a `firebase-tools` vai em versão
exata, não em faixa. Autorizada pelo fundador em 2026-10-28.

O `Backend Deploy` do merge do PR #272 falhou, e **nada no PR o causou**: o diff não toca
`.github/workflows/` nem o `firebase.json`. Falhou o 13º e último passo, "Publicar o alvo
`api` no Firebase Hosting", depois de os doze anteriores passarem — migração aplicada e
serviço no Cloud Run servindo 100% do tráfego. **Produção está no ar**: o rewrite aponta
para o serviço sem fixar revisão, então o release anterior do Hosting já roteia para a
revisão nova, e o passo que falhou apenas o republicava.

A causa é `firebase-tools@latest` na linha 145. A CLI é baixada a cada publicação; entre
19/10 e 28/10 saiu versão que passou a consultar a Service Usage API antes de publicar e a
**abortar** no `403` dela em vez de tolerá-lo. O `403` é antigo e não é o gatilho: no run
verde de 19/10 o próprio gcloud o registrou duas vezes, como aviso, e seguiu. Que fixar a
versão resolve não é aposta — o `App 09 Deploy` publicou no Hosting no **mesmo commit**,
pela mesma conta e no mesmo projeto, com `15.28.1`, e passou.

O `backend-deploy.yml` divergiu dos outros sete workflows de publicação em quatro pontos, e
todos na mesma direção: é o único com `@latest`, o único sem o comentário que explica por que
não usá-lo, e o único que não lista o próprio caminho nem o `firebase.json` nos `paths` do
gatilho. Ele entrou em 25/09, cinco semanas **depois** da decisão, sem que nada acusasse: a
regra não está em `CLAUDE.md`, em `docs/`, em `openspec/specs/` nem no cronograma — vive num
`design.md` arquivado e em comentários copiados entre arquivos. É o mesmo padrão que a change
de 21/08 descreveu para o curto-circuito do client ID, e que ela corrigiu ali e não na
própria regra.

## What Changes

- **A versão da `firebase-tools` é fixada** no `backend-deploy.yml`, em `15.28.1` — a mesma
  dos outros sete workflows —, com o comentário de justificativa que eles carregam.
- **O gatilho passa a incluir o próprio workflow.** Hoje os `paths` só olham `backend/**`,
  então editar o workflow não o reexecuta e esta correção não se provaria no merge.
- **A regra passa a existir em lugar vivo:** uma linha na seção "As três esteiras" do
  `CLAUDE.md`. Escolhido por ser o artefato que entra no contexto de todo agente que
  trabalha aqui, o que previne na escrita do próximo workflow, não na execução dele.
- **Duas dívidas entram no documento 09** como pendências, por serem ato de console ou
  desenho maior: a conta de deploy não tem permissão de leitura na Service Usage — hoje o
  `403` fica mascarado pelo aviso "Skipped validating" do gcloud —, e o rewrite do alvo
  `api` não se republica quando o `firebase.json` muda, porque o gatilho não olha o arquivo.

Fora do escopo: incluir `firebase.json` e `.firebaserc` nos `paths`, como fazem os sete — ali
é build de frontend, aqui uma mudança em alvo alheio dispararia build de imagem, **migração**
e deploy do núcleo; guarda automática que varra `.github/workflows/` e falhe em
`firebase-tools` sem versão exata, que exigiria passo ou workflow novo, porque nenhuma
esteira cobre `.github/` hoje; subir a versão fixa dos oito workflows, que é ato revisado à
parte; e liberar a permissão no Google Cloud, que é ato de console e por isso é pendência.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

Nenhuma. Não há capability de implantação em `openspec/specs/`, e nenhuma spec trata da
versão da CLI — nem a change de 21/08 criou requisito para ela. Nenhum comportamento do
produto muda, então a change sai com `skip_specs: true`, como as demais de esteira.

## Impact

- `.github/workflows/backend-deploy.yml` — a versão da CLI, o comentário e os `paths`.
- `CLAUDE.md` — a linha da regra em "As três esteiras".
- `docs/09-topicos-em-aberto-e-sugestoes.md` §1 — as duas pendências.
- `openspec/cronograma-de-fatias.md` — linha sem número em "Infraestrutura transversal
  (sem PRD)", como a esteira de deploy das Apps 07 e 08.
- **Sem impacto** em rota, contrato de API, modelo de dados, chave de aplicação, migração,
  `firebase.json` ou código do núcleo. Nenhuma aplicação é tocada.
- O merge em `main` **dispara** o `backend-deploy.yml`, pelos `paths` que a change acrescenta:
  a correção se prova no próprio merge, republicando o rewrite que ficou sem publicar. O
  deploy repete build, migração e Cloud Run sobre código idêntico ao que já está no ar.
  A migração é a `c4e81b2a9d60`, já aplicada, e `alembic upgrade head` não a reaplica.
