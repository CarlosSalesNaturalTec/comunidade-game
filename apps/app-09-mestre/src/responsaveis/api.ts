import { chamarNucleo } from "comum/api";

export interface GuerreiroVinculavel {
  id: string;
  nick: string;
  avatar: string;
}

export interface ListaDeGuerreirosVinculaveis {
  itens: GuerreiroVinculavel[];
  proximo_cursor: string | null;
}

// Nick e avatar dos Guerreiros e Guerreiras ativos das comunidades do
// Mestre em sessão — nunca nome civil, nascimento ou imagem real
// (`RF-09-62`, `RN-09-18`).
export function listarGuerreirosVinculaveis(
  token: string,
  cursor: string | null = null,
): Promise<ListaDeGuerreirosVinculaveis> {
  const caminho = cursor
    ? `/v1/guerreiros/vinculaveis?cursor=${encodeURIComponent(cursor)}`
    : "/v1/guerreiros/vinculaveis";
  return chamarNucleo<ListaDeGuerreirosVinculaveis>(caminho, { token });
}

export interface ResponsavelCriado {
  id: string;
  nome: string;
}

// O nome é o conteúdo mínimo do responsável, e o cadastro pressupõe que
// ele se apresentou pessoalmente no encontro (`RF-09-62`, `RN-09-15`).
// O e-mail é opcional e, informado, abre o login pela conta Google na App 07
// (`RF-09-147`, `RF-01-92`).
export function cadastrarResponsavel(
  nome: string,
  token: string,
  email?: string,
): Promise<ResponsavelCriado> {
  const corpo: { nome: string; email?: string } = { nome };
  if (email?.trim()) corpo.email = email.trim();
  return chamarNucleo<ResponsavelCriado>("/v1/responsaveis", {
    metodo: "POST",
    corpo,
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
  nome: string;
  grau_de_parentesco: string;
}

export interface ResponsavelDaLista {
  id: string;
  nome: string;
  // O acesso: e-mail do login social e usuário da credencial de usuário e
  // senha, vazios quando não existem — nunca a senha (`RF-01-92`).
  email: string;
  usuario: string;
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
// própria. Nome do responsável e, de cada vinculado, nick, nome e grau de
// parentesco: nunca credencial, usuário ou contato, nem imagem real,
// nascimento ou contato da criança (`RF-09-122`, `RN-09-18`).
export function listarResponsaveis(token: string): Promise<ListaDeResponsaveis> {
  return chamarNucleo<ListaDeResponsaveis>("/v1/responsaveis", { token });
}
