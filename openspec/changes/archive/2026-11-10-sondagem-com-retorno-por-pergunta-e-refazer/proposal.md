# Proposal

**PRD de origem:** PRD-05 (Área do Guerreiro(a)), com o alcance no PRD-04 (App 01). **Fatia:**
17 do PRD-05 no `openspec/cronograma-de-fatias.md`, criada nesta change. **Identificadores:**
`RF-05-99`, `RF-05-100`, `RF-05-101`, `RN-05-56`, `RN-05-57` e `RF-04-78` (**novos**, criados
nesta change), alcançando `RF-05-72`, `RF-05-73`, `RF-05-97`, `RN-05-34`, `RN-05-46`,
`RN-05-47`, `RN-05-55`, `RF-04-73` e `RF-04-77`.

Decisão do fundador de 2026-11-10, elicitada em `/opsx:propose`, em quatro partes:

1. **Pontuação é o resultado, sem ponto.** O que se atualiza a cada realização é o placar da
   sondagem (acertos e total). Toda tentativa segue gravada; o resultado que **vale** é o da
   mais recente. Nenhum ponto é creditado e nada define nível — o documento 11 §5 não muda.
2. **O gabarito vai na leitura, só da sondagem.** A leitura da missão no percurso passa a
   trazer a alternativa correta de cada pergunta **da sondagem**, e a tela confere sozinha. O
   fundador aceitou que a criança possa ver o gabarito pelo navegador: a sondagem não tranca
   nada. No desafio de desbloqueio a alternativa correta segue só no núcleo.
3. **Apps 01 e 05 juntas**, pelo precedente das fatias 22, 27, 28 e 29 do PRD-04: a tela é
   `comum/trilha`.
4. **Refazer quando quiser.** A sondagem já respondida continua alcançável no percurso e se
   refaz a qualquer tempo, sem limite.

## Why

Hoje a sondagem é um quiz mudo: a criança marca as respostas, envia tudo de uma vez e a trilha
abre, sem saber o que acertou. Ela também não volta — depois de respondida, nenhuma tela a
reapresenta, e o núcleo nem gravaria a nova tentativa, porque devolve a situação do
desbloqueio já existente sem registrar nada. Retorno imediato por pergunta e a chance de
refazer tornam a sondagem uma experiência de aprender, e a última tentativa passa a ser a
medida de partida que o Mestre lê.

## What Changes

- **Retorno por pergunta** (`RF-05-99`): respondida uma pergunta — por toque ou pela janela de
  voz do `RF-05-97` —, a tela mostra por **2 segundos** um símbolo **verde de acerto** ou
  **vermelho de erro**, com forma distinta e texto acessível — **falado** com a narração
  ligada —, e avança sozinha para a seguinte.
  A resposta dada não se troca: some o "Pergunta anterior" e o "Enviar respostas" da sondagem.
- **Tela final** (`RF-05-100`): depois da última pergunta a sondagem é submetida sem toque, e a
  tela mostra o **total de acertos e de erros**, segundo o núcleo, com os botões **Refazer** e
  **Concluir**. Refazer recomeça da primeira pergunta; Concluir segue o percurso — é ali, e não
  no envio, que a trilha recarrega.
- **Refazer quando quiser** (`RF-05-101`): com a sondagem respondida, o rodapé da trilha
  oferece **Refazer a sondagem**, que a reapresenta com o mesmo retorno e a mesma tela final.
- **Toda realização é gravada, e vale a última** (`RN-05-56`): o núcleo passa a gravar a
  submissão da sondagem **já respondida** como tentativa nova e devolve o placar dela, sem
  criar segundo desbloqueio, sem crédito e sem nível. Sondagem largada no meio não grava nada e
  recomeça da primeira pergunta.
- **Gabarito só na sondagem** (`RN-05-57`): `GET /v1/eu/trilhas/{id}/missoes/{ordem}` passa a
  trazer `alternativa_correta` em cada pergunta **quando a missão é a sondagem**; nas demais,
  segue ausente.
- **Mesma tela no encontro** (`RF-04-78`): a App 01 recebe tudo isso por `comum/trilha`.
- Dois glifos novos no `Icone` comum — **acerto** e **erro** —, com as cores de sucesso e erro
  dos tokens.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `desbloqueio-da-missao`: a sondagem respondida aceita submissão nova, grava a tentativa e
  devolve o placar, valendo a mais recente; a exceção do gabarito da sondagem entra no
  requisito da imagem da pergunta, que hoje diz que a alternativa correta fica fora de toda
  saída ao Guerreiro(a).
- `trilha-e-missao`: o requisito da leitura do Mestre autor deixa de dizer que a alternativa
  correta nunca alcança o Guerreiro(a), passando a ressalvar a sondagem.
- `area-do-guerreiro`: a sondagem da App 05 ganha o retorno por pergunta, a tela final com
  Refazer e Concluir e o refazer pelo rodapé; o requisito que proibia exibir acerto e erro
  passa a admiti-los como retorno, nunca como nota.
- `aplicacao-da-aula-presencial`: a App 01 apresenta a mesma sondagem (`RF-04-78`).
- `sondagem-por-voz`: o fim da janela passa pelo retorno de 2 segundos antes de avançar, e a
  última resposta leva à tela final.

## Impact

- **Núcleo:** `backend/src/nucleo/trilhas/regra.py` (submissão da sondagem já respondida) e
  `rotas.py` (alternativa correta na pergunta da sondagem, no percurso). Sem migração: a
  `SubmissaoDoDesbloqueio` já guarda o instante de cada tentativa.
- **Camada comum:** `comum/trilha` (`Sondagem`, `DesafioDeDesbloqueio`, `GuiaDaTrilha`,
  `api.ts`, `estilos.css`) e `comum/react/Icone.tsx`.
- **Aplicações:** Apps 01 e 05, sem código próprio novo — recebem pela camada comum.
- **Documentação:** documento 09 §1 (decisão nova), documento 11 §2.2 (uma frase na regra da
  sondagem), PRD-05 e PRD-04 (identificadores novos e rastreabilidade) e o cronograma.
- **Fora do escopo:** a leitura do resultado da sondagem pelo Mestre e a medida de fim de ciclo
  do documento 10, que não existem hoje e não nascem aqui; o desafio de desbloqueio e o Quiz ao
  Vivo, que não mudam; o PRD-05 §3.2 segue valendo.
