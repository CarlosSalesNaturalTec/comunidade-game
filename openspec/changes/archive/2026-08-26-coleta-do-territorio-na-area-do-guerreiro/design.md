## Context

Ver `proposal.md` — Why. O território já está inteiro no núcleo: as capacidades
`serie-de-coleta`, `registro-de-coleta`, `desafio-de-coleta`, `auditoria-da-coleta`,
`local-do-territorio` e `solicitacao-de-local` cobrem abertura, cadência, faixa, interrupção,
mídia, invalidação e pedido de local. Falta **porta de leitura** por onde a criança chegue, e
falta a aplicação. A App 05 nasceu na fatia anterior com `comum/` já ligado — cliente de API,
_tokens_, fontes e a sessão do Guerreiro(a).

## Goals / Non-Goals

**Goals**

- Quatro leituras no núcleo, todas derivadas de regra existente, sem entidade nova e sem
  migração de dados.
- O bloco da coleta na App 05, do abrir série ao histórico.

**Non-Goals**

- Nenhuma escrita nova no núcleo: `POST /v1/series-de-coleta`, `POST /v1/registros-de-coleta` e
  `POST /v1/solicitacoes-de-local` entram como estão.
- Nada de credencial de dispositivo do sensor: é caminho do PRD-08, não desta aplicação.
- Nenhum trabalho em modo desconectado além de recusar o registro (`RF-05-85`).

## Decisions

**1. O ditado por voz é transcrito no aparelho.** Decisão do fundador, 2026-08-26: a API de voz
do navegador transcreve e ao núcleo vai só o número, com origem `voz`. Segue o precedente da
biometria — processa no aparelho, ao núcleo vai o resultado —, não gera custo de nuvem e não
põe áudio de criança em trânsito. _Descartadas:_ transcrever no núcleo por Gemini (cresce a
fatia e cria custo de _cloud_ para o que o navegador já faz); adiar a voz para o Ciclo 02
(deixaria `RF-05-33` parcial sem necessidade). A decisão é gravada no documento 03 e movida no
documento 09 nesta mesma change.

**2. Foto e vídeo são a mídia do registro, não uma origem.** O `RF-05-33` lista quatro
maneiras — digitado, voz, foto, vídeo —, e o núcleo as modela em dois eixos: `origem`
(`manual` ou `voz`) e a **forma de registro do tipo de coleta** (`numero`, `foto`, `video`). A
aplicação aplica a leitura já consolidada em `registro-de-coleta`: a forma do tipo decide o que
a tela pede, a origem grava como o número chegou. Não é regra nova — é o mesmo requisito lido
contra o modelo que já existe.

**3. A próxima medição é derivada no núcleo, pela régua que já existe.** `periodo_de_cadencia`
é o ponto único de apuração do período civil, e a interrupção já conta por ele. A próxima
medição sai do mesmo lugar: início do período seguinte ao da última medição válida, ou o
período corrente quando não há medição válida. Derivar no aplicativo duplicaria a régua e
divergiria dela no fuso e no mês. _Descartada:_ coluna gravada na série — seria estado
derivável guardado, contra o desenho da capacidade.

**4. Os desafios elegíveis saem das mesmas condições que a abertura confere.** A leitura não
reimplementa vigência nem teto de granularidade: extrai de `abrir_serie_de_coleta` o predicado
e o compartilha, para que a lista jamais ofereça o que a abertura recusaria. _Descartada:_
consulta própria com as condições reescritas — divergiria na primeira mudança de regra.

**5. As rotas seguem a convenção do núcleo, não a tabela do PRD-05 §9.** A §9 do PRD-05 nomeia
`GET /v1/eu/series` e `POST /v1/series/{id}/registros`, escritas antes de o PRD-08 entrar; o
núcleo entregou `GET /v1/series-de-coleta/minhas` e `POST /v1/registros-de-coleta`, no padrão
`/minhas` de `minhas-turmas`, `necessidades/minhas` e `meus-aportes`. As rotas novas seguem o
que existe:

| Rota                                     | Requisito                |
| ---------------------------------------- | ------------------------ |
| `GET /v1/series-de-coleta/{id}/registros` | `RF-05-37`, `RF-05-38`  |
| `GET /v1/desafios-de-coleta/disponiveis`  | `RF-05-30`              |
| `GET /v1/solicitacoes-de-local/minhas`    | `RF-05-32`              |

É correção de redação do PRD-05 §9, não decisão nova — mesmo precedente do `RF-04-41`,
corrigido na sexta fatia do PRD-04.

**6. Sem rede, recusa na hora.** Nenhum _service worker_ de fila, nenhum armazenamento local da
medição: a tela detecta a falha da chamada e explica (`RF-05-85`, decisão já gravada no
PRD-05 §13). A mídia escolhida é descartada com a recusa.

**7. As leituras novas ficam nos módulos que já as sustentam.** As três de coleta em
`backend/src/nucleo/coletas/`, a das solicitações em `backend/src/nucleo/locais/` — nenhum
módulo novo, nenhuma pasta de topo nova.

## Risks / Trade-offs

- **A API de voz do navegador não existe em todo aparelho modesto** → o ditado é oferecido
  apenas quando o navegador o suporta; a digitação continua sendo o caminho sempre disponível,
  e a ausência da voz nunca impede o registro.
- **A lista de desafios elegíveis pode envelhecer entre a leitura e a abertura** (vigência que
  vence no intervalo) → a abertura continua sendo a autoridade; a tela explica a recusa em
  linguagem simples, e a lista é relida depois dela.
- **O histórico de uma série longa cresce sem limite** → a leitura nasce paginada por cursor,
  como toda listagem do núcleo.
- **A criança pode ler o motivo da invalidação como acusação** → o texto da tela separa o que é
  do Mestre (o motivo) do que é da série (segue valendo), e o `RF-05-35` já obriga a explicação
  sem acusação no caso irmão, do "a conferir".

## Migration Plan

Nenhuma migração de esquema: as quatro leituras são consultas sobre tabelas existentes, e o
único campo novo em saída é a próxima medição, derivada. As rotas novas são aditivas; nenhum
contrato existente muda.
