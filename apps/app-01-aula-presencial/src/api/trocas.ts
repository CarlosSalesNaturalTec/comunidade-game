import { chamarNucleo } from "comum/api";

export interface TrocaRegistrada {
  id: string;
  item_de_catalogo_avulso_id: string;
  guerreiro_id: string;
  preco_cobrado: number;
  aula_id: string;
  autor_id: string;
  registrado_em: string;
}

interface RegistrarTrocaEntrada {
  item_de_catalogo_avulso_id: string;
  guerreiro_id: string;
}

// Sempre com o token de trabalho — o Mestre que entrega é o autor da
// troca, e o núcleo grava `autor_id` da persona da sessão; o token do
// Guerreiro(a) nunca assina esta escrita (`RF-04-52`, `RF-04-55`, design —
// decisão 4).
export function registrarTroca(
  aulaId: string,
  entrada: RegistrarTrocaEntrada,
  tokenDeTrabalho: string,
): Promise<TrocaRegistrada> {
  return chamarNucleo<TrocaRegistrada>(`/v1/aulas/${aulaId}/trocas`, {
    metodo: "POST",
    corpo: entrada,
    token: tokenDeTrabalho,
  });
}
