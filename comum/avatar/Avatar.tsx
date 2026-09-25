import type { ReactElement } from "react";
import "./estilos.css";
import { camadaDoAvatar, type NomeDeCamada, tracoDoCatalogo } from "./catalogo";
import { type AvatarDoGuerreiro, lerAvatar, resolverAvatar } from "./objeto";

// O renderizador do avatar: **SVG embutido**, composto no próprio aparelho, na
// ordem das nove camadas do documento 15 §7.1. Mesma razão do sistema de ícone
// do §11.1 — nada é buscado em domínio de terceiro nem no núcleo, que o
// princípio 6 veda e que o §7 proíbe de outra forma: o avatar é do aparelho, e
// o App 04 joga com o catálogo guardado.
//
// Cada camada sai num `<g data-camada>` com o nome dela no objeto do §7.2, na
// ordem da tabela — é a ordem de pintura, e é o que se confere no teste. As
// camadas 3 e 4 são as duas faces do cabelo: a 3 traz a **massa** do penteado e
// a 4 o **comprimento** que cai atrás, ambas na cor escolhida na camada 4. As
// duas ficam antes do rosto, que é pintado por cima — o que aparece do penteado
// é o que passa da silhueta do rosto.

const GRADE = 64;

const COR_DA_ESCLERA = "#ffffff";
const COR_DO_TRACO_DA_BOCA = "#5a2b2b";

// Camada 3 — a massa do penteado, atrás do rosto.
const MASSAS_DE_CABELO: Record<string, ReactElement> = {
  "black-power": <circle cx="32" cy="27" r="18" />,
  "crespo-curto": <path d="M15 31a17 15 0 0 1 34 0Z" />,
  trancas: <path d="M17 30a15 15 0 0 1 30 0Z" />,
  dreads: <path d="M16 30a16 15 0 0 1 32 0Z" />,
  cacheado: <ellipse cx="32" cy="27" rx="16" ry="14" />,
  ondulado: <ellipse cx="32" cy="28" rx="15" ry="13" />,
  liso: <path d="M17 32a15 16 0 0 1 30 0Z" />,
  raspado: <path d="M21 30a11 10 0 0 1 22 0Z" />,
  coque: (
    <>
      <circle cx="32" cy="10" r="6" />
      <path d="M18 31a14 14 0 0 1 28 0Z" />
    </>
  ),
  rabo: <path d="M18 31a14 14 0 0 1 28 0Z" />,
};

// Camada 4 — o comprimento, na cor escolhida. Penteado curto não tem nenhum, e
// a camada sai vazia: a ordem das nove continua a mesma.
const COMPRIMENTOS_DE_CABELO: Record<string, ReactElement | null> = {
  "black-power": null,
  "crespo-curto": null,
  trancas: <path d="M16 26h6v26h-6zM42 26h6v26h-6z" />,
  dreads: <path d="M15 26h4v22h-4zM22 26h3v20h-3zM39 26h3v20h-3zM45 26h4v22h-4z" />,
  cacheado: <path d="M14 28q-2 14 4 20h4q-6-8-4-20zM50 28q2 14-4 20h-4q6-8 4-20z" />,
  ondulado: <path d="M16 28q-1 12 3 18h4q-5-8-3-18zM48 28q1 12-3 18h-4q5-8 3-18z" />,
  liso: <path d="M17 28v20h5V28zM42 28v20h5V28z" />,
  raspado: null,
  coque: null,
  rabo: <path d="M44 24q10 4 8 16-4 8-10 4 6-8 2-20z" />,
};

const ROSTOS: Record<string, ReactElement> = {
  r1: <circle cx="32" cy="31" r="13" />,
  r2: <ellipse cx="32" cy="31" rx="11.5" ry="14" />,
  r3: <rect x="20" y="18" width="24" height="26" rx="6" />,
  r4: <path d="M20 27a12 12 0 0 1 24 0c0 10-5.5 17-12 17s-12-7-12-17Z" />,
};

const OLHOS_PUXADOS = new Set(["o2", "o4", "o6"]);

function olhos(id: string, cor: string): ReactElement {
  const puxados = OLHOS_PUXADOS.has(id);
  return (
    <>
      {[26.5, 37.5].map((x) => (
        <g key={x}>
          {puxados ? (
            <ellipse cx={x} cy="31" rx="3.2" ry="2" fill={COR_DA_ESCLERA} />
          ) : (
            <circle cx={x} cy="31" r="2.8" fill={COR_DA_ESCLERA} />
          )}
          <circle cx={x} cy="31" r={puxados ? 1.3 : 1.4} fill={cor} />
        </g>
      ))}
    </>
  );
}

const BOCAS: Record<string, ReactElement> = {
  b1: <path d="M27.5 37.5q4.5 4 9 0" />,
  b2: <path d="M28 38.5h8" />,
  b3: <path d="M28 37.8q5 3.4 8-.6" />,
  b4: <path d="M27.5 37q4.5 5.5 9 0Z" fill="#7a2f3a" stroke="none" />,
};

const TORSO = "M17 64v-8a15 13 0 0 1 30 0v8Z";

const ROUPAS: Record<string, { cor: string; forma: ReactElement }> = {
  camisa: {
    cor: "var(--cor-acao)",
    forma: (
      <>
        <path d={TORSO} />
        <path
          d="M28 51l4 5 4-5"
          fill="none"
          stroke="var(--cor-superficie)"
          strokeWidth="1.6"
        />
      </>
    ),
  },
  regata: {
    cor: "var(--cor-moeda)",
    forma: (
      <>
        <path d="M20 64v-8a12 12 0 0 1 24 0v8Z" />
        <path
          d="M26 52q6 8 12 0"
          fill="none"
          stroke="var(--cor-superficie)"
          strokeWidth="1.6"
        />
      </>
    ),
  },
  jaqueta: {
    cor: "var(--cor-texto-secundario)",
    forma: (
      <>
        <path d={TORSO} />
        <path d="M32 51v13" stroke="var(--cor-superficie)" strokeWidth="1.4" />
      </>
    ),
  },
  moletom: {
    cor: "var(--cor-ponto)",
    forma: (
      <>
        <path d={TORSO} />
        <path
          d="M24 52a8 8 0 0 0 16 0"
          fill="none"
          stroke="var(--cor-superficie)"
          strokeWidth="1.6"
        />
      </>
    ),
  },
  "camisa-projeto": {
    cor: "var(--cor-marca)",
    forma: (
      <>
        <path d={TORSO} />
        <path d="M17 58h30" stroke="var(--cor-sobre-marca)" strokeWidth="2" />
      </>
    ),
  },
};

const ACESSORIOS: Record<string, ReactElement | null> = {
  nenhum: null,
  oculos: (
    <g fill="none" stroke="var(--cor-texto)" strokeWidth="1.4">
      <circle cx="26.5" cy="31" r="4.2" />
      <circle cx="37.5" cy="31" r="4.2" />
      <path d="M30.7 31h2.6" />
    </g>
  ),
  bone: (
    <g fill="var(--cor-acao)">
      <path d="M18 26a14 12 0 0 1 28 0Z" />
      <path d="M44 23h9v3.5h-9z" />
    </g>
  ),
  tiara: (
    <path d="M19 24q13-10 26 0" fill="none" stroke="var(--cor-ponto)" strokeWidth="2.4" />
  ),
  fone: (
    <g fill="var(--cor-texto)">
      <path
        d="M17 30a15 15 0 0 1 30 0"
        fill="none"
        stroke="var(--cor-texto)"
        strokeWidth="2.2"
      />
      <rect x="13" y="28" width="6" height="9" rx="2.5" />
      <rect x="45" y="28" width="6" height="9" rx="2.5" />
    </g>
  ),
  lenco: <path d="M17 28a15 14 0 0 1 30 0Z" fill="var(--cor-moeda)" />,
};

/** A cor do traço, quando a camada guarda cor. O traço já vem resolvido pelo
 * catálogo, então a busca nunca falha. */
function cor(camada: NomeDeCamada, id: string): string {
  return tracoDoCatalogo(camada, id)?.cor ?? "";
}

interface Props {
  /** O que o núcleo guardou no campo `avatar` — texto opaco —, ou o objeto do
   * documento 15 §7.2 já montado, como na tela que compõe o avatar. Ausente,
   * vazio ou desconhecido desenha o avatar padrão do projeto (§7.3). */
  avatar: string | AvatarDoGuerreiro | null | undefined;
  /** Lado do desenho, em pixels. */
  tamanho?: number;
}

// O avatar é sempre decorativo para a tecnologia assistiva (`aria-hidden`),
// como o ícone do documento 15 §11.1: quem identifica o Guerreiro(a) é o
// **nick** ao lado, e o documento 15 §5 não admite desenho como única forma de
// identificar alguém (`RN-04-14`). Quem navega por leitor de tela alcança o
// nick, não a descrição do desenho.
export function Avatar({ avatar, tamanho = 48 }: Props) {
  const composto =
    typeof avatar === "string" || avatar === null || avatar === undefined
      ? lerAvatar(avatar)
      : resolverAvatar(avatar);

  const pele = cor("tom", composto.tom);
  const corDoCabelo = cor("cabelo_cor", composto.cabelo_cor);
  const roupa = ROUPAS[composto.roupa] ?? ROUPAS[camadaDoAvatar("roupa").padrao];
  const comprimento = COMPRIMENTOS_DE_CABELO[composto.cabelo];

  return (
    <svg
      className="cg-avatar"
      width={tamanho}
      height={tamanho}
      viewBox={`0 0 ${GRADE} ${GRADE}`}
      aria-hidden="true"
      focusable="false"
    >
      <g data-camada="fundo">
        <rect x="0" y="0" width={GRADE} height={GRADE} fill={cor("fundo", composto.fundo)} />
      </g>
      <g data-camada="tom" fill={pele}>
        <rect x="27" y="38" width="10" height="16" />
        <circle cx="19.5" cy="32" r="3.4" />
        <circle cx="44.5" cy="32" r="3.4" />
      </g>
      <g data-camada="cabelo" fill={corDoCabelo}>
        {MASSAS_DE_CABELO[composto.cabelo] ??
          MASSAS_DE_CABELO[camadaDoAvatar("cabelo").padrao]}
      </g>
      <g data-camada="cabelo_cor" fill={corDoCabelo}>
        {comprimento}
      </g>
      <g data-camada="rosto" fill={pele}>
        {ROSTOS[composto.rosto] ?? ROSTOS[camadaDoAvatar("rosto").padrao]}
      </g>
      <g data-camada="olhos">{olhos(composto.olhos, cor("olhos", composto.olhos))}</g>
      <g
        data-camada="boca"
        fill="none"
        stroke={COR_DO_TRACO_DA_BOCA}
        strokeWidth="1.6"
        strokeLinecap="round"
      >
        {BOCAS[composto.boca] ?? BOCAS[camadaDoAvatar("boca").padrao]}
      </g>
      <g data-camada="roupa" fill={roupa.cor}>
        {roupa.forma}
      </g>
      <g data-camada="acessorio">{ACESSORIOS[composto.acessorio]}</g>
    </svg>
  );
}
