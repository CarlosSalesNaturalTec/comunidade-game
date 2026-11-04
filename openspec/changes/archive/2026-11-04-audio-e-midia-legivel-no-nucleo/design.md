# Design

## Context

Ver `proposal.md` — Why. O que molda a abordagem é o que já existe no núcleo:

| Peça | Estado hoje |
| --- | --- |
| `TipoDeProducaoDaCriacaoOriginal` | cinco valores, `Enum(native_enum=False, length=16)` — **VARCHAR**, não enum nativo |
| Mídia da criação original | `POST` e `PATCH` de `/criacoes/{id}/arquivo`; **nenhum `GET`** |
| Mídia do conteúdo da missão | `POST`, `PATCH` **e `GET`** — o molde pronto |
| `ProducaoDaMissao` | sem coluna de mídia; o modelo diz "sem coluna de foto, de áudio nem de custo" |
| Portão público da criação | `condicoes_de_criacao_publica`, aplicado só à **listagem** |

A sessão de envio retomável em partes já existe e serve conteúdo e criação original. Nada
disso precisa ser inventado — precisa ser estendido.

## Goals / Non-Goals

**Goals:**

- Áudio como sexto tipo de produção **do aluno**, sem tocar o conteúdo do Mestre.
- Mídia da criação original legível: uma rota autenticada e uma pública.
- `ProducaoDaMissao` com mídia guardada, por sessão de envio, e legível.

**Non-Goals:**

- Nenhuma aplicação muda nesta fatia. As telas vêm nas fatias 13, 26, 27 e 12.
- Nenhuma transcodificação, compressão, miniatura ou limite de duração de áudio.
- Nenhuma rota pública para a mídia da **produção da missão** — ela não é item de acervo.
- A comprovação do desafio prático e os dois vereditos: fatias 13 e 27.

## Decisions

### 1. A transcrição continua, e o áudio passa a ser guardado ao lado dela

O fundador decidiu "guardar mídia na atividade da missão e nos desafios", sem dizer o que
acontece com a transcrição feita no aparelho. **Mantemos as duas.**

Não é escolha de conveniência: a devolutiva construtiva é feita **sobre texto**, e o núcleo
`NEVER SHALL transcrever fala` — regra que esta change não reverte. Se a transcrição parasse,
a entrega falada ficaria sem texto algum e a devolutiva morreria, revertendo por tabela um
requisito que ninguém mandou reverter. Guardar o áudio é **aditivo**; substituir a transcrição
por ele seria subtrativo.

_Alternativa descartada:_ o núcleo transcrever o áudio recebido. Criaria custo por ato, que o
`RF-09-90` não mede, e dependência de serviço externo — decisão nova, fora desta fatia.

### 2. Duas rotas para a mídia da criação, não uma com autenticação opcional

`GET /v1/criacoes/{id}/arquivo` (com sessão) e uma rota pública separada.

Uma rota só, com sessão opcional, teria de decidir o portão pelo que o chamador apresenta — e
é exatamente esse tipo de ramo que deixa passar byte de criança por engano. Duas rotas têm
cada uma **um** portão, e o portão público é o mesmo objeto já usado pela listagem,
`condicoes_de_criacao_publica`, em vez de uma segunda cópia da regra que pode divergir dela.

### 3. A rota pública responde 404, nunca 403

Distinguir "não existe" de "existe e não pode aparecer" transforma a rota em oráculo sobre
quais crianças têm autorização — o que o `RN-01-22` já veda para o nick. Mesmo corpo, mesmo
código, nos dois casos.

### 4. A mídia da produção espelha a da criação original

`referencia` (`String(512)`) e `tamanho` (`Integer`), os mesmos nomes e tipos que
`CriacaoOriginal` já usa, servidos pela mesma `PortaDeArmazenamento`. Um vocabulário de mídia
no núcleo, não dois.

### 5. O sexto valor do enum não pede DDL

`Enum(..., native_enum=False, length=16)` é **VARCHAR(16)**, e o `create_constraint` do
SQLAlchemy é `False` por padrão: não há CHECK no banco, e a validação do conjunto é Python.
`"audio"` cabe nos 16. **A migração é só das colunas de mídia da produção.** O apply confere
isso contra o esquema vivo antes de assumir — se houver CHECK, a migração o recria.

_Alternativa descartada:_ enum nativo do Postgres. Daria `ALTER TYPE ... ADD VALUE`, que não
roda em transação em versões mais velhas, e o repositório já escolheu não usá-lo.

### 6. Produção antiga não ganha mídia retroativa

Produção gravada antes desta change não tem arquivo — ele nunca foi gravado. A leitura
responde **404**, e não há _backfill_ possível. É consequência aceita da regra que vigorava.

### 7. A mídia da produção é guardada do que já chega, sem sessão de envio

Descoberto no apply, e **corrige a spec que eu havia escrito por analogia**: a produção da
missão não usa sessão retomável. As duas rotas são `multipart/form-data` com `UploadFile`, e a
foto **precisa** chegar inline, porque é dela que o núcleo tira a transcrição por OCR. Os bytes
já estão no núcleo no ato do registro.

Guardar passa a ser, literalmente, **não descartar o que já se recebeu** — uma linha de
`gravar`, não uma máquina de envio nova. O áudio entra pelo mesmo campo `arquivo`, ao lado da
transcrição em `texto`.

_Alternativa descartada:_ sessão de envio em ato próprio, como a criação original tem. Mudaria
o contrato das duas rotas da App 01 sem necessidade, e a foto teria de chegar duas vezes — uma
para o OCR e outra para a guarda. A spec e a tarefa 5.4 foram corrigidas.

### 8. A criação original ganha a coluna do tipo MIME

Descoberto no apply: `CriacaoOriginal` guarda `referencia` e `tamanho`, e **não** o tipo MIME —
o `tipo_mime` ia só para a sessão de envio. Sem ele, a leitura devolveria sempre
`application/octet-stream` e nenhum navegador renderizaria a mídia. Entra
`tipo_do_arquivo`, espelhando `ConteudoDaMissao`, gravada na confirmação a partir do
`EnvioConsultado.tipo_mime` — que o armazenamento apura, nunca o cliente declara. A migração,
que já existia para a produção, cobre as duas tabelas.

## Risks / Trade-offs

- **A mídia da produção da missão nasce sem portão público, mas nasce guardada.** Uma fatia
  futura que resolva expô-la encontrará o arquivo lá. → A spec diz `NEVER SHALL` haver rota
  pública para ela, e o teste afirma a ausência; expor exige decisão do fundador, não um
  `GET` a mais.
- **Guardar foto e áudio de criança muda o perfil de retenção do projeto.** → Fora do escopo
  desta fatia mexer no documento 03 §12 ou no inventário da LGPD do PRD-01 §11; mas o apply
  deve conferir se a tabela de dados pessoais do PRD-01 §11 precisa da linha nova. Anotado
  como tarefa, não como suposição.
- **Áudio sem limite de tamanho ou duração.** O envio em partes aguenta, o armazenamento
  cresce. → Nenhum limite novo é inventado aqui; o que vale é o limite de envio já vigente.
- **Dois avisos de `openspec validate`** sobre descrição longa, nos dois requisitos de entrega
  da produção. → É texto preexistente, carregado inteiro ao renomear o requisito; dividi-lo
  exigiria change feita para isso, e as regras do OpenSpec desaconselham fazê-lo de passagem.

## Migration Plan

1. Migração Alembic: `referencia` e `tamanho` em `producao_da_missao`, ambas _nullable_ —
   nenhuma linha existente precisa de valor.
2. `downgrade` derruba as duas colunas. O sexto valor do enum não tem DDL a desfazer; voltar
   atrás no código basta, e nenhuma criação terá sido gravada com `audio` antes do deploy.
3. Sem janela de indisponibilidade: tudo é aditivo e _nullable_.

## Open Questions

Nenhuma que possa esperar. A única dúvida real — o destino da transcrição — está resolvida na
decisão 1, porque deixá-la aberta mudaria as specs.
