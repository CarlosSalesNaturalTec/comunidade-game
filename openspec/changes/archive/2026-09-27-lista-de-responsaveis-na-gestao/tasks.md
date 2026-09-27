# Tasks

## 1. Regra do núcleo — os dois recortes

- [x] 1.1 (`RF-02-111`, `RF-09-122`) Em `backend/src/nucleo/responsaveis/regra.py`, criar
      `responsaveis_visiveis(sessao, *, operador, parametros)` devolvendo a página de
      responsáveis mais o cursor: Admin alcança todos; Mestre alcança quem tem vínculo
      vigente com Guerreiro(a) da comunidade do seu vínculo **ou** foi cadastrado por ele
      (design — decisões 3 e 4). Verificável: Mestre sem vínculo vigente ainda reencontra o
      que cadastrou.
- [x] 1.2 (`RF-02-111`) Resolver os vinculados de uma página em duas consultas em lote —
      `VinculoResponsavel` vigente por `responsavel_id.in_(…)` e `Nick` por
      `persona_id.in_(…)` —, sem consulta por responsável (design — decisão 5). Verificável:
      o número de consultas não cresce com o tamanho da página.
- [x] 1.3 (`RF-02-111`) Em `backend/tests/test_responsavel.py`, cobrir os recortes: Admin vê
      todos; Mestre vê os da sua comunidade; responsável de outra comunidade não aparece a
      ele; o que ele cadastrou sem vincular aparece; responsável sem vínculo vem com
      vinculados vazio; vínculo encerrado não entra.

## 2. Rota do núcleo

- [x] 2.1 (`RF-02-111`) Em `backend/src/nucleo/responsaveis/rotas.py`, expor
      `GET /v1/responsaveis` em `PaginaDeResultado`, sob
      `exigir_permissao(Operacao.vinculo_com_guerreiros_e_guerreiras, "le")` — nenhuma
      `Operacao` nova (design — decisões 1 e 2). A saída traz `id`, `nome` e os vinculados
      com `guerreiro_id`, `nick` e `grau_de_parentesco`, e nada de credencial ou contato.
- [x] 2.2 (`RF-02-111`) Em `backend/tests/test_responsavel_rota.py`, cobrir os cenários de
      rota do delta: Admin e Mestre leem; responsável, Apoiador e Guerreiro(a) recebem 403;
      a resposta não traz credencial, senha, usuário nem contato; os vinculados não trazem
      imagem real, nome civil nem nascimento; a paginação devolve cursor.

## 3. Tela da App 03

- [x] 3.1 (`RF-02-111`) Em `apps/app-03-gestao/src/personas/api.ts`, declarar
      `listarResponsaveis` e os tipos da saída da rota nova.
- [x] 3.2 (`RF-02-111`) Criar a lista dos responsáveis no padrão de `ListaDeAdultos`
      (`Tabela` de `comum/react`, colunas recolhidas no celular), com o cadastro sem vínculo
      sinalizado e o Guerreiro(a) sem nick também (design — decisões 6 e 8), e ligá-la à
      sub-área Responsáveis em `TelaDePersonas.tsx`, junto do botão de cadastrar que já
      existe. Verificável: a sub-área deixa de ser só um botão.
- [x] 3.3 (`RF-02-111`, `RF-02-06`, `RN-02-08`) Em `FormularioDeResponsavel.tsx`, permitir
      que o passo de vínculo abra para um responsável já existente, escolhido na lista, sem
      passar pelo cadastro (design — decisão 7), mantendo a mensagem do teto de três na
      retomada. Verificável: vincular um segundo Guerreiro(a) a um responsável antigo não
      cria responsável novo.
- [x] 3.4 (`RF-02-111`, `RF-02-64`) Em `personas.test.tsx`, cobrir os cenários do delta da
      gestão: a sub-área apresenta os cadastrados; cadastro interrompido aparece sinalizado;
      a retomada cria o vínculo sem cadastrar responsável; o teto de três continua explicado
      na retomada; lista vazia é dita; a lista não expõe credencial nem dado civil da
      criança; o aviso de coleta está na tela.

## 4. Documentação

- [x] 4.1 Gravar a decisão nova no documento-fonte e na pauta: uma frase em `docs/02-*.md`
      §1 sobre quem consulta os responsáveis cadastrados e com que recorte, e a linha em
      "Já decididos" do `docs/09-topicos-em-aberto-e-sugestoes.md` §1, com o porquê do ramo
      `criada_por` (decisão do fundador, 2026-09-26).
- [x] 4.2 Declarar `RF-02-111` em `docs/prds/prd-02-frontend-de-gestao.md` — a tabela de
      requisitos da §6, a rota `GET /v1/responsaveis` na tabela da §9 e a rastreabilidade —,
      e `RF-09-122` em `docs/prds/prd-09-area-do-mestre.md`, **declarado sem tela**, que é a
      fatia 22 daquele PRD.
- [x] 4.3 Marcar a fatia 24 do PRD-02 como implementada em
      `openspec/cronograma-de-fatias.md`, deixando a fatia 22 do PRD-09 em aberto. Conferir
      se a relação entre documentos mudou (doc 99 §8); a situação do PRD-02 em
      `docs/prds/index.md` não muda, e nenhum arquivo novo entra em `docs/`, logo a `nav` do
      `mkdocs.yml` fica como está.
