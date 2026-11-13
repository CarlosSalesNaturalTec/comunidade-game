# Tasks

## 1. `comum/customizacao`

- [x] 1.1 `comum/customizacao/api.ts` e `indice.ts`, com a entrada `./customizacao` e a pasta em
      `files` no `comum/package.json`: tipos da leitura de `GET /v1/eu/customizacoes`;
      `lerMinhasCustomizacoes`, `registrarMinhaCustomizacao`, `enviarMidiaDaCustomizacao`
      (movido da App 01, mesma assinatura) e `cancelarCustomizacao` (`RF-05-102`, `RF-05-103`,
      design — decisão 1). Verificação: tarefa 1.3.
- [x] 1.2 `comum/customizacao/RegistroDaCustomizacao.tsx`: descrição por texto e por fala
      transcrita no aparelho, aviso com o texto aprovado e o Saber mais **antes** do seletor,
      seletor só de imagem e vídeo com câmera traseira, registrar indisponível sem descrição ou
      sem arquivo, progresso, queda de rede com retomada ao mesmo registro, `registroIdInicial`
      para o pendente sem mídia, recusa do núcleo em linguagem simples (`RF-05-102`, design —
      decisões 2, 4 e 5). Verificação: tarefa 1.3.
- [x] 1.3 Testes em `comum/customizacao/customizacao.test.tsx`: os dois cenários do delta de
      `camada-visual-comum` e os quatro do segundo requisito do delta de `area-do-guerreiro` —
      aviso antes do envio, controle indisponível sem descrição ou mídia, fala no campo, queda
      de rede e retomada ao mesmo registro (`RF-05-102`). Verificação: `npx vitest run` no
      recorte, verde.

## 2. App 05 — conquistas

- [x] 2.1 `apps/app-05-guerreiro/src/carteira/Conquistas.tsx`: as duas leituras juntas, a
      junção por `recompensa_de_marco_id`, o último registro por kit e a ação da tabela do
      primeiro requisito do delta; Cancelar; Enviar de novo abre registro novo; releitura depois
      de cada ato; falha só das customizações com aviso único, sem esconder as conquistas
      (`RF-05-102`, `RF-05-103`, design — decisão 3). Verificação: tarefa 2.2.
- [x] 2.2 Testes em `carteira/Conquistas.test.tsx`: os quatro cenários do primeiro requisito do
      delta de `area-do-guerreiro` — kit aberto oferece o registro, recompensa sem customização
      não muda, pendente aguarda a aula e se cancela, reprovado mostra o motivo e se reenvia —
      e o cenário "Nenhuma tela vende recompensa de marco" ainda verde (`RF-05-102`,
      `RF-05-103`, `RF-05-46`). Verificação: `npx vitest run` no recorte, verde.

## 3. App 01 — envio delegado

- [x] 3.1 `apps/app-01-aula-presencial/src/api/cuidadoDoBem.ts`: `enviarMidiaDaCustomizacao`
      passa a função local que delega ao `comum/customizacao`, sem mudar a exportação; nenhuma
      asserção de `cuidado/cuidado.test.tsx` editada (design — decisão 1). Verificação: o teste
      do recorte verde.

## 4. Documentação

- [x] 4.1 PRD-05 §9: as rotas da customização em que o ato é do Guerreiro(a) —
      `GET` e `POST /v1/eu/customizacoes`, `POST /v1/customizacoes/{id}/envios`,
      `/envios/confirmacao` e `/cancelamento`. `openspec/cronograma-de-fatias.md`: fatia 18 do
      PRD-05 com o slug `2026-11-13-registro-da-customizacao-do-kit-em-casa` e situação
      "implementado". Sem decisão nova a gravar no documento 09; `docs/prds/index.md`, o
      documento 99 e a `nav` não mudam. Verificação: `npm run lint` e `mkdocs build --strict`
      verdes.
