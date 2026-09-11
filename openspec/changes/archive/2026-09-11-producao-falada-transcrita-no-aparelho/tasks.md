## 1. O núcleo deixa de receber áudio

- [x] 1.1 `producoes/regra.py`: `_conferir_forma_unica` passa a conferir o conteúdo esperado de
      cada forma — `texto` e `audio` exigem `texto` e recusam `arquivo`; `foto` exige `arquivo`
      e recusa `texto` —, seguindo com 422 no campo `forma` (`RF-05-74`, `RF-05-76`,
      `RN-05-32`, design — decisão 2). Verificação: a mesma conferência serve as duas portas,
      sem ramo por porta.
- [x] 1.2 `producoes/regra.py`: em `_ler_e_montar_producao`, o desvio da indisponibilidade
      passa de `forma == texto` para `forma != foto` — a entrega falada grava com a transcrição
      recebida e a devolutiva em branco, e só a foto levanta
      `LeituraDaProducaoIndisponivel` (`RF-05-76`, design — decisão 4). Verificação: a linha de
      log da indisponibilidade só sai na foto, e segue sem o byte do arquivo.
- [x] 1.3 `producoes/rotas.py`: `arquivo` segue `UploadFile | None` nas duas rotas, agora só
      aceito com `forma=foto`; atualizar as docstrings que prometem áudio ou foto no arquivo
      (`RF-04-45`, `RF-05-74`, `RF-05-76`, design — decisão 1). Verificação: as duas rotas
      seguem em `multipart/form-data` no OpenAPI.
- [x] 1.4 `producoes/local.py`: a forma `audio` passa pelo caminho do texto — devolve o texto
      recebido como transcrição — e cai a transcrição simulada de áudio; só a `foto` continua
      simulando leitura de mídia (`RF-05-76`, design — decisão 3).
- [x] 1.5 `producoes/nuvem.py`: montar passada só de texto para `texto` e `audio`, com
      `inlineData` apenas na foto; `_MIME_POR_FORMA` se reduz à imagem (`RF-05-76`,
      `RN-05-32`, design — decisão 3). Verificação: nenhum `audio/webm` sobra no módulo.

## 2. As duas telas transcrevem no aparelho

- [x] 2.1 `apps/app-01-aula-presencial/src/trilhas/EntregaDaProducao.tsx`: trocar
      `getUserMedia`/`MediaRecorder` por `iniciarTranscricao` de `comum/fala` — o botão de
      falar abre o microfone, a tela mostra "Ouvindo…" enquanto ele está aberto e a transcrição
      cai no campo da produção, editável antes do envio, com `forma=audio` (`RF-04-45`,
      `RF-05-76`, `RN-04-20`, `RN-05-32`, design — decisões 5, 6). Verificação: nenhum `Blob`
      nem `MediaRecorder` sobra no arquivo, e o encerrador é chamado na limpeza do efeito.
- [x] 2.2 `EntregaDaProducao.tsx` da App 01: quando `existeTranscricaoDeFala()` for falso, não
      oferecer a forma fala e avisar que ali a entrega é por texto ou por foto; quando a
      transcrição falhar ou não devolver nada, dizê-lo sem apagar o que estava escrito
      (`RF-04-45`, `RF-05-76`, spec `aplicacao-da-aula-presencial`).
- [x] 2.3 `apps/app-05-guerreiro/src/trilha/EntregaDaProducao.tsx`: a forma "Gravar a fala"
      passa a "Falar", pelo `comum/fala`, com a transcrição caindo no mesmo campo de texto da
      produção, editável, e `forma=audio` no envio; o `input type="file"` de áudio e a entrada
      `FORMATOS_ACEITOS.audio` saem (`RF-05-74`, `RF-05-76`, `RN-05-32`, design — decisões 5,
      6).
- [x] 2.4 `EntregaDaProducao.tsx` da App 05: o aviso antes da fala passa a dizer, em linguagem
      da criança, que a gravação **não sai do aparelho**; o da foto segue dizendo o descarte na
      leitura. Sem a API no navegador, a forma fala não é oferecida e a tela o diz, mantendo
      escrever, fotografar e entregar ao Mestre no encontro (`RF-05-76`, `RF-05-78`,
      `RN-05-32`, `RN-05-37`, spec `area-do-guerreiro`).
- [x] 2.5 `apps/app-01-aula-presencial/src/api/producao.ts` e
      `apps/app-05-guerreiro/src/api/trilha.ts`: os dois comentários de cabeçalho deixam de
      prometer que "o áudio não fica no aparelho depois do envio" e passam a dizer que o áudio
      não é enviado — a fala vai transcrita (`RF-05-76`, `RN-05-32`). A assinatura das duas
      funções não muda: `texto` e `arquivo` já são opcionais.
- [x] 2.6 `apps/app-05-guerreiro/src/coleta/RegistrarMedicao.tsx`: trocar a cópia própria da
      Web Speech API — `ConstrutorDeReconhecimento` e `obterConstrutorDeReconhecimento` — por
      `existeTranscricaoDeFala` e `iniciarTranscricao` de `comum/fala`, preservando
      `extrairNumero`, a origem `voz` e o ditado oferecido só onde a API existe (`RF-05-33`,
      `RN-05-32`, design — decisão 7). O duplo de `SpeechRecognition` de
      `RegistrarMedicao.test.tsx` ganha `stop()` e passa a chamar `onend`, que o contrato de
      `comum/fala` exige. Verificação: nenhum `SpeechRecognition` sobra em
      `apps/app-05-guerreiro/src/` fora do duplo de teste.

## 3. Testes

- [x] 3.1 `backend/tests/test_producao_da_missao.py`: trocar as entregas por áudio com
      `files=` pelos cenários novos das duas portas — fala transcrita chegando como `texto` com
      `forma=audio` e gravada assim, e `forma=audio` com arquivo recusada em 422 no campo
      `forma` —, mantendo os cenários de foto, de duas formas juntas e de entrega sem conteúdo
      (`RF-05-74`, `RF-05-76`, `RN-05-32`, spec `producao-da-missao`).
- [x] 3.2 `backend/tests/test_producao_da_missao_porta.py`: adequar os testes dos dois
      adaptadores — o local devolve o texto recebido na forma `audio`, e o corpo mandado ao
      Gemini traz só `text` fora da foto; trocar
      `test_503_na_foto_e_no_audio_quando_leitura_indisponivel` e o par individual dele por
      503 **só na foto** e 201 com devolutiva em branco na fala; o teste de que o log não traz
      o byte enviado passa a ser o da foto (`RF-05-76`, `RN-05-32`, spec
      `producao-da-missao`).
- [x] 3.3 `apps/app-05-guerreiro/src/trilha/EntregaDaProducao.test.tsx`: substituir os cenários
      de envio de arquivo de áudio pelos da tela nova — a fala virando texto no campo, a
      transcrição editada antes do envio chegando corrigida com `forma=audio`, o aviso de que a
      gravação não sai do aparelho, o aviso onde o navegador não transcreve e quando a
      transcrição não devolve nada —, com o duplo de `SpeechRecognition` injetado em `window`
      (`RF-05-74`, `RF-05-76`, `RN-05-32`, spec `area-do-guerreiro`).
- [x] 3.4 `apps/app-01-aula-presencial/src/trilhas/trilhas.test.tsx`: acrescentar aos cenários
      da entrega da equipe a fala transcrita no aparelho chegando como texto com `forma=audio`,
      o microfone fechado sem toque e o aviso onde o navegador não transcreve; o cenário do 503
      passa a ser o da foto (`RF-04-45`, `RF-05-76`, `RN-04-20`, `RN-05-32`, spec
      `aplicacao-da-aula-presencial`).

## 4. Documentação

- [x] 4.1 `openspec/cronograma-de-fatias.md`: marcar a fatia do PRD-05 como `implementado` com
      o slug desta change e corrigir, na mesma linha, a afirmação de que o núcleo deduz a forma
      do campo preenchido — ela já chega explícita desde a fatia 9 do PRD-04 (proposal — What
      Changes).
- [x] 4.2 `docs/03-plataforma-e-arquitetura.md` §12.2: a linha "Foto e áudio da produção do
      Guerreiro(a)" passa a separar as duas mídias — a foto **descartada na leitura**, o áudio
      **não recebido**, porque a fala é transcrita no aparelho (§1.12). Correção de texto para
      uma decisão já gravada (fundador, 2026-09-10, documento 09 §1): nada entra no documento
      09, nenhum PRD muda, a situação do PRD-05 em `docs/prds/index.md` não muda, nenhuma
      relação entre documentos mudou e nenhum arquivo nasceu em `docs/`.
