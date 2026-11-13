# Proposal

**Origem:** PRD-04 — Aula presencial (App 01), **fatia 35** do `openspec/cronograma-de-fatias.md`
("Registro da customização pela criança, no encontro"). Atende `RF-04-80` e o passo 1 da jornada
§5.13 do PRD-04, sob as regras do núcleo já vigentes (`RF-01-84`, `RF-01-86`, `RN-01-66`).
Decisão do fundador de 2026-11-12 (documento 09 §1, "Customização do kit recebido"). Depende da
fatia 34 do PRD-04, implementada, e consome o que a fatia 18 do PRD-05 subiu ao `comum`.

## Why

A criança só registra a customização em casa, na App 05; quem não tem aparelho em casa, ou
esqueceu, depende da captura na hora pelo Mestre. O `RF-04-80` põe o mesmo registro no percurso
dela no aparelho do encontro, "sem divergir da App 05" — e a fatia 18 do PRD-05 já deixou o
formulário e o cliente no `comum` para isso.

## What Changes

- **App 01 — percurso do Guerreiro(a):** o caminho **Trilhas e missões**, que é o percurso da
  criança no aparelho do encontro, passa a mostrar, ao lado das atividades do encontro, cada
  **kit recebido com customização aberta** e a situação do último registro dele, com a ação que
  cabe — registrar, retomar o envio, aguardar a aula e cancelar, ler o motivo e enviar de novo
  (`RF-04-80`, §5.13.1). Sem kit aberto, nada aparece. Nenhum caminho novo na tela inicial.
- **`comum/customizacao` — a situação e a ação do kit:** o bloco que decide, pelo último
  registro, o que o kit mostra e oferece sobe da App 05 ao `comum`, junto com a escolha do
  último registro do kit. A App 05 e a App 01 consomem o mesmo bloco: é isso que garante "sem
  divergir da App 05". A App 05 **não muda de comportamento**.
- **Sem rede**, o caminho já não abre (`RF-04-58`): nada do registro é enfileirado no aparelho.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `camada-visual-comum`: a situação e a ação da customização do kit passam a ser componente do
  `comum`, consumido pela App 05 e pela App 01.
- `aplicacao-da-aula-presencial`: o percurso do Guerreiro(a) no aparelho do encontro registra,
  acompanha e cancela a customização do kit aberto.

## Fora do escopo

- O julgamento, a captura na hora pelo Mestre e a conservação (`RF-04-81` a `RF-04-84`): fatia
  34 do PRD-04, entregue. A fila do Mestre não muda.
- O registro em casa (`RF-05-102`, `RF-05-103`): fatia 18 do PRD-05, entregue.
- A customização no portfólio (`RF-03-88`): fatia 14 do PRD-03.
- Conferência automática de "só o kit, sem rosto": é o Mestre da aula quem confere ao julgar.

## Impact

- **`comum/customizacao/`:** componente novo da situação e da ação do kit e a função do último
  registro, exportados no `indice.ts`, com o teste.
- **App 05:** `apps/app-05-guerreiro/src/carteira/Conquistas.tsx` passa a consumir o bloco do
  `comum`, sem mudar as asserções do teste dela.
- **App 01:** `apps/app-01-aula-presencial/src/trilhas/TelaDeTrilhasDoGuerreiro.tsx` e o teste
  dela.
- **Backend:** nenhum — as rotas existem (`openspec/specs/customizacao-do-kit/`).
- **Documentação:** PRD-04 §9 ganha as rotas da customização em que o ato é do Guerreiro(a); a
  linha da fatia 35 no cronograma.
