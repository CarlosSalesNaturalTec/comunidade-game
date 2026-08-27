## Context

O núcleo já tem tudo o que a fatia lança: `POST /v1/aulas/{id}/lancamentos` (converte reserva
em baixa e passa a aula a realizada), `POST /v1/aulas/{id}/presencas`,
`POST /v1/ocorrencias-de-conduta` e `POST /v1/lancamentos/{id}/ajuste`. O que ele **não** tem é
por onde listar lançamentos e como desfazer uma presença. A App 03 já tem o padrão de área com
seletor de comunidade, o `chamarNucleo` de `comum/api` e a leitura do encontro em
`GET /v1/painel-do-dia`, que devolve `aula_id`, presenças com avatar e nick, equipes,
atividades previstas e as pendências.

## Goals / Non-Goals

**Goals:**

- Fechar o encontro pela App 03: desfecho por participante, presença conferida e infração
  registrada, sem recriar regra que já está no núcleo.
- Dar ao `RF-02-40` um lançamento a corrigir, e ao `RF-02-36` o segundo sentido do ajuste.

**Non-Goals:**

- Lançar aula já encerrada — a área opera sobre a aula vigente (`RF-02-47`).
- Item do Código de Conduta (`RF-02-38`), atividade avulsa (`RF-02-29`) e conferência de
  inventário (`RF-02-56`): travados por pendência do documento 09.

## Decisions

1. **A área Lançamentos se ancora no `GET /v1/painel-do-dia`, não numa rota nova.** O painel já
   resolve a aula vigente para o operador em sessão e traz participantes, presenças e
   atividades previstas — é o mesmo recorte que a tela precisa. Descartado: um
   `GET /v1/aulas/{id}` com o mesmo conteúdo, que duplicaria a montagem do painel para servir a
   mesma aula.
2. **A área é nova, e não um modo de escrita do Painel do dia.** A spec vigente exige que o
   painel seja de leitura e que cada pendência leve à tela que a resolve; misturar escrita ali
   contrariaria requisito já aprovado.
3. **`GET /v1/lancamentos` com filtro de ponto de apoio obrigatório**, pelo
   `contrato_de_listagem` já usado em `GET /v1/locais`: os filtros universais de período e
   persona vêm de graça, o de ponto de apoio e o de tipo de recurso são os do domínio. Ponto de
   apoio no lugar de comunidade porque é ele que o `Lancamento` referencia — o livro-razão é
   por espaço, não por comunidade.
4. **A anulação da presença é coluna, não linha nova.** `Presenca` recebe `anulada_em`,
   `anulada_por_id` e `motivo_da_anulacao`, todos anuláveis; a `UniqueConstraint`
   `(aula_id, guerreiro_id)` dá lugar a um **índice único parcial** sobre as não anuladas
   (`postgresql_where=anulada_em IS NULL`), que é o que deixa registrar a presença correta
   depois do engano sem apagar o registro errado. Descartado: apagar a linha, que contraria a
   `RN-02-12`; e uma entidade `AnulacaoDePresenca`, que criaria entidade fora do PRD.
5. **A anulação é rota própria** — `POST /v1/aulas/{id_da_aula}/presencas/{id}/anulacao` —, e
   não um `DELETE`: o verbo `DELETE` diria "apagar", e o registro permanece. Restrita ao Admin
   pelo mesmo padrão de `lancar_atividade_realizada_rota`, que confere o papel na regra.
6. **`registrar_presenca` passa a ignorar a anulada na idempotência.** A busca do registro
   existente filtra `anulada_em IS NULL`; sem isso, o reenvio do App 01 devolveria a presença
   que o Admin acabou de anular, e o ajuste não se completaria. O painel do dia e o lançamento
   filtram pelo mesmo critério.
7. **O Mestre alcança a área Lançamentos só pela infração.** A App 03 não replica a matriz de
   permissões: a tela oferece ao Mestre apenas o formulário da infração, e o 403 do núcleo
   sobre atividade de trilha alheia é apresentado em uma frase, como já se faz na condução da
   partida.
8. **O extrato mora na área Pontos de Apoio**, ao lado dos saldos e da transferência que já
   estão lá: o lançamento é do ponto de apoio, e não do encontro. Descartado: uma área
   Livro-razão própria, que separaria saldo de extrato sem ganho para o operador.

## Risks / Trade-offs

- **Aula encerrada sem lançamento fica sem tela.** É a consequência aceita da decisão 1, e o
  `RF-02-47` existe justamente para que a pendência seja vista antes de a aula acabar. Se a
  operação do Ciclo 01 mostrar que acontece, a saída é uma leitura de aula por identificador —
  decisão do fundador, não da change.
- **O índice único parcial é do PostgreSQL.** É o banco decidido no documento 03 e o mesmo que
  os testes usam; a migração não é portável para SQLite, que o projeto não usa.
- **O extrato pode crescer muito** num ponto de apoio antigo. A paginação por cursor do PRD-01
  já é a resposta, e o filtro de período limita a leitura corrente.
