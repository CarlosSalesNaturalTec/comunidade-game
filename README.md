# Comunidade Game

Plataforma educacional gamificada, de código aberto, para comunidades periféricas — um "jogo"
cujas partidas acontecem na vida real. Ela conecta **Guerreiros e Guerreiras**, **Mestres** e
**Apoiadores** em torno de trilhas de aprendizagem que terminam em criação própria e em dados
reais sobre o território onde essas pessoas moram.

> Interação digital com comunidades para oferecer orientação educacional, informação e geração
> de dados que auxiliem na tomada de decisões — e para que essas ações e esses dados retornem
> como impacto positivo para a própria comunidade.

O que a plataforma produz não sai da comunidade: volta para ela. O Guerreiro(a) aprende e
realiza; o que ele registra dá à comunidade evidência para decidir, em vez de percepção; a
conquista ganha visibilidade e atrai apoio; o apoio custeia novas atividades; quem chega
ao topo volta como multiplicador. O documento 01 detalha o ciclo.

**Situação.** Documentação validada e treze PRDs aprovados; a implementação corre por fatias.
A primeira implantação real é o **Case 01 — Comunidade Guerreira Zeferina** (Salvador/BA), no
**Ciclo 01, de agosto a dezembro de 2026**.

## Como a plataforma está montada

Um **Backend API** — o núcleo — e **oito aplicações web** que o consomem. Toda aplicação se
identifica por **chave própria**, inclusive as do projeto: **sem chave a API não responde**. O
que a leitura pública dispensa é o login da pessoa — na vitrine e no jogo quem se identifica é
a aplicação, não o visitante. Escrita e gestão exigem, além da chave, a credencial da persona.

| Aplicação   | O que é                                            | Quem usa                             |
| ----------- | -------------------------------------------------- | ------------------------------------ |
| Backend API | O núcleo: regra de negócio, dados e contrato `/v1` | As oito aplicações e terceiros       |
| App 01      | Aula presencial — onboarding e trilhas em equipe   | Guerreiros e Guerreiras, no encontro |
| App 03      | Gestão                                             | Admin                                |
| App 04      | Jogo em JavaScript                                 | Qualquer pessoa, sem login           |
| App 05      | Área do Guerreiro(a)                               | Guerreiros e Guerreiras              |
| App 06      | Vitrine pública — a raiz do domínio                | Qualquer pessoa, sem login           |
| App 07      | Área dos pais e responsáveis                       | Responsáveis                         |
| App 08      | Área do Apoiador                                   | Apoiadores                           |
| App 09      | Área do Mestre                                     | Mestres                              |

Todas são **Web Apps responsivos, Mobile First** — sem aplicativo nativo e sem aplicação sobre
mensageria de terceiros. O documento 03 é a fonte da arquitetura.

### Construir sobre a API

A API é aberta a aplicações de terceiros, sob **contrato de somente leitura**: nada que se
construa sobre ela escreve no domínio, e a chave não amplia direito nenhum. Quem quer construir
pede a chave na **Área do Apoiador Desenvolvedor**, seção pública da vitrine, que reúne um
assistente de chat sobre esta documentação, os links da documentação e do repositório e o
formulário do pedido. Emitida a chave, há **30 dias para apresentar a URL** do que foi
construído; não apresentada, a chave é revogada — e pedir outra é sempre possível.

O contrato em **OpenAPI** fica fora do prefixo de versão e aberto, sem chave: quem ainda não
tem uma precisa ler o contrato para decidir pedi-la.

## Stack do Ciclo 01

| Camada       | Escolha                                                                  |
| ------------ | ------------------------------------------------------------------------ |
| Backend API  | Python 3.12 com FastAPI, SQLAlchemy e Alembic, em contêiner no Cloud Run |
| Banco        | PostgreSQL com PostGIS — inclusive as séries temporais do território     |
| Frontends    | React com TypeScript sobre Vite, saída estática no Firebase Hosting      |
| Jogo         | Phaser                                                                   |
| Documentação | MkDocs                                                                   |
| Região       | `southamerica-east1` (São Paulo)                                         |

Contêiner e banco são portáteis: outra comunidade replica a plataforma fora do Google Cloud.

## Organização do repositório

Monorepo, uma pasta por aplicação, com o número da aplicação no nome (documento 03 §1.2):

```text
comunidade-game/
├─ backend/     Backend API — o núcleo que todas consomem
├─ apps/        as aplicações web, uma pasta por aplicação
├─ jogos/       o jogo, fora de apps/ porque a API admite outros
├─ comum/       o que as aplicações compartilham — tokens, fontes e componentes
├─ docs/        documentação do produto — o site MkDocs
└─ openspec/    artefatos de implementação
```

Cada pasta de código tem o seu próprio `README.md`, com os comandos e as variáveis de ambiente
dela, e a verificação automática dela no CI.

## Como rodar localmente

```bash
npm install                                      # aplicações e ferramentas de texto
python -m venv .venv && source .venv/bin/activate # Windows: .venv/Scripts/activate
pip install -r requirements-docs.txt             # documentação
cd backend && uv sync --dev                      # núcleo; Postgres de teste em CG_DSN_BANCO_TESTE
```

| O que verificar    | Comando                                                                  |
| ------------------ | ------------------------------------------------------------------------ |
| Núcleo             | `ruff format --check .`, `ruff check .` e `pytest`, dentro de `backend/` |
| Aplicações e jogos | `biome check .` e `vitest run`, dentro da pasta                          |
| Documentação       | `npm run lint` e `mkdocs build --strict`, na raiz                        |

## Como contribuir

Contribuição aqui não é só código: documentação, trilha, conteúdo educacional, tradução, teste
e revisão contam igual. Uma regra governa todas as outras — **este projeto não aceita código
que não venha de um requisito escrito**, e a ordem de autoridade vai do documento de negócio ao
código, nunca ao contrário. Boa ideia que não está em nenhum PRD vira pergunta ao
fundador, não _pull request_.

O desenvolvimento é conduzido pelo framework de _Spec-Driven Development_ **OpenSpec**, uma
fatia por _change_. Leia o [`CONTRIBUTING.md`](CONTRIBUTING.md) inteiro antes da primeira
_issue_ — ele é curto de propósito.

- [`GOVERNANCE.md`](GOVERNANCE.md) — quem decide o quê
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) — como se convive aqui
- [`CLA.md`](CLA.md) — toda contribuição externa entra por CLA; sem ele o _pull request_
  não é integrado

## Licenças

- **Código: AGPL** ([`LICENSE`](LICENSE)). Quem replica a plataforma e a oferece pela rede abre
  também as suas modificações. Quem apenas **consome a API** com aplicação própria não é
  alcançado: usar a API pela rede não torna a aplicação derivada.
- **Conteúdo educacional publicado: CC BY-SA.** Qualquer um usa e adapta, creditando o Mestre
  autor, e o derivado herda a mesma licença.

A titularidade do direito autoral do código é da pessoa jurídica vinculada ao projeto, e
é o que o CLA preserva.

## Documentação

A documentação completa do produto está publicada em
<https://carlossalesnaturaltec.github.io/comunidade-game/> e versionada em
[`docs/`](docs/index.md). Ela é a fonte: este arquivo é a porta de entrada e não decide nada.

**Construção assistida por IA, sob direção humana.** Os artefatos da plataforma são construídos
com auxílio de ferramentas de IA; a idealização, o contexto humano e social e as decisões são
humanas. A nota pública de transparência, na vitrine, declara esse uso e o das IAs que atendem
as pessoas na plataforma.
