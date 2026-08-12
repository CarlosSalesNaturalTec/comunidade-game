## 1. Modelo de dados e migração

- [ ] 1.1 Criar o modelo `Nick`, em tabela própria, com o valor sob índice único e chave
      estrangeira única para `persona`, de modo que a unicidade alcance toda a plataforma e não
      só a comunidade (`RF-01-19`, `RN-01-22`, `RN-01-30`, design — decisões).
- [ ] 1.2 Exigir nick em toda persona de Guerreiro(a), recusando a criação sem ele (`RF-01-19`,
      `RN-01-30`).
- [ ] 1.3 Criar o modelo `AcessoAoTemplate` com o Guerreiro(a) alcançado, quem ou o quê acessou,
      a natureza do acesso, o desfecho e o momento com fuso (`RN-01-14`, documento 03 §3.3).
- [ ] 1.4 Alargar `credencial.segredo` de `String(512)` para `Text`, para caber o descritor
      cifrado e codificado (design — decisões).
- [ ] 1.5 Escrever a quarta migração Alembic criando `nick` e `acesso_ao_template` e alargando
      `credencial.segredo`, sem tocar as tabelas das fatias anteriores, e conferir que ela sobe
      e desce.
- [ ] 1.6 Criar na mesma migração o _trigger_ que recusa `UPDATE` e `DELETE` em
      `acesso_ao_template`, com o _listener_ de mapeador equivalente (`RN-01-14`, design —
      decisões).

## 2. Configuração e cifra

- [ ] 2.1 Acrescentar à configuração a duração da sessão do Guerreiro(a), o limiar de comparação,
      a dimensão esperada do descritor e a chave de cifragem — os quatro **sem valor padrão**, de
      modo que o ambiente que não os declarar não suba (`RF-01-04`, `RN-01-14`, design —
      decisões).
- [ ] 2.2 Implementar a cifra e a decifra do _template_ com AES-GCM, guardando a versão da chave
      junto ao dado para que a rotação futura não exija migração de estrutura (`RN-01-14`,
      design — decisões).
- [ ] 2.3 Verificar que o serviço falha na subida sem a chave de cifragem declarada, e que nenhum
      caminho grava _template_ em claro (`RN-01-14`).

## 3. Gravação e recadastro do _template_

- [ ] 3.1 Acrescentar à matriz de permissões as operações de confirmação de identidade e de
      cadastro biométrico do Guerreiro(a), para Mestre e Admin, com origem declarada nos
      requisitos (`RF-01-06`, `RF-01-08`, `RF-01-16`, design — decisões).
- [ ] 3.2 Implementar `POST /v1/guerreiros/{id}/descritor`, restrita a Mestre e Admin pela
      operação da matriz, gravando o _template_ cifrado como `Credencial` de tipo `biometria`
      (`RF-01-05`, `RF-01-07`, `RF-01-16`).
- [ ] 3.3 Recusar com 422 a gravação sem consentimento vigente do responsável para a captura
      biométrica, considerando vigente o registro mais recente de concessão (`RF-01-07`,
      `RN-01-17`).
- [ ] 3.4 Recusar com 422 o descritor cuja dimensão não corresponde ao parâmetro declarado, pelo
      corpo de erro único (`RF-01-05`).
- [ ] 3.5 Recusar qualquer requisição que traga fotografia, em qualquer rota do núcleo
      (`RF-01-05`, `RN-01-15`).
- [ ] 3.6 Implementar o recadastro pela mesma rota, substituindo o _template_ anterior e gravando
      quem recadastrou, com data e hora (`RF-01-08`, `RF-01-03`).
- [ ] 3.7 Garantir que nenhuma resposta — de sucesso ou de erro — devolve o descritor ou o
      _template_, e que não existe rota de leitura dele (`RF-01-05`, `RN-01-14`).

## 4. Sessão do Guerreiro(a)

- [ ] 4.1 Implementar `POST /v1/sessoes/guerreiro`, pública quanto à persona e exigindo chave de
      aplicação, abrindo sessão por nick e descritor com `como_autenticou` igual a `biometria`
      (`RF-01-04`, `RF-01-05`).
- [ ] 4.2 Restringir a busca ao nick por correspondência exata, decifrando um único _template_ e
      comparando pela distância contra o limiar declarado (`RF-01-04`, `RN-01-22`, design —
      decisões).
- [ ] 4.3 Responder 401 indistinguível entre nick inexistente, Guerreiro(a) sem _template_ e
      descritor que não confere, com a orientação de chamar o Mestre (`RF-01-04`, `RN-01-22`).
- [ ] 4.4 Comparar contra um _template_ de descarte gerado na subida quando o nick não é
      encontrado, para que o tempo de resposta não revele a existência do nick (`RN-01-22`,
      design — decisões).
- [ ] 4.5 Recusar com 422 o pedido de sessão sem descritor, e garantir que não existe caminho de
      sessão de Guerreiro(a) por senha, PIN ou código (`RF-01-04`).
- [ ] 4.6 Implementar `POST /v1/sessoes/guerreiro/confirmacao`, restrita a Mestre e Admin pela
      operação da matriz, com `como_autenticou` igual a `confirmacao_humana` e `quem_confirmou`
      gravado (`RF-01-06`, `RF-01-16`).
- [ ] 4.7 Garantir que o caminho da confirmação vale igualmente para o Guerreiro(a) sem
      _template_, para a falha de reconhecimento e para quem recusou a biometria, e que a sessão
      resultante tem os mesmos direitos da aberta por biometria (`RF-01-06`, `RN-01-16`,
      `RN-01-21`).
- [ ] 4.8 Aplicar a duração declarada à sessão do Guerreiro(a) e conferir que a expiração
      acontece sem intervenção humana (`RF-01-04`).

## 5. Auditoria do acesso ao _template_

- [ ] 5.1 Gravar registro de acesso em toda comparação de login, com o desfecho, tenha ela
      conferido ou não (`RN-01-14`, documento 03 §3.3).
- [ ] 5.2 Gravar registro de acesso na gravação e no recadastro, com quem operou (`RN-01-14`).
- [ ] 5.3 Verificar que o registro de acesso não se edita nem se apaga, pelas duas camadas
      (`RN-01-14`).

## 6. Verificação

- [ ] 6.1 Testar que nick repetido é recusado entre papéis diferentes, e que Guerreiro(a) sem
      nick não é criado (`RF-01-19`, `RN-01-30`).
- [ ] 6.2 Testar que nenhuma rota lista, completa ou sugere nick (`RN-01-22`).
- [ ] 6.3 Testar que as três recusas de sessão respondem corpo e código idênticos, e que o tempo
      de resposta não as separa (`RF-01-04`, `RN-01-22`, PRD-01 §12).
- [ ] 6.4 Testar que o Guerreiro(a) sem _template_ não entra sozinho, entra pela confirmação do
      Mestre, e passa a entrar sozinho depois de gravado o consentimento e o descritor (PRD-01
      §12).
- [ ] 6.5 Testar que nenhuma resposta da API devolve o _template_ nem aceita imagem (PRD-01 §12).
- [ ] 6.6 Testar que duas sessões de Guerreiros diferentes no mesmo aparelho não se alcançam e
      expiram cada uma na sua (`RF-01-04`, PRD-01 §12).
- [ ] 6.7 Testar que o Guerreiro(a) recebe 403 ao tentar gravar o próprio _template_, e que papel
      diferente de Mestre ou Admin recebe 403 na confirmação (`RF-01-16`).
- [ ] 6.8 Rodar `ruff format --check`, `ruff check` e `pytest` com a cobertura publicada no log,
      sem limiar que bloqueie.

## 7. Documentação

- [x] 7.1 Acrescentar ao PRD-01 §4 a confirmação de identidade e o cadastro biométrico na célula
      do Mestre, que `RF-01-06` e `RF-01-08` já lhe dão (`RF-01-16`).
- [x] 7.2 Registrar no PRD-01 §3.2 que a exclusão do _template_ é do PRD-13, e gravar no PRD-13 os
      requisitos correspondentes — `RF-13-43`, `RF-13-44` e `RN-13-22` —, com a decisão no
      documento 09 (documento 03 §3.3).
- [ ] 7.3 Atualizar `docs/prds/index.md` se a situação do PRD-01 mudar ao fim desta fatia.
- [ ] 7.4 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR.
