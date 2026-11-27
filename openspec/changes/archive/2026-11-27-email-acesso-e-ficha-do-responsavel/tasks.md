# Tasks

## 1. Núcleo

- [x] 1.1 Em `backend/src/nucleo/personas/regra.py`, tornar públicas a gravação da credencial
      social, a busca da credencial social ativa e a conferência de e-mail em uso, sem mudar
      comportamento; ajustar os chamadores (`RF-01-92`, design — decisão 1). Verifica:
      `uv run pytest tests/test_cadastro_de_adulto.py tests/test_edicao_e_exclusao_de_adulto.py -x` segue verde.
- [x] 1.2 Em `responsaveis/regra.py`, `cadastrar_responsavel` aceita `email` opcional: grava
      `Persona.email` e a credencial social; e-mail de outra credencial ativa → 422 `email`
      (`RF-01-92`, `RF-01-13`). Nasce `alterar_responsavel(nome?, email?)` com criação, troca
      e desativação da credencial social (`RF-01-92`, `RF-02-121`, design — decisão 3).
- [x] 1.3 Em `responsaveis/rotas.py`: `CadastrarResponsavelEntrada.email` opcional;
      `PATCH /v1/responsaveis/{id}` só Admin, 404 para quem não é responsável;
      `ResponsavelDaListaSaida` com `email` e `usuario` das credenciais ativas, numa consulta
      por página (`RF-01-92`, `RF-02-121`, `RF-02-111`, `RF-09-122`, design — decisões 2 e 5).
- [x] 1.4 Testes em `backend/tests/test_responsavel.py` e `test_responsavel_rota.py`: cadastro
      com e sem e-mail, e-mail duplicado no cadastro e na edição, login social reconhecendo o
      e-mail gravado e o trocado e recusando o retirado, credencial de usuário e senha intacta
      na retirada, 403 ao Mestre e aos demais papéis na edição, 404 para outro papel, lista
      com e-mail e usuário, vazios sem credencial ativa, e sem senha nem troca pendente.

## 2. App 03 — gestão

- [x] 2.1 `personas/api.ts`: `cadastrarResponsavel(nome, email?)`, `alterarResponsavel` e o
      tipo `ResponsavelDaLista` com `email` e `usuario` (`RF-02-06`, `RF-02-121`).
- [x] 2.2 `FormularioDeResponsavel.tsx`: campo opcional "E-mail da conta Google", recusa de
      e-mail duplicado no campo (`RF-02-06`, `RF-01-92`).
- [x] 2.3 `ListaDeResponsaveis.tsx` com a coluna **Acesso** e a ação **Editar ficha**; nasce
      `EdicaoDoResponsavel.tsx`, no molde de `EdicaoDoAdulto`, com nome e e-mail, aviso de
      retirada do acesso Google e retorno à lista atualizada; `TelaDeResponsaveis.tsx` liga a
      edição e o aviso de coleta passa a citar e-mail e usuário (`RF-02-111`, `RF-02-121`).
- [x] 2.4 Testes em `personas/personas.test.tsx`: cadastro com e-mail, e-mail duplicado, coluna
      de acesso com e-mail, usuário e "sem acesso", edição do nome, gravação e retirada do
      e-mail, nome em branco não enviado, nenhuma senha na lista.

## 3. App 09 — Área do Mestre

- [x] 3.1 `responsaveis/api.ts`, `FormularioDeResponsavel.tsx` e `ListaDeResponsaveis.tsx`:
      e-mail opcional no cadastro, recusa no campo, coluna **Acesso**, sem edição da ficha;
      aviso de coleta citando e-mail e usuário (`RF-09-147`, `RF-09-122`, `RF-01-92`).
- [x] 3.2 Testes em `responsaveis/responsaveis.test.tsx`: cadastro com e sem e-mail, e-mail
      duplicado, coluna de acesso, nenhuma ação de editar, nenhuma senha.

## 4. Documentação

- [x] 4.1 Documento 09 §1: a decisão de 2026-11-27 em "Já decididos" (e-mail opcional no
      cadastro e na edição, edição só do Admin, acesso visível nas listas); PRD-01: `RF-01-92`
      e as linhas `POST` e `PATCH /v1/responsaveis` da §9; PRD-02: `RF-02-121` e o enunciado
      do `RF-02-111`; PRD-09: `RF-09-147` e o enunciado do `RF-09-122`; cronograma: fatia 33
      do PRD-02 e fatia 40 do PRD-09, com o slug desta change. Sem arquivo novo em `docs/`, sem
      mudança na `nav` nem no documento 99. Verifica: `npm run lint` e
      `mkdocs build --strict` verdes.
