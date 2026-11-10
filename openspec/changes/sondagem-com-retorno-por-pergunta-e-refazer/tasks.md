# Tasks

## 1. Documentação da decisão

- [ ] 1.1 Registrar a decisão do fundador de 2026-11-10 no documento 09 §1, em "Já decididos":
      retorno por pergunta de 2 s, tela final com Refazer e Concluir, refazer quando quiser,
      vale a última tentativa sem ponto, gabarito da sondagem na leitura do percurso, Apps 01
      e 05 juntas (`RF-05-99` a `RF-05-101`, `RN-05-56`, `RN-05-57`, `RF-04-78`). Verificar
      pela linha nova na tabela.
- [ ] 1.2 Documento 11 §2.2, regra "Sondagem antes de ensinar": uma frase — a sondagem pode ser
      refeita quando o Guerreiro(a) quiser, e vale a tentativa mais recente. Verificar que o
      §5 segue dizendo que ela não credita nem define nível.
- [ ] 1.3 PRD-05: `RF-05-99`, `RF-05-100`, `RF-05-101` na tabela de requisitos, `RN-05-56` e
      `RN-05-57` na de regras, e as linhas de rastreabilidade; PRD-04: `RF-04-78`, com a
      rastreabilidade. Verificar que nenhum identificador repete número já usado.
- [ ] 1.4 `openspec/cronograma-de-fatias.md`: linha da fatia 17 do PRD-05, "Sondagem com
      retorno por pergunta e refazer", com o recorte e a situação `em aberto`. Verificar que a
      numeração do bloco segue contínua.

## 2. Núcleo

- [ ] 2.1 `regra.py`: extrair a aferição do quiz para função auxiliar e, quando o desbloqueio
      da sondagem já existe, gravar a submissão nova e devolver `aprovado=True`, `acertos` e
      `total`, sem segundo desbloqueio (`RF-05-101`, `RN-05-56`, `RN-05-47`). Verificar com
      2.3.
- [ ] 2.2 `rotas.py`: `alternativa_correta` opcional em `PerguntaDoDesbloqueioSaida`, preenchida
      em `GET /v1/eu/trilhas/{id}/missoes/{ordem}` só quando a missão é sondagem (`RN-05-57`).
      Verificar com 2.3.
- [ ] 2.3 Testes em `tests/test_desbloqueio_da_missao.py` e `tests/test_percurso_da_trilha.py`:
      refazer grava tentativa nova e devolve o placar; as anteriores seguem; um desbloqueio só;
      saldo e nível intactos; a mais recente é a última por instante; quiz comum já cumprido
      responde como antes; a pergunta da sondagem traz a correta e a do desafio não.

## 3. Camada comum

- [ ] 3.1 `comum/react/Icone.tsx`: glifos `acerto` e `erro`, com teste em `Icone.test.tsx` de
      que são formas distintas (`RF-05-99`).
- [ ] 3.2 `comum/trilha/api.ts`: `alternativa_correta?: number | null` em
      `PerguntaDoDesbloqueio`, com o comentário do gabarito atualizado (`RN-05-57`).
- [ ] 3.3 `comum/trilha/DesafioDeDesbloqueio.tsx`: `respostaPorVoz` vira `ehSondagem`; na
      sondagem, pergunta da vez sem paginador, retorno de 2 s com alternativas travadas,
      avanço e submissão sozinhos, temporizador limpo ao desmontar, tela final com acertos e
      erros do núcleo, Refazer, Concluir e "Tentar de novo" na falha; o fim da janela de voz
      entra no mesmo retorno (`RF-05-99`, `RF-05-100`, `RF-05-97`, `RN-05-55`). Verificar com
      3.6.
- [ ] 3.4 `comum/trilha/Sondagem.tsx` e `estilos.css`: passa `ehSondagem`, liga Concluir a
      `aoResponder`; estilo do símbolo grande e centralizado com as cores de sucesso e erro.
- [ ] 3.5 `comum/trilha/GuiaDaTrilha.tsx`: localizar a sondagem na trilha publicada, oferecer
      **Refazer a sondagem** no rodapé quando respondida e com submissão ligada, apresentá-la
      no grupo 1 e voltar ao percurso no Concluir (`RF-05-101`). Verificar com 3.6.
- [ ] 3.6 Testes em `comum/trilha/trilha.test.tsx` e `sondagemPorVoz.test.tsx`, com relógio
      falso: símbolo verde e vermelho por 2 s e avanço; alternativas travadas; sem voltar nem
      enviar; tela final com o total; Refazer recomeça; Concluir recarrega; falada sem
      alternativa é erro; abandono não submete; rodapé oferece refazer só com a sondagem
      respondida; janela de voz passa pelo retorno antes de avançar e de submeter.

## 4. Aplicações

- [ ] 4.1 Apps 01 e 05: conferir que as duas recebem o fluxo pela camada comum, sem código
      próprio, e ajustar teste de tela que dependia do "Enviar respostas" ou do voltar na
      sondagem (`RF-04-78`). Verificar pelos testes de cada aplicação.

## 5. Fechamento

- [ ] 5.1 Marcar a fatia 17 do PRD-05 como `implementado` no cronograma, com o slug arquivado.
      `docs/prds/index.md` não muda (o PRD-05 segue `implementado`); `mkdocs.yml` e o
      documento 99 não mudam (nenhum arquivo novo, nenhuma relação nova entre documentos).
