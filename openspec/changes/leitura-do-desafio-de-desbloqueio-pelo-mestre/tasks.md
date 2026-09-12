## 1. Núcleo — o desafio na leitura das trilhas próprias

- [ ] 1.1 `RF-09-26`, `RF-09-118`, `RF-09-119`: em `backend/src/nucleo/trilhas/rotas.py`,
      aninhar o desafio de desbloqueio em `MissaoDoMestreSaida` — tipo, enunciado do prático e,
      no quiz, as perguntas vigentes na ordem, cada uma com identificador, alternativas,
      `alternativa_correta` e `imagem_referencia`. Reaproveitar `_saida_das_perguntas` e
      `PerguntaDoDesbloqueioAoAutorSaida`, de modo que a saída seja intercambiável com a da
      declaração (design — decisões 1 e 2). Missão sem desafio sai sem desafio. Verificar pela
      resposta de `GET /v1/trilhas/minhas` trazendo o quiz declarado.
- [ ] 1.2 `RF-09-118`: ler as perguntas de todas as missões da trilha em uma consulta por
      trilha, com o mesmo filtro de vigência e a mesma ordem de `perguntas_do_desbloqueio`, em
      vez de uma consulta por missão dentro do laço (design — decisão 3). Verificar que a
      leitura de uma trilha com várias missões com quiz não multiplica consultas pelo número de
      missões.

## 2. App 09 — reabrir o desafio declarado

- [ ] 2.1 `RF-09-26`, `RF-09-118`, `RF-09-119`: em `apps/app-09-mestre/src/trilhas/api.ts`,
      passar a receber o desafio pela leitura das trilhas e remover o comentário que descreve a
      ausência como intencional (design — decisão 6). Verificar pelo tipo da missão carregando
      as perguntas com identificador e referência da imagem.
- [ ] 2.2 `RF-09-26`, `RF-09-118`: em `DesafioDeDesbloqueio.tsx`, o formulário nasce do que a
      leitura trouxe — tipo, enunciado, perguntas com a alternativa correta marcada e o
      identificador que endereça a imagem —, e o aviso de "ainda não tem desafio" só aparece em
      missão que de fato não tem. Verificar que, com a missão vinda da leitura, a tela abre
      preenchida e anexar imagem a pergunta antiga não pede gravação prévia.
- [ ] 2.3 `RF-09-118`: em `ListaDeMissoes.tsx`, o resumo da linha passa a refletir o desafio que
      a leitura trouxe, em vez de dizer que a missão está sem desafio. Verificar pelo resumo de
      uma missão com quiz de três perguntas carregada da lista.

## 3. App 09 — a imagem visível ao Mestre autor

- [ ] 3.1 `RF-09-119`: exibir a imagem da pergunta em `DesafioDeDesbloqueio.tsx` pelo padrão da
      App 05 — busca dos bytes pela função cliente `lerImagemDaPergunta`, endereço local
      revogado na saída, e aviso sem travar quando não carregar (design — decisão 4). Verificar
      que a pergunta com imagem a exibe e que a falha de carregamento não impede corrigir nem
      gravar.

## 4. App 09 — a sondagem pelo nome

- [ ] 4.1 `RF-09-81`, `RN-09-30`, `RN-05-46`: quando a missão é sondagem, `ListaDeMissoes.tsx`
      e `DesafioDeDesbloqueio.tsx` usam o rótulo "Sondagem", a abertura "Essa sondagem abre a
      trilha e mostra a você de onde a turma parte.", o lugar do corte "Aqui não tem passar nem
      reprovar: a trilha abre assim que o Guerreiro(a) responde.", o aviso "Esta sondagem ainda
      não tem perguntas." e os resumos "Sondagem ainda sem perguntas." e "Sondagem com N
      pergunta(s)."; a escolha entre quiz e prático não é oferecida, e o tipo declarado é
      sempre quiz (design — decisão 5). Verificar que o corte de 60% não aparece em missão de
      sondagem e continua aparecendo nas demais.

## 5. Testes

- [ ] 5.1 `backend/tests/test_trilha_rota.py`: a leitura das trilhas próprias devolve o quiz com
      a alternativa correta e a referência da imagem, devolve o enunciado do prático, não
      devolve pergunta substituída e distingue missão sem desafio de quiz sem pergunta — os
      cenários de `trilha-e-missao` no delta. Cobrir também que a alternativa correta não sai
      pelas leituras que alcançam o Guerreiro(a) (`RF-09-118`, `RF-09-119`).
- [ ] 5.2 `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`: a tela reabre o quiz e o prático
      declarados, o resumo da linha reflete o que existe, a imagem é exibida e a que não
      carrega não trava a edição, e a sondagem usa os textos próprios sem o corte de 60% e sem
      a escolha de tipo — os cenários de `area-do-mestre` no delta (`RF-09-26`, `RF-09-118`,
      `RF-09-119`, `RF-09-81`, `RN-09-30`).

## 6. Documentação

- [ ] 6.1 Marcar a linha desta change como `implementado` em
      `openspec/cronograma-de-fatias.md`, com o slug, e registrar em
      `docs/09-topicos-em-aberto-e-sugestoes.md` §1 a pendência da sondagem publicável sem
      nenhuma pergunta (`RF-09-82` confere só a existência da missão). Nenhum PRD muda —
      a change aplica requisitos que já existem —, nenhuma relação entre documentos muda e
      nenhum arquivo novo entra em `docs/`, de modo que o documento 99, `docs/prds/index.md` e a
      `nav` do `mkdocs.yml` seguem como estão.
