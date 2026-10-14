# Proposal

**PRD de origem:** PRD-03 (Vitrine Pública), com reflexo no `RF-02-80` do PRD-02.
**Fatia:** nenhuma — change de decisão do fundador fora de fatia numerada, no padrão da
`2026-10-11-vitrine-reordenada-e-entrada-verde`. A linha entra no
`openspec/cronograma-de-fatias.md` com `—` na coluna de fatia.
**Identificadores atendidos:** `RF-03-45`, `RF-03-46`, `RF-03-48`; `RF-02-80` no que o Admin
edita. Nenhum enunciado de `RF` muda: os requisitos sempre disseram o que a seção exibe, não
o que ela diz.

## Why

A fatia 5 do PRD-03 entregou a entidade, as rotas e a semeadura do conteúdo institucional,
mas deixou o conteúdo em aberto: "Quem somos" nasceu com o **rascunho** da nota de
transparência sobre IA e nada de apresentação, "Contatos" nasceu **vazio** — nenhum
documento trazia contato algum — e a pendência do texto final consta do PRD-03 §14. O
fundador decidiu os nove pontos que faltavam em 2026-10-14, e esta change os desce pelo
fluxo da hierarquia de autoridade: documento-fonte, documento 09, PRD e só então código.

Três decisões não são redação e por isso precisam de documento-fonte antes do texto: o
auxílio de IA **não altera a licença** de nenhum artefato (documento 03 §1, princípio 4), o
canal do recibo de doação passa a existir (documento 04 §1), e a **marca reservada** passa a
ser declarada na vitrine, onde quem replica a plataforma a lê.

## What Changes

- **Documento 03 §1, princípio 4** — grava que o auxílio de ferramentas de IA não altera a
  licença do artefato: código em AGPL, conteúdo e dados em CC BY-SA, crédito de quem decidiu,
  revisou e publicou. É a fonte única do licenciamento (documento 99 §1).
- **Documento 04 §1** — a regra "quem precisa de recibo escreve para a pessoa jurídica
  vinculada" passa a nomear para onde se escreve.
- **Documento 09** — cinco linhas em "Já decididos": canal único de contato, nota de IA como
  texto final, licença do gerado com auxílio de IA, "Quem somos" só no recorte padrão e
  marca reservada declarada na vitrine.
- **PRD-03 §14** — fecha a pendência do texto final da nota de transparência sobre IA, o que
  destrava o `RF-03-48` por inteiro. A pendência do título da criação original permanece.
- **Semeadura** — as três seções passam a nascer com texto. "Contatos" deixa de nascer vazio;
  "Quem somos" ganha a apresentação institucional antes dos dois blocos que já existem, com a
  nota de IA **intacta** e "Licenças" acrescido de dois parágrafos; "Como apoiar" ganha o
  comprovante obrigatório e a regra do recibo, que o documento 04 §1 já decidia e a porta do
  convite não dizia.

Fora do escopo, conforme o PRD-03 §3.2 e as decisões de 2026-10-11: o vídeo de apresentação
(`RF-03-49`, desejável) continua sem link, porque não existe; "Como apoiar" continua sem
seção na abertura; "Quem somos" continua fora dos recortes de pesquisadores e de gestores.

## Capabilities

### New Capabilities

Nenhuma. O conteúdo institucional já é capacidade consolidada.

### Modified Capabilities

- `conteudo-institucional`: o requisito da semeadura **sai**, porque mandava semear a nota como
  **rascunho** e deixar **"Contatos" sem texto** — as duas coisas deixaram de valer. Em seu
  lugar entram seis requisitos, um por comportamento: a mecânica da semeadura das três seções,
  e o conteúdo decidido de "Quem somos", do bloco "Licenças", de "Contatos" e de "Como apoiar".
  O requisito da entidade é ajustado num ponto só: o cenário da seção sem texto usava "Contatos"
  como exemplo, e "Contatos" passa a nascer com texto.

## Impact

| Alvo | O quê |
| ---- | ----- |
| `docs/03-plataforma-e-arquitetura.md` §1 | Princípio 4 — a frase do licenciamento com auxílio de IA |
| `docs/04-modelo-economico-e-sustentabilidade.md` §1 | O canal do recibo de doação |
| `docs/09-topicos-em-aberto-e-sugestoes.md` | Cinco linhas em "Já decididos" |
| `docs/prds/prd-03-vitrine-publica.md` §14 | Fecha a pendência da nota |
| `backend/src/nucleo/conteudo_institucional/semeadura.py` | Os três textos |
| `backend/tests/test_conteudo_institucional_semeadura.py` | A terceira semente |
| `openspec/cronograma-de-fatias.md` | A linha da change |

Sem migração: o modelo da entidade não muda. Sem mudança de contrato: as três rotas
(`GET /v1/vitrine/conteudo-institucional`, `GET /v1/conteudo-institucional`,
`PUT /v1/conteudo-institucional/{secao}`) ficam como estão. Nenhuma pasta nova, nenhuma
esteira de CI nova.

**Duas consequências operacionais, que a change registra e não resolve:** produção já foi
semeada, e a semeadura converge só onde a seção não tem texto — portanto mudá-la **não**
atualiza produção, onde quem publica é o Admin pelo `PUT`; e "Quem somos" e "Contatos"
renderizam no build da App 06, de modo que o texto publicado só aparece no site **após
redeploy**. "Como apoiar" é a exceção: a porta do convite a lê a cada visita.
