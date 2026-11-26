-- =============================================================================
-- Cópia do conteúdo de produção para a homologação — 1/2: EXPORTAÇÃO.
-- Roda na base de PRODUÇÃO, como `comunidade`, numa transação só de leitura.
-- Procedimento: 2026-11-26-copia-do-conteudo-para-homologacao.md.
--
-- Lista FECHADA: só o que está aqui sai de produção. Nunca entram criança,
-- responsável, portfólio, aula, movimento de recurso, credencial, sessão, chave,
-- auditoria, biometria (inclusive medicao_do_limiar) nem termo (semeado nos dois
-- ambientes). As personas adultas saem SEM e-mail, WhatsApp e PIN; o fundador
-- não sai — a homologação já tem o dela, e a carga troca um id pelo outro.
--
-- Uso:  psql "<conexão de produção>" -v fundador=<uuid> -f <este arquivo>
-- =============================================================================
\set ON_ERROR_STOP on

BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY;

-- O psql não substitui variável dentro do \copy: o id do fundador vai por configuração.
\o /dev/null
SELECT set_config('copia.fundador', :'fundador', true);
\o

-- Personas adultas, mascaradas na origem: o contato real nunca deixa produção.
-- Colunas nomeadas, e não `*`, porque a máscara exige; a carga usa a mesma lista.
\copy (SELECT id, papel, nome, nascimento, NULL AS email, NULL AS whatsapp, avatar, NULL AS pin_verificador, criada_por, criada_em, desativada_em FROM persona WHERE papel IN ('admin', 'mestre', 'apoiador') AND id <> current_setting('copia.fundador')::uuid) TO 'persona.csv' CSV HEADER

-- Território
\copy (SELECT * FROM comunidade_virtual) TO 'comunidade_virtual.csv' CSV HEADER
\copy (SELECT * FROM local) TO 'local.csv' CSV HEADER
\copy (SELECT * FROM ponto_de_apoio) TO 'ponto_de_apoio.csv' CSV HEADER
\copy (SELECT * FROM vinculo_do_mestre) TO 'vinculo_do_mestre.csv' CSV HEADER

-- Catálogo de recursos e acervo
\copy (SELECT * FROM tipo_de_recurso) TO 'tipo_de_recurso.csv' CSV HEADER
\copy (SELECT * FROM preco_de_referencia) TO 'preco_de_referencia.csv' CSV HEADER
\copy (SELECT * FROM valor_de_referencia) TO 'valor_de_referencia.csv' CSV HEADER
\copy (SELECT * FROM item_de_catalogo_avulso) TO 'item_de_catalogo_avulso.csv' CSV HEADER
\copy (SELECT * FROM item_patrimonial) TO 'item_patrimonial.csv' CSV HEADER

-- Poderes, trilhas e missões
\copy (SELECT * FROM poder) TO 'poder.csv' CSV HEADER
\copy (SELECT * FROM trilha) TO 'trilha.csv' CSV HEADER
\copy (SELECT * FROM missao) TO 'missao.csv' CSV HEADER
\copy (SELECT * FROM recompensa_de_marco) TO 'recompensa_de_marco.csv' CSV HEADER
\copy (SELECT * FROM atividade WHERE aula_id IS NULL) TO 'atividade.csv' CSV HEADER
\copy (SELECT * FROM conteudo_da_missao) TO 'conteudo_da_missao.csv' CSV HEADER
\copy (SELECT * FROM bibliografia_da_missao) TO 'bibliografia_da_missao.csv' CSV HEADER
\copy (SELECT * FROM pergunta_de_quiz) TO 'pergunta_de_quiz.csv' CSV HEADER
\copy (SELECT * FROM pergunta_do_desbloqueio) TO 'pergunta_do_desbloqueio.csv' CSV HEADER
\copy (SELECT * FROM tipo_de_coleta) TO 'tipo_de_coleta.csv' CSV HEADER
\copy (SELECT * FROM desafio_de_coleta) TO 'desafio_de_coleta.csv' CSV HEADER
\copy (SELECT * FROM culminancia) TO 'culminancia.csv' CSV HEADER
\copy (SELECT * FROM etiqueta_ods) TO 'etiqueta_ods.csv' CSV HEADER
-- O direcionado leva o nick e a justificativa de uma criança: só o aberto sai.
\copy (SELECT * FROM desafio_extra WHERE modalidade = 'aberto') TO 'desafio_extra.csv' CSV HEADER

-- Apoio escolar e vitrine
\copy (SELECT * FROM disciplina) TO 'disciplina.csv' CSV HEADER
\copy (SELECT * FROM conteudo) TO 'conteudo.csv' CSV HEADER
\copy (SELECT * FROM conteudo_institucional) TO 'conteudo_institucional.csv' CSV HEADER

COMMIT;
