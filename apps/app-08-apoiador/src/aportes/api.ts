import { chamarNucleo } from "comum/api";

export interface AporteDoApoiador {
  id: string;
  tipo_de_recurso_id: string;
  tipo_de_recurso_nome: string;
  quantidade: string;
  ponto_de_apoio_id: string;
  ponto_de_apoio_nome: string;
  valor_em_moedas: string;
  forma: string;
  situacao_de_ressarcimento: string;
  data_do_aporte: string;
}

export interface MeusAportesSaida {
  poder_sustentador_em_moedas: string;
  aportes: AporteDoApoiador[];
}

// "Meus aportes": só os já homologados, com o Poder Sustentador como total
// acumulado em moedas (`RF-14-21`, `RF-14-22`).
export function listarMeusAportes(token: string): Promise<MeusAportesSaida> {
  return chamarNucleo<MeusAportesSaida>("/v1/meus-aportes", { token });
}

export interface NecessidadeDeRecurso {
  aula_id: string;
  tipo_de_recurso_id: string;
  tipo_de_recurso_nome: string;
  quantidade_faltante: string;
  valor_em_moedas: string | null;
  comunidade_virtual_id: string;
  comunidade_virtual_nome: string;
  ponto_de_apoio_id: string;
  ponto_de_apoio_nome: string;
  inicio_em: string;
  fim_em: string;
}

// As necessidades em aberto de todas as comunidades, pública e sem token —
// a mesma rota que a porta pública já lê (`RF-14-24`).
export function listarNecessidadesEmAberto(): Promise<NecessidadeDeRecurso[]> {
  return chamarNucleo<NecessidadeDeRecurso[]>("/v1/vitrine/necessidades");
}

export type OrigemDaEscolhaDoAporte =
  | "missao"
  | "necessidade"
  | "valor_sugerido"
  | "valor_livre";
export type SituacaoDaDeclaracao = "pendente" | "homologada" | "recusada";

export interface AporteDeclarado {
  id: string;
  valor_declarado: string;
  origem_da_escolha: OrigemDaEscolhaDoAporte;
  aula_id: string | null;
  tipo_de_recurso_id: string | null;
  missao_do_apoiador_id: string | null;
  situacao: SituacaoDaDeclaracao;
  registrado_em: string;
  motivo_da_recusa: string | null;
}

export interface DeclararAporteEntrada {
  valor_declarado: number;
  origem_da_escolha: OrigemDaEscolhaDoAporte;
  aula_id?: string;
  tipo_de_recurso_id?: string;
  missao_do_apoiador_id?: string;
  comprovante: File;
}

// A declaração do Apoiador em sessão: sempre em dinheiro, sempre pendente,
// sem creditar nada até a homologação do Admin (`RF-14-25`, `RF-14-26`,
// `RN-14-07`). A origem `missao` aponta a missão escolhida, inteira ou em
// parte (`RF-14-63`).
export function declararAporte(
  entrada: DeclararAporteEntrada,
  token: string,
): Promise<AporteDeclarado> {
  const formulario = new FormData();
  formulario.set("valor_declarado", String(entrada.valor_declarado));
  formulario.set("forma", "financeira");
  formulario.set("origem_da_escolha", entrada.origem_da_escolha);
  if (entrada.aula_id) formulario.set("aula_id", entrada.aula_id);
  if (entrada.tipo_de_recurso_id)
    formulario.set("tipo_de_recurso_id", entrada.tipo_de_recurso_id);
  if (entrada.missao_do_apoiador_id)
    formulario.set("missao_do_apoiador_id", entrada.missao_do_apoiador_id);
  formulario.set("comprovante", entrada.comprovante);

  return chamarNucleo<AporteDeclarado>("/v1/aportes/declarados", {
    metodo: "POST",
    formulario,
    token,
  });
}

// A situação de cada declaração do próprio Apoiador — pendente, homologada
// ou recusada com motivo (`RF-14-27`).
export function listarMinhasDeclaracoesDeAporte(token: string): Promise<AporteDeclarado[]> {
  return chamarNucleo<AporteDeclarado[]>("/v1/eu/aportes/declarados", { token });
}
