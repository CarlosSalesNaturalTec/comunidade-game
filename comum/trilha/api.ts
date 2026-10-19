import { chamarNucleo, lerArquivoDoNucleo } from "../api/cliente";

// A fatia do cliente de trilha que as telas promovidas usam — leitura do
// percurso, conteúdo da missão, catálogo de poderes e os dois atos de
// escrita que as duas aplicações ligam: a inscrição e a submissão do
// desbloqueio. O que é só da App 05 — progresso, retomadas e entrega
// individual da produção — continua no cliente dela (`RF-05-08`,
// `RF-05-09`, `RF-05-10`, `RF-05-17`, design — decisão 2).

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

export interface PerguntaDoDesbloqueio {
  id: string;
  ordem: number;
  enunciado: string;
  // Nunca a alternativa correta: ela não sai do núcleo para o
  // Guerreiro(a) (`RF-09-118`).
  alternativas: string[];
  // Diz apenas **se** a pergunta tem imagem; os bytes vêm da rota própria,
  // que confere quem pede (`RF-09-119`).
  imagem_referencia: string | null;
}

// Os bytes da imagem da pergunta, servidos a quem está inscrito na trilha.
// `<img src>` não manda cabeçalho, e toda rota sob `/v1` exige a chave da
// aplicação — por isso a tela busca e cria a URL local (`RF-09-119`).
export function lerImagemDaPergunta(idDaPergunta: string, token: string): Promise<Blob> {
  return lerArquivoDoNucleo(`/v1/perguntas-do-desbloqueio/${idDaPergunta}/imagem`, { token });
}

export interface DesafioDeDesbloqueio {
  tipo: TipoDeDesafioDeDesbloqueio;
  // O quiz traz `perguntas`, uma ou mais; o prático traz `enunciado`.
  enunciado: string | null;
  perguntas: PerguntaDoDesbloqueio[] | null;
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
// continuam vindo de `GET /v1/trilhas/{id}`.
export function obterMissaoNoPercurso(
  trilhaId: string,
  ordem: number,
  token: string,
): Promise<MissaoNoPercurso> {
  return chamarNucleo<MissaoNoPercurso>(`/v1/eu/trilhas/${trilhaId}/missoes/${ordem}`, {
    token,
  });
}

export interface RespostaDoDesbloqueio {
  pergunta_id: string;
  alternativa_escolhida: number;
}

export interface ResultadoDaSubmissaoDoDesbloqueio {
  aprovado: boolean | null;
  aguardando_mestre: boolean;
  acertos: number;
  total: number;
}

// Submete o desafio de desbloqueio — no quiz, a submissão leva a resposta
// de **todas** as perguntas de uma vez e a devolutiva diz quantas ele
// acertou; no prático, a chamada é a própria declaração de que cumpriu
// (`RF-05-13`, `RF-05-14`, `RF-05-89`, `RN-05-20`).
export function submeterDesafioDeDesbloqueio(
  missaoId: string,
  respostas: RespostaDoDesbloqueio[] | null,
  token: string,
): Promise<ResultadoDaSubmissaoDoDesbloqueio> {
  return chamarNucleo<ResultadoDaSubmissaoDoDesbloqueio>(
    `/v1/eu/missoes/${missaoId}/desbloqueio`,
    {
      metodo: "POST",
      corpo: { respostas },
      token,
    },
  );
}

export interface AtividadeDaMissaoPublica {
  id: string;
  titulo: string;
  producao_esperada: string;
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

// Os bytes do arquivo do conteúdo, servidos a quem está inscrito na trilha
// — mesma razão da imagem da pergunta: `<img src>` não manda cabeçalho e
// toda rota sob `/v1` exige a chave da aplicação (`RF-05-11`).
export function lerArquivoDoConteudo(idDoConteudo: string, token: string): Promise<Blob> {
  return lerArquivoDoNucleo(`/v1/conteudos/${idDoConteudo}/arquivo`, { token });
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
  atividades: AtividadeDaMissaoPublica[];
  conteudos: ConteudoDaMissaoPublico[];
  bibliografia: BibliografiaDaMissaoPublica[];
}

export type ModalidadeDaCulminancia = "individual" | "em_equipe";

export interface CulminanciaDaTrilha {
  id: string;
  trilha_id: string;
  descricao: string;
  modalidade: ModalidadeDaCulminancia;
  criterio_de_validacao: string;
}

export interface TrilhaPublicaComMissoes {
  id: string;
  nome: string;
  licenca: string;
  autor_nome: string | null;
  missoes: MissaoPublica[];
  // `null` é "esta trilha ainda não declarou culminância" — a tela avisa
  // em linguagem simples e não oferece a entrega (`RF-05-39`).
  culminancia: CulminanciaDaTrilha | null;
}

// Conteúdo, bibliografia, crédito e licença — sem inventar rota nova: a
// mesma leitura pública que a capacidade `conteudo-da-missao` já entrega.
// `pontoDeApoioId` só orienta a disponibilidade do exemplar da
// bibliografia, quando o Guerreiro(a) tiver um.
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

// A recompensa de marco que o Guerreiro(a) **conquistou** — o marco alcançado
// é o desbloqueio da missão, e no desafio prático só depois de o Mestre autor
// julgar (`RF-05-45`, `RN-05-50`).
export interface RecompensaConquistada {
  recompensa_de_marco_id: string;
  trilha_id: string;
  missao_id: string;
  tipo_de_recurso_id: string;
  // O nome e a unidade do tipo: sem eles a tela só tem a quantidade, e "1"
  // não diz se é o livro, a camisa ou o kit. Nunca valor em moedas nem em
  // reais, que ficam no lançamento (invariante 16).
  tipo_de_recurso_nome: string;
  tipo_de_recurso_unidade: string;
  quantidade: number;
  entregue: boolean;
  entregue_em: string | null;
  // `RN-05-50`: é o que faz a tela aparecer uma vez, e esperar o julgamento
  // do Mestre no desafio prático.
  ciente: boolean;
}

// As recompensas conquistadas pelo Guerreiro(a) em sessão, de **todas** as
// trilhas que ele percorre — quem apresenta filtra pela trilha aberta, para
// recompensa de outra trilha nunca interromper este percurso (design —
// decisão 3).
export function listarMinhasRecompensas(token: string): Promise<RecompensaConquistada[]> {
  return chamarNucleo<RecompensaConquistada[]>("/v1/eu/recompensas", { token });
}

export interface CienciaDaRecompensa {
  recompensa_de_marco_id: string;
  guerreiro_id: string;
  registrado_em: string;
}

// Dá ciência da recompensa — o ato do botão avançar. Ninguém a dá pelo outro,
// e por isso não há corpo: o Guerreiro(a) é o da sessão. Chamar de novo
// mantém a ciência que havia, sem erro (`RN-05-50`, design — decisão 8).
export function darCienciaDaRecompensa(
  recompensaId: string,
  token: string,
): Promise<CienciaDaRecompensa> {
  return chamarNucleo<CienciaDaRecompensa>(`/v1/eu/recompensas/${recompensaId}/ciencia`, {
    metodo: "POST",
    token,
  });
}
