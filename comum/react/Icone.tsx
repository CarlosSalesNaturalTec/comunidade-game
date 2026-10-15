import type { ReactElement } from "react";

/** Os quatro tamanhos do documento 15 §11.1 — nenhum outro. */
export type TamanhoDeIcone = 16 | 24 | 32 | 48;

export type NomeDeGlifo =
  | "onboarding"
  | "presenca"
  | "equipes"
  | "quiz"
  | "medicao"
  | "troca"
  | "trilhas"
  // Os dois estados do alternador da narração e as duas ações de quem opera
  // o aparelho (decisão do fundador de 2026-10-14). `som` e `som-desligado`
  // são desenhos diferentes, não o mesmo em duas cores: o estado se
  // reconhece pela forma (documento 15 §5).
  | "som"
  | "som-desligado"
  | "encerrar"
  | "momento-de-troca"
  // Os glifos de poder do documento 15 §8.4 — um por poder do catálogo do
  // documento 02 §2, mais o genérico. Quem os escolhe pelo nome do poder é
  // `GlifoDePoder`; aqui são glifos como os demais, na mesma grade.
  | "poder"
  | "poder-ia-e-robotica"
  | "poder-do-territorio"
  | "poder-sustentador"
  | "poder-da-rima"
  | "poder-das-redes"
  | "poder-da-capoeira";

// Os glifos, desenhados na grade de `24` px do documento 15 §11.1.
// Nenhum declara cor: o traço é `currentColor`, herdado do texto que o ícone
// acompanha, e é assim que a camada semântica do §12 alcança o ícone sem
// repetir cor nenhuma — trocar o tema troca o ícone junto.
const GLIFOS: Record<NomeDeGlifo, ReactElement> = {
  // Pessoa com sinal de mais.
  onboarding: (
    <>
      <circle cx="10" cy="8" r="3.5" />
      <path d="M4 20c0-3.3 2.7-6 6-6s6 2.7 6 6" />
      <path d="M18 5v6M15 8h6" />
    </>
  ),
  // Visto dentro de círculo.
  presenca: (
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="m8 12 3 3 5-6" />
    </>
  ),
  // Duas silhuetas lado a lado.
  equipes: (
    <>
      <circle cx="9" cy="8" r="3" />
      <path d="M3 19c0-3 2.7-5 6-5s6 2 6 5" />
      <circle cx="17.5" cy="9.5" r="2.5" />
      <path d="M16.5 14.6c2.6.5 4.5 2.3 4.5 4.4" />
    </>
  ),
  // Balão de fala com interrogação.
  quiz: (
    <>
      <path d="M4 6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-7l-5 4v-4a2 2 0 0 1-2-2Z" />
      <path d="M10 8.5a2 2 0 1 1 2.7 1.9c-.5.2-.7.6-.7 1.1v.4" />
      <path d="M12 14.5h.01" />
    </>
  ),
  // Mira com escala.
  medicao: (
    <>
      <circle cx="12" cy="12" r="7" />
      <path d="M12 2v3M12 19v3M2 12h3M19 12h3" />
      <path d="M12 12h.01" />
    </>
  ),
  // Duas flechas em sentidos opostos.
  troca: (
    <>
      <path d="M3 9h14" />
      <path d="m14 6 3 3-3 3" />
      <path d="M21 15H7" />
      <path d="m10 18-3-3 3-3" />
    </>
  ),
  // Caminho em marcos, subindo da esquerda para a direita.
  trilhas: (
    <>
      <path d="M4 19h3l3-7h4l3-7h3" />
      <circle cx="4" cy="19" r="1.5" />
      <circle cx="12" cy="12" r="1.5" />
      <circle cx="20" cy="5" r="1.5" />
    </>
  ),
  // Alto-falante com as ondas saindo dele.
  som: (
    <>
      <path d="M11 5 6.5 9H3v6h3.5L11 19Z" />
      <path d="M15 9.5a3.5 3.5 0 0 1 0 5" />
      <path d="M17.5 7a7 7 0 0 1 0 10" />
    </>
  ),
  // O mesmo alto-falante, sem as ondas e cortado em X: a forma difere do
  // ligado, e não só a cor.
  "som-desligado": (
    <>
      <path d="M11 5 6.5 9H3v6h3.5L11 19Z" />
      <path d="m15.5 10 5 5M20.5 10l-5 5" />
    </>
  ),
  // Porta com a flecha saindo dela.
  encerrar: (
    <>
      <path d="M14 3h4a1.5 1.5 0 0 1 1.5 1.5v15A1.5 1.5 0 0 1 18 21h-4" />
      <path d="M10 12H3" />
      <path d="m6.5 8.5-3.5 3.5 3.5 3.5" />
    </>
  ),
  // A chave do momento: as duas flechas da troca dentro de uma janela que
  // abre e fecha. Não é o glifo `troca`, porque com o momento aberto os dois
  // cartões ficam encostados e têm funções opostas (design — decisão 6).
  "momento-de-troca": (
    <>
      <rect x="3" y="4.5" width="18" height="15" rx="2" />
      <path d="M7.5 10h7" />
      <path d="m12 7.5 2.5 2.5-2.5 2.5" />
      <path d="M16.5 14h-7" />
      <path d="m12 11.5-2.5 2.5 2.5 2.5" />
    </>
  ),
  // O genérico do documento 15 §8.4 — losango num círculo. Não é estrela nem
  // hexágono de propósito: a estrela é a grandeza ponto do §9 e o hexágono é a
  // silhueta do badge de protagonismo do §8.3, e o genérico não pode se
  // confundir com nenhum dos dois.
  poder: (
    <>
      <circle cx="12" cy="12" r="8.5" />
      <path d="M12 8l4 4-4 4-4-4Z" />
    </>
  ),
  // Cabeça de robô com antena.
  "poder-ia-e-robotica": (
    <>
      <rect x="5" y="8" width="14" height="11" rx="3" />
      <path d="M12 4.5v3.5" />
      <path d="M9.5 13h.01M14.5 13h.01" />
      <path d="M2.5 12v3M21.5 12v3" />
    </>
  ),
  // Marco fincado no chão do território.
  "poder-do-territorio": (
    <>
      <path d="M12 3a5.5 5.5 0 0 1 5.5 5.5c0 4-5.5 9.5-5.5 9.5S6.5 12.5 6.5 8.5A5.5 5.5 0 0 1 12 3Z" />
      <circle cx="12" cy="8.5" r="2" />
      <path d="M3 20.5h18" />
    </>
  ),
  // Mão aberta sustentando o que sobe.
  "poder-sustentador": (
    <>
      <path d="M12 3v7" />
      <path d="m8.5 6.5 3.5-3.5 3.5 3.5" />
      <path d="M3.5 13.5v2a5 5 0 0 0 5 5h7a5 5 0 0 0 5-5v-2" />
    </>
  ),
  // Microfone de mão.
  "poder-da-rima": (
    <>
      <rect x="9" y="2.5" width="6" height="11" rx="3" />
      <path d="M5.5 11.5a6.5 6.5 0 0 0 13 0" />
      <path d="M12 18v3.5M8.5 21.5h7" />
    </>
  ),
  // Câmera de vídeo.
  "poder-das-redes": (
    <>
      <rect x="2.5" y="6" width="13" height="12" rx="2.5" />
      <path d="m15.5 11 6-3.5v9L15.5 13Z" />
    </>
  ),
  // Figura em movimento, de pernas abertas.
  "poder-da-capoeira": (
    <>
      <circle cx="12" cy="4.5" r="2.5" />
      <path d="M12 7v6" />
      <path d="m12 13-4.5 7.5M12 13l5 7" />
      <path d="M12 9.5 5 7.5M12 9.5l7 1.5" />
    </>
  ),
};

interface Props {
  glifo: NomeDeGlifo;
  /** Um dos quatro tamanhos do documento 15 §11.1. */
  tamanho?: TamanhoDeIcone;
}

// O sistema de ícone do documento 15 §11.1: SVG embutido, servido pelo próprio
// domínio junto do pacote da aplicação — nunca buscado em domínio de terceiro,
// que o princípio 6 veda e que não herdaria a cor do texto.
//
// O ícone é sempre decorativo para a tecnologia assistiva (`aria-hidden`):
// quem o usa é dono do rótulo, e o documento 15 §5 não abre exceção — ícone
// nunca é a única forma de identificar um elemento acionável, e nunca
// substitui o rótulo que o elemento já tem. Quem navega por leitor de tela
// alcança o rótulo, não a descrição do desenho.
export function Icone({ glifo, tamanho = 24 }: Props) {
  return (
    <svg
      className="cg-icone"
      width={tamanho}
      height={tamanho}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
    >
      {GLIFOS[glifo]}
    </svg>
  );
}
