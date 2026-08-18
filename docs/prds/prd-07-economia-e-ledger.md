# PRD-07 — Economia de recursos e livro-razão

## 1. Identificação

| Campo            | Valor                                                |
| ---------------- | ---------------------------------------------------- |
| PRD              | PRD-07                                               |
| Aplicação        | — (domínio consumido pelas Apps 03, 05, 06, 08 e 09) |
| Onda             | 1                                                    |
| Situação         | aprovado                                             |
| Versão e data    | v8 — 2026-08-17                                      |
| Depende de       | PRD-08                                               |
| Documentos-fonte | 04 §§1–3, 05 §§2–3, 11 §5                            |

## 2. Contexto e objetivo

Nenhuma atividade da plataforma acontece sem recurso provido. Este PRD define o **livro-razão**
que registra o que entra, o que sai e o que sobra — e que, por isso, é o que autoriza ou barra
o agendamento de uma aula.

Ele responde a três perguntas que o projeto se comprometeu a responder em público: **quem
sustentou o quê**, em moedas da plataforma; **o que já foi consumido**; e **o que falta** para
a próxima atividade acontecer.

É também o instrumento que torna a hipótese **H3 do Ciclo 01** mensurável — se os recursos de
implantação do MVP serão supridos por Mestres e Apoiadores —, porque a verificação da hipótese
é literalmente a leitura deste livro: lastro registrado contra recursos necessários às
atividades previstas.

## 3. Escopo

### 3.1 Dentro do escopo

- Catálogo de tipos de recurso — hora-aula, lanche, recompensa, insumo, kit, livro, camisa,
  cloud, serviços e **produção executiva** — com unidade e **valor de referência em moedas**.
- **Produção executiva**: o tempo do fundador e dos Admins na **construção** e na **operação**
  da plataforma, registrado por absorção com a frente, o período apurado e as horas aportadas.
- Tabela de referência versionada: o valor de um tipo muda no tempo sem reescrever o passado.
- Registro de aporte financeiro, material ou de serviço, com provedor, comprovante e
  homologação de Admin.
- **Aporte por absorção**: Mestre ou Admin que provê o recurso sem receber tem o aporte
  registrado em seu nome, marcado como **ressarcível** e com destaque público pelo ato.
- Receita destinada a **ressarcir recursos absorvidos**, com fila por antiguidade e pagamento
  por decisão de Admin.
- Comprovante da transferência anexado ao ressarcimento — **sem armazenar dado bancário**.
- **Ponto de apoio** cadastrado pela gestão, ligado a uma comunidade: é onde o recurso fica
  guardado e onde a aula acontece.
- Saldo por tipo de recurso e ponto de apoio, com **reserva no agendamento da aula** e baixa
  na realização dela.
- Aula sem lastro fica **pendente de lastro**, e a falta é publicada como necessidade de
  recurso na vitrine (App 06), na área do Apoiador (App 08) e na área dos Mestres da trilha
  (App 09), de onde o aporte pode ser assumido.
- Poder Sustentador do provedor, derivado da soma de moedas aportadas.
- Patrimônio permanente: exemplar tombado, responsável designado e estado de conservação.
- Baixa definitiva de recompensa entregue — livro da linha Alpha e camisa.
- Conferência de inventário a cada módulo, com resultado publicável na prestação de contas.
- Lastro do desafio extra do Apoiador, exigido antes da publicação.
- Rotas públicas de prestação de contas, sempre em moedas.

### 3.2 Fora do escopo

- **Empréstimo de bancada e reposição solidária**: o documento 05 adia os dois para o ciclo
  seguinte. No Ciclo 01 o exemplar não sai do ponto de apoio, a perda é anotada na ficha de
  vida e entra na conferência de inventário. A vedação de cobrar da família **não** é adiada.
- **Entrega de dados a pesquisadores e gestores públicos**: é gratuita (documento 03 §12.3),
  não movimenta recurso e não gera lançamento no livro-razão. O pedido, a aprovação e o
  registro da entrega são da App 03 (PRD-02) e da vitrine (PRD-03).
- **Efetividade do apoio ao Apoiador**: o ledger guarda os dados que a alimentam; o painel que
  a mostra é do PRD-14.
- **Interface de gestão de recursos** — pertence ao PRD-02 (App 03).
- Contabilidade fiscal e prestação de contas formal da pessoa jurídica.

## 4. Personas e permissões

| Persona      | O que faz neste domínio                                                                                                                | O que não pode fazer                                             |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Admin        | Cadastra pontos de apoio, tipos de recurso e valores de referência, registra e homologa aportes, designa responsável de ponto de apoio | Alterar aporte já homologado; apagar lançamento                  |
| Mestre       | Aporta recurso, inclusive por absorção, acompanha a situação do ressarcimento e faz a conferência de inventário do acervo              | Homologar o próprio aporte; exigir ressarcimento                 |
| Apoiador     | Consulta seus aportes e seu Poder Sustentador; provê o lastro dos desafios extras                                                      | Editar o ledger; ver dado de contato de Guerreiro(a)             |
| Guerreiro(a) | Vê o que recebeu como recompensa e o acervo em seu uso                                                                                 | Ver valores em reais; assumir dívida por perda ou dano           |
| Visitante    | Lê a prestação de contas pública, em moedas                                                                                            | Ver valor em reais, comprovante ou dado de doador não publicável |

## 5. Jornadas principais

### 5.1 Admin registra um aporte

1. Admin seleciona o provedor — Apoiador, Mestre ou Admin — e o tipo de recurso.
2. Informa a quantidade e anexa o comprovante: nota, orçamento, termo de doação ou
   comprovante de PIX.
3. O sistema calcula o valor em **moedas** pela tabela de referência vigente na data.
4. Admin homologa. O aporte credita o saldo do tipo de recurso e o Poder Sustentador do
   provedor.
5. Tipo de recurso ainda não catalogado: o Admin **cadastra o tipo e o valor na hora**, e o
   aporte segue no mesmo fluxo.

### 5.2 Mestre ou Admin absorve um recurso

1. Falta saldo do recurso necessário — não há hora-aula provida, não há lanche. A falta está
   publicada como **necessidade**, e o Mestre da trilha a vê na App 09.
2. O Mestre (ou o Admin) provê ele mesmo: dá a aula sem receber, leva o lanche, cede o insumo,
   e **assume o aporte a partir da própria necessidade**, em um ato de confirmação.
3. O sistema registra um **aporte por absorção** em nome de quem proveu, valorado pela tabela.
4. O saldo é creditado e imediatamente reservado pela aula — que passa a ter lastro.
5. O aporte entra no Poder Sustentador de quem absorveu, nasce marcado como **ressarcível** e
   soma ao selo público de quem sustentou atividade sem recurso.

### 5.3 Agendamento da aula com reserva de recurso

1. A gestão agenda a aula, declarando o ponto de apoio e os recursos que ela consome.
2. O sistema verifica o saldo de cada tipo naquele ponto de apoio.
3. Havendo saldo, **reserva** as quantidades; faltando, a aula fica **pendente de lastro** e o
   que falta é publicado como necessidade de recurso — na vitrine, na área do Apoiador e na
   dos Mestres da trilha.
4. Suprida a necessidade, por aporte ou por absorção, a aula é confirmada e a reserva
   acontece.
5. Realizada a aula, a reserva vira **baixa**.
6. Aula cancelada **libera** a reserva, devolvendo o saldo.

### 5.4 Tombamento e ficha de vida do exemplar

1. O exemplar permanente é tombado, com ponto de apoio, responsável designado e estado de
   conservação.
2. A ficha de vida guarda quem cuidou daquele exemplar, e o Guerreiro(a) a lê na App 05.
3. A conferência de inventário, a cada módulo, apura o que está em cada ponto de apoio e em
   que estado, e o resultado é publicável na prestação de contas.
4. Perda ou dano **não gera débito** ao Guerreiro(a) nem à família: é anotado na ficha de vida
   e entra na conferência. A **reposição solidária** é do ciclo seguinte (documento 05).

### 5.5 Visitante lê a prestação de contas

1. O visitante abre a prestação de contas pública, sem login.
2. Vê o total movimentado e o aportado por provedor, **em moedas**.
3. Não vê valor em reais, comprovante nem qualquer documento anexado.

### 5.6 Ressarcimento de um aporte absorvido

1. Um Apoiador doa com destinação **ressarcir recursos absorvidos** — é o que cria o dinheiro
   para isso; não há fila permanente nem promessa de devolução sem essa receita.
2. O sistema lista os aportes ressarcíveis em aberto, **do mais antigo ao mais novo**.
3. Admin decide quais paga, dentro do que a receita destinada cobre, e comunica quem será
   ressarcido.
4. **Só nesta etapa e fora da plataforma**, a pessoa envia a chave PIX por **e-mail ao Admin**.
5. Admin faz a transferência e **anexa o comprovante** (PDF ou imagem) ao registro. Nenhuma
   chave, banco ou conta é gravada em campo da plataforma.
6. Pago o ressarcimento, as **moedas revertem**: o Poder Sustentador de quem absorveu volta ao
   que era antes daquele aporte.
7. O registro do ato e o **selo público permanecem** — o reconhecimento é por ter sustentado a
   atividade quando faltou recurso, não pelo valor.

## 6. Requisitos funcionais

| ID         | Requisito                                                                                                                        | Prioridade |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `RF-07-47` | Admin cadastra ponto de apoio, com nome e comunidade a que pertence                                                              | essencial  |
| `RF-07-49` | Admin designa ou troca o responsável pelo acervo do ponto de apoio, entre os adultos cadastrados                                 | essencial  |
| `RF-07-01` | Admin cadastra tipo de recurso com unidade e valor de referência em moedas                                                       | essencial  |
| `RF-07-02` | Sistema versiona o valor de referência por data de vigência                                                                      | essencial  |
| `RF-07-03` | Admin cadastra tipo novo no ato do registro de um aporte, sem interromper o fluxo                                                | essencial  |
| `RF-07-04` | Admin registra aporte com provedor, tipo, quantidade, comprovante e data                                                         | essencial  |
| `RF-07-29` | Aporte declarado no pré-cadastro entra pendente, com comprovante e sem creditar nada                                             | essencial  |
| `RF-07-30` | Homologação do aporte pendente converte o valor em moedas e credita o Poder Sustentador                                          | essencial  |
| `RF-07-05` | Sistema converte todo aporte em moedas pela tabela vigente na data do aporte                                                     | essencial  |
| `RF-07-06` | Sistema registra aporte por absorção em nome do Mestre ou Admin que proveu o recurso                                             | essencial  |
| `RF-07-07` | Sistema mantém saldo por tipo de recurso e ponto de apoio                                                                        | essencial  |
| `RF-07-08` | Agendamento da aula reserva os recursos declarados no seu ponto de apoio; sem saldo, ela fica pendente de lastro                 | essencial  |
| `RF-07-27` | Falta de lastro é publicada como necessidade na vitrine e nas áreas do Apoiador e do Mestre                                      | essencial  |
| `RF-07-28` | Mestre ou Admin assume o aporte por absorção a partir da necessidade publicada                                                   | essencial  |
| `RF-07-31` | Necessidade publicada aceita cobertura parcial: o aporte homologado abate o que falta e ela só sai da lista quando o saldo fecha | essencial  |
| `RF-07-09` | Realização da aula converte a reserva em baixa; cancelamento dela libera a reserva                                               | essencial  |
| `RF-07-10` | Sistema calcula o Poder Sustentador de cada provedor pela soma de moedas aportadas                                               | essencial  |
| `RF-07-11` | Sistema registra exemplar tombado com ponto de apoio, responsável designado e conservação                                        | essencial  |
| `RF-07-13` | Sistema registra baixa definitiva de recompensa entregue, sem devolução                                                          | essencial  |
| `RF-07-48` | Perda ou dano é anotado na ficha de vida do exemplar, nunca como débito ao Guerreiro(a) ou à família                             | essencial  |
| `RF-07-15` | Sistema exige lastro da recompensa do desafio extra antes da publicação                                                          | essencial  |
| `RF-07-16` | Rota pública devolve o movimentado por provedor, aula e comunidade, em moedas                                                    | essencial  |
| `RF-07-17` | Apoiador consulta seus aportes e seu Poder Sustentador, sem edição                                                               | essencial  |
| `RF-07-18` | Sistema expõe o que falta de recurso para as aulas já agendadas                                                                  | essencial  |
| `RF-07-19` | Lançamento é imutável; correção se faz por lançamento de ajuste, com motivo e autor                                              | essencial  |
| `RF-07-32` | Sistema aceita aporte com período apurado anterior à entrada do livro-razão no ar, com comprovante anexado                       | essencial  |
| `RF-07-20` | Conferência de inventário por módulo, com resultado publicável na prestação de contas                                            | desejável  |
| `RF-07-21` | Aporte por absorção nasce marcado como ressarcível, com situação de ressarcimento                                                | essencial  |
| `RF-07-22` | Ressarcimento pago exige comprovante anexado, e a plataforma não guarda dado bancário                                            | essencial  |
| `RF-07-23` | Sistema aceita doação com destinação a ressarcir recursos absorvidos                                                             | essencial  |
| `RF-07-24` | Sistema lista os aportes ressarcíveis em aberto por antiguidade, e o Admin decide o pagamento                                    | essencial  |
| `RF-07-25` | Ressarcimento pago reverte as moedas do aporte e mantém o registro do ato                                                        | essencial  |
| `RF-07-26` | Card e página pública do Mestre ou Admin exibem quantas vezes ele sustentou atividade sem recurso                                | essencial  |
| `RF-07-33` | Sistema mantém o item do catálogo avulso com tipo de recurso, preço em pontos extras, estoque e comunidade                       | essencial  |
| `RF-07-34` | Item do catálogo avulso só fica ativo com lastro registrado no saldo do seu tipo de recurso                                      | essencial  |
| `RF-07-35` | Troca registra item, Guerreiro(a), preço cobrado, encontro e Mestre que entregou                                                 | essencial  |
| `RF-07-36` | Entrega da troca gera baixa no livro-razão e decrementa o estoque do item                                                        | essencial  |
| `RF-07-37` | Sistema recusa troca de item sem estoque ou sem lastro                                                                           | essencial  |
| `RF-07-38` | Preço em pontos extras vem da tabela de referência vigente, sem derivação do valor em moedas do tipo de recurso                  | essencial  |
| `RF-07-42` | Admin cadastra o preço de referência em pontos extras por tipo de recurso                                                        | essencial  |
| `RF-07-43` | Sistema versiona o preço de referência por data de vigência, como o valor em moedas                                              | essencial  |
| `RF-07-44` | Sistema recusa preço de referência menor que 20 pontos extras                                                                    | essencial  |
| `RF-07-45` | Item do catálogo herda o preço da tabela vigente; o cadastro do item não aceita preço próprio                                    | essencial  |
| `RF-07-46` | Troca cobra o preço vigente na data da troca e o registra no histórico                                                           | essencial  |
| `RF-07-39` | Publicação de desafio extra reserva a recompensa; sem saldo, a publicação é recusada                                             | essencial  |
| `RF-07-40` | Desafio extra encerrado sem conclusão libera a reserva, devolvendo o saldo                                                       | essencial  |
| `RF-07-41` | Sistema aceita custeio do desafio extra por absorção do proponente ou por saldo de recurso existente                             | essencial  |

## 7. Regras de negócio

| ID         | Regra                                                                                                                                | Invariante | Fonte        |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------- | ------------ |
| `RN-07-01` | Nenhuma atividade acontece sem lastro dos recursos que consome                                                                       | 9          | 04 §1        |
| `RN-07-02` | Todo custo de toda ação é atribuído a um provedor                                                                                    | —          | 04 §1        |
| `RN-07-03` | Aporte não financeiro é valorado pela tabela de referência da gestão                                                                 | —          | 04 §1        |
| `RN-07-04` | A moeda vale R$ 10,00, admite duas casas decimais e a escala é fixa por ciclo                                                        | 16         | 04 §1        |
| `RN-07-05` | Toda saída pública exibe moedas, nunca reais                                                                                         | 16         | 04 §1        |
| `RN-07-06` | Recurso provido sem contrapartida financeira por Mestre ou Admin é aporte em nome dele                                               | —          | 04 §1        |
| `RN-07-07` | Aporte de patrimônio credita o Poder Sustentador uma única vez, sem baixa por consumo                                                | —          | 04 §1        |
| `RN-07-08` | Livro da linha Alpha e camisa entregues ao Guerreiro(a) têm baixa definitiva                                                         | —          | 05 §3        |
| `RN-07-09` | Perda ou dano de material comum não gera dívida ao Guerreiro(a) nem à família                                                        | —          | 05 §3        |
| `RN-07-10` | Cada ponto de apoio tem responsável designado pelo acervo permanente e pelos kits                                                    | —          | 05 §3        |
| `RN-07-11` | O exemplar permanente não sai do ponto de apoio; a retirada registrada é do ciclo seguinte                                           | —          | 05 §3        |
| `RN-07-33` | O ponto de apoio pertence a uma comunidade e é onde o recurso fica guardado e a aula acontece                                        | —          | 05 §2        |
| `RN-07-34` | O responsável pelo acervo é designado depois do cadastro e é Admin, Mestre ou Apoiador — nunca Guerreiro(a) nem responsável familiar | —          | 05 §3        |
| `RN-07-12` | A recompensa do desafio extra precisa de lastro antes da publicação do desafio                                                       | 9          | 04 §3        |
| `RN-07-13` | O Apoiador não recebe dado de contato nem identificação de Guerreiro(a)                                                              | 10         | 04 §3        |
| `RN-07-14` | Camisa é conquistada no marco de missão declarado pelo Mestre, não entregue a todo inscrito                                          | —          | 02 §8, 05 §3 |
| `RN-07-15` | Lançamento do livro-razão nunca é apagado nem editado                                                                                | —          | 04 §1        |
| `RN-07-16` | Quem homologa o aporte não pode ser o próprio provedor                                                                               | —          | 04 §1        |
| `RN-07-23` | Na cobertura parcial, cada provedor recebe as moedas do que aportou; ninguém recebe crédito pelo que outro deu                       | 16         | 04 §1        |
| `RN-07-17` | Ressarcimento não é direito nem promessa: só ocorre havendo receita destinada a ele                                                  | —          | 04 §1        |
| `RN-07-18` | Ressarcimento pago reverte as moedas; o registro do ato e o destaque público permanecem                                              | —          | 04 §1        |
| `RN-07-19` | O selo público mostra o número de absorções, nunca o valor em reais                                                                  | 16         | 11 §8.2      |
| `RN-07-20` | Chave PIX, banco e conta nunca são armazenados; o trâmite guarda apenas o comprovante                                                | —          | 04 §1        |
| `RN-07-21` | Aporte declarado no pré-cadastro não credita moeda alguma antes da homologação de Admin                                              | 16         | 04 §2        |
| `RN-07-22` | Comprovante é aceito em PDF, JPG ou PNG; não há confirmação automática de PIX                                                        | —          | 04 §2        |
| `RN-07-24` | Reais, moedas da plataforma e pontos extras não se convertem entre si                                                                | 23         | 02 §8.2      |
| `RN-07-25` | Preço do catálogo avulso é declarado em pontos extras e nunca deriva do valor em moedas                                              | 23         | 02 §8.2      |
| `RN-07-29` | Quem fixa o preço é a tabela de referência da gestão; nem o Mestre nem o Apoiador arbitram valor                                     | 23         | 02 §8.2      |
| `RN-07-30` | Nenhum item do catálogo avulso vale menos de 20 pontos extras                                                                        | 23         | 02 §8.2      |
| `RN-07-31` | A prestação de contas pública é painel vivo, sem fechamento periódico no Ciclo 01                                                    | —          | 04 §1        |
| `RN-07-32` | As horas da produção executiva são declaradas pelo Admin por período; commits são lastro, não fórmula                                | —          | 04 §1        |
| `RN-07-26` | Nenhum item entra no catálogo avulso sem lastro, como toda recompensa                                                                | 9          | 02 §8.2      |
| `RN-07-27` | A entrega da troca é imediata; não há reserva de item do catálogo entre encontros                                                    | —          | 02 §8.2      |
| `RN-07-28` | Pontos do desafio extra são no máximo 10, de qualquer proponente                                                                     | —          | 04 §3        |

## 8. Modelo de dados

```text
ComunidadeVirtual 1 ─ N PontoDeApoio      (PRD-01/PRD-08)
PontoDeApoio  1 ──── N Aula               (a Aula é do PRD-01)
TipoDeRecurso 1 ──── N ValorDeReferencia  (versionado por vigência)
TipoDeRecurso 1 ──── N Aporte
Provedor      1 ──── N Aporte             (Apoiador, Mestre ou Admin)
Aporte        1 ──── 1 Lancamento         (crédito)
Aula          1 ──── N Reserva ──── 1 Lancamento (débito, na realização)
TipoDeRecurso 1 ──── 1 SaldoDeRecurso     (por ponto de apoio)
TipoDeRecurso 1 ──── N PrecoDeReferencia  (versionado por vigência)
TipoDeRecurso 1 ──── N ItemDeCatalogoAvulso
ItemDeCatalogoAvulso 1 ── N Troca ──── 1 Lancamento (débito, na entrega)
Aporte        0..1 ─ 1 Ressarcimento      (só quando o aporte é por absorção)
Aporte        0..1 ─ N ItemPatrimonial    (quando o aporte é durável)
PontoDeApoio  1 ──── N ItemPatrimonial
```

| Entidade               | Atributos essenciais                                                                                                                                                                                                                                                                                                   |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PontoDeApoio`         | nome, comunidade, responsável designado pelo acervo — em designação posterior ao cadastro —, ativo                                                                                                                                                                                                                     |
| `TipoDeRecurso`        | nome, natureza (consumível, durável, serviço, financeiro), unidade, exige comprovante                                                                                                                                                                                                                                  |
| `ValorDeReferencia`    | tipo, valor em moedas, vigência inicial e final, admin responsável                                                                                                                                                                                                                                                     |
| `Aporte`               | provedor, tipo, quantidade, valor em moedas, valor de origem, forma (financeira, material, serviço, absorção), **origem do registro** (gestão, pré-cadastro ou App 08), solicitação de origem, **ressarcível**, situação de ressarcimento (não se aplica, em aberto, ressarcido), comprovante, admin homologador, data |
| `Lancamento`           | natureza (crédito, débito, ajuste), tipo de recurso, quantidade, moedas, aula, aporte, data, autor, motivo do ajuste                                                                                                                                                                                                   |
| `Reserva`              | aula **ou desafio extra**, tipo de recurso, quantidade, ponto de apoio, estado (reservada, consumida, liberada)                                                                                                                                                                                                        |
| `PrecoDeReferencia`    | tipo de recurso, **preço em pontos extras**, vigência inicial e final, admin responsável                                                                                                                                                                                                                               |
| `ItemDeCatalogoAvulso` | nome, tipo de recurso, estoque, comunidade, quem cadastrou (Mestre ou Apoiador), situação de homologação, ativo — o **preço vem da tabela de referência**, não do cadastro do item                                                                                                                                     |
| `Troca`                | item, Guerreiro(a), preço em pontos extras cobrado, encontro, Mestre que entregou, data                                                                                                                                                                                                                                |
| `SaldoDeRecurso`       | tipo, ponto de apoio, quantidade disponível, quantidade reservada                                                                                                                                                                                                                                                      |
| `ItemPatrimonial`      | aporte de origem, título, número de tombo, ponto de apoio, responsável designado, estado de conservação, ficha de vida — quem cuidou dele e as perdas e danos anotados                                                                                                                                                 |
| `Ressarcimento`        | aporte absorvido, valor em reais, receita destinada de origem, admin pagador, data, comprovante anexado (PDF ou imagem)                                                                                                                                                                                                |

Imutabilidade: `Lancamento` é **somente inserção**. Erro se corrige por lançamento de
**ajuste**, que referencia o original e guarda motivo e autor. O saldo é sempre **derivado**
dos lançamentos, nunca um número editável.

Duas faces do valor: o `Aporte` guarda **moedas** e **valor de origem em reais**. Toda saída
pública lê apenas a primeira.

O `PontoDeApoio` é a dimensão do saldo: o recurso fica onde é usado. A `Aula`, entidade do
PRD-01, passa a declarar **em qual ponto de apoio acontece** — é o que leva a reserva ao saldo
certo. Ele não se confunde com o `Local` do PRD-08, que é a hierarquia territorial da coleta.

**Três unidades que não se convertem entre si:** reais, moedas da plataforma e pontos extras.
O `ItemDeCatalogoAvulso` guarda o preço em **pontos extras**, que **não deriva** do valor em
moedas do seu tipo de recurso — o custo real segue no lançamento, invisível para a criança.

## 9. Contratos de API

| Método | Rota                                | Autenticação    | Descrição                                                            |
| ------ | ----------------------------------- | --------------- | -------------------------------------------------------------------- |
| GET    | `/prestacao-de-contas`              | pública         | Movimentado total e por provedor, em moedas                          |
| GET    | `/prestacao-de-contas/aulas`        | pública         | Consumo por aula e por comunidade, em moedas                         |
| GET    | `/provedores/{id}/poder-economico`  | pública         | Poder Sustentador do provedor, em moedas                             |
| GET    | `/necessidades`                     | pública         | O que falta de recurso para as aulas já agendadas                    |
| GET    | `/necessidades/minhas`              | Mestre          | Necessidades das aulas das trilhas do próprio Mestre                 |
| POST   | `/pontos-de-apoio`                  | Admin           | Cadastra ponto de apoio, com nome e comunidade                       |
| PUT    | `/pontos-de-apoio/{id}/responsavel` | Admin           | Designa ou troca o responsável pelo acervo                           |
| POST   | `/tipos-de-recurso`                 | Admin           | Cadastra tipo e valor de referência                                  |
| POST   | `/aportes`                          | Admin           | Registra e homologa aporte, com comprovante                          |
| POST   | `/aportes/absorcao`                 | Mestre ou Admin | Registra aporte por absorção de quem proveu o recurso                |
| GET    | `/aportes/ressarciveis`             | Admin           | Aportes absorvidos em aberto, do mais antigo ao mais novo            |
| POST   | `/aportes/{id}/ressarcimento`       | Admin           | Registra o ressarcimento com comprovante anexado e reverte as moedas |
| POST   | `/aulas/{id}/reservas`              | gestão          | Reserva os recursos no agendamento da aula                           |
| POST   | `/aulas/{id}/baixa`                 | gestão          | Converte reservas em baixa na realização da aula                     |
| POST   | `/lancamentos/{id}/ajuste`          | Admin           | Lança ajuste referenciando o lançamento original                     |
| GET    | `/meus-aportes`                     | Apoiador        | Aportes e Poder Sustentador do próprio Apoiador                      |
| GET    | `/meus-aportes/ressarciveis`        | Mestre ou Admin | Situação dos aportes que absorveu                                    |

Erros previstos: agendamento sem saldo (422, com a lista do que falta); homologação pelo
próprio provedor (403); aporte de tipo inexistente (422, com a rota de cadastro do tipo);
tentativa de editar lançamento (405); ressarcimento sem comprovante anexado (422).

## 10. Requisitos não funcionais

- Consulta pública de prestação de contas responde sem login de pessoa — a chave da aplicação
  segue exigida, como em toda rota (PRD-01) — e é cacheável.
- O cálculo de saldo é reprodutível: recontar os lançamentos devolve o mesmo número.
- Registro de aporte em Web App responsivo Mobile First, no ponto de apoio.
- Painel do dia lê o saldo do ponto de apoio em tempo de encontro (PRD-02).
- Valor em reais nunca é servido por rota pública, nem em campo auxiliar da resposta.
- Código aberto, em pt-BR.

## 11. LGPD e proteção da criança

| Dado                           | Finalidade                | Base legal        | Retenção   | Quem acessa             |
| ------------------------------ | ------------------------- | ----------------- | ---------- | ----------------------- |
| Identificação do provedor      | Crédito público do aporte | consentimento     | permanente | público (nome e moedas) |
| Comprovante do aporte          | Auditoria do livro-razão  | obrigação legal   | permanente | gestão                  |
| Valor de origem em reais       | Conversão e auditoria     | obrigação legal   | permanente | gestão                  |
| Guerreiro(a) que usou exemplar | Ficha de vida do acervo   | interesse público | permanente | gestão e o próprio      |
| Comprovante de ressarcimento   | Auditoria do pagamento    | obrigação legal   | permanente | gestão                  |

- **Nenhum dado bancário é armazenado em campo da plataforma.** A chave PIX chega ao Admin
  por e-mail, fora da plataforma, e não é transcrita para cá. O que fica é o comprovante da
  transferência — que, sendo imagem de documento bancário, é **anexo de acesso restrito à
  gestão**, nunca servido por rota pública.
- Este domínio **não trata dado pessoal de criança** além do vínculo com o exemplar que ele
  usou, na ficha de vida, e com a recompensa recebida.
- O Apoiador nunca recebe dado de contato de Guerreiro(a): o que ele vê é agregado e por
  avatar.
- Nenhuma dívida é atribuída a Guerreiro(a) ou família, o que impede o uso do ledger como
  instrumento de cobrança sobre quem o projeto quer proteger.

## 12. Critérios de aceite e métricas

- Aporte de tipo material registrado com quantidade 3 e valor de referência 0,50 resulta em
  1,50 moeda, e o Poder Sustentador do provedor sobe exatamente isso.
- Alteração do valor de referência de um tipo **não** altera o valor em moedas de aportes já
  registrados.
- Agendamento de aula que consome recurso sem saldo no seu ponto de apoio é recusado, e a
  resposta diz o que falta.
- Aporte por absorção registrado durante a aula credita e reserva na mesma operação, e a aula
  passa a ter lastro.
- Cancelamento de aula devolve ao saldo exatamente a quantidade reservada.
- Saldo aportado a um ponto de apoio não lastreia aula agendada em outro.
- Exemplar dado como perdido é anotado na ficha de vida, entra na conferência de inventário e
  gera **nenhum** débito ao Guerreiro(a).
- Aporte por absorção nasce com situação de ressarcimento **em aberto** e some da lista quando
  é pago.
- Ressarcimento pago devolve o Poder Sustentador ao valor anterior ao aporte, e o selo público
  continua contando aquela absorção.
- Registro de ressarcimento sem comprovante anexado é recusado; nenhum campo da API aceita
  chave PIX, banco ou conta.
- Nenhuma rota pública devolve valor em reais nem dado bancário.

Métrica de ciclo: este PRD é o que torna a hipótese **H3** verificável — lastro registrado no
livro-razão contra recursos necessários às atividades previstas do Ciclo 01.

## 13. Decisões tomadas neste PRD

| Decisão                                                                        | Gravada em     | Doc 09                                       |
| ------------------------------------------------------------------------------ | -------------- | -------------------------------------------- |
| Ponto de apoio como entidade da gestão, ligada a uma comunidade                | 05 §2          | Ponto de apoio como entidade da plataforma   |
| Saldo de recurso por tipo **e ponto de apoio**                                 | 04 §1          | Ponto de apoio como entidade da plataforma   |
| A aula é a atividade que declara recursos, reserva e dá baixa                  | 04 §1          | A atividade que reserva recurso é a aula     |
| A aula declara em qual ponto de apoio acontece — altera o PRD-01               | 05 §2          | A atividade que reserva recurso é a aula     |
| Empréstimo de bancada e reposição solidária ficam para o ciclo seguinte        | 05 §3 (já era) | Empréstimo de bancada e reposição solidária  |
| Aporte não financeiro valorado por tabela de referência da gestão              | 04 §1          | Já decididos                                 |
| Tipo de aporte novo cadastrado na hora por um Admin                            | 04 §1          | Já decididos                                 |
| Moeda com duas casas decimais                                                  | 04 §1          | Já decididos                                 |
| Lastro por saldo de tipo de recurso, com reserva no agendamento                | 04 §1          | Já decididos                                 |
| Aporte por absorção de Mestre ou Admin                                         | 04 §1          | Já decididos                                 |
| Responsável designado pelo acervo em cada ponto de apoio                       | 05 §3          | Já decididos                                 |
| Designação do responsável posterior ao cadastro, entre os adultos cadastrados  | 05 §3          | Ponto de apoio como entidade da plataforma   |
| Aporte por absorção marcado como ressarcível, com destaque público pelo ato    | 04 §1, 11 §8.2 | Já decididos                                 |
| Ressarcimento só com receita destinada, por antiguidade e decisão de Admin     | 04 §1          | Já decididos                                 |
| Ressarcimento reverte as moedas; o registro do ato permanece                   | 04 §1          | Já decididos                                 |
| Sem armazenar dado bancário: chave PIX por e-mail e apenas comprovante anexado | 04 §1, 03 §11  | Já decididos                                 |
| Produção executiva como tipo de recurso, aportada por absorção                 | 04 §1          | Já decididos                                 |
| Faturas anteriores ao livro-razão guardadas e lançadas retroativamente         | 04 §1          | Já decididos                                 |
| Catálogo avulso com lastro, estoque e baixa na entrega da troca                | 02 §8.2        | Troca de pontos extras por recompensa avulsa |
| Preço em pontos extras sem derivação do valor em moedas                        | 02 §8.2        | Troca de pontos extras por recompensa avulsa |
| Preço fixado por tabela de referência da gestão, versionada por vigência       | 02 §8.2        | Quem fixa o preço do catálogo avulso         |
| Piso de 20 pontos extras para qualquer item do catálogo avulso                 | 02 §8.2        | Quem fixa o preço do catálogo avulso         |
| Desafio extra reserva a recompensa na publicação e libera se encerrar sem uso  | 04 §3          | Desafio extra — proponente, teto e custeio   |
| Custeio do desafio extra por absorção ou por saldo já existente na plataforma  | 04 §3          | Desafio extra — proponente, teto e custeio   |
| Horas da produção executiva declaradas por período, com commits como lastro    | 04 §1          | Apuração da produção executiva               |
| Valor-hora único na tabela de referência, versionado por vigência              | 04 §1          | Apuração da produção executiva               |
| Prestação de contas pública em painel vivo, sem fechamento periódico           | 04 §1          | Formato da prestação de contas pública       |
| Dupla entrada fora do Ciclo 01; segue proposta no documento-fonte              | 04 §1          | Formato da prestação de contas pública       |

## 14. Pendências que permanecem

Uma. **Quem desativa um ponto de apoio, e o que acontece com aula já agendada e com saldo
ainda guardado ali**, segue no documento 09: o `ativo` de §8 existe sem operação que o mude
até a decisão vir. Das seis anteriores, duas viraram decisão, na tabela de §13, e quatro não
eram decisão de produto: os valores da tabela de referência e os preços do catálogo avulso são
cadastro da gestão — os preços ainda dependem do calendário do Ciclo 01 e seguem no documento
09 —, o relatório de efetividade já estava decidido como painel vivo no PRD-14, e a modelagem
em dupla entrada segue proposta no documento 04, fora do Ciclo 01.

**Qual prédio** hospeda o ponto de apoio do Ciclo 01 segue no documento 09, entre as
pendências do Case 01. Não trava este PRD: o cadastro é da gestão e a entidade opera com
qualquer número de pontos de apoio.

## 15. Rastreabilidade

| Requisito               | Origem                                           |
| ----------------------- | ------------------------------------------------ |
| `RF-07-47`              | 05 §2 (pontos de apoio) e 04 §1 (saldo)          |
| `RF-07-49`              | 05 §3 (responsável designado pelo acervo)        |
| `RF-07-01` a `RF-07-05` | 04 §1 (moeda e tabela de referência)             |
| `RF-07-06`              | 04 §1 (aporte por absorção)                      |
| `RF-07-07` a `RF-07-09` | 04 §1 (regra de lastro, com a aula reservando)   |
| `RF-07-10`              | 04 §1 (Poder Sustentador)                        |
| `RF-07-11` e `RF-07-13` | 05 §3 (tombamento e baixa definitiva)            |
| `RF-07-48`              | 05 §3 (perda anotada na ficha de vida)           |
| `RF-07-15`              | 04 §3 (desafios extras)                          |
| `RF-07-16` a `RF-07-18` | 04 §1 (transparência) e 10 §3 (hipótese H3)      |
| `RF-07-19`              | 04 §1 (livro-razão auditável)                    |
| `RF-07-20`              | 05 §3 (conferência de inventário)                |
| `RF-07-21` a `RF-07-25` | 04 §§1–2 (absorção, ressarcimento e comprovante) |
| `RF-07-26`              | 11 §8.2 (cards e páginas individuais)            |
| `RF-07-33` a `RF-07-38` | 02 §8.2 (catálogo avulso, lastro e entrega)      |
| `RF-07-42` a `RF-07-46` | 02 §8.2 (tabela de referência e piso de 20)      |
| `RF-07-39` a `RF-07-41` | 04 §3 (custeio e reserva do desafio extra)       |
| `RF-07-27` e `RF-07-28` | 04 §1 (necessidade publicada e absorção)         |
| `RF-07-32`              | 04 §1 (custos anteriores ao livro-razão)         |
| `RF-07-29` e `RF-07-30` | 04 §2 (pré-cadastro, comprovante e homologação)  |
| `RF-07-31`              | 04 §1 (cobertura parcial da necessidade)         |
| `RN-07-20`              | 04 §1 (sem armazenamento de dado bancário)       |
| `RN-07-33`              | 05 §2 (estrutura física — pontos de apoio)       |
| `RN-07-31` e `RN-07-32` | 04 §1 (painel vivo e horas declaradas)           |
