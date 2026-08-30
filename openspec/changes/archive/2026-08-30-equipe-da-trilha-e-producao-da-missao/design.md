## Context

Ver `proposal.md` — Why. O que já está de pé e condiciona o desenho:

- `openspec/specs/equipe/spec.md` tem a **regra inteira** das duas equipes — criação pelo
  Guerreiro(a), tetos de composição, equipe única por trilha, homologação que congela — e o
  backend a implementa em `equipes/regra.py`. Falta só a **porta HTTP** da equipe da trilha.
- `Operacao.homologacao_da_equipe_da_trilha` já está na matriz de `permissoes.py`, no Mestre.
- `openspec/specs/template-da-missao/spec.md` e `backend/src/nucleo/template_de_missao/`
  estabeleceram o padrão de chamada a modelo: `porta.py` abstrata, `local.py` fora de
  produção, `nuvem.py` com Gemini, `fabrica.py` escolhendo pelo ambiente, `None` como
  indisponibilidade e **nenhum lançamento de custo por ato**.
- `coletas/rotas.py` estabeleceu o padrão de entrada `multipart/form-data` com `UploadFile`.
- A equipe da aula já declara a **atividade corrente** (`equipes/regra.py`), e a `Atividade` já
  carrega `producao_esperada`.

## Goals / Non-Goals

**Goals:**

- Dar porta HTTP ao que o núcleo já sabe fazer com a equipe da trilha, sem tocar na regra.
- Pôr de pé a `ProducaoDaMissao` inteira, como o PRD-05 §8 a declara, com o vínculo de equipe
  que a decisão de 2026-08-30 acrescentou.
- Garantir, no código, que foto e áudio não sobrevivem à leitura.

**Non-Goals:**

- Corpus fechado, guardrails e recusa fora do corpus: são do **assistente** (fatia 10), não da
  devolutiva.
- Porta individual da produção (`POST /v1/eu/missoes/{id}/producao`): fatia 7 do PRD-05.
- Qualquer crédito, `Resultado` ou progressão a partir da entrega.

## Decisions

**1. A produção pendura na equipe da aula e na atividade corrente, não na missão solta.**
A rota é `POST /v1/equipes/{id}/producao` e a missão vem da `atividade_corrente_id` que a
equipe já declarou. Descartado ancorar na missão pelo caminho do PRD-05
(`/v1/eu/missoes/{id}/producao`): no encontro quem produz é a equipe, e a missão sem a
atividade perderia a `producao_esperada` que diz o que entregar.

**2. A entidade nasce com a restrição "equipe ou Guerreiro(a), nunca os dois em branco".**
`ProducaoDaMissao` guarda `equipe_id` e `guerreiro_id`, exatamente um preenchido — o mesmo
desenho de `Equipe`, que é de aula **ou** de trilha. A entrega do App 01 preenche a equipe; a
fatia 7 do PRD-05 preencherá o Guerreiro(a), sem migração nova. Descartado gravar uma linha por
integrante: repetiria a mesma transcrição cinco vezes e faria a devolutiva parecer individual.

**3. `multipart/form-data`, com a foto e o áudio lidos em memória e nunca escritos.**
`forma` e `texto` chegam por `Form`, `arquivo` por `UploadFile`. O byte lido vai direto à porta
da leitura e sai de escopo; o módulo `armazenamento` **não é chamado** e o caminho não passa
por disco nem por Cloud Storage. Nenhum `log` recebe o conteúdo — o tratador de erro registra a
forma e o tamanho, nunca o byte. É o `RF-04-46` virando ausência de código, não configuração.

**4. Uma porta só para a leitura e a devolutiva, no padrão do template de missão.**
`PortaDaProducaoDaMissao.ler(forma, texto, arquivo, producao_esperada) -> LeituraDaProducao |
None`, devolvendo `transcricao` e `devolutiva`. Um par de chamadas (transcrever, depois
comentar) foi descartado: Gemini é multimodal e a mesma passada lê e comenta, com metade da
latência num encontro presencial. `local.py` fora de produção devolve o eco do texto e uma
devolutiva fixa; `nuvem.py` chama o Gemini em produção; `fabrica.py` escolhe pelo ambiente.

**5. `None` significa coisas diferentes conforme a forma da entrega.**
No texto, a transcrição existe sem o modelo: grava com devolutiva em branco e responde 201. No
áudio e na foto, sem leitura não há nada a gravar: responde **503** e não grava. Descartado
gravar registro vazio para foto e áudio — guardaria a prova de que houve entrega e perderia o
que ela dizia, com o arquivo já descartado.

**6. Nenhuma operação nova na matriz para a fatia 8; uma para a fatia 9.**
`POST /v1/trilhas/{id}/equipes` reusa `Operacao.equipe_que_forma_na_aula`, que já protege
`POST /v1/equipes/{id}/integrantes` e `DELETE .../eu` — as duas já servem equipe de aula e de
trilha. Renomear a operação foi descartado: mexeria na matriz inteira por uma fatia que não
muda permissão de ninguém. A entrega da produção ganha `Operacao.producao_da_equipe`, no
Guerreiro(a), que é o que devolve **403** a Mestre e Admin.

**7. A trilha entra no item da programação, sem rota nova.**
`ItemDaProgramacaoSaida` ganha `trilha_id` e `trilha_titulo`. Uma rota "trilhas do encontro"
foi descartada: seria uma segunda leitura da mesma coisa, e o aparelho já carrega a
programação para mostrar a missão.

**8. O App 01 põe as duas telas dentro do caminho das trilhas que já existe.**
`TelaDaProgramacao` ganha, na atividade corrente, a formação da equipe da trilha e a entrega da
produção; a homologação aparece quando quem está no aparelho é o **Mestre em sessão de
trabalho**, que a `AparelhoDaAula` já conhece. Nenhuma tela nova de topo — o encontro tem um
aparelho por equipe, e navegação a mais é atrito na aula.

## Risks / Trade-offs

- **A foto do manuscrito volta transcrição pobre, e a devolutiva comenta o que não foi escrito**
  → a `producao_esperada` da atividade vai no pedido, e a devolutiva é construtiva por
  contrato: aponta o próximo passo, nunca reprova. O resultado continua sendo do Mestre.
- **Latência do modelo trava a fila do aparelho no encontro** → a entrega é ato único por
  atividade, e a indisponibilidade tem desfecho declarado (decisão 5) em vez de espera.
- **A produção da equipe fica sem dono quando a aula encerra** → ela pendura na equipe, e a
  equipe da aula preserva o que realizou ligado a cada integrante (`equipe`, requisito da aula
  que encerra). O histórico não se perde com a composição.
- **Homologar no mesmo aparelho em que as crianças se autenticam** → a homologação corre sob a
  **sessão de trabalho**, que é do Mestre e vale pela janela da aula; a sessão do Guerreiro(a)
  não a alcança, e a matriz devolve 403.

## Migration Plan

Uma migração Alembic: a tabela `producao_da_missao`, com `equipe_id` e `guerreiro_id`
anuláveis e a restrição de exatamente um preenchido. Nada a preencher em registro antigo, e
nada a reverter além da tabela.
