import { chamarNucleo } from "../api/cliente";

export interface PontoDeApoioDaLista {
  id: string;
  nome: string;
  comunidade_virtual_id: string;
  responsavel_id: string | null;
  ativo: boolean;
}

interface ListaDePontosDeApoio {
  itens: PontoDeApoioDaLista[];
  proximo_cursor: string | null;
}

// Admin declara a comunidade, sempre; o Mestre a tem derivada do próprio
// vínculo no núcleo, e por isso não a envia (`RF-07-47`, `RF-01-18`).
export function listarPontosDeApoio(
  token: string,
  comunidadeId?: string,
): Promise<ListaDePontosDeApoio> {
  const consulta = comunidadeId ? `?comunidade=${encodeURIComponent(comunidadeId)}` : "";
  return chamarNucleo<ListaDePontosDeApoio>(`/v1/pontos-de-apoio${consulta}`, { token });
}

export interface CadastrarPontoDeApoioEntrada {
  nome: string;
  comunidade_id: string;
}

interface PontoDeApoioCriado {
  id: string;
  nome: string;
  comunidade_virtual_id: string;
  responsavel_id: string | null;
  ativo: boolean;
}

export function cadastrarPontoDeApoio(
  entrada: CadastrarPontoDeApoioEntrada,
  token: string,
): Promise<PontoDeApoioCriado> {
  return chamarNucleo<PontoDeApoioCriado>("/v1/pontos-de-apoio", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}
