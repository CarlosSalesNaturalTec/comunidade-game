# Design — template da missão no DeepSeek

## Context

Motivação em `proposal.md` — Why. O que o desenho precisa saber:

- As três portas de IA têm a mesma forma: `httpx.post` dentro de um `try` que devolve `None` em
  qualquer falha. A indisponibilidade nunca vira exceção nem 5xx — é requisito (`RF-09-91`,
  `RN-04-21`, `RN-05-35`), não detalhe.
- O DeepSeek é compatível com a API de _chat completions_ da OpenAI: `POST`
  `https://api.deepseek.com/chat/completions`, `Authorization: Bearer`, modelos
  `deepseek-v4-flash` e `deepseek-v4-pro`, e `response_format={"type": "json_object"}` desde
  que a palavra "json" apareça no prompt.
- O `_INSTRUCAO` atual já pede JSON e já descreve o formato campo a campo. O
  `_validar_estrutura` e o `EstruturaSugerida` não mudam: o que muda é quem responde e como a
  resposta chega.
- `CG_GEMINI_MODELO` e `CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE` já são o precedente de parâmetro
  não secreto em `--set-env-vars`.

## Goals / Non-Goals

**Goals:**

- A sugestão de estrutura volta a funcionar, a custo compatível com o Ciclo 01.
- A próxima falha de provedor se diagnostica na primeira leitura do log, não na terceira.
- Nenhuma credencial em texto claro no Cloud Logging.

**Non-Goals:**

- Não mover `producoes` nem `assistente`: leem imagem e áudio, que o DeepSeek não faz
  (documento 03 §1.12). Ficam no Gemini e seguem esperando crédito.
- Não unificar os três adaptadores num cliente comum. Eles se parecem, mas passam a falar com
  provedores diferentes; abstrair agora é acoplar o que a decisão acabou de separar.
- Não mudar o prompt além do necessário: o `_INSTRUCAO` já pede o JSON que o validador espera.

## Decisions

**1. `deepseek-v4-flash`, fixado, e não `latest`.** A tarefa é montar estrutura de missão a
partir de um tópico — trabalho simples, que o _flash_ atende, e o mais barato da linha. Fixar a
versão, e não seguir um apelido móvel, é o que mantém reprodutível o que o Mestre viu ontem;
foi também a lição do `gemini-2.5-flash`, que sumiu para contas novas sem aviso. Trocar segue
sendo uma linha no `env:` do workflow.

**2. `response_format={"type": "json_object"}`, e o `_extrair_json` continua.** O modo JSON do
DeepSeek elimina a cerca de código que obrigava a extrair o trecho entre a primeira `{` e a
última `}`. Ainda assim o `_extrair_json` fica: é barato, e o modo JSON não garante que nenhum
provedor futuro volte a embrulhar. _Descartado:_ remover o `_extrair_json` confiando no modo
JSON — economiza cinco linhas e reintroduz uma classe de falha silenciosa.

**3. O corpo da resposta entra no log, truncado, quando o erro é de HTTP.** `raise_for_status`
levanta com a linha de status e descarta o corpo, que é justamente onde o provedor explica o
que houve. O `except` passa a distinguir `httpx.HTTPStatusError` das demais exceções e a
registrar `status_code` e um recorte do corpo. Truncado porque a resposta de erro é curta mas
não tem teto declarado, e log não é lugar de despejo. _Descartado:_ logar o corpo inteiro — sem
teto, um provedor verboso enche o Cloud Logging. _Descartado:_ manter só `exc_info` — é o que
temos hoje, e foi o que custou três rodadas.

**4. A credencial sai da URL nos três adaptadores.** No DeepSeek, por construção: a
autenticação é por cabeçalho. No Gemini, trocando `?key=` pelo cabeçalho `x-goog-api-key`, que
a API aceita — verificado contra o endpoint real nesta sessão, com `ListModels` e com
`generateContent`. Sem isso, a URL da exceção continuaria carregando a chave para o log, agora
acompanhada do corpo da resposta que a decisão 3 acrescenta.

**5. O escape de `%` no `env.py` é `.replace("%", "%%")`, no ponto da declaração.**
`config.set_main_option` grava num `configparser`, que trata `%` como interpolação. Escapar na
única linha que declara a URL resolve para qualquer DSN, e não muda nada para os que não têm
`%`. _Descartado:_ documentar a restrição no README em vez de consertar — o README já lista `/`
e `+` como caracteres proibidos na senha, e a lista só cresce enquanto a causa não sai.

## Risks / Trade-offs

- **O DeepSeek pode responder num formato que o validador recusa.** → O `_validar_estrutura` já
  devolve `None` e agora registra a causa (fatia anterior), e a tela mostra o aviso. Os testes
  cobrem resposta válida, embrulhada e fora do formato.
- **Dois provedores, duas contas, dois lugares de custo.** → É a consequência aceita da decisão
  por funcionalidade, já registrada no documento 09.
- **O prompt foi escrito para o Gemini.** → É instrução em português pedindo JSON descrito
  campo a campo, sem nada específico do Gemini. Se a qualidade da sugestão cair, é ajuste de
  prompt numa change própria, com o Mestre avaliando — não se resolve às cegas aqui.
- **O `x-goog-api-key` muda o transporte de duas portas que hoje não têm como ser exercitadas**
  (sem crédito). → Os testes de porta cobrem o cabeçalho enviado; o exercício contra o provedor
  real só acontece quando houver crédito, e a tabela do README diz o que olhar.

## Migration Plan

1. Merge. Sem a chave mapeada, o adaptador devolve `None` e a tela segue no aviso — o mesmo
   estado de hoje, sem regressão.
2. Fundador: acrescentar `CG_DEEPSEEK_CHAVE_DE_API=cg-deepseek-api-key:latest` ao
   `GCP_SECRETOS_CG` e redeployar.
3. Conferência: acionar o Template da Missão na App 09 e ler o log pela tabela do README.

Reversão: retirar o mapeamento devolve o aviso de indisponibilidade. Voltar ao Gemini é
reverter o _commit_ — e reencontrar o `429`.
