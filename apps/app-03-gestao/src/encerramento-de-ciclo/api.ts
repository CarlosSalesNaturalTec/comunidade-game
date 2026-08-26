import { chamarNucleo } from "comum/api";

export interface CicloEncerrado {
  ocorrencias_expurgadas: number;
}

// Restrita a Admin no núcleo (`RF-02-99`); o ato não declara o ciclo
// seguinte, que é declaração à parte na implantação.
export function encerrarCiclo(token: string): Promise<CicloEncerrado> {
  return chamarNucleo<CicloEncerrado>("/v1/ciclo/encerramento", {
    metodo: "POST",
    token,
  });
}
