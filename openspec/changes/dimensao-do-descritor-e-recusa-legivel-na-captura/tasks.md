## 1. A dimensão do descritor como fato do núcleo

- [x] 1.1 Declarar em `backend/src/nucleo/biometria/regra.py` a constante da dimensão do
      descritor, com `1024` e o comentário que nomeia a origem — o modelo `faceres` da
      biblioteca Human, saída `global_pooling/Mean`, decidida no documento 03 §3.3 —, e fazer a
      conferência de dimensão e `_template_de_descarte` lerem dela, não da `Configuracao`
      (`RF-01-05`, `RN-01-15`, design — decisões 1 e 2).
- [x] 1.2 Remover `biometria_dimensao_do_descritor` de `backend/src/nucleo/configuracao.py` e a
      linha da variável em `backend/README.md`, deixando na lista das sem valor padrão apenas o
      limiar e a chave de cifragem, que seguem sendo parâmetro de implantação (design —
      decisão 3).
- [x] 1.3 Fazer as fixtures do backend usarem a **constante do núcleo** no lugar da dimensão
      própria: `DIMENSAO_DE_TESTE_DO_DESCRITOR` em `backend/tests/conftest.py` passa a ser ela,
      e somem a declaração da variável em `test_migracoes.py` e os valores em
      `test_configuracao.py`, `test_portas_de_ia.py` e `test_armazenamento_porta.py`. Foi a
      dimensão própria da suíte que a manteve verde enquanto produção recusava toda captura —
      com a constante, um número errado passa a quebrar o teste (`RF-01-05`).
- [x] 1.4 Cobrir em `backend/tests/test_biometria.py` os cenários do delta de
      `template-biometrico`: descritor na dimensão da biblioteca é aceito e grava o _template_;
      descritor de outra dimensão é recusado com 422 no campo `descritor`, e a recusa por
      dimensão acontece **antes** da conferência de consentimento; e nenhuma variável de
      ambiente fixa a dimensão (`RF-01-05`, `RF-01-07`, `RN-01-15`).

## 2. A recusa do núcleo chega legível ao Mestre

- [x] 2.1 Fazer `apps/app-01-aula-presencial/src/onboarding/TelaDeCaptura.tsx` apresentar
      `ErroDaApi.message` — a mensagem que a camada de acesso já entrega — no lugar da frase
      fixa do consentimento, guardando frase própria apenas para a falha sem corpo de erro, no
      mesmo padrão da `TelaDoTermo.tsx` ao lado (`RF-04-13`, `RF-04-20`, `RF-01-02`, design —
      decisão 4).
- [x] 2.2 Cobrir em `apps/app-01-aula-presencial/src/onboarding/captura.test.tsx` os três
      cenários do delta de `aplicacao-da-aula-presencial`: a recusa por consentimento aparece
      com a mensagem do núcleo; a recusa por outra causa aparece com o motivo dela, e não com a
      frase do consentimento; e a falha sem resposta do núcleo tem frase própria, sem atribuir
      recusa a ele (`RF-04-13`, `RF-04-20`, `RF-01-02`).

## 3. Implantação

- [ ] 3.1 **EM ABERTO — exige acesso ao Secret Manager e ao projeto do Cloud Run, que a sessão
      de implementação não tem.** Apagar o secret `cg-biometria-dimensao-do-descritor` e
      retirá-lo do mapeamento `GCP_SECRETOS_CG` usado pelo `backend-deploy.yml`. Não é
      pré-requisito do _merge_: o `pydantic-settings` travado no `uv.lock` ignora variável de
      ambiente sem campo correspondente (design — Riscos), então a ordem é livre. Conferir
      depois que o serviço subiu e que uma captura no App 01 grava o _template_.

## 4. Documentação

- [x] 4.1 Declarar no **documento-fonte** da biometria, `docs/03-plataforma-e-arquitetura.md`
      §3.3, que a **dimensão** do descritor é fato da biblioteca e fica fixa no núcleo, ao lado
      do que a §3.3 já diz sobre a minimização e a comparação — é decisão nova, e decisão nova
      mora no documento-fonte antes de morar no doc 09.
- [x] 4.2 Separar, na linha "Parâmetros da entrada do Guerreiro(a)" do
      `docs/09-topicos-em-aberto-e-sugestoes.md` §1, o que é calibrável do que não é: o limiar
      segue parâmetro de implantação calibrado no encontro real; a **dimensão do descritor** sai
      da lista e passa a ser fato da biblioteca, fixo no núcleo — decisão do fundador de
      2026-09-17, registrada na mesma linha. Conferir que nenhum outro documento afirma o
      contrário, e que o documento 03 §3.3 segue coerente.
- [x] 4.3 Marcar como implementada a linha `—` desta change no bloco do PRD-04 do
      `openspec/cronograma-de-fatias.md`, acrescentada com situação `em andamento` na abertura,
      com a ressalva da tarefa 3.1 enquanto ela não for feita. `docs/prds/index.md` não muda: a
      situação do PRD-04 é a mesma, e o documento 99 não muda porque nenhuma relação entre
      documentos mudou.
