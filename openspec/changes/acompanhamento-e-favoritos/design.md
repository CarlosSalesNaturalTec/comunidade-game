## Context

Ver `proposal.md` — Why. O que esta fatia encontra pronto:

- A **leitura pública** já existe no núcleo (`openspec/specs/leitura-publica-da-vitrine`): seis
  rotas sob `/v1/vitrine`, o portão da divulgação resolvido dentro da consulta e a projeção
  única de avatar e nick. Nada disso muda aqui; a App 08 passa a consumi-las.
- `vitrine.publico.buscar_persona_guerreiro_publica_por_nick` já resolve nick e vigência **na
  mesma consulta**, que é o que impede o código de vazar a diferença entre nick inexistente e
  nick sem autorização (`RN-01-22`). É a peça de que `RF-14-51` precisa, pronta.
- Os quatro fatos da novidade já têm data no núcleo: `CriacaoOriginal.validado_em` com
  `situacao = validada`, `Nivel.certificado_em`, `Badge.certificado_em` e
  `Trilha.situacao_alterada_em` com `situacao = publicada` e `autor_id` do Mestre.
- A App 08 tem oito áreas autenticadas, cada uma com `api.ts`, tela e teste, e a navegação em
  `App.tsx`.

## Goals / Non-Goals

**Goals:** uma entidade nova e três rotas; a novidade derivada em uma consulta por tipo de
fato; a área de acompanhamento consumindo a vitrine sem token de sessão.

**Non-Goals:** rota pública nova (a de Mestres é do PRD-03); qualquer escrita na vitrine;
armazenar novidade; qualquer campo de contato.

## Decisions

### 1. Módulo próprio `favoritos/`, com modelo, regra e rotas

`Favorito` não é atributo de persona nem de aporte: é entidade própria do Apoiador (PRD-01 §8),
e a novidade cruza quatro módulos. Módulo próprio, no padrão de `efetividade_do_apoio` e
`missoes_do_apoiador`, com o roteador registrado em `principal.py`.
_Alternativa descartada:_ pendurar em `personas/`, que já é o maior módulo do núcleo.

### 2. A guarda é o papel na rota, não a matriz de permissões

PRD-01 §4 não lista favorito entre o que o Apoiador escreve, e `Favorito` é, por definição do
PRD-01 §8, **preferência de quem lê**, existente só na App 08. A rota confere
`contexto.papel != Papel.apoiador` e devolve 403, como `efetividade_do_apoio` e
`selos_do_apoiador` já fazem — mesmo precedente do catálogo de tipos de coleta, cuja leitura o
próprio `permissoes.py` documenta como fora da tabela do PRD-01 §4.
_Alternativa descartada:_ acrescentar `Operacao.favoritos` à matriz, o que exigiria alterar
PRD-01 §4 — decisão de produto, não de implementação.

### 3. Uma tabela, duas colunas de alvo excludentes

`favorito` guarda `apoiador_id`, `guerreiro_id`, `mestre_id` e `incluido_em`, com
`CheckConstraint` de exatamente um alvo preenchido — o mesmo desenho de `CriacaoOriginal`
(`equipe_id` ou `guerreiro_id`) e de `Badge` (`trilha_id` ou `poder_id`). Duas
`UniqueConstraint` parciais, uma por alvo, garantem um só favorito por par.
_Alternativa descartada:_ coluna `alvo_id` com discriminador, que perde a chave estrangeira.

### 4. Favoritar de novo é idempotente, não é 409

PRD-14 §10 exige escrita idempotente para não duplicar registro por falha de rede, e `RF-14-55`
permite favoritar de novo depois de remover. O `POST` do alvo já favoritado devolve o favorito
existente, com o mesmo corpo do primeiro. Nada na resposta distingue os dois casos — o que
importa porque, no alvo Guerreiro(a), distinguir seria confirmar existência.
_Alternativa descartada:_ 409, que vira canal de sonda de nick.

### 5. A remoção é apagamento, e o 404 cobre os dois casos

O favorito é preferência de leitura, não fato com lastro: removê-lo apaga a linha. `DELETE` de
favorito inexistente e de favorito de outro Apoiador devolvem o **mesmo 404**, resolvido em uma
consulta que já filtra por `apoiador_id` — sem desvio no código que revele qual dos dois é.
_Alternativa descartada:_ situação `removido`, que guardaria o interesse do Apoiador por uma
criança depois de ele o desfazer.

### 6. A novidade é uma consulta por tipo de fato, com janela de 30 dias

`montar_novidades()` recebe os alvos dos favoritos e devolve, por alvo, os fatos com data
`>= agora - 30 dias`: criação original validada, badge certificado, nível certificado e trilha
publicada. Quatro consultas com `IN` sobre o conjunto de alvos, nunca uma por favorito — o
mesmo cuidado de `buscar_avatares_e_nicks`. A criação original de equipe alcança o favoritado
pela participação dele na equipe, e passa pelo mesmo portão de `listar_criacoes_publicas`: só
aparece quando **todos** os creditados têm autorização vigente.
_Alternativa descartada:_ tabela de novidade alimentada por gatilho — PRD-14 §8 diz que a
novidade é derivada, nunca armazenada.

### 7. O portão da divulgação entra na consulta dos favoritos, não em pós-filtro

`GET /v1/eu/favoritos` resolve os alvos Guerreiro(a) pela mesma
`condicao_de_autorizacao_vigente` da vitrine, dentro da consulta. Quem perdeu a autorização sai
da resposta sem lacuna e sem contagem — a linha continua no banco, e o alvo volta se a
autorização voltar. A leitura nunca informa que um favorito foi omitido: dizê-lo seria expor o
estado do consentimento de uma criança.

### 8. O freio de nick protege o `POST`, na superfície que já existe

O `POST` com alvo por nick é sonda de nick tanto quanto `GET /v1/vitrine/guerreiros/{nick}`, e
recebe a mesma dependência `exigir_freio_por_origem("consulta_por_nick")` (`RF-01-65`), sem
superfície nova de configuração.

### 9. A App 08 consome a vitrine pela chave, sem token

A área de acompanhamento chama `/v1/vitrine/...` com a chave de aplicação e **sem** token de
sessão, como PRD-14 §9 exige. O cliente `comum/api` já separa as duas credenciais; a chamada
pública apenas não passa `token`.

### 10. Uma área, dois blocos

A área **Acompanhamento** reúne o painel público e os favoritos em uma tela só, com dois
blocos, em vez de duas entradas na navegação: PRD-14 §5.8 as trata como uma jornada, e a App 08
já tem oito áreas — uma nona basta.

## Risks / Trade-offs

- **A tela de favoritos não tem como chegar a um Mestre** enquanto a página pública dele não
  existir (PRD-03) → decisão do fundador de 2026-09-02: o contrato aceita o alvo desde já, a
  tela lista quem foi favoritado, e a descoberta chega com o PRD-03. Registrado na proposta e
  na linha do cronograma.
- **A novidade fica com quatro dos cinco fatos** até o PRD-10 → a spec declara a lacuna e o
  cronograma a anota nos dois blocos, para que a fatia de batalhas não a perca de vista.
- **Quatro consultas de novidade por leitura** → todas com `IN` sobre o conjunto de alvos e
  janela de 30 dias; o volume é o dos favoritos de um Apoiador, não o da plataforma.
- **Republicar uma trilha despublicada reacende o destaque**, porque `situacao_alterada_em` é a
  única data de publicação que o núcleo guarda → aceito: o fato exibido é "trilha publicada", e
  a data mostrada é a que o núcleo tem.

## Migration Plan

Uma migração Alembic **aditiva**: cria `favorito` com o `CheckConstraint` do alvo único e as
duas `UniqueConstraint` parciais. Nenhuma tabela existente muda. `downgrade` derruba a tabela.
Nada a semear, nada a preencher.
