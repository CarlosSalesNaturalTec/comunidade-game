# Spec Delta

## MODIFIED Requirements

### Requirement: O painel do dia é a leitura do encontro em andamento

O núcleo SHALL expor **`GET /v1/painel-do-dia`** (PRD-02 §9), que devolve, **numa leitura só**,
o estado da aula em andamento — aquela cuja janela de data e horários contém o instante da
consulta, na comunidade de quem consulta.

O painel SHALL ser **inteiramente derivado**: fora a escolha corrente da equipe, ele NEVER SHALL
ter entidade, coluna ou registro próprio, e cada campo SHALL ser recomputado a cada consulta a
partir do que os domínios já gravaram.

Ler o painel SHALL ser ato de **Admin** ou de **Mestre**; o Mestre SHALL alcançar apenas as
aulas das comunidades a que está vinculado (`RN-02-20`). Guerreiro(a), responsável e Apoiador
SHALL receber **403**. Fora da janela de qualquer aula, o painel SHALL devolver **200 com o
encontro vazio**, e não erro — é o dia sem encontro. (`RF-02-41` a `RF-02-47`, `RF-02-69`,
`RN-02-20`, PRD-02 §§6.4, 9, 12)

Havendo **mais de uma aula vigente** no instante da consulta entre as comunidades de quem
consulta, o painel SHALL servir **uma** delas — a de início mais antigo —, pelo mesmo
precedente que já vale para o Admin: não é do núcleo escolher entre comunidades, e o painel
serve um encontro por vez (`RF-01-32`, `RF-01-18`).

#### Scenario: O painel devolve o encontro em andamento numa leitura

- **WHEN** um Admin consulta o painel do dia durante a janela de uma aula
- **THEN** o núcleo devolve aquela aula com presenças, equipes, previsto e provido, saldo e
  lançamentos pendentes, sem exigir outra consulta

#### Scenario: Fora de qualquer janela o painel volta vazio

- **WHEN** o painel é consultado num instante fora da janela de toda aula agendada
- **THEN** o núcleo responde 200 com o encontro vazio, e não erro

#### Scenario: O Mestre lê apenas o encontro da comunidade dele

- **WHEN** um Mestre consulta o painel e há aula em andamento em comunidade a que ele não está
  vinculado
- **THEN** aquela aula não aparece para ele

#### Scenario: Duas aulas vigentes nas comunidades do Mestre servem a mais antiga

- **WHEN** um Mestre vinculado a duas comunidades consulta o painel e há aula em andamento em
  cada uma
- **THEN** o painel serve a de início mais antigo, e só ela

#### Scenario: Guerreiro(a) não lê o painel

- **WHEN** um Guerreiro(a) em sessão consulta o painel do dia
- **THEN** o núcleo responde 403 e nada é devolvido
