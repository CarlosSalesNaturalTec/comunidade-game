import { chamarNucleo, enviarParteComProgresso } from "comum/api";

export type EtapaDoCiclo = "abertura" | "desenvolvimento" | "marcos" | "fechamento";

// O objetivo vai de 1 a 18 e a meta é livre e opcional; quem recusa o
// objetivo fora da faixa é o núcleo (`RF-09-92`, `RF-09-98`).
export interface EtiquetaOds {
  id: string;
  objetivo: number;
  meta: string | null;
  trilha_id: string | null;
  missao_id: string | null;
}

export interface EtiquetaOdsDeclarada {
  objetivo: number;
  meta?: string | null;
}

// A cobertura é sempre da trilha — a união dos objetivos dela e das missões
// dela —, nunca por Guerreiro(a) (`RF-09-94`, `RN-01-24`).
export interface CoberturaOdsDaTrilha {
  objetivos: number[];
  ciclo: string;
}

export interface AtividadeDaMissao {
  id: string;
  missao_id: string;
  titulo: string;
  descricao: string | null;
  modalidade: string;
  formato: string;
  natureza: string;
  producao_esperada: string;
  // O encontro em que a atividade presencial acontece — anulável, e nunca
  // declarado por atividade on-line ou assíncrona (`RF-09-69`, `RF-09-73`).
  aula_id: string | null;
}

export type TipoDeConteudo = "texto" | "imagem" | "link_externo" | "video" | "arquivo";
export type AutoriaDoConteudo = "propria" | "terceiro";

export interface ConteudoDaMissao {
  id: string;
  missao_id: string;
  ordem: number;
  tipo: TipoDeConteudo;
  corpo: string | null;
  endereco: string | null;
  referencia: string | null;
  tamanho: number | null;
  autoria: AutoriaDoConteudo;
  fonte: string | null;
}

export interface BibliografiaDaMissao {
  id: string;
  missao_id: string;
  titulo: string;
  capitulo: string;
  item_patrimonial_id: string | null;
  // Só a leitura pública (`GET /trilhas/{id}`) devolve os dois — a criação
  // nunca aceita nem grava nenhum (`RF-09-22`, `RF-09-23`).
  disponivel?: boolean | null;
  apoiador_nome?: string | null;
}

export type TipoDeDesafioDeDesbloqueio = "quiz" | "pratico";

// Os seis níveis do território, nessa ordem de contenção (`RF-08-04`,
// PRD-08 §8) — os mesmos da App 03, aqui só para a granularidade exigida do
// desafio de coleta.
export type NivelDoLocal = "comunidade" | "bairro" | "rua" | "condominio" | "bloco" | "quadra";

export const NIVEIS_DO_LOCAL: NivelDoLocal[] = [
  "comunidade",
  "bairro",
  "rua",
  "condominio",
  "bloco",
  "quadra",
];

export type CadenciaDeColeta = "diaria" | "semanal" | "mensal";

export interface DesafioDeColetaDaMissao {
  id: string;
  tipo_de_coleta_id: string;
  cadencia: CadenciaDeColeta;
  vigencia_inicio: string;
  vigencia_fim: string;
  granularidade_exigida: NivelDoLocal;
  registros_que_pontuam_por_periodo: number;
}

export interface MissaoDaTrilha {
  id: string;
  trilha_id: string;
  titulo: string;
  posicao: number;
  nivel_de_dificuldade: number;
  obrigatoria: boolean;
  e_sondagem: boolean;
  etapa_do_ciclo: EtapaDoCiclo;
  cadencia_de_retomada: number[] | null;
  // O desafio que abre a missão seguinte — fato do Guerreiro(a) na trilha,
  // nunca da equipe; declarar de novo substitui o anterior (`RF-09-26`,
  // `RF-09-117`, documento 11 §2.2). Só a resposta de `declararDesafioDe
  // Desbloqueio` traz esses quatro campos, com a alternativa correta — a
  // mesma resposta nunca sai de `GET /trilhas/minhas` nem da leitura
  // pública, para que a resposta certa não vaze ao Guerreiro(a).
  tipo_do_desafio_de_desbloqueio?: TipoDeDesafioDeDesbloqueio;
  desafio_de_desbloqueio_enunciado?: string;
  desafio_de_desbloqueio_alternativas?: string[] | null;
  desafio_de_desbloqueio_alternativa_correta?: number | null;
  atividades: AtividadeDaMissao[];
  // As etiquetas **próprias** da missão: a leitura não cai para as da
  // trilha, ainda que a missão sem etiqueta própria responda por elas nos
  // vínculos (`RF-09-98`, `RF-01-45`).
  etiquetas_ods: EtiquetaOds[];
  // Só vem de `GET /trilhas/minhas` — a leitura pública não traz o desafio
  // de coleta (`RF-09-27`, `RF-09-28`, design — decisão 1). `undefined` é
  // "não veio desta leitura", distinto de lista vazia.
  desafios_de_coleta?: DesafioDeColetaDaMissao[];
  // Nunca vem de `GET /trilhas/minhas` — só o que foi declarado nesta
  // sessão, no mesmo padrão que `culminancia` já firma nesta aplicação.
  conteudos?: ConteudoDaMissao[];
  bibliografia?: BibliografiaDaMissao[];
}

export interface TrilhaDaLista {
  id: string;
  nome: string;
  objetivo: string;
  area_do_conhecimento: string;
  poder_id: string;
  situacao: string;
  motivo_da_situacao: string | null;
  etiquetas_ods: EtiquetaOds[];
  cobertura_ods: CoberturaOdsDaTrilha;
}

export interface TrilhaDoMestre extends TrilhaDaLista {
  missoes: MissaoDaTrilha[];
  // Nunca vem de `GET /trilhas/minhas` — só é conhecida depois que o Mestre
  // a declara nesta sessão (`POST /trilhas/{id}/culminancia` não tem par de
  // leitura, PRD-09 §9). `undefined` é "ainda não declarada nesta sessão",
  // distinto de `null`, que o núcleo nunca devolve.
  culminancia?: CulminanciaDaTrilha | null;
}

export type ModalidadeDaCulminancia = "individual" | "em_equipe";

export interface CulminanciaDaTrilha {
  id: string;
  trilha_id: string;
  descricao: string;
  modalidade: ModalidadeDaCulminancia;
  criterio_de_validacao: string;
}

// `GET /trilhas/minhas` já traz missões e atividades aninhadas — o PRD-09
// §9 não declara rota própria para nenhuma das duas (design — decisão 2).
export function listarMinhasTrilhas(token: string): Promise<TrilhaDoMestre[]> {
  return chamarNucleo<TrilhaDoMestre[]>("/v1/trilhas/minhas", { token });
}

export interface CriarTrilhaEntrada {
  nome: string;
  objetivo: string;
  area_do_conhecimento: string;
  poder_id: string;
}

export function criarTrilha(
  entrada: CriarTrilhaEntrada,
  token: string,
): Promise<TrilhaDaLista> {
  return chamarNucleo<TrilhaDaLista>("/v1/trilhas", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface CriarMissaoEntrada {
  titulo: string;
  posicao: number;
  nivel_de_dificuldade: number;
  obrigatoria: boolean;
  etapa_do_ciclo: EtapaDoCiclo;
  e_sondagem?: boolean;
}

export function criarMissao(
  idDaTrilha: string,
  entrada: CriarMissaoEntrada,
  token: string,
): Promise<MissaoDaTrilha> {
  return chamarNucleo<MissaoDaTrilha>(`/v1/trilhas/${idDaTrilha}/missoes`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface CriarAtividadeEntrada {
  titulo: string;
  descricao?: string;
  modalidade: string;
  formato: string;
  natureza: string;
  producao_esperada: string;
  aula_id?: string;
}

export function criarAtividade(
  idDaMissao: string,
  entrada: CriarAtividadeEntrada,
  token: string,
): Promise<AtividadeDaMissao> {
  return chamarNucleo<AtividadeDaMissao>(`/v1/missoes/${idDaMissao}/atividades`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// `cadenciaDeRetomada` nulo deixa a missão sem retomada — o caminho que
// `RF-09-83` exige preservar (design — decisão 4).
export function declararCadenciaDeRetomada(
  idDaMissao: string,
  cadenciaDeRetomada: number[] | null,
  token: string,
): Promise<MissaoDaTrilha> {
  return chamarNucleo<MissaoDaTrilha>(`/v1/missoes/${idDaMissao}/retomada`, {
    metodo: "POST",
    corpo: { cadencia_de_retomada: cadenciaDeRetomada },
    token,
  });
}

export interface DeclararDesafioDeDesbloqueioEntrada {
  tipo: TipoDeDesafioDeDesbloqueio;
  enunciado: string;
  alternativas?: string[] | null;
  alternativa_correta?: number | null;
}

// Só o Mestre autor declara — a posse, a exigência das quatro alternativas
// no quiz e a substituição do desafio anterior já são do núcleo
// (`RF-09-26`, `RF-09-117`).
export function declararDesafioDeDesbloqueio(
  idDaMissao: string,
  entrada: DeclararDesafioDeDesbloqueioEntrada,
  token: string,
): Promise<MissaoDaTrilha> {
  return chamarNucleo<MissaoDaTrilha>(`/v1/missoes/${idDaMissao}/desbloqueio`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface DesbloqueioPendente {
  id: string;
  guerreiro_id: string;
  guerreiro_nome: string | null;
  missao_id: string;
  missao_titulo: string;
  momento: string;
}

// As declarações de desafio prático ainda não julgadas, só das trilhas do
// Mestre autor em sessão (`RF-09-26`, `RF-09-117`).
export function listarDesbloqueiosPendentes(token: string): Promise<DesbloqueioPendente[]> {
  return chamarNucleo<DesbloqueioPendente[]>("/v1/missoes/desbloqueios-pendentes", { token });
}

// Aprovada, a missão seguinte abre para aquele Guerreiro(a); reprovada, ele
// pode declarar de novo, sem limite e sem punição (`RF-09-117`, `RN-05-20`).
export function julgarDesafioPratico(
  idDaMissao: string,
  idDoGuerreiro: string,
  aprovado: boolean,
  token: string,
): Promise<{ aprovado: boolean }> {
  return chamarNucleo<{ aprovado: boolean }>(
    `/v1/missoes/${idDaMissao}/desbloqueios/${idDoGuerreiro}/julgamento`,
    {
      metodo: "POST",
      corpo: { aprovado },
      token,
    },
  );
}

export interface DeclararCulminanciaEntrada {
  descricao: string;
  modalidade: ModalidadeDaCulminancia;
  criterio_de_validacao: string;
}

// Privativa do Mestre autor; a segunda declaração substitui a anterior, e
// não cria uma segunda culminância (`RF-09-29`, `RF-09-30`).
export function declararCulminancia(
  idDaTrilha: string,
  entrada: DeclararCulminanciaEntrada,
  token: string,
): Promise<CulminanciaDaTrilha> {
  return chamarNucleo<CulminanciaDaTrilha>(`/v1/trilhas/${idDaTrilha}/culminancia`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// Publica ou republica, a partir de rascunho ou despublicada — a mesma
// rota para as duas origens (`RF-09-05`, `RF-09-11`).
export function publicarTrilha(idDaTrilha: string, token: string): Promise<TrilhaDaLista> {
  return chamarNucleo<TrilhaDaLista>(`/v1/trilhas/${idDaTrilha}/publicacao`, {
    metodo: "POST",
    token,
  });
}

// As duas rotas recebem a **lista completa** e substituem o conjunto do
// alvo: o que estava é apagado, o que veio é gravado. Lista vazia deixa o
// alvo sem etiqueta, situação legal no Ciclo 01 (`RF-09-92`, `RF-09-93`).
export function substituirEtiquetasOdsDaTrilha(
  idDaTrilha: string,
  etiquetas: EtiquetaOdsDeclarada[],
  token: string,
): Promise<EtiquetaOds[]> {
  return chamarNucleo<EtiquetaOds[]>(`/v1/trilhas/${idDaTrilha}/ods`, {
    metodo: "POST",
    corpo: { etiquetas },
    token,
  });
}

// Escopada à missão: nunca alcança as etiquetas da trilha (`RF-09-98`).
export function substituirEtiquetasOdsDaMissao(
  idDaMissao: string,
  etiquetas: EtiquetaOdsDeclarada[],
  token: string,
): Promise<EtiquetaOds[]> {
  return chamarNucleo<EtiquetaOds[]>(`/v1/missoes/${idDaMissao}/ods`, {
    metodo: "POST",
    corpo: { etiquetas },
    token,
  });
}

export interface CriarConteudoEntrada {
  tipo: TipoDeConteudo;
  ordem: number;
  corpo?: string;
  endereco?: string;
  autoria: AutoriaDoConteudo;
  fonte?: string;
}

// A autoria estrita, a coerência de cada tipo e a fonte do terceiro já são
// do núcleo (`RF-09-14`, `RF-09-15`, `RF-09-24`).
export function criarConteudo(
  idDaMissao: string,
  entrada: CriarConteudoEntrada,
  token: string,
): Promise<ConteudoDaMissao> {
  return chamarNucleo<ConteudoDaMissao>(`/v1/missoes/${idDaMissao}/conteudos`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

interface AbrirEnvioSaida {
  endereco_da_sessao: string;
}

// Abre a sessão retomável — a recusa por formato ou por tamanho acontece
// aqui, antes de qualquer byte ser enviado (`RF-09-16` a `RF-09-19`,
// `RF-09-115`).
export function abrirEnvio(
  idDoConteudo: string,
  tipoMime: string,
  tamanhoDeclarado: number,
  token: string,
): Promise<string> {
  return chamarNucleo<AbrirEnvioSaida>(`/v1/conteudos/${idDoConteudo}/arquivo`, {
    metodo: "POST",
    corpo: { tipo_mime: tipoMime, tamanho_declarado: tamanhoDeclarado },
    token,
  }).then((saida) => saida.endereco_da_sessao);
}

// Só depois desta chamada o conteúdo passa a servir bytes — o núcleo
// consulta o armazenamento pelo tamanho real antes de gravar a referência
// (`RF-09-16`, `RF-09-17`).
export function confirmarEnvio(
  idDoConteudo: string,
  token: string,
): Promise<ConteudoDaMissao> {
  return chamarNucleo<ConteudoDaMissao>(`/v1/conteudos/${idDoConteudo}/arquivo`, {
    metodo: "PATCH",
    token,
  });
}

const TAMANHO_DA_PARTE = 5 * 1024 * 1024;

// Consulta o quanto a sessão já recebeu, sem enviar bytes — o que sustenta
// a retomada depois de recarregar a página no meio do envio (`RF-09-19`).
export async function consultarProgressoDaSessao(
  enderecoDaSessao: string,
  tamanhoDoArquivo: number,
): Promise<number> {
  const resultado = await enviarParteComProgresso(
    enderecoDaSessao,
    new Blob([]),
    `bytes */${tamanhoDoArquivo}`,
    () => {},
  );
  return resultado.bytesRecebidos;
}

// Envia o arquivo em partes, retomando de `posicaoInicial` — uma queda de
// rede no meio de uma parte é resolvida enviando a mesma parte de novo, e
// uma queda entre partes é resolvida por `consultarProgressoDaSessao`
// antes de chamar esta função de novo (`RF-09-19`).
export async function enviarArquivo(
  enderecoDaSessao: string,
  arquivo: File,
  aoProgredir: (bytesEnviados: number, total: number) => void,
  posicaoInicial = 0,
): Promise<void> {
  let posicao = posicaoInicial;
  const total = arquivo.size;
  while (posicao < total) {
    const fim = Math.min(posicao + TAMANHO_DA_PARTE, total);
    const parte = arquivo.slice(posicao, fim);
    const resultado = await enviarParteComProgresso(
      enderecoDaSessao,
      parte,
      `bytes ${posicao}-${fim - 1}/${total}`,
      (bytesDaParte) => aoProgredir(posicao + bytesDaParte, total),
    );
    posicao = resultado.bytesRecebidos;
    aoProgredir(posicao, total);
  }
}

export interface CriarBibliografiaEntrada {
  titulo: string;
  capitulo: string;
  item_patrimonial_id?: string;
}

// O exemplar é opcional; o Apoiador creditado nunca é digitado — deriva na
// leitura pública (`RF-09-21` a `RF-09-23`).
export function criarBibliografia(
  idDaMissao: string,
  entrada: CriarBibliografiaEntrada,
  token: string,
): Promise<BibliografiaDaMissao> {
  return chamarNucleo<BibliografiaDaMissao>(`/v1/missoes/${idDaMissao}/bibliografia`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface ExemplarDoAcervo {
  id: string;
  titulo: string;
  numero_de_tombo: string;
  ponto_de_apoio_id: string;
}

// Alimenta só o seletor da bibliografia — a gestão completa do acervo é do
// PRD-07 (`RF-09-21`).
export function listarAcervo(token: string): Promise<ExemplarDoAcervo[]> {
  return chamarNucleo<ExemplarDoAcervo[]>("/v1/itens-patrimoniais", { token });
}

// A pré-visualização usa a mesma leitura pública que a App 05 vai consumir
// — se a tela do Guerreiro(a) divergir depois, a pré-visualização
// acompanha o contrato, não a tela (`RF-09-25`, design — Risks).
export function obterTrilhaPublica(
  idDaTrilha: string,
  token: string,
): Promise<TrilhaDoMestre> {
  return chamarNucleo<TrilhaDoMestre>(`/v1/trilhas/${idDaTrilha}`, { token });
}

export type FormaDeRegistroDeColeta = "numero" | "foto" | "video";

export interface TipoDeColeta {
  id: string;
  nome: string;
  forma_de_registro: FormaDeRegistroDeColeta;
  unidade: string | null;
  faixa_minima: number | null;
  faixa_maxima: number | null;
  ativo: boolean;
}

interface PaginaDeTiposDeColeta {
  itens: TipoDeColeta[];
  proximo_cursor: string | null;
}

// Só para o Mestre escolher o tipo ao declarar o desafio — o cadastro do
// catálogo é privativo do Admin (`RF-09-27`, `RF-08-05`).
export function listarTiposDeColeta(token: string): Promise<TipoDeColeta[]> {
  return chamarNucleo<PaginaDeTiposDeColeta>("/v1/tipos-de-coleta", { token }).then(
    (pagina) => pagina.itens,
  );
}

export interface CriarDesafioDeColetaEntrada {
  missao_id: string;
  tipo_de_coleta_id: string;
  cadencia: CadenciaDeColeta;
  vigencia_inicio: string;
  vigencia_fim: string;
  granularidade_exigida: NivelDoLocal;
  registros_que_pontuam_por_periodo: number;
}

// A escrita é a rota do PRD-08 já existente — nenhuma regra de coleta nasce
// na App 09 (`RF-09-27`, `RF-09-28`).
export function criarDesafioDeColeta(
  entrada: CriarDesafioDeColetaEntrada,
  token: string,
): Promise<DesafioDeColetaDaMissao> {
  return chamarNucleo<DesafioDeColetaDaMissao>("/v1/desafios-de-coleta", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}
