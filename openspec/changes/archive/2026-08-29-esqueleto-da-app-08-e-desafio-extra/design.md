## Context

Ver `proposal.md` — Why. O que molda o desenho:

- O núcleo já tem tudo o que a entrada do Apoiador exige: `sessao-do-adulto` decide os três
  casos (login social, usuário e senha, senha provisória), `persona-e-credencial` cria o
  Apoiador por ato de Admin, a matriz de `permissoes.py` já lhe dá `propostas_de_desafio_extra`
  e a chave `app-08-apoiador` já é semeada. **Nenhuma regra de acesso é escrita aqui.**
- `DesafioExtra` é a primeira entidade do projeto cujo ciclo de vida atravessa **três
  aplicações**: propõe-se na App 08, valida-se na App 09 e aprova-se na App 03. Duas dessas
  etapas são fatias de outros PRDs, ainda não implementadas.
- `apps/` já tem quatro aplicações no mesmo molde (Vite, React, TS, `comum/`), e o
  `frontend-ci.yml` já cobre `apps/**` por caminho.

## Goals / Non-Goals

**Goals:**

- A entidade `DesafioExtra` completa, com os atributos do PRD-14 §8, pronta para as três fatias
  que a esperam.
- A App 08 de pé, com a entrada do Apoiador e as duas telas do desafio extra.

**Non-Goals:**

- As **transições** de situação: a validação do Mestre (fatia 15 do PRD-09) e a aprovação e
  publicação pelo Admin (fatia 15 do PRD-02), que traz a reserva e a liberação da recompensa.
- A **implantação** da App 08: o alvo de _hosting_ não existe em `.firebaserc`, e criá-lo é ato
  de infraestrutura, como foi para a App 03 (`implantacao-da-app-03-e-do-nucleo`).

## Decisions

### O módulo nasce no molde do núcleo, com a situação em quatro estados

`backend/src/nucleo/desafios_extras/` com `modelo.py`, `regra.py` e `rotas.py`, mais a migração
Alembic — o mesmo molde de `catalogo_avulso/` e dos demais. A situação é um `StrEnum` de quatro
valores — `em_validacao_do_mestre`, `em_aprovacao_do_admin`, `publicado`, `recusado` —, e toda
proposta nasce no primeiro (`RF-14-35`, `RN-14-13`).

**As transições ficam na `regra`, sem porta HTTP nesta fatia.** A guarda da publicação —
recusar sem lastro provido (`RF-07-15`, `RF-14-34`) — é escrita e testada aqui, porque é
requisito desta fatia; quem a chama é a rota de aprovação da fatia 15 do PRD-02. Alternativa
descartada: entregar aqui as rotas de validação e de aprovação — ampliaria o recorte de dois
outros PRDs.

### O nick do destinatário é texto, nunca chave estrangeira

O PRD-14 §8 é explícito: o nick é guardado **como o Apoiador o digitou**. Coluna de texto, sem
`ForeignKey` e sem consulta de existência na escrita — é o que impede a aplicação de confirmar
que o nick existe (`RF-14-33`, `RN-14-18`). A ligação com a pessoa é feita na validação do
Mestre, fora desta fatia.

### `lastro_provido` é derivado, não coluna

O desafio guarda o **custeio declarado** — `aporte_do_proponente` ou `saldo_de_recurso`
(`RF-14-76`, `RF-07-41`) — e, no primeiro caso, o aporte que o lastreia. Se o lastro está
provido é lido na hora: aporte **homologado** (PRD-07) ou saldo disponível suficiente do tipo
de recurso. Segue o padrão do projeto para o Poder Sustentador e o saldo — derivar dos
lançamentos em vez de guardar um espelho que envelhece. Alternativa descartada: coluna
booleana recalculada a cada escrita, como em `ItemDeCatalogoAvulso.ativo` — ali a coluna existe
porque a listagem do catálogo filtra por ela em consulta quente, o que não é o caso aqui.

### A imutabilidade do publicado é guarda de escrita, não de leitura

Alteração de desafio **publicado** é recusada com **405** na regra, e a proposta anterior fica
registrada com o desfecho que teve (`RF-14-38`). É o mesmo desenho do lançamento do
livro-razão: não se edita, corrige-se com registro novo.

### A App 08 é a quinta aplicação no molde existente

`apps/app-08-apoiador/` copia a estrutura de `apps/app-09-mestre/` — Vite, React, TS, `comum/`
para acesso e camada visual, `src/autenticacao/` e uma pasta por assunto. O `frontend-ci.yml`
já a alcança por `apps/**`: **não nasce workflow novo de CI**. O que a fatia acrescenta é a
pasta, o `package.json` no _workspace_ e o `.env.example` com a chave da App 08.

### O custo do desafio extra não entra no livro-razão nesta fatia

A proposta não movimenta recurso: quem reserva a recompensa é a publicação, na fatia 15 do
PRD-02 (`RF-07-39`, `RF-07-40`). Nada aqui gera lançamento.

## Risks / Trade-offs

- **Regra de publicação sem chamador até a fatia 15 do PRD-02** → é o mesmo desenho já aceito
  em `poder-trilha-missao-e-atividade`, cuja regra esperou a porta da fatia seguinte; o teste
  cobre a guarda diretamente, sem depender de rota.
- **A App 08 fica sem implantação até a criação do alvo de _hosting_** → o `frontend-ci.yml`
  garante formatador, _linter_ e testes desde o primeiro _commit_; a publicação entra quando o
  alvo existir, como foi na App 03.
- **`lastro_provido` derivado custa uma leitura de saldo por desafio na listagem do proponente**
  → a lista é dos desafios de um Apoiador, dezenas na pior hipótese, e o projeto prefere o dado
  correto ao espelho barato.
