## Context

Ver `proposal.md` — Why. Como a fatia anterior, é **exposição**: as três regras de desfecho e a
guarda `liberar_conjunto_de_dados` estão em `backend/src/nucleo/fila/regra.py` e especificadas em
`openspec/specs/fila-de-avaliacao/spec.md`. Nenhuma muda.

Esta fatia herda inteiros os padrões que `avaliacao-da-participacao-e-do-pre-cadastro` fixou: a
fila sem filtro por comunidade, o atraso derivado na resposta, a guarda de reavaliação na rota e
a área Filas com filtro por natureza. O que segue são só as decisões que a fatia anterior não
teve de tomar.

## Goals / Non-Goals

**Goals:**

- Fechar as quatro naturezas da fila, deixando a capacidade sem regra inalcançável.
- Destravar a emissão de chave de terceiro, hoje impossível por falta do degrau anterior.

**Non-Goals:**

- Tocar `chave-de-aplicacao`. A emissão, o prazo, a revogação por decurso e a revogação por
  Admin já estão especificados e implementados; esta fatia apenas os alcança.
- Gerar o conjunto de dados entregue. É do PRD-08; aqui ficam a guarda e o registro da entrega.

## Decisions

**1. O desfecho da chave é rota própria, e `POST /chaves` continua só emitindo.** Decidido pelo
fundador em 2026-08-22, completando o PRD-02 §9: `POST /v1/solicitacoes-de-chave/{id}/avaliacao`,
simétrica às outras três naturezas. `emitir_chave_de_terceiro` não muda — segue exigindo
solicitação aceita, o que agora é alcançável.
_Descartado:_ `POST /chaves` como o próprio ato de aprovação, que juntaria aprovar e emitir num
passo só e exigiria mudar a regra de emissão para acomodar a recusa.

**2. O compromisso de não reidentificação é campo do desfecho, não caixa de marcar na tela.**
`avaliar_solicitacao_de_dados` já o exige como parâmetro e recusa a aprovação sem ele; a rota
apenas o transporta. A tela o apresenta junto dos três critérios, mas a garantia é do núcleo.
_Descartado:_ conferência só no cliente, que deixaria a rota aprovar sem o compromisso.

**3. As quatro leituras compartilham a forma da resposta, não o endpoint.** O PRD-02 §9 declara
quatro rotas separadas, e cada natureza tem campos próprios. O que se repete — situação, prazo,
atraso derivado, quem avaliou, parecer e data — sai no mesmo formato nas quatro, para que a lista
unificada da App 03 as componha sem tratar cada uma de um jeito.
_Descartado:_ um `GET /solicitacoes` polimórfico, que o PRD não declara e que misturaria naturezas
com campos incompatíveis numa resposta só.

**4. O painel de chaves é área da App 03 ao lado das Filas, não dentro delas.** A fila mostra
**pedidos**; o painel mostra **chaves emitidas**, que já não são pedido e têm ciclo próprio —
prazo, URL apresentada, revogação. Juntá-los faria a lista unificada carregar duas entidades
diferentes sob um filtro que promete naturezas de solicitação.

**5. O segredo vive só na memória da tela que o recebeu.** A App 03 o apresenta na resposta da
emissão e não o guarda em `sessionStorage` nem em estado que sobreviva à navegação — `RN-02-28`
diz que não é recuperável, e guardá-lo no navegador criaria uma segunda cópia que a regra não
prevê.

## Risks / Trade-offs

- **O Admin perde o segredo ao sair da tela antes de copiá-lo** → é o comportamento que
  `RN-02-28` determina, não um efeito colateral. A tela avisa antes, e a saída pede confirmação.
- **A emissão de chave de terceiro entra em uso pela primeira vez** → o ciclo inteiro está
  implementado e testado por unidade desde `ciclo-de-vida-da-chave-de-terceiro`, mas nunca
  correu de ponta a ponta. Os testes desta fatia percorrem solicitação → aprovação → emissão →
  apresentação de URL, que é o caminho que ninguém exercitou junto.
- **`avaliar_sugestao` credita ponto extra e badge dentro do desfecho** → é a operação única que
  `RN-01-50` exige, e a idempotência por `creditado_em` já está implementada. A rota não repete
  a guarda; o teste confirma que regravar não credita de novo.
- **A guarda de reavaliação segue na rota, agora em quatro lugares** → repetição aceita nesta
  fatia. Consolidá-la na regra alcançaria as quatro naturezas de uma vez e é candidata a fatia
  de limpeza depois que todas existirem, não durante.

## Open Questions

Nenhuma. As duas que a `proposal.md` levantou foram decididas pelo fundador em 2026-08-22: a
rota de desfecho da chave é simétrica, e o `RF-02-93` de §6.5 recebe identificador novo. As duas
correções entram no PRD-02 nesta change.
