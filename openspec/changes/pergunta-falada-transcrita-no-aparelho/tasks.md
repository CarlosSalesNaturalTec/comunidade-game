## 1. Transcrição no aparelho, em `comum/`

- [x] 1.1 Criar `comum/fala/fala.ts` com os tipos mínimos de `SpeechRecognition` e as duas
      funções do design — decisão 1: `existeTranscricaoDeFala()`, por
      `window.SpeechRecognition ?? window.webkitSpeechRecognition` (decisão 6), e
      `iniciarTranscricao({ aoTranscrever, aoEncerrar, aoFalhar })`, com `lang = "pt-BR"`,
      `continuous = false` e `interimResults = false` (decisões 4 e 5), devolvendo o encerrador
      que fecha o microfone em `onend`, em `onerror` e quando chamado (`RF-04-39`, `RF-04-40`).
      Verificação: o módulo compila no `tsc` do pacote e nenhuma dependência nova entra no
      `package.json`.
- [x] 1.2 Exportar `comum/fala/indice.ts` e acrescentar o subcaminho `./fala` e a pasta `fala`
      ao `exports` e ao `files` do `comum/package.json`, no molde de `./biometria`. Verificação:
      um `import { existeTranscricaoDeFala } from "comum/fala"` na App 01 resolve.

## 2. O núcleo deixa de receber áudio

- [x] 2.1 `assistente/porta.py`: `responder(*, texto: str, corpus: str)` — cai o parâmetro
      `arquivo`, e o texto deixa de ser opcional (`RF-04-40`, `RN-04-21`, design — decisão 3).
      Verificação: nenhuma referência a `arquivo` sobra em `src/nucleo/assistente/`.
- [x] 2.2 `assistente/local.py`: usar o texto recebido como transcrição e remover a simulação de
      transcrição de áudio (`RF-04-40`).
- [x] 2.3 `assistente/nuvem.py`: montar uma passada só de texto ao Gemini — cai o `inlineData`
      com `audio/webm` e o `base64` que o alimentava (`RF-04-40`, decisão 3). Verificação: o
      `import base64` sai do arquivo.
- [x] 2.4 `assistente/regra.py`: `consultar_assistente_de_trilhas` recebe só `texto`, recusa com
      422 pergunta vazia ou só de espaços — no lugar da regra das "duas formas" —, e passa o
      texto à porta (`RF-04-40`, `RN-04-21`).
- [x] 2.5 `assistente/rotas.py`: a rota passa a receber corpo JSON com
      `ConsultaAoAssistenteEntrada(equipe_id, texto)` e `ConfigDict(extra="forbid")`, no lugar
      de `Form`/`UploadFile` (decisão 2). Verificação: `arquivo` no corpo devolve 422 com o
      campo apontado, e o OpenAPI da rota não declara `multipart/form-data`.

## 3. A tela transcreve e manda texto

- [x] 3.1 `apps/app-01-aula-presencial/src/api/assistente.ts`: `consultarAssistenteDeTrilhas`
      recebe a pergunta como `texto: string` e chama `chamarNucleo` com `corpo`, não com
      `formulario`; cai o tipo de entrada com `arquivo` (`RF-04-40`).
- [x] 3.2 `TelaDoAssistente.tsx`: trocar `getUserMedia`/`MediaRecorder` por
      `iniciarTranscricao` — o botão de falar abre a transcrição, a tela mostra "Ouvindo…"
      enquanto o microfone está aberto, e a transcrição final entra no campo da pergunta,
      editável antes do envio (`RF-04-39`, `RF-04-40`, `RN-04-20`, `RN-04-21`). Verificação:
      nenhum `Blob` nem `MediaRecorder` sobra no arquivo, e o encerrador é chamado na limpeza do
      efeito.
- [x] 3.3 `TelaDoAssistente.tsx`: quando `existeTranscricaoDeFala()` for falso, avisar em
      linguagem simples que ali a pergunta é por texto e não apresentar o botão de falar; e
      quando a transcrição falhar ou não devolver nada, dizê-lo sem apagar o que estava escrito
      (`RF-04-39`, `RF-04-40`, spec `aplicacao-da-aula-presencial` — requisito novo).

## 4. Testes

- [x] 4.1 `comum/fala/fala.test.ts`: navegador sem a API, transcrição devolvida ao
      `aoTranscrever`, falha no `aoFalhar` e microfone encerrado em `onend`, `onerror` e pelo
      encerrador — com um duplo de `SpeechRecognition` injetado em `window`, no padrão do
      `MediaRecorder` falso já usado na App 01 (`RF-04-39`, `RF-04-40`).
- [x] 4.2 `backend/tests/test_assistente_porta.py`: adequar os testes do adaptador local e do de
      nuvem à assinatura sem `arquivo`; trocar `test_local_transcreve_audio_sem_expor_os_bytes` e
      `test_nuvem_nao_registra_o_byte_do_audio_em_log` por um teste de que o corpo mandado ao
      Gemini traz só `text`, sem `inlineData` (`RF-04-40`, `RN-04-21`).
- [x] 4.3 `backend/tests/test_consulta_ao_assistente_rota.py`: trocar
      `test_duas_formas_juntas_e_recusada`, `test_nenhuma_forma_e_recusada` e
      `test_pergunta_por_audio_e_transcrita` pelos cenários novos da spec — pergunta em texto
      respondida e gravada, pergunta vazia ou só de espaços em 422, e `arquivo` no corpo recusado
      em 422 por `extra="forbid"`; adequar as demais chamadas de `files=`/`data=` ao corpo JSON
      (`RF-04-40`, `RN-04-21`, spec `consulta-ao-assistente`).
- [x] 4.4 `apps/app-01-aula-presencial/src/trilhas/assistente.test.tsx`: substituir os cenários
      de gravação de áudio pelos da tela nova — a fala virando texto no campo, a transcrição
      editada antes do envio chegando corrigida à chamada, o aviso onde o navegador não
      transcreve, o aviso quando a transcrição não devolve nada, e o microfone fechado sem toque
      (`RF-04-39`, `RF-04-40`, `RN-04-20`, `RN-04-21`).

## 5. Documentação

- [x] 5.1 `openspec/cronograma-de-fatias.md`: numerar a fatia do PRD-04 como **13** e marcá-la
      `implementado` com o slug desta change; corrigir na mesma linha o "quase não muda", e na
      linha da fatia irmã do PRD-05 a afirmação de que esta não tem delta de spec — tem, em
      `consulta-ao-assistente` e em `aplicacao-da-aula-presencial` (proposal — Capabilities).
- [x] 5.2 Nada muda em `docs/`: a decisão já está gravada no documento 03 §§1.12, 7, no
      documento 09 §1 e nos enunciados de `RF-04-40` e `RN-04-21`; a situação do PRD-04 em
      `docs/prds/index.md` não muda, nenhuma relação entre documentos mudou e nenhum arquivo
      nasceu em `docs/`. Verificação: o diff da change não toca `docs/` nem `mkdocs.yml`.
