# Tasks

## 1. Núcleo — a ciência da recompensa

- [x] 1.1 `RN-05-50`: criar o modelo da ciência da recompensa de marco em
      `backend/src/nucleo/recompensas_de_marco/modelo.py` — par (recompensa, Guerreiro(a)) e
      instante, com índice pelo Guerreiro(a) e unicidade do par, no molde da
      `EntregaDeRecompensa`. Verificar que `python -c "import nucleo.modelos"` resolve e que o
      `__init__.py` do módulo exporta a classe nova.
- [x] 1.2 `RN-05-50`: migração Alembic que cria a tabela, nascendo vazia e sem alterar coluna
      existente (design — Migration Plan). Verificar `alembic upgrade head` e `alembic downgrade
      -1` num banco limpo, com a tabela presente e ausente respectivamente.
- [x] 1.3 `RF-05-45`, `RF-05-14`, `RN-05-50`: regra `dar_ciencia_da_recompensa` em
      `regra.py` — recusa 403 quem não é o próprio Guerreiro(a), recusa 422 marco não
      alcançado reusando a conferência de marco alcançado que já existe (a mesma que recusa o
      prático não julgado), e gravação repetida mantém a ciência que havia, sem erro.
- [x] 1.4 `RF-05-45`, `RN-05-50`: rota `POST /v1/eu/recompensas/{id}/ciencia` em `rotas.py`,
      restrita ao papel Guerreiro(a), sem corpo. Verificar na interface OpenAPI que a rota
      aparece sob `/v1` e exige a credencial da persona.
- [x] 1.5 `RF-05-45`, `RF-05-14`, `RN-05-50`: testes em
      `backend/tests/test_ciencia_da_recompensa.py`, cobrindo os cenários do delta de
      `recompensa-de-marco` — o Guerreiro(a) dá ciência; a ciência de um não alcança os colegas;
      dar ciência de novo não duplica nem falha; ciência de recompensa não conquistada é 422;
      ninguém dá ciência pelo outro é 403; a ciência não move entrega, lançamento nem saldo; o
      prático não julgado é 422 e, julgado, admite a ciência.

## 2. Núcleo — a leitura das conquistadas nomeia o recurso

- [x] 2.1 `RF-05-45`, `RN-05-50`: estender `listar_recompensas_conquistadas` e a
      `RecompensaConquistadaSaida` com o `nome` e a `unidade` do `TipoDeRecurso` e o `ciente`,
      sem trazer valor em moedas nem em reais (invariante 16). Verificar a resposta de
      `GET /v1/eu/recompensas` com recompensa semeada.
- [x] 2.2 `RF-05-45`, `RF-05-46`, `RN-05-50`: acrescentar a
      `backend/tests/test_recompensa_conquistada.py` os cenários novos do delta — a leitura
      nomeia o recurso conquistado, a leitura diz se já houve ciência — e conferir que os
      cenários já existentes seguem passando sem alteração de asserção.

## 3. Camada comum — o trio de estrelas

- [x] 3.1 `RF-05-45`: componente do trio de estrelas em `comum/react/`, com SVG próprio na
      grade de `24` px, `aria-hidden`, exportado pelo `indice.ts` — no precedente do
      `BadgeDaFamilia`, nunca como glifo do `Icone`, que fixa `fill="none"` e
      `stroke="currentColor"` (design — decisão 6).
- [x] 3.2 `RF-05-45`: regra em `comum/react/estilos.css` com preenchimento `--cor-ponto` e
      contorno `--cor-ponto-contorno`, sem valor de cor no arquivo do glifo. Verificar que
      nenhum `#` de cor entra no componente nem no CSS novo.
- [x] 3.3 `RF-05-45`: testes do trio em `comum/react/`, cobrindo os cenários do delta de
      `camada-visual-comum` — três estrelas apresentadas; a cor vem dos tokens; o trio é
      escondido de leitor de tela; e o cenário do requisito modificado, a peça preenchida tira a
      cor dos tokens.

## 4. `comum/trilha` — a tela da recompensa no percurso

- [x] 4.1 `RF-05-45`, `RN-05-50`: acrescentar ao cliente `comum/trilha/api.ts` a leitura das
      recompensas conquistadas e a gravação da ciência, com os tipos do contrato da §8 do
      `design.md`.
- [x] 4.2 `RF-05-45`: componente da tela da recompensa em `comum/trilha/`, com os quatro
      elementos na ordem — trio, nome e quantidade do recurso, aviso de que o Mestre confirma a
      entrega, e avançar —, o trio dentro do `RetornoDeConquista` com o fato
      `missao_desbloqueada`, e nenhum caminho de aquisição nem valor em moedas ou reais
      (`RF-05-46`, invariantes 16 e 23).
- [x] 4.3 `RF-05-45`, `RF-05-14`, `RN-05-50`: compor a tela no `GuiaDaTrilha`, substituindo os
      quatro grupos e preservando o cabeçalho, com a leitura filtrada pela trilha aberta, a
      ordenação pela posição da missão e o avançar gravando a ciência antes de seguir (design —
      decisões 2 a 5).
- [x] 4.4 `RF-05-45`, `RF-05-14`, `RF-05-72`, `RN-05-45`, `RN-05-50`: testes em
      `comum/trilha/trilha.test.tsx` cobrindo os cenários comuns às duas aplicações — sondagem
      respondida e quiz aprovado apresentam a tela antes da próxima missão; avançar leva à
      próxima missão; marco sem recompensa não interrompe; a tela não vende nem mostra custo;
      aparece uma vez; recompensa sem ciência espera a volta; prático não julgado não apresenta
      e, julgado, apresenta na volta; duas recompensas saem uma por tela.

## 5. Apps 01 e 05 — o que cada uma acrescenta

- [x] 5.1 `RF-04-72`, `RF-04-73`, `RN-05-50`: conferir na `TelaDeTrilhasDoGuerreiro` da App 01
      que a tela chega pelos componentes compartilhados e que o caminho sem rede segue dizendo
      que precisa de rede, sem enfileirar a ciência na fila local da presença (`RF-04-23`).
      Testes em `apps/app-01-aula-presencial/src/trilhas/trilhas.test.tsx`, com os cenários do
      delta de `aplicacao-da-aula-presencial` — sem rede o caminho não abre; a ciência não entra
      na fila local; a ciência não se perde no aparelho compartilhado.
- [x] 5.2 `RF-05-45`: fazer o `Conquistas.tsx` da App 05 nomear o recurso conquistado com a
      quantidade, em lugar de "Quantidade conquistada: N", e cobrir em
      `apps/app-05-guerreiro/src/carteira/Conquistas.test.tsx` o cenário do delta de
      `area-do-guerreiro` — a lista nomeia o que foi conquistado — mantendo os cenários de
      entrega feita e de não vender.

## 6. Documentação da fatia

- [x] 6.1 Decisão nova de 2026-10-19 nos documentos-fonte: a exceção da estrela cheia e do trio
      na tabela das três grandezas do `docs/15-identidade-visual.md` §9, e as linhas
      correspondentes no `docs/09-topicos-em-aberto-e-sugestoes.md` §1 — a decisão tomada e a
      pendência nova da descrição escrita pelo Mestre autor. Verificar que a §9 segue dizendo
      que as grandezas não se confundem na tela e que o trio é o diferenciador.
- [x] 6.2 `RN-05-50` no `docs/prds/prd-05-area-do-guerreiro.md` — o enunciado na §7 e a
      rastreabilidade da §13, sem tocar no `RF-05-45`, que já exige o aviso. Conferir se a §5.6
      precisa de ajuste de uma linha e se a situação do PRD-05 em `docs/prds/index.md` muda de
      coluna; se não muda, dizer isso em uma linha.
- [x] 6.3 Marcar a fatia 10 do PRD-05 como implementada em
      `openspec/cronograma-de-fatias.md` — a situação daquela linha, nada mais. O documento 99 e
      a `nav` do `mkdocs.yml` só mudam se a relação entre documentos mudar ou nascer arquivo
      novo em `docs/`; nenhum arquivo novo nasce nesta fatia.
