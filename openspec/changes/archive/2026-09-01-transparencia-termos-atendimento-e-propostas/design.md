## Context

Ver `proposal.md` — Why. O que restringe o desenho, no que já existe:

- A **trilha de auditoria** grava uma linha por escrita aceita sob `/v1`, por um _middleware_
  que lê o que `exigir_persona` e `exigir_chave_de_aplicacao` puseram em `request.state` — **sem
  que rota alguma declare nada**. A linha guarda autor, papel, ação, entidade afetada, momento e
  origem, e **não sabe qual criança a escrita alcançou**. A tabela é somente inserção, com
  _trigger_ no banco.
- O **`guerreiro_id` quase sempre chega no corpo** do pedido, não no caminho — e o lançamento do
  resultado de uma atividade alcança **todos os participantes numa operação só**.
- O núcleo guarda a **versão vigente do termo** em `Configuracao`, carimbada em cada
  consentimento, e **nunca o texto**. Trocar o termo é trocar a configuração.
- `POST /v1/consentimentos` já registra ato de Admin ou Mestre com origem, testemunha e quem
  operou; `POST /v1/sugestoes` e `/v1/sugestoes/minhas` já aceitam o responsável.
- A App 07 hoje **encerra a sessão de quem não é responsável**, e as Apps 01, 03, 05 e 09 já têm
  o par `AvisoDeColeta` + área de direitos, replicado por aplicação.

## Goals / Non-Goals

**Goals:**

- Responder "o que vocês guardam do meu filho, por quanto tempo e quem mexeu nisso" sem que o
  responsável precise pedir nada a ninguém.
- Dar texto ao termo que o núcleo já versiona, e prova de leitura para medir H2.
- Registrar o ato de quem não tem smartphone com a mesma força do ato de quem tem.

**Non-Goals:**

- Registrar **leitura** de dado na trilha: a auditoria é de escrita, como o PRD-01 §11 define.
- Publicar ou editar termo por rota: o texto é conteúdo, e a versão vigente é configuração.
- Alcançar, no modo assistido, qualquer tela que não seja a decisão da autorização.

## Decisions

**1. O Guerreiro(a) alcançado pela escrita vira tabela lateral da trilha, colhida pelo
_middleware_.** Nasce `acesso_ao_dado_do_guerreiro` — uma linha por (auditoria, Guerreiro(a)) —,
preenchida pelo mesmo _middleware_, que colhe todo `guerreiro_id` dos `path_params` e do corpo
JSON já em cache, inclusive os que estão dentro de listas. Nenhuma rota declara nada, a trilha
continua somente inserção e o lançamento em lote fica ligado a cada criança que alcançou.
_Descartadas:_ coluna única em `auditoria` — não representa o lançamento em lote; cada rota
declarar o alcançado — dezenove módulos e o oposto do princípio que criou o _middleware_.

**2. O texto do termo é conteúdo semeado, não rota de gestão.** `Termo(tipo, versao, texto,
vigente_desde)` é semeado na implantação, como as chaves de aplicação, e a vigente continua
sendo a da `Configuracao`. _Descartada:_ rota de publicação na App 03 — nenhum requisito a
prevê, e o texto exige revisão jurídica, não operação de rotina.

**3. A leitura do termo é um registro por responsável e versão.** Reler não grava de novo, e a
data do primeiro permanece — mesmo precedente da decisão repetida do responsável, que também não
gera segundo registro. É o que H2 precisa: quantos responsáveis tomaram ciência, não quantas
vezes abriram a tela. _Descartada:_ uma linha por leitura.

**4. O catálogo de dados é declarado no núcleo, com a marca do que está guardado.** As linhas
saem das tabelas do PRD-01 §11 e do documento 03 §12.2, e cada uma responde se o núcleo guarda
aquele dado **daquele** Guerreiro(a) hoje. A rota fica em módulo próprio `transparencia/`, que
só lê. _Descartada:_ tabela estática no frontend, como nas Apps 03 e 09 — ali o dado é do
próprio adulto; aqui o PRD-13 §9 declara a rota e o requisito é sobre a criança.

**5. O ato assistido é rota própria, sobre a mesma regra.** `POST
/v1/guerreiros/{id}/autorizacao/assistida` chama `registrar_consentimento`, como a rota
genérica, mas exige o responsável presente vinculado e a testemunha — exigências que `POST
/v1/consentimentos` não faz e não pode passar a fazer, porque serve também ao termo impresso da
biometria. _Descartada:_ ampliar a rota genérica com campos condicionais.

**6. Nenhuma `Operacao` nova.** Termos por `exigir_persona`, de qualquer papel; leitura do termo
por `consentimentos` (escreve, do responsável); dados e acessos por
`guerreiros_sob_sua_responsabilidade` (lê); responsáveis de um Guerreiro(a) e ato assistido por
`vinculo_com_guerreiros_e_guerreiras` e `testemunho_do_termo_impresso`, que Admin e Mestre já
têm. A matriz do PRD-01 §4 não muda.

**7. O modo assistido é rota de tela da App 07, não aplicação nova.** `App.tsx` deixa de derrubar
toda persona que não é responsável: sessão de Admin ou de Mestre entra **direto no modo
assistido** e não alcança mais nada; Guerreiro(a) e Apoiador continuam recusados como hoje.

**8. O crédito da proposta confere o papel do autor.** `avaliar_sugestao` credita os 20 extras e
o badge apenas quando o autor é Guerreiro(a) — hoje credita a qualquer persona, o que faria a
proposta de um responsável pontuar contra a `RN-13-18`.

## Risks / Trade-offs

- **A trilha é de escrita: quem só leu não aparece** → o histórico mostra o que o PRD-01 §11
  guarda, e é exatamente o que o PRD-13 §11 manda expor. A tela nomeia o que está listado sem
  prometer o que a trilha não tem.
- **Escrita que não nomeia a criança fica fora do histórico** → as que importam à família —
  presença, resultado, ocorrência, consentimento, criação — todas levam `guerreiro_id`; a spec
  declara o limite em vez de escondê-lo.
- **Ler o corpo no _middleware_** → só para `application/json`, com o corpo em cache antes do
  `call_next`; _upload_ nunca é lido, e a gravação segue best-effort, sem desfazer resposta já
  entregue.
- **Texto do termo sem revisão jurídica** → a redação aprovada pelo fundador entra como
  conteúdo; a revisão dos três textos continua na pauta do documento 09, e trocá-los é semear
  versão nova, sem tocar em registro já gravado.
- **O modo assistido põe Admin e Mestre dentro da App 07** → a spec fecha o alcance na decisão
  da autorização, e o histórico do responsável mostra quem operou cada ato em nome dele.

## Migration Plan

Uma migração Alembic: `termo`, `leitura_de_termo` (única por responsável e versão) e
`acesso_ao_dado_do_guerreiro`, com índice por Guerreiro(a) e por momento. A semente grava o texto
aprovado na versão **`2026-08`**, a que a `Configuracao` já carimba — antes desta fatia nenhum
texto existia, e semeá-lo na versão vigente evita consentimento apontando versão sem texto. Se a
base já tiver consentimento de produção, a semente entra como versão nova e a configuração passa
a apontá-la, sem reescrever o que os registros antigos afirmam.

Nada a desfazer no rollback além da migração: as três tabelas são novas e o recorte da trilha é
aditivo.
