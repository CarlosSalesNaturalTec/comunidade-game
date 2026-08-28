import { chamarNucleo } from "comum/api";

export interface RecursoFaltante {
  tipo_de_recurso_id: string;
  quantidade_declarada: string;
  quantidade_disponivel: string;
}

export interface AulaDaAgenda {
  id: string;
  comunidade_virtual_id: string;
  ponto_de_apoio_id: string;
  inicio_em: string;
  fim_em: string;
  situacao: string;
  cancelamento_motivo: string | null;
  // Só a aula pendente de lastro tem o que faltar — as demais chegam com
  // lista vazia (`RF-02-32`, `RF-07-08`).
  recursos_faltantes: RecursoFaltante[];
}

interface ListaDeAulas {
  itens: AulaDaAgenda[];
  proximo_cursor: string | null;
}

export interface FiltroDeAgenda {
  comunidadeId?: string;
  periodoInicio?: string;
  periodoFim?: string;
}

// Admin declara a comunidade, sempre; o Mestre a tem derivada do próprio
// vínculo no núcleo, e por isso não a envia (`RF-02-12`, `RF-01-18`).
export function listarAgenda(
  token: string,
  filtro: FiltroDeAgenda = {},
): Promise<ListaDeAulas> {
  const parametros = new URLSearchParams();
  if (filtro.comunidadeId) parametros.set("comunidade", filtro.comunidadeId);
  if (filtro.periodoInicio) parametros.set("periodo_inicio", filtro.periodoInicio);
  if (filtro.periodoFim) parametros.set("periodo_fim", filtro.periodoFim);
  const consulta = parametros.toString();
  return chamarNucleo<ListaDeAulas>(`/v1/aulas${consulta ? `?${consulta}` : ""}`, { token });
}

export interface RecursoDeclarado {
  tipo_de_recurso_id: string;
  quantidade: string;
}

export interface AgendarAulaEntrada {
  comunidade_virtual_id: string;
  ponto_de_apoio_id: string;
  inicio_em: string;
  fim_em: string;
  // O que a aula consome — a reserva é disparada pelo núcleo, nunca
  // calculada aqui (`RF-02-31`, documento 04 §1).
  recursos_declarados: RecursoDeclarado[];
}

export function agendarAula(
  entrada: AgendarAulaEntrada,
  token: string,
): Promise<AulaDaAgenda> {
  return chamarNucleo<AulaDaAgenda>("/v1/aulas", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export function cancelarAula(
  idDaAula: string,
  motivo: string,
  token: string,
): Promise<AulaDaAgenda> {
  return chamarNucleo<AulaDaAgenda>(`/v1/aulas/${idDaAula}/cancelamento`, {
    metodo: "POST",
    corpo: { motivo },
    token,
  });
}
