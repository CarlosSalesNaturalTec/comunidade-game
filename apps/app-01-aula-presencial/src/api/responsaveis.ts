import { chamarNucleo } from "comum/api";

export interface ResponsavelCadastrado {
  id: string;
  nome: string;
}

interface CadastroDoResponsavel {
  nome: string;
}

// O responsável mínimo do encontro: só o nome (`RF-04-60`, design —
// decisão 1). E-mail, credencial e digitalização do termo ficam com a
// gestão — a tela do encontro nunca os pede.
export function cadastrarResponsavelNoEncontro(
  entrada: CadastroDoResponsavel,
  tokenDeTrabalho: string,
): Promise<ResponsavelCadastrado> {
  return chamarNucleo<ResponsavelCadastrado>("/v1/responsaveis", {
    metodo: "POST",
    corpo: entrada,
    token: tokenDeTrabalho,
  });
}

export interface VinculoCriado {
  id: string;
  responsavel_id: string;
  guerreiro_id: string;
  grau_de_parentesco: string;
  inicio: string;
}

interface CriarVinculoEntrada {
  guerreiro_id: string;
  grau_de_parentesco: string;
}

// O vínculo com o grau de parentesco declarado na tela do responsável
// (`RF-04-60`).
export function criarVinculo(
  responsavelId: string,
  entrada: CriarVinculoEntrada,
  tokenDeTrabalho: string,
): Promise<VinculoCriado> {
  return chamarNucleo<VinculoCriado>(`/v1/responsaveis/${responsavelId}/vinculos`, {
    metodo: "POST",
    corpo: entrada,
    token: tokenDeTrabalho,
  });
}
