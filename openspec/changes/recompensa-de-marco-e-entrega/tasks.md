## 1. Modelo

- [ ] 1.1 Criar `backend/src/nucleo/recompensas_de_marco/modelo.py` com `RecompensaDeMarco`
      (trilha, missão do marco, tipo de recurso, quantidade, Mestre autor, data) e
      `EntregaDeRecompensa` (recompensa de marco, Guerreiro(a), ponto de apoio, Mestre que
      entregou, lançamento emitido, data), sem situação de entrega na primeira e sem ponto de
      apoio nela (`RF-09-71`, `RF-07-13`)
- [ ] 1.2 Registrar as duas tabelas na criação do schema, seguindo o que `trocas/` e
      `patrimonio/` já fazem, e conferir que nenhuma coluna nova é exigida de `Lancamento`

## 2. Declaração do marco

- [ ] 2.1 Em `recompensas_de_marco/regra.py`, escrever `declarar_recompensa_de_marco`: só o
      Mestre autor da trilha grava; marco que não seja missão da trilha é recusado com 422;
      preço ou contrapartida em qualquer moeda é recusado (`RF-09-71`, `RN-09-26`, `RN-09-39`)
- [ ] 2.2 Escrever a leitura das recompensas de marco de uma trilha, para a gestão (`RF-09-71`)

## 3. Entrega e baixa

- [ ] 3.1 Tornar pública em `pontuacao/regra.py` a derivação das missões concluídas por
      Guerreiro(a) numa trilha, hoje `_missoes_concluidas_pelo_guerreiro`, sem mudar o que ela
      calcula (`RF-07-13`)
- [ ] 3.2 Escrever `_validar_entrega` com as cinco recusas na ordem do delta — durável, lastro
      reverificado no ponto de apoio da entrega, quantidade esgotada pela contagem de entregas,
      Mestre não vinculado à comunidade do Guerreiro(a), marco não alcançado —, todas antes de
      qualquer escrita e cada uma dizendo qual recusou (`RF-07-13`, `RN-07-07`, `RN-09-26`,
      invariante 9)
- [ ] 3.3 Escrever `registrar_entrega` como operação atômica única: grava a entrega e emite o
      lançamento de débito da quantidade, no ponto de apoio da entrega, valorado pela vigência
      corrente e **sem aula**; falhando qualquer parte, nada persiste; nenhum ponto regular nem
      extra do Guerreiro(a) é tocado (`RF-07-13`, `RN-07-08`, `RN-07-36`, `RN-07-15`)
- [ ] 3.4 Escrever `listar_entregas` filtrada por persona — o Guerreiro(a) lê as próprias, o
      Mestre e o Admin as da comunidade —, sem valor em moedas nem em reais na saída
      (`RF-07-13`, `RN-07-05`, invariante 16)

## 4. Rotas

- [ ] 4.1 Criar `recompensas_de_marco/rotas.py` com `POST` e `GET`
      `/v1/trilhas/{id}/recompensas-de-marco`, `POST
      /v1/recompensas-de-marco/{id}/entregas` e `GET /v1/entregas`, com a exigência de
      credencial de persona de cada uma e a recusa do Admin na confirmação da entrega
      (`RF-09-76`, `RF-02-50`, `RF-02-51`)
- [ ] 4.2 Registrar o roteador em `principal.py` por `incluir_roteador_de_dados`, como os de
      `trocas` e `patrimonio`

## 5. Testes

- [ ] 5.1 `backend/tests/test_recompensa_de_marco.py` — declaração: Mestre autor grava; Mestre
      não autor é recusado; marco que não é missão é recusado; declaração com preço é recusada
      (`RF-09-71`, `RN-09-26`, `RN-09-39`)
- [ ] 5.2 `backend/tests/test_entrega_de_recompensa.py` — as cinco recusas, uma a uma, e o
      cenário de que a recusa não move nada: nem entrega, nem lançamento, nem saldo
      (`RF-07-13`, `RN-07-07`, invariante 9)
- [ ] 5.3 No mesmo arquivo, a entrega feliz: grava a entrega, o saldo do tipo naquele ponto de
      apoio cai pela quantidade, o débito é gravado sem aula, e o ponto regular e o extra do
      Guerreiro(a) — disponível e acumulado — seguem intactos. Inclui o critério de aceite do
      PRD-07 §12 de que a perda da recompensa entregue gera **nenhum** débito (`RF-07-13`,
      `RN-07-08`, `RN-07-09`, `RN-02-15`, `RN-02-16`)
- [ ] 5.4 No mesmo arquivo, a atomicidade e o histórico: falha no lançamento desfaz a entrega;
      duas entregas da mesma recompensa convivem sem situação própria; a leitura por persona
      não traz moedas nem reais (`RF-07-13`, `RN-07-05`)
- [ ] 5.5 Em `backend/tests/test_prestacao_de_contas.py`, o cenário de que a entrega fica fora
      do consumo por aula: aula com baixa e entrega no mesmo encontro somam só o débito da
      baixa em `GET /prestacao-de-contas/aulas` (`RF-07-16`, `RN-07-15`)

## 6. Documentação

- [ ] 6.1 Gravar as quatro decisões novas no documento 02 §8.1 — quem confirma a entrega, o
      lastro reverificado no ato, a migração da garantia de lastro da publicação para a
      entrega e a verificação do marco — e as linhas correspondentes no documento 09 §1
      "Já decididos", incluindo a resolução do conflito PRD-02 × PRD-09
- [ ] 6.2 Aplicar as correções nos PRDs: PRD-02 (`RF-02-50` e `RF-02-51` passam a mostrar),
      PRD-09 §§6, 7 e 8 (`RF-09-72` e `RN-09-27` sem lastro na publicação; a entrega como
      entidade própria e sem ponto de apoio na `RecompensaDeMarco`), PRD-07 §6 (`RF-07-13`
      ganha o ator) e §8 (a entrega entra entre os débitos que não declaram aula)
- [ ] 6.3 Atualizar `docs/prds/index.md` com a décima fatia do PRD-07 e o que resta dele, e o
      documento 99 §8, porque a relação PRD-07 × PRD-09 muda. Nenhum arquivo novo em `docs/`,
      logo a `nav` do `mkdocs.yml` não muda
