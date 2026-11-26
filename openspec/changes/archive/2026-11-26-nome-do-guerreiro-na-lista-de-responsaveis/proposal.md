# Proposal

PRD-02 — Frontend de gestão (App 03), **fatia 32**, e PRD-09 — Área do Mestre (App 09),
**fatia 37**, do `openspec/cronograma-de-fatias.md`. Alcança `RF-02-111` e `RF-09-122`, sem
identificador novo: é decisão de exibição do fundador de 2026-11-26 sobre requisito já
entregue.

## Why

Na lista de responsáveis o vinculado aparece só como `nick (grau)`. O nick nem sempre diz quem
é a criança, e quem confere o vínculo — o Admin na gestão, o Mestre no encontro — precisa
reconhecê-la pelo nome para saber se o responsável certo está ligado à criança certa. É o mesmo
motivo da fatia 31 do PRD-02, que pôs o nome ao lado do nick na lista de Guerreiros e Guerreiras.

## What Changes

- **Núcleo:** cada vinculado de `GET /v1/responsaveis` passa a trazer o **nome** do
  Guerreiro(a), ao lado do nick e do grau de parentesco, para os dois papéis que leem a rota
  (Admin e Mestre). Recorte por papel, paginação e permissão não mudam.
- **App 03 e App 09:** a coluna dos vinculados passa a mostrar **nick, nome e grau de
  parentesco** de cada um.
- **BREAKING (de spec, não de contrato):** sai a proibição de "nome civil do Guerreiro(a)"
  nessa leitura, gravada pela fatia 24 do PRD-02 e pela fatia 22 do PRD-09. Continuam proibidos
  imagem real, nascimento e contato da criança, e credencial, usuário e contato do responsável
  (`RN-09-18`, invariante 12 do documento 99 §6 — a lista não é superfície pública).
- **Documentação:** a linha "Quem consulta os responsáveis cadastrados" do documento 09 §1
  passa a dizer que a lista traz também o nome do Guerreiro(a) (decisão de 2026-11-26).

Fora do escopo: o formulário de cadastro e de vínculo das duas aplicações, a confirmação de
vínculo recém-criado (fatias 23 do PRD-02 e 21 do PRD-09), as demais rotas de responsável
(`/v1/eu/guerreiros`, `/v1/guerreiros/{id}/responsaveis`) e a App 01.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `responsavel-e-vinculo`: "Admin e Mestre leem os responsáveis cadastrados, com os vinculados
  de cada um" passa a exigir o nome do vinculado e deixa de proibir o nome civil.
- `aplicacao-de-gestao`: "A gestão apresenta os responsáveis cadastrados e retoma o vínculo de
  um deles" passa a exibir o nome do vinculado.
- `area-do-mestre`: "O Mestre consulta os responsáveis que alcança e retoma o vínculo de um
  deles" passa a exibir o nome do vinculado.

## Impact

- `backend/src/nucleo/responsaveis/regra.py` (`vinculados_por_responsavel`) e `rotas.py`
  (`VinculadoDoResponsavelSaida`, docstring de `listar_responsaveis_rota`);
  `backend/tests/test_responsavel_rota.py`.
- `apps/app-03-gestao/src/personas/api.ts`, `ListaDeResponsaveis.tsx`, `personas.test.tsx`.
- `apps/app-09-mestre/src/responsaveis/api.ts`, `ListaDeResponsaveis.tsx`,
  `responsaveis.test.tsx`.
- `docs/09-topicos-em-aberto-e-sugestoes.md` §1 e `openspec/cronograma-de-fatias.md`.
- Sem migração, sem rota nova, sem `Operacao` nova. Campo **acrescentado** à resposta: cliente
  que o ignora segue funcionando.
