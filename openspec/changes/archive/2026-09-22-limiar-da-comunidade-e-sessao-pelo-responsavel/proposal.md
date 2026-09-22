## Why

Origem: **PRD-01**, linha sem número do bloco do PRD-04 no `openspec/cronograma-de-fatias.md`
— "Limiar da comunidade e sessão aberta pelo responsável, no núcleo". Recorte: `RN-01-57`,
`RF-01-74`, `RN-01-58`, alcançando `RF-01-73`, `RF-01-16`, `RN-01-22` e `RN-01-56`.

A App 05 é usada em casa, entre as aulas. Ali não há aula nem ponto de apoio, e o núcleo hoje
recusa toda comparação feita sem eles — a rota exige `aula_id`, e sem limiar não confere
ninguém. O responsável, que é quem está na sala em casa, não tem no núcleo a operação que
abriria a sessão da criança.

Esta é a primeira das duas fatias da entrada fora do encontro: o núcleo inteiro, sem tela. A
segunda leva a App 05.

## What Changes

- `aula_id` passa a **opcional** em `POST /v1/sessoes/guerreiro`. Presente, vale o caminho de
  hoje — a aula determina o ponto de apoio e o limiar. Ausente, o limiar vem da **comunidade do
  vínculo vigente** do Guerreiro(a), pelo **mais frouxo** entre os pontos de apoio **ativos**
  dela.
- Sem vínculo vigente, ou sem nenhum ponto de apoio com limiar medido na comunidade, a
  comparação recusa — dentro da recusa única, indistinguível no corpo e no tempo.
- O **responsável** ganha operação própria, **com escopo**, na matriz de permissões: abre a
  sessão por confirmação apenas dos Guerreiros e Guerreiras sob a responsabilidade dele.
- Nick que não está sob a responsabilidade de quem confirma recusa de forma **indistinguível**
  de nick inexistente. Sem isso, o responsável ganharia um oráculo para sondar nicks.
- **BREAKING**: nenhum. O campo deixa de ser obrigatório, o que só amplia o que a rota aceita.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `sessao-do-guerreiro`: a aula passa a opcional no pedido, e a confirmação humana passa a
  admitir o responsável, com escopo e recusa indistinguível.
- `template-biometrico`: a comparação ganha a resolução do limiar pela comunidade, para quando
  não houver aula.
- `permissoes-e-escopo-de-comunidade`: a matriz ganha a operação do responsável, que é a
  primeira com escopo por vínculo.

## Impact

- `backend/src/nucleo/sessoes/rotas.py` — `aula_id` opcional; a rota de confirmação passa a
  conferir o escopo de quem confirma.
- `backend/src/nucleo/biometria/regra.py` — resolução do limiar pela comunidade, em tempo
  constante com o caminho da aula.
- `backend/src/nucleo/permissoes.py` — a operação nova do responsável.
- `backend/tests/` — `test_sessao_de_guerreiro.py`, `test_biometria.py`, `test_permissoes.py`.
- Nada em `apps/`. A App 05 é a fatia seguinte; a App 01 não muda, e a change dela precisa
  entrar **antes** desta.
