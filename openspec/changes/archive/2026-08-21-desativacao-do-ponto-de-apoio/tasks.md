## 1. Modelo e migração

- [x] 1.1 Acrescentar a `PontoDeApoio` o **motivo** e a **autoria da última mudança de estado**
      em `backend/src/nucleo/pontos_de_apoio/modelo.py`, e a referência mútua entre os dois
      lançamentos de uma transferência em `backend/src/nucleo/livro_razao/modelo.py`, com a
      migração Alembic; verificar que `alembic upgrade head` sobe limpo (`RF-07-47`,
      `RF-07-19`)

## 2. Transferência no livro-razão

- [x] 2.1 Em `backend/src/nucleo/livro_razao/regra.py`, gravar a transferência como par débito
      e crédito na mesma operação, com motivo, autoria e momento comuns, recusando com 422
      origem igual ao destino, quantidade não positiva, saldo insuficiente na origem e destino
      inativo (`RF-07-19`, `RN-07-15`, `RN-07-04`, `RN-07-33`)
- [x] 2.2 Expor a rota de transferência, de Admin, com 403 para outro papel; verificar que o
      saldo derivado dos dois pontos de apoio acompanha o movimento

## 3. Desativação e reativação

- [x] 3.1 Em `backend/src/nucleo/pontos_de_apoio/regra.py`, escrever desativar e reativar com
      motivo obrigatório, recusando 422 para ponto já no estado pedido, e conferir os dois
      bloqueios: **aula futura**, informando quantas, e **saldo remanescente**, informando os
      tipos (`RF-07-47`, `RN-07-01`, `RN-07-33`)
- [x] 3.2 Expor `POST /v1/pontos-de-apoio/{id}/desativacao` e a rota de reativação, ambas de
      Admin, conforme o desenho; verificar que aula passada e lançamento continuam apontando o
      ponto desativado
- [x] 3.3 Em `backend/src/nucleo/aulas/regra.py`, recusar com 422 o agendamento que declare
      ponto de apoio inativo (`RF-07-47`, `RN-07-33`, `RF-02-31`)

## 4. Telas da App 03

- [x] 4.1 Acrescentar a `apps/app-03-gestao/src/pontos-de-apoio/` as ações de desativar e
      reativar com motivo obrigatório, oferecidas só ao Admin, e a distinção entre ativo e
      inativo na lista (`RF-07-47`, `RN-02-21`)
- [x] 4.2 Apresentar a recusa em linguagem simples — quantas aulas prendem, quais tipos têm
      saldo — com o caminho da transferência na recusa por saldo (`RN-07-01`, `RN-07-15`)
- [x] 4.3 Acrescentar a tela de transferência, mostrando o saldo disponível na origem, sem
      oferecer destino inativo nem a própria origem, e barrando quantidade acima do saldo antes
      de enviar (`RF-07-19`, `RN-07-33`)

## 5. Testes

- [x] 5.1 Em `backend/tests/test_lancamento.py`, cobrir os cenários do delta de `livro-razao`:
      transferência gravando o par, saldo dos dois pontos acompanhando, recusa por saldo
      insuficiente, origem igual ao destino, destino inativo, 403 do Mestre e a transferência
      que não usa ajuste
- [x] 5.2 Em `backend/tests/test_ponto_de_apoio.py`, cobrir os cenários do delta de
      `ponto-de-apoio`: desativar, reativar, 403 do Mestre, recusa sem motivo, aula passada que
      continua apontando, os três cenários do bloqueio por aula futura e os três do bloqueio
      por saldo
- [x] 5.3 Em `backend/tests/test_aula.py`, cobrir o cenário novo do delta de `aula-e-presenca`:
      agendamento em ponto de apoio inativo recusado com 422
- [x] 5.4 Em `apps/app-03-gestao/src/pontos-de-apoio/`, cobrir os cenários do delta de
      `aplicacao-de-gestao`: desativar com motivo, inativo que continua na lista, ação não
      oferecida ao Mestre, recusa sem motivo, as duas recusas explicadas, e os três cenários da
      transferência

## 6. Documentação

- [x] 6.1 Gravar a decisão nova nos documentos-fonte e nos PRDs, no mesmo PR: documento 05 §2
      (o Admin desativa e reativa; a desativação é bloqueada por aula futura; o saldo sai por
      transferência), documento 09 (mover "Desativação de ponto de apoio" para os já
      decididos), PRD-07 §8 e PRD-02, que recebem o requisito da operação, e
      `docs/prds/index.md`
