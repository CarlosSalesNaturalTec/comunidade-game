# 14 — Gamificação do Apoiador

> A camada de jogo de quem sustenta o projeto: os níveis de necessidade da plataforma, as
> missões que os cobrem, as modalidades de apoio, a progressão e o reconhecimento. Moeda,
> livro-razão e desafios extras ficam no documento 04; persona e solicitação de participação,
> no documento 02; o motor de pontos do Guerreiro(a), no documento 11.

## 1. Regra de separação

Três distinções que nenhuma edição pode borrar:

- **O Apoiador não pontua.** Ele progride em **moedas**, **selos** e **níveis de sustento**.
  Ponto é do Guerreiro(a) e nasce de realização.
- **Missão do Apoiador não é missão da trilha.** A da trilha é a menor unidade de progressão
  do Guerreiro(a) e é trava de publicação. A do Apoiador é chamado de sustento dirigido ao
  adulto, e nunca aparece em tela de criança.
- **Missão do Apoiador não é desafio extra.** O desafio extra vai do Apoiador ao Guerreiro(a).
  A missão vem da plataforma ao Apoiador.

## 2. Os quatro níveis de necessidade

O que a plataforma precisa, ordenado pelo que quebra primeiro se faltar:

| Nível            | O que sustenta                                               | Se falta                  |
| ---------------- | ------------------------------------------------------------ | ------------------------- |
| **1 Existir**    | Infraestrutura digital e código da plataforma                | A plataforma não roda     |
| **2 Acontecer**  | Ponto de apoio, equipamento, hora-aula, lanche, insumo       | O encontro não acontece   |
| **3 Reconhecer** | Recompensa de marco, acervo, camisa                          | O marco não fecha         |
| **4 Permanecer** | Reposição, formação de multiplicadores, conteúdo educacional | O ciclo seguinte não abre |

O nível 2 é a leitura direta da regra de lastro: sem recurso provido, a atividade não ocorre.

## 3. Modalidades de apoio

| Modalidade                    | Porta                                      | Valoração                   | Situação            |
| ----------------------------- | ------------------------------------------ | --------------------------- | ------------------- |
| Dinheiro (PIX)                | Pré-cadastro na App 08                     | Escada de valores sugeridos | vigente             |
| Insumo, equipamento, alimento | Formulário da vitrine                      | Tabela de referência        | valoração a definir |
| Serviço                       | Formulário da vitrine                      | Tabela de referência        | valoração a definir |
| Conteúdo educacional          | Formulário da vitrine                      | Tabela de referência        | valoração a definir |
| **Código**                    | Área do Apoiador Desenvolvedor, na vitrine | Hora-técnica pelos commits  | `[Proposta]`        |
| Divulgação                    | Formulário da vitrine                      | Não valorada                | vigente             |
| Ensinar — virar Mestre        | Formulário da vitrine                      | Não é aporte                | vigente             |

A entrada de material, serviço e conteúdo é vigente; o que falta é a conversão em moedas.
O conteúdo educacional doado sai sob a mesma licença dos demais, com crédito ao autor.

**`[Proposta]` Apoio em código.** Tem três formas — melhoria da plataforma, aplicação sobre a
API e jogo sobre a API — e é aporte como qualquer outro, sem persona nova. Aplicação de
terceiro **lê e não escreve**: a regra do jogo somente leitura vale para todas elas. A
valoração aproveita o precedente já vigente de lastrear a construção da plataforma no
histórico de commits do repositório. Depende da governança de código aberto do projeto
(documento 09).

## 4. Perfis: pessoa física e pessoa jurídica

O perfil é **declarado, nunca verificado** — a plataforma não coleta CPF nem CNPJ. Quem
escolhe é o próprio Apoiador, no pré-cadastro, e o que o comprova são os artefatos que um
Admin anexa ao cadastro.

| O que muda              | Pessoa física                       | Pessoa jurídica                        |
| ----------------------- | ----------------------------------- | -------------------------------------- |
| Escada de valores       | Degraus menores                     | Degraus maiores                        |
| Identidade do card      | Nick e imagem escolhida             | Nick e logomarca                       |
| Destaque da efetividade | O que aconteceu por causa do aporte | Cobertura de ODS e frentes sustentadas |

Não muda nada mais: moldura comum do card, piso de moedas do avatar próprio, ausência de
publicidade e ausência de qualquer contato com criança valem igual para os dois.

## 5. Missão do Apoiador

Tarefa que a plataforma propõe a quem apoia, derivada de uma **necessidade de recurso
publicada** ou de uma frente do ciclo.

**Atributos:** nível de necessidade, o que se pede, quantidade em moedas ou em itens, prazo,
quem valida e selo que rende.

**Regras:**

- Missão só se conclui com **aporte homologado por Admin**. Declarar não conclui, e ninguém
  homologa o próprio aporte.
- Missão rende **moeda e selo**, nunca ponto.
- **Missão coletiva.** Várias pessoas cobrem a mesma necessidade em aportes parciais, e a
  missão conclui quando o saldo fecha. Cada uma recebe as moedas do que aportou e o selo de
  mutirão.
- Missão sem necessidade real por trás não é publicada: o que se pede existe no livro-razão
  antes de virar chamado.

## 6. Catálogo de missões

Arquétipos. As quantidades e os prazos do Ciclo 01 ficam no documento 08 e no PRD-14.

| Missão                           | Nível      | O que entrega                              | Modalidade  |
| -------------------------------- | ---------- | ------------------------------------------ | ----------- |
| Mantenha a luz acesa             | Existir    | Um mês de servidor e armazenamento         | Dinheiro    |
| `[Proposta]` Abra a porta da API | Existir    | Melhoria aceita no repositório             | Código      |
| `[Proposta]` Traga um jogo novo  | Existir    | Aplicação ou jogo sobre a API, homologado  | Código      |
| O lanche do encontro             | Acontecer  | O lanche de um encontro                    | Dinheiro    |
| A aula que não pode faltar       | Acontecer  | A hora-aula de um Mestre                   | Dinheiro    |
| Bancada equipada                 | Acontecer  | Insumos da oficina                         | Insumo      |
| Um aparelho a mais               | Acontecer  | Notebook, tablet ou smartphone             | Equipamento |
| Teto para o acervo               | Acontecer  | Espaço com guarda do acervo                | Serviço     |
| Ida e volta                      | Acontecer  | Transporte de material ou à culminância    | Serviço     |
| Marco cumprido                   | Reconhecer | A recompensa de um marco da trilha         | Dinheiro    |
| Kit da mesa                      | Reconhecer | Kits de alimentos do catálogo              | Alimento    |
| Camisa do time                   | Reconhecer | Camisas do catálogo                        | Insumo      |
| A culminância merece plateia     | Reconhecer | Registro e apresentação pública da criação | Serviço     |
| Reposição sem cobrança           | Permanecer | Bem perdido ou danificado, reposto         | Insumo      |
| Quem ensina fica                 | Permanecer | Formação de um multiplicador               | Dinheiro    |
| Conteúdo que fica                | Permanecer | Material validado por um Mestre            | Conteúdo    |
| Passe o bastão                   | Permanecer | Alguém que assume uma trilha como Mestre   | Ensinar     |

"Reposição sem cobrança" traduz a regra do Código de Conduta: dano acidental nunca vira
dívida da família, vira necessidade a ser aportada.

## 7. Níveis de sustento

**Nível é percurso, não volume** — a mesma lógica dos níveis do Guerreiro(a). Sobe quem cobre
**frentes diferentes**, não quem transfere mais dinheiro: cobrir um lanche e repor um livro
vale mais que só transferir valor.

| Nível | Nome                   | Condição verificável                             |
| ----- | ---------------------- | ------------------------------------------------ |
| 1     | Apoiador               | Primeiro aporte homologado                       |
| 2     | Sustenta o encontro    | Missão homologada no nível Acontecer             |
| 3     | Sustenta o ciclo       | Missões em dois níveis de necessidade diferentes |
| 4     | Sustenta a permanência | Missões em três níveis, um deles o Permanecer    |
| **5** | **Multiplicador**      | Virou Mestre                                     |

**Nível conquistado não regride.** O piso de moedas do avatar próprio continua o que é —
identidade, não progressão.

Adotado o apoio em código, o **aporte em código homologado** passa a ser a segunda via para o
Nível 5. Enquanto ele for proposta, a via é uma só.

O Nível 5 fecha o mesmo arco do Guerreiro(a): quem chega ao topo volta como multiplicador.

## 8. Selos do Apoiador

Selo é o reconhecimento do Apoiador, como o badge é o do Guerreiro(a). Quatro famílias:

| Família              | Exemplos                                               |
| -------------------- | ------------------------------------------------------ |
| **De frente**        | Um por nível de necessidade coberto                    |
| **De modalidade**    | Dinheiro, material, serviço, conteúdo, código          |
| **De ato**           | Primeiro a cobrir uma necessidade · mutirão · absorção |
| **De multiplicação** | Virou Mestre · aplicação ou jogo publicado sobre a API |

Selo é por frente e por ato, **nunca global**, e o já conquistado não se perde. Os selos ligados
a código só existem se a modalidade for adotada.

## 9. Técnicas admitidas e vedadas

Admitidas:

- Necessidade publicada com **progresso visível em moedas**.
- **Urgência real e datada** — a atividade tem data e está pendente de lastro.
- Reciprocidade rastreável pelo painel vivo de efetividade.
- Reconhecimento público na moldura comum de todos os apoiadores.
- Coleção de selos, que premia **diversidade** e não volume.
- Missão coletiva.
- Convite ao próximo passo **uma vez, sem insistir**.

Vedadas:

- **Ranking de apoiadores por dinheiro.** Há coleção e nível, não pódio de valor.
- Urgência fabricada, contagem regressiva artificial, escassez inventada.
- Qualquer mecânica que use a criança como gatilho de doação — foto, nome, história individual
  ou apadrinhamento de um Guerreiro(a).
- **Vantagem comprada.** Moeda nenhuma abre dado de criança, canal de contato, prioridade
  pedagógica ou aprovação mais rápida de desafio.
- Publicidade e patrocínio.
- Recorrência punitiva: perder um mês não retira selo nem nível conquistado.

## 10. Portas de entrada

Continuam **duas**, e nenhuma delas cadastra ninguém. O que muda é o garfo na entrada: a
chamada "Quero participar" pergunta **o que a pessoa traz** e a encaminha.

| O que traz                    | Para onde vai          | O que comprova               |
| ----------------------------- | ---------------------- | ---------------------------- |
| Dinheiro                      | Pré-cadastro na App 08 | Comprovante da transferência |
| Insumo, equipamento, alimento | Formulário da vitrine  | Descrição e foto do bem      |
| Serviço                       | Formulário da vitrine  | O que faz e quando pode      |
| Conteúdo educacional          | Formulário da vitrine  | Amostra do material          |
| Código                        | Formulário da vitrine  | Repositório e portfólio      |
| Divulgação                    | Formulário da vitrine  | Alcance e mídia própria      |
| Ensinar                       | Formulário da vitrine  | Artefatos da habilidade      |

As duas portas terminam na mesma fila de avaliação do Admin, com o prazo de resposta já
definido. Quem cadastra continua sendo um Admin.

## 11. Reflexos nas aplicações

| Aplicação                 | O que passa a ter                                                                                |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| App 06 — Vitrine          | Garfo de modalidade na chamada; a vitrine das aplicações de terceiros depende do apoio em código |
| App 08 — Área do Apoiador | Missões, níveis de sustento e selos                                                              |
| App 03 — Gestão           | Fila separada por modalidade e homologação que conclui a missão                                  |
| App 09 — Área do Mestre   | Validação do conteúdo educacional doado                                                          |

## 12. Pendências

Seguem na pauta do documento 09: a tabela de valoração dos aportes não financeiros, a
valoração da hora-técnica de código, a governança de código aberto e a chave de acesso das
aplicações de terceiros, e o catálogo de missões do Ciclo 01 com quantidades e prazos.
