PRD-04 (App 01 — Aula presencial), **fatia 15** — fatia nova, não prevista, acrescentada ao
`openspec/cronograma-de-fatias.md` com esta change. Alcança também o PRD-01 (o núcleo, onde o
limiar mora e como a comparação o lê) e o PRD-02 (a tela de consulta na gestão).

Cria os identificadores `RF-04-66`, `RN-04-35`, `RF-01-73`, `RN-01-56` e `RF-02-109`, a partir
da **decisão do fundador de 2026-09-18**, e amplia `RF-04-63` e `RN-04-32`.

## Why

O limiar de comparação é hoje variável de ambiente — uma só, para a plataforma inteira — e vale
**0,5**, a convenção do `face-api.js` de descritor normalizado de 128 posições. A escala da
biblioteca Human está na casa de **~10**, então **nenhuma criança é reconhecida**, e a falha é
silenciosa: a comparação que não confere registra recusa, a criança entra pela confirmação
humana, e o desfecho é idêntico ao de quem não tem _template_.

A bancada da fatia 14 já mede a distância no aparelho do encontro. O que falta é o resto do
caminho, e ele tem três buracos:

1. **A bancada não sabe o que está medindo.** As capturas da mesma pessoa (o **piso**) e as de
   pessoas diferentes (o **teto**) saem na mesma lista, sem rótulo. Só a memória de quem opera
   distingue as duas séries — e é a folga entre elas que define se existe limiar viável.
2. **O número medido não tem para onde ir.** Gravá-lo exige editar um segredo no Secret Manager
   e refazer o _deploy_: um ato de infraestrutura para um parâmetro que quem conduz o encontro
   acabou de medir com a câmera na mão.
3. **Um valor só não serve.** O limiar depende da câmera e da luz da sala — e o projeto tem um
   ponto de apoio por espaço, em comunidades diferentes. Um valor global nasce errado para o
   segundo ponto de apoio.

A decisão do fundador, de 2026-09-18: o limiar **deixa de ser parâmetro de implantação** e passa
a ser **dado medido de cada ponto de apoio**, gravado pela própria bancada ao fim de uma medição
concluída. Ponto de apoio sem limiar medido **não reconhece ninguém** — e, para que isso não seja
mais uma falha silenciosa, a gestão passa a mostrar quais pontos de apoio estão nessa situação.

## What Changes

- A **bancada** (`RF-04-63`) passa a medir em **duas séries declaradas** — piso e teto —, a
  apresentá-las separadas e a saber quando a medição está concluída (`RF-04-66`, `RN-04-35`).
- Concluída a medição, a bancada **propõe** o limiar e **grava** o valor confirmado por Mestre
  ou Admin, no ponto de apoio da aula em curso. O que viaja são **distâncias e o número**;
  descritor e imagem seguem sem sair do aparelho (`RF-04-66`, `RN-04-32`).
- O **núcleo** passa a ler o limiar do **ponto de apoio**, e não do ambiente. A variável
  `CG_BIOMETRIA_LIMIAR_DE_COMPARACAO` deixa de existir (`RF-01-73`).
- Ponto de apoio **sem limiar medido** faz a comparação **recusar**, com a recusa indistinguível
  das três causas que o `RN-01-22` já funde (`RN-01-56`).
- A **gestão** ganha a consulta do limiar vigente por ponto de apoio, com quem mediu, quando, as
  duas séries e o destaque de quem ainda não tem limiar (`RF-02-109`).
- Os documentos-fonte acompanham: o documento 03 §3.3 hoje diz que a medição **nada envia ao
  núcleo**, e isso deixa de ser verdade para o número e as distâncias.

Fica **fora**:

- **Editar** o limiar pela gestão. A tela do `RF-02-109` é de consulta: o número nasce de uma
  medição, e trocá-lo à mão desfaria a garantia de que todo limiar vigente foi medido.
- **Normalizar o descritor** antes de comparar. A hipótese de que a distância euclidiana crua
  varia com a luz mais do que com a identidade existe, e esta change a torna verificável —
  as séries ficam gravadas —, mas mexer no cálculo é decisão nova, com change própria.
- **Medir sobre Guerreiro(a)** fora do onboarding: o `RN-04-33` segue como está.
- A **primeira medição** em produção, que é ato de operação e acontece depois do _merge_.

## Capabilities

### New Capabilities

Nenhuma. O limiar é atributo do ponto de apoio, não capacidade nova.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: a bancada ganha as duas séries, o critério de conclusão, o
  valor proposto e a gravação; o Requirement que hoje afirma que ela nunca fala com o núcleo
  passa a distinguir **o que** nunca sai do aparelho (descritor e imagem) do que passa a sair
  (as distâncias e o número).
- `template-biometrico`: o limiar deixa de ser parâmetro de implantação e passa a ser dado
  medido do ponto de apoio, com histórico; ausência de limiar medido faz a comparação recusar.
- `sessao-do-guerreiro`: a rota de abertura por nick e imagem passa a receber a **aula** em que
  a entrada acontece — é ela que determina o ponto de apoio —, e a recusa por ponto de apoio sem
  limiar entra no conjunto indistinguível.
- `aplicacao-de-gestao`: a área Pontos de Apoio passa a apresentar o limiar vigente, a origem
  dele e quem ainda não tem.

## Impact

- `backend/src/nucleo/biometria/` — o modelo da medição, a regra que lê o limiar vigente e a
  comparação que passa a recusar sem ele.
- `backend/src/nucleo/configuracao.py` e `backend/README.md` — a variável que sai.
- `backend/src/nucleo/sessoes/rotas.py` e a rota da medição — o contrato novo.
- Migração Alembic — a tabela da medição.
- `apps/app-01-aula-presencial/src/bancada/` — as duas séries, o critério e a gravação.
- `apps/app-03-gestao/src/pontos-de-apoio/` — a consulta.
- `docs/03`, `docs/09`, `docs/99`, `docs/prds/prd-01`, `prd-02`, `prd-04` — a decisão e os
  identificadores novos.

**Substitui** a tarefa em aberto da change `2026-09-17-bancada-de-calibracao-do-limiar`, que
previa trocar o segredo pelo valor medido: o segredo deixa de existir.
