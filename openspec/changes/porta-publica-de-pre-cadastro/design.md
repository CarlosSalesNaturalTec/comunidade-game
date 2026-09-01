## Context

A rota do pré-cadastro já existe e é pública sob chave de aplicação —
`POST /v1/solicitacoes-de-participacao`, com aporte declarado, comprovante, nick reservado por
sete dias, recusa de documento pessoal e freio por origem na superfície
`formulario_participacao` (`openspec/specs/fila-de-avaliacao/spec.md`). A leitura das
necessidades em aberto também: `GET /v1/vitrine/necessidades`, pública, com
`quantidade_faltante` e `valor_em_moedas` (`openspec/specs/necessidade-de-recurso/spec.md`). O
que falta é a tela — e dois ajustes no núcleo. Motivação em `proposal.md`.

A App 08 nasceu inteiramente autenticada na fatia 1 e não tem roteador: `App.tsx` decide a tela
por estado.

## Goals / Non-Goals

**Goals:** a porta pública da App 08 com o pré-cadastro completo, o perfil declarado guardado no
núcleo e o formato do comprovante conferido lá.

**Non-Goals:** rota nova, entidade nova, homologação, e a opção "missão aberta" do `RF-14-02` —
ela depende de `MissaoDoApoiador`, da fatia 5 (decisão do fundador, 2026-09-01).

## Decisions

1. **A porta é a tela padrão de quem não tem sessão, e a entrada fica a um clique.** `App.tsx`
   ganha um estado a mais sem sessão — porta pública ou entrada —, no mesmo padrão da fatia 1.
   Descartado: roteador na App 08, que nenhuma das outras aplicações usa.
2. **O perfil vira coluna própria**, enum `PerfilDeApoiador` (`pessoa_fisica`,
   `pessoa_juridica`), nula na pretensão de Mestre, com migração Alembic. Descartado: embutir o
   perfil no texto do aporte declarado — a gestão não conseguiria lê-lo como dado.
3. **A escolha do aporte viaja no campo `aporte declarado`**, que o PRD-01 §8 já define como
   "necessidade, valor sugerido ou livre": a porta compõe a linha com a necessidade escolhida
   ou o valor, sempre com o equivalente em moedas. Descartado: campos estruturados novos, que o
   PRD-01 não prevê e que o Admin não usa — ele homologa lendo o comprovante.
4. **A escada e a conversão ficam na tela**, pela escala fixa de 1 moeda = R$ 10,00 e pelas duas
   escadas do documento 04 §2. Descartado: buscar a escada no núcleo — não há cadastro dela, e a
   escala é decisão fixa, não parâmetro de operação.
5. **Comprovante: obrigatoriedade na tela, formato no núcleo.** A mesma rota serve o formulário
   da vitrine, por onde entra quem apoia sem dinheiro (`RF-14-07`) e não tem comprovante a
   anexar; exigi-lo no núcleo fecharia esse caminho. A porta exige (`RF-14-04`) e o núcleo
   confere o formato quando o arquivo vem, com a mesma lista que `aportes` e `ressarcimentos`
   já aplicam.
6. **O freio por origem não muda**: a superfície `formulario_participacao` já cobre a rota com
   atraso progressivo. A porta apenas apresenta o 429 em linguagem simples e preserva o
   formulário preenchido (`RF-14-06`).
7. **O endereço do formulário da vitrine entra por variável de ambiente**
   (`VITE_URL_DO_FORMULARIO_DA_VITRINE`), vazia enquanto a App 06 não existir; sem valor, a tela
   explica o caminho em texto (decisão do fundador, 2026-09-01). Descartado: fixar o domínio
   agora, que renderia link quebrado.

Nada aqui tem custo de nuvem além da chamada já existente, e nenhum dado de território é
tocado — o pré-cadastro não gera lançamento no livro-razão: o `Aporte` só nasce na homologação
do Admin (`RN-14-01`, `RN-14-07`).

## Risks / Trade-offs

- **A porta pública amplia a superfície aberta da App 08** → nenhuma chamada dela usa token de
  sessão, e o núcleo já protege a rota com chave de aplicação e freio por origem.
- **O aporte declarado continua sendo texto** → o Admin homologa conferindo o comprovante, como
  hoje; a porta compõe o texto sempre no mesmo formato, para a fila ficar legível.
- **A porta nasce sem o aviso de coleta** que o PRD-14 §11 pede → é o `RF-14-58`, do recorte da
  fatia 8; a fatia 2 não o antecipa.

## Migration Plan

Uma migração Alembic acrescenta a coluna `perfil`, nula, à `solicitacao_de_participacao`. As
solicitações já registradas ficam sem perfil, o que é o correto: elas não o declararam. O
`downgrade` remove a coluna.
