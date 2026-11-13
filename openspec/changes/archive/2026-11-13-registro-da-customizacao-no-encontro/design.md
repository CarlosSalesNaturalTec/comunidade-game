# Design

## Context

O registro já existe e é do `comum` (`openspec/specs/camada-visual-comum/`, "A camada comum
entrega o registro da customização do kit"): `comum/customizacao` tem o cliente das rotas da
criança e o `RegistroDaCustomizacao`. O que **não** subiu na fatia 18 do PRD-05 é o bloco que,
pelo último registro, decide a situação e a ação do kit — hoje `CustomizacaoDoKit` e
`ultimoRegistroDoKit`, privados de `apps/app-05-guerreiro/src/carteira/Conquistas.tsx`. Na App
01, o percurso da criança é `trilhas/TelaDeTrilhasDoGuerreiro.tsx`, já atrás da guarda de
presença e fechado sem rede, com o `token` da sessão do Guerreiro(a).

## Goals / Non-Goals

**Goals:** o registro, o acompanhamento e o cancelamento no percurso da App 01, pelo mesmo bloco
que a App 05 usa.

**Non-Goals:** mudar a App 05, o formulário do registro, a fila do Mestre ou o núcleo.

## Decisions

1. **`comum/customizacao/CustomizacaoDoKit.tsx`** recebe o bloco e `ultimoRegistroDoKit`, com
   as mesmas frases e as mesmas props de hoje (`kit`, `ultimo`, `token`, `formularioAberto`,
   `abrirFormulario`, `fecharFormulario`, `aoMudar`), mais o tipo `FormularioAberto`; tudo
   exportado no `indice.ts`. O estado de qual formulário está aberto fica em quem consome — um
   formulário aberto por vez, como na App 05. Descartado: copiar o bloco na App 01 — é a
   divergência que o `RF-04-80` proíbe.
2. **Os testes espiam `comum/customizacao/api`**, nova entrada do `package.json` no molde de
   `comum/trilha/api`: o bloco chama `cancelarCustomizacao` pelo `./api`, e o espião posto no
   `indice` não o alcança. O teste da App 05 troca só o alvo do `vi.spyOn`; as asserções ficam.
3. **Lugar na App 01:** uma seção "Customização dos seus kits", irmã de "Atividades do
   encontro", nos três estados do percurso — catálogo, lista de trilhas e guia (pelo slot
   `atividadesDoEncontro`). Cada kit se identifica por `tipo_de_recurso_nome` e `trilha_nome`,
   que a rota já devolve. Sem kit com `customizacao_aberta`, a seção não se monta. Descartado:
   caminho próprio na tela inicial — o `RF-04-80` diz "no próprio percurso".
4. **Leitura:** `lerMinhasCustomizacoes` sai com as duas leituras do percurso, mas em
   `catch` separado: a falha só dela vira o aviso "Não foi possível carregar a customização dos
   seus kits agora. Tente de novo em instantes." (o mesmo da App 05), e o percurso segue. Depois
   de registrar ou cancelar, só a customização é lida de novo.

## Risks / Trade-offs

- **Nasce dormente**, como a fatia 18 do PRD-05: sem trilha que declare recompensa e kit
  apresentado, nenhum kit abre (pendência do catálogo de marcos, PRD-05 §14).
- O atendimento termina ao voltar ao início e limpa a sessão da criança: um envio interrompido
  retoma pelo "pendente sem mídia" na próxima entrada, não no estado da tela.
