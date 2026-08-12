## Context

Ver `proposal.md` — Why. Das três fatias anteriores já existem: middleware de chave em toda rota
sob `/v1`, corpo único de erro, `Persona` em tabela única com o papel como discriminador,
`Credencial` com `tipo` em (biometria, login social, usuário e senha), `Sessao` opaca conferida
no banco, mixin `ComAutoria`, matriz de permissões declarativa e `Consentimento` somente
inserção.

Quatro decisões já tomadas moldam esta fatia e não se reabrem. `Credencial` nasceu com o tipo
`biometria` previsto e `ComoAutenticou` nasceu com `biometria` e `confirmacao_humana`: a fatia 2
deixou o encaixe pronto. A fatia 2 firmou que atributo próprio de papel entra em **tabela
satélite**, nunca em coluna anulável de `persona`, e nomeou o nick como caso da fatia 4. E a
fatia 3 entregou `Consentimento`, que `RN-01-17` põe como condição da gravação do _template_.

A restrição que domina o desenho é o `RN-01-14`: o _template_ é cifrado, nenhuma rota o devolve,
e todo acesso a ele é auditado — este último alargado pela decisão gravada no documento 03 §3.3,
que faz "acesso" alcançar também cada comparação de login.

## Goals / Non-Goals

**Goals**

- Fazer a impossibilidade de devolver o _template_ ser propriedade do modelo, não disciplina de
  quem escreve rota depois.
- Deixar a unicidade do nick conferível em toda a plataforma, e não por comunidade.
- Fazer a recusa de sessão ser indistinguível — no corpo **e** no tempo.
- Deixar o registro de acesso pronto para a trilha consultável do `RF-01-29`, de outra fatia.

**Non-Goals**

- Rota que cria o Guerreiro(a) e conferência de unicidade na conversa: são do PRD-04 (ver
  `proposal.md`).
- **Exclusão do _template_** ao fim do vínculo ou a pedido do responsável: o documento 03 §3.3 a
  exige, mas nenhum `RF` do PRD-01 a declara. Ver Open Questions.
- Prova de vivacidade: acontece no aparelho, antes do descritor (documento 03 §3.3).
- Limite de tentativas na rota pública: segue com `RN-01-27` no documento 09.

## Decisions

### O nick mora em tabela própria, compartilhada pelos papéis que o têm

Nasce a tabela `nick`, com o valor sob índice único e uma chave estrangeira única para `persona`.
Não é coluna de `persona` — a fatia 2 vetou coluna anulável de papel — nem coluna de uma satélite
de Guerreiro(a), porque `RN-01-30` exige que o nick do Apoiador **não colida** com o do
Guerreiro(a), e unicidade entre duas satélites não se declara no banco. Uma tabela só resolve as
duas exigências com um índice, e é onde o Apoiador entra sem migração de estrutura na fatia dele.

Alternativa descartada: coluna em cada satélite mais _trigger_ de conferência cruzada — mesma
garantia, com código que o índice único dá de graça.

### A cifra é autenticada, e o ambiente que não declara a chave não sobe

O _template_ é cifrado com AES-GCM, que dá confidencialidade e detecção de adulteração no mesmo
passo. A chave vem da configuração, como já vale para a duração da sessão: sem valor padrão, de
modo que o ambiente que não a declarar falha na subida em vez de gravar biometria em claro. No
Cloud Run a variável é populada pelo Secret Manager; em outra hospedagem, direto — é o que
preserva a portabilidade do documento 03 §1.

`Credencial.segredo` passa de `String(512)` a `Text`: o descritor cifrado e codificado não cabe
no limite que a fatia 2 dimensionou para _hash_ de senha.

Alternativa descartada: cifrar e decifrar por chamada ao Cloud KMS — põe rede no caminho de cada
entrada de criança e amarra a plataforma ao Google Cloud, contra o documento 03 §1.

### A comparação decifra um _template_ só

O nick já restringiu a busca a um Guerreiro(a) — é o que a jornada do PRD-01 §5.1 descreve —,
então a comparação decifra **um** registro e calcula a distância contra o descritor recebido. Não
há varredura da base, o custo por login é constante, e o limiar é parâmetro declarado na
implantação, sem valor padrão. A dimensão esperada do descritor é parâmetro pelo mesmo motivo:
ela acompanha o modelo da biblioteca Human que o App 01 usa (PRD-04), e o núcleo não a arbitra.

### A recusa é indistinguível também no tempo

Corpo e código iguais não bastam: se o nick inexistente responde antes, a diferença de tempo
revela que o nick existe, e `RN-01-22` cai. Quando o nick não é encontrado, o núcleo compara o
descritor recebido contra um _template_ de descarte, gerado na subida, e só então responde 401.
Mesmo caminho, mesmo trabalho, mesma resposta.

### O registro de acesso é somente inserção, como o consentimento

Nasce `acesso_ao_template`, com o Guerreiro(a) alcançado, quem ou o quê acessou, a natureza do
acesso, o desfecho e o momento com fuso. Ganha as duas camadas que a fatia 3 firmou para
`Consentimento` — _listener_ de mapeador e _trigger_ que recusa `UPDATE` e `DELETE` —, porque
guarda permanente sem imutabilidade é promessa, não prova. É a tabela que o `RF-01-29` vai ler.

Alternativa descartada: reaproveitar a autoria do mixin `ComAutoria` — ele grava quem escreveu
numa entidade de negócio, e a comparação de login não escreve entidade nenhuma.

### Duas operações novas entram na matriz de permissões

`RF-01-06` e `RF-01-08` dão a Mestre e Admin a confirmação de identidade e o cadastro biométrico.
A matriz nasceu como transcrição do PRD-01 §4, cuja célula do Mestre não nomeia nenhuma das duas
— mas o vocabulário foi declarado extensível pelas fatias seguintes, e é por ele que as rotas
declaram o que exigem. As duas entram como operação do Mestre, com origem no `RF`, e o PRD-01 §4
recebe a menção correspondente. Ver Open Questions.

### A sessão do Guerreiro(a) reusa o que já existe

Nada de tabela nova: `Sessao` já tem `como_autenticou` e `quem_confirmou`, e o encerramento por
`DELETE /v1/sessoes/atual` já está entregue. A fatia só acrescenta os dois caminhos de abertura e
a segunda duração de configuração.

## Risks / Trade-offs

- **A chave de cifragem é única e não rotaciona no Ciclo 01** → decisão registrada no documento
  09; a coluna guarda a versão da chave desde já, para que a rotação futura não exija migração de
  estrutura, só recifragem.
- **Limiar apertado recusa criança legítima com mais frequência** → é o lado recuperável do erro:
  a confirmação do Mestre (`RF-01-06`) abre a sessão no encontro, e o parâmetro se calibra sem
  tocar em código.
- **Um registro de acesso por login faz a tabela crescer rápido** → é o custo aceito da decisão
  do fundador; a tabela nasce indexada por Guerreiro(a) e por momento, e a partição por tempo é
  o mesmo caminho já decidido para as séries do território.
- **O _template_ de descarte precisa parecer real** → é gerado na subida com a mesma dimensão do
  parâmetro; se a dimensão mudar, o teste de indistinguibilidade quebra e avisa.
- **`Credencial.segredo` passa a guardar dois tipos de segredo com formatos diferentes** → o
  `tipo` já discrimina, e a leitura de cada um vive no módulo do seu papel.

## Migration Plan

1. Quarta migração cria `nick` e `acesso_ao_template`, com o _trigger_ de imutabilidade desta
   última, e alarga `credencial.segredo` para `Text`.
2. A migração é aditiva: nenhuma linha existente muda, e as três fatias anteriores seguem
   funcionando sem o nick, que só é exigido de persona de Guerreiro(a) — e ainda não há nenhuma
   em produção, porque a rota que a cria é do PRD-04.
3. Rollback é a migração reversa; como nada existente é alterado, ela não perde dado de fatia
   anterior.
4. Os três parâmetros novos — duração da sessão do Guerreiro(a), limiar e dimensão do descritor —
   e a chave de cifragem entram na implantação antes do primeiro _deploy_ desta fatia. Sem eles o
   serviço não sobe, por decisão de desenho.

## Open Questions

- **Exclusão do _template_.** O documento 03 §3.3 manda excluí-lo ao fim do vínculo ou a pedido
  do responsável, e o PRD-01 §11 dá a retenção "enquanto durar o vínculo" — mas nenhum `RF` do
  PRD-01 declara a operação. Fica fora desta fatia, e a decisão é do fundador: virar requisito do
  PRD-01 ou ficar com o PRD-13, que já trata dos pedidos do responsável.
- **PRD-01 §4.** A célula do Mestre não nomeia a confirmação de identidade nem o cadastro
  biométrico que `RF-01-06` e `RF-01-08` lhe dão. A emenda é de uma linha e está prevista nas
  tarefas, mas depende do aval do fundador.
