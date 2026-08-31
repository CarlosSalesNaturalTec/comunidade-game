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

interface ConsultarAssistenteEntrada {
  texto?: string;
  arquivo?: Blob;
}

// `RF-04-36` a `RF-04-40`: a pergunta da equipe ao assistente de trilhas,
// por texto ou por fala, sempre uma única forma. A recusa explicada e o
// encaminhamento à App 05 chegam aqui como resposta comum, em 200 — nunca
// como erro (`RF-04-37`, `RF-04-38`); só a indisponibilidade é `ErroDaApi`
// com status 503.
export function consultarAssistenteDeTrilhas(
  equipeId: string,
  entrada: ConsultarAssistenteEntrada,
  token: string,
): Promise<ConsultaAoAssistente> {
  const formulario = new FormData();
  formulario.set("equipe_id", equipeId);
  if (entrada.texto !== undefined) formulario.set("texto", entrada.texto);
  if (entrada.arquivo !== undefined) formulario.set("arquivo", entrada.arquivo);

  return chamarNucleo<ConsultaAoAssistente>("/v1/assistente/trilhas/consultas", {
    metodo: "POST",
    formulario,
    token,
  });
}
