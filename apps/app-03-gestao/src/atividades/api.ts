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
  // A aula do encontro em que ela acontece — é por ela que a área
  // Lançamentos a alcança (`RF-02-29`, `RF-02-112`).
  aula_id: string | null;
}

// A única atividade que a gestão cadastra, fora de trilha — sem campo de
// pontuação (o motor deriva) nem de recurso (é declaração da aula)
// (`RF-02-29`, PRD-02 §9).
export function listarAtividadesAvulsas(
  token: string,
  aulaId?: string,
): Promise<AtividadeAvulsa[]> {
  const consulta = aulaId ? `?aula=${encodeURIComponent(aulaId)}` : "";
  return chamarNucleo<AtividadeAvulsa[]>(`/v1/atividades${consulta}`, { token });
}

export interface CadastrarAtividadeAvulsaEntrada {
  titulo: string;
  descricao?: string;
  modalidade: ModalidadeDeAtividade;
  formato: FormatoDeAtividade;
  natureza: string;
  producao_esperada: string;
  poder_id: string;
  // A comunidade nunca é enviada: estreita a lista de aulas na tela, e o
  // núcleo a deriva da aula (`RF-02-29`, documento 09 §1).
  aula_id: string;
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
