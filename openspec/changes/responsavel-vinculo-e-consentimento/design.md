## Context

Ver `proposal.md` — Why. O que já existe, das duas fatias anteriores: middleware de chave em
toda rota sob `/v1`, corpo único de erro, `Persona` em tabela única com o papel como
discriminador, sessão opaca conferida no banco, mixin `ComAutoria` e a matriz de permissões
declarativa de `permissoes.py`.

Três coisas do que já está pronto moldam esta fatia. A matriz **já tem** as operações de que ela
precisa — `cadastro_de_responsavel`, `vinculo_com_guerreiros_e_guerreiras`, `consentimentos` e
`guerreiros_sob_sua_responsabilidade` —, porque foi escrita inteira a partir do PRD-01 §4; aqui
elas passam de vocabulário a uso. O design da fatia 2 firmou que atributo próprio de papel entra
em tabela satélite, e não em coluna anulável de `persona`. E a autoria de escrita já é gravada
pelo mixin, então nada aqui precisa reinventá-la.

A restrição que domina o desenho é outra: `Consentimento` é **somente inserção** (PRD-01 §8) e é
prova de obrigação legal, com guarda permanente (PRD-01 §11). Ele não pode depender de disciplina
de quem escreve o código depois.

## Goals / Non-Goals

**Goals**

- Fazer a imutabilidade do consentimento ser propriedade do banco, não promessa do código.
- Deixar o recorte por vínculo pronto e conferível, para que as rotas do PRD-13 e do PRD-04 só o
  declarem.
- Deixar `Consentimento` pronto para a fatia da biometria, que depende dele por `RN-01-17`.

**Non-Goals**

- Rotas de consentimento: são do PRD-04 e do PRD-13 (ver `proposal.md`).
- Encerrar vínculo: o PRD-01 §9 não declara rota para isso, e o PRD-13 §3.2 põe a edição do
  vínculo no PRD-02.
- Anexar a digitalização do termo: a coluna nasce, a rota é do PRD-13.

## Decisions

### A imutabilidade do consentimento é garantida no banco, não só pela ausência de rota

A migração cria um _trigger_ que recusa `UPDATE` e `DELETE` em `consentimento`, e o modelo ganha
um _listener_ de mapeador que levanta erro antes de chegar lá. São duas camadas porque cada uma
falha de um jeito diferente: o _listener_ dá mensagem clara e é testável em memória; o _trigger_
vale para migração, script e psql — tudo o que não passa pelo ORM. "Somente inserção" é o que
sustenta a resposta "o que valia naquela data", e nenhuma das duas camadas custa manutenção.

Alternativa descartada: confiar em não haver rota de escrita — é exatamente o modo de falha por
omissão que a fatia 2 rejeitou ao escolher dependência única em vez de decorador por rota.

### O teto de três responsáveis trava a linha do Guerreiro(a) antes de contar

Contar e inserir em duas etapas deixa duas requisições simultâneas criarem o quarto vínculo, e
`RN-01-19` não é do tipo que se pode violar "raramente". Índice único não expressa "no máximo
três". Então a criação de vínculo abre a transação com `SELECT ... FOR UPDATE` na linha da
persona do Guerreiro(a), conta os vigentes e insere. Serializa por criança, que é um volume de
no máximo três escritas na vida do registro.

Alternativa descartada: contador desnormalizado em `persona` — duplicaria estado que a contagem
já dá, e teria de ser mantido em toda mudança de vigência.

### O teto conta vínculos vigentes

`VinculoResponsavel` tem `início` e `fim` no PRD-01 §8, e `RN-01-19` fala em três responsáveis
**vinculados**, enquanto o PRD-01 §12 fala nos três vínculos que "continuam válidos". A leitura
aplicada é a literal: conta quem está vigente. O efeito prático nesta fatia é nulo — nada aqui
encerra vínculo, porque não há rota para isso —, então a leitura só passa a valer quando o PRD-02
trouxer a edição. Ver Open Questions.

### O recorte por vínculo é dependência declarativa, como o filtro por comunidade

`exigir_vinculo_do_responsavel` é uma dependência que, quando o papel em sessão é responsável,
exige vínculo vigente com o Guerreiro(a) alvo e nega por padrão; para os demais papéis, quem
decide continua sendo a matriz. É o mesmo formato do filtro por comunidade da fatia 2 — e é
proposital que sejam **dois recortes independentes**: `RF-01-15` não é uma variação do filtro por
comunidade, e a spec exige que a mesma comunidade não amplie o alcance de ninguém.

Nesta fatia nenhuma rota do PRD-01 lê dado de Guerreiro(a), então a dependência nasce conferida
por teste, como a autoria nasceu na fatia 2 sem a rota que a consulta. A primeira rota a declará-la
é `GET /v1/eu/guerreiros`, do PRD-13.

### O consentimento nasce como função de domínio, sem rota

`registrar_consentimento` concentra as três invariantes — versão do termo obrigatória, vínculo
vigente exigido e inserção sempre nova — em um lugar só. As rotas do PRD-04
(`POST /v1/consentimentos`) e do PRD-13 (`POST /v1/eu/guerreiros/{id}/autorizacao`) a chamarão sem
reimplementar nada. Espalhar as invariantes pelas duas aplicações seria repetir regra em dois
PRDs diferentes.

### `tipo` do consentimento fica aberto, com os dois valores que os PRDs já nomeiam

O PRD-01 §8 exige o atributo `tipo` e não fecha catálogo. Dois já têm dono: a **autorização**,
uma só, do PRD-13, e o **consentimento biométrico**, de termo impresso próprio, do PRD-04. A
coluna aceita esses dois desde já e não vira enumeração fechada nesta fatia — fechá-la seria
decidir pelos PRDs que ainda vão usá-la.

### O anexo do termo guarda referência, não binário

A coluna do anexo nasce anulável e guarda a referência ao objeto no Cloud Storage (documento 03),
não o arquivo. Nada nesta fatia a escreve; quem escreve é `POST /v1/consentimentos/{id}/anexo`,
do PRD-13.

### Estrutura da pasta

Segue o desenho das fatias anteriores: `src/nucleo/responsaveis/` e
`src/nucleo/consentimentos/`, cada uma com modelo, regra e — só a primeira — rotas, ao lado de
`chaves/`, `personas/` e `sessoes/`.

## Risks / Trade-offs

- **O _trigger_ impede corrigir um consentimento gravado por engano** → é o comportamento que o
  PRD quer: a correção é registro novo, e o histórico mostra os dois. Erro de estrutura se
  resolve descendo a migração.
- **A trava de linha serializa a criação de vínculos da mesma criança** → são no máximo três na
  vida do registro; nenhuma outra escrita disputa essa linha.
- **O recorte por vínculo nasce sem rota que o exerça** → o teste do guard é parte da entrega, e
  a dependência já está pronta para o PRD-13 declará-la.
- **`Consentimento` pode parecer entidade morta até o PRD-04** → não fica: a fatia da biometria
  a consome imediatamente por `RN-01-17`, e é justamente para ela que esta fatia existe.
- **Vínculo e comunidade podem discordar** — responsável de uma criança de outra comunidade →
  o PRD não proíbe, e o recorte do responsável é o vínculo; nada aqui cruza os dois.

## Migration Plan

1. Terceira migração cria `vinculo_responsavel` e `consentimento` com os atributos do PRD-01 §8,
   mais o _trigger_ de recusa de `UPDATE` e `DELETE` em `consentimento`. As tabelas das fatias
   anteriores não são tocadas.
2. Nenhuma variável de configuração nova, nenhuma semeadura nova: o comando de implantação segue
   como está.

**Reversão:** a migração desce, as duas tabelas e o _trigger_ somem, e as fatias 1 e 2 seguem
intactas. Nenhuma aplicação consome as rotas novas ainda.

## Open Questions

- **Vínculo encerrado conta para o teto de três?** A decisão acima aplica a leitura literal de
  `RN-01-19` — conta os vigentes. Nada nesta fatia encerra vínculo, então a resposta só muda
  comportamento quando o PRD-02 trouxer a edição; se o fundador ler diferente, muda uma linha da
  contagem e um cenário da spec, não o desenho.
- **O que acontece ao vínculo quando o Guerreiro(a) muda de comunidade.** É transferência, tema
  do PRD-08; nenhum cenário desta fatia depende disso.
