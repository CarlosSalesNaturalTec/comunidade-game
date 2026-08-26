# Tarefas

Dois blocos independentes: 1 a 3 são a fatia A (PRD-05), 4 a 6 são a fatia D (PRD-02). A
tarefa 7 fecha as duas.

## 1. A pasta e a esteira da App 05

- [x] 1.1 Criar `apps/app-05-guerreiro` no padrão das três aplicações existentes — `package.json`
      com os mesmos scripts, `vite.config.ts`, `tsconfig`, `index.html`, `public/favicon.svg` e
      `src/index.css` importando `comum/tokens.css` e `comum/fontes.css`. Verificar com
      `npm run build` e `vitest run` na pasta nova, ambos limpos.
- [x] 1.2 Declarar a chave de aplicação e o endereço do núcleo por variável de ambiente do Vite,
      no padrão de `apps/app-01-aula-presencial/src/api/configuracao.ts` — uma chave por
      ambiente, nenhum valor embutido no código. Verificar que o build sem as variáveis não
      embute segredo nenhum.
- [x] 1.3 Publicar o endereço da App 05: alvo de _hosting_ no `firebase.json` e no `.firebaserc`
      e workflow `.github/workflows/app-05-deploy.yml`, espelhando `app-01-deploy.yml` nos
      caminhos que disparam. Verificar que o `frontend-ci.yml` já alcança a pasta nova por
      `apps/**`, sem alteração.

## 2. A fronteira de biometria compartilhada

- [x] 2.1 Mover `apps/app-01-aula-presencial/src/biometria/biometria.ts` para `comum/biometria/`,
      exportando pelo índice do pacote, e apontar a App 01 para o novo caminho (design —
      decisão 1). Verificar que a suíte da App 01 continua verde sem alteração de teste.
- [x] 2.2 Replicar no `vite.config.ts` da App 05 o `alias` do `@vladmandic/human` para o build
      ESM de navegador, no build e no Vitest. Verificar que um teste da App 05 que importa o
      módulo roda em jsdom sem exigir `@tensorflow/tfjs-node`.

## 3. Entrada e sessão da App 05

- [x] 3.1 Tela de entrada por nick e imagem, obtendo vivacidade e descritor no aparelho e
      submetendo só o descritor a `POST /v1/sessoes/guerreiro` (`RF-05-01`, `RN-05-01`).
      Verificar que a chamada leva o descritor e nenhuma imagem, e que a recusa não revela se o
      nick existe.
- [x] 3.2 Recusa em aparelho sem câmera, em linguagem de criança de 6 anos, sem código de erro
      nem termo técnico, dizendo o que fazer (`RF-05-02`).
- [x] 3.3 Sessão assistida por Mestre ou Admin presente, nos dois caminhos — conferência que
      falhou e Guerreiro(a) sem imagem gravada — por `POST /v1/sessoes/guerreiro/confirmacao`
      (`RF-05-03`, `RF-05-04`, `RN-05-02`). Verificar que sem adulto autenticado nenhuma sessão
      abre.
- [x] 3.4 Encerramento ao sair e por inatividade, com aviso um minuto antes e opção de continuar
      que recomeça a contagem, voltando ao pedido de nick nos dois casos (`RF-05-05`,
      `RF-05-71`). A duração vem da implantação, sem padrão no código.
- [x] 3.5 Guarda do aparelho compartilhado: nenhuma imagem nem descritor armazenados, nenhum
      dado do Guerreiro(a) anterior na tela seguinte e troca de sessão sem reiniciar a aplicação
      (`RF-05-06`, `RF-05-07`). Verificar que toda tela além do pedido de nick exige sessão
      aberta.
- [x] 3.6 Testes da entrada e da sessão, cobrindo os cenários de `specs/area-do-guerreiro` e os
      critérios de aceite do PRD-05 §12 que alcançam este recorte: entrada em poucos segundos
      com imagem gravada, recusa sem câmera, sessão aberta pelo Mestre depois da falha e tela
      seguinte sem dado da criança anterior.

## 4. O que a ocorrência de conduta passa a gravar

- [x] 4.1 Acrescentar `valor_debitado` e `encerrada_em` a `ocorrencia_de_conduta`, gravando o
      primeiro na inserção com o que o débito tirou de fato depois do aparo em zero (design —
      decisões 3 e 4, `RF-02-100`). Verificar com uma ocorrência lançada sobre trilha com menos
      de 5 pontos, em que `valor` fica 5 e `valor_debitado` fica menor.
- [x] 4.2 Estreitar o _trigger_ `trg_ocorrencia_de_conduta_somente_insercao` para admitir
      exatamente o `UPDATE` que anula `motivo` e carimba `encerrada_em`, mantendo os
      `event.listen` de mapper intactos (design — decisão 2). Verificar que `UPDATE` de qualquer
      outra coluna e todo `DELETE` continuam recusados pelo banco, inclusive um que anule o
      motivo e mude `valor` junto.
- [x] 4.3 Migração Alembic das duas colunas e da função do _trigger_, com preenchimento das
      linhas existentes de `valor_debitado` pelo valor nominal, e a cópia do _trigger_ presa ao
      `after_create` do modelo acompanhando a mudança (design — Migration Plan).

## 5. O ato de fim de ciclo

- [x] 5.1 Regra do encerramento do ciclo: expurga o motivo de todas as ocorrências que ainda o
      guardam e carimba `encerrada_em`, num só `UPDATE` de Core; não cria nada, não declara ciclo
      seguinte e não grava indicador (`RF-02-99`, `RF-02-100`, `RN-02-30`). Verificar que
      executar duas vezes seguidas não altera nada na segunda.
- [x] 5.2 Rota do ato, restrita a Admin, herdando o registro de auditoria de toda escrita
      (`RF-02-99`, design — decisão 5). Verificar que Mestre, Apoiador, responsável e
      Guerreiro(a) recebem recusa.
- [x] 5.3 O ranking público passa a somar de volta o `valor_debitado` das ocorrências com
      `encerrada_em` preenchido, sem tocar o saldo de ponto regular (`RF-02-100`). Verificar que
      ocorrência do ciclo corrente segue pesando na posição e que o saldo não muda.
- [x] 5.4 Testes do ato e do ranking, cobrindo os cenários de `specs/fim-de-ciclo`,
      `specs/ocorrencia-de-conduta` e `specs/leitura-publica-da-vitrine`: expurgo que preserva
      valor, data e autor; recusa do expurgo avulso fora do ato; posição recalculada sem o
      débito da ocorrência encerrada; indicadores da lista pública inalterados.

## 6. A tela do encerramento na App 03

- [x] 6.1 Área do encerramento do ciclo na App 03, com confirmação explícita que enuncia os dois
      efeitos antes de executar, sem oferecer declarar o ciclo seguinte (`RF-02-99`,
      `RF-02-100`, `RN-02-30`). Verificar que desistir não executa nada e que confirmar exibe o
      resultado do ato.
- [x] 6.2 Testes da tela, cobrindo os cenários de `specs/aplicacao-de-gestao`: confirmação
      pedida antes de qualquer escrita, desistência sem efeito e ausência de campo para o ciclo
      seguinte.

## 7. Documentação

- [ ] 7.1 Gravar a decisão nova do fundador de 2026-08-25 — ao fim do ciclo o ranking devolve o
      que foi debitado, não o valor nominal — no documento-fonte 11 §5, mover a linha
      correspondente no documento 09 de pendente para decidida e aplicar o requisito no PRD-02.
      Atualizar `docs/prds/index.md` com a situação do PRD-05, que passa a ter a primeira fatia
      entregue, e a do PRD-02. Conferir os invariantes do documento 99 §6 e atualizar o
      documento 99 §8 se a relação entre documentos mudou. Nenhum arquivo novo em `docs/`, logo
      nada a acrescentar à `nav` do `mkdocs.yml`.
