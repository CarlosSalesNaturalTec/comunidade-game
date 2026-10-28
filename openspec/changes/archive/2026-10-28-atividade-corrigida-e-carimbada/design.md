# Design

## Context

Ver `proposal.md` — *Why*. O que molda o desenho:

- `Atividade` (`trilhas/modelo.py`) serve às **duas** coisas: atividade de trilha (`missao_id`)
  e atividade avulsa da gestão (`poder_id`), com `CheckConstraint` de exclusividade. A regra de
  criação está repartida — `trilhas.regra.criar_atividade` para a de trilha,
  `atividades.regra.cadastrar_atividade_avulsa` para a avulsa —, e as rotas também: a de trilha
  em `trilhas/rotas.py` (`POST /missoes/{id}/atividades`), a avulsa em `atividades/rotas.py`
  (`POST`/`GET /atividades`, Admin). Os dois roteadores são montados em `/v1` sem prefixo, na
  ordem trilhas → atividades.
- **O carimbo já é padrão consolidado** nesta base: `PerguntaDoDesbloqueio.substituida_em`, com
  o filtro `substituida_em.is_(None)` nas duas leituras vigentes e o carimbo em
  `corrigir_pergunta_do_desbloqueio` e `remover_pergunta_do_desbloqueio`. Esta fatia aplica o
  mesmo padrão; nada de novo em arquitetura.
- **Nove módulos tocam `Atividade`.** Classificados pelo que fazem com ela:
  - **autoria e execução** (precisam excluir a carimbada): `trilhas/rotas.py` nas duas leituras
    que aninham atividades na missão, `trilhas.regra.desafios_em_aberto_do_guerreiro`,
    `equipes.regra` em `atividades_disponiveis`, `atividades_da_equipe` e
    `declarar_escolha_da_equipe`, e `painel_do_dia.regra` na programação do encontro;
  - **escrita de fato novo** (precisa recusar a carimbada): `resultados/regra.py`,
    `producoes/regra.py`, `quiz/regra.py` e `ocorrencias_de_conduta/regra.py`;
  - **leitura que parte de um fato gravado** (precisa **continuar** resolvendo a carimbada):
    `pontuacao/regra.py`, `evolucao/regra.py` e o `painel_do_dia` quando lê a equipe.
- `natureza` não é inerte: `quiz.regra` exige `NATUREZA_DE_COMPETICAO_AO_VIVO` para abrir
  partida, e `pontuacao.regra` concede o badge quando é `NATUREZA_DE_VALORES_E_CAUSAS`. É o que
  fundamenta `RN-09-49`.
- `FormularioDeAtividade.tsx` já tem os dicionários `ROTULO_DA_MODALIDADE` e `ROTULO_DO_FORMATO`
  locais, e `ListaDeMissoes.tsx` imprime o valor cru ao lado deles.

## Goals / Non-Goals

**Goals:**

- Um único predicado de "atividade vigente", aplicado nos três grupos acima pelo critério certo.
- Correção e remoção que não tocam em nada já gravado, e que não exigem alterar nenhuma das
  cinco chaves estrangeiras.
- Contagem dos fatos servida **sob demanda**, sem encarecer a leitura da trilha.

**Non-Goals:**

- Histórico das correções da atividade (quem mudou o que, quando). A trilha de auditoria das
  escritas do Mestre é `RF-09-48`, Ciclo 02.
- Desfazer a remoção. O carimbo guarda a linha para o fato que a aponta, não para restaurá-la;
  requisito de restauração não existe no PRD.
- Tocar em `atividades/` (a avulsa). As duas rotas novas a recusam; corrigir e remover avulsa é
  do PRD-02, se e quando o fundador abrir a fatia.

## Decisions

1. **A coluna é `Atividade.removida_em`, não `substituida_em`.** Aqui não há substituição —
   `corrigir_atividade` altera a linha no lugar, porque nada na atividade depende de identidade
   estável para o fato gravado (ao contrário da pergunta, cuja resposta aponta a geração). Uma
   só semântica, um só nome honesto. *Descartado:* reusar o nome `substituida_em` por simetria —
   simetria de nome mentindo sobre o que a coluna guarda.

2. **O carimbo é incondicional.** A remoção carimba mesmo quando nenhum fato aponta a atividade,
   como `remover_pergunta_do_desbloqueio` já faz. Um caminho só, sem ramo que depende de
   contagem. *Descartado:* apagar de verdade quando a contagem é zero — dois caminhos para
   testar e manter, e a contagem pode mudar entre a conferência e o `DELETE`.

3. **O predicado vive em `trilhas/regra.py`, como função, não como filtro repetido.**
   `atividade_vigente(consulta)` acrescenta `Atividade.removida_em.is_(None)` a uma consulta, e
   `conferir_atividade_vigente(atividade)` levanta 422 na escrita de fato novo. Os nove módulos
   chamam uma das duas; nenhum repete o `is_(None)` à mão. *Descartado:* um `@property`
   `vigente` no modelo — não serve a consulta SQL, que é onde a exclusão tem de acontecer.

4. **Correção na linha, com os cinco campos opcionais.** `CorrigirAtividadeEntrada` tem
   `extra="forbid"` e expõe só `titulo`, `descricao`, `modalidade`, `formato` e
   `producao_esperada`; `natureza` e `aula_id` ficam fora do contrato e, mandados, respondem 422
   pelo próprio Pydantic (`RN-09-48`, `RN-09-49`). Campo ausente não muda nada; campo presente é
   validado pelas mesmas conferências de `criar_atividade`, extraídas para funções reusadas pelas
   duas. *Descartado:* `PUT` com o corpo inteiro — obrigaria o cliente a reenviar a natureza que
   ele não pode mudar.

5. **A limpeza da `aula_id` acontece dentro de `corrigir_atividade`**, quando o formato efetivo
   depois da correção não é presencial. Não é efeito colateral escondido: é a única forma de o
   invariante que `criar_atividade` já mantém continuar valendo depois de uma correção.

6. **A recusa por partida aberta é conferida antes do carimbo**, por consulta a
   `PartidaDeQuiz` com `situacao == aberta` e `atividade_id` da alvo; a mensagem nomeia a
   partida que precisa ser encerrada. A limpeza do `atividade_corrente_id` é um `UPDATE` em
   `equipe` filtrado por `atividade_corrente_id == alvo.id`, no mesmo `flush` do carimbo.
   *Descartado:* encerrar a partida junto com a remoção — encerrar partida é ato do Mestre na
   tela da turma, com consequência de pontuação; o `DELETE` da atividade não é lugar de fazê-lo
   por tabela.

7. **Os fatos vêm por rota própria: `GET /v1/atividades/{id}/fatos`.** Cinco `COUNT`
   (`resultado`, `producao_da_missao`, `partida_de_quiz` — com o recorte das abertas —,
   `ocorrencia_de_conduta` e `equipe`), autoria estrita, devolvidos como inteiros nomeados.
   *Descartado:* aninhar as contagens em `GET /v1/trilhas/minhas` — cinco `COUNT` por atividade
   por missão por etapa, pago em toda abertura da tela da trilha para uma remoção que quase nunca
   acontece; é o mesmo argumento de `RN-09-46`. *Descartado:* devolver as contagens num `409` do
   próprio `DELETE` e exigir reenvio confirmado — inventaria protocolo de confirmação que nenhuma
   outra rota desta base usa.

8. **A revisão Alembic só acrescenta a coluna**, `nullable=True`, sem índice novo: nenhuma
   consulta filtra por `removida_em` isoladamente — ela entra sempre ao lado de `missao_id` ou
   `aula_id`, e `ix_atividade_aula_id` já existe. `downgrade` apaga as atividades carimbadas
   antes de dropar a coluna, como a revisão da imagem da pergunta faz com as perguntas
   substituídas.

9. **Na App 09, `FormularioDeAtividade` serve criação e correção**, pelo mesmo caminho que a
   fatia 24 abriu em `FormularioDeConteudo`: prop opcional `atividade` preenche os campos e troca
   a chamada; em modo de correção, a natureza é apresentada como texto inerte, não como campo, e
   o seletor de aula desaparece. Os dois dicionários de rótulo passam a ser exportados do módulo.
   O bloco sai de `ListaDeMissoes` para **`BlocoDeAtividades.tsx`**, como a fatia 24 fez com
   `BlocoDeConteudo`: com corrigir, remover e a confirmação por atividade, o estado deixa de
   caber no mapa por missão que `ListaDeMissoes` mantém para os blocos de um ato só.
   *Descartado:* mover os dicionários para `comum/` — só a App 09 nomeia os eixos da atividade
   hoje; extrair sem segundo consumidor é adiantamento.

10. **A contagem é buscada no clique de remover**, e a confirmação é apresentada depois que ela
    chega — a tela nunca pede contagem ao abrir (`RN-09-46`). Falha na busca da contagem não
    bloqueia: a confirmação aparece dizendo que não foi possível conferir os fatos, e a decisão
    segue sendo do Mestre.

## Risks / Trade-offs

- **Esquecer um dos nove módulos deixa atividade removida aparecendo, ou fato novo nascendo sobre
  ela.** → O predicado único da decisão 3 torna a omissão visível em revisão: módulo que toca
  `Atividade` e não chama `atividade_vigente` nem `conferir_atividade_vigente` está classificado
  no terceiro grupo e isso é afirmado no comentário. As tarefas cobrem os nove, um a um.
- **Corrigir a modalidade para `em_equipe_com_familiar` muda o valor do ponto dos lançamentos
  seguintes** (`_valor_regular`), e dois Guerreiros da mesma atividade podem ter valores
  diferentes. → É consequência de qualquer correção, e `RF-09-47` já veda mexer no que foi
  lançado. Não se estorna nada; a correção vale daqui para a frente.
- **A contagem mostrada pode envelhecer entre a conferência e a confirmação.** → Ela é
  informativa, não trava: a única trava é a partida aberta, conferida no servidor, no `DELETE`.
- **O `downgrade` perde as atividades carimbadas.** → É o que a revisão da imagem da pergunta já
  assume: a coluna é a única memória do carimbo, e sem ela a linha volta a aparecer como vigente,
  o que é pior. A tabela de diagnóstico do README do backend não muda.
