## Context

Fatia só de tela: `POST /v1/solicitacoes-de-participacao` (multipart) e
`POST /v1/solicitacoes-de-dados` (JSON) já existem com freio por origem, e devolvem só `id` e
`prazo` (`fila-de-avaliacao`, `protecao-das-rotas-publicas`). O padrão de navegação por endereço
próprio, de erro 429 explicado e de "sem rastro no aparelho" já está em `aplicacao-da-vitrine`
(página do Guerreiro, busca por nick). Nenhuma mudança no núcleo.

## Decisions

1. **Endereços próprios `/participar` e `/solicitar-dados`**, no padrão de `nickDoCaminho`
   (funções em `navegacao/recortes.ts`). Alternativa descartada: modal — o Mestre precisa de
   link direto na orientação do "Entrar".
2. **A seção "Solicitação do conjunto de dados"** dos dois recortes vira texto curto com botão
   para `/solicitar-dados`; o formulário não é duplicado dentro do recorte.
3. **O campo "recorte pedido" entra no formulário de dados**, obrigatório. O `RF-03-32` não o
   lista, mas o PRD-01 §8 e o núcleo o exigem em `SolicitacaoDeDados`; a tela apenas fornece o
   dado que o contrato já pede. Registrado como divergência de redação entre PRD-03 e PRD-01,
   sem regra nova.
4. **Pretensão Apoiador no formulário de participação** envia só os campos do `RF-03-27` e do
   `RF-03-28`. Aporte, perfil, comprovante e nick são do pré-cadastro da App 08 (PRD-03 §3.2) e
   não aparecem aqui; o núcleo os aceita como opcionais.
5. **Erros**: 422 do núcleo aponta o campo pelo nome que ele devolve; 429 usa o mesmo texto de
   espera da busca por nick — a função `esperaEmLinguagemSimples`, hoje privada em
   `PaginaDoGuerreiro.tsx`, sobe para módulo compartilhado da vitrine. O estado do formulário
   vive só em memória do componente: falhar ou ser freado não apaga o que foi digitado, e
   nada vai a `localStorage`, `sessionStorage` ou cookie (`RN-03-22`).
6. **Validação no cliente** só de presença dos campos obrigatórios, para apontar o campo antes
   do envio; formato de e-mail e demais regras ficam com o núcleo. Sem CAPTCHA.

## Risks / Trade-offs

- Dois formulários próximos podem ganhar componentes de campo repetidos: usar `Campo` e um
  campo de texto longo de `comum/react`; criar o que faltar ali só se os dois usarem.
- O link do Mestre passa a existir; o teste `entradaSemEnderecoPublicado` não trata dele
  (é dos destinos de outras aplicações) e segue valendo.
