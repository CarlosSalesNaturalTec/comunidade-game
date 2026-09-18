## 1. A decisão nova nos documentos-fonte

A decisão nasce aqui e só então vira código — hierarquia de autoridade do `CLAUDE.md`.

- [x] 1.1 Acrescentar ao documento 03 §3.3 o item **"Visor ao vivo, imagem capturada nunca
      exibida"**, com o texto do fundador (2026-09-17): o espelho é visor, mostra a pessoa a si
      mesma antes de existir captura, nada é guardado nem reexibido; o quadro congelado é
      proibido antes ou depois de gerar o descritor; o retorno a quem opera é abstrato. Verificar
      que a seção segue sem duplicar regra que já esteja em outro documento.
- [x] 1.2 Ajustar o **invariante 12** do documento 99 §6 para distinguir **visor ao vivo** de
      **imagem capturada** — sem a distinção, o espelho contradiz o invariante. Verificar que
      nenhum outro documento afirma a versão antiga da regra.
- [x] 1.3 Registrar a decisão em `docs/09-topicos-em-aberto-e-sugestoes.md` §1, linha nova
      **"Visor da captura no App 01"**, com o motivo (capturar às cegas é o que faz a vivacidade
      reprovar sem ninguém saber por quê) e o ajuste do invariante 12.
- [x] 1.4 Criar no PRD-04 os identificadores `RF-04-64` (visor ao vivo e retorno abstrato),
      `RF-04-65` (falha de preparo distinta da reprovação de vivacidade, e captura que conclui em
      aparelho sem aceleração gráfica) e `RN-04-34` (quadro congelado proibido), nas tabelas das
      seções correspondentes e na rastreabilidade do documento 99 §8, sem repetir texto
      normativo do documento 03.

## 2. O módulo `comum/biometria`

- [x] 2.1 Declarar o backend `webgl` na configuração da Human (`biometria.ts`), com o porquê em
      uma linha ao lado — a autosseleção escolhe `webgpu` onde `navigator.gpu` existe mas
      `requestAdapter()` devolve `null`, e ali o `load()` morre antes de buscar modelo
      (`RF-04-65`, design — decisão 1).
- [x] 2.2 Separar o **preparo** (abrir câmera e carregar modelos) da prova de vivacidade, com
      desfecho próprio e distinguível, de modo que falha de carga NEVER apareça como ausência de
      pessoa diante da câmera (`RF-04-65`, design — decisão 4).
- [x] 2.3 Expor a função que **acopla o espelho** a um elemento contêiner fornecido pela tela,
      anexando ali o próprio elemento de vídeo. A fronteira do módulo permanece: nem
      `MediaStream` nem quadro nem pixel saem dele (`RF-04-64`, `RN-04-34`, documento 99 §6
      invariante 12, design — decisão 2).
- [x] 2.4 Trocar o `detect()` de tiro único por **detecção em laço** até a vivacidade passar ou
      o tempo se esgotar, com o estado do laço legível por quem chama — rosto enquadrado,
      vivacidade confirmada (`RF-04-64`, design — decisão 3).

## 3. As três telas de câmera do App 01

- [x] 3.1 `TelaDeCaptura` (onboarding): apresentar o visor ao vivo e o retorno abstrato durante
      o laço, e distinguir na tela falha de preparo, reprovação de vivacidade e recusa do núcleo
      (`RF-04-64`, `RF-04-65`, `RN-04-34`).
- [x] 3.2 `TelaDeEntradaDoGuerreiro` (entrada pelo caminho das trilhas): o mesmo visor e o mesmo
      retorno abstrato, preservando a frase única da recusa do núcleo, que continua sem revelar
      a causa (`RF-04-64`, `RF-04-65`, `RF-04-20`, `RN-01-22`).
- [x] 3.3 `TelaDeMedicaoDoLimiar` (bancada): o mesmo visor nas duas capturas — referência e
      comparação —, sem mudar o que a tela guarda e descarta (`RF-04-64`, `RN-04-34`,
      `RN-04-32`).
- [x] 3.4 Acrescentar a menção ao visor no aviso de coleta e na área detalhada de direitos: a
      câmera aparece na tela e nada dela sai do aparelho (`RF-04-26`, `RF-04-64`).

## 4. Testes

- [x] 4.1 Em `captura.test.tsx` e `entrada.test.tsx`, cobrir os cenários do delta: o visor
      aparece quando a câmera abre; o quadro capturado não volta à tela; falha de preparo dá
      frase distinta da reprovação de vivacidade; e a recusa do núcleo segue indistinguível
      entre as suas três causas (`RF-04-64`, `RF-04-65`, `RF-04-20`, `RN-04-34`).
- [x] 4.2 Em `bancada.test.tsx`, cobrir o visor nas duas capturas da medição e a permanência do
      que a tela já garante — um descritor de referência por vez, comparada descartada no ato
      (`RF-04-64`, `RN-04-34`, `RN-04-32`).
- [x] 4.3 Cobrir no módulo `comum/biometria` o laço de detecção e o desfecho do preparo, com a
      Human dublada: laço que aprova, laço que esgota o tempo e preparo que falha
      (`RF-04-64`, `RF-04-65`).

## 5. Documentação

- [x] 5.1 Acrescentar ao bloco do PRD-04 do `openspec/cronograma-de-fatias.md` a linha desta
      change, sem número de fatia — correção de bug preexistente somada a decisão nova, no molde
      da linha de `2026-09-17-correcao-de-aulas-canceladas-e-modelos-de-biometria` —, registrando
      que ela **destrava a tarefa 4.1** da change da bancada. A situação do PRD-04 em
      `docs/prds/index.md` não muda, e nenhum arquivo novo entra em `docs/`, então a `nav` do
      `mkdocs.yml` segue como está.

## 6. Conferência no aparelho

- [ ] 6.1 **EM ABERTO — só existe depois do _deploy_, que acontece no _merge_ em `main`.**
      Conferir no aparelho do encontro, com DevTools: as requisições a
      `/modelos-de-biometria/` passam a existir, o visor aparece e a captura conclui. É o que
      destrava a tarefa 4.1 da change `2026-09-17-bancada-de-calibracao-do-limiar` — a medição
      do limiar, que segue sendo dela e não desta.
