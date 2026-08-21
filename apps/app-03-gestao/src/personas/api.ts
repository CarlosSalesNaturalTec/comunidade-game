import { chamarNucleo } from "../api/cliente";

export interface GuerreiroDaLista {
  id: string;
  nome: string;
  nascimento: string;
  nick: string;
  avatar: string;
}

interface ListaDeGuerreiros {
  itens: GuerreiroDaLista[];
  proximo_cursor: string | null;
}

export function listarGuerreiros(token: string): Promise<ListaDeGuerreiros> {
  return chamarNucleo<ListaDeGuerreiros>("/v1/guerreiros", { token });
}

export interface CadastrarGuerreiroEntrada {
  nome: string;
  nascimento: string;
  nick: string;
  avatar: string;
  aula_id: string;
}

export function cadastrarGuerreiro(
  entrada: CadastrarGuerreiroEntrada,
  token: string,
): Promise<GuerreiroDaLista> {
  return chamarNucleo<GuerreiroDaLista>("/v1/guerreiros", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface EditarGuerreiroEntrada {
  nome: string;
  nascimento: string;
  nick: string;
  avatar: string;
}

export function editarGuerreiro(
  id: string,
  entrada: EditarGuerreiroEntrada,
  token: string,
): Promise<GuerreiroDaLista> {
  return chamarNucleo<GuerreiroDaLista>(`/v1/guerreiros/${id}`, {
    metodo: "PATCH",
    corpo: entrada,
    token,
  });
}

export interface ArtefatoComprobatorio {
  endereco: string;
  rotulo: string;
}

export interface AdultoDaLista {
  id: string;
  nome: string;
  email: string;
  whatsapp: string | null;
  nick: string | null;
  artefatos: ArtefatoComprobatorio[];
}

interface ListaDeAdultos {
  itens: AdultoDaLista[];
  proximo_cursor: string | null;
}

export function listarMestres(token: string): Promise<ListaDeAdultos> {
  return chamarNucleo<ListaDeAdultos>("/v1/mestres", { token });
}

export function listarApoiadores(token: string): Promise<ListaDeAdultos> {
  return chamarNucleo<ListaDeAdultos>("/v1/apoiadores", { token });
}

export interface CadastrarAdultoEntrada {
  nome: string;
  email: string;
  whatsapp?: string;
  nick?: string;
  artefatos: ArtefatoComprobatorio[];
}

export function cadastrarMestre(
  entrada: CadastrarAdultoEntrada,
  token: string,
): Promise<AdultoDaLista> {
  return chamarNucleo<AdultoDaLista>("/v1/mestres", { metodo: "POST", corpo: entrada, token });
}

export function cadastrarApoiador(
  entrada: CadastrarAdultoEntrada,
  token: string,
): Promise<AdultoDaLista> {
  return chamarNucleo<AdultoDaLista>("/v1/apoiadores", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface GravarNickDoAdultoSaida {
  nick: string;
}

export function gravarNickDoAdulto(
  personaId: string,
  nick: string,
  token: string,
): Promise<GravarNickDoAdultoSaida> {
  return chamarNucleo<GravarNickDoAdultoSaida>(`/v1/personas/${personaId}/nick`, {
    metodo: "PATCH",
    corpo: { nick },
    token,
  });
}

export interface AdminDaLista {
  id: string;
  nome: string;
  email: string;
  whatsapp: string | null;
}

export interface IncluirAdminEntrada {
  nome: string;
  email: string;
  whatsapp?: string;
}

export function incluirAdmin(
  entrada: IncluirAdminEntrada,
  token: string,
): Promise<AdminDaLista> {
  return chamarNucleo<AdminDaLista>("/v1/admins", { metodo: "POST", corpo: entrada, token });
}

export interface ResponsavelCriado {
  id: string;
}

export function cadastrarResponsavel(token: string): Promise<ResponsavelCriado> {
  return chamarNucleo<ResponsavelCriado>("/v1/responsaveis", { metodo: "POST", token });
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
