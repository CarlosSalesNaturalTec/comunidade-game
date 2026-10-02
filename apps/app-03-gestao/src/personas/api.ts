import { chamarNucleo } from "comum/api";

export interface GuerreiroDaLista {
  id: string;
  nome: string;
  nascimento: string;
  nick: string;
  avatar: string;
  // O vínculo vigente, para o Admin conferir o que a aula agendada
  // atribuiu — vazio quando o Guerreiro(a) ainda não tem vínculo
  // (`RF-02-15`, `RN-02-06`).
  comunidade_virtual_id: string | null;
  vinculo_iniciado_em: string | null;
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

/** O que o cadastro declara — endereço e rótulo, nada mais. O identificador e
 * a marca de publicado são do núcleo e só existem na leitura. */
export interface ArtefatoDeclarado {
  endereco: string;
  rotulo: string;
}

export interface ArtefatoComprobatorio extends ArtefatoDeclarado {
  // A gestão precisa do identificador para alcançar a rota de anexação, e da
  // marca de publicado para separar o que espera do que já está público; os
  // dois vêm do núcleo, e `publicado` é derivado lá (`RF-02-101`).
  id: string;
  publicado: boolean;
  // Preenchidos só quando o próprio adulto editou o artefato do cadastro —
  // a ficha marca o que foi mexido e mostra o original ao lado do vigente
  // (`RF-02-04`, `RN-09-14`).
  endereco_original?: string | null;
  rotulo_original?: string | null;
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

export function listarApoiadores(token: string, cursor?: string): Promise<ListaDeAdultos> {
  const sufixo = cursor ? `?${new URLSearchParams({ cursor }).toString()}` : "";
  return chamarNucleo<ListaDeAdultos>(`/v1/apoiadores${sufixo}`, { token });
}

/** Um documento comprobatório que um Apoiador declarou pela App 08 e que
 * ainda espera a anexação do Admin, já com o Apoiador a que pertence. */
export interface ComprobatorioPendente {
  artefato_id: string;
  apoiador_id: string;
  apoiador: string;
  endereco: string;
  rotulo: string;
}

// A fila dos pendentes deriva da listagem de Apoiadores, sem rota própria no
// núcleo — decisão do fundador, 2026-10-02 (design — decisão 2). A listagem é
// paginada por cursor, e por isso percorre todas as páginas: documento em
// página seguinte também espera anexação (`RF-02-101`).
export async function listarComprobatoriosPendentes(
  token: string,
): Promise<ComprobatorioPendente[]> {
  const pendentes: ComprobatorioPendente[] = [];
  let cursor: string | null = null;
  do {
    const pagina: ListaDeAdultos = await listarApoiadores(token, cursor ?? undefined);
    for (const apoiador of pagina.itens) {
      for (const artefato of apoiador.artefatos) {
        if (artefato.publicado) continue;
        pendentes.push({
          artefato_id: artefato.id,
          apoiador_id: apoiador.id,
          apoiador: apoiador.nome,
          endereco: artefato.endereco,
          rotulo: artefato.rotulo,
        });
      }
    }
    cursor = pagina.proximo_cursor;
  } while (cursor);
  return pendentes;
}

/** O que a anexação devolve: a anexação é o ato que publica o documento na
 * página do Apoiador (`RF-02-101`, `RF-14-19`). */
export interface DocumentoAnexado {
  id: string;
  endereco: string;
  rotulo: string;
  publicado: boolean;
}

export function anexarComprobatorio(
  apoiadorId: string,
  artefatoId: string,
  token: string,
): Promise<DocumentoAnexado> {
  return chamarNucleo<DocumentoAnexado>(
    `/v1/apoiadores/${apoiadorId}/artefatos/${artefatoId}/anexacao`,
    { metodo: "POST", token },
  );
}

export interface CadastrarAdultoEntrada {
  nome: string;
  email: string;
  whatsapp?: string;
  nick?: string;
  artefatos: ArtefatoDeclarado[];
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
  nome: string;
}

// O nome é o conteúdo mínimo do responsável, e o núcleo o exige de toda
// aplicação que cadastra: é sobre ele que se apoia o consentimento que
// autoriza a captura da imagem da criança (`RF-02-06`, `RF-04-60`). E-mail e
// credencial não entram aqui — a credencial é ato próprio, mais abaixo.
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

// Nome do responsável e os vinculados dele por nick e grau de parentesco —
// nunca credencial, usuário ou contato, nem nome civil ou nascimento do
// Guerreiro(a). Responsável sem vínculo vem com `vinculados` vazio: é o
// cadastro interrompido, e é para retomá-lo que a lista existe
// (`RF-02-111`, `RN-09-18`).
export function listarResponsaveis(token: string): Promise<ListaDeResponsaveis> {
  return chamarNucleo<ListaDeResponsaveis>("/v1/responsaveis", { token });
}
