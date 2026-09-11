import { chamarNucleo } from "comum/api";

export type DesfechoDaConsulta = "respondida" | "fora_do_corpus" | "tarefa_escolar";

export interface ConsultaAoAssistente {
  id: string;
  equipe_id: string | null;
  guerreiro_id: string | null;
  assistente: "trilhas" | "apoio_escolar";
  desfecho: DesfechoDaConsulta;
  pergunta: string;
  resposta: string;
  registrado_em: string;
}

// `RF-04-36` a `RF-04-40`: a pergunta da equipe ao assistente de trilhas,
// sempre em texto — a fala é transcrita no aparelho, pela Web Speech API
// (`comum/fala`), e o áudio nunca sai dele (`RF-04-40`, `RN-04-21`,
// documento 03 §1.12). A recusa explicada e o encaminhamento à App 05
// chegam aqui como resposta comum, em 200 — nunca como erro (`RF-04-37`,
// `RF-04-38`); só a indisponibilidade é `ErroDaApi` com status 503.
export function consultarAssistenteDeTrilhas(
  equipeId: string,
  texto: string,
  token: string,
): Promise<ConsultaAoAssistente> {
  return chamarNucleo<ConsultaAoAssistente>("/v1/assistente/trilhas/consultas", {
    metodo: "POST",
    corpo: { equipe_id: equipeId, texto },
    token,
  });
}
