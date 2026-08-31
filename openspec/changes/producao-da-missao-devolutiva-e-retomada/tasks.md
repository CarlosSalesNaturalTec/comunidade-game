## 1. Núcleo — a entrega individual da produção

- [ ] 1.1 Em `producoes/regra.py`, extrair da `registrar_producao` o trecho comum às duas
      portas — conferência da forma única, chamada ao adaptador, desfecho da leitura
      indisponível e montagem do registro (design — decisão 1) — sem alterar comportamento
      algum da porta de equipe: `uv run pytest tests/test_producao_da_missao.py -x` segue verde
      sem edição.
- [ ] 1.2 Escrever `registrar_producao_individual` sobre esse trecho comum (`RF-05-74`,
      `RN-05-35`): recusa quem não é Guerreiro(a), exige trilha inscrita e missão desbloqueada
      pelo próprio, via `derivar_percurso` (design — decisão 3), e confere que a atividade
      declarada pertence à missão (design — decisão 2). Grava com `guerreiro_id` preenchido e
      `equipe_id` em branco (`RN-05-21`).
- [ ] 1.3 Expor `POST /v1/eu/missoes/{id}/producao` em `producoes/rotas.py`, com a mesma
      superfície `multipart/form-data` da porta de equipe e o mesmo `PortaDaProducaoDaMissao`
      injetado (design — decisão 6): 201 com transcrição e devolutiva, 403 para Mestre e Admin,
      422 nas recusas de 1.2 e 503 na leitura indisponível de áudio ou foto (`RF-05-74` a
      `RF-05-77`).

## 2. Núcleo — as retomadas em aberto

- [ ] 2.1 Em `trilhas/regra.py`, derivar as retomadas em aberto do Guerreiro(a) a partir da
      `cadencia_de_retomada` da missão e do momento do desbloqueio aprovado dele, fechando o
      agendamento pela produção individual com `registrado_em >= prazo` (design — decisão 4):
      atende `RF-05-79`, `RF-05-80` e `RN-05-38`, e ignora missão sem cadência, não desbloqueada
      ou com desbloqueio prático ainda não julgado.
- [ ] 2.2 Expor `GET /v1/eu/retomadas` em `trilhas/rotas.py` (design — decisão 5): missão,
      trilha e prazo de cada agendamento em aberto do Guerreiro(a) em sessão, lista vazia sem
      erro, 403 para quem não é Guerreiro(a) e nenhuma retomada de terceiro (`RF-05-79`,
      `RN-05-21`).

## 3. Testes do núcleo

- [ ] 3.1 Em `tests/test_producao_da_missao.py`, os cenários da regra individual: entrega por
      texto, áudio e foto; recusa sem forma e com duas formas; atividade de outra missão,
      trilha não inscrita e missão não desbloqueada; registro com Guerreiro(a) e equipe em
      branco; produção individual que não alcança colega (`RF-05-74`, `RN-05-21`, `RN-05-35`).
- [ ] 3.2 Ainda em `tests/test_producao_da_missao.py`, os cenários do contrato compartilhado
      aplicados à porta individual: mídia descartada e ausente de resposta e de log
      (`RF-05-76`, `RN-05-36`); devolutiva construtiva que não credita ponto, `Resultado` nem
      percurso (`RF-05-75`, `RF-05-77`, `RN-05-05`); 201 com devolutiva em branco no texto e
      503 sem gravar em áudio e foto; resposta sem custo nem cota. E os cenários de `RF-05-78`
      e `RN-05-37`: só texto basta, e missão sem produção segue desbloqueada no percurso.
- [ ] 3.3 Em `tests/test_producao_da_missao_porta.py`, os cenários HTTP da rota nova: 201 do
      Guerreiro(a) em sessão, 403 de Mestre e de Admin, recusa sem persona em sessão e a porta
      de equipe intacta (`RF-05-74`, `RF-01-16`).
- [ ] 3.4 Em `tests/test_retomadas.py` (novo), os cenários da retomada: cadência virando
      agendamentos contados do desbloqueio de cada um; só o agendamento vencido em aberto;
      missão sem cadência, não desbloqueada e com prático não julgado sem retomada; produção
      fechando o agendamento vencido; segunda entrega que não reabre nem duplica; refazer antes
      do prazo que não consome agendamento; o agendamento seguinte vencendo normalmente;
      fechamento sem crédito de ponto; e os cenários HTTP — lista vazia sem erro, 403 e nenhuma
      retomada de terceiro (`RF-05-79`, `RF-05-80`, `RN-05-38`, `RN-05-05`, `RN-05-21`).

## 4. App 05 — Área do Guerreiro(a)

- [ ] 4.1 Em `src/api/trilha.ts`, os dois clientes: a entrega individual em
      `multipart/form-data` e a leitura das retomadas, com os erros 422 e 503 tratados em
      mensagem para a criança.
- [ ] 4.2 `EntregaDaProducao` dentro de `trilha/Missao.tsx` (design — decisão 7): as três formas
      lado a lado, sem padrão obrigatório (`RF-05-74`); o aviso do descarte antes de enviar
      áudio ou foto e nenhuma mídia retida no aparelho depois do envio (`RF-05-76`,
      `RN-05-36`); e o caminho "entrego ao Mestre no encontro" com o mesmo destaque, dizendo
      que ninguém perde a missão (`RF-05-78`, `RN-05-37`).
- [ ] 4.3 Ainda em `EntregaDaProducao`, a devolutiva como próximo passo, com o aviso, na mesma
      altura, de que ela não vale ponto e de que o resultado aguarda o lançamento do Mestre; e a
      confirmação de que a produção foi guardada quando a devolutiva não vem (`RF-05-75`,
      `RF-05-77`, `RN-05-05`).
- [ ] 4.4 `Retomadas` como tela do bloco Trilha (design — decisão 7): missão, trilha e prazo de
      cada retomada, a explicação de que rever fixa, o aviso próprio quando não há nenhuma, a
      retomada entregue saindo da lista e o texto de que refazer por conta própria não rende
      ponto novo, sem palavra de atraso, dívida ou punição (`RF-05-79`, `RF-05-80`,
      `RN-05-38`).
- [ ] 4.5 Testes de `EntregaDaProducao.test.tsx` e `Retomadas.test.tsx` cobrindo os cenários de
      4.2 a 4.4, e o critério de aceite do PRD-05 §12 que a fatia toca: nenhuma tela exibe ponto
      como consequência da entrega, e missão desbloqueada sem produção não é marcada como
      pendência nem tem o conteúdo escondido.

## 5. Documentação

- [ ] 5.1 Marcar a fatia 7 do PRD-05 como implementada em `openspec/cronograma-de-fatias.md`,
      com o slug da change. Nenhuma decisão nova nasceu aqui — as duas do fundador são de
      recorte e ficam no `proposal.md` —, então documento-fonte, documento 09, PRD-05,
      `docs/prds/index.md`, documento 99 e a `nav` do `mkdocs.yml` seguem como estão.
