import { chamarNucleo, enviarParteComProgresso } from "../api/cliente";

// O cliente da customização do kit do lado da criança: a leitura dos kits
// abertos e dos registros, o registro, o envio retomável da mídia e o
// cancelamento do pendente. Mora no `comum` porque a App 05 registra em casa e
// a App 01, na fatia 35 do PRD-04, registra no encontro "sem divergir da App
// 05" (`RF-05-102`, `RF-05-103`, `RF-04-80`, design — decisão 1).

export type SituacaoDoRegistroDeCustomizacao =
  | "pendente"
  | "aprovado"
  | "reprovado"
  | "cancelado"
  | "expirado";

export interface RegistroDeCustomizacao {
  id: string;
  entrega_de_recompensa_id: string;
  descricao: string;
  situacao: SituacaoDoRegistroDeCustomizacao;
  tem_midia: boolean;
  tipo_do_arquivo: string | null;
  motivo_do_julgamento: string | null;
  registrado_em: string;
}

export interface KitAberto {
  entrega_de_recompensa_id: string;
  recompensa_de_marco_id: string;
  tipo_de_recurso_nome: string;
  trilha_nome: string;
  customizacao_aberta: boolean;
  pendente: RegistroDeCustomizacao | null;
}

export interface MinhasCustomizacoes {
  kits_abertos: KitAberto[];
  registros: RegistroDeCustomizacao[];
}

export function lerMinhasCustomizacoes(token: string): Promise<MinhasCustomizacoes> {
  return chamarNucleo<MinhasCustomizacoes>("/v1/eu/customizacoes", { token });
}

/** Grava o registro sem mídia; ele só fica pronto para o Mestre quando o envio
 * é confirmado. */
export function registrarMinhaCustomizacao(
  entrada: { entrega_de_recompensa_id: string; descricao: string },
  token: string,
): Promise<RegistroDeCustomizacao> {
  return chamarNucleo<RegistroDeCustomizacao>("/v1/eu/customizacoes", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export function cancelarCustomizacao(
  registroId: string,
  token: string,
): Promise<RegistroDeCustomizacao> {
  return chamarNucleo<RegistroDeCustomizacao>(`/v1/customizacoes/${registroId}/cancelamento`, {
    metodo: "POST",
    token,
  });
}

const TAMANHO_DA_PARTE = 5 * 1024 * 1024;

/** Abre a sessão, manda o arquivo em partes e confirma — o mesmo trajeto da
 * comprovação do prático. Só com a confirmação o registro passa a julgar. */
export async function enviarMidiaDaCustomizacao(
  registroId: string,
  arquivo: File,
  token: string,
  aoProgredir: (enviados: number, total: number) => void,
): Promise<RegistroDeCustomizacao> {
  const { endereco_da_sessao } = await chamarNucleo<{ endereco_da_sessao: string }>(
    `/v1/customizacoes/${registroId}/envios`,
    {
      metodo: "POST",
      corpo: { tipo_mime: arquivo.type, tamanho_declarado: arquivo.size },
      token,
    },
  );
  let posicao = 0;
  const total = arquivo.size;
  while (posicao < total) {
    const fim = Math.min(posicao + TAMANHO_DA_PARTE, total);
    const inicio = posicao;
    const resultado = await enviarParteComProgresso(
      endereco_da_sessao,
      arquivo.slice(inicio, fim),
      `bytes ${inicio}-${fim - 1}/${total}`,
      (bytesDaParte) => aoProgredir(inicio + bytesDaParte, total),
    );
    posicao = resultado.concluido ? fim : resultado.bytesRecebidos;
    aoProgredir(posicao, total);
  }
  return chamarNucleo<RegistroDeCustomizacao>(
    `/v1/customizacoes/${registroId}/envios/confirmacao`,
    { metodo: "POST", token },
  );
}
