# Design

## Context

O padrão já existe para Mestre e Apoiador (`cadastro-de-persona`, `RF-02-117`): o e-mail do
cadastro vira uma `Credencial` de `login_social` com o e-mail como identificador, que é o que
`POST /v1/sessoes/social` procura; `alterar_adulto` troca o identificador quando o e-mail muda
e recusa e-mail de credencial social ativa de outra persona. `Persona.email` já existe. Esta
fatia aplica o mesmo padrão ao responsável.

## Goals / Non-Goals

**Goals:** e-mail opcional no cadastro (Apps 03 e 09), edição de nome e e-mail pelo Admin
(App 03), acesso visível na lista (Apps 03 e 09).

**Non-Goals:** edição pelo Mestre; e-mail no cadastro mínimo da App 01; validação de formato
do e-mail além de não vazio — o padrão de Mestre e Apoiador também não valida formato.

## Decisions

1. **Reaproveitar, não copiar.** `_gravar_credencial_de_login_social`,
   `_credencial_social_ativa` e `_email_em_uso_por_outra` de `personas/regra.py` passam a ser
   importados por `responsaveis/regra.py` (sem o `_` inicial, por serem agora de uso
   compartilhado). `alterar_adulto` não é reusado: ele recusa e-mail vazio, e no responsável o
   e-mail é opcional.
2. **Rota:** `PATCH /v1/responsaveis/{id}` com `exigir_permissao(Operacao.tudo, "escreve")`,
   o mesmo portão só-Admin das rotas `PATCH /v1/mestres/{id}`. Sem `Operacao` nova. Corpo
   `{nome?, email?}`, `extra="forbid"`; `email` nulo ou vazio é a retirada. Persona que não é
   responsável responde 404. Devolve o responsável como a linha da lista.
3. **Retirar o e-mail desativa a credencial** (`ativa = False`) e zera `Persona.email`, em vez
   de apagar: mantém a autoria da credencial e o rastro. Regravar o e-mail depois cria
   credencial nova. Alternativa descartada: apagar a linha — perde quem a criou.
4. **Recusa de e-mail duplicado** sai como `ErroDeValidacao` com `campo="email"` (422), a mesma
   do padrão de Mestre e Apoiador; as apps a mostram no campo.
5. **Leitura da lista:** `ResponsavelDaListaSaida` ganha `email: str` e `usuario: str`, vazios
   quando não há credencial **ativa** daquele tipo. Uma consulta a `Credencial` filtrada pelos
   `persona_id` da página, agrupada em memória — sem N+1.
6. **Telas:** App 03 — campo "E-mail da conta Google (opcional)" no cadastro; na lista, coluna
   **Acesso** ("Google: x · Usuário: y" ou "sem acesso") e o botão **Editar ficha** na linha,
   abrindo `EdicaoDoResponsavel` no molde de `EdicaoDoAdulto`. App 09 — o mesmo campo e a mesma
   coluna, sem edição.

## Risks / Trade-offs

- [O nome da credencial provisória criada depois do cadastro não aparece até recarregar a
  lista] → a tela já recarrega a lista ao concluir o formulário.
- [Mostrar o usuário e o e-mail amplia o dado pessoal na tela do Mestre] → é a decisão do
  fundador; o aviso de coleta das duas telas passa a citar o e-mail e o usuário.
