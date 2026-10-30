# Proposal

Origem: a **linha transversal da marca** do `openspec/cronograma-de-fatias.md` — não é fatia
de PRD. O símbolo é a forma da marca do projeto (documento 15 §13) e serve o cabeçalho das
**oito** aplicações, além de ser o favicon de todas.

A change não fecha recorte de `RF`: executa a decisão do fundador de **2026-10-30** sobre a
figura dentro do escudo e sobre a espessura do contorno, que descem aos documentos 09 e 15
aqui. É o mesmo molde da `2026-10-02-ponta-do-escudo-e-traco-unico-da-marca`, pelo precedente
de que desenho de marca não gera identificador novo.

## Why

**O monograma `CG` não diz nada sobre o projeto.** Duas letras são o que havia quando a marca
nasceu, em 2026-10-02. O fundador decidiu substituí-las pelo **Sankofa**, o pássaro mítico
akan que anda para a frente com a cabeça virada para trás, pegando o ovo que ficou — "voltar e
buscar o que foi deixado". O sentido casa com o projeto, que trabalha herança afro-brasileira
(documento 02) e tem Zeferina no documento 10.

**Duas formas foram avaliadas, e a segunda foi descartada por colisão.** A proposta
alternativa era trocar o escudo inteiro pelo **coração** Sankofa. O coração já é a silhueta da
família de badge **"de valores e causas"** (documento 15 §8.3, implementado em
`comum/react/BadgeDaFamilia.tsx`): adotá-lo reintroduziria exatamente a confusão marca/badge
que a troca do badge **de nível** para losango resolveu em 2026-10-02, e desta vez contra a
família de sentido mais próximo. Na carta do Guerreiro(a), marca e badge apareceriam com a
mesma forma na mesma tela. **O escudo fica**, e o §8.3 segue válido sem alteração.

**O contorno do escudo é fino para a figura nova.** O fundador pediu contorno um pouco mais
grosso. A medição mostrou teto de `3,28/42`, imposto pelo caso que exige o ápice mais metade
da espessura dentro da grade, no `simbolo.svg`:

| Versão | Hoje | Teto | Margem |
| --- | --- | --- | --- |
| Colorida | `1,5/42` | `3,28/42` | ×2,19 |
| Monocromática | `2,5/42` | `3,28/42` | ×1,31 |

Não há como engrossar as duas preservando a relação de peso vigente (1,67×) sem encostar no
teto. Decidida a **opção (a)**: colorida `2,0/42`, monocromática `3,0/42`, relação em 1,50×.

**Esta decisão precede o desenho.** O contorno monta sobre a linha de centro e metade cresce
para dentro, comendo ~0,45 un. de largura útil na faixa baixa do escudo. Desenhar primeiro e
engrossar depois obrigaria a redesenhar.

## What Changes

- **A figura dentro do escudo deixa de ser o monograma `CG` e passa a ser o pássaro Sankofa**,
  nas cinco peças que carregam o escudo. Só o **segundo `<path>`** de cada arquivo muda.
- **A silhueta do escudo não muda**: proporção `1 : 1,172`, topo em ponta, base em ponta e a
  área de proteção do §13.4 ficam como estão.
- **O contorno engrossa** para `2,0/42` (colorida) e `3,0/42` (monocromática).
- **O desenho do pássaro**, fechado em seis rodadas de esboço com o fundador: silhueta
  contínua — corpo, pescoço, cabeça e bico num traçado só —, peito circular, cabeça destacada
  do pescoço por recorte na mandíbula, olho vazado, **bico aberto e simétrico**, **ovo no eixo
  do bico**, cauda em leque com as penas vazadas por dentro, vazados no peito e no dorso, e
  **pernas sem pés**.
- **O documento 15 §§13.1, 13.2 e 13.3** passam a descrever a figura nova e as razões de
  contorno; o **documento 09 §1** recebe a decisão em "Já decididos", como **linha nova**.
- **O `comum/marca/README.md` §8** registra a procedência: desenho produzido pelo projeto, a
  partir de referência do fundador **medida, não traçada**, e declara que o que a marca
  reserva (documento 03 §1, princípio 4) é **o desenho do projeto**, não o símbolo Sankofa,
  que é patrimônio adinkra akan.

## Capabilities

### New Capabilities

Nenhuma. A change altera requisitos de uma capacidade existente.

### Modified Capabilities

- `camada-visual-comum`: o requisito **"O escudo da marca tem o topo em ponta"** é
  **substituído**. Ele exige hoje que *"o **monograma** SHALL continuar dentro do escudo"*, com
  cenário homônimo, e não há mais monograma; o que ele exigia da **forma** — topo em ponta por
  duas curvas, base em ponta — segue exigido no requisito que entra no lugar. Entram ainda três
  requisitos novos: **o que a figura é**, **como as contraformas dela se comportam** nas duas
  versões, e **de quem é o reconhecimento no tamanho mínimo**.

## Impact

- `comum/marca/`: cinco arquivos redesenhados — `simbolo.svg`, `simbolo-mono.svg`,
  `marca-horizontal.svg`, `marca-horizontal-mono.svg`, `marca-empilhada.svg`. As submarcas não
  carregam escudo e **não são tocadas**.
- `comum/marca.test.ts`: a constante `RAZAO_DE_CONTORNO` e o caso
  `"mantém o monograma dentro do escudo"`, que precisa deixar de falar em monograma. Os casos
  de silhueta única, proporção, ponta no topo e ápice contra a grade **continuam valendo sem
  alteração** — é o que a decisão de manter o escudo compra.
- Orçamento de peso: `simbolo.svg` usa hoje 1.395 B de 3.072. A figura nova é maior que o
  monograma, e o orçamento precisa ser conferido na implementação.
- `docs/15-identidade-visual.md` §§13.1, 13.2, 13.3; `docs/09-topicos-em-aberto-e-sugestoes.md`
  §1; `comum/marca/README.md` §§1 e 8; `openspec/cronograma-de-fatias.md`, linha transversal
  nova.
- Nenhuma aplicação muda de comportamento: `MarcaDoProjeto` embute os arquivos por `?raw` e
  não conhece a figura. O favicon acompanha sozinho, porque `provisionamento.ts` copia o
  `simbolo.svg`.
- **Fora do escopo:** a silhueta do escudo, as submarcas, o badge de nível em losango, o
  coração da família "de valores e causas", o elenco e a moldura circular do avatar.

## Open Questions

1. **A conferência final do desenho é visual e é do fundador.** Os esboços foram julgados
   isolados, a 16, 24, 48 e 140 px. O que o estudo não mostra é o pássaro **aplicado nas cinco
   peças** — sobretudo nos dois conjuntos, onde ele reencaixa por `transform`. A revisão
   acontece no PR.
2. **Três acabamentos ficaram apontados e não decididos**: as pontas da cauda, que hoje
   terminam em borda arredondada em vez de ultrapassarem a massa; as **serrilhas da crista** no
   dorso, que a referência tem e o desenho não; e o quanto a silhueta ainda puxa para pato.
   Nenhum trava a implementação — são ajuste de traço dentro das tarefas.
