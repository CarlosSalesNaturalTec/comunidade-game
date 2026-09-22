## 1. A conferência sai sem aula

- [x] 1.1 `RF-05-01`, `RN-05-01`, `RN-01-57` — em
      `apps/app-05-guerreiro/src/api/sessoesDeGuerreiro.ts` e na entrada que a chama, declarar
      que a App 05 submete a conferência **sem aula**, com o comentário que amarra ao `RN-01-57`
      (design — decisão 1). Verificar que o pedido leva nick e descritor, e nenhuma aula.

## 2. A recusa deixa de absorver falha de camada

- [x] 2.1 `RN-05-48`, `RF-01-27` — em
      `apps/app-05-guerreiro/src/entrada/TelaDeEntradaDoGuerreiro.tsx`, reservar a frase da
      recusa ao código `autenticacao_biometrica_invalida` e apresentar a falha de camada pelo que
      ela é, em linguagem de criança e sem código técnico. Aplicar o mesmo padrão já
      implementado na App 01. Verificar que um 422 e uma falha de rede não produzem a frase da
      recusa.
- [x] 2.2 `RN-05-48` — encerrar o tratamento da recusa na conferência e dar tratamento próprio
      ao que roda depois dela. Verificar que falha posterior ao reconhecimento não vira recusa
      de rosto.

## 3. A sessão assistida passa a ser do responsável

- [x] 3.1 `RF-05-03`, `RF-05-04`, `RN-05-02` — em
      `apps/app-05-guerreiro/src/entrada/ConfirmacaoAssistida.tsx`, oferecer ao adulto os **dois**
      caminhos de login — social e usuário e senha — na mesma tela, e reescrever o texto, que hoje
      chama Mestre ou Admin (design — decisões 2 e 3). Verificar que qualquer um dos dois
      autentica e abre a sessão da criança.
- [x] 3.2 `RF-01-12`, `RF-14-09` — conduzir a **troca de senha provisória** dentro do próprio
      fluxo da confirmação, seguindo direto para abrir a sessão da criança ao concluir (design —
      decisão 4). Verificar que o responsável que entra com senha provisória não fica sem
      caminho.
- [x] 3.3 `RN-01-58`, `RN-01-22` — apresentar a recusa por criança fora da responsabilidade de
      quem confirma com a **mesma frase** da recusa por nick inexistente (design — decisão 5).
      Verificar que as duas telas são indistinguíveis.
- [x] 3.4 `RN-05-02` — conferir que a sessão do adulto continua morrendo assim que a da criança
      abre, com a chave de armazenamento própria que já existe, inclusive nos caminhos novos.

## 4. Testes

- [x] 4.1 `RF-05-01`, `RN-01-57` — em `apps/app-05-guerreiro/src/entrada/entrada.test.tsx`,
      cobrir "A conferência é submetida sem aula".
- [x] 4.2 `RN-05-48`, `RF-01-27` — cobrir "Erro de validação não vira rosto que não confere",
      "Rede fora não vira rosto que não confere" e "Nenhum código técnico chega à criança na
      falha de camada".
- [x] 4.3 `RF-05-03`, `RF-05-04`, `RF-01-12` — cobrir "Em casa, quem confirma é o responsável",
      "O responsável entra pelos dois caminhos de login" e "Senha provisória se troca ali mesmo".
- [x] 4.4 `RN-01-58`, `RN-05-02` — cobrir "Criança alheia recusa com a frase de sempre" e
      conferir que os cenários já existentes da sessão assistida seguem verdes, o de Mestre e
      Admin presentes incluído.

## 5. Documentação

- [x] 5.1 Marcar a linha desta fatia como implementada em `openspec/cronograma-de-fatias.md`.
      Nada muda em `docs/`: o documento 03, o documento 09, o documento 99 e os PRDs 01 e 05 já
      receberam, no PR de documentação que criou `RN-05-48` e revisou `RF-05-03`, `RF-05-04`,
      `RN-05-01` e `RN-05-02`, tudo o que estas decisões mudaram; nenhum arquivo nasce em `docs/`
      e a situação do PRD-05 não muda.
