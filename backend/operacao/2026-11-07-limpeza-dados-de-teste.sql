-- =============================================================================
-- Comunidade Game — limpeza dos dados de teste anteriores ao início oficial
-- das aulas na Comunidade Guerreira Zeferina (07/11/2026).
--
-- REGISTRO HISTÓRICO — execução única, já feita. Não é migração, não roda em
-- deploy e não deve ser reexecutado em produção. Registro da decisão: documento
-- 09, "Já decididos", linha "Limpeza dos dados de teste antes do Ciclo 01".
--
-- Execução em produção (07/11/2026, 15:44 UTC), após backup do Cloud SQL:
--   corte = '2026-11-07 12:00:00 America/Bahia' — os testes da manhã também
--   eram de teste. Restaram as personas admin, mestre e apoiador; nenhuma aula.
--   Os 3 arquivos órfãos do bucket foram removidos à mão. As linhas
--   persona.avatar do CSV não são arquivos (o avatar é JSON no banco) e foram
--   ignoradas.
--
-- Decisões do fundador (07/11/2026):
--   A. Todo Guerreiro(a) cadastrado antes do corte é de teste.
--   B. Os responsáveis cadastrados antes do corte também somem.
--   C. Todo movimento de recurso antes do corte é de teste: aportes, livro-razão,
--      ressarcimentos, patrimônio, selos, desafios extras e catálogo avulso.
--   D. A auditoria feita pelas personas apagadas é apagada.
--
-- MANTÉM: comunidade_virtual, local, ponto_de_apoio, tipo_de_recurso, preços e
--   valores de referência, personas admin/mestre/apoiador, vinculo_do_mestre,
--   poder, trilha, missão e todo o conteúdo dela (atividades da missão,
--   conteúdo, bibliografia, perguntas, desafios de coleta, culminância,
--   recompensa de marco, etiqueta ODS), termos, chaves.
--   A missão do Apoiador NÃO fica: ela pertence a uma aula (aula_id obrigatório)
--   e sai com a aula apagada.
--
-- APAGA: aulas com início antes do corte e tudo o que depende delas;
--   Guerreiros e responsáveis criados antes do corte e tudo o que depende deles;
--   o movimento de recurso registrado antes do corte; as séries de coleta
--   abertas antes do corte.
--
-- USO
--   0. Faça o backup:   pg_dump -Fc "$DSN" > antes-da-limpeza.dump
--   1. Ensaio (desfaz tudo no fim, só mostra o que faria):
--        psql "$DSN" -f limpeza-dados-de-teste.sql
--   2. Execução real:
--        psql "$DSN" -v confirmar=sim -f limpeza-dados-de-teste.sql
--   Corte opcional:  -v corte='2026-11-07 00:00:00 America/Bahia'
--
--   Rode com o usuário dono das tabelas (o mesmo das migrações): DISABLE TRIGGER
--   exige isso. O ALTER TABLE trava as tabelas até o fim — rode com os apps
--   parados ou fora do horário de aula.
--
--   Gera arquivos-a-apagar.csv: as referências do armazenamento (fotos,
--   produções, comprovantes) dos registros apagados. O SQL não apaga os
--   arquivos do bucket — apague-os depois, a partir dessa lista.
-- =============================================================================

\set ON_ERROR_STOP on
\pset footer off

\if :{?corte}
\else
  \set corte '2026-11-07 00:00:00 America/Bahia'
\endif

BEGIN;

CREATE TEMP TABLE parametro ON COMMIT DROP AS
  SELECT :'corte'::timestamptz AS corte;

\echo
\echo '>>> Corte:' :'corte'

-- -----------------------------------------------------------------------------
-- 1. Contagem de antes
-- -----------------------------------------------------------------------------
CREATE TEMP TABLE contagem (tabela text PRIMARY KEY, antes bigint, depois bigint)
  ON COMMIT DROP;

DO $$
DECLARE t text; n bigint;
BEGIN
  FOR t IN
    SELECT c.relname FROM pg_class c JOIN pg_namespace s ON s.oid = c.relnamespace
    WHERE s.nspname = 'public' AND c.relkind IN ('r', 'p') AND NOT c.relispartition
      AND c.relname <> 'alembic_version'
  LOOP
    EXECUTE format('SELECT count(*) FROM public.%I', t) INTO n;
    INSERT INTO contagem (tabela, antes) VALUES (t, n);
  END LOOP;
END $$;

-- -----------------------------------------------------------------------------
-- 2. Conjuntos-alvo (só IDs; nada é apagado aqui)
-- -----------------------------------------------------------------------------
CREATE TEMP TABLE alvo_persona ON COMMIT DROP AS
  SELECT id FROM persona, parametro
  WHERE papel IN ('guerreiro', 'responsavel') AND criada_em < corte;

CREATE TEMP TABLE alvo_aula ON COMMIT DROP AS
  SELECT id FROM aula, parametro WHERE inicio_em < corte;

-- Atividade da aula (avulsa) sai; atividade da missão (sem aula) é conteúdo e fica.
CREATE TEMP TABLE alvo_atividade ON COMMIT DROP AS
  SELECT id FROM atividade
  WHERE aula_id IN (SELECT id FROM alvo_aula)
     OR autor_id IN (SELECT id FROM alvo_persona);

CREATE TEMP TABLE alvo_equipe ON COMMIT DROP AS
  SELECT e.id FROM equipe e
  WHERE e.aula_id IN (SELECT id FROM alvo_aula)
     OR e.autor_id IN (SELECT id FROM alvo_persona)
     OR EXISTS (SELECT 1 FROM integrante_da_equipe i
                WHERE i.equipe_id = e.id AND i.persona_id IN (SELECT id FROM alvo_persona));

CREATE TEMP TABLE alvo_partida ON COMMIT DROP AS
  SELECT id FROM partida_de_quiz
  WHERE aula_id IN (SELECT id FROM alvo_aula)
     OR atividade_id IN (SELECT id FROM alvo_atividade)
     OR autor_id IN (SELECT id FROM alvo_persona);

-- A missão do Apoiador pertence à aula (aula_id obrigatório) e sai com ela.
CREATE TEMP TABLE alvo_missao_do_apoiador ON COMMIT DROP AS
  SELECT id FROM missao_do_apoiador
  WHERE aula_id IN (SELECT id FROM alvo_aula)
     OR autor_id IN (SELECT id FROM alvo_persona);

-- Movimento de recurso (decisão C)
CREATE TEMP TABLE alvo_lancamento ON COMMIT DROP AS
  SELECT id FROM lancamento, parametro
  WHERE registrado_em < corte
     OR aula_id IN (SELECT id FROM alvo_aula)
     OR autor_id IN (SELECT id FROM alvo_persona);

CREATE TEMP TABLE alvo_aporte_declarado ON COMMIT DROP AS
  SELECT id FROM aporte_declarado, parametro
  WHERE registrado_em < corte
     OR aula_id IN (SELECT id FROM alvo_aula)
     OR missao_do_apoiador_id IN (SELECT id FROM alvo_missao_do_apoiador)
     OR autor_id IN (SELECT id FROM alvo_persona)
     OR provedor_id IN (SELECT id FROM alvo_persona);

CREATE TEMP TABLE alvo_aporte ON COMMIT DROP AS
  SELECT id FROM aporte, parametro
  WHERE registrado_em < corte
     OR aula_id IN (SELECT id FROM alvo_aula)
     OR lancamento_id IN (SELECT id FROM alvo_lancamento)
     OR aporte_declarado_id IN (SELECT id FROM alvo_aporte_declarado)
     OR autor_id IN (SELECT id FROM alvo_persona)
     OR provedor_id IN (SELECT id FROM alvo_persona);

-- O lançamento de um aporte apagado sai junto.
INSERT INTO alvo_lancamento
  SELECT lancamento_id FROM aporte WHERE id IN (SELECT id FROM alvo_aporte)
  EXCEPT SELECT id FROM alvo_lancamento;

-- Fecho do livro-razão: estorno/ajuste que aponta para lançamento apagado sai junto.
WITH RECURSIVE fecho(id) AS (
  SELECT id FROM alvo_lancamento
  UNION
  SELECT l.id FROM lancamento l JOIN fecho f
    ON l.lancamento_original_id = f.id OR l.lancamento_relacionado_id = f.id
)
INSERT INTO alvo_lancamento SELECT id FROM fecho EXCEPT SELECT id FROM alvo_lancamento;

CREATE TEMP TABLE alvo_item_patrimonial ON COMMIT DROP AS
  SELECT id FROM item_patrimonial, parametro
  WHERE registrado_em < corte OR aporte_de_origem_id IN (SELECT id FROM alvo_aporte);

CREATE TEMP TABLE alvo_desafio_extra ON COMMIT DROP AS
  SELECT id FROM desafio_extra, parametro
  WHERE registrado_em < corte OR aporte_id IN (SELECT id FROM alvo_aporte);

CREATE TEMP TABLE alvo_catalogo ON COMMIT DROP AS
  SELECT id FROM item_de_catalogo_avulso, parametro WHERE registrado_em < corte;

-- Coleta de dados do território
CREATE TEMP TABLE alvo_serie ON COMMIT DROP AS
  SELECT id FROM serie_de_coleta, parametro
  WHERE aberta_em < corte OR coletor_id IN (SELECT id FROM alvo_persona);

CREATE TEMP TABLE alvo_credencial ON COMMIT DROP AS
  SELECT id FROM credencial
  WHERE persona_id IN (SELECT id FROM alvo_persona)
     OR serie_de_coleta_id IN (SELECT id FROM alvo_serie);

-- Auditoria (decisão D)
CREATE TEMP TABLE alvo_auditoria ON COMMIT DROP AS
  SELECT id FROM auditoria WHERE autor_id IN (SELECT id FROM alvo_persona);

\echo
\echo '>>> Alvos'
SELECT 'personas (guerreiro + responsável)' AS alvo, count(*) FROM alvo_persona
UNION ALL SELECT 'aulas',              count(*) FROM alvo_aula
UNION ALL SELECT 'missões do Apoiador', count(*) FROM alvo_missao_do_apoiador
UNION ALL SELECT 'atividades de aula', count(*) FROM alvo_atividade
UNION ALL SELECT 'equipes',            count(*) FROM alvo_equipe
UNION ALL SELECT 'partidas de quiz',   count(*) FROM alvo_partida
UNION ALL SELECT 'lançamentos',        count(*) FROM alvo_lancamento
UNION ALL SELECT 'aportes',            count(*) FROM alvo_aporte
UNION ALL SELECT 'aportes declarados', count(*) FROM alvo_aporte_declarado
UNION ALL SELECT 'itens patrimoniais', count(*) FROM alvo_item_patrimonial
UNION ALL SELECT 'desafios extras',    count(*) FROM alvo_desafio_extra
UNION ALL SELECT 'itens de catálogo',  count(*) FROM alvo_catalogo
UNION ALL SELECT 'séries de coleta',   count(*) FROM alvo_serie
UNION ALL SELECT 'credenciais',        count(*) FROM alvo_credencial
UNION ALL SELECT 'auditoria',          count(*) FROM alvo_auditoria;

-- -----------------------------------------------------------------------------
-- 3. Arquivos do armazenamento que ficam órfãos
-- -----------------------------------------------------------------------------
CREATE TEMP TABLE arquivo_a_apagar (tabela text, referencia text) ON COMMIT DROP;

INSERT INTO arquivo_a_apagar
SELECT 'persona.avatar', avatar FROM persona
  WHERE id IN (SELECT id FROM alvo_persona) AND avatar IS NOT NULL
UNION ALL SELECT 'artefato_comprobatorio', endereco FROM artefato_comprobatorio
  WHERE persona_id IN (SELECT id FROM alvo_persona)
UNION ALL SELECT 'artefato_comprobatorio', endereco_original FROM artefato_comprobatorio
  WHERE persona_id IN (SELECT id FROM alvo_persona) AND endereco_original IS NOT NULL
UNION ALL SELECT 'anexo_do_termo', a.digitalizacao_referencia FROM anexo_do_termo a
  JOIN consentimento c ON c.id = a.consentimento_id
  WHERE c.guerreiro_id IN (SELECT id FROM alvo_persona)
     OR c.responsavel_id IN (SELECT id FROM alvo_persona)
UNION ALL SELECT 'producao_da_missao', referencia FROM producao_da_missao
  WHERE guerreiro_id IN (SELECT id FROM alvo_persona)
     OR atividade_id IN (SELECT id FROM alvo_atividade)
     OR equipe_id IN (SELECT id FROM alvo_equipe)
UNION ALL SELECT 'criacao_original', referencia FROM criacao_original
  WHERE guerreiro_id IN (SELECT id FROM alvo_persona)
     OR equipe_id IN (SELECT id FROM alvo_equipe)
     OR autor_id IN (SELECT id FROM alvo_persona)
UNION ALL SELECT 'desbloqueio_da_missao', comprovacao_referencia FROM desbloqueio_da_missao
  WHERE guerreiro_id IN (SELECT id FROM alvo_persona)
UNION ALL SELECT 'aporte', comprovante_referencia FROM aporte
  WHERE id IN (SELECT id FROM alvo_aporte)
UNION ALL SELECT 'aporte_declarado', comprovante_referencia FROM aporte_declarado
  WHERE id IN (SELECT id FROM alvo_aporte_declarado)
UNION ALL SELECT 'ressarcimento', comprovante_referencia FROM ressarcimento
  WHERE aporte_id IN (SELECT id FROM alvo_aporte)
     OR receita_destinada_id IN (SELECT id FROM alvo_aporte)
     OR registrado_em < (SELECT corte FROM parametro)
UNION ALL SELECT 'registro_de_coleta', midia_referencia FROM registro_de_coleta
  WHERE serie_de_coleta_id IN (SELECT id FROM alvo_serie)
     OR credencial_id IN (SELECT id FROM alvo_credencial)
     OR autor_id IN (SELECT id FROM alvo_persona);

DELETE FROM arquivo_a_apagar WHERE referencia IS NULL OR referencia = '';

\echo
\echo '>>> Arquivos do armazenamento a apagar depois (lista em arquivos-a-apagar.csv)'
SELECT tabela, count(*) FROM arquivo_a_apagar GROUP BY tabela ORDER BY tabela;
\copy (SELECT tabela, referencia FROM arquivo_a_apagar ORDER BY 1, 2) TO 'arquivos-a-apagar.csv' WITH (FORMAT csv, HEADER)

-- -----------------------------------------------------------------------------
-- 4. Travas de só-inserção desligadas só dentro desta transação
-- -----------------------------------------------------------------------------
ALTER TABLE consentimento               DISABLE TRIGGER trg_consentimento_somente_insercao;
ALTER TABLE acesso_ao_template          DISABLE TRIGGER trg_acesso_ao_template_somente_insercao;
ALTER TABLE ponto_regular               DISABLE TRIGGER trg_ponto_regular_nunca_debita;
ALTER TABLE ponto_extra                 DISABLE TRIGGER trg_ponto_extra_acumulado_so_cresce;
ALTER TABLE auditoria                   DISABLE TRIGGER trg_auditoria_somente_insercao;
ALTER TABLE lancamento                  DISABLE TRIGGER trg_lancamento_somente_insercao;
ALTER TABLE anotacao_da_ficha_de_vida   DISABLE TRIGGER trg_anotacao_da_ficha_de_vida_somente_insercao;
ALTER TABLE ocorrencia_de_conduta       DISABLE TRIGGER trg_ocorrencia_de_conduta_somente_insercao;
ALTER TABLE fim_de_vinculo              DISABLE TRIGGER trg_fim_de_vinculo_somente_insercao;
ALTER TABLE acesso_ao_dado_do_guerreiro DISABLE TRIGGER trg_acesso_ao_dado_do_guerreiro_somente_insercao;
ALTER TABLE conclusao_de_desafio_extra  DISABLE TRIGGER trg_conclusao_de_desafio_extra_somente_insercao;

-- -----------------------------------------------------------------------------
-- 5. Remoção, das folhas para a raiz
-- -----------------------------------------------------------------------------

-- 5.1 Desbloqueio de missão
DELETE FROM resposta_da_submissao WHERE submissao_id IN (
  SELECT id FROM submissao_do_desbloqueio WHERE guerreiro_id IN (SELECT id FROM alvo_persona));
DELETE FROM submissao_do_desbloqueio WHERE guerreiro_id IN (SELECT id FROM alvo_persona);
DELETE FROM desbloqueio_da_missao    WHERE guerreiro_id IN (SELECT id FROM alvo_persona);

-- 5.2 Quiz ao vivo
DELETE FROM resposta_de_quiz
  WHERE partida_id IN (SELECT id FROM alvo_partida)
     OR equipe_id IN (SELECT id FROM alvo_equipe)
     OR autor_id IN (SELECT id FROM alvo_persona);
DELETE FROM pergunta_na_partida         WHERE partida_id IN (SELECT id FROM alvo_partida);
DELETE FROM pergunta_anulada_na_partida WHERE partida_id IN (SELECT id FROM alvo_partida);
DELETE FROM equipe_na_partida
  WHERE partida_id IN (SELECT id FROM alvo_partida) OR equipe_id IN (SELECT id FROM alvo_equipe);
DELETE FROM partida_de_quiz WHERE id IN (SELECT id FROM alvo_partida);

-- 5.3 Produção, resultado e conduta
DELETE FROM consulta_ao_assistente
  WHERE equipe_id IN (SELECT id FROM alvo_equipe)
     OR guerreiro_id IN (SELECT id FROM alvo_persona)
     OR autor_id IN (SELECT id FROM alvo_persona);
DELETE FROM producao_da_missao
  WHERE atividade_id IN (SELECT id FROM alvo_atividade)
     OR equipe_id IN (SELECT id FROM alvo_equipe)
     OR guerreiro_id IN (SELECT id FROM alvo_persona)
     OR autor_id IN (SELECT id FROM alvo_persona);
DELETE FROM criacao_original
  WHERE equipe_id IN (SELECT id FROM alvo_equipe)
     OR guerreiro_id IN (SELECT id FROM alvo_persona)
     OR autor_id IN (SELECT id FROM alvo_persona);
DELETE FROM resultado
  WHERE atividade_id IN (SELECT id FROM alvo_atividade)
     OR aula_id IN (SELECT id FROM alvo_aula)
     OR guerreiro_id IN (SELECT id FROM alvo_persona)
     OR autor_id IN (SELECT id FROM alvo_persona);
DELETE FROM ocorrencia_de_conduta
  WHERE atividade_id IN (SELECT id FROM alvo_atividade)
     OR aula_id IN (SELECT id FROM alvo_aula)
     OR guerreiro_id IN (SELECT id FROM alvo_persona)
     OR autor_id IN (SELECT id FROM alvo_persona);

-- 5.4 Equipes
DELETE FROM integrante_da_equipe
  WHERE equipe_id IN (SELECT id FROM alvo_equipe) OR persona_id IN (SELECT id FROM alvo_persona);
UPDATE equipe SET atividade_corrente_id = NULL
  WHERE atividade_corrente_id IN (SELECT id FROM alvo_atividade);
DELETE FROM equipe WHERE id IN (SELECT id FROM alvo_equipe);

-- 5.5 Presença e o que pende da aula
DELETE FROM presenca
  WHERE aula_id IN (SELECT id FROM alvo_aula)
     OR guerreiro_id IN (SELECT id FROM alvo_persona)
     OR autor_id IN (SELECT id FROM alvo_persona);
DELETE FROM mestre_da_aula            WHERE aula_id IN (SELECT id FROM alvo_aula);
DELETE FROM recurso_declarado_da_aula WHERE aula_id IN (SELECT id FROM alvo_aula);

-- 5.6 Desafio extra, reserva, catálogo e recompensa
DELETE FROM conclusao_de_desafio_extra
  WHERE desafio_id IN (SELECT id FROM alvo_desafio_extra)
     OR guerreiro_id IN (SELECT id FROM alvo_persona);
DELETE FROM reserva
  WHERE aula_id IN (SELECT id FROM alvo_aula)
     OR desafio_extra_id IN (SELECT id FROM alvo_desafio_extra)
     OR autor_id IN (SELECT id FROM alvo_persona);
DELETE FROM troca
  WHERE aula_id IN (SELECT id FROM alvo_aula)
     OR guerreiro_id IN (SELECT id FROM alvo_persona)
     OR item_de_catalogo_avulso_id IN (SELECT id FROM alvo_catalogo)
     OR autor_id IN (SELECT id FROM alvo_persona);
DELETE FROM entrega_de_recompensa
  WHERE guerreiro_id IN (SELECT id FROM alvo_persona)
     OR lancamento_id IN (SELECT id FROM alvo_lancamento)
     OR autor_id IN (SELECT id FROM alvo_persona);
DELETE FROM ciencia_da_recompensa
  WHERE guerreiro_id IN (SELECT id FROM alvo_persona) OR autor_id IN (SELECT id FROM alvo_persona);

-- 5.7 Recursos, aportes e livro-razão (decisão C)
DELETE FROM ressarcimento
  WHERE aporte_id IN (SELECT id FROM alvo_aporte)
     OR receita_destinada_id IN (SELECT id FROM alvo_aporte)
     OR registrado_em < (SELECT corte FROM parametro);
DELETE FROM selo_do_apoiador
  WHERE creditado_em < (SELECT corte FROM parametro)
     OR missao_do_apoiador_id IN (SELECT id FROM alvo_missao_do_apoiador)
     OR apoiador_id IN (SELECT id FROM alvo_persona);
DELETE FROM anotacao_da_ficha_de_vida
  WHERE item_patrimonial_id IN (SELECT id FROM alvo_item_patrimonial);
UPDATE bibliografia_da_missao SET item_patrimonial_id = NULL
  WHERE item_patrimonial_id IN (SELECT id FROM alvo_item_patrimonial);
DELETE FROM item_patrimonial WHERE id IN (SELECT id FROM alvo_item_patrimonial);
DELETE FROM desafio_extra    WHERE id IN (SELECT id FROM alvo_desafio_extra);
DELETE FROM aporte           WHERE id IN (SELECT id FROM alvo_aporte);
DELETE FROM aporte_declarado WHERE id IN (SELECT id FROM alvo_aporte_declarado);
DELETE FROM lancamento       WHERE id IN (SELECT id FROM alvo_lancamento);
DELETE FROM item_de_catalogo_avulso WHERE id IN (SELECT id FROM alvo_catalogo);

-- 5.8 Missão do Apoiador da aula apagada
DELETE FROM missao_do_apoiador WHERE id IN (SELECT id FROM alvo_missao_do_apoiador);

-- 5.9 Atividades de aula e aulas
DELETE FROM atividade WHERE id IN (SELECT id FROM alvo_atividade);
DELETE FROM aula      WHERE id IN (SELECT id FROM alvo_aula);

-- 5.10 Coleta de dados do território
DELETE FROM registro_de_coleta
  WHERE serie_de_coleta_id IN (SELECT id FROM alvo_serie)
     OR credencial_id IN (SELECT id FROM alvo_credencial)
     OR autor_id IN (SELECT id FROM alvo_persona);
DELETE FROM credencial     WHERE id IN (SELECT id FROM alvo_credencial);
DELETE FROM serie_de_coleta WHERE id IN (SELECT id FROM alvo_serie);
DELETE FROM solicitacao_de_local WHERE solicitante_id IN (SELECT id FROM alvo_persona);

-- 5.11 Tudo o que pende do Guerreiro(a) e do responsável
DELETE FROM acesso_ao_dado_do_guerreiro
  WHERE guerreiro_id IN (SELECT id FROM alvo_persona)
     OR auditoria_id IN (SELECT id FROM alvo_auditoria);
DELETE FROM auditoria WHERE id IN (SELECT id FROM alvo_auditoria);
DELETE FROM anexo_do_termo
  WHERE autor_id IN (SELECT id FROM alvo_persona)
     OR consentimento_id IN (SELECT id FROM consentimento
          WHERE guerreiro_id IN (SELECT id FROM alvo_persona)
             OR responsavel_id IN (SELECT id FROM alvo_persona)
             OR autor_id IN (SELECT id FROM alvo_persona));
DELETE FROM consentimento
  WHERE guerreiro_id IN (SELECT id FROM alvo_persona)
     OR responsavel_id IN (SELECT id FROM alvo_persona)
     OR autor_id IN (SELECT id FROM alvo_persona);
DELETE FROM leitura_de_termo  WHERE responsavel_id IN (SELECT id FROM alvo_persona);
DELETE FROM vinculo_responsavel
  WHERE guerreiro_id IN (SELECT id FROM alvo_persona)
     OR responsavel_id IN (SELECT id FROM alvo_persona)
     OR autor_id IN (SELECT id FROM alvo_persona);
DELETE FROM solicitacao_do_responsavel
  WHERE guerreiro_id IN (SELECT id FROM alvo_persona)
     OR responsavel_id IN (SELECT id FROM alvo_persona);
DELETE FROM fim_de_vinculo     WHERE guerreiro_id IN (SELECT id FROM alvo_persona);
DELETE FROM vinculo_jogador    WHERE guerreiro_id IN (SELECT id FROM alvo_persona);
DELETE FROM acesso_ao_template WHERE guerreiro_id IN (SELECT id FROM alvo_persona);
DELETE FROM apagamento_de_template WHERE guerreiro_id IN (SELECT id FROM alvo_persona);
DELETE FROM ponto_regular      WHERE guerreiro_id IN (SELECT id FROM alvo_persona);
DELETE FROM ponto_extra        WHERE guerreiro_id IN (SELECT id FROM alvo_persona);
DELETE FROM nivel              WHERE guerreiro_id IN (SELECT id FROM alvo_persona);
DELETE FROM badge              WHERE guerreiro_id IN (SELECT id FROM alvo_persona);
DELETE FROM inscricao_na_trilha WHERE guerreiro_id IN (SELECT id FROM alvo_persona);
DELETE FROM favorito           WHERE guerreiro_id IN (SELECT id FROM alvo_persona);
DELETE FROM sugestao_ou_proposta WHERE autor_id IN (SELECT id FROM alvo_persona);
DELETE FROM artefato_comprobatorio WHERE persona_id IN (SELECT id FROM alvo_persona);
DELETE FROM nick               WHERE persona_id IN (SELECT id FROM alvo_persona);
DELETE FROM sessao             WHERE persona_id IN (SELECT id FROM alvo_persona);

-- 5.12 Referências opcionais (coluna que aceita nulo) de registros mantidos
--      para as personas apagadas viram NULL — ex.: persona.criada_por,
--      ponto_de_apoio.responsavel_id, presenca.confirmador_id.
DO $$
DECLARE r record;
BEGIN
  FOR r IN
    SELECT c.conrelid::regclass AS tabela, a.attname AS coluna
    FROM pg_constraint c
    JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = c.conkey[1]
    JOIN pg_class k ON k.oid = c.conrelid
    WHERE c.contype = 'f' AND c.confrelid = 'public.persona'::regclass
      AND NOT a.attnotnull AND NOT k.relispartition
  LOOP
    EXECUTE format('UPDATE %s SET %I = NULL WHERE %I IN (SELECT id FROM alvo_persona)',
                   r.tabela, r.coluna, r.coluna);
  END LOOP;
END $$;

-- 5.13 As personas
DELETE FROM persona WHERE id IN (SELECT id FROM alvo_persona);

-- -----------------------------------------------------------------------------
-- 6. Travas religadas
-- -----------------------------------------------------------------------------
-- Antecipa a checagem das chaves estrangeiras adiadas: se sobrou referência a
-- algo apagado, o script para aqui e a transação inteira é desfeita.
SET CONSTRAINTS ALL IMMEDIATE;

ALTER TABLE consentimento               ENABLE TRIGGER trg_consentimento_somente_insercao;
ALTER TABLE acesso_ao_template          ENABLE TRIGGER trg_acesso_ao_template_somente_insercao;
ALTER TABLE ponto_regular               ENABLE TRIGGER trg_ponto_regular_nunca_debita;
ALTER TABLE ponto_extra                 ENABLE TRIGGER trg_ponto_extra_acumulado_so_cresce;
ALTER TABLE auditoria                   ENABLE TRIGGER trg_auditoria_somente_insercao;
ALTER TABLE lancamento                  ENABLE TRIGGER trg_lancamento_somente_insercao;
ALTER TABLE anotacao_da_ficha_de_vida   ENABLE TRIGGER trg_anotacao_da_ficha_de_vida_somente_insercao;
ALTER TABLE ocorrencia_de_conduta       ENABLE TRIGGER trg_ocorrencia_de_conduta_somente_insercao;
ALTER TABLE fim_de_vinculo              ENABLE TRIGGER trg_fim_de_vinculo_somente_insercao;
ALTER TABLE acesso_ao_dado_do_guerreiro ENABLE TRIGGER trg_acesso_ao_dado_do_guerreiro_somente_insercao;
ALTER TABLE conclusao_de_desafio_extra  ENABLE TRIGGER trg_conclusao_de_desafio_extra_somente_insercao;

-- -----------------------------------------------------------------------------
-- 7. Conferência
-- -----------------------------------------------------------------------------
DO $$
DECLARE t text; n bigint;
BEGIN
  FOR t IN SELECT tabela FROM contagem LOOP
    EXECUTE format('SELECT count(*) FROM public.%I', t) INTO n;
    UPDATE contagem SET depois = n WHERE tabela = t;
  END LOOP;
END $$;

\echo
\echo '>>> Linhas removidas por tabela'
SELECT tabela, antes, depois, antes - depois AS removidas
FROM contagem WHERE antes <> depois ORDER BY tabela;

\echo
\echo '>>> Tabelas que deviam ficar intactas e mudaram (esperado: nenhuma linha)'
SELECT tabela, antes, depois FROM contagem
WHERE antes <> depois AND tabela IN (
  'comunidade_virtual', 'local', 'ponto_de_apoio', 'tipo_de_recurso',
  'preco_de_referencia', 'valor_de_referencia', 'vinculo_do_mestre', 'poder', 'trilha',
  'missao', 'conteudo_da_missao', 'bibliografia_da_missao', 'pergunta_do_desbloqueio',
  'pergunta_de_quiz', 'desafio_de_coleta', 'tipo_de_coleta', 'culminancia',
  'recompensa_de_marco', 'etiqueta_ods', 'sugestao_de_estrutura',
  'disciplina', 'conteudo', 'conteudo_institucional', 'termo', 'chave_de_aplicacao');

\echo
\echo '>>> Personas por papel depois da limpeza'
SELECT papel, count(*) FROM persona GROUP BY papel ORDER BY papel;

\echo
\echo '>>> Travas religadas (esperado: 11 linhas, todas "O")'
SELECT tgrelid::regclass AS tabela, tgname, tgenabled
FROM pg_trigger WHERE NOT tgisinternal AND tgname LIKE 'trg_%' ORDER BY 1;

\if :{?confirmar}
  \echo
  \echo '>>> COMMIT — limpeza gravada.'
  COMMIT;
\else
  \echo
  \echo '>>> ENSAIO — ROLLBACK, nada foi alterado. Para gravar: -v confirmar=sim'
  ROLLBACK;
\endif
