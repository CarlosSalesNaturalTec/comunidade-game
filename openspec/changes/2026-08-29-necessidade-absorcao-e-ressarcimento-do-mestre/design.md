## Context

A fatia é quase toda de tela. As três rotas do recorte já existem e estão testadas desde o
PRD-07: `GET /v1/necessidades/minhas` (spec `necessidade-de-recurso`), `POST /v1/aportes/absorcao`
(spec `aporte`) e `GET /v1/meus-aportes/ressarciveis` (spec `ressarcimento`). O padrão de tela da
App 09 já está consolidado nas áreas `territorio/` e `propostas/`, e o de lista de necessidades,
na App 03 (`app-03-gestao/src/recursos/`). O núcleo só muda num ponto: a leitura do catálogo de
tipos de recurso, hoje privativa do Admin.

## Goals / Non-Goals

**Goals:**

- Abrir na App 09 a área de recursos: ler a necessidade, absorvê-la em um ato e acompanhar o
  ressarcimento.
- Deixar o Mestre ler o catálogo de tipos de recurso, sem lhe dar a escrita.

**Non-Goals:**

- Nenhuma rota nova, entidade nova ou migração.
- Registro do ressarcimento, anexo do comprovante da transferência e homologação de aporte —
  atos de Admin, na App 03.
- Absorção fora de necessidade publicada: o recorte da fatia é a jornada 5.8 do PRD-09.

## Decisions

1. **A leitura do catálogo de tipos de recurso passa a aceitar Mestre**, em
   `recursos/regra.py::listar_tipos_de_recurso`. Sem ela a necessidade sai só com identificador
   e a absorção não sabe se pedir o valor de origem em reais nem o comprovante. Alternativa
   descartada: repetir nome e natureza dentro da saída da necessidade — engorda um contrato do
   PRD-07 por conveniência de uma tela do PRD-09.
2. **A escrita do catálogo continua privativa do Admin.** Só a função de leitura muda; o cadastro
   e as vigências não são tocados.
3. **A absorção nasce da necessidade, não de um formulário livre.** Tipo, ponto de apoio e aula
   vêm da linha escolhida; o Mestre informa quantidade, valor de origem e, quando exigido, o
   comprovante. Alternativa descartada: uma tela de aporte genérica, que reabriria provedor,
   forma e destinação — campos que a absorção não escolhe.
4. **A quantidade sugerida é a falta, e é editável.** O núcleo aceita cobertura parcial e abate a
   falta na leitura seguinte; travar a quantidade na falta cheia inventaria regra que o PRD não
   tem.
5. **A App não decide o que é ressarcível.** Ela apresenta a marca e a situação que o núcleo
   devolve — inclusive "não se aplica", da absorção de serviço. Alternativa descartada: derivar a
   situação da natureza na tela, que duplicaria regra do núcleo.
6. **Sem seletor de comunidade.** As três rotas já se recortam pelo vínculo vigente do Mestre; a
   tela não acrescenta filtro nenhum. Os nomes de tipo, ponto de apoio e comunidade vêm de
   `GET /v1/tipos-de-recurso`, `GET /v1/pontos-de-apoio` e `GET /v1/comunidades`, no molde que a
   App 03 e a área de território já usam.
7. **O aviso sobre a chave PIX é texto de tela, sem endereço nem `mailto:`.** Nenhum documento
   fixa endereço de Admin, e inventar um seria criar decisão. A tela diz o que a regra diz: a
   plataforma não guarda dado bancário e a chave vai por e-mail ao Admin.
8. **A recusa do núcleo é apresentada como veio, traduzida em linguagem simples.** A App não
   antecipa validação que o núcleo já faz — tipo sem vigência, tipo que a aula não consome,
   comprovante exigido —, para não manter duas cópias da mesma regra.

## Risks / Trade-offs

- **Necessidade cujo tipo não tem vigência vigente não tem nome no catálogo**, porque a leitura
  descarta esses tipos. A linha aparece assim mesmo, pela aula e pelo horário, declarando a falta
  de valor de referência; a absorção dela é recusada pelo núcleo, e a tela mostra o motivo. É
  aceito: o caso é de cadastro incompleto da gestão, e a tela não o esconde nem o remenda.
- **Abrir o catálogo ao Mestre amplia quem vê a tabela de referência em moedas.** É leitura de
  catálogo de recursos, sem reais e sem dado de pessoa, e o invariante 16 do documento 99 segue
  respeitado.
- **A tela relê as listas após cada absorção**, em vez de recalcular localmente: uma ida a mais ao
  núcleo em troca de nunca divergir da falta derivada.
