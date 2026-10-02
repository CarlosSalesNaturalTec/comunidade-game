# Proposal

Origem: **PRD-05 — Área do Guerreiro(a) (App 05)**, fatia **9** do
`openspec/cronograma-de-fatias.md`.

Recorte: `RF-05-90` e `RN-05-49` (**novos**, a criar na revisão do PRD-05), alcançando
`RF-05-01` e `RF-05-02`.

## Why

A App 05 entra por reconhecimento facial (`RF-05-01`) e consome o mesmo `comum/biometria` da App
01, mas os modelos do Human só começam a baixar quando a pessoa já apertou o botão — a criança
espera o download inteiro de pé na frente do aparelho, sem saber o que está acontecendo. A fatia
24 do PRD-04 resolveu isso na App 01 e deixou `precarregarModelos()` pronto em `comum/`,
disponível à App 05 desde então.

O que faltava era **o disparo**, e ele não se herda da App 01: lá a pré-carga começa na abertura
da sessão de trabalho do aparelho, com a guarda
`if (!sessao || sessao.papel === "guerreiro") return;` — exige sessão aberta e **exclui
justamente o papel Guerreiro(a)**. Na App 05 quem vai ser reconhecido **não tem sessão**: o
reconhecimento é o que a abre. O momento equivalente era decisão do PRD-05, e o fundador o
elicitou em 2026-10-02.

## What Changes

- **A pré-carga começa depois de `existeCamera()` dar certo**, dentro do efeito que a tela de
  entrada já tem. Decisão do fundador de 2026-10-02, por duas razões: aparelho sem câmera é
  recusado pelo `RF-05-02` e vai ao adulto do `RN-05-02` — nunca gera descritor, então não faz
  sentido gastar a banda dele; e a pessoa digita o nick enquanto os modelos carregam, que é a
  sobreposição que a pré-carga existe para comprar.
- **A pré-carga sai com indicador** (`RF-05-90`, novo), no molde do `RF-04-75` da App 01:
  andamento como informação, nunca como erro, narrado quando a narração está ativada e sem
  depender de cor. A falha não interrompe a entrada.
- **A pré-carga nunca abre a câmera** (`RN-05-49`, novo), que desce do `RN-05-01` e do documento
  03 §3.3: ninguém pediu nada neste momento e não há consentimento em jogo. Carrega modelo, só.
- **Nascem `RF-05-90` e `RN-05-49` no PRD-05 §6.1**, como `RF-04-75` e `RN-04-42` nasceram na
  §6.1 do PRD-04. A alternativa — pré-carga silenciosa, sem `RF` — foi descartada pelo fundador
  em 2026-10-02.

O caminho de erro visível da conferência **não muda**: segue sendo o de `gerarDescritor()`, com
as mensagens que a tela já tem. A pré-carga não entra em aviso de coleta, porque não coleta dado
nenhum.

## Capabilities

### New Capabilities

Nenhuma. A capacidade que a fatia toca já existe.

### Modified Capabilities

- `area-do-guerreiro`: a entrada da App 05 passa a pré-carregar os modelos depois da verificação
  da câmera, com indicador de andamento e sem abrir a câmera (`RF-05-90`, `RN-05-49`, alcançando
  `RF-05-01` e `RF-05-02`). A capacidade `sessao-do-guerreiro`, que é a do núcleo, **não muda**:
  a pré-carga não chama rota nenhuma.

## Impact

| Alvo | O que muda |
| --- | --- |
| `apps/app-05-guerreiro/src/entrada/TelaDeEntradaDoGuerreiro.tsx` | o disparo e o indicador |
| `docs/prds/prd-05-area-do-guerreiro.md` §§6.1, 7, 13, 15 | `RF-05-90` e `RN-05-49` nascem |
| `docs/09-topicos-em-aberto-e-sugestoes.md` §1 | a decisão do momento e do indicador |

Nada no `backend/`: a pré-carga é inteiramente do aparelho e não chama rota nenhuma. Nada em
`comum/` — `precarregarModelos()` e `andamentoDosModelos()` já estão lá e não mudam de
assinatura; o segundo consumidor não pede componente novo em `comum/react`, pela mesma razão que
a fatia 24 do PRD-04 registrou. Nenhum lançamento no livro-razão: a pré-carga não tem custo de
nuvem, porque roda no próprio aparelho. Nenhum arquivo nasce em `docs/`.
