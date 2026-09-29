# Formulários de participação e de dados

Origem: **PRD-03 — App 06: Vitrine pública**, §§5.2, 5.4, 6.3, 7, 9 e 12. **Fatia 4** do PRD-03
no `openspec/cronograma-de-fatias.md`.

Atende `RF-03-27` a `RF-03-35`, `RN-03-11` a `RN-03-14`. Toca também `RF-03-37` (nenhuma
proteção exige CAPTCHA) e `RF-03-62` (a orientação do Mestre ganha o link que a fatia 1 deixou
de fora).

## Why

As duas portas de entrada de gente nova e de pesquisa da vitrine — pedir para ser Mestre ou
Apoiador, e pedir o conjunto de dados — existem no núcleo (`fila-de-avaliacao`, com freio por
origem nos dois envios) e não têm tela. Hoje o recorte de pesquisadores e o de gestores
terminam em "chega em entrega própria", e a orientação do Mestre nomeia o formulário em texto,
sem link, porque ele não existe.

## What Changes

- **Formulário de participação** em endereço próprio: nome, e-mail, WhatsApp, pretensão
  (Mestre ou Apoiador) e apresentação obrigatórios; instituição e links comprobatórios
  opcionais (`RF-03-27`, `RF-03-28`). Antes do envio a tela declara que a solicitação **não
  cria cadastro nem acesso**, que quem avalia é um Admin e que o prazo é de **7 dias**
  (`RF-03-29`, `RF-03-30`, `RN-03-11`, `RN-03-12`).
- **Formulário de dados** em endereço próprio: solicitante, instituição, e-mail e finalidade
  declarada obrigatórios (`RF-03-32`). A tela declara que a entrega é **gratuita,
  anonimizada, em CC BY-SA, depende de aprovação e é respondida em 7 dias**
  (`RF-03-33`, `RN-03-13`, `RN-03-14`).
- **Confirmação do registro** nos dois: a tela mostra o protocolo e o prazo que o núcleo
  devolveu e diz que o retorno virá pelo contato declarado, sem e-mail automático; nenhum
  formulário devolve dado, arquivo ou acesso no ato (`RF-03-31`, `RF-03-34`).
- **Espera crescente explicada**: recusada a origem pelo freio (429), a tela diz em linguagem
  simples o motivo e quanto falta, sem CAPTCHA, cadastro ou login e sem guardar marca no
  aparelho (`RF-03-35`, `RF-03-37`). O campo em falta, recusado pelo núcleo (422), é
  apontado no próprio campo.
- A seção "Solicitação do conjunto de dados" dos recortes de pesquisadores e de gestores
  deixa de ser pendente e leva ao formulário; a orientação do Mestre no "Entrar" passa a ter
  o link do formulário de participação.

Nenhuma rota, entidade ou migração nova: o núcleo não muda.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-vitrine`: a App 06 ganha os dois formulários públicos com os avisos, a
  confirmação e a espera explicada; a orientação do Mestre passa a apontar o formulário.

## Impact

- **Código novo**: telas dos dois formulários e o envio em `apps/app-06-vitrine/src/`
  (`api/`, `formularios/`, `navegacao/recortes.ts`, `entrada/personas.ts`, `App.tsx`).
- **Código lido**: `backend/src/nucleo/fila/rotas.py` (contrato dos dois `POST`),
  `comum/api/cliente.ts`, `comum/react/Campo.tsx`.
- **Documentação**: a linha 4 do cronograma. `docs/prds/index.md`, o documento 99 e a `nav`
  não mudam.
- **Fora do escopo**, como o PRD-03 §3.2 já exclui: login e cadastro; pré-cadastro de Apoiador
  (aporte, comprovante e nick — é da App 08); avaliação das solicitações e entrega do
  conjunto (atos de Admin na App 03); notificação por e-mail; qualquer preferência do
  visitante. Fora desta fatia, mas dentro do PRD-03: institucional (5), convite ao
  acompanhamento e necessidades (6), Mestres e Apoiadores (7) e o formulário de chave (8).
