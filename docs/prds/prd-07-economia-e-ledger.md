# PRD-07 — Economia de recursos e livro-razão

## 1. Identificação

| Campo            | Valor                                                |
| ---------------- | ---------------------------------------------------- |
| PRD              | PRD-07                                               |
| Aplicação        | — (domínio consumido pelas Apps 03, 05, 06, 08 e 09) |
| Onda             | 1                                                    |
| Situação         | aprovado                                             |
| Versão e data    | v4 — 2026-08-06                                      |
| Depende de       | PRD-08                                               |
| Documentos-fonte | 04 §§1–3, 05 §3, 11 §5                               |

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
- Saldo por tipo de recurso e ponto de apoio, com **reserva no agendamento** e baixa na
  realização da atividade.
- Atividade sem lastro fica **pendente de lastro**, e a falta é publicada como necessidade de
  recurso na vitrine (App 06), na área do Apoiador (App 08) e na área dos Mestres da trilha
  (App 09), de onde o aporte pode ser assumido.
- Poder do Sustento do provedor, derivado da soma de moedas aportadas.
- Patrimônio permanente: exemplar tombado, responsável designado, estado de conservação,
  empréstimo de bancada e devolução.
- Baixa definitiva de recompensa entregue — livro da linha Alpha e camisa.
- Necessidade de reposição por perda ou dano, sem débito para o Guerreiro(a) ou a família.
- Lastro do desafio extra do Apoiador, exigido antes da publicação.
- Rotas públicas de prestação de contas, sempre em moedas.

### 3.2 Fora do escopo

- **Entrega de dados a pesquisadores e gestores públicos**: é gratuita (documento 03 §12.3),
  não movimenta recurso e não gera lançamento no livro-razão. O pedido, a aprovação e o
  registro da entrega são da App 03 (PRD-02) e da vitrine (PRD-03).
- **Efetividade do apoio ao Apoiador**: o ledger guarda os dados que a alimentam; o painel que
  a mostra é do PRD-14.
- **Interface de gestão de recursos** — pertence ao PRD-02 (App 03).
- Contabilidade fiscal e prestação de contas formal da pessoa jurídica.

## 4. Personas e permissões

| Persona      | O que faz neste domínio                                                                                                     | O que não pode fazer                                             |
| ------------ | --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Admin        | Cadastra tipos de recurso e valores de referência, registra e homologa aportes, designa responsável de ponto de apoio       | Alterar aporte já homologado; apagar lançamento                  |
| Mestre       | Aporta recurso, inclusive por absorção, acompanha a situação do ressarcimento e registra empréstimo e devolução de exemplar | Homologar o próprio aporte; exigir ressarcimento                 |
| Apoiador     | Consulta seus aportes e seu Poder do Sustento; provê o lastro dos desafios extras                                           | Editar o ledger; ver dado de contato de Guerreiro(a)             |
| Guerreiro(a) | Vê o que recebeu como recompensa e o acervo em seu uso                                                                      | Ver valores em reais; assumir dívida por perda ou dano           |
| Visitante    | Lê a prestação de contas pública, em moedas                                                                                 | Ver valor em reais, comprovante ou dado de doador não publicável |

## 5. Jornadas principais

### 5.1 Admin registra um aporte

1. Admin seleciona o provedor — Apoiador, Mestre ou Admin — e o tipo de recurso.
2. Informa a quantidade e anexa o comprovante: nota, orçamento, termo de doação ou
   comprovante de PIX.
3. O sistema calcula o valor em **moedas** pela tabela de referência vigente na data.
4. Admin homologa. O aporte credita o saldo do tipo de recurso e o Poder do Sustento do
   provedor.
5. Tipo de recurso ainda não catalogado: o Admin **cadastra o tipo e o valor na hora**, e o
   aporte segue no mesmo fluxo.

### 5.2 Mestre ou Admin absorve um recurso

1. Falta saldo do recurso necessário — não há hora-aula provida, não há lanche. A falta está
   publicada como **necessidade**, e o Mestre da trilha a vê na App 09.
2. O Mestre (ou o Admin) provê ele mesmo: dá a aula sem receber, leva o lanche, cede o insumo,
   e **assume o aporte a partir da própria necessidade**, em um ato de confirmação.
3. O sistema registra um **aporte por absorção** em nome de quem proveu, valorado pela tabela.
4. O saldo é creditado e imediatamente reservado pela atividade — que passa a ter lastro.
5. O aporte entra no Poder do Sustento de quem absorveu, nasce marcado como **ressarcível** e
   soma ao selo público de quem sustentou atividade sem recurso.

### 5.3 Agendamento com reserva de recurso

1. A gestão agenda uma atividade que declara os recursos que consome.
2. O sistema verifica o saldo de cada tipo no ponto de apoio.
3. Havendo saldo, **reserva** as quantidades; faltando, a atividade fica **pendente de
   lastro** e o que falta é publicado como necessidade de recurso — na vitrine, na área do
   Apoiador e na dos Mestres da trilha.
4. Suprida a necessidade, por aporte ou por absorção, a atividade é confirmada e a reserva
   acontece.
5. Realizada a atividade, a reserva vira **baixa**.
6. Atividade cancelada **libera** a reserva, devolvendo o saldo.

### 5.4 Empréstimo e devolução de exemplar do acervo

1. O exemplar permanente está tombado, com ponto de apoio e responsável designado.
2. O Mestre registra a retirada de bancada vinculada a um Guerreiro(a) e a uma missão.
3. A devolução é registrada com o estado de conservação.
4. Devolução pendente aparece no painel do dia (PRD-02).
5. Perda ou dano **não gera débito** ao Guerreiro(a) nem à família: gera **necessidade de
   reposição**, a ser aportada por um Apoiador.

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
6. Pago o ressarcimento, as **moedas revertem**: o Poder do Sustento de quem absorveu volta ao
   que era antes daquele aporte.
7. O registro do ato e o **selo público permanecem** — o reconhecimento é por ter sustentado a
   atividade quando faltou recurso, não pelo valor.

## 6. Requisitos funcionais

| ID         | Requisito                                                                                         | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------------- | ---------- |
| `RF-07-01` | Admin cadastra tipo de recurso com unidade e valor de referência em moedas                        | essencial  |
| `RF-07-02` | Sistema versiona o valor de referência por data de vigência                                       | essencial  |
| `RF-07-03` | Admin cadastra tipo novo no ato do registro de um aporte, sem interromper o fluxo                 | essencial  |
| `RF-07-04` | Admin registra aporte com provedor, tipo, quantidade, comprovante e data                          | essencial  |
| `RF-07-29` | Aporte declarado no pré-cadastro entra pendente, com comprovante e sem creditar nada              | essencial  |
| `RF-07-30` | Homologação do aporte pendente converte o valor em moedas e credita o Poder do Sustento           | essencial  |
| `RF-07-05` | Sistema converte todo aporte em moedas pela tabela vigente na data do aporte                      | essencial  |
| `RF-07-06` | Sistema registra aporte por absorção em nome do Mestre ou Admin que proveu o recurso              | essencial  |
| `RF-07-07` | Sistema mantém saldo por tipo de recurso e ponto de apoio                                         | essencial  |
| `RF-07-08` | Agendamento de atividade reserva os recursos declarados; sem saldo, fica pendente de lastro       | essencial  |
| `RF-07-27` | Falta de lastro é publicada como necessidade na vitrine e nas áreas do Apoiador e do Mestre       | essencial  |
| `RF-07-28` | Mestre ou Admin assume o aporte por absorção a partir da necessidade publicada                    | essencial  |
| `RF-07-09` | Realização da atividade converte a reserva em baixa; cancelamento libera a reserva                | essencial  |
| `RF-07-10` | Sistema calcula o Poder do Sustento de cada provedor pela soma de moedas aportadas                | essencial  |
| `RF-07-11` | Sistema registra exemplar tombado com ponto de apoio, responsável designado e conservação         | essencial  |
| `RF-07-12` | Mestre registra empréstimo de bancada e devolução, com estado de conservação                      | essencial  |
| `RF-07-13` | Sistema registra baixa definitiva de recompensa entregue, sem devolução                           | essencial  |
| `RF-07-14` | Perda ou dano gera necessidade de reposição, nunca débito ao Guerreiro(a) ou à família            | essencial  |
| `RF-07-15` | Sistema exige lastro da recompensa do desafio extra antes da publicação                           | essencial  |
| `RF-07-16` | Rota pública devolve o movimentado por provedor, atividade e comunidade, em moedas                | essencial  |
| `RF-07-17` | Apoiador consulta seus aportes e seu Poder do Sustento, sem edição                                | essencial  |
| `RF-07-18` | Sistema expõe o que falta de recurso para as atividades previstas                                 | essencial  |
| `RF-07-19` | Lançamento é imutável; correção se faz por lançamento de ajuste, com motivo e autor               | essencial  |
| `RF-07-20` | Conferência de inventário por módulo, com resultado publicável na prestação de contas             | desejável  |
| `RF-07-21` | Aporte por absorção nasce marcado como ressarcível, com situação de ressarcimento                 | essencial  |
| `RF-07-22` | Ressarcimento pago exige comprovante anexado, e a plataforma não guarda dado bancário             | essencial  |
| `RF-07-23` | Sistema aceita doação com destinação a ressarcir recursos absorvidos                              | essencial  |
| `RF-07-24` | Sistema lista os aportes ressarcíveis em aberto por antiguidade, e o Admin decide o pagamento     | essencial  |
| `RF-07-25` | Ressarcimento pago reverte as moedas do aporte e mantém o registro do ato                         | essencial  |
| `RF-07-26` | Card e página pública do Mestre ou Admin exibem quantas vezes ele sustentou atividade sem recurso | essencial  |

## 7. Regras de negócio

| ID         | Regra                                                                                       | Invariante | Fonte        |
| ---------- | ------------------------------------------------------------------------------------------- | ---------- | ------------ |
| `RN-07-01` | Nenhuma atividade acontece sem lastro dos recursos que consome                              | 9          | 04 §1        |
| `RN-07-02` | Todo custo de toda ação é atribuído a um provedor                                           | —          | 04 §1        |
| `RN-07-03` | Aporte não financeiro é valorado pela tabela de referência da gestão                        | —          | 04 §1        |
| `RN-07-04` | A moeda vale R$ 10,00, admite duas casas decimais e a escala é fixa por ciclo               | 16         | 04 §1        |
| `RN-07-05` | Toda saída pública exibe moedas, nunca reais                                                | 16         | 04 §1        |
| `RN-07-06` | Recurso provido sem contrapartida financeira por Mestre ou Admin é aporte em nome dele      | —          | 04 §1        |
| `RN-07-07` | Aporte de patrimônio credita o Poder do Sustento uma única vez, sem baixa por consumo       | —          | 04 §1        |
| `RN-07-08` | Livro da linha Alpha e camisa entregues ao Guerreiro(a) têm baixa definitiva                | —          | 05 §3        |
| `RN-07-09` | Perda ou dano de material comum não gera dívida ao Guerreiro(a) nem à família               | 11         | 05 §3        |
| `RN-07-10` | Cada ponto de apoio tem responsável designado pelo acervo permanente e pelos kits           | —          | 05 §3        |
| `RN-07-11` | O exemplar permanente não sai do ponto de apoio; uso é de bancada, com registro             | —          | 05 §3        |
| `RN-07-12` | A recompensa do desafio extra precisa de lastro antes da publicação do desafio              | 9          | 04 §3        |
| `RN-07-13` | O Apoiador não recebe dado de contato nem identificação de Guerreiro(a)                     | 10         | 04 §3        |
| `RN-07-14` | Camisa é conquistada no marco de missão declarado pelo Mestre, não entregue a todo inscrito | —          | 02 §8, 05 §3 |
| `RN-07-15` | Lançamento do livro-razão nunca é apagado nem editado                                       | —          | 04 §1        |
| `RN-07-16` | Quem homologa o aporte não pode ser o próprio provedor                                      | —          | 04 §1        |
| `RN-07-17` | Ressarcimento não é direito nem promessa: só ocorre havendo receita destinada a ele         | —          | 04 §1        |
| `RN-07-18` | Ressarcimento pago reverte as moedas; o registro do ato e o destaque público permanecem     | —          | 04 §1        |
| `RN-07-19` | O selo público mostra o número de absorções, nunca o valor em reais                         | 16         | 11 §8.2      |
| `RN-07-20` | Chave PIX, banco e conta nunca são armazenados; o trâmite guarda apenas o comprovante       | —          | 04 §1        |
| `RN-07-21` | Aporte declarado no pré-cadastro não credita moeda alguma antes da homologação de Admin     | 16         | 04 §2        |
| `RN-07-22` | Comprovante é aceito em PDF, JPG ou PNG; não há confirmação automática de PIX               | —          | 04 §2        |

## 8. Modelo de dados

```text
TipoDeRecurso 1 ──── N ValorDeReferencia  (versionado por vigência)
TipoDeRecurso 1 ──── N Aporte
Provedor      1 ──── N Aporte             (Apoiador, Mestre ou Admin)
Aporte        1 ──── 1 Lancamento         (crédito)
Atividade     1 ──── N Reserva ──── 1 Lancamento (débito, na realização)
TipoDeRecurso 1 ──── 1 SaldoDeRecurso     (por ponto de apoio)
Aporte        0..1 ─ 1 Ressarcimento      (só quando o aporte é por absorção)
Aporte        0..1 ─ N ItemPatrimonial    (quando o aporte é durável)
ItemPatrimonial 1 ── N Emprestimo
ItemPatrimonial 0..1 ─ 1 NecessidadeDeReposicao
```

| Entidade                 | Atributos essenciais                                                                                                                                                                                                                                                                                                   |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TipoDeRecurso`          | nome, natureza (consumível, durável, serviço, financeiro), unidade, exige comprovante                                                                                                                                                                                                                                  |
| `ValorDeReferencia`      | tipo, valor em moedas, vigência inicial e final, admin responsável                                                                                                                                                                                                                                                     |
| `Aporte`                 | provedor, tipo, quantidade, valor em moedas, valor de origem, forma (financeira, material, serviço, absorção), **origem do registro** (gestão, pré-cadastro ou App 08), solicitação de origem, **ressarcível**, situação de ressarcimento (não se aplica, em aberto, ressarcido), comprovante, admin homologador, data |
| `Lancamento`             | natureza (crédito, débito, ajuste), tipo de recurso, quantidade, moedas, atividade, aporte, data, autor, motivo do ajuste                                                                                                                                                                                              |
| `Reserva`                | atividade, tipo de recurso, quantidade, ponto de apoio, estado (reservada, consumida, liberada)                                                                                                                                                                                                                        |
| `SaldoDeRecurso`         | tipo, ponto de apoio, quantidade disponível, quantidade reservada                                                                                                                                                                                                                                                      |
| `ItemPatrimonial`        | aporte de origem, título, número de tombo, ponto de apoio, responsável designado, estado de conservação                                                                                                                                                                                                                |
| `Emprestimo`             | item, Guerreiro(a), missão, saída, devolução, estado de conservação na devolução                                                                                                                                                                                                                                       |
| `NecessidadeDeReposicao` | item ou tipo de recurso, quantidade, motivo, situação, aporte que a supriu                                                                                                                                                                                                                                             |
| `Ressarcimento`          | aporte absorvido, valor em reais, receita destinada de origem, admin pagador, data, comprovante anexado (PDF ou imagem)                                                                                                                                                                                                |

Imutabilidade: `Lancamento` é **somente inserção**. Erro se corrige por lançamento de
**ajuste**, que referencia o original e guarda motivo e autor. O saldo é sempre **derivado**
dos lançamentos, nunca um número editável.

Duas faces do valor: o `Aporte` guarda **moedas** e **valor de origem em reais**. Toda saída
pública lê apenas a primeira.

## 9. Contratos de API

| Método | Rota                                   | Autenticação    | Descrição                                                            |
| ------ | -------------------------------------- | --------------- | -------------------------------------------------------------------- |
| GET    | `/prestacao-de-contas`                 | pública         | Movimentado total e por provedor, em moedas                          |
| GET    | `/prestacao-de-contas/atividades`      | pública         | Consumo por atividade e por comunidade, em moedas                    |
| GET    | `/provedores/{id}/poder-economico`     | pública         | Poder do Sustento do provedor, em moedas                             |
| GET    | `/necessidades`                        | pública         | O que falta de recurso para as atividades previstas                  |
| GET    | `/necessidades/minhas`                 | Mestre          | Necessidades das atividades das trilhas do próprio Mestre            |
| POST   | `/tipos-de-recurso`                    | Admin           | Cadastra tipo e valor de referência                                  |
| POST   | `/aportes`                             | Admin           | Registra e homologa aporte, com comprovante                          |
| POST   | `/aportes/absorcao`                    | Mestre ou Admin | Registra aporte por absorção de quem proveu o recurso                |
| GET    | `/aportes/ressarciveis`                | Admin           | Aportes absorvidos em aberto, do mais antigo ao mais novo            |
| POST   | `/aportes/{id}/ressarcimento`          | Admin           | Registra o ressarcimento com comprovante anexado e reverte as moedas |
| POST   | `/atividades/{id}/reservas`            | gestão          | Reserva os recursos no agendamento                                   |
| POST   | `/atividades/{id}/baixa`               | gestão          | Converte reservas em baixa na realização                             |
| POST   | `/itens-patrimoniais/{id}/emprestimos` | Mestre          | Registra retirada de bancada                                         |
| POST   | `/emprestimos/{id}/devolucao`          | Mestre          | Registra devolução e estado de conservação                           |
| POST   | `/lancamentos/{id}/ajuste`             | Admin           | Lança ajuste referenciando o lançamento original                     |
| GET    | `/meus-aportes`                        | Apoiador        | Aportes e Poder do Sustento do próprio Apoiador                      |
| GET    | `/meus-aportes/ressarciveis`           | Mestre ou Admin | Situação dos aportes que absorveu                                    |

Erros previstos: agendamento sem saldo (422, com a lista do que falta); homologação pelo
próprio provedor (403); aporte de tipo inexistente (422, com a rota de cadastro do tipo);
tentativa de editar lançamento (405); ressarcimento sem comprovante anexado (422).

## 10. Requisitos não funcionais

- Consulta pública de prestação de contas responde sem autenticação e é cacheável.
- O cálculo de saldo é reprodutível: recontar os lançamentos devolve o mesmo número.
- Registro de aporte e de empréstimo em Web App responsivo Mobile First, no ponto de apoio.
- Painel do dia lê saldo e devoluções pendentes em tempo de encontro (PRD-02).
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
- Este domínio **não trata dado pessoal de criança** além do vínculo com o exemplar
  emprestado e com a recompensa recebida.
- O Apoiador nunca recebe dado de contato de Guerreiro(a): o que ele vê é agregado e por
  avatar.
- Nenhuma dívida é atribuída a Guerreiro(a) ou família, o que impede o uso do ledger como
  instrumento de cobrança sobre quem o projeto quer proteger.

## 12. Critérios de aceite e métricas

- Aporte de tipo material registrado com quantidade 3 e valor de referência 0,50 resulta em
  1,50 moeda, e o Poder do Sustento do provedor sobe exatamente isso.
- Alteração do valor de referência de um tipo **não** altera o valor em moedas de aportes já
  registrados.
- Agendamento de atividade que consome recurso sem saldo é recusado, e a resposta diz o que
  falta.
- Aporte por absorção registrado durante a atividade credita e reserva na mesma operação, e a
  atividade passa a ter lastro.
- Cancelamento de atividade devolve ao saldo exatamente a quantidade reservada.
- Exemplar emprestado e não devolvido aparece como pendência; registrado como perdido, gera
  necessidade de reposição e **nenhum** débito ao Guerreiro(a).
- Aporte por absorção nasce com situação de ressarcimento **em aberto** e some da lista quando
  é pago.
- Ressarcimento pago devolve o Poder do Sustento ao valor anterior ao aporte, e o selo público
  continua contando aquela absorção.
- Registro de ressarcimento sem comprovante anexado é recusado; nenhum campo da API aceita
  chave PIX, banco ou conta.
- Nenhuma rota pública devolve valor em reais nem dado bancário.

Métrica de ciclo: este PRD é o que torna a hipótese **H3** verificável — lastro registrado no
livro-razão contra recursos necessários às atividades previstas do Ciclo 01.

## 13. Decisões tomadas neste PRD

| Decisão                                                                        | Gravada em     | Doc 09       |
| ------------------------------------------------------------------------------ | -------------- | ------------ |
| Aporte não financeiro valorado por tabela de referência da gestão              | 04 §1          | Já decididos |
| Tipo de aporte novo cadastrado na hora por um Admin                            | 04 §1          | Já decididos |
| Moeda com duas casas decimais                                                  | 04 §1          | Já decididos |
| Lastro por saldo de tipo de recurso, com reserva no agendamento                | 04 §1          | Já decididos |
| Aporte por absorção de Mestre ou Admin                                         | 04 §1          | Já decididos |
| Responsável designado pelo acervo em cada ponto de apoio                       | 05 §3          | Já decididos |
| Aporte por absorção marcado como ressarcível, com destaque público pelo ato    | 04 §1, 11 §8.2 | Já decididos |
| Ressarcimento só com receita destinada, por antiguidade e decisão de Admin     | 04 §1          | Já decididos |
| Ressarcimento reverte as moedas; o registro do ato permanece                   | 04 §1          | Já decididos |
| Sem armazenar dado bancário: chave PIX por e-mail e apenas comprovante anexado | 04 §1, 03 §11  | Já decididos |
| Produção executiva como tipo de recurso, aportada por absorção                 | 04 §1          | Já decididos |

## 14. Pendências que permanecem

- **Valor-hora da produção executiva** e o critério que converte o histórico de commits e o
  registro do Admin em horas aportadas — cadastro da gestão, como os demais valores da tabela.
- **Formato dos relatórios públicos de prestação de contas** por atividade, comunidade e
  provedor — o que exatamente se publica e com que agregação.
- **Formato do relatório de efetividade** entregue ao Apoiador: assunto do PRD-14, que lê
  este ledger.
- **Modelagem formal em dupla entrada**: segue como `[Proposta]` no documento 04. Os
  requisitos deste PRD não dependem dela.
- **Valores da tabela de referência**: deixaram de ser pendência de documentação e passaram a
  ser cadastro da gestão, alimentado por Admin antes do primeiro aporte do ciclo.

## 15. Rastreabilidade

| Requisito               | Origem                                           |
| ----------------------- | ------------------------------------------------ |
| `RF-07-01` a `RF-07-05` | 04 §1 (moeda e tabela de referência)             |
| `RF-07-06`              | 04 §1 (aporte por absorção)                      |
| `RF-07-07` a `RF-07-09` | 04 §1 (regra de lastro)                          |
| `RF-07-10`              | 04 §1 (Poder do Sustento)                        |
| `RF-07-11` a `RF-07-14` | 05 §3 (acervo, guarda e reposição)               |
| `RF-07-15`              | 04 §3 (desafios extras)                          |
| `RF-07-16` a `RF-07-18` | 04 §1 (transparência) e 10 §3 (hipótese H3)      |
| `RF-07-19`              | 04 §1 (livro-razão auditável)                    |
| `RF-07-20`              | 05 §3 (conferência de inventário)                |
| `RF-07-21` a `RF-07-25` | 04 §§1–2 (absorção, ressarcimento e comprovante) |
| `RF-07-26`              | 11 §8.2 (cards e páginas individuais)            |
| `RF-07-27` e `RF-07-28` | 04 §1 (necessidade publicada e absorção)         |
| `RN-07-20`              | 04 §1 (sem armazenamento de dado bancário)       |
