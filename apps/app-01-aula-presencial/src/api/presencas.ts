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

interface RegistrarPresencaSemRedeEntrada {
  nick: string;
  momento_do_fato: string;
}

// A presença que entrou na fila sem rede, com o PIN já conferido no
// aparelho: o núcleo a grava pelo nick, com quem abriu a sessão de trabalho
// como confirmador, e nunca abre sessão do Guerreiro(a) — a sincronização
// não abre o que a queda não abriu (`RF-04-23`, `RN-04-38`, design —
// decisão 6).
export function registrarPresencaSemRede(
  aulaId: string,
  entrada: RegistrarPresencaSemRedeEntrada,
  tokenDeTrabalho: string,
): Promise<PresencaRegistrada> {
  return chamarNucleo<PresencaRegistrada>(`/v1/aulas/${aulaId}/presencas/sem-rede`, {
    metodo: "POST",
    corpo: entrada,
    token: tokenDeTrabalho,
  });
}

export interface MinhaPresenca {
  presente: boolean;
  momento_do_fato: string | null;
  modo: "reconhecimento" | "confirmacao" | null;
}

// Com o token do **Guerreiro(a)**, não o da sessão de trabalho: a presença
// lida é sempre a dele, e o núcleo a toma do contexto da sessão
// (`RF-04-68`, `RN-04-40`, invariante 15). Ausência de presença é resposta
// normal, e não erro — é ela que distingue "não tem presença" de "não foi
// possível perguntar" (`RN-04-36`).
export function lerMinhaPresenca(
  aulaId: string,
  tokenDoGuerreiro: string,
): Promise<MinhaPresenca> {
  return chamarNucleo<MinhaPresenca>(`/v1/aulas/${aulaId}/presencas/eu`, {
    token: tokenDoGuerreiro,
  });
}
