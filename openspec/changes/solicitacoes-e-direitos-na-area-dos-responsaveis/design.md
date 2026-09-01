## Context

O núcleo da `SolicitacaoDoResponsavel` já existe (fatia 14 do PRD-02, spec
`solicitacao-do-responsavel`): abertura, protocolo, prazo de 7 dias, atraso derivado, fila do
Admin e desfecho. A App 07 já tem esqueleto, sessão, lista de vinculados com abas por criança e
a tela de autorização única (specs `area-dos-responsaveis` e `consentimento`). O _template_
biométrico é a `Credencial` de tipo `biometria`, cifrada em `segredo`, com auditoria própria em
`AcessoAoTemplate` (spec `template-biometrico`).

O que não existe: qualquer forma de **apagar** o _template_, o **marco do fim do vínculo** e um
lugar onde **prazo de guarda** se cumpra. Seis decisões do fundador (2026-09-01) fecham essas
lacunas e são o que este desenho aplica.

## Goals / Non-Goals

**Goals:**

- Telas da App 07 sobre o núcleo que já existe, sem duplicar regra dele.
- O _template_ apagado nos três gatilhos e nos prazos do documento 03 §12.2.
- Um só lugar que cumpre prazo, testável sem esperar o relógio.

**Non-Goals:**

- **Execução** da despersonalização do dado de território (`RN-13-12`) — Ciclo 02, por decisão
  do fundador. Aqui ela é só o texto declarado antes do aceite.
- Tela da App 03 que encerra o vínculo — é do PRD-02; aqui nasce a rota do núcleo.
- Transparência, termos e histórico de acessos (`RF-13-29` a `RF-13-34`) — fatia 5, travada.
- Reabertura de vínculo encerrado: quem volta faz nova captura, e nenhuma rota desfaz o fim.

## Decisions

**1. Marca de apagamento em tabela própria, uma por Guerreiro(a).** `ApagamentoDeTemplate`
guarda `guerreiro_id` (único), `gatilho`, `apagar_em` e `criado_em`. Único por Guerreiro(a) é o
que implementa "gatilho novo não empurra a data": o segundo gatilho encontra marca e não faz
nada. _Descartado:_ colunas em `Credencial`, que é compartilhada pelos quatro tipos de
credencial e não deve carregar regra de um só.

**2. Apagar é remover a `Credencial` de tipo `biometria`.** É o registro que guarda o cifrado;
removê-lo destrói o dado sem deixar coluna de onde recompô-lo. `AcessoAoTemplate` ganha a
natureza `apagamento`, com `acessado_por` nulo — o comando não tem persona —, e a auditoria
anterior permanece, por ser somente inserção. _Descartado:_ anular `segredo` mantendo a linha,
que deixaria uma credencial de biometria sem segredo confundindo a conferência de login.

**3. Fim do vínculo em módulo próprio, `nucleo/vinculo_do_guerreiro/`.** `FimDeVinculo` guarda
`guerreiro_id` (único), `origem` (`admin` ou `varredura`), `encerrado_por` (nulo na varredura),
`motivo` e `momento`. Não é o `VinculoJogador` de `comunidades`, que é vínculo com a **Comunidade
Virtual** e tem histórico próprio: o fim do vínculo **com o projeto** é marco de prazo de guarda
e nada mais, como o documento 03 §12.2 o define. _Descartado:_ reaproveitar `VinculoJogador`,
que confundiria transferência de comunidade com saída do projeto.

**4. Os 12 meses contam da mais recente entre presença, resultado e coleta** (decisão do
fundador); sem nenhuma das três, contam da criação da persona. A varredura consulta os três
máximos por Guerreiro(a) numa consulta só, e ignora quem já tem `FimDeVinculo`.

**5. Comando de manutenção em `nucleo/manutencao.py`, chamado por `python -m nucleo.manutencao`.**
Faz duas coisas, nessa ordem: encerra os vínculos vencidos e apaga os _templates_ vencidos —
assim um vínculo encerrado hoje já nasce com a marca de 30 dias na mesma execução. Fica fora do
`cli.py`, que é o comando de implantação e roda uma vez por ambiente; este roda periodicamente.
A implantação o agenda. _Descartado:_ rota HTTP de expurgo, que exporia por chave de aplicação a
única operação destrutiva do núcleo; e avaliação preguiçosa, que deixaria o dado vivo enquanto
ninguém tocasse na criança.

**6. Três rotas novas, seguindo o desenho das que já existem:**

| Método | Rota                                     | Persona     | O que faz                                     |
| ------ | ---------------------------------------- | ----------- | --------------------------------------------- |
| POST   | `/v1/eu/guerreiros/{id}/biometria/recusa` | Responsável | Grava a recusa e devolve a data do apagamento |
| GET    | `/v1/eu/guerreiros/{id}/biometria`        | Responsável | Estado da captura, data e gatilho do apagamento |
| POST   | `/v1/guerreiros/{id}/fim-de-vinculo`      | Admin       | Encerra o vínculo com motivo                  |

A recusa é rota **separada** de `/v1/eu/guerreiros/{id}/autorizacao` porque a spec
`consentimento` já proíbe aquela rota de alcançar a biometria: a autorização é uma só, e a
biometria fica fora dela. As três entram na tabela do PRD-13 §9, que hoje não as tem.
Permissões pela matriz existente: `consentimentos` e `guerreiros_sob_sua_responsabilidade` para
o responsável, `tudo` para o Admin — nenhuma `Operacao` nova.

**7. A versão do termo da biometria é a mesma configuração vigente**
(`consentimento_versao_vigente_do_termo`), carimbada pelo núcleo como em todo consentimento. Uma
versão distinta para o termo impresso é parâmetro que a operação declara quando o texto do termo
existir, não decisão de produto a tomar aqui.

**8. Duas abas novas por vinculado na App 07** — "Solicitações" e "Imagem do onboarding" —, ao
lado de "Evolução" e "Autorização". A recusa da imagem em aba própria é o que cumpre a exigência
de não aparecer misturada com a autorização única. O aviso do apagamento, quando existe, aparece
na aba da imagem, que é onde o assunto vive.

**9. A App 07 não calcula prazo nem atraso.** Protocolo, prazo, `em_atraso` e a data do
apagamento vêm do núcleo e são exibidos como vieram — a mesma disciplina já aplicada ao estado
da autorização.

## Risks / Trade-offs

- **O prazo depende de alguém agendar o comando.** Se a implantação não o agendar, o _template_
  marcado sobrevive à data. Mitigação: o comando relata o que fez e o que ficou vencido, e a
  tarefa de documentação registra a exigência de agendá-lo no ambiente de produção.
- **A varredura dos 12 meses varre a base inteira.** No Ciclo 01 a base é de uma comunidade e o
  custo é irrelevante; se crescer, a consulta pede índice pelos três máximos.
- **Marca que não se cancela é decisão dura de propósito.** A família que recusar e voltar atrás
  em menos de cinco dias perde a captura e refaz o onboarding. Foi a escolha do fundador, e é o
  que o documento 03 §9 já avisa ao responsável.
- **A tela da App 03 que encerra o vínculo não existe ainda.** Até a fatia do PRD-02 entrar, o
  ato de Admin só é alcançável pela API. A varredura dos 12 meses não depende dela.
