import { chamarNucleo, lerArquivoDoNucleo } from "comum/api";
import { enviarMidiaDaCustomizacao as enviarMidiaDoComum } from "comum/customizacao";

// O cuidado com o bem recebido, no encontro: a fila de quem chegou, o
// julgamento da customização, a captura na hora e a conservação. Tudo vai sob
// o **token de trabalho** — quem lê e quem escreve é o Mestre que abriu o
// aparelho, e é a persona dele que o núcleo grava como autora (`RF-04-81` a
// `RF-04-84`, design — decisão 6).

export type SituacaoDoRegistro =
  | "pendente"
  | "aprovado"
  | "reprovado"
  | "cancelado"
  | "expirado";
export type FonteDaPontuacao = "conservacao" | "customizacao";

export interface RegistroDeCustomizacao {
  id: string;
  entrega_de_recompensa_id: string;
  descricao: string;
  situacao: SituacaoDoRegistro;
  tem_midia: boolean;
  tipo_do_arquivo: string | null;
  motivo_do_julgamento: string | null;
}

export interface UltimoRegistroAprovado {
  fonte: "customizacao_do_kit" | "comprovacao_do_pratico";
  id: string;
  descricao: string | null;
  tipo_do_arquivo: string | null;
}

export interface BemRecebido {
  entrega_de_recompensa_id: string;
  tipo_de_recurso_nome: string;
  trilha_nome: string;
  customizacao_aberta: boolean;
  ultimo_aprovado: UltimoRegistroAprovado | null;
  pendente: RegistroDeCustomizacao | null;
  pontuado_na_aula: FonteDaPontuacao | null;
}

export interface PresenteNaFila {
  guerreiro_id: string;
  guerreiro: { avatar: string | null; nick: string } | null;
  bens: BemRecebido[];
}

export function lerFilaDoCuidado(aulaId: string, token: string): Promise<PresenteNaFila[]> {
  return chamarNucleo<PresenteNaFila[]>(`/v1/aulas/${aulaId}/fila-do-cuidado`, { token });
}

export function julgarCustomizacao(
  registroId: string,
  entrada: { aula_id: string; aprovado: boolean; motivo?: string },
  token: string,
): Promise<RegistroDeCustomizacao> {
  return chamarNucleo<RegistroDeCustomizacao>(`/v1/customizacoes/${registroId}/julgamento`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export function validarConservacao(
  aulaId: string,
  entrada: { guerreiro_id: string; entrega_de_recompensa_id: string },
  token: string,
): Promise<unknown> {
  return chamarNucleo<unknown>(`/v1/aulas/${aulaId}/conservacoes`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// A captura na hora grava o registro em nome do Guerreiro(a) presente; a
// mídia vem depois, pela sessão retomável (`RF-04-82`).
export function capturarCustomizacao(
  aulaId: string,
  entrada: { guerreiro_id: string; entrega_de_recompensa_id: string; descricao: string },
  token: string,
): Promise<RegistroDeCustomizacao> {
  return chamarNucleo<RegistroDeCustomizacao>(`/v1/aulas/${aulaId}/customizacoes`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

/** Abre a sessão, manda o arquivo em partes e confirma. O trajeto mora em
 * `comum/customizacao`, que a App 05 usa no registro em casa; a função local
 * fica para a tela e os testes desta aplicação (design — decisão 1 da change
 * `2026-11-13-registro-da-customizacao-do-kit-em-casa`). */
export async function enviarMidiaDaCustomizacao(
  registroId: string,
  arquivo: File,
  token: string,
  aoProgredir: (enviados: number, total: number) => void,
): Promise<RegistroDeCustomizacao> {
  return enviarMidiaDoComum(registroId, arquivo, token, aoProgredir);
}

/** O "agora": a mídia do registro pendente. */
export function lerMidiaDoRegistro(registroId: string, token: string): Promise<Blob> {
  return lerArquivoDoNucleo(`/v1/customizacoes/${registroId}/arquivo`, { token });
}

/** O "antes": o último aprovado do kit, pela rota do bem, nas duas fontes
 * (`RF-04-81`, design — decisões 1 e 2). */
export function lerMidiaDoUltimoAprovado(entregaId: string, token: string): Promise<Blob> {
  return lerArquivoDoNucleo(
    `/v1/entregas-de-recompensa/${entregaId}/ultimo-aprovado/arquivo`,
    {
      token,
    },
  );
}
