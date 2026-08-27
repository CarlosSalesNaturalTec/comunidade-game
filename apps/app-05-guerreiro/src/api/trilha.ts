import { chamarNucleo } from "comum/api";

export interface TrilhaComProximaMissao {
  id: string;
  nome: string;
  poder_id: string;
  proxima_missao_id: string | null;
  proxima_missao_titulo: string | null;
  proxima_missao_posicao: number | null;
}

// As trilhas em que o Guerreiro(a) em sessão está inscrito, cada uma com a
// próxima missão do percurso dele — sem inscrição, a lista sai vazia
// (`RF-05-08`, `RF-05-17`).
export function listarMinhasTrilhas(token: string): Promise<TrilhaComProximaMissao[]> {
  return chamarNucleo<TrilhaComProximaMissao[]>("/v1/eu/trilhas", { token });
}

export interface Inscricao {
  id: string;
  trilha_id: string;
  momento: string;
}

// Ato do próprio Guerreiro(a) — inscrever-se de novo na mesma trilha
// devolve a inscrição existente, sem erro (`RF-05-09`, `RN-05-43`).
export function inscreverNaTrilha(trilhaId: string, token: string): Promise<Inscricao> {
  return chamarNucleo<Inscricao>(`/v1/eu/trilhas/${trilhaId}/inscricao`, {
    metodo: "POST",
    token,
  });
}

export type TipoDeDesafioDeDesbloqueio = "quiz" | "pratico";

export interface DesafioDeDesbloqueio {
  tipo: TipoDeDesafioDeDesbloqueio;
  enunciado: string;
  alternativas: string[] | null;
}

export interface MissaoNoPercurso {
  id: string;
  titulo: string;
  posicao: number;
  obrigatoria: boolean;
  e_sondagem: boolean;
  desbloqueada: boolean;
  e_proxima: boolean;
  aguardando_mestre: boolean;
  motivo_do_bloqueio: string | null;
  desafio_de_desbloqueio: DesafioDeDesbloqueio | null;
}

// O estado da missão no percurso do Guerreiro(a) — desbloqueada, próxima,
// bloqueada com motivo ou aguardando o Mestre. O conteúdo e a bibliografia
// continuam vindo de `GET /v1/trilhas/{id}` (design — decisão 6).
export function obterMissaoNoPercurso(
  trilhaId: string,
  ordem: number,
  token: string,
): Promise<MissaoNoPercurso> {
  return chamarNucleo<MissaoNoPercurso>(`/v1/eu/trilhas/${trilhaId}/missoes/${ordem}`, {
    token,
  });
}

export interface ResultadoDaSubmissaoDoDesbloqueio {
  aprovado: boolean | null;
  aguardando_mestre: boolean;
}

// Submete o desafio de desbloqueio — no quiz, `alternativaEscolhida` é
// exigida; no prático, a chamada é a própria declaração de que cumpriu
// (`RF-05-13`, `RF-05-14`, `RN-05-20`).
export function submeterDesafioDeDesbloqueio(
  missaoId: string,
  alternativaEscolhida: number | null,
  token: string,
): Promise<ResultadoDaSubmissaoDoDesbloqueio> {
  return chamarNucleo<ResultadoDaSubmissaoDoDesbloqueio>(
    `/v1/eu/missoes/${missaoId}/desbloqueio`,
    {
      metodo: "POST",
      corpo: { alternativa_escolhida: alternativaEscolhida },
      token,
    },
  );
}

export interface ProgressoDaTrilha {
  trilha_id: string;
  trilha_nome: string;
  nivel_atual: number | null;
  obrigatorias_desbloqueadas: number;
  obrigatorias_totais: number;
  pontos_regulares: number;
  badges: string[];
}

// Nível e quanto falta para o próximo, pontos e badges, por trilha
// inscrita — nível é percurso, nunca saldo de pontos (`RF-05-15`,
// `RF-05-16`, `RN-05-03`, `RN-05-04`).
export function obterProgresso(token: string): Promise<ProgressoDaTrilha[]> {
  return chamarNucleo<ProgressoDaTrilha[]>("/v1/eu/progresso", { token });
}

export interface ConteudoDaMissaoPublico {
  id: string;
  ordem: number;
  tipo: string;
  corpo: string | null;
  endereco: string | null;
  referencia: string | null;
  autoria: string;
  fonte: string | null;
}

export interface BibliografiaDaMissaoPublica {
  id: string;
  titulo: string;
  capitulo: string;
  disponivel: boolean | null;
  apoiador_nome: string | null;
}

export interface MissaoPublica {
  id: string;
  titulo: string;
  posicao: number;
  obrigatoria: boolean;
  e_sondagem: boolean;
  conteudos: ConteudoDaMissaoPublico[];
  bibliografia: BibliografiaDaMissaoPublica[];
}

export interface TrilhaPublicaComMissoes {
  id: string;
  nome: string;
  licenca: string;
  autor_nome: string | null;
  missoes: MissaoPublica[];
}

// Conteúdo, bibliografia, crédito e licença — sem inventar rota nova: a
// mesma leitura pública que a capacidade `conteudo-da-missao` já entrega
// (design — decisão 6). `pontoDeApoioId` só orienta a disponibilidade do
// exemplar da bibliografia, quando o Guerreiro(a) tiver um.
export function obterTrilhaPublica(
  trilhaId: string,
  pontoDeApoioId?: string | null,
): Promise<TrilhaPublicaComMissoes> {
  const consulta = pontoDeApoioId
    ? `?ponto_de_apoio_id=${encodeURIComponent(pontoDeApoioId)}`
    : "";
  return chamarNucleo<TrilhaPublicaComMissoes>(`/v1/trilhas/${trilhaId}${consulta}`);
}

export interface TrilhaPublica {
  id: string;
  nome: string;
}

export interface PoderPublico {
  id: string;
  nome: string;
  descricao: string;
  trilhas: TrilhaPublica[];
}

// O catálogo de poderes do ciclo, com as trilhas publicadas de cada um —
// a mesma leitura pública que a Carteira já usa para o filtro do ranking
// (`RF-05-09`).
export function listarPoderesDoCatalogo(): Promise<PoderPublico[]> {
  return chamarNucleo<PoderPublico[]>("/v1/vitrine/poderes");
}
