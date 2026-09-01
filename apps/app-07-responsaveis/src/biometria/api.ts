import { chamarNucleo } from "comum/api";

export interface RecusaDaBiometriaSaida {
  guerreiro_id: string;
  apagar_em: string | null;
}

// A App 07 só oferece a recusa — a concessão é do termo impresso assinado
// no encontro (`RF-13-27`, `RN-13-06`, PRD-13 §3.2).
export function recusarBiometria(
  guerreiroId: string,
  token: string,
): Promise<RecusaDaBiometriaSaida> {
  return chamarNucleo<RecusaDaBiometriaSaida>(
    `/v1/eu/guerreiros/${guerreiroId}/biometria/recusa`,
    { metodo: "POST", token },
  );
}

export type DecisaoDoTermoDaBiometria = "concede" | "nega";
export type GatilhoDoApagamento = "exclusao_deferida" | "recusa_biometria" | "fim_do_vinculo";

export interface EstadoDaBiometria {
  tem_template: boolean;
  decisao_do_termo: DecisaoDoTermoDaBiometria | null;
  apagar_em: string | null;
  gatilho_do_apagamento: GatilhoDoApagamento | null;
}

// Nunca o descritor nem o _template_ — só o estado da captura, a decisão
// mais recente do termo e, havendo marca, a data e o gatilho do apagamento
// (`RF-13-27`, `RF-13-44`, `RN-13-04`).
export function lerEstadoDaBiometria(
  guerreiroId: string,
  token: string,
): Promise<EstadoDaBiometria> {
  return chamarNucleo<EstadoDaBiometria>(`/v1/eu/guerreiros/${guerreiroId}/biometria`, {
    token,
  });
}
