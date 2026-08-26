## 1. Núcleo — as duas leituras novas

- [x] 1.1 Extrair para `pontuacao/regra.py` a derivação do ranking hoje embutida em
      `vitrine/rotas.py` — soma de `PontoRegular` menos o débito das ocorrências de ciclo
      encerrado —, parametrizada pelo **portão de divulgação** e pelo **recorte** por
      `trilha_id` ou `poder_id`, e reescrever `GET /vitrine/rankings` para chamá-la sem mudar
      de contrato (design — decisões 2 e 3; `RF-05-52`, `RN-05-18`).
- [x] 1.2 Escrever no mesmo módulo a consulta do **ranking da turma**: comunidade do
      Guerreiro(a) em sessão, portão de divulgação desligado, recorte opcional por trilha ou
      poder e a **posição do próprio Guerreiro(a)** sempre na resposta, ainda que fora da
      página (`RF-05-53`, `RF-05-84`, `RN-05-16`).
- [x] 1.3 Publicar `GET /v1/rankings/{comunidade}` em `pontuacao/rotas.py` — módulo novo,
      registrado em `principal.py` —, restrita ao papel Guerreiro(a) com 403 para os demais e
      403 para comunidade diferente da dele; saída só com avatar, nick, posição e ponto regular
      (`RF-05-52`, `RF-05-84`, `RN-05-21`, invariante 12).
- [x] 1.4 Escrever em `recompensas_de_marco/regra.py` a consulta das **recompensas
      conquistadas** pelo Guerreiro(a), reaproveitando a derivação de marco alcançado que a
      recusa de entrega já usa; cada uma com trilha, marco, tipo de recurso, quantidade e a
      situação da entrega — entregue com data, ou aguardando o Mestre —, sem moedas e sem reais
      e sem antecipar lastro nem esgotamento (`RF-05-45`, `RN-05-07`).
- [x] 1.5 Publicar `GET /v1/eu/recompensas` em `recompensas_de_marco/rotas.py`, restrita ao
      Guerreiro(a) em sessão, com 403 para os demais papéis (`RF-05-45`, `RN-05-21`).
- [x] 1.6 Acrescentar a `EuSaida`, em `sessoes/rotas.py`, o estado da **autorização de
      divulgação** do Guerreiro(a), derivado por `autorizacao_de_divulgacao_vigente`; o campo
      só aparece para papel Guerreiro(a) e não traz responsável, data nem motivo (`RF-05-50`,
      `RN-05-14`, `RN-05-21`).

## 2. App 05 — carteira, catálogo, conquistas, perfil e ranking

- [x] 2.1 Criar o cliente das rotas do bloco em `apps/app-05-guerreiro/src/api/`, no molde de
      `coleta.ts`: pontos extras, catálogo avulso, trocas, recompensas conquistadas, ranking e
      o estado da divulgação vindo de `GET /v1/eu`.
- [x] 2.2 Abrir a área do bloco em `AreaDoGuerreiro.tsx`, ao lado da coleta, com as quatro
      telas — carteira, catálogo, conquistas e ranking —, lendo à entrada e **sem sondagem
      periódica** (design — decisão 6).
- [x] 2.3 Tela da **carteira**: acumulado e saldo disponível separados e rotulados, sem soma e
      sem ponto regular, com a frase de que o acumulado só cresce e o trocável é o saldo
      (`RF-05-82`, `RN-05-39`, `RN-05-40`, `RN-05-42`).
- [x] 2.4 Tela do **catálogo avulso**: itens ativos da comunidade com preço em pontos extras e
      estoque, o aviso de que a troca é presencial com o Mestre ao fim do encontro, nenhuma
      ação de trocar ou reservar, e a explicação do catálogo vazio (`RF-05-83`, `RF-05-86`,
      `RF-05-87`).
- [x] 2.5 **Histórico de trocas** na mesma tela do catálogo: item, preço cobrado na época e
      data, sem moedas e sem reais (`RF-05-88`).
- [x] 2.6 Tela das **conquistas**: recompensa de marco conquistada, dizendo que o Mestre
      confirma a entrega, e a entregue com a data; nenhum caminho de compra em nenhuma tela do
      bloco (`RF-05-45`, `RF-05-46`, `RN-05-41`).
- [x] 2.7 **Estado do perfil público** dentro da carteira: se a divulgação foi autorizada, em
      linguagem de criança, dizendo que quem decide é o responsável na App 07, sem ação de
      autorizar ou revogar e sem expor o ato do adulto (`RF-05-50`).
- [x] 2.8 Tela do **ranking**: turma inteira da comunidade, recorte por trilha ou poder, só
      pontos regulares, a própria posição sempre visível e cada colega só por avatar, nick e
      posição (`RF-05-52`, `RF-05-53`, `RF-05-84`, `RN-05-21`).

## 3. Testes

- [x] 3.1 `tests/test_ranking_da_turma.py`: turma inteira contra ranking público filtrado,
      própria posição fora da página, ordenação só por ponto regular, recorte por trilha e por
      poder, 403 de outro papel e de outra comunidade, e a saída sem dado pessoal — os cenários
      de `pontos-niveis-e-badges`.
- [x] 3.2 Estender `tests/test_vitrine.py` com a garantia de que a extração da tarefa 1.1 não
      mudou o ranking público: quem não autorizou segue fora, a numeração não pula e a
      ocorrência de ciclo encerrado segue fora da contagem.
- [x] 3.3 `tests/test_recompensa_conquistada.py`: marco alcançado aparece, não alcançado não
      aparece, entregue mostra a data, ponto de apoio sem lastro não muda a leitura, nenhum
      valor em moedas ou reais e nenhuma recompensa de outra criança — os cenários de
      `recompensa-de-marco`.
- [x] 3.4 Estender `tests/test_autorizacao_vigente.py` com o estado da divulgação em
      `GET /v1/eu`: vigente, sem decisão, revogada por um dos responsáveis, sem revelar quem
      decidiu e sem operação de decidir — os cenários de `consentimento`.
- [x] 3.5 Testes das telas em `apps/app-05-guerreiro/src/`, um arquivo por tela, cobrindo os
      cenários de `area-do-guerreiro`: carteira com as duas contas separadas, catálogo sem ação
      de troca e com o caso vazio, histórico com o preço da época, conquistas sem caminho de
      compra, perfil sem ação de decidir e ranking com a própria posição sempre visível.

## 4. Documentação

- [x] 4.1 Corrigir no PRD-05 §9 a rota do ranking, que a §9 declara **pública** contra o
      `RF-05-84`, o `RN-05-16` e a decisão do ranking interno do documento 09: ela nasce
      autenticada e restrita à comunidade do Guerreiro(a). Não é decisão nova — é o PRD
      alcançando a fonte —, e por isso não entra no documento 09. Atualizar `docs/prds/index.md`
      com a terceira fatia do PRD-05. Nenhum arquivo novo em `docs/`, nenhuma mudança na `nav`
      do `mkdocs.yml` e nenhuma relação nova entre documentos.
