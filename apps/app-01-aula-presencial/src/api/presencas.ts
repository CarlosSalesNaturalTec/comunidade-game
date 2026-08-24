import { chamarNucleo } from "comum/api";

export interface PresencaRegistrada {
  id: string;
  aula_id: string;
  guerreiro_id: string;
  modo: "reconhecimento" | "confirmacao";
  confirmador_id: string | null;
  momento_do_fato: string;
}

interface RegistrarPresencaEntrada {
  guerreiro_id: string;
  modo: "reconhecimento" | "confirmacao";
  momento_do_fato: string;
}

// Sempre com o token da sessão de trabalho do aparelho, nunca o do
// Guerreiro(a) recém-aberta: é ela quem autentica o encontro, sem virar
// autora da presença (`RF-04-18`, `RF-04-21`, design — decisão 2). O
// núcleo devolve o registro existente sem erro no reenvio — o
// `momento_do_fato` da resposta é o gravado, e a tela o compara com o
// enviado para saber se a presença já constava (`RF-04-19`, design —
// decisão 3).
export function registrarPresenca(
  aulaId: string,
  entrada: RegistrarPresencaEntrada,
  tokenDeTrabalho: string,
): Promise<PresencaRegistrada> {
  return chamarNucleo<PresencaRegistrada>(`/v1/aulas/${aulaId}/presencas`, {
    metodo: "POST",
    corpo: entrada,
    token: tokenDeTrabalho,
  });
}
