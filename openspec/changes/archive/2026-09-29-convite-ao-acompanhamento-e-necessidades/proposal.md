# Convite ao acompanhamento e necessidades em aberto

Origem: **PRD-03 — App 06: Vitrine pública**, §§3.1, 5.5, 6.4, 6.5, 7, 9 e 12. **Fatia 6** do
PRD-03 no `openspec/cronograma-de-fatias.md`.

Atende `RF-03-38` a `RF-03-44`, `RF-03-47`, `RN-03-15` a `RN-03-17` e `RN-03-25`.

## Why

A vitrine já mostra Guerreiros e Guerreiras, portfólio, ranking, poderes, comunidades e o
território, mas quem se comove com o que viu não tem por onde entrar: nenhuma página individual
convida a nada, "Como apoiar" ainda diz que as necessidades "chegam em entrega própria" e a
porta de pré-cadastro da App 08 existe sem que a vitrine aponte para ela. O núcleo já serve
`GET /v1/vitrine/necessidades` com tipo, quantidade faltante, moedas, comunidade, ponto de apoio
e horário da aula (`necessidade-de-recurso`), e a chave PIX já chega em "Como apoiar" pela
fatia 5: falta só a superfície.

## What Changes

- **Porta `/quero-participar`** na vitrine, em endereço próprio: o que é ser Apoiador — aportar,
  propor desafios extras, acompanhar favoritos —, o caminho do **pré-cadastro da App 08**, a
  **chave PIX** que "Como apoiar" publica e as **necessidades de recurso em aberto**
  (`RF-03-42`, `RF-03-43`). A tela declara que nada ali cria cadastro nem acesso e que quem
  cadastra Apoiador é um Admin, com prazo de 7 dias (`RN-03-17`).
- **Garfo de modalidade** na abertura da porta, só de encaminhamento: a pergunta é **o que a
  pessoa traz** e a resposta encaminha — dinheiro ao pré-cadastro da App 08; insumo,
  equipamento, alimento, serviço, conteúdo educacional, código, divulgação e a pretensão de
  ensinar ao formulário `/participar` que já existe, cada modalidade com o comprobatório que o
  documento 14 §10 lhe dá, nomeado na tela. Nenhum campo novo no formulário e nenhum atributo
  novo no núcleo (decisão do fundador, 2026-09-29).
- **Chamada "Quero participar"** e **ação de acompanhar** nas páginas individuais que existem —
  Guerreiro(a) e comunidade —, as duas levando à mesma porta (`RF-03-39`, `RF-03-40`). A
  chamada é do projeto: a porta **não recebe nick, identificador nem nome** de quem estava sendo
  visto, e nenhuma tela dela cita a pessoa da página de origem (`RF-03-41`, `RN-03-25`).
- **Necessidades de recurso em aberto** publicadas em dois lugares: dentro da porta e como bloco
  de "Como apoiar", no recorte de sociedade civil, com tipo, quantidade que falta, valor em
  moedas, comunidade, ponto de apoio, data e horário da aula (`RF-03-47`). Nenhum valor em
  reais e nenhuma pessoa na saída.
- **Recusar o convite** devolve o visitante à navegação de onde ele veio, sem gravar nada sobre
  a visita (`RF-03-44`).
- **Nada de favorito na vitrine**: nem no servidor, nem no aparelho, nem em parâmetro de rota —
  favoritar é função de Apoiador cadastrado, na App 08 (`RF-03-38`, `RN-03-15`, `RN-03-16`).
- `RF-03-39` sai **declaradamente parcial**: as páginas de Mestre e de Apoiador chegam na fatia 7
  e recebem a chamada lá; o **poder não tem página individual** — a fatia 2 o deixou como lista,
  e criá-la não é recorte desta fatia (decisão do fundador, 2026-09-29).

Nenhuma rota, entidade ou migração nova: o núcleo não muda.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-vitrine`: a App 06 ganha a porta do convite com o garfo de modalidade, a chamada
  e a ação de acompanhar nas páginas individuais, a publicação das necessidades em aberto e a
  proibição explícita de guardar favorito ou preferência do visitante.

## Impact

- **Código novo**: a porta, o garfo, a lista de necessidades e a chamada nas páginas, em
  `apps/app-06-vitrine/src/` (`api/leituras.ts`, `convite/`, `necessidades/`,
  `navegacao/caminhos.ts`, `navegacao/recortes.ts`, `institucional/SecoesInstitucionais.tsx`,
  `guerreiros/PaginaDoGuerreiro.tsx`, `territorio/PaginaDaComunidade.tsx`, `App.tsx`).
- **Código lido**: `backend/src/nucleo/necessidades/rotas.py` (contrato da saída pública),
  `comum/react/Botao.tsx`, `comum/react/Tabela.tsx`.
- **Documentação**: a linha 6 do cronograma e o PRD-03 §§6.4 e 15, que ganham o requisito do
  garfo — decisão já registrada nos documentos 02 §1, 14 §§10 e 11 e 09 §1 ("Já decididos"),
  que o PRD apenas aplica. `docs/prds/index.md`, o documento 09, o documento 99 e a `nav` não
  mudam.
- **Fora do escopo**, como o PRD-03 §3.2 já exclui: cadastro, login e área restrita na vitrine;
  o pré-cadastro em si — aporte declarado, comprovante e nick são da App 08; favoritar e
  acompanhar de verdade, que são da App 08; homologação do aporte e cadastro do Apoiador, atos
  de Admin na App 03; recibo e notificação por e-mail; qualquer preferência do visitante. Fora
  desta fatia, mas dentro do PRD-03: cards e páginas de Mestres e Apoiadores (7) e a Área do
  Apoiador Desenvolvedor (8).
