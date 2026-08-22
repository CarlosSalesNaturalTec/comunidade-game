## Context

O ciclo de situação da trilha já tem irmão consolidado no repositório: a change
`desativacao-do-ponto-de-apoio` resolveu o mesmo problema no `PontoDeApoio` — mudar de estado
com motivo, guardando quem mudou, em que papel e quando. A spec `trilha-e-missao` já declara
que a situação nasce no PRD-01 e que "o fluxo que a muda" é do PRD-09: é este o fluxo.

Duas decisões do fundador de 2026-08-22 fecham o que faltava — três situações e republicação
pelo Mestre autor. Estão na proposal; aqui ficam só as escolhas de desenho que elas abrem.

## Goals / Non-Goals

**Goals:**

- A `Culminancia` como entidade própria, uma por trilha, com a porta do Mestre autor.
- As três travas de publicação conferidas numa transação, antes de qualquer escrita.
- A procedência da mudança de situação legível pelo Mestre autor.

**Non-Goals:**

- Versão de trilha e edição de trilha publicada — fora do escopo, decisão do fundador.
- Etiqueta ODS, desafio de desbloqueio e validação da criação original.
- Tela de despublicação na App 03 — travada pelo `RF-02-71` sem rota.

## Decisions

1. **`Culminancia` é módulo próprio (`nucleo/culminancias/`), não coluna da `Trilha`.** São
   quatro atributos com regra de posse e substituição, e o PRD-09 §8 a lista como entidade. A
   unicidade por trilha sai de índice único em `trilha_id`, e a segunda declaração é
   `UPDATE` na linha existente — não uma segunda linha nem histórico. Descartado: colunas na
   `Trilha`, que misturaria a especificação da produção com o cabeçalho da trilha.

2. **A `CriacaoOriginal` não ganha `culminancia_id`.** Com uma culminância por trilha, o
   `trilha_id` que ela já tem resolve a referência do PRD-09 §8. Descartado: coluna nova, que
   exigiria retroalimentar criações gravadas antes desta fatia sem ganho de expressividade.

3. **A situação vira enum de três valores e a procedência copia o `PontoDeApoio`** —
   `motivo_da_situacao`, `autor_da_situacao_id`, `papel_do_autor_da_situacao`,
   `situacao_alterada_em`, todos anuláveis. `SituacaoDaTrilha` é `native_enum=False`, então a
   migração altera a restrição de verificação, sem tipo novo no Postgres. Descartado: guardar
   o motivo na trilha de auditoria — `GET /v1/auditoria` é restrita a Admin por
   `Operacao.tudo` e `RegistroDeAuditoriaSaida` não tem campo de motivo, logo não serve ao
   `RF-09-10`, que exige o motivo **ao Mestre autor**.

4. **Uma só rota publica e republica.** `POST /v1/trilhas/{id}/publicacao` aceita origem
   `rascunho` ou `despublicada` e recusa `publicada`. Descartado: rota separada de
   republicação, que duplicaria as três travas em dois lugares.

5. **As travas são conferidas juntas e a recusa nomeia todas as que faltam.** O `RF-09-08`
   pede que a recusa diga *exatamente* o que falta; parar na primeira obrigaria o Mestre a
   três tentativas. A recusa é um `422` do contrato de erro único do PRD-01, com a lista das
   travas pendentes no corpo. Descartado: recusa curto-circuitada na primeira falha.

6. **A trava da coleta é existência, não contagem.** `RF-09-06` e `RN-09-02` pedem "ao menos
   um desafio de coleta"; a conferência é `EXISTS` sobre `DesafioDeColeta` juntado às missões
   da trilha, sem exigir que esteja na sondagem nem em etapa específica.

7. **A republicação limpa o motivo.** Voltar ao ar apaga `motivo_da_situacao` e regrava a
   procedência com o Mestre autor. O histórico da despublicação fica na trilha de auditoria,
   que já registra toda escrita; a coluna guarda a situação corrente, não o histórico — o
   mesmo contrato do `PontoDeApoio`. Descartado: entidade de histórico de despublicações, que
   nenhum `RF` pede.

8. **`GET /v1/trilhas/{id}` é pública e serve só `publicada`.** Rascunho e despublicada
   respondem 404, e não 403: distinguir os dois vazaria a existência de rascunho alheio, que
   o `RF-09-04` protege.

## Risks / Trade-offs

- **A despublicação nasce sem tela.** É rota de Admin, e a App 03 não tem por onde listar a
  trilha de um Mestre enquanto o `RF-02-71` não tiver rota. Fica testada e alcançável por
  contrato; a tela entra quando a pendência for decidida.
- **Trilha publicada é imutável até a fatia de edição.** O Mestre que encontrar um erro
  depende de um Admin despublicar. Consequência conhecida da decisão de 2026-08-22, registrada
  no documento 09 — não é defeito desta fatia.
- **Migração sobre trilhas existentes.** O enum ganha valor novo e as quatro colunas nascem
  anuláveis: nenhuma trilha já gravada precisa ser retroalimentada.
