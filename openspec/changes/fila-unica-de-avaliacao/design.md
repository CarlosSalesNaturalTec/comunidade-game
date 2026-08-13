## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta do que já está no ar:

- O **freio por origem** existe como _dependency_ de rota,
  `exigir_freio_por_origem("<superficie>")`, com as superfícies `formulario_participacao` e
  `formulario_dados` já registradas e sem nenhuma rota que as declare. Ao contrário da cota,
  ele **não é transversal**: cada rota declara a sua.
- A **chave de aplicação** e a **cota de leitura** entram por `incluir_roteador_de_dados`, de
  modo que todo roteador novo sob `/v1` nasce protegido sem declarar nada.
- A **auditoria** é _middleware_ e alcança toda escrita bem-sucedida sozinha.
- A **matriz de permissões** é dado, em `Operacao` e `MATRIZ_DE_PERMISSOES`. As operações de
  proposta das personas já existem — `suas_sugestoes`, `solicitacoes_e_propostas`,
  `propostas_de_evolucao` —, e falta apenas a do Mestre, cuja ausência era contradição entre
  o documento 03 §11 e o PRD-01 §4, corrigida pelo fundador no commit que antecede esta
  change.
- O módulo `ponto_extra` só conhece **fontes duplas**, e o valor de cada fonte é constante de
  `regra.py`.
- **Nenhum módulo toca armazenamento de arquivo.** O comprovante do pré-cadastro é o primeiro
  binário que o núcleo recebe.

## Goals / Non-Goals

**Goals:**

- Um ciclo de avaliação só, aplicado às quatro naturezas sem que nenhuma perca os campos que
  o PRD-01 §8 lhe dá.
- Rotas de envio que **não conseguem** criar acesso, por construção e não por disciplina.
- O crédito da proposta adotada na mesma transação do desfecho, sem caminho que credite duas
  vezes.

**Non-Goals:**

- Leitura da fila pela gestão além do necessário para o desfecho: a tela é do PRD-02.
- Qualquer geração de arquivo de exportação — ver `proposal.md`.
- Notificação a quem enviou: não existe no Ciclo 01.

## Decisions

### Quatro tabelas com um _mixin_ de ciclo, não tabela única

Cada natureza vira a sua tabela, com os campos que o PRD-01 §8 lhe atribui, e o ciclo comum
— situação, prazo, quem avaliou, parecer, data do desfecho — entra por um _mixin_
`EmAvaliacao`, no mesmo idioma do `ComAutoria` já usado no núcleo.

O PRD nomeia quatro entidades com atributos próprios e bem diferentes entre si; fundi-las
custaria colunas nulas em massa e apagaria do modelo o que cada natureza exige. A fila
"única" é **única na avaliação, não no armazenamento** — o que a App 03 precisa é de uma
visão, e visão é problema de leitura.

- _Alternativa descartada:_ tabela única com discriminador e carga em JSON — perde restrição
  de coluna e esconde do banco os campos que o PRD declara.
- _Alternativa descartada:_ herança por junção, com tabela-base e quatro filhas — acrescenta
  junção a toda leitura sem ganho nesta escala.

### Dois enums de situação, porque o desfecho tem vocabulário próprio

As três solicitações terminam em **aceita** ou **recusada**; a sugestão termina em **adotada**
ou **não adotada** (PRD-05 §5.8). São palavras do domínio, e o projeto não as renomeia. Ficam
`SituacaoDaSolicitacao` e `SituacaoDaSugestao`, ambas abrindo em `recebida` e passando por
`em_avaliacao`.

- _Alternativa descartada:_ um enum só com a união dos estados — permitiria gravar "adotada"
  numa solicitação de chave.

### O prazo de 7 dias é constante do módulo, não parâmetro de configuração

O prazo é promessa de produto escrita nos documentos 02 §1 e 03 §§7, 12.3, não afinação de
operação. Segue o precedente do `ponto_extra`, cujos valores do documento 11 §5 são constantes
de `regra.py` — e não o da proteção das rotas, cujos números vêm da tabela operacional do
documento 03 §8 e vivem em `Configuracao`.

O prazo é **gravado na linha** no momento do registro, não calculado na leitura: o desfecho
precisa ser julgado contra o prazo que valia quando a solicitação entrou.

### O atraso é derivado, não é uma situação

"Em atraso" não vira estado gravado: é `prazo < agora` numa solicitação sem desfecho. Estado
gravado exigiria alguém para virá-lo — tarefa periódica que o Ciclo 01 não tem — e criaria
duas fontes de verdade para o mesmo fato.

### O comprovante vai para uma porta de armazenamento, e o registro guarda a referência

Nasce `armazenamento/`, com uma interface mínima — gravar, ler, remover — e dois adaptadores:
**disco** em desenvolvimento e **Cloud Storage** em produção (documento 03 §1), escolhidos por
configuração. O registro guarda **referência, nome original, tipo e tamanho**; os bytes nunca
entram na tabela.

É o mesmo motivo que já manda no contêiner e no banco: o documento 03 §1 exige que outra
comunidade replique fora do Google Cloud. Uma porta com dois adaptadores é o menor desenho que
cumpre isso, e as fatias seguintes que precisarem de arquivo herdam-na pronta.

- _Alternativa descartada:_ gravar os bytes no PostgreSQL — infla o banco e a cópia de
  segurança com dado que não se consulta.
- _Alternativa descartada:_ URL assinada para envio direto ao Cloud Storage — prende o desenho
  ao provedor exatamente onde a portabilidade importa.

### As duas rotas de formulário declaram a superfície do freio; a de chave não

`POST /v1/solicitacoes-de-participacao` e `POST /v1/solicitacoes-de-dados` recebem a
_dependency_ do freio com a sua superfície. `POST /v1/solicitacoes-de-chave` não a recebe
(`RN-01-46`). Nada muda no mecanismo — esta change apenas conecta o que a fatia 12 deixou
pronto.

### O crédito da proposta adotada é idempotente pela própria linha

Adotar grava o desfecho e credita 20 extras e o badge **na mesma transação**. A idempotência
vem da linha da sugestão, que registra que já creditou; não de contagem posterior. Regravar
"adotada" numa sugestão já creditada não credita de novo, e o badge de protagonismo é
concedido uma vez por autor.

### A rota de sugestão aceita texto, e só

Não há campo de áudio, nem rota que o receba. O documento 03 §12.2 manda descartar áudio na
transcrição; a forma mais barata de nunca falhar nisso é o núcleo não ter por onde recebê-lo.
É o mesmo raciocínio da fotografia do onboarding, que não trafega.

## Risks / Trade-offs

- **Quatro tabelas exigem quatro consultas para a visão única da App 03** → a leitura unificada
  nasce quando o PRD-02 a pedir, como `UNION` das colunas do ciclo; nenhuma decisão desta
  fatia a impede.
- **A porta de armazenamento é infraestrutura nova numa fatia de domínio** → fica com a
  interface mínima que o comprovante exige, sem versionamento, sem ciclo de vida e sem
  varredura; quem precisar de mais acrescenta na fatia que precisar.
- **O adaptador de disco não é o de produção** → o teste de integração roda contra o de disco,
  e o contrato da porta é o que os dois cumprem; divergência de provedor aparece na
  implantação, não no domínio.
- **O descarte da sugestão não adotada aos 90 dias precisa de quem o execute** → nesta fatia
  entra a regra e o cálculo da data; a varredura que a aplica é operação, e o Ciclo 01 não tem
  agendador. Fica registrado em Open Questions.

## Migration Plan

Uma migração do Alembic cria as quatro tabelas e os dois tipos enumerados. Não há dado a
migrar: as quatro entidades nascem vazias e nenhuma tabela existente muda de forma.

A porta de armazenamento entra com o adaptador de disco como padrão, de modo que a esteira e o
ambiente de desenvolvimento não dependem de credencial de nuvem.

Reversão é o `downgrade` da migração — sem perda de dado de outra capacidade, porque nenhuma
depende destas tabelas.

## Open Questions

1. **Quem executa o descarte aos 90 dias** da transcrição da sugestão não adotada. O prazo é
   requisito e a data fica calculada e gravada; o que falta é o gatilho — varredura na subida,
   agendador ou rotina de operação. Não muda spec, desenho nem tarefas desta fatia, e a
   resposta serve também aos demais prazos de guarda do documento 03 §12.2, que outras fatias
   vão precisar.
