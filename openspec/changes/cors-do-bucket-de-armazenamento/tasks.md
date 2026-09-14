## 1. Confirmar o defeito antes de consertar

- [ ] 1.1 Reproduzir em produção o anexo da imagem de uma pergunta do quiz, com a aba de rede
      aberta, e confirmar que o `POST` da sessão responde 201 e que o `PUT` ao armazenamento é
      barrado pelo navegador antes de qualquer byte. Registrar o que a aba mostra no
      `proposal.md`; se a falha for outra, parar a change e corrigir o recorte (`RF-09-119`,
      `RF-09-19`).

## 2. A configuração de CORS do bucket

- [x] 2.1 Criar o arquivo de configuração de CORS do bucket, versionado no repositório,
      autorizando o envio a partir dos endereços das aplicações que enviam bytes — App 09 e
      App 05, no endereço do documento 03 §1 e no `.web.app` em que hoje respondem —, com o
      método do envio e o cabeçalho de posição do protocolo retomável, e expondo o cabeçalho
      que diz de onde retomar (`RF-09-19`, design — decisões 1 e 2).
- [x] 2.2 Acrescentar ao `backend/README.md` §2 a linha que aplica esse arquivo ao bucket, na
      mesma sequência do `create` e do `add-iam-policy-binding`, e a linha que lê de volta o
      que o bucket guarda; verificar que a seção segue legível e que nenhuma outra afirma
      comportamento diferente (`RF-09-19`, design — decisão 1).
- [ ] 2.3 Aplicar a configuração ao bucket de produção, ler de volta o que ele passou a
      guardar e anexar o resultado à change, como a change do bucket fez com o IAM
      (`RF-09-19`, design — decisão 4).

## 3. A origem declarada na abertura da sessão

- [x] 3.1 Fazer `abrir_sessao` do adaptador de nuvem declarar, ao abrir a sessão retomável, a
      origem de quem vai enviar os bytes, recebida de quem pediu a sessão e nunca fixada no
      código; o adaptador de disco não muda (`RF-09-19`, design — decisão 3).
- [x] 3.2 Levar a origem da requisição até a abertura da sessão nas rotas que a abrem — imagem
      da pergunta, arquivo do conteúdo e criação original —, sem mudar o corpo de entrada nem
      a saída de nenhuma delas (`RF-09-119`, `RF-09-19`).
- [x] 3.3 Cobrir em `backend/tests/test_armazenamento_porta.py` que o adaptador de nuvem abre a
      sessão declarando a origem recebida, que a ausência dela não derruba a abertura, e que o
      adaptador de disco segue devolvendo endereço relativo (`RF-09-19`).

## 4. O motivo da recusa no envio de bytes

- [x] 4.1 Fazer `enviarParteComProgresso` em `comum/api/cliente.ts` entregar a recusa que traga
      o corpo de erro único da API como as demais chamadas da camada, e distinguir dela a falha
      sem resposta, que se apresenta como falha de envio (`RF-01-02`, `RF-09-19`, design —
      decisão 5).
- [x] 4.2 Cobrir em `comum/api/cliente.test.ts` os dois desfechos do envio de uma parte: a
      recusa com corpo de erro, que chega com código e mensagem, e a falha sem resposta, que
      não se apresenta como recusa do núcleo (`RF-01-02`, `RF-09-19`).
- [x] 4.3 Conferir que as telas que anexam arquivo — a imagem da pergunta na App 09, o conteúdo
      da missão e a criação original na App 05 — passam a mostrar o motivo que a camada entrega,
      sem mudança própria, e ajustar apenas o que estiver interpretando texto (`RF-09-119`,
      `RF-09-115`).

## 5. Documentação

- [ ] 5.1 Marcar como implementada a linha `—` desta change no bloco PRD-09 do
      `openspec/cronograma-de-fatias.md`, acrescentada com situação `em andamento` na abertura.
      Nada muda em `docs/`, em `docs/prds/index.md` nem no documento 09: a change não toma
      decisão de produto, aplica o que o documento 03 §11 e o `RF-09-119` já decidiram.
