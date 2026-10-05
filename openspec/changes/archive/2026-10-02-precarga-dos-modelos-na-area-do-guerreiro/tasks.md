# Tasks

> A tarefa 1.1 vem primeiro: `RF-05-90` e `RN-05-49` precisam existir no PRD-05 antes de o
> código os citar, como `RF-04-75` e `RN-04-42` nasceram antes da fatia 24 do PRD-04.

## 1. Os requisitos no PRD-05

- [x] 1.1 Gravar `RF-05-90` (indicador do andamento da pré-carga, como informação e não como
      erro) na §6.1 do PRD-05 e `RN-05-49` (a pré-carga nunca abre a câmera) na §7, com a
      descendência do `RN-05-01` e do documento 03 §3.3; acrescentar as duas linhas à
      rastreabilidade da §15 e registrar na §13 a decisão do fundador de 2026-10-02 — o momento
      do disparo e a escolha do indicador sobre a pré-carga silenciosa

## 2. O disparo e o indicador na entrada

- [x] 2.1 Disparar `precarregarModelos()` em `TelaDeEntradaDoGuerreiro.tsx` depois de
      `existeCamera()` dar certo, dentro do efeito que a tela já tem, sem bloquear o campo do
      nick e sem disparar no caminho da recusa por falta de câmera (`RF-05-90`, alcançando
      `RF-05-01` e `RF-05-02`)
- [x] 2.2 Apresentar o andamento com `Aviso tipo="andamento"`, lendo `andamentoDosModelos()`, e a
      falha como linha local de `role="status"` que não interrompe a entrada nem usa a frase da
      recusa da conferência (`RF-05-90`, `RN-05-48`)
- [x] 2.3 Garantir que a pré-carga não acende a câmera nem grava imagem no aparelho — a
      verificação de existência não é captura (`RN-05-49`, `RF-05-06`)

## 3. Testes

- [x] 3.1 Em `entrada.test.tsx`, cobrir os cenários do delta de `area-do-guerreiro` sobre o
      disparo: a pré-carga começa quando há câmera; NUNCA começa quando a verificação falha ou o
      acesso é negado; e o campo do nick segue aceitando digitação e submissão durante ela
      (`RF-05-90`, `RF-05-02`)
- [x] 3.2 No mesmo arquivo, cobrir os cenários do indicador e da privacidade: o andamento é
      anunciado como estado e não depende de cor; a falha não interrompe a entrada e não veste a
      frase da recusa do rosto; a pré-carga não abre a câmera e não deixa imagem no aparelho
      (`RF-05-90`, `RN-05-49`, `RN-05-48`, `RF-05-06`)

## 4. Documentação

- [x] 4.1 Marcar a fatia 9 do PRD-05 como `implementado` em
      `openspec/cronograma-de-fatias.md`, com o slug da change; mover para "Já decididos" do
      documento 09 §1 a decisão do momento do disparo e do indicador. A situação do PRD-05 em
      `docs/prds/index.md` não muda — já é `implementado` —, nenhuma relação entre documentos
      muda, nenhum arquivo nasce em `docs/` e a `nav` do `mkdocs.yml` fica como está
