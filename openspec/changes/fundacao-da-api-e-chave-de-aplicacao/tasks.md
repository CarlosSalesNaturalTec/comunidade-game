## 1. Pasta do backend e esteira de CI

- [ ] 1.1 Criar `backend/` conforme o documento 03 §1.2, com a estrutura de `design.md` —
      `src/nucleo/`, `alembic/` e `tests/`. Verificável: a árvore existe e nenhuma pasta nova
      de topo foi criada no repositório
- [ ] 1.2 Criar `backend/pyproject.toml` com Python 3.12, as dependências e a configuração do
      Ruff nos conjuntos `E`, `F`, `I`, `UP` e `B`. Verificável: `ruff check .` e
      `ruff format --check .` rodam na pasta e passam
- [ ] 1.3 Configurar o pytest no mesmo `pyproject.toml`, com medição de cobertura publicada no
      log e **sem limiar que bloqueie**. Verificável: `pytest` roda e imprime a cobertura sem
      falhar por causa dela
- [ ] 1.4 Criar `backend/Dockerfile` portátil, sem dependência de serviço do Google Cloud, como
      o documento 03 §1.13 exige. Verificável: a imagem constrói e sobe localmente
- [ ] 1.5 Criar `.github/workflows/backend-ci.yml`, disparado **só** por `backend/**`, rodando
      `ruff format --check`, `ruff check` e `pytest`, as três bloqueando o merge, com
      PostgreSQL como serviço para os testes que tocam banco. Verificável: o workflow roda no
      PR e não dispara em mudança que só toque `docs/`

## 2. Convenções da API

- [ ] 2.1 Montar a aplicação FastAPI com todas as rotas de dados sob o prefixo `/v1`
      (`RF-01-01`). Verificável: rota de dados registrada fora do prefixo não existe
- [ ] 2.2 Implementar o corpo único de erro — `codigo`, `mensagem` em linguagem simples e
      `campo` quando couber — substituindo os três manipuladores do FastAPI: validação,
      `HTTPException` e falha não tratada (`RF-01-27`). Verificável: 404, 422 e 500 saem no
      mesmo formato
- [ ] 2.3 Criar o catálogo de códigos de erro em `erros.py` como fonte única, com as entradas
      que esta change usa (`RF-01-27`). Verificável: nenhuma rota declara código solto
- [ ] 2.4 Garantir que o 500 registre o rastro no log e devolva ao cliente só código e
      mensagem, sem rastro de pilha, nome de tabela, consulta ou caminho de arquivo
      (`RF-01-27`). Verificável: teste que provoca falha e inspeciona o corpo
- [ ] 2.5 Implementar o contrato de paginação por cursor opaco e os filtros de comunidade,
      período e persona, com página padrão de 25 e teto de 100 em configuração (`RF-01-28`).
      Verificável: o contrato é reutilizável e ainda não tem listagem que o exercite
- [ ] 2.6 Recusar com 422, nomeando o parâmetro, tamanho de página acima do teto e filtro não
      declarado pela rota (`RF-01-28`). Verificável: nenhum parâmetro desconhecido é ignorado
      em silêncio
- [ ] 2.7 Exigir fuso em toda data e hora de entrada e saída, e guardar a data do fato distinta
      da data do registro (PRD-01 §9). Verificável: data e hora sem fuso recebe 422 nomeando o
      campo
- [ ] 2.8 Publicar o schema OpenAPI e a interface **fora do prefixo `/v1` e sem chave**,
      conforme o documento 03 §1.1 (`RF-01-30`). Verificável: `/openapi.json` responde sem
      cabeçalho de chave

## 3. Chave de aplicação

- [ ] 3.1 Modelar `ChaveDeAplicacao` com os atributos do PRD-01 §8, incluindo `ambiente` e
      `natureza`, guardando **apenas o resumo criptográfico** do segredo (`RN-01-35`).
      Verificável: não há coluna que receba segredo em claro
- [ ] 3.2 Escrever a migração inicial com unicidade sobre aplicação e ambiente entre as chaves
      vigentes e índice pelo identificador público (`RF-01-54`). Verificável: a migração sobe e
      desce, e o banco volta a vazio
- [ ] 3.3 Implementar a geração do segredo no formato `cg_<ambiente>_<id>.<segredo>`, com 256
      bits aleatórios e resumo SHA-256 (`RN-01-35`). Verificável: dois segredos gerados nunca
      coincidem e o resumo não é reversível
- [ ] 3.4 Implementar a conferência da chave no cabeçalho `X-Chave-Aplicacao`, aplicada a toda
      rota de dados sob `/v1` e **somente** a elas (`RF-01-48`, `RN-01-32`). Verificável:
      chamada sob `/v1` sem chave recebe 401 e nada da rota executa
- [ ] 3.5 Implementar o caminho único de recusa do `design.md`: sempre calcular o resumo e
      comparar em tempo constante, sem ramo curto para chave ausente, inexistente, divergente,
      de outro ambiente ou revogada (`RF-01-48`). Verificável: os cinco casos convergem para o
      mesmo ponto de saída
- [ ] 3.6 Conferir o ambiente da chave contra o ambiente de partida do núcleo (`RF-01-54`).
      Verificável: chave de desenvolvimento apresentada ao núcleo de produção recebe 401
- [ ] 3.7 Implementar a distinção entre rota pública e rota autenticada, em que a pública
      dispensa a credencial de persona e nunca a chave (`RF-01-02`, `RN-01-34`). Verificável:
      declarar uma rota como pública não a tira de trás da chave
- [ ] 3.8 Garantir que a chave não atribua persona nem autorize escrita, qualquer que seja a
      natureza dela (`RN-01-33`, `RN-01-34`). Verificável: o contexto da requisição pública não
      carrega persona alguma
- [ ] 3.9 Implementar o comando de semeadura convergente: uma chave vigente por aplicação e por
      ambiente, imprimindo o segredo **uma única vez** na criação e nada quando já existe
      (`RF-01-54`, `RN-01-35`). Verificável: rodar duas vezes não duplica, não reemite e não
      imprime segredo de novo
- [ ] 3.10 Semear as oito aplicações do projeto com natureza "do projeto" e **sem prazo de
      apresentação de URL** (`RF-01-54`). Verificável: nenhuma das oito é cobrada por URL nem
      revogada por decurso de prazo

## 4. Verificação contra os critérios de aceite

- [ ] 4.1 Testar que a chamada sob `/v1` com chave vigente é processada e a sem chave recebe
      401 (`RF-01-48`, critério do PRD-01 §12)
- [ ] 4.2 Testar que consulta pública sem chave recebe 401, ainda que não exija credencial de
      persona (`RN-01-32`, critério do PRD-01 §12)
- [ ] 4.3 Testar que chave ausente, inexistente e revogada produzem **corpo idêntico**, sem
      distinguir o motivo (`RF-01-48`, critério do PRD-01 §12)
- [ ] 4.4 Testar que o tempo de resposta dos três casos não os denuncia, medindo a dispersão
      entre eles (spec de `chave-de-aplicacao`). Verificável: teste que falha se um caso for
      sistematicamente mais rápido
- [ ] 4.5 Testar que a chave revogada perde o acesso na chamada seguinte, sem tolerância
      (`RF-01-48`)
- [ ] 4.6 Testar que uma segunda leitura de chave já emitida nunca recupera o segredo e que
      nenhum registro operacional o contém em claro (`RN-01-35`, critério do PRD-01 §12)
- [ ] 4.7 Testar que semear o mesmo ambiente duas vezes mantém as chaves vigentes intactas
      (`RF-01-54`)
- [ ] 4.8 Testar que o schema OpenAPI responde sem chave, descreve rotas sem servir dado de
      domínio, e que ler o schema não abre as rotas de dados que ele descreve (`RF-01-30`,
      `RN-01-32`)
- [ ] 4.9 Testar que 404, 422 e 500 saem no corpo único, com campo em falta nomeado apenas no
      erro de validação (`RF-01-27`)
- [ ] 4.10 Testar que data e hora sem fuso é recusada e que a data do fato sobrevive a um envio
      atrasado (PRD-01 §9)

## 5. Documentação

- [ ] 5.1 Conferir que as decisões desta change seguem refletidas no documento 03 §§1, 1.1 e
      1.13, no documento 09 e no PRD-01 — gravadas antes da change, e nada mais mudou desde
      então. Verificável: nenhuma decisão do `design.md` ficou sem origem em documento
- [ ] 5.2 Conferir que `docs/prds/index.md` e o documento 99 seguem corretos: a situação do
      PRD-01 é de aprovação do requisito, não de implementação, e nenhuma relação entre
      documentos mudou. Verificável: os dois seguem sem alteração, e isso é a conclusão
- [ ] 5.3 Conferir que nenhum arquivo novo entrou em `docs/` — o plano de execução fica na
      change, não na documentação do produto. Verificável: a `nav` do `mkdocs.yml` não precisa
      de entrada nova
- [ ] 5.4 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR.
      Verificável: os três passam
