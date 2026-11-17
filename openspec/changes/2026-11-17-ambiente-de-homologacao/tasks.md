# Tasks

## 1. Núcleo

- [ ] 1.1 `backend/src/nucleo/configuracao.py`: `Ambiente` ganha `"homologacao"`, e
      `conferir_configuracao_de_producao` passa a exigir o bucket em todo ambiente que não
      seja `desenvolvimento` (`RF-01-54`, design — decisão 1).
- [ ] 1.2 `backend/tests/test_configuracao.py`: homologação sem bucket não sobe;
      desenvolvimento sem bucket sobe; `CG_AMBIENTE=homologacao` é aceito.
- [ ] 1.3 `backend/tests/test_chave_de_aplicacao.py`: a semeadura de homologação converge
      oito chaves `cg_homologacao_*` e não duplica na segunda execução; chave de homologação
      recebe 401 no núcleo de produção e a de produção, no de homologação (`RF-01-54`,
      `RN-01-51` — cenários do delta de `chave-de-aplicacao`).

## 2. Hospedagem dos frontends

- [ ] 2.1 `firebase.json`: um alvo `<alvo>-homologacao` por alvo existente, com a mesma
      configuração; `api-homologacao` com _rewrite_ para `nucleo-comunidade-game-homologacao`;
      `X-Robots-Tag: noindex, nofollow` em `**` nos alvos de homologação (design — decisão 3).
- [ ] 2.2 `.firebaserc`: os alvos de homologação apontando para os sites `cg-hml-*`.

## 3. Esteiras

- [ ] 3.1 `.github/workflows/backend-deploy.yml`: job único parametrizado pelo _environment_;
      `push`/`workflow_dispatch` publicam na homologação com build da imagem; `workflow_call`
      com `ambiente` e `versao`, e em produção usa `nucleo:<versao>` sem reconstruir,
      falhando se a imagem não existir; publica o alvo `api` com o sufixo do ambiente
      (design — decisão 4).
- [ ] 3.2 Os sete `app-NN-deploy.yml`: mesmos gatilhos da 3.1, checkout de `versao` quando
      chamado, `VITE_*` e alvo lidos do _environment_ (`vars`/`secrets`), `concurrency` por
      ambiente.
- [ ] 3.3 `.github/workflows/producao-deploy.yml` (novo): `workflow_dispatch` com `versao`
      obrigatória, chama o núcleo e, depois dele, as sete Apps com `ambiente: producao`, e
      escreve o `sha` publicado no resumo da execução.

## 4. Provisionamento (fundador, antes do merge)

- [ ] 4.1 Escrever em `backend/operacao/2026-11-17-provisionamento-da-homologacao.md` os
      comandos da decisão 2 e 3 do design — base e usuário na `nucleo-db` com PostGIS,
      bucket com CORS, conta de execução e permissões, segredos `-homologacao`, sites
      `cg-hml-*`, origens no cliente OAuth, _environments_ `homologacao` e `producao` no
      GitHub — e a vedação de restaurar _backup_ de produção na homologação.
- [ ] 4.2 Fundador executa o procedimento e a semeadura da homologação, e grava as oito chaves
      nos segredos do _environment_ `homologacao`. Confirmar ao fim: núcleo de homologação
      responde, e uma chave de homologação recebe 401 em produção.

## 5. Documentação

- [ ] 5.1 `openspec/config.yaml`: a linha de "dois ambientes … 16 chaves" passa a três
      ambientes e 24 chaves, e entra a regra de que notificação a pessoa nunca sai da
      homologação (design — decisão 6). `docs/09` §1, linha "Entrega dos segredos da
      semeadura": "16 segredos" passa a "os segredos de cada ambiente". Documento 03, documento
      09 e PRD-01 já foram atualizados na decisão de 2026-11-17; `docs/prds/index.md`, doc 99
      e `mkdocs.yml` não mudam. Ao arquivar, a linha do cronograma vira `implementado`.
