## Context

Ver `proposal.md` — Why. O que o desenho precisa saber: a conferência de dimensão vive num
único ponto do núcleo (`gravar_ou_recadastrar_template`), é a **primeira** guarda da rota, e a
`comum/biometria` é o único módulo que produz descritor — fronteira já estabelecida pela spec
`template-biometrico`. A `camada-de-acesso-comum` já entrega a mensagem do núcleo à tela; a
`TelaDeCaptura` é quem a descarta.

## Goals / Non-Goals

**Goals:** a dimensão para de ser configurável e passa a ser fato do núcleo; a recusa do núcleo
chega inteira ao Mestre.

**Non-Goals:** o limiar de comparação, o laço de detecção e a `RF-04-16` — todos fora, com
motivo na `proposal.md`. Também não entra rota, contrato de API nem migração.

## Decisions

**1. A constante mora só no núcleo.** É lá que a conferência acontece; a aplicação envia o que a
biblioteca gerou e não precisa do número. _Alternativa descartada:_ declarar a dimensão também
em `comum/biometria` para as duas pontas "concordarem" — criaria o mesmo número em dois lugares,
que é a duplicidade que este repositório proíbe, e não impediria divergência nenhuma.

**2. A constante nasce com a origem escrita ao lado.** O comentário nomeia o modelo `faceres` da
Human e a saída de onde o número sai, para que trocar de biblioteca seja uma leitura, não uma
arqueologia. Foi a falta disso que deixou o defeito vivo por um mês.

**3. Remover a variável, não esvaziá-la.** `biometria_dimensao_do_descritor` sai da
`Configuracao`. _Alternativa descartada:_ manter a variável e conferi-la na subida contra a
constante (opção "C" apresentada ao fundador) — mantém em pé um parâmetro que não é parâmetro, e
o fundador decidiu pela remoção.

**4. A tela apresenta `ErroDaApi.message`, com frase própria só na falha sem corpo.** É o que a
`TelaDoTermo`, no mesmo fluxo, já faz — o padrão existe e não se inventa outro aqui.

## Risks / Trade-offs

**A mensagem do núcleo é escrita para desenvolvedor, não para criança** → as duas mensagens da
rota ("Descritor fora da dimensão esperada", "Cadastro biométrico exige consentimento vigente do
responsável para a captura") são legíveis por Mestre adulto, que é quem opera a captura. Se a
primeira turma mostrar o contrário, a correção é de texto do núcleo, não de desenho da tela.

**Trocar de biblioteca passa a exigir _deploy_ do núcleo** → é a contrapartida aceita da decisão
do fundador, e trocar de biblioteca já exigiria _build_ novo dos dois frontends que a importam.

**O secret fica órfão em produção até alguém apagá-lo** → confirmado que não derruba nada:
`pydantic-settings` 2.15.0, a versão travada no `uv.lock`, **ignora** variável de ambiente sem
campo correspondente. A remoção do secret é higiene, não pré-requisito, e a ordem entre _merge_
e limpeza é livre.

## Migration Plan

1. Sem migração Alembic: `credencial.segredo` já é `Text`, e não existe _template_ em produção
   para migrar — nenhuma gravação passou desde 2026-08-29.
2. _Deploy_ do núcleo com a constante. A partir dele a captura grava.
3. _Deploy_ da App 01 com a mensagem legível. Independente do passo 2, em qualquer ordem.
4. Limpeza da implantação, à mão: apagar o secret `cg-biometria-dimensao-do-descritor` e tirá-lo
   do mapeamento `GCP_SECRETOS_CG`.
5. _Rollback_: reverter o _merge_ e recriar o secret com `1024` — não com `128`, que é o valor
   defeituoso.

## Open Questions

Nenhuma. As duas decisões que este desenho exigia — o destino da dimensão e o recorte do limiar
— foram tomadas pelo fundador em 2026-09-17, antes da proposta.
