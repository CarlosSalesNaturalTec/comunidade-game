import { chamarNucleo } from "comum/api";

export type FormaDeEntregaDaProducao = "texto" | "audio" | "foto";

export interface ProducaoDaMissao {
  id: string;
  equipe_id: string | null;
  guerreiro_id: string | null;
  missao_id: string;
  atividade_id: string;
  forma: FormaDeEntregaDaProducao;
  transcricao: string;
  devolutiva: string | null;
  registrado_em: string;
}

interface EntregarProducaoEntrada {
  forma: FormaDeEntregaDaProducao;
  texto?: string;
  arquivo?: Blob;
}

// `RF-04-45` a `RF-04-47`: a entrega da produção pela equipe, na atividade
// corrente que ela já declarou — texto, fala ou foto, sempre uma única
// forma. A devolutiva volta construtiva e nunca credita ponto. `arquivo` é
// só da foto, que não fica no aparelho depois do envio (documento 03
// §12.2); a fala vai transcrita no aparelho, em `texto`, e o áudio não é
// enviado (`RF-05-76`, `RN-05-32`).
export function entregarProducao(
  equipeId: string,
  entrada: EntregarProducaoEntrada,
  token: string,
): Promise<ProducaoDaMissao> {
  const formulario = new FormData();
  formulario.set("forma", entrada.forma);
  if (entrada.texto !== undefined) formulario.set("texto", entrada.texto);
  if (entrada.arquivo !== undefined) formulario.set("arquivo", entrada.arquivo);

  return chamarNucleo<ProducaoDaMissao>(`/v1/equipes/${equipeId}/producao`, {
    metodo: "POST",
    formulario,
    token,
  });
}
