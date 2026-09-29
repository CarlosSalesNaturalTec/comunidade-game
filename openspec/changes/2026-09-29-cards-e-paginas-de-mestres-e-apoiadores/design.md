# Design

## Context

O padrão da leitura pública já está consolidado em
`openspec/specs/leitura-publica-da-vitrine/spec.md` e em `backend/src/nucleo/vitrine/`:
roteador incluído por `incluir_roteador_de_dados` (chave de aplicação, sem token de sessão),
listagem paginada por cursor e composição montada na própria listagem, para não cair no freio
por origem. Esta fatia **aplica** esse padrão a dois papéis novos; o que ela decide é de onde
vem cada campo que o documento 11 §8.2 atribui às variantes Mestre e Apoiador, já que nenhum
deles tem campo próprio na persona.

Tudo o que a fatia lê já existe: `Persona`, `Nick`, `ArtefatoComprobatorio`, `Trilha`, `Poder`,
`SeloDoApoiador`, `DesafioExtra`, `ConclusaoDoDesafioExtra`, `moedas_acumuladas_de` e
`contagem_de_absorcoes_de`. **Nenhuma entidade nova, nenhuma migração, nenhuma escrita.**

## Goals / Non-Goals

**Goals:**

- As quatro rotas públicas — listagem e leitura individual de cada papel — sobre o mesmo
  contrato de listagem das demais rotas da vitrine.
- Uma só projeção por papel, servindo card e página, como a fatia 2 fez com a carta do
  Guerreiro(a).
- O portão do aporte homologado e o piso do avatar resolvidos **no núcleo**, nunca na tela.

**Non-Goals:**

- Página individual do poder: a seção recebe os Mestres responsáveis, e nada mais.
- Qualquer leitura por nick de adulto — o nick é opcional, e a busca por nick da vitrine
  continua sendo só a do Guerreiro(a).

## Decisions

### 1. A leitura individual é por identificador, não por nick

O `RF-03-11` e o freio de `consulta_por_nick` existem porque o nick do Guerreiro(a) é
enumerável e a recusa precisa ser indistinta. Adulto pode **não ter nick**, então a página
individual de Mestre e de Apoiador responde pelo **identificador da persona**, que a listagem
já devolve. _Alternativa descartada:_ por nick, que deixaria sem página quem ainda não o
definiu.

**Sem freio por origem próprio** nestas rotas: a cota por faixa da chave, que a capacidade
`protecao-das-rotas-publicas` já aplica, é o que cobre listagem e leitura por identificador —
o freio por origem é da superfície de busca, não da navegação por card.

### 2. A identificação sai declarada, nunca implícita

A saída traz a identificação **e o que ela é** — nick ou nome —, para que a carta nunca
apresente nome civil no lugar reservado ao nick. É a forma mínima de aplicar a decisão do
fundador de 2026-09-29 sem que a tela tenha de adivinhar. _Alternativa descartada:_ um só
campo `nick` preenchido com o nome, que apagaria a diferença na superfície e no teste.

### 3. O total do Apoiador é o acumulado, não o Poder Sustentador

`moedas_acumuladas_de` mede o que entrou em aportes homologados e **não regride**;
`poder_sustentador_de` cai quando um ressarcimento é pago. O `RF-03-66` e o `RN-14-11` falam
de direito que não regride, e o `RF-03-55` de "total de moedas aportadas" — logo, o acumulado.
É a mesma medida que `personas/regra.py` já usa para liberar o avatar próprio, e usar a outra
faria o card discordar da App 08.

### 4. O piso do avatar é resolvido no núcleo

A resposta traz o avatar **já resolvido**: o próprio quando o Apoiador alcançou as 10 moedas,
e o sinal de avatar padrão quando não. Assim a tela nunca recebe um avatar que não pode
exibir, e a regra mora num lugar só. O mesmo sinal cobre o avatar que **falta** em qualquer
papel (documento 15 §7.3).

### 5. Os campos sem coluna própria são derivados de dado real

| Campo do documento 11 §8.2         | De onde vem                                                            |
| ---------------------------------- | ---------------------------------------------------------------------- |
| Áreas de habilidade do Mestre      | `area_do_conhecimento` das trilhas publicadas de autoria dele          |
| Trilhas de autoria                 | `Trilha.autor_id`, situação publicada                                  |
| Selo de sustento do Mestre         | `contagem_de_absorcoes_de`, a mesma do Poder Sustentador               |
| Prova pública (os dois papéis)     | `ArtefatoComprobatorio` — endereço e rótulo, sem tipo                  |
| Nível de sustento e selos          | `SeloDoApoiador` e o nível derivado das frentes cobertas               |
| Desafios propostos e efetividade   | `DesafioExtra` do proponente, com `ConclusaoDoDesafioExtra` contada    |
| Mestres responsáveis de um poder   | autores das trilhas publicadas daquele poder, deduplicados             |

O artefato comprobatório **não tem tipo**: currículo, portfólio e rede social são o mesmo
registro, distinguidos pelo rótulo que quem declarou escreveu. O `RF-03-07` sai atendido pela
lista de links com rótulo, que é a forma que o Ciclo 01 decidiu para a prova.

### 6. A efetividade pública é a projeção agregada, não o painel da App 08

A capacidade `efetividade-do-apoio` permanece restrita ao próprio Apoiador. O que a vitrine
publica é outra projeção, com **trilha, período e contagem de conclusões** — a decisão do
fundador de 2026-09-29 —, montada direto de `DesafioExtra` e `ConclusaoDoDesafioExtra`, sem
tocar naquela capacidade. Nada de nick, avatar ou dado de quem concluiu, e o direcionado sai
apenas como "houve conclusão".

### 7. A ordem é alfabética, porque pódio é proibido

`RN-14-38` proíbe ordenar apoiadores por valor. A listagem ordena pela identificação exibida,
o mesmo critério das demais listagens da vitrine, e o cursor de paginação segue esse campo.

### 8. As duas decisões novas descem pelo fluxo antes do código

A hierarquia do `CLAUDE.md` não admite decisão nascendo em artefato do OpenSpec. O **nome no
lugar do nick ausente** e a **efetividade pública com trilha e período** mudam o que o
documento 11 §8.2 permite em público: entram primeiro no documento 11 §8.2, depois na tabela
do documento 09 §1 como já decididos, depois no PRD-03, e só então no código. As tarefas
seguem essa ordem.

## Risks / Trade-offs

- **O nome civil do adulto passa a aparecer em público** → só de Mestre e de Apoiador, que o
  PRD-03 §4 já descreve como quem "aparece com a prova pública", e nunca de Guerreiro(a); a
  spec grava a proibição explícita para criança e adolescente.
- **Áreas de habilidade derivadas deixam sem áreas o Mestre que ainda não publicou trilha** →
  a regra da carta pela metade já cobre: ele é apresentado em outra forma, não em carta vazia.
- **Contar conclusões por desafio é uma consulta por item** → a contagem sai agregada numa
  consulta só por Apoiador, no mesmo cuidado que a fatia 2 tomou ao montar a carta na
  listagem, para não multiplicar consulta por card.
- **`moedas_acumuladas_de` e `contagem_de_absorcoes_de` passam a ser chamadas em rota
  pública** → as duas já são leitura derivada de lançamentos homologados, sem dado sensível;
  a rota pública de Poder Sustentador já as expõe hoje.
