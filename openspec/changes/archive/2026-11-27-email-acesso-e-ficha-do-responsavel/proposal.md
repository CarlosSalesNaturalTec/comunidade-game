# Proposal

**Origem:** PRD-02, fatia 33, e PRD-09, fatia 40, de `openspec/cronograma-de-fatias.md` —
mesma change, como as fatias 32 e 37. Alcança o PRD-01 (`RF-01-13`).
**Identificadores:** `RF-01-13`, `RF-01-92` (novo), `RF-02-06`, `RF-02-111`, `RF-02-121`
(novo), `RF-09-62`, `RF-09-122`, `RF-09-147` (novo), `RN-01-18`.
**Decisões do fundador de 2026-11-27**, em `/opsx:propose`: (1) o e-mail do responsável entra
**no cadastro, como campo opcional, e na edição**; gravá-lo cria a credencial de login social,
como já acontece com Mestre e Apoiador; (2) o **Admin** edita a ficha do responsável — **nome e
e-mail** — na App 03; (3) a lista de responsáveis passa a mostrar o **acesso** de cada um — o
e-mail do login social e o usuário da credencial de usuário e senha —, nas Apps 03 e 09,
revertendo, só para esses dois campos, a exclusão gravada em 2026-09-26. A senha nunca aparece.

## Why

Os documentos dizem que o responsável carrega **nome e e-mail** (documento 09 §1, "Identidade
do adulto no cadastro") e entra na App 07 **por login social** (documento 03 §1.1). Mas nenhuma
rota grava o e-mail do responsável: `POST /v1/responsaveis` aceita só o nome, e não há edição.
O login social procura uma credencial pelo e-mail — sem ela, todo responsável com conta Google
é recusado com 403, e o único caminho que funciona hoje é a credencial provisória. A lista,
por sua vez, não diz se um responsável já tem acesso, e o Admin não sabe a quem falta dá-lo.

## What Changes

- `POST /v1/responsaveis` passa a aceitar **e-mail opcional**; informado, nasce a credencial de
  login social. O nome continua o único campo obrigatório (`RF-04-60`, App 01 intocada).
- Nasce `PATCH /v1/responsaveis/{id}`, **só Admin**: altera nome e e-mail. Gravar e-mail onde
  não havia cria a credencial social; trocar o e-mail troca o identificador; retirar o e-mail
  desativa a credencial social. E-mail já usado por outra credencial ativa é recusado.
- `GET /v1/responsaveis` passa a trazer o **e-mail** e o **usuário de acesso** (só das
  credenciais ativas). Senha, hash e troca pendente continuam fora.
- **App 03:** campo de e-mail opcional no cadastro; ação **Editar ficha** a partir da lista;
  coluna **Acesso** na lista.
- **App 09:** campo de e-mail opcional no cadastro do encontro; coluna **Acesso** na lista. O
  Mestre não edita a ficha.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `responsavel-e-vinculo`: cadastro aceita e-mail opcional; nasce a edição da ficha pelo Admin;
  a leitura da lista passa a trazer e-mail e usuário de acesso.
- `aplicacao-de-gestao`: cadastro com e-mail, edição da ficha e coluna de acesso na App 03.
- `area-do-mestre`: cadastro com e-mail e coluna de acesso na App 09.

## Impact

- Núcleo: `backend/src/nucleo/responsaveis/` (rotas e regra), reaproveitando
  `_gravar_credencial_de_login_social` e `_email_em_uso_por_outra` de `personas/regra.py`. Sem
  migração: `Persona.email` e `Credencial` já existem. Sem `Operacao` nova.
- Apps 03 e 09: `personas/` e `responsaveis/` — formulário, lista, `api.ts` e testes.
- Documentação: documento 09 §1 (decisão), PRD-01, PRD-02 e PRD-09 (requisitos novos e o
  enunciado da lista), cronograma.
- Fora do escopo: o Mestre editar a ficha; e-mail no cadastro mínimo da App 01; notificação por
  e-mail (`RN-13-15`); edição do vínculo ou do grau de parentesco.
