## Context

Ver `proposal.md` — Why. A fatia é sobretudo **exposição**: a regra de agendamento, de
cancelamento e de derivação das vigentes já está em `openspec/specs/aula-e-presenca/spec.md` e
implementada; o cadastro do ponto de apoio, em `openspec/specs/ponto-de-apoio/spec.md`. Nada
disso muda.

O que já está consolidado e esta fatia apenas aplica:

| Padrão                                        | Onde                                                    |
| --------------------------------------------- | -------------------------------------------------------- |
| Envelope de página, cursor e filtros de rota  | `backend/src/nucleo/paginacao.py`, `convencoes-da-api`   |
| Escopo por papel na leitura de gestão         | `listar_acervo`, em `patrimonio/regra.py`                |
| Rota com chave e sem persona                  | as rotas de `vitrine/`, `protecao-das-rotas-publicas`    |
| Camada visual e associação do erro ao campo   | `comum/react/`, `camada-visual-comum`                    |

## Goals / Non-Goals

**Goals:**

- Expor as três leituras sem tocar em nenhuma regra de escrita já implementada.
- Deixar a App 01 com uma rota estável de onde tirar a comunidade da janela em curso.

**Non-Goals:**

- Refatorar `aulas_vigentes`, `agendar_aula` ou `cancelar_aula`. Se a fatia precisar mudá-las,
  é sinal de que o recorte está errado.
- Criar componente visual que as três telas não usem.

## Decisions

**1. As duas leituras de gestão usam `contrato_de_listagem`, e o escopo por papel copia
`listar_acervo`.** Admin declara a comunidade e a leitura recusa com 422 sem o filtro; Mestre
tem a comunidade derivada do vínculo vigente, e sem vínculo lê lista vazia; Apoiador,
Guerreiro(a) e responsável recebem 403. É o precedente do acervo patrimonial aplicado tal
qual — não há razão para dois desenhos de escopo no mesmo núcleo.
_Descartado:_ escopo declarado rota a rota, que espalharia a matriz de permissões pelo código.

**2. `GET /aulas/vigentes` sai no mesmo envelope de página, mas com o filtro de comunidade
opcional.** A convenção manda paginar toda listagem; o filtro obrigatório, porém, derrotaria a
rota — quem a chama é justamente quem **ainda não sabe** a comunidade. O contrato admite a
distinção: o filtro obrigatório é declarado por rota, não imposto a todas.
_Descartado:_ rota sem envelope de página, que abriria exceção à convenção por conveniência.

**3. A rota das vigentes exige chave e não exige persona, e não recebe freio por origem.** É o
mesmo caminho das rotas de `vitrine/`. O freio por origem alcança apenas a consulta por nick e
os dois formulários públicos; a cota de leitura por faixa da chave já cobre toda leitura,
inclusive esta.
_Descartado:_ exigir persona, que impediria o App 01 de abrir antes de alguém se identificar.

**4. O campo de data e hora com fuso nasce em `comum/react/`, não na App 03.** É o primeiro
formulário da plataforma a coletar horário, e o documento 15 §12 põe em `comum/` o que as oito
aplicações repetem. A App 03 NUNCA envia horário sem fuso.
_Descartado:_ nascer na App 03 e mudar de lugar quando a segunda aplicação precisar — o custo
de mover cresce, o de nascer no lugar certo é o mesmo agora.

**5. O seletor de ponto de apoio refaz a consulta filtrada quando a comunidade muda.** A
alternativa seria carregar todos os pontos de apoio e filtrar no cliente, o que traria à
memória do navegador dado de comunidade que aquela tela não está mostrando — contra
`RF-01-18`, ainda que a tela nunca o exiba.

## Risks / Trade-offs

- **A agenda cresce e a lista densa fica ilegível** → o filtro por período entra no contrato
  desde a primeira versão, não como melhoria depois.
- **Mestre sem vínculo vigente lê lista vazia, e vazio se confunde com falha** → `EstadoDaLista`
  de `comum/react` já distingue lista vazia de erro de carregamento; a tela usa os dois estados.
- **A rota das vigentes é pública e ninguém a monitora** → ela não devolve dado pessoal:
  comunidade, ponto de apoio e horários da aula. Nenhum Guerreiro(a), nenhum nick, nenhum
  avatar.
- **`GET /aulas` sem filtro de período varre a tabela inteira** → `aula` hoje não tem índice em
  `inicio_em`, e o cursor limita a página. O índice entra quando o volume justificar; no Ciclo
  01, com uma comunidade, não justifica, e criá-lo agora custaria uma migração que esta fatia
  não precisa ter.

## Open Questions

- **Modalidade da aula** — a contradição entre o PRD-02 §8, o `RF-02-30` e a exigência de ponto
  de apoio da capacidade `aula-e-presenca` está na `proposal.md` como pergunta ao fundador. Ela
  não muda as specs nem as tarefas desta fatia, que agenda a aula presencial, e por isso não a
  trava.
