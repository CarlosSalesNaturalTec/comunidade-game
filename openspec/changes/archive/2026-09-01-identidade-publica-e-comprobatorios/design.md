## Context

A identidade do adulto já é capacidade consolidada: `PUT /v1/eu/apoiador/identidade` grava o
nick, `GET /v1/nicks/disponibilidade` confere com sugestões e a unicidade é do índice
insensível a caixa da tabela `nick` (`openspec/specs/identidade-do-adulto/spec.md`). O
comprobatório do adulto também: `ArtefatoComprobatorio` é satélite da `Persona`, com endereço,
rótulo e `declarado_por_id`, e o Mestre já o publica pela `prova-de-habilidade`. A coluna
`Persona.avatar` existe desde a primeira fatia do PRD-01, opaca ao núcleo, e **nenhuma rota a
grava**. `GET /v1/meus-aportes` já devolve os aportes do Apoiador em moedas.

O que falta é o avatar, o piso que o libera e o ciclo de dois atos do documento comprobatório.
Motivação em `proposal.md`.

## Goals / Non-Goals

**Goals:** o avatar do Apoiador gravado sob o piso de 10 moedas que não regride, o documento
comprobatório nascendo pendente com o ato de Admin que o publica, e as duas telas da App 08.

**Non-Goals:** entidade nova, armazenamento de arquivo, a fila e a tela da App 03 (fatia 16 do
PRD-02), o card na vitrine (PRD-03) e a auditoria por amostragem do avatar e do nick.

## Decisions

1. **O piso mede a soma dos aportes homologados, não o Poder Sustentador.** Derivação nova
   `moedas_acumuladas_de` em `poder_sustentador/regra.py`, vizinha da que já existe: soma
   `Aporte.valor_em_moedas` do provedor, sem olhar lançamento de ajuste. Descartado: reaproveitar
   `poder_sustentador_de`, que o ressarcimento pago derruba — o `RN-14-11` diz que o direito
   alcançado não regride, e o `RN-07-15` diz que o Poder Sustentador regride: são duas leituras
   diferentes do mesmo aporte, e confundi-las tiraria o avatar de quem já o tem.
2. **O avatar entra na rota de identidade que já existe**, como o PRD-01 §9 declara: o `PUT`
   passa a aceitar nick e avatar, cada um opcional, e ganha o `GET` correspondente com nick,
   avatar, moedas acumuladas e o que falta para o piso. Descartado: rota própria de avatar — o
   `PATCH /v1/eu/avatar` é do Guerreiro(a), no PRD-05, com semântica de características, não de
   imagem.
3. **O avatar viaja como texto opaco**, o endereço da imagem que o Apoiador declara, no mesmo
   precedente da coluna: o núcleo não valida forma, não guarda arquivo e não serve imagem.
   Descartado: envio de arquivo para o Cloud Storage — nenhum documento decide armazenamento de
   avatar, e o documento 02 §1 já mantém anexo de arquivo fora do Ciclo 01 para a prova do
   adulto.
4. **O documento do Apoiador é `ArtefatoComprobatorio`**, que ganha `anexado_por_id` e
   `anexado_em`, nulos enquanto pendente. Descartado: entidade de fila própria, que duplicaria
   endereço e rótulo e obrigaria a copiar o registro na anexação, perdendo a data do envio.
5. **Pendente é só o que o próprio Apoiador declarou e ninguém anexou.** A exigência de anexação
   é do Apoiador (`RN-14-12`), não do Mestre (`RF-09-66`) e não do que o Admin declarou no
   cadastro: esses seguem públicos no ato, com as colunas novas vazias. Descartado: publicar por
   `anexado_em` preenchido em todo artefato, o que obrigaria a reescrever os já gravados e a
   inventar um "anexador" para o Mestre que publica a si mesmo.
6. **As rotas seguem o PRD-14 §9 onde ele as declara.** `POST /v1/eu/apoiador/documentos` é a do
   PRD; o `GET` da mesma rota atende o `RF-14-20`, e a anexação é
   `POST /v1/apoiadores/{id}/artefatos/{artefato_id}/anexacao`, no molde do
   `POST /v1/consentimentos/{id}/anexo` que o Admin já usa. Descartado: reaproveitar
   `/v1/mestres/{id}/artefatos`, cujo alcance é do Mestre e cuja publicação é imediata.
7. **Erro novo `PisoDeMoedasNaoAlcancado`**, 409 com quantas moedas faltam, no molde dos demais
   409 de `erros.py`. O 409 e a mensagem são os que o PRD-14 §9 prevê.
8. **A App 08 ganha duas áreas na navegação que `App.tsx` já monta**, sem roteador, como as
   demais aplicações.

Nada aqui tem custo de nuvem novo e nenhum dado de território é tocado; o envio de documento e a
gravação de avatar não geram lançamento no livro-razão — quem gera é a homologação do aporte
(`RN-14-07`).

## Risks / Trade-offs

- **O avatar padrão do projeto depende da marca gráfica**, pendência aberta do documento 09. A
  App 08 o apresenta como marca neutra na moldura comum do documento 11 §8.2, trocada quando a
  marca existir; não é decisão nova nem trava o `RF-14-15`.
- **O Admin anexa sem fila.** A rota existe e é testada, mas a lista dos documentos pendentes é
  da fatia 16 do PRD-02: até lá o Admin precisa do identificador do documento. É o preço de não
  antecipar tela de outra aplicação.
- **O avatar é endereço declarado**, e imagem que sai do ar quebra o card. É a mesma exposição do
  artefato comprobatório, que o documento 02 §1 aceita em troca de prova verificável por
  qualquer visitante.

## Migration Plan

Uma migração Alembic acrescenta `anexado_por_id` e `anexado_em` a `artefato_comprobatorio`,
nulos, **sem reescrever linha alguma**: pela decisão 5, artefato de Mestre e artefato declarado
por Admin no cadastro seguem públicos com as colunas vazias, e nenhum dos já gravados foi
declarado pelo próprio Apoiador. O `downgrade` remove as duas colunas.
