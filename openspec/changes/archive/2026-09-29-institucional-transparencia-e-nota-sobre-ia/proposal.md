# Institucional, transparência e nota sobre IA

Origem: **PRD-03 — App 06: Vitrine pública**, §§3.1, 6.5, 7, 9, 11 e 12. **Fatia 5** do PRD-03 no
`openspec/cronograma-de-fatias.md`.

Atende `RF-03-45`, `RF-03-46`, `RF-03-48`, `RF-03-49`, `RF-03-52`, `RF-03-53`, `RN-03-23`. Toca
também `RF-02-80` (o `PUT` de Admin, que o núcleo passa a ter) e `RF-03-50`, `RF-03-51` e
`RN-03-21`, `RN-03-22` (o que a vitrine não faz segue valendo nas telas novas).

## Why

A vitrine não tem "Quem somos", "Contatos" nem "Como apoiar": a seção "Como apoiar" existe como
frase de "chega em entrega própria", e a chave PIX que o documento 04 §1 já decidiu não aparece
em lugar nenhum. Falta também a nota de transparência sobre IA, para a qual o documento 03 §7.1
manda apontar o texto reescrito por IA, e a área que diz ao visitante o que a plataforma coleta.
O núcleo não tem a entidade do conteúdo institucional nem a rota que a lê, e a fatia 16 do PRD-02
depende dela.

## What Changes

- **Núcleo**: entidade do conteúdo institucional, de três seções — "Quem somos", "Contatos" e
  "Como apoiar" —, com o texto, o autor e a data de quem publicou; `GET
  /v1/vitrine/conteudo-institucional` pública e `PUT /v1/conteudo-institucional/{secao}` de
  Admin (`RF-02-80`). A semeadura da implantação cria "Como apoiar" com a chave PIX e o titular
  do documento 04 §1 e "Quem somos" com o **rascunho** da nota de transparência e o bloco
  "Licenças". A fatia 16 do PRD-02 fica só com a tela de edição.
- **"Quem somos"** exibe o texto publicado, o vídeo de apresentação quando houver link, a
  **nota de transparência sobre IA** dentro dele e o bloco "Licenças", ao qual a nota remete
  (`RF-03-45`, `RF-03-48`, `RF-03-49`). **"Contatos"** e **"Como apoiar"** exibem o que foi
  publicado, e "Como apoiar" traz a chave PIX (`RF-03-45`, `RF-03-46`). Seção ainda não
  publicada aparece dizendo isso, sem inventar texto.
- **Aviso de coleta** em toda tela da vitrine, com acesso à **área detalhada**, que explica o que
  a plataforma coleta, de quem, para quê e por quanto tempo, e declara que a vitrine não coleta
  dado do visitante (`RF-03-52`, `RF-03-53`, `RN-03-23`).
- **Documentação**: a linha do documento 09 sobre a etiqueta de IA passa a apontar para a nota
  que existe; o cronograma marca a fatia.

## Capabilities

### New Capabilities

- `conteudo-institucional`: as três seções editáveis por Admin, a leitura pública delas e a
  semeadura do que já está decidido.

### Modified Capabilities

- `aplicacao-da-vitrine`: a App 06 ganha as três seções institucionais, o vídeo, a nota de
  transparência, o bloco "Licenças", o aviso de coleta em toda tela e a área detalhada.

## Impact

- **Código novo**: `backend/src/nucleo/conteudo_institucional/` (modelo, regra, rotas,
  semeadura), migração Alembic, registro em `principal.py`, `modelos.py` e `cli.py`, operação
  nova em `permissoes.py`; na App 06, telas das três seções, área detalhada e rodapé de coleta
  em `apps/app-06-vitrine/src/`.
- **Código lido**: `backend/src/nucleo/termos/semeadura.py` (padrão de semeadura idempotente),
  `comum/api/cliente.ts`.
- **Documentação**: linha 5 do PRD-03 no cronograma; linha do documento 09 sobre a etiqueta de
  IA; PRD-03 §14 (o rascunho existe, o texto final segue do fundador); ajuste de redação no
  documento 09 onde a nota cita só o Gemini no atendimento. O documento 99, `docs/prds/index.md`
  e a `nav` não mudam.
- **Fora do escopo**, como o PRD-03 §3.2 já exclui: a tela de edição do Admin (fatia 16 do
  PRD-02); a etiqueta no texto reescrito das Apps 01 e 05, que é da personalização por IA; o
  convite ao acompanhamento e as necessidades em aberto (fatia 6); os cards de Mestres e
  Apoiadores (fatia 7); a Área do Desenvolvedor (fatia 8); publicidade e patrocínio; qualquer
  preferência do visitante. Não há decisão de produto nova: o texto final da nota, o texto de
  "Quem somos" e os contatos são insumos do fundador (PRD-03 §14), e a tela admite e exibe o que
  for publicado.
