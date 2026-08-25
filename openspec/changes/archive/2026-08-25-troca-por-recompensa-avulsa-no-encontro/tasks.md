## 1. Núcleo — o saldo disponível ganha quem o leia

- [x] 1.1 `ponto_extra/rotas.py` (novo): `GET /v1/eu/pontos-extras`, sob `exigir_persona`,
      devolvendo `acumulado` e `saldo_disponivel` da persona da sessão; papel diferente de
      Guerreiro(a) recebe 403, e Guerreiro(a) sem linha em `ponto_extra` recebe as duas contas em
      zero. Sem identificador de persona no caminho (`RF-04-51`, `RF-05-82`, `RN-01-41`, design —
      decisão 1). Verificação: 200 com as duas contas para o Guerreiro(a), 403 para Mestre e para
      Admin, e zero para quem nunca recebeu ponto extra.
- [x] 1.2 Registrar o roteador em `principal.py`, no mesmo padrão dos demais módulos
      (`RF-04-51`). Verificação: a rota aparece no OpenAPI e responde sob `/v1`.

## 2. App 01 — os clientes das três rotas

- [x] 2.1 `api/pontosExtras.ts` (novo): cliente de `GET /v1/eu/pontos-extras`, sempre com o
      **token do Guerreiro(a)** (`RF-04-51`, design — decisão 4). Verificação: o teste da tela
      mostra que o token de trabalho nunca é o usado nesta chamada.
- [x] 2.2 `api/catalogoAvulso.ts` (novo): cliente de `GET /v1/catalogo-avulso`, sem declarar
      comunidade, usado com o token de trabalho na sondagem da abertura e com o token do
      Guerreiro(a) na leitura que a tela exibe (`RF-04-50`, design — decisões 3 e 4).
      Verificação: os dois usos aparecem nos testes, e nenhum envia `comunidade_virtual_id`.
- [x] 2.3 `api/trocas.ts` (novo): cliente de `POST /v1/aulas/{id}/trocas`, com o **token de
      trabalho** e `guerreiro_id` recebido de quem chama (`RF-04-52`, `RF-04-55`, design —
      decisão 4). Verificação: o teste mostra que o token do Guerreiro(a) nunca assina esta
      escrita.

## 3. App 01 — o momento de troca

- [x] 3.1 `AparelhoDaAula.tsx`: estado do momento de troca, em memória e nascendo fechado, com a
      abertura oferecida **só quando a sessão de trabalho é de Mestre**; o Admin não recebe o
      controle (`RF-04-49`, decisão do fundador de 2026-08-25, design — decisão 2). Verificação:
      com sessão de trabalho de Admin nenhum controle de abertura aparece; com Mestre, aparece.
- [x] 3.2 A abertura faz a sondagem do catálogo e só abre com resposta do núcleo; falha de rede
      mantém o momento fechado, com o aviso de que a troca exige rede (`RF-04-57`, design —
      decisão 3). Verificação: `fetch` que rejeita deixa o momento fechado e mostra o aviso.
- [x] 3.3 `TelaInicial.tsx`: terceiro caminho, visível apenas com o momento aberto, levando à
      entrada por nick e imagem quando não há sessão de Guerreiro(a) — o mesmo caminho das
      trilhas, sem tela de cadastro (`RF-04-01`, `RF-04-49`). Verificação: fechado o momento, o
      caminho não aparece em tela alguma.

## 4. App 01 — a tela da troca

- [x] 4.1 `troca/TelaDeTroca.tsx` (novo): lê o catálogo e o saldo sob o token do Guerreiro(a) e
      exibe os itens com preço em pontos extras e estoque restante, e o **saldo disponível** —
      nunca o acumulado, nunca ponto regular, nunca reais ou moedas (`RF-04-50`, `RF-04-51`,
      `RF-04-56`, `RN-04-23`, `RN-04-28`). Verificação: a tela não contém o acumulado nem
      qualquer valor em reais ou moedas.
- [x] 4.2 A mesma tela oculta o item de **estoque zero** e recusa, antes de enviar, o item cujo
      preço supera o saldo, dizendo a diferença em pontos (`RF-04-54`, `RF-04-53`, `RN-04-25`,
      design — decisão 5). Verificação: item zerado não aparece; item caro mostra a diferença e
      não emite requisição.
- [x] 4.3 A confirmação da entrega pelo Mestre envia a troca num único `POST`, com o
      `guerreiro_id` vindo de `sessaoDoGuerreiro.persona_id`, e ao fim volta à tela inicial
      (`RF-04-52`, `RF-04-55`, `RF-04-28`, `RN-04-27`). Verificação: um envio por troca, nenhum
      nick consultado, e a tela seguinte sem dado do atendimento.
- [x] 4.4 O 422 do núcleo — saldo, estoque ou lastro mudados depois da leitura — é apresentado em
      linguagem simples, com a escolha de outro item sem repetir a entrada (`RF-04-53`,
      `RF-07-37`). Verificação: a recusa do núcleo mantém a sessão do Guerreiro(a) aberta.

## 5. Testes

- [x] 5.1 `tests/` do núcleo, ponto extra: os cenários da spec de `ponto-extra` — as duas contas
      do próprio Guerreiro(a), zero para quem nunca recebeu, 403 de Mestre e de Admin, e o
      contrato de leitura dos jogos seguindo sem o saldo (`RF-04-51`, `RF-05-82`, `RN-01-41`).
- [x] 5.2 `troca.test.tsx` da App 01: os cenários da spec de `aplicacao-da-aula-presencial` para
      o momento de troca — abertura só por Mestre, Admin sem controle, catálogo ausente fora do
      momento, sem rede não abre, e recarga que volta a fechar (`RF-04-49`, `RF-04-57`).
- [x] 5.3 No mesmo arquivo, os cenários da tela: catálogo com preço e estoque, saldo sem
      acumulado, item zerado oculto, ponto regular ausente, diferença em pontos na recusa, saldo
      que cai o preço com acumulado intacto, e volta à tela inicial ao fim (`RF-04-50` a
      `RF-04-56`, PRD-04 §12).
- [x] 5.4 `inicio.test.tsx`: o terceiro caminho aparece com o momento aberto e some quando ele
      fecha, e leva à entrada por nick e imagem, nunca ao cadastro (`RF-04-01`, `RF-04-49`).

## 6. Documentação

- [x] 6.1 No mesmo PR: PRD-04 §9 com as três rotas do §6.3, que a tabela não tinha, e §13 com as
      duas decisões do fundador de 2026-08-25 (a troca exige Mestre no aparelho, e a troca é
      escrita sob a sessão de trabalho com o Guerreiro(a) vindo da sessão aninhada); PRD-07 §9
      com `GET /v1/eu/pontos-extras`; as linhas correspondentes no documento 09;
      `docs/prds/index.md` com a quinta fatia do PRD-04. A janela de troca sem estado no núcleo
      **não** vira linha nova — o documento 09 já a decidiu, e duplicá-la contraria a fonte
      única. Nenhum arquivo novo em `docs/`, logo a `nav` do `mkdocs.yml` não muda; a relação
      entre documentos não muda, logo o documento 99 não muda.
