## Context

O painel agrega sete domínios que já existem — `aula-e-presenca`, `equipe`, `reserva-de-recurso`,
`livro-razao`, `resultado-de-atividade`, `consentimento` e `catalogo-de-tipos-de-recurso` — e não
inaugura nenhum. A sondagem repete o padrão já consolidado na condução da partida
(`aplicacao-de-gestao`), e o anexo repete o do comprovante de aporte (`aporte`). Motivação e
recorte: ver `proposal.md`.

O que esta fatia decide é onde a escolha da equipe mora, como o painel se mantém barato sendo
derivado, e como anexar a digitalização sem violar a imutabilidade do consentimento.

## Goals / Non-Goals

**Goals:**

- Uma leitura só para o encontro inteiro — o painel é aberto por hora, não por segundo, mas
  sonda a cada poucos segundos, e não pode custar uma consulta por bloco.
- A escolha da equipe gravada sem virar percurso, nem sobreviver à aula.
- O anexo gravado sem tocar no consentimento.

**Non-Goals:**

- Nenhuma escrita nova de gestão. O painel lista pendências; quem as resolve são as rotas que já
  existem.
- Nenhum canal de tempo real. A sondagem basta e é o padrão da casa.

## Decisions

**A escolha da equipe é coluna na equipe da aula, não entidade nova.** A equipe da aula já morre
com a aula; guardar nela a atividade corrente faz a escolha herdar esse tempo de vida sem
código de expurgo. Alternativa descartada: entidade `EscolhaDaEquipe` com histórico — cria
percurso, que é exatamente o que o documento 02 §5 proíbe para a equipe da aula.

**A escolha é substituída, nunca acumulada.** Uma coluna, sobrescrita a cada declaração. A
alternativa — gravar cada troca — daria ao núcleo um histórico de percurso pela porta dos fundos,
e ninguém pediu por ele.

**A digitalização é registro próprio, apontando para o consentimento.** `consentimento` é de
somente inserção e nenhuma rota pode editá-lo; anexar como coluna do consentimento violaria essa
regra. Um `AnexoDoTermo` que aponta para o consentimento satisfaz o `RF-02-68` e mantém o
registro intocado — é o mesmo movimento do lançamento de ajuste, que corrige sem apagar o
original. Alternativa descartada: coluna `digitalizacao` no consentimento — proibida pela spec
vigente.

**A digitalização entra na própria requisição, não em sessão retomável.** É documento
digitalizado, no mesmo teto do comprovante de aporte, e a sessão retomável da sexta fatia do
PRD-09 existe para vídeo e arquivo de apoio. Reusar a `PortaDeArmazenamento` pelo caminho simples.

**O painel é um módulo de leitura, sem modelo próprio.** `backend/src/nucleo/painel_do_dia/` só
consulta os repositórios dos domínios e compõe a resposta; nenhuma tabela, nenhuma migração.
Alternativa descartada: view materializada — otimização sem problema medido, e o painel serve
uma aula por vez.

**Quem aguarda aparelho sai da mesma consulta das presenças.** É a diferença entre os presentes
e os que integram alguma equipe daquela aula, resolvida em consulta, não em laço na aplicação.

**A App 09 leva ao painel por navegação, não por cópia.** O `RF-09-50` é um caminho para a App
03; a App 09 não reimplementa a tela. A App 03 tem endereço próprio (documento 03 §1), então o
caminho é para o endereço dela.

## Risks / Trade-offs

- **A sondagem multiplica a consulta agregada por operador com o painel aberto** → o painel serve
  uma aula, e o encontro tem poucos operadores; se o custo aparecer, o alvo é o intervalo da
  sondagem, não a forma da consulta. Nada a otimizar antes de medir.
- **A escolha da equipe é escrita nova na App 01, e o painel depende dela para o `RF-02-42`** →
  as duas entram nesta fatia, na ordem núcleo → App 01 → App 03, para que o campo do painel nasça
  cheio. Equipe que não declarou aparece sem missão, que é estado legítimo e não erro.
- **A escolha declarada pode envelhecer**: a equipe troca de atividade na mesa e esquece de
  declarar → o painel mostra a última declarada, e o Mestre circula de qualquer jeito. Adivinhar
  a atividade corrente por outro sinal seria supor, e o `RF-02-42` não pede isso.
- **A pendência de digitalização depende de o consentimento de biometria existir** → Guerreiro(a)
  cadastrado sem imagem (`RF-04-15`) não tem consentimento de biometria e não gera pendência.
  É o comportamento correto: não há termo assinado a digitalizar.
