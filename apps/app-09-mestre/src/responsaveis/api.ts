import { chamarNucleo } from "comum/api";

export interface GuerreiroVinculavel {
  id: string;
  nick: string;
  avatar: string;
}

interface ListaDeGuerreirosVinculaveis {
  itens: GuerreiroVinculavel[];
  proximo_cursor: string | null;
}

// Nick e avatar dos Guerreiros e Guerreiras ativos das comunidades do
// Mestre em sessão — nunca nome civil, nascimento ou imagem real
// (`RF-09-62`, `RN-09-18`).
export function listarGuerreirosVinculaveis(
  token: string,
): Promise<ListaDeGuerreirosVinculaveis> {
  return chamarNucleo<ListaDeGuerreirosVinculaveis>("/v1/guerreiros/vinculaveis", { token });
}

export interface ResponsavelCriado {
  id: string;
  nome: string;
}

// O nome é o conteúdo mínimo do responsável, e o cadastro pressupõe que
// ele se apresentou pessoalmente no encontro (`RF-09-62`, `RN-09-15`).
export function cadastrarResponsavel(nome: string, token: string): Promise<ResponsavelCriado> {
  return chamarNucleo<ResponsavelCriado>("/v1/responsaveis", {
    metodo: "POST",
    corpo: { nome },
    token,
  });
}

export interface CriarVinculoEntrada {
  guerreiro_id: string;
  grau_de_parentesco: string;
}

export interface VinculoCriado {
  id: string;
  responsavel_id: string;
  guerreiro_id: string;
  grau_de_parentesco: string;
  inicio: string;
}

// Cada vínculo declara o seu próprio grau de parentesco; o núcleo recusa o
// quarto vínculo vigente para o mesmo Guerreiro(a) (`RF-09-63`, `RF-09-64`,
// `RN-09-15`).
export function criarVinculo(
  responsavelId: string,
  entrada: CriarVinculoEntrada,
  token: string,
): Promise<VinculoCriado> {
  return chamarNucleo<VinculoCriado>(`/v1/responsaveis/${responsavelId}/vinculos`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface CriarCredencialEntrada {
  persona_id: string;
  usuario: string;
}

export interface CredencialCriada {
  id: string;
  usuario: string;
  senha_provisoria: string;
}

// Só para o responsável sem conta Google — a senha só é exibida nesta
// resposta e nunca mais é recuperável (`RF-09-65`, `RN-09-23`).
export function criarCredencialProvisoria(
  entrada: CriarCredencialEntrada,
  token: string,
): Promise<CredencialCriada> {
  return chamarNucleo<CredencialCriada>("/v1/credenciais", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}
