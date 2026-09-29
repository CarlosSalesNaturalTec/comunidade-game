import type { ReactNode } from "react";
import { SecaoDeApoiadores } from "../adultos/SecaoDeApoiadores";
import { SecaoDeMestres } from "../adultos/SecaoDeMestres";
import { SecaoDeSolicitacaoDeDados } from "../formularios/SecaoDeSolicitacaoDeDados";
import { SecaoDeGuerreiros } from "../guerreiros/SecaoDeGuerreiros";
import {
  SecaoComoApoiar,
  SecaoContatos,
  SecaoQuemSomos,
} from "../institucional/SecoesInstitucionais";
import { SecaoDePoderes } from "../poderes/SecaoDePoderes";
import { SecaoDoPortfolio } from "../portfolio/SecaoDoPortfolio";
import { SecaoDoRanking } from "../ranking/SecaoDoRanking";
import { BlocoDoGestor } from "../territorio/BlocoDoGestor";
import { SecaoDaCobertura } from "../territorio/SecaoDaCobertura";
import { SecaoDeComunidades } from "../territorio/SecaoDeComunidades";
import { PREFIXO_DA_PAGINA_DO_APOIADOR, PREFIXO_DA_PAGINA_DO_MESTRE } from "./caminhos";

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

export interface PropsDaSecao {
  irPara: (destino: string) => void;
}

export interface Secao {
  titulo: string;
  /** O que ainda não existe, e por qual entrega chega. As seções que já têm
   * conteúdo trazem `Conteudo`; as que faltam seguem com a frase. */
  pendente?: string;
  Conteudo?: (props: PropsDaSecao) => ReactNode;
}

const GUERREIROS: Secao = {
  titulo: "Guerreiros e Guerreiras",
  Conteudo: SecaoDeGuerreiros,
};
const PORTFOLIO: Secao = {
  titulo: "Portfólio de criações originais",
  Conteudo: SecaoDoPortfolio,
};
const RANKING: Secao = {
  titulo: "Ranking",
  Conteudo: SecaoDoRanking,
};
const PODERES: Secao = {
  titulo: "Poderes",
  Conteudo: SecaoDePoderes,
};
const MESTRES: Secao = {
  titulo: "Mestres",
  Conteudo: SecaoDeMestres,
};
const APOIADORES: Secao = {
  titulo: "Apoiadores",
  Conteudo: SecaoDeApoiadores,
};
const COMUNIDADES: Secao = {
  titulo: "Comunidades Virtuais",
  Conteudo: SecaoDeComunidades,
};
// As séries e a metodologia moram na **página de cada comunidade**, que o
// card abre: o painel é do território daquela comunidade, não de todas
// juntas (`RF-03-15`, documento 11 §8.2).
const TERRITORIO: Secao = {
  titulo: "Séries do território e metodologia",
  Conteudo: SecaoDeComunidades,
};
const COBERTURA: Secao = {
  titulo: "Cobertura da Agenda 2030",
  Conteudo: SecaoDaCobertura,
};
const SOLICITACAO_DE_DADOS: Secao = {
  titulo: "Solicitação do conjunto de dados",
  Conteudo: SecaoDeSolicitacaoDeDados,
};
const BLOCO_DO_GESTOR: Secao = {
  titulo: "Para que a plataforma serve ao município",
  Conteudo: BlocoDoGestor,
};
const QUEM_SOMOS: Secao = {
  titulo: "Quem somos",
  Conteudo: SecaoQuemSomos,
};
const COMO_APOIAR: Secao = {
  titulo: "Como apoiar",
  Conteudo: SecaoComoApoiar,
};
const CONTATOS: Secao = {
  titulo: "Contatos",
  Conteudo: SecaoContatos,
};

// A sexta seção de cards do PRD-03 §3.1 — **batalhas** — não entra: o dado é
// do PRD-10 e a rota não existe. Decisão do fundador de 2026-09-26.
export const RECORTES: Recorte[] = [
  {
    chave: "sociedade-civil",
    caminho: "/",
    rotulo: "Sociedade civil",
    secoes: [
      QUEM_SOMOS,
      GUERREIROS,
      PORTFOLIO,
      RANKING,
      PODERES,
      MESTRES,
      APOIADORES,
      COMUNIDADES,
      COMO_APOIAR,
      CONTATOS,
    ],
  },
  {
    chave: "pesquisadores",
    caminho: "/pesquisadores",
    rotulo: "Pesquisadores",
    // A seção é a mesma de "sociedade civil", com o título que o PRD-03 §5.2
    // dá a ela aqui: o pesquisador chega direto às séries por comunidade.
    // Entrar duas vezes duplicaria o conteúdo e a leitura (design — Decisão 7).
    secoes: [TERRITORIO, COBERTURA, SOLICITACAO_DE_DADOS, CONTATOS],
  },
  {
    chave: "gestores-publicos",
    caminho: "/gestores-publicos",
    rotulo: "Gestores públicos",
    secoes: [BLOCO_DO_GESTOR, TERRITORIO, COBERTURA, SOLICITACAO_DE_DADOS, CONTATOS],
  },
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
  if (!caminho.startsWith(PREFIXO_DA_PAGINA_DA_COMUNIDADE)) return null;
  const id = decodeURIComponent(caminho.slice(PREFIXO_DA_PAGINA_DA_COMUNIDADE.length));
  return id.length > 0 ? id : null;
}

/** A **página individual** é o único endereço próprio que esta fatia
 * acrescenta, porque o `RF-03-03` a exige compartilhável e alcançável
 * direto (design — decisão 6). Devolve o nick do caminho, ou `null` quando
 * o caminho não é de página individual. */
export function nickDoCaminho(caminho: string): string | null {
  if (!caminho.startsWith(PREFIXO_DA_PAGINA_DO_GUERREIRO)) return null;
  const nick = decodeURIComponent(caminho.slice(PREFIXO_DA_PAGINA_DO_GUERREIRO.length));
  return nick.length > 0 ? nick : null;
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
