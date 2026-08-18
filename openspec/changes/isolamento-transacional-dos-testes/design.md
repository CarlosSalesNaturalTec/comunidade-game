## Context

A fixture `sessao` (`backend/tests/conftest.py`) abre uma sessão por teste sobre um engine de
escopo de sessão e, no teardown, executa `TRUNCATE` de todas as tabelas de `Base.metadata`.
O comentário que está no arquivo explica por que é `TRUNCATE` e não `DELETE`: o `DELETE`
dispara o gatilho de linha que recusa remoção em `consentimento` (`RN-01-12`), e o mesmo vale
para `auditoria`, `lancamento`, `ponto_extra` e `ponto_regular`, que têm gatilhos de
imutabilidade equivalentes criados junto com a tabela.

Três detalhes da suíte de hoje condicionam o desenho, e foram confirmados no protótipo:

1. **A aplicação e o teste compartilham a mesma sessão.** A fixture `app` faz
   `dependency_overrides[obter_sessao] = lambda: sessao`, então tudo que a rota grava já está
   na sessão do teste.
2. **Vinte e um pontos abrem uma segunda conexão** por `engine.connect()` ou `engine.begin()`,
   para provar gatilho de banco, restrição de integridade e concorrência. `test_cli.py`
   também monta a própria `sessionmaker` a partir do `engine`.
3. **O middleware de auditoria não usa a injeção de dependência.** `_gravar()` chama
   `obter_fabrica_de_sessao()` de `nucleo.banco` e commita numa sessão própria, de propósito —
   é gravação _best-effort_, que não pode ser desfeita pela transação da requisição.

## Goals / Non-Goals

**Goals:**

- Suíte completa abaixo de 90 s sem perder cobertura nem cenário.
- Custo do isolamento deixa de crescer com o número de tabelas.
- Cada teste continua partindo de um banco vazio, com a mesma garantia de hoje.

**Non-Goals:**

- Paralelizar a suíte (`pytest-xdist`): é ganho independente, exige um banco por _worker_ e
  uma dependência nova de desenvolvimento — decisão do fundador, em outra fatia.
- Reduzir o número de testes, agrupar cenários ou trocar teste de rota por teste de unidade.
- Mudar `backend/src/`, migração, esteira de CI ou qualquer regra de produto.

## Decisions

**1. Transação desfeita no fim, em vez de `TRUNCATE`.** A fixture `conexao` abre uma conexão,
inicia uma transação e a desfaz no teardown; `sessao` é construída com `bind=conexao` e
`join_transaction_mode="create_savepoint"`, de modo que os `commit()` que os testes e as rotas
fazem virem `SAVEPOINT` dentro dessa transação. Nada chega ao banco, nada precisa ser apagado
e nenhum gatilho de imutabilidade é acionado — o motivo original do `TRUNCATE` desaparece em
vez de ser contornado. _Alternativa descartada:_ `TRUNCATE` só das tabelas que o teste tocou —
exigiria rastrear escrita a cada teste e continuaria custando uma ida ao banco.

**2. Uma conexão por teste, exposta como fixture.** O SQL cru dos testes passa a rodar na
mesma conexão da sessão: `engine.connect()` vira o uso direto de `conexao` e `engine.begin()`
vira `conexao.begin_nested()`. É o que mantém visível, para o SQL cru, o dado que a sessão
gravou — e é também o que garante que ele seja desfeito junto. _Alternativa descartada:_
manter o `engine` nesses testes e limpar só eles por `TRUNCATE` — o dado da sessão continuaria
invisível para a segunda conexão, e os testes de gatilho passariam a mentir.

**3. A fábrica de sessão do middleware é substituída no teste.** Uma fixture troca
`obter_fabrica_de_sessao` de `nucleo.banco` por uma fábrica presa à `conexao` do teste,
enquanto o teste dura. O middleware continua abrindo e commitando a própria sessão — o
comportamento _best-effort_ que o PRD-01 pede não muda —, só que dentro da transação do teste.
_Alternativa descartada:_ fazer o middleware aceitar a sessão da requisição — mudaria o
comportamento de produção para servir ao teste, o que a hierarquia de autoridade não permite.

**4. Marcador `banco_compartilhado` para o que precisa de dado gravado.** O teste que depende
de duas conexões enxergando o mesmo dado — hoje só o da criação simultânea do terceiro vínculo
do responsável — declara `@pytest.mark.banco_compartilhado`, recebe sessão presa ao `engine` e
paga o `TRUNCATE` no fim. O marcador é registrado em `pyproject.toml` e a exceção fica
explícita no código, em vez de virar um `engine` solto.

**5. `RESTART IDENTITY` some junto.** Nenhum modelo usa coluna de identidade nem `Sequence`:
todas as chaves são `Uuid`. A cláusula não tinha efeito e não é reproduzida no caminho do
marcador.

## Risks / Trade-offs

- **Teste que dependa de estado realmente commitado passa a falhar** → o protótipo rodou a
  suíte inteira e mostrou exatamente quais são: 17 falhas, todas nas três categorias tratadas
  pelas decisões 2, 3 e 4. A conversão termina com a suíte inteira verde, o que fecha o risco.
- **`create_savepoint` altera o significado de `rollback()` dentro do teste** — o teste que
  espera um `rollback()` desfazer tudo passa a desfazer até o savepoint. Nenhum teste de hoje
  depende disso, e a conversão confirma teste a teste.
- **A conexão única serializa o que hoje é concorrente** → é o que a decisão 4 preserva pelo
  marcador, para o único caso que precisa.
- **O gatilho de imutabilidade deixa de ser exercitado pelo teardown.** Ele nunca foi teste:
  os testes que o provam são explícitos e continuam existindo, agora dentro da transação.
