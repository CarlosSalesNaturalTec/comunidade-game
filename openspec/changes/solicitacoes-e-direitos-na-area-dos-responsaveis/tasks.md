## 1. Modelo e migração

- [ ] 1.1 Criar `nucleo/vinculo_do_guerreiro/modelo.py` com `FimDeVinculo` — `guerreiro_id`
  único, `origem` (`admin` ou `varredura`), `encerrado_por` nulo na varredura, `motivo` e
  `momento` com fuso —, somente inserção como `Consentimento` (`RF-13-44`).
- [ ] 1.2 Criar `ApagamentoDeTemplate` em `nucleo/biometria/modelo.py` — `guerreiro_id` único,
  `gatilho`, `apagar_em`, `criado_em` — e acrescentar `apagamento` a `NaturezaDoAcesso`
  (`RF-13-43`, `RF-13-44`, `RN-13-22`).
- [ ] 1.3 Escrever a migração Alembic das duas tabelas e do valor novo da natureza, com o mesmo
  _trigger_ de somente inserção que `consentimento` e `acesso_ao_template` já usam.

## 2. Apagamento do _template_ no núcleo

- [ ] 2.1 Em `nucleo/biometria/regra.py`, `marcar_apagamento(guerreiro, gatilho)` — 5 dias para
  a recusa e para o desfecho aceito de exclusão, 30 dias para o fim do vínculo; sem _template_
  gravado não marca e não falha; havendo marca, não substitui nem adia (`RF-13-43`, `RF-13-44`,
  `RN-13-22`).
- [ ] 2.2 Em `nucleo/biometria/regra.py`, `apagar_templates_vencidos()` — remove a `Credencial`
  de tipo `biometria`, grava o acesso de natureza `apagamento` sem descritor, preserva a
  auditoria anterior e é repetível (`RF-13-43`, `RN-01-14`).
- [ ] 2.3 Conferir que nenhuma rota cancela a marca nem apaga fora do comando: a única saída é
  `apagar_templates_vencidos` (`RN-13-22`, decisão do fundador, 2026-09-01).

## 3. Fim do vínculo e comando de manutenção

- [ ] 3.1 Em `nucleo/vinculo_do_guerreiro/regra.py`, `encerrar_vinculo` (409 no já encerrado) e
  `varrer_vinculos_vencidos()` — 12 meses contados da mais recente entre presença, resultado e
  coleta, ou da criação da persona quando não houver nenhuma —, marcando o apagamento em 30 dias
  (`RF-13-44`).
- [ ] 3.2 Expor `POST /v1/guerreiros/{id}/fim-de-vinculo` em `rotas.py`, restrita ao Admin por
  `Operacao.tudo`, com motivo obrigatório e 403 para os demais papéis (`RF-13-44`).
- [ ] 3.3 Criar `nucleo/manutencao.py`, chamado por `python -m nucleo.manutencao`: encerra os
  vínculos vencidos, depois apaga os _templates_ vencidos, relata os dois números e é repetível
  sem efeito duplicado (`RF-13-43`, `RF-13-44`).

## 4. Recusa da biometria e leitura do estado

- [ ] 4.1 Em `nucleo/consentimentos/regra.py`, a recusa da biometria pelo responsável: exige
  vínculo vigente (403 sem ele), grava `tipo=biometria`, `decisao=nega`, origem própria e a
  versão vigente do termo, recusa a concessão por essa via e é idempotente na recusa repetida
  (`RF-13-27`, `RN-13-06`, `RN-13-10`).
- [ ] 4.2 Expor `POST /v1/eu/guerreiros/{id}/biometria/recusa`, que marca o apagamento em 5 dias
  no mesmo ato e devolve a data — sem data quando não há _template_ (`RF-13-27`, `RF-13-43`).
- [ ] 4.3 Expor `GET /v1/eu/guerreiros/{id}/biometria` com o estado da captura, a decisão mais
  recente do termo, e a data e o gatilho do apagamento quando houver; nunca o descritor, nunca
  criança não vinculada (`RF-13-27`, `RF-13-44`, `RN-13-04`).
- [ ] 4.4 Em `nucleo/solicitacoes_do_responsavel/regra.py`, ligar o desfecho **aceito** do tipo
  **exclusão** à marca de 5 dias, sem tocar em registro de território nem em qualquer outro dado
  (`RF-13-43`, `RN-13-12`, `RN-13-22`).

## 5. Telas da App 07

- [ ] 5.1 Criar `src/solicitacoes/api.ts` e `src/biometria/api.ts` sobre `POST /v1/solicitacoes`,
  `GET /v1/eu/solicitacoes` e as duas rotas novas da biometria, sem calcular prazo nem atraso no
  cliente (`RF-13-22`, `RF-13-25`, `RF-13-27`).
- [ ] 5.2 Criar `TelaDeSolicitacoes.tsx`: abertura nos quatro tipos sobre o vinculado escolhido,
  protocolo e prazo devolvidos na confirmação, explicação da duplicata em aberto, e a lista das
  próprias com situação, prazo, marca de em atraso e o desfecho com a data (`RF-13-22`,
  `RF-13-24`, `RF-13-25`, `RF-13-26`, `RN-13-13`).
- [ ] 5.3 No mesmo componente, o limite declarado antes do aceite da exclusão — território
  despersonalizado e não apagado, _template_ apagado como exceção —, apresentado antes de a
  confirmação ficar disponível e só nesse tipo (`RF-13-23`, `RN-13-12`, `RN-13-22`).
- [ ] 5.4 Criar `TelaDaImagemDoOnboarding.tsx`: termo próprio e finalidade da imagem antes do
  ato, recusa sem caminho de concessão, alternativa equivalente dita no mesmo ato, e o aviso do
  apagamento com a data, o gatilho e o que significa a volta (`RF-13-27`, `RF-13-28`, `RF-13-43`,
  `RF-13-44`, `RN-13-09`, `RN-13-15`).
- [ ] 5.5 Acrescentar as abas "Solicitações" e "Imagem do onboarding" em `TelaDeVinculados.tsx`,
  mantendo a aba escolhida ao trocar de vinculado (`RF-13-05`, `RF-13-22`, `RF-13-27`).

## 6. Testes

- [ ] 6.1 `tests/test_apagamento_de_template.py`: os três gatilhos e seus prazos, Guerreiro(a)
  sem _template_, desfecho recusado e de outro tipo, marca que não se cancela nem se adia,
  apagamento que destrói o cifrado e audita sem descritor, auditoria anterior preservada,
  comparação de login que deixa de conferir e participação que segue igual.
- [ ] 6.2 `tests/test_fim_de_vinculo.py`: ato de Admin com motivo, 403 dos demais papéis, 409 no
  já encerrado, o que a varredura encerra e o que ela segura (coleta recente, persona nova),
  repetição sem segundo registro e o que o fim do vínculo não apaga.
- [ ] 6.3 `tests/test_manutencao.py`: o comando encerra e apaga o que venceu, não toca no que
  ainda não venceu, relata os números e é repetível.
- [ ] 6.4 `tests/test_recusa_de_biometria.py`: recusa gravada com origem e versão do termo,
  concessão recusada pela rota, 403 sem vínculo e de outro papel, recusa repetida idempotente,
  autorização única intacta, data devolvida e leitura do estado sem descritor.
- [ ] 6.5 `apps/app-07-responsaveis/src/solicitacoes/solicitacoes.test.tsx` e
  `src/biometria/biometria.test.tsx`: abertura com protocolo e prazo, duplicata explicada, limite
  antes do aceite e ausente nos outros tipos, lista com atraso vindo do núcleo, recusa sem
  concessão, alternativa equivalente e aviso do apagamento com a data.

## 7. Documentação

- [ ] 7.1 Gravar no documento 09 §1 as seis decisões do fundador de 2026-09-01 — marco do fim do
  vínculo por ato de Admin, comando de manutenção como executor dos prazos, recusa da biometria
  que apaga em 5 dias, execução da despersonalização adiada para o Ciclo 02, os três registros
  que contam como atividade nos 12 meses e a marca que não se cancela — e refletir no documento
  03 §§3.3 e 12.2 o que mudou. Registrar como pendências novas a **tela da App 03 que encerra o
  vínculo** e a **volta do Guerreiro(a) que teve o vínculo encerrado**.
- [ ] 7.2 Atualizar o PRD-13: a §9 com as três rotas novas, a §3.2 para distinguir a concessão
  da biometria (fora do escopo) da recusa que a `RF-13-27` dá à App 07, e as §§13 e 14 com o que
  foi decidido e o que saiu da lista de pendências.
- [ ] 7.3 Marcar a fatia 4 como implementada em `openspec/cronograma-de-fatias.md`, com o slug
  desta change, anotando que a execução da `RN-13-12` foi para o Ciclo 02; atualizar
  `docs/prds/index.md` só se a situação do PRD-13 mudar. Nenhum arquivo novo em `docs/`, e por
  isso nenhuma entrada nova na `nav` do `mkdocs.yml`.
