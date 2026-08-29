import { chamarNucleo } from "comum/api";

interface Pagina<T> {
  itens: T[];
  proximo_cursor: string | null;
}

export interface PontoDeApoioDaLista {
  id: string;
  nome: string;
  comunidade_virtual_id: string;
}

// Sem `comunidade`: o núcleo já recorta pelo vínculo vigente do Mestre, sem
// seletor na tela (design — decisão 6, `RF-07-47`).
export async function listarMeusPontosDeApoio(token: string): Promise<PontoDeApoioDaLista[]> {
  const pontos: PontoDeApoioDaLista[] = [];
  let cursor: string | null = null;
  do {
    const consulta = cursor ? `?cursor=${encodeURIComponent(cursor)}` : "";
    const pagina: Pagina<PontoDeApoioDaLista> = await chamarNucleo<
      Pagina<PontoDeApoioDaLista>
    >(`/v1/pontos-de-apoio${consulta}`, { token });
    pontos.push(...pagina.itens);
    cursor = pagina.proximo_cursor;
  } while (cursor);
  return pontos;
}

export interface TipoDeRecurso {
  id: string;
  nome: string;
  natureza: string;
  unidade: string;
  exige_comprovante: boolean;
  valor_em_moedas: string;
  vigencia_inicio: string;
}

// Admin e Mestre leem — o Mestre precisa da natureza e de exige_comprovante
// para saber o que o formulário de absorção exige (`RF-09-56`, `RF-09-57`).
export function listarTiposDeRecurso(token: string): Promise<TipoDeRecurso[]> {
  return chamarNucleo<TipoDeRecurso[]>("/v1/tipos-de-recurso", { token });
}

export interface NecessidadeDeRecurso {
  aula_id: string;
  tipo_de_recurso_id: string;
  quantidade_faltante: string;
  valor_em_moedas: string | null;
  comunidade_virtual_id: string;
  ponto_de_apoio_id: string;
  inicio_em: string;
  fim_em: string;
}

// A falta das aulas da comunidade do Mestre, já recortada pelo núcleo — a
// aplicação não soma, reordena nem recalcula (`RF-09-56`, `RN-09-12`).
export function listarMinhasNecessidades(token: string): Promise<NecessidadeDeRecurso[]> {
  return chamarNucleo<NecessidadeDeRecurso[]>("/v1/necessidades/minhas", { token });
}

export interface AporteRegistrado {
  id: string;
  tipo_de_recurso_id: string;
  quantidade: string;
  ponto_de_apoio_id: string;
  valor_em_moedas: string;
  ressarcivel: boolean;
  situacao_de_ressarcimento: string;
  aula_id: string | null;
  data_do_aporte: string;
}

export interface AbsorverNecessidadeEntrada {
  tipoDeRecursoId: string;
  quantidade: string;
  pontoDeApoioId: string;
  dataDoAporte: string;
  aulaId?: string;
  valorDeOrigem?: string;
  comprovante?: File;
}

// A absorção nasce da necessidade, não de formulário livre: tipo, ponto de
// apoio e aula vêm da linha escolhida, e o aporte nasce em nome do próprio
// Mestre e ressarcível (`RF-09-57`, `RF-09-58`, `RN-09-13`, design —
// decisão 3).
export function absorverNecessidade(
  entrada: AbsorverNecessidadeEntrada,
  token: string,
): Promise<AporteRegistrado> {
  const formulario = new FormData();
  formulario.set("tipo_de_recurso_id", entrada.tipoDeRecursoId);
  formulario.set("quantidade", entrada.quantidade);
  formulario.set("ponto_de_apoio_id", entrada.pontoDeApoioId);
  formulario.set("data_do_aporte", entrada.dataDoAporte);
  if (entrada.aulaId) formulario.set("aula_id", entrada.aulaId);
  if (entrada.valorDeOrigem) formulario.set("valor_de_origem", entrada.valorDeOrigem);
  if (entrada.comprovante) formulario.set("comprovante", entrada.comprovante);

  return chamarNucleo<AporteRegistrado>("/v1/aportes/absorcao", {
    metodo: "POST",
    formulario,
    token,
  });
}

export type SituacaoDeRessarcimento = "nao_se_aplica" | "em_aberto" | "ressarcido";

export interface AbsorcaoDoMestre {
  id: string;
  tipo_de_recurso_id: string;
  quantidade: string;
  ponto_de_apoio_id: string;
  valor_em_moedas: string;
  situacao_de_ressarcimento: SituacaoDeRessarcimento;
  data_do_aporte: string;
}

// Somente leitura: a situação do que o próprio Mestre absorveu, sem ação de
// exigir, apressar, reordenar ou cancelar (`RF-09-59`).
export function listarMinhasAbsorcoes(token: string): Promise<AbsorcaoDoMestre[]> {
  return chamarNucleo<AbsorcaoDoMestre[]>("/v1/meus-aportes/ressarciveis", { token });
}
