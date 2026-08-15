## Why

**PRD de origem:** PRD-08 — Comunidades Virtuais e dados do território. Sétima fatia dele e
vigésima terceira da esteira, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-08-16` (rota pública devolve a série histórica da comunidade
agregada até o bairro, sem coletor), `RF-08-28` e `RN-08-24` (recorte publicado com menos de
três coletores distintos sobe para o nível acima), `RN-08-12` (anonimização na saída, nunca no
armazenamento), `RN-08-13` (a saída pública para no bairro; rua e abaixo só em entrega
aprovada) e, do PRD-01, `RF-01-28` (listagem paginada com filtro por período), `RF-01-02` e
`RN-01-32` (rota pública sem credencial de persona, nunca sem chave de aplicação).

O território já está todo gravado e ainda não sai. As seis fatias anteriores do PRD-08
construíram a comunidade, a hierarquia de locais, o catálogo de tipos, o desafio, a série, o
registro e o ciclo de vida da série — e a única leitura que existe hoje é a do próprio coletor,
`GET /v1/series-de-coleta/minhas`, presa à sessão dele. **Nenhum dado do território é
consultável por quem está de fora**, que é a razão de o dado existir: o documento 02 §1 põe a
saída pública agregada como a contrapartida da guarda permanente com o coletor identificado.

É também a fatia que fecha o invariante 7 do documento 99 §6. Ele tem duas metades — guarda
permanente com autoria, e anonimização **na saída** — e só a primeira está implementada. Sem
superfície de saída, a segunda metade não tem onde recair, e o `RN-08-12` permanece regra sem
código que a exerça.

### Por que agora, e não a auditoria

A ordem natural seria a auditoria por amostragem (`RF-08-13`), que é o outro requisito
essencial em aberto do PRD-08. Ela **não entra** porque `RF-08-13` manda a invalidação
**estornar** os pontos, e `RF-01-57`, `RN-01-38` e o invariante 23 do documento 99 §6 dizem que
ponto regular **nunca é debitado, em nenhuma hipótese**. A contradição é de nível 1 — está
dentro do próprio documento 11 §5, que afirma as duas coisas — e já foi implementada num dos
lados: `PontoRegular` tem `CheckConstraint total >= 0` e gatilho no banco que recusa qualquer
redução, e a capacidade `pontos-niveis-e-badges` grava isso como requisito. Não se resolve
dentro de um artefato do OpenSpec: foi levada ao fundador e a change espera a decisão.

Esta fatia não depende dela. A leitura pública conta **registro válido**, e `SituacaoDoRegistro`
já nasceu preparado para o valor `invalidada` que a fatia da auditoria acrescenta — o filtro
nasce escrito certo e passa a excluir sozinho o que aquela fatia vier a marcar.

## What Changes

- Nasce a **leitura pública do território**: rota de consulta da série histórica de uma
  comunidade, **sem credencial de persona** e com **chave de aplicação obrigatória**, na mesma
  régua que a vitrine já usa (`RF-08-16`, `RF-01-02`, `RN-01-32`).
- A saída é **agregada por tipo de coleta e por local**, e **para no bairro**: nenhum recorte de
  rua, condomínio, bloco ou quadra sai por esta rota, qualquer que seja o parâmetro recebido
  (`RN-08-13`).
- A saída **não leva coletor**: nem identificador, nem nick, nem avatar, nem contagem que
  isole um. O vínculo de autoria continua gravado — a anonimização é da saída, não do
  armazenamento (`RN-08-12`, invariante 7 do documento 99 §6).
- O **piso de três coletores distintos** passa a valer no recorte publicado: recorte abaixo do
  piso **soma-se ao nível acima** até alcançá-lo, e o que não alcança nem no topo **não sai**
  (`RF-08-28`, `RN-08-24`). O piso é **parâmetro de configuração**, com três como valor
  inicial, exatamente como o documento 02 §1 o declara.
- A consulta é **paginada e filtrável por período**, no contrato de listagem do núcleo:
  `cursor`, `tamanho`, `periodo_inicio`, `periodo_fim`, e **422** para parâmetro não declarado
  (`RF-01-28`).
- A rota de **leitura da comunidade** passa a existir em público, devolvendo a comunidade, os
  **locais até o bairro** e os **tipos de coleta ativos** nela — o que o PRD-08 §9 descreve
  para `GET /comunidades/{id}` e o que torna a série consultável por quem não conhece os
  identificadores.
- Apenas registro de situação **válida** entra na agregação.

### Fora do escopo

O que o PRD-08 §3.2 já exclui segue excluído — importação de fontes públicas, GPS por
coordenada, interface das telas e escolha do banco de séries. Além disso, e por recorte desta
fatia:

| Fica para                          | Porque                                                            |
| ---------------------------------- | ----------------------------------------------------------------- |
| `RF-08-13`, `RN-08-09`, `RN-08-20` | auditoria e invalidação: travadas pela contradição do estorno     |
| `RF-08-19`, `RF-08-27`             | exportação a instituições e declaração da meta 17.18              |
| `RF-08-26`                         | cobertura de ODS **das séries** no painel da comunidade           |
| `RF-08-20`                         | crescimento visual do painel: é frontend, documento 11 §8.3       |
| `RF-08-18`                         | consulta do responsável pela App 07: é PRD-13                     |
| `RN-08-19`                         | despersonalização por revogação do consentimento                  |
| `RF-08-03`                         | transferência entre comunidades: fora do Ciclo 01 por decisão     |
| mídia do registro em público       | o PRD-08 §11 a condiciona à auditoria, que ainda não existe       |

O `GET /comunidades` do PRD-08 §9 — "lista comunidades com indicadores agregados" — **não
entra**: o PRD nomeia a rota mas não declara **quais** indicadores ela devolve, e um artefato do
OpenSpec não inventa a lista. Vira pergunta ao fundador, junto com a do estorno.

A entrega de dados abaixo do bairro mediante aprovação de Admin (documento 03 §12.3) também
fica de fora: é outra superfície, com outra autorização, e `RN-08-13` só a menciona para dizer
que **não** é esta.

## Capabilities

### New Capabilities

- `leitura-publica-do-territorio`: a saída pública do dado do território — a rota que dispensa
  credencial de persona e nunca a chave; a agregação por tipo de coleta e local que **para no
  bairro**; a ausência de coletor em toda a resposta; o piso de três coletores distintos, com a
  subida ao nível acima e a supressão do recorte que não o alcança nem no topo; o recorte por
  período e a paginação por cursor; e a leitura pública da comunidade com os seus locais até o
  bairro e os tipos de coleta ativos.

### Modified Capabilities

Nenhuma. A fatia é **somente leitura**: não altera requisito de `serie-de-coleta`, de
`registro-de-coleta` nem de `local-do-territorio`, e a exigência de chave sem persona já está
escrita em `chave-de-aplicacao` e em `permissoes-e-escopo-de-comunidade` na forma que esta rota
apenas aplica.

## Impact

- `backend/src/nucleo/coletas/`: a agregação da série pública — a consulta que soma registros
  válidos por tipo e local, conta coletores distintos e aplica o piso.
- `backend/src/nucleo/comunidades/rotas.py`: a leitura pública da comunidade, com os locais até
  o bairro e os tipos de coleta ativos.
- `backend/src/nucleo/configuracao.py`: o piso de coletores distintos do recorte publicado,
  com três como valor inicial.
- `backend/src/nucleo/principal.py`: as rotas novas, sob o prefixo de versão e sem dependência
  de persona.
- `backend/tests/`: recorte de bairro com três coletores que sai; recorte com dois que sobe
  para a comunidade; recorte que não alcança o piso nem no topo e não sai; ausência de coletor
  em toda a resposta; recusa de nível abaixo do bairro; consulta sem chave recusada com 401;
  consulta sem sessão aceita; parâmetro não declarado recusado com 422; registro invalidado
  fora da agregação quando a situação existir.
- `docs/`: nenhuma decisão de produto nova — o piso de três e a linha de corte no bairro já
  estão no documento 02 §1, e o documento 09 já os lista como decididos. Muda apenas
  `docs/prds/index.md`, na nota de situação do PRD-08, se ela precisar refletir o que resta.
  O documento 99 não muda: nenhuma relação entre documentos foi alterada.

## Perguntas que seguem com o fundador

Não travam esta fatia — travam as seguintes, e estão aqui para não se perderem.

1. **Estorno versus ponto regular que nunca decresce.** `RF-08-13` e o critério de aceite do
   PRD-08 §12 mandam a invalidação reduzir o saldo; `RF-01-57`, `RN-01-38` e o invariante 23
   dizem que ponto regular nunca é debitado. Trava `RF-08-13` inteiro.
2. **"A conferir" credita na hora ou espera o Mestre?** O documento 02 §1 afirma as duas
   coisas em bullets vizinhos, e o documento 11 §5 repete a segunda. O PRD-08 §5.3 resolveu por
   "credita na hora" e o código seguiu; se a leitura correta for a outra, a fatia da auditoria
   ganha um ato de **confirmação** que nenhum RF hoje declara.
3. **Quais indicadores agregados** o `GET /comunidades` do PRD-08 §9 devolve.
