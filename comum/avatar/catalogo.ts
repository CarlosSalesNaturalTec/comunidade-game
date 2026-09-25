// O catálogo fechado do avatar do Guerreiro(a) — as nove camadas do
// documento 15 §7.1, na ordem de composição delas. É conteúdo de domínio, e
// por isso mora em `comum/avatar/`, não em `comum/react/`, que guarda o
// contrato de acessibilidade dos componentes (design — decisão 1).
//
// Duas exigências do documento 15 §7 são deste arquivo, não de quem desenha:
//
// 1. **Nome dizível em português simples** em cada traço — "cabelo black
//    power", nunca "modelo 7": no onboarding o avatar nasce de características
//    ditas em voz alta por uma criança de 6 anos (`RF-04-06`).
// 2. **Representatividade como mecânica:** a escala de tons de pele abre pelo
//    **mais retinto** e as texturas de cabelo **crespo vêm antes das lisas**. É
//    a causa antirracista do projeto virando ordem de catálogo, e é requisito —
//    não arrumação de tabela.
//
// Nenhum traço carrega marca de gênero: todos são oferecidos a qualquer
// pessoa, e a forma de tratamento é campo próprio da persona.

/** As chaves do objeto versionado do documento 15 §7.2 — uma por camada. */
export type NomeDeCamada =
  | "fundo"
  | "tom"
  | "cabelo"
  | "cabelo_cor"
  | "rosto"
  | "olhos"
  | "boca"
  | "roupa"
  | "acessorio";

export interface TracoDoCatalogo {
  id: string;
  /** Nome dizível em português simples (documento 15 §7, exigência 2). */
  nome: string;
  /** Só nas camadas em que o traço **é** uma cor — fundo, tom de pele, cor do
   * cabelo e cor da íris. O fundo usa a camada semântica dos tokens; as
   * demais são escala própria do catálogo, que a paleta do documento 15 §3
   * não descreve. */
  cor?: string;
}

export interface CamadaDoCatalogo {
  nome: NomeDeCamada;
  /** Rótulo dizível da camada, para a tela de escolha. */
  rotulo: string;
  /** O traço em que a camada nasce, e onde cai o traço desconhecido
   * (documento 15 §7.2). */
  padrao: string;
  tracos: TracoDoCatalogo[];
}

// A escala de oito degraus do documento 15 §7.1, aberta pelo mais retinto.
const TONS_DE_PELE: TracoDoCatalogo[] = [
  { id: "t1", nome: "Pele retinta", cor: "#3a2418" },
  { id: "t2", nome: "Pele marrom escura", cor: "#4e3122" },
  { id: "t3", nome: "Pele marrom", cor: "#6b422b" },
  { id: "t4", nome: "Pele marrom clara", cor: "#8a5636" },
  { id: "t5", nome: "Pele morena", cor: "#a86d45" },
  { id: "t6", nome: "Pele morena clara", cor: "#c48a5f" },
  { id: "t7", nome: "Pele clara", cor: "#ddad83" },
  { id: "t8", nome: "Pele muito clara", cor: "#efd0ae" },
];

// As dez texturas do documento 15 §7.1, na ordem dele: as crespas — black
// power, crespo curto, tranças e dreads — antes das lisas.
const TEXTURAS_DE_CABELO: TracoDoCatalogo[] = [
  { id: "black-power", nome: "Cabelo black power" },
  { id: "crespo-curto", nome: "Cabelo crespo curto" },
  { id: "trancas", nome: "Cabelo de tranças" },
  { id: "dreads", nome: "Cabelo de dreads" },
  { id: "cacheado", nome: "Cabelo cacheado" },
  { id: "ondulado", nome: "Cabelo ondulado" },
  { id: "liso", nome: "Cabelo liso" },
  { id: "raspado", nome: "Cabelo raspado" },
  { id: "coque", nome: "Cabelo de coque" },
  { id: "rabo", nome: "Cabelo de rabo de cavalo" },
];

export const CAMADAS_DO_AVATAR: CamadaDoCatalogo[] = [
  {
    nome: "fundo",
    rotulo: "Cor do fundo",
    padrao: "marca-100",
    // Cor chapada da paleta (documento 15 §7.1), pela camada semântica dos
    // tokens — a primitiva não é referenciada fora de `tokens.css` (§12).
    tracos: [
      { id: "marca-100", nome: "Fundo laranja da marca", cor: "var(--cor-marca)" },
      { id: "acao-100", nome: "Fundo azul", cor: "var(--cor-acao)" },
      { id: "ponto-100", nome: "Fundo amarelo", cor: "var(--cor-ponto)" },
      { id: "moeda-100", nome: "Fundo verde", cor: "var(--cor-moeda)" },
      { id: "cal-050", nome: "Fundo claro", cor: "var(--cor-superficie)" },
      { id: "tinta-100", nome: "Fundo cinza", cor: "var(--cor-separador)" },
    ],
  },
  { nome: "tom", rotulo: "Tom de pele", padrao: "t1", tracos: TONS_DE_PELE },
  { nome: "cabelo", rotulo: "Cabelo", padrao: "black-power", tracos: TEXTURAS_DE_CABELO },
  {
    nome: "cabelo_cor",
    rotulo: "Cor do cabelo",
    padrao: "c1",
    tracos: [
      { id: "c1", nome: "Cabelo preto", cor: "#1b1b1f" },
      { id: "c2", nome: "Cabelo castanho escuro", cor: "#3b2417" },
      { id: "c3", nome: "Cabelo castanho", cor: "#5e3a1e" },
      { id: "c4", nome: "Cabelo castanho claro", cor: "#8a5a2b" },
      { id: "c5", nome: "Cabelo ruivo", cor: "#a23b13" },
      { id: "c6", nome: "Cabelo loiro", cor: "#d9a94a" },
      { id: "c7", nome: "Cabelo grisalho", cor: "#b9bec9" },
      { id: "c8", nome: "Cabelo azul de fantasia", cor: "#2f6fe0" },
      { id: "c9", nome: "Cabelo rosa de fantasia", cor: "#e0468f" },
      { id: "c10", nome: "Cabelo verde de fantasia", cor: "#1f9d6a" },
    ],
  },
  {
    nome: "rosto",
    rotulo: "Formato do rosto",
    padrao: "r1",
    tracos: [
      { id: "r1", nome: "Rosto redondo" },
      { id: "r2", nome: "Rosto oval" },
      { id: "r3", nome: "Rosto quadrado" },
      { id: "r4", nome: "Rosto de queixo fino" },
    ],
  },
  {
    nome: "olhos",
    rotulo: "Olhos",
    padrao: "o1",
    // "Formato e cor" numa camada só, como o documento 15 §7.1 a descreve.
    tracos: [
      { id: "o1", nome: "Olhos castanhos redondos", cor: "#4a2c18" },
      { id: "o2", nome: "Olhos castanhos puxados", cor: "#4a2c18" },
      { id: "o3", nome: "Olhos escuros redondos", cor: "#20242e" },
      { id: "o4", nome: "Olhos escuros puxados", cor: "#20242e" },
      { id: "o5", nome: "Olhos verdes redondos", cor: "#2f6b45" },
      { id: "o6", nome: "Olhos azuis puxados", cor: "#2f5f9e" },
    ],
  },
  {
    nome: "boca",
    rotulo: "Boca",
    padrao: "b1",
    tracos: [
      { id: "b1", nome: "Boca sorrindo" },
      { id: "b2", nome: "Boca fechada" },
      { id: "b3", nome: "Boca sorrindo de lado" },
      { id: "b4", nome: "Boca rindo" },
    ],
  },
  {
    nome: "roupa",
    rotulo: "Roupa",
    padrao: "camisa-projeto",
    tracos: [
      { id: "camisa", nome: "Camisa" },
      { id: "regata", nome: "Regata" },
      { id: "jaqueta", nome: "Jaqueta" },
      { id: "moletom", nome: "Moletom" },
      { id: "camisa-projeto", nome: "Camisa do projeto" },
    ],
  },
  {
    nome: "acessorio",
    rotulo: "Acessório",
    padrao: "nenhum",
    tracos: [
      { id: "nenhum", nome: "Nenhum acessório" },
      { id: "oculos", nome: "Óculos" },
      { id: "bone", nome: "Boné" },
      { id: "tiara", nome: "Tiara" },
      { id: "fone", nome: "Fone de ouvido" },
      { id: "lenco", nome: "Lenço na cabeça" },
    ],
  },
];

/** A camada pelo nome, para quem precisa do rótulo ou dos traços dela. */
export function camadaDoAvatar(nome: NomeDeCamada): CamadaDoCatalogo {
  const camada = CAMADAS_DO_AVATAR.find((candidata) => candidata.nome === nome);
  if (!camada) throw new Error(`Camada de avatar desconhecida: ${nome}`);
  return camada;
}

/** O traço, quando o catálogo o conhece — `null` quando não. É o que sustenta
 * a regra do documento 15 §7.2: traço desconhecido cai no padrão da camada. */
export function tracoDoCatalogo(nome: NomeDeCamada, id: string): TracoDoCatalogo | null {
  return camadaDoAvatar(nome).tracos.find((traco) => traco.id === id) ?? null;
}
