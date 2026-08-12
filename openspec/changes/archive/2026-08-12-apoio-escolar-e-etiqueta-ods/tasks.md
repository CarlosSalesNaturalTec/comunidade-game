## 1. Modelo de dados e migração

- [x] 1.1 Criar o modelo `Disciplina` com nome normalizado único e `ComAutoria` (`RF-01-35`,
      `RF-01-03`, design — decisões).
- [x] 1.2 Criar o modelo `Conteudo` com disciplina, material, `ComAutoria` e os campos opcionais
      de despublicação — `despublicado_em`, `despublicado_por_id`, `motivo_da_despublicacao`
      (`RF-01-35`, design — decisões).
- [x] 1.3 Criar o modelo `EtiquetaOds` com objetivo (1 a 18), meta opcional, `trilha_id` e
      `missao_id` opcionais e `CheckConstraint` de exatamente um dos dois preenchido
      (`RF-01-40`, `RF-01-45`, design — decisões).
- [x] 1.4 Escrever a oitava migração Alembic criando `disciplina`, `conteudo` e `etiqueta_ods`,
      sem tocar as tabelas das fatias anteriores, e conferir que ela sobe e desce.

## 2. Disciplina

- [x] 2.1 Implementar o cadastro de disciplina exigindo nome, normalizado antes de gravar, restrito
      à operação `suas_trilhas_e_conteudos` (Mestre) ou `tudo` (Admin) — sem posse (`RF-01-35`,
      `RF-01-16`, `RF-01-03`).
- [x] 2.2 Implementar a recusa de disciplina duplicada pelo nome normalizado (`RF-01-35`).
- [x] 2.3 Verificar: Mestre cadastra disciplina com autoria gravada; disciplina sem nome recebe
      422; disciplina duplicada recebe 422; persona sem a operação recebe 403 (`RF-01-35`,
      `RF-01-16`).

## 3. Conteúdo do corpus

- [x] 3.1 Implementar o cadastro de conteúdo exigindo disciplina e material, com a mesma matriz
      de acesso da disciplina, recusando com 422 o conteúdo sem disciplina (`RF-01-35`,
      `RF-01-16`, `RF-01-03`).
- [x] 3.2 Implementar a conferência de posse do conteúdo — aceita o Mestre autor e o Admin,
      recusa outro Mestre com 403 —, reaproveitando o padrão de `conferir_posse_da_trilha`
      (`RF-01-16`, design — decisões).
- [x] 3.3 Implementar a despublicação restrita a Admin, exigindo motivo e gravando quem
      despublicou e quando, sem exigir posse (`RF-01-35`, `RF-01-16`).
- [x] 3.4 Verificar: Mestre autor cadastra e altera o próprio conteúdo; outro Mestre recebe 403
      ao alterar; Admin despublica conteúdo de qualquer Mestre com motivo gravado; despublicação
      sem motivo recebe 422 (`RF-01-35`, `RF-01-16`).

## 4. Etiqueta ODS

- [x] 4.1 Implementar a criação de etiqueta em trilha ou em missão, restrita ao Mestre autor da
      trilha (própria ou da missão) e ao Admin, pela mesma conferência de posse já usada em
      trilha, missão, atividade e resultado (`RF-01-40`, `RF-01-45`, `RF-01-16`).
- [x] 4.2 Implementar a recusa de objetivo fora de 1 a 18, de etiqueta sem trilha nem missão e de
      etiqueta com as duas ao mesmo tempo, com 422 (`RF-01-40`, `RF-01-45`, design — decisões).
- [x] 4.3 Implementar a resolução da etiqueta de uma missão: a própria, se existir; a da trilha,
      na falta dela (`RF-01-45`).
- [x] 4.4 Verificar: etiqueta de trilha e de missão são aceitas e distintas; trilha e missão
      aceitam mais de uma etiqueta; objetivo fora da faixa recebe 422; etiqueta sem vínculo ou
      com os dois vínculos recebe 422; Mestre que não é autor recebe 403; a resolução por missão
      prevalece sobre a da trilha e cai para a trilha na ausência (`RF-01-40`, `RF-01-45`,
      `RF-01-16`).
- [x] 4.5 Verificar que nenhum caminho do núcleo liga etiqueta ODS a crédito de ponto,
      certificação de nível ou concessão de badge (`RN-01-23`).

## 5. Cobertura de ODS

- [x] 5.1 Implementar `cobertura_por_trilha`: união dos objetivos da trilha e das missões dela
      (`RF-01-42`, `RN-01-24`).
- [x] 5.2 Implementar `cobertura_por_poder`: união das coberturas das trilhas vinculadas ao poder
      (`RF-01-42`, `RN-01-24`).
- [x] 5.3 Implementar `cobertura_por_comunidade`: união das coberturas das trilhas em que há
      Guerreiro(a) daquela comunidade com Resultado registrado (`RF-01-42`, `RN-01-24`).
- [x] 5.4 Verificar as três agregações com trilhas, poderes e comunidades diferentes, e verificar
      que nenhuma função do núcleo agrega cobertura por Guerreiro(a) (`RF-01-42`, `RN-01-24`).

## 6. Esteira do backend

- [x] 6.1 Rodar `ruff format --check`, `ruff check` e `pytest` com a cobertura publicada no log,
      sem limiar que bloqueie. A fatia não cria pasta de topo, então não nasce workflow novo:
      `backend-ci.yml` já cobre `backend/**`.

## 7. Documentação

- [x] 7.1 Conferir que nenhuma decisão nova desta fatia ficou fora de `docs/` — a régua de ODS
      já está no documento 11 §2.1 e a do apoio escolar no documento 03 §7, sem mudança.
- [x] 7.2 Atualizar `docs/prds/index.md` se a situação do PRD-01 mudar ao fim desta fatia.
- [x] 7.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR.
