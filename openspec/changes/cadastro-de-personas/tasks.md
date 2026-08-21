## 1. Modelo e migração

- [x] 1.1 Criar a tabela satélite de **artefato comprobatório** — persona, endereço e rótulo —
      e os satélites dos dados próprios de papel que ainda faltem, em
      `backend/src/nucleo/personas/modelo.py`, com a migração Alembic; verificar que
      `alembic upgrade head` sobe limpo (`RF-02-02`, `RF-02-03`, `RF-02-04`)

      `nome`, `email` e `whatsapp` entraram como colunas nulas da própria `Persona` — comuns
      aos cinco papéis por PRD-01 §8, não atributo de um papel só — e não como satélite. Só
      `ArtefatoComprobatorio` nasceu como tabela nova.

## 2. Regra de cadastro no núcleo

- [x] 2.1 Em `backend/src/nucleo/personas/regra.py`, exigir **ao menos um artefato
      comprobatório** de Mestre e de Apoiador, recusando com 422 sem ele, e recusar anexo de
      arquivo como artefato (`RF-02-04`, `RN-02-01`)
- [x] 2.2 No mesmo módulo, expor a edição de Guerreiro(a) e a gravação de nick de adulto pelo
      Admin, ambas sujeitas à unicidade global e recusando 422 no campo `nick` sem revelar o
      dono, e a segunda recusando persona de Guerreiro(a) (`RF-02-01`, `RN-01-30`, `RN-14-10`)

## 3. Rotas do núcleo

- [x] 3.1 Criar em `backend/src/nucleo/personas/rotas.py` as quatro rotas de criação de
      persona — `POST /v1/guerreiros`, `/v1/mestres`, `/v1/apoiadores` e `/v1/admins` —, todas
      de Admin, com 403 para outro papel (`RF-02-01`, `RF-02-02`, `RF-02-03`, `RF-02-05`,
      `RN-02-02`)

      `POST /v1/guerreiros` exige `aula_id`: `RN-08-02` (já decidida) obriga toda persona de
      Guerreiro(a) a ter a comunidade atribuída pela aula agendada em que se cadastra, e esta
      rota não é exceção. Também nasceram `GET /v1/guerreiros`, `/v1/mestres` e
      `/v1/apoiadores` — paginados, Admin — porque os cenários aprovados de
      `aplicacao-de-gestao` ("a aplicação o apresenta entre os cadastrados", "sinaliza quem
      está sem nick") exigem uma leitura que a change não tinha listado; nenhum é decisão de
      produto nova, só o caminho técnico do que já estava aprovado.
- [x] 3.2 Criar a rota de edição do Guerreiro(a) e a `PUT /v1/personas/{id}/nick` de Admin,
      conforme o desenho (`RF-02-01`); verificar que a edição não troca papel nem apaga persona

      As duas nasceram como `PATCH`, não `PUT`: o CORS do núcleo e o cliente HTTP da App 03 só
      cobrem `GET`, `POST`, `PATCH` e `DELETE` — ver design.md, atualizado no mesmo commit.

## 4. Telas da App 03

- [x] 4.1 Criar o módulo `apps/app-03-gestao/src/personas/` com a tela de cadastro e edição de
      Guerreiro(a) — nome, nascimento, nick e avatar —, sem exibir imagem real e com o aviso de
      coleta (`RF-02-01`, `RN-02-22`, PRD-02 §11)

      O cadastro pede também a aula (comunidade + aula agendada), refletindo o `aula_id` que
      `POST /v1/guerreiros` exige (tarefa 3.1) — a edição não pede, porque a comunidade já está
      fixada no vínculo.
- [x] 4.2 Acrescentar ao módulo a tela de cadastro de Mestre e de Apoiador, com os artefatos
      comprobatórios como endereço e rótulo, sem anexo de arquivo e sem exigir nick, impedindo
      a confirmação sem ao menos um artefato (`RF-02-02`, `RF-02-03`, `RF-02-04`)
- [x] 4.3 Acrescentar a lista de adultos sinalizando quem está **sem nick** e o caminho de
      gravar o nick na ficha, sem sugerir nick algum ao Admin (`RF-02-01`, `RN-14-10`)
- [x] 4.4 Acrescentar a inclusão manual de Admin, o cadastro de responsável com vínculo e grau
      de parentesco barrando o quarto responsável, e a criação de credencial de usuário e senha
      provisória exibida uma única vez (`RF-02-05`, `RF-02-06`, `RF-02-07`, `RN-02-08`)

## 5. Testes

- [x] 5.1 Em `backend/tests/test_persona.py`, cobrir os cenários do delta de
      `cadastro-de-persona` para Guerreiro(a): cadastro completo, campo em falta, nick em uso
      recusado sem revelar o dono, edição que corrige nome, edição para nick em uso, e o 403 do
      Mestre
- [x] 5.2 Criar `backend/tests/test_cadastro_de_adulto.py` cobrindo os cenários de adulto:
      Mestre com link comprobatório, recusa sem artefato, adulto criado sem nick, Apoiador com
      nick do Admin, inclusão de Admin por Admin, 403 do Apoiador, e os quatro cenários da
      gravação de nick pelo Admin — inclusive a recusa quando a persona é Guerreiro(a)

      A recusa por papel do Guerreiro(a) é da rota, não de `definir_ou_trocar_nick` (genérica);
      esse cenário foi coberto ali mesmo via `cliente` (TestClient), e replicado em
      `test_persona_rota.py`, novo, com o contrato HTTP das oito rotas desta change (201, 403,
      404, 422) — não previsto nas tarefas, mas mesmo precedente de `test_responsavel_rota.py`.
- [x] 5.3 Criar `apps/app-03-gestao/src/personas/personas.test.tsx` cobrindo os cenários do
      delta de `aplicacao-de-gestao`: cadastro do Guerreiro(a), nick em uso explicado sem
      revelar o dono, ausência de imagem real, bloqueio da confirmação sem artefato, tela de
      adulto que não pede nick, sinalização de quem está sem nick, ausência de sugestão ao
      Admin, e o quarto responsável barrado

## 6. Documentação

- [x] 6.1 Atualizar `docs/prds/index.md` com a situação do PRD-02 e o PRD-02 no que esta fatia
      mudar. Esta change **não toma decisão nova**: aplica as que a change `nick-de-adulto` já
      gravou nos documentos-fonte e no documento 09, e por isso não mexe nos documentos 01–15
      nem na `nav` do `mkdocs.yml`

      `docs/prds/index.md` ganhou o parágrafo da fatia; o PRD-02 em si não mudou — nenhuma
      pendência da §14 nem linha da §13 é desta fatia, e a rastreabilidade da §15 já cobria
      `RF-02-01` a `RF-02-10`.
