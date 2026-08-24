# Desenho — entrada por reconhecimento e falha de identificação

## Context

Ver `proposal.md` — Why. Três das quatro peças desta fatia já estão escritas, testadas e
consolidadas, e nenhuma é reescrita:

| Peça                              | Onde já está                                | O que falta            |
| --------------------------------- | ------------------------------------------- | ---------------------- |
| Sessão por nick e descritor       | `openspec/specs/sessao-do-guerreiro`        | um cliente             |
| Descritor gerado no aparelho      | `apps/app-01-aula-presencial/src/biometria` | um segundo uso         |
| Presença sem confirmador          | `openspec/specs/aula-e-presenca`            | uma rota que a produza |
| Gravar e recadastrar o _template_ | `openspec/specs/template-biometrico`        | uma tela               |

A fatia é, portanto, **uma decisão de núcleo e uma costura de cliente**.

## Goals / Non-Goals

**Goals:** produzir o modo `reconhecimento`, que hoje nenhuma linha da plataforma alcança;
costurar entrada, presença e falha numa única tela de atendimento.

**Non-Goals:** fila local sem rede (jornada 5.6); captura de quem já se cadastrou sem imagem
(`RF-04-16`); qualquer alteração em `registrar_presenca`, em `autenticar_por_nick_e_descritor`
ou no módulo de biometria do aparelho.

## Decisions

### 1. O modo é decidido pela aplicação da chave, não pelo papel de quem está em sessão

A sessão de trabalho do aparelho é de um Mestre ou de um Admin — as mesmas personas que a App
09 usa para confirmar presença. O papel, sozinho, não distingue os dois casos. A chave sim: ela
declara a aplicação.

`POST /v1/aulas/{id}/presencas` passa a recusar o modo `reconhecimento` **quando a chave não é a
da App 01**, em vez de recusá-lo sempre. É o mesmo desenho que a segunda fatia deu ao `POST
/v1/guerreiros`, e o que o próprio comentário da rota já anunciava.

_Alternativas descartadas:_ rota nova só para a App 01 — duplicaria a regra de unicidade e de
comunidade; operação nova na matriz para o Guerreiro(a) — contraria a decisão do fundador de
2026-08-24, que mantém a presença como fato do encontro e não como ato da criança.

### 2. A sessão de trabalho autentica e não assina

Presença por reconhecimento nasce **sem confirmador**, ainda que a escrita tenha sido
autenticada por um adulto. `registrar_presenca` já dispensa confirmador nesse modo; a rota
apenas não o preenche. É a mesma distinção do autocadastro da segunda fatia: quem autentica não
é quem pratica.

### 3. O cliente reconhece a presença anterior pelo momento do fato

O núcleo devolve o registro existente sem erro (decisão do fundador, 2026-08-24). A App 01
envia o momento do fato que observou e compara com o que voltou: **diferente do enviado**, a
presença já existia, e a tela mostra o aviso da jornada 5.4.

_Alternativa descartada:_ 200 para existente e 201 para criado — resolveria também, mas altera o
contrato de uma rota que a App 09 já consome, para um sinal que o corpo da resposta já carrega.

### 4. O identificador do Guerreiro(a) vem da sessão, nunca de uma consulta

O recadastro da imagem (`RF-04-22`) precisa de um identificador, e o `RN-01-22` veda a rota que
resolva nick em identificador para quem quer que pergunte. O caminho não é uma consulta: a
sessão aberta por **confirmação presencial** já autentica aquele Guerreiro(a), e o `GET
/v1/quem-sou` dela diz quem é. Ninguém pergunta um nick — um adulto confirma uma criança que
está na frente dele, e a sessão responde.

Nenhuma rota nova; nenhum alcance novo. É o que dissolve o bloqueio que a terceira fatia
registrou.

### 5. A ordem da tela de entrada

```text
nick digitado
   └─ há câmera? ── não ──▶ confirmação humana ──▶ sessão + presença (confirmação)
        │ sim                                          ▲
        ▼                                              │
   vivacidade ──▶ descritor ──▶ POST /sessoes/guerreiro│
                                     │                 │
                              401 ───┴──▶ nova tentativa
                                     │        └── persiste ──────┘
                                     ▼
                                 sessão aberta
                                     ▼
                          POST /aulas/{id}/presencas (reconhecimento)
```

Duas chamadas de rede, não uma: a sessão abre antes da presença, porque é ela que prova quem
chegou. A presença é escrita pela **sessão de trabalho**, não pela sessão recém-aberta do
Guerreiro(a) — decisão 2.

## Risks / Trade-offs

- **A comparação biométrica atrasa a fila da porta** → o nick já restringe a busca a um único
  Guerreiro(a); a comparação é de um contra um, não de um contra todos. O `RN-04-09` garante a
  saída: a confirmação humana continua a um toque.
- **Falso negativo deixa a criança na porta** → nunca: a segunda falha já oferece a confirmação
  humana, e ela abre sessão com os mesmos direitos e registra a presença igual.
- **O aviso de presença já registrada depende do momento do fato devolvido** → se o núcleo
  passasse a normalizar esse campo, o sinal se perderia. A spec de `aula-e-presenca` fixa que o
  momento original é preservado e devolvido, e o teste trava isso.
- **Recadastrar imagem é operação sensível numa tela de encontro** → fica atrás da sessão do
  Guerreiro(a) aberta por confirmação presencial, restrita a Mestre e Admin pela matriz, e o
  núcleo audita toda substituição.
