# Design

## Context

A `RecompensaDeMarco`, a entrega e a fila do Mestre já estão implementadas na capacidade
`recompensa-de-marco`; marco alcançado já é o **desbloqueio da missão**, e prático não julgado
já é recusado como marco alcançado. O que falta é a metade "avisa" do `RF-05-45`.

Os componentes do percurso moram em `comum/trilha` desde a fatia 21 do PRD-04, e o
`GuiaDaTrilha` é o compositor dos quatro grupos da tela da missão desde a fatia 27. Ver
`proposal.md` — Why para a motivação.

Duas restrições moldam o desenho:

- O aparelho da App 01 é **compartilhado por equipe**, e a sessão de trabalho morre no fim do
  atendimento. Nada que precise sobreviver ao atendimento pode morar no navegador.
- Entre o "Já cumpri!" e o julgamento do Mestre pode haver **dias**, outro aparelho e outra
  aplicação. Não há push nem mensageria (invariante 1).

## Goals / Non-Goals

**Goals:**

- Uma mecânica só para os três caminhos que alcançam o marco, sem polling e sem rota de
  notificação.
- A ciência sobrevive ao aparelho, à aplicação e ao atendimento.
- O trio de estrelas entra sem quebrar o sistema de ícone nem o tema escuro.

**Non-Goals:**

- Notificar a criança fora da aplicação quando o Mestre julga. Sem mensageria, o aviso a
  alcança quando ela voltar à trilha.
- Mexer no `comum/react/Icone.tsx`, que fixa `fill="none"` e `stroke="currentColor"`.
- Consertar a falta de versão escura do `--cor-ponto-contorno`.

## Decisions

### 1. A ciência é tabela própria, por par (recompensa, Guerreiro(a))

A `RecompensaDeMarco` é **uma** para quantos alcancem o marco, então ciência não pode ser
coluna dela. Nasce tabela própria, com o par e o instante, no precedente da
`EntregaDeRecompensa` — que também é registro por Guerreiro(a) sobre uma recompensa só.

Não contraria o "a `RecompensaDeMarco` NEVER SHALL guardar situação de entrega própria" da
capacidade: ciência não é entrega, não move saldo e não emite lançamento.

- _Descartado:_ coluna `ciente` na `RecompensaDeMarco` — a ciência de um apagaria a dos demais.
- _Descartado:_ `sessionStorage`/`localStorage` no aparelho — morre no atendimento e não
  atravessa aparelho nem aplicação, que é exatamente o caso do desafio prático.

### 2. Uma leitura só decide a tela, e ela cobre o caso assíncrono de graça

A regra é **uma**: ao abrir ou atualizar a trilha, havendo recompensa conquistada **daquela
trilha** sem ciência, a tela entra. Não há caminho especial por tipo de desafio.

Isso cobre os três casos sem polling: a sondagem e o quiz porque a recarga do percurso já
acontece no mesmo ato do desbloqueio; o prático porque a criança reencontra a tela ao voltar à
trilha, depois do julgamento — em qualquer aparelho e em qualquer das duas aplicações, já que a
ciência é fato do núcleo.

- _Descartado:_ devolver a recompensa na resposta da submissão do desbloqueio — resolveria só o
  caso síncrono, e o prático precisaria de uma segunda mecânica.
- _Descartado:_ polling enquanto a tela está aberta — só funcionaria com a criança parada na
  tela, e gastaria rede no encontro inteiro.

### 3. A leitura é filtrada pela trilha aberta

`GET /v1/eu/recompensas` devolve as conquistadas de **todas** as trilhas. A tela filtra pela
trilha que está aberta: recompensa de outra trilha NEVER interrompe o percurso desta. Ela
continua alcançável pela lista de conquistas da App 05 e aparece quando a criança abrir a
trilha dela.

### 4. A tela ocupa o corpo do guia, e o `GuiaDaTrilha` a compõe

O `GuiaDaTrilha` já é o compositor dos quatro grupos, e já sabe quando o percurso mudou — é ele
quem tem o estado para decidir. A tela da recompensa **substitui os quatro grupos**, preservando
o cabeçalho com o nome da trilha: o documento 15 §6 fixa **uma decisão por tela**, e a tela da
recompensa oferece exatamente uma, que é avançar. As atividades do encontro ficam a um toque.

- _Descartado:_ apresentar a recompensa dentro do grupo 1, acima da missão — ofereceria duas
  decisões na mesma tela e deixaria a missão seguinte visível antes do aviso, que é o que o
  recorte quer evitar.

### 5. Duas recompensas saem uma por tela, na ordem da posição da missão

Uma tela por recompensa, ordenadas pela posição da missão que é o marco, cada uma com o seu
avançar; o último leva à missão. Empilhar duas numa tela diluiria as duas conquistas.

### 6. O trio é componente próprio de `comum/react`, no precedente do badge

O `Icone` fixa `fill="none"`, `stroke="currentColor"` e `aria-hidden`, e o documento 15 §11.1 o
quer assim. A **silhueta de badge** — a outra peça preenchida que o documento declara — já
resolveu isso com componente próprio e SVG próprio (`BadgeDaFamilia`, `.cg-badge__forma`), e o
trio segue o mesmo caminho: componente próprio, SVG próprio, preenchimento e contorno por
classe em `comum/react/estilos.css`, lendo `--cor-ponto` e `--cor-ponto-contorno`.

Nenhum valor de cor entra no arquivo do glifo, e o trio é `aria-hidden` como todo ícone — o
texto ao lado é a via primeira (documento 15 §5).

- _Descartado:_ um glifo `estrela` no `Icone` com variante preenchida — espalharia a exceção por
  um componente que as oito aplicações usam para tudo.

### 7. O retorno de conquista é o que já existe

`RetornoDeConquista` já existe em `comum/react` e já tem `missao_desbloqueada` entre os quatro
fatos do documento 11 §8.5. O trio entra dentro dele, com esse fato: a animação corre uma vez na
chegada, e `prefers-reduced-motion` a suprime pelos tokens, sem que o fato deixe de ser legível.
Nenhum componente novo de animação.

### 8. Contrato da API

| Rota                                     | Papel                                              |
| ---------------------------------------- | -------------------------------------------------- |
| `POST /v1/eu/recompensas/{id}/ciencia`   | grava a ciência; só o próprio Guerreiro(a)         |
| `GET /v1/eu/recompensas`                 | passa a trazer `nome` e `unidade` do tipo, e `ciente` |

A gravação repetida **mantém** a ciência que havia e responde sem erro — o avançar pode chegar
duas vezes numa rede ruim, e 409 obrigaria a tela a tratar um caso que não é erro. A ciência de
recompensa cujo marco não foi alcançado responde **422**, reusando a mesma conferência de marco
alcançado da capacidade, que é a que já recusa o prático não julgado.

Sem rede a tela não abre e a ciência **não** é enfileirada: a fila local do aparelho é da
presença, e ciência guardada fora do núcleo arriscaria consumir o aviso sem a criança o ter
visto.

## Risks / Trade-offs

- **A tela nasce dormente** → nenhuma trilha tem recompensa declarada, porque o catálogo de qual
  marco entrega qual recompensa é pendência do PRD-05 §14. Os testes a exercitam com recompensa
  semeada; em produção ela acorda quando o fundador decidir o catálogo.
- **O contorno some no tema escuro** → o `--cor-ponto-contorno` não é redefinido no bloco
  escuro do `comum/tokens.css`. O preenchimento `ponto-500` se sustenta sozinho contra o fundo
  escuro, e o texto ao lado carrega o significado. Lacuna preexistente da família ponto inteira,
  registrada e não consertada aqui.
- **Uma leitura a mais por trilha aberta** → a tela busca as recompensas conquistadas ao abrir a
  trilha. É leitura do próprio Guerreiro(a), pequena e já existente; não há laço nem polling.
- **O aviso pode chegar tarde no prático** → se o Mestre julga depois do encontro, a criança só
  vê a tela quando voltar à trilha. É consequência de não haver mensageria (invariante 1), e o
  percurso segue dizendo que a missão aguarda o Mestre enquanto isso.

## Migration Plan

Uma migração Alembic cria a tabela da ciência, com índice pelo Guerreiro(a) e unicidade do par,
no molde dos índices da `EntregaDeRecompensa`. Nada é reescrito e nenhuma coluna existente muda:
a tabela nasce vazia, e recompensa já conquistada antes da migração entra como **sem ciência** —
o que apresenta a tela uma vez a quem já tinha conquistado, que é o comportamento desejado, já
que o aviso nunca aconteceu.

Rollback é a migração reversa: a tabela cai, e a tela volta a não existir junto com o código que
a monta.
