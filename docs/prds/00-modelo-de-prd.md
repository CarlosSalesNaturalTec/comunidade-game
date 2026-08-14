# 00 — Modelo de PRD

> Modelo obrigatório de todo PRD desta pasta. Copie a estrutura, substitua o conteúdo em
> itálico e **não suprima seções**: seção sem conteúdo recebe "não se aplica" com o motivo em
> uma linha. As regras de escrita e o fluxo de decisão estão no `CLAUDE.md`.

## 1. Identificação

| Campo            | Valor                                                           |
| ---------------- | --------------------------------------------------------------- |
| PRD              | _PRD-XX_                                                        |
| Aplicação        | _App NN — nome, ou "—" quando o PRD não tem aplicação dedicada_ |
| Onda             | _1 a 5_                                                         |
| Situação         | _em elicitação / em redação / em revisão / aprovado_            |
| Versão e data    | _v1 — aaaa-mm-dd_                                               |
| Depende de       | _PRDs que precisam estar aprovados antes deste_                 |
| Documentos-fonte | _docs consultados, conforme a linha deste PRD no documento 99_  |

## 2. Contexto e objetivo

_O que este PRD resolve, para quem, e o que muda na operação do Ciclo 01 quando ele estiver
entregue. Máximo três parágrafos._

## 3. Escopo

### 3.1 Dentro do escopo

_Lista do que será construído. Cada item passa pelo teste "isto é necessário para o
Ciclo 01?"._

### 3.2 Fora do escopo

_O que fica para onda seguinte e por quê, em uma linha cada._

## 4. Personas e permissões

| Persona | O que faz nesta aplicação | O que não pode fazer |
| ------- | ------------------------- | -------------------- |

## 5. Jornadas principais

_Cada jornada em passo a passo numerado, do gatilho ao resultado, com os caminhos de exceção
relevantes (falha de identificação, rede fora, recusa de consentimento)._

## 6. Requisitos funcionais

| ID         | Requisito                          | Prioridade              |
| ---------- | ---------------------------------- | ----------------------- |
| `RF-XX-01` | _Enunciado testável, em uma frase_ | _essencial / desejável_ |

_Essencial = sem ele o Ciclo 01 não roda. Desejável = melhora a operação e pode ficar para
depois. Todo requisito precisa ser verificável por alguém que não escreveu o PRD._

## 7. Regras de negócio

| ID         | Regra                | Invariante (doc 99 §6)  | Fonte         |
| ---------- | -------------------- | ----------------------- | ------------- |
| `RN-XX-01` | _Enunciado da regra_ | _nº do invariante ou —_ | _doc e seção_ |

_A regra aqui é **aplicação** do que já está definido nos documentos 01–15. Regra nova só
entra depois de gravada no documento-fonte dela._

## 8. Modelo de dados

_Entidades tocadas, seus atributos essenciais, relacionamentos e o que é imutável. Diagramas
em bloco ` ```text `. Entidade nova precisa constar também do PRD-01._

## 9. Contratos de API

_Rotas expostas ou consumidas: método, caminho, autenticação exigida (pública × autenticada),
payload de entrada e de saída, e erros previstos._

## 10. Requisitos não funcionais

_Web App responsivo Mobile First; comportamento com rede instável; uso em aparelho
compartilhado do ponto de apoio; desempenho em celular modesto; acessibilidade no piso do
documento 15 — WCAG 2.2 AA — e linguagem simples; idioma pt-BR; código aberto._

## 11. LGPD e proteção da criança

| Dado coletado | Finalidade | Base legal | Retenção | Quem acessa |
| ------------- | ---------- | ---------- | -------- | ----------- |

_Descrever também: consentimento exigido e onde é registrado; alternativa equivalente para
quem recusar; aviso visível na aplicação sobre o que se coleta; o que a aplicação faz com
pedido de acesso, correção ou exclusão._

## 12. Critérios de aceite e métricas

_Critérios de aceite verificáveis, um por requisito essencial. Quando o PRD sustentar uma das
hipóteses do Ciclo 01 (documento 10), indicar qual e o que ele passa a medir._

## 13. Decisões tomadas neste PRD

| Decisão | Gravada em | Linha do doc 09 |
| ------- | ---------- | --------------- |

_Toda decisão nova é gravada primeiro no documento-fonte e movida para "Já decididos" no
documento 09. Esta tabela é o comprovante, não o registro normativo._

## 14. Pendências que permanecem

_O que ficou em aberto, o que trava e quando precisa de resposta. Cada item também entra na
tabela de decisões pendentes do documento 09._

## 15. Rastreabilidade

| Requisito  | Origem                        |
| ---------- | ----------------------------- |
| `RF-XX-01` | _documento e seção de origem_ |
