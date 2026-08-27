## Context

Ver `proposal.md` — Why. O que a fatia encontra pronto: `local-do-territorio` (hierarquia de
seis níveis, `POST /v1/locais` e `GET /v1/locais` com filtro de comunidade obrigatório),
`solicitacao-de-local` (`GET /v1/solicitacoes-de-local/abertas` e
`POST /v1/solicitacoes-de-local/{id}/avaliacao`, com o recorte por papel já no núcleo),
`comunidade-virtual` (`VinculoJogador` com histórico e o `vinculo_vigente` mapeado em `Persona`)
e `desafio-de-coleta` (o desafio preso à missão, e a missão à trilha).

Na App 03, o padrão de área com seletor de comunidade está de pé em Pontos de Apoio, e o de
fila com desfecho em Filas. A fatia é, quase inteira, aplicação desses dois padrões.

## Goals / Non-Goals

**Goals:**

- Uma área só — Território — que reúna hierarquia, cadastro, fila de solicitações e leitura dos
  desafios, sob a mesma comunidade escolhida.
- Duas leituras novas no núcleo, mínimas: o vínculo na listagem que já existe e a lista de
  desafios publicados.

**Non-Goals:**

- Editar ou apagar local: o `RF-02-16` cadastra, e nem o PRD-02 nem o PRD-08 declaram edição de
  local. Fora do recorte.
- Catálogo de tipos de coleta (`RF-08-05`) e qualquer escrita de desafio: autoria da App 09.
- Exportação e indicadores públicos do território: são do PRD-08, já entregues em outra ponta.

## Decisions

1. **"Publicado", no `RF-02-17`, é a trilha em situação `publicada`.** Decisão do fundador,
   2026-08-27: o desafio não tem situação própria no modelo, e a trilha é a única publicação do
   domínio. A consulta alcança a trilha por `desafio.missao_id → missao.trilha_id`, o mesmo
   caminho que `criar_etiqueta_ods` e a posse do desafio já usam. _Descartado:_ contar como
   publicado todo desafio gravado (mostraria rascunho de Mestre ao Admin); usar a vigência
   corrente, critério de `/desafios-de-coleta/disponiveis` (é disponibilidade, não publicação).

2. **O vínculo entra na saída de `GET /v1/guerreiros`, não numa rota por Guerreiro(a).** A tela
   que confere é uma lista; uma rota por item custaria uma chamada por linha. `Persona.
   vinculo_vigente` já é relacionamento mapeado, então a saída ganha dois campos e nenhuma
   consulta nova por item. _Descartado:_ `GET /v1/guerreiros/{id}/vinculo`, pelo N+1.

3. **`GET /v1/desafios-de-coleta` é de Admin e não tem filtro de comunidade.** A trilha é bem
   comum da plataforma e não tem coluna de comunidade (`RN-01-42`): exigir o filtro obrigatório
   das consultas de dado de comunidade recortaria por um vínculo que o desafio não tem. A
   contagem de séries ativas sai em agregação única por página — `COUNT` agrupado por
   `desafio_de_coleta_id` sobre os desafios da página, nunca uma consulta por desafio.
   _Descartado:_ derivar a comunidade do desafio pelos locais das séries (inventaria vínculo que
   o modelo não declara).

4. **O alerta do `RF-02-21` vive dentro da área Território, sob a comunidade escolhida.**
   `GET /v1/solicitacoes-de-local/abertas` exige o filtro de comunidade, e um alerta no item de
   navegação obrigaria a varrer todas as comunidades a cada abertura da aplicação. _Descartado:_
   marcador no menu, pelo custo; a área Filas, que a spec de `solicitacao-de-local` já proíbe —
   a solicitação de local não é uma das quatro naturezas e não tem prazo de 7 dias.

5. **Território é área nova do menu; o vínculo fica em Personas.** A área nova reúne o que é do
   território (locais, fila, desafios); o `RF-02-15` é conferência de cadastro e aparece onde a
   lista de Guerreiros e Guerreiras já está. _Descartado:_ pendurar os locais como aba de
   Comunidades (esconderia a fila que precisa alertar).

6. **O cadastro usa o `POST /v1/locais` que existe.** O PRD-08 §9 escreve
   `POST /comunidades/{id}/locais`; o núcleo implementou `POST /v1/locais` com a comunidade no
   corpo, e é isso que a spec `local-do-territorio` consolidou. A fatia consome o que está de
   pé, sem mexer na rota nem reabrir a divergência.

7. **A hierarquia é montada no cliente.** `GET /v1/locais` devolve a lista plana com
   `local_pai_id`, paginada; a App 03 a organiza em árvore para apresentar. Nenhuma rota nova de
   leitura de território. _Descartado:_ rota que devolva a árvore pronta (leitura nova sem RF que
   a peça).

## Risks / Trade-offs

- [A hierarquia montada no cliente quebra se a comunidade tiver mais locais que uma página —
  local cujo pai ficou na página seguinte apareceria órfão, e o seletor de pai sairia
  incompleto] → esta é a **primeira tela da App 03 que precisa da listagem inteira**, e por isso
  é a primeira a seguir o `proximo_cursor` até o fim, num laço na própria função de API. Todas
  as demais leem só a primeira página, e continuam como estão: o laço fica no Território.
- [A contagem de séries ativas envelhece entre uma leitura e outra] → é leitura de
  acompanhamento, não número que autoriza ato; nada no `RF-02-17` depende de ela ser
  transacional.
- [Dois campos novos na saída de `GET /v1/guerreiros` alcançam também quem já consome a rota] →
  são campos acrescentados, nunca renomeados nem removidos; o consumidor que os ignora continua
  válido.
