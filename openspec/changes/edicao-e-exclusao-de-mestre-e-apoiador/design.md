## Context

O cadastro de adulto já existe (`openspec/specs/cadastro-de-persona`, `cadastrar_adulto_com_artefatos`
em `personas/regra.py`), com a credencial de login social identificada pelo e-mail. A exclusão
"só do nunca usado" já tem helper genérico, `referencias.esta_em_uso`, criado pela fatia 27 para
os catálogos de tipo. A ficha do adulto (`FichaDoAdulto.tsx`) é de leitura desde a fatia 18.

## Goals / Non-Goals

**Goals:** editar, excluir, desativar e reativar Mestre e Apoiador pela gestão (`RF-02-117` a
`RF-02-119`, `RN-02-34`, `RN-02-35`).

**Non-Goals:** Admin, responsável e Guerreiro(a); nick, papel e termos de doação; mexer em
qualquer fato produzido pelo adulto.

## Decisions

1. **Rotas por papel, no padrão existente.** `PATCH`, `DELETE`, `POST .../desativacao` e
   `POST .../reativacao` sob `/v1/mestres/{id}` e `/v1/apoiadores/{id}`, com
   `exigir_permissao(Operacao.tudo, "escreve")`. Artefato pela gestão: `POST`, `PATCH` e `DELETE`
   em `/v1/{papel}/{id}/artefatos-da-gestao[/{artefato_id}]` — caminho próprio porque
   `/v1/mestres/{id}/artefatos` é do próprio Mestre (`RN-09-14`) e recusa perfil alheio. Papel
   da persona diferente do da rota responde 404. Alternativa descartada: rota única
   `/v1/adultos/{id}` — quebraria a simetria com o cadastro e a listagem.
2. **`PATCH` com `extra="forbid"`**: campo de nick, papel ou termos chega e é 422. Campo ausente
   mantém; `whatsapp` nulo retira.
3. **Troca de e-mail** atualiza `Persona.email` e o `identificador` da credencial ativa de login
   social na mesma transação; a `IntegrityError` do índice
   `uq_credencial_identificador_por_tipo_ativa` vira 422.
4. **Correção de artefato pelo Admin** altera o vigente e **não** toca `endereco_original`/
   `rotulo_original`, que registram a edição do próprio adulto (decisão de 2026-09-06).
5. **"Nunca usado"** é `esta_em_uso(tabela=persona, tabelas_ignoradas={nick, credencial,
   sessao, artefato_comprobatorio})`; as quatro saem junto, nessa ordem, antes da persona. A
   `persona.criada_por` do próprio adulto aponta para o Admin, não para ele, e não interfere.
   `IntegrityError` de corrida vira o mesmo 422.
6. **Desativação é `persona.desativada_em`** (`timestamptz`, nulo = ativo), por migração Alembic
   sem retroação. Desativar revoga as credenciais ativas (`ativa=false`, `revogada_por`,
   motivo "desativação pela gestão") e encerra as sessões abertas. Reativar limpa a marca e
   reativa **só a credencial de login social** revogada pela desativação; senha provisória não
   volta. Alternativa descartada: só revogar credencial — a vitrine não teria por onde filtrar.
7. **Vitrine** filtra `desativada_em IS NULL` na paginação de adultos públicos e na leitura por
   identificador, que responde 404 como a inexistente.
8. **App 03.** `FichaDoAdulto` ganha modo de edição dos três campos e reaproveita
   `FormularioDeArtefatos` para incluir, corrigir e remover; as três ações ficam no rodapé da
   ficha, com confirmação no padrão de `catalogos/AcoesDoTipo.tsx`. `ListaDeAdultos` marca a
   linha pelo `ativo` da saída.

## Risks / Trade-offs

- **Mestre desativado com aula futura agendada** segue na agenda; a gestão precisa
  reagendar à mão. Não há regra no PRD que impeça a desativação nesse caso — se o fundador
  quiser bloqueio, vira pergunta antes do `apply`.
- **Lista ignorada do helper é fixa**: tabela nova que pertença ao cadastro do adulto (e não seja
  uso) precisará entrar nela, senão o adulto deixa de ser excluível — falha segura.
