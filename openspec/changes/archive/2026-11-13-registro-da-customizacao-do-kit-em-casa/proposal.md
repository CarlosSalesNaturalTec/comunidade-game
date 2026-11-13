# Proposal

**Origem:** PRD-05 — Área do Guerreiro(a) (App 05), **fatia 18** do
`openspec/cronograma-de-fatias.md` ("Registro da customização do kit, em casa"). Atende
`RF-05-102` e `RF-05-103`, sob as regras do núcleo já vigentes (`RF-01-84`, `RF-01-86`,
`RN-01-66`). Decisão do fundador de 2026-11-12 (documento 09 §1, "Customização do kit
recebido") e duas respostas do fundador de 2026-11-13, abaixo. Depende da fatia "Customização do
kit recebido no núcleo" do PRD-01 e da fatia 31 do PRD-09, ambas implementadas.

## Why

O núcleo já recebe, guarda, julga e expira o registro da customização, e a App 01 já o julga no
encontro (fatia 34 do PRD-04), mas a criança não tem onde registrá-lo em casa: sem esta fatia,
todo registro depende da captura na hora pelo Mestre, e a criança não acompanha o que enviou nem
lê o motivo de um reprovado.

## What Changes

- **Lista de conquistas da App 05:** cada kit recebido com customização **aberta** passa a
  mostrar, no próprio cartão da conquista, a situação do último registro e a ação que cabe —
  sem aba nem caminho novo (resposta do fundador de 2026-11-13) (`RF-05-102`, `RF-05-103`).
- **Registro em casa:** foto ou vídeo **só do kit, sem rosto**, e a descrição por voz ou texto
  — a fala é transcrita no aparelho e cai no campo, editável —, com o **aviso** antes do envio,
  no texto aprovado pelo fundador em 2026-11-13, e o envio retomável com progresso
  (`RF-05-102`).
- **Acompanhamento:** aguardando a aula, aprovado, ou reprovado com o motivo e **Enviar de
  novo**; o pendente se **cancela**, e a tela diz que ele expira no fim do ciclo; o pendente
  sem mídia recebida retoma o envio do mesmo registro (`RF-05-103`).
- **`comum/customizacao`:** o cliente das rotas da criança e o formulário do registro sobem ao
  `comum`, porque a fatia 35 do PRD-04 registra pela criança no aparelho do encontro "sem
  divergir da App 05"; é o segundo uso que a fatia 34 deixou para esta decidir. A App 01
  **não muda de comportamento** nesta fatia.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `area-do-guerreiro`: a lista de conquistas registra e acompanha a customização do kit aberto.
- `camada-visual-comum`: o formulário do registro da customização, com o aviso, passa a ser
  componente do `comum`.

## Fora do escopo

- O registro pela criança no aparelho do encontro (`RF-04-80`): fatia 35 do PRD-04.
- A customização aprovada no portfólio da vitrine (`RF-03-88`): fatia 14 do PRD-03. O
  portfólio da App 05 não muda.
- O **acervo do Guerreiro(a)** na App 05: Ciclo 02 (PRD-05 §3.2).
- **Autorização de divulgação pública**: ato do responsável, na App 07 (PRD-05 §3.2).
- Conferência automática de "só o kit, sem rosto": é o Mestre da aula quem confere ao julgar.

## Impact

- **`comum/`:** pasta nova `customizacao/` (cliente e formulário), com a entrada em
  `package.json`; reúso de `comum/api` (envio em partes), `comum/fala` e `comum/react`.
- **App 05:** `apps/app-05-guerreiro/src/carteira/Conquistas.tsx` e o teste dele.
- **App 01:** `src/api/cuidadoDoBem.ts` passa a delegar o envio em partes ao `comum`, sem
  mudar a exportação nem as asserções.
- **Backend:** nenhum — as rotas existem (`openspec/specs/customizacao-do-kit/`).
- **Documentação:** PRD-05 §9 ganha as rotas da customização em que o ato é do Guerreiro(a);
  a linha da fatia 18 no cronograma.
