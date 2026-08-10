# Como contribuir com o Comunidade Game

O Comunidade Game é uma plataforma educacional gamificada, aberta, feita para comunidades
periféricas. Contribuição aqui não é só código: documentação, trilha, conteúdo educacional,
tradução, teste e revisão contam igual.

Antes de abrir a primeira _issue_ ou o primeiro _pull request_, leia este arquivo inteiro. Ele
é curto de propósito. As regras de governança — quem decide o quê — estão em `GOVERNANCE.md`.

## 1. A regra que governa todas as outras

Este projeto não aceita código que não venha de um requisito escrito. A ordem de autoridade é
esta, da maior para a menor:

```text
1. docs/01-*.md a docs/14-*.md e docs/99-*.md   regra de negócio (fonte única)
2. docs/prds/                                    requisitos de produto (RF-XX-nn, RN-XX-nn)
3. openspec/changes/<change>/                    plano de execução
4. código                                        execução
```

Cada nível apenas executa o de cima. Conflito entre níveis resolve-se **pelo nível superior** —
nunca ajustando o requisito ao código que já foi escrito.

Consequência prática: **uma boa ideia que não está em nenhum PRD não vira _pull request_.** Ela
vira pergunta ao fundador, que decide se ela entra na documentação. Só depois disso ela pode
virar código. Isso frustra no começo e economiza retrabalho no fim.

## 2. Como uma mudança entra

O desenvolvimento é conduzido pelo framework de _Spec-Driven Development_ **OpenSpec**. O
contexto do projeto e as regras de cada artefato estão em `openspec/config.yaml`.

| Etapa                           | Comando          |
| ------------------------------- | ---------------- |
| Pensar antes de propor          | `/opsx:explore`  |
| Criar a _change_ e os artefatos | `/opsx:propose`  |
| Avançar um artefato por vez     | `/opsx:continue` |
| Implementar as tarefas          | `/opsx:apply`    |
| Verificar antes de fechar       | `/opsx:verify`   |
| Arquivar a _change_ concluída   | `/opsx:archive`  |

Cada _change_ recorta **um** PRD e cita, em cada requisito e em cada tarefa, o identificador
que atende (`RF-XX-nn` ou `RN-XX-nn`). Artefato sem âncora em PRD é inválido.

A ordem das _changes_ respeita as ondas e as dependências entre PRDs descritas no documento 99.
A situação de cada PRD está em `docs/prds/index.md`.

### Quando faltar requisito

Requisito ausente, ambíguo ou em contradição com o PRD: **pare e pergunte**. Não preencha
lacuna com suposição, e não resolva a dúvida escrevendo a regra dentro do artefato do OpenSpec
— artefato de execução não cria regra de produto, número, prazo nem provedor.

Decisão nova segue sempre esta ordem:

1. gravar a regra no **documento-fonte** dela (mapa em `docs/99-mapa-de-referencias.md`);
2. mover a linha em `docs/09-topicos-em-aberto-e-sugestoes.md`, de "Decisões pendentes" para
   "Já decididos";
3. atualizar o **PRD** afetado;
4. só então propor a _change_ e implementar.

## 3. Padrões

- **Português do Brasil** em código, comentários, documentação, artefatos e mensagens de
  _commit_.
- **Termos do domínio são preservados**, nunca traduzidos nem renomeados: Guerreiro(a), Mestre,
  Apoiador, Admin, responsável, Comunidade Virtual, trilha, missão, desafio, poder, badge,
  moeda, lastro, livro-razão.
- **Linha de até 95 caracteres** em Markdown, fora de tabelas e blocos de código.
- **Bloco de código sempre com linguagem declarada**; diagrama em arte ASCII usa `text`.
- Mensagem de erro em **linguagem simples** — parte do público tem 6 anos.

### Os invariantes

O documento 99 lista invariantes que qualquer contribuição precisa preservar — entre eles: as
oito aplicações são Web responsivas Mobile First; só o Guerreiro(a) tem autocadastro; o jogo é
somente leitura e não credita pontos; nenhuma atividade acontece sem lastro; nenhum contato
direto entre Apoiador e Guerreiro(a); dado de território tem guarda permanente com anonimização
apenas na saída.

**Contrariar um invariante é defeito, não variação de implementação.** Vale para o código como
vale para o texto.

### Dado de criança

Parte deste sistema trata dado pessoal sensível de criança e adolescente. Consentimento,
anonimização na saída e prazo de guarda são **requisito**, não detalhe de implementação. Ao
mexer em qualquer coisa que toque nisso, leia a seção de LGPD do PRD alvo e a do documento 03
antes de escrever a primeira linha.

## 4. Antes de abrir o _pull request_

Quatro verificações rodam no CI e todas podem ser rodadas localmente:

```bash
npm install
npm run fix      # corrige o que é corrigível — rode sempre antes de commitar
npm run lint     # markdownlint + Prettier
mkdocs build --strict
lychee --config lychee.toml .
```

Preparação do ambiente de documentação, uma vez:

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv/Scripts/activate
pip install -r requirements-docs.txt
mkdocs serve
```

Arquivo novo em `docs/` precisa entrar na `nav` do `mkdocs.yml`, senão o _build_ falha.

## 5. Entrega

- **Um _branch_ e um _pull request_ por _change_**, aprovado antes do próximo.
- O _pull request_ leva junto: os artefatos da _change_, o código, os testes e a documentação
  que aquela _change_ mudou. **O site nunca fica atrasado em relação ao que foi implementado.**
- **_Merge commit_ — nunca _squash_.** O histórico de _commits_ é o lastro do aporte em tempo
  de quem constrói a plataforma, e _squash_ apaga esse lastro.
- O site só vai ao ar depois do _merge_ em `main`, nunca a partir de um _pull request_.

## 6. A licença do que você contribui

O código sai sob **AGPL** e o conteúdo educacional publicado sob **CC BY-SA**. Veja `LICENSE`.

Ao abrir um _pull request_, você contribui sob essas licenças. Quem replicar a plataforma e a
oferecer pela rede abre também as suas modificações; quem apenas consome a API com aplicação
própria não é alcançado pela licença.

> **A definir:** se o projeto vai adotar **DCO** (_Developer Certificate of Origin_), **CLA**
> com cessão de direitos à pessoa jurídica titular, ou nenhum dos dois. A escolha muda quem
> pode relicenciar o conjunto no futuro e precisa ser decidida antes da primeira contribuição
> externa.

## 7. Contribuir sem escrever código

- **Trilha e conteúdo educacional** são autoria de Mestre, dentro da plataforma, não deste
  repositório.
- **Revisão de documentação** é contribuição de primeira classe: as regras de redação estão no
  `CLAUDE.md`.
- **Relato de defeito e proposta de melhoria** cabem em _issue_.
- **Aplicação de terceiro sobre a API** não passa por aqui: a chave é pedida na Área do
  Apoiador Desenvolvedor, na vitrine, e a aplicação de terceiro **lê e não escreve**.

> **`[Proposta]`** O **apoio em código** como modalidade de aporte — melhoria da plataforma,
> aplicação sobre a API e jogo sobre a API valorados em hora-técnica no livro-razão — depende
> do valor-hora de referência e do critério de conversão, ambos em aberto no documento 09.
> Enquanto não for decidido, contribuição em código **não** gera moedas nem Poder Sustentador.

## 8. Conduta

O `docs/13-codigo-de-conduta-versao-previa.md` é o código de conduta **do Guerreiro(a)**, dentro
das trilhas — não governa quem contribui neste repositório.

> **A definir:** o `CODE_OF_CONDUCT.md` dos contribuidores, que é documento distinto daquele.

## 9. O que ainda não está decidido

Estes pontos afetam quem contribui e seguem em aberto no documento 09:

| Tema                                          | O que falta                                       |
| --------------------------------------------- | ------------------------------------------------- |
| DCO, CLA ou nenhum dos dois                   | A escolha, antes da primeira contribuição externa |
| Apoio em código como aporte                   | Valor-hora e critério de conversão em horas       |
| `CODE_OF_CONDUCT.md` dos contribuidores       | O documento                                       |
| Canal entre agentes de IA e humanos           | _Issues_ com _labels_, _Discussions_, _Projects_  |
| Orquestração do fluxo "do explore ao _merge_" | Se a automação com agentes entra aqui             |
| Uso do Slack no fluxo de desenvolvimento      | A decisão                                         |

Enquanto uma linha destas não for decidida, **pergunte** em vez de supor.
