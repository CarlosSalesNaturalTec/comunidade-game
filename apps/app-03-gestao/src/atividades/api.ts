import { chamarNucleo } from "comum/api";

export type ModalidadeDeAtividade = "individual" | "em_equipe" | "em_equipe_com_familiar";
export type FormatoDeAtividade = "presencial" | "on_line_assincrona";

export interface AtividadeAvulsa {
  id: string;
  titulo: string;
  descricao: string | null;
  modalidade: ModalidadeDeAtividade;
  formato: FormatoDeAtividade;
  natureza: string;
  producao_esperada: string;
  poder_id: string;
}

// A única atividade que a gestão cadastra, fora de trilha — sem campo de
// pontuação (o motor deriva) nem de recurso (é declaração da aula)
// (`RF-02-29`, PRD-02 §9).
export function listarAtividadesAvulsas(token: string): Promise<AtividadeAvulsa[]> {
  return chamarNucleo<AtividadeAvulsa[]>("/v1/atividades", { token });
}

export interface CadastrarAtividadeAvulsaEntrada {
  titulo: string;
  descricao?: string;
  modalidade: ModalidadeDeAtividade;
  formato: FormatoDeAtividade;
  natureza: string;
  producao_esperada: string;
  poder_id: string;
}

export function cadastrarAtividadeAvulsa(
  entrada: CadastrarAtividadeAvulsaEntrada,
  token: string,
): Promise<AtividadeAvulsa> {
  return chamarNucleo<AtividadeAvulsa>("/v1/atividades", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}
