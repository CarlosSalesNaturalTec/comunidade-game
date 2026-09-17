PRD-04 (App 01 — Aula presencial), com alcance no PRD-01 (núcleo). Linha **sem número** no
bloco do PRD-04 do `openspec/cronograma-de-fatias.md` — correção de defeito preexistente sobre
as fatias 3 e 4, ambas `implementado`, não fatia de requisito novo. Atende `RF-04-13`,
`RF-04-14`, `RF-04-20`, `RF-04-48`, `RF-01-05`, `RF-01-07`, `RN-01-14` e `RF-01-02`.

## Why

A captura da imagem do onboarding **nunca funcionou**: o núcleo espera um descritor de **128**
posições, declarado à mão na implantação, e a `comum/biometria` gera o descritor de **1024** do
modelo `faceres` da Human. Toda captura responde 422 desde 2026-08-29, e nenhum _template_
jamais foi gravado em produção.

O número errado sobreviveu um mês porque a tela **apaga a mensagem do núcleo**: a
`TelaDeCaptura` troca qualquer 422 pela frase "O consentimento ainda não foi registrado", e o
Mestre leu semanas de erro de consentimento diante de um erro de dimensão.

A causa de fundo é de desenho: a dimensão foi tratada como parâmetro de implantação calibrável
— o que ela não é. Ela é fato da biblioteca decidida no documento 03, e foi declarada **17 dias
antes** de essa biblioteca entrar no projeto, sem nada no repositório que reconciliasse os dois.

## What Changes

- **BREAKING (implantação)**: a dimensão do descritor deixa de ser variável de ambiente e vira
  **constante do núcleo**, com a origem documentada. `CG_BIOMETRIA_DIMENSAO_DO_DESCRITOR` e o
  secret `cg-biometria-dimensao-do-descritor` deixam de existir. Decisão do fundador,
  2026-09-17. O núcleo passa a aceitar o descritor que a aplicação realmente gera.
- A `TelaDeCaptura` apresenta a **mensagem do núcleo**, como a `TelaDoTermo` ao lado já faz — a
  recusa por consentimento e qualquer outra deixam de ser a mesma frase.
- O documento 09 separa os dois parâmetros da entrada do Guerreiro(a): o **limiar** continua
  calibrado no encontro real; a **dimensão** sai da lista.

O **limiar de comparação** (`cg-biometria-limiar-de-comparacao`) fica **fora**: ele também está
errado, mas o valor correto exige medição empírica e vai em change própria, logo em seguida.
Também ficam fora, por serem fatia própria: o laço de detecção no lugar do quadro único em
`comum/biometria`, e a `RF-04-16` (captura de quem já se cadastrou sem imagem), que a spec
vigente adia de forma declarada.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `template-biometrico`: o Requirement "Ao núcleo chega descritor, nunca imagem" passa a
  declarar que a dimensão esperada é a da biblioteca decidida no documento 03, fixada no
  núcleo, e NEVER parâmetro de implantação.
- `aplicacao-da-aula-presencial`: o Requirement "O termo é exibido e a assinatura é
  testemunhada antes da captura" passa a exigir que a tela explique **a recusa que o núcleo
  deu**, em vez de atribuir toda recusa ao consentimento.

A `camada-de-acesso-comum` **não muda**: o Requirement "A camada apresenta o erro do núcleo no
corpo único do PRD-01" já proíbe substituir a recusa por texto próprio, e a camada cumpre —
`ErroDaApi.message` carrega a mensagem do núcleo. O defeito está na tela, que a descarta.

## Impact

- `backend/src/nucleo/configuracao.py`: sai `biometria_dimensao_do_descritor`.
- `backend/src/nucleo/biometria/regra.py`: constante nova; a conferência de dimensão e o
  `_template_de_descarte` passam a lê-la.
- `apps/app-01-aula-presencial/src/onboarding/TelaDeCaptura.tsx`: apresenta a mensagem do
  núcleo.
- Testes do backend que declaram a dimensão em fixture: `conftest.py`, `test_configuracao.py`,
  `test_portas_de_ia.py`, `test_armazenamento_porta.py`.
- `backend/README.md`: a variável sai da lista das sem valor padrão.
- `docs/03-plataforma-e-arquitetura.md` §3.3: o documento-fonte da biometria passa a declarar
  que a dimensão é fato da biblioteca, fixo no núcleo.
- `docs/09-topicos-em-aberto-e-sugestoes.md`: a linha "Parâmetros da entrada do Guerreiro(a)" e
  a decisão nova de 2026-09-17.
- **Sem migração Alembic**: `credencial.segredo` é `Text` e comporta o cifrado de 1024 floats
  (~27 KB), e não há _template_ em produção para migrar.
- **Ato de implantação**, fora do alcance da sessão de implementação: apagar o secret
  `cg-biometria-dimensao-do-descritor` e retirá-lo do mapeamento `GCP_SECRETOS_CG`. Enquanto
  não for feito, o serviço sobe com uma variável que ele ignora — não quebra, mas mantém em
  produção um segredo sem dono.
