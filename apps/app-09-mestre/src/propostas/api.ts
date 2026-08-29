import { chamarNucleo } from "comum/api";

export type SituacaoDaProposta = "recebida" | "em_avaliacao" | "adotada" | "nao_adotada";

// Leitura de quem propôs — nunca o `parecer` interno, que é só de Admin
// (`RF-09-55`, `RN-02-25`).
export interface PropostaDoAutor {
  id: string;
  alvo_tipo: "atividade" | "trilha" | "plataforma";
  alvo_id: string | null;
  texto: string;
  situacao: SituacaoDaProposta;
  prazo: string;
  em_atraso: boolean;
  motivo_do_retorno: string | null;
  decidido_em: string | null;
}

interface Pagina<T> {
  itens: T[];
  proximo_cursor: string | null;
}

export function listarMinhasPropostas(token: string): Promise<PropostaDoAutor[]> {
  return chamarNucleo<Pagina<PropostaDoAutor>>("/v1/sugestoes/minhas", { token }).then(
    (pagina) => pagina.itens,
  );
}

interface PropostaRegistradaSaida {
  id: string;
  prazo: string;
}

// Sempre alvo `plataforma`, em texto — nunca áudio (03 §12.2, `RN-09-23`).
// A mesma rota de `RF-01-25`; nenhuma regra de fila nasce na App 09.
export function registrarProposta(
  texto: string,
  token: string,
): Promise<PropostaRegistradaSaida> {
  return chamarNucleo<PropostaRegistradaSaida>("/v1/sugestoes", {
    metodo: "POST",
    corpo: { alvo_tipo: "plataforma", texto },
    token,
  });
}
