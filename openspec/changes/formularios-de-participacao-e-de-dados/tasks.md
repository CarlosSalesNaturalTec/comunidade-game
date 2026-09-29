# Tasks

## 1. API e apoio da App 06

- [x] 1.1 Criar em `apps/app-06-vitrine/src/api/` o envio das duas solicitações — multipart para
      participação, JSON para dados — sobre `chamarNucleo`, sem credencial de persona, devolvendo
      protocolo e prazo (`RF-03-31`, `RF-03-34`, `RN-03-13`)
- [x] 1.2 Mover `esperaEmLinguagemSimples` de `guerreiros/PaginaDoGuerreiro.tsx` para módulo
      compartilhado da vitrine e usá-la nos dois lugares; erros 422 e 429 traduzidos para
      "campo em falta" e "espera explicada" (`RF-03-35`, `RF-03-37`)

## 2. Telas

- [x] 2.1 Entregar o formulário de participação em `/participar`: cinco campos obrigatórios,
      instituição e links opcionais, avisos de que não cria cadastro nem acesso, de que um Admin
      avalia e do prazo de 7 dias antes do envio, e a confirmação com protocolo, prazo e retorno
      pelo contato declarado (`RF-03-27` a `RF-03-31`, `RN-03-11`, `RN-03-12`)
- [x] 2.2 Entregar o formulário de dados em `/solicitar-dados`: solicitante, instituição,
      e-mail, finalidade e recorte pedido, com as cinco condições da entrega declaradas antes do
      envio e a confirmação sem arquivo nem link (`RF-03-32` a `RF-03-34`, `RN-03-13`,
      `RN-03-14`)
- [x] 2.3 Manter em memória o que foi digitado quando o envio falha ou é freado, apontar o campo
      em falta, e não guardar nada no aparelho nem pedir CAPTCHA, cadastro ou login
      (`RF-03-35`, `RF-03-37`, `RN-03-08`, `RN-03-34`)
- [x] 2.4 Ligar os caminhos: rotas `/participar` e `/solicitar-dados` em `navegacao/recortes.ts` e
      `App.tsx`; seção "Solicitação do conjunto de dados" dos recortes de pesquisadores e
      gestores com botão para o formulário; link do formulário na orientação do Mestre em
      `entrada/personas.ts` (`RF-03-62`, `RF-03-32`)

## 3. Testes

- [x] 3.1 Em `apps/app-06-vitrine/src/testes/formularioDeParticipacao.test.tsx`: avisos antes do
      envio, campo obrigatório em falta apontado sem chamar o núcleo, opcionais omitidos, envio
      com confirmação de protocolo e prazo, e o link do Mestre abrindo o formulário
      (`RF-03-27` a `RF-03-31`, `RF-03-62`, `RN-03-11`, `RN-03-12`)
- [x] 3.2 Em `apps/app-06-vitrine/src/testes/formularioDeDados.test.tsx`: as cinco condições
      declaradas, campo em falta apontado, confirmação sem arquivo nem link, e a seção dos
      recortes levando ao formulário (`RF-03-32` a `RF-03-34`, `RN-03-13`, `RN-03-14`)
- [x] 3.3 Em `apps/app-06-vitrine/src/testes/freioDosFormularios.test.tsx`: 429 nos dois
      formulários com motivo e espera em linguagem simples, texto digitado preservado, ausência
      de CAPTCHA, cadastro e login, e `localStorage`, `sessionStorage` e cookie vazios
      (`RF-03-35`, `RF-03-37`, `RN-03-08`)

## 4. Documentação

- [x] 4.1 Marcar a fatia 4 do PRD-03 como implementada em `openspec/cronograma-de-fatias.md`,
      com o slug da change; registrar no documento 09 §1 a divergência do `recorte pedido` entre
      PRD-03 `RF-03-32` e PRD-01, resolvida pelo contrato do núcleo. `docs/prds/index.md`, o
      documento 99 e a `nav` do `mkdocs.yml` não mudam — nenhum arquivo nasce em `docs/` e nenhuma
      relação entre documentos muda
