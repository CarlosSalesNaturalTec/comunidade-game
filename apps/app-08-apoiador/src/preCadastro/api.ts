import { chamarNucleo } from "comum/api";
import type { PerfilDeApoiador } from "./escada";

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

export interface PreCadastroDeApoiadorEntrada {
  nome_ou_razao_social: string;
  email: string;
  whatsapp: string;
  perfil: PerfilDeApoiador;
  nick: string;
  aporte_declarado: string;
  comprovante: File;
}

interface SolicitacaoSaida {
  id: string;
  prazo: string;
}

// A leitura das necessidades em aberto, para a primeira das três formas de
// declarar o aporte (`RF-14-02`, PRD-07). Pública, sem token de sessão.
export function listarNecessidadesEmAberto(): Promise<NecessidadeDeRecurso[]> {
  return chamarNucleo<NecessidadeDeRecurso[]>("/v1/vitrine/necessidades");
}

// O pré-cadastro em si, sem token de sessão — a mesma rota que serve o
// formulário da vitrine (`RF-14-01` a `RF-14-04`, design — decisão 5).
export function registrarPreCadastroDeApoiador(
  entrada: PreCadastroDeApoiadorEntrada,
): Promise<SolicitacaoSaida> {
  const formulario = new FormData();
  formulario.set("nome_ou_razao_social", entrada.nome_ou_razao_social);
  formulario.set("email", entrada.email);
  formulario.set("whatsapp", entrada.whatsapp);
  formulario.set("pretensao", "apoiador");
  formulario.set("apresentacao", entrada.aporte_declarado);
  formulario.set("perfil", entrada.perfil);
  formulario.set("nick", entrada.nick);
  formulario.set("aporte_declarado", entrada.aporte_declarado);
  formulario.set("comprovante", entrada.comprovante);

  return chamarNucleo<SolicitacaoSaida>("/v1/solicitacoes-de-participacao", {
    metodo: "POST",
    formulario,
  });
}
