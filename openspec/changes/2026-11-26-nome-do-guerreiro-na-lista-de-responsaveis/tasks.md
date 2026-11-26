# Tasks

## 1. Núcleo

- [ ] 1.1 Em `backend/src/nucleo/responsaveis/regra.py`, `vinculados_por_responsavel` passa a
      devolver `(vínculo, nick, nome)`, lendo o nome dos Guerreiros da página na mesma leva da
      consulta em lote, sem consulta por vinculado; nome ausente sai vazio (`RF-02-111`,
      `RF-09-122`) — verificado pelo teste 3.1
- [ ] 1.2 Em `backend/src/nucleo/responsaveis/rotas.py`, `VinculadoDoResponsavelSaida` ganha
      `nome: str`, a rota o preenche, e a docstring de `listar_responsaveis_rota` troca "nome
      civil" por nascimento e contato na lista do que nunca sai (`RF-02-111`, `RN-09-18`)

## 2. Telas

- [ ] 2.1 Em `apps/app-03-gestao/src/personas/api.ts`, `VinculadoDoResponsavel` ganha
      `nome: string` e o comentário de `listarResponsaveis` deixa de excluir o nome civil;
      em `ListaDeResponsaveis.tsx`, cada vinculado sai como `nick — nome (grau)`, com a
      ausência de nick ou de nome sinalizada (`RF-02-111`)
- [ ] 2.2 O mesmo em `apps/app-09-mestre/src/responsaveis/api.ts` e
      `ListaDeResponsaveis.tsx` (`RF-09-122`)

## 3. Testes

- [ ] 3.1 Em `backend/tests/test_responsavel_rota.py`: Admin e Mestre recebem nick, nome e
      grau de cada vinculado; Guerreiro(a) sem nome vem com nome vazio e continua na lista; o
      cenário "não expõe dado pessoal da criança" passa a afirmar ausência de imagem,
      nascimento e contato, e não mais do nome (`RF-02-111`, `RF-09-122`, `RN-09-18`)
- [ ] 3.2 Em `apps/app-03-gestao/src/personas/personas.test.tsx`: a lista mostra nick, nome e
      grau de cada vinculado, e a ausência do nome é sinalizada (`RF-02-111`)
- [ ] 3.3 Em `apps/app-09-mestre/src/responsaveis/responsaveis.test.tsx`: os mesmos dois
      cenários na App 09 (`RF-09-122`)

## 4. Documentação

- [ ] 4.1 Em `docs/09-topicos-em-aberto-e-sugestoes.md` §1, na linha "Quem consulta os
      responsáveis cadastrados", a lista passa a trazer "nome, nick, nome do Guerreiro(a) e
      grau de parentesco" com a data 2026-11-26; PRD-02, PRD-09, documento 02 e documento 99
      não mudam — os enunciados de `RF-02-111` e `RF-09-122` não fixam os campos
- [ ] 4.2 Em `openspec/cronograma-de-fatias.md`, as fatias 32 do PRD-02 e 37 do PRD-09 passam
      a `implementado`

## Workflow follow-up

- `/opsx:verify` e `/opsx:archive`, que consolida os três deltas em `openspec/specs/`.
