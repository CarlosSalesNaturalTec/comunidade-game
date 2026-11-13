# Design

## Context

O núcleo já serve tudo o que a fila precisa (`openspec/specs/customizacao-do-kit/` e
`openspec/specs/conservacao-do-bem-recebido/`): `GET /v1/aulas/{id}/fila-do-cuidado`,
`POST /v1/customizacoes/{id}/julgamento`, `POST /v1/aulas/{id}/conservacoes`,
`POST /v1/aulas/{id}/customizacoes` com o envio retomável em `/v1/customizacoes/{id}/envios` e
`/envios/confirmacao`, e `GET /v1/customizacoes/{id}/arquivo`. Falta o "antes" quando ele é a
comprovação do prático: `GET /v1/missoes/{m}/desbloqueios/{g}/comprovacao` só serve ao Mestre
autor, e a fila devolve o `id` do desbloqueio, não o da missão. A tela segue o molde de
`entregas/TelaDeEntregasDoEncontro.tsx` (fatia 31 do PRD-04).

## Goals / Non-Goals

**Goals:** a fila do cuidado operável no encontro, sob o token de trabalho, com a rota do "antes".

**Non-Goals:** o registro pela criança no aparelho (fatia 35); mover o cliente da customização
para `comum/` — a fatia 35 e a fatia 18 do PRD-05 decidem isso quando houver o segundo uso.

## Decisions

1. **Rota do "antes" pelo bem:** `GET /v1/entregas-de-recompensa/{id}/ultimo-aprovado/arquivo`,
   em `cuidado_do_bem/rotas.py`. A regra reusa `ultimo_registro_aprovado` (o mesmo cálculo que a
   fila já devolve) e a guarda `_mestre_da_comunidade_do_guerreiro` da mídia da customização; os
   bytes saem da referência da customização ou da comprovação do desbloqueio, conforme a `fonte`.
   Descartado: ampliar a rota da comprovação — alcançaria todo prático, não só o kit (decisão do
   fundador de 2026-11-13). Descartado: `missao_id` na fila — continuaria barrado pelo autor.
2. **Uma rota de mídia só para o "antes"**, nas duas fontes: a tela não ramifica pela `fonte`.
   O "agora" usa a rota já existente do registro pendente.
3. **Tela `cuidado/TelaDoCuidadoNoEncontro.tsx`**, caminho `"cuidado"` em `TelaInicial`, logo
   depois de `"entregas"` e com a mesma guarda `papelDeTrabalho === "mestre"`. Um cartão por
   Guerreiro(a); dentro dele, um bloco por bem. O estado do bem decide as ações:

   | Estado do bem                         | Ações                                      |
   | ------------------------------------- | ------------------------------------------ |
   | `pontuado_na_aula` preenchido         | nenhuma; diz por qual caminho pontuou      |
   | customização fechada                  | validar conservação                        |
   | aberta, sem pendente                  | validar conservação; capturar customização |
   | aberta, com pendente com mídia        | validar conservação; aprovar; reprovar     |
   | aberta, com pendente sem mídia        | validar conservação; enviar a mídia        |

   Escolher conservação **ou** customização é escolher o botão: o núcleo garante a `RN-01-66`, e
   a fila relida esconde as ações do bem que pontuou.
4. **Mídia por `MidiaDoNucleo`** com o token de trabalho, como a programação já faz — nunca a
   referência do armazenamento em `<img src>` (defeito consertado na fatia 33).
5. **Captura:** `POST /v1/aulas/{id}/customizacoes` com `guerreiro_id`, `entrega_de_recompensa_id`
   e `descricao`; depois o envio retomável por `enviarParteComProgresso` de `comum/api`, como a
   comprovação, e a confirmação. Arquivo por `<input type="file" capture="environment">` com
   `accept="image/*,video/*"`; descrição por `iniciarTranscricao` de `comum/fala` caindo num
   campo editável, como em `EntregaDaProducao`. Registro gravado e envio interrompido fica
   pendente sem mídia: a tela oferece retomar o envio do mesmo registro.
6. **Cliente** em `api/cuidadoDoBem.ts`, todas as chamadas com `tokenDeTrabalho`.
7. **Recusa do núcleo como vem** (`ErroDaApi.message`) e fila relida depois de cada escrita,
   bem-sucedida ou não.
8. **Glifo `cuidado`** em `comum/react/Icone.tsx`, se nenhum existente couber.

## Risks / Trade-offs

- [Vídeo grande no aparelho do encontro] → o teto é o do núcleo; a tela mostra o progresso e
  retoma pela sessão.
- [Dois Mestres julgando o mesmo kit em aparelhos diferentes] → o núcleo recusa o segundo
  (registro já julgado, `RN-01-66`); a tela mostra a recusa e relê.
- [Rota nova amplia quem vê a comprovação do prático] → só Mestre da comunidade do
  Guerreiro(a), só a do prático que abriu a customização do kit.

## Migration Plan

Sem migração. Rollback: reverter o PR.
