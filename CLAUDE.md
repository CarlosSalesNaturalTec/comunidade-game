# CLAUDE.md — Regras de trabalho neste repositório

Repositório do **Comunidade Game** — plataforma educacional gamificada, open source, para
comunidades periféricas. Neste momento o repositório **não contém código**: contém apenas a
documentação do projeto, na pasta `docs/`.

## Estado atual e próxima etapa

1. **Feito:** revisão e validação humana de todos os documentos de `docs/` (agosto de 2026).
2. **Feito:** os treze **PRDs** (_Product Requirements Documents_) do Ciclo 01, em
   `docs/prds/`, escritos a partir de `docs/08-base-para-prds.md` e aprovados pelo fundador.
3. **Agora:** desenvolvimento das oito aplicações e do Backend API.

Não iniciar a escrita de código sem sinal explícito do fundador. PRD novo ou revisão de PRD
existente continua seguindo as regras de `docs/prds/` abaixo.

## Regras de redação e revisão dos documentos de `docs/`

Estas regras valem para **toda** solicitação de ajuste de texto nesta pasta — novas seções,
correções, reescritas ou incorporação de decisões novas.

### 1. Concisão é requisito, não estilo

Os documentos são lidos por **pessoas**. Escreva o mínimo necessário para a decisão ficar clara.

- Prefira tabela e lista a parágrafo; prefira uma frase a três.
- **Corte a justificativa redundante.** Uma regra bem escrita não precisa de dois parágrafos
  explicando por que é boa. Quando a razão for indispensável para não se perder a intenção,
  guarde-a em **uma** frase.
- Não repita a mesma ideia em abertura, corpo e fechamento de seção.
- Evite ênfase decorativa: negrito só no que é definição, regra ou termo do domínio.
- **Exceções:** `docs/08-base-para-prds.md` e os arquivos de `docs/prds/` **podem** ter
  detalhamento extenso. Só eles.

### 2. Fonte única — nunca duplicar

Cada assunto tem **um** documento normativo, listado em `docs/99-mapa-de-referencias.md` §1.

- Ao alterar uma regra, altere **o documento-fonte** dela.
- Se outro documento precisa mencionar o assunto, resuma em **uma frase** e não repita a regra
  completa, a tabela nem os números.
- Ao encontrar duplicidade, consolide no documento-fonte e reduza a menção nos demais.

### 3. Referências entre documentos ficam no doc 99

- Os documentos 01–14 **não** carregam links `[XX §Y](arquivo.md#ancora)` entre si. Quando o
  leitor humano precisar mesmo ser encaminhado, escreva em texto simples: _"(documento 05)"_.
  A exceção é `docs/index.md`, cuja função é justamente indexar e linkar os demais.
- Todo o mapa de relações — fonte única, dependências, conceitos, aplicações → PRDs,
  rastreabilidade e invariantes — vive em `docs/99-mapa-de-referencias.md`, que existe para
  orientar agentes de IA, não humanos.
- **Toda alteração que mude a relação entre documentos exige atualizar o doc 99.**

### 4. Preservar o sentido original

Melhorar a redação **nunca** significa mudar a decisão. Ao reescrever:

- Mantenha as definições vigentes, os números, os nomes próprios e o tom do projeto (linguagem
  direta, popular quando couber, sem jargão corporativo).
- Não invente regra, número, prazo nem provedor de tecnologia. O que falta decidir é marcado
  como pendência, não preenchido com suposição.
- Não remova uma definição por parecer redundante sem verificar se o outro documento realmente
  a contém.

### 5. Marcações padronizadas

- **`[Proposta]`** — ideia ainda **não decidida** pelo fundador. Tudo que não estiver marcado é
  definição vigente.
- **`> **A definir:**`** — lacuna que precisa de número ou critério. Toda pendência nova deve
  também entrar na tabela do documento 09.
- **`**Definição vigente**`** — decisão tomada, quando o contraste com uma proposta próxima
  ajudar o leitor.

### 6. Coerência entre documentos

Antes de fechar qualquer edição, confira os **invariantes** listados em
`docs/99-mapa-de-referencias.md` §6 (oito aplicações Web/Mobile First, faixa 6–16, autocadastro
só do Guerreiro(a), coleta obrigatória em toda trilha, jogo que não credita pontos, lastro, guarda
permanente com anonimização na saída, escopo do Ciclo 01, entre outros). Contradizer um deles é
erro de documentação, não variação de redação.

Confira também numeração de seções contínua, títulos coerentes com o índice
(`docs/index.md`) e com a `nav` do `mkdocs.yml`, e tabelas com totais que fecham.

### 7. Idioma e formatação

- Português do Brasil.
- Markdown com linhas de até ~95 caracteres.
- Títulos em sentença (`## 3. Trilhas`), não em caixa alta.
- Tabelas para catálogos e regras comparativas; blocos de código apenas para diagramas ASCII,
  trechos de código e payloads.

## Regras dos PRDs (`docs/prds/`)

Valem todas as regras acima, com as diferenças abaixo.

### 1. O PRD é derivado — nunca fonte única

O PRD **aplica** as regras dos documentos 01–14; não cria regra própria. Quando uma decisão
nova for tomada durante a escrita de um PRD:

1. gravar a regra no **documento-fonte** dela (doc 99 §1);
2. mover a linha no **documento 09** de "Decisões pendentes" para "Já decididos";
3. só então o PRD a aplica, **sem repetir** tabela, número ou texto normativo.

Regra que existe apenas dentro de um PRD está no lugar errado.

### 2. Elicitação antes da redação

Antes de escrever um PRD, listar as pendências do documento 09 e as questões em aberto do
documento 08 que **travam** aquele PRD e perguntá-las ao fundador. Não preencher lacuna com
suposição nem escrever o PRD inteiro marcado como `[Proposta]`.

### 3. Estrutura e extensão

- Estrutura obrigatória: `docs/prds/00-modelo-de-prd.md`. Nenhuma seção é suprimida; seção
  sem conteúdo recebe "não se aplica" com o motivo em uma linha.
- Requisitos e regras recebem identificador (`RF-XX-nn`, `RN-XX-nn`) e enunciado verificável.
- Detalhamento extenso é permitido; a **linha de 95 caracteres continua valendo**.
- Um PRD cita outro pelo identificador (_"PRD-01"_), em texto simples, sem link. O mapa de
  arquivos e dependências fica no documento 99 §8.

### 4. Entrega

Um branch e um PR por PRD, aprovado antes do próximo. No mesmo PR: o arquivo do PRD, a
situação atualizada em `docs/prds/index.md`, a entrada na `nav` do `mkdocs.yml`, o documento
99 §8 e o que a decisão nova mudou nos documentos-fonte e no documento 09.

## Esteira de CI da documentação

Quatro verificações rodam a cada pull request (`.github/workflows/docs-ci.yml`). Todas
podem — e devem — ser rodadas localmente antes de abrir o PR.

| Ferramenta       | O que verifica                                         | Comando local                   |
| ---------------- | ------------------------------------------------------ | ------------------------------- |
| **markdownlint** | Estilo do Markdown, incluindo a linha de 95 caracteres | `npm run lint:md`               |
| **Prettier**     | Formatação (tabelas, listas, espaçamento, ênfase)      | `npm run lint:format`           |
| **Lychee**       | Links internos e externos quebrados                    | `lychee --config lychee.toml .` |
| **MkDocs**       | O site compila em modo `--strict`                      | `mkdocs build --strict`         |

Atalhos: `npm run lint` roda markdownlint + Prettier; **`npm run fix` corrige
automaticamente** o que for corrigível. Rode `npm run fix` antes de commitar — é o caminho
mais rápido para o CI ficar verde.

Preparação do ambiente local (uma vez):

```bash
npm install
python -m venv .venv && .venv/Scripts/activate   # Linux/macOS: source .venv/bin/activate
pip install -r requirements-docs.txt
mkdocs serve                                     # prévia em http://127.0.0.1:8000
```

Regras que a esteira impõe e que valem ao escrever:

- **Blocos de código sempre com linguagem.** Diagramas ASCII usam ` ```text `.
- **Não usar negrito como se fosse título** — se é título, use `####`.
- **Linha de até 95 caracteres** fora de tabelas e blocos de código.
- **Todo arquivo novo em `docs/` precisa entrar na `nav` do `mkdocs.yml`**, senão o build
  `--strict` falha.
- Links para domínios que bloqueiam robôs (LinkedIn, Google Drive, Phaser) ficam em
  `.lycheeignore` e precisam ser conferidos à mão quando mudarem.

O deploy do site no GitHub Pages (`.github/workflows/docs-deploy.yml`) acontece **somente
após merge em `main`** — nunca a partir de um PR.

## Integrações

Merge de PR no GitHub usa **merge commit — nunca squash.**

## Checklist antes de entregar uma revisão de documentação

- [ ] O texto ficou **menor** que antes, sem perder definição?
- [ ] Nenhuma regra foi duplicada — cada assunto está no seu documento-fonte?
- [ ] Nenhum link cruzado entre documentos 01–14 foi introduzido?
- [ ] O doc 99 foi atualizado, se alguma relação entre documentos mudou?
- [ ] Pendências novas entraram no doc 09?
- [ ] Os invariantes do doc 99 §6 continuam válidos?
- [ ] A numeração de seções está contínua e `docs/index.md` reflete a estrutura atual?
- [ ] `npm run lint` e `mkdocs build --strict` passam?
- [ ] Documento novo ou renomeado foi acrescentado à `nav` do `mkdocs.yml`?
- [ ] Se for PRD: todas as seções do modelo estão preenchidas, e cada decisão nova foi gravada
      no documento-fonte e movida no documento 09?
- [ ] Se for PRD: `docs/prds/index.md` e o documento 99 §8 refletem a situação atual?
