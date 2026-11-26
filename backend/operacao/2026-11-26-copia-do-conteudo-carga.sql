-- =============================================================================
-- Cópia do conteúdo de produção para a homologação — 2/2: CARGA.
-- Roda na base de HOMOLOGAÇÃO, como `comunidade_homologacao`, numa transação
-- única (`psql -1`): qualquer erro desfaz tudo e a base fica como estava.
-- Procedimento: 2026-11-26-copia-do-conteudo-para-homologacao.md.
--
-- Idempotente pelo id: rodar de novo pula o que já entrou. Choque com dado
-- sintético em restrição única que não seja o id (nome de poder, disciplina...)
-- PARA a carga com o nome da restrição — ajuste o dado sintético e rode de novo.
--
-- Uso:  psql "<conexão de homologação>" -1 \
--         -v fundador_producao=<uuid> -v fundador_homologacao=<uuid> \
--         -f <este arquivo>
-- =============================================================================
\set ON_ERROR_STOP on

\o /dev/null
SELECT set_config('copia.fundador_producao', :'fundador_producao', true),
       set_config('copia.fundador_homologacao', :'fundador_homologacao', true);
\o

-- 1. Área de espera: cópia vazia de cada tabela, descartada no fim da transação.
CREATE TEMP TABLE s_persona (LIKE persona) ON COMMIT DROP;
CREATE TEMP TABLE s_comunidade_virtual (LIKE comunidade_virtual) ON COMMIT DROP;
CREATE TEMP TABLE s_local (LIKE local) ON COMMIT DROP;
CREATE TEMP TABLE s_ponto_de_apoio (LIKE ponto_de_apoio) ON COMMIT DROP;
CREATE TEMP TABLE s_vinculo_do_mestre (LIKE vinculo_do_mestre) ON COMMIT DROP;
CREATE TEMP TABLE s_tipo_de_recurso (LIKE tipo_de_recurso) ON COMMIT DROP;
CREATE TEMP TABLE s_preco_de_referencia (LIKE preco_de_referencia) ON COMMIT DROP;
CREATE TEMP TABLE s_valor_de_referencia (LIKE valor_de_referencia) ON COMMIT DROP;
CREATE TEMP TABLE s_item_de_catalogo_avulso (LIKE item_de_catalogo_avulso) ON COMMIT DROP;
CREATE TEMP TABLE s_item_patrimonial (LIKE item_patrimonial) ON COMMIT DROP;
CREATE TEMP TABLE s_poder (LIKE poder) ON COMMIT DROP;
CREATE TEMP TABLE s_trilha (LIKE trilha) ON COMMIT DROP;
CREATE TEMP TABLE s_missao (LIKE missao) ON COMMIT DROP;
CREATE TEMP TABLE s_recompensa_de_marco (LIKE recompensa_de_marco) ON COMMIT DROP;
CREATE TEMP TABLE s_atividade (LIKE atividade) ON COMMIT DROP;
CREATE TEMP TABLE s_conteudo_da_missao (LIKE conteudo_da_missao) ON COMMIT DROP;
CREATE TEMP TABLE s_bibliografia_da_missao (LIKE bibliografia_da_missao) ON COMMIT DROP;
CREATE TEMP TABLE s_pergunta_de_quiz (LIKE pergunta_de_quiz) ON COMMIT DROP;
CREATE TEMP TABLE s_pergunta_do_desbloqueio (LIKE pergunta_do_desbloqueio) ON COMMIT DROP;
CREATE TEMP TABLE s_tipo_de_coleta (LIKE tipo_de_coleta) ON COMMIT DROP;
CREATE TEMP TABLE s_desafio_de_coleta (LIKE desafio_de_coleta) ON COMMIT DROP;
CREATE TEMP TABLE s_culminancia (LIKE culminancia) ON COMMIT DROP;
CREATE TEMP TABLE s_etiqueta_ods (LIKE etiqueta_ods) ON COMMIT DROP;
CREATE TEMP TABLE s_desafio_extra (LIKE desafio_extra) ON COMMIT DROP;
CREATE TEMP TABLE s_disciplina (LIKE disciplina) ON COMMIT DROP;
CREATE TEMP TABLE s_conteudo (LIKE conteudo) ON COMMIT DROP;
CREATE TEMP TABLE s_conteudo_institucional (LIKE conteudo_institucional) ON COMMIT DROP;

\copy s_persona (id, papel, nome, nascimento, email, whatsapp, avatar, pin_verificador, criada_por, criada_em, desativada_em) FROM 'persona.csv' CSV HEADER
\copy s_comunidade_virtual FROM 'comunidade_virtual.csv' CSV HEADER
\copy s_local FROM 'local.csv' CSV HEADER
\copy s_ponto_de_apoio FROM 'ponto_de_apoio.csv' CSV HEADER
\copy s_vinculo_do_mestre FROM 'vinculo_do_mestre.csv' CSV HEADER
\copy s_tipo_de_recurso FROM 'tipo_de_recurso.csv' CSV HEADER
\copy s_preco_de_referencia FROM 'preco_de_referencia.csv' CSV HEADER
\copy s_valor_de_referencia FROM 'valor_de_referencia.csv' CSV HEADER
\copy s_item_de_catalogo_avulso FROM 'item_de_catalogo_avulso.csv' CSV HEADER
\copy s_item_patrimonial FROM 'item_patrimonial.csv' CSV HEADER
\copy s_poder FROM 'poder.csv' CSV HEADER
\copy s_trilha FROM 'trilha.csv' CSV HEADER
\copy s_missao FROM 'missao.csv' CSV HEADER
\copy s_recompensa_de_marco FROM 'recompensa_de_marco.csv' CSV HEADER
\copy s_atividade FROM 'atividade.csv' CSV HEADER
\copy s_conteudo_da_missao FROM 'conteudo_da_missao.csv' CSV HEADER
\copy s_bibliografia_da_missao FROM 'bibliografia_da_missao.csv' CSV HEADER
\copy s_pergunta_de_quiz FROM 'pergunta_de_quiz.csv' CSV HEADER
\copy s_pergunta_do_desbloqueio FROM 'pergunta_do_desbloqueio.csv' CSV HEADER
\copy s_tipo_de_coleta FROM 'tipo_de_coleta.csv' CSV HEADER
\copy s_desafio_de_coleta FROM 'desafio_de_coleta.csv' CSV HEADER
\copy s_culminancia FROM 'culminancia.csv' CSV HEADER
\copy s_etiqueta_ods FROM 'etiqueta_ods.csv' CSV HEADER
\copy s_desafio_extra FROM 'desafio_extra.csv' CSV HEADER
\copy s_disciplina FROM 'disciplina.csv' CSV HEADER
\copy s_conteudo FROM 'conteudo.csv' CSV HEADER
\copy s_conteudo_institucional FROM 'conteudo_institucional.csv' CSV HEADER

-- 2. Barreira: nada de criança, responsável nem contato passa daqui.
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM s_persona WHERE papel NOT IN ('admin', 'mestre', 'apoiador')) THEN
    RAISE EXCEPTION 'persona fora dos papéis adultos na exportação';
  END IF;
  IF EXISTS (SELECT 1 FROM s_persona
              WHERE email IS NOT NULL OR whatsapp IS NOT NULL OR pin_verificador IS NOT NULL) THEN
    RAISE EXCEPTION 'persona com contato ou PIN na exportação';
  END IF;
  IF EXISTS (SELECT 1 FROM s_atividade WHERE aula_id IS NOT NULL) THEN
    RAISE EXCEPTION 'atividade de aula na exportação';
  END IF;
  IF EXISTS (SELECT 1 FROM s_desafio_extra
              WHERE modalidade <> 'aberto' OR nick_do_destinatario IS NOT NULL) THEN
    RAISE EXCEPTION 'desafio extra direcionado na exportação';
  END IF;
END $$;

-- 3. Fundador: toda coluna que aponta para persona e trazia o id dele em produção
--    passa a trazer o id dele na homologação. Lido das chaves estrangeiras, para
--    não depender de lista de colunas escrita à mão.
DO $$
DECLARE
  r record;
BEGIN
  FOR r IN
    SELECT c.conrelid::regclass::text AS tabela, a.attname AS coluna
      FROM pg_constraint c
      JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY (c.conkey)
     WHERE c.contype = 'f'
       AND c.confrelid = 'persona'::regclass
       AND c.connamespace = 'public'::regnamespace
       AND to_regclass('pg_temp.s_' || c.conrelid::regclass::text) IS NOT NULL
  LOOP
    EXECUTE format('UPDATE pg_temp.%I SET %I = $1 WHERE %I = $2',
                   's_' || r.tabela, r.coluna, r.coluna)
      USING current_setting('copia.fundador_homologacao')::uuid,
            current_setting('copia.fundador_producao')::uuid;
  END LOOP;
END $$;

-- 4. Aporte não vem (movimento de recurso fica em produção): a origem do acervo e
--    do desafio extra fica vazia. O kit da missão aponta para recompensa_de_marco,
--    que aponta para a missão: entra vazio e é religado depois das duas.
UPDATE s_item_patrimonial SET aporte_de_origem_id = NULL;
UPDATE s_desafio_extra SET aporte_id = NULL;
CREATE TEMP TABLE s_kit ON COMMIT DROP AS
  SELECT id, desafio_pratico_kit_id FROM s_missao WHERE desafio_pratico_kit_id IS NOT NULL;
UPDATE s_missao SET desafio_pratico_kit_id = NULL;

-- 5. Carga, na ordem das dependências.
INSERT INTO persona SELECT * FROM s_persona ON CONFLICT (id) DO NOTHING;
INSERT INTO comunidade_virtual SELECT * FROM s_comunidade_virtual ON CONFLICT (id) DO NOTHING;
INSERT INTO local SELECT * FROM s_local ON CONFLICT (id) DO NOTHING;
INSERT INTO ponto_de_apoio SELECT * FROM s_ponto_de_apoio ON CONFLICT (id) DO NOTHING;
INSERT INTO vinculo_do_mestre SELECT * FROM s_vinculo_do_mestre ON CONFLICT (id) DO NOTHING;
INSERT INTO tipo_de_recurso SELECT * FROM s_tipo_de_recurso ON CONFLICT (id) DO NOTHING;
INSERT INTO preco_de_referencia SELECT * FROM s_preco_de_referencia ON CONFLICT (id) DO NOTHING;
INSERT INTO valor_de_referencia SELECT * FROM s_valor_de_referencia ON CONFLICT (id) DO NOTHING;
INSERT INTO item_de_catalogo_avulso SELECT * FROM s_item_de_catalogo_avulso
  ON CONFLICT (id) DO NOTHING;
INSERT INTO item_patrimonial SELECT * FROM s_item_patrimonial ON CONFLICT (id) DO NOTHING;
INSERT INTO poder SELECT * FROM s_poder ON CONFLICT (id) DO NOTHING;
INSERT INTO trilha SELECT * FROM s_trilha ON CONFLICT (id) DO NOTHING;
INSERT INTO missao SELECT * FROM s_missao ON CONFLICT (id) DO NOTHING;
INSERT INTO recompensa_de_marco SELECT * FROM s_recompensa_de_marco ON CONFLICT (id) DO NOTHING;
UPDATE missao m SET desafio_pratico_kit_id = k.desafio_pratico_kit_id
  FROM s_kit k
 WHERE m.id = k.id AND m.desafio_pratico_kit_id IS NULL;
INSERT INTO atividade SELECT * FROM s_atividade ON CONFLICT (id) DO NOTHING;
INSERT INTO conteudo_da_missao SELECT * FROM s_conteudo_da_missao ON CONFLICT (id) DO NOTHING;
INSERT INTO bibliografia_da_missao SELECT * FROM s_bibliografia_da_missao
  ON CONFLICT (id) DO NOTHING;
INSERT INTO pergunta_de_quiz SELECT * FROM s_pergunta_de_quiz ON CONFLICT (id) DO NOTHING;
INSERT INTO pergunta_do_desbloqueio SELECT * FROM s_pergunta_do_desbloqueio
  ON CONFLICT (id) DO NOTHING;
INSERT INTO tipo_de_coleta SELECT * FROM s_tipo_de_coleta ON CONFLICT (id) DO NOTHING;
INSERT INTO desafio_de_coleta SELECT * FROM s_desafio_de_coleta ON CONFLICT (id) DO NOTHING;
INSERT INTO culminancia SELECT * FROM s_culminancia ON CONFLICT (id) DO NOTHING;
INSERT INTO etiqueta_ods SELECT * FROM s_etiqueta_ods ON CONFLICT (id) DO NOTHING;
INSERT INTO desafio_extra SELECT * FROM s_desafio_extra ON CONFLICT (id) DO NOTHING;
INSERT INTO disciplina SELECT * FROM s_disciplina ON CONFLICT (id) DO NOTHING;
INSERT INTO conteudo SELECT * FROM s_conteudo ON CONFLICT (id) DO NOTHING;
-- As três seções da vitrine já existem, semeadas: o texto de produção as substitui.
INSERT INTO conteudo_institucional SELECT * FROM s_conteudo_institucional
  ON CONFLICT (secao) DO UPDATE
     SET texto = EXCLUDED.texto,
         video_url = EXCLUDED.video_url,
         autor_id = EXCLUDED.autor_id,
         publicado_em = EXCLUDED.publicado_em;

-- 6. Conferência: exportado × presente na homologação, tabela por tabela.
SELECT 'persona' AS tabela, (SELECT count(*) FROM s_persona) AS exportadas,
       (SELECT count(*) FROM persona p JOIN s_persona s USING (id)) AS presentes
UNION ALL SELECT 'comunidade_virtual', (SELECT count(*) FROM s_comunidade_virtual),
       (SELECT count(*) FROM comunidade_virtual JOIN s_comunidade_virtual USING (id))
UNION ALL SELECT 'ponto_de_apoio', (SELECT count(*) FROM s_ponto_de_apoio),
       (SELECT count(*) FROM ponto_de_apoio JOIN s_ponto_de_apoio USING (id))
UNION ALL SELECT 'tipo_de_recurso', (SELECT count(*) FROM s_tipo_de_recurso),
       (SELECT count(*) FROM tipo_de_recurso JOIN s_tipo_de_recurso USING (id))
UNION ALL SELECT 'item_patrimonial', (SELECT count(*) FROM s_item_patrimonial),
       (SELECT count(*) FROM item_patrimonial JOIN s_item_patrimonial USING (id))
UNION ALL SELECT 'poder', (SELECT count(*) FROM s_poder),
       (SELECT count(*) FROM poder JOIN s_poder USING (id))
UNION ALL SELECT 'trilha', (SELECT count(*) FROM s_trilha),
       (SELECT count(*) FROM trilha JOIN s_trilha USING (id))
UNION ALL SELECT 'missao', (SELECT count(*) FROM s_missao),
       (SELECT count(*) FROM missao JOIN s_missao USING (id))
UNION ALL SELECT 'conteudo_da_missao', (SELECT count(*) FROM s_conteudo_da_missao),
       (SELECT count(*) FROM conteudo_da_missao JOIN s_conteudo_da_missao USING (id));
