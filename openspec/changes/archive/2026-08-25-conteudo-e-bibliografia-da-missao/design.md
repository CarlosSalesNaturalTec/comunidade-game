## Context

Ver `proposal.md` — Why. O que condiciona o desenho é o estado da porta de armazenamento:
`PortaDeArmazenamento` hoje tem três operações — `gravar`, `ler` e `remover` —, todas sobre
**bytes inteiros em memória**, com adaptador em disco fora de produção e Cloud Storage em
produção. Serve ao comprovante do aporte, que é PDF ou imagem pequena. Não serve ao vídeo de
200 MB: o núcleo roda em Cloud Run, e ler 200 MB para a memória a cada envio é o caminho mais
curto para derrubar a instância. Some-se `RF-09-19` — o envio é retomável e sobrevive à queda
de rede —, que nenhum `POST` multipart atende, e o desenho do envio deixa de ser detalhe de
implementação.

A `BibliografiaDaMissao` é o oposto: entidade pequena, cuja única sutileza é que dois dos seus
três requisitos de leitura (`RF-09-22`, `RF-09-23`) **só valem quando há vínculo** com o
exemplar tombado, decisão do fundador de 2026-08-25.

## Goals / Non-Goals

**Goals:**

- Tirar os bytes do caminho do núcleo: o núcleo autoriza e registra, o armazenamento recebe.
- Um só contrato de envio para produção e para a esteira, para que o teste exercite o mesmo
  fluxo que roda em produção — e não uma simulação dele.
- Derivar disponibilidade e crédito do Apoiador na leitura, sem persistir nenhum dos dois.

**Non-Goals:**

- **Limpeza de arquivo órfão** no bucket — envio começado e nunca confirmado. Não trava esta
  fatia: conteúdo sem confirmação não serve bytes e não aparece em lugar algum.
- **Transcodificação, miniatura e legenda** de vídeo. O que o Mestre envia é o que se serve.
- **Medição de consumo de nuvem**, em qualquer forma. É ausência deliberada, não pendência.
- **Edição de trilha publicada gerando nova versão** (PRD-09 §8): segue fora, como nas fatias
  anteriores.

## Decisions

### O envio corre por sessão retomável, aberta pelo núcleo e usada pelo cliente

O cliente pede o envio ao núcleo; o núcleo confere autoria, formato e teto, abre uma **sessão
retomável** no armazenamento e devolve ao cliente **o endereço da sessão**. O cliente envia os
bytes direto para lá, em partes, e retoma da última parte aceita quando a rede cai. Terminado,
confirma ao núcleo, que consulta o armazenamento pelo tamanho e tipo **reais** e só então marca
o conteúdo como servível.

- _Alternativa recusada:_ **multipart pelo núcleo**, como o comprovante do aporte. É o padrão
  que já existe no repositório e seria o menor diff — mas põe 200 MB na memória do contêiner e
  não retoma nada: uma queda aos 90% recomeça do zero, que é exatamente o que `RF-09-19` proíbe.
- _Alternativa recusada:_ **URL assinada de `PUT` único**. Tira os bytes do núcleo, mas também
  não retoma.

A confirmação conferindo o tamanho real é o que fecha o cenário do envio que diverge do
declarado: sem ela, o teto de 200 MB seria promessa do cliente, não regra do núcleo.

### A porta de armazenamento ganha duas operações, e nenhuma das três muda

`PortaDeArmazenamento` passa a ter `abrir_sessao` e `consultar_envio`, ao lado de `gravar`,
`ler` e `remover`. O comprovante do aporte, do ressarcimento, da fila e da coleta continua
usando exatamente o que usa hoje — nenhuma assinatura existente muda, e nenhuma dessas fatias é
tocada.

- **Produção:** a sessão retomável do Cloud Storage, que já é um protocolo de retomada por
  `Content-Range` — não se inventa protocolo novo.
- **Fora de produção:** o adaptador em disco expõe o **mesmo protocolo**, por uma rota do
  próprio núcleo que aceita as partes por `Content-Range` e as costura num arquivo temporário.
  Custa uma rota a mais e paga o preço todo: o cliente é o mesmo código nos dois ambientes, e a
  esteira exercita retomada de verdade, incluindo a queda no meio.

- _Alternativa recusada:_ **exigir credencial de nuvem na esteira**. Contraria o desenho que a
  fatia do comprovante fixou — desenvolvimento e CI não dependem de nuvem — e tornaria o teste
  de retomada dependente de rede.

### Disponibilidade e crédito do Apoiador são derivados, nunca gravados

A `BibliografiaDaMissao` guarda missão, título, capítulo e, opcional, `item_patrimonial_id`. A
disponibilidade no ponto de apoio e o Apoiador creditado **não são colunas**: saem a cada
leitura, do exemplar tombado e do aporte de origem dele. É o mesmo caminho que a terceira fatia
usou para a etiqueta do desafio de coleta, e pela mesma razão — o exemplar muda de estado, e um
valor copiado envelheceria calado.

Como `ItemPatrimonial.aporte_de_origem_id` é anulável, o crédito tem **três** saídas possíveis,
e as specs cobrem as três: sem vínculo, sem crédito; com vínculo e sem aporte de origem, sem
crédito; com vínculo e com aporte de Apoiador, crédito.

### O conteúdo guarda o tipo e só o que o tipo pede

`Conteudo` tem `tipo` — texto, imagem, link externo, vídeo, arquivo —, `corpo` para o texto,
`endereco` para o link, `referencia` e `tamanho` para os três que carregam arquivo, todos
anuláveis, com a coerência conferida na regra e não no banco. `autoria` é própria ou de
terceiro, e `fonte` é exigida na segunda. A ordem dentro da missão é inteiro declarado pelo
Mestre, como a ordem da missão dentro da trilha já é.

- _Alternativa recusada:_ **uma tabela por tipo**. Cinco tabelas para cinco variações de três
  campos, e a leitura da missão teria de unir as cinco na ordem certa.

## Risks / Trade-offs

- **A sessão retomável do Cloud Storage expira** (uma semana) → o núcleo guarda a validade
  junto da sessão e abre outra quando pedem envio numa sessão vencida. O Mestre recomeça o
  arquivo apenas nesse caso, que é o de deixar o envio parado por dias.
- **O endereço da sessão é credencial temporária nas mãos do cliente** → a sessão vale para
  **um único objeto**, e o núcleo NEVER devolve sessão de conteúdo de outro Mestre — a autoria
  é conferida antes de abrir. Nada além daquele objeto é alcançável por ela.
- **Arquivo enviado e nunca confirmado ocupa o bucket** → conteúdo sem confirmação não serve
  bytes nem aparece; o custo é armazenamento morto, e a limpeza fica para o ciclo de vida do
  bucket, fora desta fatia.
- **A rota de envio local é código que não roda em produção** → é o preço de ter um contrato
  só. Fica isolada no adaptador de disco, atrás da mesma porta, e o adaptador de produção nunca
  a importa — o mesmo desenho que a fatia do comprovante já usa para o cliente do Cloud Storage.
- **`RF-09-25` pré-visualiza sem a App 05 existir** → a pré-visualização usa a leitura pública
  da trilha, que é o contrato que a App 05 vai consumir. Se a tela da App 05 divergir depois, a
  pré-visualização acompanha o contrato, não a tela.

## Migration Plan

1. Migração com as duas tabelas novas, `conteudo` e `bibliografia_da_missao`. Nenhuma coluna
   existente muda, e nada é destrutivo — a fatia só acrescenta.
2. A porta de armazenamento ganha as duas operações; os quatro usos atuais do comprovante
   seguem inalterados e são cobertos pela suíte que já existe.
3. Configuração nova: o diretório das sessões locais, fora de produção, ao lado do
   `armazenamento_diretorio_local` que já existe.
4. Rollback: derrubar as duas tabelas. Como nenhuma outra capacidade escreve nelas e a leitura
   pública só as serve quando existem, a volta não deixa ponta solta.

## Open Questions

- **Ciclo de vida do arquivo órfão no bucket** — regra de expiração do Cloud Storage ou
  varredura periódica. Não muda spec, contrato nem tarefa desta fatia; entra quando o volume
  justificar.
