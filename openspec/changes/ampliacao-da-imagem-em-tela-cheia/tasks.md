# Tasks

## 1. Camada comum

- [ ] 1.1 `comum/react/Dialogo.tsx` e `estilos.css`: propriedades opcionais `telaCheia` e
      `fecharAoTocarFora` (design — decisão 3); os diálogos existentes não mudam. Verificar em
      `Dialogo.test.tsx`: tela cheia aplica a variante; toque no fundo fecha e devolve o foco;
      clique no corpo e no cabeçalho não fecha; sem as propriedades, nada muda (`RF-04-35`,
      `RF-05-11`, `RF-09-25`)
- [ ] 1.2 `comum/react/MidiaDoNucleo.tsx`: propriedade `ampliavel`, só para imagem — `<button>`
      com rótulo "Ampliar imagem: <alt>" em volta da imagem, abrindo o `Dialogo` em tela cheia
      com a mesma URL de objeto (design — decisões 1, 2 e 4). Verificar em
      `MidiaDoNucleo.test.tsx`: tocar abre a imagem ampliada sem nova busca; "Fechar" e `Esc`
      fecham e devolvem o foco; sem `ampliavel` não há botão; vídeo e áudio nunca ganham botão;
      falha e carregando seguem sem botão (`RF-04-35`, `RF-05-11`, `RF-09-25`)

## 2. Apps 01 e 05 — `comum/trilha`

- [ ] 2.1 `comum/trilha/Missao.tsx` e `comum/trilha/DesafioDeDesbloqueio.tsx`: ligar
      `ampliavel` na imagem do conteúdo e na da pergunta. Verificar nos testes das Apps 05 e 01
      (percurso do Guerreiro(a)) que tocar na imagem abre a tela cheia, que fechar mantém o mesmo
      item da sequência e que o vídeo não amplia (`RF-05-11`, `RF-05-13`, `RF-04-72`, `RF-04-73`)

## 3. App 01 — programação do encontro

- [ ] 3.1 `apps/app-01-aula-presencial/src/trilhas/TelaDaProgramacao.tsx`: imagem e vídeo do
      conteúdo por `MidiaDoNucleo` com `lerArquivoDoConteudo` de `comum/trilha/api`, imagem com
      `ampliavel`, e trava de avançar enquanto carrega, cedendo na falha (design — decisão 5).
      Verificar em `trilhas.test.tsx`: a imagem é buscada em bytes e nunca por
      `conteudo.referencia`; vídeo na mesma moldura; falha avisa e libera avançar; tocar amplia,
      fechar volta ao mesmo conteúdo e nada é enviado ao núcleo (`RF-04-35`)

## 4. App 09

- [ ] 4.1 Ligar `ampliavel` nas imagens de `ConteudoExibido.tsx`, `PreVisualizacaoDaMissao.tsx`,
      `DesafioDeDesbloqueio.tsx` e `TelaDeDesbloqueiosPendentes.tsx`. Verificar em
      `trilhas.test.tsx` e no teste dos desbloqueios pendentes: conteúdo, pergunta e comprovação
      em foto ampliam; vídeo não (`RF-09-25`, `RF-09-119`, `RF-09-132`)

## 5. Documentação

- [ ] 5.1 Documento 15 §12: a frase da moldura de mídia passa a dizer que a imagem, nas Apps 01,
      05 e 09, abre em tela cheia ao toque, sem pinça (decisão do fundador de 2026-11-11); e linha
      nova no topo de "Já decididos" do documento 09 §1. Os PRDs 04, 05 e 09, `docs/prds/index.md`,
      o documento 99 e a `nav` do `mkdocs.yml` não mudam. Verificar com `npm run lint` e
      `mkdocs build --strict`
- [ ] 5.2 `openspec/cronograma-de-fatias.md`: fatia 33 do bloco PRD-04 com o slug da change e a
      situação `implementado` ao arquivar (`em andamento` desde a abertura)

## Workflow follow-up

- `/opsx:verify` e `/opsx:archive` depois da revisão do fundador; o merge usa merge commit.
