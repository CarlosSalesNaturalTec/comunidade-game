## Purpose

O fim do vínculo do Guerreiro(a) com o projeto: o marco que inicia os prazos de guarda dos dados
dele. Existe por ato de Admin e, sem depender de ninguém, pela varredura dos 12 meses sem
atividade registrada — e é ele que dispara o apagamento do _template_ biométrico.

## ADDED Requirements

### Requirement: O Admin encerra o vínculo do Guerreiro(a) com o projeto

O núcleo SHALL expor ao **Admin em sessão** o ato que encerra o vínculo de um Guerreiro(a) com o
projeto, gravando **quem encerrou**, a **data e hora com fuso** e o **motivo** declarado. O
registro SHALL ser **somente inserção**: nenhuma rota SHALL editá-lo nem apagá-lo. Persona de
qualquer outro papel SHALL receber **403**, e o vínculo já encerrado SHALL recusar segundo
encerramento com **409**. (`RF-13-44`, decisão do fundador, 2026-09-01, documento 09 §1)

O fim do vínculo é **marco de prazo de guarda**, e NEVER SHALL, por si só, apagar resultado,
ponto, registro de território ou qualquer outro dado do Guerreiro(a): o que ele dispara é o
apagamento do _template_ biométrico, e nada mais. O Guerreiro(a) NEVER SHALL desaparecer das
séries e dos lançamentos que já gravou.

#### Scenario: O Admin encerra o vínculo com motivo

- **WHEN** um Admin em sessão encerra o vínculo de um Guerreiro(a) com o projeto
- **THEN** o núcleo grava o fim do vínculo com quem encerrou, o motivo e a data e hora com fuso

#### Scenario: Mestre não encerra vínculo

- **WHEN** um Mestre, um responsável ou o próprio Guerreiro(a) tenta encerrar o vínculo
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Vínculo já encerrado não se encerra de novo

- **WHEN** um Admin encerra o vínculo de um Guerreiro(a) que já o tem encerrado
- **THEN** o núcleo responde 409 e o registro original permanece como estava

#### Scenario: O fim do vínculo não apaga o que a criança realizou

- **WHEN** o vínculo de um Guerreiro(a) é encerrado
- **THEN** os registros de coleta, resultados e lançamentos dele seguem gravados e apontando
  para ele

### Requirement: A varredura encerra o vínculo de quem completou 12 meses sem atividade

O núcleo SHALL encerrar, **sem depender de ato de ninguém**, o vínculo do Guerreiro(a) que
completou **12 meses** sem nenhuma atividade registrada. Conta como atividade registrada a mais
recente entre **presença em aula**, **resultado de atividade lançado** e **registro de coleta do
território**; nenhum outro registro SHALL segurar o vínculo. O fim gravado pela varredura SHALL
declarar que veio dela — não de um Admin —, com a mesma data e hora com fuso dos demais.
(`RF-13-44`, decisão do fundador, 2026-09-01, documento 09 §1, documento 03 §12.2)

Guerreiro(a) sem nenhuma atividade registrada SHALL contar os 12 meses a partir da **criação da
persona**. A varredura NEVER SHALL encerrar de novo um vínculo já encerrado, e SHALL ser
**repetível**: rodar duas vezes no mesmo dia produz o mesmo resultado da primeira.

#### Scenario: Doze meses sem nenhum dos três registros encerram o vínculo

- **WHEN** a varredura roda e encontra um Guerreiro(a) cuja presença, resultado e coleta mais
  recentes são todos anteriores a 12 meses
- **THEN** o núcleo grava o fim do vínculo declarando que veio da varredura

#### Scenario: Uma coleta recente segura o vínculo

- **WHEN** a varredura roda sobre um Guerreiro(a) sem presença nem resultado há mais de 12
  meses, mas com um registro de coleta de dois meses atrás
- **THEN** o vínculo dele permanece aberto e nada é gravado

#### Scenario: Persona nova não é encerrada

- **WHEN** a varredura roda sobre um Guerreiro(a) criado há um mês e ainda sem atividade
- **THEN** o vínculo dele permanece aberto

#### Scenario: A varredura repetida não grava duas vezes

- **WHEN** a varredura roda duas vezes seguidas
- **THEN** o vínculo encerrado na primeira não recebe segundo registro na segunda

### Requirement: O comando de manutenção é quem cumpre os prazos

O núcleo SHALL oferecer um **comando de manutenção**, executável fora do ciclo de requisição,
que a cada execução **encerra os vínculos vencidos** pela varredura dos 12 meses e **apaga os
_templates_ biométricos** cuja data de apagamento já passou. Nenhuma rota HTTP SHALL disparar o
apagamento, e nenhuma tela SHALL depender de alguém rodar o comando para exibir o estado
correto. O comando SHALL relatar o que fez — quantos vínculos encerrou e quantos _templates_
apagou — e SHALL ser **repetível** sem efeito duplicado. (decisão do fundador, 2026-09-01,
documento 09 §1)

#### Scenario: O comando encerra e apaga o que venceu

- **WHEN** o comando de manutenção roda com um vínculo vencido pelos 12 meses e um _template_
  com data de apagamento já passada
- **THEN** o vínculo é encerrado, o _template_ é apagado, e o comando relata os dois

#### Scenario: O comando não toca no que ainda não venceu

- **WHEN** o comando roda com um _template_ cuja data de apagamento é amanhã
- **THEN** o _template_ permanece gravado e o comando relata que nada apagou

#### Scenario: Rodar duas vezes não muda o resultado

- **WHEN** o comando roda duas vezes seguidas
- **THEN** a segunda execução não encerra vínculo nem apaga _template_ de novo
