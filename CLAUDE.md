# CLAUDE.md — Regras de trabalho neste repositório

Repositório do **Comunidade Game** — plataforma educacional gamificada, open source, para
comunidades periféricas. Neste momento o repositório **não contém código**: contém apenas a
documentação do projeto, na pasta `docs/`.

## Estado atual e próxima etapa

1. **Agora:** revisão e validação humana de todos os documentos de `docs/`.
2. **Depois da validação:** geração dos **PRDs** (_Product Requirements Documents_), a partir
   do documento `docs/08-base-para-prds.md`.
3. **Depois dos PRDs:** desenvolvimento das sete aplicações e do Backend API.

Não iniciar geração de PRD nem de código sem sinal explícito do fundador de que a documentação
foi validada.

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
- **Exceção única:** `docs/08-base-para-prds.md` é o capítulo dos PRDs e **pode** ter
  detalhamento extenso. Só ele.

### 2. Fonte única — nunca duplicar

Cada assunto tem **um** documento normativo, listado em `docs/99-mapa-de-referencias.md` §1.

- Ao alterar uma regra, altere **o documento-fonte** dela.
- Se outro documento precisa mencionar o assunto, resuma em **uma frase** e não repita a regra
  completa, a tabela nem os números.
- Ao encontrar duplicidade, consolide no documento-fonte e reduza a menção nos demais.

### 3. Referências entre documentos ficam no doc 99

- Os documentos 01–13 **não** carregam links `[XX §Y](arquivo.md#ancora)` entre si. Quando o
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
`docs/99-mapa-de-referencias.md` §6 (sete aplicações Web/Mobile First, faixa 6–16, autocadastro
só do Jogador, coleta obrigatória em toda trilha, jogo que não credita pontos, lastro, guarda
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

## Checklist antes de entregar uma revisão de documentação

- [ ] O texto ficou **menor** que antes, sem perder definição?
- [ ] Nenhuma regra foi duplicada — cada assunto está no seu documento-fonte?
- [ ] Nenhum link cruzado entre documentos 01–13 foi introduzido?
- [ ] O doc 99 foi atualizado, se alguma relação entre documentos mudou?
- [ ] Pendências novas entraram no doc 09?
- [ ] Os invariantes do doc 99 §6 continuam válidos?
- [ ] A numeração de seções está contínua e `docs/index.md` reflete a estrutura atual?
- [ ] `npm run lint` e `mkdocs build --strict` passam?
- [ ] Documento novo ou renomeado foi acrescentado à `nav` do `mkdocs.yml`?
