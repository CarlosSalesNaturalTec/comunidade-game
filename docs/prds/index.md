# PRDs — Documentos de Requisitos de Produto

Esta pasta reúne os **PRDs** (_Product Requirements Documents_) do Comunidade Game, derivados
do documento 08 e escritos um a um, na ordem das ondas abaixo. Cada PRD segue o
[modelo de PRD](00-modelo-de-prd.md) e vale para o **Ciclo 01** (Guerreira Zeferina,
ago–dez/2026).

O PRD é artefato **derivado**: ele aplica as regras dos documentos 01–14 e não cria regra
própria. As regras de escrita, o fluxo de decisão das pendências e o processo de entrega estão
no `CLAUDE.md`, na raiz do repositório; o mapa de dependências entre PRDs está no documento 99.

## Situação da esteira

| PRD                                       | Assunto                                | Aplicação | Onda | Situação |
| ----------------------------------------- | -------------------------------------- | --------- | ---- | -------- |
| [PRD-08](prd-08-comunidades-virtuais.md)  | Comunidades Virtuais e território      | —         | 1    | aprovado |
| [PRD-07](prd-07-economia-e-ledger.md)     | Economia de recursos e ledger          | —         | 1    | aprovado |
| [PRD-01](prd-01-backend-api.md)           | Backend API (núcleo)                   | —         | 1    | aprovado |
| [PRD-02](prd-02-frontend-de-gestao.md)    | Frontend de gestão                     | App 03    | 2    | aprovado |
| [PRD-04](prd-04-aula-presencial.md)       | Aula presencial (onboarding e trilhas) | App 01    | 2    | aprovado |
| [PRD-09](prd-09-area-do-mestre.md)        | Área do Mestre (autoria e operação)    | App 09    | 3    | aprovado |
| [PRD-05](prd-05-area-do-guerreiro.md)     | Área do Guerreiro(a)                   | App 05    | 3    | aprovado |
| [PRD-13](prd-13-area-dos-responsaveis.md) | Área dos pais e responsáveis           | App 07    | 4    | aprovado |
| [PRD-03](prd-03-vitrine-publica.md)       | Vitrine pública                        | App 06    | 4    | aprovado |
| [PRD-14](prd-14-area-do-apoiador.md)      | Área do Apoiador                       | App 08    | 5    | aprovado |
| [PRD-10](prd-10-batalhas.md)              | Batalhas e eventos presenciais         | —         | 5    | aprovado |
| [PRD-12](prd-12-jogo-em-javascript.md)    | App 04: Jogo em JavaScript             | App 04    | 5    | aprovado |
| [PRD-11](prd-11-personalizacao-por-ia.md) | Personalização por IA                  | —         | 5    | aprovado |

Situações possíveis: **não iniciado**, **em elicitação**, **em redação**, **em revisão** e
**aprovado**. O link para o documento aparece nesta tabela quando ele entra na pasta.

A coluna **Onda** é a ordem em que os PRDs foram **escritos**, e o motivo de cada onda está
no documento 08. Ela não é a ordem em que o código entra: essa está no documento 99 §9.

O **PRD-06 — Assistente por voz e Modo Ouvinte** foi extinto: o App 02 passou a fazer parte do
App 01 e o Modo Ouvinte saiu do produto. O que restou dele está no PRD-04.
