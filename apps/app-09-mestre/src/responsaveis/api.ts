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

export interface VinculadoDoResponsavel {
  guerreiro_id: string;
  nick: string;
  grau_de_parentesco: string;
}

export interface ResponsavelDaLista {
  id: string;
  nome: string;
  vinculados: VinculadoDoResponsavel[];
}

interface ListaDeResponsaveis {
  itens: ResponsavelDaLista[];
  proximo_cursor: string | null;
}

// O recorte é do núcleo: ao Mestre em sessão, os responsáveis com vínculo
// vigente a Guerreiro(a) das comunidades em que ele atua, somados aos que
// ele próprio cadastrou — estes últimos ainda que sem vínculo algum, que é
// o cadastro interrompido no encontro. A tela não filtra nada por conta
// própria. Nome, nick e grau de parentesco: nunca credencial, usuário ou
// contato (`RF-09-122`, `RN-09-18`).
export function listarResponsaveis(token: string): Promise<ListaDeResponsaveis> {
  return chamarNucleo<ListaDeResponsaveis>("/v1/responsaveis", { token });
}
