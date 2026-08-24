import { chamarNucleo } from "comum/api";

export interface ConsentimentoRegistrado {
  id: string;
  registrado_em: string;
}

interface RegistrarConsentimentoEntrada {
  responsavel_id: string;
  guerreiro_id: string;
  tipo: "biometria" | "autorizacao_de_divulgacao";
  decisao: "concede" | "nega";
  origem: "propria" | "assistida" | "impressa";
  testemunha_id?: string;
}

// O testemunho do termo impresso, assinado pelo responsável e confirmado
// pelo Mestre ou Admin presente (`RF-04-12`, `RN-04-07`, design — decisão
// 3). A versão do termo é carimbada pelo núcleo — esta chamada nunca a
// declara.
export function registrarConsentimento(
  entrada: RegistrarConsentimentoEntrada,
  tokenDeTrabalho: string,
): Promise<ConsentimentoRegistrado> {
  return chamarNucleo<ConsentimentoRegistrado>("/v1/consentimentos", {
    metodo: "POST",
    corpo: entrada,
    token: tokenDeTrabalho,
  });
}
