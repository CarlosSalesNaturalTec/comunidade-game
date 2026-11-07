# Tasks

## 1. Registro da decisão (antes do código)

- [ ] 1.1 Documento 09 §1: linha nova em "Já decididos" — **Sondagem respondida por voz**
      (decisão do fundador, 2026-11-07): só a sondagem, com o áudio ligado, janela de 5 s,
      ligação à alternativa aproximada e transcrição literal sem alternativa; ligar o áudio pede
      o microfone; transcrição pela Web Speech API, no Chrome nos serviços do Google. Linha nova
      em "Decisões pendentes" com `> **A definir:**` o prazo de guarda da transcrição da sondagem.
      (`RF-05-97`, `RF-05-98`, `RN-05-54`, `RN-05-55`, `RF-04-77`)
- [ ] 1.2 Documento 03: em §1.12, uma frase precisando que no Chrome a transcrição é feita nos
      serviços do Google e que o áudio não chega ao núcleo; em §4, a exceção da janela da
      sondagem em "A aplicação não escuta a aula". (`RN-05-54`)
- [ ] 1.3 PRD-05: `RF-05-97`, `RF-05-98`, `RN-05-54`, `RN-05-55` nas tabelas, critério de aceite
      e rastreabilidade; PRD-04: `RF-04-77` e a exceção no requisito do microfone; documento 99
      §8 se a relação entre PRDs mudar. (`RF-05-97`, `RF-05-98`, `RN-05-54`, `RN-05-55`,
      `RF-04-77`)
- [ ] 1.4 `openspec/cronograma-de-fatias.md`: linha da fatia 15 do PRD-05, "Sondagem respondida
      por voz", com o slug e o recorte, situação `em andamento`.

## 2. Núcleo

- [ ] 2.1 `backend/src/nucleo/trilhas/modelo.py` e migração Alembic nova:
      `alternativa_escolhida` nulável, `resposta_falada` (`Text`, nulável) e o `CHECK` de forma
      única; `downgrade` reversível. (`RF-05-98`, `RN-05-55`, `RN-05-47`)
- [ ] 2.2 `rotas.py` e `regra.py`: `RespostaDoDesbloqueioEntrada` com `alternativa_escolhida`
      opcional e `resposta_falada` (máx. 500); validação de forma única e de sondagem; gravação
      com `acertou = False` sem alternativa; OpenAPI atualizado. (`RF-05-98`, `RN-05-55`,
      `RN-05-46`)
- [ ] 2.3 `backend/tests/test_desbloqueio_da_missao.py`: sondagem com resposta falada aceita e
      trilha aberta; silêncio grava vazio; desbloqueio comum sem alternativa é 422; alternativa e
      transcrição juntas é 422; transcrição acima do limite é 422. (`RF-05-98`, `RN-05-55`)

## 3. Camada comum

- [ ] 3.1 `comum/narracao/`: `falar` e `narrar` com `aoTerminar` por identidade do enunciado,
      nunca em cancelamento nem sem voz; `alternarNarracao` pede o microfone ao ligar e expõe
      `microfonePermitido`. Testes em `narracao.test.ts` e `ProvedorDeNarracao.test.tsx`: fim
      avisado, cancelamento sem aviso, sem voz sem aviso, permissão pedida e faixas paradas,
      negada sem alarme. (`RF-05-97`, `RN-05-54`)
- [ ] 3.2 `comum/fala/`: `escutarPorJanela` com prazo, parcial e encerramento único; teste em
      `fala.test.ts` com reconhecimento falso: parcial repassado, `stop` no prazo, texto
      acumulado, silêncio vazio, encerrador idempotente. (`RF-05-97`, `RN-05-54`)
- [ ] 3.3 `comum/trilha/ligarFalaAAlternativa.ts` e teste: texto aproximado, sem acento, letra,
      número, ordinal, empate e fala sem correspondência devolvendo `null`. (`RF-05-98`)
- [ ] 3.4 `comum/trilha/JanelaDeEscuta.tsx`: barra de 5 s com rótulo acessível e transcrição
      parcial em `aria-live`. (`RF-05-97`)
- [ ] 3.5 `comum/trilha/api.ts`, `DesafioDeDesbloqueio.tsx` e `Sondagem.tsx`: `respostaPorVoz`
      só na sondagem; janela aberta no fim da fala; toque encerra a janela e vale; ao fim marca
      e avança, e na última submete; resposta sem alternativa vai como `resposta_falada`.
      (`RF-05-97`, `RF-05-98`, `RN-05-54`)
- [ ] 3.6 `comum/trilha/trilha.test.tsx`: fala → janela → transcrição à vista → avanço; última
      submete sozinha; silêncio e fala sem correspondência vão literais; toque durante a janela
      vence; áudio desligado, sem transcrição ou microfone negado seguem por toque; desafio de
      desbloqueio não abre a janela. (`RF-05-97`, `RF-05-98`, `RN-05-54`)

## 4. Aplicações

- [ ] 4.1 `apps/app-05-guerreiro/src/trilha/Sondagem.test.tsx`: sondagem com o áudio ligado fala,
      escuta e avança; desligado, nada muda. (`RF-05-97`, `RF-05-72`)
- [ ] 4.2 `apps/app-01-aula-presencial/src/trilhas/trilhas.test.tsx`: o mesmo no aparelho do
      encontro, e o microfone fechado fora da janela. (`RF-04-77`, `RF-04-73`)

## 5. Documentação

- [ ] 5.1 Marcar a fatia 15 do PRD-05 como `implementado` no cronograma. `docs/prds/index.md` não
      muda (a situação do PRD-05 segue a mesma); `mkdocs.yml` não muda (nenhum arquivo novo em
      `docs/`).
