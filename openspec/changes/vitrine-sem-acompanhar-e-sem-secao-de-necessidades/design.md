# Design

## Context

Remoção pura, sem núcleo nem contrato novo. O que existe está em
`openspec/specs/aplicacao-da-vitrine/spec.md`: a chamada das páginas individuais
(`convite/ChamadaDeParticipacao.tsx`, um componente para as quatro páginas), a porta em
`/quero-participar` com PIX e necessidades, e a seção "Necessidades em aberto" da abertura
(`pages/index.astro` → `NecessidadesEmAberto`, em `institucional/SecoesInstitucionais.tsx`).
A lista e a leitura (`ListaDeNecessidades`, `useNecessidades`) servem à porta e à seção.

## Goals / Non-Goals

**Goals:**

- As quatro páginas individuais trazem só "Quero apoiar".
- A abertura passa a nove seções, sem "Necessidades em aberto".
- A porta segue listando as necessidades (`RF-03-43`, `RF-03-47`) e a vitrine segue sem
  favorito (`RF-03-38`, `RN-03-15`).

**Non-Goals:**

- Núcleo, `GET /v1/vitrine/necessidades` e a App 08 — sem mudança.
- O caminho de favoritar Mestre do `RF-14-52`, que nunca teve tela (ver proposal); é do
  PRD-14 e vai ao fundador.

## Decisions

1. **Sai também o parágrafo de ajuda da chamada** ("Acompanhar favoritos é coisa de Apoiador
   cadastrado…"). Ele existia para explicar o botão; sem o botão, sobra só a frase do projeto
   (`RN-03-25`). O que é ser Apoiador, favoritos incluídos, segue explicado na porta
   (`RF-03-42`).
2. **`NecessidadesEmAberto` é apagado**, não escondido; `ListaDeNecessidades` e
   `useNecessidades` ficam, com o comentário da leitura compartilhada corrigido — a porta é a
   única consumidora.
3. **Requisito da chamada: REMOVED + ADDED**, e não MODIFIED, porque o título antigo afirmava
   a ação de acompanhar. O cenário de "sem rastro" mantém o nome e troca o gatilho pelo
   "Quero apoiar".
4. **Ordem da abertura**: as nove restantes mantêm a ordem de 2026-10-11, só sem a linha
   removida. Alternativa descartada: reordenar — não foi pedido.

## Risks / Trade-offs

- Quem tinha a abertura como caminho para as necessidades passa a vê-las só pela porta
  ("Quero apoiar", no herói e em toda página individual) → aceito pelo fundador.
