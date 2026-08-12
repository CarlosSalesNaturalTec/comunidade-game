## 1. Dependências e configuração

- [x] 1.1 Acrescentar `argon2-cffi` e `google-auth` às dependências do `backend/pyproject.toml`,
      com o `uv.lock` atualizado (design — decisões da senha e do _ID token_).
- [x] 1.2 Acrescentar a `Configuracao` os parâmetros `identidade_fundador` (`RF-01-61`) e
      `sessao_adulto_duracao` (PRD-01 §§10, 14), **ambos obrigatórios e sem valor padrão**, e o
      custo do Argon2id com padrão ajustável.
- [x] 1.3 Verificar que o núcleo não sobe quando `CG_SESSAO_ADULTO_DURACAO` ou
      `CG_IDENTIDADE_FUNDADOR` não está declarada, com mensagem que diz qual falta.

## 2. Modelo de dados e migração

- [x] 2.1 Criar o modelo `ComunidadeVirtual` com os atributos do PRD-08 §8, **sem rota**
      (`RF-01-23`, `RN-01-05`).
- [x] 2.2 Criar o modelo `Persona` em tabela única, com o papel entre os cinco do PRD-01 §4
      (`RF-01-19`).
- [x] 2.3 Criar o vínculo obrigatório de comunidade do Guerreiro(a), com unicidade sobre o
      vínculo vigente (`RN-01-05`).
- [x] 2.4 Criar o modelo `Credencial` com os atributos do PRD-01 §8 — persona, tipo,
      identificador, segredo, criada por, troca pendente, ativa (`RF-01-11`, `RN-01-18`).
- [x] 2.5 Criar o modelo `Sessao` com os atributos do PRD-01 §8 — persona, início, expiração,
      origem, como autenticou, quem confirmou, encerrada em — e índice pelo resumo do token.
- [x] 2.6 Escrever a segunda migração Alembic criando as quatro tabelas, sem tocar
      `chave_de_aplicacao`, e conferir que ela sobe e desce.

## 3. Persona e credencial

- [x] 3.1 Recusar criação de persona sem papel declarado (`RF-01-19`).
- [x] 3.2 Aplicar quem cadastra quem: Mestre e Apoiador só por Admin, responsável por Admin ou
      Mestre, Admin novo só por outro Admin (`RN-01-01`, `RN-01-02`).
- [x] 3.3 Recusar persona de Guerreiro(a) sem comunidade e recusar segundo vínculo vigente
      (`RN-01-05`).
- [x] 3.4 Implementar `POST /v1/credenciais`, restrita a Admin e Mestre, criando a credencial de
      usuário e senha provisória com a troca pendente marcada (`RF-01-11`, `RN-01-18`).
- [x] 3.5 Guardar a senha com Argon2id e garantir que nenhuma rota, consulta ou registro
      operacional devolva a senha em claro (`RN-01-18`).
- [x] 3.6 Responder 403 a quem não é Admin nem Mestre e tenta criar credencial (`RF-01-16`).

## 4. Semeadura do Admin fundador

- [x] 4.1 Estender o comando de implantação para convergir a persona Admin do fundador a partir
      de `CG_IDENTIDADE_FUNDADOR`, além das chaves (`RF-01-61`).
- [x] 4.2 Garantir que semear duas vezes não duplica a persona e que a semeadura não cria
      persona de nenhum outro papel (`RF-01-61`).
- [x] 4.3 Falhar de forma visível, sem criar persona alguma, quando a identidade do fundador não
      está declarada (`RF-01-61`).

## 5. Sessão do adulto

- [x] 5.1 Implementar o token de sessão opaco, guardando apenas o resumo, e a dependência que
      resolve a sessão a partir do cabeçalho (PRD-01 §9).
- [x] 5.2 Implementar `POST /v1/sessoes/social`: verificar o _ID token_ contra o JWKS do Google,
      com cache, e abrir sessão para a persona correspondente (`RF-01-09`).
- [x] 5.3 Responder 503, nunca 401, quando o JWKS está indisponível (design — riscos).
- [x] 5.4 Recusar com 403, sem criar persona, o login social ou o usuário sem cadastro
      correspondente, orientando a solicitar participação pela vitrine (`RF-01-10`, `RN-01-04`).
- [x] 5.5 Implementar `POST /v1/sessoes/credencial`, abrindo sessão com o papel da persona
      vinculada (`RF-01-11`, `RN-01-18`).
- [x] 5.6 Travar a sessão com troca de senha pendente: 403 em toda rota que não seja a da troca
      (`RF-01-12`).
- [x] 5.7 Implementar `POST /v1/credenciais/senha`, que conclui a troca, derruba a pendência e
      invalida a senha provisória para um segundo acesso (`RF-01-12`, `RN-01-18`).
- [x] 5.8 Implementar `DELETE /v1/sessoes/atual`, registrando quando a sessão foi encerrada, e
      responder 401 a token encerrado ou expirado (PRD-01 §9).
- [x] 5.9 Implementar `GET /v1/eu`, devolvendo persona, papel e permissões da sessão (PRD-01 §9).

## 6. Permissões e escopo de comunidade

- [x] 6.1 Declarar a matriz de permissões espelhando a tabela do PRD-01 §4, como dado
      (`RF-01-16`).
- [x] 6.2 Conferir a matriz por dependência única, negando por padrão, com 403 para operação
      fora do papel (`RF-01-16`).
- [x] 6.3 Exigir persona autenticada em toda rota de escrita e gravar autor, papel e data e hora
      com fuso (`RF-01-03`).
- [x] 6.4 Preservar a data do fato, gravando a data do registro à parte (`RF-01-03`,
      convenções da fatia anterior).
- [x] 6.5 Aceitar e aplicar o filtro por comunidade nas consultas de dado de comunidade, com 422
      pelo corpo de erro único quando o filtro obrigatório falta (`RF-01-18`).

## 7. Verificação contra os critérios de aceite do PRD-01 §12

- [x] 7.1 Teste: login social ou usuário sem cadastro é recusado e **nenhuma persona é criada**
      (`RF-01-10`).
- [x] 7.2 Teste: adulto com senha provisória só consegue trocar a senha; qualquer outra rota
      devolve 403 (`RF-01-12`).
- [x] 7.3 Teste: toda escrita bem-sucedida gera registro com autor, papel e data e hora
      (`RF-01-03`).
- [x] 7.4 Teste: persona que tenta operação fora do papel recebe 403 (`RF-01-16`).
- [x] 7.5 Teste que percorre a **matriz inteira** do PRD-01 §4, papel por operação, comparando
      com a tabela do PRD (`RF-01-16`).
- [x] 7.6 Teste: consulta filtrada por uma comunidade não devolve registro de outra, e o filtro
      obrigatório ausente devolve 422 (`RF-01-18`).
- [x] 7.7 Teste: sessão encerrada e sessão expirada respondem 401, e uma sessão não alcança
      outra (PRD-01 §§9, 12).
- [x] 7.8 Teste: rota nova sem chave de aplicação continua respondendo 401, sem diferenciar o
      motivo (`RN-01-32`, regressão da fatia anterior).
- [x] 7.9 Rodar `ruff format --check .`, `ruff check .` e `pytest` na pasta `backend/`, as três
      verdes.

## 8. Documentação e esteira

- [x] 8.1 Conferir que a decisão da semeadura do primeiro Admin já está no documento 02 §1, no
      documento 09 e no PRD-01 (`RF-01-61`) — foi gravada antes desta change, e nada mais em
      `docs/` muda por ela.
- [x] 8.2 Conferir que nenhuma relação entre documentos mudou, que nenhum arquivo novo entrou em
      `docs/` e que `docs/prds/index.md` segue refletindo a situação.
- [x] 8.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR.
