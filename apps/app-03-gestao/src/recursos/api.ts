import { chamarNucleo } from "comum/api";

export interface TipoDeRecurso {
  id: string;
  nome: string;
  natureza: string;
  unidade: string;
  exige_comprovante: boolean;
  valor_em_moedas: string;
  vigencia_inicio: string;
}

// Rota fora do previsto na proposal desta change (design — decisão 6):
// sem ela, a homologação do aporte não teria seletor de tipo de recurso
// (`RF-02-84`).
export function listarTiposDeRecurso(token: string): Promise<TipoDeRecurso[]> {
  return chamarNucleo<TipoDeRecurso[]>("/v1/tipos-de-recurso", { token });
}

export interface NecessidadeDeRecurso {
  aula_id: string;
  tipo_de_recurso_id: string;
  quantidade_faltante: string;
  valor_em_moedas: string | null;
  comunidade_virtual_id: string;
  ponto_de_apoio_id: string;
  inicio_em: string;
  fim_em: string;
}

// A App 03 lê a mesma rota pública que a vitrine, sob a chave da aplicação
// que ela já envia — sem rota de gestão nova (`RF-02-58`, design —
// decisão 5).
export function listarNecessidades(): Promise<NecessidadeDeRecurso[]> {
  return chamarNucleo<NecessidadeDeRecurso[]>("/v1/vitrine/necessidades");
}

export interface AporteRegistrado {
  id: string;
  provedor_id: string;
  tipo_de_recurso_id: string;
  quantidade: string;
  ponto_de_apoio_id: string;
  valor_em_moedas: string;
  forma: string;
  data_do_aporte: string;
}

export interface RegistrarAporteEntrada {
  provedorId: string;
  tipoDeRecursoId: string;
  quantidade: string;
  pontoDeApoioId: string;
  dataDoAporte: string;
  forma: "financeira" | "material" | "servico";
  comprovante?: File;
}

// A porta comum de crédito do livro-razão (`RF-02-57`, `RN-02-19`): sem
// `solicitacao_de_participacao_id`, ao contrário de `aportes.homologarAporte`,
// que fecha a declaração do pré-cadastro.
export function registrarAporte(
  entrada: RegistrarAporteEntrada,
  token: string,
): Promise<AporteRegistrado> {
  const formulario = new FormData();
  formulario.set("provedor_id", entrada.provedorId);
  formulario.set("tipo_de_recurso_id", entrada.tipoDeRecursoId);
  formulario.set("quantidade", entrada.quantidade);
  formulario.set("ponto_de_apoio_id", entrada.pontoDeApoioId);
  formulario.set("data_do_aporte", entrada.dataDoAporte);
  formulario.set("forma", entrada.forma);
  formulario.set("destinacao", "lastro");
  if (entrada.comprovante) {
    formulario.set("comprovante", entrada.comprovante);
  }

  return chamarNucleo<AporteRegistrado>("/v1/aportes", {
    metodo: "POST",
    formulario,
    token,
  });
}
