import { chamarNucleo, lerArquivoDoNucleo } from "comum/api";

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
// aplicação — por isso a tela busca e cria a URL local (`RF-09-119`,
// design — decisão 6).
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

export type FormaDeEntregaDaProducao = "texto" | "audio" | "foto";

export interface ProducaoDaMissao {
  id: string;
  equipe_id: string | null;
  guerreiro_id: string | null;
  missao_id: string;
  atividade_id: string;
  forma: FormaDeEntregaDaProducao;
  transcricao: string;
  devolutiva: string | null;
  registrado_em: string;
}

interface EntregarProducaoIndividualEntrada {
  atividadeId: string;
  forma: FormaDeEntregaDaProducao;
  texto?: string;
  arquivo?: Blob;
}

// `RF-05-74` a `RF-05-77`: a entrega individual, sobre uma missão do
// próprio percurso — a mesma superfície `multipart/form-data` da porta de
// equipe do App 01, que a foto mantém. A devolutiva volta construtiva e
// nunca credita ponto; a foto não fica no aparelho depois do envio, e a
// fala vai transcrita em `texto` — o áudio não é enviado (`RF-05-76`,
// `RN-05-32`).
export function entregarProducaoIndividual(
  missaoId: string,
  entrada: EntregarProducaoIndividualEntrada,
  token: string,
): Promise<ProducaoDaMissao> {
  const formulario = new FormData();
  formulario.set("forma", entrada.forma);
  formulario.set("atividade_id", entrada.atividadeId);
  if (entrada.texto !== undefined) formulario.set("texto", entrada.texto);
  if (entrada.arquivo !== undefined) formulario.set("arquivo", entrada.arquivo);

  return chamarNucleo<ProducaoDaMissao>(`/v1/eu/missoes/${missaoId}/producao`, {
    metodo: "POST",
    formulario,
    token,
  });
}

export interface RetomadaEmAberto {
  missao_id: string;
  missao_titulo: string;
  trilha_id: string;
  trilha_titulo: string;
  prazo: string;
}

// As retomadas em aberto do Guerreiro(a) em sessão — missão, trilha e
// prazo de cada agendamento vencido sem produção, sem lista vazia
// distinguir de erro (`RF-05-79`, `RF-05-80`).
export function listarMinhasRetomadas(token: string): Promise<RetomadaEmAberto[]> {
  return chamarNucleo<RetomadaEmAberto[]>("/v1/eu/retomadas", { token });
}
