## Context

Ver `proposal.md` — Why. O que o núcleo já tem e molda o desenho:

- A `Credencial` existe com três tipos (`biometria`, `login_social`, `usuario_e_senha`), um
  `identificador`, um `segredo` e um índice único parcial
  `uq_credencial_identificador_por_tipo_ativa` sobre `(tipo, identificador)` onde `ativa`.
- A chave de aplicação já resolveu segredo devolvido uma única vez: `gerar_segredo` com 256 bits,
  `calcular_resumo` em SHA-256, comparação por `hmac.compare_digest` e resumo fantasma para o
  tempo de resposta não denunciar a inexistência do registro.
- A rota `POST /registros-de-coleta` recebe `serie_de_coleta_id` no corpo e hoje exige sessão de
  persona por `exigir_permissao(Operacao.seus_registros_de_coleta, "escreve")`.
- `Operacao` espelha **célula a célula** a matriz do PRD-01 §4 — o vocabulário é dado, não
  decisão espalhada pelas rotas.
- `registro_de_coleta` é particionada por tempo, como manda o documento 03 §1.

## Goals / Non-Goals

**Goals:**

- Autenticar o sensor por chamada, sem sessão, sem ampliar direito e sem criar entidade de
  dispositivo.
- Acomodar `RN-01-53` no esquema, e não só na regra de aplicação.
- Manter a rota de registro única, como o PRD-08 §9 determina.

**Non-Goals:**

- A queda ao fim do vínculo (`RF-01-68`, segunda metade) — ver `proposal.md`.
- Qualquer leitura pela credencial. Ela não tem rota de consulta, nem da própria série.
- Provisionamento, calibração ou telemetria do aparelho. A credencial é o registro dele, e o
  núcleo não sabe mais nada sobre o sensor.

## Decisions

### O par identificador + série é a chave de busca da credencial

`RN-01-53` parece uma restrição de integridade e é, antes disso, o **índice de busca**. O
identificador é do **aparelho** e se repete entre séries; sozinho, não localiza credencial. A
série vem no corpo da chamada de registro. Logo a busca é `(identificador, série, ativa)`, e é
exatamente o par que a regra declara único — é o que torna a busca determinística.

O sensor apresenta `X-Credencial-Dispositivo: <identificador>.<segredo>`, na mesma forma composta
que `X-Chave-Aplicacao` já usa.

Descartadas: identificador único global no núcleo — contraria "todas com o mesmo identificador"
do documento 03 §1.1; id próprio da credencial no cabeçalho — funciona, mas deixaria `RN-01-53`
sem função e obrigaria o aparelho a guardar um id por série além do seu identificador.

### O identificador do aparelho é declarado na emissão, nunca gerado pelo núcleo

Não há entidade de dispositivo onde alocar um identificador, e a segunda credencial do mesmo
aparelho tem de **repetir** o valor da primeira. Quem emite informa o identificador; o núcleo
gera apenas o segredo.

Descartada: gerar o identificador na emissão — tornaria impossível o mesmo aparelho alimentar
duas séries com o mesmo identificador.

### O índice único da `Credencial` se divide por tipo

O índice de hoje sobre `(tipo, identificador)` onde `ativa` **proibiria** o mesmo aparelho em duas
séries. Ele passa a excluir o tipo `dispositivo`, e nasce um índice parcial próprio, único sobre
`serie_de_coleta_id` onde `ativa` e `tipo = 'dispositivo'` — "nunca duas vivas para a mesma série"
(documento 03 §1.1), que já implica a unicidade do par.

Descartada: índice sobre `(tipo, identificador, serie_de_coleta_id)` — deixaria passar duas
credenciais vivas na mesma série com identificadores diferentes, que é o que a regra proíbe.

### A conferência do dispositivo é dependência própria e não devolve contexto de sessão

Vive ao lado da conferência de persona em `autenticacao.py`, mas devolve um contexto próprio — a
credencial e o coletor da série —, nunca `ContextoDaSessao`. É o que impede, por construção, a
credencial escorregar para qualquer rota que espere persona.

### A rota de registro é uma só, com dois autenticadores

O PRD-08 §9 é explícito: "mesma rota, autenticada por credencial de dispositivo". Uma dependência
resolve qual dos dois autenticou e entrega ao caso de uso o coletor, a credencial quando houver e
as origens admitidas — `manual` e `voz` para a sessão, `sensor` para o dispositivo.

Descartada: rota separada para o sensor — contraria o PRD-08 §9 e duplicaria toda a regra do
registro, que é a mesma para as duas origens.

### A autoria do registro continua sendo do coletor

`autor_id` e `papel_do_autor` recebem o **Guerreiro(a) coletor** da série, como no registro
manual; o aparelho aparece na coluna nova `credencial_id`, que é o atributo `dispositivo` do
PRD-08 §8. Assim `RN-08-11` — vínculo permanente com o coletor — vale igual para as duas origens,
e nenhuma escrita fica sem autor.

### A emissão e a revogação entram como item novo da linha do Mestre na matriz

`Operacao` tem uma entrada por item de célula do PRD-01 §4. A decisão do fundador — Admin ou o
**Mestre autor do desafio** — vira item novo na linha do Mestre daquela tabela, junto com as
demais atualizações de `docs/` que a decisão exige.

Descartada: reaproveitar `suas_trilhas_e_conteudos` — a credencial não é conteúdo de trilha, e o
reaproveitamento esconderia o escopo em vez de declará-lo.

A escrita por dispositivo **não ganha entrada na matriz**: ela não é persona, e o alcance dela
está declarado na spec de permissões como a exceção de uma única operação.

### O segredo reaproveita os utilitários da chave

`gerar_segredo` e `calcular_resumo` não têm nada de específico da chave de aplicação. A
conferência repete o padrão do resumo fantasma com `hmac.compare_digest`, para que credencial
inexistente e segredo errado custem o mesmo tempo.

## Risks / Trade-offs

- **Segredo vazar em log ou em mensagem de erro** → nunca registrar o cabeçalho; a recusa não
  ecoa o valor apresentado. Teste cobre a ausência do segredo em resposta e em registro
  operacional.
- **A exceção de escrita sem persona virar brecha** → a dependência do dispositivo é aceita
  **apenas** na rota de registro, e a spec de permissões declara o alcance de uma operação. Teste
  cobre a tentativa da credencial em outra rota de escrita e em rota de consulta.
- **Sensor com relógio errado** → nada novo: a medição no futuro já é recusada e o valor fora da
  faixa já entra "a conferir", venha de digitação ou de sensor (PRD-08 §14).
- **Aparelho compartilhado entre Guerreiros e Guerreiras** → a credencial é por série, e a série
  é individual; um aparelho que sirva a dois coletores tem duas credenciais, cada uma presa à sua
  série. Nenhuma delas alcança a série da outra.
- **O `RENAMED` do requisito de origem no arquivamento** → `openspec validate --strict` aceita a
  combinação de `RENAMED` com `MODIFIED`; conferir o resultado no `/opsx:verify` antes de
  arquivar, porque não há precedente de `RENAMED` nas changes já arquivadas.

## Migration Plan

1. Migração do esquema: colunas novas da `Credencial` — `serie_de_coleta_id`, `trilha_id`,
   `revogada_por`, `motivo_da_revogacao`, `revogada_em` —, todas anuláveis, e a troca dos índices
   descrita acima.
2. Coluna `credencial_id` em `registro_de_coleta`, anulável. `ADD COLUMN` anulável em tabela
   particionada propaga às partições sem reescrever dado.
3. Código: tipo novo no enum, conferência, dependência, rotas de emissão e revogação, origem
   `sensor` liberada na rota de registro.
4. Reversão: as colunas são anuláveis e o tipo `dispositivo` não existe nas credenciais já
   gravadas, de modo que reverter a migração não perde dado das três espécies em uso.
