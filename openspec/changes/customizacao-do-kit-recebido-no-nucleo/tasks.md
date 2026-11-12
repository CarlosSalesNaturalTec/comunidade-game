# Tasks

## 1. Kit apresentado no prático

- [ ] 1.1 Acrescentar `desafio_pratico_kit_id` a `Missao` e aceitar `kit_apresentado_id` em
      `declarar_desafio_de_desbloqueio` e na rota dela: só no prático, recompensa da mesma
      trilha, substituída ao redeclarar e apagada ao virar quiz (`RF-09-141`); verificar pelos
      testes da 1.3.
- [ ] 1.2 Devolver `kit_apresentado` (identificador da recompensa e nome do tipo de recurso)
      dentro de `desafio_de_desbloqueio` em todas as leituras que já servem os três campos do
      prático, nulo sem kit e no quiz (`RF-09-141`); verificar pelos testes da 1.3.
- [ ] 1.3 Em `tests/test_desbloqueio_da_missao.py`, cobrir os cenários da declaração e da
      leitura do kit: declarado, opcional, de outra trilha (422), no quiz (422), apagado ao
      virar quiz, e a leitura do Mestre autor e do percurso (`RF-09-141`).

## 2. Modelo e migração do cuidado com o bem

- [ ] 2.1 Criar o módulo `cuidado_do_bem/` com `RegistroDeCustomizacao` (situação, descrição,
      mídia, motivo, aula, julgamento, `ComAutoria`, índice único parcial do pendente por
      entrega) e `PontuacaoDoBem` (fonte, unicidade em aula × entrega), registrado no
      `principal.py` (`RF-01-84`, `RF-01-85`, `RF-01-87`, `RN-01-66`); verificar que o
      metadata cria as duas tabelas na suíte.
- [ ] 2.2 Escrever a revisão Alembic da coluna da missão, das duas tabelas, dos enums, da
      unicidade e do índice parcial, com `downgrade`; verificar `upgrade` e `downgrade` contra
      o banco de teste.

## 3. Registro, envio e cancelamento da customização

- [ ] 3.1 Implementar a abertura derivada (entrega do Guerreiro(a) + prático aprovado que
      declara a recompensa) e o "último aprovado" — registro aprovado mais recente ou a
      comprovação do prático (`RF-01-84`, `RF-09-141`).
- [ ] 3.2 Implementar o registro pelo Guerreiro(a) (`POST /eu/customizacoes`) e a captura pelo
      Mestre da aula (`POST /aulas/{id}/customizacoes`), com descrição obrigatória, um pendente
      por kit e presença exigida na captura (`RF-01-84`, `RF-04-80`, `RF-04-82`, `RF-05-102`).
- [ ] 3.3 Implementar a sessão de envio, a confirmação e a leitura dos bytes da mídia, só imagem
      e vídeo, com o teto do tipo, enviando quem registrou e lendo o dono e o Mestre da
      comunidade (`RF-01-84`, `RF-04-81`).
- [ ] 3.4 Implementar `GET /eu/customizacoes` (kits abertos com o último aprovado, registros com
      situação e motivo) e o cancelamento do pendente (`RF-05-103`, `RF-01-86`).
- [ ] 3.5 Em `tests/test_customizacao_do_kit.py`, cobrir os cenários da abertura, do registro,
      da captura, do envio, da mídia, do pendente único, do reenvio após reprovação, da leitura
      própria e do cancelamento, da spec `customizacao-do-kit`.

## 4. Julgamento, conservação e fila do encontro

- [ ] 4.1 Implementar o julgamento (`POST /customizacoes/{id}/julgamento`): Mestre vinculado à
      comunidade da aula, presença não anulada, mídia confirmada, motivo na reprovação; a
      aprovação grava a `PontuacaoDoBem` e credita 1 ponto extra na mesma transação
      (`RF-01-85`, `RF-04-82`, `RF-04-83`, `RN-01-66`).
- [ ] 4.2 Implementar a validação da conservação (`POST /aulas/{id}/conservacoes`) sobre
      entrega de recompensa de marco do próprio Guerreiro(a), gravando a `PontuacaoDoBem` e
      creditando 1 ponto extra, com a recusa nomeando o caminho já usado (`RF-01-87`,
      `RF-09-113`, `RF-04-84`, `RN-01-66`, `RN-09-62`).
- [ ] 4.3 Implementar `GET /aulas/{id}/fila-do-cuidado` com os presentes, os bens recebidos, o
      que já pontuou na aula, a abertura, o pendente e o último aprovado (`RF-04-81`,
      `RF-04-84`).
- [ ] 4.4 Em `tests/test_conservacao_do_bem_recebido.py` e no grupo de julgamento de
      `tests/test_customizacao_do_kit.py`, cobrir os cenários do julgamento, da validação, da
      exclusão entre as duas fontes (inclusive pelo banco), dos três bens no mesmo encontro e da
      fila; e, em `tests/test_ponto_extra.py`, os créditos de 1 extra sem ponto regular.

## 5. Fim do ciclo e acervo público

- [ ] 5.1 Acrescentar a `encerrar_ciclo` a expiração dos pendentes e `customizacoes_expiradas`
      à resposta; cobrir em `tests/test_ciclo.py` o pendente que expira e o julgado que fica
      (`RF-01-86`).
- [ ] 5.2 Acrescentar a terceira fonte ao acervo público — `FonteDoAcervo.customizacao_do_kit`,
      `condicoes_de_customizacao_publica`, a junção na paginação — e a rota pública da mídia;
      cobrir em `tests/test_vitrine.py` a aparição, o portão (reprovado, sem autorização), a
      ordem das três fontes e o 404 da mídia (`RF-03-88`).

## 6. Documentação

- [ ] 6.1 Marcar a fatia "Customização do kit recebido no núcleo" do bloco PRD-01 como
      implementada no `openspec/cronograma-de-fatias.md`, com o slug. As decisões já estão nos
      documentos 11, 02, 09 e 99 e nos PRDs; `docs/prds/index.md` não muda.
