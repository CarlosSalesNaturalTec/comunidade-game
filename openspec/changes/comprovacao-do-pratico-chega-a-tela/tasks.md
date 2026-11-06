# Tasks

## 1. Contrato do percurso

- [ ] 1.1 Criar `comum/contratos/missao-no-percurso.json` com a resposta de
      `GET /v1/eu/trilhas/{id}/missoes/{ordem}` para um prático em imagem, critério e título
      curto preenchidos, e `comprovacao_entregue` de uma declaração em mídia sem arquivo
      (`RF-05-91`, `RF-05-93`, design — decisão 2).
- [ ] 1.2 Em `backend/tests/test_desbloqueio_da_missao.py`, montar o mesmo cenário e afirmar que
      as chaves de `desafio_de_desbloqueio` e de `comprovacao_entregue` são iguais às do
      exemplo; acrescentar `comum/contratos/**` aos `paths` de `.github/workflows/backend-ci.yml`
      (`RF-05-91`, design — decisão 2).

## 2. Tela do Guerreiro(a) (`comum/trilha`)

- [ ] 2.1 Em `comum/trilha/api.ts`, renomear na interface `DesafioDeDesbloqueio` os três campos
      para `forma_de_comprovacao`, `criterio_de_aceite` e `titulo_curto`, e ajustar todo uso em
      `comum/trilha/` (`RF-05-91`, `RF-05-92`, `RF-04-76`, design — decisões 1 e 3).
- [ ] 2.2 Em `comum/trilha/DesafioDeDesbloqueio.tsx`, ler os nomes novos, tirar o comentário do
      campo "ausente" e mostrar "O que você entregou" só quando houver texto ou arquivo
      (`RF-05-92`, `RF-05-93`, design — decisões 3 e 5).
- [ ] 2.3 No mesmo componente, no ramo "aguardando o Mestre", oferecer o envio do arquivo à
      declaração em mídia sem arquivo e sem entrega no encontro — aviso da mídia guardada,
      seletor, progresso e retomada por `enviarArquivoDaComprovacao`, recarregando a missão ao
      concluir (`RF-05-91`, `RF-05-93`, design — decisão 4).

## 3. Bancada da App 09

- [ ] 3.1 Em `apps/app-09-mestre/src/turmas/TelaDeDesbloqueiosPendentes.tsx`, trocar "O envio do
      arquivo ainda não concluiu." pelas duas frases da decisão 6, conforme
      `comprovacao_entregue.forma` (`RF-09-132`, `RF-05-93`).

## 4. Testes das telas

- [ ] 4.1 `comum/trilha/trilha.test.tsx`: usar o exemplo de contrato; cobrir que o prático em
      imagem mostra critério, forma, aviso, seletor e "Vou entregar ao Mestre no encontro"; que
      a declaração pendente sem arquivo oferece o envio e, enviado, mostra o arquivo guardado;
      que "O que você entregou" não aparece vazio (`RF-05-91` a `RF-05-93`, `RN-05-51`).
- [ ] 4.2 `apps/app-05-guerreiro/src/trilha/{DesafioDeDesbloqueio,Missao,Sondagem}.test.tsx`:
      trocar os objetos escritos à mão pelo exemplo de contrato ou pelos nomes certos
      (`RF-05-91`, `RF-05-92`).
- [ ] 4.3 `apps/app-01-aula-presencial/src/trilhas/trilhas.test.tsx`: mesmos ajustes, com o
      cenário de que a App 01 apresenta o seletor de arquivo do prático em imagem
      (`RF-04-76`).
- [ ] 4.4 Teste da bancada na App 09: prático sem forma e mídia sem arquivo dizem cada um a sua
      frase, nenhuma fala em envio em andamento, e o julgamento segue disponível (`RF-09-132`).

## 5. Documentação

- [ ] 5.1 Acrescentar ao bloco do PRD-05 em `openspec/cronograma-de-fatias.md` a linha sem número
      "Comprovação do prático chega à tela", correção da fatia 13, relatada pelo fundador em
      2026-11-06. Sem decisão nova, sem mudança de PRD, de `docs/prds/index.md`, do documento
      99 nem da `nav`.
