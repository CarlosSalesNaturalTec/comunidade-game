# Tasks

## 1. A coluna do carimbo e o predicado único

- [ ] 1.1 Em `backend/src/nucleo/trilhas/modelo.py`, `Atividade.removida_em`
      (`DateTime(timezone=True)`, anulável), no molde de `PerguntaDoDesbloqueio.substituida_em`,
      com o comentário dizendo por que a atividade se carimba em vez de se apagar — cinco tabelas
      a apontam (`RN-09-47`, design — decisão 1).
- [ ] 1.2 Revisão do Alembic que acrescenta `removida_em` a `atividade`, sem índice novo, com
      `downgrade` que apaga as atividades carimbadas antes de dropar a coluna, como a revisão da
      imagem da pergunta faz (`RN-09-47`, design — decisão 8). Verificar que
      `alembic upgrade head` e `Base.metadata` seguem em paridade no teste que já cobre isso.
- [ ] 1.3 Em `backend/src/nucleo/trilhas/regra.py`, `atividade_vigente(consulta)` — acrescenta
      `Atividade.removida_em.is_(None)` — e `conferir_atividade_vigente(atividade)` — levanta
      **422** nomeando a atividade removida. São as duas únicas portas do carimbo; nenhum módulo
      repete o `is_(None)` à mão (`RN-09-47`, design — decisão 3).

## 2. Correção da atividade de trilha

- [ ] 2.1 Extrair de `criar_atividade`, em `trilhas/regra.py`, as conferências de título,
      modalidade, formato e produção esperada para funções reusadas pela criação e pela correção,
      sem mudar mensagem nem campo de nenhuma recusa que já existe (`RF-09-70`, `RF-09-127`).
- [ ] 2.2 `corrigir_atividade` em `trilhas/regra.py`: autoria **estrita**
      (`conferir_autoria_estrita_da_trilha`), recusa da avulsa (`poder_id`) com **422**, recusa da
      carimbada, campo omitido conservando o valor, e as conferências de 2.1 em cada campo
      presente (`RF-09-127`, `RN-09-49`, design — decisão 4).
- [ ] 2.3 Limpeza da `aula_id` dentro de `corrigir_atividade` quando o formato efetivo depois da
      correção não é presencial (`RN-09-48`, design — decisão 5).
- [ ] 2.4 `PATCH /v1/atividades/{id}` em `trilhas/rotas.py`, com `CorrigirAtividadeEntrada`
      (`extra="forbid"`, cinco campos opcionais, sem `natureza` e sem `aula_id`), devolvendo a
      atividade corrigida por `saida_da_atividade` (`RF-09-127`, `RN-09-48`, `RN-09-49`,
      design — decisão 4).
- [ ] 2.5 Testes da correção em `backend/tests/test_atividade.py`, cobrindo os cenários "O Mestre
      autor corrige o título da atividade", "A correção alcança a trilha publicada", "O Resultado
      já lançado não é tocado pela correção", "Correção sem título é recusada", "Modalidade fora
      dos valores previstos é recusada na correção", "Mestre que não é o autor é recusado", "Admin
      não corrige atividade de trilha", "Correção que declara natureza é recusada", "A natureza
      gravada sobrevive à correção dos demais campos", "O formato sai do presencial e a aula é
      limpa", "O formato segue presencial e a aula permanece", "Correção que declara aula é
      recusada" e "Correção de atividade avulsa é recusada" (`RF-09-127`, `RN-09-48`, `RN-09-49`).

## 3. Remoção que carimba e trata o estado vivo

- [ ] 3.1 `remover_atividade` em `trilhas/regra.py`: autoria estrita, recusa da avulsa, recusa
      **422** enquanto houver `PartidaDeQuiz` com situação aberta sobre a atividade, carimbo
      incondicional em `removida_em` e `UPDATE` que zera `equipe.atividade_corrente_id` das
      equipes que a apontavam, no mesmo `flush` (`RF-09-128`, `RN-09-47`, design — decisões 2, 6).
- [ ] 3.2 `fatos_da_atividade` em `trilhas/regra.py`: as cinco contagens — `resultado`,
      `producao_da_missao`, `partida_de_quiz` com o recorte das abertas, `ocorrencia_de_conduta`
      e `equipe` com ela corrente —, com autoria estrita (`RF-09-128`, design — decisão 7).
- [ ] 3.3 `DELETE /v1/atividades/{id}` e `GET /v1/atividades/{id}/fatos` em `trilhas/rotas.py`
      (`RF-09-128`, design — decisão 7).
- [ ] 3.4 Testes da remoção em `backend/tests/test_atividade.py`, cobrindo os cenários "A
      atividade removida sai da leitura e permanece guardada", "A remoção alcança a trilha
      publicada", "A missão pode ficar sem atividade alguma", "Mestre que não é o autor é
      recusado", "Admin não remove atividade de trilha", "Remoção de atividade avulsa é
      recusada", "Partida de quiz aberta impede a remoção", "Partida encerrada não impede a
      remoção", "O Mestre autor lê os fatos da atividade", "Atividade sem fato algum" e "Mestre
      que não é o autor é recusado" na leitura dos fatos (`RF-09-128`, `RN-09-47`).

## 4. O carimbo alcança as leituras e as escritas de fato novo

- [ ] 4.1 Leituras de autoria: `atividade_vigente` nas duas consultas de `trilhas/rotas.py` que
      aninham atividades na missão — a trilha do Mestre e a leitura pública — e na duplicação de
      trilha, que não deve copiar atividade carimbada (`RN-09-47`).
- [ ] 4.2 Leituras de execução: `atividade_vigente` em
      `trilhas.regra.desafios_em_aberto_do_guerreiro`, em
      `equipes.regra.atividades_disponiveis` e `atividades_da_equipe`, e em
      `painel_do_dia.regra._atividades_previstas`; recusa da carimbada em
      `equipes.regra.declarar_escolha_da_equipe` (`RN-09-47`, `RF-05-19`, `RF-04-35`, `RF-02-42`).
- [ ] 4.3 Escritas de fato novo: `conferir_atividade_vigente` em `resultados/regra.py`,
      `producoes/regra.py`, `quiz/regra.py` e `ocorrencias_de_conduta/regra.py` (`RN-09-47`).
- [ ] 4.4 Afirmar, em comentário, que `pontuacao/regra.py`, `evolucao/regra.py` e a leitura da
      equipe no `painel_do_dia` **continuam** resolvendo a atividade carimbada, porque partem de
      um fato gravado — é delas que o fato fala (`RN-09-47`, design — *Context*, terceiro grupo).
- [ ] 4.5 Testes do alcance, nos arquivos de cada capacidade — `test_meus_desafios.py`,
      `test_equipe_escolha.py`, `test_painel_do_dia.py`, `test_lancamento_por_atividade.py`,
      `test_producao_da_missao.py`, `test_ocorrencia_de_conduta.py` e `test_percurso_da_trilha.py`
      —, cobrindo os cenários "Atividade removida pelo Mestre não aparece", "Atividade removida
      pelo Mestre é recusada na escolha", "A remoção zera a escolha já declarada", "Atividade
      removida pelo Mestre sai dos semanais", os quatro cenários de fato novo recusado ("Lançamento
      de Resultado", "Entrega de produção", "Abertura de partida", "Ocorrência de conduta") e "O
      fato gravado segue resolvendo a atividade" (`RN-09-47`).

## 5. O bloco Atividades da App 09

- [ ] 5.1 Em `apps/app-09-mestre/src/trilhas/api.ts`, `corrigirAtividade`, `removerAtividade` e
      `fatosDaAtividade`, no padrão das chamadas que já existem (`RF-09-127`, `RF-09-128`).
- [ ] 5.2 `FormularioDeAtividade.tsx` passa a servir criação **e** correção: prop opcional
      `atividade` preenche os campos e troca a chamada; em correção a natureza é texto inerte e o
      seletor de aula desaparece, com o aviso de que a aula deixa de valer ao sair do presencial;
      `ROTULO_DA_MODALIDADE` e `ROTULO_DO_FORMATO` passam a ser exportados (`RF-09-127`,
      `RN-09-48`, `RN-09-49`, design — decisão 9).
- [ ] 5.3 `ListaDeMissoes.tsx`: o bloco Atividades nomeia modalidade e formato pelos dicionários
      de 5.2, e cada linha ganha corrigir e remover; a remoção busca os fatos no clique e
      apresenta a confirmação com as contagens, seguindo mesmo quando a busca falha
      (`RF-09-127`, `RF-09-128`, `RN-09-46`, design — decisão 10).
- [ ] 5.4 Tratamento da recusa por partida aberta em linguagem simples, pelo campo e pela
      mensagem que o núcleo devolve, no padrão de `ErroDaApi` que a tela já usa (`RF-09-128`).
- [ ] 5.5 Testes em `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`, cobrindo os cenários "A
      linha da atividade nomeia modalidade e formato em português", "O Mestre corrige o título da
      atividade", "O formulário de correção abre preenchido", "Levar o formato para fora do
      presencial avisa sobre a aula", "A recusa do núcleo aponta o campo", "A confirmação diz
      quantos fatos apontam", "Atividade sem fato algum é removida direto da confirmação", "A
      contagem não é buscada ao abrir a trilha" e "Partida aberta é recusada em linguagem simples"
      (`RF-09-127`, `RF-09-128`, `RN-09-46`).

## 6. Documentação

- [ ] 6.1 `docs/03-decisoes-tecnicas-e-arquitetura.md` §11: marcador novo com a decisão do
      fundador de 2026-10-27 — a atividade da missão se corrige e se remove, a remoção carimba,
      a natureza não se troca, o formato fora do presencial limpa a aula, a escolha corrente da
      equipe é zerada e a partida aberta impede a remoção. Em
      `docs/09-topicos-em-aberto-e-sugestoes.md` §1, a linha da decisão, nomeando esta change.
- [ ] 6.2 PRD-09: `RF-09-127` e `RF-09-128` na tabela da §6.1, `RN-09-47`, `RN-09-48` e
      `RN-09-49` na da §7, as três rotas novas na tabela da §9 e a linha de rastreabilidade na
      §15. `docs/prds/index.md` e o documento 99 só se a situação do PRD ou a relação entre
      documentos mudar — nenhum arquivo novo nasce em `docs/`, então a `nav` do `mkdocs.yml` não
      muda.
- [ ] 6.3 `openspec/cronograma-de-fatias.md`: a fatia 25 do PRD-09 passa a `implementado`, com o
      slug desta change no lugar do recorte previsto e `RN-09-49` acrescentada aos identificadores
      — ela nasceu da elicitação na abertura desta change, com decisão do fundador de 2026-10-27.
