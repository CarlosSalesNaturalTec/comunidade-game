# Tarefas — remoção do template da missão

## 1. Núcleo

- [ ] 1.1 Apagar `backend/src/nucleo/template_de_missao/` e tirar o registro do roteador em
      `principal.py` e o import do modelo em `modelos.py` — `RF-09-85` a `RF-09-89`,
      `RF-09-91`, `RF-09-95`, `RN-09-33`, `RN-09-34` (removidos; design — decisão 2).
- [ ] 1.2 Tirar `tecnico` do modelo, da regra e das rotas de `backend/src/nucleo/poderes/`;
      `/v1/poderes` deixa de aceitá-lo (422 pelo `extra="forbid"`) e de devolvê-lo —
      `RF-01-62`, `RN-01-54`, `RF-02-10`.
- [ ] 1.3 Migração Alembic nova, encadeada no _head_: apaga índice e tabela
      `sugestao_de_estrutura` e a coluna `poder.tecnico`; `downgrade` recria as duas vazias —
      design, decisão 1.
- [ ] 1.4 Tirar `deepseek_chave_de_api` e `deepseek_modelo` de `configuracao.py`, e corrigir os
      comentários que citam o template ou o DeepSeek em `configuracao.py`, `assistente/` e
      `producoes/` (fábricas, `nuvem.py`, `local.py`) — documento 03 §1.12.
- [ ] 1.5 Reescrever a frase da `NOTA_SOBRE_IA` em `conteudo_institucional/semeadura.py` para
      "hoje o Gemini, do Google" — nota de transparência, documento 03 §8.

## 2. Aplicações

- [ ] 2.1 App 09: apagar `TemplateDaMissao.tsx` e o teste dele, o `BlocoRecolhivel` "Template
      da missão" de `ListaDeMissoes.tsx` e as duas funções e tipos do template em
      `trilhas/api.ts` — `RF-09-85`, `RF-09-89` (removidos).
- [ ] 2.2 App 09: `CadenciaDeRetomada.tsx` abre o campo com `2, 7, 21` quando a missão não tem
      cadência gravada, sem gravar nada até o Mestre confirmar; resumo do bloco inalterado —
      `RF-09-116`, `RF-09-83`, `RF-09-101`.
- [ ] 2.3 App 03: tirar o campo "técnico" de `FormularioDePoder.tsx`, a marca de
      `ListaDePoderes.tsx` (e o estilo dela) e o atributo de `poderes/api.ts` — `RF-02-10`,
      `RF-01-62`.

## 3. Testes

- [ ] 3.1 Backend: apagar `test_template_de_missao.py`, `_porta.py` e `_rota.py`; tirar o
      template de `test_portas_de_ia.py` e de `conftest.py`; tirar `tecnico` de
      `test_poder.py`, `test_poder_rota.py` e `conftest.py`, com cenário de 422 ao enviar
      `tecnico` e de leitura sem a marca — `RF-01-62`, `RN-01-54`.
- [ ] 3.2 Backend: `test_migracoes.py` sem `tecnico` no `INSERT` de poder e conferindo que a
      tabela e a coluna não existem depois da migração nova;
      `test_conteudo_institucional_semeadura.py` conferindo a nota sem DeepSeek.
- [ ] 3.3 App 09 `trilhas.test.tsx`: ordem dos blocos começando por "Conteúdo", sem "Template
      da missão"; campo da cadência preenchido com `2, 7, 21` em missão sem cadência, sem
      chamada de gravação até confirmar; cadência gravada prevalece — `RF-09-116`, `RF-09-83`.
- [ ] 3.4 App 03 `poderes.test.tsx` e as fábricas de poder em `atividades.test.tsx`: sem o
      campo e sem a marca — `RF-02-10`.

## 4. Deploy

- [ ] 4.1 `.github/workflows/backend-deploy.yml`: tirar `CG_DEEPSEEK_MODELO` do `env` e dos dois
      `--set-env-vars`; `backend/README.md`: tirar a dupla do DeepSeek, o segredo
      `cg-deepseek-api-key` e a linha de diagnóstico dele — design, decisão 5.
- [ ] 4.2 Passos manuais do fundador, **depois do merge e do deploy**, nesta ordem: tirar
      `CG_DEEPSEEK_CHAVE_DE_API` do segredo `GCP_SECRETOS_CG` no GitHub; apagar
      `cg-deepseek-api-key` no Secret Manager; o Admin republicar a seção "Quem somos" pela App
      03 com a nota sem DeepSeek.

## 5. Documentação

- [ ] 5.1 Documentos-fonte e documento 09, conforme a tabela do design: 01, 02 §2, 03 §§1.12, 7,
      8 e 11, 08, 09 §1 (linha nova "Template da missão retirado da App 09", decisão do
      fundador de 2026-11-16, com os identificadores removidos; as quatro linhas reescritas e as
      duas que saem), 11 §2.2 e 99.
- [ ] 5.2 PRD-09 sem o template (§§1, 3, 5 renumerada, 6.2 só com `RF-09-90`, 7, 9, 12, 13, 14
      e 15) e com `RF-09-116` reescrito; PRD-01 (`RN-01-54`, entidade `Poder`); PRD-11 (linha
      da cadência).
- [ ] 5.3 `openspec/cronograma-de-fatias.md`: linha da fatia 35 no bloco do PRD-09, com o slug
      ao arquivar. `docs/prds/index.md` e a `nav` do `mkdocs.yml` não mudam. Ao arquivar,
      remover `openspec/specs/template-da-missao/` — design, decisão 6.
