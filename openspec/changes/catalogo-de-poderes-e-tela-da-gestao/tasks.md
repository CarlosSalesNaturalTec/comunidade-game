## 1. Porta HTTP do catálogo

- [x] 1.1 Criar `backend/src/nucleo/poderes/rotas.py` com o `roteador`, a saída
      `PoderSaida` (id, nome, descrição, natureza, vigência, papel e ativo) e `POST /poderes`,
      restrita a Admin sobre `cadastrar_poder`, sem tocar a regra — 201 com o poder gravado
      (`RF-02-10`, `RF-01-62`, `RN-01-43`, `RN-01-54`).
- [x] 1.2 Acrescentar `GET /poderes` pelo contrato único de listagem, paginado por
      `(nome, id)`, exigindo persona em sessão, sem filtro por comunidade e **incluindo o poder
      inativo** (`RF-02-10`, `RF-01-28`).
- [x] 1.3 Acrescentar `PUT /poderes/{id}` sobre `alterar_poder`, com o corpo restrito a nome,
      descrição e vigência — natureza e papel fora do contrato (`RF-02-10`, `RN-01-43`,
      `RN-01-54`).
- [x] 1.4 Acrescentar `POST /poderes/{id}/desativacao` sobre `desativar_poder`, devolvendo o
      poder já inativo (`RF-02-10`, `RF-01-62`).
- [x] 1.5 Registrar o roteador em `principal.py` por `incluir_roteador_de_dados` e conferir as
      quatro rotas sob `/v1` no schema OpenAPI publicado.

## 2. Testes do núcleo

- [x] 2.1 Criar `backend/tests/test_poder_rota.py` cobrindo a escrita: Admin cadastra com nome,
      descrição, natureza, vigência e papel; Mestre recebe 403 no cadastro, na alteração e na
      desativação; cadastro sem nome e alteração com nome vazio recebem 422 com o campo; o
      segundo papel do Território recebe 409 e o primeiro permanece.
- [x] 2.2 No mesmo arquivo, cobrir a leitura e a desativação: a listagem traz natureza,
      vigência, papel e ativo; o poder desativado aparece na listagem da gestão e **não**
      aparece em `GET /vitrine/poderes`; a consulta sem credencial de persona é recusada; o
      cursor pagina por `(nome, id)`.
- [x] 2.3 No mesmo arquivo, cobrir que a alteração não alcança natureza nem papel: renomear o
      poder do Território mantém o papel e `buscar_poder_do_territorio` segue devolvendo o
      mesmo poder; poder desativado com trilha vinculada mantém o vínculo da trilha.

## 3. Área Poderes na App 03

- [x] 3.1 Criar `apps/app-03-gestao/src/poderes/api.ts` com as quatro chamadas, no padrão de
      `pontos-de-apoio/api.ts`, incluindo a paginação por cursor.
- [x] 3.2 Criar `ListaDePoderes.tsx` e `ListaDePoderes.css` distinguindo ativo de inativo,
      vigente de ciclo futuro e o papel declarado, com a natureza visível em cada linha
      (`RF-02-10`).
- [x] 3.3 Criar `FormularioDePoder.tsx` para cadastro e edição, com a natureza selecionável só
      no cadastro e o aviso de que ela não muda depois, e a mensagem de recusa do segundo papel
      do Território (`RF-02-10`, `RN-01-43`, `RN-01-54`).
- [x] 3.4 Criar `DesativarPoder.tsx` e `TelaDePoderes.tsx`, e acrescentar a entrada "Poderes"
      em `App.tsx` ao lado de "Comunidades".
- [x] 3.5 Criar `apps/app-03-gestao/src/poderes/poderes.test.tsx` cobrindo: a lista mostra o
      inativo marcado; o cadastro envia natureza, vigência e papel; a recusa 403, a 422 de nome
      em falta e a 409 do papel do Território aparecem na tela; a desativação atualiza a linha.

## 4. Documentação

- [x] 4.1 Registrar a quinta fatia do PRD-02 em `docs/prds/index.md`, mantendo o PRD-02 em
      **aprovado**. Nenhuma decisão nova, nenhum documento-fonte alterado, nenhuma pendência
      nova no documento 09, nenhuma relação entre documentos mudada e nenhum arquivo novo em
      `docs/` — o documento 99 e a `nav` do `mkdocs.yml` ficam como estão.
