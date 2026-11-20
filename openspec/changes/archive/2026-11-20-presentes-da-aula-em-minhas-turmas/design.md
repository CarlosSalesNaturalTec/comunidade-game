# Design — Presentes da aula em Minhas turmas

## Context

A leitura das turmas está em `aula-e-presenca` ("O Mestre lê as suas turmas…") e a tela em
`area-do-mestre`. `listar_minhas_turmas_rota` (`backend/src/nucleo/aulas/rotas.py`) pagina por
`(inicio_em, id)` e não olha a situação; a fatia 34 filtra a cancelada em
`TelaDeMinhasTurmas.tsx`. Não existe rota de leitura das presenças de uma aula — só
`/presencas/eu`, do próprio Guerreiro(a). Nick e avatar em lote já existem em
`buscar_avatares_e_nicks` (`vitrine/publico.py`), usado pelas equipes da aula; o desenho do
avatar na App 09 é `Avatar` de `comum/avatar`, como na fila de entregas.

## Goals / Non-Goals

**Goals:** cancelada fora da resposta e da paginação; leitura das presenças vigentes da aula no
escopo do Mestre; lista dos presentes na tela da aula; seção Atividades presenciais removida.

**Non-Goals:** seletor de Guerreiro(a) na ocorrência a partir da lista; anulação pelo Mestre;
qualquer mudança na App 03.

## Decisions

1. **Filtro no SQL, antes do cursor e do `limit`.** `Aula.situacao != SituacaoDaAula.cancelada`
   entra na consulta de `listar_minhas_turmas_rota`; assim a página nunca sai curta por causa da
   cancelada. Filtrar na saída foi descartado: repetiria o defeito de paginação da fatia 34.
2. **Rota `GET /v1/aulas/{id_da_aula}/presencas`**, sob `exigir_permissao(Operacao.suas_turmas,
   "le")`, sem paginação — o encontro é limitado pela sala, como `GET /aulas/{id}/equipes`, que
   devolve `PaginaDeResultado` com `proximo_cursor=None`; segue-se o mesmo envelope.
3. **Escopo:** aula inexistente ou, para o Mestre, `aula.comunidade_virtual_id` fora de
   `comunidades_do_mestre` → `NaoEncontrado("Aula não encontrada.")`, mesma mensagem nos dois
   casos. Admin lê qualquer aula. `escopo_de_comunidade_da_leitura` foi descartado: exige
   `comunidade` do Admin, que aqui a aula já determina.
4. **Saída** `PresencaDaAulaSaida(AvatarENickSaida)`: `id`, `guerreiro_id`, `nick`, `avatar`,
   `momento_do_fato`, `modo`. Só presenças com `anulada_em IS NULL`, ordenadas por
   `momento_do_fato`. Nick e avatar por `buscar_avatares_e_nicks`, um round-trip.
   `guerreiro_id` vai junto: o formulário de ocorrência pede o identificador, e o Mestre o lê na
   lista sem mudar o formulário.
5. **Tela:** `TelaDaAula` carrega a lista ao montar e de novo após `confirmarPresenca` bem
   sucedido; a seção "Presentes nesta aula" vem antes dos formulários. Rótulo do modo:
   "Reconhecimento" e "Confirmação". Falha de leitura vira `Aviso` de erro só na seção.
6. **Remoção da seção:** sai o bloco "Atividades presenciais" de `TelaDeMinhasTurmas`; o estado
   `atividadesPresenciais` fica, porque alimenta `TelaDaAula`. O filtro `situacao !==
   "cancelada"` da carga sai; `aulaEmAndamento` mantém o seu, por ser regra do painel do dia.

## Risks / Trade-offs

- [App 03 deixa de ver aula cancelada no Quiz] → não há partida a conduzir em aula cancelada;
  sem mudança de código lá.
- [Lista sem paginação] → o tamanho é o de uma sala; se crescer, o envelope já é o paginado.
