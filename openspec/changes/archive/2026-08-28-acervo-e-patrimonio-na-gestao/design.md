## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta, e já está pronto:

- `POST /v1/itens-patrimoniais`, `GET /v1/itens-patrimoniais?comunidade_virtual_id=`,
  `POST /v1/itens-patrimoniais/{id}/ficha-de-vida` e `PUT /v1/pontos-de-apoio/{id}/responsavel`
  existem e não mudam — `openspec/specs/patrimonio/spec.md` e `ponto-de-apoio/spec.md`.
- A leitura do item já traz a **ficha de vida completa** e o **responsável derivado** do ponto de
  apoio: a App 03 não monta nem ordena nada disso.
- `teor` é fechado em `cuidado`, `perda` e `dano`; `estado_de_conservacao` é texto do núcleo.
- A área sob comunidade escolhida tem forma consolidada em `TelaDeTerritorio.tsx`, e o
  `podeGerenciar` por `sessao.papel` já é o padrão da App 03.

## Goals / Non-Goals

**Goals:** abrir o acervo permanente na gestão sem que a aplicação derive, some ou ordene nada
que o núcleo já resolve; deixar visível, na própria tela da perda e do dano, a regra do documento
05 §3.6.

**Non-Goals:** aporte de origem no tombamento; Admin como responsável pelo acervo; conferência de
inventário (`RF-02-56`); entregas confirmadas (`RF-02-50`, `RF-02-51`); qualquer caminho de saída
do exemplar do ponto de apoio.

## Decisions

1. **Área nova `acervo/`**, no padrão do `App.tsx`, com `api.ts`, telas e teste. A designação do
   responsável fica em `pontos-de-apoio/`, onde o ponto de apoio já mora — não é assunto do
   exemplar. _Descartado:_ pendurar o acervo dentro da área Pontos de Apoio, que já acumula
   cadastro, situação, extrato e transferência.
2. **A ficha de vida é uma seção do exemplar na própria lista**, aberta e fechada por exemplar,
   e não uma tela à parte: `GET /v1/itens-patrimoniais` já a devolve inteira, e uma tela à parte
   exigiria releitura sem trazer campo novo.
3. **O nome do responsável e o do ponto de apoio são resolvidos por mapa**, a partir de
   `listarMestres`, `listarApoiadores` e `listarPontosDeApoio` — o mesmo recurso que a área
   Território usa para o nick do Guerreiro(a). O núcleo devolve identificador; a tela nunca o
   exibe. _Descartado:_ pedir ao núcleo um campo `responsavel_nome`, que é rota nova para o que
   a aplicação já tem em mãos.
4. **O seletor da designação oferece Mestres e Apoiadores.** O núcleo também aceita Admin
   (`RF-07-49`), mas não há `GET /v1/admins` — a tela não inventa lista. Fica anotado como
   limitação, não como regra.
5. **`estado_de_conservacao` é campo de texto livre**, no tombamento e na anotação: nem o PRD-02
   nem o documento 05 fixam catálogo de estados, e artefato do OpenSpec não cria um.
6. **A releitura é do acervo inteiro da comunidade** depois de tombar ou anotar, como a área
   Recursos já faz depois do aporte: a resposta do núcleo traz o item, mas a lista se mantém
   coerente relendo, e o volume do Ciclo 01 não pede outra coisa.
7. **`RN-02-18` é ausência verificada, não texto de tela**: o teste afirma que nenhuma ação de
   retirada, empréstimo, devolução ou transferência é oferecida no exemplar. A tela não explica
   ao Admin uma operação que não existe.
8. **Nenhum custo novo entra no livro-razão por esta fatia**: o exemplar já foi creditado no
   aporte que o trouxe, e tombar não é consumo (`RN-07-07`).

## Risks / Trade-offs

- Um ponto de apoio sem responsável designado deixa todo o seu acervo sem responsável na tela →
  é o que o núcleo faz (`RN-07-10`), e a designação, que esta fatia traz, é o caminho de resolver.
- A resolução de nomes soma três leituras ao abrir a área → são as mesmas listas que outras áreas
  já carregam, e o Ciclo 01 tem uma comunidade em operação.
