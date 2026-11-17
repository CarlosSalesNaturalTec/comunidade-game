# Avatar sorteado no cadastro da gestão

Origem: **PRD-02**, fatia **28** do `openspec/cronograma-de-fatias.md` (nova, aberta nesta
change). Decisão do fundador de 2026-11-17, em `/opsx:propose`: o formulário de Guerreiro(a) da
App 03 deixa de exigir o campo **Avatar**; no cadastro direto pela gestão, o avatar nasce
**sorteado** do catálogo fechado do documento 15 §7. Na mesma decisão, a **edição** pela gestão
também perde o campo e preserva o avatar gravado.

Identificador **reescrito**: `RF-02-01` (o Admin cadastra e edita com nome, nascimento e nick;
o avatar do cadastro é sorteado). Identificadores aplicados sem mudança: `RN-02-22` (a gestão
não vê imagem real), `RN-02-23` (aviso de coleta, cujo texto deixa de citar o avatar).

## Why

O campo é texto livre: o Admin digita qualquer coisa, que a camada comum não reconhece e desenha
como o avatar padrão do projeto — todo Guerreiro(a) cadastrado pela gestão sai igual. O sorteio
dá a cada um um avatar completo e distinto, dentro do catálogo, sem pedir ao Admin escolha que
cabe à criança: ela troca o avatar quando quiser, na App 05 (`RF-05-51`).

## What Changes

- **Camada comum** — `comum/avatar/` passa a sortear um avatar: um traço do catálogo fechado
  por camada, no objeto versionado do documento 15 §7.2.
- **App 03, cadastro** — sai o campo "Avatar" do formulário de Guerreiro(a) e a checagem
  "Escolha o avatar."; o envio leva o avatar sorteado.
- **App 03, edição** — sai o mesmo campo; o envio reenvia o avatar já gravado. Guerreiro(a) sem
  avatar gravado recebe um sorteado, para a edição não esbarrar na recusa do núcleo.
- **App 03, aviso de coleta** — o texto passa a citar o nome, a data de nascimento e o nick.
- **Núcleo** — nenhuma mudança: `POST` e `PATCH /v1/guerreiros` continuam exigindo avatar, e o
  autocadastro do encontro (App 01) segue com a montagem pela criança.
- **Documentação** — documento 15 §7, documento 09 §1 ("Já decididos"), PRD-02 (`RF-02-01`),
  documento 99 §5 (PRD-02 passa a aplicar o sistema de avatar) e a linha da fatia 28 do
  cronograma.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-de-gestao`: o cadastro e a edição do Guerreiro(a) deixam de pedir avatar; o
  cadastro grava um avatar sorteado e a edição preserva o gravado.
- `camada-visual-comum`: a camada comum ganha o sorteio do avatar dentro do catálogo fechado.

## Impact

- **Camada comum**: `comum/avatar/objeto.ts` (ou arquivo vizinho), `indice.ts` e
  `avatar.test.tsx`.
- **App 03**: `apps/app-03-gestao/src/personas/FormularioDeGuerreiro.tsx` e
  `personas.test.tsx`.
- **Backend**: nenhum arquivo.
- **Dados já gravados**: o Guerreiro(a) cadastrado antes, com texto livre no avatar, continua
  desenhado como o avatar padrão; editar pela gestão **não** o troca (só o vazio é sorteado).
- **Fora do escopo** (PRD-02 §3.2 e decisão): a montagem do avatar pela criança no encontro
  (PRD-04) e a troca pela App 05 (PRD-05); a lista e a ficha da gestão continuam como estão.
