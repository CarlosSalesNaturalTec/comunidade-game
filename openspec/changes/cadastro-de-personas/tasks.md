## 1. Modelo e migração

- [ ] 1.1 Criar a tabela satélite de **artefato comprobatório** — persona, endereço e rótulo —
      e os satélites dos dados próprios de papel que ainda faltem, em
      `backend/src/nucleo/personas/modelo.py`, com a migração Alembic; verificar que
      `alembic upgrade head` sobe limpo (`RF-02-02`, `RF-02-03`, `RF-02-04`)

## 2. Regra de cadastro no núcleo

- [ ] 2.1 Em `backend/src/nucleo/personas/regra.py`, exigir **ao menos um artefato
      comprobatório** de Mestre e de Apoiador, recusando com 422 sem ele, e recusar anexo de
      arquivo como artefato (`RF-02-04`, `RN-02-01`)
- [ ] 2.2 No mesmo módulo, expor a edição de Guerreiro(a) e a gravação de nick de adulto pelo
      Admin, ambas sujeitas à unicidade global e recusando 422 no campo `nick` sem revelar o
      dono, e a segunda recusando persona de Guerreiro(a) (`RF-02-01`, `RN-01-30`, `RN-14-10`)

## 3. Rotas do núcleo

- [ ] 3.1 Criar em `backend/src/nucleo/personas/rotas.py` as quatro rotas de criação de
      persona — `POST /v1/guerreiros`, `/v1/mestres`, `/v1/apoiadores` e `/v1/admins` —, todas
      de Admin, com 403 para outro papel (`RF-02-01`, `RF-02-02`, `RF-02-03`, `RF-02-05`,
      `RN-02-02`)
- [ ] 3.2 Criar a rota de edição do Guerreiro(a) e a `PUT /v1/personas/{id}/nick` de Admin,
      conforme o desenho (`RF-02-01`); verificar que a edição não troca papel nem apaga persona

## 4. Telas da App 03

- [ ] 4.1 Criar o módulo `apps/app-03-gestao/src/personas/` com a tela de cadastro e edição de
      Guerreiro(a) — nome, nascimento, nick e avatar —, sem exibir imagem real e com o aviso de
      coleta (`RF-02-01`, `RN-02-22`, PRD-02 §11)
- [ ] 4.2 Acrescentar ao módulo a tela de cadastro de Mestre e de Apoiador, com os artefatos
      comprobatórios como endereço e rótulo, sem anexo de arquivo e sem exigir nick, impedindo
      a confirmação sem ao menos um artefato (`RF-02-02`, `RF-02-03`, `RF-02-04`)
- [ ] 4.3 Acrescentar a lista de adultos sinalizando quem está **sem nick** e o caminho de
      gravar o nick na ficha, sem sugerir nick algum ao Admin (`RF-02-01`, `RN-14-10`)
- [ ] 4.4 Acrescentar a inclusão manual de Admin, o cadastro de responsável com vínculo e grau
      de parentesco barrando o quarto responsável, e a criação de credencial de usuário e senha
      provisória exibida uma única vez (`RF-02-05`, `RF-02-06`, `RF-02-07`, `RN-02-08`)

## 5. Testes

- [ ] 5.1 Em `backend/tests/test_persona.py`, cobrir os cenários do delta de
      `cadastro-de-persona` para Guerreiro(a): cadastro completo, campo em falta, nick em uso
      recusado sem revelar o dono, edição que corrige nome, edição para nick em uso, e o 403 do
      Mestre
- [ ] 5.2 Criar `backend/tests/test_cadastro_de_adulto.py` cobrindo os cenários de adulto:
      Mestre com link comprobatório, recusa sem artefato, adulto criado sem nick, Apoiador com
      nick do Admin, inclusão de Admin por Admin, 403 do Apoiador, e os quatro cenários da
      gravação de nick pelo Admin — inclusive a recusa quando a persona é Guerreiro(a)
- [ ] 5.3 Criar `apps/app-03-gestao/src/personas/personas.test.tsx` cobrindo os cenários do
      delta de `aplicacao-de-gestao`: cadastro do Guerreiro(a), nick em uso explicado sem
      revelar o dono, ausência de imagem real, bloqueio da confirmação sem artefato, tela de
      adulto que não pede nick, sinalização de quem está sem nick, ausência de sugestão ao
      Admin, e o quarto responsável barrado

## 6. Documentação

- [ ] 6.1 Atualizar `docs/prds/index.md` com a situação do PRD-02 e o PRD-02 no que esta fatia
      mudar. Esta change **não toma decisão nova**: aplica as que a change `nick-de-adulto` já
      gravou nos documentos-fonte e no documento 09, e por isso não mexe nos documentos 01–15
      nem na `nav` do `mkdocs.yml`
