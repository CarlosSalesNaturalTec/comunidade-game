## Context

As duas portas da produção estão de pé — `POST /v1/equipes/{id}/producao` (fatia 9 do PRD-04) e
`POST /v1/eu/missoes/{id}/producao` (fatia 7 do PRD-05) —, ambas em `multipart/form-data`, com
`forma` já declarada no corpo e `arquivo` recebendo áudio ou foto. A spec consolidada está em
`openspec/specs/producao-da-missao/`; o contrato novo está no delta desta change.

O módulo da transcrição no aparelho já existe: `comum/fala/`, entregue pela fatia 13 do PRD-04
justamente para esta fatia consumir sem duplicar (`existeTranscricaoDeFala()` e
`iniciarTranscricao({ aoTranscrever, aoFalhar, aoEncerrar })`). O precedente mais antigo é
`comum/biometria/`, que resolve a prova de vivacidade no aparelho e manda ao núcleo só o
descritor.

## Goals / Non-Goals

**Goals:**

- Transcrever a fala no aparelho nas duas telas da produção e mandar texto, reaproveitando
  `comum/fala` sem código novo de reconhecimento.
- Fechar a porta do áudio no núcleo, em vez de deixá-la aberta e não usada.
- Fazer a entrega falada valer o que a entrega por texto já vale quando a devolutiva não vem.

**Non-Goals:**

- A leitura da **foto** do manuscrito, que segue no Gemini e segue em `multipart`.
- O apoio escolar por voz e o canal de sugestões em áudio — PRD-05 §3.2, Ciclo 02.
- Transcrição sem rede, ou por biblioteca embarcada no pacote da aplicação.
- Etiqueta de IA na devolutiva e medição do consumo por ato — a spec já os exclui.

## Decisions

1. **As rotas seguem em `multipart/form-data`.** A foto ainda sobe como arquivo, então não há
   corpo JSON a ganhar aqui — ao contrário da rota do assistente, que ficou sem arquivo algum e
   migrou para JSON na fatia irmã. `forma` continua `Form()` e `arquivo` continua
   `UploadFile | None`, agora recusado fora de `forma=foto`.
   _Alternativa descartada:_ duas rotas, uma JSON para texto e áudio e uma `multipart` para a
   foto — dobraria a superfície de uma entrega que é uma só.

2. **A forma única passa a ser conferida por conteúdo esperado, em `_conferir_forma_unica`.**
   `texto` e `audio` exigem `texto` e recusam `arquivo`; `foto` exige `arquivo` e recusa
   `texto` — 422 com o campo `forma` apontado, como já responde hoje. É o único lugar da regra
   que muda, e vale de graça para as duas portas, que já o compartilham.

3. **A porta mantém a assinatura e passa a ramificar na foto.**
   `ler(*, forma, texto, arquivo, producao_esperada)` fica como está: `forma` segue sendo dado
   gravado e segue na linha de log. Nos adaptadores, `audio` deixa de ser mídia e passa pelo
   caminho do texto — o de nuvem monta uma passada só de texto, sem `inlineData` de som, e o
   local devolve o texto recebido em vez de simular transcrição.
   _Alternativa descartada:_ tirar `forma` da porta e ramificar por `arquivo is None` — a porta
   perderia o dado que ela mesma registra no log da indisponibilidade.

4. **Sem leitura, a entrega falada grava com devolutiva em branco.** A regra do 503 existia
   porque sem o modelo não havia transcrição; transcrita no aparelho, a fala tem transcrição
   antes de qualquer chamada, e recusá-la seria perder a produção da criança por
   indisponibilidade de provedor. Em `_ler_e_montar_producao`, o desvio deixa de ser
   `forma == texto` e passa a ser `forma != foto`.

5. **A transcrição cai no mesmo campo de texto da produção, editável, e a `forma` enviada segue
   `audio`.** É o que distingue a fala do texto digitado num contrato em que as duas chegam
   como texto — o documento 09 §1 registra que a transcrição editável foi aceita pelo fundador
   e que, por isso, a forma "áudio" passa a valer o mesmo que "texto".
   _Alternativa descartada:_ mandar `forma=texto` para a fala transcrita — apagaria do registro
   como a criança produziu, e `RF-05-74` nomeia as três formas.

6. **Uma fala por toque, com "Ouvindo…" enquanto o microfone está aberto.** É o que
   `comum/fala` já faz (`continuous` e `interimResults` desligados) e o que a fatia irmã
   desenhou para a tela do assistente; as duas telas da produção repetem o mesmo padrão, com o
   encerrador chamado em `onend`, em `onerror` e na limpeza do efeito.

7. **`RegistrarMedicao.tsx` passa a consumir `comum/fala`.** A cópia própria da Web Speech API,
   de quando `comum/fala` não existia, sai; o `extrairNumero` fica, porque é do registro de
   coleta e não da transcrição. Mesma `RN-05-32`, nenhum comportamento novo — se a API não
   existe, o ditado segue não sendo oferecido, como hoje.

## Risks / Trade-offs

- **Sala barulhenta derruba a transcrição** → o campo de texto está sempre ao lado e a foto
  também; nenhuma forma fica atrás de uma escolha irreversível. É a mitigação que a §14 do
  PRD-04 já nomeia.
- **Em Chrome o áudio sai do aparelho, para servidor do Google** → sob a conta do navegador,
  não da plataforma; registrado no documento 09 §1 na decisão de 2026-09-10. A tela promete o
  que é verdade em toda parte: a plataforma não recebe o áudio.
- **A transcrição editável rompe a cadeia entre a fala e o texto gravado** → aceito pelo
  fundador na mesma decisão.
- **As produções já gravadas com `forma=audio` vieram de áudio transcrito no núcleo** → o dado
  gravado é o mesmo em forma e em conteúdo (transcrição e devolutiva); nada a migrar, e a
  mudança é de onde a transcrição foi feita, não do que ficou.
- **`SpeechRecognition` não existe em jsdom** → os testes injetam o duplo em `window`, no
  padrão que `comum/fala/fala.test.ts` e os testes da App 05 já usam.

## Migration Plan

Sem migração de banco: `ProducaoDaMissao` nunca teve coluna de foto nem de áudio, e `forma`
não muda de domínio. As duas rotas e suas duas únicas chamadoras mudam no mesmo PR, e não há
consumidor externo. Rollback é reverter o PR.

Uma correção de texto acompanha o código, e não é decisão nova: a linha "Foto e áudio da
produção do Guerreiro(a) — descartados na leitura" do documento 03 §12.2 passa a dizer, do
áudio, que ele **não é recebido**, como o §1.12 do mesmo documento e o `RF-05-76` já dizem.
