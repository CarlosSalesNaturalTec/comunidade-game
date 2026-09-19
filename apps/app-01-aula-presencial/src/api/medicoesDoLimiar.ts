import { chamarNucleo } from "comum/api";

export interface MedicaoDoLimiarGravada {
  id: string;
  ponto_de_apoio_id: string;
  limiar: number;
  distancias_do_piso: number[];
  distancias_do_teto: number[];
  pessoas_no_teto: number;
  medido_por: string;
  registrado_em: string;
}

interface GravarMedicaoEntrada {
  aula_id: string;
  distancias_do_piso: number[];
  distancias_do_teto: number[];
  pessoas_no_teto: number;
}

// O que sai do aparelho são **distâncias** e o número de pessoas do teto —
// nunca descritor, nunca imagem (`RF-04-66`, `RN-04-32`, documento 03 §3.3).
// O **limiar não vai no corpo**: o núcleo o calcula das mesmas séries, pela
// mesma fórmula que a tela mostra a quem confirma — número enviado seria
// número em que se precisaria confiar (`RN-04-35`, design — decisão 6).
//
// Sempre com o token da sessão de trabalho: quem confirma é Mestre ou Admin,
// e a aula em curso é o que determina o ponto de apoio (`RF-01-16`,
// `RF-01-73`).
export function gravarMedicaoDoLimiar(
  entrada: GravarMedicaoEntrada,
  tokenDeTrabalho: string,
): Promise<MedicaoDoLimiarGravada> {
  return chamarNucleo<MedicaoDoLimiarGravada>("/v1/medicoes-do-limiar", {
    metodo: "POST",
    corpo: entrada,
    token: tokenDeTrabalho,
  });
}
