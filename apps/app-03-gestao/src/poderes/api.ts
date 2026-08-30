import { chamarNucleo } from "comum/api";

export type NaturezaDoPoder = "de_guerreiro" | "derivado_do_aporte";
export type VigenciaDoPoder = "vigente" | "ciclo_futuro";
export type PapelDoPoder = "territorio";

export interface PoderDaLista {
  id: string;
  nome: string;
  descricao: string;
  natureza: NaturezaDoPoder;
  vigencia: VigenciaDoPoder;
  papel: PapelDoPoder | null;
  ativo: boolean;
  tecnico: boolean;
}

interface ListaDePoderes {
  itens: PoderDaLista[];
  proximo_cursor: string | null;
}

export function listarPoderes(token: string, cursor?: string): Promise<ListaDePoderes> {
  const consulta = cursor ? `?cursor=${encodeURIComponent(cursor)}` : "";
  return chamarNucleo<ListaDePoderes>(`/v1/poderes${consulta}`, { token });
}

export interface CadastrarPoderEntrada {
  nome: string;
  descricao: string;
  natureza: NaturezaDoPoder;
  vigencia: VigenciaDoPoder;
  papel?: PapelDoPoder;
  tecnico?: boolean;
}

export function cadastrarPoder(
  entrada: CadastrarPoderEntrada,
  token: string,
): Promise<PoderDaLista> {
  return chamarNucleo<PoderDaLista>("/v1/poderes", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// A natureza e o papel ficam de fora: `PUT /poderes/{id}` não os admite —
// mudar a natureza reescreveria o vínculo já concedido às trilhas
// (`RN-01-43`, `RN-01-54`). A marca de técnico entra: dela não deriva
// vínculo nem crédito, só a próxima sugestão do template (`RN-09-34`).
export interface AlterarPoderEntrada {
  nome?: string;
  descricao?: string;
  vigencia?: VigenciaDoPoder;
  tecnico?: boolean;
}

export function alterarPoder(
  idDoPoder: string,
  entrada: AlterarPoderEntrada,
  token: string,
): Promise<PoderDaLista> {
  return chamarNucleo<PoderDaLista>(`/v1/poderes/${idDoPoder}`, {
    metodo: "PUT",
    corpo: entrada,
    token,
  });
}

export function desativarPoder(idDoPoder: string, token: string): Promise<PoderDaLista> {
  return chamarNucleo<PoderDaLista>(`/v1/poderes/${idDoPoder}/desativacao`, {
    metodo: "POST",
    token,
  });
}
