# Design — chave do Gemini em produção

## Context

Motivação em `proposal.md` — Why. O que o desenho precisa saber do estado atual:

- Os três adaptadores de nuvem (`template_de_missao`, `producoes`, `assistente`) têm a mesma
  forma: `httpx.post` no endpoint `v1beta/models/{modelo}:generateContent?key={chave}`, tudo
  dentro de um `try` que devolve `None` em qualquer falha. A indisponibilidade nunca vira
  exceção nem 5xx — é requisito (`RF-09-91`, `RN-04-21`, `RN-05-35`), não detalhe.
- As três fábricas leem a **mesma** dupla de campos de `Configuracao`, com o nome da primeira
  fatia que precisou dela.
- O `backend-deploy.yml` monta os segredos a partir de **um** segredo de repositório,
  `GCP_SECRETOS_CG`, que guarda a lista `SEGREDO:CG_VAR,...` aceita por `--set-secrets`.
  `CG_AMBIENTE` já é o precedente de parâmetro não secreto declarado em `--set-env-vars`.
- `nucleo-runtime` já tem `roles/secretmanager.secretAccessor` no projeto: segredo novo não
  exige IAM novo.

## Goals / Non-Goals

**Goals:**

- A credencial do Gemini alcança o serviço em produção com um nome que diz o que ela é.
- Trocar de modelo é uma alteração de workflow, não de segredo.
- Quem provisiona consegue confirmar pelo log se funcionou, e distinguir as causas quando não.

**Non-Goals:**

- Não mexer no contrato, no aviso ao usuário nem em nenhum requisito das três funcionalidades.
- Não trocar o modelo padrão nem avaliar qual modelo do Gemini serve melhor a cada uso.
- Não instrumentar custo do Gemini no livro-razão: o documento 03 §1.12 lança o consumo como
  recurso de _cloud_ por absorção do fundador, fora do núcleo, e nenhuma operação desta change
  tem custo a lançar.
- Não criar chave por funcionalidade: uma credencial serve as três, como já é hoje.

## Decisions

**1. `CG_GEMINI_CHAVE_DE_API` e `CG_GEMINI_MODELO`, sem prefixo de funcionalidade.** O prefixo
`TEMPLATE_DE_MISSAO_` é falso desde que `producoes` e `assistente` passaram a ler a mesma
variável, e o custo de mantê-lo é que o mapeamento em `GCP_SECRETOS_CG` esconde duas das três
dependências. Renomear é seguro: os campos só aparecem em `configuracao.py` e nas três
`fabrica.py`; os testes constroem os adaptadores com os argumentos `chave_de_api`/`modelo`, que
não mudam. _Descartado:_ manter o nome e explicar no README — documentação não conserta nome
enganoso lido por quem edita um segredo de repositório às pressas. _Descartado:_ uma variável
por funcionalidade — triplicaria o provisionamento sem nenhum ganho, já que a conta é uma só.

**2. O modelo vai para `--set-env-vars`, junto de `CG_AMBIENTE`; a chave fica no Secret
Manager.** O critério é o mesmo que o workflow já aplica a `CG_AMBIENTE`: nome de modelo não é
segredo, e guardá-lo no Secret Manager faz uma troca de modelo custar edição de segredo em vez
de uma linha de diff revisável. Entra nas **duas** etapas — serviço e Job de migração —, porque
as duas recebem a mesma configuração e o Pydantic valida o objeto inteiro no arranque.
_Descartado:_ deixar o modelo só no padrão do código, sem declarar — trocar de modelo exigiria
deploy de imagem nova.

**3. Cada causa de indisponibilidade deixa uma linha própria no log.** Hoje dois caminhos
devolvem `None` sem escrever nada: o ramo da chave ausente, antes do `try`, e a recusa de
formato, que devolve `None` de dentro do `try` sem levantar exceção. Como a chave ausente é
justamente o estado de produção, a tabela de causas não teria como separá-la de "ninguém
acionou a tela". Cada adaptador ganha, então, dois `logger.warning` — chave ausente e formato
recusado —, ao lado do `logger.warning` de exceção que já existe, nos _loggers_
`nucleo.template_de_missao`, `nucleo.producoes` e `nucleo.assistente`. _Descartado:_
diagnosticar pela ausência de linha — não distingue as duas causas mudas e falha em silêncio
justamente quando mais importa. _Descartado:_ elevar a `error` — indisponibilidade é
comportamento previsto, não defeito do serviço; `warning` mantém o alerta sem poluir.

**4. A tabela do README mapeia sinal observado → causa, no padrão da tabela de
`chave_invalida`.** O README já resolve o mesmo problema para a recusa de chave: uma recusa
única para quem chama, com o motivo no log e uma tabela que traduz campo em causa. A tabela do
Gemini repete a forma:

| O que aparece no log | Causa |
| --- | --- |
| nenhuma linha, com a tela acionada | o serviço não chegou ao adaptador — confira `CG_AMBIENTE=producao` |
| `chave de API do Gemini ausente` | `CG_GEMINI_CHAVE_DE_API` não chegou ao contêiner — confira o mapeamento em `GCP_SECRETOS_CG` |
| `HTTPStatusError ... 400` | `CG_GEMINI_MODELO` nomeia modelo que não existe no endpoint `v1beta` |
| `HTTPStatusError ... 403` | chave restrita a outra API, ou Generative Language API desabilitada no projeto |
| `HTTPStatusError ... 429` | cota da conta estourada |
| `ReadTimeout` | o modelo passou do tempo do adaptador |
| `resposta do Gemini fora do formato esperado` | o modelo respondeu, mas não no JSON que o adaptador exige |

## Risks / Trade-offs

- **Renomear e esquecer um ponto de leitura deixa o serviço sem subir.** → Os campos não têm
  valor obrigatório, então a falha não seria de arranque e sim silenciosa: uma fábrica lendo
  campo inexistente levanta `AttributeError` na primeira chamada. Mitigação: os quatro pontos
  de leitura são conhecidos e a suíte cobre as três portas; `ruff check` acusa o nome órfão.
- **O nome antigo pode já estar mapeado em `GCP_SECRETOS_CG`.** → Não está — é o que a change
  vem consertar. Se estivesse, o serviço subiria e continuaria mudo, com a linha nova de log
  dizendo a causa em uma passada.
- **A chave é de servidor e não tem restrição por origem possível.** → Cloud Run com
  `min-instances=0` não tem IP de saída estável sem conector VPC. A contenção é restringir a
  chave à Generative Language API no console e mantê-la no Secret Manager, nunca em build de
  frontend.
- **Provisionada a chave, as três funcionalidades passam a consumir cota de verdade.** → É o
  efeito pretendido. O Ciclo 01 opera sem teto de uso, por decisão já registrada (documento 09
  — "Corpus, cota e áudio dos assistentes"); a linha de `429` na tabela é como o estouro
  aparece.

## Migration Plan

1. Merge da change. Nada quebra: sem a chave, as três seguem no aviso, como hoje.
2. Fundador, no console do GCP: API Key restrita à Generative Language API → segredo no Secret
   Manager → mapeamento `<segredo>:CG_GEMINI_CHAVE_DE_API` acrescentado a `GCP_SECRETOS_CG`.
3. `workflow_dispatch` do `backend-deploy.yml`.
4. Conferência: acionar Template da Missão na App 09 e ler o log pela tabela do README.

Reversão: retirar o mapeamento de `GCP_SECRETOS_CG` e redeployar. As três voltam ao aviso de
indisponibilidade — o mesmo estado de hoje, sem erro para quem usa.
