PRD-04 (App 01 — Aula presencial), **correção de bug preexistente**, não fatia de requisito
novo — molde da change `2026-09-17-correcao-de-aulas-canceladas-e-modelos-de-biometria`. Entra
no `openspec/cronograma-de-fatias.md` como linha sem número, no bloco do PRD-04.

Traz junto **uma decisão nova do fundador** (2026-09-17), que nasce nos documentos-fonte e só
então chega aqui: nascem `RF-04-64`, `RF-04-65` e `RN-04-34`. Alcança também `RF-04-13`,
`RF-04-14`, `RF-04-18`, `RF-04-20` e `RF-04-63`, que já existem e cujo comportamento de tela
muda.

## Why

O reconhecimento facial **nunca funcionou em produção**, e a aplicação anuncia a falha como se
fosse a criança: a tela diz "não foi possível confirmar que há uma pessoa diante da câmera"
quando a verdade é que a biblioteca não tem modelo carregado.

Confirmado no aparelho, em 2026-09-17, com DevTools sem filtro e cache desativado: **22
requisições, nenhuma para `/modelos-de-biometria/`**, com os modelos comprovadamente
publicados. A Human autosseleciona o backend `webgpu` porque `navigator.gpu` existe, mas o
`requestAdapter()` daquele aparelho devolve `null`, o tfjs estoura em `Cannot read properties
of null (reading 'features')` e o `human.load()` **nunca chega a buscar modelo**. Sem modelo,
`detect()` não encontra rosto, e a prova de vivacidade reprova.

É a **terceira vez** que este mesmo caminho falha em silêncio — o cronograma registra as duas
anteriores, o 422 de dimensão do descritor lido como falta de consentimento por um mês e o CORS
do bucket trocado por frase genérica. Não é azar: toda falha deste caminho desagua na mesma
frase. Enquanto isso durar, a tarefa 4.1 da change `2026-09-17-bancada-de-calibracao-do-limiar`
não anda, e o limiar segue em `0.5` sem nunca ter sido medido.

Há um segundo defeito, independente: `comum/biometria` cria o elemento de vídeo e **nunca o
anexa ao DOM**. Nenhuma das três telas de câmera mostra coisa alguma — quem opera captura às
cegas, sem saber se há rosto enquadrado, e a detecção é de tiro único no instante do clique.

## What Changes

- **O backend da Human passa a ser declarado** como `webgl` em `comum/biometria`, em vez de
  autosselecionado. É onde o `load()` morre, e o conserto alcança as quatro telas de câmera do
  repositório pelo módulo compartilhado.
- **Falha de preparo deixa de ser muda**: o que impediu a captura de acontecer NEVER SHALL sair
  pela frase da vivacidade reprovada. Os dois desfechos passam a ser distinguíveis na tela
  (`RF-04-65`); `RF-04-20` segue valendo para a recusa do núcleo, que continua indistinguível.
- **As três telas de câmera do App 01 ganham o espelho ao vivo** — entrada do Guerreiro(a),
  captura do onboarding e bancada de medição — com **retorno abstrato** de que há rosto e de que
  a vivacidade passou, e **detecção em laço** até aprovar ou estourar tempo, no lugar do tiro
  único (`RF-04-64`).
- **O quadro congelado fica proibido** em qualquer das telas, antes ou depois de gerar o
  descritor (`RN-04-34`).
- A decisão nova entra nos documentos-fonte: documento 03 §3.3, invariante 12 do documento 99
  §6 — que passa a distinguir **visor ao vivo** de **imagem capturada** —, documento 09 §1 e o
  PRD-04.

Fica **fora**: o espelho na entrada do Guerreiro(a) do **App 05**, que é recorte do PRD-05
(decisão do fundador, 2026-09-17). O App 05 recebe o conserto do backend pelo módulo
compartilhado, e a tela dele entra numa change do PRD-05. Fica fora também a troca do secret
`cg-biometria-limiar-de-comparacao`, que segue como a tarefa em aberto da change da bancada —
esta change a **destrava**, não a executa.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: três Requirements existentes passam a declarar o visor ao
  vivo e o retorno abstrato, e a proibição de exibir imagem passa a alcançar o **quadro
  capturado**, não o visor — "O Guerreiro(a) entra por nick e imagem, e a presença é registrada
  na entrada", "O descritor nasce no aparelho, depois da prova de vivacidade" e "O Mestre mede
  no aparelho a distância entre descritores". Nasce um Requirement para a falha de carga de
  modelo, que hoje se disfarça de vivacidade reprovada.

O `template-biometrico` **não muda**: nada do que esta change toca chega ao núcleo — nem o
backend da biblioteca, nem o visor, nem a mensagem de falha.

## Impact

- `comum/biometria/`: o backend declarado, a função que acopla o espelho ao elemento que a tela
  fornece, o laço de detecção e a falha de carga distinguível. É o módulo compartilhado, então o
  conserto do backend alcança também o App 05 sem que a tela dele mude.
- `apps/app-01-aula-presencial/`: as três telas de câmera e os testes delas.
- `docs/`: documento 03 §3.3, documento 99 §6 (invariante 12), documento 09 §1 e o PRD-04, com
  `RF-04-64`, `RF-04-65` e `RN-04-34`.
- **Sem backend**: nenhuma rota, nenhum contrato de API, nenhuma migração.
- **Destrava** a tarefa 4.1 da change `2026-09-17-bancada-de-calibracao-do-limiar`: sem captura
  que funcione no aparelho, não há o que medir.

Achado **fora do escopo**, registrado para não se perder: no `firebase.json`, o alvo `aula` não
tem `rewrites` — só o alvo `app-03` tem —, então URL profunda no App 01 responde 404.
