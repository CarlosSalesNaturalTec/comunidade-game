## Context

Fatia de frontend: o núcleo já tem a fila única e o Apoiador já a alcança pela operação
`propostas_de_evolucao`. O aviso de coleta com área detalhada é padrão consolidado nas Apps 03,
07 e 09; esta change o aplica à App 08. Motivação em `proposal.md`; requisitos no delta de
`specs/area-do-apoiador/`.

## Goals / Non-Goals

**Goals:** dar ao Apoiador a área de propostas, a área detalhada de direitos e dados e o aviso
de coleta em toda tela que grava dado, e deixar o canal fechado verificado por teste.

**Non-Goals:** mudar núcleo, banco ou contrato de API; promover o aviso a `comum/`; tratar
pedido de acesso, correção ou exclusão dentro da App 08 — ele é da gestão (PRD-14 §11).

## Decisions

1. **Reusar as rotas da fila única, sem tocar no núcleo.** `POST /v1/sugestoes` com
   `alvo_tipo: "plataforma"` e `GET /v1/sugestoes/minhas`. A PRD-14 §9 nomeia a leitura como
   `GET /v1/eu/sugestoes`; a rota implementada no núcleo é `/v1/sugestoes/minhas`, mesma
   leitura, já consumida pela App 07 — precedente da change
   `2026-09-01-transparencia-termos-atendimento-e-propostas`. Alternativa descartada: criar o
   apelido `/v1/eu/sugestoes` no núcleo, que duplicaria rota por questão de nome.
2. **A área detalhada é uma tela da própria App 08, de leitura, alimentada pela tabela da
   PRD-14 §11.** Mesmo desenho da `TelaDeDireitos` das Apps 03 e 09, com a §11 declarada em
   comentário como fonte única. Alternativas descartadas: apontar para a vitrine (PRD-03 ainda
   não entregue) e criar rota de leitura no núcleo (o conteúdo é do PRD, não do banco).
3. **`ProvedorDeDireitos` e `AvisoDeColeta` locais à App 08**, como nas Apps 03, 07 e 09: o
   `App.tsx` decide a área e o contexto leva o callback até o aviso, sem prop-drilling.
   Alternativa descartada: promover a `comum/react`, porque o destino do aviso é a navegação de
   cada aplicação — a promoção é decisão de outra fatia.
4. **O aviso e a área detalhada existem sem sessão.** A porta pública de pré-cadastro coleta
   dado antes de haver Apoiador (PRD-14 §11), então o provedor envolve também a árvore sem
   sessão e a tela de direitos só mostra a ação de sair quando há sessão.
5. **O canal fechado é garantia negativa verificada por teste** (`RF-14-59`): um teste renderiza
   as telas da aplicação e falha se aparecer campo de mensagem ou rótulo de telefone ou e-mail
   de Guerreiro(a), família ou Mestre. Alternativa descartada: confiar na revisão de código.

## Risks / Trade-offs

- [A tabela da §11 fica duplicada em código e envelhece] → comentário apontando a §11 como fonte
  única, como já se fez nas Apps 03 e 09; mudança na §11 muda a lista na mesma change.
- [Nove avisos podem virar ruído visual] → `role="status"`, discreto, sem bloquear a tela nem
  exigir confirmação, e nomeando só o dado daquela tela.
- [O teste de canal fechado pode dar falso verde varrendo texto] → ele afirma a ausência de
  campo de entrada de mensagem e dos rótulos de contato em cada tela renderizada, não a ausência
  de uma palavra no bundle.
