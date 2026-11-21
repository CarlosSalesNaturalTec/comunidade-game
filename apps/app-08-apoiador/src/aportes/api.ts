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

// As duas espécies: a da aula traz aula e horário; a da recompensa de marco,
// a trilha, sem aula nem horário (`RF-14-24`, `RF-07-54`).
export interface NecessidadeDeRecurso {
  especie: "aula" | "recompensa_de_marco";
  aula_id: string | null;
  trilha_id: string | null;
  trilha_nome: string | null;
  tipo_de_recurso_id: string;
  tipo_de_recurso_nome: string;
  quantidade_faltante: string;
  valor_em_moedas: string | null;
  comunidade_virtual_id: string;
  comunidade_virtual_nome: string;
  ponto_de_apoio_id: string;
  ponto_de_apoio_nome: string;
  inicio_em: string | null;
  fim_em: string | null;
}

// A identidade da necessidade: aula + tipo, ou comunidade + trilha + tipo
// (`RF-07-54`).
export function chaveDaNecessidade(necessidade: NecessidadeDeRecurso): string {
  return necessidade.especie === "aula"
    ? `${necessidade.aula_id}-${necessidade.tipo_de_recurso_id}`
    : `${necessidade.comunidade_virtual_id}-${necessidade.trilha_id}-${necessidade.tipo_de_recurso_id}`;
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
  comunidade_virtual_id: string | null;
  trilha_id: string | null;
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
  comunidade_virtual_id?: string;
  trilha_id?: string;
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
  if (entrada.comunidade_virtual_id)
    formulario.set("comunidade_virtual_id", entrada.comunidade_virtual_id);
  if (entrada.trilha_id) formulario.set("trilha_id", entrada.trilha_id);
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
