# Governança do Comunidade Game

Este arquivo descreve **quem decide o quê** neste projeto e como uma decisão vira código. Ele
descreve o modelo vigente — não inventa modelo novo. O que ainda não foi decidido está marcado
como tal na seção 8.

Para o processo de contribuição — como abrir _issue_, _branch_ e _pull request_ — veja
`CONTRIBUTING.md`.

## 1. Quem decide hoje

O Comunidade Game está no seu **Ciclo 01** e tem hoje **um mantenedor**: o fundador, que
acumula os papéis de Admin e de primeiro Mestre. Ele decide rumo, escopo, prioridade e o que
entra na documentação normativa.

Não há comitê, votação nem grupo de mantenedores. Isso não é omissão: é o estado real de um
projeto que ainda não teve a sua primeira turma. Quando houver mais gente sustentando o
projeto, o modelo muda — e a forma dessa mudança está em aberto (seção 8).

O que **não** é discricionário, mesmo com um mantenedor só:

- a **hierarquia dos documentos** (seção 2);
- os **invariantes** (seção 4);
- o caminho pelo qual uma decisão nova entra (seção 3).

Mudar qualquer um deles é mudança de rumo, e mudança de rumo se escreve na documentação antes
de existir em código.

## 2. A hierarquia dos documentos

```text
┌──────────────────────────────────────────────────────────────┐
│ docs/01-*.md a docs/14-*.md e docs/99-*.md                   │
│ regra de negócio — FONTE ÚNICA de cada assunto               │
└───────────────────────────┬──────────────────────────────────┘
                            │ deriva
┌───────────────────────────▼──────────────────────────────────┐
│ docs/prds/                                                   │
│ requisitos de produto — RF-XX-nn, RN-XX-nn                   │
└───────────────────────────┬──────────────────────────────────┘
                            │ deriva
┌───────────────────────────▼──────────────────────────────────┐
│ openspec/changes/<change>/                                   │
│ plano de execução — proposal, specs, design, tasks           │
└───────────────────────────┬──────────────────────────────────┘
                            │ executa
┌───────────────────────────▼──────────────────────────────────┐
│ código                                                       │
└──────────────────────────────────────────────────────────────┘
```

Duas regras sustentam isso:

- **Fonte única.** Cada assunto tem **um** documento normativo, listado no documento 99.
  Alterar uma regra significa alterar o documento-fonte dela; os demais, quando precisam citar
  o assunto, resumem em uma frase e nunca repetem a regra completa.
- **Nível de baixo não corrige nível de cima.** Conflito resolve-se sempre pelo nível superior.
  Descobrir na implementação que o PRD está errado **não** autoriza ajustar o PRD ao código:
  autoriza levar a questão ao mantenedor.

O PRD é artefato **derivado** e nunca é fonte única de regra nenhuma. Regra que existe apenas
dentro de um PRD está no lugar errado.

## 3. Como uma decisão nova nasce

Toda decisão nova — venha da escrita de um PRD, de uma _change_ ou de uma conversa — percorre
o mesmo caminho, nesta ordem:

```text
   pergunta ao mantenedor
            │
            ▼
   1. documento-fonte      grava a regra (mapa no documento 99)
            │
            ▼
   2. documento 09         a linha migra de "Decisões pendentes"
            │              para "Já decididos"
            ▼
   3. PRD afetado          aplica a regra, sem repetir o texto normativo
            │
            ▼
   4. change + código      só agora
```

Pular etapa produz o defeito que este projeto mais combate: regra que existe no código e não
existe em lugar nenhum da documentação.

O `docs/09-topicos-em-aberto-e-sugestoes.md` é o registro público do que ainda não foi
decidido. Ele é pauta, não decisão: nada ali vale como regra até migrar para "Já decididos" e
ser gravado no documento-fonte.

## 4. Os invariantes

O documento 99 mantém uma lista de invariantes — coerências que qualquer edição de texto e
qualquer linha de código precisam preservar. Entre eles: as oito aplicações são Web responsivas
Mobile First; a faixa é de 6 a 16 anos, com progressão por dificuldade e nunca por idade; só o
Guerreiro(a) tem autocadastro e login não cria cadastro; toda trilha abre em sondagem, tem
coleta de dados reais e termina em criação original; o jogo é público, somente leitura e não
credita pontos; nenhuma atividade acontece sem lastro; nenhum contato direto entre Apoiador e
Guerreiro(a); aporte aparece em moedas, nunca em reais; a personalização por IA adapta na
sessão e não perfila a criança.

**Contrariar um invariante é erro, não variação.** Mudar um invariante é decisão de rumo e
segue o caminho da seção 3, começando pelo documento-fonte.

## 5. Papéis na plataforma × papéis no repositório

São coisas diferentes e não se confundem.

| Papel na plataforma | O que faz                                                 | Papel no repositório |
| ------------------- | --------------------------------------------------------- | -------------------- |
| Admin               | Cadastra, aprova, homologa aporte, audita, opera o ciclo  | Nenhum, por si só    |
| Mestre              | Cria trilha e conteúdo, lança o que é seu                 | Nenhum, por si só    |
| Apoiador            | Aporta recurso; pode pedir chave de API na vitrine        | Nenhum, por si só    |
| Guerreiro(a)        | Percorre trilhas; altera o código do jogo como atividade  | Nenhum, por si só    |
| Responsável         | Consente, autoriza e acompanha                            | Nenhum               |
| —                   | Quem escreve código, documentação ou teste no repositório | Contribuidor         |
| —                   | Quem aprova e integra _pull request_                      | Mantenedor           |

Ser Admin da plataforma não dá acesso de escrita ao repositório, e contribuir com código não
cria persona na plataforma. Novos Admins entram manualmente por outro Admin, dentro da
plataforma; acesso de escrita ao repositório é concedido pelo mantenedor.

O Guerreiro(a) altera o código do jogo **como atividade de trilha**, dentro da plataforma. Esse
caminho não passa por _pull request_ neste repositório.

## 6. Licença e titularidade

- **Código: AGPL.** Quem replica a plataforma e a oferece pela rede abre também as suas
  modificações. Quem apenas consome a API com aplicação própria não é alcançado.
- **Conteúdo educacional publicado: CC BY-SA**, com crédito ao Mestre autor.
- **Titular do direito autoral do código:** a pessoa jurídica vinculada ao projeto, descrita no
  documento 04. É ela quem responde pelo código e quem poderia relicenciá-lo.

O texto integral está em `LICENSE`.

A escolha da AGPL não é detalhe jurídico: é o que impede que a plataforma construída por uma
comunidade seja fechada como serviço privado por quem a replicar.

## 7. Replicar em outra comunidade

Replicação é objetivo declarado do projeto, não tolerância. O código é aberto para que qualquer
comunidade rode a sua própria instância, e a escolha de contêiner e banco de dados portáteis
existe para que isso não dependa de um provedor de nuvem específico.

Quem replicar deve: manter o código sob AGPL, publicar as modificações que oferecer pela rede,
e creditar os Mestres autores do conteúdo que reaproveitar.

> **A definir:** **o uso do nome e da marca** ao replicar. Rodar o código é livre pela licença;
> chamar a instância replicada de "Comunidade Game" é outra coisa, e ainda não há regra. Até
> que exista, combine com o mantenedor.

## 8. O que ainda não está decidido

| Tema                                     | O que falta                                                                                |
| ---------------------------------------- | ------------------------------------------------------------------------------------------ |
| Modelo de decisão com mais de uma pessoa | Quem aprova mudança de rumo quando o projeto deixar de ter um mantenedor só                |
| Marca e uso do nome                      | Quem pode chamar de "Comunidade Game" a instância que replicou                             |
| DCO, CLA ou nenhum dos dois              | Como o direito autoral da contribuição externa se relaciona com o titular                  |
| `CODE_OF_CONDUCT.md`                     | O código de conduta dos contribuidores, distinto do código de conduta do Guerreiro(a)      |
| Forma jurídica sem fins lucrativos       | Arranjo para editais e recursos públicos, que costumam não aceitar empresa como proponente |
| Separação contábil                       | Entre a atividade comercial da pessoa jurídica e os recursos do projeto                    |

Todos estão registrados no documento 09 e seguem o caminho da seção 3 quando forem decididos.
