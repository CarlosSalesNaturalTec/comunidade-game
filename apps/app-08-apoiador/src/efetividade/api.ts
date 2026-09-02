import { chamarNucleo } from "comum/api";

export interface ConcluinteExibivel {
  avatar: string | null;
  nick: string;
}

export interface DesafioDeEfetividade {
  id: string;
  trilha_id: string;
  trilha_nome: string;
  modalidade: "aberto" | "direcionado";
  situacao: string;
  etiquetas_ods: number[];
  quantidade_de_conclusoes: number | null;
  primeira_conclusao_em: string | null;
  ultima_conclusao_em: string | null;
  concluintes_exibiveis: ConcluinteExibivel[] | null;
  concluintes_nao_identificados: number | null;
  houve_conclusao: boolean | null;
}

export interface PainelDeDesafios {
  propostos: DesafioDeEfetividade[];
  publicados: DesafioDeEfetividade[];
  concluidos: DesafioDeEfetividade[];
}

export interface AporteDeEfetividade {
  id: string;
  valor_em_moedas: string;
  data_do_aporte: string;
  custeio_tipo: "missao" | "necessidade" | "desafio_extra" | "livre";
  custeio_descricao: string | null;
}

export interface MoedasDeEfetividade {
  total_em_moedas: string;
  aportes: AporteDeEfetividade[];
}

export interface CoberturaPorComunidade {
  comunidade_virtual_id: string;
  comunidade_virtual_nome: string;
  ciclo_rotulo: string;
  objetivos: number[];
}

export interface CoberturaDeOds {
  por_comunidade: CoberturaPorComunidade[];
}

export interface PainelDeEfetividade {
  desafios: PainelDeDesafios;
  moedas: MoedasDeEfetividade;
  cobertura_de_ods: CoberturaDeOds;
}

// O painel vivo: reflete a última conclusão registrada, sem fechamento nem
// periodicidade (`RF-14-40`, `RN-14-21`).
export function lerPainelDeEfetividade(token: string): Promise<PainelDeEfetividade> {
  return chamarNucleo<PainelDeEfetividade>("/v1/eu/desafios-extras/efetividade", { token });
}
