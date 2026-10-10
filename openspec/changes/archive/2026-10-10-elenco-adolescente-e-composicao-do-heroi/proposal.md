# Proposal

> **PRD-03 — Vitrine pública (App 06).** Entra no cronograma como **linha sem número** no
> bloco do PRD-03, como a correção `2026-10-09-acesso-ao-nucleo-e-rotas-servidas-da-vitrine`:
> **não fecha recorte de `RF`** — atende ou preserva `RF-03-01` e `RF-03-51`. Decisão do
> fundador de 2026-10-10, tomada em `/opsx:explore` antes de a change abrir.

## Why

O elenco chegou em 2026-10-09 com **Susy e Otávio crianças**, e o público da plataforma vai
dos 6 aos 16 anos (documento 01). Metade da faixa não se vê no herói da vitrine, que é a
primeira tela pública do projeto.

As duas figuras adolescentes já existem, dirigidas pelo fundador na mesma ferramenta e no
mesmo traço da leva anterior. O que falta é **como o repositório as acomoda** sem perder as
crianças, e **como o herói as apresenta**.

## What Changes

Quatro decisões do fundador de 2026-10-10, que descem ao documento 15 §13.6 e ao documento 09
**antes** do código, como manda a hierarquia de autoridade:

1. **Susy e Otávio passam a ter duas faixas etárias** — criança e adolescente. O elenco segue
   sendo **quatro personagens**: Trenell (adulto) e Robô Educa não ganham variante.
2. **O nome base é a versão que se apresenta.** Os pares de hoje viram
   `susy-crianca.{avif,webp}` e `otavio-crianca.{avif,webp}`; os adolescentes ocupam
   `susy.{avif,webp}` e `otavio.{avif,webp}`. Preserva a invariante do `comum/marca/README.md`
   §3, cujo sufixo até aqui só previa **expressão** e passa a prever **faixa etária**.
3. **Adereço que caracteriza é admitido** na pose do §13.6 — o skate de Susy, o controle e o
   fone de Otávio. Sem ele a mudança de idade não se lê nos 208 px de altura do herói. O
   resto da regra não afrouxa: contorno quase preto grosso e fechado, preenchimento chapado,
   fundo transparente e keyline `cal-050` gravado no arquivo.
4. **Composição nova do herói**: de `susy, otavio, trenell, robo-educa` para
   **`susy, robo-educa, trenell, otavio`** — professor e criatura ao centro, alunos nas
   extremidades, e a mão aberta do professor indicando o Robô Educa. A ordem deixa de ser
   arbitrária e passa a ter **dependência**: Trenell imediatamente à direita do Robô Educa,
   senão o gesto aponta para o vazio.

Entra também, por decisão do fundador de 2026-10-10 na mesma sessão, o **teste que faltava**:
nenhum caso guarda hoje os arquivos do elenco contra o manifesto do `README.md` §3 — só a
igualdade byte a byte entre `comum/` e `dist/`. Com o elenco virando algo que cresce, a
conferência deixa de ser manual.

**Não é BREAKING**: a vitrine continua publicando oito arquivos, com os mesmos quatro nomes
base; o que muda é o conteúdo de dois deles e a ordem de apresentação.

## Capabilities

### New Capabilities

Nenhuma. O elenco e o herói já têm dono: `camada-visual-comum` e `aplicacao-da-vitrine`.

### Modified Capabilities

- `camada-visual-comum`: requisito **novo** — o elenco admite **variante por faixa etária**,
  o arquivo de nome base é sempre a versão que se apresenta, e cada arquivo cumpre o
  manifesto (par AVIF com reserva WebP, 1024 px de lado maior, teto de peso, fundo
  transparente e keyline `cal-050` na borda). É o que o caso novo de `comum/marca.test.ts`
  verifica.
- `aplicacao-da-vitrine`: o requisito **"A abertura tem herói, com ilustração em primeiro
  plano"** ganha a **composição** — a ordem das quatro figuras é fixa e tem razão, com o
  professor ao lado da criatura que ele indica. O que já está lá (a frase, a ação única, a
  sobrevivência sem ilustração, nada de domínio de terceiro) não muda.

## Impact

| Onde | O quê |
| --- | --- |
| `comum/marca/elenco/` | 4 arquivos novos, 4 renomeados por `git mv` — 12 ao todo |
| `comum/marca/README.md` | §3 (variante por faixa etária, e o que se provisiona) e §8 (procedência da leva de 2026-10-10) |
| `comum/marca/provisionamento.ts` | `ELENCO` segue com quatro nomes: **provisiona-se só o que se apresenta**, e os `-crianca` ficam versionados fora do `dist/` |
| `comum/marca.test.ts` | caso novo do manifesto do elenco |
| `apps/app-06-vitrine/` | `Heroi.tsx` (ordem, larguras, `aria-label`), `index.css` (o comentário da composição), `saidaDoBuild.test.ts` (a sequência literal do `srcset`, que é o que trava a ordem) |
| `docs/15-identidade-visual.md` §13.6 | as duas faixas etárias, o adereço e a composição — fonte única do elenco (documento 99 §1) |
| `docs/09-topicos-em-aberto-e-sugestoes.md` | as decisões de 2026-10-10; a linha "Roteiro e narrativa do elenco" **estreita, não fecha** |
| `openspec/cronograma-de-fatias.md` | linha sem número no bloco do PRD-03 |

**Fora do escopo**, como o PRD-03 §3.2 já exclui e as decisões acima não alteram: roteiro e
identidade narrativa do elenco, e o personagem dos Rôbróders — seguem pendentes no documento
09. Variante de **expressão** não entra: a decisão é de faixa etária. Trenell e Robô Educa
não ganham variante. Nenhum arquivo nasce em `docs/`, e `docs/prds/index.md` não muda — o
PRD-03 já está implementado.
