# Design

## Context

A motivação está em proposal.md, em Why. O que existe hoje:

- `POST /v1/sessoes/guerreiro/confirmacao` (`backend/src/nucleo/sessoes/rotas.py`) confere só a
  permissão da persona em sessão. No App 01, essa persona é quem abriu a sessão de trabalho
  (`tokenDeTrabalho`), e nenhum ato dela é exigido no momento da confirmação.
- A fila sem rede (`apps/app-01-aula-presencial/src/fila/`) guarda nick, hora do fato e aula.
  Ao sincronizar, reabre a confirmação pelo nick e registra a presença.
- `Sessao` já guarda `origem` (a aplicação da chave) e `quem_confirmou`, e o contexto da rota
  já traz `sessao_id`.
- Mestre e Admin entram só pelo Google (documento 03 §1.1).

## Goals / Non-Goals

**Goals:** o PIN confere do mesmo jeito no núcleo e no navegador; o bloqueio vale por sessão de
trabalho; nenhuma rota nova resolve nick em identificador.

**Non-Goals:** exigir o PIN nos outros atos da sessão de trabalho (autocadastro, homologação,
troca). Isso seria decisão nova.

## Decisions

1. **Verificador: PBKDF2-HMAC-SHA256, sal aleatório de 16 bytes e 600 000 iterações**, guardados
   em `Persona` (`pin_verificador`, com algoritmo, iterações, sal e resumo). É a única derivação
   lenta que existe tanto no `hashlib` do núcleo quanto no `SubtleCrypto` do navegador, sem
   dependência nova. A conferência no aparelho é a mesma conta do núcleo. As iterações ficam
   no próprio verificador, para poderem subir sem invalidar os PINs já gravados.
   _Descartado:_ scrypt e Argon2, que não existem no `SubtleCrypto` e exigiriam biblioteca no
   App 01.
2. **O PIN é conferido antes do nick** na confirmação (`RN-01-22`). A ordem é: bloqueio →
   verificador ausente → resumo → nick. Assim a resposta a um PIN errado nunca depende de o
   nick existir.
3. **O contador de erros fica em `Sessao`** (`erros_de_pin_seguidos`). A sessão de trabalho é,
   na prática, "aquele aparelho": um novo login Google cria outra `Sessao`, que começa zerada.
   Não há entidade de aparelho. _Descartado:_ contador na `Persona`, porque um erro num aparelho
   bloquearia o adulto em todos.
4. **O PIN só é exigido quando a origem é o App 01**, pela chave de aplicação. É a leitura
   literal de "no encontro" (`RN-01-59`). A App 05 continua confirmando sem PIN: responsável e
   adulto entram lá com o próprio login, no ato.
5. **Erros novos, no corpo único** (`backend/src/nucleo/erros.py`): `pin_recusado` (401),
   `pin_bloqueado` (403) e `pin_nao_cadastrado` (403). A App 01 dá uma frase a cada um
   (`RN-04-36`).
6. **Sincronização sem sessão:** `POST /v1/aulas/{id}/presencas/sem-rede` recebe `{nick,
   momento_do_fato}` e grava a presença por confirmação, com o operador como confirmador. Ela
   reusa a resolução de nick da confirmação (a mesma recusa indistinguível) e a regra de
   unicidade de `aulas/regra.py`. A sincronização deixa de abrir sessões que ninguém usa.
   _Descartado:_ mandar o PIN pela fila, porque o PIN nunca pode ficar no aparelho.
7. **Verificador no aparelho:** o App 01 o busca ao abrir a sessão de trabalho e o guarda em
   `sessionStorage`, ao lado do token, apagando os dois juntos. O contador local de erros e a
   marca de bloqueio ficam no mesmo lugar, para que recarregar a página não os zere. Um
   `pin_bloqueado` vindo do núcleo também liga a marca local.
8. **Rotas do PIN pelo `/v1/eu`**: `PUT /v1/eu/pin-de-confirmacao` e
   `GET /v1/eu/pin-de-confirmacao/verificador`. O `GET /v1/eu` ganha `tem_pin_de_confirmacao`,
   um booleano, que as telas das Apps 09 e 03 usam para dizer se já há PIN. A permissão reusa
   `confirmacao_de_identidade_do_guerreiro`, que só Mestre e Admin têm: o PIN serve só a esse
   ato, e uma operação nova mudaria o `/v1/eu` de todos os papéis. A tela do PIN é uma só, em
   `comum/autenticacao`, usada pelas duas aplicações.
9. **O rótulo "Sem equipe" vai até o contrato**: o campo `aguardando_aparelho` do painel
   (`painel_do_dia/regra.py`, `apps/app-03-gestao/src/painel-do-dia/api.ts`) passa a se chamar
   `sem_equipe`. O único consumidor é a App 03, que muda no mesmo PR.

## Risks / Trade-offs

- **[Risco] Um PIN de 4 dígitos tem só 10 000 combinações, e o verificador fica no aparelho.**
  Quem copiar o `sessionStorage` durante a aula pode testar os 10 000 PINs fora dele. Com
  600 000 iterações, isso leva horas num computador comum e bem menos em GPU. → Mitigações: o
  verificador só vai à chave do App 01, só vive enquanto dura a sessão de trabalho, e trocar o
  PIN na App 09 ou na App 03 o invalida. O fundador escolheu o tamanho sabendo disso
  (documento 09). A ameaça que o PIN fecha é a criança diante da tela, não quem abre as
  ferramentas do navegador.
- **[Risco] A rota sem rede confia no aparelho.** O núcleo não tem como provar que o PIN foi
  conferido offline. → Quem chama a rota sem a tela só consegue gravar presença, nunca abrir
  sessão, ou seja, o mesmo alcance da rota de presença que já existe. A autoria continua sendo
  do adulto da sessão de trabalho.
- **[Risco] Chamar a rota de presença diretamente, no modo confirmação, sem PIN** grava
  presença com o operador como confirmador. → É o mesmo alcance do risco anterior e exige o
  identificador do Guerreiro(a), que só sai de uma sessão aberta. Fica como está.
- **[Trade-off]** A primeira conferência de PIN no aparelho leva cerca de 1 s em celular
  modesto. É aceitável num ato de exceção.

## Migration Plan

1. Migração Alembic: `persona.pin_verificador` (JSON, nulo) e
   `sessao.erros_de_pin_seguidos` (inteiro, padrão 0). Nenhum dado existente muda.
2. Deploy do núcleo e das Apps 09 e 03 primeiro. Os Mestres e Admins cadastram o PIN.
3. Deploy do App 01. A partir daí, confirmar exige PIN. Presença enfileirada antes do deploy
   sincroniza pela rota nova, sem perda.
4. Rollback: voltar o App 01 e o núcleo juntos. As colunas novas podem ficar.
