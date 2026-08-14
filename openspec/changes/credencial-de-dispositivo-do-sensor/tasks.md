## 1. A decisão do Mestre autor, antes do código

- [ ] 1.1 Gravar no documento 03 §1.1 a qualificação decidida pelo fundador: a credencial de
      dispositivo é emitida e revogada por **Admin ou pelo Mestre autor do desafio** da série,
      e não por qualquer Mestre.
- [ ] 1.2 Atualizar a linha "Autenticação do sensor do Guerreiro(a)" do documento 09, em "Já
      decididos", com a mesma qualificação — a linha já existe e não muda de seção.
- [ ] 1.3 Aplicar a decisão ao PRD-01: `RF-01-67` e `RF-01-68` em §6, o item novo na linha do
      Mestre da matriz de §4 e a linha correspondente na tabela de §13.
- [ ] 1.4 Verificar que nenhum outro documento repete a regra de quem emite — fonte única —, e
      que o documento 99 não precisa mudar, por nenhuma relação entre documentos ter mudado.

## 2. A credencial de dispositivo no modelo

- [ ] 2.1 Acrescentar `dispositivo` ao enum `TipoDeCredencial` (`RF-01-67`).
- [ ] 2.2 Acrescentar à `Credencial` as colunas `serie_de_coleta_id`, `trilha_id`,
      `revogada_por`, `motivo_da_revogacao` e `revogada_em`, todas anuláveis, como o PRD-01 §8
      declara (`RF-01-67`, `RF-01-68`).
- [ ] 2.3 Restringir o índice `uq_credencial_identificador_por_tipo_ativa` aos tipos que não
      são `dispositivo`, para o mesmo aparelho poder servir a mais de uma série (`RN-01-53`).
- [ ] 2.4 Criar o índice único parcial sobre `serie_de_coleta_id`, onde `ativa` e tipo
      `dispositivo` — nunca duas vivas para a mesma série (`RN-01-53`, documento 03 §1.1).
- [ ] 2.5 Verificar: duas credenciais ativas na mesma série são recusadas pelo índice; o mesmo
      identificador em séries distintas é aceito; revogada a primeira, a série aceita outra
      (`RN-01-53`).

## 3. Emissão

- [ ] 3.1 Emitir a credencial sobre uma série, recebendo o identificador do aparelho e a trilha
      em que ele foi construído, e gerando apenas o segredo (`RF-01-67`).
- [ ] 3.2 Vincular a credencial ao Guerreiro(a) coletor da série e à própria série, sem criar
      entidade de dispositivo alguma (`RF-01-67`, `RN-01-53`).
- [ ] 3.3 Guardar apenas o resumo criptográfico do segredo e devolver o segredo uma única vez,
      na resposta da emissão (`RF-01-67`).
- [ ] 3.4 Registrar em `permissoes.py` a operação de emissão e revogação, escopada a Admin e ao
      Mestre autor do desafio da série, conforme o item novo da matriz do PRD-01 §4.
- [ ] 3.5 Recusar com 403 o Mestre que não é autor do desafio e a persona de qualquer outro
      papel (`RF-01-67`).
- [ ] 3.6 Verificar: Admin emite; o Mestre autor emite; o Mestre que não é autor recebe 403;
      Guerreiro(a), responsável e Apoiador recebem 403; a leitura da credencial nunca devolve o
      segredo nem o seu resumo (`RF-01-67`).

## 4. Conferência, sem sessão

- [ ] 4.1 Conferir a credencial pelo cabeçalho `X-Credencial-Dispositivo`, na forma
      `<identificador>.<segredo>`, buscando pelo par identificador e série ativa (`RN-01-53`,
      `RN-08-23`).
- [ ] 4.2 Reaproveitar `gerar_segredo` e `calcular_resumo`, comparar com `hmac.compare_digest` e
      manter o resumo fantasma, para credencial inexistente e segredo errado custarem o mesmo
      tempo (`RF-01-67`).
- [ ] 4.3 Devolver contexto próprio da credencial, nunca `ContextoDaSessao`, de modo que ela não
      alcance rota que espera persona (`RN-08-23`, `RN-01-34`).
- [ ] 4.4 Continuar exigindo a chave de aplicação na chamada do sensor (`RF-01-48`).
- [ ] 4.5 Verificar: chamada com credencial ativa é processada; segredo que não confere é
      recusado; credencial revogada é recusada; sem chave de aplicação responde 401; nenhuma
      resposta devolve sessão ou credencial de sessão (`RN-08-23`).
- [ ] 4.6 Verificar que a credencial não alcança rota de consulta alguma nem outra rota de
      escrita além da gravação de registro (`RN-08-23`, `RN-01-34`).

## 5. Revogação

- [ ] 5.1 Revogar a credencial por ato de Admin ou do Mestre autor do desafio, gravando motivo,
      autoria e data e hora, e marcando-a inativa (`RF-01-68`).
- [ ] 5.2 Recusar a revogação sem motivo e a revogação por Mestre que não é autor do desafio
      (`RF-01-68`).
- [ ] 5.3 Verificar: a revogação grava motivo, autoria e data e hora; a chamada seguinte do
      sensor é recusada; os registros já gravados permanecem inalterados (`RF-01-68`,
      `RN-08-10`).
- [ ] 5.4 Verificar que a credencial **não** cai ao encerrar o vínculo do Guerreiro(a) com uma
      Comunidade Virtual, porque esse não é o fim do vínculo de que trata o `RF-01-68` — a
      segunda metade dele é de entrega posterior.

## 6. A origem sensor no registro

- [ ] 6.1 Acrescentar a coluna `credencial_id` ao `RegistroDeColeta`, anulável — o atributo
      `dispositivo` do PRD-08 §8 (`RF-08-14`).
- [ ] 6.2 Aceitar, na rota de registro, a autenticação por credencial de dispositivo ao lado da
      sessão de persona, resolvendo por dependência qual delas autenticou (`RF-08-14`, PRD-08
      §9).
- [ ] 6.3 Gravar origem `sensor` quando, e somente quando, a chamada vier por credencial de
      dispositivo, e manter a recusa com 422 da origem `sensor` na rota de sessão (`RF-08-14`,
      `RN-08-23`).
- [ ] 6.4 Recusar a gravação em série diferente daquela a que a credencial está presa, ainda que
      seja do mesmo Guerreiro(a) (`RN-08-23`).
- [ ] 6.5 Gravar como autor o Guerreiro(a) coletor da série, com o papel dele, e nunca o
      aparelho (`RN-08-11`, `RF-01-03`).
- [ ] 6.6 Verificar: o sensor autenticado grava com origem `sensor` e aponta a credencial; a
      autoria é a do coletor; a série alheia é recusada; a origem `sensor` na rota de sessão
      segue recusada com 422 (`RF-08-14`).
- [ ] 6.7 Verificar que o registro de sensor segue todas as regras já vigentes do registro — a
      hora da medição distinta da hora do envio, o valor fora da faixa marcado "a conferir", a
      comunidade vigente na data da medição e o crédito ao Poder do Território (`RF-08-08`,
      `RF-08-09`, `RF-08-12`, `RF-08-15`, `RN-08-03`).
- [ ] 6.8 Verificar que o segredo não aparece em resposta alguma nem em registro operacional,
      aceito ou recusado (`RF-01-67`).

## 7. Migração e rotas

- [ ] 7.1 Escrever a migração do Alembic: as colunas novas da `Credencial`, a troca dos dois
      índices e a coluna `credencial_id` em `registro_de_coleta`, anulável e propagada às
      partições sem reescrita.
- [ ] 7.2 Registrar `POST /v1/credenciais/dispositivo` e `DELETE /v1/credenciais/dispositivo/{id}`
      no roteador e em `principal.py`, com o schema do OpenAPI, conforme o PRD-01 §9.
- [ ] 7.3 Verificar `downgrade` simétrico da migração, com os índices originais restaurados.

## 8. Documentação e esteira

- [ ] 8.1 Atualizar `docs/prds/index.md`: sai a exceção declarada de `RF-01-67` e `RF-01-68`,
      entra a nota de que resta do PRD-01 apenas a metade do `RF-01-68` que depende do marco de
      fim do vínculo.
- [ ] 8.2 Conferir que a `nav` do `mkdocs.yml` não muda, por nenhum arquivo ter nascido ou sido
      renomeado em `docs/`.
- [ ] 8.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict`.
- [ ] 8.4 Rodar `ruff format --check .`, `ruff check .` e `pytest` no backend.
