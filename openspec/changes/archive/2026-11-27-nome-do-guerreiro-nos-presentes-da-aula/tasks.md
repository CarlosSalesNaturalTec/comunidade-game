# Tasks

## 1. Núcleo

- [x] 1.1 Em `backend/src/nucleo/aulas/rotas.py`, acrescentar `nome: str | None` a
      `PresencaDaAulaSaida` e ler `Persona.nome` na consulta de `listar_presencas_da_aula_rota`,
      atualizando as docstrings (`RF-09-145`, `RN-09-18`); verificável pela tarefa 3.1.

## 2. App 09

- [x] 2.1 Em `apps/app-09-mestre/src/turmas/api.ts`, acrescentar `nome: string | null` a
      `PresencaDaAula` (`RF-09-145`); verificável pelo `tsc`/Vitest da tarefa 3.2.
- [x] 2.2 Em `apps/app-09-mestre/src/turmas/TelaDaAula.tsx`, exibir cada presente como avatar,
      `nick — nome`, com "sem nome" quando o nome for nulo ou vazio (`RF-09-145`, `RN-09-18`);
      verificável pela tarefa 3.2.

## 3. Testes

- [x] 3.1 Em `backend/tests/test_presenca_do_mestre.py`, o cenário "O Mestre lê os presentes da
      sua aula" passa a conferir o `nome` de cada presença e o conjunto de campos da saída com
      `nome`; os demais cenários da leitura seguem verdes (`RF-09-145`, `RN-09-08`,
      `RN-09-18`).
- [x] 3.2 Em `apps/app-09-mestre/src/turmas/turmas.test.tsx`, o grupo "presentes nesta aula"
      confere nick e nome de cada presente, avatar desenhado sem `img`, e o cenário "Presente
      sem nome cadastrado" com a marca "sem nome" (`RF-09-145`, `RN-09-18`).

## 4. Documentação

- [x] 4.1 Decisão de 2026-11-27: na linha "Presentes da aula em Minhas turmas" do documento 09
      §1, "por nick e avatar" passa a "por nick, nome e avatar", com a data; no PRD-09, o
      enunciado do `RF-09-145` recebe o nome e a §"Decisões de 2026-11-20" ganha uma frase sobre
      a de 2026-11-27; na linha da fatia 38 de `openspec/cronograma-de-fatias.md`, a situação
      vira `implementado` com o slug da change. `docs/prds/index.md`, doc 99 e `nav` não mudam.

## Workflow follow-up

- `/opsx:verify` e `/opsx:archive` ao fim; um PR com artefatos, código, testes e documentação.
