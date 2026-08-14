## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Décima quinta fatia, na ordem do
documento 99 §9.

**Requisitos atendidos:** `RF-01-02` (consulta pública sem login de pessoa, mediante chave),
`RF-01-33` (consulta pública por nick exato, só de quem tem divulgação autorizada),
`RF-01-34` (sem busca parcial, sugestão ou completação de nick), `RF-01-43` (cobertura de
ODS em rota pública, agregada por comunidade e ciclo), `RF-01-22` (jogos leem progresso e
não têm nenhuma rota de escrita), `RF-01-59` (jogos leem o acumulado de pontos extras, nunca
o saldo disponível), `RN-01-06` (pontos só vêm de realização; o App 04 apenas lê),
`RN-01-10` (Guerreiro(a) aparece publicamente só por avatar e nick, e só com autorização do
responsável), `RN-01-11` (rota pública nunca devolve dado de contato, valor em reais ou
imagem real de criança) e `RN-01-41` (nenhuma rota de jogo expõe o saldo disponível).

As catorze fatias anteriores construíram a escrita e a identidade do núcleo: personas,
sessões, biometria, responsáveis, trilhas, pontuação, equipes, quiz, fila de avaliação,
chaves e auditoria. Nenhuma delas entregou **leitura pública**. O padrão é visível no
código: dos vinte e um módulos de `backend/src/nucleo/`, só sete têm `rotas.py` — o restante
saiu como `modelo.py` e `regra.py`, domínio sem superfície.

Esta change abre essa superfície. Ela vem agora porque tudo de que depende já está no ar: a
chave obrigatória com 401 indistinto, a cota por faixa com 429, o freio por origem e a
invariante de busca exata por nick foram entregues pelas fatias anteriores, que a anunciaram
por escrito — `openspec/specs/persona-e-credencial/spec.md` registra que "a consulta pública
por nick exato (`RF-01-33`) e a ausência de busca parcial na vitrine (`RF-01-34`) são de
outra fatia; esta grava a invariante que aquelas rotas herdam".

O contrato de leitura dos jogos entra junto de propósito. Ele é a mesma superfície com as
mesmas regras de saída — o invariante 8 do documento 99 §6 exige que o personagem do App 04
seja escolhido "estritamente entre os Guerreiros e Guerreiras com divulgação autorizada,
como na vitrine". Separá-lo renderia uma change que repete o mesmo portão e a mesma
projeção pública, só com outro nome.

## What Changes

- Nasce a **leitura pública da vitrine**, em seis rotas sob `/v1/vitrine`, todas sem
  credencial de persona e todas exigindo a chave da aplicação (`RF-01-02`). As rotas são as
  que o PRD-03 §9 enumera e para as quais o núcleo já tem domínio: cards dos Guerreiros e
  Guerreiras, perfil por nick exato, rankings, poderes, criações originais e cobertura
  de ODS.
- Nasce o **portão único da divulgação**: nenhuma superfície pública mostra Guerreiro(a) sem
  consentimento vigente de divulgação, e a ausência dele é indistinguível do nick inexistente
  (`RN-01-10`, `RF-01-33`).
- Nasce a **projeção pública**, uma só, aplicada a toda saída: avatar e nick e mais nada de
  pessoal — sem nome, sem contato, sem valor em reais, sem imagem (`RN-01-10`, `RN-01-11`).
- Nasce o **contrato de leitura dos jogos**: progresso do Guerreiro(a) para montar o
  personagem — pontos regulares, acumulado de pontos extras, poderes, badges e níveis — e
  **nenhuma rota de escrita**, verificável como ausência (`RF-01-22`, `RF-01-59`,
  `RN-01-06`, `RN-01-41`).
- A **cobertura de ODS ganha o eixo do ciclo**, que `RF-01-42` deixou de fora e `RF-01-43`
  exige na rota pública.
- O **`tipo` do consentimento passa a ser enumerado**, com os dois valores que a
  documentação nomeia, e o núcleo ganha o predicado de autorização vigente que o portão
  consulta.
- A **`Persona` ganha o atributo do avatar**, sem o qual `RN-01-10` não tem o que exibir.

### Três deltas em capacidades já consolidadas

Nenhum dos três inventa regra; os três fecham lacuna que a leitura pública torna visível.

| Delta                              | Porque                                                    |
| ---------------------------------- | --------------------------------------------------------- |
| `consentimento`: `tipo` enumerado  | `RN-01-10` exige saber se há autorização; o `tipo` é livre |
| `persona-e-credencial`: avatar     | `RN-01-10` manda exibir avatar, que não existe no núcleo   |
| `etiqueta-ods`: eixo do ciclo      | `RF-01-43` exige o eixo que `RF-01-42` não agregou         |

Os dois valores do `tipo` são os que o PRD-13 nomeia: a **autorização única**, que cobre
divulgação do perfil, imagem em eventos e captação da produção (`RN-13-05`), e a
**biometria** do onboarding, que fica fora dela e tem termo impresso próprio (`RN-13-06`) —
o mesmo consentimento que `RN-01-17` já exige para gravar o _template_. O consentimento
específico do **vínculo de autoria do dado de território** (documento 03 §12.1) fica de
fora: é do PRD-08, e nenhum requisito escrito o define ainda.

O atributo do avatar segue o precedente do nick. A fatia `persona-e-credencial` criou o
atributo e a invariante de unicidade e deixou para o PRD-04 a rota que o escreve; o avatar
nasce aqui pelo mesmo motivo — `RN-01-10` é do PRD-01 —, e as rotas que o gravam e o alteram
seguem sendo do PRD-04 (`RF-04-07`) e do PRD-05 (`RF-05-51`).

### O ciclo é rótulo declarado, não entidade

`Ciclo` não existe como entidade em nenhum PRD, e o "calendário do Ciclo 01" segue pendente
no documento 09 §1. Decisão do fundador: o ciclo entra como **rótulo declarado na
implantação**, com `Ciclo 01` (invariante 13) como valor inicial — mesmo tratamento da
duração da sessão do Guerreiro(a) e do prazo de apresentação da chave. Não é pendência de
produto; é parâmetro de configuração, e a change não trava por causa dele.

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; regras de pontuação,
cadência de coleta e valoração de aporte; captura da imagem, conversa de cadastro e geração
do descritor no aparelho; exclusão do _template_; telemetria da Batalha de Laser e
personalização por IA.

As rotas que o PRD-03 §9 enumera e que **não** têm domínio no núcleo ainda:

| Rota adiada                        | Espera                                          |
| ---------------------------------- | ----------------------------------------------- |
| `GET /v1/vitrine/mestres`          | PRD-09 — nome, apresentação e comprobatórios    |
| `GET /v1/vitrine/apoiadores`       | PRD-07 e PRD-14 — aportes homologados em moedas |
| `GET /v1/vitrine/batalhas`         | PRD-10 — partida e telemetria                   |
| `GET /v1/vitrine/necessidades`     | PRD-07 — recursos e lastro                      |
| `GET /v1/comunidades` e `/series`  | PRD-08 — território e séries temporais          |
| `GET /v1/comunidades/{id}/ods`     | PRD-08 — depende da comunidade acima            |
| `POST /v1/assistente-do-desenvolvedor` | PRD-11 — personalização por IA              |
| `GET /v1/vitrine/conteudo-institucional` | PRD-03 — conteúdo editorial da vitrine    |

O que é do PRD-01 mas de outra fatia:

| Fica para                                      | Porque                             |
| ---------------------------------------------- | ---------------------------------- |
| `RF-01-24`, `RF-01-58`, `RF-01-60`             | livro-razão, PRD-07                |
| `RF-01-66`, `RN-01-08`, `RN-01-09`, `RN-01-26`, `RN-01-47` | território e entrega do conjunto, PRD-08 |
| `RF-01-41`                                     | desafio extra, PRD-14              |
| `RF-01-44`                                     | trava de publicação do Ciclo 02    |
| `RF-01-31`                                     | PRD-01 §14, pendência declarada    |

Fica fora também a **agregação mínima dentro do bairro**, pendência aberta no documento 09
§1: ela alcança as séries do território, que não entram aqui.

## Capabilities

### New Capabilities

- `leitura-publica-da-vitrine`: as seis rotas de consulta pública, o portão único do
  consentimento de divulgação, a projeção pública de avatar e nick sem dado pessoal, o
  404 indistinto entre nick inexistente e nick sem autorização, e a cobertura de ODS
  agregada por comunidade e ciclo.
- `contrato-de-leitura-dos-jogos`: o que o App 04 lê para montar o personagem, o mesmo
  portão da divulgação, a exposição do acumulado de pontos extras com o saldo disponível
  fora de alcance, e a ausência verificável de qualquer rota de escrita para jogos.

### Modified Capabilities

- `consentimento`: o `tipo` deixa de ser texto livre e passa a enumerar os dois valores que
  o PRD-13 nomeia; nasce o predicado de autorização vigente, derivado do histórico somente
  inserção que a capacidade já grava — a decisão mais recente por tipo é a que vale, e a
  revogação vale para frente sem apagar o passado.
- `persona-e-credencial`: a `Persona` de Guerreiro(a) ganha as características do avatar,
  atributo obrigatório da exibição pública. A capacidade já guarda o nick com a mesma
  divisão de responsabilidade: o atributo nasce aqui, a rota que o escreve é de outro PRD.
- `etiqueta-ods`: a cobertura passa a agregar também por **ciclo**, quarto eixo que
  `RF-01-42` enuncia e a spec vigente não implementou, e sem o qual `RF-01-43` não se
  cumpre.

## Impact

- `backend/src/nucleo/`: módulo novo `vitrine/` — as seis rotas, a projeção pública e o
  portão da divulgação. Módulo novo `jogos/` — a leitura de progresso do App 04. Os dois
  leem `personas`, `consentimentos`, `pontuacao`, `ponto_extra`, `poderes`, `trilhas`,
  `criacoes_originais` e `ods`, e não escrevem em nenhum.
- `backend/src/nucleo/consentimentos/`: `tipo` vira enumeração; nasce a consulta de
  autorização vigente em `regra.py`. Migração do Alembic para a coluna.
- `backend/src/nucleo/personas/`: atributo do avatar na `Persona`. Migração do Alembic.
- `backend/src/nucleo/ods/regra.py`: quarto eixo de agregação.
- `backend/src/nucleo/principal.py`: registra os dois roteadores novos.
- `backend/tests/`: além dos testes de cada rota, dois testes de **ausência** — nenhuma rota
  de escrita para jogos (`RF-01-22`) e nenhuma saída pública com o saldo disponível
  (`RN-01-41`).
- `docs/`: nada a atualizar por decisão nova. Ver a questão aberta abaixo sobre o parâmetro
  do rótulo de ciclo. `docs/prds/index.md` não muda de situação: o PRD-01 segue "aprovado",
  fatiado em changes.

## Questões que ficam para o `design.md`

1. **Como a projeção pública se torna difícil de furar.** A regra é sempre a mesma — avatar,
   nick e progressão, nada mais —, e ela vale em seis rotas e no contrato dos jogos.
   Repetir a seleção de campos em cada rota é o caminho que erra; a alternativa é uma
   projeção única por onde toda saída pública passa. É desenho de execução, não regra.
2. **Onde o portão da divulgação se prende.** Ele filtra listagem (cards, rankings, elenco
   do jogo) e decide o 404 do perfil por nick. Um mesmo predicado nos dois usos, ou um
   filtro de consulta e uma guarda de rota.
3. **Como se resolve a autorização vigente** sobre um histórico somente inserção com até
   três responsáveis por Guerreiro(a), lembrando que `RN-13-07` manda a recusa prevalecer.

## Questão aberta para o fundador

O **rótulo de ciclo** entra como parâmetro de implantação, decidido acima. O PRD-01 §13
registra os parâmetros dessa natureza em linha própria — a duração da sessão e o limiar da
biometria estão lá, com origem no documento 03 e entrada no documento 09. Se o rótulo de
ciclo deve receber o mesmo tratamento, é uma edição de uma linha em cada um dos três, e esta
change a carrega. Se for parâmetro de operação sem registro normativo, `docs/` não muda.
Confirme antes do `/opsx:apply`.
