import { chamarNucleo } from "comum/api";

export interface AporteHomologado {
  id: string;
  provedor_id: string;
  tipo_de_recurso_id: string;
  quantidade: string;
  ponto_de_apoio_id: string;
  valor_em_moedas: string;
  forma: string;
  data_do_aporte: string;
}

export interface HomologarAporteEntrada {
  provedorId: string;
  tipoDeRecursoId: string;
  quantidade: string;
  pontoDeApoioId: string;
  dataDoAporte: string;
  forma: "financeira" | "material" | "servico";
  solicitacaoDeParticipacaoId: string;
}

// Homologa o que o pré-cadastro só declarou (`RF-02-84`, `RF-07-30`,
// `RN-07-21`). Nenhuma rota nova: `POST /aportes` já existe e já recusa
// homologar a mesma solicitação duas vezes.
export function homologarAporte(
  entrada: HomologarAporteEntrada,
  token: string,
): Promise<AporteHomologado> {
  const formulario = new FormData();
  formulario.set("provedor_id", entrada.provedorId);
  formulario.set("tipo_de_recurso_id", entrada.tipoDeRecursoId);
  formulario.set("quantidade", entrada.quantidade);
  formulario.set("ponto_de_apoio_id", entrada.pontoDeApoioId);
  formulario.set("data_do_aporte", entrada.dataDoAporte);
  formulario.set("forma", entrada.forma);
  formulario.set("destinacao", "lastro");
  formulario.set("solicitacao_de_participacao_id", entrada.solicitacaoDeParticipacaoId);

  return chamarNucleo<AporteHomologado>("/v1/aportes", {
    metodo: "POST",
    formulario,
    token,
  });
}
