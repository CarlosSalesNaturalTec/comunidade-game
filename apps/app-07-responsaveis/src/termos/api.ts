import { chamarNucleo } from "comum/api";

export interface VersaoDoTermo {
  versao: string;
  texto: string;
  vigente_desde: string;
}

export interface CatalogoDeTermo {
  tipo: string;
  vigente: VersaoDoTermo;
  historico: VersaoDoTermo[];
}

// A versão vigente e o histórico, de cada tipo — hoje só a autorização de
// divulgação —, numa só chamada, sem exigir vínculo com Guerreiro(a)
// algum: o texto do termo não é dado de criança (`RF-13-32`, `RF-13-33`).
export function consultarTermos(token: string): Promise<CatalogoDeTermo[]> {
  return chamarNucleo<CatalogoDeTermo[]>("/v1/termos", { token });
}

export interface LeituraDeTermoSaida {
  id: string;
  versao: string;
  lida_em: string;
}

// Registra a leitura — reler a mesma versão não grava de novo, e a tela só
// precisa mostrar o que o núcleo devolveu (`RF-13-32`, design — decisão 3).
export function registrarLeituraDeTermo(
  versao: string,
  token: string,
): Promise<LeituraDeTermoSaida> {
  return chamarNucleo<LeituraDeTermoSaida>(`/v1/termos/${versao}/leitura`, {
    metodo: "POST",
    token,
  });
}
