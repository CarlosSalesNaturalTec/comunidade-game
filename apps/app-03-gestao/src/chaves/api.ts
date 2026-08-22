import { chamarNucleo } from "../api/cliente";

export interface ChaveDeAplicacao {
  id: string;
  aplicacao: string;
  natureza: "do_projeto" | "de_terceiro";
  ambiente: string;
  prazo_de_apresentacao: string | null;
  url_apresentada: string | null;
  situacao: "vigente" | "revogada";
}

interface ListaDeChaves {
  itens: ChaveDeAplicacao[];
  proximo_cursor: string | null;
}

export function listarChaves(token: string): Promise<ListaDeChaves> {
  return chamarNucleo<ListaDeChaves>("/v1/chaves", { token });
}

export interface ChaveEmitida {
  id: string;
  segredo: string;
}

// A emissão em si é `RF-01-50`, já implantada; esta chamada só alcança a
// rota existente a partir da fila de solicitações de chave (`RF-02-89`).
export function emitirChave(idDaSolicitacao: string, token: string): Promise<ChaveEmitida> {
  return chamarNucleo<ChaveEmitida>("/v1/chaves", {
    metodo: "POST",
    corpo: { solicitacao_id: idDaSolicitacao },
    token,
  });
}

export function revogarChave(idDaChave: string, motivo: string, token: string): Promise<void> {
  return chamarNucleo<void>(`/v1/chaves/${idDaChave}`, {
    metodo: "DELETE",
    corpo: { motivo },
    token,
  });
}
