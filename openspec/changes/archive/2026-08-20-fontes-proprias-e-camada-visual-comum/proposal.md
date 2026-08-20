## Why

**Origem: PRD-02 §10** — _"Acessibilidade digital no piso do documento 15 — WCAG 2.2 AA"_ —,
com a autoridade dos documentos 15 §§4, 5 e 12. Como os demais requisitos não funcionais
do PRD-02, esse não tem `RF-XX-nn` nem `RN-XX-nn`: o identificador que a change atende é
o requisito `A aplicação cumpre o piso de acessibilidade das oito aplicações`, já
consolidado em `openspec/specs/aplicacao-de-gestao/spec.md`, que a fatia da implantação
deixou declarado sem estar cumprido. Nenhum requisito novo é criado aqui.

Três coisas estão erradas hoje, e nenhuma delas avisa:

| O que está escrito                                         | O que acontece de verdade                     |
| ----------------------------------------------------------- | ----------------------------------------------- |
| `--fonte-texto: "Atkinson Hyperlegible Next"` em `comum/`  | Nenhum `@font-face` existe; renderiza em `system-ui` |
| Documento 15 §4 — duas famílias servidas pelo próprio domínio | Nenhum arquivo de fonte no repositório       |
| O erro do campo em `role="alert"`                          | Não está ligado ao campo: sem `aria-describedby` |

A terceira é a que pesa. Em `FormularioDeComunidade`, os três erros de campo aparecem em
parágrafo solto: quem usa leitor de tela tabula até o campo e não ouve nada, porque o `alert`
fala uma vez, ao surgir, e some do campo para sempre. Isso reprova o piso do documento 15 §5, e
vai se repetir em cada formulário das outras seis aplicações enquanto não houver onde consertar
uma vez só.

Consertar **agora**, com três telas, é o menor tamanho que esse conserto jamais terá.

## What Changes

**Quatro decisões do fundador**, tomadas na exploração desta fatia e gravadas nos
documentos-fonte no mesmo PR:

| Decisão                                                              | Gravada em          |
| -------------------------------------------------------------------- | ------------------- |
| `comum/` passa a abrigar também as fontes e uma camada de componentes | 03 §1.2, 15 §12, 09 |
| Archivo entra com o eixo de largura, e não só com o de peso          | 09                  |
| A lista de comunidades da App 03 é lista densa, não carta            | 09                  |
| A camada visual é capacidade própria, não parte da App 03            | esta change         |

A terceira aplica o temperamento **Operação** do documento 15 §6 — densidade alta, ilustração
só onde é dado. A carta do documento 15 §8.1 não entra: a rota de lista não devolve o
território, a representação visual nem a contagem de vinculados que o documento 11 §8.2 exige
dela, e carta pela metade contraria o documento 11 §8.3.

O que a change entrega:

- **As duas famílias servidas do próprio domínio**, em `comum/fontes/`: quatro `.woff2`
  variáveis, subconjuntos `latin` e `latin-ext`, com o `@font-face` em `comum/fontes.css`
  escrito no repositório — não importado de pacote de terceiro, para que o nome da família seja
  o do documento 15 e nenhum subconjunto fora do latino entre na saída.
- **A licença OFL de cada família** junto dos arquivos, como ela própria exige.
- **A camada de componentes em `comum/react/`**: `Botao`, `Campo`, `Aviso`, `Moldura`,
  `Cabecalho` e `EstadoDaLista` — seis, tirados do que as três telas usam, sem variante
  especulativa. É onde o alvo de toque, o foco visível, a associação do erro ao campo e a
  largura de leitura passam a ser cumpridos por construção, para as oito aplicações.
- **As três telas da App 03 revestidas** — entrada, comunidades e formulário —, consumindo a
  camada. A lista de comunidades vira lista densa.
- **`comum/` ganha a verificação dela**: `tsconfig.json` e Vitest próprios. O `frontend-ci.yml`
  já alcança a pasta pelo caminho e roda `npm run test --workspaces --if-present`, então
  nenhum workflow é editado.

Fora do escopo, sem exclusão nova: tudo o que o PRD-02 §3.2 já exclui; a carta do documento 15
§8.1, que a change anterior também deixou de fora e que segue sem prazo; o temperamento Arena,
que nasce com a primeira aplicação que o use; e as outras sete aplicações, que não existem.

## Capabilities

### New Capabilities

- `camada-visual-comum`: o que as oito aplicações compartilham para cumprir o piso do documento
  15 — as duas famílias tipográficas servidas do próprio domínio, as camadas de token e o
  contrato de acessibilidade dos componentes comuns (alvo de toque, foco visível, erro
  associado ao campo, nenhum significado por cor sozinha, largura de leitura).

### Modified Capabilities

- `aplicacao-de-gestao`: o requisito `A aplicação cumpre o piso de acessibilidade das oito
  aplicações` passa a exigir que as telas consumam a camada comum e ganha o cenário do erro de
  campo anunciado **no próprio campo** — que hoje nenhum cenário cobre e que a implementação
  atual não cumpre.

## Impact

- `comum/` — `fontes/` com quatro `.woff2` e as duas licenças, `fontes.css`, `react/` com seis
  componentes, `tsconfig.json`, testes e o mapa de `exports` do `package.json` ampliado para
  `./fontes.css` e `./react`.
- `apps/app-03-gestao/src/` — `index.css` e as quatro telas e componentes de tela; nenhuma
  mudança em `api/`, em `autenticacao/ContextoDeSessao.tsx` nem no armazenamento da sessão.
- `docs/03-plataforma-e-arquitetura.md` §1.2, `docs/15-identidade-visual.md` §12 e
  `docs/09-topicos-em-aberto-e-sugestoes.md` — as decisões novas. `docs/99` §1 só se a relação
  entre documentos mudar.
- **Sem impacto** em rota, contrato de API, modelo de dados, migração, chave de aplicação,
  sessão ou requisito de PRD. O backend não é tocado.
- Peso entregue ao navegador: 224 KB de fonte no `dist`, dos quais o aparelho em português
  baixa 121 KB — o `unicode-range` impede o pedido dos subconjuntos `latin-ext`.
