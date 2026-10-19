# Proposal

Origem: **PRD-05 — Área do Guerreiro(a)**, **fatia 10** do
`openspec/cronograma-de-fatias.md`.

| Identificador | Papel nesta change                                                     |
| ------------- | ---------------------------------------------------------------------- |
| `RF-05-45`    | **quitado** — marco alcançado avisa a recompensa e que o Mestre entrega |
| `RF-05-46`    | alcançado — nenhum caminho de compra na tela                            |
| `RN-05-50`    | **novo** — a ciência da recompensa, por Guerreiro(a) e uma vez só       |
| `RF-05-13`, `RF-05-14`, `RF-05-72`, `RF-05-89`, `RN-05-45` | alcançados — os três atos que alcançam o marco |
| `RF-04-72`, `RF-04-73` | alcançados — o mesmo percurso no aparelho do encontro         |

## Why

O `RF-05-45` é **essencial e nunca foi implementado**. Ele exige que o marco alcançado avise
o que foi conquistado e que a entrega é confirmada pelo Mestre; hoje o `Conquistas.tsx` da
App 05 cobre só a metade "lê", e a metade "avisa" não existe em aplicação alguma. A criança
desbloqueia a missão que dá o livro, a camisa ou o kit e **nada lhe diz**.

A fatia 29 do PRD-04 levantou esse aviso na elicitação de 2026-10-16 e o deixou fora, "sem
virar fatia nova". A decisão do fundador de **2026-10-19 reverte** aquele descarte e recorta
a fatia.

## What Changes

- A **tela da recompensa de desbloqueio** entra em `comum/trilha`, **antes** da próxima
  missão, quando o marco alcançado tem `RecompensaDeMarco` declarada. Quatro elementos, de
  cima para baixo: o **trio de estrelas**, a **descrição** do que foi conquistado, o **aviso
  de que a entrega é confirmada pelo Mestre** — que a §5.6.1 do PRD-05 obriga, e não é
  decoração — e o botão **Avançar**.
- Os três caminhos que alcançam o marco passam pela mesma tela: a **sondagem** respondida
  (`RF-05-72`), o **quiz** com ao menos 60% (`RN-05-45`) e o **desafio prático julgado pelo
  Mestre autor** (`RF-05-14`). No prático a tela **só** aparece depois da aprovação, porque
  marco alcançado é o desbloqueio e a capacidade `recompensa-de-marco` já recusa prático não
  julgado como marco alcançado.
- A **ciência da recompensa** nasce como fato do núcleo, por par (recompensa,
  Guerreiro(a)): o Avançar a grava, a leitura a devolve, e é ela que faz a tela aparecer
  **uma vez** e esperar a aprovação do Mestre sem polling (`RN-05-50`).
- `GET /v1/eu/recompensas` passa a devolver o **nome** e a **unidade** do tipo de recurso,
  além da quantidade que já devolvia. Hoje devolve o `tipo_de_recurso_id` cru, e por isso o
  `Conquistas.tsx` imprime "Quantidade conquistada: 1" sem dizer se é o livro, a camisa ou o
  kit — embora a capacidade já mande a leitura trazer o tipo de recurso. Corrigido junto, no
  mesmo ato.
- A camada comum ganha o **glifo de estrela cheia**, o primeiro do repositório, servido em
  trio. Preenchimento `--cor-ponto` e contorno `--cor-ponto-contorno`.
- **Exceção declarada ao documento 15 §9**, que reserva a estrela cheia ao ponto regular e
  abre com "nunca podem ser confundidas na tela". O fundador escolheu a estrela porque é o
  que a criança entende como "ganhei", e o **trio** é o diferenciador da grandeza ponto, que
  é sempre uma.

Nenhum ponto é creditado por este caminho: o desbloqueio não credita ponto por si, e
recompensa de marco não se compra nem se troca (`RF-05-46`, `RN-05-41`, invariante 23). A
tela nunca traz valor em moedas nem em reais (invariante 16).

### Fora do escopo

Reproduz o que o PRD-05 §3.2 e a §14 já excluem, sem exclusão nova:

- A **entrega** da recompensa e a fila do Mestre, que são do PRD-07 e do PRD-09 e já estão
  implementadas.
- O **acervo do Guerreiro(a)** (`RF-05-47` a `RF-05-49`), que é Ciclo 02.
- **Descrição escrita pelo Mestre autor** para a recompensa: fica como pendência nova do
  documento 09, por decisão do fundador de 2026-10-19 — nesta fatia a descrição é derivada
  do tipo de recurso.
- O **catálogo de qual marco entrega qual recompensa**, pendência do PRD-05 §14 que trava o
  `RF-05-45` "na prática, não no desenho".

## Capabilities

### New Capabilities

Nenhuma. O comportamento cabe nas capacidades que já existem.

### Modified Capabilities

- `recompensa-de-marco`: a **ciência** da recompensa conquistada passa a ser fato
  registrado, por Guerreiro(a); a leitura das conquistadas passa a trazer o **nome** e a
  **unidade** do tipo de recurso, e o `ciente`.
- `camada-visual-comum`: a camada passa a entregar o **glifo de estrela cheia** e o trio que
  marca a recompensa de marco, com a exceção do documento 15 §9 declarada.
- `aplicacao-da-aula-presencial`: o percurso da trilha no aparelho do encontro passa a
  apresentar a tela da recompensa antes da próxima missão.
- `area-do-guerreiro`: o mesmo na Área do Guerreiro(a), que é de quem o `RF-05-45` é.

## Impact

| Camada                   | O que muda                                                      |
| ------------------------ | --------------------------------------------------------------- |
| `backend/` — núcleo      | tabela da ciência, rota de gravação, leitura estendida          |
| `backend/alembic/`       | migração da tabela nova                                         |
| `comum/react/`           | glifo de estrela e o trio                                       |
| `comum/trilha/`          | a tela da recompensa e o ponto do percurso em que ela entra     |
| `apps/app-01-*`          | recebe a tela pelos componentes compartilhados                  |
| `apps/app-05-*`          | recebe a tela, e o `Conquistas.tsx` passa a nomear o recurso    |
| `docs/15-*` §9           | a exceção da estrela                                            |
| `docs/09-*` §1           | a decisão de 2026-10-19 e a pendência da descrição escrita      |
| `docs/prds/prd-05-*`     | a `RN-05-50`                                                    |
| `docs/99-*`              | se a relação entre documentos mudar                             |

Nenhuma pasta nova nasce: as esteiras de `backend/`, de `apps/*` e de `comum/` já existem, e
nenhum workflow de CI precisa ser criado. A revisão dos documentos entra **no mesmo PR**,
pelo precedente da fatia 24 do PRD-04.

### Riscos declarados

1. **A tela nasce dormente.** Nenhuma trilha tem `RecompensaDeMarco` declarada, porque o
   catálogo de qual marco entrega qual recompensa é pendência aberta do PRD-05 §14. O
   requisito está travado "na prática, não no desenho": a tela sai correta e só acorda
   quando o fundador decidir o catálogo. Os testes a exercitam com recompensa semeada.
2. **O contorno não tem versão escura.** O `--cor-ponto-contorno` não é redefinido no bloco
   `prefers-color-scheme: dark` do `comum/tokens.css`, então no tema escuro a borda
   `ponto-700` quase desaparece e o amarelo se sustenta sozinho. É lacuna **preexistente** da
   família ponto inteira, registrada aqui e **não** consertada nesta fatia.
