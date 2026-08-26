# Design — carteira, catálogo, conquistas e ranking

## Context

A fatia é majoritariamente **leitura sobre o que já existe**. As capacidades `ponto-extra`,
`catalogo-avulso`, `troca-de-recompensa-avulsa` e `recompensa-de-marco` já descrevem o
comportamento das quatro rotas consumidas como estão, e `area-do-guerreiro` já firmou, na
primeira fatia, como a App 05 se comporta em aparelho compartilhado: nada do Guerreiro(a)
anterior sobrevive à troca de sessão, e nenhuma recusa chega à criança em termo técnico. Este
documento traz só o que esta fatia decide.

## Decisions

**A rota do ranking logado nasce autenticada, em `GET /v1/rankings/{comunidade}`.** O PRD-05 §9
a declarava pública, contra o `RF-05-84` e a decisão do ranking interno do documento 09 — é a
tela ser logada que sustenta a exceção à divulgação. O segmento de comunidade é mantido, como o
PRD declara, e a rota recusa com 403 comunidade diferente da do Guerreiro(a) em sessão.
_Descartada:_ `GET /v1/eu/ranking`, sem o segmento — mais curta, mas afasta-se do contrato
declarado no PRD sem ganho de comportamento.

**A derivação do ranking passa a ser uma só, em `pontuacao/`.** A soma de `PontoRegular` menos o
débito das ocorrências de ciclo encerrado hoje vive dentro da rota pública, em `vitrine/`. Esta
fatia a extrai para a regra de `pontuacao/`, parametrizada pelo **portão de divulgação** e pelo
**recorte** — trilha, poder ou nenhum —, e as duas rotas passam a chamá-la. Duplicar a consulta
poria a regra do ciclo encerrado em dois lugares, e o invariante 23 exige que só o ponto regular
conte. _Descartada:_ copiar a consulta para o módulo novo.

**O recorte por trilha ou poder usa as colunas que `PontoRegular` já tem** — `trilha_id` e
`poder_id`, anuláveis —, sem tabela nova e sem agregação materializada.

**O estado da divulgação entra em `GET /v1/eu`, não em rota nova.** O PRD-05 §9 não declara rota
para o `RF-05-50`, e `GET /v1/eu` já é a leitura da persona em sessão. O campo só aparece para
persona de papel Guerreiro(a). _Descartada:_ `GET /v1/eu/perfil`, que duplicaria a leitura da
persona por um único booleano.

**A leitura das conquistas sai em `GET /v1/eu/recompensas`**, como o PRD-05 §9 declara, e
reaproveita a derivação de marco alcançado que `recompensas_de_marco/regra.py` já usa para
recusar a entrega. Nenhuma consulta nova de percurso.

**A App 05 ganha uma área só, com quatro telas** — carteira, catálogo, conquistas e ranking —,
mais o estado do perfil dentro da carteira. Todas leem à entrada, sem sondagem periódica: nada
aqui muda durante o encontro por ato de terceiro, diferente do painel do dia e da partida de
quiz.

## Risks / Trade-offs

- **Catálogo e conquistas dependem de cadastro da gestão** (PRD-05 §14): sem preço de referência
  cadastrado ou sem recompensa declarada no marco, as telas abrem vazias. É estado legítimo, e
  cada tela explica a ausência em vez de mostrar tela em branco.
- **O ranking logado é a única leitura da plataforma que alcança quem não autorizou divulgação.**
  A trava é dupla e fica no núcleo, não na tela: só papel Guerreiro(a), só a própria comunidade.

## Migration Plan

Não se aplica: nenhuma tabela nova, nenhuma coluna nova, nenhuma migração. A extração da
derivação do ranking preserva o contrato da rota pública, coberto pelos cenários já existentes
em `leitura-publica-da-vitrine`.

## Open Questions

Nenhuma. As duas pendências da §14 do PRD-05 que tocam o recorte são cadastro da gestão, não
desenho.
