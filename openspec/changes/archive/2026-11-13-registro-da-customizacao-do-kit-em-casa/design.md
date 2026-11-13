# Design

## Context

O núcleo serve tudo (`openspec/specs/customizacao-do-kit/`): `GET /v1/eu/customizacoes` devolve
`kits_abertos` — cada um com `recompensa_de_marco_id`, `ultimo_aprovado` e `pendente` — e
`registros`, com `situacao`, `tem_midia` e `motivo_do_julgamento`; `POST /v1/eu/customizacoes`
grava o registro sem mídia; `/v1/customizacoes/{id}/envios`, `/envios/confirmacao` e
`/cancelamento` completam o ciclo. A App 01 já tem o envio em partes em
`src/api/cuidadoDoBem.ts` (`enviarMidiaDaCustomizacao`) e a captura do Mestre em
`cuidado/TelaDoCuidadoNoEncontro.tsx`, que é o molde do formulário. O aviso segue o
`AvisoDaMidiaGuardada` de `comum/trilha/DesafioDeDesbloqueio.tsx`.

## Goals / Non-Goals

**Goals:** o registro e o acompanhamento em casa, num componente que a fatia 35 do PRD-04
consome sem cópia.

**Non-Goals:** mudar a captura na hora do Mestre; ligar a App 01 ao formulário novo (fatia 35);
mostrar na App 05 a mídia já enviada — o `RF-05-103` pede a situação, não a imagem.

## Decisions

1. **`comum/customizacao/`**, exportado como `comum/customizacao`: `api.ts` com
   `lerMinhasCustomizacoes`, `registrarMinhaCustomizacao`, `enviarMidiaDaCustomizacao` (movido
   da App 01, mesma assinatura) e `cancelarCustomizacao`; `RegistroDaCustomizacao.tsx`, o
   formulário; `indice.ts`. A App 01 passa a reexportar `enviarMidiaDaCustomizacao` por uma
   função local que delega ao `comum` — os `vi.spyOn` dos testes dela continuam valendo.
   Descartado: deixar o cliente na App 05 — a fatia 35 o copiaria.
2. **O formulário recebe** `entregaDeRecompensaId`, `registroIdInicial` (o pendente sem mídia,
   para retomar), `token`, `aoConcluir` e `aoCancelar`. Sem `registroIdInicial`, grava o
   registro e envia; com ele, só envia. O registro gravado com envio interrompido guarda o `id`
   no estado, e Tentar novamente reenvia ao mesmo — o padrão da decisão 5 da fatia 34.
3. **A junção é no `Conquistas.tsx`:** carrega `GET /v1/eu/recompensas` e `GET
   /v1/eu/customizacoes` juntos e casa por `recompensa_de_marco_id`. O "último registro" do kit
   é o mais recente de `registros` com aquela `entrega_de_recompensa_id`, por `registrado_em`.
   A tabela da spec decide a ação. Falha só na leitura das customizações não esconde as
   conquistas: o cartão segue como antes, com um aviso único de que a customização não carregou.
4. **Frases da tela**, além do aviso aprovado: "Aguardando a aula: mostre o kit ao Mestre no
   encontro. Se não for apresentado até o fim do ciclo, este registro expira."; "Aprovado pelo
   Mestre."; "O Mestre pediu um ajuste: {motivo}". As de fala reusam as da App 01
   ("Não foi possível entender a fala. Fale de novo ou escreva." e "Este aparelho não transcreve
   fala. Escreva a descrição.").
5. **`accept="image/*,video/*"`** e `capture="environment"`, como na captura da App 01: a
   câmera traseira aponta para o kit, não para o rosto.

## Risks / Trade-offs

- **Nasce dormente** enquanto nenhuma trilha declara recompensa nem kit apresentado — a pendência
  do catálogo de marcos (PRD-05 §14) trava o `RF-05-45` na prática, e com ele este.
- Uma leitura a mais ao abrir Conquistas; sem polling, como o resto da carteira.
