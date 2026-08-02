# PRD-07 — Economia de recursos e livro-razão

## 1. Identificação

| Campo            | Valor                                                |
| ---------------- | ---------------------------------------------------- |
| PRD              | PRD-07                                               |
| Aplicação        | — (domínio consumido pelas Apps 03, 05, 06, 08 e 09) |
| Onda             | 1                                                    |
| Situação         | em revisão                                           |
| Versão e data    | v1 — 2026-08-02                                      |
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
  cloud e serviços — com unidade e **valor de referência em moedas**.
- Tabela de referência versionada: o valor de um tipo muda no tempo sem reescrever o passado.
- Registro de aporte financeiro, material ou de serviço, com provedor, comprovante e
  homologação de Admin.
- **Aporte por absorção**: Mestre ou Admin que provê o recurso sem receber tem o aporte
  registrado em seu nome, marcado como **ressarcível** e com destaque público pelo ato.
- Receita destinada a **ressarcir recursos absorvidos**, com fila por antiguidade e pagamento
  por decisão de Admin.
- Dados de recebimento do Mestre ou Admin — chave PIX, banco e favorecido — para o eventual
  ressarcimento.
- Saldo por tipo de recurso e ponto de apoio, com **reserva no agendamento** e baixa na
  realização da atividade.
- Bloqueio do agendamento de atividade sem lastro.
- Poder Econômico do provedor, derivado da soma de moedas aportadas.
- Patrimônio permanente: exemplar tombado, responsável designado, estado de conservação,
  empréstimo de bancada e devolução.
- Baixa definitiva de recompensa entregue — livro da linha Alpha e camisa.
- Necessidade de reposição por perda ou dano, sem débito para o jogador ou a família.
- Lastro do desafio extra do Apoiador, exigido antes da publicação.
- Rotas públicas de prestação de contas, sempre em moedas.

### 3.2 Fora do escopo

- **Rateio da monetização dos dados**: não há monetização prevista até dez/2026, e o termo, a
  base legal e a periodicidade do pagamento seguem pendentes no documento 09. A regra dos
  50% / 50% continua vigente no documento 04 e será implementada quando houver receita real.
- **Relatório de efetividade ao Apoiador**: o ledger guarda os dados que o alimentam; o
  formato do relatório é do PRD-14.
- **Interface de gestão de recursos** — pertence ao PRD-02 (App 03).
- Contabilidade fiscal e prestação de contas formal da pessoa jurídica.

## 4. Personas e permissões

| Persona   | O que faz neste domínio                                                                                                  | O que não pode fazer                                             |
| --------- | ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Admin     | Cadastra tipos de recurso e valores de referência, registra e homologa aportes, designa responsável de ponto de apoio    | Alterar aporte já homologado; apagar lançamento                  |
| Mestre    | Aporta recurso, inclusive por absorção, cadastra seus dados de recebimento e registra empréstimo e devolução de exemplar | Homologar o próprio aporte; exigir ressarcimento                 |
| Apoiador  | Consulta seus aportes e seu Poder Econômico; provê o lastro dos desafios extras                                          | Editar o ledger; ver dado de contato de jogador                  |
| Jogador   | Vê o que recebeu como recompensa e o acervo em seu uso                                                                   | Ver valores em reais; assumir dívida por perda ou dano           |
| Visitante | Lê a prestação de contas pública, em moedas                                                                              | Ver valor em reais, comprovante ou dado de doador não publicável |

## 5. Jornadas principais

### 5.1 Admin registra um aporte

1. Admin seleciona o provedor — Apoiador, Mestre ou Admin — e o tipo de recurso.
2. Informa a quantidade e anexa o comprovante: nota, orçamento, termo de doação ou
   comprovante de PIX.
3. O sistema calcula o valor em **moedas** pela tabela de referência vigente na data.
4. Admin homologa. O aporte credita o saldo do tipo de recurso e o Poder Econômico do
   provedor.
5. Tipo de recurso ainda não catalogado: o Admin **cadastra o tipo e o valor na hora**, e o
   aporte segue no mesmo fluxo.

### 5.2 Mestre ou Admin absorve um recurso

1. Falta saldo do recurso necessário — não há hora-aula provida, não há lanche.
2. O Mestre (ou o Admin) provê ele mesmo: dá a aula sem receber, leva o lanche, cede o insumo.
3. O sistema registra um **aporte por absorção** em nome de quem proveu, valorado pela tabela.
4. O saldo é creditado e imediatamente reservado pela atividade — que passa a ter lastro.
5. O aporte entra no Poder Econômico de quem absorveu, nasce marcado como **ressarcível** e
   soma ao selo público de quem sustentou atividade sem recurso.

### 5.3 Agendamento com reserva de recurso

1. A gestão agenda uma atividade que declara os recursos que consome.
2. O sistema verifica o saldo de cada tipo no ponto de apoio.
3. Havendo saldo, **reserva** as quantidades; faltando, **o agendamento é recusado** e o que
   falta aparece como necessidade de recurso.
4. Realizada a atividade, a reserva vira **baixa**.
5. Atividade cancelada **libera** a reserva, devolvendo o saldo.

### 5.4 Empréstimo e devolução de exemplar do acervo

1. O exemplar permanente está tombado, com ponto de apoio e responsável designado.
2. O Mestre registra a retirada de bancada vinculada a um jogador e a um ponto de trilha.
3. A devolução é registrada com o estado de conservação.
4. Devolução pendente aparece no painel do dia (PRD-02).
5. Perda ou dano **não gera débito** ao jogador nem à família: gera **necessidade de
   reposição**, a ser aportada por um Apoiador.

### 5.5 Visitante lê a prestação de contas

1. O visitante abre a prestação de contas pública, sem login.
2. Vê o total movimentado e o aportado por provedor, **em moedas**.
3. Não vê valor em reais, comprovante nem qualquer documento anexado.

### 5.6 Ressarcimento de um aporte absorvido

1. Um Apoiador doa com destinação **ressarcir recursos absorvidos** — é o que cria o dinheiro
   para isso; não há fila permanente nem promessa de devolução sem essa receita.
2. O sistema lista os aportes ressarcíveis em aberto, **do mais antigo ao mais novo**.
3. Admin decide quais paga, dentro do que a receita destinada cobre.
4. Pago o ressarcimento, as **moedas revertem**: o Poder Econômico de quem absorveu volta ao
   que era antes daquele aporte.
5. O registro do ato e o **selo público permanecem** — o reconhecimento é por ter sustentado a
   atividade quando faltou recurso, não pelo valor.

## 6. Requisitos funcionais

| ID         | Requisito                                                                                         | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------------- | ---------- |
| `RF-07-01` | Admin cadastra tipo de recurso com unidade e valor de referência em moedas                        | essencial  |
| `RF-07-02` | Sistema versiona o valor de referência por data de vigência                                       | essencial  |
| `RF-07-03` | Admin cadastra tipo novo no ato do registro de um aporte, sem interromper o fluxo                 | essencial  |
| `RF-07-04` | Admin registra aporte com provedor, tipo, quantidade, comprovante e data                          | essencial  |
| `RF-07-05` | Sistema converte todo aporte em moedas pela tabela vigente na data do aporte                      | essencial  |
| `RF-07-06` | Sistema registra aporte por absorção em nome do Mestre ou Admin que proveu o recurso              | essencial  |
| `RF-07-07` | Sistema mantém saldo por tipo de recurso e ponto de apoio                                         | essencial  |
| `RF-07-08` | Agendamento de atividade reserva os recursos declarados e é recusado sem saldo                    | essencial  |
| `RF-07-09` | Realização da atividade converte a reserva em baixa; cancelamento libera a reserva                | essencial  |
| `RF-07-10` | Sistema calcula o Poder Econômico de cada provedor pela soma de moedas aportadas                  | essencial  |
| `RF-07-11` | Sistema registra exemplar tombado com ponto de apoio, responsável designado e conservação         | essencial  |
| `RF-07-12` | Mestre registra empréstimo de bancada e devolução, com estado de conservação                      | essencial  |
| `RF-07-13` | Sistema registra baixa definitiva de recompensa entregue, sem devolução                           | essencial  |
| `RF-07-14` | Perda ou dano gera necessidade de reposição, nunca débito ao jogador ou à família                 | essencial  |
| `RF-07-15` | Sistema exige lastro da recompensa do desafio extra antes da publicação                           | essencial  |
| `RF-07-16` | Rota pública devolve o movimentado por provedor, atividade e comunidade, em moedas                | essencial  |
| `RF-07-17` | Apoiador consulta seus aportes e seu Poder Econômico, sem edição                                  | essencial  |
| `RF-07-18` | Sistema expõe o que falta de recurso para as atividades previstas                                 | essencial  |
| `RF-07-19` | Lançamento é imutável; correção se faz por lançamento de ajuste, com motivo e autor               | essencial  |
| `RF-07-20` | Sistema registra a coproprietariedade do dado publicado, sem calcular ou pagar rateio             | desejável  |
| `RF-07-21` | Conferência de inventário por módulo, com resultado publicável na prestação de contas             | desejável  |
| `RF-07-22` | Aporte por absorção nasce marcado como ressarcível, com situação de ressarcimento                 | essencial  |
| `RF-07-23` | Mestre e Admin cadastram chave PIX, banco e nome do favorecido para eventual ressarcimento        | essencial  |
| `RF-07-24` | Sistema aceita doação com destinação a ressarcir recursos absorvidos                              | essencial  |
| `RF-07-25` | Sistema lista os aportes ressarcíveis em aberto por antiguidade, e o Admin decide o pagamento     | essencial  |
| `RF-07-26` | Ressarcimento pago reverte as moedas do aporte e mantém o registro do ato                         | essencial  |
| `RF-07-27` | Card e página pública do Mestre ou Admin exibem quantas vezes ele sustentou atividade sem recurso | essencial  |

## 7. Regras de negócio

| ID         | Regra                                                                                   | Invariante | Fonte   |
| ---------- | --------------------------------------------------------------------------------------- | ---------- | ------- |
| `RN-07-01` | Nenhuma atividade acontece sem lastro dos recursos que consome                          | 9          | 04 §1   |
| `RN-07-02` | Todo custo de toda ação é atribuído a um provedor                                       | —          | 04 §1   |
| `RN-07-03` | Aporte não financeiro é valorado pela tabela de referência da gestão                    | —          | 04 §1   |
| `RN-07-04` | A moeda vale R$ 100,00 e admite duas casas decimais                                     | 16         | 04 §1   |
| `RN-07-05` | Toda saída pública exibe moedas, nunca reais                                            | 16         | 04 §1   |
| `RN-07-06` | Recurso provido sem contrapartida financeira por Mestre ou Admin é aporte em nome dele  | —          | 04 §1   |
| `RN-07-07` | Aporte de patrimônio credita o Poder Econômico uma única vez, sem baixa por consumo     | —          | 04 §1   |
| `RN-07-08` | Livro da linha Alpha e camisa entregues ao jogador têm baixa definitiva                 | —          | 05 §3   |
| `RN-07-09` | Perda ou dano de material comum não gera dívida ao jogador nem à família                | 11         | 05 §3   |
| `RN-07-10` | Cada ponto de apoio tem responsável designado pelo acervo permanente e pelos kits       | —          | 05 §3   |
| `RN-07-11` | O exemplar permanente não sai do ponto de apoio; uso é de bancada, com registro         | —          | 05 §3   |
| `RN-07-12` | A recompensa do desafio extra precisa de lastro antes da publicação do desafio          | 9          | 04 §3   |
| `RN-07-13` | O Apoiador não recebe dado de contato nem identificação de jogador                      | 10         | 04 §3   |
| `RN-07-14` | Dados publicados são coproprietários da entidade e do jogador que os gerou              | 17         | 04 §2   |
| `RN-07-15` | Lançamento do livro-razão nunca é apagado nem editado                                   | —          | 04 §1   |
| `RN-07-16` | Quem homologa o aporte não pode ser o próprio provedor                                  | —          | 04 §1   |
| `RN-07-17` | Ressarcimento não é direito nem promessa: só ocorre havendo receita destinada a ele     | —          | 04 §1   |
| `RN-07-18` | Ressarcimento pago reverte as moedas; o registro do ato e o destaque público permanecem | —          | 04 §1   |
| `RN-07-19` | O selo público mostra o número de absorções, nunca o valor em reais                     | 16         | 11 §8.2 |

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

| Entidade                 | Atributos essenciais                                                                                                                                                                                                                   |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TipoDeRecurso`          | nome, natureza (consumível, durável, serviço, financeiro), unidade, exige comprovante                                                                                                                                                  |
| `ValorDeReferencia`      | tipo, valor em moedas, vigência inicial e final, admin responsável                                                                                                                                                                     |
| `Aporte`                 | provedor, tipo, quantidade, valor em moedas, valor de origem, forma (financeira, material, serviço, absorção), **ressarcível**, situação de ressarcimento (não se aplica, em aberto, ressarcido), comprovante, admin homologador, data |
| `Lancamento`             | natureza (crédito, débito, ajuste), tipo de recurso, quantidade, moedas, atividade, aporte, data, autor, motivo do ajuste                                                                                                              |
| `Reserva`                | atividade, tipo de recurso, quantidade, ponto de apoio, estado (reservada, consumida, liberada)                                                                                                                                        |
| `SaldoDeRecurso`         | tipo, ponto de apoio, quantidade disponível, quantidade reservada                                                                                                                                                                      |
| `ItemPatrimonial`        | aporte de origem, título, número de tombo, ponto de apoio, responsável designado, estado de conservação                                                                                                                                |
| `Emprestimo`             | item, jogador, ponto de trilha, saída, devolução, estado de conservação na devolução                                                                                                                                                   |
| `NecessidadeDeReposicao` | item ou tipo de recurso, quantidade, motivo, situação, aporte que a supriu                                                                                                                                                             |
| `Ressarcimento`          | aporte absorvido, valor em reais, receita destinada de origem, admin pagador, data, comprovante                                                                                                                                        |
| `DadosDeRecebimento`     | pessoa (Mestre ou Admin), chave PIX, banco, agência, conta, nome do favorecido, atualizado em                                                                                                                                          |

Imutabilidade: `Lancamento` é **somente inserção**. Erro se corrige por lançamento de **ajuste**,
que referencia o original e guarda motivo e autor. O saldo é sempre **derivado** dos lançamentos,
nunca um número editável.

Duas faces do valor: o `Aporte` guarda **moedas** e **valor de origem em reais**. Toda saída
pública lê apenas a primeira.

## 9. Contratos de API

| Método | Rota                                   | Autenticação    | Descrição                                             |
| ------ | -------------------------------------- | --------------- | ----------------------------------------------------- |
| GET    | `/prestacao-de-contas`                 | pública         | Movimentado total e por provedor, em moedas           |
| GET    | `/prestacao-de-contas/atividades`      | pública         | Consumo por atividade e por comunidade, em moedas     |
| GET    | `/provedores/{id}/poder-economico`     | pública         | Poder Econômico do provedor, em moedas                |
| GET    | `/necessidades`                        | pública         | O que falta de recurso para as atividades previstas   |
| POST   | `/tipos-de-recurso`                    | Admin           | Cadastra tipo e valor de referência                   |
| POST   | `/aportes`                             | Admin           | Registra e homologa aporte, com comprovante           |
| POST   | `/aportes/absorcao`                    | Mestre ou Admin | Registra aporte por absorção de quem proveu o recurso |
| POST   | `/atividades/{id}/reservas`            | gestão          | Reserva os recursos no agendamento                    |
| POST   | `/atividades/{id}/baixa`               | gestão          | Converte reservas em baixa na realização              |
| POST   | `/itens-patrimoniais/{id}/emprestimos` | Mestre          | Registra retirada de bancada                          |
| POST   | `/emprestimos/{id}/devolucao`          | Mestre          | Registra devolução e estado de conservação            |
| POST   | `/lancamentos/{id}/ajuste`             | Admin           | Lança ajuste referenciando o lançamento original      |
| GET    | `/meus-aportes`                        | Apoiador        | Aportes e Poder Econômico do próprio Apoiador         |

Erros previstos: agendamento sem saldo (422, com a lista do que falta); homologação pelo
próprio provedor (403); aporte de tipo inexistente (422, com a rota de cadastro do tipo);
tentativa de editar lançamento (405).

## 10. Requisitos não funcionais

- Consulta pública de prestação de contas responde sem autenticação e é cacheável.
- O cálculo de saldo é reprodutível: recontar os lançamentos devolve o mesmo número.
- Registro de aporte e de empréstimo em Web App responsivo Mobile First, no ponto de apoio.
- Painel do dia lê saldo e devoluções pendentes em tempo de encontro (PRD-02).
- Valor em reais nunca é servido por rota pública, nem em campo auxiliar da resposta.
- Código aberto, em pt-BR.

## 11. LGPD e proteção da criança

| Dado                      | Finalidade                | Base legal        | Retenção   | Quem acessa             |
| ------------------------- | ------------------------- | ----------------- | ---------- | ----------------------- |
| Identificação do provedor | Crédito público do aporte | consentimento     | permanente | público (nome e moedas) |
| Comprovante do aporte     | Auditoria do livro-razão  | obrigação legal   | permanente | gestão                  |
| Valor de origem em reais  | Conversão e auditoria     | obrigação legal   | permanente | gestão                  |
| Jogador que usou exemplar | Ficha de vida do acervo   | interesse público | permanente | gestão e o próprio      |

- Este domínio **não trata dado pessoal de criança** além do vínculo com o exemplar
  emprestado e com a recompensa recebida.
- O Apoiador nunca recebe dado de contato de jogador: o que ele vê é agregado e por avatar.
- Nenhuma dívida é atribuída a jogador ou família, o que impede o uso do ledger como
  instrumento de cobrança sobre quem o projeto quer proteger.

## 12. Critérios de aceite e métricas

- Aporte de tipo material registrado com quantidade 3 e valor de referência 0,50 resulta em
  1,50 moeda, e o Poder Econômico do provedor sobe exatamente isso.
- Alteração do valor de referência de um tipo **não** altera o valor em moedas de aportes já
  registrados.
- Agendamento de atividade que consome recurso sem saldo é recusado, e a resposta diz o que
  falta.
- Aporte por absorção registrado durante a atividade credita e reserva na mesma operação, e a
  atividade passa a ter lastro.
- Cancelamento de atividade devolve ao saldo exatamente a quantidade reservada.
- Exemplar emprestado e não devolvido aparece como pendência; registrado como perdido, gera
  necessidade de reposição e **nenhum** débito ao jogador.
- Aporte por absorção nasce com situação de ressarcimento **em aberto** e some da lista quando
  é pago.
- Ressarcimento pago devolve o Poder Econômico ao valor anterior ao aporte, e o selo público
  continua contando aquela absorção.
- Nenhuma rota pública devolve valor em reais nem dado bancário.

Métrica de ciclo: este PRD é o que torna a hipótese **H3** verificável — lastro registrado no
livro-razão contra recursos necessários às atividades previstas do Ciclo 01.

## 13. Decisões tomadas neste PRD

| Decisão                                                           | Gravada em | Doc 09       |
| ----------------------------------------------------------------- | ---------- | ------------ |
| Aporte não financeiro valorado por tabela de referência da gestão | 04 §1      | Já decididos |
| Tipo de aporte novo cadastrado na hora por um Admin               | 04 §1      | Já decididos |
| Moeda com duas casas decimais                                     | 04 §1      | Já decididos |
| Lastro por saldo de tipo de recurso, com reserva no agendamento   | 04 §1      | Já decididos |
| Aporte por absorção de Mestre ou Admin                            | 04 §1      | Já decididos |
| Responsável designado pelo acervo em cada ponto de apoio          | 05 §3      | Já decididos |
| Rateio da monetização sem implementação no Ciclo 01               | —          | Pendente     |

## 14. Pendências que permanecem

- **Termo, base legal e periodicidade do rateio da monetização** dos dados publicados. Não
  trava o Ciclo 01, porque não há monetização prevista até dez/2026.
- **Formato dos relatórios públicos de prestação de contas** por atividade, comunidade e
  provedor — o que exatamente se publica e com que agregação.
- **Formato do relatório de efetividade** entregue ao Apoiador: assunto do PRD-14, que lê
  este ledger.
- **Modelagem formal em dupla entrada**: segue como `[Proposta]` no documento 04. Os
  requisitos deste PRD não dependem dela.
- **Guarda dos dados bancários** de Mestres e Admins: criptografia, quem acessa, retenção e o
  que acontece quando a pessoa deixa o projeto. Trava a implementação do `RF-07-23`.
- **Valores da tabela de referência**: deixaram de ser pendência de documentação e passaram a
  ser cadastro da gestão, alimentado por Admin antes do primeiro aporte do ciclo.

## 15. Rastreabilidade

| Requisito               | Origem                                      |
| ----------------------- | ------------------------------------------- |
| `RF-07-01` a `RF-07-05` | 04 §1 (moeda e tabela de referência)        |
| `RF-07-06`              | 04 §1 (aporte por absorção)                 |
| `RF-07-07` a `RF-07-09` | 04 §1 (regra de lastro)                     |
| `RF-07-10`              | 04 §1 (Poder Econômico)                     |
| `RF-07-11` a `RF-07-14` | 05 §3 (acervo, guarda e reposição)          |
| `RF-07-15`              | 04 §3 (desafios extras)                     |
| `RF-07-16` a `RF-07-18` | 04 §1 (transparência) e 10 §3 (hipótese H3) |
| `RF-07-19`              | 04 §1 (livro-razão auditável)               |
| `RF-07-20`              | 04 §2 (titularidade dos dados publicados)   |
| `RF-07-21`              | 05 §3 (conferência de inventário)           |
| `RF-07-22` a `RF-07-26` | 04 §§1–2 (absorção e ressarcimento)         |
| `RF-07-27`              | 11 §8.2 (cards e páginas individuais)       |
