import { PREFIXO_DA_PAGINA_DO_APOIADOR, PREFIXO_DA_PAGINA_DO_MESTRE } from "./caminhos";

/** Os três recortes de leitura do PRD-03 §6.2. Cada um tem **caminho
 * próprio**, e não é guardado em lugar nenhum: a raiz é sempre sociedade
 * civil, e quem volta à raiz volta ao padrão (`RF-03-25`, `RF-03-26`,
 * `RF-03-51`).
 *
 * Aqui mora só o que a navegação precisa. **Quais seções cada recorte abre, e
 * em que ordem, mora na página do recorte** em `src/pages/`: é ali que se vê,
 * seção a seção, o que sai no documento servido e o que é ilha (PRD-03 §10). */
export type ChaveDeRecorte = "sociedade-civil" | "pesquisadores" | "gestores-publicos";

export interface Recorte {
  chave: ChaveDeRecorte;
  caminho: string;
  rotulo: string;
}

export const RECORTES: Recorte[] = [
  { chave: "sociedade-civil", caminho: "/", rotulo: "Sociedade civil" },
  { chave: "pesquisadores", caminho: "/pesquisadores", rotulo: "Pesquisadores" },
  { chave: "gestores-publicos", caminho: "/gestores-publicos", rotulo: "Gestores públicos" },
];

export const RECORTE_PADRAO = RECORTES[0];

/** Caminho que não é de recorte nenhum cai no padrão: a vitrine é pública e
 * não tem tela trancada, então não há para onde recusar (`RF-03-25`). */
export function recorteDoCaminho(caminho: string): Recorte {
  return RECORTES.find((recorte) => recorte.caminho === caminho) ?? RECORTE_PADRAO;
}

const PREFIXO_DA_PAGINA_DO_GUERREIRO = "/guerreiros/";
const PREFIXO_DA_PAGINA_DA_COMUNIDADE = "/comunidades/";

/** O endereço próprio da página da comunidade, no mesmo padrão da página do
 * Guerreiro(a): compartilhável e alcançável direto (documento 11 §8.2). */
export function caminhoDaComunidade(id: string): string {
  return `${PREFIXO_DA_PAGINA_DA_COMUNIDADE}${encodeURIComponent(id)}`;
}

/** Devolve o identificador da comunidade no caminho, ou `null` quando o
 * caminho não é de página de comunidade. */
export function comunidadeDoCaminho(caminho: string): string | null {
  return identificadorDoCaminho(caminho, PREFIXO_DA_PAGINA_DA_COMUNIDADE);
}

/** A **página individual** é endereço próprio porque o `RF-03-03` a exige
 * compartilhável e alcançável direto. Devolve o nick do caminho, ou `null`
 * quando o caminho não é de página individual. */
export function nickDoCaminho(caminho: string): string | null {
  return identificadorDoCaminho(caminho, PREFIXO_DA_PAGINA_DO_GUERREIRO);
}

/** Devolve o identificador do Mestre no caminho, ou `null` quando o caminho
 * não é o da página individual dele (`RF-03-03`). */
export function mestreDoCaminho(caminho: string): string | null {
  return identificadorDoCaminho(caminho, PREFIXO_DA_PAGINA_DO_MESTRE);
}

/** O mesmo, para o Apoiador. */
export function apoiadorDoCaminho(caminho: string): string | null {
  return identificadorDoCaminho(caminho, PREFIXO_DA_PAGINA_DO_APOIADOR);
}

function identificadorDoCaminho(caminho: string, prefixo: string): string | null {
  if (!caminho.startsWith(prefixo)) return null;
  const id = decodeURIComponent(caminho.slice(prefixo.length));
  return id.length > 0 ? id : null;
}
