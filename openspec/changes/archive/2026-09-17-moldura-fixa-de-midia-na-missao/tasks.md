## 1. Token e componente comum

- [x] 1.1 Acrescentar `--largura-de-miniatura: 320px` e `--altura-de-miniatura: 240px` a
      `comum/tokens.css`, na camada semântica, e verificar que nenhum token existente muda.
- [x] 1.2 Criar `MidiaDoNucleo` em `comum/react`: recebe a função que busca os bytes, o `tipo`
      (`imagem`/`video`), o token de sessão, o `alt`/rótulo e o texto de erro; busca, monta e
      revoga a URL de objeto, aplica a moldura fixa (`--largura-de-miniatura`/
      `--altura-de-miniatura`, `object-fit: contain`, friso `--cor-campo-desabilitado`, borda
      `--cor-separador`, `--raio-campo`) e trata carregando/erro sem travar a tela. Exportar ao
      lado de `Aviso`/`Botao`. Verificar com o teste da tarefa 1.3.
- [x] 1.3 Testar `MidiaDoNucleo`: imagem exibida com a classe/estilo da moldura fixa, vídeo com
      a mesma moldura, erro de carregamento mostrando o texto de aviso sem travar, e a URL de
      objeto revogada ao desmontar. `vitest run` do arquivo passa.

## 2. App 09 — pré-visualização e edição do desafio

- [x] 2.1 Em `PreVisualizacaoDaMissao.tsx`, trocar `ConteudoPreVisualizado` por `MidiaDoNucleo`
      para imagem e vídeo do conteúdo da missão (`RF-09-25`).
- [x] 2.2 Na mesma tela, exibir a imagem da pergunta do desafio de desbloqueio/sondagem via
      `MidiaDoNucleo`, chamando `lerImagemDaPergunta` para cada pergunta que tiver
      `imagem_referencia` (`RF-09-25`, `RF-09-119`).
- [x] 2.3 Em `DesafioDeDesbloqueio.tsx` (App 09), trocar `ImagemDaPergunta` por `MidiaDoNucleo`
      para a imagem anexada na edição (`RF-09-119`).
- [x] 2.4 Testar em `trilhas.test.tsx`: a pré-visualização exibe conteúdo e imagem da pergunta
      em moldura fixa (cenários "A pré-visualização apresenta a imagem da pergunta do quiz" e
      "Imagem grande cabe na moldura fixa, sem cortar"), e a edição do desafio exibe a imagem
      anexada na mesma moldura (cenário "A imagem anexada na edição do desafio usa a mesma
      moldura"). `vitest run` do arquivo passa (117/117).

## 3. App 05 — telas reais do Guerreiro(a)

- [x] 3.1 Em `Missao.tsx`, trocar `ConteudoDaMissao` por `MidiaDoNucleo` para imagem e vídeo do
      conteúdo (`RF-05-11`).
- [x] 3.2 Em `DesafioDeDesbloqueio.tsx` (App 05), trocar `ImagemDaPergunta` por `MidiaDoNucleo`
      para a imagem da pergunta (`RF-05-11`, `RF-09-119`).
- [x] 3.3 Testar em `Missao.test.tsx` e `DesafioDeDesbloqueio.test.tsx`: conteúdo e imagem da
      pergunta exibidos em moldura fixa, cobrindo os cenários "Imagem grande do conteúdo cabe
      na moldura fixa, sem cortar", "Vídeo do conteúdo usa a mesma moldura da imagem" e "A
      imagem da pergunta do desbloqueio usa a mesma moldura". `vitest run` de cada arquivo
      passa (20/20 em `Missao.test.tsx`+`DesafioDeDesbloqueio.test.tsx`+`Sondagem.test.tsx`+
      `Trilha.test.tsx`+`GuiaDaTrilha.test.tsx`).

## 4. Documentação e fechamento

- [x] 4.1 Acrescentar em `docs/15-identidade-visual.md` §12 a nota dos dois tokens novos
      (`--largura-de-miniatura`, `--altura-de-miniatura`).
- [x] 4.2 Marcar a linha "Moldura fixa de mídia na missão" como "implementado" em
      `openspec/cronograma-de-fatias.md`.
