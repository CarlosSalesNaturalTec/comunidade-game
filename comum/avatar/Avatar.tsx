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
// ordem da tabela — é a ordem de pintura, e é o que se confere no teste.
//
// O que **se vê** de um penteado não é a massa dele: o rosto é pintado depois,
// e cobre quase tudo. Por isso cada textura se desenha em três lugares, e são
// esses três que a distinguem das outras (documento 15 §7.1):
//
// - a **massa** (camada 3), de que aparece só o que passa da silhueta do rosto;
// - o **comprimento** (camada 4), que precisa cair fora do rosto e fora da
//   largura do torso para não ser coberto pela roupa da camada 8;
// - a **frente** (dentro da camada 5), o cabelo que cai sobre a testa, pintado
//   por cima do rosto na cor da camada 4. É a parte que uma criança reconhece
//   primeiro, e é o que devolve desenho ao cabelo raspado.
//
// As formas saem de helpers paramétricos, não de `path` escrito à mão: é o que
// faz `bolhas` servir ao black power, ao crespo curto e ao cacheado com
// números diferentes, e o que torna o próximo penteado algumas linhas de dados.

const GRADE = 64;

const COR_DA_ESCLERA = "#ffffff";
const COR_DO_TRACO_DA_BOCA = "#5a2b2b";

// Realce da silhueta do rosto. Sem ele, cabelo preto (`c1`) sobre pele retinta
// (`t1`) — que é a composição padrão do projeto — não tem separação alguma.
// Branco translúcido serve aos oito tons sem acrescentar cor ao catálogo.
const COR_DO_REALCE = "rgba(255,255,255,0.22)";

// Fio de sombra do cabelo — a amarração do coque, o laço do rabo de cavalo.
const COR_DO_FIO = "rgba(0,0,0,0.22)";

/** Duas casas bastam na grade de 64, e evitam coordenada quilométrica. */
const casas = (valor: number) => Number(valor.toFixed(2));

function pontosEmElipse(
  cx: number,
  cy: number,
  rx: number,
  ry: number,
  quantidade: number,
  grauInicial: number,
  grauFinal: number,
): [number, number][] {
  return Array.from({ length: quantidade }, (_, indice) => {
    const t = quantidade === 1 ? 0.5 : indice / (quantidade - 1);
    const grau = ((grauInicial + (grauFinal - grauInicial) * t) * Math.PI) / 180;
    return [casas(cx + rx * Math.cos(grau)), casas(cy + ry * Math.sin(grau))];
  });
}

/** Cachos e bolhas de cabelo crespo: círculos ao longo de um arco de elipse. */
function bolhas(
  cx: number,
  cy: number,
  rx: number,
  ry: number,
  quantidade: number,
  grauInicial: number,
  grauFinal: number,
  raio: number,
): ReactElement {
  return (
    <>
      {pontosEmElipse(cx, cy, rx, ry, quantidade, grauInicial, grauFinal).map(([x, y]) => (
        <circle key={`${x}:${y}`} cx={x} cy={y} r={raio} />
      ))}
    </>
  );
}

/** Mecha reta de ponta arredondada — o lock do dread. `cx` é o centro dela. */
function mecha(cx: number, de: number, ate: number, largura: number): ReactElement {
  return (
    <rect
      x={casas(cx - largura / 2)}
      y={de}
      width={largura}
      height={casas(ate - de)}
      rx={casas(largura / 2)}
    />
  );
}

/** Trança: contas enfileiradas do alto até a ponta. */
function contas(
  cx: number,
  de: number,
  ate: number,
  raio: number,
  passo: number,
): ReactElement {
  const alturas: number[] = [];
  for (let y = de; y <= ate; y += passo) alturas.push(casas(y));
  return (
    <>
      {alturas.map((y) => (
        <circle key={`${cx}:${y}`} cx={cx} cy={y} r={raio} />
      ))}
    </>
  );
}

/** Mecha ondulada: a linha de centro oscila e as duas bordas a acompanham. */
function onda(
  cx: number,
  de: number,
  ate: number,
  largura: number,
  amplitude: number,
  periodo: number,
): ReactElement {
  const passos = 18;
  const centro = (indice: number): [number, number] => {
    const y = de + ((ate - de) * indice) / passos;
    return [cx + amplitude * Math.sin((2 * Math.PI * (y - de)) / periodo), y];
  };

  let d = "";
  for (let i = 0; i <= passos; i++) {
    const [x, y] = centro(i);
    d += `${i === 0 ? "M" : "L"}${casas(x - largura / 2)} ${casas(y)}`;
  }
  for (let i = passos; i >= 0; i--) {
    const [x, y] = centro(i);
    d += `L${casas(x + largura / 2)} ${casas(y)}`;
  }
  return <path d={`${d}Z`} />;
}

/** Fio de sombra sobre o cabelo, na mesma cor para qualquer cor de cabelo. */
function fio(d: string, largura: number): ReactElement {
  return (
    <path d={d} fill="none" stroke={COR_DO_FIO} strokeWidth={largura} strokeLinecap="round" />
  );
}

interface TexturaDeCabelo {
  /** Camada 3 — a massa do penteado, atrás do rosto. */
  massa: ReactElement;
  /** Camada 4 — o que cai, na cor escolhida. Penteado curto não tem. */
  comprimento: ReactElement | null;
  /** Dentro da camada 5 — o cabelo sobre a testa, por cima do rosto. */
  frente: ReactElement | null;
}

// As dez texturas do documento 15 §7.1, na ordem dele: as crespas — black
// power, crespo curto, tranças e dreads — antes das lisas.
const TEXTURAS_DE_CABELO: Record<string, TexturaDeCabelo> = {
  "black-power": {
    massa: (
      <>
        <ellipse cx="32" cy="25" rx="17.5" ry="16.5" />
        {bolhas(32, 25, 17, 16, 15, 160, 380, 3.1)}
      </>
    ),
    comprimento: null,
    frente: null,
  },
  "crespo-curto": {
    massa: (
      <>
        <path d="M15.5 33a16.5 18 0 0 1 33 0Z" />
        {bolhas(32, 33, 16.5, 18, 13, 186, 354, 2.2)}
      </>
    ),
    comprimento: null,
    frente: bolhas(32, 31, 13.6, 13.6, 9, 202, 338, 2.3),
  },
  trancas: {
    massa: <path d="M17 32a15 17 0 0 1 30 0Z" />,
    comprimento: (
      <>
        {contas(14.6, 27, 53, 2.2, 4.4)}
        {contas(18.4, 27, 44, 2.1, 4.4)}
        {contas(49.4, 27, 53, 2.2, 4.4)}
        {contas(45.6, 27, 44, 2.1, 4.4)}
      </>
    ),
    frente: bolhas(32, 31, 13.4, 13.4, 5, 208, 332, 2.6),
  },
  dreads: {
    massa: (
      <>
        <ellipse cx="32" cy="28" rx="16" ry="15" />
        {bolhas(32, 28, 15.5, 14.5, 11, 190, 350, 2)}
      </>
    ),
    comprimento: (
      <>
        {mecha(12.4, 26, 56, 2.8)}
        {mecha(15.9, 26, 50, 2.6)}
        {mecha(19.4, 27, 45, 2.4)}
        {mecha(48.8, 26, 54, 2.8)}
        {mecha(45.5, 26, 48, 2.6)}
        {mecha(42.2, 27, 45, 2.4)}
      </>
    ),
    frente: (
      <>
        {bolhas(32, 31, 13.2, 13.2, 7, 204, 336, 2.1)}
        {mecha(23, 19, 27, 2.2)}
        {mecha(31, 18, 28, 2.2)}
        {mecha(39, 19, 27, 2.2)}
      </>
    ),
  },
  cacheado: {
    massa: (
      <>
        <ellipse cx="32" cy="27.5" rx="16" ry="14.5" />
        {bolhas(32, 27.5, 15.5, 14, 9, 172, 368, 3.5)}
      </>
    ),
    comprimento: (
      <>
        <circle cx="14.5" cy="37" r="3.4" />
        <circle cx="13.5" cy="43" r="3.2" />
        <circle cx="15.2" cy="48.5" r="3" />
        <circle cx="49.5" cy="37" r="3.4" />
        <circle cx="50.5" cy="43" r="3.2" />
        <circle cx="48.8" cy="48.5" r="3" />
      </>
    ),
    frente: (
      <>
        <circle cx="24.5" cy="21.5" r="3.2" />
        <circle cx="32" cy="19.5" r="3.4" />
        <circle cx="39.5" cy="21.5" r="3.2" />
      </>
    ),
  },
  ondulado: {
    massa: <path d="M16.8 32a15.2 17 0 0 1 30.4 0Z" />,
    comprimento: (
      <>
        {onda(15.2, 25, 50, 5.2, 2.2, 13)}
        {onda(48.8, 25, 50, 5.2, -2.2, 13)}
      </>
    ),
    frente: (
      <path d="M19 26.4c4-5.2 9.4-6.6 13.4-5.4 4 1.2 8.6 3.8 12.6 6.8A14.6 16.6 0 0 0 19 26.4Z" />
    ),
  },
  liso: {
    massa: <path d="M16.4 32.5a15.6 17.5 0 0 1 31.2 0Z" />,
    comprimento: (
      <>
        <path d="M12.9 50V33.4q0-8.4 6.3-10V50Z" />
        <path d="M51.1 50V33.4q0-8.4-6.3-10V50Z" />
      </>
    ),
    frente: (
      <path d="M17.6 26.2c4.4-5.4 10.4-6.8 15.2-5.6 4.8 1.2 9.2 4 13.6 7.2A15 17 0 0 0 17.6 26.2Z" />
    ),
  },
  raspado: {
    // A massa passa 2 unidades da silhueta e a frente traz a linha do cabelo
    // baixa com as duas costeletas: sem elas o raspado não desenhava nada, e
    // levava junto a camada da cor do cabelo.
    massa: <path d="M17.4 31.5a14.6 16 0 0 1 29.2 0Z" />,
    comprimento: null,
    frente: (
      <>
        <path d="M19.6 26.4a12.9 12.9 0 0 1 24.8 0q-5.2-6.6-12.4-6.6t-12.4 6.6Z" />
        <path d="M18.9 23.6h2.8v5.4h-2.8z" />
        <path d="M42.3 23.6h2.8v5.4h-2.8z" />
      </>
    ),
  },
  coque: {
    massa: (
      <>
        <path d="M18 31.5a14 16.5 0 0 1 28 0Z" />
        <circle cx="32" cy="11.8" r="6" />
        {fio("M26.8 16.8q5.2 3.2 10.4 0", 1.8)}
      </>
    ),
    comprimento: null,
    frente: <path d="M19.4 25.6a13 13 0 0 1 25.2 0q-6-4.8-12.6-4.8t-12.6 4.8Z" />,
  },
  rabo: {
    massa: <path d="M17.6 31.5a14.4 16.5 0 0 1 28.8 0Z" />,
    comprimento: (
      <>
        <path d="M44 22.6q9.6 2.4 10.8 13.4 1.2 9.4-5.6 13.8-3.8 2.4-5-1.6 5.4-5.2 4.8-12.4-.6-7.8-7-11.6Z" />
        {fio("M44.4 24.2q2.6 1.4 4.4 3.6", 1.8)}
      </>
    ),
    frente: <path d="M19.4 25.8a13 13 0 0 1 25.2 0q-5.4-5.8-13-5.4-7.6.4-12.2 5.4Z" />,
  },
};

const ROSTOS: Record<string, ReactElement> = {
  r1: <circle cx="32" cy="31" r="13" />,
  r2: <ellipse cx="32" cy="31" rx="11.5" ry="14" />,
  r3: <rect x="20" y="18" width="24" height="26" rx="6" />,
  r4: <path d="M20 27a12 12 0 0 1 24 0c0 10-5.5 17-12 17s-12-7-12-17Z" />,
};

// As orelhas são do grupo do rosto, não do tom de pele: pintadas na camada 2
// elas ficavam atrás do cabelo, e o black power as engolia por inteiro.
const ORELHAS = (
  <>
    <circle cx="19.5" cy="32" r="3.4" />
    <circle cx="44.5" cy="32" r="3.4" />
  </>
);

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
  const cabelo =
    TEXTURAS_DE_CABELO[composto.cabelo] ?? TEXTURAS_DE_CABELO[camadaDoAvatar("cabelo").padrao];

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
      </g>
      <g data-camada="cabelo" fill={corDoCabelo}>
        {cabelo.massa}
      </g>
      <g data-camada="cabelo_cor" fill={corDoCabelo}>
        {cabelo.comprimento}
      </g>
      <g data-camada="rosto" fill={pele}>
        {ORELHAS}
        <g stroke={COR_DO_REALCE} strokeWidth="1">
          {ROSTOS[composto.rosto] ?? ROSTOS[camadaDoAvatar("rosto").padrao]}
        </g>
        <g fill={corDoCabelo}>{cabelo.frente}</g>
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
      {/* O contorno da roupa é o mesmo fio que as peças já usam nos detalhes:
          sem ele o torso some quando a cor da roupa coincide com a do fundo, e
          quatro das seis cores de fundo têm peça de cor idêntica. */}
      <g
        data-camada="roupa"
        fill={roupa.cor}
        stroke="var(--cor-superficie)"
        strokeWidth="1.2"
        strokeLinejoin="round"
      >
        {roupa.forma}
      </g>
      <g data-camada="acessorio">{ACESSORIOS[composto.acessorio]}</g>
    </svg>
  );
}
