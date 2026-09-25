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
  | "trilhas";

// Os sete glifos, desenhados na grade de `24` px do documento 15 §11.1.
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
