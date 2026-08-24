## Context

Motivação em `proposal.md` — Why; requisitos nas specs do delta.

Três restrições do código existente moldam tudo o que segue:

1. **O núcleo não conhece "sessão de trabalho do aparelho".** Ela é conceito da App 01: para o
   backend, o que chega é `ContextoDaSessao` — `persona_id`, `papel`, `sessao_id` — de um login
   social comum de Mestre ou Admin. Não há marcador que diga "esta sessão está operando um
   aparelho de aula". O que **existe** é o `ContextoDaChave`, conferido em toda chamada sob
   `/v1`, com `aplicacao` e `ambiente`.
2. **`POST /v1/guerreiros` é uma rota só, declarada pelos dois PRDs** — pela §9 do PRD-04, sob a
   sessão do App 01, e pelo `RF-02-01`, como caminho da gestão. Não cabe inventar rota nova.
3. **`registrar_presenca` já é idempotente** por par de aula e Guerreiro(a), já aceita o momento
   do fato e já exige confirmador no modo confirmação. `criar_persona` já aplica unicidade
   global de nick e já deriva a comunidade da aula.

## Goals / Non-Goals

**Goals:**

- Separar o caminho do encontro do caminho da gestão sem duplicar a rota nem a validação comum.
- Fazer a faixa etária existir num só lugar, alcançando os dois caminhos.
- Devolver variações de nick sem que exista rota de consulta com alcance total.
- Gravar cadastro e presença numa transação só.

**Non-Goals:**

- Marcar a sessão de trabalho no núcleo como tipo próprio de sessão. Nada nesta fatia exige
  distinguir "sessão de trabalho" de "sessão de Mestre" além do que a chave já resolve, e criar
  um tipo de sessão é decisão do PRD-01, não desta fatia.
- Reescrever `criar_persona`, `registrar_presenca` ou `conferir_disponibilidade_de_nick`.

## Decisions

### 1. A chave de aplicação discrimina os dois caminhos

`POST /v1/guerreiros` atende os dois caminhos e escolhe entre eles pela **aplicação declarada na
chave**: chave da App 01 → caminho do encontro, persona criada **sem criador**; qualquer outra →
caminho da gestão, restrito a Admin, persona criada com ele como criador.

É a função que a chave já tem — identificar a aplicação consumidora (documento 03 §1) — e o
`MiddlewareDeAuditoria` já a lê para gravar a origem de toda escrita. A autorização continua na
matriz de permissões, não na chave: o Mestre alcança a rota pela operação nova (decisão 2), e o
caminho da gestão segue exigindo `Operacao.tudo`. Um Admin operando o aparelho cai no caminho do
encontro, que é o correto — quem se cadastra ali é a criança.

Alternativas descartadas: rota nova sob `/v1/aulas/{id}/guerreiros` — contraria a §9 do PRD-04;
discriminar pela presença de `aula_id` no corpo — os dois caminhos precisam da aula; discriminar
pelo papel de quem chama — ambíguo para o Admin, que tem os dois.

### 2. A matriz ganha uma operação, e a regra ganha duas funções

A matriz recebe a operação de **cadastro de Guerreiro(a) no encontro**, concedida a **Mestre e
Admin** — é o código da decisão do fundador de 2026-08-24 já gravada na fatia anterior. A rota
exige essa operação **ou** `Operacao.tudo`, conforme o caminho que a chave selecionou.

Em `personas/regra.py`, `cadastrar_guerreiro_pela_gestao` permanece intacta — inclusive a recusa
de quem não é Admin, que é a regra do caminho dela — e nasce ao lado uma função do caminho do
encontro, que **não** recebe operador como autor. As validações comuns — nome, nascimento,
avatar, faixa etária — ficam numa função compartilhada pelas duas, para que a faixa não exista
em dois lugares.

Alternativa descartada: uma função com um parâmetro de caminho — apagaria a distinção de autoria
que o invariante 3 protege, que é exatamente o que esta fatia veio afirmar.

### 3. A faixa etária é apurada na data da criação, com os extremos dentro

A idade sai da data de nascimento contra a data corrente, e a faixa aceita **6 e 16 inclusive**.
A conferência vive na validação comum da decisão 2, e por isso alcança a gestão sem que a rota
da gestão mude — é a decisão retroativa do fundador.

Aniversário durante o Ciclo 01 **não** desativa ninguém: a faixa é condição de **entrada**, não
de permanência. Nada nos documentos manda desligar quem completa 17 anos, e inventar isso seria
regra nova — se vier a ser necessária, é pergunta ao fundador, não desta fatia.

### 4. As variações nascem de uma função de alcance total, que nenhuma rota consulta

Nasce, ao lado de `conferir_disponibilidade_de_nick` — que segue adulto-only e intocada —, uma
conferência de **alcance total** e a geração de variações sobre ela. Ela é chamada **num único
ponto**: a montagem da recusa por nick em uso do caminho do encontro. Nenhuma rota a expõe, e a
rota pública `GET /v1/nicks/disponibilidade` não a alcança.

A recusa continua sendo **422 no campo `nick`**, sem dizer de quem é o nick; as variações vão no
corpo da recusa, até três, como `sugerir_variacoes_de_nick` já faz. O caminho da gestão **não**
as recebe: lá a recusa é a de hoje.

Alternativa descartada: rota de conferência com alcance total atrás da sessão do aparelho —
contraria o requisito consolidado de `persona-e-credencial`, que define a vedação pelo que a
resposta alcança e não por quem pergunta. Decidido pelo fundador em 2026-08-24.

### 5. Cadastro e presença numa transação, com o adulto da sala como confirmador

O `RF-04-17` pede a presença "no mesmo ato". Duas chamadas da App 01 deixariam cadastro sem
presença quando a rede caísse entre elas — e rede instável é requisito não funcional declarado
do App 01 (PRD-04 §10). A rota do caminho do encontro grava persona, vínculo de comunidade e
presença numa transação, com um único `commit`.

A presença é gravada no **modo confirmação**, tendo como confirmador a persona da sessão de
trabalho — o Mestre ou o Admin presente. É o que descreve o fato: quem atesta que aquela criança
está na sala é o adulto que abriu o aparelho. O modo reconhecimento não é usado aqui, porque não
há captura nesta fatia.

Isso resolve, sem coluna nova, o "registro de quem confirmou" do `RF-04-15`: `Presenca.confirmador`
o guarda de forma transacional. O `MiddlewareDeAuditoria` também registra a persona da sessão,
mas é _best-effort_ — falha dele vai só para o log —, e por isso não é a garantia do requisito,
apenas o complemento dela. Fecha a pendência 2 da proposal.

### 6. A App 01 não confere nick antes de enviar

A tela não pergunta ao núcleo se o nick está livre: envia o cadastro e trata a recusa. É o que a
decisão do fundador impõe — não há rota de conferência do onboarding — e é também o que evita a
tela afirmar "disponível" para um nick que a gravação recusaria.

A tela do cadastro vive em `apps/app-01-aula-presencial/src/onboarding/`, ao lado das três que já
existem, e o botão do onboarding em `TelaInicial.tsx` perde o `disabled`.

## Risks / Trade-offs

- **A recusa de nick só aparece ao concluir, não ao digitar** → é o custo aceito da decisão do
  fundador; mitigado por até três variações prontas para um toque, sem nova digitação.
- **A chave passa a selecionar comportamento, não só a identificar quem chama** → a autorização
  continua inteiramente na matriz de permissões; a chave escolhe o caminho, nunca concede acesso.
  Chave da App 01 sem persona autorizada segue recusada como hoje.
- **A conferência de alcance total é um oráculo de nick por outra porta** → limitada a uma
  resposta de escrita recusada, exigindo chave da App 01, sessão aberta, aula vigente e adulto
  autenticado no encontro. Registrado como segunda exceção declarada na spec, para não virar
  precedente silencioso.
- **Um Admin operando a App 03 com a chave errada criaria persona sem autor** → as chaves são por
  aplicação e por ambiente, semeadas na implantação; a troca não acontece por acidente de uso.

## Open Questions

Nenhuma que altere as specs, o desenho ou as tarefas.
