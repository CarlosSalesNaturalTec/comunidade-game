import { chamarNucleo } from "comum/api";

export interface TipoDeRecurso {
  id: string;
  nome: string;
  natureza: string;
  unidade: string;
  exige_comprovante: boolean;
  // Desativado sai só da escolha nova; a leitura por nome segue com todos
  // (`RF-07-52`, `RF-02-115`).
  ativo: boolean;
  valor_em_moedas: string;
  vigencia_inicio: string;
}

// Filtro dos seletores de **escolha nova**: o tipo desativado não é
// oferecido, e o núcleo o recusaria (`RF-07-52`, design — decisão 8).
export function apenasAtivos(tipos: TipoDeRecurso[]): TipoDeRecurso[] {
  return tipos.filter((tipo) => tipo.ativo !== false);
}

// Rota fora do previsto na proposal desta change (design — decisão 6):
// sem ela, a homologação do aporte não teria seletor de tipo de recurso
// (`RF-02-84`).
export function listarTiposDeRecurso(token: string): Promise<TipoDeRecurso[]> {
  return chamarNucleo<TipoDeRecurso[]>("/v1/tipos-de-recurso", { token });
}

export type NaturezaDoRecurso = "consumivel" | "duravel" | "servico" | "financeiro";

export const ROTULO_DA_NATUREZA_DO_RECURSO: Record<NaturezaDoRecurso, string> = {
  consumivel: "Consumível",
  duravel: "Durável",
  servico: "Serviço",
  financeiro: "Financeiro",
};

export interface CadastrarTipoDeRecursoEntrada {
  nome: string;
  natureza: NaturezaDoRecurso;
  unidade: string;
  valor_em_moedas: string;
  vigencia_inicio: string;
  exige_comprovante?: boolean;
}

// O tipo e a primeira vigência do valor de referência num ato só, porque é
// assim que o núcleo os grava — a tela nunca oferece dois passos
// (`RF-02-107`, `RF-07-01`, `RF-07-02`, design — decisão 2).
export function cadastrarTipoDeRecurso(
  entrada: CadastrarTipoDeRecursoEntrada,
  token: string,
): Promise<TipoDeRecurso> {
  return chamarNucleo<TipoDeRecurso>("/v1/tipos-de-recurso", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface AlterarTipoDeRecursoEntrada {
  nome?: string;
  unidade?: string;
  exige_comprovante?: boolean;
}

// Nome, unidade e exige comprovante; a natureza não se altera
// (`RF-02-113`, `RF-07-51`).
export function alterarTipoDeRecurso(
  id: string,
  entrada: AlterarTipoDeRecursoEntrada,
  token: string,
): Promise<TipoDeRecurso> {
  return chamarNucleo<TipoDeRecurso>(`/v1/tipos-de-recurso/${id}`, {
    metodo: "PATCH",
    corpo: entrada,
    token,
  });
}

// Vigência nova do valor em moedas: encerra a vigente no dia de início da
// nova, sem reescrevê-la (`RF-07-51`, `RF-07-02`).
export function registrarValorDeReferencia(
  id: string,
  entrada: { valor_em_moedas: string; vigencia_inicio: string },
  token: string,
): Promise<unknown> {
  return chamarNucleo(`/v1/tipos-de-recurso/${id}/valores-de-referencia`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface PrecoDeReferencia {
  id: string;
  tipo_de_recurso_id: string;
  preco_em_pontos_extras: number;
  vigencia_inicio: string;
  vigencia_fim: string | null;
}

// Histórico do preço em pontos extras, da vigência mais recente para a mais
// antiga (`RF-07-43`).
export function listarPrecosDeReferencia(
  id: string,
  token: string,
): Promise<PrecoDeReferencia[]> {
  return chamarNucleo<PrecoDeReferencia[]>(`/v1/tipos-de-recurso/${id}/precos-de-referencia`, {
    token,
  });
}

export function registrarPrecoDeReferencia(
  id: string,
  entrada: { preco_em_pontos_extras: number; vigencia_inicio: string },
  token: string,
): Promise<PrecoDeReferencia> {
  return chamarNucleo<PrecoDeReferencia>(`/v1/tipos-de-recurso/${id}/precos-de-referencia`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export function desativarTipoDeRecurso(id: string, token: string): Promise<TipoDeRecurso> {
  return chamarNucleo<TipoDeRecurso>(`/v1/tipos-de-recurso/${id}/desativacao`, {
    metodo: "POST",
    token,
  });
}

export function reativarTipoDeRecurso(id: string, token: string): Promise<TipoDeRecurso> {
  return chamarNucleo<TipoDeRecurso>(`/v1/tipos-de-recurso/${id}/reativacao`, {
    metodo: "POST",
    token,
  });
}

// Só o tipo nunca usado sai; o usado volta com o código `tipo_em_uso`
// (`RN-07-40`).
export function excluirTipoDeRecurso(id: string, token: string): Promise<void> {
  return chamarNucleo<void>(`/v1/tipos-de-recurso/${id}`, { metodo: "DELETE", token });
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
