# Proposal

**PRD de origem:** PRD-03 (App 06). **Fatia:** linha "—" nova no bloco PRD-03 de
`openspec/cronograma-de-fatias.md` — ajuste por decisão do fundador, como as demais linhas "—"
do bloco. **Identificadores:** `RF-03-85`, `RF-03-88` e `RF-03-03` — **sem identificador novo**,
como na fatia 33 do PRD-04: a ampliação é apresentação da mídia que esses requisitos já
exibem, e nenhum enunciado do PRD-03 muda.

## Why

Na vitrine, a imagem do acervo abre na própria linha, presa na moldura fixa de 320 × 240 px
(documento 15 §12), e o detalhe de um desenho, de uma foto ou de uma customização do kit fica
ilegível. A decisão do fundador de 2026-11-11 deu a ampliação em tela cheia às Apps 01, 05 e
09 e deixou a App 06 de fora de propósito. O fundador decidiu em **2026-11-14** estendê-la à
vitrine, do mesmo jeito que o conteúdo da missão na App 01.

## What Changes

- **A imagem do acervo amplia ao toque.** Aberta a produção de um item do tipo imagem, a imagem
  na moldura passa a ser um controle: tocar, clicar ou acionar pelo teclado a abre **inteira,
  sem corte, no maior tamanho que a tela comporta**, sobre a página. Fecha pelo botão
  **"Fechar"**, pela tecla `Esc` ou pelo toque fora dela, e o foco volta à imagem.
- **Vale para as três fontes do acervo** — criação original, comprovação do prático e
  customização do kit — e para os dois lugares onde a linha aparece: a seção do portfólio e o
  portfólio da página do Guerreiro(a).
- **A linha não muda.** A produção continua abrindo na própria linha (`RF-03-85`); "Fechar a
  produção" continua recolhendo a linha; nada é gravado no aparelho (`RN-03-22`).
- **Só imagem**, sem pinça e sem arrastar, como nas outras aplicações. Vídeo e áudio ficam com
  os controles nativos; texto, link externo e arquivo não mudam.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-vitrine`: a imagem aberta na linha do portfólio passa a ampliar em tela cheia.

## Impact

- **Código:** `apps/app-06-vitrine/src/portfolio/ProducaoDoAcervo.tsx` liga a propriedade
  `ampliavel` do `MidiaDoNucleo`, que já existe; o comentário de `comum/react/MidiaDoNucleo.tsx`
  deixa de dizer que a vitrine não a pede. Sem CSS novo: a vitrine já carrega os estilos da
  camada comum, e o polyfill de `showModal` já está na configuração de teste da App 06.
- **Backend e API:** nenhuma mudança; a imagem ampliada reaproveita os bytes já buscados.
- **Documentação:** documento 15 §12 (a App 06 entra na ampliação), documento 09 §1 (a linha
  de 2026-11-11 deixa de excluir a vitrine, e a decisão de 2026-11-14 entra em "Já decididos")
  e a linha nova no cronograma. O PRD-03 não muda: ele não enuncia a moldura, que vive no
  documento 15 e nos specs.
