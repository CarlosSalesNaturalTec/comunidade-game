## Context

Ver `proposal.md` — Why. O que já existe, da fatia anterior: middleware que confere a chave de
aplicação em toda rota sob `/v1`, corpo único de erro, contrato de paginação, `Configuracao` com
prefixo `CG_`, sessão de banco por requisição e um comando de implantação que semeia as chaves.
Nada disso muda aqui; esta fatia se pendura no que está pronto.

Restrições que moldam o desenho: a plataforma é **instância única**, com a comunidade como
vínculo nos registros; a escrita é sempre autenticada e auditada; o núcleo nunca recebe imagem
nem devolve _template_ — mas isso é da fatia 4, e nada aqui pode fechar aquela porta.

## Goals / Non-Goals

**Goals**

- Deixar a sessão, o papel e a comunidade disponíveis a qualquer rota, para que as fatias
  seguintes só declarem o que exigem.
- Fazer a matriz de permissões do PRD-01 §4 ser conferível por teste, não por leitura de código.
- Deixar `Credencial` pronta para receber o tipo biometria na fatia 4 sem migração de estrutura.

**Non-Goals**

- Renovação de sessão sem reautenticar: não está no PRD.
- Rotas de cadastro de persona: são do PRD-02.
- Trilha de auditoria consultável: `RF-01-29`, de outra fatia. Aqui grava-se a autoria; ninguém
  a consulta ainda.

## Decisions

### O token de sessão é opaco e conferido no banco, não um JWT

`DELETE /v1/sessoes/atual` precisa **encerrar** de verdade, e a entidade `Sessao` do PRD-01 §8 já
guarda `encerrada em`. Um JWT autocontido continuaria válido até expirar, ou exigiria consulta ao
banco a cada chamada — que é justamente o custo que ele existe para evitar. Então o token é
aleatório e opaco, e o núcleo guarda o **resumo** dele, como faz com o segredo da chave.

Alternativa descartada: JWT com lista de revogados — mesma consulta ao banco, mais peças.

### A senha usa função de derivação, não o SHA-256 das chaves

A fatia anterior decidiu SHA-256 para o resumo do segredo da chave, e a razão está registrada
lá: o segredo tem 256 bits de entropia aleatória. **Senha de pessoa não tem**, então aqui entra
Argon2id (`argon2-cffi`), com o custo em parâmetro de configuração. Aplicar a mesma escolha da
chave à senha seria ler mal aquela decisão.

Alternativa descartada: bcrypt — serviria, mas limita a senha a 72 bytes e não tem o parâmetro
de memória.

### O fluxo social acontece no aparelho; o núcleo verifica o token

A aplicação faz o fluxo com o Google e envia o _ID token_ ao núcleo, que confere assinatura,
audiência e validade contra o JWKS do Google e casa a identidade com a persona. É o que a rota
`POST /v1/sessoes/social` ser **pública** já implica: ela não tem credencial de persona a
apresentar, tem um token a provar. Biblioteca: `google-auth`, do próprio provedor já decidido no
documento 03.

Alternativa descartada: o núcleo conduzir o _redirect_ — obrigaria oito aplicações em endereços
próprios a passar por ele, e o documento 03 as quer independentes.

### Persona em tabela única, com o papel como discriminador

O PRD-01 §8 nomeia Guerreiro(a), Mestre, Apoiador, Admin e Responsavel no bloco de identidade,
mas o que a sessão, a matriz e a autoria referenciam é sempre "a persona". Uma tabela `persona`
com o papel, e os atributos próprios de cada papel em tabela satélite, conforme cada fatia os
trouxer. Evita cinco chaves estrangeiras em `Sessao` e `Credencial`.

Alternativa descartada: tabela por papel — duplicaria os vínculos de sessão e credencial cinco
vezes.

### `Credencial` já nasce com o tipo do PRD-01 §8

Uma tabela, com `tipo` em (biometria, login social, usuário e senha), como o PRD-01 §8 define.
Esta fatia usa dois dos três; o terceiro chega na fatia 4 sem alterar a estrutura. `troca
pendente` e `ativa` são colunas desde já, porque `RF-01-12` e `RN-01-18` dependem delas.

### A matriz de permissões é dado, não código espalhado

Uma estrutura declarativa que espelha a tabela do PRD-01 §4 — papel × operação —, conferida por
uma dependência única, e um teste que percorre a matriz inteira comparando com aquela tabela.
`RF-01-16` exige a conferência "em toda operação": com decorador por rota, a rota esquecida
passa despercebida; com dependência única, o padrão é negar.

Alternativa descartada: decorador por rota — falha por omissão, que é o modo de falha errado
para permissão.

### O filtro por comunidade é declarado pela rota e aplicado na consulta

Cada rota de dado de comunidade declara se o filtro é obrigatório. Faltando onde é obrigatório,
o núcleo responde 422 pelo corpo de erro único da fatia anterior, indicando o campo em falta.
`ComunidadeVirtual` nasce com os atributos que o PRD-08 §8 define, sem nenhuma rota: quem a cria
e a mantém é aquele PRD.

### A semeadura do Admin fundador estende o comando que já existe

O mesmo comando de implantação que semeia as chaves passa a convergir também a persona Admin do
fundador, lendo a identidade social de `CG_IDENTIDADE_FUNDADOR`. Convergir, não inserir — rodar
duas vezes não duplica, como já vale para as chaves. Sem a variável declarada, o comando falha
de forma visível em vez de criar meio ambiente.

### A duração da sessão não tem valor padrão no código

`CG_SESSAO_ADULTO_DURACAO` é configuração **obrigatória**, sem valor padrão: o ambiente que não
a declarar não sobe. É a tradução literal de "a calibrar no primeiro encontro real" — um padrão
em código viraria o número que ninguém decidiu. A do Guerreiro(a) não entra agora porque não há
sessão de Guerreiro(a) nesta fatia.

### Estrutura da pasta

Segue o desenho da fatia anterior: `src/nucleo/personas/`, `src/nucleo/sessoes/` e
`src/nucleo/permissoes.py`, cada pasta com modelo, regra e rota, ao lado de `chaves/`.

## Risks / Trade-offs

- **Tabela única de persona aperta quando os papéis ganharem atributos próprios** (fatia 3,
  fatia 4, PRD-02) → atributo de papel entra em tabela satélite, nunca em coluna anulável de
  `persona`.
- **A verificação do _ID token_ depende do JWKS do Google, pela rede** → JWKS em cache com
  validade; falha de rede responde 503, nunca 401 — recusar por indisponibilidade diria à
  aplicação que o cadastro não existe.
- **Matriz declarativa pode divergir do PRD-01 §4 com o tempo** → o teste que a percorre é parte
  da entrega, e a divergência quebra o CI.
- **Conferir a sessão no banco a cada chamada custa uma consulta** → é o preço de encerrar de
  verdade; a consulta é por índice do resumo, como a da chave.

## Migration Plan

1. Segunda migração cria `comunidade_virtual`, `persona`, `credencial` e `sessao`, com os
   atributos do PRD-01 §8 e do PRD-08 §8. `chave_de_aplicacao` não é tocada.
2. O comando de implantação passa a convergir a persona Admin do fundador, além das chaves.
3. Cada ambiente declara `CG_IDENTIDADE_FUNDADOR` e `CG_SESSAO_ADULTO_DURACAO` antes de subir.

**Reversão:** a migração desce e as quatro tabelas somem; as chaves da fatia anterior seguem
intactas. Nenhuma aplicação consome as rotas novas ainda.

## Open Questions

- **Quantas sessões simultâneas a mesma persona pode ter.** O PRD não diz, e nenhum cenário
  desta fatia depende disso. Vira pergunta de verdade na fatia 4, onde o aparelho é
  compartilhado.
- **O custo do Argon2id** — memória e iterações — é parâmetro de configuração, e o valor inicial
  se calibra no aparelho de produção. Não muda spec, tarefa nem estrutura.
