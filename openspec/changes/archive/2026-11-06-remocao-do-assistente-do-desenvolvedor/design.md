# Design

## Context

A fatia 8 do PRD-03 (`2026-09-29-area-do-apoiador-desenvolvedor`) levou o chat à área
(`ChatDoDesenvolvedor`, `abertura.ts`), a rota `POST /v1/assistente-do-desenvolvedor` com porta
e adaptadores local/Gemini, o corpus montado na esteira e a superfície própria do freio. O
núcleo já publica Swagger em `/docs` e o schema em `/openapi.json`, fora de `/v1` e sem chave
(defaults do FastAPI, documento 09 "Documentação da API em OpenAPI"). A App 06 já recebe a
URL do núcleo por `VITE_URL_DO_NUCLEO` (`api/configuracao.ts`).

## Goals / Non-Goals

**Goals:** retirar o assistente do Desenvolvedor de ponta a ponta — documento, PRD, tela,
núcleo, freio, esteira — e pôr o link do Swagger na seção "Documentação e código".

**Non-Goals:** mexer no assistente de trilhas (App 01), no adaptador Gemini compartilhado em
`nucleo/assistente/`, no formulário de chave, na apresentação da URL ou nos prazos; reescrever
o institucional já publicado em produção.

## Decisions

1. **Documento antes do código.** Documento 03 §8 perde o item do assistente e ganha o link da
   documentação da API na lista da área (continuam quatro coisas); a linha "Acesso das
   aplicações de terceiros" do documento 09 registra a decisão de 2026-11-06 e corta o que
   descrevia o assistente (corpus, recorte, freio, abertura). O doc 99 não muda: nenhuma
   relação entre documentos muda — a linha "Chave de aplicação e Área do Desenvolvedor"
   continua apontando 03 §§1, 8.
2. **No PRD-03, os identificadores retirados somem das tabelas e não são reaproveitados.** O
   `RF-03-67` muda de enunciado; `RF-03-68` a `RF-03-72`, `RF-03-81`, `RN-03-30`, `RN-03-31`,
   `RN-03-38` e `RN-03-39` saem das §§6.6 e 7, e §§3.1, 4, 5.8, 8, 9, 11, 12, 13 e 15 deixam
   de citá-los. Uma linha na §13 registra a retirada com a data, para a rastreabilidade das
   changes arquivadas que os citam. Alternativa descartada: manter as linhas marcadas como
   retiradas — texto morto num documento normativo.
3. **Link do Swagger derivado de `URL_DO_NUCLEO`**, como `${URL_DO_NUCLEO}/docs`, com o rótulo
   "Documentação da API (Swagger)", em nova aba, ao lado dos dois links que já existem.
   `URL_DA_DOCUMENTACAO` e `URL_DO_REPOSITORIO` são constantes porque são iguais em todo
   ambiente; o núcleo não é. Sem `VITE_URL_DO_NUCLEO` declarada o link não aparece, em vez de
   apontar para `/docs` da própria vitrine. Alternativa descartada: ReDoc em `/redoc` — o
   fundador escolheu só o Swagger.
4. **Remoção completa no núcleo**: apagar `nucleo/assistente/desenvolvedor/` e
   `nucleo/corpus_do_desenvolvedor/`, o `include` em `principal.py` e no `conftest.py`, as
   chaves `protecao_freio_assistente_do_desenvolvedor_*` e `corpus_do_desenvolvedor_*` de
   `configuracao.py`, a entrada `assistente_do_desenvolvedor` de `protecao/freio.py`, e os
   testes `test_assistente_do_desenvolvedor.py`, `test_freio_do_assistente_do_desenvolvedor.py`
   e `test_corpus_do_desenvolvedor.py`. Código de erro `assistente_do_desenvolvedor_*` sai com
   o módulo. A rota passa a 404, como qualquer rota inexistente.
5. **Esteira**: sai o passo "Montar o corpus" de `backend-deploy.yml` com o comentário e os passos "Instalar uv" e
   `setup-python`, que nenhum outro passo do workflow usa, o `COPY` do
   corpus no `Dockerfile` e a entrada no `.gitignore`.
6. **Semeadura do institucional**: o rascunho de "Construir sobre a plataforma" troca "traz o
   assistente que responde dúvidas de integração" por "traz a documentação da API". Só vale
   para semeadura nova; o texto já gravado em produção é do Admin, pelo
   `PUT /conteudo-institucional/{secao}`.
7. **Sitemap**: `/desenvolvedor` continua fora do `sitemap.xml` (decisão da fatia 9); só o
   comentário de `descoberta/enderecos.ts` deixa de citar o `RN-03-38` como motivo.

## Risks / Trade-offs

- **Rota removida sem prazo de versão anterior (`RF-01-31`)** → o único consumidor é a App 06,
  que sai no mesmo PR; não há chave de terceiro que a use, e a rota nunca foi contrato de
  leitura de dado.
- **Institucional em produção pode seguir prometendo o assistente** → aviso ao fundador no PR,
  para o Admin editar o texto publicado.
- **Swagger em produção revela as rotas** → já é decisão vigente (documento 09): descreve
  rotas, não devolve conteúdo.
