## Context

O assistente de trilhas já está de pé (fatias 10 a 12): rota, porta com adaptador local e de
nuvem, tela com botão de falar e campo de texto. O que existe hoje manda o áudio ao núcleo. Ver
`proposal.md` — Why; o contrato novo está nas duas specs do delta.

O precedente do desenho já está no repositório: `comum/biometria/` resolve a prova de vivacidade
e o descritor facial **no aparelho** e manda ao núcleo só o resultado. A transcrição da fala é o
mesmo caso, e o documento 03 §1.12 diz isso com estas palavras.

## Goals / Non-Goals

**Goals:**

- Transcrever no aparelho e mandar texto, com o microfone obedecendo `RF-04-39`.
- Deixar a transcrição em `comum/`, pronta para a fatia irmã do PRD-05 sem duplicação.
- Fechar a porta do áudio no núcleo, em vez de deixá-la aberta e não usada.

**Non-Goals:**

- A entrega da produção por fala (fatia irmã do PRD-05) e a leitura da foto do manuscrito, que
  segue no Gemini.
- Transcrição sem rede, ou transcrição por biblioteca embarcada no pacote da aplicação.
- Etiqueta de IA na resposta do assistente — pendência declarada na §14 do PRD-04.

## Decisions

1. **A transcrição vive em `comum/fala/`, em funções, não em hook.** Molde de
   `comum/biometria/`: `existeTranscricaoDeFala()` responde se o navegador oferece a API, e
   `iniciarTranscricao({ aoTranscrever, aoEncerrar, aoFalhar })` devolve um encerrador. Sem
   React dentro do módulo, sem dependência nova no `package.json` — a API é do navegador.
   _Alternativa descartada:_ hook em cada aplicação, que duplicaria o módulo nas Apps 01 e 05.

2. **A rota passa de `multipart/form-data` a corpo JSON**, com `model_config =
   ConfigDict(extra="forbid")`, como toda escrita de texto do núcleo (`equipes`, por exemplo).
   Ganho de graça: quem insistir em mandar `arquivo` recebe 422 com o campo apontado, em vez de
   ter o áudio ignorado em silêncio. _Alternativa descartada:_ manter `Form()` sem o arquivo —
   sustentaria `multipart` sem arquivo algum e aceitaria campo estranho calado.

3. **A porta do assistente perde o parâmetro `arquivo`.** `responder(texto: str, corpus: str)`:
   o adaptador de nuvem monta uma passada só de texto, e o local para de simular transcrição.
   `producoes` **não é tocada** — ela lê imagem e áudio até a fatia irmã do PRD-05.

4. **Uma fala por abertura do microfone, sem resultado parcial.** `continuous = false` e
   `interimResults = false`: a API fecha sozinha ao fim da fala, que é exatamente o que
   `RF-04-39` manda, e a tela não precisa decidir quando cortar. Enquanto o microfone está
   aberto a tela mostra "Ouvindo…"; a transcrição final cai no campo da pergunta, editável.
   _Alternativa descartada:_ resultado parcial em tela — dá retorno melhor durante a fala, mas
   acrescenta estado que a primeira entrega não precisa.

5. **`lang = "pt-BR"` fixo.** A plataforma é de uma comunidade brasileira e nenhum documento
   prevê outro idioma; herdar `navigator.language` faria um aparelho com locale inglês
   transcrever português como se fosse inglês.

6. **Detecção por `window.SpeechRecognition ?? window.webkitSpeechRecognition`**, com os tipos
   mínimos declarados dentro de `comum/fala/` — sem pacote de tipos novo, porque a interface
   usada é pequena e estável.

7. **Sem rede o caminho já está fechado.** Em Chrome a transcrição usa servidor do Google, então
   ela também depende de rede — e a tela do assistente já fica indisponível sem rede
   (`RF-04-58`, entregue na fatia 11). Nada novo a desenhar.

## Risks / Trade-offs

- **Sala barulhenta derruba a transcrição** → o campo de texto está sempre ao lado, nunca atrás
  de uma escolha de forma. É a pendência que a §14 do PRD-04 já registra, e a mitigação é a que
  ela mesma nomeia.
- **Em Chrome o áudio sai do aparelho, para servidor do Google** → sob a conta do navegador, não
  da plataforma. Registrado no documento 09 §1 na decisão de 2026-09-10; não há o que fazer no
  código, e não se promete em tela o que não é verdade em toda parte.
- **A transcrição editável rompe a cadeia entre a fala e o texto gravado** → aceito pelo
  fundador na mesma decisão: a forma "áudio" passa a valer o mesmo que a forma "texto".
- **`SpeechRecognition` não existe em jsdom** → os testes injetam um duplo em `window`, no mesmo
  padrão com que `assistente.test.tsx` já injeta `MediaRecorder` e `navigator.mediaDevices`.
- **Reconhecimento aberto e não encerrado deixaria o microfone ligado** → o encerrador é chamado
  em `onend`, em `onerror` e na limpeza do efeito da tela, e a tela nunca abre um segundo
  reconhecimento com um aberto.

## Migration Plan

Sem migração de banco: `ConsultaAoAssistente` guarda só as duas transcrições e nunca registrou a
forma da pergunta. A rota e a única chamadora dela mudam no mesmo PR, e não há consumidor
externo. Rollback é reverter o PR.
