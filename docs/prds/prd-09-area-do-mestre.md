# PRD-09 — App 09: Área do Mestre (autoria e operação)

## 1. Identificação

| Campo            | Valor                                                       |
| ---------------- | ----------------------------------------------------------- |
| PRD              | PRD-09                                                      |
| Aplicação        | App 09 — Área do Mestre                                     |
| Onda             | 3                                                           |
| Situação         | aprovado                                                    |
| Versão e data    | v3 — 2026-08-05                                             |
| Depende de       | PRD-01                                                      |
| Documentos-fonte | 02 §§1–4, 03 §§1, 11, 05 §§3, 5, 6, 06, 07, 11 §§2, 4, 5, 7 |

## 2. Contexto e objetivo

A App 09 é a bancada de trabalho de quem ensina. É aqui que a trilha nasce — pontos,
conteúdo, bibliografia, desafios, coleta e culminância — e é daqui que o Mestre conduz o que é
dele: as suas turmas, os seus lançamentos, as suas necessidades de recurso. A fronteira com a
App 03 é simples e não se negocia: **a gestão cadastra, aprova e opera o dia; o Mestre cria e
lança o que é seu**.

Sem esta aplicação não existe conteúdo a percorrer. A Área do Guerreiro(a) (PRD-05) guia o
Guerreiro(a) por uma trilha que precisa ter sido escrita antes, e as trilhas 1 e 2 do Ciclo 01
— Robô Educa e Batalha de Laser — são o teste do modelo de autoria: se a ferramenta modela
essas duas, modela as demais.

O modelo é **agnóstico de área do conhecimento** e essa é a exigência mais dura deste PRD.
Nenhum campo, nenhuma tela e nenhum fluxo pode pressupor que o Mestre entenda de tecnologia:
ele pode ser de humanas, de artes, de esporte ou de cultura, e precisa publicar uma trilha
inteira sem escrever uma linha de código.

## 3. Escopo

### 3.1 Dentro do escopo

- **Autoria da trilha**: criação, pontos de trilha em sequência com dificuldade gradual,
  paginação pelas etapas do ciclo e publicação pelo próprio Mestre.
- **Atividades de cada ponto de trilha**, com modalidade (individual ou em equipe) e formato
  (presencial ou on-line) declarados pelo Mestre.
- **Recompensa de cada marco** — desbloqueio de ponto, etapa, batalha ou culminância —, com
  lastro exigido antes da publicação e entrega confirmada pelo Mestre.
- **Conteúdo do ponto**: texto formatado com imagens, link externo, upload de vídeo e de
  arquivo hospedados pela plataforma, e bibliografia de apoio por ponto.
- **Desafios**: desbloqueio do ponto, desafio de coleta de dados reais e culminância com a
  criação original — os dois últimos como **trava de publicação**.
- **Validação da criação original** entregue pelo Guerreiro(a) ou pela equipe, com autoria
  creditada e badge de autoria.
- **Auditoria por amostragem** dos registros de coleta das próprias trilhas.
- **Banco de perguntas do Quiz ao Vivo**, cadastrado aqui; a partida é conduzida na App 03.
- **Minhas turmas**: lançamento de atividades realizadas, presenças, resultados, méritos e
  pontuação negativa das aulas que o Mestre ministra.
- **Validação pedagógica dos desafios extras** propostos por Apoiadores para as suas trilhas.
- **Necessidades de recurso** das suas atividades, aporte por absorção e acompanhamento do
  ressarcimento.
- **Aprovação das solicitações de novo local** dos Guerreiros e Guerreiras das suas trilhas.
- **Cadastro do responsável** que se apresentou no encontro e vínculo com Guerreiros e
  Guerreiras já cadastrados.
- **Artefatos comprobatórios** da habilidade do Mestre, que alimentam a sua página na vitrine.
- **Registro de propostas** de evolução da plataforma, na fila única da gestão.
- **Disciplinas e conteúdo do apoio escolar** que o assistente da App 05 pode usar — o Admin
  cadastra o mesmo conteúdo pela App 03.

### 3.2 Fora do escopo

- **Cadastro de Mestre e de qualquer outra persona além do responsável** — segue exclusivo de
  Admin, na App 03.
- **Condução da partida do Quiz ao Vivo** — acontece na App 03, com o banco cadastrado aqui.
- **Aprovação final do desafio extra** — é ato privativo de Admin (PRD-02).
- **Criação de Comunidade Virtual e cadastro de locais** — são de Admin (PRD-08 e PRD-02).
- **Telas do Guerreiro(a)**: percorrer a trilha, responder ao quiz e registrar coleta são da
  App 05 (PRD-05).
- **Regras de pontuação, cadência e valoração**: normatizadas nos documentos 11, 02 e 04 e
  detalhadas nos PRD-08 e PRD-07.
- **Notificação por e-mail**: no Ciclo 01 todo retorno acontece dentro da plataforma.
- **Trilhas de ciclo futuro** — Rima, Capoeira, Redes, PNED/BNCC e Soft Skills: o modelo as
  comporta, o Ciclo 01 não as inclui.
- **Curadoria pedagógica prévia**: não existe aprovação antes da publicação; o que existe é
  auditoria posterior do Admin.

## 4. Personas e permissões

| Persona      | O que faz nesta aplicação                                                               | O que não pode fazer                                                    |
| ------------ | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Mestre       | Cria e publica trilhas, cadastra perguntas, lança o que é seu, valida, absorve e propõe | Lançar atividade de outro Mestre; cadastrar persona além do responsável |
| Admin        | Audita trilhas publicadas por amostragem e despublica com motivo                        | Editar a trilha de um Mestre — despublicar não é reescrever             |
| Guerreiro(a) | Nada: não acessa esta aplicação                                                         | Entrar                                                                  |
| Visitante    | Nada: a aplicação é inteiramente autenticada                                            | Acessar qualquer tela                                                   |

O Mestre entra por login social, como todo adulto. O que ele vê é sempre recortado pelo que é
dele: as suas trilhas, as suas turmas, as suas necessidades e as solicitações dos Guerreiros e
Guerreiras que percorrem as suas trilhas.

## 5. Jornadas principais

### 5.1 Escrever e publicar uma trilha

1. O Mestre cria a trilha, vincula a um **poder** do catálogo do ciclo e declara a área do
   conhecimento. A trilha nasce em **rascunho**, visível só para ele.
2. Acrescenta **pontos de trilha** em sequência, cada um com o seu nível de dificuldade.
3. Em cada ponto, monta o conteúdo, a bibliografia de apoio e o **desafio de desbloqueio**.
4. Cria as **atividades daquele ponto**, declarando de cada uma a **modalidade** (individual ou
   em equipe) e o **formato** (presencial ou on-line) — uma desplugada e um Quiz ao Vivo são
   presenciais; um quiz entre encontros é on-line.
5. Cria ao menos um **desafio de coleta**, declarando o que se mede, com que cadência e por
   quanto tempo.
6. Define a **culminância**: o que a criação original precisa ser, se é individual ou de
   equipe, e o critério com que será validada.
7. **Pagina a trilha** pelas etapas do ciclo — abertura, desenvolvimento, marcos e fechamento —
   e declara **qual marco concede qual recompensa**: desbloqueio de ponto, conclusão de etapa,
   batalha ou culminância. Recompensa sem lastro registrado não vai ao ar com a trilha.
8. Manda publicar. A aplicação confere as duas travas: **sem desafio de coleta não publica** e
   **sem culminância com criação original não publica**, dizendo em linguagem simples o que
   falta.
9. Passando, a trilha vai ao ar **na hora, sem aprovação de ninguém**, declarando a licença
   **CC BY-SA** e o crédito do Mestre autor.
10. Depois, um Admin audita por amostragem. Encontrando problema, **despublica com motivo
    registrado**, e o Mestre vê o motivo e corrige — a trilha volta a rascunho, e o que a turma
    já percorreu não se perde.

### 5.2 Montar o conteúdo de um ponto de trilha

1. O Mestre escreve o conteúdo em texto formatado, com imagens, sem digitar código.
2. Se o material está em vídeo, ele **envia o arquivo** (até 200 MB) ou **cola o link** de um
   vídeo já hospedado fora.
3. Anexa arquivos de apoio — PDF, imagem ou áudio — de até 20 MB por ponto.
4. Caindo a rede no meio do envio, o upload **retoma de onde parou**; nada recomeça do zero.
5. Passando do limite, a aplicação recusa dizendo o tamanho do arquivo e o limite, sem jargão.
6. Vincula ao ponto o **título e o capítulo** do acervo que apoiam aquele conteúdo, e a
   aplicação mostra ao Guerreiro(a) se há exemplar disponível no ponto de apoio dele, creditando
   o Apoiador que forneceu o material.
7. Usando conteúdo de terceiros, registra a fonte e a autorização de uso.
8. O armazenamento consumido é lançado como recurso de _cloud_ no livro-razão.

### 5.3 Validar a criação original da culminância

1. Concluída a trilha, o Guerreiro(a) ou a equipe apresenta a **criação original**.
2. O Mestre autor confere contra o critério que ele mesmo declarou na culminância.
3. Validando, credita a **autoria** — individual ou de equipe, com o papel de cada integrante —
   e libera o **badge de autoria**.
4. A criação passa a integrar o portfólio do Guerreiro(a); **a exposição pública só acontece se
   o responsável tiver autorizado a divulgação**.
5. Recusando, registra o motivo, e a criação volta para ajuste sem perder a autoria.

### 5.4 Cadastrar o banco de perguntas do Quiz ao Vivo

1. O Mestre cadastra a pergunta em **múltipla escolha, com quatro alternativas** e uma correta.
2. Vincula a pergunta à trilha e ao ponto a que ela se refere.
3. **Não há tempo por pergunta**: o ritmo é de quem conduz a partida.
4. A aplicação recusa pergunta sem as quatro alternativas ou sem a correta declarada.
5. Na aula, o próprio Mestre — ou um Admin — abre a partida pela App 03 com esse banco.

### 5.5 Conduzir as minhas turmas

1. O Mestre abre **Minhas atividades** e vê apenas as suas turmas e as atividades que propôs,
   separadas pelo formato: as **presenciais** do encontro e as **on-line** entre encontros.
2. Lança a atividade realizada com data, participantes e equipes. Na atividade em equipe, lança
   a equipe inteira de uma vez, preservando o papel de cada integrante.
3. Atribui o resultado de cada um: **realizada**, **com mérito** ou **mérito extra por auxílio
   aos colegas**.
4. Registra a presença do seu encontro e ajusta o que o App 01 não capturou.
5. Alcançado um **marco** com recompensa declarada, a entrega aparece como pendência do
   Mestre e a baixa vai para o livro-razão quando ele confirma.
6. Havendo má conduta, lança a **pontuação negativa** com o motivo — efetivada na hora, sem
   revisão de Admin, porque quem estava na sala é quem viu o que aconteceu.
7. Lançamento não se edita: correção é **ajuste** que referencia o original, e tudo entra na
   trilha de auditoria com autor, papel, data e hora.

### 5.6 Validar o desafio extra de um Apoiador

1. O Apoiador propõe, na App 08, um desafio extra vinculado a uma trilha do Mestre.
2. O Mestre recebe a proposta e faz a **validação pedagógica**: aprova com parecer ou recusa
   com motivo.
3. Recusado, o desafio **não chega** à aprovação do Admin.
4. Validado, segue para o Admin, que aprova exigindo o lastro da recompensa registrado.

### 5.7 Cobrir uma necessidade de recurso e acompanhar o ressarcimento

1. A atividade agendada sem lastro publica a **necessidade**, que aparece para o Mestre da
   trilha em moedas da plataforma.
2. Da própria necessidade, o Mestre **assume o aporte por absorção** em um ato de confirmação.
3. O aporte nasce em nome dele, marcado como **ressarcível**, e a atividade é confirmada sem
   intervenção de Admin.
4. O Mestre acompanha a situação do que absorveu. Havendo receita destinada, ele envia a chave
   PIX **por e-mail ao Admin** — a plataforma não guarda dado bancário, apenas o comprovante da
   transferência.

### 5.8 Tratar as solicitações dos Guerreiros e Guerreiras e propor melhorias

1. **Solicitação de novo local** vinda da App 05, para uma trilha do Mestre, aparece com alerta
   enquanto está em aberto; ele aprova, criando o local, ou recusa com motivo.
2. Pela amostra de auditoria, ele confere registros de coleta das suas trilhas e **invalida com
   motivo** o que não se sustenta — o registro nasce válido, a auditoria é posterior.
3. O Mestre **registra propostas** de evolução da plataforma, na mesma fila única que recebe as
   sugestões das Apps 05, 07 e 08, e acompanha o status.
4. Cadastra o **responsável** que se apresentou pessoalmente no encontro, vincula os Guerreiros
   e Guerreiras já cadastrados com o grau de parentesco e, sem conta Google, cria a credencial
   provisória.

## 6. Requisitos funcionais

### 6.1 Autoria e publicação da trilha

| ID         | Requisito                                                                                      | Prioridade |
| ---------- | ---------------------------------------------------------------------------------------------- | ---------- |
| `RF-09-01` | Mestre cria trilha vinculada a um poder do catálogo, com nome, objetivo e área do conhecimento | essencial  |
| `RF-09-02` | Mestre ordena pontos de trilha em sequência, com nível de dificuldade declarado em cada ponto  | essencial  |
| `RF-09-03` | Mestre pagina a trilha pelas etapas do ciclo: abertura, desenvolvimento, marcos e fechamento   | essencial  |
| `RF-09-04` | Trilha em rascunho é visível apenas ao Mestre autor                                            | essencial  |
| `RF-09-05` | Mestre publica a própria trilha sem aprovação prévia de Admin ou de outro Mestre               | essencial  |
| `RF-09-06` | Aplicação recusa publicar trilha sem ao menos um desafio de coleta de dados reais              | essencial  |
| `RF-09-07` | Aplicação recusa publicar trilha sem culminância com criação original prevista                 | essencial  |
| `RF-09-08` | Recusa de publicação diz, em linguagem simples, exatamente o que falta                         | essencial  |
| `RF-09-09` | Publicação declara a licença CC BY-SA do conteúdo e credita o Mestre autor                     | essencial  |
| `RF-09-10` | Admin despublica trilha auditada com motivo registrado, e o Mestre autor vê o motivo           | essencial  |
| `RF-09-11` | Trilha despublicada volta a rascunho preservando o percurso já realizado pelos Guerreiros      | essencial  |
| `RF-09-12` | Nenhum campo de autoria exige escrever código, HTML ou configuração técnica                    | essencial  |
| `RF-09-13` | Mestre duplica trilha existente como ponto de partida de uma nova                              | desejável  |
| `RF-09-69` | Mestre cria as atividades do ponto de trilha, com modalidade e formato declarados em cada uma  | essencial  |
| `RF-09-70` | Aplicação recusa atividade de trilha sem ponto, sem modalidade ou sem formato                  | essencial  |
| `RF-09-71` | Mestre declara qual marco da trilha concede qual recompensa, e em que quantidade               | essencial  |
| `RF-09-72` | Aplicação recusa publicar trilha cujo marco prometa recompensa sem lastro registrado           | essencial  |

### 6.2 Conteúdo e bibliografia do ponto

| ID         | Requisito                                                                          | Prioridade |
| ---------- | ---------------------------------------------------------------------------------- | ---------- |
| `RF-09-14` | Mestre escreve o conteúdo do ponto em texto formatado, com imagens                 | essencial  |
| `RF-09-15` | Mestre inclui link para vídeo hospedado fora da plataforma                         | essencial  |
| `RF-09-16` | Mestre envia vídeo de até 200 MB por ponto de trilha, hospedado pela plataforma    | essencial  |
| `RF-09-17` | Mestre envia arquivo de apoio de até 20 MB por ponto — PDF, imagem ou áudio        | essencial  |
| `RF-09-18` | Aplicação recusa upload acima do limite informando tamanho e limite, sem jargão    | essencial  |
| `RF-09-19` | Upload é retomável e sobrevive à queda de rede sem recomeçar do zero               | essencial  |
| `RF-09-20` | Armazenamento consumido é lançado como recurso de _cloud_ no livro-razão           | essencial  |
| `RF-09-21` | Mestre vincula ao ponto o título e o capítulo do acervo que apoiam aquele conteúdo | essencial  |
| `RF-09-22` | Bibliografia indica se há exemplar disponível no ponto de apoio do Guerreiro(a)    | essencial  |
| `RF-09-23` | Bibliografia credita o Apoiador que forneceu o material                            | essencial  |
| `RF-09-24` | Conteúdo de terceiros é registrado com fonte e autorização de uso                  | essencial  |
| `RF-09-25` | Mestre pré-visualiza o ponto como o Guerreiro(a) o verá, antes de publicar         | desejável  |

### 6.3 Desafios, coleta e culminância

| ID         | Requisito                                                                                        | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------------ | ---------- |
| `RF-09-26` | Mestre cria o desafio de desbloqueio do ponto, na forma de quiz ou de desafio prático            | essencial  |
| `RF-09-27` | Mestre cria desafio de coleta declarando o que se mede, a cadência, a vigência e a granularidade | essencial  |
| `RF-09-28` | Desafio de coleta declara quantos registros pontuam por período de cadência                      | essencial  |
| `RF-09-29` | Mestre define a culminância: o que a criação original precisa ser e o critério de validação      | essencial  |
| `RF-09-30` | Culminância declara se a criação é individual ou de equipe                                       | essencial  |
| `RF-09-31` | Mestre valida a criação original entregue, creditando autoria e liberando o badge de autoria     | essencial  |
| `RF-09-32` | Criação de equipe registra o papel de cada integrante, com crédito individual preservado         | essencial  |
| `RF-09-33` | Criação validada só aparece no portfólio público se o responsável tiver autorizado a divulgação  | essencial  |
| `RF-09-34` | Mestre recusa a criação com motivo, devolvendo-a para ajuste sem perder a autoria                | essencial  |
| `RF-09-35` | Mestre audita por amostragem os registros de coleta das suas trilhas e invalida com motivo       | essencial  |

### 6.4 Banco do Quiz ao Vivo

| ID         | Requisito                                                                                | Prioridade |
| ---------- | ---------------------------------------------------------------------------------------- | ---------- |
| `RF-09-36` | Mestre cadastra pergunta de múltipla escolha com quatro alternativas e uma correta       | essencial  |
| `RF-09-37` | Aplicação recusa pergunta sem quatro alternativas ou sem a alternativa correta declarada | essencial  |
| `RF-09-38` | Pergunta não tem tempo próprio: o ritmo é de quem conduz a partida                       | essencial  |
| `RF-09-39` | Pergunta é vinculada à trilha e ao ponto de trilha a que se refere                       | essencial  |
| `RF-09-40` | Mestre filtra as suas perguntas por trilha e ponto ao montar o banco de uma aula         | essencial  |
| `RF-09-41` | Banco cadastrado fica disponível para a partida conduzida na App 03                      | essencial  |

### 6.5 Minhas turmas e lançamentos

| ID         | Requisito                                                                                 | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------- | ---------- |
| `RF-09-42` | Mestre vê apenas as suas turmas, as suas atividades e os Guerreiros e Guerreiras delas    | essencial  |
| `RF-09-43` | Mestre lança a atividade realizada que propôs, com data, participantes e equipes          | essencial  |
| `RF-09-44` | Mestre atribui o resultado: realizada, com mérito ou mérito extra por auxílio aos colegas | essencial  |
| `RF-09-45` | Mestre registra presença do seu encontro e ajusta o que o App 01 não capturou             | essencial  |
| `RF-09-46` | Mestre lança pontuação negativa da sua aula com motivo, efetivada sem revisão de Admin    | essencial  |
| `RF-09-47` | Lançamento não é editável; correção é ajuste que referencia o original                    | essencial  |
| `RF-09-48` | Toda escrita do Mestre entra na trilha de auditoria com autor, papel, data e hora         | essencial  |
| `RF-09-49` | Aplicação recusa lançamento de atividade que não é do Mestre autenticado                  | essencial  |
| `RF-09-50` | Aplicação leva o Mestre ao painel do dia da sua aula, operado na App 03                   | desejável  |
| `RF-09-73` | Minhas atividades separa as presenciais do encontro das on-line entre encontros           | essencial  |
| `RF-09-74` | Mestre lança a equipe inteira de uma vez, preservando o papel de cada integrante          | essencial  |
| `RF-09-75` | Marco alcançado com recompensa declarada vira pendência de entrega para o Mestre          | essencial  |
| `RF-09-76` | Mestre confirma a entrega da recompensa do marco, gerando a baixa no livro-razão          | essencial  |

### 6.6 Validações, filas e propostas

| ID         | Requisito                                                                                      | Prioridade |
| ---------- | ---------------------------------------------------------------------------------------------- | ---------- |
| `RF-09-51` | Mestre valida com parecer, ou recusa com motivo, o desafio extra proposto para a sua trilha    | essencial  |
| `RF-09-52` | Desafio extra recusado pelo Mestre não chega à fila de aprovação do Admin                      | essencial  |
| `RF-09-53` | Mestre aprova ou recusa solicitação de novo local dos Guerreiros e Guerreiras das suas trilhas | essencial  |
| `RF-09-54` | Solicitações de local em aberto aparecem com alerta enquanto não são tratadas                  | essencial  |
| `RF-09-55` | Mestre registra proposta de evolução da plataforma e acompanha o status na fila única          | essencial  |
| `RF-09-77` | Mestre cadastra disciplinas do apoio escolar, com nome, faixa de dificuldade e situação        | essencial  |
| `RF-09-78` | Mestre cadastra o conteúdo de cada disciplina, que é o único insumo do assistente da App 05    | essencial  |

### 6.7 Recursos, absorção e ressarcimento

| ID         | Requisito                                                                                          | Prioridade |
| ---------- | -------------------------------------------------------------------------------------------------- | ---------- |
| `RF-09-56` | Mestre vê as necessidades de recurso das suas atividades, expressas em moedas da plataforma        | essencial  |
| `RF-09-57` | Mestre assume a necessidade como aporte por absorção em um ato de confirmação                      | essencial  |
| `RF-09-58` | Aporte por absorção nasce em nome do Mestre, marcado como ressarcível                              | essencial  |
| `RF-09-59` | Mestre acompanha a situação do ressarcimento do que absorveu                                       | essencial  |
| `RF-09-60` | Aplicação não coleta nem exibe dado bancário; guarda apenas o comprovante da transferência         | essencial  |
| `RF-09-61` | Mestre registra empréstimo e devolução de exemplar do acervo permanente, com estado de conservação | essencial  |

### 6.8 Responsáveis, perfil público e avisos

| ID         | Requisito                                                                                       | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------------- | ---------- |
| `RF-09-62` | Mestre cadastra responsável apresentado no encontro e vincula Guerreiros e Guerreiras já ativos | essencial  |
| `RF-09-63` | Vínculo registra o grau de parentesco em texto livre                                            | essencial  |
| `RF-09-64` | Aplicação recusa o quarto vínculo de responsável para o mesmo Guerreiro(a)                      | essencial  |
| `RF-09-65` | Mestre cria credencial de usuário e senha provisória para responsável sem conta Google          | essencial  |
| `RF-09-66` | Mestre publica currículo, portfólio, redes sociais e artefatos comprobatórios da sua habilidade | essencial  |
| `RF-09-67` | Aplicação não cadastra Mestre nem cria acesso de Mestre                                         | essencial  |
| `RF-09-68` | Toda tela que coleta dado traz aviso discreto do que coleta, com acesso à área detalhada        | essencial  |

## 7. Regras de negócio

| ID         | Regra                                                                                            | Invariante (doc 99 §6) | Fonte         |
| ---------- | ------------------------------------------------------------------------------------------------ | ---------------------- | ------------- |
| `RN-09-01` | Trilha publicada vai ao ar sem aprovação prévia; a curadoria é auditoria posterior do Admin      | —                      | 03 §11        |
| `RN-09-02` | Trilha sem ao menos um desafio de coleta de dados reais não é publicável                         | 5                      | 02 §3, 03 §11 |
| `RN-09-03` | Trilha sem culminância com criação original não é publicável                                     | 5                      | 02 §4, 03 §11 |
| `RN-09-04` | A criação original é validada pelo Mestre autor e carrega a autoria por toda a vida do registro  | —                      | 02 §4, 11 §7  |
| `RN-09-05` | O conteúdo educacional publicado sai sob CC BY-SA, com crédito ao Mestre autor                   | —                      | 03 §1         |
| `RN-09-06` | Vídeo até 200 MB e arquivo até 20 MB por ponto de trilha                                         | —                      | 03 §11        |
| `RN-09-07` | O armazenamento consumido é recurso de _cloud_ registrado no livro-razão                         | 9                      | 04 §1         |
| `RN-09-08` | O Mestre lança apenas as atividades que propôs e as turmas em que atua                           | —                      | 03 §11        |
| `RN-09-09` | A pontuação negativa lançada pelo Mestre é efetivada sem revisão de outro Admin                  | —                      | 02 §4, 03 §11 |
| `RN-09-10` | Pontos de habilidade só vêm de atividade realizada proposta por Mestre                           | 8                      | 02 §4, 11 §5  |
| `RN-09-11` | O desafio extra exige validação do Mestre da trilha antes da aprovação do Admin                  | —                      | 04 §3         |
| `RN-09-12` | Atividade sem lastro não acontece; a falta vira necessidade publicada                            | 9                      | 04 §1         |
| `RN-09-13` | Aporte por absorção é ressarcível e não gera armazenamento de dado bancário                      | —                      | 04 §1         |
| `RN-09-14` | A aplicação não cadastra Mestre: o cadastro é exclusivo de Admin, com habilidade comprovada      | 3                      | 02 §1, 03 §11 |
| `RN-09-15` | O responsável é cadastrado depois de se apresentar pessoalmente; no máximo três por Guerreiro(a) | 3                      | 03 §9         |
| `RN-09-16` | O modelo de trilha é agnóstico de área do conhecimento e não pressupõe habilidade técnica de TI  | —                      | 03 §11, 11 §2 |
| `RN-09-17` | A dificuldade é gradual e acessível a toda a faixa de 6 a 16 anos, sem segmentação por idade     | 2                      | 02 §1         |
| `RN-09-18` | Nenhum conteúdo publicado exibe imagem real de Guerreiro(a)                                      | 12                     | 03 §12        |
| `RN-09-19` | Criação original só vai à vitrine com autorização do responsável                                 | 11                     | 03 §12        |
| `RN-09-20` | Catálogo de poderes do Ciclo 01: IA/Robótica e Poder do Território; os demais são ciclo futuro   | 13                     | 02 §2         |
| `RN-09-21` | Registro de coleta nasce válido; o Mestre audita por amostragem e pode invalidar com motivo      | 6                      | 02 §1, PRD-08 |
| `RN-09-22` | Toda trilha é paginada pelas etapas do ciclo, com a coleta aberta já na abertura                 | —                      | 11 §2.3       |
| `RN-09-23` | Nenhum retorno sai por e-mail no Ciclo 01, salvo a chave PIX do ressarcimento enviada ao Admin   | —                      | 03 §9, 04 §1  |
| `RN-09-24` | Toda atividade de trilha pertence a um ponto de trilha e declara modalidade e formato            | —                      | 11 §§2.1, 4   |
| `RN-09-25` | Atividade avulsa, fora de trilha, é cadastro da gestão na App 03, não da autoria do Mestre       | —                      | 11 §4, 03 §11 |
| `RN-09-26` | Recompensa é conquistada em marco da trilha, nunca comprada com saldo de pontos                  | —                      | 02 §8         |
| `RN-09-27` | Recompensa prometida em marco exige lastro registrado antes da publicação da trilha              | 9                      | 04 §1, 02 §8  |

## 8. Modelo de dados

As entidades de trilha já existem no PRD-01; as de coleta, no PRD-08; as de recurso, no
PRD-07. Este PRD **acrescenta quatro entidades** ao núcleo — `Conteudo`, `BibliografiaDoPonto`,
`Culminancia` e `RecompensaDeMarco` — e detalha os atributos que a autoria exige. A `Atividade`
já existe no PRD-01 e passa a **pertencer obrigatoriamente a um ponto de trilha** quando é
atividade de trilha.

```text
AUTORIA (esta aplicação escreve)        CONSOME (definidos em outro PRD)
Trilha                                  DesafioDeColeta      (PRD-08)
PontoDeTrilha                           SerieDeColeta        (PRD-08)
Atividade                               RegistroDeColeta     (PRD-08)
Conteudo            [entidade nova]     Necessidade/Aporte   (PRD-07)
BibliografiaDoPonto [entidade nova]     ItemPatrimonial      (PRD-07)
Culminancia         [entidade nova]     DesafioExtra         (PRD-01)
RecompensaDeMarco   [entidade nova]     Responsavel          (PRD-01)
DesafioDeDesbloqueio                    SugestaoOuProposta   (PRD-01)
PerguntaDeQuiz                          Auditoria            (PRD-01)
CriacaoOriginal
Resultado / Presenca / Lancamento
```

| Entidade              | Atributos essenciais                                                                                                                                   |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Trilha`              | nome, poder, área do conhecimento, Mestre autor, objetivo, situação (rascunho, publicada, despublicada), versão, licença, paginação pelas etapas       |
| `PontoDeTrilha`       | trilha, ordem, título, nível de dificuldade, etapa do ciclo, desafio de desbloqueio                                                                    |
| `Atividade`           | ponto de trilha, título, descrição, **modalidade** (individual, equipe, equipe com familiar), **formato** (presencial ou on-line), natureza, recursos  |
| `RecompensaDeMarco`   | trilha, marco (ponto de trilha, etapa, batalha ou culminância), recompensa, quantidade, lastro confirmado, situação da entrega                         |
| `Conteudo`            | ponto de trilha, tipo (texto, imagem, link externo, vídeo, arquivo), corpo ou endereço, tamanho, autoria (própria ou de terceiro), fonte e autorização |
| `BibliografiaDoPonto` | ponto de trilha, título do acervo, capítulo recomendado, Apoiador creditado                                                                            |
| `Culminancia`         | trilha, descrição da criação original esperada, modalidade (individual ou equipe), critério de validação                                               |
| `CriacaoOriginal`     | Guerreiro(a) ou equipe com o papel de cada integrante, trilha, culminância, situação (entregue, validada, devolvida), Mestre validador, data e hora    |
| `PerguntaDeQuiz`      | Mestre curador, trilha, ponto de trilha, enunciado, quatro alternativas, alternativa correta, situação                                                 |

Imutabilidade e versionamento:

- `CriacaoOriginal` **nunca perde a autoria**: devolver para ajuste muda a situação, não o
  autor.
- Editar trilha publicada gera **nova versão**; o percurso já realizado permanece atrelado à
  versão que o Guerreiro(a) cursou.
- `Conteudo` de terceiro sem fonte registrada não é publicável.
- `RecompensaDeMarco` **não debita saldo do Guerreiro(a)**: a entrega é baixa de recurso no
  livro-razão, exatamente como a entrega do exemplar Alpha na abertura da trilha.
- `Atividade` sem ponto de trilha só existe como atividade avulsa da gestão (App 03).

## 9. Contratos de API

A aplicação segue as convenções do PRD-01 — prefixo `/v1`, token de sessão, erro em formato
único e filtro por comunidade e período. As rotas de coleta (`/desafios-de-coleta`,
`/auditoria/amostra`, `/registros/{id}/invalidacao`, `/solicitacoes-de-local/...`) são do
PRD-08 e as de recurso (`/necessidades/minhas`, `/aportes/absorcao`,
`/meus-aportes/ressarciveis`, `/itens-patrimoniais/...`) são do PRD-07 — não se repetem aqui.

| Método | Rota                                    | Autenticação | Descrição                                                      |
| ------ | --------------------------------------- | ------------ | -------------------------------------------------------------- |
| POST   | `/v1/trilhas`                           | Mestre       | Cria trilha em rascunho, vinculada a um poder                  |
| GET    | `/v1/trilhas/minhas`                    | Mestre       | Trilhas do próprio Mestre, com a situação de cada uma          |
| POST   | `/v1/trilhas/{id}/pontos`               | Mestre       | Acrescenta ponto de trilha, com ordem e dificuldade            |
| POST   | `/v1/pontos/{id}/conteudos`             | Mestre       | Cria conteúdo de texto, imagem ou link externo                 |
| POST   | `/v1/conteudos/{id}/arquivo`            | Mestre       | Envia vídeo ou arquivo, em upload retomável, dentro do limite  |
| POST   | `/v1/pontos/{id}/bibliografia`          | Mestre       | Vincula título e capítulo do acervo ao ponto                   |
| POST   | `/v1/pontos/{id}/atividades`            | Mestre       | Cria atividade do ponto, com modalidade e formato              |
| POST   | `/v1/pontos/{id}/desbloqueio`           | Mestre       | Define o quiz ou desafio que abre o ponto seguinte             |
| POST   | `/v1/trilhas/{id}/recompensas-de-marco` | Mestre       | Declara a recompensa de um marco, com quantidade e lastro      |
| POST   | `/v1/recompensas-de-marco/{id}/entrega` | Mestre       | Confirma a entrega e gera a baixa no livro-razão               |
| POST   | `/v1/trilhas/{id}/culminancia`          | Mestre       | Declara a criação original esperada e o critério de validação  |
| POST   | `/v1/trilhas/{id}/publicacao`           | Mestre       | Publica a trilha; recusa sem coleta ou sem culminância         |
| POST   | `/v1/trilhas/{id}/despublicacao`        | Admin        | Despublica trilha auditada, com motivo registrado              |
| GET    | `/v1/trilhas/{id}`                      | pública      | Trilha publicada, com licença e crédito do Mestre autor        |
| POST   | `/v1/perguntas`                         | Mestre       | Cadastra pergunta com quatro alternativas e uma correta        |
| GET    | `/v1/perguntas/minhas`                  | Mestre       | Banco do Mestre, filtrável por trilha e ponto                  |
| GET    | `/v1/minhas-turmas`                     | Mestre       | Turmas e atividades do próprio Mestre                          |
| POST   | `/v1/atividades/{id}/lancamentos`       | Mestre       | Lança a atividade que propôs, com participantes e resultados   |
| POST   | `/v1/aulas/{id}/presencas`              | Mestre       | Registra e ajusta presença do próprio encontro                 |
| POST   | `/v1/criacoes-originais/{id}/validacao` | Mestre       | Valida ou devolve a criação, creditando autoria e badge        |
| POST   | `/v1/desafios-extras/{id}/validacao`    | Mestre       | Validação pedagógica, com parecer ou motivo da recusa          |
| POST   | `/v1/responsaveis`                      | Mestre       | Cadastra responsável e vincula Guerreiros e Guerreiras         |
| POST   | `/v1/mestres/{id}/artefatos`            | Mestre       | Publica currículo, portfólio, redes e artefatos comprobatórios |
| POST   | `/v1/sugestoes`                         | Mestre       | Registra proposta de evolução na fila única da gestão          |

Erros previstos: atividade de trilha sem ponto, sem modalidade ou sem formato (422); publicação
de trilha cujo marco prometa recompensa sem lastro (422); publicação de trilha sem desafio de
coleta (422) ou sem culminância (422);
upload acima do limite de 200 MB para vídeo ou 20 MB para arquivo (413); conteúdo de terceiro
sem fonte registrada (422); pergunta sem quatro alternativas ou sem correta declarada (422);
lançamento de atividade que não é do Mestre autenticado (403); tentativa de editar lançamento
(405); despublicação pedida por Mestre (403); quarto vínculo de responsável para o mesmo
Guerreiro(a) (422); cadastro de Mestre por esta aplicação (403); publicação de criação original
sem autorização do responsável (409).

## 10. Requisitos não funcionais

- Web App responsivo **Mobile First**. O Mestre escreve trilha no computador, mas **lança
  resultado no celular, em pé, entre as bancadas** — as duas telas precisam servir.
- **Linguagem simples e zero jargão de TI**: nenhum campo pede código, HTML, _markup_ ou
  configuração técnica. É o requisito que sustenta o Mestre de humanas, artes ou esporte.
- **Upload tolerante a rede instável**: retomável, com progresso visível e sem recomeço do
  zero; a rede do ponto de apoio é a pior condição de projeto, não a exceção.
- **Rascunho salvo automaticamente**: perder texto de trilha por queda de rede é inaceitável.
- Desempenho em celular modesto, o mesmo do ponto de apoio.
- Escrita idempotente: reenviar o mesmo lançamento por falha de rede não duplica o registro.
- Acessibilidade digital e linguagem simples também no conteúdo entregue ao Guerreiro(a).
- Idioma pt-BR; código aberto; conteúdo educacional sob CC BY-SA.

## 11. LGPD e proteção da criança

| Dado coletado                      | Finalidade                       | Base legal        | Retenção                 | Quem acessa          |
| ---------------------------------- | -------------------------------- | ----------------- | ------------------------ | -------------------- |
| Artefatos comprobatórios do Mestre | Provar habilidade                | consentimento     | enquanto durar o vínculo | gestão e visitante   |
| Conteúdo autoral do Mestre         | Ensinar nas trilhas              | consentimento     | permanente, sob CC BY-SA | público              |
| Presença e resultado de atividade  | Registro da participação         | consentimento     | enquanto durar o vínculo | gestão e responsável |
| Pontuação negativa e motivo        | Aplicação do Código de Conduta   | interesse público | enquanto durar o vínculo | gestão e responsável |
| Criação original do Guerreiro(a)   | Autoria, portfólio e culminância | consentimento     | permanente, com autoria  | gestão e responsável |
| Contato do responsável             | Canal oficial com a família      | consentimento     | enquanto durar o vínculo | gestão               |

- **O Mestre não vê imagem real de Guerreiro(a)** em nenhuma tela: a identificação é por nick e
  avatar, e a conferência biométrica acontece no núcleo.
- **Nenhum conteúdo publicado pode exibir imagem real de criança.** A tela de envio avisa isso
  antes do upload, e o material com rosto de Guerreiro(a) é recusado pela curadoria.
- A **criação original** é do Guerreiro(a): fica guardada com autoria, mas **só vai à vitrine
  com autorização do responsável** — sem autorização, existe na plataforma e não em público.
- O registro de **pontuação negativa** é dado sensível de criança: restrito à gestão e ao
  responsável, nunca em rota pública, ranking ou vitrine.
- Pedido de acesso, correção ou exclusão chega pela App 07 e é tratado pela gestão; **o registro
  de coleta do território não é apagado**, e a resposta ao responsável diz isso.
- Toda tela que coleta dado traz o aviso discreto do que se coleta, com acesso à área detalhada
  sobre destino e uso.

## 12. Critérios de aceite e métricas

- Atividade de trilha criada sem ponto, sem modalidade ou sem formato é recusada; a mesma
  atividade, criada fora de trilha, é cadastro da gestão e não aparece na autoria do Mestre.
- Trilha cujo marco promete recompensa sem lastro registrado não publica.
- Marco alcançado por um Guerreiro(a) gera pendência de entrega para o Mestre, e a confirmação
  baixa o recurso no livro-razão — **sem debitar saldo de pontos de ninguém**.
- Trilha sem desafio de coleta não publica, e a mensagem diz o que falta sem jargão.
- Trilha sem culminância com criação original não publica, pela mesma regra.
- Trilha completa publicada pelo Mestre fica visível **na hora**, sem passar por nenhuma
  aprovação, com a licença CC BY-SA e o crédito do autor na página pública.
- Admin despublica com motivo; o Mestre vê o motivo, e o percurso já feito pela turma continua
  atrelado à versão cursada.
- Mestre que tenta despublicar recebe 403; Mestre que tenta lançar atividade de outro recebe 403.
- Vídeo de 250 MB é recusado com a mensagem do limite; vídeo de 180 MB sobe e, derrubada a rede
  no meio, **retoma de onde parou**.
- Conteúdo de terceiro sem fonte registrada não publica.
- Pergunta com três alternativas é recusada; pergunta com quatro e uma correta entra no banco e
  aparece na partida aberta na App 03.
- Pontuação negativa lançada pelo Mestre é efetivada na hora e aparece na auditoria com o nome
  dele.
- Tentativa de editar lançamento devolve 405, e a correção aparece como ajuste com o original
  preservado.
- Desafio extra recusado pelo Mestre não aparece na fila de aprovação do Admin.
- Necessidade das atividades do Mestre aparece em moedas, e a absorção confirma a atividade sem
  intervenção de Admin.
- Quarto vínculo de responsável ao mesmo Guerreiro(a) é recusado.
- Criação original validada de Guerreiro(a) sem autorização do responsável **não** aparece na
  vitrine, e continua creditada dentro da plataforma.
- Uma trilha de área não técnica — sem nenhum campo de tecnologia — é publicável do começo ao
  fim, com coleta e culminância.
- Nenhuma tela desta aplicação exibe imagem real de Guerreiro(a).

Hipóteses do Ciclo 01 (documento 10): este PRD **sustenta H1** — sem trilha publicada não há
trilha a iniciar, e é o número de Guerreiros e Guerreiras que iniciam uma trilha que mede a
hipótese. Contribui para **H3**, porque a absorção do Mestre é uma das fontes de lastro, e
para **H4**, porque a dificuldade gradual por ponto é o que permite a mesma trilha atender dos
6 aos 16 anos.

## 13. Decisões tomadas neste PRD

| Decisão                                                                             | Gravada em  | Linha do doc 09                     |
| ----------------------------------------------------------------------------------- | ----------- | ----------------------------------- |
| Trilha vai ao ar sem aprovação prévia; Admin audita por amostragem e despublica     | 03 §11      | Publicação e curadoria da trilha    |
| Publicação travada sem desafio de coleta e sem culminância com criação original     | 03 §11      | Trava de publicação da trilha       |
| Conteúdo do ponto: texto, imagem, link e upload de vídeo (200 MB) e arquivo (20 MB) | 03 §11      | Conteúdo do ponto de trilha         |
| Pergunta do Quiz ao Vivo em múltipla escolha, quatro alternativas, sem tempo        | 05 §5       | Formato da pergunta do Quiz ao Vivo |
| Conteúdo educacional publicado sob licença CC BY-SA                                 | 03 §1       | Licença do conteúdo educacional     |
| Atividade de trilha pertence a um ponto de trilha, com modalidade e formato         | 11 §§2.1, 4 | Atividade do ponto de trilha        |
| Recompensa conquistada em marco da trilha, nunca comprada com pontos                | 02 §8       | Recompensa conquistada em marco     |

As quatro entidades novas — `Conteudo`, `BibliografiaDoPonto`, `Culminancia` e
`RecompensaDeMarco` — foram acrescentadas ao modelo do PRD-01, e a `Atividade` passou a
pertencer a um ponto de trilha. Na App 03 (PRD-02), a auditoria das trilhas publicadas entrou
como ação de Admin e o cadastro de atividade ficou restrito à **atividade avulsa**.

## 14. Pendências que permanecem

- **Curadoria do conteúdo de apoio escolar** que o Mestre cadastra para o assistente da App 05:
  sem aprovação prévia na ferramenta, a conferência do corpus precisa de critério combinado.
- **Mapeamento dos livros nas trilhas**: qual capítulo apoia qual ponto das trilhas 1 e 2 é
  trabalho de leitura do acervo, não de ferramenta — mas sem ele a bibliografia nasce vazia.
- **Licença do código** da plataforma (AGPL, MIT ou outra): a do conteúdo já está decidida.
- **Formatos de arquivo aceitos no upload** e política de moderação do que é enviado: o limite
  de tamanho está decidido, a lista de extensões e a checagem de conteúdo impróprio não.
- **Revisão pedagógica das trilhas 1 e 2** antes da primeira turma: sem aprovação prévia na
  ferramenta, a conferência é combinada fora dela.
- **Quais recompensas em quais marcos**: a regra está decidida — recompensa se conquista em
  marco —, mas o catálogo do Ciclo 01 ainda não diz que marco entrega o quê. **Trava** o
  `RF-09-71` na prática, não no desenho.

## 15. Rastreabilidade

| Requisito               | Origem                                                           |
| ----------------------- | ---------------------------------------------------------------- |
| `RF-09-01` a `RF-09-13` | 11 §2 (anatomia da trilha) e 03 §11 (publicação e curadoria)     |
| `RF-09-14` a `RF-09-25` | 03 §11 (conteúdo e upload), 05 §3 e 11 §2.1 (bibliografia)       |
| `RF-09-26` a `RF-09-28` | 02 §§1, 3, PRD-08 (desafio de coleta e série temporal)           |
| `RF-09-29` a `RF-09-34` | 02 §4 e 11 §7 (criação original, autoria e badge)                |
| `RF-09-35`              | PRD-08 (auditoria por amostragem da coleta)                      |
| `RF-09-36` a `RF-09-41` | 05 §5 (Quiz ao Vivo) e PRD-02 (condução da partida)              |
| `RF-09-42` a `RF-09-50` | 03 §11 e 11 §§4, 5 (lançamentos e motor de pontuação)            |
| `RF-09-51` a `RF-09-52` | 04 §3 (desafios extras e validação pedagógica)                   |
| `RF-09-53` a `RF-09-55` | PRD-08 (solicitação de local) e 03 §§7, 9, 10, 11 (fila única)   |
| `RF-09-56` a `RF-09-61` | 04 §1 e PRD-07 (necessidades, absorção, ressarcimento e acervo)  |
| `RF-09-62` a `RF-09-65` | 03 §9 e PRD-01 (cadastro do responsável e credencial provisória) |
| `RF-09-66` a `RF-09-67` | 02 §1 e 03 §11 (prova de habilidade e governança de personas)    |
| `RF-09-68`              | 03 §12 (aviso visível de coleta e área detalhada)                |
| `RF-09-69` e `RF-09-70` | 11 §§2.1, 4 (atividade dentro do ponto de trilha)                |
| `RF-09-71` a `RF-09-76` | 02 §8 e 11 §2.1 (recompensa conquistada no marco)                |
| `RF-09-77` e `RF-09-78` | 03 §§7, 11 (disciplinas e conteúdo do apoio escolar)             |
