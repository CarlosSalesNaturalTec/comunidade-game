# Design — remoção do template da missão

## Context

O template nasceu na fatia 12 (`2026-08-30-template-da-missao-recompensa-e-duplicacao-da-trilha`)
e foi para o DeepSeek em `2026-09-10-template-da-missao-no-deepseek`. Hoje ele ocupa:

- **núcleo** — `backend/src/nucleo/template_de_missao/` (porta, adaptadores local e nuvem,
  regra das lacunas, modelo `SugestaoDeEstrutura`, duas rotas), registrado em `principal.py` e
  `modelos.py`; a coluna `poder.tecnico` e a tabela `sugestao_de_estrutura` nasceram juntas na
  revisão `8134f16e4d7a`;
- **App 09** — `TemplateDaMissao.tsx`, o primeiro `BlocoRecolhivel` de `ListaDeMissoes.tsx` e
  duas funções de `trilhas/api.ts`;
- **App 03** — o campo "técnico" em `FormularioDePoder.tsx` e a marca em `ListaDePoderes.tsx`;
- **DeepSeek** — só o adaptador do template o chama; `assistente/` e `producoes/` o citam apenas
  em comentário. A dupla `CG_DEEPSEEK_*` está em `configuracao.py`, no deploy e no README.

As decisões do fundador de 2026-11-16 (alcance total, tabela apagada, DeepSeek fora de tudo,
marca de técnico fora, cadência preenchida no campo, semeadura corrigida) estão na proposal.

## Goals / Non-Goals

**Goals:** nenhum rastro do template, da marca de técnico nem do DeepSeek no código, no banco,
no deploy e na documentação; a cadência de 2, 7 e 21 dias continua oferecida ao Mestre.

**Non-Goals:** mexer nas portas de leitura da produção e do assistente de trilhas; resolver a
pendência "Provedor da leitura da produção" do documento 09.

## Decisions

1. **Uma migração Alembic nova**, encadeada no _head_ atual, apaga o índice e a tabela
   `sugestao_de_estrutura` e a coluna `poder.tecnico`. O `downgrade` recria as duas vazias
   (coluna com `server_default` falso), sem prometer os dados de volta. A revisão `8134f16e4d7a`
   não é editada: histórico de migração não se reescreve.
   _Descartada:_ manter a tabela órfã — o fundador escolheu apagar.
2. **Rotas retiradas dentro do `/v1`, sem versão nova.** O precedente é o de
   `2026-09-26-carta-pela-sessao-e-nome-do-responsavel` e
   `2026-10-28-conteudo-corrigido-removido-exibido-e-ordenado`: os únicos consumidores (Apps 09 e
   03) mudam no mesmo PR, e o PRD-09 §9 registra a saída. O campo `tecnico` passa a ser campo
   desconhecido na escrita de `/v1/poderes` — 422 pelo `extra="forbid"` que já existe.
3. **A cadência sugerida mora só na App 09.** `CadenciaDeRetomada` inicia o campo com
   `"2, 7, 21"` quando `missao.cadencia_de_retomada` é nula; o resumo do bloco segue dizendo
   "sem retomada" até o Mestre gravar. O núcleo não ganha padrão: a missão sem cadência segue
   válida (`RF-09-101`). A constante sai do `regra.py` do template e vai para o componente.
4. **Requisitos retirados somem das tabelas do PRD**, sem linha "revogado"; os identificadores
   não são reaproveitados, e a lista deles fica na linha nova do documento 09 §1.
5. **DeepSeek sai da configuração**: `pydantic-settings` só lê do ambiente os campos
   declarados, então `CG_DEEPSEEK_CHAVE_DE_API` ainda presente no Cloud Run não derruba a subida.
   A ordem segura em produção é: merge e deploy → tirar a entrada do segredo `GCP_SECRETOS_CG`
   no GitHub → apagar `cg-deepseek-api-key` no Secret Manager. Apagar antes quebra o deploy.
6. **A capacidade `template-da-missao` termina sem requisito**: ao arquivar, a pasta
   `openspec/specs/template-da-missao/` é removida em vez de ficar só com o _Purpose_.

#### Documentação que muda

| Documento     | O que muda                                                                                          |
| ------------- | --------------------------------------------------------------------------------------------------- |
| 01            | nota sobre IA: atende com Gemini, sem DeepSeek                                                      |
| 02 §2         | sai o item da marca de técnico                                                                      |
| 03 §1.12      | Gemini como único modelo de linguagem do Ciclo 01; escolha por funcionalidade mantida                |
| 03 §§7, 8, 11 | sai o porquê do DeepSeek no custo; nota sem DeepSeek; saem a linha "Template de missão" e a regra da IA da autoria |
| 08            | sai o template de missão da lista da App 09                                                         |
| 09 §1         | linha nova da decisão; reescritas "Cadência padrão", "Revisão espaçada", "Modelos de IA", "Nota de transparência"; saem "Auxílio de IA na autoria" e "O que torna um poder técnico" |
| 11 §2.2       | ODS sem "o template sugere"; padrão 2, 7, 21 aberto no campo da cadência                             |
| 99            | linha "Modelo de missão e template de autoria" e a menção ao custo do template                      |
| PRD-01        | `RN-01-54` e a entidade `Poder` sem a marca                                                         |
| PRD-09        | §§1, 5, 6, 7, 9, 12, 13, 14 e rastreabilidade sem o template; `RF-09-116` reescrito                  |
| PRD-11        | linha da cadência sem "template"                                                                    |

## Risks / Trade-offs

- **Sugestões já gravadas se perdem** → aceito pelo fundador; o `downgrade` não as recupera.
- **Seção do PRD-09 numerada que perde conteúdo** (§5.2 e §6.2) → §5 é renumerada; §6.2 fica
  com `RF-09-90`, que a leitura da produção aplica, e muda de título.
- **Nota sobre IA em produção segue citando o DeepSeek** até o Admin republicá-la → passo
  manual listado nas tarefas; a semeadura não alcança banco já semeado.
- **Segredo apagado antes do deploy derruba a subida** → ordem da decisão 5 nas tarefas.
