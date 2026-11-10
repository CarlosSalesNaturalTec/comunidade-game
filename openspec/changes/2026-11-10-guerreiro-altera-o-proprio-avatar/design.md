# Design

## Context

O avatar já tem tudo, menos a alteração: catálogo, renderizador e objeto do documento 15 §7.2
em `comum/avatar` (`camada-visual-comum`), atributo opaco na persona (`persona-e-credencial`) e
leitura por `GET /v1/eu` (`RF-01-76`). As rotas do Mestre (`PUT /v1/eu/mestre/identidade`) e do
Apoiador já gravam o próprio avatar sem validar forma; esta fatia segue o mesmo molde. A
montagem por camada existe só dentro da `TelaDeCadastro` da App 01.

## Goals / Non-Goals

**Goals:** `PATCH /v1/eu/avatar` no núcleo; a montagem promovida a `comum/avatar`; a tela de
alteração na carteira da App 05.

**Non-Goals:** regravar a facial (pendência nova no documento 09 §1); trocar nick ou forma de
tratamento; auditoria própria da troca, que o PRD-05 não pede; qualquer mudança no catálogo.

## Decisions

1. **Rota no módulo `personas`, ao lado das do Mestre e do Apoiador.** Regra
   `definir_avatar_do_guerreiro(sessao, persona, avatar)`, sem validação de forma; a rota checa
   `contexto.papel == Papel.guerreiro` e responde `PermissaoNegada` (403) aos demais, no molde de
   `_exigir_mestre_em_sessao`. Entrada `{"avatar": str}` com `min_length=1` e
   `extra="forbid"` (vazio dá 422 pela validação); saída `{"avatar": str}`. Sem migração.
   _Descartada:_ reaproveitar `PATCH /v1/guerreiros/{id}` — é do Admin e troca os quatro campos.
2. **O envelope é preservado no cliente, não no núcleo.** O texto gravado pela App 01 é
   `{"formaDeTratamento": …, "avatar": {objeto §7.2}}`. A App 05 lê o texto vigente de
   `GET /v1/eu`, e ao gravar: se ele é envelope (objeto JSON com `avatar` objeto), troca só
   `avatar` e mantém as demais chaves; se é o objeto §7.2 sozinho, texto livre antigo ou nada,
   grava o objeto novo sozinho, porque não há forma de tratamento a preservar. A função pura
   `regravarAvatar(textoVigente, avatarNovo): string` fica em `comum/avatar/objeto.ts`, ao lado
   de `lerAvatar`, que já conhece o envelope. _Descartada:_ merge no núcleo — quebraria a
   opacidade que as três rotas de avatar mantêm.
3. **Montagem como componente controlado.** `MontagemDoAvatar({ avatar, aoAlterar, tamanho? })`
   em `comum/avatar`, extraída sem mudança de marcação do `fieldset.cg-escolha-de-avatar` da
   `TelaDeCadastro` (legenda "Monte o seu avatar", `Avatar` de 96, um `select` por camada de
   `CAMADAS_DO_AVATAR`). As três regras `.cg-escolha-de-avatar*`, hoje só no `index.css` da App 01,
   sobem para `comum/avatar/estilos.css` — sem elas a montagem na App 05 sairia sem estilo. A App 01 passa a consumi-la; o fundo de partida `acao-100` segue
   sendo da `TelaDeCadastro`, não do componente.
4. **Na App 05, tela dentro da carteira.** `MinhaCarteira` ganha o botão "Mudar o meu avatar"
   no apoio do palco; acionado, a seção troca o palco pela `AlterarMeuAvatar`, que lê
   `GET /v1/eu`, abre a montagem em `lerAvatar(texto)` e oferece "Salvar o meu avatar" e
   "Voltar sem salvar". Salvo, volta à carteira e remonta a `MinhaCarta` por `key`, para a carta
   reler `GET /v1/eu`. Cliente `alterarMeuAvatar(token, avatar)` em `src/api/carteira.ts`.
   _Descartada:_ quinto caminho no menu — o avatar é da carta, e a carta mora na carteira.
5. **Frases** (linguagem de criança, PRD-05 §10), a aprovar com os artefatos: botão "Mudar o meu
   avatar"; título "Meu avatar"; "Salvar o meu avatar" / "Salvando…"; "Voltar sem salvar";
   falha "Não deu para salvar o seu avatar agora. Tente de novo em instantes."

## Risks / Trade-offs

- **Gravação concorrente** (Admin edita pela App 03 enquanto a criança monta): vence a última,
  como nas demais rotas de avatar. Aceito.
- **Avatar de texto livre antigo** perde o texto ao ser alterado. Ele já não desenha nada —
  `lerAvatar` o resolve no avatar padrão — e não carrega forma de tratamento legível.
