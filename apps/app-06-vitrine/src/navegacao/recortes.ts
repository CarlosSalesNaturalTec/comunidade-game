/** Os três recortes de leitura do PRD-03 §6.2. Cada um tem **caminho
 * próprio**, e não é guardado em lugar nenhum: a raiz é sempre sociedade
 * civil, e quem volta à raiz volta ao padrão (`RF-03-25`, `RF-03-26`,
 * `RF-03-51`). */
export type ChaveDeRecorte = "sociedade-civil" | "pesquisadores" | "gestores-publicos";

export interface Recorte {
  chave: ChaveDeRecorte;
  caminho: string;
  rotulo: string;
  /** Por onde este recorte entra na vitrine, na ordem em que o PRD-03 §5 o
   * descreve. Trocar de recorte muda a porta de entrada e a ordem — nunca o
   * conteúdo público disponível nem o direito de acesso (`RF-03-26`). */
  secoes: Secao[];
}

export interface Secao {
  titulo: string;
  /** O que ainda não existe, e por qual entrega chega. Esta fatia é o
   * esqueleto: o conteúdo de cada seção vem nas fatias 2 a 8 do PRD-03. */
  pendente: string;
}

const GUERREIROS: Secao = {
  titulo: "Guerreiros e Guerreiras",
  pendente: "Os cards e as páginas individuais chegam na próxima entrega.",
};
const PODERES: Secao = {
  titulo: "Poderes",
  pendente: "Os cards dos poderes chegam na próxima entrega.",
};
const MESTRES: Secao = {
  titulo: "Mestres",
  pendente: "Os cards e as páginas dos Mestres chegam em entrega própria.",
};
const APOIADORES: Secao = {
  titulo: "Apoiadores",
  pendente: "Os cards e as páginas dos Apoiadores chegam em entrega própria.",
};
const COMUNIDADES: Secao = {
  titulo: "Comunidades Virtuais",
  pendente: "O painel de cada comunidade chega em entrega própria.",
};
const TERRITORIO: Secao = {
  titulo: "Séries do território e metodologia",
  pendente: "As séries e a metodologia de cada uma chegam em entrega própria.",
};
const COBERTURA: Secao = {
  titulo: "Cobertura da Agenda 2030",
  pendente: "O painel de cobertura por comunidade e por ciclo chega em entrega própria.",
};
const SOLICITACAO_DE_DADOS: Secao = {
  titulo: "Solicitação do conjunto de dados",
  pendente: "O formulário de solicitação de dados chega em entrega própria.",
};
const BLOCO_DO_GESTOR: Secao = {
  titulo: "Para que a plataforma serve ao município",
  pendente: "O bloco em destaque do gestor público chega em entrega própria.",
};
const COMO_APOIAR: Secao = {
  titulo: "Como apoiar",
  pendente: "O conteúdo institucional e as necessidades em aberto chegam em entrega própria.",
};

// A sexta seção de cards do PRD-03 §3.1 — **batalhas** — não entra: o dado é
// do PRD-10 e a rota não existe. Decisão do fundador de 2026-09-26.
export const RECORTES: Recorte[] = [
  {
    chave: "sociedade-civil",
    caminho: "/",
    rotulo: "Sociedade civil",
    secoes: [GUERREIROS, PODERES, MESTRES, APOIADORES, COMUNIDADES, COMO_APOIAR],
  },
  {
    chave: "pesquisadores",
    caminho: "/pesquisadores",
    rotulo: "Pesquisadores",
    secoes: [TERRITORIO, COMUNIDADES, COBERTURA, SOLICITACAO_DE_DADOS],
  },
  {
    chave: "gestores-publicos",
    caminho: "/gestores-publicos",
    rotulo: "Gestores públicos",
    secoes: [BLOCO_DO_GESTOR, TERRITORIO, COBERTURA, SOLICITACAO_DE_DADOS],
  },
];

export const RECORTE_PADRAO = RECORTES[0];

/** Caminho que não é de recorte nenhum cai no padrão: a vitrine é pública e
 * não tem tela trancada, então não há para onde recusar (`RF-03-25`). */
export function recorteDoCaminho(caminho: string): Recorte {
  return RECORTES.find((recorte) => recorte.caminho === caminho) ?? RECORTE_PADRAO;
}
