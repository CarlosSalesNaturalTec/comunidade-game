## ADDED Requirements

### Requirement: O Guerreiro(a) lê as duas contas de ponto extra, e ninguém as lê por ele

O núcleo SHALL devolver ao **Guerreiro(a) em sessão** as suas duas contas de ponto extra — o
**acumulado** e o **saldo disponível** —, numa rota que NEVER SHALL receber identificador de
persona: ela alcança apenas quem está autenticado nela. Persona de papel **Mestre**, **Admin**,
**Apoiador** ou **responsável** SHALL receber **403**: nenhum adulto lê o saldo de uma criança,
nem o Mestre que entrega o item da troca.

Guerreiro(a) que ainda não recebeu ponto extra algum SHALL receber as duas contas em **zero**,
e não um erro — quem nunca ganhou tem saldo, e ele é nenhum.

A leitura NEVER SHALL alcançar o contrato de leitura dos jogos, que segue devolvendo apenas o
**acumulado**, sem persona e sem sessão: o saldo disponível continua fora dele, e trocar por
recompensa avulsa continua sem enfraquecer o personagem. (`RF-04-51`, `RF-05-82`, `RF-01-22`,
`RN-01-39`, `RN-01-40`, `RN-01-41`, invariantes 8 e 23)

#### Scenario: O Guerreiro(a) lê as próprias contas

- **WHEN** um Guerreiro(a) em sessão consulta os seus pontos extras
- **THEN** o núcleo devolve o acumulado e o saldo disponível dele, separados

#### Scenario: Guerreiro(a) sem ponto extra tem saldo zero

- **WHEN** um Guerreiro(a) que nunca recebeu ponto extra consulta os seus pontos extras
- **THEN** o núcleo devolve acumulado zero e saldo disponível zero, sem erro

#### Scenario: O Mestre não lê o saldo de uma criança

- **WHEN** um Mestre em sessão tenta consultar os pontos extras por essa rota
- **THEN** o núcleo responde 403 e nada do saldo é devolvido

#### Scenario: O Admin não lê o saldo por esta rota

- **WHEN** um Admin em sessão tenta consultar os pontos extras por essa rota
- **THEN** o núcleo responde 403 e nada do saldo é devolvido

#### Scenario: A rota não aponta para outra criança

- **WHEN** um Guerreiro(a) em sessão tenta alcançar o saldo de outro Guerreiro(a)
- **THEN** não há como fazê-lo: a rota não recebe identificador de persona e devolve sempre as
  contas de quem está em sessão

#### Scenario: O contrato dos jogos segue sem o saldo

- **WHEN** o App 04 lê o progresso de um Guerreiro(a) para montar o personagem
- **THEN** a resposta traz o acumulado de pontos extras e NÃO traz o saldo disponível
