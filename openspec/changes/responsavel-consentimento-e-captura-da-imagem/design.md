## Context

Ver `proposal.md` — Why. O que molda o desenho:

- A regra do consentimento está pronta e consolidada em `openspec/specs/consentimento/spec.md`;
  falta só a porta. `consentimentos/regra.py` não muda nesta fatia.
- A cadeia da jornada 5.2 são **cinco requisições HTTP**, cada uma exigida pela seguinte, sem
  transação que as envolva.
- É a primeira integração de biblioteca de terceiro no navegador do repositório. A biblioteca
  está decidida no documento 03 §3.3 (**Human**, vivacidade → descritor) e não se reabre.
- O documento 03 §3.3 é explícito: como o descritor nasce em código do aparelho, a garantia da
  captura é **também presencial**. O núcleo não tem como reconferi-la.

## Goals / Non-Goals

**Goals:**

- Abrir a porta do consentimento sem tocar a regra que já existe.
- Deixar a cadeia de cinco chamadas **retomável**, não atômica.
- Isolar a Human atrás de um módulo próprio, para que o Vitest não baixe modelo nem abra câmera.

**Non-Goals:**

- Reconhecimento facial na entrada e captura de quem já se cadastrou sem imagem (`RF-04-16`,
  `RF-04-18`) — fatia seguinte, pelo motivo na spec da App 01.
- Conversa conduzida por IA e leitura do termo em voz alta (`RF-04-06`) — a modalidade áudio
  não existe ainda.
- Redação do termo impresso — pendência da §14 do PRD-04, e não é código.

## Decisions

### 1. O responsável mínimo é o nome, e só

`POST /v1/responsaveis` passa a receber `nome`, obrigatório. Decisão do fundador, 2026-08-24.

O consentimento é a base legal da captura, e apoiá-lo numa persona anônima não sustenta a §11 do
PRD-04. E-mail, credencial e digitalização ficam na gestão, como o PRD-13 §11 e o PRD-04 §3.2 já
atribuem — colher e-mail na porta da aula, com fila esperando, é passo que o produto não pediu.

_Descartado:_ manter o corpo vazio de hoje (consentimento apontando para ninguém); colher também
e-mail e senha provisória (move para a porta da aula um ato que é da gestão).

### 2. A versão do termo é carimbada pelo núcleo

Nova constante em `Configuracao` — padrão de `ciclo_rotulo` e `territorio_licenca` —, lida pela
rota. `POST /v1/consentimentos` **não** recebe `versao_do_termo`. Decisão do fundador,
2026-08-24.

Cliente não escolhe a versão do termo jurídico que a linha de auditoria vai afirmar. A validação
de versão em branco **permanece** em `registrar_consentimento`: ela protege qualquer chamador,
inclusive a rota do responsável na App 07, que virá depois.

_Descartado:_ receber a versão no corpo (deixa o cliente determinar a prova).

### 3. A matriz ganha a operação do testemunho

`Operacao.consentimentos` é do **responsável** — o consentimento que ele próprio dá na App 07.
O ato da App 01 é outro: Mestre ou Admin **testemunhando** o termo impresso assinado por um
terceiro. Reaproveitar a operação do responsável daria ao Mestre, de lambuja, o caminho da App 07.

Entra operação nova de escrita do Mestre, no mesmo desenho que a fatia anterior usou para
`cadastro_do_guerreiro_no_encontro`. Consequência documental: a matriz do **PRD-01 §4** ganha a
linha, no mesmo PR.

_Descartado:_ pôr `Operacao.consentimentos` no conjunto do Mestre.

### 4. A cadeia é retomável, não atômica

As cinco chamadas não têm transação comum, e não vale inventar uma rota composta que o PRD-04 §9
não declara. O desenho é **avançar por passo concluído**: a App 01 guarda o que já obteve
(`guerreiro_id`, `responsavel_id`) na memória do atendimento e retoma do primeiro passo que
faltou. Nenhum estado parcial é inválido:

| Falhou depois de       | O que fica                    | Como se resolve                          |
| ---------------------- | ----------------------------- | ---------------------------------------- |
| `POST /guerreiros`     | criança cadastrada, sem imagem | é exatamente a jornada 5.3               |
| `POST /responsaveis`   | responsável sem vínculo        | inócuo — a spec já diz que não alcança ninguém |
| `POST .../vinculos`    | vínculo sem consentimento      | retoma no termo                          |
| `POST /consentimentos` | consentimento sem _template_   | retoma na câmera; o consentimento vale   |

O pior caso é a jornada 5.3, que é caminho previsto do produto — nunca cadastro pela metade.

_Descartado:_ rota composta que crie responsável, vínculo e consentimento num ato (regra nova que
o PRD não tem); fila local (o `RF-04-24` já exige rede para cadastro novo).

### 5. A Human fica atrás de um módulo com fronteira estreita

Um módulo da App 01 expõe duas funções — provar vivacidade e gerar descritor — e é o único lugar
que importa a Human, carrega modelo ou toca `getUserMedia`. O teste substitui o módulo; nenhum
teste baixa modelo nem abre dispositivo.

A fronteira é o que garante o invariante 12 por construção: se a fotografia só existe dentro
desse módulo e ele devolve `number[]`, não há caminho por onde ela escape para requisição, para
registro de erro ou para armazenamento.

Os modelos são carregados **sob demanda**, ao entrar no passo da captura — não na subida da
aplicação —, para não pesar a tela inicial nem o caminho das trilhas (documento 03 §3.4:
aparelho modesto, rede instável).

### 6. Sem câmera, o onboarding continua

Decisão do fundador, 2026-08-24: a falta de câmera fecha a captura, não o caminho. Consequência
documental: dois critérios da **§12 do PRD-04** deixam de descrever o comportamento e são
corrigidos no mesmo PR —

1. _"Em aparelho sem câmera, a aplicação bloqueia o onboarding e orienta a trocar de aparelho"_
   passa a bloquear só a captura.
2. _"Descritor gerado sem a prova de vivacidade não é aceito pelo núcleo"_ atribui ao núcleo uma
   conferência que ele não tem como fazer. O documento 03 §3.3 — autoridade acima do PRD — diz
   que a ordem é garantida no aparelho e a entrada é assegurada pelo contexto presencial. O
   critério passa a dizer isso.

## Risks / Trade-offs

- **Peso dos modelos da Human no primeiro carregamento** (pendência da §14 do PRD-04) → carga sob
  demanda no passo da captura, e o resultado medido na primeira turma. Se não couber, a decisão é
  do fundador, não desta fatia.
- **Vivacidade não é verificável pelo núcleo** → aceito e documentado: a garantia é presencial
  (documento 03 §3.3), e todo acesso ao _template_ já é auditado.
- **Cadeia de cinco chamadas na porta da aula, com fila esperando** → retomada por passo, e o
  pior desfecho é a jornada 5.3, que já é caminho previsto.
- **Responsável sem e-mail não entra na App 07 até a gestão agir** → é o desenho do PRD-13 §11,
  não efeito colateral; a pendência aparece no painel do dia, como a digitalização do termo.

## Open Questions

- **Valor inicial da constante da versão do termo.** É parâmetro que a operação declara, não
  decisão de produto — mas o valor não se inventa. Perguntar ao fundador antes de fechar as
  tarefas; nada nas specs nem no recorte depende da resposta.
