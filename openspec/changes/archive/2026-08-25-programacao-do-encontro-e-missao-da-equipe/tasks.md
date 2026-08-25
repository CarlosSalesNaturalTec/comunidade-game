## 1. Núcleo — o vínculo atividade → aula

- [x] 1.1 Somar `aula_id` anulável à `Atividade` em `trilhas/modelo.py`, com chave estrangeira
      para `aula` e índice, e gerar a migração Alembic; verificar que `alembic upgrade head` e
      o `downgrade` correm limpos numa base com atividade já existente (`RF-09-69`).
- [x] 1.2 Aplicar em `trilhas/regra.py` as recusas do vínculo — formato não presencial com aula
      declarada e aula inexistente devolvem 422; Mestre que não é o autor da trilha recebe 403;
      atividade sem aula segue válida (`RF-09-69`, `RF-09-73`, `RF-01-16`).
- [x] 1.3 Expor o campo na criação e na saída da atividade em `trilhas/rotas.py`, sem tocar as
      travas de publicação de `trilhas/regra.py`; verificar pelo OpenAPI que o campo é opcional
      (`RF-09-69`).

## 2. Núcleo — a programação do encontro

- [x] 2.1 Escrever em `equipes/regra.py` a derivação da programação: equipe da aula → aula →
      atividades presenciais que a declararam → missão, conteúdo e bibliografia, filtrando por
      trilha publicada e devolvendo lista vazia quando não houver nada declarado (`RF-04-35`).
- [x] 2.2 Expor `GET /v1/equipes/{id}/missao` em `equipes/rotas.py`, sob a sessão do
      Guerreiro(a), com 403 para quem não integra a equipe; confirmar que `permissoes.py` não
      precisa de operação nova (`RF-04-35`, `RF-01-16`).
- [x] 2.3 Trazer a aula declarada em cada atividade presencial na leitura de turmas do Mestre,
      em `aulas/regra.py`, mantendo a separação por formato e o vínculo em branco quando não
      houver (`RF-09-42`, `RF-09-73`).

## 3. Testes do núcleo

- [x] 3.1 Em `tests/test_atividade.py`, cobrir os cenários do delta `atividade-de-trilha` —
      declaração pelo Mestre autor, atividade sem aula, recusa de on-line e de assíncrona com
      aula, 403 do não autor e 422 de aula inexistente (`RF-09-69`, `RF-09-73`).
- [x] 3.2 Em `tests/test_equipe_rota.py`, cobrir os cenários do delta `equipe` — programação
      devolvida ao integrante, duas trilhas no mesmo encontro, lista vazia sem programação,
      trilha em rascunho fora da saída, 403 de quem não integra e ausência de gravação
      (`RF-04-35`).
- [x] 3.3 Em `tests/test_aula_rota.py`, cobrir os dois cenários novos da leitura de turmas — a
      atividade presencial com a aula declarada e a atividade ainda sem encontro (`RF-09-42`,
      `RF-09-73`).

## 4. App 09 — o Mestre declara o encontro

- [x] 4.1 Somar a escolha da aula ao `FormularioDeAtividade.tsx` e ao `trilhas/api.ts`, ofertada
      só no formato presencial e alimentada pelas turmas que o Mestre já lê; verificar em
      `trilhas.test.tsx` que a escolha some ao trocar o formato e que a atividade é enviada com
      e sem aula (`RF-09-69`, `RF-09-73`).

## 5. App 01 — a equipe consome

- [x] 5.1 Criar `src/api/programacao.ts` para `GET /v1/equipes/{id}/missao` e o módulo
      `src/trilhas/` com a tela da programação — missão, conteúdo por tipo com a fonte do
      terceiro, bibliografia e atividade do dia (`RF-04-35`).
- [x] 5.2 Ligar o caminho das trilhas da tela inicial: da equipe escolhida à programação, com
      a escolha entre atividades mantida no aparelho e nunca enviada ao núcleo, e o aviso em
      linguagem simples quando a programação vier vazia (`RF-04-35`, `RN-04-15`).
- [x] 5.3 Manter legível, sem rede, o conteúdo já carregado, avisar que a programação não pode
      ser atualizada e não enfileirar leitura alguma (`RF-04-58`).

## 6. Testes das aplicações

- [x] 6.1 Em `src/trilhas/trilhas.test.tsx` da App 01, cobrir os cenários dos dois requisitos
      do delta `aplicacao-da-aula-presencial` — missão, conteúdo e atividade do dia; duas
      atividades viram escolha sem envio ao núcleo; programação vazia avisa; fonte do terceiro
      exibida; nenhum dado pessoal além de avatar e nick; rede caída mantém o conteúdo e não
      enfileira (`RF-04-35`, `RF-04-58`, `RN-04-14`).

## 7. Documentação

- [x] 7.1 Gravar a decisão nova no documento-fonte — documento 05 §4, onde o encontro é
      definido — e mover a linha correspondente no documento 09 para "Já decididos"; aplicar ao
      PRD-04 §9 o contrato de `GET /v1/equipes/{id}/missao` (programação em lista, guarda de
      integrante) e ao PRD-09 §6.6 o vínculo na leitura de turmas; somar o parágrafo da fatia a
      `docs/prds/index.md`. O documento 99 e a `nav` do `mkdocs.yml` não mudam — nenhuma
      relação entre documentos muda e nenhum arquivo nasce em `docs/`.
